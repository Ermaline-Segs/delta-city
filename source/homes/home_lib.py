"""Delta City home builder (Blender 5.x). Buildings are generated from room plans.
Plan frame: metres, x across, y depth with the FRONT at small y; Blender X = x, Blender Y = y, Z up.
After glTF export the front faces +Z (glTF z = -Blender y)."""
import bpy, bmesh, math, os, json
import numpy as np
import mathutils
V = mathutils.Vector
STOREY = 3.3            # floor to floor
CEIL = 3.0              # ceiling height
T_EXT, T_INT = 0.23, 0.15
TEX = {}                # set by configure()
TEX_PX = 512


def configure(tex_dirs):
    for d in tex_dirs:
        for f in os.listdir(d):
            if f.lower().endswith(('.jpg', '.png')):
                TEX[f.rsplit('.', 1)[0].replace('_diff', '')] = os.path.join(d, f)


# ------------------------------------------------------------------ materials
MATS = {}


def material(name, tex=None, color=(1, 1, 1), scale=2.0, rough=0.8, metal=0.0, alpha=1.0, grey=False):
    """tex: key in TEX; colour multiplies the texture (exported as glTF baseColorFactor); scale: metres per texture repeat"""
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if tex:
        img = bpy.data.images.load(TEX[tex], check_existing=True)
        if img.size[0] > TEX_PX:
            img.scale(TEX_PX, TEX_PX)
        if grey:
            px = np.array(img.pixels[:]).reshape(-1, 4); l = px[:, :3] @ np.array([0.3, 0.59, 0.11])
            l = l / max(l.mean(), 1e-3) * 0.75; px[:, :3] = np.clip(l, 0, 1)[:, None]; img.pixels[:] = px.ravel()
        img.pack()
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = img
        if tuple(color) != (1, 1, 1):
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
            nt.links.new(t.outputs['Color'], mx.inputs['A']); mx.inputs['B'].default_value = (*color, 1)
            nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
        else:
            nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
    else:
        b.inputs['Base Color'].default_value = (*color, 1)
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
    m['uv_scale'] = scale
    MATS[name] = m
    return m


def std_materials(wall_color=(0.93, 0.88, 0.76), roof_color=(0.52, 0.27, 0.18)):
    P = 'painted_plaster_wall' if 'painted_plaster_wall' in TEX else 'white_plaster_02'
    return dict(
        wall_out=material('wall_paint_exterior', P, wall_color, 2.5),
        wall_in=material('wall_paint_interior', P, (0.96, 0.95, 0.92), 2.5),
        plinth=material('plinth_paint', 'concrete_floor', (0.55, 0.53, 0.5), 2.0),
        ceiling=material('ceiling_white', None, (0.93, 0.93, 0.91), 1, 0.9),
        roof=material('roof_stone_coated', 'clay_roof_tiles_02', roof_color, 2.0, 0.7, grey=True),
        soffit=material('soffit', None, (0.9, 0.9, 0.88), 1, 0.8),
        fascia=material('fascia', None, (0.85, 0.84, 0.8), 1, 0.6),
        f_living=material('floor_ceramic_living', 'large_floor_tiles_02', (1, 0.97, 0.92), 1.8, 0.35),
        f_room=material('floor_ceramic_room', 'tiled_floor_001', (1, 1, 1), 2.4, 0.4),
        f_bath=material('floor_anti_slip', 'anti_skid_tiles', (1, 1, 1), 1.5, 0.6),
        f_kitchen=material('floor_terracotta', 'terracotta_floor_tiles', (1, 1, 1), 1.6, 0.5),
        f_granite=material('floor_granite', 'granite_tile', (1, 1, 1), 2.0, 0.25),
        f_wood=material('floor_wood', 'wood_floor', (1, 1, 1), 2.4, 0.5),
        f_veranda=material('floor_terrazzo', 'terrazzo_tiles', (1, 1, 1), 1.6, 0.4),
        f_concrete=material('concrete', 'concrete_floor', (0.8, 0.8, 0.8), 3.0, 0.9),
        bath_wall=material('wall_tiles_bath', 'square_tiled_wall', (1, 1, 1), 1.2, 0.3),
        door_wood=material('door_wood', 'wooden_door' if 'wooden_door' in TEX else 'wood_floor', (0.8, 0.6, 0.45), 2.1, 0.6),
        frame=material('door_frame', None, (0.35, 0.22, 0.14), 1, 0.6),
        steel=material('steel_black', None, (0.06, 0.06, 0.065), 1, 0.45, 0.6),
        win_frame=material('window_frame_aluminium', None, (0.25, 0.2, 0.15), 1, 0.4, 0.5),
        glass_out=material('glass_dark', None, (0.08, 0.1, 0.12), 1, 0.08),
        glass_in=material('glass_clear', None, (0.6, 0.72, 0.8), 1, 0.05, alpha=0.3),
        rail=material('railing_steel', None, (0.12, 0.12, 0.13), 1, 0.4, 0.6),
        column=material('column_paint', P, (0.97, 0.96, 0.93), 2.5),
        step=material('step_terrazzo', 'terrazzo_tiles', (1, 1, 1), 1.6, 0.4))


# ------------------------------------------------------------------ geometry accumulation
class Mesh:
    """faces grouped by material; named nodes (doors, gates) kept apart with their own origin"""

    def __init__(self):
        self.groups = {}       # (node, mat) -> [polys]
        self.nodes = {}        # node -> dict(origin, rot_z)

    def poly(self, mat, pts, node=None):
        self.groups.setdefault((node, mat.name), []).append([tuple(p) for p in pts])

    def box(self, mat, x0, x1, y0, y1, z0, z1, node=None, faces='all'):
        if x1 - x0 < 1e-4 or y1 - y0 < 1e-4 or z1 - z0 < 1e-4:
            return
        c = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        F = {'-z': (0, 3, 2, 1), '+z': (4, 5, 6, 7), '-y': (0, 1, 5, 4), '+y': (2, 3, 7, 6), '-x': (3, 0, 4, 7), '+x': (1, 2, 6, 5)}
        for k, f in F.items():
            if faces == 'all' or k in faces:
                self.poly(mat, [c[i] for i in f], node)

    def cyl(self, mat, cx, cy, z0, z1, r, seg=12, node=None, caps=True):
        ring = [(cx + r * math.cos(2 * math.pi * i / seg), cy + r * math.sin(2 * math.pi * i / seg)) for i in range(seg)]
        for i in range(seg):
            a, b = ring[i], ring[(i + 1) % seg]
            self.poly(mat, [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)], node)
        if caps:
            self.poly(mat, [(p[0], p[1], z1) for p in ring], node)
            self.poly(mat, [(p[0], p[1], z0) for p in reversed(ring)], node)

    def node(self, name, origin, rot_z=0.0):
        self.nodes[name] = dict(origin=tuple(origin), rot_z=rot_z)

    def build(self, root_name):
        root = bpy.data.objects.new(root_name, None); bpy.context.scene.collection.objects.link(root)
        node_objs = {}
        for n, d in self.nodes.items():
            e = bpy.data.objects.new(n, None); bpy.context.scene.collection.objects.link(e); e.parent = root
            e.location = d['origin']; e.rotation_euler = (0, 0, d['rot_z']); node_objs[n] = e
        objs = [root] + list(node_objs.values())
        by_node = {}
        for (node, mname), polys in self.groups.items():
            by_node.setdefault(node, []).append((mname, polys))
        for node, lst in by_node.items():
            bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap'); mats = []
            org = V(self.nodes[node]['origin']) if node else V((0, 0, 0))
            for mname, polys in lst:
                mi = len(mats); mats.append(bpy.data.materials[mname]); sc = mats[-1].get('uv_scale', 2.0)
                for pts in polys:
                    vs = [bm.verts.new(V(p) - org) for p in pts]
                    try:
                        f = bm.faces.new(vs)
                    except ValueError:
                        continue
                    f.material_index = mi
                    nrm = (V(pts[1]) - V(pts[0])).cross(V(pts[2]) - V(pts[0]))
                    ax = max(range(3), key=lambda i: abs(nrm[i])) if nrm.length > 1e-9 else 2
                    a, b = [i for i in range(3) if i != ax]
                    for lp, p in zip(f.loops, pts):
                        lp[uvl].uv = (p[a] / sc, p[b] / sc)
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
            me = bpy.data.meshes.new((node or root_name) + '_mesh'); bm.to_mesh(me); bm.free()
            for m in mats:
                me.materials.append(m)
            o = bpy.data.objects.new((node + '_mesh') if node else (root_name + '_static'), me); bpy.context.scene.collection.objects.link(o)
            o.parent = node_objs[node] if node else root; objs.append(o)
        return root, objs


# ------------------------------------------------------------------ plans
OPEN_KINDS = {'open', 'void', 'stair_open'}
HABITABLE = {'living', 'bed', 'kitchen', 'dining', 'study', 'lounge', 'family', 'hall'}
WET = {'bath', 'wc'}


def rect_of(r):
    return r['rect']


def room_at(rooms, x, y):
    for r in rooms:
        x0, y0, x1, y1 = r['rect']
        if x0 < x < x1 and y0 < y < y1:
            return r
    return None


def enclosed(r):
    return r is not None and r['kind'] not in OPEN_KINDS


def wall_pieces(floor):
    """elementary wall pieces of one floor: dict(o='h'|'v', c, a0, a1, A, B) where A is the room on the low side
    (smaller y for 'h', smaller x for 'v') and B on the high side (None = outside)"""
    rooms = floor['rooms']; lines = {}
    for r in rooms:
        x0, y0, x1, y1 = r['rect']
        lines.setdefault(('h', round(y0, 3)), []).append((x0, x1)); lines.setdefault(('h', round(y1, 3)), []).append((x0, x1))
        lines.setdefault(('v', round(x0, 3)), []).append((y0, y1)); lines.setdefault(('v', round(x1, 3)), []).append((y0, y1))
    out = []
    for (o, c), ivs in lines.items():
        cuts = sorted({round(v, 3) for iv in ivs for v in iv} | {round(v, 3) for r in rooms for v in ((r['rect'][0], r['rect'][2]) if o == 'h' else (r['rect'][1], r['rect'][3]))})
        for a0, a1 in zip(cuts, cuts[1:]):
            m = (a0 + a1) / 2
            if not any(i0 - 1e-6 <= m <= i1 + 1e-6 for i0, i1 in ivs):
                continue
            A = room_at(rooms, m, c - 0.05) if o == 'h' else room_at(rooms, c - 0.05, m)
            B = room_at(rooms, m, c + 0.05) if o == 'h' else room_at(rooms, c + 0.05, m)
            if A is B:
                continue
            out.append(dict(o=o, c=c, a0=a0, a1=a1, A=A, B=B))
    # merge consecutive pieces with the same rooms on both sides
    out.sort(key=lambda p: (p['o'], p['c'], p['a0'])); merged = []
    for p in out:
        q = merged[-1] if merged else None
        if q and q['o'] == p['o'] and q['c'] == p['c'] and abs(q['a1'] - p['a0']) < 1e-6 and q['A'] is p['A'] and q['B'] is p['B']:
            q['a1'] = p['a1']
        else:
            merged.append(dict(p))
    return merged


def is_open_pair(floor, A, B):
    names = {A['name'] if A else None, B['name'] if B else None}
    return any(set(pr) == names for pr in floor.get('open_pairs', []))


def piece_kind(floor, p):
    """'wall_ext' | 'wall_int' | 'rail' | None"""
    A, B = p['A'], p['B']
    names = {A['name'] if A else None, B['name'] if B else None}
    if any(set(pr) == names for pr in floor.get('clear_pairs', [])):
        return None
    void = lambda r: r is not None and r['kind'] == 'void'
    if (void(A) and enclosed(B)) or (void(B) and enclosed(A)):
        return 'wall_int'                       # stairwell walls
    if (void(A) and B is None) or (void(B) and A is None):
        r = A if void(A) else B
        return 'rail' if r.get('outdoor') else 'wall_ext'
    if is_open_pair(floor, A, B):
        return 'rail' if (A and A['kind'] == 'void') or (B and B['kind'] == 'void') else None
    eA, eB = enclosed(A), enclosed(B)
    if eA and eB:
        return 'wall_int'
    if eA or eB:
        return 'wall_ext'
    # neither enclosed: open/void/outside
    if (floor['z'] > 0 or floor.get('rail_open')) and ((A and A['kind'] == 'open') or (B and B['kind'] == 'open')):
        if not ((A and A['kind'] == 'open') and (B and B['kind'] == 'open')):
            return 'rail'
    if bool(A and A['kind'] == 'void') != bool(B and B['kind'] == 'void'):
        return 'rail'
    return None


def find_shared(floor, a, b):
    """pieces between rooms named a and b (b may be None for outside)"""
    res = []
    for p in floor['pieces']:
        na = p['A']['name'] if p['A'] else None; nb = p['B']['name'] if p['B'] else None
        if {na, nb} == {a, b}:
            res.append(p)
    return res


def place_openings(floor, plan):
    """doors from the plan, then automatic windows on exterior walls. Each opening: dict(piece, s0, s1, z0, z1, kind, ...)"""
    ops = []
    for d in floor.get('doors', []):
        a, b = d[0], d[1]; w = d[2] if len(d) > 2 else 0.9; kind = d[3] if len(d) > 3 else 'door'; frac = d[4] if len(d) > 4 else 0.5
        ps = find_shared(floor, a, None if b == 'out' else b)
        if b == 'out' and len(d) > 5:      # side hint for outside doors
            side = d[5]
            ps = [p for p in ps if (side == 'front' and p['o'] == 'h' and p['c'] == min(r['rect'][1] for r in floor['rooms'] if r['name'] == a))
                  or (side == 'back' and p['o'] == 'h' and p['c'] == max(r['rect'][3] for r in floor['rooms'] if r['name'] == a))
                  or (side in ('left', 'right') and p['o'] == 'v')]
        if not ps:
            raise ValueError(f"no shared wall for door {d} on floor {floor['z']}")
        p = max(ps, key=lambda q: q['a1'] - q['a0']); L = p['a1'] - p['a0']
        w = min(w, L - 0.2); m = p['a0'] + 0.1 + w / 2 + (L - 0.2 - w) * frac
        ops.append(dict(piece=p, s0=m - w / 2, s1=m + w / 2, z0=0.0, z1=2.1 if kind != 'arch' else 2.4, kind=kind, rooms=(a, b), main=len(d) > 6 and d[6]))
    party = plan.get('party', [])
    for p in floor['pieces']:
        if piece_kind(floor, p) != 'wall_ext':
            continue
        if any((p['o'], round(p['c'], 3)) == (o, round(c, 3)) for o, c in party):
            continue
        room = p['A'] if enclosed(p['A']) else p['B']
        if not enclosed(room):
            continue
        k = room['kind']
        if k in ('store', 'stair', 'corridor') or room.get('no_windows'):
            continue
        L = p['a1'] - p['a0']
        if k in WET:
            w, z0, z1 = 0.6, 1.5, 2.1
        elif k == 'kitchen':
            w, z0, z1 = 1.2, 1.1, 2.1
        else:
            w, z0, z1 = 1.5, 0.9, 2.1
        busy = [(o['s0'], o['s1']) for o in ops if o['piece'] is p]
        free = [(p['a0'] + 0.35, p['a1'] - 0.35)]
        for b0, b1 in busy:
            nf = []
            for f0, f1 in free:
                if b1 + 0.3 <= f0 or b0 - 0.3 >= f1:
                    nf.append((f0, f1))
                else:
                    if b0 - 0.3 > f0:
                        nf.append((f0, b0 - 0.3))
                    if b1 + 0.3 < f1:
                        nf.append((b1 + 0.3, f1))
            free = nf
        for f0, f1 in free:
            span = f1 - f0
            if span < 0.6:
                continue
            n = 2 if span > 4.4 and k not in WET else 1
            ww = min(w, span / n - 0.2)
            if ww < 0.5:
                continue
            for i in range(n):
                m = f0 + span * (i + 0.5) / n
                ops.append(dict(piece=p, s0=m - ww / 2, s1=m + ww / 2, z0=z0, z1=z1, kind='window', room=room['name']))
    floor['openings'] = ops


def outside_sign(floor, p):
    """+1 if the outside (non-enclosed side) is on the high side of the piece, -1 if on the low side"""
    return 1 if not enclosed(p['B']) else -1


# ------------------------------------------------------------------ build a dwelling / building
def build_building(M, plan, mats, mode, base_z=0.0, off=(0.0, 0.0), prefix=''):
    """mode 'interior' (all walls, floors, ceilings, doors open) or 'exterior' (shell, roof, plinth, doors closed)"""
    ox, oy = off
    info = dict(doors=[], rooms=[])
    floors = plan['floors']
    if mode == 'interior':
        M.node(prefix + 'ceiling', (0, 0, 0))
    cols = set()
    for fl in floors:
        fl['pieces'] = wall_pieces(fl)
        place_openings(fl, plan)
    top = max(fl['z'] for fl in floors)
    for fl in floors:
        z = base_z + fl['z'] * STOREY
        upper = fl['z'] > 0
        # floors
        for r in fl['rooms']:
            x0, y0, x1, y1 = r['rect']
            info['rooms'].append(dict(name=r['name'], kind=r['kind'], floor=fl['z'], rect=[round(x0 + ox, 3), round(y0 + oy, 3), round(x1 + ox, 3), round(y1 + oy, 3)],
                                      size=[round(x1 - x0, 2), round(y1 - y0, 2)]))
            if r['kind'] == 'void':
                continue
            fm = mats[r.get('floor', {'living': 'f_living', 'lounge': 'f_living', 'family': 'f_living', 'dining': 'f_living', 'hall': 'f_living', 'corridor': 'f_living',
                                      'bed': 'f_room', 'study': 'f_wood', 'bath': 'f_bath', 'wc': 'f_bath', 'kitchen': 'f_kitchen', 'store': 'f_kitchen',
                                      'open': 'f_veranda', 'stair': 'f_living', 'stair_open': 'f_concrete'}.get(r['kind'], 'f_room'))]
            if mode == 'interior' or r['kind'] == 'open':
                if r['kind'] != 'stair_open':
                    M.box(fm, x0 + ox, x1 + ox, y0 + oy, y1 + oy, z - (0.25 if upper else 0.05), z, faces=('+z', '-z') if upper else ('+z',))
            if mode == 'interior' and enclosed(r) and r['kind'] != 'stair' and not r.get('no_ceiling'):
                M.box(mats['ceiling'], x0 + ox, x1 + ox, y0 + oy, y1 + oy, z + CEIL, z + CEIL + 0.02, node=prefix + 'ceiling', faces=('-z',))
            if r['kind'] in ('stair', 'stair_open'):
                stair(M, mats, r, z, ox, oy)
            if mode == 'interior' and r['kind'] in WET:      # tiled walls to 2.1 m inside wet rooms
                for p in fl['pieces']:
                    if p['A'] is r or p['B'] is r:
                        sgn = 1 if p['A'] is r else -1          # room on the low side -> panel just below the line
                        t = (T_EXT if piece_kind(fl, p) == 'wall_ext' else T_INT) / 2 + 0.005
                        ops = [o for o in fl['openings'] if o['piece'] is p]
                        segs = solid_segments(p['a0'], p['a1'], [(o['s0'], o['s1'], o['z0'], o['z1']) for o in ops], 0, 2.1)
                        for a0, a1, zz0, zz1 in segs:
                            if p['o'] == 'h':
                                cc = p['c'] - sgn * t
                                M.box(mats['bath_wall'], a0 + ox, a1 + ox, cc - 0.004 + oy, cc + 0.004 + oy, z + zz0, z + zz1)
                            else:
                                cc = p['c'] - sgn * t
                                M.box(mats['bath_wall'], cc - 0.004 + ox, cc + 0.004 + ox, a0 + oy, a1 + oy, z + zz0, z + zz1)
        # walls and railings; a horizontal wall is lengthened by half a thickness only at ends with no wall continuing on the same line
        built = [q for q in fl['pieces'] if piece_kind(fl, q) in (('wall_ext',) if mode == 'exterior' else ('wall_ext', 'wall_int'))]
        ends = {}
        for q in built:
            for e in (q['a0'], q['a1']):
                ends[(q['o'], round(q['c'], 3), round(e, 3))] = ends.get((q['o'], round(q['c'], 3), round(e, 3)), 0) + 1
        for p in fl['pieces']:
            k = piece_kind(fl, p)
            if k is None:
                continue
            if k == 'rail':
                railing(M, mats, p, z, ox, oy, fl)
                continue
            if mode == 'exterior' and k != 'wall_ext':
                continue
            t = T_EXT if k == 'wall_ext' else T_INT
            mat = mats['wall_in'] if mode == 'interior' else mats['wall_out']
            ops = [o for o in fl['openings'] if o['piece'] is p]
            free_end = lambda e: ends.get((p['o'], round(p['c'], 3), round(e, 3)), 0) <= 1
            e0 = T_EXT / 2 if p['o'] == 'h' and free_end(p['a0']) else 0.0
            e1 = T_EXT / 2 if p['o'] == 'h' and free_end(p['a1']) else 0.0
            for a0, a1, zz0, zz1 in solid_segments(p['a0'] - e0, p['a1'] + e1,
                                                   [(o['s0'], o['s1'], o['z0'], o['z1']) for o in ops], 0, STOREY):
                if p['o'] == 'h':
                    M.box(mat, a0 + ox, a1 + ox, p['c'] - t / 2 + oy, p['c'] + t / 2 + oy, z + zz0, z + zz1)
                else:
                    M.box(mat, p['c'] - t / 2 + ox, p['c'] + t / 2 + ox, a0 + oy, a1 + oy, z + zz0, z + zz1)
            for o in ops:
                if o['kind'] == 'window':
                    window(M, mats, p, o, t, z, ox, oy, mode, fl)
                else:
                    d = door(M, mats, p, o, t, z, ox, oy, mode, fl, prefix)
                    if d:
                        info['doors'].append(d)
        # columns at the outer corners of open rooms
        for r in fl['rooms']:
            if r['kind'] != 'open' or r.get('no_columns'):
                continue
            x0, y0, x1, y1 = r['rect']
            for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                touch = any(enclosed(q) and q['rect'][0] - 1e-3 <= cx <= q['rect'][2] + 1e-3 and q['rect'][1] - 1e-3 <= cy <= q['rect'][3] + 1e-3 for q in fl['rooms'])
                key = (round(cx + ox, 2), round(cy + oy, 2), fl['z'])
                if not touch and key not in cols:
                    cols.add(key)
                    zt = z + (STOREY if fl['z'] < top or mode == 'exterior' else CEIL)
                    if fl['z'] == top and mode == 'interior':
                        zt = z + 1.0           # top-floor balcony in an interior: newel post only
                    M.box(mats['column'], cx - 0.15 + ox, cx + 0.15 + ox, cy - 0.15 + oy, cy + 0.15 + oy, z, zt)
    return info


def solid_segments(a0, a1, holes, z0, z1):
    """boxes (a0, a1, z0, z1) of a wall from a0 to a1, z0..z1, minus rectangular holes (s0, s1, hz0, hz1)"""
    out = []; holes = sorted(h for h in holes if h[1] > a0 and h[0] < a1)
    cur = a0
    for s0, s1, hz0, hz1 in holes:
        if s0 > cur:
            out.append((cur, s0, z0, z1))
        if hz0 > z0:
            out.append((s0, s1, z0, hz0))
        if hz1 < z1:
            out.append((s0, s1, hz1, z1))
        cur = max(cur, s1)
    if cur < a1:
        out.append((cur, a1, z0, z1))
    return out


def along(p, s, n, ox, oy):
    """point at position s along the piece, offset n across it (+ = high side)"""
    return (s + ox, p['c'] + n + oy) if p['o'] == 'h' else (p['c'] + n + ox, s + oy)


def bx(M, mat, p, s0, s1, n0, n1, z0, z1, ox, oy, node=None):
    if p['o'] == 'h':
        M.box(mat, s0 + ox, s1 + ox, p['c'] + n0 + oy, p['c'] + n1 + oy, z0, z1, node)
    else:
        M.box(mat, p['c'] + n0 + ox, p['c'] + n1 + ox, s0 + oy, s1 + oy, z0, z1, node)


def window(M, mats, p, o, t, z, ox, oy, mode, fl):
    s0, s1, z0, z1 = o['s0'], o['s1'], z + o['z0'], z + o['z1']
    f = 0.05
    for a, b, c, d in ((s0, s1, z0, z0 + f), (s0, s1, z1 - f, z1), (s0, s0 + f, z0, z1), (s1 - f, s1, z0, z1), ((s0 + s1) / 2 - 0.02, (s0 + s1) / 2 + 0.02, z0, z1)):
        bx(M, mats['win_frame'], p, a, b, -0.04, 0.04, c, d, ox, oy)
    bx(M, mats['glass_out'] if mode == 'exterior' else mats['glass_in'], p, s0 + f, s1 - f, -0.006, 0.006, z0 + f, z1 - f, ox, oy)
    sg = outside_sign(fl, p); n = sg * (t / 2 + 0.03)
    # burglary-proof bars on the outside face: square rods every 12 cm, two flat bars, a frame
    for a, b, c, d in ((s0, s1, z0, z0 + 0.03), (s0, s1, z1 - 0.03, z1), (s0, s1, (z0 + z1) / 2 - 0.015, (z0 + z1) / 2 + 0.015)):
        bx(M, mats['steel'], p, a, b, min(n, n + sg * 0.02), max(n, n + sg * 0.02), c, d, ox, oy)
    k = max(2, int((s1 - s0) / 0.12))
    for i in range(k + 1):
        s = s0 + (s1 - s0) * i / k
        bx(M, mats['steel'], p, s - 0.008, s + 0.008, min(n, n + sg * 0.016), max(n, n + sg * 0.016), z0, z1, ox, oy)
    # sill
    bx(M, mats['plinth'], p, s0 - 0.05, s1 + 0.05, -t / 2 - 0.04, t / 2 + 0.04, z0 - 0.04, z0, ox, oy)


def door(M, mats, p, o, t, z, ox, oy, mode, fl, prefix):
    s0, s1, z1 = o['s0'], o['s1'], z + o['z1']
    for a, b, c, d in ((s0 - 0.06, s0, z, z1), (s1, s1 + 0.06, z, z1), (s0 - 0.06, s1 + 0.06, z1, z1 + 0.06)):
        bx(M, mats['frame'], p, a, b, -t / 2 - 0.01, t / 2 + 0.01, c, d, ox, oy)
    if o['kind'] == 'arch':
        return None
    a, b = o['rooms']; outside = b == 'out' or not enclosed(p['A']) or not enclosed(p['B'])
    if mode == 'exterior' and not outside:
        return None
    name = f"{prefix}door_f{fl['z']}_{a}_{b}".replace(' ', '_')
    w = s1 - s0
    # hinge at s0, leaf swings toward the low side (-n) when opened inward
    hx, hy = along(p, s0, 0, ox, oy)
    open_ang = 0.0
    if mode == 'interior':
        open_ang = math.radians(85) * (1 if p['o'] == 'h' else -1)
    M.node(name, (hx, hy, z), open_ang)
    leaf_mat = mats['door_wood']
    # leaf modelled closed, relative positions in world space before the node rotation is applied by the importer
    bx(M, leaf_mat, p, s0, s1, -0.025, 0.025, z, z1 - 0.01, ox, oy, node=name)
    hh = along(p, s1 - 0.08, 0.04, ox, oy)
    M.box(mats['steel'], hh[0] - 0.015, hh[0] + 0.015, hh[1] - 0.015, hh[1] + 0.015, z + 1.0, z + 1.05, node=name)
    if o.get('main') or (outside and mode == 'exterior' and b == 'out') or (outside and o.get('main') is None and fl['z'] == 0 and b != 'out' and False):
        pass
    sec = None
    if o.get('main'):
        sg = outside_sign(fl, p); n0 = sg * (t / 2 + 0.02)
        sec = name + '_security'
        hx2, hy2 = along(p, s0, n0, ox, oy)
        M.node(sec, (hx2, hy2, z), (math.radians(-85) * (1 if p['o'] == 'h' else -1)) * (1 if mode == 'interior' else 0) * 0)
        # barred steel security door in front of the main door
        for a_, b_, c_, d_ in ((s0, s1, z, z + 0.05), (s0, s1, z1 - 0.06, z1 - 0.01), (s0, s0 + 0.05, z, z1 - 0.01), (s1 - 0.05, s1, z, z1 - 0.01),
                               (s0, s1, z + 0.9, z + 0.95)):
            bx(M, mats['steel'], p, a_, b_, min(n0, n0 + sg * 0.03), max(n0, n0 + sg * 0.03), c_, d_, ox, oy, node=sec)
        k = int(w / 0.11)
        for i in range(1, k):
            s = s0 + w * i / k
            bx(M, mats['steel'], p, s - 0.008, s + 0.008, min(n0, n0 + sg * 0.02), max(n0, n0 + sg * 0.02), z + 0.05, z1 - 0.06, ox, oy, node=sec)
        bx(M, mats['steel'], p, s0, s1, min(n0, n0 + sg * 0.01), max(n0, n0 + sg * 0.01), z + 0.05, z + 0.9, ox, oy, node=sec)   # sheet panel below
    pos = along(p, (s0 + s1) / 2, 0, ox, oy)
    return dict(node=name, security_node=sec, between=[a, b], floor=fl['z'], centre=[round(pos[0], 3), round(pos[1], 3), round(z, 3)], width=round(w, 2),
                wall='x' if p['o'] == 'h' else 'z', main=bool(o.get('main')))


def railing(M, mats, p, z, ox, oy, fl):
    h = 1.0
    bx(M, mats['rail'], p, p['a0'], p['a1'], -0.03, 0.03, z + h - 0.05, z + h, ox, oy)
    bx(M, mats['rail'], p, p['a0'], p['a1'], -0.02, 0.02, z + 0.1, z + 0.14, ox, oy)
    k = max(2, int((p['a1'] - p['a0']) / 0.12))
    for i in range(k + 1):
        s = p['a0'] + (p['a1'] - p['a0']) * i / k
        bx(M, mats['rail'], p, s - 0.009, s + 0.009, -0.009, 0.009, z, z + h, ox, oy)


def stair(M, mats, r, z, ox, oy):
    x0, y0, x1, y1 = r['rect']; d = r.get('dir', '+y'); n = 18; rise = STOREY / n
    along_y = d in ('+y', '-y'); L = (y1 - y0) if along_y else (x1 - x0)
    run = L / n
    for i in range(n):
        top = z + rise * (i + 1)
        if d == '+y':
            M.box(mats['step'], x0 + 0.05 + ox, x1 - 0.05 + ox, y0 + run * i + oy, y0 + run * (i + 1) + oy, top - 0.18 if i else z, top)
        elif d == '-y':
            M.box(mats['step'], x0 + 0.05 + ox, x1 - 0.05 + ox, y1 - run * (i + 1) + oy, y1 - run * i + oy, top - 0.18 if i else z, top)
        elif d == '+x':
            M.box(mats['step'], x0 + run * i + ox, x0 + run * (i + 1) + ox, y0 + 0.05 + oy, y1 - 0.05 + oy, top - 0.18 if i else z, top)
        else:
            M.box(mats['step'], x1 - run * (i + 1) + ox, x1 - run * i + ox, y0 + 0.05 + oy, y1 - 0.05 + oy, top - 0.18 if i else z, top)
    if r['kind'] == 'stair_open':      # handrail on the open side(s)
        for side in r.get('rails', []):
            k = 8
            for i in range(k + 1):
                f = i / k; zz = z + STOREY * f
                if along_y:
                    xx = x0 if side == 'lo' else x1; yy = (y0 + L * f) if d == '+y' else (y1 - L * f)
                    M.box(mats['rail'], xx - 0.02 + ox, xx + 0.02 + ox, yy - 0.02 + oy, yy + 0.02 + oy, zz, zz + 1.0)
                else:
                    yy = y0 if side == 'lo' else y1; xx = (x0 + L * f) if d == '+x' else (x1 - L * f)
                    M.box(mats['rail'], xx - 0.02 + ox, xx + 0.02 + ox, yy - 0.02 + oy, yy + 0.02 + oy, zz, zz + 1.0)


def roof(M, mats, x0, y0, x1, y1, z, pitch=22, over=0.6, ox=0, oy=0):
    x0, y0, x1, y1 = x0 - over + ox, y0 - over + oy, x1 + over + ox, y1 + over + oy
    W, D = x1 - x0, y1 - y0; tn = math.tan(math.radians(pitch))
    if W >= D:
        h = D / 2 * tn; r0 = (x0 + D / 2, (y0 + y1) / 2, z + h); r1 = (x1 - D / 2, (y0 + y1) / 2, z + h)
        M.poly(mats['roof'], [(x0, y0, z), (x1, y0, z), r1, r0]); M.poly(mats['roof'], [(x1, y1, z), (x0, y1, z), r0, r1])
        M.poly(mats['roof'], [(x0, y1, z), (x0, y0, z), r0]); M.poly(mats['roof'], [(x1, y0, z), (x1, y1, z), r1])
    else:
        h = W / 2 * tn; r0 = ((x0 + x1) / 2, y0 + W / 2, z + h); r1 = ((x0 + x1) / 2, y1 - W / 2, z + h)
        M.poly(mats['roof'], [(x1, y0, z), (x1, y1, z), r1, r0]); M.poly(mats['roof'], [(x0, y1, z), (x0, y0, z), r0, r1])
        M.poly(mats['roof'], [(x0, y0, z), (x1, y0, z), r0]); M.poly(mats['roof'], [(x1, y1, z), (x0, y1, z), r1])
    M.poly(mats['soffit'], [(x0, y0, z), (x0, y1, z), (x1, y1, z), (x1, y0, z)])
    for a, b, c, d in ((x0, x1, y0 - 0.02, y0), (x0, x1, y1, y1 + 0.02), (x0 - 0.02, x0, y0, y1), (x1, x1 + 0.02, y0, y1)):
        M.box(mats['fascia'], a, b, c, d, z - 0.2, z)
    return h


def plan_bbox(plan, floors=None, kinds=None):
    xs, ys = [], []
    for fl in plan['floors']:
        if floors is not None and fl['z'] not in floors:
            continue
        for r in fl['rooms']:
            if kinds and r['kind'] not in kinds:
                continue
            xs += [r['rect'][0], r['rect'][2]]; ys += [r['rect'][1], r['rect'][3]]
    return min(xs), min(ys), max(xs), max(ys)


def exterior_building(M, plan, mats, off, plinth=0.3, pitch=22):
    """shell + roof + plinth + entrance steps for a plan placed with its plan origin at `off` (compound coords)"""
    ox, oy = off
    info = build_building(M, plan, mats, 'exterior', base_z=plinth, off=off, prefix=plan.get('prefix', ''))
    gx0, gy0, gx1, gy1 = plan_bbox(plan, floors=[0])
    M.box(mats['plinth'], gx0 - 0.12 + ox, gx1 + 0.12 + ox, gy0 - 0.12 + oy, gy1 + 0.12 + oy, 0, plinth - 0.05, faces=('+z', '-y', '+y', '-x', '+x'))
    top = max(fl['z'] for fl in plan['floors'])
    rx0, ry0, rx1, ry1 = plan.get('roof_rect') or plan_bbox(plan)
    rh = roof(M, mats, rx0, ry0, rx1, ry1, plinth + (top + 1) * STOREY, pitch, plan.get('overhang', 0.6), ox, oy)
    # upper-floor slabs show as bands between storeys on the outside
    for d in info['doors']:
        if d['main'] or 'out' in d['between']:
            cx, cy, cz = d['centre']
            if cz <= plinth + 0.01:       # ground floor: steps down to the compound
                for i, (dz, dd) in enumerate(((plinth - 0.1, 0.35), (plinth - 0.2, 0.7))):
                    pass
    for st in plan.get('steps', []):     # entrance steps: (x0, x1, y of the plinth edge, '-y' = steps go toward the front)
        x0, x1, y, dirn = st; sg = -1 if dirn == '-y' else 1
        for i, zt in enumerate((plinth - 0.1, plinth - 0.2)):
            ya, yb = y + sg * 0.12 + sg * 0.3 * i, y + sg * 0.12 + sg * 0.3 * (i + 1)
            M.box(mats['step'], x0 + ox, x1 + ox, min(ya, yb) + oy, max(ya, yb) + oy, 0, zt)
    return info, rh


# ------------------------------------------------------------------ compound
def compound(M, mats, W, D, gate_x=0.0, gate_w=7.2, wall_h=2.4, wall_mat=None, prefix=''):
    """block wall with pillars and coping round a W x D compound centred on the origin; gate in the front (y = -D/2) wall"""
    wm = wall_mat or mats['wall_out']; t = 0.23
    x0, x1, y0, y1 = -W / 2, W / 2, -D / 2, D / 2
    g0, g1 = gate_x - gate_w / 2, gate_x + gate_w / 2
    runs = [((x0, y0), (g0 - 0.25, y0)), ((g1 + 0.25, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
    for (ax, ay), (bx_, by) in runs:
        lx0, lx1, ly0, ly1 = min(ax, bx_), max(ax, bx_), min(ay, by), max(ay, by)
        if ly0 == ly1:
            M.box(wm, lx0 - t / 2, lx1 + t / 2, ly0 - t / 2, ly0 + t / 2, 0, wall_h)
            M.box(mats['plinth'], lx0 - t / 2 - 0.03, lx1 + t / 2 + 0.03, ly0 - t / 2 - 0.03, ly0 + t / 2 + 0.03, wall_h, wall_h + 0.06)
            n = max(1, int((lx1 - lx0) / 3.0))
            for i in range(n + 1):
                px = lx0 + (lx1 - lx0) * i / n
                M.box(wm, px - 0.2, px + 0.2, ly0 - 0.2, ly0 + 0.2, 0, wall_h + 0.2)
        else:
            M.box(wm, lx0 - t / 2, lx0 + t / 2, ly0, ly1, 0, wall_h)
            M.box(mats['plinth'], lx0 - t / 2 - 0.03, lx0 + t / 2 + 0.03, ly0, ly1, wall_h, wall_h + 0.06)
            n = max(1, int((ly1 - ly0) / 3.0))
            for i in range(n + 1):
                py = ly0 + (ly1 - ly0) * i / n
                M.box(wm, lx0 - 0.2, lx0 + 0.2, py - 0.2, py + 0.2, 0, wall_h + 0.2)
    # gate pillars and two steel leaves (nodes, hinged at the pillars, swing inward)
    for px in (g0 - 0.25, g1 + 0.25):
        M.box(wm, px - 0.25, px + 0.25, y0 - 0.25, y0 + 0.25, 0, wall_h + 0.4)
        M.box(mats['plinth'], px - 0.3, px + 0.3, y0 - 0.3, y0 + 0.3, wall_h + 0.4, wall_h + 0.48)
    leaf = gate_w / 2; gh = 2.2
    for name, hx, sg in ((prefix + 'gate_left', g0, 1), (prefix + 'gate_right', g1, -1)):
        M.node(name, (hx, y0, 0))
        a0, a1 = (hx, hx + leaf - 0.02) if sg > 0 else (hx - leaf + 0.02, hx)
        M.box(mats['steel'], a0, a1, y0 - 0.025, y0 + 0.025, 0.05, 1.1, node=name)                       # sheet panel
        for zz in (1.1, gh):
            M.box(mats['steel'], a0, a1, y0 - 0.03, y0 + 0.03, zz - 0.05, zz, node=name)
        for xx in (a0, a1):
            M.box(mats['steel'], xx - 0.03, xx + 0.03, y0 - 0.03, y0 + 0.03, 0.05, gh, node=name)
        k = int(leaf / 0.12)
        for i in range(1, k):
            xx = a0 + (a1 - a0) * i / k
            M.box(mats['steel'], xx - 0.01, xx + 0.01, y0 - 0.01, y0 + 0.01, 1.1, gh + (0.12 if i % 2 else 0.05), node=name)
    return dict(gate=dict(left=prefix + 'gate_left', right=prefix + 'gate_right', centre=[gate_x, 0, y0], width=gate_w,
                          note='leaves hinged at the pillars; open inward by rotating about the vertical axis'))


def ground(M, mats, W, D, paved, holes=()):
    """grass over the compound, paving rectangles on top (1 cm higher); holes = rectangles left open (pool)"""
    grass = material('ground_grass', 'leafy_grass' if 'leafy_grass' in TEX else 'grass', (1, 1, 1), 3.0, 0.9)
    pave = material('paving_interlock', 'hexagonal_concrete_paving', (1, 1, 1), 2.0, 0.8)
    rects = [(-W / 2, -D / 2, W / 2, D / 2)]
    for hx0, hy0, hx1, hy1 in holes:
        nr = []
        for x0, y0, x1, y1 in rects:
            if hx1 <= x0 or hx0 >= x1 or hy1 <= y0 or hy0 >= y1:
                nr.append((x0, y0, x1, y1)); continue
            if hy0 > y0: nr.append((x0, y0, x1, hy0))
            if hy1 < y1: nr.append((x0, hy1, x1, y1))
            if hx0 > x0: nr.append((x0, max(y0, hy0), hx0, min(y1, hy1)))
            if hx1 < x1: nr.append((hx1, max(y0, hy0), x1, min(y1, hy1)))
        rects = nr
    for x0, y0, x1, y1 in rects:
        M.poly(grass, [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)])
    # paving: the union of the rectangles, split into non-overlapping cells (overlapping coplanar faces flicker)
    xs = sorted({v for r in paved for v in (r[0], r[2])}); ys = sorted({v for r in paved for v in (r[1], r[3])})
    for xa, xb in zip(xs, xs[1:]):
        for ya, yb in zip(ys, ys[1:]):
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            if any(r[0] <= mx <= r[2] and r[1] <= my <= r[3] for r in paved):
                M.poly(pave, [(xa, ya, 0.02), (xb, ya, 0.02), (xb, yb, 0.02), (xa, yb, 0.02)])


def car_bays(M, n, x0, y, w=2.5, d=5.0, facing='+y'):
    line = material('road_marking_white', None, (0.92, 0.92, 0.9), 1, 0.6)
    bays = []
    for i in range(n + 1):
        xx = x0 + i * w
        M.box(line, xx - 0.05, xx + 0.05, y, y + d, 0.02, 0.025)
    for i in range(n):
        bays.append([round(x0 + (i + 0.5) * w, 2), round(y + d / 2, 2)])
    return bays


def generator_spot(M, mats, x, y, rot=0.0):
    """concrete pad 2.0 x 1.6 with a lean-to canopy; returns the pad centre for placing a generator from assets/home"""
    M.box(mats['f_concrete'], x - 1.0, x + 1.0, y - 0.8, y + 0.8, 0, 0.12)
    sheet = material('corrugated_sheet', 'corrugated_metal_roof' if 'corrugated_metal_roof' in TEX else None, (0.85, 0.85, 0.85), 1.5, 0.5, 0.6)
    for px, py, h in ((x - 0.95, y - 0.75, 2.2), (x + 0.95, y - 0.75, 2.2), (x - 0.95, y + 0.75, 2.0), (x + 0.95, y + 0.75, 2.0)):
        M.box(mats['steel'], px - 0.03, px + 0.03, py - 0.03, py + 0.03, 0.12, h)
    M.poly(sheet, [(x - 1.1, y - 0.9, 2.22), (x + 1.1, y - 0.9, 2.22), (x + 1.1, y + 0.9, 2.02), (x - 1.1, y + 0.9, 2.02)])
    M.poly(sheet, [(x - 1.1, y + 0.9, 2.0), (x + 1.1, y + 0.9, 2.0), (x + 1.1, y - 0.9, 2.2), (x - 1.1, y - 0.9, 2.2)])
    return [x, y, 0.12]


def tank_stand(M, mats, x, y, h=3.0):
    """steel stand with a 2,000 litre plastic tank (1.3 m across, 1.65 m tall)"""
    tank = material('water_tank_black', None, (0.05, 0.05, 0.055), 1, 0.55)
    s = 0.75
    for px in (x - s, x + s):
        for py in (y - s, y + s):
            M.box(mats['steel'], px - 0.05, px + 0.05, py - 0.05, py + 0.05, 0, h)
    for zz in (0.9, 1.9):
        for (a, b, c, d) in ((x - s, x + s, y - s - 0.02, y - s + 0.02), (x - s, x + s, y + s - 0.02, y + s + 0.02),
                             (x - s - 0.02, x - s + 0.02, y - s, y + s), (x + s - 0.02, x + s + 0.02, y - s, y + s)):
            M.box(mats['steel'], a, b, c, d, zz, zz + 0.05)
    M.box(mats['steel'], x - s - 0.1, x + s + 0.1, y - s - 0.1, y + s + 0.1, h, h + 0.08)
    M.cyl(tank, x, y, h + 0.08, h + 0.08 + 1.55, 0.65, 16)
    M.cyl(tank, x, y, h + 1.63, h + 1.73, 0.25, 12)
    M.box(mats['steel'], x + 0.5, x + 0.56, y - 0.03, y + 0.03, 0.2, h + 0.1)      # outlet pipe
    return [x, y, h]


def pool(M, mats, x0, y0, x1, y1, depth=1.5):
    tiles = material('pool_tiles', 'blue_floor_tiles_01', (0.45, 0.7, 0.95), 1.2, 0.3)
    water = material('pool_water', None, (0.2, 0.55, 0.75), 1, 0.05, alpha=0.55)
    cope = material('pool_coping', 'terrazzo_tiles', (1, 1, 1), 1.6, 0.4)
    M.poly(tiles, [(x0, y0, -depth), (x1, y0, -depth), (x1, y1, -depth), (x0, y1, -depth)])
    M.poly(tiles, [(x0, y0, -depth), (x0, y0, 0), (x1, y0, 0), (x1, y0, -depth)][::-1])
    M.poly(tiles, [(x1, y1, -depth), (x1, y1, 0), (x0, y1, 0), (x0, y1, -depth)][::-1])
    M.poly(tiles, [(x0, y1, -depth), (x0, y1, 0), (x0, y0, 0), (x0, y0, -depth)][::-1])
    M.poly(tiles, [(x1, y0, -depth), (x1, y0, 0), (x1, y1, 0), (x1, y1, -depth)][::-1])
    M.poly(water, [(x0, y0, -0.15), (x1, y0, -0.15), (x1, y1, -0.15), (x0, y1, -0.15)])
    for a, b, c, d in ((x0 - 0.3, x1 + 0.3, y0 - 0.3, y0), (x0 - 0.3, x1 + 0.3, y1, y1 + 0.3), (x0 - 0.3, x0, y0, y1), (x1, x1 + 0.3, y0, y1)):
        M.box(cope, a, b, c, d, 0, 0.05)
    return dict(rect=[x0, y0, x1, y1], depth=depth, water_level=-0.15)


def export(objs, path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', use_selection=True, export_animations=False, export_image_format='JPEG',
                              export_jpeg_quality=80)


def tris(objs):
    n = 0
    for o in objs:
        if o.type == 'MESH':
            o.data.calc_loop_triangles(); n += len(o.data.loop_triangles)
    return n


def reach_check(plan):
    """every enclosed room reachable from the main door through doors, arches, open pairs and stairs"""
    adj = {}
    def link(a, b):
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    start = None
    for fl in plan['floors']:
        for d in fl.get('doors', []):
            a, b = (fl['z'], d[0]), (fl['z'], d[1])
            if d[1] == 'out' or (len(d) > 6 and d[6]):
                start = start or (fl['z'], d[0])
                if d[1] != 'out':
                    link(a, b)
                continue
            link(a, b)
        for pr in fl.get('open_pairs', []):
            link((fl['z'], pr[0]), (fl['z'], pr[1]))
    for a, b in plan.get('stair_links', []):
        link(tuple(a), tuple(b))
    seen = set(); st = [start] if start else []
    while st:
        n = st.pop()
        if n in seen:
            continue
        seen.add(n); st += list(adj.get(n, []))
    missing = [(fl['z'], r['name']) for fl in plan['floors'] for r in fl['rooms'] if r['kind'] not in ('void',) and (fl['z'], r['name']) not in seen]
    return missing
