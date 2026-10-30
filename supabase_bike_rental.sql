-- Delta City: motorbike rental — K10,000 for 24 hours from any car park.
--
-- A rental is a normal vehicles row owned by the renter, model 'motorbike', with rents_until set
-- by the server's clock (now()). Re-renting replaces the old bike: the old row is deleted wherever
-- it is (stored or out, even if being driven), the renter pays K10,000 again, a fresh 24 hours
-- starts and there is no refund. The payment goes through pay_service into the car park's state
-- account, in the same transaction, so a refused or failed payment creates nothing. When
-- rents_until passes, veh_sweep deletes the row; the vehicle_audit rows stay (verified below).
-- No role check: any signed-in citizen with a character can rent. Driving stays ownership/keys.
--
-- Needs supabase_vehicles.sql (vehicles, vehicle_keys, vehicle_audit, car_parks, vehicle_plate_seq,
-- veh_log, veh_free_bay, veh_row, veh_sweep) and supabase_services.sql (pay_service).
-- Run the whole file once in the Supabase SQL editor. Running it again is safe: every statement
-- is idempotent (create or replace / if not exists / grant-revoke pairs).

-- (a) the rental expiry, set from the server's clock; null for every non-rental vehicle
alter table vehicles add column if not exists rents_until timestamptz;

create index if not exists vehicles_rent_expiring on vehicles (rents_until) where rents_until is not null;

-- (b) rent a motorbike from a car park: K10,000 for 24 hours. Replaces any rental bike the renter
-- already has (deleted, audit row written), then charges, then creates the fresh bike.
create or replace function public.veh_rent_bike(p_park text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me       uuid := auth.uid();
  pk_state text;
  my_state text;
  b        int;
  id_    bigint;
  pl     text;
  paid   jsonb;
  old    record;
  old_id bigint;
  until_ timestamptz;
  v        vehicles;
begin
  if me is null then raise exception 'Sign in to rent a bike'; end if;
  if not exists(select 1 from characters where owner = me) then raise exception 'You need a character to rent a bike'; end if;
  if not exists(select 1 from car_parks where id = p_park) then raise exception 'That is not a car park'; end if;
  select state into pk_state from car_parks where id = p_park for update;   -- lock the row so two rentals at once can't take the same bay
  -- every car park is a public one belonging to a state; the character may only use the parks of their own state
  select town into my_state from characters where owner = me;
  if my_state is null or my_state <> pk_state then
    raise exception 'You can only rent a bike in your own state — your character is in %, that car park is in %', coalesce(my_state, '(no state yet)'), pk_state;
  end if;

  -- an old rental bike of this citizen is replaced: deleted wherever it is, with an audit row
  for old in
    select * from vehicles
     where owner = me and model = 'motorbike' and rents_until is not null
     order by id
     for update
  loop
    perform veh_log(me, old.id, 'rental replaced', jsonb_build_object('park', old.park_id, 'bay', old.bay, 'status', old.status, 'state', old.state));
    delete from vehicles where id = old.id;
    old_id := old.id;
  end loop;

  b := veh_free_bay(p_park);
  if b is null then raise exception 'Every bay in that car park is taken — rent again once a bay frees up'; end if;

  -- the money is taken in the same transaction: if the renter cannot afford it (or anything else
  -- fails), everything above unwinds and nothing is created
  paid := pay_service(10000, pk_state, 'bike rental 24h');

  until_ := now() + interval '24 hours';
  pl := 'DC-BIKE-' || lpad(nextval('vehicle_plate_seq')::text, 5, '0');
  insert into vehicles(plate, owner, model, special, status, park_id, bay, rents_until, created_by)
    values (pl, me, 'motorbike', false, 'stored', p_park, b, until_, me)
    returning id into id_;
  insert into vehicle_keys(vehicle_id, holder, granted_by) values (id_, me, me);
  perform veh_log(me, id_, 'rented', jsonb_build_object('park', p_park, 'bay', b, 'amount', 10000, 'rents_until', until_, 'replaced', old_id));

  select * into v from vehicles where id = id_;
  return jsonb_build_object('ok', true,
    'vehicle', veh_row(v, me),
    'cash', paid->>'cash', 'rents_until', until_);
end $$;

-- (c) the server's own sweep, extended: a rental bike whose 24 hours are up is DELETED (its audit
-- rows stay — vehicle_audit has no foreign key to vehicles). Stored and active alike.
create or replace function public.veh_sweep()
returns int language plpgsql security definer set search_path = public as $$
declare cfg jsonb := veh_cfg(); v record; n int := 0; held boolean; left_at timestamptz; who_state text;
begin
  -- expired rentals: deleted for good, an audit row first
  for v in select * from vehicles where rents_until is not null and rents_until <= now() order by id for update skip locked loop
    perform veh_log(null, v.id, 'rental expired', jsonb_build_object('rents_until', v.rents_until, 'status', v.status));
    delete from vehicles where id = v.id;
    n := n + 1;
  end loop;

  for v in select * from vehicles where status = 'active' order by id for update skip locked loop
    held := v.hold is not null and v.hold_since > now() - make_interval(secs => (cfg->>'hold_max_s')::numeric);
    if held then continue; end if;
    -- a car standing in a car park bay is safe
    if v.in_bay is not null then
      if v.last_seen < now() - make_interval(secs => (cfg->>'stale_s')::numeric) then perform veh_put_away(v.id, null, 'left in a bay'); n := n + 1; end if;
      continue;
    end if;
    -- left on the street: from when it was left, or from when the game stopped reporting with someone still in it
    left_at := v.abandoned_at;
    if v.last_seen < now() - make_interval(secs => (cfg->>'stale_s')::numeric) then left_at := least(coalesce(left_at, v.last_seen), v.last_seen); end if;
    if left_at is not null and left_at <= now() - make_interval(secs => (cfg->>'abandon_s')::numeric) then
      perform veh_put_away(v.id, null, 'abandoned'); n := n + 1; continue;
    end if;
    -- Rule A, checked by the server: the driver has travelled to another state
    select c.town into who_state from characters c where c.owner = v.active_by;
    if who_state is not null and v.state is not null and who_state <> v.state and not v.occupied then
      perform veh_put_away(v.id, null, 'driver left the state'); n := n + 1;
    end if;
  end loop;
  return n;
end $$;

-- (d) veh_row with the rental expiry, so the client can show a countdown and veh_mine gets it for free
create or replace function public.veh_row(v vehicles, p_me uuid)
returns jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object(
    'id', v.id, 'plate', v.plate, 'model', v.model, 'special', v.special, 'status', v.status,
    'park', v.park_id, 'bay', v.bay, 'state', v.state, 'pos', v.pos, 'damage', v.damage,
    'mine', v.owner = p_me,
    'owner_name', (select name from characters where owner = v.owner),
    'out_by_me', v.status = 'active' and v.active_by = p_me,
    'token', case when v.status = 'active' and v.active_by = p_me then v.token end,
    'in_bay', v.in_bay, 'hold', v.hold, 'occupied', v.occupied, 'abandoned_at', v.abandoned_at, 'last_seen', v.last_seen,
    'rents_until', v.rents_until,
    'keys', case when v.owner = p_me then (select coalesce(jsonb_agg(jsonb_build_object('holder', k.holder, 'name', c.name, 'since', k.granted_at) order by k.granted_at), '[]'::jsonb)
                                            from vehicle_keys k left join characters c on c.owner = k.holder where k.vehicle_id = v.id and k.revoked_at is null) end)
$$;

-- (e) verified against supabase_vehicles.sql: vehicle_audit.vehicle_id is a plain bigint with only
-- a regular index (vehicle_audit_vehicle) and NO foreign key to vehicles, so deleting a vehicles
-- row never cascades or blocks — its vehicle_audit rows survive. No schema change needed.

-- only the signed-in citizens can rent; everyone else gets nothing
revoke all on function public.veh_rent_bike(text) from public, anon;
grant execute on function public.veh_rent_bike(text) to authenticated;