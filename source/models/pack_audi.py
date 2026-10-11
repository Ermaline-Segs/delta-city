"""The car file arrives as half a car with every material white: its mirror was not applied on
export and its paints did not come through. Rebuild it: mirror the half parts, drop the stray
planes, and colour each part by the name of its material."""
import sys,json,numpy as np
sys.argv=[sys.argv[0]]+sys.argv[1:]
from pack_static import load,acc,local,pack
PAINT=sys.argv[2] if len(sys.argv)>2 else "#c1121f"
hexc=lambda h:[int(h[i:i+2],16) for i in (1,3,5)]
def colour(name):
    n=(name or '').lower()
    for key,c in (('paint',hexc(PAINT)),('glass',[28,40,52]),('tyyre',[22,22,24]),('rubber',[24,24,26]),('kauçuk',[26,26,28]),('black',[18,18,20]),('karbon',[34,36,40]),('steel',[188,194,200]),('aliminyum',[176,182,188]),('led',[230,30,30]),('light',[255,250,235]),('wire',[40,42,46])):
        if key in n: return c
    return [70,74,80]
j,bin_=load('/mnt/user-data/uploads/Audi_R8.glb'); P=[];C=[];I=[];base=0
for i in j['scenes'][0]['nodes']:
    n=j['nodes'][i]; name=n.get('name') or ''
    if name in ('Plane.007','Plane.011','Plane.012'): continue                       # stray flat planes: a backdrop and two lamps
    W=local(n)
    for p in j['meshes'][n['mesh']]['primitives']:
        pos=acc(j,bin_,p['attributes']['POSITION']).astype(np.float64)@W[:3,:3].T+W[:3,3]; idx=acc(j,bin_,p['indices']).reshape(-1,3).astype(np.int64)
        col=np.tile(colour(j['materials'][p['material']]['name'] if 'material' in p else ''),(len(pos),1)).astype(np.float64)
        P.append(pos);C.append(col);I.append(idx+base);base+=len(pos)
        if pos[:,0].min()>-.06 and pos[:,0].max()>.2:                                   # a half part: add its mirror image
            m=pos*np.array([-1,1,1]); P.append(m);C.append(col);I.append(idx[:,::-1]+base);base+=len(pos)
P=np.vstack(P);C=np.vstack(C);T=np.vstack(I); lo,hi=P.min(0),P.max(0); print('rebuilt size',np.round(hi-lo,2),'triangles',len(T))
P=(P-np.array([(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2]))*(4.43/(hi[2]-lo[2]))             # a real R8 is 4.43 m long
d=pack(P,C,T,sys.argv[1]); print('wrote',d['verts'],'points',d['tris'],'triangles | size',np.round(P.max(0)-P.min(0),2))
