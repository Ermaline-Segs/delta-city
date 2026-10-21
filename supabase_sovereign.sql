-- Delta City RP: the Audi R8 is replaced by the Sovereign GT.
--
-- Every car saved as an Audi becomes a Sovereign GT (same plate, owner, keys, garage space and damage), new cars are
-- Sovereign GTs, and the Chief Admin's "give a car" makes Sovereign GTs. Run this whole file once in the Supabase SQL
-- editor; running it again is safe (it only changes what is still an Audi).
--
-- (supabase_vehicles.sql has the same changes, for a database set up from scratch.)

alter table vehicles alter column model set default 'sovereign';
update vehicles set model = 'sovereign' where model = 'audi';

-- the Chief Admin's "give a car": the only model is now the Sovereign GT
do $$
declare src text;
begin
  select pg_get_functiondef(p.oid) into src from pg_proc p join pg_namespace n on n.oid = p.pronamespace
   where n.nspname = 'public' and p.proname = 'veh_admin_provision' limit 1;
  if src is null then raise notice 'veh_admin_provision is not in this database yet: run supabase_vehicles.sql'; return; end if;
  if position('''audi''' in src) > 0 then execute replace(src, '''audi''', '''sovereign'''); raise notice 'veh_admin_provision now gives Sovereign GTs'; end if;
end $$;

select model, count(*) from vehicles group by model;
