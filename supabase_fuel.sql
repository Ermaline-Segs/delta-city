-- Delta City RP: buying fuel at the filling stations (two in each state).
--
-- The price per litre is ONE server setting (game_settings 'fuel_price_k', K950 to start), the same in all four states.
-- Only the Chief Admin and the Minister of Petroleum can change it (fuel_set_price checks the caller on the server).
-- The game only shows it; it never decides it.
--
-- Also adds the national post "Minister of Petroleum" to gov_posts (a copy of the Minister of Housing & Infrastructure's
-- row: same scope and pay; it clocks in at its own office in the Federal Council).
--
-- How a fill works:
--   1. fuel_start: the player chooses "Fill tank" or "Buy amount" (a K amount). The server works out the most it will
--      sell: the space in the tank, the amount typed (amount / price litres) and what the player can afford, whichever
--      is least. It opens a fuel session and says how many litres that is.
--   2. The attendant fills; the pump counts up. The fill stops at that many litres, when the tank is full, or when the
--      player drives off.
--   3. fuel_finish: the game says how many litres went in. The server allows no more than the session's limit, nor
--      more than a pump can deliver in the time since the start (4 litres a second, so a game cannot claim a full tank
--      in an instant), and charges litres x price rounded to the nearest K through pay_service: the player's cash goes
--      to the state's account in the same transaction (pay_service refuses if they cannot afford it, and then nothing
--      is charged). Only then may the car's fuel go up on the server (the 'fuel' credit used by veh_update).
--
-- Also: the four new filling stations' car parks (one more station in each state).
--
-- Run this whole file once in the Supabase SQL editor, after supabase_services.sql and supabase_vehicles.sql.
-- Running it again is safe: it never changes a price that has already been set, and keeps every fuel session.

begin;

create table if not exists public.game_settings (
  key        text primary key,
  value      jsonb not null,
  updated_by uuid,
  updated_at timestamptz not null default now()
);
alter table public.game_settings enable row level security;          -- read and changed only through the functions below
insert into public.game_settings(key, value) values ('fuel_price_k', '950'::jsonb) on conflict (key) do nothing;

create table if not exists public.fuel_sessions (
  id          bigserial primary key,
  owner       uuid not null,
  vehicle_id  bigint,
  state       text not null,
  station     text not null,
  price       bigint not null,               -- K a litre when the fill began
  max_litres  numeric(10,4) not null,        -- the most this fill may put in (litres to 4 places, so K10,000 buys exactly K10,000)
  started_at  timestamptz not null default now(),
  finished_at timestamptz,
  litres      numeric(10,4),
  charged     bigint,
  status      text not null default 'open'   -- open, done, abandoned
);
alter table public.fuel_sessions alter column max_litres type numeric(10,4), alter column litres type numeric(10,4);
create index if not exists fuel_sessions_open on public.fuel_sessions(owner) where status = 'open';
alter table public.fuel_sessions enable row level security;

-- the price, for anyone (the pumps show it)
create or replace function public.fuel_price()
returns jsonb language sql stable security definer set search_path = public as $$
  select jsonb_build_object('price', (select (value #>> '{}')::bigint from game_settings where key = 'fuel_price_k'))
$$;

-- the Minister of Petroleum post, copied from another national minister (left alone if it already exists)
do $$
declare cols text := ''; sel text := ''; c record;
begin
  if to_regclass('public.gov_posts') is null or exists (select 1 from gov_posts where title = 'Minister of Petroleum') then return; end if;
  if not exists (select 1 from gov_posts where title = 'Minister of Housing & Infrastructure') then
    raise notice 'Minister of Housing & Infrastructure is not in gov_posts, so the Minister of Petroleum could not be copied from it. Add the post by hand.';
    return;
  end if;
  for c in select column_name from information_schema.columns
            where table_schema = 'public' and table_name = 'gov_posts' and coalesce(column_default, '') not like 'nextval(%'
              and is_identity = 'NO' and is_generated = 'NEVER' and column_name not in ('created_at') order by ordinal_position loop
    cols := cols || case when cols = '' then '' else ', ' end || quote_ident(c.column_name);
    sel  := sel  || case when sel  = '' then '' else ', ' end || case c.column_name when 'title' then quote_literal('Minister of Petroleum')
                                                                     when 'key' then quote_literal('min_petroleum') else quote_ident(c.column_name) end;
  end loop;
  execute format('insert into gov_posts (%s) select %s from gov_posts where title = %L limit 1', cols, sel, 'Minister of Housing & Infrastructure');
  raise notice 'Minister of Petroleum added';
end $$;

-- may this signed-in person change the fuel price? The Chief Admin, or whoever holds the Minister of Petroleum post
-- (read with the game's own gov_me(), so it follows appointments and dismissals exactly as the game does)
create or replace function public.fuel_price_setter()
returns boolean language plpgsql stable security definer set search_path = public as $$
declare me uuid := auth.uid(); posts jsonb;
begin
  if me is null then return false; end if;
  if exists(select 1 from characters where owner = me and role = 'admin') then return true; end if;
  begin
    posts := coalesce(gov_me()->'posts', '[]'::jsonb);
  exception when undefined_function then return false;
  end;
  return exists(select 1 from jsonb_array_elements(posts) p where lower(p->>'title') = 'minister of petroleum');
end $$;

-- the Chief Admin or the Minister of Petroleum changes the price (K a litre)
create or replace function public.fuel_set_price(p_price bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid();
begin
  if not fuel_price_setter() then
    raise exception 'Only the Chief Admin and the Minister of Petroleum can change the fuel price.';
  end if;
  if p_price is null or p_price < 1 or p_price > 1000000 then raise exception 'The price must be between K1 and K1,000,000 a litre.'; end if;
  update game_settings set value = to_jsonb(p_price), updated_by = me, updated_at = now() where key = 'fuel_price_k';
  return fuel_price();
end $$;

-- start a fill. p_room: the space in the tank in litres (as the game sees it); p_amount: the K amount typed, or null to fill
create or replace function public.fuel_start(p_vehicle bigint, p_state text, p_station text, p_room numeric, p_amount bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); price bigint; cash bigint; room numeric; afford numeric; want numeric; lim numeric; why text; sid bigint;
begin
  if me is null then raise exception 'Sign in to buy fuel.'; end if;
  if p_state is null or p_state not in ('Asaba', 'Warri', 'Ozoro', 'Agbor') then raise exception 'Unknown state: %', coalesce(p_state, '(none)'); end if;
  if p_vehicle is not null and not veh_can_drive(p_vehicle, me) then raise exception 'You do not have the keys to this vehicle.'; end if;
  select (value #>> '{}')::bigint into price from game_settings where key = 'fuel_price_k';
  if price is null or price <= 0 then raise exception 'No fuel price has been set.'; end if;
  select coalesce(c.cash, 0) into cash from characters c where c.owner = me;
  if cash is null then raise exception 'No citizen record for this account.'; end if;
  room := greatest(0, least(coalesce(p_room, 0), 200));
  if room < 0.05 then raise exception 'The tank is full.'; end if;
  if p_amount is not null and p_amount < price then
    raise exception 'The smallest amount is one litre: K%.', to_char(price, 'FM999,999,999,990');
  end if;
  if cash < price then
    raise exception 'Not enough cash: one litre costs K% and you have K%.', to_char(price, 'FM999,999,999,990'), to_char(cash, 'FM999,999,999,990');
  end if;
  afford := floor(cash::numeric * 10000 / price) / 10000;                   -- litres the cash covers
  want := case when p_amount is null then room else floor(p_amount::numeric * 10000 / price) / 10000 end;   -- K10,000 at K950: 10.5263 litres
  lim := least(room, want, afford);
  why := case when lim = afford and afford < least(room, want) then 'cash' when lim = room and room < want then 'tank' when p_amount is null then 'tank' else 'amount' end;
  update fuel_sessions set status = 'abandoned', finished_at = now() where owner = me and status = 'open';     -- a fill left unfinished (the game was closed)
  insert into fuel_sessions(owner, vehicle_id, state, station, price, max_litres)
    values (me, p_vehicle, p_state, left(coalesce(p_station, ''), 40), price, round(lim, 4)) returning id into sid;
  return jsonb_build_object('id', sid, 'price', price, 'max_litres', round(lim, 4), 'limit', why, 'cash', cash);
end $$;

-- finish a fill: charge for what went in
create or replace function public.fuel_finish(p_session bigint, p_litres numeric)
returns jsonb language plpgsql security definer set search_path = public as $$
declare me uuid := auth.uid(); s fuel_sessions; secs numeric; litres numeric; amount bigint; paid jsonb := null; cfg jsonb; until_ numeric;
begin
  if me is null then raise exception 'Sign in to buy fuel.'; end if;
  select * into s from fuel_sessions where id = p_session and owner = me for update;
  if not found then raise exception 'That fill is not yours.'; end if;
  if s.status <> 'open' then raise exception 'That fill is already finished.'; end if;
  secs := extract(epoch from now() - s.started_at);
  litres := round(greatest(0, least(coalesce(p_litres, 0), s.max_litres, secs * 4 + 0.5)), 4);
  amount := round(litres * s.price);
  if amount > 0 then
    paid := pay_service(amount, s.state, 'Fuel: ' || to_char(litres, 'FM99990.00') || ' litres at ' || s.station);   -- refuses (and charges nothing) if they cannot afford it
  end if;
  if s.vehicle_id is not null and litres > 0 then                            -- the car's fuel may now go up on the server
    cfg := veh_cfg(); until_ := extract(epoch from now()) + coalesce((cfg->>'credit_s')::numeric, 7200);
    update vehicles set credit = coalesce(credit, '{}'::jsonb) || jsonb_build_object('fuel', until_) where id = s.vehicle_id;
    perform veh_log(me, s.vehicle_id, 'fuel', jsonb_build_object('litres', litres, 'amount', amount, 'state', s.state, 'station', s.station));
  end if;
  update fuel_sessions set status = 'done', finished_at = now(), litres = finish.litres, charged = amount from (select litres) finish where id = s.id;
  return jsonb_build_object('ok', true, 'litres', litres, 'amount', amount, 'price', s.price, 'cash', coalesce((paid->>'cash')::bigint, (select cash from characters where owner = me)));
end $$;

revoke all on function public.fuel_price() from public;
grant execute on function public.fuel_price() to anon, authenticated;
revoke all on function public.fuel_price_setter() from public, anon;
grant execute on function public.fuel_price_setter() to authenticated;
revoke all on function public.fuel_set_price(bigint) from public, anon;
grant execute on function public.fuel_set_price(bigint) to authenticated;
revoke all on function public.fuel_start(bigint, text, text, numeric, bigint) from public, anon;
grant execute on function public.fuel_start(bigint, text, text, numeric, bigint) to authenticated;
revoke all on function public.fuel_finish(bigint, numeric) from public, anon;
grant execute on function public.fuel_finish(bigint, numeric) to authenticated;

-- the second filling station in each state: its car park
insert into car_parks(id, state, name, x, z, bays) values
  ('asaba-fshop2', 'Asaba', 'Asaba West Filling Station Car Park', -124, 164.8, 3),
  ('warri-fshop2', 'Warri', 'Warri West Filling Station Car Park', -199.5, -84, 3),
  ('ozoro-fshop2', 'Ozoro', 'Ozoro West Filling Station Car Park', -135.9, -126.3, 3),
  ('agbor-fshop2', 'Agbor', 'Agbor West Filling Station Car Park', -135.9, -126.3, 3)
on conflict (id) do update set state = excluded.state, name = excluded.name, x = excluded.x, z = excluded.z, bays = excluded.bays;

commit;

select key, value from game_settings where key = 'fuel_price_k';
select id, name, x, z from car_parks where id like '%-fshop2' order by id;
select title, key from gov_posts where title = 'Minister of Petroleum';
