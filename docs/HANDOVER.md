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
  Sketchfab "Standard/Free Standard" licences. `.glb`, real size in metres, Y-up, front facing -Z.
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
3. **Phase 3, homes**: see section 6.
4. **Live multiplayer**: see section 7.
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
  Development Officer, Director) can serve players and manage listings; only the Director (and the Chief Admin)
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

Implementation status (22 October 2026): `index.html` has an initial Rental Desk, home status and contract calls, a personal home marker, a private starter interior, and starter furniture hooks. This is partial Phase 3 work. The furniture shop workflows (buy, place, move, turn, remove, and sell back), full furnishing set, and visitor movement are not complete. The home contract calls need the matching Supabase SQL to be installed before they can be tested against an account. Registration and character-save functions were not part of this home update.

## 7. Live multiplayer

Supabase Realtime (broadcast and presence, one channel per town or building). Show every signed-in player in the same
place, walking, running, driving, sitting, with their own character, smooth movement and name tags. Share cars,
knocked-over street objects, burst hydrants, doors and repairs. The free plan allows 2 million messages a month: send
only when something changes, about 2 updates a second when moving, fewer for distant players, nothing when still.
Show players online. Test with two browser windows as different players. Chat comes with this.

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
