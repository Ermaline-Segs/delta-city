"""Any vehicle in assets/vehicles/ as a game model with moving parts.

The model is packed with every part in its place, colours from the textures, and the whole turned half round so
the front is +Z and the left is +X; but its triangles are kept in order part by part, and the file says where each
part's triangles are, so the game can draw a door, a wheel or the steering wheel on its own and move it:
  parts   {"body":[first,last], "door_FL":[...], "wheel_FL":[...], "steering_wheel":[...], ...}  (triangle numbers)
  rig     doors: hinge (or slide) point, opening direction and the most it opens; wheels: centre and radius;
          the steering wheel: centre and the axis it spins on; seats: the hip points from vehicles.md
All points are in the game's car space: metres, on the ground under the middle of the car, +X left, +Z front.
Colour rules (only for vehicles listed in STYLE; others keep their own colours, with glass made dark):
  paint  R>150, G<70 (shiny)   glass  R<40, B>44 (see-through, cracks)   lamps  R>220 (glow, break)
Run: python3 pack_vehicle.py ../../assets/vehicles/sovereign_gt.glb sovereign.json"""
import sys,io,re,os,json,numpy as np
from PIL import Image
from pack_static import load,acc,local,quat,pack
src,out=sys.argv[1],sys.argv[2];name=os.path.basename(src)
STYLE={'sovereign_gt.glb':dict(paint='car-body',colour=[193,18,31],glass='Glass',red='Glass_-_Red',head=(.75,.95))}
st=STYLE.get(name)
j,bin_=load(src);imgs={}
def image(i):
    if i not in imgs:
        im=j['images'][i];bv=j['bufferViews'][im['bufferView']]
        pic=Image.open(io.BytesIO(bin_[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB');pic.thumbnail((1024,1024));imgs[i]=np.asarray(pic)
    return imgs[i]
P=[];C=[];M=[];I=[];G=[];base=0;nodes={}
def visit(i,W0,part):
    global base
    n=j['nodes'][i];W=W0@local(n);nm=n.get('name') or ''
    if re.match(r'(door_|wheel_|steering_wheel)',nm):part=nm;nodes[nm]=n
    if 'mesh' in n:
        for p in j['meshes'][n['mesh']]['primitives']:
            pos=acc(j,bin_,p['attributes']['POSITION']).astype(np.float64)@W[:3,:3].T+W[:3,3]
            idx=acc(j,bin_,p['indices']).reshape(-1).astype(np.int64) if 'indices' in p else np.arange(len(pos))
            mat=j['materials'][p['material']] if 'material' in p else {};pbr=mat.get('pbrMetallicRoughness',{});f=np.array(pbr.get('baseColorFactor',[1,1,1,1])[:3])
            col=np.tile(np.clip(f**(1/2.2),0,1)*255,(len(pos),1))
            if 'baseColorTexture' in pbr and 'TEXCOORD_0' in p['attributes']:
                tex=image(j['textures'][pbr['baseColorTexture']['index']]['source']);uv=acc(j,bin_,p['attributes']['TEXCOORD_0']);h,w=tex.shape[:2]
                col=tex[np.clip(((uv[:,1]%1)*h).astype(int),0,h-1),np.clip(((uv[:,0]%1)*w).astype(int),0,w-1)].astype(np.float64)*f
            P.append(pos);C.append(col);M.append(np.full(len(pos),mat.get('name') or '',dtype=object));I.append(idx+base);G.append(np.full(len(idx)//3,part,dtype=object));base+=len(pos)
    for c in n.get('children',[]):visit(c,W,part)
for r in j['scenes'][j.get('scene',0)]['nodes']:visit(r,np.eye(4),'body')
P=np.vstack(P);C=np.vstack(C);M=np.concatenate(M);T=np.concatenate(I).reshape(-1,3);G=np.concatenate(G)
FLIP=np.array([-1,1,-1])
P=P*FLIP                                                  # half a turn: front to +Z, left to +X
lo,hi=P.min(0),P.max(0);mid=np.array([(lo[0]+hi[0])/2,0,(lo[2]+hi[2])/2]);P=P-mid
L=(hi[2]-lo[2])/2
g=lambda v:[round(float(x),3) for x in np.array(v)*FLIP-mid]          # a point from the file into the game's car space
glass=np.array(['glass' in m.lower() or 'window' in m.lower() for m in M])
if st:
    red=np.array([m.startswith(st['red']) for m in M])
    paint=(M==st['paint'])&(C[:,0]>C[:,1]*1.8)&(C[:,0]>60);C[paint]=np.clip(np.array(st['colour'],float)*(.85+.15*C[paint,0:1]/255),0,255)
    tail=red;head=glass&~red&(P[:,2]>L-st['head'][0])&(P[:,1]<st['head'][1]);C[tail]=[255,36,30];C[head]=[255,250,235]
else:paint=tail=head=np.zeros(len(P),bool)
win=glass&~tail&~head;C[win]=[26,38,58]
other=~(paint|tail|head|win);c=C[other]                   # nothing else may pass for paint, glass or a lamp by accident
c[:,0]=np.where(c[:,0]>215,215,c[:,0]);c[:,0]=np.where((c[:,0]>150)&(c[:,1]<70),150,c[:,0]);dark=(c[:,0]<40)&(c[:,2]>44);c[dark,2]=44;C[other]=c
# triangles part by part, the body first
names=['body']+sorted(set(G)-{'body'});order=np.concatenate([np.where(G==n)[0] for n in names]);T=T[order];G=G[order]
parts={};k=0
for n in names:m=int((G==n).sum());parts[n]=[k,k+m];k+=m
# the rig
doors={};wheels={};steer=None
for nm,n in nodes.items():
    t=n.get('translation',[0,0,0]);tri=T[parts[nm][0]:parts[nm][1]];pts=P[np.unique(tri)] if len(tri) else np.zeros((1,3))
    if nm.startswith('door_'):
        side=nm[5:]
        if side.startswith('P'):                          # the bus's sliding passenger doors
            v={'door_P1':[.07,0,1.49],'door_P2':[.07,0,1.32]}[nm];doors[side]={'at':g(t),'slide':[round(float(x),3) for x in np.array(v)*FLIP]}
        else:
            left=side.endswith('L');big=name=='brt_bus.glb'
            doors[side]={'at':g(t),'open':round(float(np.radians(80 if big else 70))*(-1 if left else 1),3)}
    elif nm.startswith('wheel_'):wheels[nm[6:]]={'at':g(t),'r':round(float((pts[:,1].max()-pts[:,1].min())/2),3)}
    else:
        R=quat(n.get('rotation',[0,0,0,1]));ax=R@np.array([0,0,1.])*FLIP
        steer={'at':g(t),'axis':[round(float(x),4) for x in ax]}
# seats: the hip points from vehicles.md (this vehicle's own seat table, else the driver's from the table of drivers)
seats={};md=open(os.path.join(os.path.dirname(src),'vehicles.md')).read()
sec=re.search(r'\n## [^\n]*`'+re.escape(name)+r'`[^\n]*\n(.*?)(?=\n## |\Z)',md,re.S)
num=r'`\[\s*(-?[\d.]+),\s*(-?[\d.]+),\s*(-?[\d.]+)\s*\]`'
if sec:
    for m in re.finditer(r'\|\s*([^|`\n]+?)\s*\|\s*'+num,sec.group(1)):
        k_=m.group(1).strip().lower()
        if k_ in ('seat',) or k_.startswith('door') or k_.startswith('wheel') or k_.startswith('steer'):continue
        seats[k_]=g([float(m.group(i)) for i in (2,3,4)])
if 'driver' not in seats:
    m=re.search(r'\|\s*`'+re.escape(name)+r'`\s*\|[^|]*\|\s*left\s*\|\s*'+num+r'\s*\|\s*'+num,md)
    if m:seats['driver']=g([float(m.group(i)) for i in (4,5,6)])
rig={'doors':doors,'wheels':wheels,'steer':steer,'seats':seats,'size':[round(float(x),3) for x in hi-lo]}
print(name,'points',len(P),'triangles',len(T),'| parts',{n:v[1]-v[0] for n,v in parts.items()})
print(json.dumps(rig))
d=pack(P,C,T,out,{'parts':parts,'rig':rig});print('wrote',out,round(len(json.dumps(d))/1e6,2),'MB')
