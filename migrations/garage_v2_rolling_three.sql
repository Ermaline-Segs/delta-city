-- Garage v2: rolling three-vehicle roster (PR #26)
--
-- What this changes on the live Supabase project:
--   1. drops the old vehicles_one_out_each unique index (one-out-each is no longer the rule),
--   2. replaces public.veh_spawn with the rolling-roster version kept verbatim in
--      supabase_vehicles.sql, which:
--        * takes a per-citizen advisory lock so the three-out cap can never be raced,
--        * puts the OLDEST out vehicle away (by spawned_at, never by id or plate) until at most
--          three of the citizen's vehicles are out,
--        * refuses the spawn (undoing everything) if the oldest is busy (driven/towed/repaired/
--          refuelled/burning) instead of silently removing a live vehicle,
--        * reports what it put away in the returned jsonb field "stowed": [{"id":..,"plate":..}].
--
-- Run this file once against the Supabase SQL editor / psql. It is idempotent:
-- "drop index if exists" and "create or replace" are both safe to re-run.
--
-- Client note: index.html reads r.stowed and drops only those exact vehicle ids from the world.
-- An unpatched client talking to this server still works (it falls back to dropping its focused
-- vehicle when the server moved one), and a patched client against an unpatched server works via
-- the r.moved_from fallback.

drop index if exists public.vehicles_one_out_each;

-- spawn one of my vehicles (or one I hold keys to) in a free bay of this car park. Wherever the vehicle is - stored in
-- another car park, or out on the road - it is moved here: the old copy is put away first (its token stops working, so
-- it disappears from the game that had it) and its damage, fuel and the rest come with it. All of this happens under
-- the vehicle's row lock, so two requests at once (two taps, two phones) can never make two copies. A second
-- request for a car already standing in this car park just returns it. A citizen can have up to three vehicles out
-- at once (the rolling three-vehicle roster): when a fourth is spawned, the OLDEST by spawn order goes back
-- to its bay automatically and is reported to the client in `stowed`. A vehicle that is busy (driven, towed,
-- repaired, refuelled, burning) is never put away. Refused (with the reason) when someone is driving the car,
-- it is being towed, repaired or refuelled, or it is burning. Returns {vehicle, moved_from, stowed} or {error}.
create or replace function public.veh_spawn(p_vehicle bigint, p_park text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; o vehicles; b int; pk car_parks; why text; was jsonb; stowed jsonb := '[]'::jsonb;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  -- one spawn at a time per citizen, across tabs/phones, so the three-out cap is never raced
  perform pg_advisory_xact_lock(hashtext('vehroster:' || me::text));
  perform veh_sweep();
  select * into pk from car_parks where id = p_park;
  if pk.id is null then return jsonb_build_object('error', 'That is not a car park'); end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found then return jsonb_build_object('error', 'That vehicle does not exist'); end if;
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
  -- the rolling three-vehicle roster: put my oldest out cars (by spawn order) away until at most three of mine
  -- are out. A car that is busy (driven, towed, repaired, refuelled, burning) is never put away — the spawn is
  -- refused (and the whole transaction undone, so nothing changes) instead of silently removing a live vehicle.
  for o in select * from vehicles where status = 'active' and active_by = me and id <> v.id
           order by coalesce(spawned_at, last_seen) asc, id asc for update loop
    if (select count(*) from vehicles where active_by = me and status = 'active') <= 3 then
      exit;
    end if;
    why := veh_busy(o);
    if why is not null then
      return jsonb_build_object('error', 'Your other car (' || o.plate || ') cannot be put away right now: ' || why || '. Store it first.');
    end if;
    stowed := stowed || jsonb_build_object('id', o.id, 'plate', o.plate);
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
  return jsonb_build_object('now', now(), 'vehicle', veh_row(v, me), 'moved_from', was, 'stowed', stowed);
end $$;
