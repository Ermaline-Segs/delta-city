# University

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

- **`lecture_seating.glb`:** the writing desk is on the **+Z** side of the seats, so seated students face +Z. Point +Z at the lecturer.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `bookshelf.glb` | Wooden Display Shelves 01 | 2,950 | 1.08 x 0.37 x 1.56 | 0.4 MB | [Poly Haven: Wooden Display Shelves 01](https://polyhaven.com/a/wooden_display_shelves_01) | CC0 |
| `classroom_chair.glb` | School Chair 01 | 2,950 | 0.57 x 0.68 x 1.01 | 0.4 MB | [Poly Haven: School Chair 01](https://polyhaven.com/a/SchoolChair_01) | CC0 |
| `classroom_desk.glb` | School Desk 01 | 2,949 | 0.71 x 0.55 x 0.88 | 0.4 MB | [Poly Haven: School Desk 01](https://polyhaven.com/a/SchoolDesk_01) | CC0 |
| `lab_bench.glb` | Laboratory bench, 2.4 x 0.75 m: white cabinets, black resin top, sink with gooseneck tap, reagent shelf | 796 | 2.44 x 0.78 x 1.55 | 0.1 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `lectern.glb` | Lectern: oak, 1.15 m, sloped reading top with a lip | 104 | 0.66 x 0.52 x 1.16 | 1.3 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `lecture_seating.glb` | Lecture-hall row: four upholstered seats with a continuous writing desk in front, 2.2 m | 548 | 2.25 x 0.92 x 1.03 | 3.7 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `library_bookshelf.glb` | Wooden Bookshelf Worn | 4,950 | 1.37 x 0.58 x 2.06 | 2.5 MB | [Poly Haven: Wooden Bookshelf Worn](https://polyhaven.com/a/wooden_bookshelf_worn) | CC0 |
| `library_shelves.glb` | Double-sided library shelving, 1.0 x 0.6 x 2.0 m, oak, five shelves a side filled with books | 3,116 | 1.00 x 0.60 x 2.00 | 1.5 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `microscope.glb` | Industrial Microscope | 2,950 | 0.21 x 0.50 x 0.46 | 1.9 MB | [Poly Haven: Industrial Microscope](https://polyhaven.com/a/industrial_microscope) | CC0 |
| `reading_table.glb` | Wooden Table 02 | 196 | 1.13 x 0.71 x 0.80 | 0.5 MB | [Poly Haven: Wooden Table 02](https://polyhaven.com/a/wooden_table_02) | CC0 |
| `whiteboard.glb` | Wall whiteboard, 1.8 x 1.2 m, aluminium frame and pen tray (hang with its bottom edge about 0.9 m up) | 304 | 1.84 x 0.09 x 1.25 | 0.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
