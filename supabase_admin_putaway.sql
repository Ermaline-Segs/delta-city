-- supabase_admin_putaway.sql
--
-- "Put this vehicle back in its garage" — an admin-only tool.
--
-- Use it when a car is stuck active on the server (for example after it
-- caught fire and nobody's browser tab was open to let the fire finish):
-- the function stores the car in a free bay regardless of its hold and of
-- the staleness sweep, so the next veh_update from the game sends
-- p_hold=null and the server's hold clears.
--
-- It reuses veh_put_away, so it follows whatever the garage code does
-- today (finds the car's own bay first, then a free bay in its state,
-- then any free bay, and clears hold, hold_since, occupied, token and
-- active_by). It never changes ownership, and it writes an audit row
-- 'admin put away' on top of the normal 'despawn' row.
--
-- Only the Chief Admin (characters.role = 'admin') may call it; the
-- "no role check on driving" rule is not touched by this file.
--
-- Safe to run twice: everything is create or replace / idempotent grant.

create or replace function public.veh_admin_putaway(p_vehicle bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare
  me uuid := auth.uid();
  v  vehicles;
  r  jsonb;
begin
  if me is null or veh_role(me) is distinct from 'admin' then
    raise exception 'Only the Chief Admin can put a vehicle back in its garage';
  end if;
  select * into v from vehicles where id = p_vehicle;
  if not found then
    raise exception 'No such vehicle';
  end if;
  if v.status = 'stored' and v.park_id is not null then
    return jsonb_build_object('park', v.park_id, 'bay', v.bay, 'already', true);
  end if;
  r := veh_put_away(p_vehicle, me, 'admin put away');
  perform veh_log(me, v.id, 'admin put away',
    jsonb_build_object('plate', v.plate, 'park', r->>'park', 'bay', r->>'bay'));
  return r;
end $$;

revoke all on function public.veh_admin_putaway(bigint) from public, anon;
grant execute on function public.veh_admin_putaway(bigint) to authenticated;