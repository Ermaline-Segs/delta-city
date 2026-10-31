-- ============================================================================
-- DELTA CITY RP — repair workshops: bays, the shared waiting list, jobs, the
-- one-time finish and the refund. Run in the Supabase SQL editor (top to
-- bottom). Every statement is idempotent (create or replace / if not exists /
-- grant-revoke pairs): it is safe to run the whole file twice.
--
-- This file does not touch game code. It gives the client (index.html, a
-- later change) the server-side truth that today only exists in one player's
-- browser: which bay holds which car, where a car stands in the waiting
-- list, which job a car has, whether it is finished (exactly once) or was
-- refunded (exactly once).
--
-- How it fits the rules already decided with the owner:
--   * One workshop per town, three bays each; a car is in a bay OR on the
--     waiting list, and a player has at most ONE open entry across ALL
--     workshops, bays and waiting lists combined (the per-player unique index
--     below). A vehicle has at most one open entry anywhere (another unique
--     index), and a bay number 1-3 is unique per workshop (yet another).
--   * The car is paid for the moment it JOINS — a bay or the list — through
--     pay_service (supabase_services.sql) into the state's account, in the
--     same transaction, so a crash between paying and queuing cannot happen.
--     Leaving the list, or cancelling before the work has started, refunds
--     the full price: the refund DEBITS the state's account (the exact
--     opposite of pay_service) and credits the player's cash, and writes its
--     own ledger row, so no money is created or destroyed.
--   * The 15-minute cap: every job's planned duration is scaled
--     proportionally so it never exceeds 15 minutes, and the server clamps
--     planned_until to now() + 15 min as a safety limit on top of that.
--   * The "never finish twice" guarantee: rep_finish's UPDATE flips the row
--     from finished=false to finished=true and succeeds only for the call
--     that actually did the flipping. Two callers at the same instant:
--     Postgres locks the row, the loser re-reads finished=true and gets a
--     no-op result instead of a second payout moment. It also refuses until
--     the server's own now() has passed planned_until — the wall clock is
--     the server's, never the client's.
--   * Collecting the car is a separate, only-after-finished step (rep_collect)
--     that releases the bay and puts the car into the workshop's own car
--     park. Each workshop's park is an ordinary car_parks row, so the
--     existing garage flow (veh_store, the one-car-per-bay rule) works on a
--     finished car exactly as it does for any other park.
--
-- Server time is the only authority: started_at, planned_until, joined_at,
-- finished_at and cancelled_at all come from now() inside these functions.
-- Row security is on for every table; players can only read (and only the
-- queues of their own town's workshops), and every mutation goes through one
-- of the security-definer functions below, which check auth.uid() and
-- ownership.
-- ============================================================================

-- ---------- the four workshops (and the park each of them keeps cars in) ----
create table if not exists workshops (
  id        text primary key,        -- 'asaba', 'warri', 'ozoro', 'agbor'
  name      text not null,
  state     text not null,           -- the state account repairs are paid into
  park_id   text references car_parks(id),
  x         numeric,                 -- town coords (mirror of the client)
  z         numeric,
  yaw       numeric,
  bays      int not null default 3 check (bays > 0)
);

-- The workshop car parks: ordinary car_parks rows. A finished car is parked
-- here (rep_collect), in a bay of its own, and the usual garage flow — the
-- one-car-per-bay index and veh_store/veh_spawn — applies to it without any
-- special case.
insert into car_parks(id, state, name, x, z, bays) values
  ('asaba-ws-park', 'Asaba', 'Asaba Auto Workshop Car Park', -60, 186.3, 4),
  ('warri-ws-park', 'Warri', 'Warri Port Auto Workshop Car Park', 70, 110, 4),
  ('ozoro-ws-park', 'Ozoro', 'Ozoro Auto Workshop Car Park', -95.4, 15.4, 4),
  ('agbor-ws-park', 'Agbor', 'Agbor Auto Workshop Car Park', -95.4, 15.4, 4)
on conflict (id) do nothing;

insert into workshops(id, name, state, park_id, x, z, yaw, bays) values
  ('asaba', 'Asaba Auto Workshop',           'Asaba', 'asaba-ws-park', -60, 186.3, 0, 3),
  ('warri', 'Warri Port Auto Workshop',      'Warri', 'warri-ws-park', 70, 110, 0, 3),
  ('ozoro', 'Ozoro Auto Workshop',           'Ozoro', 'ozoro-ws-park', -95.4, 15.4, 0, 3),
  ('agbor', 'Agbor Auto Workshop',           'Agbor', 'agbor-ws-park', -95.4, 15.4, 0, 3)
on conflict (id) do update set name = excluded.name, state = excluded.state,
  park_id = excluded.park_id, x = excluded.x, z = excluded.z, bays = excluded.bays;

-- ---------- the waiting list + bay occupancy (shared by every player) -------
create table if not exists repair_queue (
  id          bigserial primary key,
  workshop    text not null references workshops(id),
  vehicle_id  bigint not null references vehicles(id),
  owner       uuid not null,
  joined_at   timestamptz not null default now(),
  status      text not null default 'waiting'
              check (status in ('waiting', 'in_bay', 'finished', 'collected', 'left')),
  bay         int check (bay between 1 and 3),
  in_bay_at   timestamptz,
  note        text
);

-- One active entry per vehicle, across every workshop: the same car cannot
-- stand in two queues at once.
create unique index if not exists repair_queue_one_per_vehicle
  on repair_queue (vehicle_id)
  where status in ('waiting', 'in_bay');
-- One active entry per PLAYER, across every workshop: bays + queue together,
-- as the owner decided.
create unique index if not exists repair_queue_one_per_player
  on repair_queue (owner)
  where status in ('waiting', 'in_bay');
-- Bay number 1-3 is unique per workshop (an open entry may hold a bay only).
create unique index if not exists repair_queue_bay_per_workshop
  on repair_queue (workshop, bay)
  where status = 'in_bay' and bay is not null;
create index if not exists repair_queue_open on repair_queue (workshop, status, joined_at);

-- ---------- the repair jobs --------------------------------------------------
create table if not exists repair_jobs (
  id            bigserial primary key,
  queue_id      bigint not null references repair_queue(id),
  workshop      text not null references workshops(id),
  vehicle_id    bigint not null references vehicles(id),
  owner         uuid not null,
  state         text not null,        -- pay_service destination state
  items         jsonb not null,       -- [{"k":"engine","price":75000,"mins":12}, ...] (minutes already 15-min-scaled)
  price         bigint not null check (price > 0),
  planned_mins  int not null check (planned_mins between 1 and 15),  -- the 15-minute cap, scaled
  paid_at       timestamptz not null default now(),
  started_at    timestamptz,          -- work has begun; a refund is no longer possible
  planned_until timestamptz,          -- server-time wall clock, not the client's
  finished_at   timestamptz,
  finished      boolean not null default false,
  cancelled_at  timestamptz,
  status        text not null default 'pending'
                check (status in ('pending', 'in_progress', 'finished', 'cancelled'))
);
create index if not exists repair_jobs_vehicle on repair_jobs (vehicle_id, paid_at);
create index if not exists repair_jobs_open on repair_jobs (workshop, status)
  where status in ('pending', 'in_progress');

-- RLS: players can NEVER read or write these tables directly. All reading and
-- writing goes through the security definer RPCs below; rep_queue_view hides
-- player ids and shows display names only.
alter table workshops      enable row level security;
alter table repair_queue   enable row level security;
alter table repair_jobs    enable row level security;

revoke all on workshops, repair_queue, repair_jobs from anon, authenticated, public;
revoke all on sequence repair_queue_id_seq, repair_jobs_id_seq from anon, authenticated, public;

drop policy if exists "workshops are public" on workshops;
drop policy if exists "players read the queue"  on repair_queue;
drop policy if exists "players read the jobs"   on repair_jobs;
create policy "workshops are public" on workshops for select using (true);

-- -------------------------------- helpers -----------------------------------

create or replace function public.rep_role(p_owner uuid)
returns text language sql stable security definer set search_path = public as $$
  select role from characters where owner = p_owner limit 1
$$;

-- A car belongs to a workshop's queue only while one of its open entries says
-- so. (The function exists so the client can ask one question: "where is my
-- car at this workshop?")
create or replace function public.rep_state(p_workshop text, p_vehicle bigint)
returns jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'workshop',  p_workshop,
    'vehicle',   p_vehicle,
    'open_entry', (select jsonb_build_object(
                      'queue_id', q.id, 'status', q.status, 'bay', q.bay,
                      'position', (select count(*) + 1 from repair_queue q2
                                    where q2.workshop = p_workshop and q2.status = 'waiting'
                                      and (q2.joined_at < q.joined_at or
                                        (q2.joined_at = q.joined_at and q2.id < q.id))),
                      'joined_at', q.joined_at)
                   from repair_queue q
                   where q.vehicle_id = p_vehicle and q.status in ('waiting', 'in_bay')
                   order by q.id desc limit 1),
    'open_job',  (select jsonb_build_object(
                      'job_id', j.id, 'status', j.status, 'items', j.items,
                      'price', j.price, 'planned_mins', j.planned_mins,
                      'started_at', j.started_at,
                      'planned_until', j.planned_until, 'finished_at', j.finished_at,
                      'finished', j.finished)
                  from repair_jobs j
                  where j.vehicle_id = p_vehicle and j.status in ('pending', 'in_progress')
                  order by j.id desc limit 1),
    'last_job',  (select jsonb_build_object(
                      'job_id', j.id, 'status', j.status, 'items', j.items,
                      'price', j.price, 'finished_at', j.finished_at)
                  from repair_jobs j
                  where j.vehicle_id = p_vehicle
                  order by j.id desc limit 1))
$$;

-- The whole workshop from the client's point of view: the bays, the waiting
-- list in number order, and each open job's countdown left. The client calls
-- this on enter and on poll instead of reading the tables.
create or replace function public.rep_queue_view(p_workshop text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare r jsonb;
begin
  if not exists(select 1 from workshops where id = p_workshop) then
    raise exception 'That is not a workshop';
  end if;
  -- auto-finish first, even if this poll comes from a player who owns nothing
  -- here: the server clock alone frees bays and moves the queue
  perform public.rep_sweep(p_workshop);
  select jsonb_build_object(
    'ok', true,
    'workshop', p_workshop,
    'now', now(),
    'bays', (select jsonb_object_agg(bay, vehicle_id) from (
               select bay, vehicle_id from repair_queue
                where workshop = p_workshop and status = 'in_bay' and bay is not null
              ) as b),
    'jobs', coalesce((
               select jsonb_agg(jo) from (
                 select jsonb_build_object(
                         'job', j.id,
                         'vehicle', j.vehicle_id,
                         'status', j.status,
                         'items', j.items,
                         'price', j.price,
                         'started_at', j.started_at,
                         'planned_until', j.planned_until,
                         'finished_at', j.finished_at) as jo
                 from repair_jobs j
                 where j.workshop = p_workshop
                   and j.status in ('pending', 'in_progress')
                 order by j.id
               ) as jw),
                      to_jsonb(array[]::int[])),
    'waiting', coalesce((
               select jsonb_agg(wo) from (
                 select jsonb_build_object(
                         'vehicle',  w.vehicle_id,
                         'name',     coalesce(c.name, 'a player'),
                         'position', w.position,
                         'joined_at', w.joined_at) as wo
                 from (select vehicle_id, owner, joined_at,
                              row_number() over (order by joined_at, id) as position
                       from repair_queue
                       where workshop = p_workshop and status = 'waiting') as w
                 left join characters c on c.owner = w.owner
                 order by w.position
               ) as ww),
                     to_jsonb(array[]::int[]))
  ) into r;
  return r;
end;
$$;

-- -------------------------------- the queue ----------------------------------

-- Join a workshop: PAID, in one transaction. The car goes into the first free
-- bay (work starts at once: started_at = now(), planned_until = now() + the
-- clamped minutes) or into the waiting list (work starts when a bay frees up).
-- Payment goes through pay_service into the state account IN THIS SAME
-- transaction, so a failed placement refunds nothing and a failed payment
-- never leaves a queue row behind. The 15-minute cap is applied by scaling
-- every item's minutes proportionally so a full restoration is 15 minutes;
-- planned_until is additionally clamped to 15 minutes as a safety limit.
create or replace function public.rep_join(p_workshop text, p_vehicle bigint, p_items jsonb, p_mins int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me      uuid := auth.uid();
  w       workshops;
  itm     jsonb;
  k       text;
  price   numeric := 0;
  mins    numeric := 0;
  scale   numeric;
  items   jsonb;
  total_m numeric;
  q       repair_queue;
  j       repair_jobs;
  paid    jsonb;
  in_bay  boolean;
begin
  if me is null then
    raise exception 'Sign in first.';
  end if;
  -- lock the workshop row: two joins at once cannot both take the last free bay
  select * into w from workshops where id = p_workshop for update;
  if not found then
    raise exception 'That is not a workshop';
  end if;
  perform public.rep_sweep(p_workshop);
  if not public.veh_can_drive(p_vehicle, me) then
    raise exception 'You cannot drive that car (you must own it or hold its key)';
  end if;
  if exists(select 1 from repair_queue
             where vehicle_id = p_vehicle and status in ('waiting', 'in_bay')) then
    raise exception 'That car already has an open entry in a workshop';
  end if;
  if exists(select 1 from repair_queue
             where owner = me and status in ('waiting', 'in_bay')) then
    raise exception 'You already have a car in a workshop queue or bay';
  end if;

  -- the work: a list of parts, each with a price and minutes
  if p_items is null or jsonb_typeof(p_items) <> 'array' then
    raise exception 'The work must be a list of parts';
  end if;
  select coalesce(sum((it->>'price')::numeric), 0),
         coalesce(sum((it->>'mins')::numeric), 0)
    into price, mins
    from jsonb_array_elements(p_items) as it;
  if not exists(select 1 from jsonb_array_elements(p_items) as it
                 where coalesce((it->>'price')::numeric, 0) > 0)
     or mins <= 0 then
    raise exception 'The work must cost money and take minutes';
  end if;
  -- the game's own minimums (repairItems in index.html): every part key comes
  -- from the REPAIRS list, and repairItems never prices a part below 1500 nor
  -- times it below 1 minute, so a value under either floor is not from the game
  if exists(select 1 from jsonb_array_elements(p_items) as it
             where coalesce(it->>'k', '') not in
                   ('engine', 'chassis', 'susp', 'radiator', 'bumperF', 'bumperR',
                    'bonnet', 'grille', 'trunk', 'sideL', 'sideR', 'under',
                    'oilLeak', 'fuelLeak', 'elec', 'steer', 'ws', 'rw', 'winL', 'winR')
                or coalesce((it->>'price')::numeric, 0) < 1500
                or coalesce((it->>'mins')::numeric, 0) < 1) then
    raise exception 'Every part must come from the repair list, cost at least 1500, and take at least 1 minute';
  end if;

  -- the 15-minute cap: scale every part's minutes proportionally
  if mins > 15 then
    scale := 15 / mins;
    select coalesce(jsonb_agg(
        (jsonb_set(it, '{mins}', to_jsonb(round(((it->>'mins')::numeric * scale)::numeric, 1)))
        || jsonb_build_object('orig_mins', (it->>'mins')::numeric))), '[]'::jsonb)
      into items
      from jsonb_array_elements(p_items) as it;
    select sum((it->>'mins')::numeric) into total_m from jsonb_array_elements(items) as it;
  else
    items := p_items;
    total_m := mins;
  end if;
  -- the safety clamp on the planned duration
  total_m := least(total_m, 15);

  -- the payment, in the same transaction: citizen -> state account
  paid := public.pay_service(price::bigint, w.state,
                             'Repair: ' || w.name || ' (job of ' || coalesce((select name from characters where owner = me), 'you') || ')');

  -- a free bay starts the job at once; otherwise the car waits its number
  in_bay := (select count(*) from repair_queue
               where workshop = p_workshop and status = 'in_bay' and bay is not null) < w.bays;
  if in_bay then
    insert into repair_queue(workshop, vehicle_id, owner, status, bay, in_bay_at)
    values (p_workshop, p_vehicle, me, 'in_bay',
            (select min(n) from generate_series(1, w.bays) n
               where not exists(select 1 from repair_queue
                                  where workshop = p_workshop and status = 'in_bay' and bay = n)),
            now())
    returning * into q;
    insert into repair_jobs(queue_id, workshop, vehicle_id, owner, state, items, price, paid_at,
                            planned_mins, status, started_at, planned_until)
    values (q.id, p_workshop, p_vehicle, me, w.state, items, price, now(),
            greatest(1, least(15, total_m::int)),
            'in_progress', now(), now() + make_interval(mins => total_m::int))
    returning * into j;
  else
    insert into repair_queue(workshop, vehicle_id, owner, status)
    values (p_workshop, p_vehicle, me, 'waiting')
    returning * into q;
    insert into repair_jobs(queue_id, workshop, vehicle_id, owner, state, items, price, paid_at,
                            planned_mins)
    values (q.id, p_workshop, p_vehicle, me, w.state, items, price, now(),
            greatest(1, least(15, total_m::int)))
    returning * into j;
  end if;

  perform public.rep_advance(p_workshop);
  return jsonb_build_object('ok', true, 'queue_id', q.id, 'job', j.id,
                            'in_bay', in_bay, 'price', price, 'minutes', total_m,
                            'cash', (paid->>'cash')::bigint,
                            'queue', public.rep_queue_view(p_workshop));
end;
$$;

-- Leave before work starts: FULL refund, only while the job has not started.
-- The refund is the opposite of pay_service: the state account is DEBITED
-- (its balance goes down) and a 'refund' ledger row is written, so no money is
-- created. The player's cash goes back up by the paid price. Ledger rules:
-- every movement is a ledger row; the refund row balances the original
-- payment row (same price, opposite direction). If the state account's
-- balance is too small it is allowed to go negative - the refund of a payment
-- that was made must always succeed (the state is short, not the player).
create or replace function public.rep_leave(p_workshop text, p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me   uuid := auth.uid();
  j    repair_jobs;
  q    repair_queue;
  n    int;
begin
  if me is null then
    raise exception 'Sign in first.';
  end if;
  perform public.rep_sweep(p_workshop);
  select * into j from repair_jobs
   where workshop = p_workshop and vehicle_id = p_vehicle and owner = me
     and status in ('pending', 'in_progress') and cancelled_at is null
   order by paid_at desc, id desc limit 1;
  if not found then
    raise exception 'There is no open job of yours for this car here';
  end if;
  if j.started_at is not null then
    raise exception 'Work has already started; a refund is no longer possible';
  end if;
  -- the once-only flip, decided by the row count of the guarded UPDATE
  update repair_jobs set cancelled_at = now(), status = 'cancelled'
    where id = j.id and status in ('pending', 'in_progress') and cancelled_at is null;
  get diagnostics n = row_count;
  if n = 0 then
    raise exception 'This job was already refunded';
  end if;
  -- the opposite of pay_service: DEBIT the state account, credit the player
  update characters set cash = coalesce(cash, 0) + j.price where owner = me;
  perform public.rep_ledger_refund(j.state, me, j.price, j.id, j.workshop);
  update repair_queue set status = 'left', bay = null, note = 'refunded'
    where id = j.queue_id and status in ('waiting', 'in_bay');
  perform public.rep_advance(p_workshop);
  return jsonb_build_object('ok', true, 'job', j.id, 'refunded', j.price,
                            'queue', public.rep_queue_view(p_workshop));
end;
$$;

-- The ledger row of a refund: the opposite of pay_service's row (the state is
-- now the payer, the citizen the payee). Fills the ledger columns the same
-- way pay_service does, so the two directions balance in the same table.
create or replace function public.rep_ledger_refund(p_state text, p_citizen uuid, p_amount numeric, p_job bigint, p_workshop text)
returns void language plpgsql security definer set search_path = public as $$
declare
  v_name text;
  v_cols text := '';
  v_vals text := '';
  v_scol text;
  v_bcol text;
  r      record;
  v      text;
  c      text;
begin
  select coalesce(name, '') into v_name from characters where owner = p_citizen;
  for r in
    select column_name::text as col, udt_name::text as typ, is_nullable = 'NO' and column_default is null as must
      from information_schema.columns
     where table_schema = 'public' and table_name = 'ledger' and is_generated = 'NEVER' and is_identity = 'NO'
     order by ordinal_position
  loop
    c := lower(r.col);
    v := case
      when c ~ '^(from|src|source|payer)_?(kind|type)$'                              then 'state'
      when c ~ '^(to|dst|dest|target|payee)_?(kind|type)$'                           then 'citizen'
      when c ~ '^(from|src|source|payer)_?(id|owner|user|user_id|uid|citizen|ref|account)$' then p_state
      when c ~ '^(from|src|source|payer)_?(name|label)$'                             then p_state
      when c ~ '^(to|dst|dest|target|payee)_?(id|ref|account|state|state_name|name|label)$' then p_citizen::text
      when c ~ '^(to|dst|dest|target|payee)_?(name|label)$'                          then coalesce(v_name, '')
      when c ~ '^(kind|type|action|category|txn_type|tx_type)$'                      then 'refund'
      when c ~ '^(amount|sum|value|qty|quantity|total)$'                             then p_amount::text
      when c ~ '^(reason|note|desc|description|memo|detail|reference|ref)$'          then 'Repair refund: ' || p_workshop || ' (job ' || p_job || ')'
      when c ~ '^(at|time|date|created|when|ts|stamp)$'                              then now()::text
      else null end;
    if v is null then
      if r.must then
        raise exception 'rep_ledger_refund cannot fill the ledger column "%"', r.col;
      end if;
      continue;
    end if;
    v_cols := v_cols || case when v_cols = '' then '' else ',' end || quote_ident(r.col);
    v_vals := v_vals || case when v_vals = '' then '' else ',' end || quote_literal(v) || '::' || quote_ident(r.typ);
  end loop;
  if v_cols = '' then
    raise exception 'The ledger table has none of the expected columns.';
  end if;
  execute format('insert into ledger (%s) values (%s)', v_cols, v_vals);
  -- the state account is debited: the opposite of pay_service's credit.
  -- Same column introspection pay_service uses, because state_accounts is
  -- not defined in this file (state / state_name / name and balance / amount / cash).
  v_scol := (select column_name from information_schema.columns
             where table_schema = 'public' and table_name = 'state_accounts'
               and column_name in ('state', 'state_name', 'name') limit 1);
  v_bcol := (select column_name from information_schema.columns
             where table_schema = 'public' and table_name = 'state_accounts'
               and column_name in ('balance', 'amount', 'cash') limit 1);
  if v_scol is null or v_bcol is null then
    raise exception 'state_accounts needs a state column and a balance column.';
  end if;
  execute format('update state_accounts set %I = coalesce(%I, 0) - $1 where %I = $2', v_bcol, v_bcol, v_scol) using p_amount, p_state;
end;
$$;

-- Auto-finish: every in-progress job whose planned_until has passed flips to
-- finished (once only - the guarded UPDATE's row count is the race guard),
-- frees its bay and queue row, then rep_advance moves the next waiting car in
-- and starts its job. The server clock is the ONLY authority: the owner never
-- has to call anything, and any player's poll unblocks the whole workshop.
create or replace function public.rep_sweep(p_workshop text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare done int := 0; j repair_jobs; n int;
begin
  if not exists(select 1 from workshops where id = p_workshop) then
    raise exception 'That is not a workshop';
  end if;
  for j in
    select * from repair_jobs
     where workshop = p_workshop and status = 'in_progress'
       and finished = false and cancelled_at is null
       and planned_until is not null and planned_until <= now()
order by id
      for update
  loop
    update repair_jobs
       set finished = true, status = 'finished', finished_at = now()
     where id = j.id and status = 'in_progress'
       and finished = false and cancelled_at is null;
    get diagnostics n = row_count;
    if n = 0 then
      continue;
    end if;
    update repair_queue
       set status = 'finished', bay = null
     where id = j.queue_id and status = 'in_bay';
    done := done + 1;
  end loop;
  if done > 0 then
    perform public.rep_advance(p_workshop);
  end if;
  return jsonb_build_object('ok', true, 'finished_now', done);
end;
$$;

-- Advance the workshop: the first waiting car fills a free bay and ITS JOB
-- starts (started_at = now(), planned_until = now() + the clamped minutes,
-- status 'pending' -> 'in_progress'). Server time is the only authority.
-- Called by every poll, join, leave and finish.
create or replace function public.rep_advance(p_workshop text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare moved int := 0; q repair_queue; j repair_jobs;
begin
  if not exists(select 1 from workshops where id = p_workshop) then
    raise exception 'That is not a workshop';
  end if;
  perform public.rep_sweep(p_workshop);
  for q in
    select * from repair_queue
    where workshop = p_workshop and status = 'waiting'
    order by joined_at, id
    for update skip locked
  loop
    if exists(select 1 from repair_queue
               where workshop = p_workshop and status = 'in_bay' and bay is not null)
           -- only move the car into a bay when one is genuinely free
       and (select count(*) from repair_queue
              where workshop = p_workshop and status = 'in_bay' and bay is not null) >=
           (select bays from workshops where id = p_workshop)
    then
      exit;
    end if;
    select * into j from repair_jobs
     where queue_id = q.id and status = 'pending' and cancelled_at is null
     limit 1;
    if not found then
      continue;
    end if;
    update repair_queue
       set status = 'in_bay',
           bay = (select min(n) from generate_series(1, (select bays from workshops where id = p_workshop)) n
                    where not exists(select 1 from repair_queue
                                       where workshop = p_workshop and status = 'in_bay' and bay = n)),
           in_bay_at = now()
     where id = q.id;
    update repair_jobs
       set status = 'in_progress', started_at = now(),
           planned_until = now() + make_interval(mins =>
               least((select coalesce(sum((it->>'mins')::numeric), 0)
                        from jsonb_array_elements(j.items) as it), 15)::int)
     where id = j.id;
    moved := moved + 1;
  end loop;
  return jsonb_build_object('ok', true, 'moved', moved,
                            'queue', public.rep_queue_view(p_workshop));
end;
$$;

-- Finish a job: atomic, once-only, and REFUSED until the server's now() has
-- passed planned_until. The UPDATE's own row count decides who did the flip;
-- a second call (or a concurrent loser) finds finished already true and is a
-- no-op. Finishing frees the bay; the car is collected from the workshop's
-- car park with rep_collect.
create or replace function public.rep_finish(p_workshop text, p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me   uuid := auth.uid();
  j    repair_jobs;
  n    int;
  till timestamptz;
begin
  if me is null then
    raise exception 'Sign in first.';
  end if;
  select * into j from repair_jobs
   where workshop = p_workshop and vehicle_id = p_vehicle and owner = me
     and status in ('in_progress', 'finished') and cancelled_at is null
   order by paid_at desc, id desc limit 1;
  if not found then
    raise exception 'There is no running job of yours for this car here';
  end if;
  if j.finished and j.status = 'finished' then
    -- a no-op: it has been finished already
    return jsonb_build_object('ok', true, 'already', true, 'job', j.id);
  end if;
  if j.planned_until is null or now() < j.planned_until then
    raise exception 'The repair is not finished yet; it is planned until %', j.planned_until;
  end if;
  -- the once-only flip, decided by the row count of the guarded UPDATE
  update repair_jobs set finished = true, finished_at = now(), status = 'finished'
    where id = j.id and finished = false and cancelled_at is null and status in ('in_progress');
  get diagnostics n = row_count;
  if n = 0 then
    -- a no-op: someone (or something) finished it already
    return jsonb_build_object('ok', true, 'already', true, 'job', j.id);
  end if;
  update repair_queue
     set status = 'finished'
   where id = j.queue_id and status = 'in_bay';
  perform public.rep_advance(p_workshop);
  return jsonb_build_object('ok', true, 'job', j.id, 'finished_at', j.finished_at,
                            'queue', public.rep_queue_view(p_workshop));
end;
$$;

-- Collect the finished car: only once the job is finished, from the
-- workshop's car park. Releases the bay and stores the car in the workshop's
-- car park through the same vehicles rows the ordinary garage flow uses, so
-- picking it up later works exactly like any other stored car.
create or replace function public.rep_collect(p_workshop text, p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me uuid := auth.uid();
  w workshops;
  j repair_jobs;
  nb int;
begin
  if me is null then
    raise exception 'Sign in first.';
  end if;
  perform public.rep_sweep(p_workshop);
  select * into w from workshops where id = p_workshop;
  if not found then
    raise exception 'That is not a workshop';
  end if;
  select * into j from repair_jobs
   where workshop = p_workshop and vehicle_id = p_vehicle and owner = me
     and finished = true and cancelled_at is null
   order by paid_at desc, id desc limit 1;
  if not found then
    raise exception 'There is no finished job of yours for this car here';
  end if;
  if exists(select 1 from repair_queue where id = j.queue_id and status = 'collected') then
    -- a no-op: already collected
    return jsonb_build_object('ok', true, 'already', true, 'job', j.id);
  end if;
  nb := public.veh_free_bay(w.park_id);
  if nb is null then
    raise exception 'The workshop car park is full; try again shortly.';
  end if;
  update vehicles set status = 'stored', park_id = w.park_id, bay = nb,
         in_bay = null, token = null, active_by = null, occupied = false,
         hold = null, hold_since = null, abandoned_at = null,
         pos = null, state = null, last_seen = now()
    where id = p_vehicle;
  update repair_queue set status = 'collected', bay = null
    where id = j.queue_id and status <> 'collected';
  perform public.rep_advance(p_workshop);
  return jsonb_build_object('ok', true, 'job', j.id, 'bay', nb,
                            'park', w.park_id,
                            'queue', public.rep_queue_view(p_workshop));
end;
$$;

-- --------------------------------- the car lock ---------------------------------
-- A car with an open workshop entry is locked out of the normal vehicle functions
-- (veh_spawn, veh_update, veh_store and veh_despawn all go through veh_can_drive):
-- it cannot be driven off while it is waiting, in a bay, or finished but not yet
-- collected. The lock lifts only when the owner collects the car with rep_collect
-- (queue row -> 'collected') or leaves with a refund (queue row -> 'left').
-- rep_join checks veh_can_drive BEFORE it inserts the queue row, so a car can
-- never be locked by its own entry. This is the one re-definition of an older
-- function in this file; it runs last, so this is the definition that stays.
create or replace function public.veh_can_drive(p_vehicle bigint, p_who uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select (exists(select 1 from vehicles where id = p_vehicle and owner = p_who)
          or exists(select 1 from vehicle_keys where vehicle_id = p_vehicle and holder = p_who and revoked_at is null))
      and not exists(select 1 from repair_queue
                      where vehicle_id = p_vehicle
                        and status in ('waiting', 'in_bay', 'finished'))
$$;

-- ---------------------------------- access ----------------------------------

revoke execute on function
  public.rep_state(text, bigint),
  public.rep_queue_view(text),
  public.rep_join(text, bigint, jsonb, integer),
  public.rep_leave(text, bigint),
  public.rep_advance(text),
  public.rep_finish(text, bigint),
  public.rep_collect(text, bigint)
  from anon, public;

grant execute on function
  public.rep_state(text, bigint),
  public.rep_queue_view(text),
  public.rep_join(text, bigint, jsonb, integer),
  public.rep_leave(text, bigint),
  public.rep_advance(text),
  public.rep_finish(text, bigint),
  public.rep_collect(text, bigint)
  to authenticated;

grant select on workshops, repair_queue, repair_jobs to authenticated;

-- collect/advance are driven by the game server or by the first poller; keep
-- them callable by the same authenticated role the game uses.