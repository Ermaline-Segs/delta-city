"""Sample furniture from assets/home for an interior preview (proves the rooms fit).
usage: python -I furn_gen.py <type.json> <assets/home> <out.json>   ->  [[glb, x, y_blender, z, rot_deg], ...]
Furniture fronts face glTF +Z (= Blender -Y, toward the front of the home); rot 180 turns a piece to face the back."""
import json, sys, os
J, H, OUT = sys.argv[1:4]
rooms = json.load(open(J))['interior']['rooms']
F = lambda p: os.path.join(H, p)
SZ = {'bed_king': (1.87, 2.15), 'bed_double': (1.62, 2.01), 'bed_single': (1.02, 2.01), 'wardrobe': (0.98, 0.63), 'sofa3': (2.03, 0.82), 'sofa1': (0.88, 0.82),
      'tvstand': (1.65, 0.44), 'centre': (1.0, 0.6), 'dining6': (3.08, 1.82), 'dining4': (1.5, 1.61), 'kbase': (2.42, 0.64), 'fridge': (0.7, 0.7),
      'cooker': (1.0, 0.65), 'toilet': (0.42, 0.68), 'shower': (0.92, 0.92), 'basin': (0.55, 0.45)}
out = []
used = set()


def put(f, x, y, z, rot=0):
    out.append([F(f), round(x, 3), round(y, 3), z, rot])


for r in rooms:
    x0, x1 = r['x']; y0, y1 = -r['z'][1], -r['z'][0]; z = r['floor_y']; k = r['kind']; w, d = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2; m = 0.12
    if k == 'bed':
        bed = 'bed_king' if w >= 3.9 and d >= 3.9 else ('bed_double' if w >= 2.8 else 'bed_single')
        bw, bd = SZ[bed]
        fn = {'bed_king': 'bedroom/bed_king_blue.glb', 'bed_double': 'bedroom/bed_double_starter.glb', 'bed_single': 'bedroom/bed_single_starter.glb'}[bed]
        put(fn, cx, y1 - m - bd / 2, z)
        if w - bw > 2.2:
            put('bedroom/wardrobe_oak.glb', x0 + m + 0.49, y1 - m - 0.32, z)
    elif k in ('living', 'lounge', 'family'):
        put('living-room/sofa_3-seater_navy.glb', cx, y1 - m - 0.41, z)
        put('living-room/centre_table_oak.glb', cx, y1 - m - 1.6, z)
        if d > 4.0:
            put('living-room/tv_stand_oak.glb', cx, y0 + m + 0.22 + 0.4, z, 180)
            put('living-room/tv_43in_black.glb', cx, y0 + m + 0.22 + 0.4, z + 0.58, 180)
        if w > 4.4:
            put('living-room/sofa_single_navy.glb', x0 + m + 0.5, (y0 + y1) / 2 + 0.3, z, 90)
    elif k == 'dining':
        big = w >= 4.6 and d >= 3.2
        put('dining-other/dining_set_6_oak.glb' if big else 'dining-other/dining_set_4_oak.glb', cx, (y0 + y1) / 2, z)
    elif k == 'kitchen':
        if w >= 2.6:
            put('kitchen/kitchen_base_units.glb', x0 + m + 1.21, y1 - m - 0.32, z)
            put('kitchen/fridge_white_starter.glb', x1 - m - 0.35, y1 - m - 0.35, z)
        else:
            put('kitchen/gas_cooker_with_cylinder.glb', cx, y1 - m - 0.33, z)
    elif k == 'bath':
        put('bathroom/toilet_starter.glb', x0 + m + 0.25, y1 - m - 0.34, z)
        if w >= 1.8:
            put('bathroom/shower_starter.glb', x1 - m - 0.46, y1 - m - 0.46, z)
    elif k == 'wc':
        put('bathroom/toilet_starter.glb', cx, y1 - m - 0.34, z)
json.dump(out, open(OUT, 'w'), indent=0)
print('FURN', len(out))
