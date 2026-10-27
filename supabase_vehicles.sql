-- Delta City RP: owned vehicles, car parks, spawning and despawning, and keys.
--
-- Run the whole file once in the Supabase SQL editor. Running it again is safe.
--
-- What it adds (nothing that exists is changed):
--   * veh_cfg(): every number in one place (how far the owner may walk away, how long a car may stand abandoned, ...).
--   * car_parks: the car parks in each state (every public building's own, inside its compound, and the lay-bys by
--     roadside shops) and how many bays each has. The game draws them at the same places.
--   * vehicles: one row per vehicle, with a unique id and plate, its owner (the citizen's permanent account id, the same
--     as characters.owner), where it is (stored in a car park bay, or out on the road), and its damage.
--   * vehicle_keys: who else may drive a vehicle (one row per vehicle and citizen; revoking keeps the row, dated).
--   * vehicle_audit: every spawn, store, despawn, key change, paid repair and admin action, with who did it and when.
--   * Functions the game calls. Only these functions touch the tables (they check who is calling with auth.uid()):
--       veh_mine, veh_spawn, veh_update, veh_store, veh_despawn, veh_pay, veh_find_citizen, veh_key_give,
--       veh_key_revoke, veh_admin_provision, veh_admin_list.
--
-- The rules the server enforces:
--   * A new citizen gets no vehicle. Vehicles are only created by the Chief Admin (veh_admin_provision); the special
--     Chief Admin vehicle can only be given to a Chief Admin account.
--   * A vehicle can only be brought out of the car park it is stored in, by its owner or someone holding its keys,
--     and only if it is not already out: the row is locked while this is checked, so two phones pressing "Retrieve"
--     at the same moment get one car between them. Each citizen can have one vehicle out at a time.
--   * Every message about a vehicle that is out carries the secret token handed out when it was spawned. A stale or
--     copied token is refused, so there is only ever one live copy of each vehicle.
--   * A vehicle can only be stored in a real bay of a real car park, near that car park, in a bay nobody else is using.
--   * Rule A: if the person who brought the car out is more than despawn_distance_m from it, or in another state,
--     the car is put away (sent back to a car park).
--   * Rule B: a car left outside a car park with nobody in it is put away abandon_s (15 minutes) after it was left,
--     timed by the server's clock. A car stored in a car park bay never despawns.
--   * Safety: a car being towed, repaired, refuelled or on fire is not put away (for at most hold_max_s), and a car with
--     someone in it is not put away while their game keeps reporting in.
--   * Damage is kept through despawning and spawning. The server never lets damage go down (or fuel and oil go up)
--     unless that repair or refuel was paid for through veh_pay first.

create or replace function public.veh_cfg()
returns jsonb language sql immutable set search_path = public as $$
  select jsonb_build_object(
    'despawn_distance_m', 250,    -- Rule A: the driver walks further than this from the car (or leaves the state)
    'abandon_s',          900,    -- Rule B: 15 minutes standing outside a car park with nobody in it
    'stale_s',            300,    -- a car whose game stops reporting for this long counts as left where it was
    'hold_max_s',         3600,   -- towing, a repair, refuelling or a fire delays despawning for at most this long
    'park_radius_m',      22,     -- how close to a car park's centre a car must be to be stored there
    'credit_s',           7200)   -- a paid repair may be applied to the car within this many seconds
$$;

create table if not exists car_parks (
  id     text primary key,
  state  text not null,
  name   text not null,
  x      numeric not null,
  z      numeric not null,
  bays   int not null check (bays > 0)
);
-- every public building's own car park, inside its compound (and the lay-bys beside roadside shops); the game draws them at the same places
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

create sequence if not exists vehicle_plate_seq;

create table if not exists vehicles (
  id           bigserial primary key,
  plate        text not null unique,
  owner        uuid not null,                         -- characters.owner: the citizen's permanent account id
  model        text not null default 'sovereign',
  special      boolean not null default false,        -- the Chief Admin's special vehicle
  status       text not null default 'stored' check (status in ('stored', 'active')),
  park_id      text references car_parks(id),         -- stored: the car park it is in; active: the one it came from
  bay          int,                                   -- stored: its bay (null: waiting at the car park office for a bay)
  state        text,                                  -- active: the state it is out in
  pos          jsonb,                                 -- active: {x, z, yaw}, as last reported
  damage       jsonb not null default '{}'::jsonb,
  token        uuid,                                  -- active: the secret of the one live copy
  active_by    uuid,                                  -- active: who brought it out (the owner or a key holder)
  occupied     boolean not null default false,
  in_bay       int,                                   -- active: standing in this bay of park_id (then it never despawns)
  hold         text,                                  -- active: tow / repair / refuel / fire
  hold_since   timestamptz,
  abandoned_at timestamptz,                           -- active: when it was last left outside a car park
  spawned_at   timestamptz,
  last_seen    timestamptz,
  credit       jsonb not null default '{}'::jsonb,    -- paid repairs not yet applied: {field: paid_until_epoch}
  created_at   timestamptz not null default now(),
  created_by   uuid
);
-- the Audi R8 has left the game: every car saved as one is now the Sovereign GT (safe to run again)
alter table vehicles alter column model set default 'sovereign';
update vehicles set model = 'sovereign' where model = 'audi';

create index if not exists vehicles_owner on vehicles (owner);
create index if not exists vehicles_active on vehicles (status) where status = 'active';
create unique index if not exists vehicles_one_per_bay on vehicles (park_id, bay) where status = 'stored' and bay is not null;
create unique index if not exists vehicles_one_out_each on vehicles (active_by) where status = 'active';

create table if not exists vehicle_keys (
  id          bigserial primary key,
  vehicle_id  bigint not null references vehicles(id) on delete cascade,
  holder      uuid not null,
  granted_by  uuid not null,
  granted_at  timestamptz not null default now(),
  revoked_at  timestamptz,
  revoked_by  uuid
);
create unique index if not exists vehicle_keys_live on vehicle_keys (vehicle_id, holder) where revoked_at is null;

create table if not exists vehicle_audit (
  id          bigserial primary key,
  at          timestamptz not null default now(),
  actor       uuid,
  vehicle_id  bigint,
  action      text not null,
  detail      jsonb not null default '{}'::jsonb
);
create index if not exists vehicle_audit_vehicle on vehicle_audit (vehicle_id, at);

alter table car_parks enable row level security;
alter table vehicles enable row level security;
alter table vehicle_keys enable row level security;
alter table vehicle_audit enable row level security;
revoke all on car_parks, vehicles, vehicle_keys, vehicle_audit from anon, authenticated;

-- ------------------------------------------------------------------------------------------------ helpers

create or replace function public.veh_log(p_actor uuid, p_vehicle bigint, p_action text, p_detail jsonb)
returns void language sql security definer set search_path = public as $$
  insert into vehicle_audit(actor, vehicle_id, action, detail) values (p_actor, p_vehicle, p_action, coalesce(p_detail, '{}'::jsonb))
$$;

create or replace function public.veh_role(p_owner uuid)
returns text language sql stable security definer set search_path = public as $$
  select role from characters where owner = p_owner limit 1
$$;

-- may this citizen drive this vehicle? (its owner, or someone holding keys that have not been taken back)
create or replace function public.veh_can_drive(p_vehicle bigint, p_who uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select exists(select 1 from vehicles where id = p_vehicle and owner = p_who)
      or exists(select 1 from vehicle_keys where vehicle_id = p_vehicle and holder = p_who and revoked_at is null)
$$;

-- the first free bay in a car park, or null when it is full
create or replace function public.veh_free_bay(p_park text)
returns int language sql stable security definer set search_path = public as $$
  select b from car_parks p, generate_series(0, p.bays - 1) b
   where p.id = p_park
     and not exists(select 1 from vehicles v where v.status = 'stored' and v.park_id = p_park and v.bay = b)
     and not exists(select 1 from vehicles v where v.status = 'active' and v.park_id = p_park and v.in_bay = b)
   order by b limit 1
$$;

-- a damage value as a number (true counts as 1), or null
create or replace function public.veh_num(j jsonb)
returns numeric language sql immutable set search_path = public as $$
  select case jsonb_typeof(j) when 'number' then j::text::numeric when 'boolean' then case when j::text = 'true' then 1 else 0 end end
$$;

-- the newly reported damage, kept honest: a part can only get worse, fuel and oil and coolant can only go down, and a
-- burnt-out or dead car stays so, unless the field was paid for (credit). Everything else (temperature, the fire's
-- progress, the mechanic's job, ...) is taken as reported.
create or replace function public.veh_merge_damage(p_old jsonb, p_new jsonb, p_credit jsonb)
returns jsonb language plpgsql stable set search_path = public as $$
declare out_ jsonb := coalesce(p_old, '{}'::jsonb) || coalesce(p_new, '{}'::jsonb); o jsonb := coalesce(p_old, '{}'::jsonb); c jsonb := coalesce(p_credit, '{}'::jsonb);
        k text; i int; arr jsonb; ov numeric; nv numeric; paid boolean; nowe numeric := extract(epoch from now());
begin
  if o = '{}'::jsonb then return out_; end if;
  foreach k in array array['bumperF','bumperR','bonnet','grille','trunk','sideL','sideR','hlL','hlR','tlL','tlR','radiator','engine',
                           'susp','chassis','under','oilLeak','fuelLeak','elec','steer','ws','rw','winL','winR','burnt','hlL','hlR','tlL','tlR'] loop
    paid := coalesce(veh_num(c->k), 0) > nowe;
    ov := coalesce(veh_num(o->k), 0); nv := coalesce(veh_num(out_->k), ov);
    if not paid and nv < ov then out_ := jsonb_set(out_, array[k], o->k); end if;
  end loop;
  foreach k in array array['coolant','oil','fuel'] loop
    paid := coalesce(veh_num(c->k), 0) > nowe;
    ov := coalesce(veh_num(o->k), 1); nv := coalesce(veh_num(out_->k), ov);
    if not paid and nv > ov then out_ := jsonb_set(out_, array[k], to_jsonb(ov)); end if;
  end loop;
  foreach k in array array['tyre','flat','rim'] loop
    arr := coalesce(out_->k, o->k, '[0,0,0,0]'::jsonb);
    for i in 0..3 loop
      paid := coalesce(veh_num(c->('ty' || i)), 0) > nowe;
      ov := coalesce(veh_num(o->k->i), 0); nv := coalesce(veh_num(arr->i), ov);
      if not paid and nv < ov then arr := jsonb_set(arr, array[i::text], to_jsonb(ov)); end if;
    end loop;
    out_ := jsonb_set(out_, array[k], arr);
  end loop;
  if coalesce((o->>'dead')::boolean, false) and not coalesce((out_->>'dead')::boolean, false)
     and not exists(select 1 from jsonb_each(c) e where e.key in ('engine', 'chassis', 'susp', 'burnt', 'elec', 'dead') and veh_num(e.value) > nowe) then
    out_ := jsonb_set(out_, '{dead}', 'true'::jsonb);
  end if;
  return out_;
end $$;

-- a vehicle out on the road is put away: back into a bay of the car park it came from (or another in that state, or
-- the car park office when every bay is taken), with its damage kept. The caller holds the row lock.
create or replace function public.veh_put_away(p_vehicle bigint, p_actor uuid, p_reason text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v vehicles; pk text; b int;
begin
  select * into v from vehicles where id = p_vehicle;
  if v.status <> 'active' then return jsonb_build_object('park', v.park_id, 'bay', v.bay); end if;
  pk := v.park_id; b := null;
  if v.in_bay is not null then b := v.in_bay; end if;
  -- clear this car's place first so its own bay counts as free
  update vehicles set status = 'stored', bay = null, in_bay = null, token = null, active_by = null, occupied = false, hold = null,
         hold_since = null, abandoned_at = null, pos = null, state = null where id = v.id;
  if b is null and pk is not null then b := veh_free_bay(pk); end if;
  if b is null then
    select p.id, veh_free_bay(p.id) into pk, b from car_parks p
     where p.state = coalesce(v.state, (select state from car_parks where id = v.park_id)) and veh_free_bay(p.id) is not null
     order by p.id limit 1;
    if pk is null then pk := v.park_id; end if;
  end if;
  update vehicles set park_id = pk, bay = b where id = v.id;
  perform veh_log(p_actor, v.id, 'despawn', jsonb_build_object('reason', p_reason, 'park', pk, 'bay', b, 'pos', v.pos, 'state', v.state));
  return jsonb_build_object('park', pk, 'bay', b);
end $$;

-- the server's own sweep: Rule B (abandoned for 15 minutes, by the server's clock), cars whose game stopped reporting,
-- and Rule A for a driver who is now in another state. Runs whenever anyone's game calls in.
create or replace function public.veh_sweep()
returns int language plpgsql security definer set search_path = public as $$
declare cfg jsonb := veh_cfg(); v record; n int := 0; held boolean; left_at timestamptz; who_state text;
begin
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
    'keys', case when v.owner = p_me then (select coalesce(jsonb_agg(jsonb_build_object('holder', k.holder, 'name', c.name, 'since', k.granted_at) order by k.granted_at), '[]'::jsonb)
                                            from vehicle_keys k left join characters c on c.owner = k.holder where k.vehicle_id = v.id and k.revoked_at is null) end)
$$;

-- ------------------------------------------------------------------------------------------------ for the game

-- my vehicles and the ones I hold keys to, the car parks, the settings and the server's clock
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
                  where v.owner = me or exists(select 1 from vehicle_keys k where k.vehicle_id = v.id and k.holder = me and k.revoked_at is null)));
end $$;

-- why a vehicle that is out cannot be moved right now (someone is driving it, it is being towed, repaired, refuelled or is
-- burning), or null when it can be. A game that has stopped reporting does not count as someone driving.
create or replace function public.veh_busy(v vehicles)
returns text language sql stable security definer set search_path = public as $$
  select case
    when v.status <> 'active' then null
    when v.occupied and v.last_seen > now() - make_interval(secs => (veh_cfg()->>'stale_s')::numeric) then 'someone is driving it right now'
    when v.hold is not null and v.hold_since > now() - make_interval(secs => (veh_cfg()->>'hold_max_s')::numeric) then
      case v.hold when 'tow' then 'it is being towed' when 'repair' then 'it is being repaired at the workshop'
                  when 'refuel' then 'it is being refuelled' when 'fire' then 'it is on fire' else 'it is in use' end
  end
$$;

-- spawn one of my vehicles (or one I hold keys to) in a free bay of this car park. Wherever the vehicle is - stored in
-- another car park, or out on the road - it is moved here: the old copy is put away first (its token stops working, so
-- it disappears from the game that had it) and its damage, fuel and the rest come with it. All of this happens under
-- the vehicle's row lock, so two requests at once (two taps, two phones) can never make two copies. A second request
-- for a car already standing in this car park just returns it. Each citizen has one vehicle out: another of theirs
-- that is out is put away first. Refused (with the reason) when someone is driving the car, it is being towed,
-- repaired or refuelled, or it is burning. Returns {vehicle, moved_from} or {error}.
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

-- the game reports on a vehicle that is out (every few seconds while it is, and when something happens). Returns
-- {ok, now, abandoned_at} or {gone: why} when this copy is no longer the live one or was put away.
create or replace function public.veh_update(p_vehicle bigint, p_token uuid, p_pos jsonb, p_damage jsonb, p_occupied boolean,
                                             p_park text, p_in_bay int, p_hold text, p_owner_dist numeric, p_state text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); cfg jsonb := veh_cfg(); v vehicles; r jsonb; pk car_parks; bay_ int := p_in_bay;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or v.status <> 'active' or v.token is distinct from p_token or v.active_by <> me then
    return jsonb_build_object('gone', 'This car has been put away', 'now', now());
  end if;
  v.damage := veh_merge_damage(v.damage, p_damage, v.credit);
  -- keys taken back: the car is put away with its damage
  if not veh_can_drive(v.id, me) then
    update vehicles set damage = v.damage where id = v.id;
    r := veh_put_away(v.id, me, 'keys revoked');
    return jsonb_build_object('gone', 'You do not have the keys to this vehicle', 'now', now(), 'park', r);
  end if;
  -- standing in a bay only counts in a real, free bay of the car park nearby
  if bay_ is not null then
    select * into pk from car_parks where id = coalesce(p_park, v.park_id);
    if pk.id is null or bay_ < 0 or bay_ >= pk.bays or p_pos is null
       or sqrt(power((p_pos->>'x')::numeric - pk.x, 2) + power((p_pos->>'z')::numeric - pk.z, 2)) > (cfg->>'park_radius_m')::numeric
       or coalesce(p_state, v.state) <> pk.state
       or exists(select 1 from vehicles o where o.id <> v.id and o.park_id = pk.id
                   and ((o.status = 'stored' and o.bay = bay_) or (o.status = 'active' and o.in_bay = bay_))) then
      bay_ := null;
    end if;
  end if;
  update vehicles set pos = coalesce(p_pos, pos), damage = v.damage, occupied = coalesce(p_occupied, false), in_bay = bay_,
         park_id = case when bay_ is not null then pk.id else park_id end,
         state = coalesce(p_state, state), last_seen = now(),
         hold = case when p_hold in ('tow', 'repair', 'refuel', 'fire') then p_hold end,
         hold_since = case when p_hold in ('tow', 'repair', 'refuel', 'fire') then coalesce(case when hold = p_hold then hold_since end, now()) end,
         abandoned_at = case when coalesce(p_occupied, false) or bay_ is not null then null else coalesce(abandoned_at, now()) end
   where id = v.id returning * into v;
  -- Rule A (reported by the game) and Rule B (the server's clock), unless the car is held for safety
  if v.hold is null or v.hold_since <= now() - make_interval(secs => (cfg->>'hold_max_s')::numeric) then
    if p_owner_dist is not null and p_owner_dist > (cfg->>'despawn_distance_m')::numeric and not v.occupied then
      r := veh_put_away(v.id, me, 'driver walked away');
      return jsonb_build_object('gone', 'You walked too far from your car, so it was taken back to the car park', 'now', now(), 'park', r);
    end if;
    if v.abandoned_at is not null and v.abandoned_at <= now() - make_interval(secs => (cfg->>'abandon_s')::numeric) then
      r := veh_put_away(v.id, me, 'abandoned');
      return jsonb_build_object('gone', 'Your car was left on the street for 15 minutes, so it was taken back to the car park', 'now', now(), 'park', r);
    end if;
  end if;
  return jsonb_build_object('ok', true, 'now', now(), 'abandoned_at', v.abandoned_at, 'in_bay', v.in_bay, 'damage', v.damage);
end $$;

-- store the vehicle that is out in a bay of the car park it is at
create or replace function public.veh_store(p_vehicle bigint, p_token uuid, p_park text, p_bay int, p_pos jsonb, p_damage jsonb)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); cfg jsonb := veh_cfg(); v vehicles; pk car_parks;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or v.status <> 'active' or v.token is distinct from p_token or v.active_by <> me then
    raise exception 'This car has already been put away';
  end if;
  if not veh_can_drive(v.id, me) then raise exception 'You do not have the keys to this vehicle'; end if;
  select * into pk from car_parks where id = p_park;
  if pk.id is null then raise exception 'That is not a car park'; end if;
  if p_bay is null or p_bay < 0 or p_bay >= pk.bays then raise exception 'That is not a bay in %', pk.name; end if;
  if p_pos is null or sqrt(power((p_pos->>'x')::numeric - pk.x, 2) + power((p_pos->>'z')::numeric - pk.z, 2)) > (cfg->>'park_radius_m')::numeric
     or coalesce(v.state, pk.state) <> pk.state then
    raise exception 'Drive the car into % to store it there', pk.name;
  end if;
  if exists(select 1 from vehicles o where o.id <> v.id and o.park_id = p_park
              and ((o.status = 'stored' and o.bay = p_bay) or (o.status = 'active' and o.in_bay = p_bay))) then
    raise exception 'Bay % is taken', p_bay + 1;
  end if;
  update vehicles set damage = veh_merge_damage(damage, p_damage, credit), status = 'stored', park_id = p_park, bay = p_bay,
         in_bay = null, token = null, active_by = null, occupied = false, hold = null, hold_since = null, abandoned_at = null,
         pos = null, state = null, last_seen = now()
   where id = v.id returning * into v;
  perform veh_log(me, v.id, 'store', jsonb_build_object('park', p_park, 'bay', p_bay));
  return jsonb_build_object('now', now(), 'vehicle', veh_row(v, me));
end $$;

-- the game puts the car away itself (Rule A noticed in the game, or the driver chose to)
create or replace function public.veh_despawn(p_vehicle bigint, p_token uuid, p_reason text, p_damage jsonb)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; r jsonb;
begin
  if me is null then raise exception 'Sign in to use your vehicles'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or v.status <> 'active' or v.token is distinct from p_token or v.active_by <> me then
    return jsonb_build_object('gone', 'This car has already been put away', 'now', now());
  end if;
  update vehicles set damage = veh_merge_damage(damage, p_damage, credit) where id = v.id;
  r := veh_put_away(v.id, me, left(coalesce(p_reason, 'put away'), 60));
  return jsonb_build_object('ok', true, 'now', now(), 'park', r);
end $$;

-- pay for a repair or for fuel on one vehicle: the money is taken by pay_service (all or nothing), and the parts paid
-- for may then be made good on the car (p_fields: the repair items, e.g. engine, ty0, coolant, fuel, burnt)
create or replace function public.veh_pay(p_vehicle bigint, p_amount bigint, p_state text, p_reason text, p_fields text[])
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); cfg jsonb := veh_cfg(); v vehicles; paid jsonb; f text; cr jsonb; until_ numeric;
begin
  if me is null then raise exception 'Sign in to pay'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or not veh_can_drive(v.id, me) then raise exception 'You do not have the keys to this vehicle'; end if;
  if p_amount is null or p_amount <= 0 or coalesce(array_length(p_fields, 1), 0) = 0 then raise exception 'Nothing to pay for'; end if;
  paid := pay_service(p_amount, p_state, p_reason);
  until_ := extract(epoch from now()) + (cfg->>'credit_s')::numeric;
  cr := v.credit;
  foreach f in array p_fields loop
    if f = 'burnt' then
      cr := cr || jsonb_build_object('burnt', until_, 'elec', until_, 'dead', until_);
    elsif f in ('coolant', 'radiator') then
      cr := cr || jsonb_build_object(f, until_, 'coolant', until_);
    elsif f = 'oilLeak' then
      cr := cr || jsonb_build_object('oilLeak', until_, 'oil', until_);
    else
      cr := cr || jsonb_build_object(left(f, 20), until_);
    end if;
  end loop;
  update vehicles set credit = cr where id = v.id;
  perform veh_log(me, v.id, 'paid', jsonb_build_object('amount', p_amount, 'state', p_state, 'reason', p_reason, 'fields', to_jsonb(p_fields)));
  return paid;
end $$;

-- citizens by name or certificate number, for handing over keys
create or replace function public.veh_find_citizen(p_query text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); q text := trim(coalesce(p_query, ''));
begin
  if me is null then raise exception 'Sign in first'; end if;
  if length(q) < 2 then raise exception 'Type at least two letters of their name'; end if;
  return (select coalesce(jsonb_agg(jsonb_build_object('owner', owner, 'name', name)), '[]'::jsonb) from (
            select owner, name from characters where owner <> me and (name ilike '%' || q || '%' or (to_jsonb(characters)->>'cert_no') = q)
             order by name limit 8) c);
end $$;

create or replace function public.veh_key_give(p_vehicle bigint, p_holder uuid)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; who text;
begin
  if me is null then raise exception 'Sign in first'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or v.owner <> me then raise exception 'Only the owner can hand over the keys'; end if;
  if p_holder = me then raise exception 'You already own this vehicle'; end if;
  select name into who from characters where owner = p_holder;
  if who is null then raise exception 'That citizen does not exist'; end if;
  if not exists(select 1 from vehicle_keys where vehicle_id = v.id and holder = p_holder and revoked_at is null) then
    insert into vehicle_keys(vehicle_id, holder, granted_by) values (v.id, p_holder, me);
    perform veh_log(me, v.id, 'key given', jsonb_build_object('holder', p_holder, 'name', who));
  end if;
  return jsonb_build_object('ok', true, 'name', who);
end $$;

create or replace function public.veh_key_revoke(p_vehicle bigint, p_holder uuid)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); v vehicles; n int;
begin
  if me is null then raise exception 'Sign in first'; end if;
  select * into v from vehicles where id = p_vehicle for update;
  if not found or v.owner <> me then raise exception 'Only the owner can take back the keys'; end if;
  update vehicle_keys set revoked_at = now(), revoked_by = me where vehicle_id = v.id and holder = p_holder and revoked_at is null;
  get diagnostics n = row_count;
  if n > 0 then perform veh_log(me, v.id, 'key revoked', jsonb_build_object('holder', p_holder)); end if;
  -- if they have it out, it is put away at once
  if v.status = 'active' and v.active_by = p_holder then perform veh_put_away(v.id, me, 'keys revoked'); end if;
  return jsonb_build_object('ok', true, 'revoked', n);
end $$;

-- the Chief Admin gives a citizen a vehicle, stored in a free bay of a car park
create or replace function public.veh_admin_provision(p_owner uuid, p_model text, p_special boolean, p_park text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); b int; id_ bigint; pl text; who text; whose_role text;
begin
  if me is null or veh_role(me) is distinct from 'admin' then raise exception 'Only the Chief Admin can give out vehicles'; end if;
  select name, role into who, whose_role from characters where owner = p_owner;
  if who is null then raise exception 'That citizen does not exist'; end if;
  if coalesce(p_model, '') not in ('sovereign') then raise exception 'Unknown vehicle model'; end if;
  if coalesce(p_special, false) and whose_role is distinct from 'admin' then raise exception 'The special vehicle can only be given to a Chief Admin'; end if;
  if not exists(select 1 from car_parks where id = p_park) then raise exception 'That is not a car park'; end if;
  perform 1 from car_parks where id = p_park for update;   -- one provision at a time per car park, so two never take the same bay
  b := veh_free_bay(p_park);
  if b is null then raise exception 'Every bay in that car park is taken'; end if;
  pl := case when coalesce(p_special, false) then 'DC-ADMIN-' || nextval('vehicle_plate_seq') else 'DC-' || lpad(nextval('vehicle_plate_seq')::text, 5, '0') end;
  insert into vehicles(plate, owner, model, special, status, park_id, bay, created_by)
    values (pl, p_owner, p_model, coalesce(p_special, false), 'stored', p_park, b, me) returning id into id_;
  perform veh_log(me, id_, 'provision', jsonb_build_object('owner', p_owner, 'name', who, 'model', p_model, 'special', coalesce(p_special, false), 'park', p_park, 'bay', b));
  return jsonb_build_object('ok', true, 'id', id_, 'plate', pl, 'name', who, 'park', p_park, 'bay', b);
end $$;

-- the Chief Admin: every vehicle, and the latest audit entries
create or replace function public.veh_admin_list()
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if me is null or veh_role(me) is distinct from 'admin' then raise exception 'Only the Chief Admin can see every vehicle'; end if;
  perform veh_sweep();
  return jsonb_build_object('now', now(),
    'vehicles', (select coalesce(jsonb_agg(jsonb_build_object('id', v.id, 'plate', v.plate, 'owner_name', c.name, 'status', v.status, 'park', v.park_id, 'bay', v.bay, 'state', v.state, 'special', v.special) order by v.id), '[]'::jsonb)
                   from vehicles v left join characters c on c.owner = v.owner),
    'audit', (select coalesce(jsonb_agg(to_jsonb(a) order by a.id desc), '[]'::jsonb) from (select * from vehicle_audit order by id desc limit 50) a));
end $$;

-- only the game's functions are callable; the helpers are not
revoke all on function public.veh_log(uuid, bigint, text, jsonb), public.veh_role(uuid), public.veh_num(jsonb), public.veh_can_drive(bigint, uuid),
  public.veh_free_bay(text), public.veh_merge_damage(jsonb, jsonb, jsonb), public.veh_put_away(bigint, uuid, text),
  public.veh_sweep(), public.veh_row(vehicles, uuid), public.veh_busy(vehicles) from public, anon, authenticated;
revoke all on function public.veh_mine(), public.veh_spawn(bigint, text),
  public.veh_update(bigint, uuid, jsonb, jsonb, boolean, text, int, text, numeric, text), public.veh_store(bigint, uuid, text, int, jsonb, jsonb),
  public.veh_despawn(bigint, uuid, text, jsonb), public.veh_pay(bigint, bigint, text, text, text[]), public.veh_find_citizen(text),
  public.veh_key_give(bigint, uuid), public.veh_key_revoke(bigint, uuid), public.veh_admin_provision(uuid, text, boolean, text),
  public.veh_admin_list() from public, anon;
grant execute on function public.veh_mine(), public.veh_spawn(bigint, text),
  public.veh_update(bigint, uuid, jsonb, jsonb, boolean, text, int, text, numeric, text), public.veh_store(bigint, uuid, text, int, jsonb, jsonb),
  public.veh_despawn(bigint, uuid, text, jsonb), public.veh_pay(bigint, bigint, text, text, text[]), public.veh_find_citizen(text),
  public.veh_key_give(bigint, uuid), public.veh_key_revoke(bigint, uuid), public.veh_admin_provision(uuid, text, boolean, text),
  public.veh_admin_list() to authenticated;
