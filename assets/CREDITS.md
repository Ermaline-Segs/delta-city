# Asset credits

Most files in this folder are CC0 (public domain). Files marked **CC-BY** may be used freely, including commercially, but the author must be credited in the game (for example on a credits screen).

## Credits required (CC-BY)

- "Bus Stop" by Zsky ([Poly Pizza](https://poly.pizza/m/OWczicNWhO)), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Used as `props/bus_stop.glb`, unchanged.
- "Small Hospital Bed" by qubodup ([OpenGameArt](https://opengameart.org/content/small-hospital-bed)), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Converted to `interiors/hospital/hospital_bed.glb`.
- "Hospital Screen" by ouren ([OpenGameArt](https://opengameart.org/content/hospital-screen)), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Converted and scaled to `interiors/hospital/curtain_screen.glb`.
- "Metal File Cabinet" by ulf ([OpenGameArt](https://opengameart.org/content/metal-file-cabinet)), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Converted to `interiors/office/filing_cabinet.glb`, with the loose paper folder removed.

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

## Characters (`characters/`)

From the [Microsoft Rocketbox avatar library](https://github.com/microsoft/Microsoft-Rocketbox), © 2020 Microsoft, under the **MIT licence** (full text below; it must be kept with these files).

| File | Rocketbox character | Triangles | Height |
|---|---|---|---|
| `characters/Male_Adult_12.glb` | `Assets/Avatars/Adults/Male_Adult_12` | 6,722 | 1.81 m |
| `characters/Male_Adult_18.glb` | `Assets/Avatars/Adults/Male_Adult_18` | 6,434 | 1.81 m |
| `characters/Male_Adult_04.glb` | `Assets/Avatars/Adults/Male_Adult_04` | 8,684 | 1.87 m |
| `characters/Business_Male_05.glb` | `Assets/Avatars/Professions/Business_Male_05` | 7,164 | 1.80 m |
| `characters/Construction_Male_03.glb` | `Assets/Avatars/Professions/Construction_Male_03` | 9,376 | 1.85 m |
| `characters/Military_Male_01.glb` | `Assets/Avatars/Professions/Military_Male_01` | 15,387 | 1.84 m |
| `characters/Sports_Male_03.glb` | `Assets/Avatars/Professions/Sports_Male_03` | 9,534 | 1.84 m |
| `characters/Business_Female_01.glb` | `Assets/Avatars/Professions/Business_Female_01` | 8,966 | 1.74 m |
| `characters/Pilot_Female_02.glb` | `Assets/Avatars/Professions/Pilot_Female_02` | 8,458 | 1.78 m |
| `characters/Military_Female_02.glb` | `Assets/Avatars/Professions/Military_Female_02` | 12,957 | 1.78 m |
| `characters/Fire_Female_02.glb` | `Assets/Avatars/Professions/Fire_Female_02` | 11,932 | 1.86 m |

Each `.png` next to a `.glb` is a front-view render of the converted file.

Changes made: each character's plain `.fbx` (not the `_facial` one) was converted to a single `.glb` with Blender 3.6 in background mode. Only the colour textures and, where present, the opacity texture (used for hair and eyelashes) were kept; normal and specular maps were dropped. The skeleton (68 bones) and skinning were kept, with no animations. Textures are JPEG, except the opacity textures, which Blender saves as PNG because JPEG cannot hold transparency.

```
MIT License

Copyright (c) 2020 Microsoft

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Interior furniture and equipment (`interiors/`)

Realistic models with photographic textures, at real-world size in metres (bottom on the floor, centred on the origin). All were converted to `.glb` with Blender 5.2. Models over 3,000 triangles were reduced with Blender's Decimate (collapse) modifier; the "Original" column shows their triangle count before that.

| File | Source asset | Author / site | Licence | Triangles | Original | Size (m, W×D×H) |
|---|---|---|---|---|---|---|
| `interiors/university/classroom_desk.glb` | [School Desk 01](https://polyhaven.com/a/SchoolDesk_01) | Poly Haven | CC0 | 2,949 | 4,162 | 0.71×0.55×0.88 |
| `interiors/university/classroom_chair.glb` | [School Chair 01](https://polyhaven.com/a/SchoolChair_01) | Poly Haven | CC0 | 2,950 | 5,072 | 0.57×0.68×1.01 |
| `interiors/university/bookshelf.glb` | [Wooden Display Shelves 01](https://polyhaven.com/a/wooden_display_shelves_01) | Poly Haven | CC0 | 2,950 | 3,174 | 0.37×1.08×1.56 |
| `interiors/university/reading_table.glb` | [Wooden Table 02](https://polyhaven.com/a/wooden_table_02) | Poly Haven | CC0 | 196 | – | 1.13×0.71×0.80 |
| `interiors/university/microscope.glb` | [Industrial Microscope](https://polyhaven.com/a/industrial_microscope) | Poly Haven | CC0 | 2,950 | 16,598 | 0.21×0.50×0.46 |
| `interiors/hospital/hospital_bed.glb` | [Small Hospital Bed](https://opengameart.org/content/small-hospital-bed) | qubodup, OpenGameArt | **CC-BY 3.0** | 540 | – | 1.15×2.20×1.05 |
| `interiors/hospital/curtain_screen.glb` | [Hospital Screen](https://opengameart.org/content/hospital-screen) | ouren, OpenGameArt | **CC-BY 3.0** | 1,368 | – | 1.51×0.34×1.80 |
| `interiors/hospital/waiting_chair.glb` | [Plastic Monobloc Chair 01](https://polyhaven.com/a/plastic_monobloc_chair_01) | Poly Haven | CC0 | 2,950 | 3,356 | 0.64×0.63×0.88 |
| `interiors/office/office_desk.glb` | [Metal Office Desk](https://polyhaven.com/a/metal_office_desk) | Poly Haven | CC0 | 2,949 | 6,898 | 2.00×0.95×0.79 |
| `interiors/office/office_chair.glb` | [Office Chair](https://opengameart.org/content/office-chair-1) | nisu, OpenGameArt | CC0 | 2,948 | 4,674 | 0.55×0.54×1.01 |
| `interiors/office/filing_cabinet.glb` | [Metal File Cabinet](https://opengameart.org/content/metal-file-cabinet) | ulf, OpenGameArt | **CC-BY 3.0** | 368 | – | 0.49×0.68×1.22 |
| `interiors/office/meeting_table.glb` | [Painted Wooden Table](https://polyhaven.com/a/painted_wooden_table) | Poly Haven | CC0 | 600 | – | 2.41×1.14×0.96 |
| `interiors/office/potted_plant.glb` | [Potted Plant 04](https://polyhaven.com/a/potted_plant_04) (small succulent) | Poly Haven | CC0 | 2,949 | 8,929 | 0.17×0.18×0.27 |
| `interiors/court/public_bench.glb` | [Painted Wooden Bench](https://polyhaven.com/a/painted_wooden_bench) | Poly Haven | CC0 | 630 | – | 1.16×0.50×0.89 |

Poly Haven models keep their 1K colour, normal and roughness/metal textures. The OpenGameArt models use their colour texture only.
