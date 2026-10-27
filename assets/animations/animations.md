# Animations (`animations/`)

Everyday motions for human characters: 20 clips at 24 fps. Every file is **CC0**: they come from Quaternius' [Universal Animation Library 1 and 2](https://quaternius.com/packs/universalanimationlibrary.html), Standard (free) version. No Mixamo files are used.

- **Skeleton:** all clips share Quaternius' universal 65-bone humanoid rig, the UE5-mannequin naming (`root`, `pelvis`, `spine_01-03`, `neck_01`, `Head`, `clavicle_l/r`, `upperarm`, `lowerarm`, `hand`, fingers, `thigh`, `calf`, `foot`, `ball`).
  - **Matches:** Quaternius' Universal Base Characters (also CC0).
  - **Doesn't match:** the Rocketbox characters (`Bip01`) or the MPFB modular characters (`game_engine` rig). Use the retargeted sets in `rocketbox/` and `mpfb/` instead (see the end of this file).
- **No root motion:** clips play in place, so the game moves the character itself.
- **Files:**
  - `<Clip>.glb`: skeleton plus that one clip, no mesh.
  - `animations_all.glb`: the Quaternius mannequin plus every clip, for testing in three.js (`gltf.animations`).
  - `mannequin.glb`: the mannequin alone.
- **Previews:** `previews/<Clip>.png` shows 5 evenly spaced frames from the front-left.
- **Seated clips** (`Sit_*`, `Car_Drive_Loop`) expect a seat about 0.45 m high, with the hips about 0.30 m behind the feet; the pelvis sits at about 0.54 m.
- **`Sleep_Loop` and the end of `Lie_Down`:** lying on the back, head toward +Z in glTF (the character's back on the floor).
- **Built clips:** some clips were built in Blender from library clips, with arm IK and added motion. Their source column says what was combined. They remain CC0.

| File | What it shows | Length | Loops | Source | Licence | Preview |
|---|---|---|---|---|---|---|
| `Idle_Loop.glb` | standing idle | 2.50 s (61 frames) | yes | UAL1 `Idle_Loop` | CC0 | ![](previews/Idle_Loop.png) |
| `Walk_Loop.glb` | walk, in place (no root motion) | 1.33 s (33 frames) | yes | UAL1 `Walk_Loop` | CC0 | ![](previews/Walk_Loop.png) |
| `Get_Up.glb` | from lying on the floor or a bed to standing | 1.53 s (38 frames) | no | UAL2 `LayToIdle` | CC0 | ![](previews/Get_Up.png) |
| `Sit_Down.glb` | standing to seated (chair, toilet, car seat) | 1.30 s (32 frames) | no | UAL1 `Sitting_Enter` | CC0 | ![](previews/Sit_Down.png) |
| `Sit_Idle_Loop.glb` | seated idle (table, toilet, waiting) | 1.67 s (41 frames) | yes | UAL1 `Sitting_Idle_Loop` | CC0 | ![](previews/Sit_Idle_Loop.png) |
| `Sit_Talk_Loop.glb` | seated, talking with gestures | 2.93 s (71 frames) | yes | UAL1 `Sitting_Talking_Loop` | CC0 | ![](previews/Sit_Talk_Loop.png) |
| `Stand_Up.glb` | seated to standing | 1.03 s (26 frames) | no | UAL1 `Sitting_Exit` | CC0 | ![](previews/Stand_Up.png) |
| `Eat_Standing.glb` | eat or drink: hand to mouth and back, standing | 1.33 s (33 frames) | no | UAL2 `Consume` | CC0 | ![](previews/Eat_Standing.png) |
| `Phone_Talk_Loop.glb` | standing, phone held to the ear, talking | 2.93 s (71 frames) | yes | UAL2 `Idle_TalkingPhone_Loop` | CC0 | ![](previews/Phone_Talk_Loop.png) |
| `Carry_Walk_Loop.glb` | walking while carrying a box in both arms | 2.00 s (49 frames) | yes | UAL2 `Walk_Carry_Loop` | CC0 | ![](previews/Carry_Walk_Loop.png) |
| `Pick_Up.glb` | reach down and pick something up from a table | 0.83 s (21 frames) | no | UAL1 `PickUp_Table` | CC0 | ![](previews/Pick_Up.png) |
| `Car_Drive_Loop.glb` | seated, both hands on a steering wheel | 1.67 s (41 frames) | yes | UAL1 `Driving_Loop` | CC0 | ![](previews/Car_Drive_Loop.png) |
| `Interact.glb` | reach out and press or use something (door, switch, counter) | 2.00 s (49 frames) | no | UAL1 `Interact` | CC0 | ![](previews/Interact.png) |
| `Lie_Down.glb` | from standing down to lying on the back (end pose = Sleep_Loop) | 1.54 s (38 frames) | no | UAL2 `LayToIdle` played backwards | CC0 | ![](previews/Lie_Down.png) |
| `Sleep_Loop.glb` | lying on the back, slow breathing | 4.00 s (97 frames) | yes | UAL2 `LayToIdle` first pose + added breathing | CC0 | ![](previews/Sleep_Loop.png) |
| `Sit_Eat_Loop.glb` | seated at a table: right hand from plate to mouth twice per loop, left hand on the table | 2.67 s (65 frames) | yes | UAL1 `Sitting_Idle_Loop` body + arm IK | CC0 | ![](previews/Sit_Eat_Loop.png) |
| `Sit_Type_Loop.glb` | seated at a desk, both hands on a keyboard, alternating taps | 2.00 s (49 frames) | yes | UAL1 `Sitting_Idle_Loop` body + arm IK | CC0 | ![](previews/Sit_Type_Loop.png) |
| `Cook_Stir_Loop.glb` | standing at a stove: left hand holds the pot handle, right hand stirs | 2.50 s (61 frames) | yes | UAL1 `Idle_Loop` body + arm IK | CC0 | ![](previews/Cook_Stir_Loop.png) |
| `Shower_Loop.glb` | standing under a shower, both hands scrubbing the head | 2.67 s (65 frames) | yes | UAL1 `Idle_Loop` body + arm IK | CC0 | ![](previews/Shower_Loop.png) |
| `Carry_Idle_Loop.glb` | standing still while holding a box | 2.50 s (61 frames) | yes | UAL1 `Idle_Loop` body + UAL2 `Walk_Carry_Loop` arms | CC0 | ![](previews/Carry_Idle_Loop.png) |

## Covering the requested actions
- **Lying down and getting up:** `Lie_Down`, `Get_Up`.
- **Sleeping:** `Sleep_Loop`.
- **Sitting at a table and eating:** `Sit_Down`, then `Sit_Eat_Loop`, then `Stand_Up`.
- **Cooking at a stove:** `Cook_Stir_Loop`.
- **Showering:** `Shower_Loop`.
- **Using a toilet:** `Sit_Down`, then `Sit_Idle_Loop`, then `Stand_Up`.
- **Typing at a computer:** `Sit_Type_Loop`.
- **Talking on a phone:** `Phone_Talk_Loop`.
- **Carrying a box:** `Pick_Up`, then `Carry_Walk_Loop` / `Carry_Idle_Loop`.
- **Getting in and out of a car seat:** `Sit_Down`, then `Car_Drive_Loop`, then `Stand_Up`. These are generic sit and stand movements; slide the character sideways into the seat in the game.

## Retargeted sets (Rocketbox and MPFB)

The 20 clips above use the Quaternius rig. They have been retargeted onto the game's own skeletons, so each set plays directly on those characters. Bind by node name; every track was checked to find its bone.

| Folder | Skeleton | Use it for | Hip-height ratio K |
|---|---|---|---|
| `rocketbox/male/` | Rocketbox Biped, male proportions (68 bones) | `Male_Adult_04/12/18`, `Business_Male_05`, `Construction_Male_03/06`, `Military_Male_01/06`, `Pilot_Male_03`, `Police_Male_01/04`, `Security_Male_01`, `Sports_Male_03` **and `Fire_Female_02`** (she uses the male skeleton) | 0.96 |
| `rocketbox/female/` | Rocketbox Biped, female proportions | `Business_Female_01`, `Construction_Female_01`, `Military_Female_02`, `Pilot_Female_02` | 0.991 |
| `mpfb/female/` | MPFB `game_engine` (53 bones), female | `../modular/base_female*.glb` and every female piece | 0.918 |
| `mpfb/male/` | MPFB `game_engine` (53 bones), male | `../modular/base_male*.glb` and every male piece | 1.041 |

Within each Rocketbox family every character has the same rest rotations (within 0.05 degrees) and the same bone lengths, so one set serves the whole family. The MPFB female and male rest poses differ, so each has its own set.

- **Files per folder:**
  - `<Clip>.glb`: that body's skeleton plus one clip, no mesh.
  - `animations_all.glb`: the skeleton plus all 20 clips.
  - `check.json`: the measurements below, per clip.
- **Previews:** five frames each, played on the real skinned character:
  - `rocketbox/previews/<Clip>.png`, on `Male_Adult_12`;
  - `mpfb/previews/<Clip>.png`, on `base_female`.
- **Rerun:**
  - `source/anim/retarget.py` (Blender 5.x, usage at the top of the file) rebuilds a set from `animations_all.glb` and a character.
  - `source/anim/preview.py` renders the strips.

### Bone maps

| Quaternius | Rocketbox | MPFB |
|---|---|---|
| `pelvis` | `Bip01 Pelvis` | `pelvis` |
| `spine_01` | `Bip01 Spine` | `spine_01` |
| `spine_02` | `Bip01 Spine1` | `spine_02` |
| `spine_03` | `Bip01 Spine2` | `spine_03` |
| `neck_01` | `Bip01 Neck` | `neck_01` |
| `Head` | `Bip01 Head` | `head` |
| `clavicle_l/_r` | `Bip01 L/R Clavicle` | `clavicle_l/_r` |
| `upperarm_l/_r` | `Bip01 L/R UpperArm` | `upperarm_l/_r` |
| `lowerarm_l/_r` | `Bip01 L/R Forearm` | `lowerarm_l/_r` |
| `hand_l/_r` | `Bip01 L/R Hand` | `hand_l/_r` |
| `thigh_l/_r` | `Bip01 L/R Thigh` | `thigh_l/_r` |
| `calf_l/_r` | `Bip01 L/R Calf` | `calf_l/_r` |
| `foot_l/_r` | `Bip01 L/R Foot` | `foot_l/_r` |
| `ball_l/_r` | none (Rocketbox has no toe bone) | `ball_l/_r` |
| `thumb_01_l/_r` | `Bip01 L/R Finger0` | `thumb_01_l/_r` |
| `thumb_02_l/_r` | `Bip01 L/R Finger01` | `thumb_02_l/_r` |
| `thumb_03_l/_r` | none (Rocketbox fingers have 2 joints) | `thumb_03_l/_r` |
| `index_01_l/_r` | `Bip01 L/R Finger1` | `index_01_l/_r` |
| `index_02_l/_r` | `Bip01 L/R Finger11` | `index_02_l/_r` |
| `index_03_l/_r` | none (Rocketbox fingers have 2 joints) | `index_03_l/_r` |
| `middle_01_l/_r` | `Bip01 L/R Finger2` | `middle_01_l/_r` |
| `middle_02_l/_r` | `Bip01 L/R Finger21` | `middle_02_l/_r` |
| `middle_03_l/_r` | none (Rocketbox fingers have 2 joints) | `middle_03_l/_r` |
| `ring_01_l/_r` | `Bip01 L/R Finger3` | `ring_01_l/_r` |
| `ring_02_l/_r` | `Bip01 L/R Finger31` | `ring_02_l/_r` |
| `ring_03_l/_r` | none (Rocketbox fingers have 2 joints) | `ring_03_l/_r` |
| `pinky_01_l/_r` | `Bip01 L/R Finger4` | `pinky_01_l/_r` |
| `pinky_02_l/_r` | `Bip01 L/R Finger41` | `pinky_02_l/_r` |
| `pinky_03_l/_r` | none (Rocketbox fingers have 2 joints) | `pinky_03_l/_r` |

Rocketbox's foot keeps its rest angle to the shin, because it has no toe bone. Unmapped bones (Rocketbox face bones, MPFB `Root`) stay at rest.

### Ground contact

The floor is measured on the deformed skin, not the bones: the lowest skin vertex, every frame.

- **Standing clips:** one fixed height offset per clip and body, so the soles touch y = 0.
- **Seated clips** (`Car_Drive_Loop`, `Sit_Down`, `Sit_Idle_Loop`, `Sit_Talk_Loop`, `Sit_Eat_Loop`, `Sit_Type_Loop`, `Stand_Up`) keep their seat height. They only get the body's own sole correction (its `Idle_Loop` offset) and are never pulled down to the floor.
- **Per-frame contact, smoothed** (no popping): only `Lie_Down`, `Sleep_Loop` and `Get_Up`.
- **Flat floor only:** steps, kerbs and slopes are for the game to handle.

| Body | Standing offset (m) | Pelvis height seated (m) | Pelvis height standing (m) | Lowest skin point, all clips (m) | In-place walk speed (m/s) |
|---|---|---|---|---|---|
| Rocketbox male skeleton (`Male_Adult_12`) | +0.002 | 0.537 | 0.859 | -0.001 | 0.94 |
| Rocketbox female skeleton (`Business_Female_01`) | +0.003 | 0.554 | 0.887 | -0.001 | 0.96 |
| MPFB female (`base_female`) | +0.007 | 0.532 | 0.840 | -0.001 | 0.89 |
| MPFB male (`base_male`) | +0.012 | 0.598 | 0.947 | -0.001 | 1.03 |

The walk clips play in place. Move the character forward at about the speed in the last column so the planted foot does not slide.

### Hands

- **Wrists follow the source wrists.** Near the head (mouth, ear, scrubbing) they are measured from the head. Elsewhere (plate, keyboard, pot) they are measured from the same-side shoulder, scaled by arm reach.
- **Added hand poses:**
  - `Sit_Type_Loop`, both hands: palms down, fingers forward and tipped 20 degrees down, a light curl.
  - `Sit_Eat_Loop`, the left hand: the same pose, resting on the table.
  - `Phone_Talk_Loop`, the right hand: fingers curled round a phone.
  - `Eat_Standing`, the left hand: fingers closed as if holding food; as the source hand rises, the wrist is led to a point just under the chin, so the hand reaches the mouth at the top of the lift.
- **Where the hands land** (character facing +Z, origin on the floor under the hips):
  - **Typing:** wrists 0.79 to 0.86 m high, 0.55 m in front of the pelvis, which suits a 0.74 m desk.
  - **Cooking:** left wrist at 1.0 m on the pot handle; right wrist stirring at 1.1 m, 0.4 m in front.
  - **Eating seated:** the right wrist comes within 0.12 to 0.14 m of the head bone (the mouth) twice per loop.
  - **Showering:** both wrists stay 0.14 to 0.16 m from the head bone, on the head.
  - **Phone:** the wrist is beside the ear, about 0.2 m from the head bone.

### Test results

Tested in three.js r160: every clip on all four bodies, at phone size (375x812) and desktop size (1280x800).

All 80 clip/body pairs passed the automatic checks:
- every track bound to a bone;
- no NaN values;
- the skin never more than 2 mm below the floor;
- seated pelvis heights match Blender's to the millimetre.

The table below gives the visual verdict.

| Clip | Rocketbox male | Rocketbox female | MPFB female | MPFB male | Notes |
|---|---|---|---|---|---|
| `Idle_Loop` | pass | pass | pass | pass |  |
| `Car_Drive_Loop` | pass | pass | pass | pass |  |
| `Carry_Idle_Loop` | pass | pass | pass | pass |  |
| `Carry_Walk_Loop` | pass | pass | pass | pass | Plays in place, like `Walk_Loop`. |
| `Cook_Stir_Loop` | pass | pass | pass | pass |  |
| `Eat_Standing` | pass | pass | pass | pass | The closed left hand comes up to the mouth (wrist within 2 cm of its target under the chin, 0.13 to 0.14 m from the head bone, at mid-clip). The source clip stops in front of the chest, so the retarget adds a mouth target for this clip. |
| `Get_Up` | pass | pass | pass | pass | Per-frame contact, as `Lie_Down`. |
| `Interact` | pass | pass | pass | pass |  |
| `Lie_Down` | pass | pass | pass | pass | Per-frame contact. The feet slide while the body rolls down, as in the source. |
| `Phone_Talk_Loop` | pass | pass | pass | pass | A closed hand beside the ear, a few cm off it; a phone prop fills the gap. The Rocketbox fist has 2 finger joints and MPFB 3; both read as holding something. |
| `Pick_Up` | pass | pass | pass | pass |  |
| `Shower_Loop` | pass | pass | pass | pass |  |
| `Sit_Down` | pass | pass | pass | pass | The feet shuffle 2 to 4 cm, as in the source. |
| `Sit_Eat_Loop` | pass | pass | pass | pass |  |
| `Sit_Idle_Loop` | pass | pass | pass | pass |  |
| `Sit_Talk_Loop` | pass | pass | pass | pass |  |
| `Sit_Type_Loop` | pass | pass | pass | pass | Palms down over the keys. Rocketbox curls only 2 joints per finger, so its fingers look a little stiffer than MPFB's. |
| `Sleep_Loop` | pass | pass | pass | pass | Per-frame contact; flat on the back. |
| `Stand_Up` | pass | pass | pass | pass | As `Sit_Down`. |
| `Walk_Loop` | pass | pass | pass | pass | Plays in place; move the character at the walk speed above. |

The game draws with its own WebGL code, not three.js. This test proves the files are valid glTF that bind by node name; the game's own loader still has to be checked in the game.
