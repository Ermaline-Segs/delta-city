# Hospital

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `curtain_screen.glb` | Hospital curtain screen on wheels | 1,368 | 1.51 x 0.34 x 1.80 | 0.4 MB | [OpenGameArt: Hospital Screen](https://opengameart.org/content/hospital-screen) by ouren | **CC-BY 3.0** |
| `hospital_bed.glb` | Small hospital bed | 540 | 1.15 x 2.19 x 1.05 | 0.2 MB | [OpenGameArt: Small Hospital Bed](https://opengameart.org/content/small-hospital-bed) by qubodup | **CC-BY 3.0** |
| `waiting_chair.glb` | Plastic monobloc waiting chair | 2,950 | 0.64 x 0.63 x 0.88 | 1.9 MB | [Poly Haven: Plastic Monobloc Chair 01](https://polyhaven.com/a/plastic_monobloc_chair_01) | CC0 |
