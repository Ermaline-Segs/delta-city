const SAND="#d6c79c",TAR="#3b3d42",PAVE="#cfc8b6";
const WHITE="#fbfaf5",MARBLE="#f2eee5",DARKWOOD="#4a3222",MIDWOOD="#7a5636",GLASSI="#cfe6f2";
/* ============================ scenes: outside and inside ============================ */
let WALLS=[],SHADOWS=[];                       // WALLS: where you cannot walk [x0,z0,x1,z1,level]; SHADOWS: what stands on the floor
const corners=(x,z,w,d)=>{let x0=1e9,z0=1e9,x1=-1e9,z1=-1e9;for(const[a,b]of[[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]]){const px=M[0]*(x+a)+M[8]*(z+b)+M[12],pz=M[2]*(x+a)+M[10]*(z+b)+M[14];x0=Math.min(x0,px);x1=Math.max(x1,px);z0=Math.min(z0,pz);z1=Math.max(z1,pz)}return[x0,z0,x1,z1]};
function solid(x,z,w,d,level){const r=corners(x,z,w,d);r.push(level);WALLS.push(r)}
function stands(x,z,w,d){SHADOWS.push(corners(x,z,w,d))}
function capture(fn){BAKE=null;CLEAR_GLASS=false;reset();fn();return upload()}
/* Indoors, each corner of every surface is lit once, here: by the ceiling lamps near it, and
   darkened where furniture stands on the floor. The room is built twice: first to learn where
   the furniture is, then for real. */
function captureLit(fn,lights,split,ceilH){BAKE=null;CLEAR_GLASS=true;reset();WALLS=[];SHADOWS=[];fn();const sh=SHADOWS.slice(),wl=WALLS.filter(w=>w[4]!==-1);
  const sm=v=>{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v)};
  BAKE=(x,y,z,nx,ny,nz)=>{let L=.5;for(const l of lights){if(split&&((l[1]>3.4&&y<3.25&&z<-2.3)||(l[1]<3.2&&y>3.28)))continue;      // the gallery floor blocks light between levels
      const dx=l[0]-x,dy=l[1]-y,dz=l[2]-z,d2=dx*dx+dy*dy+dz*dz,d=Math.sqrt(d2)||1;L+=l[3]*Math.max(.3,(nx*dx+ny*dy+nz*dz)/d)/(1+d2/(l[4]*l[4]))}
    const up=split&&y>3.25,level=up?1:0,base=up?y-3.3:y;
    if(Math.abs(ny)>.9){                                   // floors and ceilings: darker where furniture stands, and along the foot and head of every wall
      if(ny>0&&base<.25)for(const b of sh){const ax=Math.max(b[0]-x,0,x-b[2]),az=Math.max(b[1]-z,0,z-b[3]);L*=1-.5*Math.exp(-Math.hypot(ax,az)/.22)}
      if(base<.25||ny<0){let near=9;for(const w of wl){if(w[4]!==undefined&&w[4]!==level)continue;const ax=Math.max(w[0]-x,0,x-w[2]),az=Math.max(w[1]-z,0,z-w[3]),dd=Math.hypot(ax,az);if(dd<near)near=dd}L*=1-.3*Math.exp(-near/.38)}}
    else{L*=.7+.3*sm(base/.55);if(ceilH)L*=.86+.14*sm((ceilH-y)/.45)}      // everything upright: darker towards the floor, and just under the ceiling
    return Math.min(1.06,L)};
  reset();WALLS=[];SHADOWS=[];fn();BAKE=null;const out=upload();CLEAR_GLASS=false;return out}

/* ---------------------------------- shared pieces ---------------------------------- */
function floorGrid(x0,z0,x1,z1,y,color,kind,step){const c=hex(color),s=step||1;for(let x=x0;x<x1-1e-6;x+=s)for(let z=z0;z<z1-1e-6;z+=s){const xa=Math.min(x+s,x1),za=Math.min(z+s,z1);quad([x,y,za],[xa,y,za],[xa,y,z],[x,y,z],c,kind)}}
function ceilGrid(x0,z0,x1,z1,y,color,step){const c=hex(color),s=step||2;for(let x=x0;x<x1-1e-6;x+=s)for(let z=z0;z<z1-1e-6;z+=s){const xa=Math.min(x+s,x1),za=Math.min(z+s,z1);quad([x,y,z],[xa,y,z],[xa,y,za],[x,y,za],c)}}
// a wall in 2 m pieces so the light on it can vary along its length; collide: also stops you walking through
function wallRun(x0,z0,x1,z1,y0,y1,color,kind,level,noCollide){const len=Math.hypot(x1-x0,z1-z0),n=Math.max(1,Math.round(len/2)),alongX=Math.abs(x1-x0)>Math.abs(z1-z0);
  const bands=y1-y0>2?[[y0,y0+.55],[y0+.55,y1-.45],[y1-.45,y1]]:[[y0,y1]];                       // three bands, so the shade at the foot and head of the wall can show
  for(let k=0;k<n;k++){const ax=x0+(x1-x0)*(k+.5)/n,az=z0+(z1-z0)*(k+.5)/n;for(const[a,b]of bands)box(ax,a,az,alongX?len/n:.2,b-a,alongX?.2:len/n,color,kind)}
  if(!noCollide)WALLS.push([Math.min(x0,x1)-(alongX?0:.12),Math.min(z0,z1)-(alongX?.12:0),Math.max(x0,x1)+(alongX?0:.12),Math.max(z0,z1)+(alongX?.12:0),level])}
function discZ(x,y,z,r,color,kind,n){const c=hex(color),N=n||20;for(let k=0;k<N;k++){const a=k/N*6.2832,b=(k+1)/N*6.2832;tri([x,y,z],[x+Math.cos(a)*r,y+Math.sin(a)*r,z],[x+Math.cos(b)*r,y+Math.sin(b)*r,z],c,kind)}}
function label(x,y,z,w,h,text,bg,fg,turn){at(x,z,turn||0,()=>{box(0,y-.04,-.03,w+.1,h+.08,.04,GOLD,K.gold);sign(0,y,0,w,h,text,bg,fg)})}
function atm(x,z,turn){at(x,z,turn,()=>{box(0,0,0,.9,2.0,.75,NAVY);box(0,1.2,.38,.56,.42,.03,"#9fd8ff",K.glow);box(0,.86,.44,.56,.2,.16,"#d9dde2");box(.28,.62,.385,.2,.06,.02,"#111820");box(0,1.74,.385,.8,.2,.02,GOLD,K.gold);box(-.3,1.0,.385,.14,.05,.02,"#35d07f",K.glow);stands(0,0,.9,.75)});}
function chair(x,z,turn,color){at(x,z,turn,()=>{const c=color||NAVY2;box(0,.4,0,.52,.1,.5,c,K.fabric);box(0,.5,-.23,.52,.5,.08,c,K.fabric);cyl(0,0,0,.24,.04,"#8d8f94",8);cyl(0,.04,0,.035,.36,"#8d8f94",6);stands(0,0,.5,.5)})}
function sofa(x,z,turn,n){at(x,z,turn,()=>{const L=n*.8;box(0,.12,0,L+.3,.3,.9,NAVY,K.fabric);box(0,.42,-.36,L+.3,.5,.18,NAVY,K.fabric);for(const s of[-1,1])box(s*(L/2+.06),.42,0,.18,.26,.9,NAVY,K.fabric);
  for(let k=0;k<n;k++){box(-L/2+.4+k*.8,.42,.06,.74,.14,.68,NAVY2,K.fabric);box(-L/2+.4+k*.8,.56,-.2,.5,.34,.12,IVORY,K.fabric)}for(const[a,b]of[[-L/2,-.36],[L/2,-.36],[-L/2,.36],[L/2,.36]])cyl(a,0,b,.04,.12,GOLD,6);stands(0,0,L+.3,.9);solid(0,0,L+.3,.9,0)})}
function lowTable(x,z){box(x,.42,z,1.2,.04,.7,GLASSI,K.glass);for(const[a,b]of[[-.52,-.28],[.52,-.28],[-.52,.28],[.52,.28]])cyl(x+a,0,z+b,.03,.42,GOLD,6);box(x,.44,z,.36,.03,.26,"#f4f4f0");stands(x,z,1.2,.7)}
function palmPot(x,z){cyl(x,0,z,.3,.62,GOLD,10,.36);cyl(x,.62,z,.05,1.0,"#5b4a2e",6);for(let k=0;k<7;k++)at(x,z,k/7*6.2832,()=>{const g=hex("#2f8f4b");both([0,1.55,-.08],[.6,1.95,-.16],[.6,1.95,.16],[0,1.55,.08],g);both([.6,1.95,-.16],[1.05,1.55,-.05],[1.05,1.55,.05],[.6,1.95,.16],g.map(v=>v*.85))});stands(x,z,.8,.8);solid(x,z,.6,.6,0)}
function column(x,z,h){cyl(x,0,z,.5,.3,GOLD,14);cyl(x,.3,z,.36,h-.7,WHITE,14);cyl(x,h-.4,z,.36,.4,GOLD,14,.52);stands(x,z,1,1);solid(x,z,.8,.8,0)}
function desk(x,z,turn,w,top,front){at(x,z,turn,()=>{const W=w||1.7;box(0,.72,0,W,.07,.85,top||DARKWOOD,K.wood);box(0,0,-.32,W-.1,.72,.06,front||NAVY);for(const s of[-1,1])box(s*(W/2-.05),0,0,.07,.72,.8,top||DARKWOOD,K.wood);box(0,.69,-.345,W-.1,.04,.03,GOLD,K.gold);
  box(.32,.8,.02,.56,.36,.04,"#161b22");box(.32,.82,.045,.5,.3,.01,"#a7d8f2",K.glow);box(.32,.79,.02,.14,.03,.16,"#161b22");box(-.4,.795,.1,.34,.02,.24,"#f6f6f2");box(-.02,.795,.2,.3,.02,.1,"#2a2f38");stands(0,0,W,.85);solid(0,0,W,.85)})}
function ropeLine(pts){for(const[x,z]of pts){cyl(x,0,z,.16,.04,GOLD,10);cyl(x,.04,z,.035,.95,GOLD,8);cyl(x,.99,z,.07,.06,GOLD,8);stands(x,z,.3,.3)}
  for(let k=0;k<pts.length-1;k++){const[a,b]=pts[k],[c,d]=pts[k+1];box((a+c)/2,.82,(b+d)/2,Math.abs(c-a)||.05,.06,Math.abs(d-b)||.05,NAVY2,K.fabric)}}
function ceilingLamp(x,y,z){box(x,y-.05,z,1.3,.05,.64,"#fffdf2",K.glow);box(x,y-.03,z,1.44,.03,.78,GOLD,K.gold)}

/* --------------------------- inside Crestfield Bank: "Royal Banking" ---------------------------
   Navy, gold, ivory and white. A tall banking hall behind a glass front, polished tiles, a
   glass-fronted teller line under a gallery, customer service to one side, and a staircase up
   to the offices. Customers have the hall; staff have the tellers' side, the vault and upstairs. */
const HALL={x0:-17,x1:17,z0:-10,z1:10,high:6.4,mezz:3.3};
function bankInside(){const H=HALL.high,MZ=HALL.mezz;
  // ---- floor: polished tiles, a navy and gold border, a medallion under the chandelier
  floorGrid(-17,-10,17,10,0,MARBLE,K.tile,.5);
  for(const[x,z,w,d]of[[0,8.3,31,.35],[0,-.9,31,.35],[-15.5,3.7,.35,9.55],[15.5,3.7,.35,9.55]])box(x,0,z,w,.006,d,NAVY,K.tile);
  for(const[x,z,w,d]of[[0,8.0,30.3,.08],[0,-.6,30.3,.08],[-15.2,3.7,.08,8.7],[15.2,3.7,.08,8.7]])box(x,0,z,w,.008,d,GOLD,K.gold);
  cyl(0,0,3.6,2.9,.006,NAVY,40);cyl(0,0,3.6,2.6,.008,GOLD,40);cyl(0,0,3.6,2.45,.01,WHITE,40);cyl(0,0,3.6,1.2,.012,NAVY,32);cyl(0,0,3.6,.95,.014,GOLD,32);
  for(let k=0;k<8;k++)at(0,3.6,k/8*6.2832,()=>tri([0,.016,.2],[2.3,.016,0],[0,.016,-.2],hex(NAVY),K.tile));
  // ---- ceilings and their lamps (on a 4 m grid, which the shiny floor mirrors)
  ceilGrid(-17,-10,17,10,H,WHITE,2);for(let x=-16;x<=16;x+=4)for(const z of[0,4,8,-4,-8])ceilingLamp(x,H,z);
  for(let x=-17;x<17;x+=4)box(x+2,H-.35,4,.25,.35,12,IVORY);for(const z of[-2,2,6,10])box(0,H-.35,z,34,.35,.25,IVORY);          // ceiling beams
  // ---- side and back walls: ivory, with navy panelling and a gold rail
  for(const sx of[-1,1]){wallRun(sx*17,-10,sx*17,10,0,H,IVORY);for(let z=-9;z<10;z+=2){box(sx*16.86,.12,z,.06,1.0,1.7,NAVY);box(sx*16.83,.3,z,.04,.64,1.34,NAVY2)}box(sx*16.85,1.16,0,.08,.07,20,GOLD,K.gold);box(sx*16.86,0,0,.08,.12,20,GOLD,K.gold)}
  wallRun(-17,-10,17,-10,0,H,IVORY);
  // ---- the glass front, with the way out in the middle
  for(let x=-17;x<=17;x+=2)if(Math.abs(x)>1.2)box(x,0,10,.16,H,.2,NAVY);for(const y of[2.7,4.6])box(0,y,10,34,.14,.2,NAVY);box(0,H-.5,10,34,.5,.24,NAVY);box(0,0,10,34,.14,.2,NAVY);
  for(let x=-16;x<17;x+=2){const mid=Math.abs(x)<1.1;box(x,mid?2.84:.14,10,1.84,mid?H-3.34:H-.64,.04,GLASSI,K.glass)}
  WALLS.push([-17,9.85,-1.5,10.15],[1.5,9.85,17,10.15]);for(const s of[-1,1])box(s*1.55,0,10,.16,2.7,.22,GOLD,K.gold);entrance(0,0,9.9,2.9,2.6,Math.PI,true);label(0,2.95,9.86,1.5,.36,"EXIT",NAVY,"#f1d27a",Math.PI);
  box(0,-.3,22,90,.1,24,"#cfc8b6",K.tile);                                                                                   // the forecourt, seen through the glass
  // ---- columns
  for(const[x,z]of[[-9,6],[9,6],[-9,1.6],[9,1.6]])column(x,z,H);for(const x of[-15.6,-9,-2.6,10])column(x,-2.2,MZ);
  // ---- the gallery (upper floor) across the back, its edge and glass rail
  box(0,MZ-.25,-6,34,.23,8,WHITE);floorGrid(-17,-10,17,-2,MZ,MARBLE,K.tile,1);box(0,MZ-.55,-2.05,34,.6,.2,NAVY);box(0,MZ-.02,-2.02,34,.07,.26,GOLD,K.gold);box(0,MZ-.58,-2.02,34,.06,.24,GOLD,K.gold);
  for(let x=-16.5;x<14;x+=1.5)box(x+.75,MZ+.08,-2.02,1.42,.95,.03,GLASSI,K.glass);for(let x=-17;x<=14;x+=1.5)box(x,MZ,-2.02,.06,1.08,.06,GOLD,K.gold);box(-1.5,MZ+1.06,-2.02,31,.06,.1,GOLD,K.gold);
  WALLS.push([-17,-2.14,14.05,-1.9,1]);
  label(-6.5,MZ-.47,-1.92,5,.42,"TELLERS",NAVY,"#f1d27a");label(9.4,MZ-.47,-1.92,6.4,.42,"CUSTOMER SERVICE",NAVY,"#f1d27a");
  // ---- the teller line: marble top, navy front, glass to the gallery, five windows
  box(-6.5,0,-2.9,18.4,1.08,.75,NAVY);box(-6.5,.5,-2.51,18.4,.08,.02,GOLD,K.gold);box(-6.5,1.08,-2.9,18.7,.07,1.0,WHITE,K.tile);WALLS.push([-15.9,-3.4,2.9,-2.4,0]);
  for(let k=0;k<5;k++){const x=-13.9+k*3.7;box(x,1.15,-3.05,3.3,MZ-1.7,.04,GLASSI,K.glass);for(const s of[-1,1])box(x+s*1.75,1.15,-3.05,.07,MZ-1.7,.08,GOLD,K.gold);box(x,1.15,-3.05,.9,.28,.1,NAVY);
    label(x,MZ-1.05,-2.98,.7,.42,String(k+1),NAVY,"#f1d27a");desk(x,-4.9,Math.PI,1.6,MIDWOOD,NAVY2);chair(x,-5.8,0,"#2a2f38");box(x-.55,.8,-4.7,.28,.14,.16,"#3f9a5a");box(x-.2,.8,-4.7,.28,.09,.16,"#57b271")}
  box(-6.5,MZ-.55,-3.05,18.6,.3,.1,NAVY);
  ropeLine([[-12,.2],[-12,2.4],[-9,2.4]]);ropeLine([[-6,.2],[-6,2.4],[-3,2.4]]);ropeLine([[-1,.2],[-1,2.4]]);
  // ---- the staff door beside the counter
  wallRun(2.9,-3,3.5,-3,0,MZ-.25,IVORY,0,0);wallRun(4.7,-3,5.3,-3,0,MZ-.25,IVORY,0,0);box(4.1,2.15,-3,1.2,MZ-2.4,.2,IVORY);label(4.1,2.25,-2.88,1.15,.34,"STAFF ONLY",NAVY,"#f1d27a");
  // ---- behind the tellers: the vault in the back wall, cabinets, a counting table
  floorGrid(-17,-10,5.2,-3.4,.004,"#d9d4c8",K.tile,1);wallRun(5.3,-10,5.3,-3,0,MZ-.25,IVORY,0,0);
  box(-6,.3,-9.8,3.6,2.9,.3,"#7f8a93");discZ(-6,1.75,-9.62,1.25,"#aab4bc");discZ(-6,1.75,-9.6,1.02,"#8d99a3");discZ(-6,1.75,-9.58,.34,GOLD,K.gold);
  for(let k=0;k<6;k++){const a=k/6*6.2832;box(-6+Math.cos(a)*.62,1.71+Math.sin(a)*.62,-9.56,.09,.09,.06,"#5b6470")}for(let k=0;k<4;k++)box(-7.6,.7+k*.6,-9.6,.2,.14,.14,"#5b6470");label(-6,3.25-.42,-9.6,1.4,.3,"VAULT",NAVY,"#f1d27a");
  for(const x of[-15,-13.4,-11.8,1,2.6]){box(x,0,-9.5,1.5,2.0,.6,MIDWOOD,K.wood);box(x,1.0,-9.18,1.4,.03,.02,GOLD,K.gold);stands(x,-9.5,1.5,.6)}
  at(-1.5,-8,0,()=>{box(0,.8,0,2.6,.07,1.1,"#5b6470");for(const s of[-1,1])box(s*1.2,0,0,.07,.8,1,"#5b6470");for(let a=0;a<4;a++)for(let b=0;b<2;b++)box(-.8+a*.52,.87+b*.11,0,.42,.1,.22,b?"#3f9a5a":"#57b271");stands(0,0,2.6,1.1);solid(0,0,2.6,1.1,0)});
  // ---- customer service, under the gallery: three desks between glass screens, and a waiting sofa
  for(let k=0;k<3;k++){const x=7+k*2.6;desk(x,-8.2,Math.PI,1.8,IVORY,NAVY);chair(x,-9.1,0,"#2a2f38");chair(x-.4,-7.1,Math.PI);chair(x+.4,-7.1,Math.PI);if(k)box(x-1.3,0,-8.4,.05,1.7,2.6,GLASSI,K.glass)}
  box(13.6,0,-8.4,.05,1.7,2.6,GLASSI,K.glass);sofa(9.6,-4.4,0,3);label(9.6,2.25,-9.86,3.4,.5,"LOANS  •  ACCOUNTS  •  CARDS",NAVY,"#f1d27a");
  // ---- the hall: a lounge, an enquiries desk, tables for filling in slips, greenery, the bank's name
  sofa(-13.4,6.2,Math.PI/2,3);sofa(-11,8.6,Math.PI,3);lowTable(-11.4,6.2);box(-11.6,.006,6.4,5.6,.01,5,NAVY2,K.fabric);
  at(11.5,6.6,0,()=>{box(0,0,0,3.8,1.08,.8,NAVY);box(0,.5,.41,3.8,.08,.02,GOLD,K.gold);box(0,1.08,0,4,.07,1,WHITE,K.tile);box(-.8,1.16,-.1,.5,.34,.04,"#161b22");stands(0,0,3.8,.8);solid(0,0,3.8,.9,0)});chair(11.5,5.7,0,"#2a2f38");label(11.5,2.1,6.6,2.6,.42,"ENQUIRIES",NAVY,"#f1d27a");for(const s of[-1,1])cyl(11.5+s*1.36,1.15,6.6,.03,.95,GOLD,6);
  for(const x of[-3.6,3.6]){at(x,6.2,0,()=>{cyl(0,0,0,.34,.05,GOLD,12);cyl(0,.05,0,.06,1.0,GOLD,8);cyl(0,1.05,0,.52,.05,WHITE,16);box(0,1.11,0,.3,.02,.2,"#f6f6f2");stands(0,0,1,1);solid(0,0,.7,.7,0)})}
  for(const[x,z]of[[-16,9.2],[16,9.2],[-16,-1.2],[6.2,-1.4],[13.2,2.6]])palmPot(x,z);
  label(-16.84,3.4,3.6,7.5,1.25,"CRESTFIELD BANK",NAVY,"#f1d27a",Math.PI/2);label(-16.84,2.6,3.6,5,.42,"Secure.  Established.  Yours.",IVORY,NAVY,Math.PI/2);
  at(16.84,3.4,-Math.PI/2,()=>{box(0,3.0,-.04,6.6,2.3,.06,"#0b1730");for(let r=0;r<4;r++){box(-1.2,4.75-r*.5,0,3.6,.26,.02,r?"#9fd8ff":"#f1d27a",K.glow);box(2.3,4.75-r*.5,0,1.2,.26,.02,r%2?"#35d07f":"#ff8f8f",K.glow)}});
  // ---- chandelier over the medallion
  cyl(0,H-1.5,3.6,.04,1.5,GOLD,6);for(const[r,y]of[[1.5,H-1.9],[1.0,H-1.6],[.5,H-1.35]]){for(let k=0;k<16;k++){const a=k/16*6.2832;box(Math.cos(a)*r,y,3.6+Math.sin(a)*r,.16,.07,.16,GOLD,K.gold);if(k%2===0)box(Math.cos(a)*r,y-.14,3.6+Math.sin(a)*r,.09,.14,.09,"#fff6d8",K.glow)}}
  // ---- the staircase up to the gallery (staff): navy carpet, gold edges, glass rail
  const N=18;for(let k=0;k<N;k++){const z=4-(k+.5)*(6/N),y=(k+1)*(MZ/N);box(15.55,0,z,2.7,y,6/N,WHITE);box(15.55,y,z,1.7,.012,6/N,NAVY,K.fabric);for(const s of[-1,1])box(15.55+s*.9,y,z,.06,.014,6/N,GOLD,K.gold)}
  for(let k=0;k<=6;k++){const z=4-k,y=k*(MZ/6);box(14.15,y,z,.06,1.05,.06,GOLD,K.gold);if(k<6)both([14.15,y+.1,z],[14.15,y+MZ/6+.1,z-1],[14.15,y+MZ/6+.98,z-1],[14.15,y+.98,z],hex(GLASSI),K.glass)}
  WALLS.push([14.0,-2,14.3,4.1],[14.2,-2.2,17,-1.95,0]);for(const x of[14.2,16.9])box(x,0,4.25,.08,1.1,.08,GOLD,K.gold);
  // ---- upstairs: three glass-fronted rooms along the back
  for(const[x0,x1,name,carpet]of[[-17,-6,"DIRECTOR","#5a2a2f"],[-6,5,"MANAGER","#2b4a3a"],[5,17,"BOARDROOM",NAVY2]]){const mid=(x0+x1)/2;
    box(mid,MZ+.004,-7.7,x1-x0-.3,.01,4.4,carpet,K.fabric);for(let x=x0+.3;x<x1-.3;x+=1.6){if(Math.abs(x+.8-mid)<.9)continue;box(x+.8,MZ,-5.4,1.5,H-MZ,.04,GLASSI,K.glass);box(x,MZ,-5.4,.07,H-MZ,.08,NAVY)}
    box(mid,MZ+2.2,-5.4,1.8,H-MZ-2.2,.06,NAVY);label(mid,MZ+2.3,-5.34,1.5,.32,name,NAVY,"#f1d27a");WALLS.push([x0,-5.5,mid-.75,-5.3,1],[mid+.75,-5.5,x1,-5.3,1]);if(x1<17)wallRun(x1,-10,x1,-5.4,MZ,H,IVORY,0,1)}
  M=mul(M,trans(0,0,0));const up=fn=>{const keep=M;M=mul(M,new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,0,MZ,0,1]));fn();M=keep};
  const trophy=(x,y,z,s)=>{cyl(x,y,z,.1*s,.05*s,DARKWOOD,8);cyl(x,y+.05*s,z,.025*s,.12*s,GOLD,6);cyl(x,y+.17*s,z,.05*s,.2*s,GOLD,10,.12*s);for(const d of[-1,1])box(x+d*.13*s,y+.24*s,z,.03*s,.1*s,.02*s,GOLD,K.gold)};
  up(()=>{
    // the Director's office, at the far end: a large desk, a sofa for visitors, and the bank's awards
    desk(-11.5,-8.5,Math.PI,2.5,DARKWOOD,NAVY);chair(-11.5,-9.4,0,"#20262e");chair(-12.2,-7.4,Math.PI);chair(-10.8,-7.4,Math.PI);sofa(-7.2,-7.6,-Math.PI/2,2);lowTable(-8.6,-7.6);
    for(const y of[.9,1.5,2.1]){box(-16.72,y,-7.7,.34,.05,3.6,DARKWOOD,K.wood);for(let k=0;k<5;k++)trophy(-16.72,y+.05,-9.1+k*.7,(k+y*2)%2<1?1:.8)}                // three shelves of trophies
    box(-16.86,.5,-7.7,.06,2.2,3.8,NAVY);
    at(-9.4,-5.95,0,()=>{box(0,0,0,.7,1.0,.7,NAVY);box(0,1.0,0,.76,.04,.76,GOLD,K.gold);trophy(0,1.04,0,1.9);box(0,1.04,0,.66,.75,.66,GLASSI,K.glass);stands(0,0,.7,.7);solid(0,0,.7,.7,1)});      // the biggest trophy, under glass
    palmPot(-15.9,-6.1)});
  for(const[x,text]of[[-14.4,"BANK OF THE YEAR 2026"],[-12.5,"MOST TRUSTED BANK"],[-10.6,"BEST CUSTOMER SERVICE"],[-8.7,"EXCELLENCE IN GOVERNANCE"]]){label(x,MZ+1.75,-9.86,1.5,1.0,text,"#fbf7ea",NAVY);box(x,MZ+1.62,-9.84,.36,.1,.02,GOLD,K.gold)}
  label(-11.5,MZ+3.0,-9.86,3.6,.5,"Crestfield Bank",IVORY,NAVY);
  for(const[z,text]of[[-8.8,"DIRECTOR OF THE YEAR"],[-7.2,"25 YEARS OF SERVICE"]])label(-6.14,MZ+1.6,z,1.3,.5,text,NAVY,"#f1d27a",-Math.PI/2);
  label(-11.5,MZ+1.86,-5.34,1.5,.2,"By appointment",IVORY,NAVY);
  up(()=>{
    // the Manager's office, in the middle
    desk(-.5,-8.4,Math.PI,2.1,DARKWOOD,NAVY);chair(-.5,-9.3,0,"#20262e");chair(-1.1,-7.3,Math.PI);chair(.1,-7.3,Math.PI);box(4.6,0,-7.8,.5,2,3,DARKWOOD,K.wood);stands(4.6,-7.8,.5,3);palmPot(-5.2,-6.1);
    // the boardroom
    box(11,.74,-7.7,5.6,.08,1.7,DARKWOOD,K.wood);for(const s of[-1,1])cyl(11+s*2,0,-7.7,.14,.74,GOLD,10);stands(11,-7.7,5.6,1.7);for(let k=0;k<5;k++){chair(8.8+k*1.1,-6.5,Math.PI);chair(8.8+k*1.1,-8.9,0)}
    box(11,1.5,-9.86,3.4,1.9,.06,"#0b1730");box(11,1.6,-9.82,3.1,1.6,.02,"#a7d8f2",K.glow)});
  for(const x of[-.5])label(x,MZ+2.9,-9.86,2.6,.6,"Crestfield Bank",IVORY,NAVY)}

const BANK_LIGHTS=(()=>{const L=[];for(let x=-16;x<=16;x+=4){for(const z of[0,4,8])L.push([x,6.2,z,.15,5.2]);for(const z of[-4,-8]){L.push([x,3.0,z,.2,2.6]);L.push([x,6.2,z,.13,4.6])}}L.push([0,4.6,3.6,.22,3.5]);return L})();

/* ------------------------------- outside the bank ------------------------------- */
function bankOutside(){quad([-110,-.02,110],[110,-.02,110],[110,-.02,-110],[-110,-.02,-110],hex(SAND));
  at(0,34,Math.PI/2,()=>{box(0,0,0,9,.05,200,TAR,K.road);for(const s of[-1,1]){for(let k=0;k<125;k++)box(s*4.7,0,-100+k*1.6+.8,.4,.22,1.6,k%2?"#f4f4f0":"#0f8a4c");box(s*6.6,0,0,3.4,.12,200,PAVE,K.tile)}for(let k=0;k<50;k++)box(0,.05,-99+k*4,.16,.012,2,"#f1f1ea")});
  royalBank({name:"Crestfield Bank",w:34,d:20,h:7.2,yardW:54,yardD:44});for(const x of[-40,40])lamp(x,28.4,-Math.PI/2)}
const OUT=capture(bankOutside),IN=captureLit(bankInside,BANK_LIGHTS,true),IN_WALLS=WALLS.slice();
/* Who may go where. Customers have the hall. Tellers have the counter side and upstairs.
   The Director's office opens only for the Director, the Manager, and a visitor the Director has invited. */
const ROLES=[["customer","a customer"],["teller","a teller"],["manager","the Manager"],["director","the Director"],["visitor","a visitor for the Director"]];
const ACCESS={tellers:["teller","manager","director"],stairs:["teller","manager","director","visitor"],director:["manager","director","visitor"]};
const can=key=>ACCESS[key].includes(me.role);
const GATES=[{key:"tellers",r:[3.5,-3.15,4.7,-2.85],level:0,msg:"Staff only. Customers cannot go through here."},
  {key:"stairs",r:[14.3,4.1,17,4.4],level:0,msg:"Upstairs is for staff and invited visitors."},
  {key:"director",r:[-12.25,-5.55,-10.75,-5.25],level:1,msg:"The Director's office opens only for the Director, the Manager and invited visitors."}];
const lit=fn=>captureLit(fn,BANK_LIGHTS,true),MZ1=HALL.mezz;
const DOORS=[
  {key:"tellers",shut:lit(()=>{box(4.1,0,-3,1.16,2.1,.07,DARKWOOD,K.wood);box(4.5,1.0,-2.95,.06,.06,.06,GOLD,K.gold)}),open:lit(()=>{box(3.54,0,-3.55,.07,2.1,1.1,DARKWOOD,K.wood)})},
  {key:"stairs",shut:lit(()=>{box(15.55,.05,4.25,2.6,1.0,.05,GLASSI,K.glass);box(15.55,1.05,4.25,2.7,.06,.08,GOLD,K.gold);label(15.55,1.3,4.3,1.6,.3,"STAFF & VISITORS",NAVY,"#f1d27a")}),
   open:lit(()=>{box(14.25,.05,4.9,.05,1.0,1.3,GLASSI,K.glass);box(16.85,.05,4.9,.05,1.0,1.3,GLASSI,K.glass)})},
  {key:"director",shut:lit(()=>{box(-11.5,MZ1,-5.4,1.46,2.15,.07,DARKWOOD,K.wood);box(-11.5,MZ1+1.0,-5.35,1.3,.04,.02,GOLD,K.gold);box(-10.95,MZ1+1.0,-5.34,.07,.07,.06,GOLD,K.gold)}),
   open:lit(()=>{box(-12.22,MZ1,-6.1,.07,2.15,1.4,DARKWOOD,K.wood)})}];
const OUT_WALLS=[[-17.3,-10.3,17.3,10.2]];

/* ================================== playing ================================== */
const me={x:0,y:0,z:26,yaw:0,pitch:.04,inside:false,role:"customer",busy:false},input={x:0,y:0},keys={};
let last=0,frames=0,acc=0,slow=0,quality=Math.min(window.devicePixelRatio||1,1.25),toastT=0;
function toast(t){const el=document.getElementById("toast");el.textContent=t;el.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>el.hidden=true,2600)}
function go(inside){if(me.busy)return;me.busy=true;const f=document.getElementById("fade");document.getElementById("where").textContent=inside?"Crestfield Bank: banking hall":"Outside Crestfield Bank";f.classList.add("on");
  setTimeout(()=>{me.inside=inside;me.y=0;if(inside){me.x=0;me.z=8.4;me.yaw=0}else{me.x=0;me.z=13.2;me.yaw=Math.PI}me.pitch=.02;setTimeout(()=>{f.classList.remove("on");me.busy=false},260)},300)}
// how high the floor is where you stand: the stairs rise from the hall to the gallery
function floorAt(x,z,y){if(!me.inside)return 0;if(x>14.3&&z<=4.1&&z>=-2)return clamp((4-z)/6,0,1)*HALL.mezz;if(y>1.6&&z<-1.9)return HALL.mezz;return 0}
function blocked(x,z){const r=.32;if(!me.inside){for(const w of OUT_WALLS)if(x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r)return true;return false}
  const level=me.y>1.6?1:0;for(const w of IN_WALLS){if(w[4]!==undefined&&w[4]!==level)continue;if(x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r)return true}
  if(x<-17+r||x>17-r||z<-10+r)return true;if(level===1&&z>-2.2&&!(x>14.3))return true;
  for(const g of GATES){const w=g.r;if(g.level===level&&!can(g.key)&&x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r){toast(g.msg);return true}}return false}
function frame(now){requestAnimationFrame(frame);const t=now/1000,real=t-last||.016,dt=Math.min(.05,real);last=t;
  const ix=input.x+(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),iy=input.y+(keys.w||keys.arrowup?1:0)-(keys.s||keys.arrowdown?1:0);
  if(!me.busy&&(ix||iy)){const sp=(keys.shift?4.6:2.6)*dt,dx=(-Math.sin(me.yaw)*iy+Math.cos(me.yaw)*ix)*sp,dz=(-Math.cos(me.yaw)*iy-Math.sin(me.yaw)*ix)*sp;
    if(!blocked(me.x+dx,me.z))me.x+=dx;if(!blocked(me.x,me.z+dz))me.z+=dz;me.y=floorAt(me.x,me.z,me.y);
    if(!me.inside&&Math.abs(me.x)<1.5&&me.z<11.6&&me.z>10)go(true);else if(me.inside&&me.y<.5&&Math.abs(me.x)<1.5&&me.z>9.55)go(false);
    if(!me.inside){me.x=clamp(me.x,-80,80);me.z=clamp(me.z,-60,60)}}
  const w=cv.clientWidth,h=cv.clientHeight,dpr=Math.min(window.devicePixelRatio||1,quality);if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr)}
  gl.viewport(0,0,cv.width,cv.height);const ey=me.y+1.62,eye=[me.x,ey,me.z],cp=Math.cos(me.pitch),to=[me.x-Math.sin(me.yaw)*cp,ey+Math.sin(me.pitch),me.z-Math.cos(me.yaw)*cp];
  const VP=mul(persp(w>h?1.05:1.25,w/h,.08,400),look(eye,to,[0,1,0]));
  gl.clearColor(.66,.84,.93,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);
  const parts=me.inside?[IN].concat(DOORS.map(d=>can(d.key)?d.open:d.shut)):[OUT];for(const S of parts)drawScene(S,VP,eye,me.inside);for(const S of parts)drawSceneClear(S,VP,eye,t);
  frames++;acc+=real;if(acc>=.5){const fps=frames/acc;document.getElementById("fps").textContent=Math.round(fps);frames=0;acc=0;
    document.getElementById("info").textContent=(me.inside?"Inside, ":"Outside, ")+Math.round((me.inside?IN.tris:OUT.tris)/1000)+"k triangles, "+cv.width+"x"+cv.height;
    if(t>3&&fps<48&&quality>.5){slow++;if(slow>=2){quality=Math.max(.5,quality-.2);slow=0}}else slow=0}}   // drop the sharpness until it runs smoothly
const touch=matchMedia("(pointer:coarse)").matches||"ontouchstart" in window;if(touch)document.body.classList.add("touch");
document.getElementById("tip").textContent=touch?"Left thumb: walk. Drag anywhere else: look around. Walk through the blue doorway to go in.":"Walk with W A S D or the arrow keys, hold Shift to hurry, drag to look around. Walk through the blue doorway to go in.";
addEventListener("keydown",e=>{keys[e.key.toLowerCase()]=true});addEventListener("keyup",e=>{keys[e.key.toLowerCase()]=false});
const stick=document.getElementById("stick"),knob=document.getElementById("knob");let stickId=null,lookId=null,lx=0,ly=0;
function stickMove(e){const r=stick.getBoundingClientRect();let dx=(e.clientX-r.left-r.width/2)/(r.width/2),dy=(e.clientY-r.top-r.height/2)/(r.height/2);const l=Math.hypot(dx,dy);if(l>1){dx/=l;dy/=l}input.x=dx;input.y=-dy;knob.style.transform=`translate(${dx*37}px,${dy*37}px)`}
stick.addEventListener("pointerdown",e=>{stickId=e.pointerId;stick.setPointerCapture(e.pointerId);stickMove(e);e.stopPropagation()});stick.addEventListener("pointermove",e=>{if(e.pointerId===stickId)stickMove(e)});
const stickEnd=e=>{if(e.pointerId===stickId){stickId=null;input.x=input.y=0;knob.style.transform=""}};stick.addEventListener("pointerup",stickEnd);stick.addEventListener("pointercancel",stickEnd);
cv.addEventListener("pointerdown",e=>{if(lookId===null){lookId=e.pointerId;lx=e.clientX;ly=e.clientY;cv.setPointerCapture(e.pointerId)}});
cv.addEventListener("pointermove",e=>{if(e.pointerId!==lookId)return;me.yaw+=(e.clientX-lx)*.005;me.pitch=clamp(me.pitch+(e.clientY-ly)*.004,-1.1,1.1);lx=e.clientX;ly=e.clientY});
const lookEnd=e=>{if(e.pointerId===lookId)lookId=null};cv.addEventListener("pointerup",lookEnd);cv.addEventListener("pointercancel",lookEnd);
{const el=document.getElementById("picks"),who=document.createElement("button");const set=()=>{who.textContent="You are: "+ROLES.find(r=>r[0]===me.role)[1]+"  (tap to change)"};
  who.addEventListener("click",()=>{me.role=ROLES[(ROLES.findIndex(r=>r[0]===me.role)+1)%ROLES.length][0];set();
    toast({customer:"A customer: the banking hall only.",teller:"A teller: the counter side, the vault area and upstairs, but not the Director's office.",manager:"The Manager: everywhere, including the Director's office.",director:"The Director: everywhere.",visitor:"A visitor for the Director: the hall, the stairs and the Director's office."}[me.role])});set();el.appendChild(who);
  const d=document.createElement("button");d.textContent="Go in / out";d.addEventListener("click",()=>go(!me.inside));el.appendChild(d)}
requestAnimationFrame(frame);
</script>
</body>
</html>
