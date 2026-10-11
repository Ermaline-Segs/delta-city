"""Add the female actor's recordings to the game's clips. Each becomes a seamless loop, stored in
the same skeleton-free form as the others."""
import json,base64,numpy as np
exec(open('rpm.py').read().split('if __name__=="__main__":')[0])
base=json.load(open('anims.json')); k=KEEP.index; U='/mnt/user-data/uploads/'
def qmul(a,b): return np.array([a[3]*b[0]+a[0]*b[3]+a[1]*b[2]-a[2]*b[1],a[3]*b[1]-a[0]*b[2]+a[1]*b[3]+a[2]*b[0],a[3]*b[2]+a[0]*b[1]-a[1]*b[0]+a[2]*b[3],a[3]*b[3]-a[0]*b[0]-a[1]*b[1]-a[2]*b[2]])
def qbetween(a,b):
    d=float(np.dot(a,b)); c=np.cross(a,b); q=np.array([c[0],c[1],c[2],1+d]); return q/np.linalg.norm(q)
def convert(c):
    F=len(c["R"]); Q=np.zeros((F,len(KEEP),4)); P0=c["P0"]; hip=P0[k("Hips")][1]
    for b,name in enumerate(KEEP):
        K=np.array([0,0,0,1.])
        if name in base["child"] and any(name.endswith(s) for s in ("Arm","ForeArm","UpLeg","Leg")):       # this pack rests slightly differently from the first: carry the difference
            d=P0[k(base["child"][name])]-P0[b]; K=qbetween(np.array(base["restDir"][name]),d/np.linalg.norm(d))
        for f in range(F):
            q=qmul(matq(c["R"][f,b]@c["R0"][b].T),K)
            if f and np.dot(q,Q[f-1,b])<0: q=-q
            Q[f,b]=q
    return Q,(c["P"][:,k("Hips")]-P0[k("Hips")])/hip
def nl(a,b,w):
    b=np.where((a*b).sum(-1,keepdims=True)<0,-b,b); q=a+(b-a)*w; return q/np.linalg.norm(q,axis=-1,keepdims=True)
def loop_cycle(Q,H,f0,f1,kf):          # one cycle f0..f1; its last frames lean towards the frames that led into f0, so the end meets the start
    q=Q[f0:f1].copy(); h=H[f0:f1].copy(); n=f1-f0
    for i in range(kf):
        w=(i+1)/(kf+1); j=n-kf+i; src=f0-kf+i
        if src>=2: q[j]=nl(q[j],Q[src],w); h[j]=h[j]+(H[src]-h[j])*w*np.array([0,1,0])
        else: q[j]=nl(q[j],Q[f0],w*.6)
    return q,h
def loop_idle(Q,H,f0,kf):
    q=Q[f0:].copy(); h=H[f0:].copy(); n=len(q)-kf; out=q[:n].copy(); oh=h[:n].copy()
    for j in range(kf): w=j/kf; out[j]=nl(q[n+j],q[j],w); oh[j]=h[n+j]+(h[j]-h[n+j])*w
    return out,oh
leg_r=None; made={}
def put(name,q,h,speed=0.0):
    made[name]={"frames":len(q),"dur":round(len(q)/30,4),"speed":round(float(speed),4),"q":base64.b64encode(np.round(q*32767).astype("<i2").tobytes()).decode(),"h":base64.b64encode(np.round(np.clip(h,-1,1)*32767).astype("<i2").tobytes()).decode()}
    print(" %-9s %3d frames, %.2f s%s"%(name,len(q),len(q)/30,", %.2f m/s on her own legs"%(speed*leg_r/base["leg"]) if speed else ""))
c=read(U+"F_Walk_002.glb"); P0=c["P0"]; leg_r=float(np.linalg.norm(P0[k("LeftUpLeg")]-P0[k("LeftLeg")])+np.linalg.norm(P0[k("LeftLeg")]-P0[k("LeftFoot")])); norm=base["leg"]/leg_r
Q,H=convert(c); z=c["P"][:,k("Hips"),2]; q,h=loop_cycle(Q,H,51,83,6); put("f_walk",q,h,(z[83]-z[51])/(32/30)*norm)
c=read(U+"F_Jog_001.glb"); Q,H=convert(c); z=c["P"][:,k("Hips"),2]; q,h=loop_cycle(Q,H,3,24,3); put("f_jog",q,h,(z[24]-z[3])/(21/30)*norm)
c=read(U+"F_Walk_Backwards_001.glb"); Q,H=convert(c); z=c["P"][:,k("Hips"),2]; q,h=loop_cycle(Q,H,29,57,6); put("f_back",q,h,abs(z[57]-z[29])/(28/30)*norm)
for nm,src,cut in (("f_idle","F_Standing_Idle_001",None),("f_idle2","F_Standing_Idle_Variations_002",None),("f_idle3","F_Standing_Idle_Variations_005",None),("f_talk","F_Talking_Variations_001",None),("f_talk2","F_Talking_Variations_005",None)):
    c=read(U+src+".glb"); Q,H=convert(c); q,h=loop_idle(Q,H,2,24); put(nm,q,h)
base["clips"].update(made); json.dump(base,open("anims.json","w"),separators=(",",":")); print("anims.json is now %.0f KB with %d clips"%(len(open('anims.json').read())/1024,len(base["clips"])))
