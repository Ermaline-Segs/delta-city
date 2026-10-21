# Vehicles (`vehicles/`)

Four drivable vehicles with doors, wheels and a steering wheel as separate named parts. The van and the Corrado are **CC0** from OpenGameArt. The taxi and the BRT bus are **CC-BY 4.0** from Sketchfab, and their authors must be credited (they're listed under "Credits required" in `../CREDITS.md`).
Parts were cut and pivoted in Blender 5.2; the door pictures in `previews/` are rendered from the exported `.glb` files themselves.

| File | Car | Triangles | Size | Textures |
|---|---|---|---|---|
| `uaz_452.glb` | UAZ-452 utility van ("bukhanka"), low poly | 2,776 | 227 KB | 256 px body, 128 px wheel, 32 px palette (PNG) |
| `vw_corrado.glb` | VW Corrado coupé, low poly | 6,524 | 647 KB | 1467 x 360 px (PNG) |
| `taxi_corolla.glb` | Corolla E180 saloon as a yellow taxi, 4 doors, full interior | 19,159 | 2.9 MB | up to 1024 px (JPEG) |
| `brt_bus.glb` | Mercedes-Benz Citaro 12 m city bus, red and white with BRT lettering, sliding passenger doors, seats and poles | 24,102 | 1.0 MB | none (plain materials) |
| `mula_van.glb` | Mula Van: budget minivan | 27,410 | 1.8 MB | up to 1024 px (JPEG) |
| `harmattan_gt.glb` | Harmattan GT: vintage muscle coupé | 32,347 | 3.8 MB | up to 1024 px (JPEG) |
| `strada_rs.glb` | Strada RS: premium sports coupé | 36,386 | 2.6 MB | up to 1024 px (JPEG) |
| `vela_v12.glb` | Vela V12: fictional sports car | 30,890 | 3.2 MB | up to 1024 px (JPEG) |
| `kite.glb` | Kite: budget city car (kei car) | 27,164 | 1.3 MB | up to 1024 px (JPEG) |
| `harmony.glb` | Harmony: family saloon (the taxi's car in private colours) | 19,135 | 2.9 MB | up to 1024 px (JPEG) |
| `comet.glb` | Comet: budget hatchback | 19,490 | 0.8 MB | up to 1024 px (JPEG) |
| `savanna.glb` | Savanna: small SUV | 36,523 | 3.4 MB | up to 1024 px (JPEG) |
| `meridian.glb` | Meridian: family saloon | 39,522 | 3.8 MB | up to 1024 px (JPEG) |
| `sovereign_gt.glb` | Sovereign GT: premium coupé, the Chief Administrator's car | 24,542 | 2.3 MB | up to 1024 px (JPEG) |

## Driver's side

Every vehicle is **left-hand drive**, as in Nigeria. The steering wheel and the driver's seat are on the left (negative x).

The Harmattan GT was built from an Australian right-hand-drive car, so its interior was mirrored. `previews/harmattan_gt_interior.png` shows it from above with the roof cut away.

| File | Vehicle | Driver | Steering wheel `[x, y, z]` | Driver's hip point `[x, y, z]` | Note |
|---|---|---|---|---|---|
| `uaz_452.glb` | UAZ-452 van | left | `[-0.45, 1.36, -1.40]` | `[-0.45, 1.18, -0.92]` |  |
| `vw_corrado.glb` | VW Corrado | left | `[-0.38, 0.82, -0.30]` | `[-0.38, 0.47, 0.12]` |  |
| `taxi_corolla.glb` | Taxi | left | `[-0.36, 0.84, -0.55]` | `[-0.36, 0.60, 0.12]` |  |
| `brt_bus.glb` | BRT bus | left | `[-0.75, 1.41, -5.40]` | `[-0.75, 1.01, -4.95]` |  |
| `mula_van.glb` | Mula Van: budget minivan | 27,410 | 1.8 MB | up to 1024 px (JPEG) |
| `harmony.glb` | Harmony | left | `[-0.36, 0.84, -0.55]` | `[-0.36, 0.60, 0.12]` |  |
| `sovereign_gt.glb` | Sovereign GT | left | `[-0.44, 0.83, -0.00]` | `[-0.44, 0.62, 0.29]` |  |
| `meridian.glb` | Meridian | left | `[-0.38, 0.95, -0.58]` | `[-0.41, 0.57, -0.30]` |  |
| `savanna.glb` | Savanna | left | `[-0.37, 0.74, -0.82]` | `[-0.37, 0.67, 0.04]` |  |
| `comet.glb` | Comet | left | `[-0.34, 0.81, -0.42]` | `[-0.37, 0.34, 0.06]` |  |
| `kite.glb` | Kite | left | `[-0.33, 1.00, -0.36]` | `[-0.33, 0.74, 0.05]` |  |
| `vela_v12.glb` | Vela V12 | left | `[-0.37, 0.78, -0.66]` | `[-0.36, 0.60, 0.15]` |  |
| `strada_rs.glb` | Strada RS | left | `[-0.38, 0.86, -0.17]` | `[-0.38, 0.55, 0.25]` |  |
| `harmattan_gt.glb` | Harmattan GT | left | `[-0.42, 0.74, -0.42]` | `[-0.40, 0.62, 0.15]` | interior mirrored from right-hand drive |

## Coordinates (what the game sees after loading the `.glb`)

- Metres. **+Y is up, the front of the car points toward -Z, the driver's (left) side is -X.**
- The root node (`uaz_452` / `vw_corrado`) sits on the ground (y = 0) under the middle of the car; every part is a direct child of it.
- All positions below are in the root node's space, `[x, y, z]`.

## Parts and how to move them

| Part | Pivot | How to animate it (three.js) |
|---|---|---|
| `body` | root origin | Everything else: the shell, bumpers, plates, mirrors and a simple interior (floor, dashboard, steering column, two front seats, rear bench seat(s)). The shell has a dark inner lining so the cabin looks closed from inside. |
| `door_FL`, `door_FR` | on the hinge line at the door's **front edge**, on the outer skin, halfway up the door | `door.rotation.y`: **left door negative, right door positive** to open (e.g. -60 deg / +60 deg). Closed = 0. The rear edge swings outward. |
| `wheel_FL`, `wheel_FR`, `wheel_RL`, `wheel_RR` | wheel centre | Rolling: `wheel.rotation.x`; **negative = rolling forward**. Steering (front wheels): `wheel.rotation.y`, positive = turn left. Set `wheel.rotation.order = 'YXZ'` if you do both. |
| `steering_wheel` | centre of the rim | The node already carries the column tilt (a rotation about X). Spin it with `steering_wheel.rotation.z` only (it is the wheel's own axis); positive = anticlockwise as the driver sees it, i.e. turning left. Don't overwrite `rotation.x`. |

Neither car has rear doors (the UAZ's side and back doors are painted on its texture; the Corrado is a 2-door coupé), so there is no `door_RL` / `door_RR`.

## UAZ-452 van (`uaz_452.glb`)

- **Size:** 4.37 m long, 2.28 m wide (including mirrors), 2.03 m high.
- **Driver:** sits on the **left** (left-hand drive, like Nigeria). Driver's hip point: `[-0.45, 1.18, -0.92]`.
- **Doors:** 0.62 m long, 1.11 m high.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.927, 1.325, -1.480]` | driver's door |
| `door_FR` | `[0.927, 1.325, -1.480]` | passenger door |
| `wheel_FL` | `[-0.719, 0.376, -1.162]` | radius 0.376, width 0.244 |
| `wheel_FR` | `[0.724, 0.376, -1.162]` | |
| `wheel_RL` | `[-0.719, 0.376, 1.176]` | |
| `wheel_RR` | `[0.724, 0.376, 1.176]` | |
| `steering_wheel` | `[-0.450, 1.360, -1.400]` | radius 0.21, tilted 55 deg from vertical (bus-style, quite flat) |

Wheelbase 2.34 m, track 1.44 m.

## VW Corrado (`vw_corrado.glb`)

- **Size:** 3.61 m long, 1.78 m wide (including mirrors), 1.30 m high.
- **Driver:** sits on the **left**. Driver's hip point: `[-0.38, 0.47, 0.12]`.
- **Doors:** 1.16 m long, 0.94 m high (a long coupé door, including the window frame).

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.879, 0.770, -0.654]` | driver's door |
| `door_FR` | `[0.874, 0.770, -0.654]` | passenger door |
| `wheel_FL` | `[-0.780, 0.281, -1.075]` | radius 0.28, width 0.215 |
| `wheel_FR` | `[0.780, 0.281, -1.075]` | |
| `wheel_RL` | `[-0.780, 0.281, 1.214]` | |
| `wheel_RR` | `[0.780, 0.281, 1.214]` | |
| `steering_wheel` | `[-0.380, 0.820, -0.300]` | radius 0.18, tilted 22 deg from vertical |

Wheelbase 2.29 m, track 1.56 m.

## Yellow taxi: Toyota Corolla E180 (`taxi_corolla.glb`)

- **Source:** "2014 Toyota Corolla E180 EU (with interior)" by Armored Wave, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:**
  - Painted taxi yellow, with a roof sign added.
  - The four doors cut out, each pivoted on its hinge.
  - Wheels and steering wheel separated.
  - Maker badges removed.
  - Reduced from 84,000 to 19,159 triangles.
  - Textures reduced to 1024 px.
- **Size:** 4.34 m long, 2.04 m wide (including mirrors), 1.51 m high (including the roof sign). The file is 2.9 MB.
- **Driver:** sits on the **left**.
- **Interior:** the original was kept: seats, dashboard, door cards, centre console and belts.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.845, 0.770, -0.870]` | hinged on its front edge; 1.06 m long, 1.00 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.845, 0.770, -0.870]` | hinged on its front edge; 1.06 m long, 1.00 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.852, 0.770, 0.210]` | hinged on its front edge; 0.69 m long, 1.00 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.852, 0.770, 0.210]` | hinged on its front edge; 0.69 m long, 1.00 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.610, 0.307, -1.253]` | radius 0.31 m |
| `wheel_FR` | `[0.612, 0.307, -1.252]` | radius 0.31 m |
| `wheel_RL` | `[-0.610, 0.307, 1.293]` | radius 0.31 m |
| `wheel_RR` | `[0.610, 0.308, 1.293]` | radius 0.31 m |
| `steering_wheel` | `[-0.359, 0.843, -0.553]` | tilted 14 deg from vertical; spins about its own local Z axis, with positive meaning turning left. Keep the loaded quaternion `q0` and set `steering_wheel.quaternion.copy(q0).multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 0, 1), angle))` |

Each door includes its window, its frame and its inner door card. The front doors also carry the mirrors, as on the real car.

**Seats** are given as hip points: where a seated character's pelvis goes, in metres, in the root node's space.

| Seat | Hip point `[x, y, z]` |
|---|---|
| driver | `[-0.360, 0.600, 0.120]` |
| front passenger | `[0.360, 0.600, 0.120]` |
| rear left | `[-0.360, 0.600, 0.730]` |
| rear right | `[0.360, 0.600, 0.730]` |
| rear middle | `[0.000, 0.600, 0.730]` |

The driver plus three passengers use the driver's seat, the front passenger seat, rear left and rear right. The rear middle seat is a fifth place if you want one.

## BRT bus: Mercedes-Benz Citaro (`brt_bus.glb`)

- **Source:** "Low Poly Mercedes-Benz Citaro 530" by giosassets, **CC-BY 4.0**, credited in `../CREDITS.md`. The source was exterior only.
- **Changes:**
  - Scaled to a real 12.0 m Citaro.
  - Painted red and white: a red body and roof, a white band along the windows, "BRT" in white on both sides and in red on the front, and see-through glass.
  - Wheels rebuilt as clean tyres and rims at the original wheel centres, because the source tyres fall apart when simplified.
  - Passenger doors `door_P1` and `door_P2` cut on the right (kerb) side, plus a driver's door on the left.
  - Wheels and steering wheel separated.
  - A full interior built: floor, inner lining, wheel-arch covers, red fabric seats on pedestals, yellow grab poles at the doors and every second row, ceiling grab rails along the aisle, and a driver's cab with seat, dashboard, partition and steering column.
  - 24,102 triangles, 1.0 MB, no image textures.
- **Size:** 12.02 m long, 2.57 m wide (including mirrors), 3.37 m high.
- **Driver:** sits on the **left**, hip point `[-0.75, 1.01, -4.95]`. Passengers board on the right.
- **Floor:** the passenger floor is at y = 0.36 m. The rear bench sits on a 0.24 m step.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_P1` | `[1.22, 0.29, -4.90]` | passenger door, 1.47 m wide, 2.49 m high, on the right (kerb) side. Pivot at the bottom centre of the door. **Slides**: to open, move it by `[0.07, 0.00, 1.49]`, i.e. 7 cm out from the side and 1.49 m toward the rear, along the outside of the body. Closed = its loaded position. |
| `door_P2` | `[1.23, 0.29, 1.10]` | passenger door, 1.30 m wide, 2.49 m high, on the right (kerb) side. Pivot at the bottom centre of the door. **Slides**: to open, move it by `[0.07, 0.00, 1.32]`, i.e. 7 cm out from the side and 1.32 m toward the rear, along the outside of the body. Closed = its loaded position. |
| `door_FL` | `[-1.26, 1.29, -5.64]` | driver's door, 0.81 m wide, 2.01 m high, on the left. Hinged on its front edge; open with negative `rotation.y` (up to about 80 deg). |
| `wheel_FL` | `[-0.95, 0.48, -3.30]` | radius 0.48 m |
| `wheel_RL` | `[-0.95, 0.48, 2.62]` | radius 0.48 m |
| `wheel_FR` | `[0.95, 0.48, -3.30]` | radius 0.48 m |
| `wheel_RR` | `[0.95, 0.48, 2.62]` | radius 0.48 m |
| `steering_wheel` | `[-0.75, 1.41, -5.40]` | radius 0.25 m, tilted 40 deg from vertical (bus-style). Spin it about its local Z axis, the same as the taxi's; positive means turning left. |

**Passenger seats (29)** are given as hip points `[x, y, z]`, all facing forward (toward -z). They are listed from the front to the rear, left to right. The last 5 are the rear bench.

| Seat | Hip point |
|---|---|
| 1 | `[-0.91, 0.92, -2.34]` |
| 2 | `[-0.48, 0.92, -2.34]` |
| 3 | `[0.48, 0.92, -2.29]` |
| 4 | `[0.91, 0.92, -2.29]` |
| 5 | `[-0.91, 0.92, -1.56]` |
| 6 | `[-0.48, 0.92, -1.56]` |
| 7 | `[0.48, 0.92, -1.51]` |
| 8 | `[0.91, 0.92, -1.51]` |
| 9 | `[-0.91, 0.92, -0.78]` |
| 10 | `[-0.48, 0.92, -0.78]` |
| 11 | `[0.48, 0.92, -0.73]` |
| 12 | `[0.91, 0.92, -0.73]` |
| 13 | `[-0.91, 0.92, 0.00]` |
| 14 | `[-0.48, 0.92, 0.00]` |
| 15 | `[0.48, 0.92, 0.05]` |
| 16 | `[0.91, 0.92, 0.05]` |
| 17 | `[-0.91, 0.92, 3.90]` |
| 18 | `[-0.48, 0.92, 3.90]` |
| 19 | `[0.48, 0.92, 3.95]` |
| 20 | `[0.91, 0.92, 3.95]` |
| 21 | `[-0.91, 0.92, 4.68]` |
| 22 | `[-0.48, 0.92, 4.68]` |
| 23 | `[0.48, 0.92, 4.73]` |
| 24 | `[0.91, 0.92, 4.73]` |
| 25 | `[-0.92, 0.95, 5.45]` |
| 26 | `[-0.46, 0.95, 5.45]` |
| 27 | `[0.00, 0.95, 5.45]` |
| 28 | `[0.46, 0.95, 5.45]` |
| 29 | `[0.92, 0.95, 5.45]` |

**Standing areas** (floor at y = 0.36 m; x across the bus, z along it):

| Area | Across | Along | Floor area |
|---|---|---|---|
| aisle | x -0.27 to 0.27 | z -4.60 to 4.30 | 4.8 m^2 |
| front entry (door_P1) | x 0.00 to 1.14 | z -5.63 to -4.20 | 1.6 m^2 |
| middle area opposite door_P2 (wheelchair / buggy bay) | x -1.14 to 1.14 | z 0.30 to 1.90 | 3.6 m^2 |

Board through `door_P1` at the front, ride seated or standing, and get off through `door_P2` in the middle.

## Sovereign GT (`sovereign_gt.glb`)

- **Type:** premium coupé, the Chief Administrator's car.
- **Source:** "Generic Sport Coupé Car" by Márcio Meireles, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; doors (with their windows and door cards), wheels and steering wheel separated and pivoted; simplified from 114,000 triangles; textures reduced to 1024 px.
- **Size:** 4.73 m long, 2.28 m wide (including mirrors), 1.38 m high.
- **File:** 24,542 triangles, 2.3 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.98, 0.78, -0.52]` | hinged on its front edge; 1.48 m long, 0.98 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.98, 0.78, -0.52]` | hinged on its front edge; 1.48 m long, 0.98 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.84, 0.38, -1.43]` | radius 0.38 m |
| `wheel_FR` | `[0.84, 0.38, -1.43]` | radius 0.38 m |
| `wheel_RL` | `[-0.84, 0.38, 1.51]` | radius 0.38 m |
| `wheel_RR` | `[0.84, 0.38, 1.51]` | radius 0.38 m |
| `steering_wheel` | `[-0.44, 0.83, -0.00]` | tilted 21 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.44, 0.62, 0.29]` |
| front right | `[0.45, 0.62, 0.29]` |

Previews: `previews/sovereign_gt_doors_open.png`, `previews/sovereign_gt_closed.png`, `previews/sovereign_gt_top_open.png`.

## Meridian (`meridian.glb`)

- **Type:** family saloon.
- **Source:** "Generic Sedan Car" by Márcio Meireles, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; four doors (with their windows and door cards), wheels and steering wheel separated and pivoted; simplified from 113,000 triangles; textures reduced to 1024 px.
- **Size:** 4.98 m long, 2.15 m wide (including mirrors), 1.51 m high.
- **File:** 39,522 triangles, 3.8 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.84, 0.84, -1.21]` | hinged on its front edge; 1.42 m long, 1.15 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.84, 0.84, -1.21]` | hinged on its front edge; 1.42 m long, 1.15 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.94, 0.84, 0.07]` | hinged on its front edge; 1.22 m long, 1.15 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.94, 0.84, 0.07]` | hinged on its front edge; 1.22 m long, 1.15 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.82, 0.34, -1.58]` | radius 0.34 m |
| `wheel_FR` | `[0.82, 0.34, -1.58]` | radius 0.34 m |
| `wheel_RL` | `[-0.82, 0.34, 1.34]` | radius 0.34 m |
| `wheel_RR` | `[0.82, 0.34, 1.34]` | radius 0.34 m |
| `steering_wheel` | `[-0.38, 0.95, -0.58]` | tilted 18 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.41, 0.57, -0.30]` |
| front right | `[0.40, 0.57, -0.30]` |
| rear left | `[-0.38, 0.62, 0.69]` |
| rear middle | `[0.00, 0.62, 0.69]` |
| rear right | `[0.38, 0.62, 0.69]` |

Previews: `previews/meridian_doors_open.png`, `previews/meridian_closed.png`, `previews/meridian_top_open.png`.

## Savanna (`savanna.glb`)

- **Type:** small SUV.
- **Source:** "MMC Generic Small SUV Car" by MMC Works, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; four doors (with their windows and door cards), wheels and steering wheel separated and pivoted; simplified from 167,000 triangles; textures reduced to 1024 px.
- **Size:** 4.19 m long, 1.95 m wide (including mirrors), 1.59 m high.
- **File:** 36,523 triangles, 3.4 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.87, 0.92, -0.81]` | hinged on its front edge; 1.16 m long, 1.12 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.87, 0.92, -0.81]` | hinged on its front edge; 1.16 m long, 1.12 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.86, 0.93, 0.22]` | hinged on its front edge; 1.04 m long, 1.10 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.86, 0.93, 0.22]` | hinged on its front edge; 1.05 m long, 1.10 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.74, 0.33, -1.37]` | radius 0.33 m |
| `wheel_FR` | `[0.74, 0.33, -1.37]` | radius 0.33 m |
| `wheel_RL` | `[-0.74, 0.33, 1.29]` | radius 0.33 m |
| `wheel_RR` | `[0.74, 0.33, 1.29]` | radius 0.33 m |
| `steering_wheel` | `[-0.37, 0.74, -0.82]` | tilted -50 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.37, 0.67, 0.04]` |
| rear left | `[-0.38, 0.77, 0.80]` |
| rear middle | `[0.00, 0.77, 0.80]` |
| rear right | `[0.38, 0.77, 0.80]` |
| front right | `[0.37, 0.67, 0.04]` |

Previews: `previews/savanna_doors_open.png`, `previews/savanna_closed.png`, `previews/savanna_top_open.png`.

## Comet (`comet.glb`)

- **Type:** budget hatchback.
- **Source:** "Skoda Felicia w/ Basic Interior (1998 Facelift)" by SimonStrikesBack, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; maker logos and number-plate holders removed; scaled from 1/5 size to a real 3.86 m; the two-sided door parts split into four doors, pivoted with wheels and steering wheel.
- **Size:** 3.88 m long, 1.70 m wide (including mirrors), 1.42 m high.
- **File:** 19,490 triangles, 0.8 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.77, 0.84, -0.67]` | hinged on its front edge; 1.11 m long, 1.02 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.77, 0.84, -0.67]` | hinged on its front edge; 1.11 m long, 1.02 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.77, 0.84, 0.31]` | hinged on its front edge; 1.02 m long, 1.02 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.77, 0.84, 0.31]` | hinged on its front edge; 1.02 m long, 1.02 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.68, 0.30, -1.09]` | radius 0.30 m |
| `wheel_FR` | `[0.68, 0.30, -1.09]` | radius 0.30 m |
| `wheel_RL` | `[-0.68, 0.30, 1.34]` | radius 0.30 m |
| `wheel_RR` | `[0.68, 0.30, 1.34]` | radius 0.30 m |
| `steering_wheel` | `[-0.34, 0.81, -0.42]` | tilted 29 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.37, 0.34, 0.06]` |
| front right | `[0.37, 0.34, 0.06]` |
| rear left | `[-0.38, 0.61, 1.14]` |
| rear middle | `[0.00, 0.61, 1.14]` |
| rear right | `[0.38, 0.61, 1.14]` |

Previews: `previews/comet_doors_open.png`, `previews/comet_closed.png`, `previews/comet_top_open.png`.

## Harmony (`harmony.glb`)

- **Type:** family saloon (the taxi's car in private colours).
- **Source:** "2014 Toyota Corolla E180 EU (with interior)" by Armored Wave, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; painted dark blue; maker badges removed; four doors cut out and pivoted on their hinges, wheels and steering wheel separated; simplified from 84,000 triangles; textures reduced to 1024 px.
- **Size:** 4.34 m long, 2.04 m wide (including mirrors), 1.38 m high.
- **File:** 19,135 triangles, 2.9 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.84, 0.77, -0.87]` | hinged on its front edge; 1.06 m long, 1.00 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.84, 0.77, -0.87]` | hinged on its front edge; 1.06 m long, 1.00 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.85, 0.77, 0.21]` | hinged on its front edge; 0.69 m long, 1.00 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.85, 0.77, 0.21]` | hinged on its front edge; 0.69 m long, 1.00 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.61, 0.31, -1.26]` | radius 0.31 m |
| `wheel_FR` | `[0.61, 0.31, -1.25]` | radius 0.31 m |
| `wheel_RL` | `[-0.61, 0.31, 1.29]` | radius 0.31 m |
| `wheel_RR` | `[0.61, 0.31, 1.29]` | radius 0.31 m |
| `steering_wheel` | `[-0.36, 0.84, -0.55]` | tilted 14 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.36, 0.60, 0.12]` |
| front passenger | `[0.36, 0.60, 0.12]` |
| rear left | `[-0.36, 0.60, 0.73]` |
| rear right | `[0.36, 0.60, 0.73]` |
| rear middle | `[0.00, 0.60, 0.73]` |

Previews: `previews/harmony_doors_open.png`, `previews/harmony_closed.png`, `previews/harmony_top_open.png`.

## Kite (`kite.glb`)

- **Type:** budget city car (kei car).
- **Source:** "2015 Daihastu Cast Sport SAII LA250S" by SIU Car Garage, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; bonnet badge removed; four doors cut out of the shell and pivoted on their hinges; simple interior added (the source had none: lining, floor, dashboard, seats, steering column and steering wheel); wheels separated.
- **Size:** 3.41 m long, 1.78 m wide (including mirrors), 1.86 m high.
- **File:** 27,164 triangles, 1.3 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.73, 0.85, -0.68]` | hinged on its front edge; 1.05 m long, 1.26 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.73, 0.85, -0.68]` | hinged on its front edge; 1.05 m long, 1.26 m high; open with `rotation.y` positive (up to about 70 deg) |
| `door_RL` | `[-0.72, 0.84, 0.38]` | hinged on its front edge; 0.71 m long, 1.28 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_RR` | `[0.72, 0.84, 0.38]` | hinged on its front edge; 0.71 m long, 1.28 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.65, 0.30, -1.17]` | radius 0.29 m |
| `wheel_FR` | `[0.65, 0.30, -1.17]` | radius 0.29 m |
| `wheel_RL` | `[-0.65, 0.30, 1.27]` | radius 0.29 m |
| `wheel_RR` | `[0.65, 0.30, 1.27]` | radius 0.29 m |
| `steering_wheel` | `[-0.33, 1.00, -0.36]` | tilted 25 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.33, 0.74, 0.05]` |
| front right | `[0.33, 0.74, 0.05]` |
| rear left | `[-0.38, 0.76, 0.85]` |
| rear middle | `[0.00, 0.76, 0.85]` |
| rear right | `[0.38, 0.76, 0.85]` |

Previews: `previews/kite_doors_open.png`, `previews/kite_closed.png`, `previews/kite_top_open.png`.

## Vela V12 (`vela_v12.glb`)

- **Type:** fictional sports car.
- **Source:** "Saba V12 '95 - Low poly model" by Daniel Zhabotinsky, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; badges and number plates removed; both doors cut out of the shell (with their windows and the matching part of the interior) and pivoted on their hinges; wheels and steering wheel separated.
- **Size:** 4.51 m long, 2.22 m wide (including mirrors), 1.32 m high.
- **File:** 30,890 triangles, 3.2 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.92, 0.75, -0.90]` | hinged on its front edge; 1.46 m long, 1.01 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.92, 0.75, -0.90]` | hinged on its front edge; 1.46 m long, 1.01 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.77, 0.33, -1.28]` | radius 0.33 m |
| `wheel_FR` | `[0.77, 0.33, -1.28]` | radius 0.33 m |
| `wheel_RL` | `[-0.80, 0.37, 1.47]` | radius 0.37 m |
| `wheel_RR` | `[0.80, 0.37, 1.47]` | radius 0.37 m |
| `steering_wheel` | `[-0.37, 0.78, -0.66]` | tilted 20 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.36, 0.60, 0.15]` |
| front right | `[0.36, 0.60, 0.15]` |

Previews: `previews/vela_v12_doors_open.png`, `previews/vela_v12_closed.png`, `previews/vela_v12_top_open.png`.

## Strada RS (`strada_rs.glb`)

- **Type:** premium sports coupé.
- **Source:** "BMW E46 M3 Sports Car Red" by BaseOptimal, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; maker roundels on the bonnet and boot painted over and the wheel-centre logos covered with plain caps; scaled from model size to a real 4.49 m; both doors cut out of the shell and pivoted on their hinges; wheels separated; simple interior added (the source had none); simplified from 71,000 triangles; textures reduced to 1024 px.
- **Size:** 4.53 m long, 1.91 m wide (including mirrors), 1.42 m high.
- **File:** 36,386 triangles, 2.6 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.88, 0.75, -0.85]` | hinged on its front edge; 1.40 m long, 1.10 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.88, 0.75, -0.85]` | hinged on its front edge; 1.40 m long, 1.10 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.73, 0.34, -1.48]` | radius 0.34 m |
| `wheel_FR` | `[0.73, 0.34, -1.48]` | radius 0.34 m |
| `wheel_RL` | `[-0.72, 0.34, 1.28]` | radius 0.34 m |
| `wheel_RR` | `[0.72, 0.34, 1.28]` | radius 0.34 m |
| `steering_wheel` | `[-0.38, 0.86, -0.17]` | tilted 22 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.38, 0.55, 0.25]` |
| front right | `[0.38, 0.55, 0.25]` |
| rear left | `[-0.38, 0.57, 1.00]` |
| rear middle | `[0.00, 0.57, 1.00]` |
| rear right | `[0.38, 0.57, 1.00]` |

Previews: `previews/strada_rs_doors_open.png`, `previews/strada_rs_closed.png`, `previews/strada_rs_top_open.png`.

## Harmattan GT (`harmattan_gt.glb`)

- **Type:** vintage muscle coupé.
- **Source:** "Ford Falcon GT 1973" by Tom Zimmermann, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; converted from right-hand drive to left-hand drive by mirroring the interior (steering wheel and driver's seat now on the left; check: previews/harmattan_gt_interior.png); maker lettering removed; scaled to a real 4.72 m; both doors cut out of the shell and pivoted on their hinges; wheels cut out of the underside and steering wheel out of the dashboard; simplified from 96,000 triangles; textures reduced to 1024 px.
- **Size:** 4.77 m long, 2.10 m wide (including mirrors), 1.46 m high.
- **File:** 32,347 triangles, 3.8 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.97, 0.81, -0.76]` | hinged on its front edge; 1.50 m long, 0.98 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.97, 0.81, -0.76]` | hinged on its front edge; 1.50 m long, 0.98 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.70, 0.35, -1.48]` | radius 0.35 m |
| `wheel_FR` | `[0.70, 0.35, -1.48]` | radius 0.35 m |
| `wheel_RL` | `[-0.60, 0.34, 1.28]` | radius 0.34 m |
| `wheel_RR` | `[0.60, 0.34, 1.28]` | radius 0.34 m |
| `steering_wheel` | `[-0.42, 0.74, -0.42]` | tilted 12 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| driver | `[-0.40, 0.62, 0.15]` |
| front right | `[0.40, 0.62, 0.15]` |
| rear left | `[-0.40, 0.62, 0.95]` |
| rear middle | `[0.00, 0.62, 0.95]` |
| rear right | `[0.40, 0.62, 0.95]` |

Previews: `previews/harmattan_gt_doors_open.png`, `previews/harmattan_gt_closed.png`, `previews/harmattan_gt_top_open.png`.

## Mula Van (`mula_van.glb`)

- **Type:** budget minivan.
- **Source:** "Suzuki Carry Minivan" by ProPolyModels, **CC-BY 4.0**, credited in `../CREDITS.md`.
- **Changes:** Renamed; maker lettering, wheel logos and number plates removed; turned straight and scaled from centimetres to a real 3.4 m; both front doors cut out of the shell and pivoted on their hinges; wheels and steering wheel separated; simplified from 152,000 triangles.
- **Size:** 3.41 m long, 1.80 m wide (including mirrors), 1.96 m high.
- **File:** 27,410 triangles, 1.8 MB.
- **Driver:** sits on the **left**.

| Part | Pivot `[x, y, z]` (m) | Notes |
|---|---|---|
| `door_FL` | `[-0.75, 1.28, -1.26]` | hinged on its front edge; 0.81 m long, 1.23 m high; open with `rotation.y` negative (up to about 70 deg) |
| `door_FR` | `[0.66, 1.06, -1.24]` | hinged on its front edge; 0.77 m long, 0.79 m high; open with `rotation.y` positive (up to about 70 deg) |
| `wheel_FL` | `[-0.61, 0.31, -0.95]` | radius 0.31 m |
| `wheel_FR` | `[0.61, 0.31, -0.95]` | radius 0.31 m |
| `wheel_RL` | `[-0.62, 0.31, 0.95]` | radius 0.31 m |
| `wheel_RR` | `[0.62, 0.31, 0.95]` | radius 0.31 m |
| `steering_wheel` | `[-0.33, 1.10, -1.25]` | tilted 44 deg from vertical; spins about its own local Z axis, with positive meaning turning left (same as the taxi) |

**Seats** are given as hip points `[x, y, z]`:

| Seat | Hip point |
|---|---|
| front right | `[0.25, 0.95, -0.80]` |
| driver | `[-0.33, 0.95, -0.81]` |

Previews: `previews/mula_van_doors_open.png`, `previews/mula_van_closed.png`, `previews/mula_van_top_open.png`.

## Door check (`previews/`)

For each car: `<car>_driver_open.png` (front-left corner, driver's door open 60 deg), `<car>_top_open.png` (from above, both doors open 60 deg) and `<car>_closed.png` (doors shut).
- **Hinge:** each door was opened by rotating its node about its own vertical axis. Points on the outer skin of the front edge moved at most 1 mm.
- **Opening direction:** the rear edge swung outward.
- **Closed doors:** they fill their openings exactly, because each door was cut out of the body's own surface. They are 4 cm thick, with a dark inner face.
- **One limitation:** both cars' sides lean inward toward the roof, and the hinge axis is vertical. So the top of the window frame sits up to 20 cm (van) or 5 cm (Corrado) inboard of the hinge. When the door opens, that part swings backward into the door opening, not into the pillar.

## Limits of these models

- **Interiors are simple added boxes.** Neither source model had an interior: the windows are painted, opaque glass. You only see the cabin through an open door.
- **No glass to see through.** You can't see into the cabin through the windows.
- **The Corrado is a little small:** 3.61 m against 4.05 m for the real car. It is kept at its source scale.

## Not done yet

- **Audi R8:** removed from the game. The Sovereign GT replaced it everywhere (the practice car, the Chief Admin's car, every garage car; `supabase_sovereign.sql` turns cars saved as Audis into Sovereign GTs). The game draws it from `source/models/sovereign.json`, packed from `sovereign_gt.glb` by `source/models/pack_sovereign.py`, with its doors, wheels and steering wheel joined to the body for now.
- **Car sounds:** not started yet.
