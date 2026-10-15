# Character creator parts

Each character is **one skinned mesh** on the Rocketbox "Bip01" skeleton. Rocketbox does not split head, body and hair
into separate meshes; they are separate **materials** on that mesh. In the `.glb`, each material is its own primitive of the one mesh, so
a part can be shown, hidden or re-textured by material name. Textures are embedded in the `.glb`; their original Rocketbox file names are
listed here. All are at most 1024 px. Opacity textures are PNG (they need transparency); the rest are JPEG.

All 15 share the same 68 skeleton joints, with the same names in the same order, so animations made for one fit all of them.
The one exception is `Female_Party_02`, which has one extra helper joint, `neutral_bone`, appended at the end (69 in all).

## Male_Adult_12 (M1, man)

`Male_Adult_12.glb` · 6,722 triangles · 1.81 m tall · picture: `Male_Adult_12.png`

Mesh: `m007_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m007_body` | 3,694 | `m007_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m007_head` | 3,028 | `m007_head_color.tga` | 1024x1024 | none |

## Male_Adult_18 (M2, man)

`Male_Adult_18.glb` · 6,434 triangles · 1.81 m tall · picture: `Male_Adult_18.png`

Mesh: `m023_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m023_body` | 4,350 | `m023_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m023_head` | 2,084 | `m023_head_color.tga` | 1024x1024 | none |

## Male_Adult_04 (M3, man)

`Male_Adult_04.glb` · 8,684 triangles · 1.87 m tall · picture: `Male_Adult_04.png`

Mesh: `m006_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m006_body` | 4,760 | `m006_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m006_head` | 3,236 | `m006_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `m006_opacity` | 688 | `m006_opacity_color.tga` | 1024x1024 | alpha mask |

## Business_Male_05 (M4, man)

`Business_Male_05.glb` · 7,164 triangles · 1.80 m tall · picture: `Business_Male_05.png`

Mesh: `m016_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m016_body` | 4,182 | `m016_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m016_head` | 2,982 | `m016_head_color.tga` | 1024x1024 | none |

## Sports_Male_03 (M5, man)

`Sports_Male_03.glb` · 9,534 triangles · 1.84 m tall · picture: `Sports_Male_03.png`

Mesh: `m300_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m300_body` | 4,988 | `m300_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m300_head` | 3,774 | `m300_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `m300_opacity` | 772 | `m300_opacity_color.tga` | 1024x1024 | alpha mask |

## Male_Adult_17 (M6, man)

`Male_Adult_17.glb` · 7,084 triangles · 1.81 m tall · picture: `Male_Adult_17.png`

Mesh: `m022_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m022_body` | 3,880 | `m022_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m022_head` | 3,204 | `m022_head_color.tga` | 1024x1024 | none |

## Male_Adult_15 (M7, man)

`Male_Adult_15.glb` · 7,292 triangles · 1.82 m tall · picture: `Male_Adult_15.png`

Mesh: `m204_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m204_body` | 4,150 | `m204_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m204_head` | 3,142 | `m204_head_color.tga` | 1024x1024 | none |

## Wood_Male_01 (M8, man)

`Wood_Male_01.glb` · 7,108 triangles · 1.81 m tall · picture: `Wood_Male_01.png`

Mesh: `m110_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `m110_body` | 4,018 | `m110_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `m110_head` | 3,090 | `m110_head_color.tga` | 1024x1024 | none |

## Business_Female_01 (W1, woman)

`Business_Female_01.glb` · 8,966 triangles · 1.74 m tall · picture: `Business_Female_01.png`

Mesh: `f014_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f014_body` | 5,146 | `f014_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f014_head` | 3,206 | `f014_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `f014_opacity` | 614 | `f014_opacity_color.tga` | 1024x1024 | alpha mask |

## Female_Party_02 (W2, woman)

`Female_Party_02.glb` · 9,874 triangles · 1.79 m tall · picture: `Female_Party_02.png`

Mesh: `f022_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f022_body` | 5,084 | `f022_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f022_head` | 3,150 | `f022_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `f022_opacity` | 1,640 | `f022_opacity_color.tga` | 1024x1024 | alpha mask |

## Pilot_Female_02 (W3, woman)

`Pilot_Female_02.glb` · 8,458 triangles · 1.78 m tall · picture: `Pilot_Female_02.png`

Mesh: `f169_hipoly_81_bones`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f169_body` | 4,634 | `f169_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f169_head` | 3,186 | `f169_head_color.tga` | 1024x1024 | none |
| hat | `f169_hat` | 638 | `f169_hat_color.tga` | 1024x512 | none |

## Female_Adult_10 (W4, woman)

`Female_Adult_10.glb` · 6,460 triangles · 1.74 m tall · picture: `Female_Adult_10.png`

Mesh: `f201_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f201_body` | 4,332 | `f201_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f201_head` | 1,920 | `f201_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `f201_opacity` | 208 | `f201_opacity_color.tga` | 512x256 | alpha mask |

## Female_Adult_06 (W5, woman)

`Female_Adult_06.glb` · 6,992 triangles · 1.74 m tall · picture: `Female_Adult_06.png`

Mesh: `f202_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f202_body` | 3,634 | `f202_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f202_head` | 3,016 | `f202_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `f202_opacity` | 342 | `f202_opacity_color.tga` | 1024x256 | alpha mask |

## Business_Female_02 (W8, woman)

`Business_Female_02.glb` · 8,640 triangles · 1.73 m tall · picture: `Business_Female_02.png`

Mesh: `f015_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f015_body` | 4,440 | `f015_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f015_head` | 3,186 | `f015_head_color.tga` | 1024x1024 | none |
| glasses | `f015_glasses` | 220 | `f015_glasses_opacity_color.tga` | 512x256 | alpha mask |
| hair / eyelashes (alpha) | `f015_opacity` | 794 | `f015_opacity_color.tga` | 1024x1024 | alpha mask |

## Business_Female_03 (W9, woman)

`Business_Female_03.glb` · 8,438 triangles · 1.74 m tall · picture: `Business_Female_03.png`

Mesh: `f016_hipoly_81_bones_opacity`

| Part | Material | Faces | Texture | Size | Transparency |
|---|---|---|---|---|---|
| body (clothes, hands) | `f016_body` | 5,182 | `f016_body_color.tga` | 1024x1024 | none |
| head (face, skin) | `f016_head` | 2,712 | `f016_head_color.tga` | 1024x1024 | none |
| hair / eyelashes (alpha) | `f016_opacity` | 544 | `f016_opacity_color.tga` | 1024x1024 | alpha mask |
