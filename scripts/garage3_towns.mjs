// Three simultaneous spawned vehicles: replaces the single TOWNS[st].car slot with a
// per-town collection (T.cars) plus a focus pointer (T.car) used by panels/doors/prompts.
import { readFileSync, writeFileSync } from "node:fs";
const F="index.html";
const s0=readFileSync(F,"utf8");
const out=[s0];let n=0;
const put=(old,new2)=>{
  const i=out[n].indexOf(old);
  if(i<0)throw new Error("NOT FOUND ["+n+"]: "+old.slice(0,80));
  if(out[n].indexOf(old,i+1)>=0)throw new Error("AMBIGUOUS ["+n+"]: "+old.slice(0,80));
  n++;out[n]=out[n].slice(0,i)+new2+out[n].slice(i+old.length)};

/* 1 — town vehicle collection + focus, right before garMine */
put("function garMine(){",
`// up to three of your vehicles can be out in one town at once. T.cars is the collection; T.car is the one
// in focus (the one being driven, or, on foot, the nearest) — doors, prompts and the vehicle panels follow it.
const GAR_MAXCARSTOWN=3;let DRIVEN=null;
function tCars(T){if(!T.cars)T.cars=[];if(T.car&&T.cars.indexOf(T.car)<0)T.cars.push(T.car);return T.cars}
function tHas(T,vid){return vid!=null&&tCars(T).some(C=>C.vid===vid)}
function tFocus(){const T=townOf(me.town);if(!T)return;if(!tCars(T).length){T.car=null;return}
  let best=T.cars[0],bd=1e9;for(const C of T.cars){if(!C)continue;const d=(driving&&C===DRIVEN)?-1:Math.hypot(C.x-cam.x,C.z-cam.z);if(d<bd){bd=d;best=C}}T.car=best}
function garMine(){`)

/* 2 — the kick-out in garGone releases the driven-car lock */
put("if(driving&&townOf(me.town)===T){const p=carPt(C,carDoors(C).driver.stand);driving=false;C.v=0;",
"if(driving&&townOf(me.town)===T){const p=carPt(C,carDoors(C).driver.stand);driving=false;DRIVEN=null;C.v=0;")

/* 3 — carSeated locks the driven car */
put("function carSeated(C){driving=true;VEH.belt=false;",
"function carSeated(C){driving=true;DRIVEN=C;VEH.belt=false;")

/* 4 — carExit releases it */
put("const seat=carPt(C,door.seat);driving=false;C.v=0;VEH.gear=\"P\";VEH.ind=\"off\";vehicleLetGo();sndUpdate(false);dashUpdate();",
"const seat=carPt(C,door.seat);driving=false;DRIVEN=null;C.v=0;VEH.gear=\"P\";VEH.ind=\"off\";vehicleLetGo();sndUpdate(false);dashUpdate();")

/* 5 — spawn branch: no more auto-replacing the old copy */
put("const v=r.vehicle,T=townOf(P.st),B=P.bays[v.in_bay||0],M=garMine();if(M&&!(r.already&&M.C.vid===v.id))garGone(M.T,M.C,\"\");       // the old copy (this car elsewhere, or my other car) goes\n      if(!(r.already&&garMine()))garPlace(T,v,B.x,B.z,B.yaw,v.damage&&Object.keys(v.damage).length?v.damage:null);",
`const v=r.vehicle,T=townOf(P.st),B=P.bays[v.in_bay||0];
      if(tHas(T,v.id)){say("That vehicle is already out in "+T.name+". Drive to it or store it first.",true);return garDraw()}
      if(tCars(T).length>=GAR_MAXCARSTOWN){say("Your garage here is full: three vehicles can be out at once. Store one first.",true);return garDraw()}
      garPlace(T,v,B.x,B.z,B.yaw,v.damage&&Object.keys(v.damage).length?v.damage:null);`)

/* 6 — garResume: every out vehicle is restored (up to three per town) */
put("function garResume(){const v=GAR.list.find(q=>q.out_by_me&&q.token),M=garMine();\n  if(M&&(!v||v.id!==M.C.vid)){garGone(M.T,M.C,\"Your car was taken back to the car park.\");return}\n  if(!v||M||v.state!==me.town)return;const T=townOf(v.state);let x,z,yaw;\n  if(v.pos&&isFinite(v.pos.x)){x=v.pos.x;z=v.pos.z;yaw=v.pos.yaw||0}else{const P=(T.parks||[]).find(p=>p.id===v.park),B=P&&P.bays[v.in_bay||0];if(!B)return;x=B.x;z=B.z;yaw=B.yaw}\n  let dmg=v.damage&&Object.keys(v.damage).length?v.damage:null;const s=T.savedCar;if(s&&s.vid===v.id){dmg=Object.assign({},s);delete dmg.pos;delete dmg.vid}T.savedCar=null;\n  garPlace(T,v,x,z,yaw,dmg)}",
`function garResume(){const outs=GAR.list.filter(q=>q.out_by_me&&q.token);
  for(const M of[...tCars(myTown()),...Object.values(TOWNS).flatMap(T=>tCars(T))])if(!outs.some(q=>q.id===M.vid)&&!tCars(myTown()).includes(M))garGone(myTown(),M,"Your car was taken back to the car park.");
  for(const v of outs.slice(0,GAR_MAXCARSTOWN)){const T=townOf(v.state);if(!T||v.state!==me.town||tHas(T,v.id))continue;
    let x,z,yaw;if(v.pos&&isFinite(v.pos.x)){x=v.pos.x;z=v.pos.z;yaw=v.pos.yaw||0}else{const P=(T.parks||[]).find(p=>p.id===v.park),B=P&&P.bays[v.in_bay||0];if(!B)continue;x=B.x;z=B.z;yaw=B.yaw}
    let dmg=v.damage&&Object.keys(v.damage).length?v.damage:null;const s=T.savedCar;if(s&&s.vid===v.id){dmg=Object.assign({},s);delete dmg.pos;delete dmg.vid}T.savedCar=null;
    garPlace(T,v,x,z,yaw,dmg)}}`)

/* 7 — fire: any car in the town can burn */
put("function fireLamps(T){const C=T&&T.car,D=C&&C.dmg;if(!D||!(D.fire>0))return[];const p=carWorld(C,[0,1.5,CARFX.engine[2]]);return[[p[0],p[1],p[2],(.8+.25*Math.random())*(.6+D.fire),\"f\"]];}",
"function fireLamps(T){const L=[];for(const C of(T?tCars(T):[])){const D=C.dmg;if(!D||!(D.fire>0))continue;const p=carWorld(C,[0,1.5,CARFX.engine[2]]);L.push([p[0],p[1],p[2],(.8+.25*Math.random())*(.6+D.fire),\"f\"])}return L}")

/* 8 — every car in the town simulates (engine heat, leaks, fire) */
put("if(scene===\"town\")carSim(townOf(me.town),dt);",
"if(scene===\"town\")for(const C of tCars(T))carSim(T,dt,C);")

/* 9 — every car's frame advances (wheels, doors, poses) */
put("if(scene===\"town\"&&T.car&&CARSCENE)carPose(T.car,dt);else if(T.car)carMesh(T.car);if(T.car&&CARSCENE)carPose(T.car,dt);",
"if(scene===\"town\")for(const C of tCars(T)){if(CARSCENE)carPose(C,dt);else carMesh(C);if(CARSCENE)carPose(C,dt)}")

/* 10 — the camera avoids every parked car, not just the focused one */
put("  const C=T.car,hitT=(x,z,r)=>T.blocks.some(w=>x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r);",
`  const C=T.car,hitT=(x,z,r)=>T.blocks.some(w=>x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r)||tCars(T).some(w=>{const q=carWorld(w,[0,0,0]);return Math.hypot(x-q[0],z-q[2])<(w.dmg&&w.dmg.model===\"m_bike\")?1.2:2.4});`)

/* 11 — every car in the town is drawn */
put("    if(T.car)carDraw(VP,eye,false,false);",
"    if(tCars(T).length)for(const C of tCars(T)){carMesh(C);if(CARSCENE)carPose(C,dt);carDraw(VP,eye,false,false)}")

/* 12 — dynamic collision: parked cars block movement too */
put("const dynLay=T=>{const d=T.map.dyn||[],c=T.car;",
"const dynLay=T=>{const d=T.map.dyn||[],cs=tCars(T);")

writeFileSync(F,out[out.length-1]);
console.log("ok edits="+n);