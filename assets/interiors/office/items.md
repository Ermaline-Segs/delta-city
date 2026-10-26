# Offices and counters

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `executive_desk.glb` | Walnut office desk, 1.6 x 0.8 m, drawer pedestal and modesty panel | 248 | 1.60 x 0.80 x 0.75 | 1.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `filing_cabinet.glb` | Metal file cabinet | 368 | 0.49 x 0.68 x 1.22 | 0.9 MB | [OpenGameArt: Metal File Cabinet](https://opengameart.org/content/metal-file-cabinet) by ulf | **CC-BY 3.0** |
| `meeting_table.glb` | Painted Wooden Table | 600 | 2.41 x 1.14 x 0.96 | 1.7 MB | [Poly Haven: Painted Wooden Table](https://polyhaven.com/a/painted_wooden_table) | CC0 |
| `notice_board.glb` | Wall notice board, 1.2 x 0.9 m: wood frame, felt pin board, pinned notices (hang with its bottom edge about 1.0 m up) | 260 | 1.26 x 0.04 x 0.96 | 2.9 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `office_chair.glb` | Office chair | 2,948 | 0.55 x 0.54 x 1.01 | 0.8 MB | [OpenGameArt: Office Chair](https://opengameart.org/content/office-chair-1) by nisu | CC0 |
| `office_desk.glb` | Metal Office Desk | 2,949 | 2.00 x 0.95 x 0.79 | 1.4 MB | [Poly Haven: Metal Office Desk](https://polyhaven.com/a/metal_office_desk) | CC0 |
| `potted_plant.glb` | Potted Plant 04 | 2,949 | 0.17 x 0.18 x 0.27 | 1.9 MB | [Poly Haven: Potted Plant 04](https://polyhaven.com/a/potted_plant_04) | CC0 |
| `queue_post.glb` | Queue post: chrome post with a 2 m retractable red belt, 0.95 m high | 176 | 0.34 x 0.34 x 0.97 | 0.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `queue_posts_pair.glb` | Two queue posts 1.8 m apart joined by a red belt | 340 | 2.14 x 0.34 x 0.97 | 0.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `service_counter.glb` | Service counter: 3.0 m, marble top at 1.05 m, glass screen with a pass-through gap | 264 | 3.04 x 0.75 x 1.85 | 2.7 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `waiting_chairs.glb` | Three-seat waiting bench: black leather seats on a steel beam | 476 | 1.90 x 0.56 x 0.96 | 0.7 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
