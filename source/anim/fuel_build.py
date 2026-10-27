# blender -b --factory-startup -P fuel_build.py -- <assets/animations/animations_all.glb> <out_dir>
# Builds the filling-station attendant clips on the Quaternius mannequin (same rig as the other 20 clips), from the
# Idle_Loop body plus right-arm IK, and writes <out>/<clip>.glb, <out>/animations_all.glb (mannequin + all clips).
# Frame: Blender, the character faces -Y, its right is -X, feet at z=0.
#   Fuel_Take       2.0 s  reach the pump's holster (wrist at HOLSTER), grip, lift the nozzle out, bring it to CARRY
#   Fuel_Hold_Loop  2.5 s  right hand holds the nozzle in the car's fuel cap (wrist at CAP), small trigger squeeze
#   Fuel_Hang       2.0 s  Fuel_Take played backwards: from CARRY back into the holster, release, back to idle
import bpy, sys, os, math, mathutils
V, Q = mathutils.Vector, mathutils.Quaternion
SRC, OUT = sys.argv[sys.argv.index('--') + 1:][:2]
os.makedirs(OUT, exist_ok=True)
HOLSTER = V((-0.22, -0.46, 1.08)); CARRY = V((-0.26, -0.24, 0.96)); CAP = V((-0.20, -0.42, 1.00))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
sc = bpy.context.scene; FPS = sc.render.fps
for o in list(sc.objects):
    if o.type in ('CAMERA', 'LIGHT') or (o.type == 'MESH' and o.name.lower().startswith(('cube', 'icosphere'))):
        bpy.data.objects.remove(o, do_unlink=True)
arm = [o for o in sc.objects if o.type == 'ARMATURE'][0]
if arm.animation_data is None:
    arm.animation_data_create()
A = {a.name: a for a in bpy.data.actions}; PB = arm.pose.bones
idle = A['Idle_Loop']


def use(act):
    arm.animation_data.action = act
    if hasattr(arm.animation_data, 'action_slot') and act.slots:
        arm.animation_data.action_slot = act.slots[0]


def sample(act, t):
    use(act); f0, f1 = act.frame_range; L = f1 - f0; t = f0 + (t % L if L > 0 else 0)
    sc.frame_set(int(t), subframe=t - int(t))
    return {b.name: (b.location.copy(), b.rotation_quaternion.copy(), b.scale.copy()) for b in PB}


def add_rot(pose, bone, axis, deg):
    l, r, s = pose[bone]; pose[bone] = (l, r @ Q({'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}[axis], math.radians(deg)), s)


def bake(name, n, pose_at):
    poses = [pose_at(f) for f in range(n + 1)]
    act = bpy.data.actions.new(name); use(act)
    for f, pose in enumerate(poses):
        for b in PB:
            b.location, b.rotation_quaternion, b.scale = pose[b.name]
            b.keyframe_insert('location', frame=f); b.keyframe_insert('rotation_quaternion', frame=f); b.keyframe_insert('scale', frame=f)
    return act


def idle_wrist(f):
    sample(idle, f); return arm.matrix_world @ PB['hand_r'].head


smooth = lambda x: x * x * (3 - 2 * x)
def lerp(a, b, x):
    return V(a).lerp(V(b), smooth(min(max(x, 0.0), 1.0)))


def ik_clip(name, n, wrist_at, tweak):
    """Idle_Loop body (+ tweak(pose, f)), right wrist driven to wrist_at(f) by a two-bone IK with the elbow out and down"""
    def base(f):
        p = sample(idle, f); tweak(p, f); return p
    tmp = bake(name + '_base', n, base); use(tmp)
    e = bpy.data.objects.new('ik_r', None); sc.collection.objects.link(e)
    pole = bpy.data.objects.new('pole_r', None); sc.collection.objects.link(pole)
    pole.location = arm.matrix_world @ PB['upperarm_r'].head + V((-0.45, 0.45, -0.55))
    c = PB['lowerarm_r'].constraints.new('IK'); c.target = e; c.pole_target = pole; c.pole_angle = math.radians(-90)
    c.chain_count = 2; c.use_tail = True
    for f in range(n + 1):
        e.location = wrist_at(f); e.keyframe_insert('location', frame=f)
    bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True); bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE'); bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.nla.bake(frame_start=0, frame_end=n, only_selected=False, visual_keying=True, clear_constraints=True, use_current_action=False, bake_types={'POSE'})
    bpy.ops.object.mode_set(mode='OBJECT')
    act = arm.animation_data.action; act.name = name
    for o in (e, pole):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.data.actions.remove(tmp)
    return act


# ---- Fuel_Take: 0-6 idle, 6-20 reach, 20-26 grip, 26-34 lift out, 34-44 bring to CARRY, 44-48 hold
N = 2 * FPS
IW = [idle_wrist(f) for f in range(N + 1)]
LIFT = HOLSTER + V((0, 0.05, 0.06))
def take_wrist(f):
    if f < 6: return IW[f]
    if f < 20: return lerp(IW[f], HOLSTER, (f - 6) / 14)
    if f < 26: return HOLSTER
    if f < 34: return lerp(HOLSTER, LIFT, (f - 26) / 8)
    if f < 44: return lerp(LIFT, CARRY, (f - 34) / 10)
    return CARRY
def take_tweak(p, f):
    w = smooth(min(max((f - 4) / 14, 0), 1)) * (1 - smooth(min(max((f - 30) / 12, 0), 1)))
    add_rot(p, 'spine_03', 'X', 9 * w); add_rot(p, 'Head', 'X', 12 * w + 6)
take = ik_clip('Fuel_Take', N, take_wrist, take_tweak)

# ---- Fuel_Hold_Loop: wrist at the fuel cap, a gentle squeeze of the trigger, looking down at the cap
NH = int(round(2.5 * FPS))
def hold_wrist(f):
    return CAP + V((0, 0, 0.004 * math.sin(2 * math.pi * f / NH * 3)))
def hold_tweak(p, f):
    add_rot(p, 'spine_03', 'X', 5); add_rot(p, 'Head', 'X', 16)
hold = ik_clip('Fuel_Hold_Loop', NH, hold_wrist, hold_tweak)

# ---- Fuel_Hang: Fuel_Take backwards
def take_pose(f):
    use(take); sc.frame_set(int(f)); return {b.name: (b.location.copy(), b.rotation_quaternion.copy(), b.scale.copy()) for b in PB}
hang = bake('Fuel_Hang', N, lambda f: take_pose(N - f))

CLIPS = [('Fuel_Take', take), ('Fuel_Hold_Loop', hold), ('Fuel_Hang', hang)]
meshes = [o for o in sc.objects if o.type == 'MESH']


def export(path, objs, mode):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=mode is not None,
                              export_animation_mode=mode or 'ACTIONS', export_force_sampling=True, export_frame_step=1,
                              export_optimize_animation_size=True, export_def_bones=True, export_image_format='JPEG')


for name, act in CLIPS:
    act.use_fake_user = True; use(act)
    export(os.path.join(OUT, name + '.glb'), [arm], 'ACTIVE_ACTIONS')
for a in bpy.data.actions:
    a.use_fake_user = True
arm.animation_data.action = None
export(os.path.join(OUT, 'animations_all.glb'), [arm] + meshes, 'ACTIONS')
print('BUILT', [c[0] for c in CLIPS], 'actions in file', len([a for a in bpy.data.actions]), flush=True)
