# Vehicles (`vehicles/`)

Four drivable vehicles with doors, wheels and a steering wheel as separate named parts. The van and the Corrado are **CC0** from OpenGameArt. The taxi and the BRT bus are **CC-BY 4.0** from Sketchfab, and their authors must be credited (they're listed under "Credits required" in `../CREDITS.md`).
Parts were cut and pivoted in Blender 5.2; the door pictures in `previews/` are rendered from the exported `.glb` files themselves.

| File | Car | Triangles | Size | Textures |
|---|---|---|---|---|
| `uaz_452.glb` | UAZ-452 utility van ("bukhanka"), low poly | 2,776 | 227 KB | 256 px body, 128 px wheel, 32 px palette (PNG) |
| `vw_corrado.glb` | VW Corrado coupé, low poly | 6,524 | 647 KB | 1467 x 360 px (PNG) |
| `taxi_corolla.glb` | Toyota Corolla E180 saloon as a yellow taxi, 4 doors, full interior | 19,118 | 2.9 MB | up to 1024 px (JPEG) |
| `brt_bus.glb` | Mercedes-Benz Citaro 12 m city bus, red and white with BRT lettering, sliding passenger doors, seats and poles | 24,102 | 1.0 MB | none (plain materials) |
| `sovereign_gt.glb` | Sovereign GT: premium coupé, the Chief Administrator's car | 24,542 | 2.3 MB | up to 1024 px (JPEG) |

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
  - Reduced from 84,000 to 19,118 triangles.
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

- **Audi R8:** the original model is not in the repository. Only `source/models/audi.json` is there, a packed copy made from `Downloads/Audi+R8.glb`: about 93,000 triangles, vertex colours, no recorded author or licence. It was not converted.
- **Car sounds:** not started yet.
