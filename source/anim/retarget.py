# Retarget the 20 Delta City clips (Quaternius UAL rig) onto another humanoid skeleton by bone name.
# Usage (Blender 5.x):
#   blender -b --factory-startup -P retarget.py -- <assets/animations/animations_all.glb> <character.glb> <rocketbox|mpfb> <out_dir>
# Writes <out>/<Clip>.glb (the character's skeleton + one clip, no mesh), <out>/animations_all.glb (skeleton + all clips)
# and <out>/check.json (offsets, seat heights, lowest skin point, foot slide, hand reach).
#
# How it works:
#  1. Facing: both rigs are turned to face the same way (forward = character's left x up, left from the thighs).
#  2. Matched rest: each target bone is turned so its direction (its head to the next bone's head) equals the source
#     bone's rest direction. Bones at the end of a chain (hands, feet, finger tips, head) take their parent's turn.
#     Bone tails are never used: the glTF importer invents them, and on the Rocketbox rig they are meaningless.
#  3. Every frame, every mapped bone gets the source bone's world rotation change on top of its matched rest. The pelvis
#     also gets the source's movement, scaled by the ratio of hip heights (K).
#  4. Two-bone IK, solved here (no Blender constraints). Ankles: the source ankle relative to the pelvis, sideways scaled
#     by hip width, forward by K, height from the target's own rest ankle. Wrists (eating, typing, cooking, showering,
#     phone): the source wrist measured from the head when near it, else from the same-side shoulder scaled by arm reach.
#     The knee / elbow stays in the plane it bends in during the source motion.
#  5. Ground contact, measured on the deformed skin (not the bones): one fixed height offset per clip; seated clips keep
#     their seat height and only get the body's own sole correction from Idle_Loop (never pulled down to the floor);
#     Lie_Down, Sleep_Loop and Get_Up use smoothed per-frame contact.
import bpy, sys, os, json, math, mathutils
import numpy as np
V, Q, M = mathutils.Vector, mathutils.Quaternion, mathutils.Matrix
SRC, TGT, RIG, OUT = sys.argv[sys.argv.index('--') + 1:][:4]
os.makedirs(OUT, exist_ok=True)

SEATED = {'Car_Drive_Loop', 'Sit_Down', 'Sit_Idle_Loop', 'Sit_Talk_Loop', 'Sit_Eat_Loop', 'Sit_Type_Loop', 'Stand_Up'}
PER_FRAME = {'Lie_Down', 'Sleep_Loop', 'Get_Up'}
SMOOTH_SIGMA = 3.0      # frames, for the per-frame contact clips

UAL = ['pelvis', 'spine_01', 'spine_02', 'spine_03', 'neck_01', 'Head', 'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l',
       'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r', 'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
FING = ['thumb', 'index', 'middle', 'ring', 'pinky']
if RIG == 'mpfb':
    MAP = {b: ('head' if b == 'Head' else b) for b in UAL}
    for s in 'lr':
        for f in FING:
            for k in (1, 2, 3):
                MAP[f'{f}_0{k}_{s}'] = f'{f}_0{k}_{s}'
else:
    MAP = {'pelvis': 'Bip01 Pelvis', 'spine_01': 'Bip01 Spine', 'spine_02': 'Bip01 Spine1', 'spine_03': 'Bip01 Spine2',
           'neck_01': 'Bip01 Neck', 'Head': 'Bip01 Head'}
    for s, S_ in (('l', 'L'), ('r', 'R')):
        MAP.update({f'clavicle_{s}': f'Bip01 {S_} Clavicle', f'upperarm_{s}': f'Bip01 {S_} UpperArm', f'lowerarm_{s}': f'Bip01 {S_} Forearm',
                    f'hand_{s}': f'Bip01 {S_} Hand', f'thigh_{s}': f'Bip01 {S_} Thigh', f'calf_{s}': f'Bip01 {S_} Calf', f'foot_{s}': f'Bip01 {S_} Foot'})
        for i, f in enumerate(FING):   # Rocketbox fingers have two joints: Finger<i> and Finger<i>1
            MAP[f'{f}_01_{s}'] = f'Bip01 {S_} Finger{i}'; MAP[f'{f}_02_{s}'] = f'Bip01 {S_} Finger{i}1'

# ---- load
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
src = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
for o in [o for o in bpy.data.objects if o.type != 'ARMATURE']:
    bpy.data.objects.remove(o, do_unlink=True)
src_actions = list(bpy.data.actions)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=TGT)
tgt = [o for o in bpy.data.objects if o.type == 'ARMATURE' and o not in before][0]
for o in [o for o in bpy.data.objects if o not in before and o.type not in ('ARMATURE', 'MESH')]:
    bpy.data.objects.remove(o, do_unlink=True)
skin = [o for o in bpy.data.objects if o.type == 'MESH' and o not in before and any(m.type == 'ARMATURE' and m.object == tgt for m in o.modifiers)]
for o in [o for o in bpy.data.objects if o.type == 'MESH' and o not in before and o not in skin]:
    bpy.data.objects.remove(o, do_unlink=True)    # stray unskinned meshes (e.g. an Icosphere in some Rocketbox files)
for a in [a for a in bpy.data.actions if a not in src_actions]:
    bpy.data.actions.remove(a)
sc = bpy.context.scene; FPS = sc.render.fps
MAP = {s: t for s, t in MAP.items() if s in src.data.bones and t in tgt.data.bones}
print('MAPPED', len(MAP), 'bones; skinned meshes', len(skin), flush=True)
for ob in (src, tgt):
    if ob.animation_data is None:
        ob.animation_data_create()


def use(ob, act):
    ob.animation_data.action = act
    if act is not None and hasattr(ob.animation_data, 'action_slot') and act.slots:
        ob.animation_data.action_slot = act.slots[0]


# ---- facing
def front(ob, l, r):
    mw = ob.matrix_world; lv = (mw @ ob.data.bones[l].head_local) - (mw @ ob.data.bones[r].head_local); lv.z = 0
    return lv.normalized().cross(V((0, 0, 1))).normalized()


fs = front(src, 'thigh_l', 'thigh_r'); ft = front(tgt, MAP['thigh_l'], MAP['thigh_r'])
ang = math.atan2(fs.x * ft.y - fs.y * ft.x, fs.x * ft.x + fs.y * ft.y)
src.rotation_mode = 'XYZ'; src.rotation_euler.z += ang; bpy.context.view_layer.update()
print('FACING turn source by', round(math.degrees(ang), 1), 'deg', flush=True)

# ---- scale from hip heights at rest
hip_s = (src.matrix_world @ src.data.bones['thigh_l'].head_local).z
hip_t = (tgt.matrix_world @ tgt.data.bones[MAP['thigh_l']].head_local).z
K = hip_t / hip_s
print('SCALE hips', round(hip_s, 3), round(hip_t, 3), 'K', round(K, 3), flush=True)

# ---- rest data (target armature space unless noted)
TW = tgt.matrix_world.copy(); TWi = TW.inverted(); TWr = TW.to_quaternion(); TWri = TWr.inverted(); TW3i = TW.to_3x3().inverted()
tb = tgt.data.bones; sb = src.data.bones
order = [b.name for b in tb]          # parents come before children
rest_arm = {b.name: b.matrix_local.copy() for b in tb}
rel = {b.name: (rest_arm[b.parent.name].inverted() @ rest_arm[b.name]) if b.parent else rest_arm[b.name] for b in tb}
src_rest_world = {s: (src.matrix_world.to_quaternion() @ sb[s].matrix_local.to_quaternion()) for s in MAP}
T2S = {t: s for s, t in MAP.items()}

NEXT = {'pelvis': 'spine_01', 'spine_01': 'spine_02', 'spine_02': 'spine_03', 'spine_03': 'neck_01', 'neck_01': 'Head'}
PARENT_S = {}
for s_ in 'lr':
    NEXT.update({f'clavicle_{s_}': f'upperarm_{s_}', f'upperarm_{s_}': f'lowerarm_{s_}', f'lowerarm_{s_}': f'hand_{s_}',
                 f'thigh_{s_}': f'calf_{s_}', f'calf_{s_}': f'foot_{s_}', f'foot_{s_}': f'ball_{s_}'})
    PARENT_S.update({f'hand_{s_}': f'lowerarm_{s_}', f'foot_{s_}': f'calf_{s_}', f'ball_{s_}': f'foot_{s_}'})
    for fi in FING:
        NEXT[f'{fi}_01_{s_}'] = f'{fi}_02_{s_}'; NEXT[f'{fi}_02_{s_}'] = f'{fi}_03_{s_}'
        PARENT_S.update({f'{fi}_01_{s_}': f'hand_{s_}', f'{fi}_02_{s_}': f'{fi}_01_{s_}', f'{fi}_03_{s_}': f'{fi}_02_{s_}'})
corr = {}


def get_corr(s):
    """world-space turn that brings the target bone's rest direction onto the source bone's rest direction"""
    if s not in corr:
        n = NEXT.get(s)
        if n in MAP:
            d_s = (src.matrix_world @ sb[n].head_local) - (src.matrix_world @ sb[s].head_local)
            d_t = (TW @ tb[MAP[n]].head_local) - (TW @ tb[MAP[s]].head_local)
            corr[s] = d_t.normalized().rotation_difference(d_s.normalized())
        elif PARENT_S.get(s) in MAP:
            corr[s] = get_corr(PARENT_S[s])
        else:
            corr[s] = Q()
    return corr[s]


matched = {t: TWri @ get_corr(s) @ TWr @ rest_arm[t].to_quaternion() for s, t in MAP.items()}

HEAD_T = MAP['Head']
LEG = {s_: (MAP[f'thigh_{s_}'], MAP[f'calf_{s_}'], MAP[f'foot_{s_}']) for s_ in 'lr'}
ARM = {s_: (MAP[f'upperarm_{s_}'], MAP[f'lowerarm_{s_}'], MAP[f'hand_{s_}']) for s_ in 'lr'}
fwd = ft.copy(); left = V((0, 0, 1)).cross(fwd).normalized() * -1
if (TW @ tb[MAP['thigh_l']].head_local - TW @ tb[MAP['thigh_r']].head_local).dot(left) < 0:
    left = -left
fwd_a = (TW3i @ fwd).normalized()
ank_s = {s_: src.matrix_world @ sb['foot_' + s_].head_local for s_ in 'lr'}
hipw = lambda ob, l, r: ((ob.matrix_world @ ob.data.bones[l].head_local) - (ob.matrix_world @ ob.data.bones[r].head_local)).length
HR = hipw(tgt, MAP['thigh_l'], MAP['thigh_r']) / hipw(src, 'thigh_l', 'thigh_r')     # hip-width ratio, for foot spacing
reach = lambda ob, u, l, h: ((ob.matrix_world @ ob.data.bones[l].head_local) - (ob.matrix_world @ ob.data.bones[u].head_local)).length +     ((ob.matrix_world @ ob.data.bones[h].head_local) - (ob.matrix_world @ ob.data.bones[l].head_local)).length
AR = {s_: reach(tgt, *ARM[s_]) / reach(src, f'upperarm_{s_}', f'lowerarm_{s_}', f'hand_{s_}') for s_ in 'lr'}   # arm-reach ratio
print('RATIOS hip width', round(HR, 3), 'arm reach', {k: round(v, 3) for k, v in AR.items()}, flush=True)
ank_t = {s_: TW @ tb[MAP['foot_' + s_]].head_local for s_ in 'lr'}


def fk(act, f):
    """desired armature-space matrix of every target bone for source clip `act` at frame f"""
    use(src, act); sc.frame_set(int(f), subframe=f - int(f))
    sw = src.matrix_world; swr = sw.to_quaternion(); D = {}
    for t in order:
        b = tb[t]; s = T2S.get(t)
        head = (D[b.parent.name] @ rel[t]).to_translation() if b.parent else rest_arm[t].to_translation()
        if s is not None:
            delta = swr @ src.pose.bones[s].matrix.to_quaternion() @ src_rest_world[s].inverted()
            rot = TWri @ delta @ TWr @ matched[t]
            if s == 'pelvis':
                d = (sw @ src.pose.bones['pelvis'].head - sw @ sb['pelvis'].head_local) * K
                head = rest_arm[t].to_translation() + TW3i @ d
        else:
            rot = (D[b.parent.name] @ rel[t]).to_quaternion() if b.parent else rest_arm[t].to_quaternion()
        D[t] = M.LocRotScale(head, rot, V((1, 1, 1)))
    p_s = sw @ src.pose.bones['pelvis'].head; p_t = TW @ D[MAP['pelvis']].to_translation(); feet = {}
    for s_ in 'lr':
        a = sw @ src.pose.bones['foot_' + s_].head; r_ = a - p_s
        xy = p_t + left * (r_.dot(left) * HR) + fwd * (r_.dot(fwd) * K)
        feet[s_] = V((xy.x, xy.y, ank_t[s_].z + (a.z - ank_s[s_].z) * K))
    return D, feet


def two_bone(D, up, lo, end, T, bend):
    """turn `up` and `lo` (armature space) so the head of `end` lands on T; the knee/elbow stays in its current bend plane"""
    A = D[up].to_translation(); B = D[lo].to_translation(); C = D[end].to_translation()
    l1 = (B - A).length; l2 = (C - B).length; AT = T - A; d = AT.length
    if d < 1e-6:
        return
    u = AT / d; d = min(max(d, abs(l1 - l2) + 1e-4), l1 + l2 - 1e-4)
    v = (B - A) - u * (B - A).dot(u)
    if v.length < 1e-3 * l1:
        v = bend - u * bend.dot(u)
    v.normalize()
    ca = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d); sa = math.sqrt(max(0.0, 1 - ca * ca))
    B2 = A + u * (l1 * ca) + v * (l1 * sa); T2 = A + u * d
    R1 = (B - A).rotation_difference(B2 - A)
    R2 = (R1 @ (C - B)).rotation_difference(T2 - B2)
    D[up] = M.LocRotScale(A, R1 @ D[up].to_quaternion(), V((1, 1, 1)))
    D[lo] = M.LocRotScale(B2, R2 @ R1 @ D[lo].to_quaternion(), V((1, 1, 1)))


def relink(D):
    """after IK, recompute every child's head from its (new) parent; rotations stay as they are.
    The pelvis keeps its own (moved) head even when it has a parent (MPFB: Root)."""
    for t in order:
        b = tb[t]
        if b.parent and t != MAP['pelvis']:
            D[t] = M.LocRotScale((D[b.parent.name] @ rel[t]).to_translation(), D[t].to_quaternion(), V((1, 1, 1)))


HAND_IK = {'Sit_Eat_Loop', 'Sit_Type_Loop', 'Cook_Stir_Loop', 'Shower_Loop', 'Phone_Talk_Loop', 'Eat_Standing'}


def hand_targets(D):
    """wrist targets (world) from the source's own wrists in the current frame: near the head (mouth, ear, scrubbing) they
    are measured from the head and scaled by K; away from it (plate, keyboard, pot) from the same-side shoulder, scaled by
    arm reach; in between they blend"""
    sw = src.matrix_world; h_s = sw @ src.pose.bones['Head'].head; h_t = TW @ D[HEAD_T].to_translation(); out = {}
    for s_ in 'lr':
        w_s = sw @ src.pose.bones['hand_' + s_].head; sh_s = sw @ src.pose.bones['upperarm_' + s_].head
        sh_t = TW @ D[ARM[s_][0]].to_translation()
        by_head = h_t + (w_s - h_s) * K; by_sh = sh_t + (w_s - sh_s) * AR[s_]
        x = min(max((0.45 - (w_s - h_s).length) / 0.25, 0.0), 1.0); x = x * x * (3 - 2 * x)
        out[s_] = by_sh.lerp(by_head, x)
    return out


# hand poses the source does not give: palm down on a keyboard / table, fingers curled round a phone
HAND_POSE = {'Sit_Type_Loop': {'l': 'type', 'r': 'type'}, 'Sit_Eat_Loop': {'l': 'type'}, 'Phone_Talk_Loop': {'r': 'phone'}}
CURL = {'type': (25, 25, 15), 'phone': (65, 55, 40), 'hold': (45, 40, 30)}
TO_MOUTH = {'Eat_Standing'}      # the source hand stops in front of the chest: lift the eating hand to the mouth      # degrees per finger joint (index to pinky; thumb untouched)
SUB = {t: [c for c in order if c == t or tb[t] in tb[c].parent_recursive] for t in order}
left_a = (TW3i @ left).normalized(); up_a = (TW3i @ V((0, 0, 1))).normalized()


def rot_sub(D, root, R):
    """turn bone `root` and everything below it about the root's head (armature space)"""
    p = D[root].to_translation(); Mr = M.Translation(p) @ R.to_matrix().to_4x4() @ M.Translation(-p)
    for t in SUB[root]:
        D[t] = Mr @ D[t]


def hand_frame(D, s_):
    h = D[ARM[s_][2]].to_translation()
    d = (D[MAP[f'middle_01_{s_}']].to_translation() - h).normalized()
    sd = D[MAP[f'index_01_{s_}']].to_translation() - D[MAP[f'pinky_01_{s_}']].to_translation()
    return d, (sd - d * sd.dot(d)).normalized()


def pose_hand(D, s_, kind):
    if kind == 'type':   # fingers forward, tipped 20 degrees down; palm down (index side toward the body's centre)
        a = math.radians(20); d_des = (fwd_a * math.cos(a) - up_a * math.sin(a)).normalized()
        sd_des = left_a if s_ == 'r' else -left_a; sd_des = (sd_des - d_des * sd_des.dot(d_des)).normalized()
        d, sd = hand_frame(D, s_)
        C = M((d, sd, d.cross(sd))).transposed(); Dm = M((d_des, sd_des, d_des.cross(sd_des))).transposed()
        rot_sub(D, ARM[s_][2], (Dm @ C.transposed()).to_quaternion())
    d, sd = hand_frame(D, s_); n = d.cross(sd) * (-1 if s_ == 'r' else 1)       # palm normal
    for fi in ('index', 'middle', 'ring', 'pinky'):
        joints = [MAP[k] for k in (f'{fi}_01_{s_}', f'{fi}_02_{s_}', f'{fi}_03_{s_}') if k in MAP]
        seg = d
        for j, b in enumerate(joints):       # a finger tip bone has no next joint: reuse the previous segment's direction
            nxt = joints[j + 1] if j + 1 < len(joints) else None
            if nxt:
                seg = D[nxt].to_translation() - D[b].to_translation()
            ax = seg.cross(n)
            if ax.length > 1e-6:
                rot_sub(D, b, Q(ax.normalized(), math.radians(CURL[kind][min(j, 2)])))


def lowest_skin():
    dg = bpy.context.evaluated_depsgraph_get(); low = 9.0
    for o in skin:
        e = o.evaluated_get(dg); me = e.to_mesh(); Mw = np.array(e.matrix_world)
        A = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', A); A = A.reshape(-1, 3)
        low = min(low, float((A @ Mw[2, :3] + Mw[2, 3]).min())); e.to_mesh_clear()
    return low


results = []
pel = MAP['pelvis']
ONLY = [c for c in os.environ.get('RT_ONLY', '').split(',') if c]     # optional: retarget only these clips (testing)
BODY_OFFSET = 0.0      # this body's sole correction, measured on Idle_Loop (done first) and reused by the seated clips
for act in sorted(src_actions, key=lambda a: (a.name != 'Idle_Loop', a.name)):
    if ONLY and act.name not in ONLY:
        continue
    f0, f1 = act.frame_range; n = int(round(f1 - f0))
    new = bpy.data.actions.new(act.name + '__rt'); new.use_fake_user = True; use(tgt, new)
    hand_err = 0.0; is_hands = act.name in HAND_IK
    eat = None
    if act.name in TO_MOUTH:      # the eating hand is the one whose wrist rises most; its height drives the blend to the mouth
        hz = {s_: [] for s_ in 'lr'}
        for f in range(n + 1):
            use(src, act); sc.frame_set(int(f0 + f))
            for s_ in 'lr':
                hz[s_].append((src.matrix_world @ src.pose.bones['hand_' + s_].head).z)
        s_e = max('lr', key=lambda k: max(hz[k]) - min(hz[k]))
        eat = (s_e, hz[s_e], min(hz[s_e]), max(hz[s_e])); HAND_POSE[act.name] = {s_e: 'hold'}
        print('EAT hand', s_e, 'source wrist rises', round(eat[3] - eat[2], 3), 'm', flush=True)
    for f in range(n + 1):
        D, feet = fk(act, f0 + f)
        for s_ in 'lr':
            two_bone(D, *LEG[s_], TWi @ feet[s_], fwd_a)
        relink(D)
        if is_hands:
            ht = hand_targets(D)
            if eat:
                s_e, hzs, lo, hi = eat
                x = min(max(((hzs[f] - lo) / max(hi - lo, 1e-6) - 0.35) / 0.55, 0.0), 1.0); w = x * x * (3 - 2 * x)
                head = TW @ D[HEAD_T].to_translation()
                mouth = head + fwd * (0.12 * K) + V((0, 0, -0.065 * K)) + left * (0.02 if s_e == "l" else -0.02)   # wrist under the chin: fingers at the mouth
                ht[s_e] = ht[s_e].lerp(mouth, w)
            for s_ in 'lr':
                if os.environ.get('RT_DEBUG') and f == 0:
                    A_ = TW @ D[ARM[s_][0]].to_translation(); B_ = TW @ D[ARM[s_][1]].to_translation(); C_ = TW @ D[ARM[s_][2]].to_translation()
                    print('DBG', act.name, s_, 'shoulder', [round(x, 2) for x in A_], 'wrist', [round(x, 2) for x in C_], 'target', [round(x, 2) for x in ht[s_]],
                          'dist', round((ht[s_] - A_).length, 3), 'reach', round((B_ - A_).length + (C_ - B_).length, 3), flush=True)
                two_bone(D, *ARM[s_], TWi @ ht[s_], -fwd_a)
            relink(D)
            hand_err = max(hand_err, max(((TW @ D[ARM[s_][2]].to_translation()) - ht[s_]).length for s_ in 'lr'))
        for s_, kind in HAND_POSE.get(act.name, {}).items():
            pose_hand(D, s_, kind)
        for t in order:
            b = tb[t]; m = (D[b.parent.name] @ rel[t]).inverted() @ D[t] if b.parent else rest_arm[t].inverted() @ D[t]
            pb = tgt.pose.bones[t]; pb.rotation_mode = 'QUATERNION'
            loc, rot, _ = m.decompose()
            pb.rotation_quaternion = rot; pb.scale = V((1, 1, 1)); pb.keyframe_insert('rotation_quaternion', frame=f)
            pb.location = loc if t == pel else V((0, 0, 0))
            if t == pel:
                pb.keyframe_insert('location', frame=f)
    # ground contact from the deformed skin
    lows = []
    for f in range(n + 1):
        sc.frame_set(f); lows.append(lowest_skin())
    lows = np.array(lows)
    if act.name in SEATED:
        mode = 'seated (Idle offset)'; shift = np.full(n + 1, BODY_OFFSET)
    elif act.name in PER_FRAME:
        mode = 'per-frame, smoothed'
        k = np.arange(-9, 10); w = np.exp(-0.5 * (k / SMOOTH_SIGMA) ** 2); w /= w.sum()
        gauss = lambda x: np.convolve(np.pad(x, 9, mode='edge'), w, mode='valid')
        shift = gauss(-lows)
        for _ in range(8):     # push smoothly out of the floor wherever the smoothing left the body below it
            shift = shift + gauss(np.maximum(-lows - shift, 0.0)) * 1.5
    else:
        mode = 'fixed'; shift = np.full(n + 1, -lows.min())
        if act.name == 'Idle_Loop':
            BODY_OFFSET = float(-lows.min())
    pb = tgt.pose.bones[pel]
    for f in range(n + 1):
        sc.frame_set(f)
        if abs(shift[f]) > 1e-5:
            pb.location = pb.location + (rest_arm[pel].to_3x3().inverted() @ (TW3i @ V((0, 0, float(shift[f])))))
            pb.keyframe_insert('location', frame=f)
    # checks after grounding
    lows2 = []; slide = 0.0; prev = None; seat = []
    for f in range(n + 1):
        sc.frame_set(f); lows2.append(lowest_skin())
        pts = {s_: tgt.matrix_world @ tgt.pose.bones[LEG[s_][2]].head for s_ in 'lr'}
        seat.append((tgt.matrix_world @ tgt.pose.bones[pel].head).z)
        if prev:   # slide of a planted foot: horizontal movement while the ankle is within 2 cm of its lowest height
            for s_ in 'lr':
                if pts[s_].z < ank_t[s_].z + float(shift[f]) + 0.02:
                    dxy = (pts[s_] - prev[s_]); dxy.z = 0; slide = max(slide, dxy.length)
        prev = pts
    r = dict(name=act.name, frames=n + 1, seconds=round(n / FPS, 2), ground=mode,
             offset_m=round(float(shift.mean()), 3) if mode != 'per-frame, smoothed' else [round(float(shift.min()), 3), round(float(shift.max()), 3)],
             lowest_skin_after=[round(min(lows2), 3), round(max(lows2), 3)], pelvis_height=[round(min(seat), 3), round(max(seat), 3)],
             planted_foot_slide_per_frame=round(slide, 3))
    if is_hands:
        r['hand_target_error_m'] = round(hand_err, 3)
    results.append(r); print('CLIP', json.dumps(r), flush=True)

# ---- export (skeleton only)
for o in skin:
    bpy.data.objects.remove(o, do_unlink=True)
bpy.data.objects.remove(src, do_unlink=True)
for a in src_actions:
    bpy.data.actions.remove(a)
for r in results:
    bpy.data.actions[r['name'] + '__rt'].name = r['name']
bpy.ops.object.select_all(action='DESELECT'); tgt.select_set(True); bpy.context.view_layer.objects.active = tgt
for r in results:
    use(tgt, bpy.data.actions[r['name']])
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, r['name'] + '.glb'), export_format='GLB', use_selection=True,
                              export_animation_mode='ACTIVE_ACTIONS', export_force_sampling=True, export_optimize_animation_size=True)
use(tgt, None)
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, 'animations_all.glb'), export_format='GLB', use_selection=True,
                          export_animation_mode='ACTIONS', export_force_sampling=True, export_optimize_animation_size=True)
json.dump(dict(target=os.path.basename(TGT), rig=RIG, hip_scale_K=round(K, 3), facing_turn_deg=round(math.degrees(ang), 1),
               bone_map=MAP, clips=results), open(os.path.join(OUT, 'check.json'), 'w'), indent=1)
print('DONE', len(results), flush=True)
