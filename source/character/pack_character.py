"""Turn a MetaPerson .glb into the compact character the game loads.

Keeps the colour textures (at 512px), drops facial-expression data and the
extra surface maps, folds finger/eye/toe-tip joints into their parents so the
skeleton is small enough for phones, and stores vertices in compact form."""
import base64, io, json, struct, sys
import numpy as np
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
KEEP_JOINTS = ["Hips","Spine","Spine1","Spine2","Neck","Neck1","Neck2","Head",
    "LeftShoulder","LeftArm","LeftForeArm","LeftForeArm1","LeftForeArm2","LeftHand",
    "RightShoulder","RightArm","RightForeArm","RightForeArm1","RightForeArm2","RightHand",
    "LeftUpLeg","LeftLeg","LeftFoot","LeftToeBase","RightUpLeg","RightLeg","RightFoot","RightToeBase"]
KEEP_PARTS = ["AvatarBody","AvatarHead","AvatarLeftEyeball","AvatarRightEyeball","haircut",
              "outfit_top","outfit_bottom","outfit_shoes"]

b = open(SRC,"rb").read(); jl = struct.unpack("<I", b[12:16])[0]
J = json.loads(b[20:20+jl]); BIN = 20+jl+8
CT = {5120:"i1",5121:"u1",5122:"<i2",5123:"<u2",5125:"<u4",5126:"<f4"}; NC = {"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT4":16}
def acc(i):
    a = J["accessors"][i]; bv = J["bufferViews"][a["bufferView"]]; dt = np.dtype(CT[a["componentType"]]); n = NC[a["type"]]
    off = BIN + bv.get("byteOffset",0) + a.get("byteOffset",0); stride = bv.get("byteStride") or dt.itemsize*n
    if stride == dt.itemsize*n: arr = np.frombuffer(b, dt, a["count"]*n, off).reshape(a["count"], n)
    else: arr = np.stack([np.frombuffer(b, dt, n, off+k*stride) for k in range(a["count"])])
    arr = arr.astype(np.float64) if dt.kind == "f" else arr
    if a.get("normalized"): arr = arr / {1:255.0,2:65535.0}[dt.itemsize]
    return arr

# ---- skeleton at rest
N = J["nodes"]
def local(n):
    if "matrix" in n: return np.array(n["matrix"],float).reshape(4,4).T
    t = n.get("translation",[0,0,0]); x,y,z,w = n.get("rotation",[0,0,0,1]); s = n.get("scale",[1,1,1])
    R = np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
    M = np.eye(4); M[:3,:3] = R*np.array(s); M[:3,3] = t; return M
world = {}; parent = {}
def walk(i, P, par):
    world[i] = P @ local(N[i]); parent[i] = par
    for c in N[i].get("children",[]): walk(c, world[i], i)
for r in J["scenes"][J.get("scene",0)]["nodes"]: walk(r, np.eye(4), None)
skin = J["skins"][0]; joints = skin["joints"]; ibm = acc(skin["inverseBindMatrices"]).reshape(-1,4,4).transpose(0,2,1)
name_of = {j: N[j].get("name") for j in joints}
kept_nodes = [next(j for j in joints if name_of[j]==nm) for nm in KEEP_JOINTS]
def kept_ancestor(node):
    while node is not None and node not in kept_nodes: node = parent[node]
    return node
remap = np.array([kept_nodes.index(kept_ancestor(j)) for j in joints])
bones = []
for k, node in enumerate(kept_nodes):
    par = kept_ancestor(parent[node]); pk = kept_nodes.index(par) if par is not None else -1
    rel = world[node] if pk < 0 else np.linalg.inv(world[par]) @ world[node]
    bones.append({"name": KEEP_JOINTS[k], "parent": pk, "local": [round(float(v),6) for v in rel.T.flatten()],
                  "inv": [round(float(v),6) for v in ibm[joints.index(node)].T.flatten()]})

# ---- meshes
mats = J["materials"]; blobs = []; parts = []; textures = {}
def push(arr):
    off = sum(len(x) for x in blobs); pad = (-off) % 4
    if pad: blobs.append(b"\0"*pad); off += pad
    blobs.append(arr.tobytes()); return off
allpos = np.concatenate([acc(p["attributes"]["POSITION"]) for m in J["meshes"] for p in m["primitives"] if mats[p["material"]]["name"] in KEEP_PARTS])
lo, hi = allpos.min(0), allpos.max(0); span = (hi-lo).max()
tris = 0; light_parts = []; light_tris = 0
LIGHT_CELL = {"AvatarBody":.026,"AvatarHead":.011,"outfit_top":.022,"outfit_bottom":.022,"outfit_shoes":.016}
for m in J["meshes"]:
    for p in m["primitives"]:
        mat = mats[p["material"]]
        if mat["name"] not in KEEP_PARTS: continue
        pos = acc(p["attributes"]["POSITION"]); nor = acc(p["attributes"]["NORMAL"]); uv = acc(p["attributes"]["TEXCOORD_0"])
        jn = remap[acc(p["attributes"]["JOINTS_0"]).astype(int)]; wt = acc(p["attributes"]["WEIGHTS_0"]).astype(float)
        # merge weights that now point at the same bone, keep the four largest, make them sum to 255
        W = np.zeros((len(pos), len(KEEP_JOINTS)))
        for c in range(4): np.add.at(W, (np.arange(len(pos)), jn[:,c]), wt[:,c])
        top4 = np.argsort(-W, axis=1)[:, :4]; w4 = np.take_along_axis(W, top4, 1); w4 /= w4.sum(1, keepdims=True)
        wq = np.round(w4*255).astype(int); wq[:,0] += 255 - wq.sum(1)
        idx = acc(p["indices"]).astype(np.int64).flatten()
        def store(pos, nor, uv, j4, w4q, idx):
            uvlo, uvhi = uv.min(0), uv.max(0); uvspan = np.maximum(uvhi-uvlo, 1e-6)
            q = np.round((pos-lo)/span*65535).astype(np.uint16)
            nq = np.zeros((len(pos),4), np.int8); nq[:,:3] = np.round(nor/np.maximum(np.linalg.norm(nor,axis=1,keepdims=True),1e-9)*127)
            return {"name": mat["name"], "verts": len(pos), "count": len(idx), "alpha": mat.get("alphaMode","OPAQUE"),
                    "uvlo": uvlo.tolist(), "uvspan": uvspan.tolist(),
                    "pos": push(q), "nor": push(nq), "uv": push(np.round((uv-uvlo)/uvspan*65535).astype(np.uint16)),
                    "joints": push(j4.astype(np.uint8)), "weights": push(w4q.astype(np.uint8)), "idx": push(idx.astype(np.uint16))}
        part = store(pos, nor, uv, top4, wq, idx)
        # The light version, for people seen from further away: vertices that fall in the same
        # small cube (and the same patch of texture) are merged into one, and flattened triangles dropped.
        cell = LIGHT_CELL.get(mat["name"])
        if mat["name"] in ("haircut","AvatarLeftEyeball","AvatarRightEyeball"):
            light = None          # drawn as plain shapes, or not at all, from far away
        elif cell:
            key = np.concatenate([np.floor(pos/cell), np.floor(uv*24)], 1).astype(np.int64)
            _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
            ni = inv.flatten()[idx].reshape(-1,3)
            ni = ni[(ni[:,0]!=ni[:,1])&(ni[:,1]!=ni[:,2])&(ni[:,0]!=ni[:,2])]
            ni = np.unique(np.sort(ni,1), axis=0, return_index=True)[1]; 
            tri = inv.flatten()[idx].reshape(-1,3); tri = tri[(tri[:,0]!=tri[:,1])&(tri[:,1]!=tri[:,2])&(tri[:,0]!=tri[:,2])][np.sort(ni)]
            light = store(pos[first], nor[first], uv[first], top4[first], wq[first], tri.flatten())
        else:
            light = dict(part)
        if light: light_parts.append(light); light_tris += light["count"]//3
        tex = mat.get("pbrMetallicRoughness",{}).get("baseColorTexture")
        if tex is not None:
            src = J["textures"][tex["index"]]["source"]
            if src not in textures:
                bv = J["bufferViews"][J["images"][src]["bufferView"]]
                im = Image.open(io.BytesIO(b[BIN+bv.get("byteOffset",0):][:bv["byteLength"]]))
                im = im.resize((512,512), Image.LANCZOS) if im.width > 512 else im
                buf = io.BytesIO()
                if mat.get("alphaMode") and im.mode == "RGBA": im.save(buf, "WEBP", quality=80); mime = "image/webp"
                else: im.convert("RGB").save(buf, "JPEG", quality=82); mime = "image/jpeg"
                g = np.asarray(im.convert("RGBA"), float); a = g[...,3] > 40
                lum = (0.3*g[...,0]+0.59*g[...,1]+0.11*g[...,2])[a].mean()/255 if a.any() else 0.5
                textures[src] = {"url": f"data:{mime};base64,"+base64.b64encode(buf.getvalue()).decode(), "avg": round(float(lum),4), "bytes": buf.tell()}
            part["tex"] = list(textures).index(src)
        if light and "tex" in part: light["tex"] = part["tex"]
        parts.append(part); tris += len(idx)//3
data = b"".join(blobs)
out = {"lo": lo.tolist(), "span": float(span), "bones": bones, "parts": parts, "light": light_parts,
       "textures": [{"url": t["url"], "avg": t["avg"]} for t in textures.values()],
       "data": base64.b64encode(data).decode()}
json.dump(out, open(OUT,"w"), separators=(",",":"))
print("light version:", light_tris, "triangles", [(p["name"], p["count"]//3) for p in light_parts])
print("bones", len(bones), "| parts", [p["name"] for p in parts], "| triangles", tris, "| vertices", sum(p["verts"] for p in parts))
print("geometry %.2f MB, textures %.2f MB, packed file %.2f MB" % (len(data)/1e6, sum(t["bytes"] for t in textures.values())/1e6, len(json.dumps(out))/1e6))
