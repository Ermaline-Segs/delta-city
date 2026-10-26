# Church

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `altar.glb` | Altar table, 2.0 x 0.9 x 1.0 m: oak with panelled front, white linen cloth, brass cross and candlesticks | 456 | 2.10 x 0.96 x 1.55 | 2.8 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `pew.glb` | Church pew, 3.0 m oak with red cushion, kneeler and hymn-book shelf behind | 340 | 3.07 x 0.91 x 0.98 | 2.4 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `pulpit.glb` | Pulpit: raised oak enclosure on a 0.6 m platform with three steps at the side and a sloped book rest | 208 | 2.02 x 1.03 x 1.79 | 2.4 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
