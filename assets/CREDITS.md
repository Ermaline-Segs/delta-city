# Asset credits

Every file in this folder is either CC0 (public domain) or under a licence that allows free commercial use with no restrictions.

## Ground textures (`textures/`)

All are the colour (diffuse) map only, 1024×1024 JPG, seamless tiling. Downloaded from Poly Haven's 1K JPG files without changes, only renamed.

| File | Source asset | Author / site | Licence |
|---|---|---|---|
| `textures/asphalt_road.jpg` | [Clean Asphalt](https://polyhaven.com/a/clean_asphalt) (`clean_asphalt_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/red_laterite.jpg` | [Red Laterite Soil Stones](https://polyhaven.com/a/red_laterite_soil_stones) (`red_laterite_soil_stones_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/dry_ground.jpg` | [Dry Ground 01](https://polyhaven.com/a/dry_ground_01) (`dry_ground_01_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/grass.jpg` | [Leafy Grass](https://polyhaven.com/a/leafy_grass) (`leafy_grass_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/concrete_pavement.jpg` | [Concrete Pavement](https://polyhaven.com/a/concrete_pavement) (`concrete_pavement_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/plaster_wall.jpg` | [White Plaster 02](https://polyhaven.com/a/white_plaster_02) (`white_plaster_02_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/concrete_wall.jpg` | [Concrete Wall 008](https://polyhaven.com/a/concrete_wall_008) (`concrete_wall_008_diff_1k.jpg`) | Poly Haven | CC0 |

## Trees (`trees/`)

| File | Source asset | Author / site | Licence | Triangles |
|---|---|---|---|---|
| `trees/broadleaf_tree.glb` | `CommonTree_5` from the [Stylized Nature MegaKit (Standard)](https://opengameart.org/content/stylized-nature-megakit) ([quaternius.com](https://quaternius.com/packs/stylizednaturemegakit.html)) | Quaternius | CC0 | 3,182 |
| `trees/palm_tree.glb` | [Palm tree v2 low poly edition](https://opengameart.org/content/palm-tree-v2-low-poly-edition) | Nobiax, polycount reduction by Julius | CC0 (readme: "Absolutely free to use or to modify in any kind of work (personal, commercial or else)") | 451 |
| `trees/shrub.glb` | `Bush_Common_Flowers` from the [Stylized Nature MegaKit (Standard)](https://opengameart.org/content/stylized-nature-megakit) | Quaternius | CC0 | 1,368 |

Changes made:
- The Quaternius models were packed from `.gltf` + `.bin` + PNG textures into a single `.glb`. Geometry, materials and textures are unchanged. The leaves use alpha-masked PNG textures.
- The palm came as OBJ + TGA. It was converted to GLB with Blender: the diffuse TGA (which has an alpha channel) became an embedded PNG, and the leaf material was set to alpha mask (cutoff 0.5), double-sided. The normal and specular maps were not used.
