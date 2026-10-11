/* ============================ people who walk ============================
   The player's own character, drawn with its skeleton moved on the graphics chip. The walk and
   run are the same measured gait as in the walking test; it works on any character whose bones
   carry the standard names, so the woman and Henry share it. */
const WALKER=(()=>{
const D=Math.PI/180;let WOMAN=null;
const SKINP=program(`attribute vec3 p,n;attribute vec2 uv;attribute vec4 j,w,paint;uniform vec4 B[84];uniform mat4 vp,model;uniform vec3 lo;uniform float span;uniform vec2 uvlo,uvspan;varying vec3 vn;varying vec2 vu;varying vec4 vpaint;
vec3 bone(float i,vec4 v){int k=int(i)*3;return vec3(dot(B[k],v),dot(B[k+1],v),dot(B[k+2],v));}
void main(){vec4 v=vec4(lo+p*span,1.),d=vec4(n,0.);vec3 q=w.x*bone(j.x,v)+w.y*bone(j.y,v)+w.z*bone(j.z,v)+w.w*bone(j.w,v),m=w.x*bone(j.x,d)+w.y*bone(j.y,d)+w.z*bone(j.z,d)+w.w*bone(j.w,d);
  vn=normalize((model*vec4(m,0.)).xyz);vu=uvlo+uv*uvspan;vpaint=paint;gl_Position=vp*model*vec4(q,1.);}`,`precision mediump float;varying vec3 vn;varying vec2 vu;varying vec4 vpaint;uniform sampler2D t;uniform vec3 tint,plain;uniform float cut,useTint,avg,useFlat;
void main(){vec4 c=texture2D(t,vu);if(useFlat>.5)c=vec4(plain,1.);if(c.a<cut)discard;if(useTint>.5){float l=dot(c.rgb,vec3(.3,.59,.11))/max(avg,.02);c.rgb=tint*clamp(l,.5,1.45);}c.rgb=mix(c.rgb,vpaint.rgb,smoothstep(.35,.65,vpaint.a));
  vec3 n=normalize(vn);float d=dot(n,normalize(vec3(.42,.86,.5)));vec3 sh=mix(vec3(.5,.52,.6),vec3(.66,.72,.84),.5+.5*n.y);gl_FragColor=vec4(c.rgb*(sh+vec3(1.,.96,.86)*max(d,0.)*.62),1.);}`);
const BLOC=gl.getUniformLocation(SKINP.p,"B");
const mk=(d,t)=>{const b=gl.createBuffer();gl.bindBuffer(t||gl.ARRAY_BUFFER,b);gl.bufferData(t||gl.ARRAY_BUFFER,d,gl.STATIC_DRAW);return b};
async function load(id,clips){const src=JSON.parse(document.getElementById(id).textContent),raw=atob(src.data),bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
  const images=await Promise.all(src.textures.map(t=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>ok(im);im.onerror=()=>no(new Error("picture"));im.src=t.url})));
  const tex=images.map(im=>{const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);const pot=v=>(v&(v-1))===0;if(pot(im.width)&&pot(im.height)){gl.generateMipmap(gl.TEXTURE_2D);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR)}else{gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE)}return t});
  const parts=src.parts.map(p=>({name:p.name,verts:p.verts,count:p.count,cut:p.alpha==="OPAQUE"?0:.35,uvlo:p.uvlo,uvspan:p.uvspan,tex:p.tex===undefined?null:tex[p.tex],avg:p.tex===undefined?.5:src.textures[p.tex].avg,flat:p.flat,
    pos:new Uint16Array(bytes.buffer,p.pos,p.verts*3),p:mk(new Uint16Array(bytes.buffer,p.pos,p.verts*3)),n:mk(new Int8Array(bytes.buffer,p.nor,p.verts*4)),uv:mk(new Uint16Array(bytes.buffer,p.uv,p.verts*2)),j:mk(new Uint8Array(bytes.buffer,p.joints,p.verts*4)),w:mk(new Uint8Array(bytes.buffer,p.weights,p.verts*4)),i:mk(new Uint16Array(bytes.buffer,p.idx,p.count),gl.ELEMENT_ARRAY_BUFFER),paints:{}}));
  const bones=src.bones.map(b=>({name:b.name,parent:b.parent,local:new Float32Array(b.local),inv:new Float32Array(b.inv)})),index={};bones.forEach((b,i)=>index[b.name]=i);
  const m={lo:src.lo,span:src.span,parts,bones,index,armDrop:src.armDrop||0,clips:Object.assign({idle:"idle",walk:"walk",jog:"jog"},clips||{})};WOMAN=m;measureLegs();m.LEG=LEG;m.speed={walk:gaitSpeed(0),run:gaitSpeed(1)};if(ANIM)prepare(m);return m}
function use(m){WOMAN=m;LEG=m.LEG}
/* ---- recorded movement ----
   The clips hold, for every frame and every main bone, how far that bone has turned in the world
   from the recording's rest pose. To put a clip on a character: first line the two rest poses up
   (a character may rest with arms level or arms lowered), then give each bone its recorded turn,
   and place each joint where its parent's turn carries it. */
let ANIM=null;
const qmul=(a,b)=>[a[3]*b[0]+a[0]*b[3]+a[1]*b[2]-a[2]*b[1],a[3]*b[1]-a[0]*b[2]+a[1]*b[3]+a[2]*b[0],a[3]*b[2]+a[0]*b[1]-a[1]*b[0]+a[2]*b[3],a[3]*b[3]-a[0]*b[0]-a[1]*b[1]-a[2]*b[2]];
const qrot=(q,v)=>{const x=q[0],y=q[1],z=q[2],w=q[3],tx=2*(y*v[2]-z*v[1]),ty=2*(z*v[0]-x*v[2]),tz=2*(x*v[1]-y*v[0]);return[v[0]+w*tx+y*tz-z*ty,v[1]+w*ty+z*tx-x*tz,v[2]+w*tz+x*ty-y*tx]};
const qbetween=(a,b)=>{const d=a[0]*b[0]+a[1]*b[1]+a[2]*b[2];if(d>.99999)return[0,0,0,1];if(d<-.99999)return[1,0,0,0];const c=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],q=[c[0],c[1],c[2],1+d],l=Math.hypot(...q);return q.map(v=>v/l)};
function init(){const d=JSON.parse(document.getElementById("anims").textContent),b64=s=>{const r=atob(s),u=new Uint8Array(r.length);for(let i=0;i<r.length;i++)u[i]=r.charCodeAt(i);return new Int16Array(u.buffer)};
  ANIM={bones:d.bones,child:d.child,restDir:d.restDir,hip:d.hip,leg:d.leg,clips:{}};for(const[k,c]of Object.entries(d.clips))ANIM.clips[k]={frames:c.frames,dur:c.dur,speed:c.speed,q:b64(c.q),h:b64(c.h)}}
// what one character needs to follow the clips: its own rest pose, and the turn that lines each bone up with the recording's
function prepare(m){use(m);poseBones({});const n=m.bones.length;m.rest=[];for(let i=0;i<n;i++)m.rest.push(new Float32Array(W[i]));const P=i=>[m.rest[i][12],m.rest[i][13],m.rest[i][14]],I=m.index,len=(a,b)=>Math.hypot(P(a)[0]-P(b)[0],P(a)[1]-P(b)[1],P(a)[2]-P(b)[2]);
  m.amap=m.bones.map(b=>ANIM.bones.indexOf(b.name));
  m.cinv=m.bones.map((b,i)=>{const c=ANIM.child[b.name];if(!c||I[c]===undefined||!/(Arm|ForeArm|UpLeg|Leg)$/.test(b.name))return[0,0,0,1];      // line up the limbs only: both skeletons already stand upright, and their spine joints sit in different places
    const a=P(i),e=P(I[c]),l=len(i,I[c]);return qbetween([(e[0]-a[0])/l,(e[1]-a[1])/l,(e[2]-a[2])/l],ANIM.restDir[b.name])});
  for(const s of["Left","Right"]){if(I[s+"Hand"]!==undefined)m.cinv[I[s+"Hand"]]=m.cinv[I[s+"ForeArm"]];for(const f of["Foot","ToeBase"])if(I[s+f]!==undefined)m.cinv[I[s+f]]=m.cinv[I[s+"Leg"]]}      // a hand follows its forearm's line-up and a foot its shin's, so a character that rests with lowered arms keeps natural wrists
  m.hipH=P(I.Hips)[1];m.legLen=len(I.LeftUpLeg,I.LeftLeg)+len(I.LeftLeg,I.LeftFoot);m.footY=P(I.LeftFoot)[1];m.toeY=P(I.LeftToeBase)[1];const k=m.legLen/ANIM.leg;
  const cw=ANIM.clips[m.clips.walk],cj=ANIM.clips[m.clips.jog];m.speed={walk:cw.speed*k,run:Math.min(cj.speed*k,4.8)};m.jogRate=m.speed.run/(cj.speed*k)}
const QB=new Float32Array(32*4),HB=[0,0,0];
// mix the clips for this moment into one turn for each recorded bone
function mixClips(list){QB.fill(0);HB[0]=HB[1]=HB[2]=0;const nb=ANIM.bones.length;for(const[clip,ph,wgt]of list){if(wgt<=.001)continue;const c=ANIM.clips[clip],f=((ph%1)+1)%1*c.frames,f0=Math.floor(f)%c.frames,f1=(f0+1)%c.frames,u=f-Math.floor(f);
    for(let k=0;k<nb;k++){const a=(f0*nb+k)*4,b=(f1*nb+k)*4;let x=c.q[a]+(c.q[b]-c.q[a])*u,y=c.q[a+1]+(c.q[b+1]-c.q[a+1])*u,z=c.q[a+2]+(c.q[b+2]-c.q[a+2])*u,w=c.q[a+3]+(c.q[b+3]-c.q[a+3])*u;const o=k*4,s=(QB[o]*x+QB[o+1]*y+QB[o+2]*z+QB[o+3]*w<0?-1:1)*wgt/32767;QB[o]+=x*s;QB[o+1]+=y*s;QB[o+2]+=z*s;QB[o+3]+=w*s}
    for(let k=0;k<3;k++)HB[k]+=(c.h[f0*3+k]+(c.h[f1*3+k]-c.h[f0*3+k])*u)/32767*wgt}
  for(let k=0;k<nb;k++){const o=k*4,l=Math.hypot(QB[o],QB[o+1],QB[o+2],QB[o+3])||1;QB[o]/=l;QB[o+1]/=l;QB[o+2]/=l;QB[o+3]/=l}}
const DQ=[];
// move this character's bones to the mixed pose; returns how far to lift the body so the lower foot rests on the ground
// place every bone from its turn in DQ. On foot the hips only rise and fall: the game itself moves the body forward.
function solve(m,grounded,sway){const B=m.bones;for(let i=0;i<B.length;i++){const par=B[i].parent,r=m.rest[i],w=W[i];if(m.amap[i]<0)DQ[i]=par>=0?DQ[par]:[0,0,0,1];const d=DQ[i];
    for(let c=0;c<12;c+=4){const v=qrot(d,[r[c],r[c+1],r[c+2]]);w[c]=v[0];w[c+1]=v[1];w[c+2]=v[2];w[c+3]=0}
    if(par<0){const side=grounded?0:1;w[12]=r[12]+HB[0]*m.hipH*side+(sway||0);w[13]=r[13]+HB[1]*m.hipH;w[14]=r[14]+HB[2]*m.hipH*side}
    else{const pr=m.rest[par],v=qrot(DQ[par],[r[12]-pr[12],r[13]-pr[13],r[14]-pr[14]]),pw=W[par];w[12]=pw[12]+v[0];w[13]=pw[13]+v[1];w[14]=pw[14]+v[2]}
    w[15]=1;const iv=B[i].inv,o=i*12;for(let rr=0;rr<3;rr++){BONES[o+rr*4]=w[rr]*iv[0]+w[4+rr]*iv[1]+w[8+rr]*iv[2]+w[12+rr]*iv[3];BONES[o+rr*4+1]=w[rr]*iv[4]+w[4+rr]*iv[5]+w[8+rr]*iv[6]+w[12+rr]*iv[7];BONES[o+rr*4+2]=w[rr]*iv[8]+w[4+rr]*iv[9]+w[8+rr]*iv[10]+w[12+rr]*iv[11];BONES[o+rr*4+3]=w[rr]*iv[12]+w[4+rr]*iv[13]+w[8+rr]*iv[14]+w[12+rr]*iv[15]}}}
/* A more feminine walk, laid over the recorded one. Read from the pose itself which foot is ahead
   and which is off the ground, then: let the hip drop on the side of the lifted foot and turn
   with the leading leg; sway the body over the standing foot; bring the legs in so each foot lands
   near the middle line; turn the chest gently against the hips; keep the arms closer to the body
   with a soft bend at the elbow. `fem` is how strongly to apply it, 0 to 1. */
function feminine(m,fem){const I=m.index,L=W[I.LeftFoot],R=W[I.RightFoot],ahead=clamp((L[14]-R[14])/(m.legLen*.5),-1,1),lifted=clamp((R[13]-L[13])/(m.legLen*.12),-1,1),k=Math.PI/180*fem;
  const qx=a=>[Math.sin(a/2),0,0,Math.cos(a/2)],qy=a=>[0,Math.sin(a/2),0,Math.cos(a/2)],qz=a=>[0,0,Math.sin(a/2),Math.cos(a/2)],add=(name,q)=>{const i=I[name];if(i!==undefined)DQ[i]=qmul(q,DQ[i])};
  add("Hips",qmul(qz(7.5*k*lifted),qy(-10*k*ahead)));
  for(const[s,side]of[["Left",-1],["Right",1]]){add(s+"UpLeg",qz(side*5.5*k));add(s+"Leg",qz(side*5.5*k));add(s+"Foot",qy(side*-4*k));add(s+"Arm",qz(side*7*k));add(s+"ForeArm",qmul(qz(side*5*k),qx(-8*k)));add(s+"Hand",qmul(qz(side*-8*k),qx(-10*k)))}
  add("Spine",qy(3*k*ahead));add("Spine1",qy(6*k*ahead));add("Spine2",qmul(qy(7*k*ahead),qx(-2.5*k)));add("Neck",qx(-2*k));return .024*lifted*fem}
/* A more feminine way of standing, laid over the recorded idle. Her weight rests on one leg: that
   hip rises and pushes out to the side, the other knee relaxes and bends with the foot turned out
   a little; the shoulders tilt the opposite way to the hips; the feet stand closer together; the
   arms rest close to the body with a soft bend. Every so often she shifts her weight to the other
   leg. `w` is how strongly to apply it, 0 to 1. */
function feminineStand(m,w,t){const I=m.index,sd=clamp(Math.sin(t*.36)*3.2,-1,1),a=Math.abs(sd),k=Math.PI/180*w,
    qx=q=>[Math.sin(q/2),0,0,Math.cos(q/2)],qy=q=>[0,Math.sin(q/2),0,Math.cos(q/2)],qz=q=>[0,0,Math.sin(q/2),Math.cos(q/2)],add=(name,q)=>{const i=I[name];if(i!==undefined)DQ[i]=qmul(q,DQ[i])};
  const stand=sd>=0?"Left":"Right",ease=sd>=0?"Right":"Left",ss=sd>=0?-1:1;                         // ss: which way "inwards" is for the standing leg
  add("Hips",qmul(qz(7*k*sd),qy(-5*k*sd)));
  add(stand+"UpLeg",qz(ss*4.5*k*a));add(stand+"Leg",qz(ss*2*k*a));
  add(ease+"UpLeg",qmul(qz(-ss*6.5*k*a),qx(-11*k*a)));add(ease+"Leg",qmul(qz(-ss*5*k*a),qx(13*k*a)));add(ease+"Foot",qmul(qy(ss*16*k*a),qx(9*k*a)));add(ease+"ToeBase",qy(ss*16*k*a));
  add("Spine",qmul(qz(-2*k*sd),qx(-3.5*k)));add("Spine1",qmul(qz(-4*k*sd),qx(-3.5*k)));add("Spine2",qmul(qz(-4.5*k*sd),qx(-3.5*k)));add("Neck",qmul(qz(2.5*k*sd),qx(3*k)));add("Head",qmul(qmul(qz(3*k*sd),qy(4*k*sd)),qx(5*k)));       // and she stands tall, not leaning forward
  for(const[s,side]of[["Left",-1],["Right",1]]){add(s+"Arm",qz(side*7*k));add(s+"ForeArm",qmul(qz(side*6*k),qx(-9*k)));add(s+"Hand",qmul(qz(side*-9*k),qx(-8*k)))}
  return .034*sd*w}
// move this character's bones to the mixed pose; returns how far to lift the body so the lower foot rests on the ground
function poseClips(m,list,grounded,fem,stand,t){mixClips(list);const B=m.bones;for(let i=0;i<B.length;i++){const k=m.amap[i];if(k>=0)DQ[i]=qmul([QB[k*4],QB[k*4+1],QB[k*4+2],QB[k*4+3]],m.cinv[i])}
  if(m.armIn){const I=m.index,h=m.armIn*Math.PI/360,s=Math.sin(h),c=Math.cos(h);for(const[n,sg]of[["Left",-1],["Right",1]])for(const part of["Arm","ForeArm","Hand"]){const i=I[n+part];if(i!==undefined)DQ[i]=qmul([0,0,sg*s,c],DQ[i])}}      // her arms hang a little closer to her body than the actor's did on a wider frame
  solve(m,grounded,0);if(fem>.01||stand>.01){let sway=0;if(fem>.01)sway+=feminine(m,fem);if(stand>.01)sway+=feminineStand(m,stand,t||0);solve(m,grounded,sway)}
  if(!grounded)return 0;const I=m.index;return Math.max(0,-Math.min(W[I.LeftFoot][13]-m.footY,W[I.RightFoot][13]-m.footY,W[I.LeftToeBase][13]-m.toeY,W[I.RightToeBase][13]-m.toeY))}      // never below the ground; in a run both feet may be off it
/* Work out where every bone is for one moment of standing or walking.
   `turns` maps a bone name to rotations about the character's own axes
   (x = side to side, y = up, z = front to back), applied at that joint. */
const W=[],BONES=new Float32Array(84*4);for(let i=0;i<28;i++)W.push(new Float32Array(16));
function mulInto(o,a,b){for(let c=0;c<4;c++){const b0=b[c*4],b1=b[c*4+1],b2=b[c*4+2],b3=b[c*4+3];o[c*4]=a[0]*b0+a[4]*b1+a[8]*b2+a[12]*b3;o[c*4+1]=a[1]*b0+a[5]*b1+a[9]*b2+a[13]*b3;o[c*4+2]=a[2]*b0+a[6]*b1+a[10]*b2+a[14]*b3;o[c*4+3]=a[3]*b0+a[7]*b1+a[11]*b2+a[15]*b3}}
function poseBones(turns){
  const B=WOMAN.bones;
  for(let i=0;i<B.length;i++){const w=W[i];if(B[i].parent<0)w.set(B[i].local);else mulInto(w,W[B[i].parent],B[i].local);
    const t=turns[B[i].name];
    if(t)for(let k=0;k<t.length;k+=2){const ax=t[k],c=Math.cos(t[k+1]),sn=Math.sin(t[k+1]);      // turn about the joint itself: only its three directions change
      for(let col=0;col<12;col+=4){const x=w[col],y=w[col+1],z=w[col+2];
        if(ax==="x"){w[col+1]=y*c-z*sn;w[col+2]=y*sn+z*c}else if(ax==="y"){w[col]=x*c+z*sn;w[col+2]=-x*sn+z*c}else{w[col]=x*c-y*sn;w[col+1]=x*sn+y*c}}}
    const v=B[i].inv,o=i*12;
    for(let r=0;r<3;r++){BONES[o+r*4]=w[r]*v[0]+w[4+r]*v[1]+w[8+r]*v[2]+w[12+r]*v[3];BONES[o+r*4+1]=w[r]*v[4]+w[4+r]*v[5]+w[8+r]*v[6]+w[12+r]*v[7];
      BONES[o+r*4+2]=w[r]*v[8]+w[4+r]*v[9]+w[8+r]*v[10]+w[12+r]*v[11];BONES[o+r*4+3]=w[r]*v[12]+w[4+r]*v[13]+w[8+r]*v[14]+w[12+r]*v[15]}}
}
/* ------------------------------------------------------------------------------
   Walking and running, from measured human gait.
   One full cycle runs from a heel landing to the same heel landing again.
   Walking: the foot is on the ground for the first 60% and swinging for 40%.
   Running: on the ground for about 35%, with moments when neither foot touches.
   Each row is [percent of the cycle, degrees]. Hip: + is thigh forward.
   Knee: + is bent. Ankle: + is toes up, - is toes down.
   ------------------------------------------------------------------------------ */
const GAIT={
  walk:{period:1.06,stanceEnd:.6,lean:3,hop:0,arm:{mid:-7,swing:17,elbow:16,bend:11,wrist:8},
    hip:  [[0,28],[10,24],[30,3],[50,-11],[60,-2],[73,14],[87,28],[100,28]],
    knee: [[0,4],[15,16],[40,4],[50,9],[60,38],[73,61],[87,27],[100,4]],
    ankle:[[0,0],[10,-6],[30,5],[47,10],[60,-19],[73,-5],[87,0],[100,0]]},
  run:{period:.71,stanceEnd:.36,lean:9,hop:.055,arm:{mid:-18,swing:30,elbow:84,bend:10,wrist:4},
    hip:  [[0,28],[18,8],[36,-15],[50,8],[70,46],[85,55],[100,28]],
    knee: [[0,20],[17,42],[36,18],[46,55],[60,98],[72,84],[88,36],[100,20]],
    ankle:[[0,4],[16,19],[36,-24],[55,-6],[80,4],[100,4]]}
};
// a smooth repeating curve through the rows above
function curve(keys){const k=keys.slice(0,-1),n=k.length;return p=>{p=((p%1)+1)%1*100;let i=n-1;for(let q=0;q<n;q++)if(k[q][0]<=p)i=q;
  const at=j=>k[((j%n)+n)%n],x0=at(i)[0],x1=i+1<n?at(i+1)[0]:100,u=(p-x0)/(x1-x0||1);
  const p0=at(i-1)[1],p1=at(i)[1],p2=at(i+1)[1],p3=at(i+2)[1];
  return .5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u)}}
for(const g of Object.values(GAIT)){g.fHip=curve(g.hip);g.fKnee=curve(g.knee);g.fAnkle=curve(g.ankle)}
let LEG=null;                                // her own leg measurements, read from her skeleton
function measureLegs(){poseBones({});const I=WOMAN.index,y=i=>W[i][13],z=i=>W[i][14],d=(i,j)=>Math.hypot(W[i][12]-W[j][12],W[i][13]-W[j][13],W[i][14]-W[j][14]);
  LEG={thigh:d(I.LeftUpLeg,I.LeftLeg),shin:d(I.LeftLeg,I.LeftFoot),ankle:y(I.LeftFoot),hip:y(I.LeftUpLeg),toe:Math.max(.1,z(I.LeftToeBase)-z(I.LeftFoot))}}
// the three leg angles (radians) for one leg at one moment; run: 0 walking .. 1 running; amt: 0 standing .. 1 moving
function legAngles(p,run,amt){const w=GAIT.walk,r=GAIT.run,mix=(a,b)=>(a+(b-a)*run)*amt*D;
  return{hip:mix(w.fHip(p),r.fHip(p)),knee:mix(w.fKnee(p),r.fKnee(p)),ankle:mix(w.fAnkle(p),r.fAnkle(p))}}
// where that leg's ankle and sole end up, measured from the hip joint (z forward, y up)
function legReach(a){const shin=a.hip-a.knee,az=LEG.thigh*Math.sin(a.hip)+LEG.shin*Math.sin(shin),ay=-(LEG.thigh*Math.cos(a.hip)+LEG.shin*Math.cos(shin));
  const tilt=shin+a.ankle,pt=(fz,fy)=>ay+fy*Math.cos(tilt)+fz*Math.sin(tilt);
  return{z:az,low:Math.min(pt(-.05,-LEG.ankle),pt(LEG.toe,-LEG.ankle*.55))}}
/* Everything about the body at one moment: the bone turns, how far the hips must
   drop or rise to keep a foot on the ground, and how far forward each ankle is. */
function gaitPose(p,run,amt,t){
  const L=legAngles(p,run,amt),R=legAngles(p+.5,run,amt),rl=legReach(L),rr=legReach(R);
  const w=GAIT.walk,r=GAIT.run,mx=(a,b)=>a+(b-a)*run,tw=Math.cos(p*2*Math.PI),br=Math.sin(t*1.6)*.012;
  /* Arms. Measured walking: the shoulder swings through about 27 degrees and the elbow through
     about 15 to 30, once per cycle, opposite to the leg on the same side. The arm is furthest
     forward as the opposite heel lands; the elbow and wrist follow a little later, which is what
     makes a real arm look loose and not like a stick. */
  const A=k=>mx(w.arm[k],r.arm[k]),TAU=2*Math.PI,sway=Math.sin(t*1.1)*.02*(1-amt);
  const arm=q=>{const a=TAU*(q-.53);return{sh:(A("mid")+A("swing")*Math.cos(a))*D*amt+sway,
    el:((A("elbow")+A("bend")*Math.cos(a-.65))*amt+11*(1-amt))*D,wr:A("wrist")*Math.sin(a-.9)*D*amt,in:2.5*Math.cos(a)*D*amt,girdle:.05*Math.cos(a)*amt}};
  const aL=arm(p),aR=arm(p+.5);
  const stance=mx(w.stanceEnd,r.stanceEnd),pp=((p%1)+1)%1,air=(pp>stance&&pp<.5)?(pp-stance)/(.5-stance):(pp>.5+stance)?(pp-.5-stance)/(.5-stance):-1;
  const hop=air>=0?4*mx(w.hop,r.hop)*air*(1-air)*amt:0;
  return{
    rise:-(LEG.hip+Math.min(rl.low,rr.low))+hop, zL:rl.z, zR:rr.z, onLeft:pp<.5, inAir:air>=0&&run>.5,
    turns:{
      Hips:["y",-tw*.075*amt,"z",Math.sin(p*2*Math.PI)*.03*amt],
      Spine:["x",mx(w.lean,r.lean)*D*amt],Spine1:["y",tw*.14*amt,"x",br],Spine2:["x",br],Neck:["y",-tw*.065*amt,"x",-mx(1,4)*D*amt],
      LeftShoulder:["y",-aL.girdle],RightShoulder:["y",aR.girdle],
      LeftArm:["z",-(84*D-WOMAN.armDrop)-aL.in,"x",-aL.sh],RightArm:["z",(84*D-WOMAN.armDrop)+aR.in,"x",-aR.sh],
      LeftForeArm:["x",-aL.el],RightForeArm:["x",-aR.el],LeftHand:["z",.12,"x",aL.wr],RightHand:["z",-.12,"x",aR.wr],
      LeftUpLeg:["x",-L.hip],RightUpLeg:["x",-R.hip],LeftLeg:["x",L.knee],RightLeg:["x",R.knee],
      LeftFoot:["x",-L.ankle],RightFoot:["x",-R.ankle]}};
}
// average speed of each gait, found by walking one whole cycle on the spot
function gaitSpeed(run){let dist=0,prev=null;for(let i=0;i<=200;i++){const g=gaitPose(i/200,run,1,0),z=g.onLeft?g.zL:g.zR;if(prev&&prev.left===g.onLeft)dist+=Math.max(0,prev.z-z);prev={z,left:g.onLeft}}
  const T=GAIT.walk.period+(GAIT.run.period-GAIT.walk.period)*run;return dist/T/(run>.5?GAIT.run.stanceEnd*2:1)}
// colour painted on to the body for an outfit (the woman's tops and leggings)
function paintFor(m,part,look,key){if(part.paints[key]!==undefined)return part.paints[key];let buf=null;if(part.name==="AvatarBody"&&look&&look.paint){const C=new Uint8Array(part.verts*4);for(let k=0;k<part.verts;k++){const r=look.paint(m.lo[0]+part.pos[k*3]/65535*m.span,m.lo[1]+part.pos[k*3+1]/65535*m.span);if(r){const h=hex(r[0]);C[k*4]=h[0];C[k*4+1]=h[1];C[k*4+2]=h[2];C[k*4+3]=r[1]*255}}buf=mk(C)}return part.paints[key]=buf}
// draw one person. state: {p: place in the walk cycle, run: 0..1, amt: 0 standing .. 1 moving}. Returns the pose, for hair fixed to the head.
function draw(m,VP,x,y,z,yaw,state,t,look,lookKey){use(m);let lift;if(ANIM&&m.rest){const a=state.amt,r=state.run;lift=state.sit?poseClips(m,[["drive",t/ANIM.clips.drive.dur,1]],false,0):poseClips(m,[[state.idle||m.clips.idle,t/ANIM.clips[state.idle||m.clips.idle].dur,1-a],[state.walk||(state.back&&m.clips.back)||m.clips.walk,state.p,a*(1-r)],[m.clips.jog,state.p,a*r]],true,m.fem?(state.fem===undefined?m.fem:state.fem)*a*(1-.55*r):0,0,t)}
  else{const g=gaitPose(state.p,state.run,state.amt,t);poseBones(g.turns);lift=g.rise}const model=mul(trans(x,y+lift,z),rotY(yaw+Math.PI)),P=SKINP;
  gl.enable(gl.CULL_FACE);gl.useProgram(P.p);gl.uniformMatrix4fv(P.u.vp,false,VP);gl.uniformMatrix4fv(P.u.model,false,model);gl.uniform4fv(BLOC,BONES);gl.uniform3fv(P.u.lo,m.lo);gl.uniform1f(P.u.span,m.span);
  const A=(loc,buf,size,type,norm,stride)=>{gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,size,type,norm,stride||0,0)};
  for(const part of m.parts){A(P.a.p,part.p,3,gl.UNSIGNED_SHORT,true);A(P.a.n,part.n,3,gl.BYTE,true,4);A(P.a.uv,part.uv,2,gl.UNSIGNED_SHORT,true);A(P.a.j,part.j,4,gl.UNSIGNED_BYTE,false);A(P.a.w,part.w,4,gl.UNSIGNED_BYTE,true);
    const paint=paintFor(m,part,look,lookKey||"");if(paint)A(P.a.paint,paint,4,gl.UNSIGNED_BYTE,true);else{gl.disableVertexAttribArray(P.a.paint);gl.vertexAttrib4f(P.a.paint,0,0,0,0)}
    const tint=look?(part.name==="outfit_top"?look.top:part.name==="outfit_bottom"?look.bottom:part.name==="outfit_shoes"?look.shoes:null):null;gl.uniform1f(P.u.useTint,tint?1:0);if(tint){const h=hex(tint);gl.uniform3f(P.u.tint,h[0]/255,h[1]/255,h[2]/255);gl.uniform1f(P.u.avg,part.avg)}
    gl.uniform1f(P.u.useFlat,part.tex?0:1);if(!part.tex)gl.uniform3fv(P.u.plain,part.flat||[.4,.4,.4]);gl.uniform2fv(P.u.uvlo,part.uvlo);gl.uniform2fv(P.u.uvspan,part.uvspan);gl.uniform1f(P.u.cut,part.cut);
    gl.activeTexture(gl.TEXTURE0);if(part.tex)gl.bindTexture(gl.TEXTURE_2D,part.tex);gl.uniform1i(P.u.t,0);gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,part.i);gl.drawElements(gl.TRIANGLES,part.count,gl.UNSIGNED_SHORT,0)}
  for(const a of[P.a.j,P.a.w,P.a.paint,P.a.uv])gl.disableVertexAttribArray(a);
  const h=m.index.Head;return{model,head:mul(model,mul(W[h],m.bones[h].inv))}}
return{load,draw,init,dbg:(m,list)=>{use(m);poseClips(m,list,true,0);return{W:W.slice(0,m.bones.length).map(w=>Array.from(w)),Q:Array.from(QB.slice(0,ANIM.bones.length*4)),D:DQ.slice(0,m.bones.length),names:ANIM.bones}},cycle:(m,run,back)=>ANIM&&m.rest?1/((1-run)/ANIM.clips[(back&&m.clips.back)||m.clips.walk].dur+run*m.jogRate/ANIM.clips[m.clips.jog].dur):1.06+(.71-1.06)*run}})();
