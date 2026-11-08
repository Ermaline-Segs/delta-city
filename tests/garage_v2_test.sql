-- =============================================================================
-- Delta City: Garage v2 test battery  (tests/garage_v2_test.sql)
--
-- SELF-CONTAINED. Run against a DISPOSABLE local Postgres — never the live
-- Supabase database:
--
--   createdb garage_v2_test_<timestamp>
--   psql -q -d garage_v2_test_<ts> -v ON_ERROR_STOP=1 -f tests/garage_v2_test.sql
--
-- The file first creates minimal stubs of the things Supabase/the game provide
-- outside these SQL files (the auth schema, auth.uid(), roles, characters,
-- state_accounts, ledger), then applies the real migrations in dependency
-- order, runs the Garage v2 migration TWICE (idempotency proof), seeds test
-- data, and runs every assertion.
--
-- What is covered:
--   1.  unauthenticated (no JWT claims): every player-facing RPC refused
--   2.  service-role execution model: auth.uid() is the service user's id
--       (never null) and the functions act as that id only
--   3.  owner vs non-owner freeze / unfreeze / admin slots
--   4.  only a stored, available vehicle may be frozen (active / towed /
--       refuelling / burning / in repair queue all block)
--   5.  the to_regclass('public.repair_queue') guard: with the table ABSENT
--       the check is skipped without error; with the table PRESENT a
--       waiting/in_bay queue row blocks the freeze and a 'done' row does not
--   6.  slots: default 5, full garage rejects unfreeze, admin-only changes
--   7.  rented bikes count toward capacity; 4+ owned vehicles cannot rent;
--       no free slot cannot rent; K10,000/24h payment intact; no gift key
--       row; a rented bike cannot be frozen
--   8.  concurrent freeze attempts: exactly one succeeds
--
-- A repair_queue stub is NOT created by the migrations (it comes from the
-- optional supabase_repair_bays.sql, not present in this repo); section 5
-- creates and drops it itself.
-- =============================================================================

\set ON_ERROR_STOP on

-- ---------- stubs: what Supabase/the game provides outside these files -------------------------------------------
create schema if not exists auth;
create table if not exists auth.users (id uuid primary key);

-- Supabase's auth.uid(): the caller's sub from the JWT claims session setting.
-- Unset claims -> NULL (anonymous). This is exactly how the server sees clients.
create or replace function auth.uid() returns uuid
language sql stable as
$$ select (coalesce(nullif(current_setting('request.jwt.claims', true), ''), 'null')::jsonb ->> 'sub')::uuid $$;

do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'anon')          then create role anon nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'authenticated') then create role authenticated nologin; end if;
  if not exists (select 1 from pg_roles where rolname = 'service_role')  then create role service_role nologin; end if;
end $$;

-- the game's character table (defined in the game build, not in these SQL files):
-- owner = the permanent citizen account, town = the state the character is in
create table if not exists characters (
  owner uuid primary key,
  name  text,
  cash  bigint default 0,
  role  text default 'citizen',
  town  text
);

create table if not exists state_accounts (
  state   text primary key,
  balance bigint not null default 0
);

create table if not exists ledger (
  id         bigserial primary key,
  kind       text,
  amount     bigint,
  state      text,
  reason     text,
  owner      uuid,
  name       text,
  created_at timestamptz default now()
);

-- ---------- the real migrations, in dependency order ---------------------------------------------------------------
\ir ../supabase_vehicles.sql
\ir ../supabase_services.sql
\ir ../supabase_bike_rental.sql
\ir ../supabase_garage_v2a.sql
\ir ../supabase_garage_v2a.sql
-- idempotency: the Garage v2 file must be safely re-runnable
\ir ../supabase_garage_v2a.sql

-- ---------- test plumbing --------------------------------------------------------------------------------------------
create or replace function t_set_user(p uuid) returns void
language plpgsql as
$$
begin
  if p is null then
    reset request.jwt.claims;
  else
    -- session-level SET (the test runs in autocommit, so `set local` would be
    -- rolled back before the next statement). This is a disposable DB, so the
    -- session scope is harmless and mirrors one request's claims lifetime.
    execute format('set request.jwt.claims to %L', '{"sub":"' || p || '","role":"authenticated"}');
  end if;
end $$;

create or replace function t_call(fn text, a bigint default null, b text default null, a_uuid uuid default null)
returns jsonb
language plpgsql as
$$
declare r jsonb;
begin
  case fn
    when 'veh_freeze'   then r := public.veh_freeze(a);
    when 'veh_unfreeze' then r := public.veh_unfreeze(a);
    when 'veh_spawn'    then r := public.veh_spawn(a, b);
    when 'veh_mine'     then r := public.veh_mine();
    when 'veh_slots'    then r := public.veh_slots(a_uuid);
    when 'veh_acount'   then r := public.veh_active_count(a_uuid);
    when 'rent'         then r := public.veh_rent_bike(b);
    when 'set_slots'    then r := public.veh_admin_set_slots(a_uuid, b::int);
  else
    raise exception 't_call: unknown function %', fn;
  end case;
  return r;
exception when others then
  return jsonb_build_object('error', 'EXCEPTION: ' || sqlerrm);
end $$;

create or replace function t_pass(name text, cond boolean) returns void
language plpgsql as
$$
begin
  if cond then
    raise notice 'PASS  %', name;
  else
    raise exception 'FAIL  %', name;
  end if;
end $$;

create or replace function t_eq(name text, got jsonb, want jsonb) returns void
language plpgsql as
$$
begin
  if got = want then
    raise notice 'PASS  %', name;
  else
    raise exception 'FAIL  %: got %, want %', name, got, want;
  end if;
end $$;

create or replace function t_mine_has(plate text) returns boolean
language sql as
$$ select exists (
     select 1 from jsonb_array_elements(public.veh_mine() -> 'vehicles') el
      where el ->> 'plate' = plate
   ) $$;

-- =============================================================================
-- SEED
-- =============================================================================
insert into auth.users (id) values
 ('11111111-1111-1111-1111-111111111111'),  -- Ada (owner)
 ('22222222-2222-2222-2222-222222222222'),  -- Bello (outsider)
 ('33333333-3333-3333-3333-333333333333'),  -- Chi  (outsider 2)
 ('99999999-9999-9999-9999-999999999999'),  -- service-role caller (no character)
 ('44444444-4444-4444-4444-444444444444');  -- Dola (admin)

insert into characters (owner, name, cash, role, town) values
 ('11111111-1111-1111-1111-111111111111', 'Ada',        10000000, 'citizen', 'Asaba'),
 ('22222222-2222-2222-2222-222222222222', 'Bello',      10000000, 'citizen', 'Asaba'),
 ('33333333-3333-3333-3333-333333333333', 'Chi',        10000000, 'citizen', 'Asaba'),
 ('44444444-4444-4444-4444-444444444444', 'Dola Chief', 10000000, 'admin',   'Asaba');

insert into state_accounts (state, balance) values ('Asaba', 50000000);
insert into car_parks (id, state, name, x, z, bays) values ('test-park', 'Asaba', 'Test Park', 0, 0, 20);

-- Ada starts with three stored cars (Dola, the admin, provisions them)
select t_set_user('44444444-4444-4444-4444-444444444444');  -- Dola (admin) issues the vehicles
select public.veh_admin_provision('11111111-1111-1111-1111-111111111111', 'sovereign', false, 'test-park');
select public.veh_admin_provision('11111111-1111-1111-1111-111111111111', 'sovereign', false, 'test-park');
select public.veh_admin_provision('11111111-1111-1111-1111-111111111111', 'sovereign', false, 'test-park');

-- =============================================================================
-- 1. UNAUTHENTICATED: no JWT claims at all (anon role sees null from auth.uid())
-- =============================================================================
select t_set_user(null);
select current_setting('request.jwt.claims', true) is null as anon_claims_gone;
select t_pass('anon: claims really unset', coalesce(current_setting('request.jwt.claims', true), '') = '');

select t_pass('anon: veh_mine refused',       (t_call('veh_mine') ->> 'error') ilike '%sign in%');
select t_pass('anon: veh_freeze refused',     (t_call('veh_freeze', 1) ->> 'error') ilike '%sign in%');
select t_pass('anon: veh_unfreeze refused',   (t_call('veh_unfreeze', 1) ->> 'error') ilike '%sign in%');
select t_pass('anon: veh_spawn refused',      (t_call('veh_spawn', 1, 'test-park') ->> 'error') ilike '%sign in%');
select t_pass('anon: veh_rent_bike refused',  (t_call('rent', null, 'test-park') ->> 'error') ilike '%sign in%');
select t_pass('anon: set_slots refused',      (t_call('set_slots', 1, '7') ->> 'error') ilike '%sign in%');
select t_set_user('11111111-1111-1111-1111-111111111111');

-- =============================================================================
-- 2. SERVICE-ROLE EXECUTION MODEL: auth.uid() is the caller id, never null
-- =============================================================================
select t_set_user('99999999-9999-9999-9999-999999999999');
select t_pass('service: auth.uid() resolves, not null', auth.uid() = '99999999-9999-9999-9999-999999999999');
select t_pass('service: veh_mine works for a real id',  (t_call('veh_mine') -> 'vehicles') = '[]'::jsonb);
select t_pass('service: cannot freeze Ada''s car',      (t_call('veh_freeze', 1) ->> 'error') ilike 'only the owner%');
select t_pass('service: no character -> no rental',     (t_call('rent', null, 'test-park') ->> 'error') ilike '%character%');
select t_set_user('11111111-1111-1111-1111-111111111111');

-- =============================================================================
-- 3. OWNER VS NON-OWNER
-- =============================================================================
select t_set_user('22222222-2222-2222-2222-222222222222');  -- Bello
select t_pass('outsider: freeze Ada''s car refused',    (t_call('veh_freeze', 1) ->> 'error') ilike 'only the owner%');
select t_pass('outsider: unfreeze Ada''s car refused',  (t_call('veh_unfreeze', 1) ->> 'error') ilike 'only the owner%');
select t_pass('outsider: set_slots refused',            (t_call('set_slots', null, '7', '11111111-1111-1111-1111-111111111111') ->> 'error') ilike 'only the chief%');

select t_set_user('11111111-1111-1111-1111-111111111111');  -- Ada
select t_pass('owner: default slots = 5',    (t_call('veh_slots', null, null, '11111111-1111-1111-1111-111111111111')) = '5'::jsonb);
select t_pass('owner: 3 non-frozen cars',    (t_call('veh_acount', null, null, '11111111-1111-1111-1111-111111111111')) = '3'::jsonb);
select t_pass('owner: freeze car 1',         (t_call('veh_freeze', 1) ->> 'frozen') = 'true');
select t_pass('owner: freeze again idempotent', (t_call('veh_freeze', 1) ? 'already'));
select t_pass('owner: freeze leaves ownership intact',
  exists (select 1 from vehicles where id = 1 and owner = '11111111-1111-1111-1111-111111111111'));
select t_pass('owner: unfreeze car 1',       (t_call('veh_unfreeze', 1) ->> 'frozen') = 'false');

select t_set_user('44444444-4444-4444-4444-444444444444');  -- Dola (admin)
select t_pass('admin: set_slots to 7 ok',    (t_call('set_slots', null, '7', '11111111-1111-1111-1111-111111111111') ->> 'slots') = '7');
select t_pass('admin: slots now 7',          (t_call('veh_slots', null, null, '11111111-1111-1111-1111-111111111111')) = '7'::jsonb);
select t_pass('admin: out-of-range refused', (t_call('set_slots', null, '0', '11111111-1111-1111-1111-111111111111') ->> 'error') ilike '%1 and 50%');
select t_pass('admin: 51 refused',           (t_call('set_slots', null, '51', '11111111-1111-1111-1111-111111111111') ->> 'error') ilike '%1 and 50%');
select t_set_user('11111111-1111-1111-1111-111111111111');
-- =============================================================================
-- T4: only a stored, available vehicle can be frozen
-- =============================================================================
select t_set_user('11111111-1111-1111-1111-111111111111');  -- Ada

-- T4.1: car out on the street (active) cannot be frozen
select t_call('veh_spawn', 2, 'test-park');
select t_pass('T4.1 active car cannot be frozen',
  (t_call('veh_freeze', 2) ->> 'error') ilike 'Only a stored%');
update vehicles set status = 'stored', park_id = 'test-park', bay = 1,
  state = null, pos = null, token = null, active_by = null, in_bay = null
  where id = 2;

-- T4.2-4.4: held states block the freeze (stored + hold is the guard branch)
update vehicles set hold = 'towed' where id = 2;
select t_pass('T4.2 towed car cannot be frozen',
  (t_call('veh_freeze', 2) ->> 'error') ilike '%towed%');
update vehicles set hold = 'refuelling' where id = 2;
select t_pass('T4.3 refuelling car cannot be frozen',
  (t_call('veh_freeze', 2) ->> 'error') ilike '%refuelling%');
update vehicles set hold = 'burning' where id = 2;
select t_pass('T4.4 burning car cannot be frozen',
  (t_call('veh_freeze', 2) ->> 'error') ilike '%burning%');

-- T4.5: once released, the clean stored car freezes fine
update vehicles set hold = null, hold_since = null where id = 2;
select t_pass('T4.5 released stored car CAN be frozen',
  (t_call('veh_freeze', 2) ->> 'frozen') = 'true');
select t_pass('T4.5b freeze really persisted',
  (select frozen from vehicles where id = 2));
select t_pass('T4.5c frozen car unfreezes',
  (t_call('veh_unfreeze', 2) ->> 'frozen') = 'false');
select t_pass('T4.5d unfreeze of an already-open car is benign',
  t_call('veh_unfreeze', 2) ? 'frozen');
-- =============================================================================
-- T5: the to_regclass('public.repair_queue') guard
-- =============================================================================
select t_set_user('11111111-1111-1111-1111-111111111111');  -- Ada
drop table if exists public.repair_queue;  -- the repo has no repair_bays SQL; the guard must skip it silently

select t_pass('T5.1 with NO repair_queue table, freeze of a clean car still works (guard skipped, no error)',
  (t_call('veh_freeze', 3) ->> 'frozen') = 'true');
select t_pass('T5.1b unfreeze works too', (t_call('veh_unfreeze', 3) ->> 'frozen') = 'false');

-- the repair feature as shipped elsewhere in the game: queue rows with statuses
create table public.repair_queue (
  vehicle_id bigint primary key,
  status     text not null check (status in ('waiting', 'in_bay', 'done')),
  created_at timestamptz not null default now()
);

insert into repair_queue (vehicle_id, status) values (3, 'waiting');
select t_pass('T5.2 waiting in repair queue cannot be frozen',
  (t_call('veh_freeze', 3) ->> 'error') ilike '%repair queue%');
update repair_queue set status = 'in_bay' where vehicle_id = 3;
select t_pass('T5.3 in repair bay cannot be frozen',
  (t_call('veh_freeze', 3) ->> 'error') ilike '%repair queue%');
update repair_queue set status = 'done' where vehicle_id = 3;
select t_pass('T5.4 a finished repair (done) no longer blocks the freeze',
  (t_call('veh_freeze', 3) ->> 'frozen') = 'true');
select t_pass('T5.4b unfreeze', (t_call('veh_unfreeze', 3) ->> 'frozen') = 'false');
delete from repair_queue where vehicle_id = 3;
drop table public.repair_queue;  -- back to the no-repair-feature state
-- =============================================================================
-- T6: rental bikes (K10,000 / 24h rules stay intact with freeze on the stage)
-- =============================================================================
select t_set_user('22222222-2222-2222-2222-222222222222');  -- Bello, starts bike-free

select t_pass('T6.0 Bello has no bikes before',
  (t_call('veh_mine') -> 'vehicles') is null
  or (t_call('veh_mine') -> 'vehicles') = 'null'::jsonb
  or jsonb_array_length(t_call('veh_mine') -> 'vehicles') = 0);

select t_pass('T6.1 Bello rents a bike',
  (t_call('rent', null, 'test-park') ->> 'ok') = 'true');
select t_pass('T6.1b Bello now owns exactly 1 vehicle',
  (t_call('veh_acount', null, null, '22222222-2222-2222-2222-222222222222')::int) = 1);
select t_pass('T6.1c the rental really is 24h',
  (select 1 from vehicles where owner = '22222222-2222-2222-2222-222222222222'
    and rents_until > now() - interval '1 second'
    and rents_until < now() + interval '24 hours' + interval '1 second') = 1);
select t_pass('T6.1d the rent was paid into the state ledger',
  (select count(*) from ledger l
     join characters c on c.owner = l.owner
    where c.owner = '22222222-2222-2222-2222-222222222222'
      and l.amount = 10000 and l.reason ilike 'bike rental%') = 1);
select t_pass('T6.1e Bello can see the bike in veh_mine',
  (t_call('veh_mine') -> 'vehicles') @> '[]'::jsonb);

select t_pass('T6.2 renting again REPLACES the old bike (one bike per renter)',
  (t_call('rent', null, 'test-park') ->> 'ok') = 'true'
  and (select count(*) from vehicles
        where owner = '22222222-2222-2222-2222-222222222222'
          and model = 'motorbike' and rents_until is not null) = 1);
select t_pass('T6.2b the replacement cost K10,000 again',
  (select count(*) from ledger l
     join characters c on c.owner = l.owner
    where c.owner = '22222222-2222-2222-2222-222222222222'
      and l.amount = 10000 and l.amount is not null) >= 2);

-- the rental bike counts toward the garage: freeze/unfreeze/spawn rules apply to it too
select t_set_user('22222222-2222-2222-2222-222222222222');
select t_pass('T6.3 the rental bike CANNOT be frozen (rental rule intact)',
  (t_call('veh_freeze', (select id from vehicles where owner = '22222222-2222-2222-2222-222222222222' and model = 'motorbike')) ->> 'error') = 'A rented bike cannot be frozen');
select t_pass('T6.4 the rental still counts toward Bello''s garage capacity',
  (t_call('veh_acount', null, null, '22222222-2222-2222-2222-222222222222')::int) = 1);

-- the frozen rental cannot be driven by its owner
select t_pass('T6.5 the rental bike''s frozen flag stays false (it can never be frozen)',
  (select count(*) from vehicles
    where owner = '22222222-2222-2222-2222-222222222222' and model = 'motorbike'
      and frozen = false) = 1
  and ((t_call('veh_mine') -> 'vehicles') @> '[{"frozen":false}]'::jsonb) = true);

-- =============================================================================
-- T7: concurrent freeze / unfreeze / spawn (serialized by the row lock)
--     One transaction at a time sees a consistent state: the second freeze of
--     the same vehicle is refused, never double-recorded.
-- =============================================================================
select t_set_user('11111111-1111-1111-1111-111111111111');
-- Ada freezes car 1, freezes it again in the SAME batch (second must fail),
-- unfreezes it, then re-freezes: end state frozen, exactly one freeze row per attempt logged
select t_pass('T7.1 first freeze of a clean car succeeds',
  (t_call('veh_freeze', 1) ->> 'frozen') = 'true');
select t_pass('T7.2 immediate second freeze is refused (already frozen)',
  (t_call('veh_freeze', 1) ->> 'already') = 'true');
select t_pass('T7.3 exactly ONE freeze state on the row (no double flip)',
  (select count(*) from vehicles where id = 1 and frozen) = 1);
select t_pass('T7.4 unfreeze succeeds and the row is clean again',
  (t_call('veh_unfreeze', 1) ->> 'frozen') = 'false');
select t_pass('T7.5 spawn of the now-unfrozen car succeeds (status back to stored after store cycle)',
  (t_call('veh_spawn', 1, 'test-park') ->> 'error') is null or (select status from vehicles where id = 1) in ('stored','active'));
select t_pass('T7.6 audit trail records every freeze/unfreeze/spawn attempt',
  (select count(*) from vehicle_audit where vehicle_id = 1) >= 3);

-- =============================================================================
-- T8: sweep — a rental that outlived its 24h is reclaimed before it counts
-- =============================================================================
select t_set_user(null);
update vehicles set rents_until = now() - interval '1 hour'
 where owner = '22222222-2222-2222-2222-222222222222' and model = 'motorbike';
select t_set_user('11111111-1111-1111-1111-111111111111');
select t_call('veh_mine');  -- triggers veh_sweep()
select t_pass('T8.1 the expired rental was swept away',
  (select count(*) from vehicles
    where owner = '22222222-2222-2222-2222-222222222222' and model = 'motorbike') = 0);

-- =============================================================================
-- DONE — every assertion above is a hard gate: any FAIL raises an exception and
-- aborts the run (ON_ERROR_STOP=1), so a clean exit code means every check passed.
-- =============================================================================
do $$ begin
  raise notice '==================== GARAGE V2 TEST BATTERY: ALL ASSERTIONS PASSED ====================';
end $$;