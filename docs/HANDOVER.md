# Delta City RP: handover (every decision so far)

Read this before doing anything. It records what the owner has decided, so nobody needs to ask again.
If anything here conflicts with an older instruction, this document wins. When the owner decides something new, add it here.

## 1. The project

- A 3D role-play city game in the browser (phones first, desktops too), one file: `index.html`.
- Live site: https://ermaline-segs.github.io/delta-city/ (GitHub Pages, repository `Ermaline-Segs/delta-city`).
- Database and logins: Supabase project `jowcbkdesdrggkaivgbv`. The owner runs every SQL file by hand in the Supabase
  SQL Editor ("Run and enable RLS" if asked). Every SQL file must be safe to run twice. Never put secret keys in the game.
- Four states, each its own town map: **Asaba** (capital), **Warri**, **Ozoro**, **Agbor**.
- The game copies the owner's old **Discord** role-play server. `docs/interiors_from_discord.md` is the source of truth
  for buildings (categories), rooms (channels) and who may enter (permissions). `docs/workplaces.md` lists each post's
  clock-in room.

## 2. Working rules (for every AI helper)

- **Pull before starting and before every push. Never force-push.** Other helpers push to the same repository.
- **Only one helper changes `index.html` at a time.** Assets go in `assets/`; documents in `docs/`.
- Each helper works in **its own folder** on the laptop (`delta-city` for local Claude, `delta-city-codex` for Codex).
  Never touch or delete another helper's unfinished files.
- **Test in a real browser** before pushing, on a phone-sized screen and a desktop. Report what changed, what passed and
  what didn't. Never claim success from pictures alone, and never show fake numbers or buttons that do nothing.
- Assets: realistic (photo textures, not cartoon), CC0 or CC-BY only (credit CC-BY in `CREDITS.md` under
  "Credits required"). Never use models ripped from games, or with NonCommercial, NoDerivatives, ShareAlike or
  Sketchfab "Standard/Free Standard" licences. `.glb`, real size in metres, Y-up, cars face -Z; furniture and interiors face +Z. Check each model's real front.
- **The Nigerian way:** money is **K** (e.g. K250,000), not ₦. Traffic drives on the **right**; every car is
  **left-hand drive**; anticlockwise round roundabouts. Players are mostly Nigerian.

## 3. What exists (summary)

Logins and saving; citizenship; a Chief Admin (role `admin`, account 62fb9e58-b44d-432c-a485-78c74d80df5c) who can go
everywhere and give roles in the game; the government (87 posts from the bot + Swat and Student; appointments by the
Chief Admin, President, Vice President and Chief of Staff; daily pay after 5 hours clocked in, tax and pension, paid
from the state's account or the National Reserve, unpaid days stay owed); the National Treasury and Central Bank
(printing K100,000 a minute; armoured cash vans); the hospital; banks; Immigration; insides for every workplace,
public place, hotel, Lifestyle centre (clubhouse, **no chapel**), Asaba Church, shops, airports, filling stations and
workshop offices; room-level clocking in; indoor maps; driving with gears, lights, damage, fire, leaks, mechanic,
workshops and a paid tow truck; vehicle ownership, keys, 9-11 car parks per town, garage spawning; street lamps,
traffic lights, hydrants and breakable street objects; the cream-and-green HUD; the Sovereign GT (the Audi is gone).

## 4. The work queue, in order

1. **Markets and shops for Warri, Ozoro and Agbor** (like Asaba's).
2. **Car doors opening, characters visible in cars** (moved up by the owner). The driver walks to the left front door,
   it swings open on its hinge, the character sits visibly with hands on the wheel, the door shuts; reverse to get out.
   Wheels spin, front wheels and steering wheel turn, passengers sit visibly. Door sounds from `assets/sounds/`.
   Works for every car with separate parts in `assets/vehicles/`.
3. **Live multiplayer** on Cloudflare (Durable Objects), not Supabase Realtime: see section 7. (Moved before homes by the owner.)
4. **Phase 3, homes**: see section 6.
5. **Solid usable furniture everywhere**: nothing walk-through indoors; sit on chairs and sofas, lie on beds, cook,
   use toilets, showers, computers and counters. Needs motion recordings (lying, cooking, eating, showering, typing).
6. **Highways joining the four states**, with the cash vans driving them.
7. **Public transport**: see section 8.
8. **Character creator** from `assets/modular/` (read its `modular.md` and `hide_lists.json`). Navy-and-gold creator
   screens; Female/Male; face presets, 50 skins, hair with colours, clothes, accessories, name. Hide the body under
   clothes. Load pieces only when chosen. Map the MPFB `game_engine` rig to the game's animations. Save to the
   citizen's `look` field. Players use the creator; the Rocketbox characters stay as staff and townspeople.
   Men are only playable once the creator exists (Henry was removed for good). Missing from free libraries and wanted
   later: beards, locs, twists, headwraps, agbada, kaftan, ankara, sandals, slippers.
9. **Buying cars**: see section 9.
10. **Life needs** (health, hunger, thirst, energy, hygiene, social, bladder, stress) and the hospital's treatment,
    bills and insurance. Decisions still needed from the owner (rates, prices, insurance).

## 5. Fixed numbers and choices

- Cash vans: up to K5,000,000 each; several vans travel together. Loading at the Treasury and unloading at the bank:
  2 minutes + 2 minutes per K1,000,000. Journeys: Asaba = the van's real drive (about 40 s); Warri 30 min; Ozoro 78;
  Agbor 150 (the Discord flight times x6). Credit only when unloading finishes, exactly once.
- Repairs and the tow truck are paid to the **state's account** (a mechanic business later).
- **Fuel: K950 a litre**, one server setting (`game_settings` `fuel_price_k`, from `supabase_fuel.sql`), the same in all
  four states; never in `index.html`. Shown on every pump as "K950 / litre". Changed only by the **Chief Admin** and the
  **Minister of Agriculture & Natural Resources** (`fuel_set_price`, role checked on the server through `gov_me()`); the
  cooking-gas price will follow the same rule. There is **no** Minister of Petroleum. A fill is charged at the
  end: litres actually put in x the price, rounded to the nearest K, paid to the **state's account**. A typed amount buys
  amount / price litres (K10,000 = 10.53 L, exactly K10,000), stopping early if the tank fills.
- **Cooking gas:** sold at the gas depot beside **every** filling station (8 depots, 2 per state); gas prices to be
  decided (same price rule as fuel: Chief Admin and the Minister of Agriculture & Natural Resources).
- BRT bus livery: **red and white**, "BRT" on the sides and front.
- No mosque. Asaba's Lifestyle centre "#Chapel" is part of the club.

## 6. Homes (phase 3)

- Renting and buying happen at each state's **Housing Development**, at the **Rental Desk** (`#rental-desk`):
  a computer-run clerk shows available homes. Housing staff (Housing Administrator, Land & Property Officer, Urban
  Development Officer, Director) can serve players and manage listings; only the Minister of Housing & Infrastructure (and the Chief Admin)
  changes prices. Listings board (`#land-property-listing`), deeds and receipts (`#deed-receipt`), reminders board
  (`#reminders`). **Visitors may rent; only citizens may buy.**
- A few home buildings per town. Home types (rent every 2 weeks / buy): self-contained room K250,000 / K15M;
  2-bedroom flat K500,000 / K30M; 3-bedroom bungalow K800,000 / K50M; duplex K1.2M / K75M; mansion K3M / K200M.
  These are **starting prices** in the Phase 3 price table on the server; only the Minister of Housing & Infrastructure
  and the Chief Admin can change them (checked on the server). All money to the **state's account**.
- No fixed units, never "full": every resident gets their **own private copy** of the inside, even in the same
  building. Nobody sees another's home unless invited. The server decides who may enter.
- One home per player (rented or bought). "Home" marker on that player's map only. "Enter home" at the door only for
  residents and invited visitors.
- Unpaid rent: locked out until paid; home and furniture kept **7 days**, then freed and furniture to storage.
  Reminder 2 days before rent is due.
- Furniture store in each town near the market; buy, place, move, turn, remove; sell back at half price. Furniture is
  in `assets/home/` (Codex is adding a large Nigerian home set: fans, generators, gas cooker and cylinder, TVs, sofas,
  beds, mosquito nets, buckets and so on).
- Invitations: build the rules now; seeing visitors move inside comes with live multiplayer.
- **Home buildings (made by the local session, commit a7552b7):** in `assets/buildings/homes/`, one exterior and one
  interior `.glb` per type, each with a `.json` of its door nodes. **Quarters** use the self-contained room row
  (`room_*`); **Township** the flat block (`flat_*`) and the three-bedroom bungalow (`bungalow_*`); **GRA** and
  **Estate** the duplex (`duplex_*`) and the mansion (`mansion_*`). Door, room, gate and car-park positions are in
  `assets/buildings/homes/homes.md`. The **three-bedroom bungalow** is new (owner's price: K800,000 rent every 2
  weeks / K50M to buy, a starting price like the others).
- **Owner's decisions on changing homes:**
  - Rent already paid is **not refunded** when a renter upgrades to buying, moves to another home or ends the
    rental. The new contract starts fresh. Ending a rental keeps the home until the paid 14 days run out, then it is
    freed and the furniture goes to storage.
  - An owner may **rent their home out** to another player, or **sell it** to another player or to the state.
  - **Selling back to the state:** the state pays **70% of the price the owner actually paid** (no rent refunds of any kind), so the price paid is
    stored on the home record. It is paid from the state's account. If the state's account can't cover it, **ask the
    owner** before choosing a fallback.
  - Furniture in a sold home goes to the owner's **storage, appended** (never replacing what is already there); the
    same for a rental that expires.
  - Home prices are changed only by the **Minister of Housing & Infrastructure** and the **Chief Admin**, through a
    server function that checks the role; housing staff serve players and manage listings.

## 7. Live multiplayer

**Decided by the owner: Cloudflare, not Supabase Realtime.** Supabase stays for logins, money, ownership, roles and
saving. Comes **before** Phase 3 (homes), by the owner's decision. Code and the owner's setup steps: `server/README.md`.
**Cloudflare is set up** (owner): workers.dev subdomain `deltacity`, server address
`https://delta-city-live.deltacity.workers.dev`, secrets `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` and `CF_ANALYTICS_TOKEN` in GitHub.

- Cloudflare Workers free plan with **one Durable Object (SQLite-backed) for the whole game**; every town and every
  building inside is a **room** inside it (one object keeps running time under the free 13,000 GB-s a day).
  **WebSocket Hibernation.** Each player is sent only the players near them.
- Players connect by WebSocket after signing in and send their Supabase login token; the Worker checks it against
  Supabase's **public signing keys (JWKS)**. Any secret ever needed is a **Worker secret**, never in `index.html` or
  the repository.
- Free limits: **100,000 requests a day**, incoming WebSocket messages counted **20 to 1**, outgoing messages free;
  reset at 00:00 UTC. When a limit is hit, multiplayer stops until 00:00 UTC.
- About **2 updates a second while moving, none when still**, fewer for players over 60 m away.
- If the server can't be reached or is over its limit, the game falls back to **single-player with a small "Offline
  mode" notice**. It must never break.
- The Chief Admin's Admin screen shows the **measured daily request count** against the limit and a **projection for
  2, 5 and 10 players**.
- Show other players with their own character, smooth movement and name tags; share cars, street objects, hydrants,
  doors and repairs; a simple chat.
- Code in `server/` with a README; published by GitHub Actions with `wrangler deploy`, using the owner's API token from
  a GitHub secret (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`).
- Test with two signed-in browser windows.

## 8. Public transport

BRT buses (`brt_bus.glb`, sliding doors `door_P1`/`door_P2`, 29 seats and standing areas) and taxis
(`taxi_corolla.glb`). Driven by **players** with the Driver job, who clock in at the Transport Authority; **computer
drivers run BRT routes when no player is driving; taxis only run with a player.** Passengers board, sit or stand, and
travel while the driver drives, then get off at their stop. Routes and stops on the map. Fares to the state's account
now, the driver's business later. Keep right; overtake on the left.

## 9. Buying cars (dealership)

Prices (K), roughly double the first suggestion:
budget K5M-K8M (Daihatsu-based, Skoda Felicia-based, Mula Van); family K12M-K16M (Meridian, Corolla in non-taxi
colours); SUV K25M (Savanna); premium K40M-K55M (Strada RS); luxury K90M-K150M (Vela V12); vintage K30M-K45M
(Harmattan GT, Studebaker-based). Use the Delta City names the local session gave each car (see `vehicles.md`).
The two Ural trucks are kept for the police and fire service later. Still to decide: instalments, road tax,
insurance, selling cars between players. The owner may download more premium and luxury cars.

## 10. Assets already prepared

`assets/vehicles/` (Sovereign GT, taxi, BRT bus, UAZ van, Corrado, dealership cars, `vehicles.md`),
`assets/sounds/` (17 CC0 sounds), `assets/interiors/` (court, police, office, university, hotel, church, mosque,
market), `assets/home/`, `assets/modular/` (character creator, 420 MB), `assets/characters/` (Rocketbox staff).

**From the local session (commits 8d17fac and a7552b7), and how the game uses them:**
- **Filling station:** `assets/props/fuel/` (`fuel.md`): `fuel_pump.glb` (two-sided, faces +X side A and -X side B;
  nodes `nozzle_A/B` and `hose_A/B` are the holster nozzles and hoses), `fuel_nozzle.glb` (hand-held), `fuel_hose.glb`.
  In the game the pump body is built into each station; each side's holster nozzle and hose is drawn on its own and
  hidden while that nozzle is in an attendant's hand. The "K950 / litre" text is drawn by the game (pump tags), not the
  model. A station built before the models load keeps simple boxes.
- **Attendants:** `assets/characters/Fuel_Attendant_Male.glb` / `Fuel_Attendant_Female.glb` (green coverall; red and
  navy texture variants `__red.jpg` / `__navy.jpg` are not used yet). One of each at every station.
- **Attendant movements:** `assets/animations/rocketbox/<male|female>/Fuel_Take.glb`, `Fuel_Hold_Loop.glb`,
  `Fuel_Hang.glb` (`assets/animations/animations.md`, "Filling-station attendant": the nozzle's transform in the right
  hand, and where to stand so the grip lands on the holster and the spout on the cap). The game reads them at run time
  (`clipLoad` in `index.html` turns a Rocketbox glTF clip into the game's own recording format). All the other
  retargeted clips are in `assets/animations/rocketbox/` (Rocketbox) and `assets/animations/mpfb/` (character creator
  bodies); `clipLoad` can read the Rocketbox ones the same way.
- **Fuel caps:** side and point for all 17 vehicles in `assets/vehicles/vehicles.md` ("Fuel caps"); copied into
  `FUELCAP` in `index.html` (turned into the game's car space). Caps lower than about 0.85 m (BRT bus, Starlite, UAZ,
  Mula Van) need the attendant's hand lowered from the 0.98 m hold height: **not done yet** (only the Sovereign GT
  is drivable so far). When each new car becomes drivable, add a refuel test for its own fuel-cap side.
- **Cooking-gas depot:** `assets/props/gas/` (`gas.md`): `gas_cage_stocked.glb`, `gas_scale.glb`, 6 kg and 12.5 kg
  cylinders in four colours. In the game: the stocked cage, the scale and two cylinders in front of each depot. No buttons.
- **Character layers:** `assets/modular/hide_lists.json` now has a `"layers"` section (rules for two pieces worn
  together: a top over a bottom, shoes under trousers, a hat over hair and so on). **The character creator must apply
  it after loading the worn pieces, the same way as the body hide lists.**
- **Home buildings:** see section 6 (`assets/buildings/homes/`, `homes.md`).

## 11. Updates since the first handover (newest first)

- **Bike feel: lean, steering, controls and top speed (this PR; owner feedback "too stiff, does not drive or feel like a real bike ride")** — `index.html` only, motorbike only (every change is guarded by `isBike(C)`; the car path, including the Sovereign GT config line, is byte-identical before/after).
  1. **Lean:** bike and rider lean into turns together — `VEH.lean = atan(clamp(lat,-9,9)*.08*clamp(|v|/3,0,1))`, smoothed with a ~0.15 s time constant (`dt*6.7`). Up to ~30° near top speed, less at low speed, zero when stopped. The lean is applied to the whole model+rider by multiplying the model matrix by `mrotZ(lean)` in `WALKER.draw` (new `lean` argument, car passes 0). The bike model has **no separate handlebar node**, so the bars are not turned; the whole rig leans.
  2. **Speed-dependent steering:** `steerMax/(1 + v/10 + (v/16.7)²)` (bike only; car keeps `steerMax/(1+v/14)`). Tight at walking pace (U-turn possible below ~15 km/h), calmer at speed. Measured turning radius: 1.8 m @10 km/h, 8.3 m @30 km/h, 32.7 m @60 km/h.
  3. **No P R N D:** the gear strip (`.dgears`) is hidden for the bike; the bike starts in drive and throttle always goes forward. Reverse is allowed but capped at ~5 km/h (measured 5.04).
  4. **Handbrake → "Brake":** the dash button reads **Brake** for the bike; it is the rear brake — decelerates hard but smoothly (brake 6 m/s², torque-curve keeps pulling at low speed) and never locks the wheel or spins the bike.
  5. **Acceleration/braking:** 0–60 in **5.03 s**, 60–0 in **2.56 s** (measured with the real physics code, flat road). Config now `vmax:16.9, accel:4.2, rev:5, brake:6, torq:16`.
  6. **Top speed = 60 km/h:** with the real drag in the code the plateau measured **60.09 km/h** (59–61 target met). Tuned by sweep on the actual vehicleStep loop, not by guessing vmax.
  - **Not touched:** bike lights/indicators, crash behaviour, multiplayer, garage, and everything for cars.

- **PR 13, branch `pr/c-motorbike-drives` (item: PR C — the bike drives), commit `a083f10`** — `index.html`
  only, on top of the merged bike-asset PRs (#10 asset, #12 GLB header fix, #11 rental SQL). What PR C does:
  - Adds the `CARS.motorbike` model config (top speed ~60 km/h, gear ratio, mass, drag) so the vehicle
    physics knows how a bike behaves, driven by the new per-model helpers `carPhys(C)`, `carSit(C)`,
    `carRig(C)` and `tankOf(C)` instead of the old single global config.
  - Per-model config: `carPhys(C)` returns the CARS entry for the vehicle's own model (car vs bike) so each
    vehicle type keeps its own speed / handling / tank numbers.
  - Adds a `m_bike` rig and a `BIKESCENE` (built once at startup) so the bike is drawn from the bike model,
    while cars keep using `CARSCENE` — `carScenes({model:"m_bike"})` picks the right scene.
  - Seat: the rider is drawn seated on the bike seat (driver-eyes and half-in draw paths now go through
    `carSit(C)` / `carRig(C)` so the seat height/anchor is per model).
  - Small fuel tank: the bike's tank is smaller than a car's; fuel tick, refuel panel and server-confirm all
    use `tankOf(C)` so the bike's bar and fill rate match its real tank size.
  - **NOT done in this PR (later work):** the bike wheels do not spin yet, the rent button UI and other
    players seeing the bike (network sync) come in a later PR.

- **PR 9 merged as 7e2a1c7** (guest play and stale practice-car strings removed; main is at 7e2a1c7 as of this
  asset-branch work).

main is at `f44031f` (29 October 2026) as of this work; once this PR (#8) is merged, main's
history will include `36b5267` (the unowned-car fix) plus this handover commit, and main will
point at the merge commit created at merge time. Everything below that is merged is live on
main and at the Pages URL. The repo has no build, typecheck or lint; the only runnable check is
`test/flags.mjs` (`node test/flags.mjs` from the repo root — it must pass before pushing).

- **Owner decisions, 29 October 2026 (after PR 8; recorded on merge commit `558afa8`):**
  1. **No practice car, and no new player gets a car.** Removed deliberately in PR 8 — not a bug. Do not re-add it.
  2. **How new players get around until they can buy a car:**
     - the public transport system (BRT buses and taxis — section 8);
     - **renting a bike:** a player can rent one specific bike from any garage at the start.
       **Open decisions (owner to decide — not assumptions):** which bike, the rental price, the
       rental period, and whether a rented bike is saved to the account.
     - No bike model exists in `assets/vehicles/` yet, so a bike asset is needed first — a
       local-session/Blender job, not a cloud job.
3. **No "play without an account" option — signing in is required to play.** This is NOT the same
      as the multiplayer "Offline mode" fallback, which stays exactly as it is: a signed-in player
      whose live server is unreachable keeps playing single-player with the Offline notice (section 7
      and "If multiplayer causes problems", section 12). Do not confuse the two: guest/account-less
      play is to be removed; Offline mode stays.
      **Done in PR 9 (this handover entry):** the sign-in screen's guest button and its offline
      handler are gone, the "play without an account" fallback sentences and all guest-facing text
      are removed, and the now-dead `!AUTH.offline` terms in the gates were cleaned up
      (`garOn`, `govOn`, the CB terminal gate, `adminAct`, the fuel `signed` flag and the phone
      sheet's `signed`). The stale practice-car strings (`garLine`, the garage panel note, the
      comment in the owned-vehicles section) were removed in the same PR. The `netPill` "Offline
      mode" fallback for a signed-in player whose server is unreachable is unchanged.
  4. **The car gate is ownership, not role.** "Only the Chief Admin has a car" is true today only
     because the dealership (section 9) is not built. Anyone will be able to buy and drive a car;
     do not add a role check to driving.

- **Unowned-car exploit: FIXED (PR 8, this work — commit `36b5267`):**
  - The finding below (section 12, "reported, not fixed") is now resolved. Chosen fix: **dropped
    the `!C.vid` fallback in `garCanDrive`** (it is now `!!C.vid && GAR.list.some(...)`) and
    **removed `parkCar` entirely** — `toTown` no longer spawns any car at the kerb, so a car with
    no recorded owner can no longer be driven by anyone, including the Chief Admin. The gate is
    ownership, not role: a car with a `vid` is drivable by its owner or a key-holder; `garPlace`
    (the keys-given path) is unchanged, so the Chief Admin's Sovereign GT and any keys they hand
    out work exactly as before. `carEnter` needs no change: it only starts the enter sequence when
    `garCanDrive` already passed, so it is the sole entry gate.
  - **Why not make `parkCar` ownership-aware instead:** a role-aware `parkCar` would keep spawning
    a car object that non-owners can see but not use (a "phantom car") and would need an admin
    check — the wrong gate. The rule "only the Chief Admin has a car" is only true **today**
    because the dealership (section 9) does not exist yet; once it does, buying a car writes the
    `vehicles` row that IS the `vid`, so bought cars will be drivable with no further change here.
    **Do not add a Chief-Admin/role check to driving.**
  - A player with no car still gets a working town: no car spawns, no crash, no stuck state; the
    street hint now reads "There is no car in the street; the Chief Admin gives keys at the car
    parks (P on the map)."
  - Verified: `node test/flags.mjs` from the repo root (ALL 10 FLAG CHECKS PASS) before pushing;
    real-browser (Chromium, headless) test at 390x844 (phone) and 1280x800 (desktop) driving the
    real game functions with a fresh page load per case: (A) Chief Admin drives the Sovereign GT —
    `garCanDrive` true, enter sequence starts; (B) signed-in player with no car — no kerb car
    spawns, nothing drivable, no crash; (C) player given keys by the Chief Admin (`garPlace`
    path) — drives the car; (D) offline/unsigned guest with a simulated old-style no-`vid` kerb
    car — `garCanDrive` false, entry blocked with the "You do not have the keys to this vehicle"
    toast. All four cases pass at both viewports; no page errors in any case (only unrelated
    400/404 network noise from the local test server).

- **Agbor/Grandview: rebuilt the L-staircase and moved the ATM vestibule off the stair
  approach (PR 7, merged 29 October 2026):**
  - The PR 5 ATM vestibule was sitting on Grandview Bank's (Agbor) stair approach, so the
    L-shaped staircase was rebuilt and the vestibule relocated clear of the approach
    (21+/12- in `index.html`, commit `0500f64`).
  - The original commit was pushed from the ephemeral sandbox working tree before it could
    be reworked (the headless geometry audit crashed three times), so it shipped UNVERIFIED.
    It was then verified by: a headless render (no console errors), a by-eye browser
    walkthrough, and the owner's screenshot review of the four review composites (each
    bank's stairs and ATM vestibule placement).
  - **No automated geometry or clearance check was run on this change — no walkable-path or
    footprint measurements exist for it.** Crestfield, Eastway and Trustmark were checked by
    eye only and needed no changes; Trustmark was the weakest pass (dark frames).
  - **Status: merged 29 October 2026 (merge commit `50228b8`).**
- **A distinct look for each state bank (PR 6, merged 29 October 2026, commit `6479eae`):**
  - Bank names come from the Discord server; no real Nigerian bank names or logos anywhere.
    `BANK_STYLES` in `index.html` holds each bank's palette, logo and layout variant, applied inside
    and out: walls, sign bands, counters, carpets, medal wall and the bank's ATMs (which carry the
    bank's name and colours, PR 5).
  - **Crestfield Bank (Asaba)** — emerald green and gold, gold crest/shield logo: grand double-height
    hall, round information desk mid-hall, long curved teller counter at the back, twin staircases up
    to a mezzanine gallery of offices overlooking the hall.
  - **Eastway Bank (Warri)** — deep teal and silver, rising-sun-with-arrow-east logo: long narrow hall,
    tellers along one wall, customer-service desks along the other, queue lane down the middle, offices
    along a back corridor, straight side staircase.
  - **Trustmark Bank (Ozoro)** — burgundy and cream with dark wood, round seal logo: compact
    wood-panelled hall, tellers behind glass windows facing the door, rows of waiting benches, the
    manager's office visible through glass, corner staircase.
  - **Grandview Bank (Agbor)** — charcoal and amber, window-over-skyline logo: open-plan modern hall,
    island teller pods, self-service area by the ATM vestibule, glass-walled offices around the edge,
    L-shaped staircase.
  - Rooms and who may enter them are unchanged (still per `docs/interiors_from_discord.md`); stairs,
    doors, counters and aisles checked clear; the PR 5 ATM vestibule and the outside ATM gallery are
    kept at every bank.
  - Visually checked in a real browser (phone and desktop sizes): all eight screenshots (four
    exteriors, four halls) render as proper 3D scenes; Crestfield (dark green walls, gold sign band)
    and Eastway (deep teal, silver) confirmed by vision; Trustmark and Grandview verified by their
    own colour signatures in the saved frames (the vision API was billing-blocked mid-check).
  - **How it was verified: a headless render check (screenshots of all four banks, phone and
    desktop sizes), a by-eye browser walkthrough, and the owner's screenshot review before
    merge. No automated geometry, clearance, build or typecheck check was run on it either —
    the repo has no build, typecheck or lint; `test/flags.mjs` is the only runnable check.**
  - **Status: merged 29 October 2026 — the owner OK'd the screenshots before merge.**

- **Blocked paths, real doors, ATMs everywhere (PR 5, merged 29 October 2026):**
  - **36 ATMs — 9 per state** — all wired to the existing banking system: the machine only reads
    the wallet the bank keeps, in K; deposits/withdrawals stay at the teller counters, no new
    money rules. Each shows its state bank's name, sits on the map with a 🏧 icon, and is
    one-player-at-a-time ("Use the ATM" prompt; a toast asks you to wait your turn if the machine
    is taken). Per state: 1 machine in the bank's ATM Services vestibule (Agbor's old stairway
    blocker removed — the vestibule now has exactly one), 4 in a row in the bank's compound under
    an "ATM GALLERY • 24 HOURS" sign, and 4 at public places: the Market, the Filling Station, the
    Delta International Airport, and the Lifestyle Centre.
  - **Airport and repair shops (garage):** real doors people walk through — a gap in the front
    wall with the blue entry square at the door — and the "Delta International Airport" sign moved
    off the gate to the terminal's roof.
  - **Filling stations and gas depots (all 8):** the planter between the way in and the way out
    pulled 1.35 units back from the forecourt gate (z 13.25 → 11.9) so the gate is clear.
  - **Car parks:** `streetTidy` now takes the town's parks and pushes street props, trees and
    lamps out of each gate's apron and out of every numbered bay's footprint; the roadside-park
    no-props strip extended (3.4 → 6.2). No building, grass, flower, tree or prop overlaps a bay,
    gate or driveway.
  - **Entry check, all four towns:** every building's entry square and every interior walked;
    stairs, doors, counters and aisles reachable. Aggravating fix: the Agbor stairway ATM (above).
  - Verified headless in a real browser at 390×844 (phone) and 1280×800 (desktop): 36 machines
    registered (8 town + 1 bank in each state), no console errors.
- **Note: the work is on main via direct merge commit `dfe4f47`. GitHub pull request #5 is now
    closed (as superseded) — the commit on main is the record of this work.**

- **No HUD bar covers a dialog's buttons (PR 4, merged 29 October 2026):** on phones, the phone /
  inventory / settings bar (and the other bottom HUD bars) covered Violet's "Begin registration" button
  and the buttons of every other dialog. Fix in `index.html`: while `#talk` or `#choose` is open, the
  bottom HUD bars (`#nav`, `.tbtn`, `.towskip`, `#picks.sheet`, `#hudSheet`) get `display:none` via one
  `body:has(...)` rule, and `.talk` carries `z-index:7` as a backstop. Every dialog in the game (auth,
  registration, buying, refuelling, garage, admin, settings) goes through `#talk` or `#choose`, so all
  are covered. Verified in a real browser at 390×844 (phone) and 1280×800 (desktop): no bar over the
  dialog, all buttons visible.

**Ways of working**
- All Claude sessions (this chat, local Claude Code, cloud Claude Code) share **one weekly allowance**. Run one at a time
  where possible. Codex does not use it (good for simple, well-defined asset jobs; it struggled with `index.html`).
- **Only the cloud session edits `index.html`.** The local session does Blender and asset work in `delta-city`.
- Keep this file up to date with every new decision.
- **Handover discipline (from 29 October 2026):** update `docs/HANDOVER.md` at the end of every
  task and commit it with the work — the chat context gets truncated, so this file is the only
  reliable record of project state.

**Done since the first handover**
- Markets and shops in Warri, Ozoro and Agbor. Right-hand traffic (vans and tow truck keep right, anticlockwise round
  roundabouts, kerb-side parking). The Audi is gone; the **Sovereign GT** replaced it everywhere (`supabase_sovereign.sql`).
- **Car doors and the seated driver:** the left front door swings open, the driver sits visibly with hands on the wheel,
  wheels spin and steer. `source/models/pack_vehicle.py` prepares any car in `assets/vehicles/` with moving parts.
- **11 converted cars** (all left-hand drive, badges removed, makers credited): Sovereign GT (Chief Admin), Kite, Comet,
  Mula Van, Harmony, Meridian, Savanna, Strada RS, Vela V12, Harmattan GT, Starlite. Dropped as game rips: the
  600LT-style car and the SRT Viper. The Ural police and fire trucks are not converted yet.
- Map names shrink instead of vanishing (minimum 9 px, always shown); every shop has a tag (group "Services").
  Entering: a 1.5 s grace period after arriving inside (`exitCool`), arrival at `G_LD - 2.2`. `clearDoorways` removes loose
  street objects and trees within 7 m in front of every door.
- **20 animations** in `assets/animations/` (CC0, Quaternius): lying down and getting up, sleeping, eating, cooking,
  showering, toilet, typing, phone, carrying a box, car seat. They use Quaternius' 65-bone rig, so they must be
  **retargeted** to the Rocketbox and MPFB skeletons before use.
- **Entering (cloud, items 1-2):** every arrival point inside is about 2.6 m from the way out (hospital, Treasury, bank,
  Immigration, government-style buildings); every door in all four towns walked into with a held joystick (99 of 99).
- **Compounds (cloud, item 3):** every workplace and public place has its own fenced compound, a gate of 7 m or more
  facing its road (most 17 m; the Treasury's car gate 10.5 m, beside its own railings) and its own car park inside
  (3+ numbered bays, terminal, P sign); the market one compound; roadside shops a lay-by along the kerb. 91 car parks
  replace the 39 old ones. **Run `supabase_compound_car_parks.sql`** (after `supabase_vehicles.sql`): it moves every
  stored car to the nearest new car park in its state, keeping owner, keys and damage. Moved to clear plots: Asaba's
  Lifestyle centre and Ministry of Trade (now on the expressway), Asaba's university (12 m east), the Asaba and Warri
  workshops, Warri's market, and four roadside shops.
- **Tap anywhere on the big map (cloud, item 4):** a route along the roads to that spot, arrows on the map and the road;
  cleared on arrival, by tapping the marker, or with Cancel.
- **Map tags (cloud, item 5):** every building door has a tag; every living area is tagged (Ozoro's is called "Estate",
  not "GRA": the owner to say whether to rename it).
- **Furniture facing (cloud, item 6):** each model's real front was checked by rendering it. Most `assets/interiors/`
  models face -Z in the file and are turned half round when placed (`IPFRONT_Z` in `index.html`); the office chair
  and desks face +Z. Lecture seats face the lectern, pews the altar, court benches the judge, beds have their heads to
  the wall, TVs face the room, counters show their public side to the door. Whiteboards and notice boards stand clear
  of the wall.
- **Solid furniture (cloud, item 7):** every model registers its own outline, measured from the model and turned with
  it (pieces at a slant are cut into short lengths). Only boards on walls, rugs and things standing on another piece
  are not solid. Fixed on the way: hospital furniture was not solid at all, and its outlines were leaking into the
  town as invisible blocks near the town centre; the bank's mezzanine furniture blocked the floor below it; the counter
  rooms had the staff side sealed off (the counter now stands 2.3 m from the back wall with a gap at one end); the
  maternity beds were too close together; the Chief Admin could not open some bank and Immigration doors. Checked with
  a flood fill of every inside (every room, door and counter reachable) and by walking into a piece in each kind of
  room on a phone and a desktop screen (18 of 18).
- **Feet on the ground (cloud, item 8):** while a town is built every low surface (road, pavement, kerb, compound
  paving, each entrance step, the Treasury steps and podium) is kept as a standing height (`groundTop`); the body
  follows it step by step, and each foot is placed on the height under it (two-bone IK at hip and knee, `placeFeet`).
  The bank's stairs are 18 real steps. Tested walking up and down the Treasury steps, onto a pavement over a kerb, at
  the hospital entrance and on the bank stairs, on phone and desktop sizes: no foot below the ground at any moment.
- **Reverse camera (owner's request):** in R the chase camera glides to the front corner on the driver's side and
  looks back past the car; it glides back behind the car out of reverse.
- **Home rules decided by the owner:** see section 6 (selling back, furniture, no refunds).
- **Refuelling (cloud, owner's report "paid, tank not filling"):** the old pump took the money first, then filled by
  counting game frames with each frame capped at 0.05 s, so on a phone below 20 frames a second it filled at a
  fraction of the speed, and stopped where it was if the car moved. Rebuilt: the server sets the price and the most it
  will sell (`fuel_start`), the fill is timed by the clock (2.5 litres a second), and the charge comes at the end for
  what went in (`fuel_finish`, through `pay_service`; no more than a pump could deliver in the time). "Fill tank" or
  "Buy amount" (a K amount); engine off to start; driving off or starting the engine stops it and charges for what
  went in. **Run `supabase_fuel.sql`.**
- **Filling stations: two in each state** (the first, and a "West" one on the other side of town), each driven through
  one way (IN at the upstream end, OUT at the other, keeping right, a planter between, arrows on the forecourt), with
  its own compound, car park (`<state>-fshop2`), map tag and route-to. Two attendants each (one man, one woman: Rocketbox
  staff in their own clothes) walk to the car's fuel cap, fill with a stand-in hose, and walk back; the pump display
  counts litres and K. Uses the game's walk, idle and talk recordings until the local session delivers a nozzle, a
  "holding the nozzle" pose and uniforms. Clock-in points for a future Filling Station Attendant job are in
  `docs/workplaces.md`.
- **Gas depots:** one in the back corner of every filling station's compound (8), reached through the same entrance:
  the building (shutter down), its signs and a map tag ("... Gas Depot", group Services). No buttons yet. The space in
  front is kept free for a sales counter and a cylinder cage; the game keeps each depot's door, counter and cage spots
  (`town.gas`) for Phase 3's gas refills.
- **Fuel caps needed (for the local session, `assets/vehicles/vehicles.md`):** only the Sovereign GT is drivable now,
  and its cap is a guess (rear left quarter, car space `[0.93, 0.95, -1.35]`). Each car that becomes drivable needs
  its fuel-cap side and position, and gets its own refuel test.
- Furniture finding: the models may face **+Z**, not -Z as some `items.md` notes say. Check each model's real front.
  Codex's `assets/home/` set is complete but had faults (pieces floating, kettle and blender too big, fan mount); the
  local session is fixing them.

**The cloud session's list (items 1-8 all done)**
Entering fix, blocked doors, compounds, tap-anywhere route, map tags, furniture facing, solid furniture, feet and
stairs: all done and pushed, plus the reverse camera.

**The order from here (owner, newest)**
1. **Live multiplayer on Cloudflare** (section 7). The three GitHub secrets are in place: `CLOUDFLARE_ACCOUNT_ID`,
   `CLOUDFLARE_API_TOKEN`, `CF_ANALYTICS_TOKEN`. Supabase stays for logins, money and saving.
2. **Phase 3, homes** (section 6), only after multiplayer works and is pushed.

**Notes for later integration (owner; not now, after multiplayer allows)**
- `assets/animations/` now holds retargeted sets for `rocketbox/{male,female}` and `mpfb/{female,male}`. See
  `animations.md` for walk speeds (0.9-1.0 m/s; the clips play in place) and seat heights (0.53-0.60 m).
- Check that the game's renderer can skin the MPFB 53-bone skeleton (the skinning uniform holds 84 bones today).
- The Ural trucks have six wheels (`wheel_F*`, `wheel_M*`, `wheel_R*`): the driving code must spin and place the
  middle pair too.

**The local session's list, in order**
1. Fix the home furniture (floating pieces, sizes, fan mount, facing) and check `assets/interiors/` facing the same way.
2. Retarget the 20 animations to the Rocketbox and MPFB skeletons.
3. Nigerian clothing and hair for the character creator (agbada, kaftan, senator wear, beards, ankara gown, iro and
   buba, gele, locs, twists, slippers, sandals), fitted to the MPFB bodies with hide lists.
4. Convert the Ural police and fire trucks.

## 12. State of the project (28 October 2026; read this first if you are new)

This file alone is enough to carry on. The game is one file, `index.html`, served by GitHub Pages at
https://ermaline-segs.github.io/delta-city/ (from `main`). Supabase holds logins, money, ownership, roles and saving (the
`supabase_*.sql` files set it up). The live multiplayer server is in `server/` and runs on Cloudflare at
`https://delta-city-live.deltacity.workers.dev`. Rules for helpers are in section 2; the owner's decisions are in
sections 5 to 9.

### Finished and live (on `main`)
- Four states (Asaba, Warri, Ozoro, Agbor), with government, courts, police, banks, Treasury, Immigration, hospital,
  markets and shops, public insides, compounds with gates and car parks, and a map tag on every building.
- Driving: the Sovereign GT with opening doors, a visible driver, damage, repairs and tow, garages and car parks, and a
  reverse camera.
- Feet on the ground: real stairs and kerbs; solid indoor furniture.
- Fuel: two filling stations per state, each with one male and one female attendant, the real pump and nozzle, and
  real fuel caps. K950 a litre, held on the server; only the Chief Admin and the Minister of Agriculture & Natural
  Resources can change it. Each state has a cooking-gas depot beside both of its stations (building, sign, map tag and
  props, no buttons yet).
- **Live multiplayer, first version** (pull request https://github.com/Ermaline-Segs/delta-city/pull/1, merged
  28 October 2026; its server deploy needed a test fix, https://github.com/Ermaline-Segs/delta-city/pull/2): who is online, and other players walking in the same town or building with name tags. When the
  server can't be reached it falls back to single-player with an "Offline mode" notice.

### Multiplayer: what is left, in order
Everything below is already written in `index.html` and `server/`, each behind its own flag on one line near the top of
`index.html`: `const NET_EXTRAS_CARS=...,NET_EXTRAS_STREET=...,NET_EXTRAS_INDOORS=...,NET_EXTRAS_CHAT=...;`.
Set a flag to `true` to turn that one on, then test with two signed-in windows, phone and desktop. The test scripts
used so far are described in sections 7 and 11; the flag defaults are guarded by `test/flags.mjs` (run
`node test/flags.mjs` from the repository root — it must pass before pushing a change to that line).
1. **Other players' cars:** the car, doors, wheels and seated driver. **Turned on by job 1 (this PR, 28 October
   2026):** `NET_EXTRAS_CARS=true` ships, so a driving player is now seen in their car with name tag, instead of
   being hidden. Until the server records which model each player drives, **every remote car is drawn as a Sovereign
   GT** — add a `car` field to the peer message when more cars become drivable.
2. **The shared street:** knocked-over and repaired street objects, and burst hydrants, seen by everyone in the town.
3. **Chat:** the phone's Chat app, or T on a keyboard. Today it only says "Chat is coming soon".
4. **Inside buildings:** players in the same room see each other, and doors open for other players. This was already
   live since the first version and was never behind the old `NET_EXTRAS` flag, so `NET_EXTRAS_INDOORS` ships `true`:
   the re-test job only confirms it, it does not switch anything off.

**Job 1 result (28 October 2026, this PR):** the one `NET_EXTRAS` flag was split into four per-feature flags;
`NET_EXTRAS_CARS` ships on, `NET_EXTRAS_STREET` and `NET_EXTRAS_CHAT` ship off, `NET_EXTRAS_INDOORS` ships on (it
protects what was already live). Checks: `node test/flags.mjs` 10 of 10 pass; JavaScript syntax check clean;
`npm test` in `server/` 31 of 31 pass (server unchanged).

**Live two-account car test (final run, 28 October 2026):** one car — the Chief Admin's Sovereign GT, given to
Account A. Account B stays on foot throughout and never holds the Chief Admin role. Round 1: A drives in a
desktop-sized window, B watches in a phone-sized window. Round 2: the windows are resized so A drives at phone
size and B watches at desktop size. Score **44 of 56 pass, 12 fail, 0 errors.** Every check of what the driver
does to its own car passes in both rounds (get in, door, wheel spin, speed, gear, seated driver, get out); all 12
failures are on what the *watcher* sees of the *other player's car*:
- R1 (5): name tag not positioned in the DOM before the walk (`before=null`); name tag left/top never sampled;
  peer-car lights + state desynced (self `l=1` vs peer `l=0`, peer `dr=0` while A is driving); name tag never
  follows the moving car (`null -> null`); B still sees A as "in-car" after A exits.
- R2 (7): B's view of the peer car is stale for the whole round — door opening not seen (`null`); peer car
  position frozen (`d=0.00m`), no yaw change on steer (`dYaw=0.000rad`), front wheels never steer (`st=0`),
  lights + state mismatch (self `l=2` vs peer `l=1, st=0, dr=0`), name tag not attached to the car
  (`null -> null`), peer wheel spin never accumulates (`0 -> 0`). "B drives, A watches" was not tested because
  there is only one car; the code path is the same in both directions. These 12 are the remaining remote-car
  bugs to chase before the car experience is considered done; the on-foot checks (position, heading, name-tag
  presence, reconnection, state change, chat/street off) pass in both rounds.

**Finding (fixed in `36b5267`, PR 8) — `toTown()` → `parkCar(T)` gave ordinary players a drivable
Sovereign GT at the kerb, breaking the "only the Chief Admin has the car, and only the Chief Admin gives cars"
rule:** `index.html:2903` — `toTown` calls `parkCar(T)` whenever the town has no car and `garOn()` is false.
`garOn()` at `index.html:3896` is `!!AUTH.user && !AUTH.offline && !!AUTH.char` — true for **any** signed-in
player with a character, not admin-only; for those players `parkCar` is skipped and `T.car` stays null unless
the Chief Admin handed over keys. But for a player without a car in their profile (or one who is offline /
unsigned) the guard fails open: `parkCar` (`index.html:2905-2906`) spawns `T.car = {x, z, yaw, v: 0}` **with no
`vid`**, and `garCanDrive` at `index.html:3937` is `!C.vid || GAR.list.some(...)` — a no-`vid` car is drivable by
**everyone** through the `!C.vid` branch, and `carEnter` at `index.html:3631-3632` has no role check at all.
The only place `vid` (ownership) is set is `garPlace`, `index.html:3916-3918`, which handles only keys-given
cars. So an ordinary player arriving in a town with no parked car gets a Sovereign GT at the kerb that anyone
can drive. Fixed in `36b5267` (PR 8, 29 October 2026): the `!C.vid` fallback was dropped from `garCanDrive`, so
a car with no recorded owner (`vid`) cannot be driven by anyone — not even the Chief Admin — and `parkCar` was
removed, so no vid-less kerb car is ever spawned. The Chief Admin still has the Sovereign GT because they own
it (`vid` is set), and the `garPlace` keys path is unchanged. Verified by `node test/flags.mjs` and a headless
browser pass at 390x844 and 1280x800 covering all four cases: Chief Admin drives the Sovereign GT; a signed-in
player with no car cannot drive anything; a player given keys by the Chief Admin can drive that car; an
offline/unsigned player cannot drive a kerb car.
**Intent — record for the future:** "only the Chief Admin has a car" is true **today only** because the
dealership (section 9) does not exist yet. It is not a permanent rule — anyone will be able to buy and drive a
car. When the dealership is built, buying a car writes the `vehicles` row, and that row **is** the `vid`, so
bought cars will work with no further change to this code. Do not re-add a Chief-Admin or role check to driving;
the gate is on ownership, not role.

### Next steps after that, in order
1. Phase 3, homes (section 6). The buildings are ready in `assets/buildings/homes/`. Prices are set: room
   K250,000 / K15M, flat K500,000 / K30M, three-bedroom bungalow K800,000 / K50M, duplex K1.2M / K75M, mansion
   K3M / K200M. Rent is per two weeks, followed by the price to buy. Only the Minister of Housing & Infrastructure
   and the Chief Admin can change them, checked on the server.
2. Then the rest of the queue in section 4 (solid usable furniture, highways, public transport, character creator,
   buying cars, life needs).
3. Smaller jobs:
   - when another car becomes drivable, lower the attendant's hand for low fuel caps (BRT bus, Starlite, UAZ,
     Mula Van), and add a refuel test for that car's fuel-cap side;
   - set a cooking-gas price (the owner decides it);
   - the attendants' red and navy coverall variants;
   - the six-wheel Ural trucks;
   - whether the 53-bone MPFB skeleton can be skinned in the game.

### SQL the owner still has to run

Bike rental (this branch, from the open decision in section 4): the SQL for the motorbike rental
is in **`supabase_bike_rental.sql`** — **run on live Supabase on 30 Oct 2026**. It is safe to run
twice: every statement is idempotent (`add column if not exists`, `create or replace`,
`create index if not exists`).

**Ordering warning:** `supabase_bike_rental.sql` must run **after** `supabase_vehicles.sql`, and
`supabase_vehicles.sql` must **not** be re-run on the live database afterwards — it contains the
older `veh_row` and `veh_sweep` and would silently remove the rental support. If
`supabase_vehicles.sql` ever has to be re-run, re-run `supabase_bike_rental.sql` straight after it.

**How to run it:** in the Supabase SQL Editor, paste the full contents of `supabase_bike_rental.sql`
and press **Run**. Order matters only within the file — run the file as one paste, top to bottom.

What it does, in order:
1. `vehicles.rents_until` column (server-clock expiry, null for non-rentals) + a partial index.
2. `veh_rent_bike(p_park text)` — signed-in check, locks the car park row, deletes any rental bike
   the renter already has (audit row written), finds a free bay or raises, charges K10,000 through
   `pay_service` in the same transaction (a failed payment creates nothing), inserts the bike
   (model `motorbike`, `rents_until = now() + interval '24 hours'`) with a `vehicle_keys` row and an
   audit row, returns the vehicle as json like `veh_mine`. No role check — anyone signed in can rent;
   a second rental replaces the old bike, pays again, no refund.
3. `veh_sweep()` extended — any row with `rents_until <= now()` is DELETED (stored and active alike),
   audit row `rental expired` written first; the audit rows stay (see 5).
4. `veh_row(v, me)` now includes `rents_until` so the client can show a countdown; `veh_mine` gets it
   for free since it calls `veh_row`.
5. Audit check (item e): `vehicle_audit.vehicle_id` is a plain `bigint` with only a regular index
   (`vehicle_audit_vehicle`) and **no foreign key** to `vehicles`, so deleting a vehicles row neither
   cascades nor blocks — its `vehicle_audit` rows survive. No schema change was needed.

**Checklist to run in the SQL Editor after the file has been applied.**

In the SQL Editor, `auth.uid()` is **null** — there is no signed-in request. So **each test block
below starts with the same sign-in line**; replace `<a real test user uuid>` with the `owner` uuid
of a real test character (find it with `select owner, name, town, cash from characters;`) and run
that block as one paste, top to bottom. The character's `town` must be a state that has car parks
(Asaba, Warri, Ozoro or Agbor), and pick a car park in that same state (`select id, state, name,
bays from car_parks;`) — the file now refuses any park outside the character's own state.

**1. Rent** (expects `{"ok": true, ...}` with a `vehicle` whose `model` is `motorbike` and
`rents_until` about 24 hours ahead):
```sql
select set_config('request.jwt.claims', json_build_object('sub', '<a real test user uuid>')::text, true);
select public.veh_rent_bike('<park id in the character's own state>');
select id, plate, model, status, park_id, bay, rents_until from public.vehicles
 where owner = '<a real test user uuid>' and model = 'motorbike';
```

**2. Cash and key** (cash down by exactly 10,000, one live `vehicle_keys` row for the bike):
```sql
select set_config('request.jwt.claims', json_build_object('sub', '<a real test user uuid>')::text, true);
select owner, name, cash from public.characters where owner = '<a real test user uuid>';
select id, vehicle_id, holder, granted_by, revoked_at from public.vehicle_keys
 where vehicle_id = (select id from public.vehicles where model = 'motorbike'
                     and owner = '<a real test user uuid>') and revoked_at is null;
```

**3. Rent again (replacement)** (old bike row gone wherever it was, fresh bike with fresh 24 hours,
cash down by another 10,000, and a `vehicle_audit` row with action `rental replaced` for the old
bike):
```sql
select set_config('request.jwt.claims', json_build_object('sub', '<a real test user uuid>')::text, true);
select public.veh_rent_bike('<park id in the character's own state>');
select id, action, detail from public.vehicle_audit where action in ('rented', 'rental replaced')
 order by id desc limit 5;
```

**4. Wrong-state park (new rule)** (a park in another state must be refused, nothing created,
nothing charged):
```sql
select set_config('request.jwt.claims', json_build_object('sub', '<a real test user uuid>')::text, true);
select public.veh_rent_bike('<a park id in a DIFFERENT state>');   -- expect the "own state" error
select count(*) from public.vehicles where model = 'motorbike' and owner = '<a real test user uuid>';
```

**5. Expiry** (force the bike past its `rents_until` on the server's clock, then sweep — the bike
row is deleted, the audit rows stay):
```sql
select set_config('request.jwt.claims', json_build_object('sub', '<a real test user uuid>')::text, true);
update public.vehicles set rents_until = now() - interval '1 minute'
 where model = 'motorbike' and owner = '<a real test user uuid>';
select public.veh_sweep();
select count(*) from public.vehicles where model = 'motorbike' and owner = '<a real test user uuid>';
select id, action, detail from public.vehicle_audit
 where vehicle_id = (select max(vehicle_id) from public.vehicle_audit where vehicle_id is not null)
 order by id desc limit 5;   -- expect 'rented', any 'rental replaced', and a 'rental expired' row
```

**6. Unsigned sanity (optional)** (no signed-in user in the same run: `veh_rent_bike` raises a
"sign in" error and changes nothing):
```sql
select set_config('request.jwt.claims', '{}'::text, true);
select public.veh_rent_bike('<any park id>');   -- expect the sign-in error
select count(*) from public.vehicles where model = 'motorbike';
```

### If multiplayer causes problems
1. **Undo it:**
   1. Open https://github.com/Ermaline-Segs/delta-city/pull/1 and press **Revert**. GitHub makes a new pull
      request.
   2. Open that new pull request and press **Merge pull request**, then **Confirm merge**.
   3. GitHub Pages republishes the game without multiplayer within a few minutes. Players should reload the page.
   4. Leave pull request 2 as it is: it only changed a server test, and it works with the old server too.
2. **The server:** merging the revert also puts back the previous server code automatically. The revert changes
   `server/`, and the "Live server" workflow (`.github/workflows/live-server.yml`) publishes `server/` to Cloudflare
   whenever it changes on `main`. **Nothing needs doing in Cloudflare.**
   - Check it under the repository's **Actions** tab: a green tick on "Live server".
   - If it shows a red cross, open **Actions → Live server → Run workflow** (branch `main`) to publish again.
   - Without multiplayer the game never contacts the server, so even an old or stopped server does no harm.
3. **Daily use, and the free limit:**
   - **In the game:** the Chief Admin's **Admin** screen, "Live server" part. It shows today's requests against the
     free 100,000, running time, players online, and a projection for 2, 5 and 10 players.
   - **In Cloudflare:** dash.cloudflare.com → **Workers & Pages** → `delta-city-live` → **Metrics**.
   - **When the free daily limit is used up:** the server stops taking players. The game carries on single-player.
     A small "Offline mode" notice appears top right; on a computer, holding the mouse over it says "the live server has used
     today's free allowance; it comes back at 01:00". That is 00:00 UTC, 01:00 Lagos time. Players reconnect by
     themselves after that.
   - The server stops at 95,000 requests, so it stays inside the free plan and never costs money.
