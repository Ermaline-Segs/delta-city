# blender -b --factory-startup -P home_build.py -- <homes_dir(scripts)> <repo_assets> <out_dir> <type> [interior|exterior|both]
import bpy, sys, os, json, math
a = sys.argv[sys.argv.index('--') + 1:]
HD, A, OUT, TYPE = a[:4]; WHAT = a[4] if len(a) > 4 else 'both'
sys.path.insert(0, HD)
import importlib, home_lib as L, home_plans as P
os.makedirs(OUT, exist_ok=True)
S = os.path.dirname(HD.rstrip('/\\'))
L.configure([os.path.join(S, 'htex'), os.path.join(A, 'textures'), os.path.join(A, 'textures', 'buildings')])
GEN = os.path.join(A, 'home', 'cooling-power', 'generator_large_green.glb')

# per type: interior plan, exterior plan(s) and compound layout (compound W x D, building offset, car bays, extras)
CFG = {
    'room': dict(interior=lambda: P.ROOM_INTERIOR, building=P.room_row, W=31.0, D=24.0, off=(-12.6, 0.0),
                 paved=[(-15.5, -12.0, 15.5, 0.0)], bays=(4, -5.0, -9.5), gen=(13.5, -9.5), tank=(-13.5, -9.0), wall=(0.93, 0.88, 0.76), roof=(0.52, 0.27, 0.18)),
    'flat': dict(interior=P.flat_interior, building=P.flat_block, W=38.0, D=32.0, off=(-15.3, 1.6),
                 paved=[(-19.0, -16.0, 19.0, 0.2)], bays=(6, -7.5, -12.5), gen=(16.5, -13.5), tank=(-16.6, -13.0), wall=(0.96, 0.95, 0.92), roof=(0.3, 0.3, 0.32)),
    'bungalow': dict(interior=P.bungalow, building=P.bungalow, W=24.0, D=30.0, off=(-6.9, 0.0),
                     paved=[(-4.5, -15.0, 4.5, -0.2), (-9.0, -10.5, 9.0, -4.5)], bays=(3, -3.75, -10.0), gen=(9.5, 11.5), tank=(-9.5, 12.5),
                     wall=(0.86, 0.68, 0.38), roof=(0.52, 0.27, 0.18)),
    'duplex': dict(interior=P.duplex, building=P.duplex, W=22.0, D=34.0, off=(-6.0, 0.0),
                   paved=[(-4.0, -17.0, 4.0, -2.2), (-8.5, -11.0, 8.5, -5.0)], bays=(3, -3.75, -10.5), gen=(8.5, 14.5), tank=(-8.5, 14.5),
                   wall=(0.93, 0.88, 0.76), roof=(0.3, 0.3, 0.32)),
    'mansion': dict(interior=P.mansion, building=P.mansion, W=44.0, D=48.0, off=(-9.0, -4.0),
                    paved=[(-4.0, -24.0, 4.0, -6.6), (-9.0, -9.6, 9.0, -6.6), (-8.0, -19.0, 8.0, -12.0)], bays=(4, -5.0, -18.5),
                    gen=(-19.5, 18.5), tank=(-19.0, 21.5), wall=(0.96, 0.95, 0.92), roof=(0.52, 0.27, 0.18),
                    pool=(-4.0, 13.0, 4.0, 17.0), bq=(12.0, 16.0), gatehouse=(6.0, -23.2)),
}
C = CFG[TYPE]


def gl(p):          # Blender (x, y, z) -> glTF (x, y up, z = -y)
    return [round(p[0], 3), round(p[2], 3), round(-p[1], 3)]


def rect_gl(r):
    x0, y0, x1, y1 = r
    return dict(x=[round(x0, 3), round(x1, 3)], z=[round(-y1, 3), round(-y0, 3)])


def to_gl_info(info, z0=0.0):
    rooms = [dict(name=r['name'], kind=r['kind'], floor=r['floor'], floor_y=round(z0 + r['floor'] * L.STOREY, 2), size_m=r['size'], **rect_gl(r['rect'])) for r in info['rooms']]
    doors = [dict(node=d['node'], security_node=d['security_node'], between=d['between'], floor=d['floor'], centre=gl(d['centre']), width=d['width'],
                  in_wall_along=d['wall'], main=d['main']) for d in info['doors']]
    return rooms, doors


def import_glb(path, loc, rot=0.0):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    top = [o for o in new if o.parent is None]
    for o in top:
        o.location = loc; o.rotation_euler[2] += rot
    return new


summary = {}
if WHAT in ('interior', 'both'):
    bpy.ops.wm.read_factory_settings(use_empty=True); L.MATS.clear()
    plan = C['interior']()
    miss = L.reach_check(plan)
    if miss:
        print('UNREACHABLE', miss, flush=True)
    mats = L.std_materials(C['wall'], C['roof'])
    x0, y0, x1, y1 = L.plan_bbox(plan)
    off = (-(x0 + x1) / 2, -(y0 + y1) / 2)
    M = L.Mesh()
    info = L.build_building(M, plan, mats, 'interior', 0.0, off)
    root, objs = M.build(f'{TYPE}_interior')
    fn = os.path.join(OUT, f'{TYPE}_interior.glb'); L.export(objs, fn)
    rooms, doors = to_gl_info(info)
    summary['interior'] = dict(file=os.path.basename(fn), tris=L.tris(objs), bytes=os.path.getsize(fn), size_m=[round(x1 - x0, 2), round(y1 - y0, 2)],
                               storeys=1 + max(f['z'] for f in plan['floors']), rooms=rooms, doors=doors, unreachable=miss)
    print('INTERIOR', TYPE, 'tris', summary['interior']['tris'], 'bytes', summary['interior']['bytes'], 'doors', len(doors), flush=True)

if WHAT in ('exterior', 'both'):
    bpy.ops.wm.read_factory_settings(use_empty=True); L.MATS.clear()
    mats = L.std_materials(C['wall'], C['roof'])
    M = L.Mesh(); extra = {}
    plan = C['building']()
    binfo, rh = L.exterior_building(M, plan, mats, C['off'])
    holes = [C['pool']] if 'pool' in C else []
    L.ground(M, mats, C['W'], C['D'], C['paved'], holes)
    extra['compound'] = L.compound(M, mats, C['W'], C['D'])
    n, bx0, by = C['bays']; extra['car_bays'] = [gl((x, y, 0)) for x, y in L.car_bays(M, n, bx0, by)]
    gx, gy = C['gen']; pad = L.generator_spot(M, mats, gx, gy)
    tx, ty = C['tank']; extra['water_tank'] = gl(L.tank_stand(M, mats, tx, ty))
    if 'pool' in C:
        extra['pool'] = L.pool(M, mats, *C['pool']); extra['pool']['rect'] = rect_gl(C['pool'])
        L.ground(M, mats, 0.0, 0.0, [(C['pool'][0] - 2.0, C['pool'][1] - 2.0, C['pool'][2] + 2.0, C['pool'][1] - 0.3)])   # pool deck strip (paving)
    others = {}
    if 'bq' in C:
        bq = P.boys_quarters(); bi, _ = L.exterior_building(M, bq, mats, C['bq'], plinth=0.15); others['boys_quarters'] = bi
    if 'gatehouse' in C:
        gh = P.gatehouse(); gi, _ = L.exterior_building(M, gh, mats, C['gatehouse'], plinth=0.15); others['gatehouse'] = gi
    root, objs = M.build(f'{TYPE}_exterior')
    gen = import_glb(GEN, (pad[0], pad[1], pad[2]))
    for o in gen:
        if o.parent is None:
            o.parent = root
    objs += gen
    fn = os.path.join(OUT, f'{TYPE}_exterior.glb'); L.export(objs, fn)
    rooms, doors = to_gl_info(binfo, 0.3)
    extra['generator'] = gl(pad)
    summary['exterior'] = dict(file=os.path.basename(fn), tris=L.tris(objs), bytes=os.path.getsize(fn), compound_m=[C['W'], C['D']],
                               building_offset=gl((C['off'][0], C['off'][1], 0)), floor_level_above_ground=0.3, roof_rise=round(rh, 2),
                               doors=doors, **extra,
                               others={k: to_gl_info(v, 0.15)[1] for k, v in others.items()})
    print('EXTERIOR', TYPE, 'tris', summary['exterior']['tris'], 'bytes', summary['exterior']['bytes'], 'doors', len(doors), flush=True)

old = {}
jp = os.path.join(OUT, f'{TYPE}.json')
if os.path.exists(jp):
    old = json.load(open(jp))
old.update(summary)
json.dump(old, open(jp, 'w'), indent=1)
