-- Delta City RP: make one account the Chief Admin and give it the special Chief Admin car.
--
-- Run supabase_vehicles.sql first (once), then this whole file in the Supabase SQL editor.
-- Running it again is safe: the role is set again, and a second special car is not made if the account already has one.
-- The id below can be the account's id (characters.owner) or the character's own id (characters.id).

do $$
declare want text := '62fb9e58-b44d-432c-a485-78c74d80df5c'; who uuid; nm text; b int; pk text; id_ bigint; pl text;
begin
  select c.owner, c.name into who, nm from characters c where c.owner::text = want or to_jsonb(c)->>'id' = want limit 1;
  if who is null then raise exception 'No character has the id %', want; end if;
  update characters set role = 'admin' where owner = who;
  if exists(select 1 from vehicles where owner = who and special) then
    raise notice '% is the Chief Admin and already has the special car', nm;
    return;
  end if;
  -- the first car park in Asaba with a free bay
  select p.id, veh_free_bay(p.id) into pk, b from car_parks p where p.state = 'Asaba' and veh_free_bay(p.id) is not null order by p.id limit 1;
  if pk is null then raise exception 'Every bay in Asaba is taken'; end if;
  pl := 'DC-ADMIN-' || nextval('vehicle_plate_seq');
  insert into vehicles(plate, owner, model, special, status, park_id, bay, created_by)
    values (pl, who, 'sovereign', true, 'stored', pk, b, who) returning id into id_;
  perform veh_log(who, id_, 'provision', jsonb_build_object('owner', who, 'name', nm, 'model', 'sovereign', 'special', true, 'park', pk, 'bay', b, 'by', 'supabase_chief_admin.sql'));
  raise notice '% is the Chief Admin. Special car % is in bay % of %', nm, pl, b + 1, (select name from car_parks where id = pk);
end $$;

select name, role, (select string_agg(plate || ' in ' || park_id || ' bay ' || (bay + 1), ', ') from vehicles v where v.owner = c.owner) as vehicles
  from characters c where c.owner::text = '62fb9e58-b44d-432c-a485-78c74d80df5c' or to_jsonb(c)->>'id' = '62fb9e58-b44d-432c-a485-78c74d80df5c';
