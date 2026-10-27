-- Delta City RP: every public building now has its own fenced compound with its own car park inside (a gate at least
-- 7 m wide, at least 3 numbered bays and the garage terminal); roadside shops have a lay-by. These replace the old
-- separate car parks.
--
-- What this does (safe to run twice):
--   1. adds the 91 new car parks (or updates them to the game's positions);
--   2. moves every car that belongs to an old car park to the NEAREST new car park in the same state:
--        * a stored car gets a free bay there (or the next nearest car park with a free bay); if every car park in its
--          state were full it would wait at the nearest one for a free bay, as the game already allows;
--        * a car out on the road keeps going; only the car park it returns to changes;
--      its owner, keys, damage, plate and everything else stay exactly as they were. Each move is written to
--      vehicle_audit ('park_moved'), so nothing is lost and it can be checked;
--   3. removes the old car parks once no car refers to them.
-- Run it after supabase_vehicles.sql (which now lists the new car parks too).

begin;

insert into car_parks(id, state, name, x, z, bays) values
  ('asaba-gov', 'Asaba', 'State Government House Car Park', 9.7, -157.9, 3),
  ('asaba-court', 'Asaba', 'Supreme Court Car Park', 57.7, -11.7, 3),
  ('asaba-police', 'Asaba', 'Police HQ Car Park', 117.7, -11.7, 3),
  ('asaba-bank', 'Asaba', 'Crestfield Bank Car Park', 36.3, 11.7, 3),
  ('asaba-hosp', 'Asaba', 'National Specialist Hospital Car Park', 102.3, 11.7, 3),
  ('asaba-uni', 'Asaba', 'Cambridge University Car Park', 118.3, -93.9, 3),
  ('asaba-util', 'Asaba', 'National Public Utilities Car Park', -53.7, 11.4, 3),
  ('asaba-trans', 'Asaba', 'National Transport Authority Car Park', -121.7, 11.7, 3),
  ('asaba-house', 'Asaba', 'Asaba Housing Development Car Park', -11.7, 44.3, 3),
  ('asaba-agri', 'Asaba', 'Ministry of Agriculture & Resources Car Park', -11.7, 78.3, 3),
  ('asaba-fed', 'Asaba', 'Federal Government Car Park', -64.5, -17.4, 5),
  ('asaba-air', 'Asaba', 'Delta International Airport Car Park', -243.9, -82.7, 5),
  ('asaba-hotel', 'Asaba', 'Best GRA Hotel Car Park', 60.2, -116.1, 4),
  ('asaba-guest', 'Asaba', 'Asaba Guest House Car Park', 102.7, 85.9, 3),
  ('asaba-market', 'Asaba', 'Asaba Market Car Park', 148.2, 85, 4),
  ('asaba-church', 'Asaba', 'Asaba Church Car Park', -87.7, 13.9, 3),
  ('asaba-treasury', 'Asaba', 'National Treasury Car Park', 97.3, -93.5, 3),
  ('asaba-imm', 'Asaba', 'Immigration Car Park', 29.1, -90.4, 3),
  ('asaba-trade', 'Asaba', 'Ministry of Trade & Commerce Car Park', -160.8, 76.9, 3),
  ('asaba-foreign', 'Asaba', 'Ministry of Foreign Affairs Car Park', -29.2, 150.3, 3),
  ('asaba-culture', 'Asaba', 'National Culture & Heritage Bureau Car Park', -132.4, 70.8, 3),
  ('asaba-stats', 'Asaba', 'National Bureau of Statistics Car Park', -118.6, 115.7, 3),
  ('asaba-lifestyle', 'Asaba', 'Lifestyle Centre Car Park', -173.8, 35, 3),
  ('asaba-woffice', 'Asaba', 'Asaba Auto Workshop Car Park', -68.6, 176, 3),
  ('asaba-fshop', 'Asaba', 'Asaba Filling Station Car Park', 215.3, 8, 3),
  ('asaba-shop6', 'Asaba', 'Shop 6 Lay-by', 82.4, 91.7, 3),
  ('asaba-shop7', 'Asaba', 'Shop 7 Lay-by', -5.8, 106.6, 3),
  ('asaba-shop8', 'Asaba', 'Shop 8 Lay-by', -5.8, 138.4, 3),
  ('warri-agri', 'Warri', 'Natural Resources Office Car Park', -11.7, -67.7, 3),
  ('warri-hosp', 'Warri', 'Warri State Hospital Car Park', 11.9, -34.7, 3),
  ('warri-uni', 'Warri', 'Warri State University Car Park', 13.9, -48.3, 3),
  ('warri-house', 'Warri', 'Warri Housing Development Car Park', -11.7, -35.7, 3),
  ('warri-police', 'Warri', 'Police Command Car Park', 11.9, 62.3, 3),
  ('warri-gov', 'Warri', 'State Government House Car Park', 15.9, 43.7, 3),
  ('warri-bank', 'Warri', 'Eastway Bank Car Park', -11.7, 21.3, 3),
  ('warri-util', 'Warri', 'Warri Public Utilities Car Park', -79.7, 11.7, 3),
  ('warri-court', 'Warri', 'State High Court Car Park', 82.3, 11.7, 3),
  ('warri-trans', 'Warri', 'State Ministry of Transport Car Park', 109.7, 80.9, 3),
  ('warri-imm', 'Warri', 'Immigration Car Park', 11.7, 128.7, 3),
  ('warri-air', 'Warri', 'Warri Airport Car Park', -57.3, -112, 5),
  ('warri-hotel', 'Warri', 'Bon Hotel Hyatti Car Park', 227.2, -103.6, 4),
  ('warri-guest', 'Warri', 'Legacy Suites Car Park', 206.3, -80.4, 3),
  ('warri-lifestyle', 'Warri', 'Lifestyle Centre Car Park', -27.3, 81.7, 3),
  ('warri-market', 'Warri', 'Warri Main Market Car Park', -52.3, -13.7, 4),
  ('warri-woffice', 'Warri', 'Warri Port Auto Workshop Car Park', 57.1, 103, 3),
  ('warri-fshop', 'Warri', 'Warri Filling Station Car Park', 133.9, 8, 3),
  ('warri-shop3', 'Warri', 'Okere Provisions Car Park', -44.7, 102.7, 3),
  ('warri-shop4', 'Warri', 'Effurun Mini Mart Car Park', 50.3, 11.2, 3),
  ('warri-shop5', 'Warri', 'Ekpan Supermarket Car Park', 59.3, 81.3, 3),
  ('ozoro-gov', 'Ozoro', 'State Government House Car Park', 9.7, -134.3, 3),
  ('ozoro-court', 'Ozoro', 'State High Court Car Park', -11.7, -75.7, 3),
  ('ozoro-police', 'Ozoro', 'Police Command Car Park', 11.7, -56.3, 3),
  ('ozoro-bank', 'Ozoro', 'Trustmark Bank Car Park', 53.7, -11.7, 3),
  ('ozoro-uni', 'Ozoro', 'University Car Park', 101.7, -11.7, 3),
  ('ozoro-hosp', 'Ozoro', 'Hospital Car Park', 56.3, 11.7, 3),
  ('ozoro-imm', 'Ozoro', 'Immigration Car Park', -36.3, -11.7, 3),
  ('ozoro-trans', 'Ozoro', 'Transport Car Park', -86.3, -11.7, 3),
  ('ozoro-house', 'Ozoro', 'Housing Office Car Park', -75.7, 11.7, 3),
  ('ozoro-util', 'Ozoro', 'Utilities Car Park', -11.7, 48.3, 3),
  ('ozoro-agri', 'Ozoro', 'Agriculture Car Park', 11.7, 73.7, 3),
  ('ozoro-air', 'Ozoro', 'Ozoro Airport Car Park', -70, 84.3, 5),
  ('ozoro-hotel', 'Ozoro', 'Ozoro Presidential Hotel Car Park', 72.8, -107.7, 4),
  ('ozoro-guest', 'Ozoro', 'Okay Hotels Car Park', 122.7, -67.7, 3),
  ('ozoro-lifestyle', 'Ozoro', 'Lifestyle Centre Car Park', -124.7, -108.5, 3),
  ('ozoro-market', 'Ozoro', 'Ozoro Central Market Car Park', 84.2, 120.7, 4),
  ('ozoro-woffice', 'Ozoro', 'Ozoro Auto Workshop Car Park', -108.3, 8.3, 3),
  ('ozoro-fshop', 'Ozoro', 'Ozoro Filling Station Car Park', 110.3, 8, 3),
  ('ozoro-shop3', 'Ozoro', 'Isoko Provisions Car Park', 24.7, -108.1, 3),
  ('ozoro-shop4', 'Ozoro', 'Oleh Road Stores Car Park', 118.7, -108.1, 3),
  ('ozoro-shop5', 'Ozoro', 'Ozoro Mini Mart Car Park', -43.1, 11.2, 3),
  ('agbor-gov', 'Agbor', 'State Government House Car Park', 9.7, -134.3, 3),
  ('agbor-court', 'Agbor', 'State High Court Car Park', -11.7, -75.7, 3),
  ('agbor-police', 'Agbor', 'Police Command Car Park', 11.7, -56.3, 3),
  ('agbor-bank', 'Agbor', 'Grandview Bank Car Park', 53.7, -11.7, 3),
  ('agbor-uni', 'Agbor', 'University Car Park', 101.7, -11.7, 3),
  ('agbor-hosp', 'Agbor', 'Hospital Car Park', 56.3, 11.7, 3),
  ('agbor-imm', 'Agbor', 'Immigration Car Park', -36.3, -11.7, 3),
  ('agbor-trans', 'Agbor', 'Transport Car Park', -86.3, -11.7, 3),
  ('agbor-house', 'Agbor', 'Housing Office Car Park', -75.7, 11.7, 3),
  ('agbor-util', 'Agbor', 'Utilities Car Park', -11.7, 48.3, 3),
  ('agbor-agri', 'Agbor', 'Agriculture Car Park', 11.7, 73.7, 3),
  ('agbor-air', 'Agbor', 'Agbor Airport Car Park', -70, 84.3, 5),
  ('agbor-hotel', 'Agbor', 'Agbor Palace Hotel Car Park', 72.8, -107.7, 4),
  ('agbor-guest', 'Agbor', 'Royal Suites Car Park', 122.7, -67.7, 3),
  ('agbor-lifestyle', 'Agbor', 'Lifestyle Centre Car Park', -124.7, -108.5, 3),
  ('agbor-market', 'Agbor', 'Agbor Obi Market Car Park', 84.2, 120.7, 4),
  ('agbor-woffice', 'Agbor', 'Agbor Auto Workshop Car Park', -108.3, 8.3, 3),
  ('agbor-fshop', 'Agbor', 'Agbor Filling Station Car Park', 110.3, 8, 3),
  ('agbor-shop3', 'Agbor', 'Ika Provisions Car Park', 24.7, -108.1, 3),
  ('agbor-shop4', 'Agbor', 'Boji-Boji Mini Mart Car Park', 118.7, -108.1, 3),
  ('agbor-shop5', 'Agbor', 'Alihame Stores Car Park', -43.1, 11.2, 3)
on conflict (id) do update set state = excluded.state, name = excluded.name, x = excluded.x, z = excluded.z, bays = excluded.bays;

do $$
declare
  old_ids text[] := array['asaba-1', 'asaba-2', 'warri-1', 'warri-2', 'ozoro-1', 'ozoro-2', 'agbor-1', 'agbor-2', 'asaba-3', 'asaba-4', 'asaba-5', 'asaba-6', 'asaba-7', 'asaba-8', 'warri-3', 'warri-4', 'warri-5', 'warri-6', 'warri-7', 'warri-8', 'ozoro-3', 'ozoro-4', 'ozoro-5', 'ozoro-6', 'ozoro-7', 'ozoro-8', 'agbor-3', 'agbor-4', 'agbor-5', 'agbor-6', 'agbor-7', 'agbor-8', 'asaba-9', 'asaba-10', 'warri-9', 'warri-10', 'warri-11', 'ozoro-9', 'agbor-9'];
  v record; np text; nb int; moved int := 0;
begin
  for v in select vv.id, vv.status, vv.park_id, p.state as pst, p.x as px, p.z as pz
             from vehicles vv join car_parks p on p.id = vv.park_id
            where vv.park_id = any(old_ids) order by vv.id loop
    np := null; nb := null;
    if v.status = 'stored' then
      select q.id, veh_free_bay(q.id) into np, nb from car_parks q
       where q.state = v.pst and not (q.id = any(old_ids)) and veh_free_bay(q.id) is not null
       order by (q.x - v.px) ^ 2 + (q.z - v.pz) ^ 2, q.id limit 1;
    end if;
    if np is null then
      select q.id into np from car_parks q where q.state = v.pst and not (q.id = any(old_ids))
       order by (q.x - v.px) ^ 2 + (q.z - v.pz) ^ 2, q.id limit 1;
      nb := null;
    end if;
    if np is null then raise exception 'No new car park in % for vehicle %', v.pst, v.id; end if;
    if v.status = 'stored' then update vehicles set park_id = np, bay = nb where id = v.id;
    else update vehicles set park_id = np, in_bay = null where id = v.id; end if;
    perform veh_log(null, v.id, 'park_moved', jsonb_build_object('from', v.park_id, 'to', np, 'bay', nb, 'status', v.status, 'by', 'supabase_compound_car_parks.sql'));
    moved := moved + 1;
  end loop;
  delete from car_parks c where c.id = any(old_ids) and not exists (select 1 from vehicles where park_id = c.id);
  raise notice 'Moved % car(s) to the new car parks', moved;
end $$;

commit;

-- check: every car is in a car park the game draws (this should list nothing)
select v.id, v.plate, v.park_id from vehicles v left join car_parks p on p.id = v.park_id where v.park_id is not null and p.id is null;
