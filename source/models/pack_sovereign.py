"""The Sovereign GT (assets/vehicles/sovereign_gt.glb) as the game's car model.

Every part (the body, both doors, the steering wheel and the four wheels) is moved to its place and joined into one
model, as the game draws a car as one piece and bends it for damage. Each point takes its colour from its texture, and
the parts the damage system needs to recognise are given its colours:
  paint   the red body                         R>150, G<70   (shiny)
  glass   windows                              R<40,  B>44   (they crack and fall out)
  lamps   headlights white, tail lights red    R>220         (they glow and break)
The game's car faces +Z with +X on its left; the file faces -Z with +X on its right, so it is turned half round.
Run: python3 pack_sovereign.py ../../assets/vehicles/sovereign_gt.glb sovereign.json"""
import sys,io,json,numpy as np
from PIL import Image
from pack_static import load,acc,local,pack
PAINT=np.array([193,18,31.])
src,out=sys.argv[1],sys.argv[2]
j,bin_=load(src);imgs={}
def image(i):
    if i not in imgs:
        im=j['images'][i];bv=j['bufferViews'][im['bufferView']]
        pic=Image.open(io.BytesIO(bin_[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB');pic.thumbnail((1024,1024));imgs[i]=np.asarray(pic)
    return imgs[i]
P=[];C=[];M=[];I=[];base=0
def visit(i,W0):
    global base
    n=j['nodes'][i];W=W0@local(n)
    if 'mesh' in n:
        for p in j['meshes'][n['mesh']]['primitives']:
            pos=acc(j,bin_,p['attributes']['POSITION']).astype(np.float64)@W[:3,:3].T+W[:3,3]
            idx=acc(j,bin_,p['indices']).reshape(-1).astype(np.int64)
            mat=j['materials'][p['material']] if 'material' in p else {};pbr=mat.get('pbrMetallicRoughness',{});f=np.array(pbr.get('baseColorFactor',[1,1,1,1])[:3])
            col=np.tile(np.clip(f**(1/2.2),0,1)*255,(len(pos),1))
            if 'baseColorTexture' in pbr and 'TEXCOORD_0' in p['attributes']:
                tex=image(j['textures'][pbr['baseColorTexture']['index']]['source']);uv=acc(j,bin_,p['attributes']['TEXCOORD_0']);h,w=tex.shape[:2]
                col=tex[np.clip(((uv[:,1]%1)*h).astype(int),0,h-1),np.clip(((uv[:,0]%1)*w).astype(int),0,w-1)].astype(np.float64)*f
            P.append(pos);C.append(col);M.append(np.full(len(pos),mat.get('name') or '',dtype=object));I.append(idx+base);base+=len(pos)
    for c in n.get('children',[]):visit(c,W)
for r in j['scenes'][j.get('scene',0)]['nodes']:visit(r,np.eye(4))
P=np.vstack(P);C=np.vstack(C);M=np.concatenate(M);T=np.concatenate(I).reshape(-1,3)
P=P*np.array([-1,1,-1])                                   # half a turn: front to +Z, left to +X
lo,hi=P.min(0),P.max(0);P=P-np.array([(lo[0]+hi[0])/2,0,(lo[2]+hi[2])/2])
L=(hi[2]-lo[2])/2
glass=np.array([m.startswith('Glass') for m in M]);red=np.array([m.startswith('Glass_-_Red') for m in M])
# the paint: the body's red points become one clean red, with a little of the texture's shading
paint=(M=='car-body')&(C[:,0]>C[:,1]*1.8)&(C[:,0]>60)
C[paint]=np.clip(PAINT*(.85+.15*C[paint,0:1]/255),0,255)
# lamps: red glass is the tail lights; clear glass low at the very front is the headlights
tail=red;head=glass&~red&(P[:,2]>L-.75)&(P[:,1]<.95)
C[tail]=[255,36,30];C[head]=[255,250,235]
# windows: every other glass, dark blue-grey
win=glass&~tail&~head;C[win]=[26,38,58]
# nothing else may pass for paint, glass or a lamp by accident
other=~(paint|tail|head|win);c=C[other]
c[:,0]=np.where(c[:,0]>215,215,c[:,0]);c[:,0]=np.where((c[:,0]>150)&(c[:,1]<70),150,c[:,0]);dark=(c[:,0]<40)&(c[:,2]>44);c[dark,2]=44;C[other]=c
print('points',len(P),'triangles',len(T),'size',np.round(P.max(0)-P.min(0),3),'| paint',paint.sum(),'head',head.sum(),'tail',tail.sum(),'windows',win.sum())
d=pack(P,C,T,out);print('wrote',out,round(len(json.dumps(d))/1e6,2),'MB')
