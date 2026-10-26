# Police

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `cell_bars.glb` | Cell front: 3.0 m wide, 2.5 m high steel bars in a frame (the door is cell_door.glb) | 428 | 3.00 x 0.10 x 2.50 | 0.6 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `cell_door.glb` | Cell door: 0.9 x 2.2 m barred steel door with lock box; hinge on its left edge (x = -0.45) | 256 | 0.92 x 0.14 x 2.20 | 0.6 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `filing_cabinet.glb` | Four-drawer steel filing cabinet, 0.47 x 0.62 x 1.32 m | 444 | 0.47 x 0.66 x 1.32 | 0.7 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `front_desk.glb` | Police front desk: 2.4 m, high public counter in front, working desk behind | 184 | 2.44 x 0.90 x 1.15 | 2.9 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `lockers.glb` | Bank of three steel lockers, 0.9 m wide, 1.8 m high, with vents and handles | 560 | 0.90 x 0.48 x 1.80 | 0.7 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
