# blender -b --factory-startup -P anim_strip2.py -- <character.glb> <animations_all.glb> <out_dir> [frames=5]
# Plays each clip of animations_all.glb on the character's own skinned mesh and renders a strip of frames.
# Also measures the lowest skinned vertex of the whole body per frame (catches feet sinking into the floor).
import bpy, sys, os, math, mathutils, json
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; CH, AN, OUT = a[:3]; NF = int(a[3]) if len(a) > 3 else 5
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CH)
arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.visible_get() and any(m.type == 'ARMATURE' for m in o.modifiers)]
before = set(bpy.data.objects); acts0 = set(bpy.data.actions)
bpy.ops.import_scene.gltf(filepath=AN)
for o in set(bpy.data.objects) - before:
    bpy.data.objects.remove(o, do_unlink=True)
acts = sorted([x for x in bpy.data.actions if x not in acts0], key=lambda x: x.name)
sc = bpy.context.scene; FPS = sc.render.fps
if arm.animation_data is None:
    arm.animation_data_create()
gr = bpy.data.objects.new('g', bpy.data.meshes.new('g')); gr.data.from_pydata([(-50, -50, 0), (50, -50, 0), (50, 50, 0), (-50, 50, 0)], [], [(0, 1, 2, 3)]); sc.collection.objects.link(gr)
gm = bpy.data.materials.new('gm'); gm.use_nodes = True; gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.5, 0.52, 0.55, 1); gr.data.materials.append(gm)
for rot, e in (((40, 0, -40), 2.4), ((60, 0, 140), 0.8)):
    l = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); l.data.energy = e; l.rotation_euler = [math.radians(x) for x in rot]; sc.collection.objects.link(l)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.8, 0.83, 0.88, 1)
cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 8; sc.cycles.use_denoising = False
sc.view_settings.view_transform = 'Standard'; sc.render.resolution_x = 220; sc.render.resolution_y = 300
# camera from the character's front-left (front from the toes)
info = {}
for act in acts:
    arm.animation_data.action = act
    if hasattr(arm.animation_data, 'action_slot') and act.slots:
        arm.animation_data.action_slot = act.slots[0]
    f0, f1 = act.frame_range
    frames = [f0 + (f1 - f0) * i / max(1, NF - 1) for i in range(NF)]
    pts = []; lows = []
    for f in [f0 + (f1 - f0) * i / 20 for i in range(21)]:
        sc.frame_set(int(round(f))); dg = bpy.context.evaluated_depsgraph_get(); low = 9
        for o in meshes:
            e = o.evaluated_get(dg); m = e.to_mesh(); M = np.array(e.matrix_world)
            A = np.empty(len(m.vertices) * 3); m.vertices.foreach_get('co', A); A = A.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
            pts.append(A[::25]); low = min(low, float(A[:, 2].min())); e.to_mesh_clear()
        lows.append(low)
    P = np.vstack(pts); lo, hi = P.min(0), P.max(0); c = (lo + hi) / 2
    info[act.name] = dict(lowest_point_min=round(min(lows), 3), lowest_point_max=round(max(lows), 3))
    size = max(hi[2] - min(lo[2], 0), (hi[:2] - lo[:2]).max()) * 1.1 + 0.2
    toe = arm.matrix_world @ arm.data.bones[0].head
    d = mathutils.Vector((-0.75, -1, 0.35)).normalized()   # both rigs face -Y in Blender (glTF +Z)
    cam.location = mathutils.Vector((c[0], c[1], (hi[2] + min(lo[2], 0)) / 2)) + d * 20
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = size
    tiles = []
    for i, f in enumerate(frames):
        sc.frame_set(int(round(f))); p = os.path.join(OUT, f'_t{i}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(300, 220, 4)); bpy.data.images.remove(im); os.remove(p)
    strip = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new(act.name, strip.shape[1], strip.shape[0]); img.pixels[:] = strip.ravel()
    img.filepath_raw = os.path.join(OUT, act.name + '.png'); img.file_format = 'PNG'; img.save(); bpy.data.images.remove(img)
    print('STRIP', act.name, info[act.name], flush=True)
json.dump(info, open(os.path.join(OUT, 'lowest_points.json'), 'w'), indent=1)
