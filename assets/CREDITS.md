# Asset credits

Most files in this folder are CC0 (public domain). Files marked **CC-BY** may be used freely, including commercially, but the author must be credited in the game (for example on a credits screen).

## Credits required (CC-BY)

- "Bus Stop" by Zsky ([Poly Pizza](https://poly.pizza/m/OWczicNWhO)), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Used as `props/bus_stop.glb`, unchanged.

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

## Building textures (`textures/buildings/`)

All are the colour (diffuse) map only, 1024×1024 JPG, seamless tiling, unchanged apart from the file name.

| File | Source asset | Author / site | Licence |
|---|---|---|---|
| `textures/buildings/glass_facade_a.jpg` | [Facade 001](https://ambientcg.com/view?id=Facade001) (`Facade001_1K-JPG_Color.jpg`) | ambientCG | CC0 |
| `textures/buildings/glass_facade_b.jpg` | [Facade 006](https://ambientcg.com/view?id=Facade006) (`Facade006_1K-JPG_Color.jpg`) | ambientCG | CC0 |
| `textures/buildings/painted_plaster_wall.jpg` | [Painted Plaster Wall](https://polyhaven.com/a/painted_plaster_wall) (`painted_plaster_wall_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/bare_concrete_wall.jpg` | [Concrete Wall 006](https://polyhaven.com/a/concrete_wall_006) (`concrete_wall_006_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/brick_wall.jpg` | [Red Brick](https://polyhaven.com/a/red_brick) (`red_brick_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/corrugated_metal_roof.jpg` | [Corrugated Iron 02](https://polyhaven.com/a/corrugated_iron_02) (`corrugated_iron_02_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/roof_tiles.jpg` | [Roof Tiles](https://polyhaven.com/a/roof_tiles) (`roof_tiles_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/wooden_door.jpg` | [Rough Pine Door](https://polyhaven.com/a/rough_pine_door) (`rough_pine_door_diff_1k.jpg`) | Poly Haven | CC0 |
| `textures/buildings/metal_security_door.jpg` | [Painted Metal Shutter](https://polyhaven.com/a/painted_metal_shutter) (`painted_metal_shutter_diff_1k.jpg`), a roller shutter | Poly Haven | CC0 |

## Street objects (`props/`)

| File | Source asset | Author / site | Licence | Triangles |
|---|---|---|---|---|
| `props/street_lamp.glb` | `light-curved` from [City Kit (Roads)](https://kenney.nl/assets/city-kit-roads) | Kenney | CC0 | 92 |
| `props/traffic_light.glb` | `traffic-light` from [City Kit (Roads)](https://kenney.nl/assets/city-kit-roads) | Kenney | CC0 | 212 |
| `props/car_saloon.glb` | `sedan` from [Car Kit](https://kenney.nl/assets/car-kit) | Kenney | CC0 | 2,032 |
| `props/car_minibus.glb` | `van` from [Car Kit](https://kenney.nl/assets/car-kit) | Kenney | CC0 | 2,082 |
| `props/car_pickup.glb` | `truck` from [Car Kit](https://kenney.nl/assets/car-kit) | Kenney | CC0 | 2,082 |
| `props/market_stall.glb` | [Market Stand](https://poly.pizza/m/DGIM5HGISb) | Quaternius, via Poly Pizza | CC0 1.0 | 1,548 |
| `props/signboard.glb` | [Sign](https://poly.pizza/m/4MSsNFk5fc) | Quaternius, via Poly Pizza | CC0 1.0 | 284 |
| `props/billboard.glb` | [Ad Board](https://poly.pizza/m/8G0qJ84VDS) | Uykucukoala, via Poly Pizza | CC0 1.0 | 400 |
| `props/bench.glb` | [Bench](https://poly.pizza/m/jLxjFxFRpw) | Quaternius, via Poly Pizza | CC0 1.0 | 376 |
| `props/waste_bin.glb` | [Trashcan Small](https://poly.pizza/m/i7HDuYDLkx) | Quaternius, via Poly Pizza | CC0 1.0 | 260 |
| `props/bus_stop.glb` | [Bus Stop](https://poly.pizza/m/OWczicNWhO) | Zsky, via Poly Pizza | **CC-BY 3.0** (credit required) | 456 |

The Kenney models load their shared `Textures/colormap.png` from a separate file. It was embedded into each `.glb` so every file stands alone. Geometry and materials are unchanged. The Poly Pizza models are the site's `.glb` downloads, unchanged.

## Small buildings (`buildings/`)

| File | Source asset | Author / site | Licence | Triangles |
|---|---|---|---|---|
| `buildings/small_shop.glb` | [Building](https://poly.pizza/m/EL3ePInr1N) | Kay Lousberg, via Poly Pizza | CC0 1.0 | 828 |
| `buildings/shop_row.glb` | [Building](https://poly.pizza/m/qOhhGLftam) | Kay Lousberg, via Poly Pizza | CC0 1.0 | 1,356 |
| `buildings/church.glb` | [Church](https://poly.pizza/m/GHzPfvoyzX) | CreativeTrio, via Poly Pizza | CC0 1.0 | 2,265 |

All three are the site's `.glb` downloads, unchanged.
