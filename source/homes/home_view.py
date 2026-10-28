# blender -b --factory-startup -P home_view.py -- <file.glb> <out.png> <exterior|interior> [furnish.json]
# exterior: front 3/4 view and rear 3/4 view.  interior: top-down plan (ceilings and upper floors hidden per storey) + a 3/4 cut view.
import bpy, sys, os, math, json, mathutils
import numpy as np
V = mathutils.Vector
a = sys.argv[sys.argv.index('--') + 1:]; F, OUT, MODE = a[:3]; FURN = a[3] if len(a) > 3 else None
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=F)
sc = bpy.context.scene
for o in list(bpy.data.objects):
    if o.name.startswith('ceiling') or 'ceiling' in o.name:
        bpy.data.objects.remove(o, do_unlink=True)
if FURN:     # place furniture: [[glb, x, y(blender), rot_deg], ...]
    for g, x, y, z, r in json.load(open(FURN)):
        b4 = set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=g)
        for o in [o for o in bpy.data.objects if o not in b4 and o.parent is None]:
            o.location = (x, y, z); o.rotation_euler[2] += math.radians(r)
bpy.context.view_layer.update()
P = np.vstack([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in sc.objects if o.type == 'MESH' and len(o.data.vertices)])
lo, hi = P.min(0), P.max(0); c = (lo + hi) / 2
cam = bpy.data.objects.new('c', bpy.data.cameras.new('c')); sc.collection.objects.link(cam); sc.camera = cam; cam.data.type = 'ORTHO'
for rot, e in (((50, 0, -30), 3.5), ((65, 0, 140), 1.3)):
    l = bpy.data.objects.new('s', bpy.data.lights.new('s', 'SUN')); l.data.energy = e; l.rotation_euler = [math.radians(x) for x in rot]; sc.collection.objects.link(l)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.78, 0.84, 0.92, 1)
w.node_tree.nodes['Background'].inputs[1].default_value = 0.8
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 16; sc.cycles.use_denoising = False
sc.view_settings.view_transform = 'Standard'; sc.render.resolution_x = 1000; sc.render.resolution_y = 700
tiles = []


def shot(d, scale, target=None, clip=None):
    d = V(d).normalized(); t = V(target if target is not None else c)
    cam.location = t + d * 120; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = scale
    cam.data.clip_start = clip if clip else 0.1; cam.data.clip_end = 400
    p = OUT + f'_{len(tiles)}.png'; sc.render.filepath = p; bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(700, 1000, 4)); bpy.data.images.remove(im); os.remove(p)


ext = max(hi[0] - lo[0], hi[1] - lo[1])
if MODE == 'exterior':
    shot((-0.75, -1.0, 0.75), ext * 1.05)
    shot((0.8, 1.0, 0.8), ext * 1.05)
else:
    import bmesh
    storeys = 2 if hi[2] > 4.5 else 1
    meshes = [o for o in sc.objects if o.type == 'MESH']
    keep = {o.name: o.data.copy() for o in meshes}
    for s in range(storeys):
        for o in meshes:        # cut away everything above this storey (light reaches the rooms), and below it for the upper storey
            me = keep[o.name].copy(); bm = bmesh.new(); bm.from_mesh(me); M_ = o.matrix_world
            zt = s * 3.3 + 2.4; zb = s * 3.3 - 0.3
            bmesh.ops.delete(bm, geom=[f for f in bm.faces if min((M_ @ v.co).z for v in f.verts) > zt or (s and max((M_ @ v.co).z for v in f.verts) < zb)], context='FACES')
            bm.to_mesh(me); bm.free(); o.data = me
        # hide everything above this storey's 2.0 m: cut by the camera's near plane looking straight down
        d = V((0, -0.0001, 1)); cam.location = V((c[0], c[1], 0)) + d.normalized() * (120); top_dist = 0.1
        cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = ext * 1.08
        cam.data.clip_start = top_dist; cam.data.clip_end = 400
        p = OUT + f'_{len(tiles)}.png'; sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(700, 1000, 4)); bpy.data.images.remove(im); os.remove(p)
    for o in meshes:           # 3/4 view: ground storey only
        me = keep[o.name].copy(); bm = bmesh.new(); bm.from_mesh(me); M_ = o.matrix_world
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if min((M_ @ v.co).z for v in f.verts) > 2.4], context='FACES'); bm.to_mesh(me); bm.free(); o.data = me
    # 3/4 cut view of the ground floor from the front-left
    d = V((-0.6, -1.0, 1.1)).normalized(); t = V((c[0], c[1], 1.0))
    cam.location = t + d * 120; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler(); cam.data.ortho_scale = ext * 1.15
    # near plane slices the walls about 2.2 m up at the target
    cam.data.clip_start = 0.1; cam.data.clip_end = 400
    p = OUT + f'_{len(tiles)}.png'; sc.render.filepath = p; bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p); tiles.append(np.array(im.pixels[:]).reshape(700, 1000, 4)); bpy.data.images.remove(im); os.remove(p)
cols = 2
rows = [np.concatenate(tiles[i:i + cols] + [np.ones_like(tiles[0])] * (cols - len(tiles[i:i + cols])), 1) for i in range(0, len(tiles), cols)]
s = np.concatenate(rows[::-1], 0)
img = bpy.data.images.new('o', s.shape[1], s.shape[0]); img.pixels[:] = s.ravel(); img.filepath_raw = OUT; img.file_format = 'PNG'; img.save()
print('VIEW', OUT, flush=True)
