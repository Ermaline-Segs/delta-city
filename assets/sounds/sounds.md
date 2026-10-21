# Sounds (`sounds/`)

17 short game sounds, all **CC0**. Each is mono, 22,050 Hz Ogg Vorbis at about 48 kbit/s, peak-normalised: one-shots to about -1 dBFS and loops to about -2 dBFS. The total is 310 KB.

They were cut from the source recordings listed below. Each was trimmed and turned into mono, and fades were added.

**Loops** (`*_loop.ogg`) are made seamless: the sound just after the loop's end is crossfaded into its start. Play them with `loop = true`. For the engine, raise `playbackRate` with speed and switch from `engine_idle_loop` to `engine_accel_loop` while accelerating.

| File | What it is | Length | Loop | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `engine_idle_loop.ogg` | Peugeot 107 1.0 L petrol engine idling | 4.00 s | yes | 27 KB | BigSoundBank #966 "Small gasoline engine" by Joseph Sardin | CC0 |
| `engine_accel_loop.ogg` | car engine revving under acceleration | 3.00 s | yes | 23 KB | BigSoundBank #291 "Car Engine #2" by Joseph Sardin | CC0 |
| `horn.ogg` | modern car horn, one long press | 1.60 s | no | 12 KB | BigSoundBank #258 "Recent Car Horn #2" by Joseph Sardin | CC0 |
| `indicator_click_loop.ogg` | car indicator relay, two tick-tock cycles (0.69 s each) | 1.37 s | yes | 9 KB | BigSoundBank #1021 "Car turn signals #1" by Joseph Sardin | CC0 |
| `tyre_screech.ogg` | four tyres squealing | 2.20 s | no | 16 KB | BigSoundBank #2369 "Screeching tires #2" by Joseph Sardin | CC0 |
| `car_door_open.ogg` | Peugeot 107 door opening | 1.80 s | no | 14 KB | BigSoundBank #1524 "Car door #3" by Joseph Sardin | CC0 |
| `car_door_close.ogg` | Peugeot 107 door closing | 0.42 s | no | 6 KB | BigSoundBank #1524 "Car door #3" by Joseph Sardin | CC0 |
| `crash_thud.ogg` | car crash impact | 0.58 s | no | 7 KB | [Crash Collision](https://opengameart.org/content/crash-collision) by qubodup, OpenGameArt | CC0 |
| `glass_break.ogg` | thick mirror shattering | 1.51 s | no | 12 KB | BigSoundBank #387 "A Mirror Explodes" by Joseph Sardin | CC0 |
| `hydrant_spray_loop.ogg` | strong water spray (a shower head), loopable | 4.00 s | yes | 29 KB | BigSoundBank #171 "Woman Takes a Shower" by Joseph Sardin | CC0 |
| `lift_ding.ogg` | lift arrival ding | 0.88 s | no | 6 KB | [Elevator ding](https://opengameart.org/content/elevator-ding) by fvcalderan, OpenGameArt | CC0 |
| `building_door_open.ogg` | Parisian apartment door: handle, latch and opening | 4.20 s | no | 29 KB | BigSoundBank #1702 "Apartment Door, Opening #1" by Joseph Sardin | CC0 |
| `cash_counting.ogg` | coins dropping into a pot (stands in for counting cash) | 2.90 s | no | 22 KB | BigSoundBank #194 "Coins #2" by Joseph Sardin | CC0 |
| `footsteps_tiles_loop.ogg` | heeled shoes on a hard tiled floor, 9 steps | 5.00 s | yes | 35 KB | BigSoundBank #166 "Heels #1" by Joseph Sardin | CC0 |
| `footsteps_pavement_loop.ogg` | quick steps in shoes on concrete | 4.00 s | yes | 30 KB | BigSoundBank #1318 "Fast Steps on Concrete" by Joseph Sardin | CC0 |
| `bus_door_hiss.ogg` | pneumatic brake release: a short compressed-air hiss | 0.88 s | no | 9 KB | BigSoundBank #1490 "Pneumatic brake released" by Joseph Sardin | CC0 |
| `bus_engine_loop.ogg` | Iveco Daily 3.0 diesel engine idling | 4.00 s | yes | 27 KB | BigSoundBank #1145 "Truck engine" by Joseph Sardin | CC0 |

## Stand-ins

These sounds aren't recordings of exactly what the game shows:
- **`hydrant_spray_loop.ogg`** is a strong shower spray. No CC0 recording of a fire hydrant was found.
- **`cash_counting.ogg`** is coins dropping into a pot. No CC0 recording of banknotes being counted was found.
- **`bus_engine_loop.ogg`** is an Iveco Daily 3.0 diesel, a large van, used as a bus engine.
- **`bus_door_hiss.ogg`** is a pneumatic brake release, the same kind of compressed-air hiss a bus door makes.

## Sources

- **BigSoundBank** (https://bigsoundbank.com), recordings by Joseph Sardin. Every sound used is marked "CC0 (public domain)" on its own page. Crediting is not required, though they welcome it.
- **OpenGameArt**, both marked CC0 on their pages:
  - "Crash Collision" by qubodup.
  - "Elevator ding" by fvcalderan.
