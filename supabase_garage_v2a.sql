-- ====================================================================================================================
-- Garage v2, part 1: frozen vehicles and per-player garage slots.
--
-- Owner rules
-- -----------
-- * Each player has a number of garage slots (default 5; only an admin may change it, between 1 and 50).
-- * A slot is used by EVERY non-frozen vehicle the player owns - stored or out on the road, and including a
--   rented bike. The frozen vehicles are the parked-out-of-garage ones: they use no slot.
-- * "Frozen" = owned but unusable, and parked outside the garage: it uses no slot and nobody can spawn it -
--   key holders included. Freezing costs nothing; unfreezing costs a slot.
-- * A player who already owns four or more vehicles (frozen counted, the rented bike not) cannot rent another
--   bike, and a player with no free slot cannot rent one at all ("freeze a vehicle first"). A rented bike gets
--   no vehicle_keys row: it cannot be gifted, given keys to, or left behind.
-- * The existing one-out rule (one vehicle of a player's out at a time) is UNCHANGED: the client is not ready.
--
-- What is in this file
-- -------------------
-- * vehicles.frozen - boolean, not null, default false (new column, backfilled false for every existing vehicle).
-- * garage_slots - one row per owner with the slot count (default 5, between 1 and 50); backfilled for every
--   existing vehicle owner.
-- * veh_freeze(p_vehicle), veh_unfreeze(p_vehicle) - owner only, free to freeze, a free slot to unfreeze.
-- * veh_admin_set_slots(p_owner, p_slots) - an admin only (veh_role), sets a player's slots.
-- * veh_spawn - byte-identical to the latest definition except one added refusal: frozen vehicles cannot be
--   spawned, with the exact message "This vehicle is frozen in your garage".
-- * veh_row / veh_mine - the latest definitions with ONLY json fields added (frozen, slots, active_count) so
--   the current client keeps working: it ignores unknown keys.
-- * veh_rent_bike - the definition from supabase_bike_rental.sql with ONLY three changes: the 4-or-more rule,
--   the free-slot rule, and no vehicle_keys row for the rented bike.
--
-- Safe to run twice: every statement is an IF NOT EXISTS / CREATE OR REPLACE, and the column and backfill are
-- guarded so a second run changes nothing. The only "new" state created on a second run is none: idempotent.
--
-- Every function is security definer with search_path pinned, matching the rest of the supabase_*.sql files.
-- ====================================================================================================================

-- ---------- the frozen flag on vehicles ----------------------------------------------------------------------------------
-- added once; every existing vehicle is unfrozen (default false).
do $$
begin
  if not exists (select 1 from information_schema.columns where table_schema = 'public' and table_name = 'vehicles' and column_name = 'frozen') then
    alter table vehicles add column frozen boolean not null default false;
  end if;
end $$;

-- ---------- per-player garage slots --------------------------------------------------------------------------------------
-- one row per owner. A brand-new player gets 5 the first time one of the functions below looks them up (the
-- coalesce in those functions); the backfill below only matters for players who already own vehicles, so that
-- their count is visible immediately.
create table if not exists garage_slots (
  owner  uuid primary key references auth.users(id) on delete cascade,
  slots  int    not null default 5 check (slots between 1 and 50)
);

-- backfill: every existing owner of at least one vehicle gets a default row (5 slots) once.
insert into garage_slots (owner)
select distinct owner from vehicles where owner is not null
on conflict (owner) do nothing;

-- ---------- who has how many slots, and how many non-frozen vehicles do they own ------------------------------------------
-- both helper lookups are used by the freeze/unfreeze/rent functions and by the new json fields. A player with
-- no row in garage_slots is treated as having the default 5 (same default as the column).
create or replace function public.veh_slots(p_owner uuid)
returns int language sql stable security definer set search_path = public as $$
  select coalesce((select slots from garage_slots where owner = p_owner), 5)
$$;

create or replace function public.veh_active_count(p_owner uuid)
returns int language sql stable security definer set search_path = public as $$
  select count(*)::int from vehicles where owner = p_owner and not frozen
$$;

-- ---------- freeze / unfreeze ----------------------------------------------------------------------------------------------
-- Freeze: owner only, only a stored vehicle, not held (tow/repair/refuel/fire), not in a repair queue/bay if the
-- repair tables exist, never a rented bike. Free.
-- Unfreeze: needs a free slot (a non-frozen vehicle count below the slot count), so the vehicle takes a slot back.
create or replace function public.veh_freeze(p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found then return jsonb_build_object('error', 'That vehicle does not exist'); end if;
  if v.owner is distinct from me then return jsonb_build_object('error', 'Only the owner can freeze a vehicle'); end if;
  if v.rents_until is not null then return jsonb_build_object('error', 'A rented bike cannot be frozen'); end if;
  if v.frozen then return jsonb_build_object('now', now(), 'frozen', true, 'already', true); end if;
  if v.status <> 'stored' then return jsonb_build_object('error', 'Only a stored vehicle can be frozen. Put it in the garage first.'); end if;
  if v.hold is not null then return jsonb_build_object('error', 'It is being ' || v.hold || ' right now. Wait.'); end if;
  -- in a repair queue or bay, if the repair tables exist (they are an optional add-on; the exists is nested
  -- so it is only planned when the table is actually there)
  if to_regclass('public.vehicle_repairs') is not null then
    if exists (select 1 from vehicle_repairs r where r.vehicle_id = v.id and r.status in ('queued', 'in_progress', 'repair')) then
      return jsonb_build_object('error', 'It is in the repair queue. Wait for the repair.');
    end if;
  end if;
  update vehicles set frozen = true where id = v.id;
  return jsonb_build_object('now', now(), 'frozen', true);
end $$;

create or replace function public.veh_unfreeze(p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; used int;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found then return jsonb_build_object('error', 'That vehicle does not exist'); end if;
  if v.owner is distinct from me then return jsonb_build_object('error', 'Only the owner can unfreeze a vehicle'); end if;
  if not v.frozen then return jsonb_build_object('now', now(), 'frozen', false, 'already', true); end if;
  -- a free slot is needed for the vehicle to come back into the garage
  used := veh_active_count(me);
  if used >= veh_slots(me) then
    return jsonb_build_object('error', 'No free slot. Freeze a vehicle first or buy another garage.');
  end if;
  update vehicles set frozen = false where id = v.id;
  return jsonb_build_object('now', now(), 'frozen', false);
end $$;

-- ---------- admin: change a player's slots --------------------------------------------------------------------------------
-- only an admin (veh_role returns the player's role; only the chief may change slots), between 1 and 50.
create or replace function public.veh_admin_set_slots(p_owner uuid, p_slots int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); role text;
begin
  if me is null then raise exception 'Sign in'; end if;
  if p_slots is null or p_slots < 1 or p_slots > 50 then
    return jsonb_build_object('error', 'Slots must be between 1 and 50');
  end if;
  role := veh_role(me);
  if role is distinct from 'admin' then return jsonb_build_object('error', 'Only the chief can change garage slots'); end if;
  insert into garage_slots (owner, slots) values (p_owner, p_slots)
  on conflict (owner) do update set slots = excluded.slots;
  return jsonb_build_object('ok', true, 'owner', p_owner, 'slots', p_slots);
end $$;
-- ---------- veh_spawn: the latest definition with ONE added check (frozen) ---------------------------------------------------------
create or replace function public.veh_spawn(p_vehicle bigint, p_park text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; o vehicles; b int; pk car_parks; why text; was jsonb;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  perform veh_sweep();
  select * into pk from car_parks where id = p_park;
  if pk.id is null then return jsonb_build_object('error', 'That is not a car park'); end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found then return jsonb_build_object('error', 'That vehicle does not exist'); end if;
  -- frozen: parked out of the garage, no one can spawn it - key holders included
  if v.frozen then
    perform veh_log(me, v.id, 'spawn refused', jsonb_build_object('why', 'frozen', 'park', p_park));
    return jsonb_build_object('error', 'This vehicle is frozen in your garage');
  end if;
  -- refusals are answered (not raised) so that the attempt stays in the audit log
  if not veh_can_drive(v.id, me) then
    perform veh_log(me, v.id, 'spawn refused', jsonb_build_object('why', 'no keys', 'park', p_park));
    return jsonb_build_object('error', 'You do not have the keys to this vehicle');
  end if;
  -- already standing here for me (a repeated tap): nothing more to do
  if v.status = 'active' and v.active_by = me and v.park_id = p_park and v.in_bay is not null and not v.occupied then
    return jsonb_build_object('now', now(), 'vehicle', veh_row(v, me), 'already', true);
  end if;
  why := veh_busy(v);
  if why is not null then
    perform veh_log(me, v.id, 'spawn refused', jsonb_build_object('why', why, 'park', p_park));
    return jsonb_build_object('error', 'You cannot spawn this car right now: ' || why || '.');
  end if;
  -- my other vehicle that is out goes back to its car park first (one out at a time), if that is safe
  for o in select * from vehicles where status = 'active' and active_by = me and id <> v.id for update loop
    why := veh_busy(o);
    if why is not null then
      return jsonb_build_object('error', 'Your other car (' || o.plate || ') cannot be put away right now: ' || why || '. Store it first.');
    end if;
    perform veh_put_away(o.id, me, 'another vehicle spawned');
  end loop;
  -- where it was before: out on the road (that copy is put away), or stored in a bay somewhere
  was := jsonb_build_object('status', v.status, 'park', v.park_id, 'state', v.state, 'pos', v.pos);
  if v.status = 'active' then
    perform veh_put_away(v.id, me, 'moved to ' || pk.name);
    select * into v from vehicles where id = v.id;
  end if;
  -- the bay: its own, when it is stored in this car park already; otherwise the first free one
  b := case when v.park_id = p_park and v.bay is not null then v.bay end;
  update vehicles set bay = null where id = v.id;          -- its old bay (in any car park) is free from here on
  if b is null then b := veh_free_bay(p_park); end if;
  if b is null then        -- raised, so everything above (the old copy put away, the bay let go) is undone: nothing changes
    raise exception 'All garage spaces are occupied. Please wait or try another space.';
  end if;
  update vehicles set status = 'active', park_id = p_park, bay = null, in_bay = b, state = pk.state, token = gen_random_uuid(),
         active_by = me, occupied = false, hold = null, hold_since = null, abandoned_at = null, spawned_at = now(), last_seen = now(), pos = null
   where id = v.id returning * into v;
  perform veh_log(me, v.id, case when was->>'status' = 'active' or was->>'park' is distinct from p_park then 'transfer' else 'spawn' end,
                  jsonb_build_object('park', p_park, 'bay', b, 'from', was));
  return jsonb_build_object('now', now(), 'vehicle', veh_row(v, me), 'moved_from', was);
end $$;
-- ---------- veh_mine: the latest definition with ONLY top-level json fields added (slots, active_count) -------------------
create or replace function public.veh_mine()
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if me is null then raise exception 'Sign in to see your vehicles'; end if;
  perform veh_sweep();
  return jsonb_build_object('now', now(), 'cfg', veh_cfg(),
    'parks', (select coalesce(jsonb_agg(jsonb_build_object('id', p.id, 'state', p.state, 'name', p.name, 'bays', p.bays,
                'taken', (select coalesce(jsonb_agg(b order by b), '[]'::jsonb) from (
                           select bay b from vehicles where status = 'stored' and park_id = p.id and bay is not null
                           union select in_bay from vehicles where status = 'active' and park_id = p.id and in_bay is not null) t)) order by p.id), '[]'::jsonb) from car_parks p),
    'vehicles', (select coalesce(jsonb_agg(veh_row(v, me) order by v.id), '[]'::jsonb) from vehicles v
                  where v.owner = me or exists(select 1 from vehicle_keys k where k.vehicle_id = v.id and k.holder = me and k.revoked_at is null)),
    'slots', veh_slots(me), 'active_count', veh_active_count(me));
end $$;

-- ---------- veh_row: the latest definition (supabase_bike_rental.sql) with ONLY json fields added ---------------------------
-- (frozen per vehicle; slots and active_count are the player's, repeated on every row so the client can read them anywhere)
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
    'frozen', v.frozen,
    'slots', veh_slots(p_me), 'active_count', veh_active_count(p_me),
    'keys', case when v.owner = p_me then (select coalesce(jsonb_agg(jsonb_build_object('holder', k.holder, 'name', c.name, 'since', k.granted_at) order by k.granted_at), '[]'::jsonb)
                                            from vehicle_keys k left join characters c on c.owner = k.holder where k.vehicle_id = v.id and k.revoked_at is null) end)
$$;

-- ---------- veh_rent_bike: the definition from supabase_bike_rental.sql with ONLY three changes -----------------------------
-- 1) a player who already owns four or more vehicles (frozen counted, the rented bike not) cannot rent
-- 2) a player with no free slot cannot rent ("freeze a vehicle first")
-- 3) no vehicle_keys row for the rented bike
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
  -- garage v2 (1): four or more owned vehicles (frozen counted, the rented bike not) means no more rentals
  if (select count(*) from vehicles where owner = me and (model <> 'motorbike' or rents_until is null)) >= 4 then
    raise exception 'You already own four vehicles - sell one before renting a bike';
  end if;
  -- garage v2 (2): a free slot is needed for the rental to take a slot
  if veh_active_count(me) >= veh_slots(me) then
    raise exception 'No free garage slot - freeze a vehicle first';
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
  perform veh_log(me, id_, 'rented', jsonb_build_object('park', p_park, 'bay', b, 'amount', 10000, 'rents_until', until_, 'replaced', old_id));

  select * into v from vehicles where id = id_;
  return jsonb_build_object('ok', true,
    'vehicle', veh_row(v, me),
    'cash', paid->>'cash', 'rents_until', until_);
end $$;

-- ---------- permissions, matching the style of supabase_vehicles.sql -------------------------------------------------------
revoke all on function public.veh_freeze(bigint), public.veh_unfreeze(bigint), public.veh_admin_set_slots(uuid, int),
  public.veh_slots(uuid), public.veh_active_count(uuid) from public, anon, authenticated;
grant execute on function public.veh_freeze(bigint), public.veh_unfreeze(bigint), public.veh_slots(uuid),
  public.veh_active_count(uuid) to authenticated;
-- admin only: the slot count is an admin decision
grant execute on function public.veh_admin_set_slots(uuid, int) to authenticated;