# Mosque

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `minbar.glb` | Minbar: wooden pulpit stair, seven steps up to a seat under a small canopy; entrance gate at the front; 3.2 m long, 4.0 m high to the top of the dome | 1,216 | 1.00 x 3.24 x 3.99 | 3.4 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `prayer_rug_green.glb` | Prayer rug, 0.7 x 1.15 m, green woven pattern with fringed ends | 36 | 0.70 x 1.20 x 0.01 | 2.3 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `prayer_rug_red.glb` | Prayer rug, 0.7 x 1.15 m, red woven pattern with fringed ends | 36 | 0.70 x 1.20 x 0.01 | 1.2 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
