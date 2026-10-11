import re,subprocess,imm_ui
src=open('town.src.html',encoding='utf-8').read().replace('__SCENE__','asaba')
bank=open('bank_tail.js',encoding='utf-8').read()
imm=open('immigration_tail.js',encoding='utf-8').read()
gov=open('gov_tail.js',encoding='utf-8').read()
walker=open('walker_tail.js',encoding='utf-8').read()
def cut(s,a,b): return s[s.index(a):s.index(b)]
def rp(s,x,y,n=1):
    assert s.count(x)==n,(x[:70],s.count(x)); return s.replace(x,y)
# ---- the bank's inside: one design, carrying each state's own bank name
bi=cut(bank,'const WHITE="#fbfaf5"','/* ------------------------------- outside the bank')
bi=bi.replace('"CRESTFIELD BANK"','BANK_NAME.toUpperCase()').replace('"Crestfield Bank"','BANK_NAME')
bw=cut(bank,'/* Who may go where.','const OUT_WALLS=')
bw=rp(bw,'const can=key=>','const bankCan=key=>')
for a,b in (('ROLES','BANK_ROLES'),('GATES','BANK_GATES'),('DOORS','BANK_DOORS')): bw=re.sub(r'\b%s\b'%a,b,bw)
bi=rp(bi,'const HALL=','let BANK_NAME="Crestfield Bank",BANK_WALLS=[];const BANK_CACHE={};\nfunction bankOf(st){BANK_NAME=STATES[st].bank;if(!BANK_CACHE[st]){BANK_CACHE[st]=captureLit(bankInside,BANK_LIGHTS,true);BANK_WALLS=WALLS.slice()}return BANK_CACHE[st]}\nconst HALL=')
bi+=bw
ia=cut(imm,'/* ====================== the Delta City Immigration Authority','/* ================================== playing')
ia=rp(ia,'const OUT_WALLS=','const BORDER_WALLS=')
ia=rp(ia,'const OUT=capture(borderOutside),IN=captureLit(immigrationInside,IMM_LIGHTS,false,CEIL),IN_WALLS=WALLS.slice();IN.ceil=[CEIL,CEIL];','const BORDER=capture(borderOutside),IMM_IN=captureLit(immigrationInside,IMM_LIGHTS,false,CEIL),IMM_WALLS=WALLS.slice();IMM_IN.ceil=[CEIL,CEIL];')
ia=rp(ia,'const ROLES=','const IMM_ROLES=');ia=rp(ia,'const can=key=>','const immCan=key=>');ia=rp(ia,'const GATES=','const IMM_GATES=');ia=rp(ia,'const DOORS=[','const IMM_DOORS=[')
ia=rp(ia,'at(VIOLET.x,VIOLET.z,0,()=>{ball(0,1.705,-.022,.104,.092,.11,"#1d1512");ball(0,1.585,-.105,.058,.052,.052,"#1d1512")});','')
talk=cut(imm,'/* The Certificate of Birth:','/* ================================ controls')
talk=rp(talk,'else if(me.role==="citizen"&&me.inside)s=','else if(me.role==="citizen"&&me.inside&&!me.entered)s=')
talk=rp(talk,'document.getElementById("act").addEventListener("click",()=>talk("hello"));','document.getElementById("act").addEventListener("click",()=>doAct());')
talk=rp(talk,'s="Step 3 of 3: you have your birth certificate. Follow the blue arrows on the floor to the CITY ENTRANCE, on the left side of the hall, and walk through."','s="Step 3 of 3: you have your birth certificate. Follow the blue arrows on the floor to the CITY ENTRANCE, on the left side of the hall. It takes you to "+me.cert.state+", your home state."')
talk=rp(talk,'Its light is now green. Walk through it.</p>','Its light is now green. Walk through it and you will arrive in ${esc(c.state)}, your home state, outside its immigration office.</p>')
head=imm_ui.apply(src[:src.index('const WORLD=upload(),TRIS=WORLD.tris;')])
head=re.sub(r'<script[^>]*id="person"[^>]*>.*?</script>\n?','',head,count=1,flags=re.S)
play=r'''/* ============================ inside the banks ============================ */
'''+bi+r'''
'''+ia+r'''
'''+gov+r'''
'''+walker+r'''
/* ================================== playing ==================================
   A new player begins on foot at the border gate, and cannot reach any town until Violet has
   issued a birth certificate. They then arrive in their home state. In a town you fly; inside
   a building you are on foot. Towns and interiors are built the first time someone goes there. */
const ROLES=[["newcomer","a new arrival (no certificate)"],["citizen","a citizen"],
  ["teller","a bank teller"],["manager","the Bank Manager"],["director","the Bank Director"],["visitor","a visitor for the Bank Director"],
  ["officer","an immigration officer"],["deputy","the Deputy Comptroller-General"],["cg","the Comptroller-General"],
  ["governor","the Governor"],["ssg","the Secretary to the State Government"],["council","a State Council member"],["govvisitor","a Government Visitor"],
  ["president","the President"],["vp","the Vice President"],["cos","the Chief of Staff"],["minister","the Minister of Finance"],["fedcouncil","a Federal Council member"],["villavisitor","a President Villa Visitor"]];
const cam={x:0,y:9,z:46,yaw:0,pitch:-.08},me={x:0,y:0,z:50,yaw:0,pitch:.03,role:"newcomer",cert:null,inside:false,entered:false,gender:"",outfit:"",town:"Asaba"},input={x:0,y:0},keys={};
let view3=true,driving=false,CARSCENE=null,lowFor=0;const CAST={},ROSTER={Male:[],Female:[],ready:false};
const pickDefault=()=>{if(!me.gender){me.gender="Female";me.outfit=ROSTER.Female.length?ROSTER.Female[0].key:"party"}};const PLAYERS={},gait={p:0,run:0,amt:0};
let scene="border",busy=false,talking=false,choosing=true,flying=false,testOpen=false,mapOpen=false,route=null,ROUTE_SCENE=null,routeCheck=0,GV=null,govSpot="",last=0,frames=0,acc=0,slow=0,quality=Math.min(window.devicePixelRatio||1,1.25),toastT=0;
const SAMPLE={no:"DC-ASB-0001",name:"Sample Citizen",dob:"01 September 1996",gender:"Female",state:"Asaba",date:"10 October 2026"};
const TOWNS={},CELLS=60;function townOf(st){if(!TOWNS[st]){BAKE=null;CLEAR_GLASS=false;reset();CELL=CELLS;const t=buildTown(st);t.scene=upload();CELL=0;TOWNS[st]=t}return TOWNS[st]}
function toast(t){const el=document.getElementById("toast");el.textContent=t;el.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>el.hidden=true,3400)}
function fadeTo(text,change){if(busy)return;busy=true;const f=document.getElementById("fade");document.getElementById("where").textContent=text;f.classList.add("on");setTimeout(()=>{change();ui();setTimeout(()=>{f.classList.remove("on");busy=false},260)},320)}
const stand=(s,o)=>{scene=s;me.inside=s==="imm";Object.assign(me,{y:0,pitch:.03},o||{})};
const allowed=who=>!who||who.includes(me.role);
const toBorder=fresh=>fadeTo("The border gate",()=>{if(fresh){me.role="newcomer";me.cert=null;me.entered=false;form.name=form.dob=form.gender=form.state="";closeTalk();stand("border",{x:0,z:50,yaw:0});chooser()}else stand("border",{x:0,z:14.4,yaw:Math.PI})});
const toImm=fromCity=>fadeTo("Delta City Immigration Authority",()=>stand("imm",fromCity?{x:-13.4,z:4.2,yaw:-Math.PI/2}:{x:0,z:9.6,yaw:0}));
const toBank=()=>fadeTo(STATES[me.town].bank+": banking hall",()=>{bankOf(me.town);stand("bank",{x:0,z:8.4,yaw:0})});
const toGov=(kind,spot)=>fadeTo(GOV_SPEC[kind](me.town).title,()=>{GV=govOf(kind,me.town);govSpot=spot;stand("gov",{x:0,z:G_LD-1.6,yaw:0})});
// arrive in a town, standing outside one of its doors and facing away from it
const toTown=(st,spot,text,dist)=>fadeTo(text||st,()=>{me.town=st;driving=false;const T=townOf(st),d=T.spots[spot]||T.spots.imm;scene="town";me.inside=false;me.entered=true;Object.assign(cam,{x:d.x+d.fx*(dist||5),y:1.7,z:d.z+d.fz*(dist||5),yaw:Math.atan2(-d.fx,-d.fz),pitch:0});if(!T.car)parkCar(T)});
// one car, parked at the kerb of the road nearest to where you arrive
function parkCar(T){let best=null;for(const r of T.map.roads){if(r.bridge)continue;const vx=r.x1-r.x0,vz=r.z1-r.z0,L=Math.hypot(vx,vz),t=clamp(((cam.x-r.x0)*vx+(cam.z-r.z0)*vz)/(L*L),.08,.92),x=r.x0+vx*t,z=r.z0+vz*t,d=Math.hypot(cam.x-x,cam.z-z);if(!best||d<best.d)best={d,x,z,ux:vx/L,uz:vz/L,w:r.w}}
  if(!best)return;const side=((cam.x-best.x)*-best.uz+(cam.z-best.z)*best.ux)>=0?1:-1,off=best.w/2-1.4;T.car={x:best.x-best.uz*side*off,z:best.z+best.ux*side*off,yaw:Math.atan2(-best.ux,-best.uz),v:0}}
// how high the bank's floor is where you stand: its stairs rise from the hall to the gallery
function floorAt(x,z,y){if(scene!=="bank")return 0;if(x>14.3&&z<=4.1&&z>=-2)return clamp((4-z)/6,0,1)*HALL.mezz;if(y>1.6&&z<-1.9)return HALL.mezz;return 0}
function blocked(x,z){const r=.32,hit=w=>x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r;
  if(scene==="border"){for(const w of BORDER_WALLS)if(hit(w))return true;return false}
  if(scene==="imm"){for(const w of IMM_WALLS){if(w[4]===-1)continue;if(hit(w))return true}for(const g of IMM_GATES)if(!immCan(g.key)&&hit(g.r)){toast(g.msg);return true}return x>15-r||z<-11+r}
  if(scene==="gov"){for(const w of GV.walls)if(hit(w))return true;for(const g of GV.gates)if(!allowed(g.who)&&hit(g.r)){toast(g.msg);return true}return Math.abs(x)>G_LW/2-r||z<GV.end+r}
  const level=me.y>1.6?1:0;for(const w of BANK_WALLS){if(w[4]!==undefined&&w[4]!==level)continue;if(hit(w))return true}
  if(x<-17+r||x>17-r||z<-10+r)return true;if(level===1&&z>-2.2&&!(x>14.3))return true;
  for(const g of BANK_GATES)if(g.level===level&&!bankCan(g.key)&&hit(g.r)){toast(g.msg);return true}return false}
const nearViolet=()=>scene==="imm"&&Math.hypot(me.x-VIOLET.x,me.z-2.6)<2.4;
const actNow=()=>{if(nearViolet())return"talk";if(scene!=="town"||flying)return null;const C=townOf(me.town).car;if(!C)return null;return driving?(Math.abs(C.v)<1.5?"out":null):Math.hypot(cam.x-C.x,cam.z-C.z)<3.6?"drive":null};
function doAct(){const a=actNow(),T=townOf(me.town),C=T.car;if(a==="talk")talk("hello");else if(a==="drive"){driving=true;cam.pitch=0;toast(touch?"Driving: push the stick up to go, down to brake, sideways to steer.":"Driving: W to go, S to brake and reverse, A and D to steer. Press F to get out.")}
  else if(a==="out"){driving=false;C.v=0;const rx=Math.cos(C.yaw),rz=-Math.sin(C.yaw);for(const s of[-1,1]){const x=C.x+rx*1.9*s,z=C.z+rz*1.9*s;if(!T.blocks.some(w=>x>w[0]-.4&&x<w[2]+.4&&z>w[1]-.4&&z<w[3]+.4)){cam.x=x;cam.z=z;break}}}}
const GPU=(()=>{try{const e=gl.getExtension("WEBGL_debug_renderer_info");return e?String(gl.getParameter(e.UNMASKED_RENDERER_WEBGL)).replace(/ANGLE \(|\)$/g,"").slice(0,34):"graphics unknown"}catch(x){return"graphics unknown"}})();
// what each door in a town leads to
const DOORWAYS={bank:()=>toBank(),imm:()=>STATES[me.town].capital?toImm(true):toast("This state immigration office has no inside yet. Registration is at the Immigration Authority in Asaba."),
  gov:()=>toGov("state","gov"),air:()=>departures(),
  fed:()=>allowed(ALL_FED)?toGov("federal","fed"):toast(GOV_SPEC.federal().noEntry),villa:()=>allowed(VILLA3)?toGov("villa","villa"):toast(GOV_SPEC.villa().noEntry),
  villa1:()=>allowed(VILLA3)?toGov("villa","villa1"):toast(GOV_SPEC.villa().noEntry),villa2:()=>allowed(VILLA3)?toGov("villa","villa2"):toast(GOV_SPEC.villa().noEntry)};
let doorCool=0;
function frame(now){requestAnimationFrame(frame);const t=now/1000,real=t-last||.016,dt=Math.min(.05,real);last=t;NOW=t;
  // A and D (or left and right) turn you, the way a person turns their head and body; W and S walk forward and back
  const turnIn=clamp(input.x+(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),-1,1),ix=0,iy=input.y+(keys.w||keys.arrowup?1:0)-(keys.s||keys.arrowdown?1:0);
  if(turnIn&&!busy&&!choosing&&!talking&&!mapOpen&&!driving)(scene==="town"?cam:me).yaw-=turnIn*2.1*dt;
  let eye,to;const T=scene==="town"?townOf(me.town):null;
  if(scene==="town"){
    const C=T.car,PM=PLAYERS[me.gender]||PLAYERS.Female,hitT=(x,z,r)=>T.blocks.some(w=>x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r);
    if(driving&&C){if(!busy&&!mapOpen){C.v+=(iy>0?(C.v<0?16:8):iy<0?(C.v>0?-18:-6):0)*dt;C.v*=1-Math.min(1,(iy?.25:1.1)*dt);C.v=clamp(C.v,-7,26);C.yaw-=clamp(input.x+(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),-1,1)*clamp(C.v/7,-1,1)*1.35*dt;
        const fx=-Math.sin(C.yaw),fz=-Math.cos(C.yaw),nx=C.x+fx*C.v*dt,nz=C.z+fz*C.v*dt;if(hitT(nx+fx*2*Math.sign(C.v||1),nz+fz*2*Math.sign(C.v||1),.9)||hitT(nx,nz,1))C.v*=-.25;else{C.x=nx;C.z=nz}}
      cam.x=C.x;cam.z=C.z;cam.yaw=C.yaw;cam.y=1.7;if(route)followRoute(t)}
    else if(!busy&&!choosing&&!mapOpen){const pace=PM&&!flying?(keys.shift?PM.speed.run:PM.speed.walk):0,sp=(flying?(keys.shift?16:6):pace||(keys.shift?7:3.2))*dt,dx=(-Math.sin(cam.yaw)*iy+Math.cos(cam.yaw)*ix)*sp,dz=(-Math.cos(cam.yaw)*iy-Math.sin(cam.yaw)*ix)*sp;
      if(flying){cam.x+=dx;cam.z+=dz;cam.y=clamp(cam.y+((keys.e?1:0)-(keys.q?1:0))*sp*(1+cam.y/20),1.2,420)}
      else{cam.y=1.7;const hit=(x,z)=>T.blocks.some(w=>x>w[0]-.4&&x<w[2]+.4&&z>w[1]-.4&&z<w[3]+.4);if(!hit(cam.x+dx,cam.z))cam.x+=dx;if(!hit(cam.x,cam.z+dz))cam.z+=dz}
      if(cam.y<3.8&&t>doorCool)for(const k in T.spots){const d=T.spots[k],ax=(cam.x-d.x)*d.fx+(cam.z-d.z)*d.fz,lat=Math.abs((cam.x-d.x)*d.fz-(cam.z-d.z)*d.fx);                  // through a blue doorway
        if(lat<1.7&&ax>-.7&&ax<1.5){doorCool=t+1.5;cam.x=d.x+d.fx*2.6;cam.z=d.z+d.fz*2.6;DOORWAYS[k]();break}}
      if(route)followRoute(t)}
    if(route)aimArrow();
    const cp=Math.cos(cam.pitch),fx=-Math.sin(cam.yaw),fz=-Math.cos(cam.yaw);
    if(flying||!view3){const ey=driving?1.12:cam.y;eye=[cam.x+(driving?fx*.1:0),ey,cam.z+(driving?fz*.1:0)];to=[eye[0]+fx*cp,ey+Math.sin(cam.pitch),eye[2]+fz*cp]}
    else{const dist=driving?7.6:3.5,up=driving?2.7:1.55,lift=clamp(.32-cam.pitch,0,1.2);let k=1;for(let q=.15;q<=1;q+=.15)if(hitT(cam.x-fx*dist*q,cam.z-fz*dist*q,.25)){k=Math.max(.15,q-.15);break}       // the camera stays this side of any wall behind you
      eye=[cam.x-fx*dist*k,up+lift*dist*.55*k,cam.z-fz*dist*k];to=[cam.x+fx*4,up-.15,cam.z+fz*4]}}
  else{
    if(!busy&&!talking&&!choosing&&(ix||iy)){const PM=PLAYERS[me.gender]||PLAYERS.Female,sp=(PM?(keys.shift?PM.speed.run:PM.speed.walk):(keys.shift?4.6:2.6))*dt,dx=(-Math.sin(me.yaw)*iy+Math.cos(me.yaw)*ix)*sp,dz=(-Math.cos(me.yaw)*iy-Math.sin(me.yaw)*ix)*sp;
      if(!blocked(me.x+dx,me.z))me.x+=dx;if(!blocked(me.x,me.z+dz))me.z+=dz;me.y=floorAt(me.x,me.z,me.y);
      if(scene==="border"){if(Math.abs(me.x)<1.5&&me.z<12.4&&me.z>11)toImm(false)}
      else if(scene==="imm"){if(Math.abs(me.x)<1.5&&me.z>10.55)toBorder(false);else if(me.x<-15.3&&immCan("city"))toTown(me.entered?"Asaba":(me.cert&&STATES[me.cert.state]?me.cert.state:"Asaba"),"imm",me.entered?"Asaba":"Welcome to "+(me.cert?me.cert.state:"Asaba")+", your home state",9)}
      else if(scene==="gov"){if(Math.abs(me.x)<1.5&&me.z>G_LD-.45)toTown(me.town,govSpot)}
      else if(me.y<.5&&Math.abs(me.x)<1.5&&me.z>9.55)toTown(me.town,"bank")}
    const ey=me.y+1.62,cp=Math.cos(me.pitch),fx=-Math.sin(me.yaw),fz=-Math.cos(me.yaw);
    if(!view3||talking){eye=[me.x,ey,me.z];to=[me.x+fx*cp,ey+Math.sin(me.pitch),me.z+fz*cp]}
    else{const wall=(x,z)=>scene==="border"?BORDER_WALLS.some(w=>x>w[0]-.2&&x<w[2]+.2&&z>w[1]-.2&&z<w[3]+.2):(scene==="imm"?IMM_WALLS:scene==="gov"?GV.walls:BANK_WALLS).some(w=>w[4]!==-1&&(scene!=="bank"||w[4]===undefined||w[4]===(me.y>1.6?1:0))&&x>w[0]-.2&&x<w[2]+.2&&z>w[1]-.2&&z<w[3]+.2);
      const dist=scene==="border"?3.4:2.5;let k=1;for(let q=.15;q<=1;q+=.15)if(wall(me.x-fx*dist*q,me.z-fz*dist*q)){k=Math.max(.12,q-.15);break}
      eye=[me.x-fx*dist*k,me.y+1.62+clamp(.25-me.pitch,0,1)*dist*.4*k,me.z-fz*dist*k];to=[me.x+fx*4,me.y+1.45,me.z+fz*4]}}
  // the walk cycle follows what the feet are doing
  {const moving=!busy&&!talking&&!choosing&&!mapOpen&&!driving&&!flying&&Math.abs(iy)>.1,PM=PLAYERS[me.gender]||PLAYERS.Female;gait.amt+=((moving?1:0)-gait.amt)*Math.min(1,dt*7);gait.run+=((moving&&keys.shift?1:0)-gait.run)*Math.min(1,dt*5);gait.back=iy<0&&moving?true:moving?false:gait.back;if(PM)gait.p+=dt*gait.amt*(gait.back&&!PM.clips.back?-1:1)/WALKER.cycle(PM,gait.run,gait.back)}
  {const a=actNow(),el=document.getElementById("act");el.hidden=!a||talking||busy||choosing||mapOpen;if(a)el.textContent=a==="talk"?"Talk to Violet":a==="drive"?"Drive the car":"Get out";}
  const w=cv.clientWidth,h=cv.clientHeight,dpr=Math.min(window.devicePixelRatio||1,quality);if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr)}
  const fly=scene==="town",indoor=scene==="bank"||scene==="imm"||scene==="gov",fovNow=fly?(w>h?.85:1.05):(w>h?1.05:1.25),PMs=PLAYERS[me.gender]||PLAYERS.Female;
  // the sun's picture first: the town near you, the car, and your own character all cast shadows
  if(scene==="town"&&SHADOW.ready&&SHADOW.on){const S=T.scene,near=S.cellBufs.filter(c=>Math.hypot(c.cx-cam.x,c.cz-cam.z)<SHADOW.range+CELLS),lists=[[S.bufs],[near]];if(T.car&&CARSCENE)lists.push([CARSCENE.bufs,mul(trans(T.car.x,0,T.car.z),rotY(T.car.yaw+Math.PI))]);
    shadowPass(lists,cam.x,cam.z,lvp=>{if(PMs&&!driving&&!flying&&!choosing){gl.colorMask(true,true,true,true);WALKER.draw(PMs,lvp,cam.x,0,cam.z,cam.yaw,gait,t,null,"");gl.colorMask(false,false,false,false)}})}
  gl.viewport(0,0,cv.width,cv.height);const VP=mul(persp(fovNow,w/h,fly?.25:.08,800),look(eye,to,[0,1,0]));
  gl.clearColor(.74,.86,.95,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);if(!indoor)drawSky(eye,to,fovNow,w/h);
  const parts=scene==="town"?townParts(T):scene==="border"?[BORDER]:scene==="bank"?[bankOf(me.town)].concat(BANK_DOORS.map(d=>bankCan(d.key)?d.open:d.shut)):scene==="gov"?[GV.scene].concat(GV.doors.map(d=>allowed(d.who)?d.open:d.shut)):[IMM_IN].concat(IMM_DOORS.map(d=>immCan(d.key)?d.open:d.shut));
  if(scene==="imm"&&me.cert&&me.role==="citizen"&&!me.entered)parts.push(GUIDE);
  for(const S of parts)drawScene(S,VP,eye,indoor);if(scene==="imm"&&CAST.violet)WALKER.draw(CAST.violet,VP,VIOLET.x,0,VIOLET.z,Math.PI,{p:0,run:0,amt:0,idle:talking?"f_talk":"f_idle"},t,null,"");
  if(scene==="town"&&T.car&&CARSCENE){CARSCENE.model=mul(trans(T.car.x,0,T.car.z),rotY(T.car.yaw+Math.PI));CARSCENE.fogFar=flying?1500:150;drawScene(CARSCENE,VP,eye,false)}
  {const PM=PLAYERS[me.gender]||PLAYERS.Female,show=PM&&view3&&!flying&&!driving&&!talking&&!choosing;      // your own character, seen from behind
    if(show){const town=scene==="town";WALKER.draw(PM,VP,town?cam.x:me.x,town?0:me.y,town?cam.z:me.z,town?cam.yaw:me.yaw,gait,t,null,"")}}
  for(const S of parts)drawSceneClear(S,VP,eye,t);if(scene==="town"&&T.car&&CARSCENE)drawSceneClear(CARSCENE,VP,eye,t);
  if(scene==="town"&&frames%3===0)drawMini(T);document.getElementById("mini").hidden=scene!=="town"||choosing;
  frames++;acc+=real;if(acc>=.5){const fps=frames/acc;document.getElementById("fps").textContent=Math.round(fps);frames=0;acc=0;let tris2=0;const tris=scene==="town"?0:parts.reduce((s,S)=>s+S.tris,0)+(scene==="imm"?15450:0);
    if(scene==="town")tris2=parts.reduce((s,S)=>s+S.bufs.concat(S.clear).reduce((q,x)=>q+x.n/3,0),0);const info=document.getElementById("info");info.textContent=({town:me.town,border:"The border gate",bank:"Inside "+STATES[me.town].bank,imm:"Inside Immigration",gov:GV?GV.title:""})[scene]+", "+Math.round((scene==="town"?tris2:tris)/1000)+"k triangles, "+cv.width+"x"+cv.height;info.appendChild(document.createElement("br"));info.appendChild(document.createTextNode(GPU));
    if(t>3&&fps<48&&quality>.5){slow++;if(slow>=2){quality=Math.max(.5,quality-.2);slow=0}}else slow=0;
    if(t>8&&fps<24&&SHADOW.on&&scene==="town"){lowFor=(lowFor||0)+1;if(lowFor>=6){SHADOW.on=false;toast("Shadows were switched off to keep the game smooth. You can turn them back on in Testing.")}}else lowFor=0}}       // shadows are the first thing to go on a slow machine        // lower the sharpness until it runs smoothly
'''+talk+r'''
/* ============================== the map and the route ==============================
   A small round map on the left shows the roads around you, north at the top, with an arrow for
   where you are. Tap it for the whole town; tap a named place and the way there is shown along
   the roads: a line on the map, arrows on the road, and the distance left at the top. */
function townParts(T){const R=flying?1e9:150,fx=-Math.sin(cam.yaw),fz=-Math.cos(cam.yaw),S=T.scene;
  const vis=c=>{const dx=c.cx-cam.x,dz=c.cz-cam.z,d=Math.hypot(dx,dz);return d<R+CELLS*.7&&(flying||d<52||(dx*fx+dz*fz)/d>.34)};
  const out=[{bufs:S.bufs.concat(S.cellBufs.filter(vis)),clear:S.clear.concat(S.cellClear.filter(vis)),sg:S.sg.filter(c=>Math.hypot(c.cx-cam.x,c.cz-cam.z)<R*.8),fogFar:flying?1500:R}];
  if(ROUTE_SCENE)out.push(ROUTE_SCENE);return out}
function paintMap(g,T,cx,cz,k,w,h,big,noMe){const o=noMe?-w/6:0,X=x=>o+w/2+(x-cx)*k,Y=z=>o+h/2+(z-cz)*k;g.fillStyle=T.map.land||"#efe6c8";g.fillRect(o-w,o-h,w*3,h*3);
  g.fillStyle="#8ec5e6";for(const poly of T.map.water){g.beginPath();poly.forEach((p,i)=>g[i?"lineTo":"moveTo"](X(p[0]),Y(p[1])));g.closePath();g.fill()}
  g.lineCap="round";for(const[col,extra]of[["#4b5563",7],["#7b8491",0]]){g.strokeStyle=col;for(const r of T.map.roads){g.lineWidth=Math.max(big?3:2.5,(r.w+extra)*k);g.beginPath();g.moveTo(X(r.x0),Y(r.z0));g.lineTo(X(r.x1),Y(r.z1));g.stroke()}
    g.fillStyle=col;for(const r of T.map.rounds){g.beginPath();g.arc(X(r.x),Y(r.z),Math.max(4,(r.r+extra/2)*k),0,6.2832);g.fill()}}
  g.fillStyle="#6aa857";for(const r of T.map.rounds){g.beginPath();g.arc(X(r.x),Y(r.z),Math.max(2,r.r*k*.45),0,6.2832);g.fill()}
  if(route){g.strokeStyle="#1d9bf0";g.lineWidth=big?5:4;g.lineJoin="round";g.beginPath();route.pts.forEach((p,i)=>g[i?"lineTo":"moveTo"](X(p[0]),Y(p[1])));g.stroke()}
  const boxes=big?T.map.places.map(p=>[X(p.x)-8,Y(p.z)-8,16,16]):[];for(const p of T.map.places){if(p.road)continue;const x=X(p.x),y=Y(p.z),on=route&&route.place===p;g.fillStyle=on?"#1d9bf0":p.color;g.strokeStyle="#ffffff";g.lineWidth=2;g.beginPath();g.arc(x,y,big?7:4,0,6.2832);g.fill();g.stroke();
    if(big){g.font="600 12px Segoe UI,system-ui,sans-serif";const tw=g.measureText(p.name).width+8;let put=null;for(const[ox,oy]of[[11,-8],[-tw-11,-8],[-tw/2,-28],[-tw/2,11],[11,-26],[11,10],[-tw-11,-26],[-tw-11,10]]){const r=[x+ox,y+oy,tw,17];if(r[0]>2&&r[0]+tw<w-2&&r[1]>2&&r[1]+17<h-2&&!boxes.some(q=>r[0]<q[0]+q[2]&&r[0]+r[2]>q[0]&&r[1]<q[1]+q[3]&&r[1]+r[3]>q[1])){put=r;break}}
      if(put){boxes.push(put);g.fillStyle="rgba(255,255,255,.88)";g.fillRect(put[0],put[1],put[2],put[3]);g.fillStyle="#111827";g.textBaseline="top";g.fillText(p.name,put[0]+4,put[1]+2)}p.px=x;p.py=y}}
  if(noMe)return;
  // you: an arrow pointing the way you face
  const px=X(cam.x),py=Y(cam.z),a=Math.atan2(-Math.sin(cam.yaw),Math.cos(cam.yaw));g.save();g.translate(px,py);g.rotate(a);g.fillStyle="#e11d48";g.strokeStyle="#ffffff";g.lineWidth=2;g.beginPath();g.moveTo(0,-(big?13:10));g.lineTo(big?9:7,big?10:8);g.lineTo(0,big?5:4);g.lineTo(big?-9:-7,big?10:8);g.closePath();g.fill();g.stroke();g.restore()}
const miniC=document.getElementById("mini");
// the round map: turned so that the way you face is always at the top, with a small N showing where north is
function drawMini(T){const s=miniC.width,g=miniC.getContext("2d");g.save();g.translate(s/2,s/2);g.rotate(cam.yaw);g.translate(-s/2,-s/2);const yaw=cam.yaw;cam.yaw=0;paintMap(g,T,cam.x,cam.z,s/230,s*1.5,s*1.5,false,true);cam.yaw=yaw;g.restore();
  g.fillStyle="#e11d48";g.strokeStyle="#fff";g.lineWidth=2.5;g.beginPath();g.moveTo(s/2,s/2-13);g.lineTo(s/2+9,s/2+10);g.lineTo(s/2,s/2+5);g.lineTo(s/2-9,s/2+10);g.closePath();g.fill();g.stroke();
  const nx=s/2+Math.sin(cam.yaw)*s*.41,ny=s/2-Math.cos(cam.yaw)*s*.41;g.fillStyle="#14263D";g.beginPath();g.arc(nx,ny,13,0,6.2832);g.fill();g.fillStyle="#fff";g.font="700 17px Segoe UI,system-ui,sans-serif";g.textAlign="center";g.textBaseline="middle";g.fillText("N",nx,ny+1)}
/* The town's own map: a photograph of the town taken from high above, looking north, with a pin
   on every named place. It is taken the first time the map is opened in each town. */
function aerial(T){if(T.aerial)return T.aerial;const W=1500,H=900;let x0=1e9,x1=-1e9,z0=1e9,z1=-1e9;for(const r of T.map.roads){x0=Math.min(x0,r.x0,r.x1);x1=Math.max(x1,r.x0,r.x1);z0=Math.min(z0,r.z0,r.z1);z1=Math.max(z1,r.z0,r.z1)}
  for(const p of T.map.places){x0=Math.min(x0,p.x);x1=Math.max(x1,p.x);z0=Math.min(z0,p.z);z1=Math.max(z1,p.z)}
  const cx=(x0+x1)/2,cz=(z0+z1)/2,span=Math.max(x1-x0,(z1-z0)*1.55)+90,eye=[cx,span*.6,cz+span*.56],VP=mul(persp(.7,W/H,2,4000),look(eye,[cx,0,cz+span*.02],[0,1,0]));
  cv.width=W;cv.height=H;gl.viewport(0,0,W,H);gl.clearColor(.62,.78,.52,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.BLEND);
  const S=T.scene,all={bufs:S.bufs.concat(S.cellBufs),clear:S.clear.concat(S.cellClear),sg:S.sg,fogFar:9000};drawScene(all,VP,eye,false);drawSceneClear(all,VP,eye,0);
  const proj=(x,z,y)=>{const v=[x,y||0,z],c=[0,1,3].map(r=>VP[r]*v[0]+VP[4+r]*v[1]+VP[8+r]*v[2]+VP[12+r]);return[(c[0]/c[2]*.5+.5)*100,(1-(c[1]/c[2]*.5+.5))*100]};
  return T.aerial={url:cv.toDataURL("image/jpeg",.88),proj,ratio:W/H}}
let mapGroup="All",mapZoom=1;
function drawBig(){const T=townOf(me.town),A=aerial(T),stage=document.getElementById("stage"),esc2=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  stage.style.width=mapZoom*100+"%";stage.style.aspectRatio=A.ratio;
  let h=`<img src="${A.url}" alt="${me.town} seen from above" draggable="false">`;
  if(route)h+=`<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="${route.pts.map(p=>A.proj(p[0],p[1],.5).map(v=>v.toFixed(2)).join(",")).join(" ")}"/></svg>`;
  T.map.places.forEach((p,i)=>{if(mapGroup!=="All"&&p.group!==mapGroup)return;if(mapGroup==="All"&&p.road)return;const q=A.proj(p.x,p.z,p.road?0:6),on=route&&route.place===p;
    h+=`<button class="pin${on?" on":""}${p.road?" road":""}${mapGroup==="All"&&mapZoom<2&&!on?" small":""}" data-i="${i}" title="${esc2(p.name)}" aria-label="${esc2(p.name)}" style="left:${q[0].toFixed(2)}%;top:${q[1].toFixed(2)}%"><i>${p.icon}</i><span>${esc2(p.name)}</span></button>`});
  const m=A.proj(cam.x,cam.z,1),f=A.proj(cam.x-Math.sin(cam.yaw)*12,cam.z-Math.cos(cam.yaw)*12,1),ang=Math.atan2(f[0]-m[0],-(f[1]-m[1])/A.ratio)*57.3;
  h+=`<div class="mepin" style="left:${m[0].toFixed(2)}%;top:${m[1].toFixed(2)}%;transform:translate(-50%,-50%) rotate(${ang.toFixed(0)}deg)" title="You are here">▲</div>`;stage.innerHTML=h;
  document.querySelectorAll("#mapMenu button").forEach(bt=>bt.classList.toggle("on",bt.dataset.g===mapGroup));return m}
function openMap(){if(scene!=="town"||choosing)return;mapOpen=true;mapZoom=1.5;mapGroup="All";document.getElementById("bigmap").hidden=false;document.getElementById("mapTitle").textContent=me.town.toUpperCase()+(STATES[me.town].capital?"  •  CAPITAL":"");zoomMap(0)}
function zoomMap(d){const vp=document.getElementById("mapView");mapZoom=clamp(mapZoom+d,1,3);const m=drawBig();requestAnimationFrame(()=>{const st=document.getElementById("stage");vp.scrollLeft=st.clientWidth*m[0]/100-vp.clientWidth/2;vp.scrollTop=st.clientHeight*m[1]/100-vp.clientHeight/2})}
document.getElementById("stage").addEventListener("click",e=>{const bt=e.target.closest(".pin");if(bt)choosePlace(townOf(me.town).map.places[+bt.dataset.i])});
document.getElementById("mapMenu").addEventListener("click",e=>{const bt=e.target.closest("button");if(bt){mapGroup=bt.dataset.g;drawBig()}});
document.getElementById("zoomIn").addEventListener("click",()=>zoomMap(.5));document.getElementById("zoomOut").addEventListener("click",()=>zoomMap(-.5));
function closeMap(){mapOpen=false;document.getElementById("bigmap").hidden=true}
function choosePlace(p){if(route&&route.place===p){clearRoute();closeMap();toast("Directions cancelled.");return}setRoute(p);closeMap()}
miniC.addEventListener("click",openMap);document.getElementById("mapClose").addEventListener("click",closeMap);document.getElementById("routeX").addEventListener("click",()=>{clearRoute();toast("Directions cancelled.")});
/* The way from one point to another along the roads. Roads are joined where they cross, where one
   ends against another, and at roundabouts; then the shortest chain of joins is found. */
function findRoute(T,sx,sz,tx,tz){const segs=T.map.roads.map(r=>({a:[r.x0,r.z0],b:[r.x1,r.z1],cuts:[0,1]})),nodes=[],adj=[];
  const node=(x,z)=>{for(let i=0;i<nodes.length;i++)if(Math.hypot(nodes[i][0]-x,nodes[i][1]-z)<1.5)return i;nodes.push([x,z]);adj.push([]);return nodes.length-1};
  const link=(i,j)=>{if(i===j)return;const d=Math.hypot(nodes[i][0]-nodes[j][0],nodes[i][1]-nodes[j][1]);adj[i].push([j,d]);adj[j].push([i,d])};
  const proj=(p,s)=>{const vx=s.b[0]-s.a[0],vz=s.b[1]-s.a[1],t=clamp(((p[0]-s.a[0])*vx+(p[1]-s.a[1])*vz)/(vx*vx+vz*vz),0,1),x=s.a[0]+vx*t,z=s.a[1]+vz*t;return{t,x,z,d:Math.hypot(p[0]-x,p[1]-z),s}};
  for(let i=0;i<segs.length;i++){const s=segs[i];
    for(let j=i+1;j<segs.length;j++){const o=segs[j],d1x=s.b[0]-s.a[0],d1z=s.b[1]-s.a[1],d2x=o.b[0]-o.a[0],d2z=o.b[1]-o.a[1],den=d1x*d2z-d1z*d2x;if(Math.abs(den)<1e-6)continue;                // roads that cross
      const u=((o.a[0]-s.a[0])*d2z-(o.a[1]-s.a[1])*d2x)/den,v=((o.a[0]-s.a[0])*d1z-(o.a[1]-s.a[1])*d1x)/den;if(u>0&&u<1&&v>0&&v<1){s.cuts.push(u);o.cuts.push(v)}}
    for(const end of[s.a,s.b]){for(const o of segs){if(o===s)continue;const q=proj(end,o);if(q.d<17&&q.t>.01&&q.t<.99){o.cuts.push(q.t);link(node(end[0],end[1]),node(q.x,q.z))}                // a road ending against another
        for(const e2 of[o.a,o.b])if(Math.hypot(end[0]-e2[0],end[1]-e2[1])<17)link(node(end[0],end[1]),node(e2[0],e2[1]))}
      for(const r of T.map.rounds)if(Math.hypot(end[0]-r.x,end[1]-r.z)<r.r+10)link(node(end[0],end[1]),node(r.x,r.z))}}
  const nearest=p=>segs.map(s=>proj(p,s)).sort((a,b)=>a.d-b.d)[0],A=nearest([sx,sz]),B=nearest([tx,tz]);A.s.cuts.push(A.t);B.s.cuts.push(B.t);
  for(const s of segs){const ts=[...new Set(s.cuts)].sort((p,q)=>p-q),P=t=>node(s.a[0]+(s.b[0]-s.a[0])*t,s.a[1]+(s.b[1]-s.a[1])*t);for(let i=0;i<ts.length-1;i++)link(P(ts[i]),P(ts[i+1]))}
  const start=node(A.x,A.z),goal=node(B.x,B.z),dist=nodes.map(()=>1e12),prev=nodes.map(()=>-1),done=nodes.map(()=>false);dist[start]=0;
  for(;;){let u=-1;for(let i=0;i<nodes.length;i++)if(!done[i]&&(u<0||dist[i]<dist[u]))u=i;if(u<0||dist[u]>=1e12||u===goal)break;done[u]=true;for(const[v,d]of adj[u])if(dist[u]+d<dist[v]){dist[v]=dist[u]+d;prev[v]=u}}
  const mid=[];if(dist[goal]<1e12)for(let u=goal;u>=0;u=prev[u])mid.unshift(nodes[u]);return[[sx,sz]].concat(mid,[[tx,tz]])}
function setRoute(p){const T=townOf(me.town);route={place:p,pts:findRoute(T,cam.x,cam.z,p.x,p.z)};
  // arrows on the road along the way, and a tall marker at the place itself
  BAKE=null;CLEAR_GLASS=false;CELL=0;reset();const c=[70,200,255];
  for(let i=1;i<route.pts.length-1;i++){const a=route.pts[i],b=route.pts[i+1],L=Math.hypot(b[0]-a[0],b[1]-a[1]),dx=(b[0]-a[0])/L,dz=(b[1]-a[1])/L;
    for(let q=3;q<L-1;q+=7){const x=a[0]+dx*q,z=a[1]+dz*q,tip=[x+dx*1.3,.3,z+dz*1.3],l=[x-dx*.8-dz*1.1,.3,z-dz*.8+dx*1.1],r=[x-dx*.8+dz*1.1,.3,z-dz*.8-dx*1.1];tri(tip,l,r,c,K.glow);tri(tip,r,l,c,K.glow)}}
  box(p.x,0,p.z,.5,30,.5,"#38b6ff",K.glow);box(p.x,30,p.z,3,3,3,"#38b6ff",K.glow);ROUTE_SCENE=upload();ROUTE_SCENE.fogFar=1500;showRoute()}
function clearRoute(){route=null;ROUTE_SCENE=null;document.getElementById("route").hidden=true}
function leftOnRoute(){const P=route.pts;let best=1e9,bi=0,bt=0;for(let i=0;i<P.length-1;i++){const vx=P[i+1][0]-P[i][0],vz=P[i+1][1]-P[i][1],L2=vx*vx+vz*vz||1,t=clamp(((cam.x-P[i][0])*vx+(cam.z-P[i][1])*vz)/L2,0,1),d=Math.hypot(cam.x-P[i][0]-vx*t,cam.z-P[i][1]-vz*t);if(d<best){best=d;bi=i;bt=t}}
  let left=Math.hypot(P[bi+1][0]-P[bi][0],P[bi+1][1]-P[bi][1])*(1-bt);for(let i=bi+1;i<P.length-1;i++)left+=Math.hypot(P[i+1][0]-P[i][0],P[i+1][1]-P[i][1]);return{left,off:best,i:bi}}
function aimArrow(){const P=route.pts,r=leftOnRoute();let i=Math.min(P.length-1,r.i+1);if(i<P.length-1&&Math.hypot(P[i][0]-cam.x,P[i][1]-cam.z)<7)i++;const dx=P[i][0]-cam.x,dz=P[i][1]-cam.z,fx=-Math.sin(cam.yaw),fz=-Math.cos(cam.yaw);
  document.getElementById("routeArrow").style.transform="rotate("+(Math.atan2(dx*-fz+dz*fx,dx*fx+dz*fz)*57.3).toFixed(0)+"deg)"}
function showRoute(){if(!route)return;const r=leftOnRoute(),m=Math.max(0,Math.round(r.left/5)*5);document.getElementById("routeText").textContent="To "+route.place.name+": "+(m>=1000?(m/1000).toFixed(1)+" km":m+" m");document.getElementById("route").hidden=false}
function followRoute(t){if(Math.hypot(cam.x-route.place.x,cam.z-route.place.z)<9){const n=route.place.name;clearRoute();toast("You have arrived at "+n+".");return}
  if(t>routeCheck){routeCheck=t+.5;const r=leftOnRoute();if(r.off>35)setRoute(route.place);else showRoute()}}                     // strayed off the route: work it out again from here

/* ================================ controls ================================ */
const touch=matchMedia("(pointer:coarse)").matches||"ontouchstart" in window;if(touch)document.body.classList.add("touch");
const typing=e=>e.target&&(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA"||e.target.tagName==="SELECT");
addEventListener("keydown",e=>{if(typing(e))return;const k=e.key.toLowerCase();keys[k]=true;if((k==="e"||k==="enter"||k==="f")&&actNow()&&!talking&&!busy)doAct();if(k==="v"&&!talking){view3=!view3;ui()}if(k==="escape"&&talking)closeTalk()});addEventListener("keyup",e=>{keys[e.key.toLowerCase()]=false});
const stick=document.getElementById("stick"),knob=document.getElementById("knob");let stickId=null,lookId=null,lx=0,ly=0;
function stickMove(e){const r=stick.getBoundingClientRect();let dx=(e.clientX-r.left-r.width/2)/(r.width/2),dy=(e.clientY-r.top-r.height/2)/(r.height/2);const l=Math.hypot(dx,dy);if(l>1){dx/=l;dy/=l}input.x=dx;input.y=-dy;knob.style.transform=`translate(${dx*37}px,${dy*37}px)`}
stick.addEventListener("pointerdown",e=>{stickId=e.pointerId;stick.setPointerCapture(e.pointerId);stickMove(e);e.stopPropagation()});stick.addEventListener("pointermove",e=>{if(e.pointerId===stickId)stickMove(e)});
const stickEnd=e=>{if(e.pointerId===stickId){stickId=null;input.x=input.y=0;knob.style.transform=""}};stick.addEventListener("pointerup",stickEnd);stick.addEventListener("pointercancel",stickEnd);
cv.addEventListener("pointerdown",e=>{if(lookId===null){lookId=e.pointerId;lx=e.clientX;ly=e.clientY;cv.setPointerCapture(e.pointerId)}});
cv.addEventListener("pointermove",e=>{if(e.pointerId!==lookId)return;const who=scene==="town"?cam:me;who.yaw+=(e.clientX-lx)*.005;who.pitch=clamp(who.pitch+(e.clientY-ly)*.004,-1.2,1.2);lx=e.clientX;ly=e.clientY});
const lookEnd=e=>{if(e.pointerId===lookId)lookId=null};cv.addEventListener("pointerup",lookEnd);cv.addEventListener("pointercancel",lookEnd);
// The only button at the top is Testing. It holds the controls that are for you, not for players.
function ui(){guide();const el=document.getElementById("picks");el.innerHTML="";const add=(label,fn,on)=>{const bt=document.createElement("button");bt.textContent=label;bt.addEventListener("click",fn);if(on)bt.setAttribute("aria-pressed","true");el.appendChild(bt);return bt};
  if(scene!=="town"&&route)clearRoute();if(scene!=="town")closeMap();
  add(view3?"View: behind me":"View: my eyes",()=>{view3=!view3;ui()});add(testOpen?"Close testing":"Testing",()=>{testOpen=!testOpen;ui()},testOpen);
  if(testOpen){const sel=document.createElement("select");sel.className="who";sel.setAttribute("aria-label","Who you are");for(const[k,label]of ROLES){const o=document.createElement("option");o.value=k;o.textContent="You are: "+label;if(k===me.role)o.selected=true;sel.appendChild(o)}
    sel.addEventListener("change",()=>{const next=sel.value;if(next==="newcomer")return toBorder(true);const was=me.role;me.role=next;if(!me.cert)me.cert=Object.assign({},SAMPLE);if(was==="newcomer"&&scene!=="town"){pickDefault();choosing=false;document.getElementById("choose").hidden=true}ui()});el.appendChild(sel);
    add(SHADOW.on?"Shadows: on":"Shadows: off",()=>{SHADOW.on=!SHADOW.on;ui()},SHADOW.on);
    if(scene==="town"){add(flying?"Flying: on":"Flying: off",()=>{flying=!flying;if(!flying)cam.y=1.7;ui()},flying);if(flying)add("See from above",()=>Object.assign(cam,{x:cam.x,y:380,z:cam.z+10,pitch:-1.54}));
      for(const st of Object.keys(STATES))if(st!==me.town)add("Go to "+st,()=>{clearRoute();toTown(st,"imm",st,9)})}
    if(scene==="bank")add("Leave the bank",()=>toTown(me.town,"bank"));if(scene==="gov")add("Leave the building",()=>toTown(me.town,govSpot));
    if(me.role==="newcomer")add("Skip registration",()=>{pickDefault();choosing=false;document.getElementById("choose").hidden=true;me.role="citizen";me.cert=Object.assign({},SAMPLE);closeTalk();toTown("Asaba","imm","Asaba",9)});
    else if(scene==="imm"||scene==="border")add("Go to the town",()=>toTown(me.entered?me.town:(me.cert&&STATES[me.cert.state]?me.cert.state:"Asaba"),"imm",null,9));
    add("Start again at the border",()=>toBorder(true))}
  const walk=touch?"Left thumb: push up to walk, left or right to turn. Drag elsewhere to look around. ":"W and S walk, A and D turn (or use the arrow keys). Drag to look around. ";
  document.getElementById("tip").textContent={town:walk+(touch?"":"Hold Shift to run. ")+"Tap the round map for directions. Blue doorways lead inside. Walk up to the red car to drive it.",
    border:walk+"Go through the gate and into the blue doorway marked Arrivals.",imm:walk+(touch?"Walk up to Violet to talk to her.":"Walk up to Violet and press E to talk to her."),bank:walk+"The blue doorway is the way out.",gov:walk+"The blue doorway is the way out."}[scene]}
/* The airport's departures board: choose a state and fly there. */
function departures(){choosing=true;const el=document.getElementById("choose");el.hidden=false;
  el.innerHTML=`<div class="card"><h1>${STATES[me.town].air}</h1><p>Departures. Choose where to fly. You arrive outside that state's airport.</p><div class="lab">Flights today</div>
    <div class="looks">${Object.keys(STATES).filter(s=>s!==me.town).map(s=>`<button class="look" data-fly="${s}">${s}<span style="font-weight:500;font-size:12.5px;opacity:.75">${STATES[s].air}</span></button>`).join("")}</div><button class="go" data-stay="1">Stay in ${me.town}</button></div>`}
/* Choosing a character, before anything else: a gender, then one of three outfits. The picture
   of the character chosen is the photograph on the birth certificate. */
const pick={gender:"",outfit:""};
function chooser(){choosing=true;const el=document.getElementById("choose");el.hidden=false;document.getElementById("guide").hidden=true;const ready=ROSTER.ready;
  el.innerHTML=`<div class="card"><h1>Welcome to Delta City</h1><p>Choose your character before you walk to the border gate.</p>
    <div class="lab">Gender</div><div class="seg">${["Male","Female"].map(v=>`<button data-g="${v}" class="${pick.gender===v?"on":""}">${v}</button>`).join("")}</div>
    ${pick.gender?`<div class="lab">Character</div>${ready?`<div class="looks">${ROSTER[pick.gender].map(c=>`<button class="look ${pick.outfit===c.key?"on":""}" data-o="${c.key}"><img src="${PICS[pick.gender][c.key].body}" alt="${c.name}">${c.name}</button>`).join("")}</div>`:`<p>Loading the characters...</p>`}`:""}
    <button class="go" data-go="1" ${pick.gender&&pick.outfit?"":"disabled"}>Enter Delta City</button></div>`}
document.getElementById("choose").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;const shut=()=>{choosing=false;document.getElementById("choose").hidden=true};
  if(b.dataset.g){pick.gender=b.dataset.g;pick.outfit="";chooser()}else if(b.dataset.o){pick.outfit=b.dataset.o;chooser()}
  else if(b.dataset.go){me.gender=pick.gender;me.outfit=pick.outfit;const c=ROSTER[me.gender].find(q=>q.key===me.outfit);if(c)PLAYERS[me.gender]=c.m;shut();guide()}
  else if(b.dataset.stay)shut();else if(b.dataset.fly){const to=b.dataset.fly;shut();toTown(to,"air","Flying to "+to+"...",16)}});
const guide0=guide;guide=function(){guide0();if(choosing)document.getElementById("guide").hidden=true};
ui();chooser();requestAnimationFrame(frame);
Promise.resolve().then(()=>{WALKER.init();return Promise.all([WALKER.load("girl",{idle:"f_idle",walk:"f_walk",jog:"f_jog",back:"f_back"}),WALKER.load("henry",{idle:"m_idle",walk:"m_walk",jog:"m_jog",back:"m_back"}),WALKER.load("c_party2",{idle:"f_idle",walk:"f_walk",jog:"f_jog",back:"f_back"}),WALKER.load("c_club",{idle:"f_idle",walk:"f_walk",jog:"f_jog",back:"f_back"})])}).then(([w,h,p2,club])=>{w.armIn=8;CAST.violet=w;
  // everyone a player can choose, by gender. The first in each list is the default.
  ROSTER.Male=[{key:"henry",name:"Henry",m:h}];ROSTER.Female=[{key:"party",name:"Zoey",m:p2},{key:"club",name:"Tracy",m:club}];PLAYERS.Male=h;PLAYERS.Female=p2;
  // each one's photograph (for the certificate) and full-length picture (for choosing), framed to their own height
  const still={p:0,run:0,amt:0},bg=[.84,.88,.92];for(const g of["Male","Female"])for(const c of ROSTER[g]){const hy=c.m.rest[c.m.index.Head][13],dr=VP=>WALKER.draw(c.m,VP,0,0,0,Math.PI,still,2,null,"");
    PICS[g][c.key]={face:snap(300,396,[.1,hy+.1,.94],[0,hy+.065,0],.5,bg,dr),body:snap(240,440,[.5,hy*.66,hy*2.3],[0,hy*.57,0],.5,bg,dr)}}
  ROSTER.ready=true;
  BAKE=null;CLEAR_GLASS=false;CELL=0;reset();placeModel("m_audi",c=>c[0]>220&&c[1]>220?K.glow:c[0]>220?K.glow:c[0]>150&&c[1]<70?K.gold:c[0]<40&&c[2]>44?K.glass:0);CARSCENE=upload();CARSCENE.twoSided=true;
  if(choosing&&scene==="border")chooser()}).catch(e=>{console.error(e);toast("The characters could not be loaded. You can still play, but pictures will be missing.")});
</script>
</body>
</html>
'''
out=head+play
out=out.replace('<div class="stick" id="stick">','<canvas id="mini" class="mini" width="280" height="280" role="button" tabindex="0" aria-label="Open the map" hidden></canvas>\n<div id="route" class="routebar" hidden><i id="routeArrow" aria-hidden="true">▲</i><span id="routeText"></span><button id="routeX" aria-label="Cancel directions">Cancel</button></div>\n<div id="bigmap" class="bigmap" hidden><div class="mapcard"><div class="maphead"><span class="brand">DELTA CITY</span><b id="mapTitle"></b><button id="mapClose">Close</button></div><div class="mapbody"><div class="mapmenu" id="mapMenu"><button data-g="All">All places</button><button data-g="Districts">Districts</button><button data-g="Roads">Roads</button><button data-g="Transport">Transport</button><button data-g="Government">Government</button><button data-g="Services">Services</button><small>Zoom in, or pick a group, to see names.</small></div><div class="mapview" id="mapView"><div class="stage" id="stage"></div></div><div class="zoom"><button id="zoomIn" aria-label="Zoom in">+</button><button id="zoomOut" aria-label="Zoom out">−</button></div><div class="compass" aria-hidden="true"><b>N</b><i></i></div></div></div></div>\n<div class="stick" id="stick">',1)
CSS=r'''.guide{pointer-events:none}
.mini{position:fixed;left:calc(12px + env(safe-area-inset-left,0px));top:calc(112px + env(safe-area-inset-top,0px));width:140px;height:140px;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 16px rgba(0,0,0,.35);cursor:pointer}
.routebar{position:fixed;left:50%;top:calc(12px + env(safe-area-inset-top,0px));transform:translateX(-50%);background:#1d9bf0;color:#fff;font-weight:700;font-size:15.5px;padding:8px 8px 8px 16px;border-radius:999px;display:flex;gap:10px;align-items:center;box-shadow:0 6px 18px rgba(0,0,0,.25);max-width:92vw}.routebar button{background:rgba(255,255,255,.22);color:#fff;border-color:transparent;padding:6px 12px}
.routebar i{display:inline-block;font-style:normal;font-size:20px;line-height:1;transition:transform .12s linear}
.mapcard .brand{font-weight:800;letter-spacing:1px;margin-right:14px}.maphead{background:#0f1f33;color:#fff}.maphead b{flex:1;font-weight:600;letter-spacing:1px}.maphead button{background:rgba(255,255,255,.16);color:#fff;border-color:transparent}
.mapbody{position:relative}.mapmenu{position:absolute;left:10px;top:10px;z-index:3;background:rgba(15,31,51,.92);border-radius:14px;padding:6px;display:grid;gap:2px;width:150px}.mapmenu button{background:transparent;color:#e7edf5;border-color:transparent;border-radius:10px;text-align:left;font-size:14px;padding:9px 12px}.mapmenu button.on{background:#1d6fd6;color:#fff}.mapmenu small{color:#b9c6d6;font-size:11.5px;padding:6px 10px 4px;line-height:1.3}
.mapview{position:absolute;inset:0;overflow:auto;background:#d4cca8;touch-action:pan-x pan-y}.stage{position:relative}.stage img{display:block;width:100%;height:100%;-webkit-user-drag:none}.stage svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}.stage polyline{fill:none;stroke:#1d9bf0;stroke-width:5;stroke-linejoin:round;stroke-linecap:round;vector-effect:non-scaling-stroke}
.pin{position:absolute;transform:translate(-18px,-100%);display:flex;align-items:center;gap:6px;background:rgba(15,31,51,.93);color:#fff;border:0;border-radius:999px;padding:3px 10px 3px 3px;font-size:12.5px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,.4);margin-top:-8px}.pin::after{content:"";position:absolute;left:14px;bottom:-8px;border:5px solid transparent;border-top:8px solid rgba(15,31,51,.93);border-bottom:0}
.pin i{font-style:normal;width:26px;height:26px;border-radius:50%;background:#1d4ed8;display:grid;place-items:center;font-size:14px;border:2px solid #fff}.pin.small{padding:3px;transform:translate(-16px,-100%)}.pin.small span{display:none}.pin.on{background:#1d9bf0}.pin.on::after{border-top-color:#1d9bf0}.pin.road{background:rgba(255,255,255,.9);color:#111827;padding:2px 9px;transform:translate(-50%,-50%);margin:0}.pin.road i{display:none}.pin.road::after{display:none}
.mepin{position:absolute;color:#e11d48;font-size:26px;line-height:1;text-shadow:0 0 3px #fff,0 0 3px #fff,0 0 6px #fff;pointer-events:none;z-index:2}
.zoom{position:absolute;left:10px;bottom:10px;z-index:3;display:grid;gap:4px}.zoom button{width:44px;height:44px;border-radius:12px;background:rgba(15,31,51,.92);color:#fff;border-color:transparent;font-size:22px;padding:0}
.compass{position:absolute;right:14px;bottom:14px;z-index:3;width:64px;height:64px;border-radius:50%;background:rgba(15,31,51,.92);border:2px solid rgba(255,255,255,.5);color:#fff;display:grid;place-items:start center;font-size:12px}.compass i{position:absolute;left:50%;top:50%;width:0;height:0;border:7px solid transparent;border-bottom:22px solid #e11d48;transform:translate(-50%,-78%)}
.bigmap{position:fixed;inset:0;z-index:6;background:rgba(10,18,32,.72);display:grid;place-items:center;padding:12px;touch-action:auto}.mapcard{width:min(1040px,100%);height:min(680px,100%);background:var(--panel);border-radius:18px;border:1px solid var(--line);display:flex;flex-direction:column;overflow:hidden}.maphead{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;font-size:17px}.mapbody{flex:1;display:flex;min-height:0}.mapwrap{flex:1;min-width:0;position:relative}.mapwrap canvas{position:absolute;inset:0;width:100%;height:100%;cursor:pointer}.places{width:220px;overflow:auto;padding:8px;display:grid;gap:6px;align-content:start;border-left:1px solid var(--line)}.places button{border-radius:10px;text-align:left;white-space:normal;font-size:13.5px;padding:8px 10px}.places button.on{background:#1d9bf0;color:#fff;border-color:#1d9bf0}
@media (max-width:760px){.mini{width:112px;height:112px;top:calc(96px + env(safe-area-inset-top,0px))}.mapmenu{width:auto;grid-auto-flow:column;top:6px;left:6px;right:6px;overflow-x:auto}.mapmenu button{white-space:nowrap;padding:8px 10px}.picks{top:calc(10px + env(safe-area-inset-top,0px));left:auto}}
select.who{font:inherit;font-weight:600;font-size:14px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:999px;padding:8px 12px;max-width:min(78vw,340px)}'''
out=out.replace("[hidden]{display:none !important}","[hidden]{display:none !important}\n"+CSS,1)
MODELS="".join('<script type="application/json" id="%s">%s</script>\n'%(i,open('/home/claude/w/models/'+f).read()) for i,f in (("m_terminal","terminal.json"),("m_audi","audi.json"),("henry","henry.json"),("girl","../game3d/woman.json"),("c_party2","party2.json"),("c_club","club.json"),("anims","../anim/anims.json")))
out=out.replace('<canvas id="mini"',MODELS+'<canvas id="mini"',1)
open('town.html','w',encoding='utf-8').write(out)
js=out[out.rindex('<script>')+8:out.rindex('</script>')]; open('/tmp/town.js','w').write(js)
print('built',len(out),'|',subprocess.run(['node','--check','/tmp/town.js'],capture_output=True,text=True).stderr[:600] or 'syntax ok')
