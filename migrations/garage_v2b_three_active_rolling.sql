-- Garage v2, part 2: the rolling three-vehicle roster, live (follow-up to PR #26)
--
-- Why this file exists
-- --------------------
-- PR #25 (supabase_garage_v2a.sql) redefined public.veh_spawn with the OLD one-vehicle-out
-- behaviour: a loop that puts EVERY other active vehicle of the citizen away before the new
-- one is shown. If that file was the last garage SQL executed on the live Supabase project,
-- the live database still enforces one-out-each, no matter what the earlier base file says.
--
-- PR #26 added migrations/garage_v2_rolling_three.sql, but it had two problems:
--   1. it had not been executed against the live project, so the live veh_spawn was still the
--      one-out-each version from PR #25 (the reported symptom: "spawning another vehicle stores
--      the currently displayed vehicle before showing the next");
--   2. its rolling veh_spawn was copied from the pre-PR-#25 base and is missing the FROZEN
--      rejection that PR #25 added. Running PR #26's file alone would re-allow frozen
--      vehicles to be spawned (a regression of the freeze behaviour).
--
-- What this file does on the live Supabase project (run once, idempotent):
--   1. drops the old vehicles_one_out_each unique index (one-out-each is no longer the rule);
--   2. replaces public.veh_spawn with the rolling three-vehicle roster version that ALSO keeps
--      the PR #25 frozen rejection:
--        * takes a per-citizen advisory lock so the three-out cap can never be raced,
--        * refuses a frozen vehicle ("This vehicle is frozen in your garage") - key holders included,
--        * puts the OLDEST out vehicle away (by spawned_at, never by id or plate) until at most
--          three of the citizen's vehicles are out: spawns 1-3 build up [1], [1,2], [1,2,3];
--          spawn 4 auto-stows the oldest -> [2,3,4], and so on,
--        * refuses the spawn (undoing everything) if that oldest car is busy (driven, towed,
--          repaired, refuelled, burning) instead of silently removing a live vehicle,
--        * reports what it put away in the returned jsonb field "stowed": [{"id":..,"plate":..}].
--
-- It changes ONLY the garage spawn/storage rule. Freeze/unfreeze, slots, ownership, damage,
-- tow/repair/fuel and every other function are untouched. "create or replace" and
-- "drop index if exists" are both safe to re-run; the existing EXECUTE grants on veh_spawn
-- survive the replace.
--
-- Client note: index.html already reads r.stowed and drops only those exact vehicle ids from
-- the world; with an unpatched client it falls back to r.moved_from, so old builds keep working.

drop index if exists public.vehicles_one_out_each;

-- spawn one of my vehicles (or one I hold keys to) in a free bay of this car park. Wherever the vehicle is - stored in
-- another car park, or out on the road - it is moved here: the old copy is put away first (its token stops working, so
-- it disappears from the game that had it) and its damage, fuel and the rest come with it. All of this happens under
-- the vehicle's row lock, so two requests at once (two taps, two phones) can never make two copies. A second
-- request for a car already standing in this car park just returns it. A citizen can have up to three vehicles out
-- at once (the rolling three-vehicle roster): when a fourth is spawned, the OLDEST by spawn order goes back
-- to its bay automatically and is reported to the client in `stowed`. A vehicle that is busy (driven, towed,
-- repaired, refuelled, burning) is never put away. A frozen vehicle can never be spawned, key holders included
-- (PR #25 rule, kept here). Refused (with the reason) when someone is driving the car, it is being towed,
-- repaired or refuelled, or it is burning. Returns {vehicle, moved_from, stowed} or {error}.
-- put a car away EXCEPT in p_avoid_park: the rolling spawn must free the bay in the car park the
-- new car is moving into, so a car stowed there to make room keeps its own bay only when that bay
-- is not in the destination car park. Falls back to a free bay in another car park of the same
-- state, or the car park office (bay = null, waiting for a bay) when every bay is taken.
create or replace function public.veh_put_away_elsewhere(p_vehicle bigint, p_actor uuid, p_reason text, p_avoid_park text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v vehicles; pk text; b int;
begin
  select * into v from vehicles where id = p_vehicle;
  if v.status <> 'active' then return jsonb_build_object('park', v.park_id, 'bay', v.bay); end if;
  pk := v.park_id; b := null;
  if v.in_bay is not null and v.park_id is distinct from p_avoid_park then b := v.in_bay; end if;
  -- clear this car's place first so its own bay counts as free
  update vehicles set status = 'stored', bay = null, in_bay = null, token = null, active_by = null, occupied = false, hold = null,
         hold_since = null, abandoned_at = null, pos = null, state = null where id = v.id;
  if b is null then
    select p.id, veh_free_bay(p.id) into pk, b from car_parks p
     where p.state = coalesce(v.state, (select state from car_parks where id = v.park_id))
       and p.id is distinct from p_avoid_park and veh_free_bay(p.id) is not null
     order by p.id limit 1;
  end if;
  if b is null then pk := coalesce((select id from car_parks where state = coalesce(v.state, (select state from car_parks where id = v.park_id)) order by id limit 1), v.park_id); end if;
  update vehicles set park_id = pk, bay = b where id = v.id;
  perform veh_log(p_actor, v.id, 'despawn', jsonb_build_object('reason', p_reason, 'park', pk, 'bay', b, 'pos', v.pos, 'state', v.state));
  return jsonb_build_object('park', pk, 'bay', b);
end $$;

revoke all on function public.veh_put_away_elsewhere(bigint, uuid, text, text) from public, anon, authenticated;

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
  -- frozen: parked out of the garage, no one can spawn it - key holders included (PR #25)
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
  -- the rolling three-vehicle roster: put my oldest out cars (by spawn order) away until at most three of mine
  -- are out. A car that is busy (driven, towed, repaired, refuelled, burning) is never put away — the spawn is
  -- refused (and the whole transaction undone, so nothing changes) instead of silently removing a live vehicle.
  for o in select * from vehicles where status = 'active' and active_by = me and id <> v.id
           order by coalesce(spawned_at, last_seen) asc, id asc for update loop
    -- stop once the ones being moved in would leave three of mine out at most
    -- (v.id is excluded: a car moving park-to-park is not a new slot)
    if (select count(*) from vehicles where active_by = me and status = 'active' and id <> v.id) <= 2 then
      exit;
    end if;
    why := veh_busy(o);
    if why is not null then
      return jsonb_build_object('error', 'Your other car (' || o.plate || ') cannot be put away right now: ' || why || '. Store it first.');
    end if;
    stowed := stowed || jsonb_build_object('id', o.id, 'plate', o.plate);
    -- never let the stowed car keep a bay in the park the new car is moving into: that bay is the
    -- very slot the new car needs (a three-bay park cannot hold three out cars plus one stowed one).
    -- In any other park this is byte-for-byte the normal put-away.
    perform veh_put_away_elsewhere(o.id, me, 'another vehicle spawned', p_park);
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
  update vehicles set status = 'active', park_id = p_park, bay = null, in_bay = b, state = pk.state, token=gen_random_uuid(),
                      active_by = me, occupied = false, hold = null, hold_since = null, abandoned_at = null, spawned_at = now(), last_seen = now(), pos = null
   where id = v.id returning * into v;
  perform veh_log(me, v.id, case when was->>'status' = 'active' or was->>'park' is distinct from p_park then 'transfer' else 'spawn' end,
                  jsonb_build_object('park', p_park, 'bay', b, 'from', was));
  return jsonb_build_object('now', now(), 'vehicle', veh_row(v, me), 'moved_from', was, 'stowed', stowed);
end $$;