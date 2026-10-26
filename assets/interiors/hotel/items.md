# Hotels

Real-size furniture as `.glb`: metres, +Y up, every file under 5,000 triangles, textures at most 1024 px.

- **Facing:** the front of every piece faces **+Z** in the glTF file. This is three.js default "forward", the side `object.lookAt()` turns toward a target. Each file was checked by rendering it from all four sides. Earlier notes here said -Z, which was wrong.
- **Floor pieces:** the origin is on the floor (lowest point at y = 0), centred under the piece.
- **Wall boards** (notice board, whiteboard): the origin is at the bottom edge, centred. Put the origin on the wall at the bottom height of the board, with +Z into the room.

`preview.png` shows them all to scale.

| File | What it is | Triangles | Width x depth x height (m) | Size | Source | Licence |
|---|---|---|---|---|---|---|
| `armchair.glb` | Arm Chair 01 | 4,950 | 0.85 x 0.77 x 1.07 | 0.7 MB | [Poly Haven: Arm Chair 01](https://polyhaven.com/a/ArmChair_01) | CC0 |
| `coffee_table.glb` | Modern Coffee Table 01 | 4,504 | 0.60 x 1.20 x 0.39 | 1.3 MB | [Poly Haven: Modern Coffee Table 01](https://polyhaven.com/a/modern_coffee_table_01) | CC0 |
| `double_bed.glb` | Hotel double bed, 1.6 x 2.0 m mattress: walnut frame, velvet headboard, white linen, duvet, pillows | 312 | 1.72 x 2.11 x 1.15 | 5.6 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `reception_desk.glb` | Hotel reception desk, 2.6 m: walnut front with brass strip, marble counter at 1.1 m, work top behind | 290 | 2.66 x 0.81 x 1.20 | 1.4 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `sofa.glb` | Sofa 01 | 4,101 | 1.57 x 0.66 x 0.80 | 0.5 MB | [Poly Haven: Sofa 01](https://polyhaven.com/a/Sofa_01) | CC0 |
| `tv_55in.glb` | 55-inch flat-screen TV on its stand feet, 1.23 m wide | 188 | 1.23 x 0.22 x 0.78 | 0.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `tv_unit.glb` | Low walnut TV unit, 1.6 x 0.45 x 0.5 m, with two drawers and an open shelf | 280 | 1.60 x 0.48 x 0.50 | 1.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
| `wardrobe.glb` | Hotel wardrobe, 1.2 x 0.6 x 2.1 m, walnut, two doors with bar handles | 264 | 1.20 x 0.66 x 2.10 | 1.0 MB | Modelled for Delta City in Blender; textures from Poly Haven | CC0 |
