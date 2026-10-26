# Courts

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `court_bench.glb` | Public bench for the court gallery: 2.4 m dark wood with backrest | 228 | 2.47 x 0.69 x 0.98 | 1.2 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `dock.glb` | Dock: panelled enclosure for the accused, brass rail on posts, gate at the back and a bench inside | 412 | 2.40 x 1.41 x 1.52 | 2.4 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `judges_bench.glb` | Judge's bench: raised dark-wood desk on a 30 cm platform, panelled front | 248 | 2.68 x 1.46 x 1.40 | 2.1 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `judges_chair.glb` | Judge's high-backed leather chair | 460 | 0.63 x 0.66 x 1.37 | 1.6 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `public_bench.glb` | Painted Wooden Bench | 630 | 1.16 x 0.50 x 0.89 | 1.9 MB | [Poly Haven: Painted Wooden Bench](https://polyhaven.com/a/painted_wooden_bench) | CC0 |
| `witness_stand.glb` | Witness stand: panelled enclosure on a 20 cm platform, book ledge, open back with step | 280 | 1.24 x 1.31 x 1.29 | 2.1 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
