"""Turn a Character Creator style rigged .glb into the game's compact walking character: the same
packed format as the woman, with its bones renamed to the names the walk uses, small joints
(fingers, toes, face, twists) folded into their parents, meshes thinned, colour textures shrunk."""
import base64,io,json,struct,sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
SRC,OUT=sys.argv[1],sys.argv[2]; CELL=float(sys.argv[3]) if len(sys.argv)>3 else .012
MAP={"Hips":"CC_Base_Hip","Spine":"CC_Base_Waist","Spine1":"CC_Base_Spine01","Spine2":"CC_Base_Spine02","Neck":"CC_Base_NeckTwist01","Neck1":"CC_Base_NeckTwist02","Head":"CC_Base_Head",
 "LeftShoulder":"CC_Base_L_Clavicle","LeftArm":"CC_Base_L_Upperarm","LeftForeArm":"CC_Base_L_Forearm","LeftHand":"CC_Base_L_Hand","RightShoulder":"CC_Base_R_Clavicle","RightArm":"CC_Base_R_Upperarm","RightForeArm":"CC_Base_R_Forearm","RightHand":"CC_Base_R_Hand",
 "LeftUpLeg":"CC_Base_L_Thigh","LeftLeg":"CC_Base_L_Calf","LeftFoot":"CC_Base_L_Foot","LeftToeBase":"CC_Base_L_ToeBase","RightUpLeg":"CC_Base_R_Thigh","RightLeg":"CC_Base_R_Calf","RightFoot":"CC_Base_R_Foot","RightToeBase":"CC_Base_R_ToeBase"}
BIP={"Hips":"Bip01 Pelvis","Spine":"Bip01 Spine","Spine1":"Bip01 Spine1","Spine2":"Bip01 Spine2","Neck":"Bip01 Neck","Head":"Bip01 Head",
 "LeftShoulder":"Bip01 L Clavicle","LeftArm":"Bip01 L UpperArm","LeftForeArm":"Bip01 L Forearm","LeftHand":"Bip01 L Hand","RightShoulder":"Bip01 R Clavicle","RightArm":"Bip01 R UpperArm","RightForeArm":"Bip01 R Forearm","RightHand":"Bip01 R Hand",
 "LeftUpLeg":"Bip01 L Thigh","LeftLeg":"Bip01 L Calf","LeftFoot":"Bip01 L Foot","LeftToeBase":"Bip01 L Toe0","RightUpLeg":"Bip01 R Thigh","RightLeg":"Bip01 R Calf","RightFoot":"Bip01 R Foot","RightToeBase":"Bip01 R Toe0"}
SKIP=("tearline","occlusion","eyelash","tongue","teeth","cornea")
b=open(SRC,"rb").read(); jl=struct.unpack("<I",b[12:16])[0]; J=json.loads(b[20:20+jl]); BIN=20+jl+8
CT={5120:"i1",5121:"u1",5122:"<i2",5123:"<u2",5125:"<u4",5126:"<f4"}; NC={"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT4":16}
def acc(i):
    a=J["accessors"][i]; bv=J["bufferViews"][a["bufferView"]]; dt=np.dtype(CT[a["componentType"]]); n=NC[a["type"]]; off=BIN+bv.get("byteOffset",0)+a.get("byteOffset",0); stride=bv.get("byteStride") or dt.itemsize*n
    if stride==dt.itemsize*n: arr=np.frombuffer(b,dt,a["count"]*n,off).reshape(a["count"],n)
    else: arr=np.lib.stride_tricks.as_strided(np.frombuffer(b,np.uint8,stride*(a["count"]-1)+dt.itemsize*n,off),shape=(a["count"],dt.itemsize*n),strides=(stride,1)).copy().view(dt).reshape(a["count"],n)
    arr=arr.astype(np.float64) if dt.kind=="f" else arr
    if a.get("normalized"): arr=arr/{1:255.0,2:65535.0}[dt.itemsize]
    return arr
N=J["nodes"]
def local(n):
    if "matrix" in n: return np.array(n["matrix"],float).reshape(4,4).T
    t=n.get("translation",[0,0,0]); x,y,z,w=n.get("rotation",[0,0,0,1]); s=n.get("scale",[1,1,1])
    R=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]); M=np.eye(4); M[:3,:3]=R*np.array(s); M[:3,3]=t; return M
world={}; parent={}
def walk(i,P,par):
    world[i]=P@local(N[i]); parent[i]=par
    for c in N[i].get("children",[]): walk(c,world[i],i)
for r in J["scenes"][J.get("scene",0)]["nodes"]: walk(r,np.eye(4),None)
skin=J["skins"][0]; joints=skin["joints"]
if any((N[j].get("name") or "").startswith("Bip01") for j in joints): MAP=BIP          # the Rocketbox characters name their bones this way
skin=J["skins"][0]; ibm=acc(skin["inverseBindMatrices"]).reshape(-1,4,4).transpose(0,2,1); name_of={j:N[j].get("name") for j in joints}
KEEP=list(MAP); kept=[next(j for j in joints if name_of[j]==MAP[k]) for k in KEEP]
def kept_anc(node):
    while node is not None and node not in kept: node=parent[node]
    return node
remap=np.array([kept.index(kept_anc(j)) if kept_anc(j) is not None else 0 for j in joints])
# which way does he face, and how far do his arms hang below level, in his rest pose?
pos_of=lambda k:world[kept[KEEP.index(k)]][:3,3]
facing=np.sign((pos_of("LeftToeBase")-pos_of("LeftFoot"))[2]); turn=np.diag([-1,1,-1,1.]) if facing<0 else np.eye(4)
side=np.sign((turn[:3,:3]@pos_of("LeftArm"))[0])            # the game expects the left arm on +x
if side<0: print("note: left arm is on -x after facing forward")
a=pos_of("LeftForeArm")-pos_of("LeftArm"); drop=float(np.arctan2(-a[1],np.hypot(a[0],a[2])))
height=max(world[j][1,3] for j in joints)
bones=[]
for k,node in enumerate(kept):
    par=kept_anc(parent[node]); pk=kept.index(par) if par is not None else -1; rel=turn@world[node] if pk<0 else np.linalg.inv(world[par])@world[node]
    bones.append({"name":KEEP[k],"parent":pk,"local":[round(float(v),6) for v in rel.T.flatten()],"inv":[round(float(v),7) for v in ibm[joints.index(node)].T.flatten()]})
mats=J["materials"]; blobs=[]; parts=[]; textures={}
def push(arr):
    off=sum(len(x) for x in blobs); pad=(-off)%4
    if pad: blobs.append(b"\0"*pad); off+=pad
    blobs.append(arr.tobytes()); return off
prims=[(m,p) for m in J["meshes"] for p in m["primitives"] if "JOINTS_0" in p["attributes"] and not any(s in (mats[p["material"]]["name"]+m.get("name","")).lower() for s in SKIP)]
allpos=np.concatenate([acc(p["attributes"]["POSITION"]) for _,p in prims]); lo,hi=allpos.min(0),allpos.max(0); span=(hi-lo).max(); tris=0
for m,p in prims:
    mat=mats[p["material"]]; nm=mat["name"]; pos=acc(p["attributes"]["POSITION"]); nor=acc(p["attributes"]["NORMAL"]); uv=acc(p["attributes"]["TEXCOORD_0"])
    jn=remap[acc(p["attributes"]["JOINTS_0"]).astype(int)]; wt=acc(p["attributes"]["WEIGHTS_0"]).astype(float); idx=acc(p["indices"]).astype(np.int64).flatten()
    hair=nm.lower()=="hair"; cutout="opacity" in nm.lower(); hairy=hair or cutout or "haircap" in nm.lower(); cell=CELL*(.6 if any(s in nm.lower() for s in ("head","eye")) else 2.2 if hair else 1)
    key=(np.floor(pos/cell) if hair else np.concatenate([np.floor(pos/cell),np.floor(uv*40)],1)).astype(np.int64); _,first,inv=np.unique(key,axis=0,return_index=True,return_inverse=True); tri=inv.flatten()[idx].reshape(-1,3)
    tri=tri[(tri[:,0]!=tri[:,1])&(tri[:,1]!=tri[:,2])&(tri[:,0]!=tri[:,2])]; tri=tri[np.sort(np.unique(np.sort(tri,1),axis=0,return_index=True)[1])]
    if len(tri)==0: continue
    used=np.unique(tri); re=-np.ones(len(first),np.int64); re[used]=np.arange(len(used)); sel=first[used]; tri=re[tri]
    if len(used)>65535: print("too many points in",nm); continue
    pos,nor,uv,jn,wt=pos[sel],nor[sel],uv[sel],jn[sel],wt[sel]
    W=np.zeros((len(pos),len(KEEP)))
    for c in range(4): np.add.at(W,(np.arange(len(pos)),jn[:,c]),wt[:,c])
    top4=np.argsort(-W,axis=1)[:,:4]; w4=np.take_along_axis(W,top4,1); w4/=np.maximum(w4.sum(1,keepdims=True),1e-9); wq=np.round(w4*255).astype(int); wq[:,0]+=255-wq.sum(1)
    uvlo,uvhi=uv.min(0),uv.max(0); uvspan=np.maximum(uvhi-uvlo,1e-6); nq=np.zeros((len(pos),4),np.int8); nq[:,:3]=np.round(nor/np.maximum(np.linalg.norm(nor,axis=1,keepdims=True),1e-9)*127)
    part={"name":nm,"verts":len(pos),"count":int(tri.size),"alpha":"MASK" if ("haircap" in nm.lower() or cutout) else "OPAQUE","uvlo":uvlo.tolist(),"uvspan":uvspan.tolist(),"pos":push(np.round((pos-lo)/span*65535).astype(np.uint16)),"nor":push(nq),
          "uv":push(np.round((uv-uvlo)/uvspan*65535).astype(np.uint16)),"joints":push(top4.astype(np.uint8)),"weights":push(wq.astype(np.uint8)),"idx":push(tri.flatten().astype(np.uint16))}
    pbr=mat.get("pbrMetallicRoughness",{}); tex=pbr.get("baseColorTexture")
    if hairy and not hair and not cutout: part["flat"]=[.11,.08,.06]; part["alpha"]="OPAQUE"; tex=None          # the close-fitting layer of hair, in the same dark brown
    if hair and tex is not None:                      # hair becomes one solid shape
        bv=J["bufferViews"][J["images"][J["textures"][tex["index"]]["source"]]["bufferView"]]; g=np.asarray(Image.open(io.BytesIO(b[BIN+bv.get("byteOffset",0):][:bv["byteLength"]])).convert("RGBA").resize((64,64)),float); a_=g[...,3]>60
        part["flat"]=[.13,.095,.07]; tex=None          # dark brown: the file's hair texture is grey and takes its colour from a setting that does not travel with it
    if tex is not None:
        src=J["textures"][tex["index"]]["source"]
        if src not in textures:
            bv=J["bufferViews"][J["images"][src]["bufferView"]]; im=Image.open(io.BytesIO(b[BIN+bv.get("byteOffset",0):][:bv["byteLength"]])); size=1024 if MAP is BIP else 768 if "head" in nm.lower() else 512
            if im.width>size: im=im.resize((size,size),Image.LANCZOS)
            buf=io.BytesIO()
            if hairy and im.mode=="RGBA": im.save(buf,"WEBP",quality=80); mime="image/webp"
            else: im.convert("RGB").save(buf,"JPEG",quality=84); mime="image/jpeg"
            g=np.asarray(im.convert("RGBA"),float); a_=g[...,3]>40; lum=(0.3*g[...,0]+0.59*g[...,1]+0.11*g[...,2])[a_].mean()/255 if a_.any() else .5
            textures[src]={"url":f"data:{mime};base64,"+base64.b64encode(buf.getvalue()).decode(),"avg":round(float(lum),4),"bytes":buf.tell()}
        part["tex"]=list(textures).index(src)
    elif "flat" not in part: part["flat"]=[round(float(v)**(1/2.2),3) for v in pbr.get("baseColorFactor",[.5,.5,.5,1])[:3]]
    parts.append(part); tris+=tri.shape[0]
data=b"".join(blobs)
out={"lo":lo.tolist(),"span":float(span),"armDrop":round(drop,4),"height":round(float(height),3),"bones":bones,"parts":parts,"textures":[{"url":t["url"],"avg":t["avg"]} for t in textures.values()],"data":base64.b64encode(data).decode()}
json.dump(out,open(OUT,"w"),separators=(",",":"))
print("faces",'+z' if facing>0 else '-z (turned round)',"| arms hang %.0f degrees below level"%np.degrees(drop),"| height %.2f m"%height)
print("bones",len(bones),"| triangles",tris,"| parts",[(p["name"],p["count"]//3,p["alpha"][:2]) for p in parts])
print("geometry %.2f MB, textures %.2f MB, packed %.2f MB"%(len(data)/1e6,sum(t["bytes"] for t in textures.values())/1e6,len(json.dumps(out))/1e6))
