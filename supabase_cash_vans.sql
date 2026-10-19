-- Delta City RP: armoured cash vans for the Central Bank's "Send to a state".
--
-- Run the whole file once in the Supabase SQL editor. Running it again is safe.
--
-- What it changes:
--   * cb_van_cfg (new): every number for the vans, in one place.
--   * cb_vans (new table): one row per van, with its amount and its stage times, worked out here on the server.
--   * cb_distribute: the money leaves the National Reserve (DCB) when the order is made, and the order is carried by
--     vans of at most K5,000,000 each. All the order's vans load side by side, leave together when the biggest is
--     loaded, arrive together, and each unloads for as long as it loaded. It refuses if the Reserve cannot cover it.
--   * cb_settle: a state is credited with a van's money once, when that van has finished unloading, under a row
--     lock (so two settles at once, reloads or repeated calls cannot pay it twice), with one ledger row per van.
--     Printing, and distributions made before this file was run, are paid minute by minute exactly as before.
--   * cb_status: also returns the vans (current ones and the last day's deliveries), the settings and the clock.
--   * cb_vans_public (new): the vans on the road for everyone's game (times and destinations, no amounts). It also
--     settles anything due, so deliveries are paid on time while anyone is playing.
--   * cb_print and cb_role are not changed.

-- every number in one place
create or replace function public.cb_van_cfg()
returns jsonb language sql immutable set search_path = public as $$
  select jsonb_build_object(
    'cap',               5000000,  -- the most one van carries, in naira
    'load_base_s',       120,      -- loading: 2 minutes for every van ...
    'load_per_million_s',120,      -- ... plus 2 minutes for every K1,000,000 in it (unloading takes the same)
    'asaba_drive_s',     40,       -- Treasury to Crestfield Bank along the roads: about 265 m at city pace
    'journey_s', jsonb_build_object('Warri', 1800, 'Ozoro', 4680, 'Agbor', 9000))   -- flight times x 6 for road travel
$$;

alter table cb_orders add column if not exists vans boolean not null default false;

create table if not exists cb_vans (
  id            bigserial primary key,
  order_id      bigint not null references cb_orders(id),
  seq           int not null,
  of_n          int not null,
  state         text not null,
  amount        bigint not null check (amount > 0),
  load_s        numeric not null,
  started_at    timestamptz not null,       -- loading begins (the order is made)
  depart_at     timestamptz not null,       -- all the order's vans leave together
  arrive_at     timestamptz not null,       -- and reach the bank together
  unload_end_at timestamptz not null,       -- this van's money is paid when its unloading ends
  delivered     boolean not null default false,
  delivered_at  timestamptz,
  unique (order_id, seq)
);
create index if not exists cb_vans_due on cb_vans (delivered, unload_end_at);
-- only the functions below (security definer) read or write the vans
alter table cb_vans enable row level security;
revoke all on cb_vans from anon, authenticated;

create or replace function public.cb_distribute(p_state text, p_amount bigint)
returns bigint language plpgsql security definer set search_path = public as $function$
declare cfg jsonb := cb_van_cfg(); cap bigint := (cfg->>'cap')::bigint; new_id bigint; have bigint; t0 timestamptz;
        n int; i int; chunk bigint; left_ bigint; ld numeric; longest numeric := 0; journey numeric; dep timestamptz; arr timestamptz;
begin
  if cb_role() not in ('bankgov', 'admin') or cb_role() is null then raise exception 'Only the Bank Governor can distribute money'; end if;
  if p_state not in ('Asaba', 'Warri', 'Ozoro', 'Agbor') then raise exception 'Unknown state'; end if;
  if p_amount is null or p_amount <= 0 then raise exception 'Enter an amount to send'; end if;
  perform cb_settle();
  select balance into have from state_accounts where state = 'DCB' for update;
  if have < p_amount then raise exception 'The National Reserve only holds K%', have; end if;
  update state_accounts set balance = balance - p_amount, updated_at = now() where state = 'DCB';
  insert into cb_orders(kind, state, amount, rate, by_owner, vans) values ('distribute', p_state, p_amount, 100000, auth.uid(), true)
    returning id, started_at into new_id, t0;
  t0 := coalesce(t0, now());
  n := ceil(p_amount::numeric / cap)::int;
  -- the vans leave together when the biggest one is loaded (the first carries the most)
  longest := (cfg->>'load_base_s')::numeric + (cfg->>'load_per_million_s')::numeric * least(cap, p_amount) / 1000000.0;
  journey := case when p_state = 'Asaba' then (cfg->>'asaba_drive_s')::numeric else (cfg->'journey_s'->>p_state)::numeric end;
  dep := t0 + make_interval(secs => longest);
  arr := dep + make_interval(secs => journey);
  left_ := p_amount;
  for i in 1..n loop
    chunk := least(cap, left_);
    left_ := left_ - chunk;
    ld := (cfg->>'load_base_s')::numeric + (cfg->>'load_per_million_s')::numeric * chunk / 1000000.0;
    insert into cb_vans(order_id, seq, of_n, state, amount, load_s, started_at, depart_at, arrive_at, unload_end_at)
      values (new_id, i, n, p_state, chunk, ld, t0, dep, arr, arr + make_interval(secs => ld));
  end loop;
  return new_id;
end $function$;

create or replace function public.cb_settle()
returns void language plpgsql security definer set search_path = public as $function$
declare o record; v record; due bigint; delta bigint;
begin
  -- printing, and distributions made before the vans: paid minute by minute, as before
  for o in select * from cb_orders where not done and not vans order by id for update loop
    due := least(o.amount, floor(extract(epoch from (now() - o.started_at)) / 60.0 * o.rate)::bigint);
    delta := due - o.settled;
    if delta > 0 then
      if o.kind = 'print' then
        update state_accounts set balance = balance + delta, updated_at = now() where state = 'DCB';
      else
        update state_accounts set balance = balance + delta, updated_at = now() where state = o.state;
      end if;
      update cb_orders set settled = due, done = (due = o.amount) where id = o.id;
      if due = o.amount then
        insert into ledger(from_kind, from_id, to_kind, to_id, amount, reason)
          values (case when o.kind = 'print' then 'mint' else 'reserve' end, 'DCB',
                  case when o.kind = 'print' then 'reserve' else 'state' end, coalesce(o.state, 'DCB'), o.amount,
                  case when o.kind = 'print' then 'Currency printed (order ' || o.id || ')' else 'Distributed to ' || o.state || ' (order ' || o.id || ')' end);
      end if;
    end if;
  end loop;
  -- cash vans: each van that has finished unloading is paid to its state once. A van being settled by someone else at
  -- the same moment is locked; when the lock is released it is no longer "not delivered", so it is skipped here.
  for v in select * from cb_vans where not delivered and unload_end_at <= now() order by unload_end_at, id for update loop
    update state_accounts set balance = balance + v.amount, updated_at = now() where state = v.state;
    update cb_vans set delivered = true, delivered_at = now() where id = v.id;
    update cb_orders set settled = settled + v.amount, done = (settled + v.amount >= amount) where id = v.order_id;
    insert into ledger(from_kind, from_id, to_kind, to_id, amount, reason)
      values ('reserve', 'DCB', 'state', v.state, v.amount,
              'Cash van ' || v.seq || ' of ' || v.of_n || ' delivered to ' || v.state || ' (order ' || v.order_id || ')');
  end loop;
end $function$;

create or replace function public.cb_status()
returns jsonb language plpgsql security definer set search_path = public as $function$
begin
  if cb_role() not in ('bankgov', 'minister', 'admin') or cb_role() is null then raise exception 'Only the Bank Governor and the Minister of Finance can view the reserves'; end if;
  perform cb_settle();
  return jsonb_build_object(
    'now',     now(),
    'cfg',     cb_van_cfg(),
    'reserve', (select balance from state_accounts where state = 'DCB'),
    'states',  (select coalesce(jsonb_agg(jsonb_build_object('state', state, 'balance', balance) order by state), '[]'::jsonb) from state_accounts where state <> 'DCB'),
    'transit', (select coalesce(sum(amount - settled), 0) from cb_orders where kind = 'distribute' and not done),
    'orders',  (select coalesce(jsonb_agg(to_jsonb(o) order by o.id desc), '[]'::jsonb) from (select id, kind, state, amount, rate, settled, done, started_at, vans from cb_orders order by id desc limit 15) o),
    'vans',    (select coalesce(jsonb_agg(to_jsonb(v) order by v.id desc), '[]'::jsonb) from (
                  select id, order_id, seq, of_n, state, amount, load_s, started_at, depart_at, arrive_at, unload_end_at, delivered, delivered_at
                    from cb_vans where not delivered or delivered_at > now() - interval '7 days' order by id desc limit 60) v));
end $function$;

-- for everyone in the game: the vans on the road now (and those delivered in the last few minutes), without amounts
create or replace function public.cb_vans_public()
returns jsonb language plpgsql security definer set search_path = public as $function$
begin
  perform cb_settle();
  return jsonb_build_object('now', now(), 'vans',
    (select coalesce(jsonb_agg(to_jsonb(v) order by v.id), '[]'::jsonb) from (
       select id, order_id, seq, of_n, state, load_s, started_at, depart_at, arrive_at, unload_end_at, delivered, delivered_at
         from cb_vans where not delivered or delivered_at > now() - interval '5 minutes' order by id limit 40) v));
end $function$;

revoke all on function public.cb_vans_public() from public;
grant execute on function public.cb_vans_public() to anon, authenticated;
