/* ====================== government interiors: one builder, three kinds of building ======================
   Each has an entrance lobby, a central corridor with rooms either side, and (for the two
   government houses) a chamber at the far end. Who may enter each room follows the Discord
   server's permissions exactly. */
const G_CEIL=3.8,G_LW=24,G_LD=10,G_RD=7,G_SP=1.7,G_CW=20,G_CD=10;
const ALL_FED=["president","vp","cos","minister","fedcouncil","governor","ssg","cg","deputy"],VILLA3=["president","vp","villavisitor"];
const GOV_SPEC={
  state:st=>({title:st+" State Government House",silver:true,pal:{wall:"#F0EEE7",feat:"#176B70",trim:"#7F929B",carpet:"#1d5a5f",wood:"#6b4a30",floor:"#E6E7E3"},enter:null,noEntry:"",
    sign:st.toUpperCase()+" STATE GOVERNMENT",notice:true,
    west:[{name:"SECRETARY TO THE STATE GOVERNMENT",plate:"SSG",w:9,who:["governor","ssg","govvisitor"]}],
    east:[{name:"GOVERNOR OF "+st.toUpperCase()+" STATE",plate:"GOVERNOR",w:9,who:["governor","ssg"],big:true}],
    head:{name:"STATE COUNCIL CHAMBER",plate:"STATE COUNCIL",who:["governor","ssg","council"],seats:12}}),
  federal:()=>({title:"Federal Government Building",pal:{wall:"#E9E5DC",feat:"#14263D",trim:"#B99A5D",carpet:"#1b3355",wood:"#4a3222",floor:"#ECE9E1"},enter:ALL_FED,noEntry:"The Federal Government Building is open only to federal officials, Governors and Secretaries to the State Government.",
    sign:"FEDERAL GOVERNMENT OF DELTA CITY",
    west:[{name:"PRESIDENT OF DELTA CITY",plate:"PRESIDENT",w:10,who:["president","vp"],big:true},{name:"CHIEF OF STAFF",plate:"CHIEF OF STAFF",w:7,who:["president","vp","cos","fedcouncil"]},{name:"MINISTRY OF FINANCE",plate:"FINANCE",w:7,who:["minister","fedcouncil"]},{name:"ATTORNEY-GENERAL",plate:"ATTORNEY-GENERAL",w:7,who:["fedcouncil"]},{name:"MINISTER OF EDUCATION",plate:"EDUCATION",w:7,who:["fedcouncil"]},{name:"MINISTER OF TRANSPORTATION",plate:"TRANSPORTATION",w:7,who:["fedcouncil"]}],
    east:[{name:"VICE PRESIDENT",plate:"VICE PRESIDENT",w:10,who:["president","vp","cos"],big:true},{name:"MINISTER OF HEALTH",plate:"HEALTH",w:7,who:["fedcouncil"]},{name:"HOUSING & INFRASTRUCTURE",plate:"HOUSING & INFRASTRUCTURE",w:7,who:["fedcouncil"]},{name:"AGRICULTURE & RESOURCES",plate:"AGRICULTURE & RESOURCES",w:7,who:["fedcouncil"]},{name:"INFORMATION, CULTURE & HERITAGE",plate:"INFORMATION & CULTURE",w:7,who:["fedcouncil"]}],
    head:{name:"FEDERAL CHAMBERS",plate:"FEDERAL CHAMBERS",who:["president","vp","cos","minister","governor","ssg","cg","deputy"],seats:18}}),
  villa:()=>({title:"Presidential Villa",pal:{wall:"#ffffff",feat:"#14263D",trim:"#B99A5D",carpet:"#5a2a2f",wood:"#4a3222",floor:"#EFEDE6"},enter:VILLA3,noEntry:"The Presidential Villa is open only to the President, the Vice President and their invited visitors.",
    sign:"PRESIDENTIAL VILLA",
    west:[{name:"PRESIDENT'S PENTHOUSE",plate:"PRESIDENT'S PENTHOUSE",w:11,who:VILLA3,suite:true,big:true},{name:"VISITOR VILLA 1",plate:"VISITOR VILLA 1",w:8,who:VILLA3,suite:true}],
    east:[{name:"VICE PRESIDENT'S PENTHOUSE",plate:"VICE PRESIDENT'S PENTHOUSE",w:11,who:VILLA3,suite:true,big:true},{name:"VISITOR VILLA 2",plate:"VISITOR VILLA 2",w:8,who:VILLA3,suite:true}],head:null})};
function govPlan(S){const sum=a=>a.reduce((t,r)=>t+r.w,0),SL=Math.max(sum(S.west),sum(S.east)),rooms=[];
  for(const[side,list]of[[-1,S.west],[1,S.east]]){let z=0;for(const r of list){rooms.push(Object.assign({side,z0:z,z1:z-r.w,zc:z-r.w/2},r));z-=r.w}}
  return{SL,rooms,end:-SL-(S.head?G_CD:0)}}
function govInside(S){const P=S.pal,{SL,rooms,end}=govPlan(S),H=G_CEIL,X0=G_SP,X1=G_SP+G_RD,sign2=(x,y,z,w,h,t,bg,fg,turn)=>(S.silver?plate:label)(x,y,z,w,h,t,bg,fg,turn);
  const lamp=(x,z)=>{box(x,H-.05,z,1.3,.05,.64,"#fffdf4",K.glow);box(x,H-.03,z,1.44,.03,.78,P.trim,K.gold)};
  // floors, ceiling and lamps
  floorGrid(-G_LW/2,0,G_LW/2,G_LD,0,P.floor,K.tile,.5);floorGrid(-X1,-SL,X1,0,0,P.floor,K.tile,.5);if(S.head)floorGrid(-G_CW/2,end,G_CW/2,-SL,0,P.floor,K.tile,.5);
  ceilGrid(-G_LW/2,end,G_LW/2,G_LD,H,"#ffffff",2);box(0,.004,-SL/2+1,2.2,.008,SL+2,P.carpet,K.fabric);for(const s of[-1,1])box(s*1.14,.006,-SL/2+1,.06,.008,SL+2,P.trim,K.gold);
  for(const p of govLights(S))lamp(p[0],p[2]);
  // ---- the lobby
  wallRun(-G_LW/2,G_LD,-1.5,G_LD,0,H,P.wall);wallRun(1.5,G_LD,G_LW/2,G_LD,0,H,P.wall);box(0,2.7,G_LD,3,H-2.7,.2,P.wall);for(const s of[-1,1])wallRun(s*G_LW/2,0,s*G_LW/2,G_LD,0,H,P.wall);
  entrance(0,0,G_LD-.1,2.9,2.6,Math.PI,true);sign2(0,2.9,G_LD-.14,1.4,.32,"EXIT",P.feat,"#ffffff",Math.PI);
  wallRun(-G_LW/2,0,-X0,0,0,H,P.feat);wallRun(X0,0,G_LW/2,0,0,H,P.feat);box(0,2.6,0,X0*2,H-2.6,.2,P.feat);
  sign2(0,2.86,.12,X0*2-.4,.34,S.head?"OFFICES  ↑  "+S.head.plate:"RESIDENCES  ↑",P.feat,"#ffffff");
  for(const s of[-1,1]){sign2(s*6.9,2.5,.12,8.4,.62,S.sign,P.feat,S.silver?"#ffffff":"#e6cf9a");discZ(s*6.9,1.5,.13,.62,P.trim,K.gold,26);discZ(s*6.9,1.5,.14,.5,P.feat,0,26);discZ(s*6.9,1.5,.15,.2,P.trim,K.gold,5);flag(s*11,.9,3.3);box(s*6.9,.12,.14,9,.05,.05,P.trim,K.glow)}
  at(-6.5,5.2,0,()=>{box(0,0,0,4.4,1.08,.8,P.feat);box(0,.5,.41,4.4,.07,.02,P.trim,K.gold);box(0,1.08,0,4.6,.06,1,"#ffffff",K.tile);box(-1,1.14,-.1,.5,.34,.04,"#161b22");stands(0,0,4.4,.8);solid(0,0,4.4,.9)});chair(-6.5,4.3,0,"#2a2f38");sign2(-6.5,1.5,5.2,2.2,.3,"RECEPTION",P.feat,"#ffffff");for(const s of[-1,1])cyl(-6.5+s*1.2,1.14,5.2,.03,.4,P.trim,6);
  sofa(7,7.6,Math.PI,3);sofa(10.4,4.6,-Math.PI/2,2);lowTable(7,5.4);box(7.6,.006,6,7,.01,5.4,P.carpet,K.fabric);for(const[x,z]of[[-11,9],[11,9],[11,1]])palmPot(x,z);
  if(S.notice){at(G_LW/2-.14,5,-Math.PI/2,()=>{box(0,1.2,0,4.2,1.9,.05,"#3a4756");for(let r=0;r<2;r++)for(let k=0;k<5;k++)box(-1.7+k*.85,1.36+r*.86,.04,.7,.72,.02,["#ffffff","#fdf3c4","#d6f1ee","#ffffff","#e8ecf8"][(r*5+k)%5])});sign2(G_LW/2-.14,3.2,5,3,.34,"STATE NOTICE",P.feat,"#ffffff",-Math.PI/2)}
  // ---- the corridor walls, with a doorway to each room, and the rooms themselves
  for(const s of[-1,1]){const list=rooms.filter(r=>r.side===s);let z=0;for(const r of list){wallRun(s*X0,r.z0,s*X0,r.zc+.7,0,H,P.wall);wallRun(s*X0,r.zc-.7,s*X0,r.z1,0,H,P.wall);box(s*X0,2.15,r.zc,.2,H-2.15,1.4,P.wall);z=r.z1;
      sign2(s*(X0-.12),2.3,r.zc,Math.min(2.6,.2+r.plate.length*.13),.3,r.plate,P.feat,"#ffffff",s>0?-Math.PI/2:Math.PI/2);wallRun(s*X0,r.z1,s*X1,r.z1,0,H,P.wall);
      box(s*(X0+G_RD/2),.004,r.zc,G_RD-.4,.008,r.w-.5,P.carpet,K.fabric);govRoom(S,r)}
    if(z>-SL)wallRun(s*X0,z,s*X0,-SL,0,H,P.wall);wallRun(s*X1,0,s*X1,Math.max(z,-SL),0,H,P.wall)}
  // ---- the chamber at the far end
  if(S.head){const z0=-SL,cz=z0-G_CD/2;wallRun(-G_CW/2,z0,-.8,z0,0,H,P.wall);wallRun(.8,z0,G_CW/2,z0,0,H,P.wall);box(0,2.2,z0,1.6,H-2.2,.2,P.wall);sign2(0,2.34,z0+.12,2.6,.34,S.head.plate,P.feat,"#ffffff");
    for(const s of[-1,1])wallRun(s*G_CW/2,end,s*G_CW/2,z0,0,H,P.wall);wallRun(-G_CW/2,end,G_CW/2,end,0,H,P.feat);
    const n=S.head.seats,per=Math.floor((n-2)/2),L=per*1.05+1;box(0,.004,cz,L+4,.008,G_CD-1.4,P.carpet,K.fabric);box(0,.74,cz,L,.08,1.8,P.wood,K.wood);box(0,0,cz,L-.6,.74,1.1,P.feat);stands(0,cz,L,1.8);solid(0,cz,L,1.8);
    for(let k=0;k<per;k++){chair(-L/2+.8+k*1.05,cz+1.45,Math.PI,"#2a2f38");chair(-L/2+.8+k*1.05,cz-1.45,0,"#2a2f38");box(-L/2+.8+k*1.05,.83,cz+.5,.3,.02,.2,"#ffffff");box(-L/2+.8+k*1.05,.83,cz-.5,.3,.02,.2,"#ffffff")}
    chair(-L/2-.6,cz,Math.PI/2,"#161b22");chair(L/2+.6,cz,-Math.PI/2,"#161b22");sign2(0,2.5,end+.14,7,.6,S.head.name,P.feat,S.silver?"#ffffff":"#e6cf9a");box(0,1.1,end+.14,4.4,1.1,.05,"#0b1730");box(0,1.16,end+.17,4.2,.98,.02,"#a7d8f2",K.glow);for(const s of[-1,1])flag(s*4.6,end+.7,3.2)}
  else wallRun(-X1,-SL,X1,-SL,0,H,P.feat)}
function govRoom(S,r){const P=S.pal,s=r.side,xo=s*(G_SP+G_RD-.14),dT=s<0?-Math.PI/2:Math.PI/2,cx=s*(G_SP+G_RD-2.2),name=(x,y,z,w,h,t)=>(S.silver?plate:label)(x,y,z,w,h,t,P.feat,S.silver?"#ffffff":"#e6cf9a",s<0?Math.PI/2:-Math.PI/2);
  name(xo,2.5,r.zc,Math.min(r.w-1.4,5.4),.44,r.name);
  if(r.suite){at(s*(G_SP+G_RD-1.5),r.zc-r.w/2+2.4,-dT,()=>{box(0,.24,0,2,.34,2.2,"#f5f1e8",K.fabric);box(0,0,0,2.1,.24,2.3,P.wood,K.wood);box(0,.58,-1,2.1,.9,.12,P.feat,K.fabric);box(-.5,.58,-.7,.6,.14,.4,"#ffffff",K.fabric);box(.5,.58,-.7,.6,.14,.4,"#ffffff",K.fabric);box(0,.58,.5,2,.06,1,P.carpet,K.fabric);stands(0,0,2.1,2.3);solid(0,0,2.1,2.3)});
    box(xo-s*.3,0,r.zc+r.w/2-1.6,.6,2.1,2.2,P.wood,K.wood);stands(xo-s*.3,r.zc+r.w/2-1.6,.6,2.2);sofa(s*(G_SP+1.2),r.zc+(r.big?2.4:1.6),dT,2);lowTable(s*(G_SP+2.7),r.zc+(r.big?2.4:1.6));
    if(r.big){at(s*(G_SP+3.4),r.z0-1.3,0,()=>{box(0,.74,0,2.2,.06,1,P.wood,K.wood);for(const a of[-1,1])box(a*1,0,0,.08,.74,.9,P.wood,K.wood);stands(0,0,2.2,1);solid(0,0,2.2,1)});chair(s*(G_SP+3.4),r.z0-2.2,0,"#2a2f38");flag(xo-s*.6,r.z0-.8,3)}
    return}
  desk(cx,r.zc,dT,r.big?2.5:2,P.wood,P.feat);chair(cx+s*.95,r.zc,-dT,"#161b22");chair(cx-s*1.3,r.zc-.6,dT,"#2a2f38");chair(cx-s*1.3,r.zc+.6,dT,"#2a2f38");
  flag(xo-s*.5,r.z0-.9,3);box(xo-s*.26,0,r.z1+1.6,.5,2,2.4,P.wood,K.wood);for(let k=0;k<4;k++)box(xo-s*.54,.3+k*.44,r.z1+1.6,.04,.34,2.2,k%2?P.feat:"#d9d4c8");stands(xo-s*.26,r.z1+1.6,.5,2.4);
  if(r.big){sofa(s*(G_SP+1.2),r.z0-2.2,dT,2);palmPot(xo-s*.7,r.z1+3.8)}}
function govLights(S){const{SL,end}=govPlan(S),L=[],X1=G_SP+G_RD;for(let x=-8;x<=8;x+=4)for(let z=8;z>=end+1;z-=4){const inLobby=z>0,inRooms=z<0&&z>-SL&&Math.abs(x)<X1,inHead=S.head&&z<-SL;if(inLobby||inRooms||inHead)L.push([x,G_CEIL-.2,z,.22,4])}return L}
const GOV_CACHE={};
function govOf(kind,st){const key=kind==="state"?"state:"+st:kind;if(GOV_CACHE[key])return GOV_CACHE[key];const S=GOV_SPEC[kind](st),lights=govLights(S),plan=govPlan(S);
  const lit=fn=>{const s=captureLit(fn,lights,false,G_CEIL);s.ceil=[G_CEIL,G_CEIL];return s},scene=lit(()=>govInside(S)),walls=WALLS.slice(),gates=[],doors=[];
  const leaf=(x,z,open,side,color)=>{if(open)box(x+side*.12,0,z-.75-.62,.07,2.15,1.24,color);else{box(x,0,z,.08,2.15,1.36,color);box(x-side*.07,1,z+.5,.05,.07,.07,S.pal.trim,K.gold)}};
  for(const r of plan.rooms){const x=r.side*G_SP;gates.push({who:r.who,r:[x-.18,r.zc-.7,x+.18,r.zc+.7],msg:r.plate+": you do not have access to this room."});doors.push({who:r.who,shut:lit(()=>leaf(x,r.zc,false,r.side,S.pal.wood)),open:lit(()=>leaf(x,r.zc,true,r.side,S.pal.wood))})}
  if(S.head){gates.push({who:S.head.who,r:[-.8,-plan.SL-.18,.8,-plan.SL+.18],msg:S.head.plate+": you do not have access to this chamber."});
    doors.push({who:S.head.who,shut:lit(()=>{box(0,0,-plan.SL,1.56,2.2,.08,S.pal.wood,K.wood);box(.6,1,-plan.SL+.07,.07,.07,.05,S.pal.trim,K.gold)}),open:lit(()=>{box(-1.6,0,-plan.SL-.16,1.5,2.2,.07,S.pal.wood,K.wood)})})}
  return GOV_CACHE[key]={S,scene,walls,gates,doors,end:plan.end,title:S.title}}
