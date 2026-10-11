"""Turn a heavy .glb into a light model the game can draw: every part moved to its place, colour
taken from its texture at each point, then points merged on a 3-D grid until the triangle count
is near the target. Output: positions (16-bit), colours (8-bit) and triangles, as base64 in JSON."""
import sys,json,struct,base64,io
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
def load(fn):
    b=open(fn,'rb').read(); jl=struct.unpack('<I',b[12:16])[0]; j=json.loads(b[20:20+jl]); bin_=b[20+jl+8:]; return j,bin_
CT={5120:np.int8,5121:np.uint8,5122:np.int16,5123:np.uint16,5125:np.uint32,5126:np.float32}; NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def acc(j,bin_,i):
    a=j['accessors'][i]; bv=j['bufferViews'][a['bufferView']]; dt=np.dtype(CT[a['componentType']]); n=NC[a['type']]; off=bv.get('byteOffset',0)+a.get('byteOffset',0); stride=bv.get('byteStride',0)
    if stride and stride!=dt.itemsize*n:
        raw=np.frombuffer(bin_,dtype=np.uint8,count=stride*(a['count']-1)+dt.itemsize*n,offset=off); out=np.lib.stride_tricks.as_strided(raw,shape=(a['count'],dt.itemsize*n),strides=(stride,1)).copy().view(dt).reshape(a['count'],n)
    else: out=np.frombuffer(bin_,dtype=dt,count=a['count']*n,offset=off).reshape(a['count'],n)
    out=out.astype(np.float32) if dt!=np.uint32 and dt!=np.uint16 or a['type']!='SCALAR' else out
    if a.get('normalized'): out=out/np.iinfo(dt).max
    return out
def quat(q):
    x,y,z,w=q; return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def local(n):
    if 'matrix' in n: return np.array(n['matrix'],dtype=np.float64).reshape(4,4).T
    m=np.eye(4); m[:3,:3]=quat(n.get('rotation',[0,0,0,1]))@np.diag(n.get('scale',[1,1,1])); m[:3,3]=n.get('translation',[0,0,0]); return m
def gather(fn,skip=()):
    j,bin_=load(fn); imgs={}
    def image(i):
        if i not in imgs:
            im=j['images'][i]; bv=j['bufferViews'][im['bufferView']]; pic=Image.open(io.BytesIO(bin_[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB'); pic.thumbnail((2048,2048)); imgs[i]=np.asarray(pic)
        return imgs[i]
    P=[];C=[];I=[];base=0; names=[]
    def visit(i,M):
        nonlocal base
        n=j['nodes'][i]; W=M@local(n)
        if 'mesh' in n and not any(s in (n.get('name') or '') for s in skip):
            use=np.eye(4) if 'skin' in n else W          # a skinned mesh is placed by its skeleton, not by its own node
            if 'skin' in n:
                root=j['skins'][n['skin']]['joints'][0]; use=world[parent_of.get(root,root)] if parent_of.get(root) is not None else np.eye(4)
            for p in j['meshes'][n['mesh']]['primitives']:
                pos=acc(j,bin_,p['attributes']['POSITION']).astype(np.float64); pos=pos@use[:3,:3].T+use[:3,3]
                idx=acc(j,bin_,p['indices']).reshape(-1).astype(np.int64) if 'indices' in p else np.arange(len(pos))
                mat=j['materials'][p['material']] if 'material' in p else {}; pbr=mat.get('pbrMetallicRoughness',{}); f=np.array(pbr.get('baseColorFactor',[1,1,1,1])[:3])
                col=np.tile(np.clip(f**(1/2.2),0,1)*255,(len(pos),1))
                if 'baseColorTexture' in pbr and 'TEXCOORD_0' in p['attributes']:
                    tex=image(j['textures'][pbr['baseColorTexture']['index']]['source']); uv=acc(j,bin_,p['attributes']['TEXCOORD_0']); h,w=tex.shape[:2]
                    col=tex[np.clip(((uv[:,1]%1)*h).astype(int),0,h-1),np.clip(((uv[:,0]%1)*w).astype(int),0,w-1)].astype(np.float64)*f
                e=np.array(mat.get('emissiveFactor',[0,0,0]))
                if e.max()>.2: col=np.clip(col+e*255,0,255)
                if mat.get('alphaMode')=='BLEND' and pbr.get('baseColorFactor',[1,1,1,1])[3]<.6: col=col*.35+np.array([70,110,140])*.65        # glass
                P.append(pos);C.append(col);I.append(idx+base);base+=len(pos);names.append((n.get('name'),mat.get('name'),len(idx)//3))
        for c in n.get('children',[]): visit(c,W)
    # world matrices first (needed to place skinned meshes)
    world={};parent_of={}
    def pre(i,M,par):
        W=M@local(j['nodes'][i]); world[i]=W; parent_of[i]=par
        for c in j['nodes'][i].get('children',[]): pre(c,W,i)
    for r in j['scenes'][j.get('scene',0)]['nodes']: pre(r,np.eye(4),None)
    for r in j['scenes'][j.get('scene',0)]['nodes']: visit(r,np.eye(4))
    return np.vstack(P),np.vstack(C),np.concatenate(I).reshape(-1,3),names
def simplify(P,C,T,target):
    lo=P.min(0); span=(P.max(0)-lo).max(); best=None
    a,b=span/4000,span/20
    for _ in range(22):
        g=(a*b)**.5; cell=np.floor((P-lo)/g).astype(np.int64); key=cell[:,0]*4000003+cell[:,1]*2003+cell[:,2]
        uniq,inv=np.unique(key,return_inverse=True); t=inv[T]; ok=(t[:,0]!=t[:,1])&(t[:,1]!=t[:,2])&(t[:,0]!=t[:,2]); t=t[ok]
        ts=np.sort(t,1); _,first=np.unique(ts[:,0]*len(uniq)*len(uniq)+ts[:,1]*len(uniq)+ts[:,2],return_index=True); t=t[np.sort(first)]
        best=(g,uniq,inv,t)
        if abs(len(t)-target)<target*.04: break
        if len(t)>target: a=g
        else: b=g
    g,uniq,inv,t=best; n=len(uniq); cnt=np.bincount(inv,minlength=n)[:,None]
    NP=np.stack([np.bincount(inv,weights=P[:,k],minlength=n) for k in range(3)],1)/cnt; NC_=np.stack([np.bincount(inv,weights=C[:,k],minlength=n) for k in range(3)],1)/cnt
    used=np.unique(t); remap=-np.ones(n,dtype=np.int64); remap[used]=np.arange(len(used)); return NP[used],NC_[used],remap[t]
def pack(P,C,T,out,meta=None):
    lo=P.min(0); span=float((P.max(0)-lo).max()); q=np.round((P-lo)/span*65535).astype('<u2'); idx=T.astype('<u4' if len(P)>65535 else '<u2')
    d={'lo':[float(v) for v in lo],'span':span,'verts':len(P),'tris':len(T),'wide':len(P)>65535,'pos':base64.b64encode(q.tobytes()).decode(),'col':base64.b64encode(np.clip(C,0,255).astype(np.uint8).tobytes()).decode(),'idx':base64.b64encode(idx.tobytes()).decode()}
    if meta: d.update(meta)
    json.dump(d,open(out,'w')); return d
if __name__=='__main__':
    fn,out,target=sys.argv[1],sys.argv[2],int(sys.argv[3]); up=sys.argv[4] if len(sys.argv)>4 else 'y'
    P,C,T,names=gather(fn); print('read',len(P),'points',len(T),'triangles | size',np.round(P.max(0)-P.min(0),2))
    if len(T)>target*1.1: P,C,T=simplify(P,C,T,target)
    lo,hi=P.min(0),P.max(0); P=P-np.array([(lo[0]+hi[0])/2,lo[1],(lo[2]+hi[2])/2])          # stand it on the ground, centred
    d=pack(P,C,T,out); print('wrote',out,'|',d['verts'],'points',d['tris'],'triangles | size',np.round(P.max(0)-P.min(0),2),'|',round(len(json.dumps(d))/1e6,2),'MB')
