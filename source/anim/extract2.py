"""Take recorded movements out of the animation pack and store them in a form that does not depend
on the pack's own skeleton: for every frame and every main bone, how far that bone has turned
(in world space) from the pack's rest pose, plus how the hips move. The game then applies those
turns to any character whose bones carry the standard names."""
import json,struct,base64,sys
import numpy as np
SRC="../anim2/ual2/Universal Animation Library 2[Standard]/Unreal-Godot/UAL2_Standard.glb"; RM=SRC.replace(".glb","_RM.glb")
MAP={"Hips":"pelvis","Spine":"spine_01","Spine1":"spine_02","Spine2":"spine_03","Neck":"neck_01","Head":"Head","LeftShoulder":"clavicle_l","LeftArm":"upperarm_l","LeftForeArm":"lowerarm_l","LeftHand":"hand_l",
     "RightShoulder":"clavicle_r","RightArm":"upperarm_r","RightForeArm":"lowerarm_r","RightHand":"hand_r","LeftUpLeg":"thigh_l","LeftLeg":"calf_l","LeftFoot":"foot_l","LeftToeBase":"ball_l","RightUpLeg":"thigh_r","RightLeg":"calf_r","RightFoot":"foot_r","RightToeBase":"ball_r"}
CHILD={"Hips":"Spine","Spine":"Spine1","Spine1":"Spine2","Spine2":"Neck","Neck":"Head","LeftShoulder":"LeftArm","LeftArm":"LeftForeArm","LeftForeArm":"LeftHand","RightShoulder":"RightArm","RightArm":"RightForeArm","RightForeArm":"RightHand",
       "LeftUpLeg":"LeftLeg","LeftLeg":"LeftFoot","LeftFoot":"LeftToeBase","RightUpLeg":"RightLeg","RightLeg":"RightFoot","RightFoot":"RightToeBase"}
WANT={"Idle_FoldArms_Loop":"foldarms","Idle_TalkingPhone_Loop":"phone","Idle_No_Loop":"no","Yes":"yes","Idle_Rail_Loop":"rail"}
CT={5120:"i1",5121:"u1",5122:"<i2",5123:"<u2",5125:"<u4",5126:"<f4"}; NC={"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT4":16}
def load(fn):
    b=open(fn,"rb").read(); jl=struct.unpack("<I",b[12:16])[0]; return json.loads(b[20:20+jl]),b,20+jl+8
def acc(J,b,BIN,i):
    a=J["accessors"][i]; bv=J["bufferViews"][a["bufferView"]]; dt=np.dtype(CT[a["componentType"]]); n=NC[a["type"]]; return np.frombuffer(b,dt,a["count"]*n,BIN+bv.get("byteOffset",0)+a.get("byteOffset",0)).reshape(a["count"],n).astype(np.float64)
def qmat(q):
    x,y,z,w=q; return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def matq(m):
    t=np.trace(m)
    if t>0: s=np.sqrt(t+1)*2; q=[(m[2,1]-m[1,2])/s,(m[0,2]-m[2,0])/s,(m[1,0]-m[0,1])/s,.25*s]
    else:
        i=int(np.argmax(np.diag(m))); j,k=(i+1)%3,(i+2)%3; s=np.sqrt(1+m[i,i]-m[j,j]-m[k,k])*2; q=[0,0,0,0]; q[i]=.25*s; q[j]=(m[j,i]+m[i,j])/s; q[k]=(m[k,i]+m[i,k])/s; q[3]=(m[k,j]-m[j,k])/s
    q=np.array(q); return q/np.linalg.norm(q)
def slerp_sample(times,vals,t,rot):
    i=np.searchsorted(times,t,side="right")-1; i=max(0,min(len(times)-2,i)); u=0 if times[i+1]==times[i] else np.clip((t-times[i])/(times[i+1]-times[i]),0,1); a,b_=vals[i],vals[i+1]
    if rot:
        if np.dot(a,b_)<0: b_=-b_
        q=a+(b_-a)*u; return q/np.linalg.norm(q)
    return a+(b_-a)*u
def poses(J,b,BIN,anim,fps=30):
    N=J["nodes"]; par={}
    for i,n in enumerate(N):
        for c in n.get("children",[]): par[c]=i
    order=[]; 
    def visit(i):
        order.append(i)
        for c in N[i].get("children",[]): visit(c)
    for r in J["scenes"][0]["nodes"]: visit(r)
    base={i:(np.array(n.get("translation",[0,0,0]),float),np.array(n.get("rotation",[0,0,0,1]),float),np.array(n.get("scale",[1,1,1]),float)) for i,n in enumerate(N)}
    ch={}
    if anim is not None:
        for c in anim["channels"]:
            s=anim["samplers"][c["sampler"]]; ch[(c["target"]["node"],c["target"]["path"])]=(acc(J,b,BIN,s["input"]).reshape(-1),acc(J,b,BIN,s["output"]))
        dur=max(v[0][-1] for v in ch.values()); frames=max(2,int(round(dur*fps)))
    else: dur=0; frames=1
    out=[]
    for f in range(frames):
        t=dur*f/frames; W={}
        for i in order:
            T,R,S=base[i]
            if (i,"translation") in ch: T=slerp_sample(*ch[(i,"translation")],t,False)
            if (i,"rotation") in ch: R=slerp_sample(*ch[(i,"rotation")],t,True)
            if (i,"scale") in ch: S=slerp_sample(*ch[(i,"scale")],t,False)
            m=np.eye(4); m[:3,:3]=qmat(R)*S; m[:3,3]=T; W[i]=W[par[i]]@m if i in par else m
        out.append(W)
    return out,dur
J,b,BIN=load(SRC); name2node={n.get("name"):i for i,n in enumerate(J["nodes"])}; KEEP=list(MAP); idx=[name2node[MAP[k]] for k in KEEP]
rest,_=poses(J,b,BIN,None); R0=rest[0]; rot=lambda W,i:(lambda m:m/np.linalg.norm(m,axis=0))(W[i][:3,:3]); pos=lambda W,k:W[idx[KEEP.index(k)]][:3,3]
fwd=np.sign((pos(R0,"LeftToeBase")-pos(R0,"LeftFoot"))[2]); left=np.sign(pos(R0,"LeftArm")[0]); print("pack faces",'+z' if fwd>0 else '-z',"| its left arm is on",'+x' if left>0 else '-x',"| hip height %.3f"%pos(R0,"Hips")[1],"| leg %.3f"%(np.linalg.norm(pos(R0,"LeftUpLeg")-pos(R0,"LeftLeg"))+np.linalg.norm(pos(R0,"LeftLeg")-pos(R0,"LeftFoot"))))
assert fwd>0 and left>0,"the pack faces another way: turn it first"
restDir={k:[round(float(v),5) for v in (lambda d:d/np.linalg.norm(d))(pos(R0,CHILD[k])-pos(R0,k))] for k in CHILD}
hip=float(pos(R0,"Hips")[1]); leg=float(np.linalg.norm(pos(R0,"LeftUpLeg")-pos(R0,"LeftLeg"))+np.linalg.norm(pos(R0,"LeftLeg")-pos(R0,"LeftFoot")))
JR,bR,BINR=load(RM); rmnode={n.get("name"):i for i,n in enumerate(JR["nodes"])}
clips={}
for a in J["animations"]:
    if a["name"] not in WANT: continue
    P,dur=poses(J,b,BIN,a); F=len(P); Q=np.zeros((F,len(KEEP),4)); H=np.zeros((F,3))
    for f,W in enumerate(P):
        for k,i in enumerate(idx):
            q=matq(rot(W,i)@rot(R0,i).T)
            if f and np.dot(q,Q[f-1,k])<0: q=-q
            Q[f,k]=q
        H[f]=(pos(W,"Hips")-pos(R0,"Hips"))/hip
    speed=0.0
    ar=next(x for x in JR["animations"] if x["name"]==a["name"]); PR,_=poses(JR,bR,BINR,ar); root=rmnode["root"]; d=PR[-1][root][:3,3]-PR[0][root][:3,3]; speed=float(np.hypot(d[0],d[2])/dur*len(PR)/(len(PR)-1)) if dur else 0
    clips[WANT[a["name"]]]={"frames":F,"dur":round(dur,4),"speed":round(speed,4),"q":base64.b64encode(np.round(Q*32767).astype("<i2").tobytes()).decode(),"h":base64.b64encode(np.round(np.clip(H,-1,1)*32767).astype("<i2").tobytes()).decode()}
    print(" %-8s %3d frames, %.2f s, moves at %.2f of its units a second, hips move %.3f up and down"%(WANT[a["name"]],F,dur,speed,(H[:,1].max()-H[:,1].min())*hip))
base=json.load(open("anims.json")); assert abs(base["hip"]-hip)<1e-3 and base["restDir"]["LeftArm"]==restDir["LeftArm"],"the two packs rest differently"; base["clips"].update(clips); json.dump(base,open("anims.json","w"),separators=(",",":")); print("added to anims.json, now %.0f KB with"%(len(open("anims.json").read())/1024),sorted(base["clips"]))
