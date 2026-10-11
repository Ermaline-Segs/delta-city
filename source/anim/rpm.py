"""Read the Ready Player Me recordings (female actor). The files were exported with a padded
length, so first find where the real movement ends. Then report, for each, how long it really is,
whether the body travels, and where its walking cycles fall."""
import json,struct,sys,glob,os
import numpy as np
exec(open('extract.py').read().split("J,b,BIN=load(SRC)")[0])          # helpers: load, acc, qmat, matq, poses
MAP={k:k for k in MAP}                                                    # these files already use the standard bone names
KEEP=list(MAP)
def read(fn,fps=30):
    J,b,BIN=load(fn); n2={n.get("name"):i for i,n in enumerate(J["nodes"])}; idx=[n2[k] for k in KEEP]
    rest,_=poses(J,b,BIN,None); R0=rest[0]; P,dur=poses(J,b,BIN,J["animations"][0],fps)
    rot=lambda W,i:(lambda m:m/np.linalg.norm(m,axis=0))(W[i][:3,:3])
    Rw=np.array([[rot(W,i) for i in idx] for W in P]); Pw=np.array([[W[i][:3,3] for i in idx] for W in P]); R0r=np.array([rot(R0,i) for i in idx]); P0=np.array([R0[i][:3,3] for i in idx])
    # where does the real movement end? after it, every frame is identical
    diff=np.abs(Rw-Rw[-1]).reshape(len(Rw),-1).max(1)+np.abs(Pw-Pw[-1]).reshape(len(Pw),-1).max(1); moving=np.where(diff>1e-5)[0]; end=int(moving[-1])+2 if len(moving) else len(Rw)
    return dict(R=Rw[:end],P=Pw[:end],R0=R0r,P0=P0,fps=fps,name=os.path.basename(fn)[:-4])
if __name__=="__main__":
    k=KEEP.index
    for fn in sorted(glob.glob('/mnt/user-data/uploads/F_*.glb')+['/mnt/user-data/uploads/Feminine_TPose.glb']):
        c=read(fn); F=len(c["R"]); hips=c["P"][:,k("Hips")]; trav=hips[-1]-hips[0]; s=(c["P"][:,k("LeftFoot"),2]-c["P"][:,k("RightFoot"),2]); up=np.where((s[:-1]<=0)&(s[1:]>0))[0]
        print("%-34s real length %5.2f s (%3d frames) | hips travel x %+.2f z %+.2f | height %.2f..%.2f | left-foot-forward crossings at %s"%(c["name"],F/30,F,trav[0],trav[2],hips[:,1].min(),hips[:,1].max(),list(up[:8])))
    c=read('/mnt/user-data/uploads/Feminine_TPose.glb'); P0=c["P0"]
    print("rest pose: faces",'+z' if (P0[k("LeftToeBase")]-P0[k("LeftFoot")])[2]>0 else '-z',"| left arm on",'+x' if P0[k("LeftArm")][0]>0 else '-x',"| hip height %.3f"%P0[k("Hips")][1],"| arm direction",np.round((P0[k("LeftForeArm")]-P0[k("LeftArm")])/np.linalg.norm(P0[k("LeftForeArm")]-P0[k("LeftArm")]),2),"| leg %.3f"%(np.linalg.norm(P0[k("LeftUpLeg")]-P0[k("LeftLeg")])+np.linalg.norm(P0[k("LeftLeg")]-P0[k("LeftFoot")])))
