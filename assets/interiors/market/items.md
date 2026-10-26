# Market and shops

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `cash_register.glb` | Cash Register 01 | 4,949 | 0.60 x 0.62 x 0.62 | 1.2 MB | [Poly Haven: Cash Register 01](https://polyhaven.com/a/CashRegister_01) | CC0 |
| `display_shelves.glb` | Wooden Display Shelves 01 | 3,174 | 1.08 x 0.37 x 1.56 | 0.5 MB | [Poly Haven: Wooden Display Shelves 01](https://polyhaven.com/a/wooden_display_shelves_01) | CC0 |
| `market_stall_table.glb` | Market stall table, 2.0 x 1.0 m: wooden planks on trestles under a canvas sun shade | 240 | 2.30 x 1.37 x 2.17 | 2.1 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `produce_crate_plastic.glb` | Plastic Crate 02 | 4,949 | 0.51 x 0.41 x 0.25 | 2.2 MB | [Poly Haven: Plastic Crate 02](https://polyhaven.com/a/plastic_crate_02) | CC0 |
| `produce_crate_wood.glb` | Wooden Crate 02 | 4,949 | 0.53 x 1.17 x 0.46 | 2.1 MB | [Poly Haven: Wooden Crate 02](https://polyhaven.com/a/wooden_crate_02) | CC0 |
| `shelves_steel.glb` | Steel Frame Shelves 01 | 4,348 | 1.10 x 0.50 x 2.14 | 1.5 MB | [Poly Haven: Steel Frame Shelves 01](https://polyhaven.com/a/steel_frame_shelves_01) | CC0 |
| `shop_counter.glb` | Shop counter, 1.8 x 0.6 x 1.0 m: wooden base with a glass display case on top | 252 | 1.84 x 0.64 x 1.20 | 2.9 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `shop_shelf.glb` | Shop shelving unit, 1.2 x 0.5 x 1.6 m, steel with four shelves stocked with packets, tins and bottles | 2,132 | 1.20 x 0.50 x 1.60 | 0.1 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
