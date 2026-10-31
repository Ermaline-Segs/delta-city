# Repair bays — SQL Editor test checklist

## 0. Preconditions

1. The project has **supabase_services.sql** and **supabase_vehicles.sql** already applied. These create the required tables:
   - `characters`, `state_accounts`, `ledger`
   - `vehicles`, `vehicle_keys`, `car_parks`, `workshops`
   - the helper function `public.veh_can_drive`
2. If you are using a local stand‑in Postgres (not real Supabase), you also need the `auth.uid()` stub. It reads the same JWT claims real Supabase sets, so the same `set_config` line works everywhere:
    ```sql
    create schema if not exists auth;
    create or replace function auth.uid()
      returns uuid language sql stable as $$
        select (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')::uuid;
    $$;
    ```
    (On real Supabase `auth.uid()` already exists — skip this.)
3. Apply **supabase_repair_bays.sql** **twice**, back‑to‑back, with nothing in between:
   ```sql
   -- paste supabase_repair_bays.sql, run
   -- paste it again, run
   ```
   **Pass:** the second run finishes with zero errors – the file is idempotent.

## 1. Seed data

We will use four distinct players (UUIDs) and one vehicle per player.
```sql
-- characters (owner, name, cash)
insert into characters(owner, name, cash) values
  ('11111111-1111-1111-1111-111111111111', 'Ada', 500000),
  ('22222222-2222-2222-2222-222222222222', 'Bob', 500000),
  ('33333333-3333-3333-3333-333333333333', 'Cara', 500000),
  ('44444444-4444-4444-4444-444444444444', 'Dan', 500000)
  on conflict do nothing;

-- state account for the workshop (Asaba)
insert into state_accounts(state, balance) values ('Asaba', 1000000)
  on conflict (state) do update set balance = excluded.balance;

-- vehicles (explicit ids so the tests can name them; model defaults are fine)
insert into vehicles(id, plate, owner) values
  (9001, 'T-9001', '11111111-1111-1111-1111-111111111111'),
  (9002, 'T-9002', '22222222-2222-2222-2222-222222222222'),
  (9003, 'T-9003', '33333333-3333-3333-3333-333333333333'),
  (9004, 'T-9004', '44444444-4444-4444-4444-444444444444')
  on conflict (plate) do nothing;
select setval('vehicles_id_seq', (select max(id) from vehicles));

-- a key for each car too (ownership alone already lets the owner drive)
insert into vehicle_keys(vehicle_id, holder, granted_by) values
  (9001, '11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111'),
  (9002, '22222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222'),
  (9003, '33333333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-333333333333'),
  (9004, '44444444-4444-4444-4444-444444444444', '44444444-4444-4444-4444-444444444444')
  on conflict (vehicle_id, holder) where revoked_at is null do nothing;
```

## 2. Tests (run each as the indicated user)

### 2.1 Join with a free bay (Ada)
```sql
select set_config('request.jwt.claims', json_build_object('sub','11111111-1111-1111-1111-111111111111')::text, true);
select public.rep_join('asaba', 9001,
  '[{"k":"engine","price":75000,"mins":12}]'::jsonb, 12) as result;
```
**Pass:** `result -> ok:true`, `in_bay:true`, `price = 75000`, `cash` of Ada reduced to 425000, Asaba balance increased to 1 075 000, `queue` shows the car in bay 1.

### 2.2 One vehicle per player (Ada tries a second car)
```sql
-- insert a second vehicle for Ada
insert into vehicles(id, plate, owner) values (9005, 'T-9005', '11111111-1111-1111-1111-111111111111') on conflict (plate) do nothing;
insert into vehicle_keys(vehicle_id, holder, granted_by) values (9005, '11111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111') on conflict (vehicle_id, holder) where revoked_at is null do nothing;
select set_config('request.jwt.claims', json_build_object('sub','11111111-1111-1111-1111-111111111111')::text, true);
select public.rep_join('asaba', 9005, '[{"k":"brake","price":5000,"mins":5}]'::jsonb, 5);
```
**Pass:** error `You already have a car in a workshop queue or bay`.

### 2.3 Fill remaining bays (Bob and Cara)
```sql
-- Bob
select set_config('request.jwt.claims', json_build_object('sub','22222222-2222-2222-2222-222222222222')::text, true);
select public.rep_join('asaba', 9002, '[{"k":"tires","price":20000,"mins":8}]'::jsonb, 8);
-- Cara
select set_config('request.jwt.claims', json_build_object('sub','33333333-3333-3333-3333-333333333333')::text, true);
select public.rep_join('asaba', 9003, '[{"k":"paint","price":15000,"mins":6}]'::jsonb, 6);
```
**Pass:** both return `in_bay:true` with bays 2 and 3 respectively.

### 2.4 Fourth vehicle goes to the waiting list (Dan)
```sql
select set_config('request.jwt.claims', json_build_object('sub','44444444-4444-4444-4444-444444444444')::text, true);
select public.rep_join('asaba', 9004, '[{"k":"engine","price":80000,"mins":10}]'::jsonb, 10);
```
**Pass:** `in_bay:false`, `status='waiting'`, `queue` shows Dan at position 1.

### 2.5 Finish before `planned_until` (Ada)
```sql
select set_config('request.jwt.claims', json_build_object('sub','11111111-1111-1111-1111-111111111111')::text, true);
select public.rep_finish('asaba', 9001);
```
**Pass:** error `The repair is not finished yet; it is planned until …`.

### 2.6 Refund while waiting (Dan)
```sql
select set_config('request.jwt.claims', json_build_object('sub','44444444-4444-4444-4444-444444444444')::text, true);
select public.rep_leave('asaba', 9004);
```
**Pass:** `refunded` equals the price (80000), Dan's cash returns to 500000, Asaba balance is debited back, queue entry disappears, and the bay freed for the next waiting car (if any).

### 2.7 Double finish is a no‑op (Ada)
First fast‑forward time (or manually adjust) so the job is ready:
```sql
update repair_jobs set planned_until = now() - interval '1 minute'
  where vehicle_id = 9001 and workshop = 'asaba';
```
Now finish twice:
```sql
select set_config('request.jwt.claims', json_build_object('sub','11111111-1111-1111-1111-111111111111')::text, true);
select public.rep_finish('asaba', 9001) as first;
select public.rep_finish('asaba', 9001) as second;
```
**Pass:** first returns `ok:true, already:false`; second returns `ok:true, already:true` and does not change state.

### 2.8 Collect after finish (Ada)
```sql
select public.rep_collect('asaba', 9001);
```
**Pass:** car is removed from the bay, the bay becomes free, and the vehicle is stored in the workshop's car park.

### 2.9 Rights and RLS (anonymous user)

Run as the **anon** and **authenticated** roles — the file revokes the raw
tables from `anon` entirely and grants `SELECT` only to `authenticated`, so
reads must go through the player, and every write must go through the
`rep_*` functions:
```sql
-- anon: no access to the raw tables at all
set role anon;
select * from repair_queue limit 1;
-- expected error: permission denied for table repair_queue
reset role;

-- authenticated: can read, cannot write
set role authenticated;
select * from repair_queue limit 1;   -- works
insert into repair_queue(workshop, vehicle_id, owner) values ('asaba', 9001, '11111111-1111-1111-1111-111111111111');
-- expected error: permission denied for table repair_queue
reset role;
```
**Pass:** anon gets `permission denied` on the SELECT; authenticated reads
fine but the INSERT fails with `permission denied`.

## Scoring
All steps 0‑9 must succeed (green) and the double‑run in step 0 must be error‑free. Any failure should be reported with the exact error text, the SQL file fixed, and the checklist re‑run from step 0.
