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
- BRT bus livery: **red and white**, "BRT" on the sides and front.
- No mosque. Asaba's Lifestyle centre "#Chapel" is part of the club.

## 6. Homes (phase 3)

- Renting and buying happen at each state's **Housing Development**, at the **Rental Desk** (`#rental-desk`):
  a computer-run clerk shows available homes. Housing staff (Housing Administrator, Land & Property Officer, Urban
  Development Officer, Director) can serve players and manage listings; only the Minister of Housing & Infrastructure (and the Chief Admin)
  changes prices. Listings board (`#land-property-listing`), deeds and receipts (`#deed-receipt`), reminders board
  (`#reminders`). **Visitors may rent; only citizens may buy.**
- A few home buildings per town. Home types (rent every 2 weeks / buy): self-contained room K250,000 / K15M;
  2-bedroom flat K500,000 / K30M; duplex K1.2M / K75M; mansion K3M / K200M. All money to the **state's account**.
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

## 11. Updates since the first handover (newest first)

**Ways of working**
- All Claude sessions (this chat, local Claude Code, cloud Claude Code) share **one weekly allowance**. Run one at a time
  where possible. Codex does not use it (good for simple, well-defined asset jobs; it struggled with `index.html`).
- **Only the cloud session edits `index.html`.** The local session does Blender and asset work in `delta-city`.
- Keep this file up to date with every new decision.

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
- **Home rules decided by the owner (for Phase 3):** a renter who buys gets **no credit** for rent already paid; a
  renter who moves to another home gets **no credit**; ending a rental keeps the home **until the paid 14 days run
  out, no refund**, then it is freed and the furniture goes to storage. An owner may **rent their home out** to
  another player, or **sell it** to another player or to the state (sale price to the state: still to be decided).
- Furniture finding: the models may face **+Z**, not -Z as some `items.md` notes say. Check each model's real front.
  Codex's `assets/home/` set is complete but had faults (pieces floating, kettle and blender too big, fan mount); the
  local session is fixing them.

**The cloud session's list (items 1-8 all done)**
Entering fix, blocked doors, compounds, tap-anywhere route, map tags, furniture facing, solid furniture, feet and
stairs: all done and pushed, plus the reverse camera.

**Known fault (open):** the driving test's Asaba bank case fails often: reversing straight back from the road into
bay 1, the car dents something at about (32, 5.5) and stops short. It fails just as often on the version from before
items 8 and the reverse camera, so it is not caused by them. Being checked: what the car hits (a cash van unloading at
the bank, or a fixed object at the compound's gate).

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
