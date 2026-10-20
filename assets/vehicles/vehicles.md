# Vehicles (`vehicles/`)

Two drivable cars with doors, wheels and a steering wheel as separate named parts. Both are **CC0** from OpenGameArt (credits in `../CREDITS.md`).
Parts were cut and pivoted in Blender 5.2; the door pictures in `previews/` are rendered from the exported `.glb` files themselves.

| File | Car | Triangles | Size | Textures |
|---|---|---|---|---|
| `uaz_452.glb` | UAZ-452 utility van ("bukhanka"), low poly | 2,776 | 227 KB | 256 px body, 128 px wheel, 32 px palette (PNG) |
| `vw_corrado.glb` | VW Corrado coupé, low poly | 6,524 | 647 KB | 1467 x 360 px (PNG) |

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
