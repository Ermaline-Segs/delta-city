/* ====================== the Delta City Immigration Authority ======================
   Colours: the Official Authority palette. Public rooms are bright; inspection and
   restricted rooms use the darker navy and slate. */
const CW="#F4F6F8",MN="#14263D",TEAL="#167C80",SLATE="#AAB5C0",SILVER="#C9D0D6",DSLATE="#202D3A",FLOOR="#E4E8EB",FLOOR_D="#8f9aa4",CHAR="#2a3340";
const CEIL=4.2;
function plate(x,y,z,w,h,text,bg,fg,turn){at(x,z,turn||0,()=>{box(0,y-.04,-.03,w+.1,h+.08,.04,SILVER,K.gold);sign(0,y,0,w,h,text,bg||MN,fg||"#ffffff")})}
// a sign hung from the ceiling, readable from the entrance side
function hanging(x,z,w,text,bg){for(const s of[-1,1])box(x+s*(w/2-.2),3.5,z,.03,CEIL-3.5,.03,SILVER);box(x,3.0,z,w+.1,.52,.08,SILVER,K.gold);sign(x,3.03,z+.045,w,.46,text,bg||TEAL,"#ffffff")}
function ball(x,y,z,rx,ry,rz,color,n){const c=hex(color),N=n||10;const P=(a,b)=>[x+Math.sin(a)*Math.cos(b)*rx,y+Math.cos(a)*ry,z+Math.sin(a)*Math.sin(b)*rz];
  for(let i=0;i<N;i++)for(let j=0;j<N*2;j++){const a0=i/N*Math.PI,a1=(i+1)/N*Math.PI,b0=j/(N*2)*6.2832,b1=(j+1)/(N*2)*6.2832;quad(P(a0,b0),P(a0,b1),P(a1,b1),P(a1,b0),c)}}
function seats(x,z,turn,n){at(x,z,turn,()=>{const L=n*.62;box(0,.3,0,L,.06,.08,SILVER,K.gold);for(const s of[-1,1]){box(s*(L/2-.2),0,0,.06,.3,.5,SILVER,K.gold)}
  for(let k=0;k<n;k++){const sx=-L/2+.31+k*.62;box(sx,.36,.02,.54,.07,.5,SLATE,K.fabric);box(sx,.43,-.22,.54,.5,.06,SLATE,K.fabric)}for(let k=0;k<=n;k++)box(-L/2+k*.62,.5,.02,.05,.05,.44,SILVER,K.gold);stands(0,0,L,.6);solid(0,0,L,.6)})}
function belts(pts){for(const[x,z]of pts){cyl(x,0,z,.17,.04,SILVER,10);cyl(x,.04,z,.04,.95,SILVER,8);cyl(x,.99,z,.06,.06,MN,8);stands(x,z,.3,.3)}
  for(let k=0;k<pts.length-1;k++){const[a,b]=pts[k],[c,d]=pts[k+1];box((a+c)/2,.86,(b+d)/2,Math.abs(c-a)||.03,.09,Math.abs(d-b)||.03,MN)}}
function serviceCounter(x,z,w,turn,glass){at(x,z,turn,()=>{box(0,0,0,w,1.08,.8,MN);box(0,.12,.41,w-.3,.8,.02,TEAL);box(0,1.08,0,w+.2,.06,1.0,CW,K.tile);box(0,0,.42,w,.1,.03,SILVER,K.gold);
  if(glass){box(0,1.14,.1,w,1.25,.04,"#cfe6f2",K.glass);box(0,2.39,.1,w+.1,.06,.1,SILVER,K.gold)}stands(0,0,w,.9);solid(0,0,w,.95)})}
function workDesk(x,z,turn,w){at(x,z,turn,()=>{const W=w||1.6;box(0,.72,0,W,.05,.8,SLATE);for(const s of[-1,1])box(s*(W/2-.04),0,0,.05,.72,.74,SILVER,K.gold);box(0,.3,-.34,W-.1,.42,.03,CHAR);
  box(.3,.78,.02,.54,.34,.04,"#161b22");box(.3,.8,.045,.48,.28,.01,"#a7d8f2",K.glow);box(.3,.77,.02,.14,.03,.16,"#161b22");box(-.38,.775,.1,.34,.02,.24,"#ffffff");stands(0,0,W,.8);solid(0,0,W,.8)})}
function workChair(x,z,turn,color){at(x,z,turn,()=>{const c=color||CHAR;box(0,.42,0,.5,.09,.5,c);box(0,.51,-.23,.5,.5,.07,c);cyl(0,0,0,.24,.04,SILVER,8);cyl(0,.04,0,.035,.38,SILVER,6);stands(0,0,.5,.5)})}
function fileShelves(x,z,turn,w){at(x,z,turn,()=>{const W=w||2.4;box(0,0,0,W,2.2,.45,CHAR);for(let r=0;r<5;r++){box(0,.12+r*.42,.02,W-.1,.36,.42,"#3a4756");for(let k=0;k<W/.11-1;k++)box(-W/2+.1+k*.11,.14+r*.42,.19,.085,.3,.1,["#167C80","#AAB5C0","#F4F6F8","#14263D","#c9a13a"][(k*7+r*3)%5])}stands(0,0,W,.5);solid(0,0,W,.5)})}
function greenery(x,z){cyl(x,0,z,.3,.6,SILVER,10,.36);cyl(x,.6,z,.05,.9,"#5b4a2e",6);for(let k=0;k<7;k++)at(x,z,k/7*6.2832,()=>{const g=hex("#2f8f4b");both([0,1.45,-.08],[.6,1.85,-.16],[.6,1.85,.16],[0,1.45,.08],g);both([.6,1.85,-.16],[1.05,1.45,-.05],[1.05,1.45,.05],[.6,1.85,.16],g.map(v=>v*.85))});stands(x,z,.8,.8);solid(x,z,.6,.6)}
function lampPanel(x,z){box(x,CEIL-.05,z,1.3,.05,.64,"#fbfdff",K.glow);box(x,CEIL-.03,z,1.42,.03,.76,SILVER)}

const VIOLET={x:0,z:-.15};
const GLOW_T="#49d6d0",GLOW_W="#f4fbff";
function pillar(x,z){cyl(x,0,z,.42,.16,SILVER,16);cyl(x,.16,z,.3,CEIL-.5,CW,16);cyl(x,1.1,z,.31,.12,TEAL,16);cyl(x,CEIL-.34,z,.3,.34,SILVER,16,.44);stands(x,z,.84,.84);solid(x,z,.66,.66)}
function doorFrame(x,z,w,h,along){const t=.12;if(along){for(const s of[-1,1])box(x+s*(w/2+t/2),0,z,t,h+t,.3,SILVER,K.gold);box(x,h,z,w+t*2,t,.3,SILVER,K.gold)}else{for(const s of[-1,1])box(x,0,z+s*(w/2+t/2),.3,h+t,t,SILVER,K.gold);box(x,h,z,.3,t,w+t*2,SILVER,K.gold)}}
function bin(x,z){cyl(x,0,z,.2,.62,SILVER,10);cyl(x,.62,z,.21,.05,CHAR,10);stands(x,z,.4,.4)}
function immigrationInside(){
  // ---- floor: polished stone with a slate border and teal paths; ceiling with beams between the lamps
  floorGrid(-15,-2,15,11,0,"#DCE1E5",K.tile,.5);floorGrid(-15,-11,15,-2,0,"#7f8a95",K.tile,.5);ceilGrid(-15,-11,15,11,CEIL,"#ffffff",2);
  for(const[x,z,w,d]of[[0,10.2,29,.5],[0,-1.3,29,.5],[-14.2,4.5,.5,11.2],[14.2,4.5,.5,11.2]])box(x,0,z,w,.006,d,SLATE,K.tile);
  box(0,.004,5.4,2.2,.008,7.8,TEAL,K.tile);box(-7.9,.004,4.2,13.6,.008,1.6,TEAL,K.tile);for(const[x,z,w,d]of[[-1.14,5.4,.06,7.8],[1.14,5.4,.06,7.8]])box(x,.006,z,w,.008,d,"#0f5f62",K.tile);
  for(let x=-12;x<=12;x+=4)for(const z of[8,4,0,-4,-8])lampPanel(x,z);
  for(const z of[10,6,2])box(0,CEIL-.24,z,30,.24,.34,"#eef1f4");for(let x=-14;x<=14;x+=4)box(x,CEIL-.24,4.5,.34,.24,13,"#eef1f4");          // ceiling beams over the hall
  for(const s of[-1,1])box(s*14.82,CEIL-.2,4.5,.06,.06,12.6,GLOW_W,K.glow);box(0,CEIL-.2,-1.82,29,.06,.06,GLOW_T,K.glow);                    // strips of light where wall meets ceiling
  // ---- outer walls: cool white, with a slate skirting
  wallRun(-15,-11,15,-11,0,CEIL,MN);wallRun(15,-11,15,11,0,CEIL,CW);wallRun(-15,-11,-15,-2,0,CEIL,MN);wallRun(-15,-2,-15,3,0,CEIL,CW);wallRun(-15,5.4,-15,11,0,CEIL,CW);box(-15,2.5,4.2,.2,CEIL-2.5,2.4,CW);
  for(const[x,z,w,d]of[[14.88,4.5,.04,13],[-14.88,8.2,.04,5.6],[-14.88,.5,.04,5]])box(x,0,z,w,.16,d,SLATE);
  // the front: windows on to the forecourt either side of the way in
  for(const s of[-1,1]){box(s*8.5,0,11,13,.9,.2,CW);box(s*8.5,3.3,11,13,CEIL-3.3,.2,CW);box(s*8.5,.9,11,12.7,2.4,.04,"#cfe6f2",K.glass);for(let k=0;k<=6;k++)box(s*(2.1+k*2.13),.9,11,.1,2.4,.16,MN);box(s*8.5,.9,10.94,13,.07,.2,SILVER,K.gold);box(s*8.5,3.26,10.94,13,.07,.2,SILVER,K.gold)}
  WALLS.push([-15,10.85,-1.5,11.15],[1.5,10.85,15,11.15]);box(0,2.7,11,3,CEIL-2.7,.2,CW);doorFrame(0,10.94,2.9,2.62,true);
  entrance(0,0,10.9,2.9,2.6,Math.PI,true);plate(0,2.95,10.82,2.4,.34,"TO THE BORDER GATE",MN,"#ffffff",Math.PI);
  box(0,-.3,24,90,.1,26,"#d9dcdf",K.tile);                                                                                                          // the forecourt, seen through the glass
  // ---- the wall between the public hall and the restricted side, with the navy feature wall behind Registration
  wallRun(-15,-2,-11.2,-2,0,CEIL,CW);wallRun(-9.8,-2,-7,-2,0,CEIL,CW);wallRun(-7,-2,7,-2,0,CEIL,MN);wallRun(7,-2,12,-2,0,CEIL,CW);wallRun(14,-2,15,-2,0,CEIL,CW);box(-10.5,2.15,-2,1.4,CEIL-2.15,.2,CW);box(13,2.3,-2,2,CEIL-2.3,.2,CW);
  for(let x=-6.6;x<=6.6;x+=.55)box(x,.2,-1.86,.07,CEIL-.5,.05,"#1d3552");box(0,.14,-1.84,14,.05,.05,GLOW_T,K.glow);                              // slats on the feature wall, lit from below
  box(0,2.42,-1.8,10.4,1.12,.1,MN);plate(0,2.78,-1.74,9.6,.6,"DELTA CITY IMMIGRATION AUTHORITY",MN,"#ffffff");plate(0,2.3,-1.74,4.6,.32,"Citizenship  •  Permits  •  Border Control",MN,"#9fd8e0");
  at(0,-1.74,0,()=>{for(const s of[-1,1]){discZ(s*5.9,2.85,.02,.62,GLOW_T,K.glow,28);discZ(s*5.9,2.85,.03,.54,MN,0,28);discZ(s*5.9,2.85,.04,.4,SILVER,K.gold,28);discZ(s*5.9,2.85,.05,.3,TEAL,0,28)}});
  for(const x of[-10.5])doorFrame(x,-1.9,1.4,2.15,true);doorFrame(13,-1.9,2,2.3,true);plate(-10.5,2.42,-1.86,1.5,.3,"AUTHORISED STAFF ONLY",DSLATE,"#ffffff");plate(13,2.56,-1.86,1.7,.3,"STAFF ONLY",DSLATE,"#ffffff");
  // ---- Registration: Violet's counter, under a lowered ceiling with its own lights
  serviceCounter(0,1.2,7.2,0,false);box(0,1.0,1.63,7.0,.035,.03,GLOW_T,K.glow);box(0,0,1.56,7.2,.12,.14,CHAR);plate(0,.4,1.66,2.6,.4,"REGISTRATION",MN,"#ffffff");
  box(1.6,1.14,1.1,.5,.16,.06,CW);sign(1.6,1.15,1.14,.46,.14,"VIOLET",TEAL,"#ffffff");box(-1.8,1.14,1.0,.5,.34,.04,"#161b22");box(-1.8,1.16,.975,.44,.28,.01,"#a7d8f2",K.glow);
  box(2.9,1.14,1.2,.3,.05,.36,"#161b22");box(2.9,1.19,1.2,.22,.02,.22,"#35d0c0",K.glow);for(const s of[-1,1])box(s*3.3,1.14,1.2,.05,.7,.7,"#cfe6f2",K.glass);
  box(0,CEIL-.5,.9,8,.5,2.6,CW);box(0,CEIL-.56,.9,8.1,.06,2.7,SILVER,K.gold);for(const x of[-3,-1,1,3])cyl(x,CEIL-.6,1.4,.1,.04,GLOW_W,10);for(const x of[-3,-1,1,3])box(x,CEIL-.59,1.4,.16,.02,.16,GLOW_W,K.glow);
  box(0,CEIL-1.26,2.22,3.6,.62,.08,"#0b1524");box(0,CEIL-1.22,2.27,3.4,.54,.02,"#0e2a44",K.glow);sign(0,CEIL-1.2,2.29,3.3,.5,"NOW SERVING   A 012   →   REGISTRATION","#0e2a44","#7fe3ff");
  at(VIOLET.x,VIOLET.z,0,()=>{ball(0,1.705,-.022,.104,.092,.11,"#1d1512");ball(0,1.585,-.105,.058,.052,.052,"#1d1512")});for(const s of[-1,1])flag(s*6.2,-1.4,3.4);
  hanging(0,6.4,3.4,"REGISTRATION  ↑");hanging(8,5.2,3.6,"PERMITS & PASSES  →");hanging(-8.5,6.4,3.4,"←  CITY ENTRANCE");
  belts([[-1.3,9.2],[-1.3,6.3],[-1.3,3.4]]);belts([[1.3,9.2],[1.3,6.3],[1.3,3.4]]);pillar(-4.8,6);pillar(4.8,6);
  // ---- waiting seats with tables and bins, the photo and fingerprint booth, notices, a clock, plants
  seats(-8.6,9.4,Math.PI,5);seats(-8.6,7.6,Math.PI,5);seats(-12.9,8.5,Math.PI/2,3);for(const[x,z]of[[-5.4,9.4],[-11.9,7.6]]){cyl(x,0,z,.2,.04,SILVER,10);cyl(x,.04,z,.04,.42,SILVER,6);cyl(x,.46,z,.34,.04,CW,14);box(x,.5,z,.26,.02,.18,TEAL);stands(x,z,.7,.7)}
  bin(-4.6,10.3);bin(4.3,10.3);box(-8.6,.004,8.5,7.4,.006,3.6,"#c3ccd4",K.fabric);
  at(8,9.2,0,()=>{box(0,0,0,2.3,2.5,1.9,MN);box(0,0,.97,.95,2.05,.04,TEAL,K.fabric);box(.8,1.5,.97,.5,.34,.03,GLOW_W,K.glow);box(0,2.5,0,2.4,.1,2,SILVER,K.gold);box(0,2.62,.9,1.6,.3,.06,"#0e2a44");stands(0,0,2.3,1.9);solid(0,0,2.3,1.9)});sign(8,2.64,10.14,1.5,.26,"ID PHOTO","#0e2a44","#7fe3ff");
  at(5.3,10.1,0,()=>{box(0,0,0,.5,1.05,.5,MN);box(0,1.05,0,.56,.05,.56,SILVER,K.gold);box(0,1.1,0,.34,.02,.34,"#35d0c0",K.glow);box(0,1.1,-.2,.3,.34,.03,"#161b22");stands(0,0,.5,.5);solid(0,0,.5,.5)});
  at(14.86,9,-Math.PI/2,()=>{box(0,1.3,0,2.8,1.6,.05,"#3a4756");box(0,1.24,.02,2.9,.06,.06,SILVER,K.gold);box(0,2.9,.02,2.9,.06,.06,SILVER,K.gold);for(let r=0;r<2;r++)for(let k=0;k<4;k++)box(-1.05+k*.7,1.45+r*.72,.04,.56,.6,.02,["#ffffff","#fdf3c4","#d6f1ee","#ffffff","#e8ecf8","#ffffff","#fdf3c4","#d6f1ee"][r*4+k])});
  plate(14.86,3.1,9,2.2,.3,"NOTICES",MN,"#ffffff",-Math.PI/2);
  at(-14.86,9.3,Math.PI/2,()=>{discZ(0,2.9,.02,.36,SILVER,K.gold,24);discZ(0,2.9,.03,.31,CW,0,24);box(0,2.98,.045,.03,.2,.01,MN);box(.07,2.9,.045,.16,.03,.01,MN)});
  for(const[x,z]of[[-14,10.2],[14,10.2],[-14,-1],[9.4,-1.2],[-6.2,2.2],[6.2,2.2]])greenery(x,z);
  // ---- Permits and Passes: three windows down the east side, officers behind the glass
  at(10.5,2.6,-Math.PI/2,()=>{serviceCounter(0,0,8.8,0,true);box(0,1.0,.43,8.6,.035,.03,GLOW_T,K.glow);box(0,0,.36,8.8,.12,.14,CHAR);for(const s of[-1,0,1])box(s*2.95+1.47,1.14,.1,.07,1.25,.1,SILVER,K.gold)});
  box(10.5,2.45,2.6,.5,CEIL-2.45,9,CW);box(10.2,2.45,2.6,.06,.06,9,SILVER,K.gold);
  for(const[z,t]of[[5.5,"RESIDENCE PERMITS"],[2.6,"VISITOR PASSES"],[-.3,"RELOCATION"]]){box(10.2,2.62,z,.06,.46,2.66,"#0e2a44");plate(10.16,2.68,z,2.5,.34,t,MN,"#ffffff",-Math.PI/2);workDesk(12.6,z,Math.PI/2,1.5);workChair(13.5,z,-Math.PI/2);box(10.34,1.14,z-.9,.3,.05,.2,"#161b22")}
  wallRun(10.5,7,15,7,0,CEIL,CW);box(10.5,0,7,.2,CEIL,.2,CW);WALLS.push([10.1,-2,10.9,7.1]);
  // ---- the way into the city, in the west wall: a lit portal
  doorFrame(-14.9,4.2,2.4,2.5,false);box(-14.84,2.62,4.2,.1,.5,2.7,"#0e3b3d");plate(-14.76,2.7,4.2,2.3,.36,"CITY ENTRANCE",TEAL,"#ffffff",Math.PI/2);for(const z of[2.9,5.5])box(-14.84,0,z,.05,2.5,.05,GLOW_T,K.glow);
  /* ================= restricted side: darker navy and slate, lit low along the floor ================= */
  for(const[x0,x1]of[[-15,-12.2],[-11,-8],[-8,-6.1],[-4.9,-3],[-3,.4],[1.6,3.5],[3.5,5.6],[6.8,9],[9,12],[13.2,15]])wallRun(x0,-4.2,x1,-4.2,0,CEIL,MN);
  for(const x of[-11.6,-5.5,1,6.2,12.6]){box(x,2.15,-4.2,1.2,CEIL-2.15,.2,MN);doorFrame(x,-4.1,1.2,2.15,true)}for(const x of[-8,-3,3.5,9])wallRun(x,-11,x,-4.2,0,CEIL,MN);
  for(const[x,t,w]of[[-11.6,"INSPECTION",1.15],[-5.5,"HOLDING",1.15],[1,"RECORDS",1.15],[6.2,"DEPUTY COMPTROLLER-GENERAL",2.5],[12.6,"COMPTROLLER-GENERAL",2.1]])plate(x,2.42,-4.06,w,.3,t,DSLATE,"#ffffff");
  box(0,.05,-2.14,29.6,.04,.04,"#3aa0ff",K.glow);box(0,.05,-4.06,29.6,.04,.04,"#3aa0ff",K.glow);box(0,.004,-3.1,29.6,.006,1.2,CHAR,K.fabric);                // the corridor: a dark runner between two lines of blue light
  // inspection: a table under a hanging lamp, three chairs, a dark window
  at(-11.5,-8,0,()=>{box(0,.74,0,1.8,.06,.9,SLATE,K.gold);for(const[a,b]of[[-.8,-.38],[.8,-.38],[-.8,.38],[.8,.38]])box(a,0,b,.06,.74,.06,SILVER,K.gold);box(0,.8,0,.5,.02,.34,"#ffffff");stands(0,0,1.8,.9);solid(0,0,1.8,.9)});
  box(-11.5,2.5,-8,.03,CEIL-2.5,.03,CHAR);cyl(-11.5,2.3,-8,.34,.22,CHAR,14,.1);cyl(-11.5,2.28,-8,.3,.02,"#fff3c4",12);box(-11.5,2.27,-8,.4,.01,.4,"#fff3c4",K.glow);
  workChair(-11.5,-9,0);workChair(-12,-7,Math.PI,SLATE);workChair(-11,-7,Math.PI,SLATE);box(-11.5,1.3,-10.88,3.2,1.1,.04,"#0c1622",K.glass);box(-11.5,1.24,-10.86,3.36,.06,.06,SILVER,K.gold);box(-11.5,2.4,-10.86,3.36,.06,.06,SILVER,K.gold);
  // holding: benches along the walls
  for(const[x,z,w,d]of[[-7.5,-8,.6,5],[-3.5,-8,.6,5]]){box(x,.42,z,w,.08,d,SLATE,K.gold);box(x,0,z,w-.1,.42,d-.2,CHAR);stands(x,z,w,d);solid(x,z,w,d)}box(-5.5,2.2,-10.86,1.6,.5,.04,"#0c1622",K.glass);
  // records: shelves of files and a clerk's desk
  for(const x of[-1.6,1.4])fileShelves(x,-10.6,0,2.4);fileShelves(-2.7,-7.6,Math.PI/2,3);workDesk(1.6,-6.4,Math.PI,1.6);workChair(1.6,-7.3,0);
  // the two senior offices: a wooden desk facing the door, a high-backed chair, two chairs for visitors, the flag, files, a rug
  const office=(cx,name,big)=>{box(cx,.004,-8.2,big?4.6:3.8,.008,3.6,"#1f3a5a",K.fabric);at(cx,-8.7,Math.PI,()=>{const W=big?2.6:2.1;box(0,.74,0,W,.07,1.0,"#5a3d28",K.wood);box(0,0,-.4,W-.2,.74,.06,MN);for(const s of[-1,1])box(s*(W/2-.05),0,0,.07,.74,.94,"#5a3d28",K.wood);box(0,.7,-.44,W-.2,.03,.02,SILVER,K.gold);
      box(.5,.82,.05,.56,.36,.04,"#161b22");box(.5,.84,.075,.5,.3,.01,"#a7d8f2",K.glow);box(-.5,.82,-.2,.5,.1,.08,SILVER,K.gold);box(-.1,.815,.15,.34,.02,.24,"#ffffff");stands(0,0,W,1);solid(0,0,W,1)});
    at(cx,-9.7,0,()=>{box(0,.44,0,.6,.1,.56,"#161b22",K.fabric);box(0,.54,-.26,.6,.9,.09,"#161b22",K.fabric);cyl(0,0,0,.28,.04,SILVER,10);cyl(0,.04,0,.04,.4,SILVER,6);stands(0,0,.6,.6)});
    workChair(cx-.7,-7.4,Math.PI,SLATE);workChair(cx+.7,-7.4,Math.PI,SLATE);flag(cx-(big?2.3:1.9),-10.4,3.2);if(big)flag(cx+2.3,-10.4,3.2);
    plate(cx,2.85,-10.86,big?4.4:3.6,.46,name,MN,"#ffffff");plate(cx,2.36,-10.86,big?3.4:3,.3,"Delta City Immigration Authority",MN,"#9fd8e0");box(cx,2.2,-10.86,big?4.6:3.8,.04,.04,GLOW_T,K.glow)};
  office(6.2,"Deputy Comptroller-General",false);fileShelves(8.6,-7.4,-Math.PI/2,2.4);
  office(12,"Comptroller-General",true);fileShelves(14.55,-7.4,-Math.PI/2,3);greenery(9.7,-10.3);
  WALLS.push([12,-2.12,14,-1.88,-1])}                                                                         // (placeholder so the list is never empty)
const IMM_LIGHTS=(()=>{const L=[];for(let x=-12;x<=12;x+=4){for(const z of[8,4,0])L.push([x,4,z,.2,4.2]);for(const z of[-4,-8])L.push([x,4,z,.1,3.4])}return L})();

/* ------------------------------ the border gate, outside ------------------------------ */
function borderOutside(){quad([-140,-.02,140],[140,-.02,140],[140,-.02,-140],[-140,-.02,-140],hex(SAND));
  box(0,0,45,9,.05,60,TAR,K.road);for(const s of[-1,1]){for(let k=0;k<37;k++)box(s*4.7,0,15.8+k*1.6,.4,.22,1.6,k%2?"#f4f4f0":"#0f8a4c")}for(let k=0;k<14;k++)box(0,.05,18+k*4,.16,.012,2,"#f1f1ea");
  box(0,0,20.5,32,.06,19,"#d9dcdf",K.tile);box(0,.03,20.5,2.4,.02,19,TEAL,K.tile);
  // the border fence, with the gate post across the road
  for(const s of[-1,1]){box(s*32.5,0,30,55,.5,.3,"#c9ced3");for(let k=0;k<110;k++)box(s*(5.2+k*.5),.5,30,.05,2.2,.05,MN);box(s*32.5,2.7,30,55,.08,.08,MN);box(s*16,0,20.5,.3,.5,19,"#c9ced3");for(let k=0;k<38;k++)box(s*16,.5,11.2+k*.5,.05,2.2,.05,MN);box(s*16,2.7,20.5,.08,.08,19,MN)}
  for(const s of[-1,1]){box(s*5.6,0,30,.8,5,.8,CW);box(s*5.6,5,30,1,.2,1,TEAL)}box(0,5.2,30,13,1.5,1.2,MN);sign(0,5.45,30.62,11.6,1.0,"WELCOME TO DELTA CITY",MN,"#ffffff");box(0,5.0,30,13.4,.2,1.5,SILVER,K.gold);
  at(-3.4,31.6,0,()=>{box(0,0,0,1.8,2.5,1.8,CW);box(0,1.1,.92,1.2,.9,.04,"#5f93b4",K.glass);box(0,2.5,0,2.2,.16,2.2,TEAL)});cyl(-2.2,0,30.6,.1,1.1,CW,8);at(-2.2,30.6,0,()=>box(1.6,1.6,0,.1,.1,.1,CW));
  for(let k=0;k<8;k++)at(-2.2,30.6,0,()=>box(.25+k*.35,1.05+k*.33,0,.36,.1,.08,k%2?"#e11d48":"#ffffff"));                    // the barrier arm, raised
  sign(4.2,2.2,30.5,2.6,.5,"ALL ARRIVALS  ↑  IMMIGRATION",TEAL,"#ffffff");for(const s of[-1,1])box(4.2+s*1.2,0,30.46,.08,2.2,.08,SILVER);
  // the Authority's building
  const W=32,Dp=23,Ht=5.4;box(0,0,-.5,W+.8,.4,Dp+.8,"#b8bcbf");box(0,.4,-.5,W,Ht,Dp,CW);box(0,Ht+.4,-.5,W+.6,.9,Dp+.6,MN);box(0,Ht+1.3,-.5,W+.9,.12,Dp+.9,TEAL);
  for(let k=0;k<=16;k++)box(-16+k*2,.4,11,.16,Ht,.22,MN);for(let k=0;k<16;k++){const x=-15+k*2;if(Math.abs(x)>1.4)box(x,1.3,10.98,1.84,Ht-1.6,.06,"#5f93b4",K.glass)}box(0,.4,11,W,.9,.2,CW);
  sign(0,Ht+.5,11.34,17,.72,"DELTA CITY IMMIGRATION AUTHORITY",MN,"#ffffff");box(0,3.2,12.6,7,.26,3.4,MN);box(0,3.46,12.6,7.3,.08,3.7,TEAL);for(const s of[-1,1])cyl(s*3,0,14,.16,3.2,SILVER,10);
  sign(0,2.55,14.34,3,.5,"ARRIVALS",TEAL,"#ffffff");entrance(0,.4,11.14,2.9,2.6,0,true);for(let k=0;k<2;k++)box(0,0,11.7+(2-k)*.4-.2,5+(2-k)*.6,(k+1)*.2,.4,"#c9cdd0");
  for(const s of[-1,1]){flag(s*6,16,8);flag(s*7.6,16,8);palm(s*12,24,6);palm(s*12,14.5,5.6)}}
const OUT_WALLS=[[-60,29.8,-5.2,30.2],[5.2,29.8,60,30.2],[-16.2,11,-15.8,30],[15.8,11,16.2,30],[-16,10.8,-1.6,11.3],[1.6,10.8,16,11.3],[-20.2,30,-19.8,62],[19.8,30,20.2,62],[-20,61.8,20,62.2],[-4.4,30.6,-2.4,32.6]];

const OUT=capture(borderOutside),IN=captureLit(immigrationInside,IMM_LIGHTS,false,CEIL),IN_WALLS=WALLS.slice();IN.ceil=[CEIL,CEIL];
const litI=fn=>{const s=captureLit(fn,IMM_LIGHTS,false,CEIL);s.ceil=[CEIL,CEIL];return s};
/* Who may go where. A newcomer has only the public hall, and not the city, until Violet has
   issued a birth certificate. Officers have the restricted side. The Comptroller-General's
   office is the Comptroller-General's alone. */
const ROLES=[["newcomer","a new arrival (no certificate)"],["citizen","a citizen"],["officer","an immigration officer"],["deputy","the Deputy Comptroller-General"],["cg","the Comptroller-General"]];
const SENIOR=r=>r==="cg"||r==="deputy",STAFF=r=>r==="officer"||SENIOR(r);
const can=key=>key==="city"?!!me.cert||STAFF(me.role):key==="cg"?SENIOR(me.role):STAFF(me.role);        // officers may use the Deputy's office; the Comptroller-General's is for the two senior officers
const GATES=[{key:"city",r:[-15.2,3,-14.7,5.4],msg:"You need your birth certificate before you can enter the city. Speak to Violet at Registration."},
  {key:"staff",r:[-11.2,-2.15,-9.8,-1.85],msg:"Authorised staff only."},{key:"staff",r:[12,-2.15,14,-1.85],msg:"Authorised staff only."},
  {key:"deputy",r:[5.6,-4.35,6.8,-4.05],msg:"The Deputy Comptroller-General's office."},{key:"cg",r:[12,-4.35,13.2,-4.05],msg:"The Comptroller-General's office."}];
// a door leaf: shut, it fills its doorway; open, it lies flat against the wall beside the doorway (side: -1 west, +1 east; back: which face of the wall)
const leaf=(x,z,w,open,side,back)=>{if(open)box(x+side*(w+.06),0,z+back*.15,w,2.15,.07,DSLATE);else{box(x,0,z,w,2.15,.08,DSLATE);box(x+side*-(w/2-.14),1.0,z+.07,.07,.07,.05,SILVER,K.gold);box(x+side*-(w/2-.14),1.0,z-.07,.07,.07,.05,SILVER,K.gold)}};
const DOORS=[
  {key:"city",shut:litI(()=>{box(-14.95,0,4.2,.08,1.15,2.24,"#cfe6f2",K.glass);box(-14.95,1.15,4.2,.1,.06,2.3,SILVER,K.gold);box(-14.88,2.2,4.2,.06,.22,.5,"#ff5a5a",K.glow)}),
   open:litI(()=>{for(const z of[3.1,5.3])box(-14.4,0,z,1.1,1.15,.06,"#cfe6f2",K.glass);box(-14.88,2.2,4.2,.06,.22,.5,"#35d07f",K.glow);entrance(-14.96,0,4.2,2.2,2.4,Math.PI/2,true)})},
  {key:"staff",shut:litI(()=>{leaf(-10.5,-2,1.36,false,-1,-1);box(13,0,-2,1.96,2.3,.08,DSLATE)}),open:litI(()=>{leaf(-10.5,-2,1.36,true,-1,-1);box(10.98,0,-2.15,1.96,2.3,.07,DSLATE)})},
  {key:"deputy",shut:litI(()=>leaf(6.2,-4.2,1.16,false,1,-1)),open:litI(()=>leaf(6.2,-4.2,1.16,true,1,-1))},
  {key:"cg",shut:litI(()=>leaf(12.6,-4.2,1.16,false,1,-1)),open:litI(()=>leaf(12.6,-4.2,1.16,true,1,-1))}];
/* The way to the city, lit up on the floor once a newcomer has a birth certificate. */
const GUIDE=litI(()=>{const c=[70,200,255],y=.02,arrow=(x,z,dx,dz)=>{const px=-dz,pz=dx,a=[x+dx*.34,y,z+dz*.34],l=[x-dx*.22+px*.3,y,z-dz*.22+pz*.3],r=[x-dx*.22-px*.3,y,z-dz*.22-pz*.3];tri(a,l,r,c,K.glow);tri(a,r,l,c,K.glow)};
  for(let z=3.0;z<4.0;z+=.9)arrow(0,z,0,1);for(let x=-1.2;x>-14;x-=1.15)arrow(x,4.2,-1,0)});
/* ---------------------- people who stand in one place: Violet ---------------------- */
const NPCP=program(`attribute vec3 p,n;attribute vec2 uv;attribute vec4 paint;uniform mat4 vp,model;varying vec3 vn;varying vec2 vu;varying vec4 vpaint;
void main(){vec4 w=model*vec4(p,1.);vn=normalize((model*vec4(n,0.)).xyz);vu=uv;vpaint=paint;gl_Position=vp*w;}`,`
precision mediump float;varying vec3 vn;varying vec2 vu;varying vec4 vpaint;uniform sampler2D t;uniform vec3 tint;uniform float useTint,avg;
void main(){vec4 c=texture2D(t,vu);if(useTint>.5){float l=dot(c.rgb,vec3(.3,.59,.11))/max(avg,.02);c.rgb=tint*clamp(l,.5,1.45);}
  c.rgb=mix(c.rgb,vpaint.rgb,smoothstep(.35,.65,vpaint.a));vec3 n=normalize(vn);gl_FragColor=vec4(c.rgb*(.82+.12*n.y+.1*max(n.z,0.)),1.);}`);
let VIOLET_BODY=null,PERSON_BASE=null;
// garments painted onto the body. Positions are in the rest pose: standing, arms out sideways.
const pc=v=>Math.max(0,Math.min(1,v)),pTorso=(x,y)=>(Math.abs(x)<.21&&y>1.0&&y<1.53&&!(Math.abs(x)<.07&&y>1.43))?1:0,pSleeve=(x,y,to)=>Math.abs(x)>=.17&&y>1.2?pc((to-Math.abs(x))/.035):0,pLegs=(x,y)=>(y<.84&&Math.abs(x)<.3)?pc((y-.1)/.03):0;
const dress=(top,sleeveTo,legs)=>(x,y)=>{const a=Math.max(pTorso(x,y),pSleeve(x,y,sleeveTo));if(a>0)return[top,a];if(legs){const l=pLegs(x,y);if(l>0)return[legs,l]}return null};
const VIOLET_LOOK={top:TEAL,bottom:CHAR,shoes:"#16181d",paint:dress(TEAL,.67,CHAR)};
/* The three outfits a woman can choose on arrival, and the hair that goes with each. */
const WOMAN_LOOKS={
  classic:{top:"#6e1f2f",bottom:"#6e1f2f",shoes:"#2a2a2e",paint:dress("#6e1f2f",.67,"#6e1f2f"),hair:[[0,1.705,-.022,.104,.092,.11],[0,1.585,-.105,.058,.052,.052]],hairColor:"#1d1512"},
  cute:{top:"#f6e27a",bottom:"#8fb7dd",shoes:"#ffffff",paint:dress("#f6e27a",.34,null),hair:[[0,1.705,-.022,.104,.092,.11],[0,1.72,-.04,.155,.14,.15]],hairColor:"#2a1d18"},
  sporty:{top:"#f2c230",bottom:"#1b2a4a",shoes:"#f4f4f4",paint:dress("#f2c230",.67,"#1b2a4a"),hair:[[0,1.705,-.022,.104,.092,.11],[0,1.705,-.115,.04,.045,.04],[0,1.63,-.165,.038,.1,.04],[0,1.5,-.17,.03,.08,.03]],hairColor:"#1d1512"}};
async function loadPersonBase(){const src=JSON.parse(document.getElementById("person").textContent);
  const raw=atob(src.data),bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
  const images=await Promise.all(src.textures.map(t=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>ok(im);im.onerror=()=>no(new Error("picture"));im.src=t.url})));
  const tex=images.map(im=>{const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,im);gl.generateMipmap(gl.TEXTURE_2D);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);return t});
  // stand her with her arms at her sides: work out each bone once
  const D=Math.PI/180,turns={LeftArm:["z",-82*D,"x",-.08],RightArm:["z",82*D,"x",-.08],LeftForeArm:["x",-.3],RightForeArm:["x",-.3],LeftHand:["z",.12],RightHand:["z",-.12]},Wb=[],Bm=[];
  src.bones.forEach((b,i)=>{let w=b.parent<0?new Float32Array(b.local):mul(Wb[b.parent],b.local);const t=turns[b.name];
    if(t)for(let k=0;k<t.length;k+=2){const c=Math.cos(t[k+1]),sn=Math.sin(t[k+1]);for(let col=0;col<12;col+=4){const x=w[col],y=w[col+1],z=w[col+2];if(t[k]==="x"){w[col+1]=y*c-z*sn;w[col+2]=y*sn+z*c}else if(t[k]==="y"){w[col]=x*c+z*sn;w[col+2]=-x*sn+z*c}else{w[col]=x*c-y*sn;w[col+1]=x*sn+y*c}}}
    Wb[i]=w;Bm[i]=mul(w,b.inv)});
  const mk=(d,t)=>{const b=gl.createBuffer();gl.bindBuffer(t||gl.ARRAY_BUFFER,b);gl.bufferData(t||gl.ARRAY_BUFFER,d,gl.STATIC_DRAW);return b};
  // move every point of her body into that pose once; the shape is then shared by everyone who uses this body
  const parts=src.parts.map(p=>{const q=new Uint16Array(bytes.buffer,p.pos,p.verts*3),nq=new Int8Array(bytes.buffer,p.nor,p.verts*4),uq=new Uint16Array(bytes.buffer,p.uv,p.verts*2),J=new Uint8Array(bytes.buffer,p.joints,p.verts*4),Wt=new Uint8Array(bytes.buffer,p.weights,p.verts*4);
    const P=new Float32Array(p.verts*3),N=new Float32Array(p.verts*3),U=new Float32Array(p.verts*2),rest=new Float32Array(p.verts*2);
    for(let v=0;v<p.verts;v++){const x=src.lo[0]+q[v*3]/65535*src.span,y=src.lo[1]+q[v*3+1]/65535*src.span,z=src.lo[2]+q[v*3+2]/65535*src.span,nx=nq[v*4]/127,ny=nq[v*4+1]/127,nz=nq[v*4+2]/127;let ox=0,oy=0,oz=0,mx=0,my=0,mz=0;
      for(let k=0;k<4;k++){const w=Wt[v*4+k]/255;if(!w)continue;const m=Bm[J[v*4+k]];ox+=w*(m[0]*x+m[4]*y+m[8]*z+m[12]);oy+=w*(m[1]*x+m[5]*y+m[9]*z+m[13]);oz+=w*(m[2]*x+m[6]*y+m[10]*z+m[14]);mx+=w*(m[0]*nx+m[4]*ny+m[8]*nz);my+=w*(m[1]*nx+m[5]*ny+m[9]*nz);mz+=w*(m[2]*nx+m[6]*ny+m[10]*nz)}
      P[v*3]=ox;P[v*3+1]=oy;P[v*3+2]=oz;N[v*3]=mx;N[v*3+1]=my;N[v*3+2]=mz;U[v*2]=p.uvlo[0]+uq[v*2]/65535*p.uvspan[0];U[v*2+1]=p.uvlo[1]+uq[v*2+1]/65535*p.uvspan[1];rest[v*2]=x;rest[v*2+1]=y}
    return{name:p.name,verts:p.verts,rest,p:mk(P),n:mk(N),uv:mk(U),i:mk(new Uint16Array(bytes.buffer,p.idx,p.count),gl.ELEMENT_ARRAY_BUFFER),count:p.count,tex:tex[p.tex],avg:src.textures[p.tex].avg}});
  PERSON_BASE={parts,mk}}
// one person: the shared body, in one look
function dressPerson(look){const B=PERSON_BASE;return{parts:B.parts.map(p=>{const C=new Uint8Array(p.verts*4);
    if(p.name==="AvatarBody"&&look.paint)for(let v=0;v<p.verts;v++){const r=look.paint(p.rest[v*2],p.rest[v*2+1]);if(r){const h=hex(r[0]);C[v*4]=h[0];C[v*4+1]=h[1];C[v*4+2]=h[2];C[v*4+3]=r[1]*255}}
    return{p:p.p,n:p.n,uv:p.uv,i:p.i,count:p.count,tex:p.tex,avg:p.avg,c:B.mk(C),tint:p.name==="outfit_top"?look.top:p.name==="outfit_bottom"?look.bottom:p.name==="outfit_shoes"?look.shoes:null}})}}
/* Men, for now: a simple figure built from shapes, in the same three outfits. It is replaced when there is a male model. */
const MAN_LOOKS={classic:{top:"#f4f6fb",long:1,tie:"#1f2f4d",leg:"#1f2f4d",shoe:"#111827"},cute:{top:"#c7b3f0",leg:"#4a4f5c",shoe:"#ffffff"},sporty:{top:"#00a86b",stripe:"#ffffff",leg:"#111827",shin:1,sock:"#ffffff",shoe:"#16181d",band:"#ffffff"}};
function toyMan(o){const sk="#8d5a3b",hair="#1b1310";
  for(const s of[-1,1]){cyl(s*.085,.46,0,.066,.46,o.leg,10,.086);cyl(s*.085,.06,0,.05,.4,o.shin?sk:o.leg,10,.064);if(o.sock)cyl(s*.085,.06,0,.054,.2,o.sock,10,.058);ball(s*.085,.05,.045,.062,.05,.115,o.shoe,6)}
  ball(0,.93,0,.17,.115,.125,o.leg,10);ball(0,1.17,0,.2,.27,.125,o.top,14);ball(0,1.385,0,.215,.075,.13,o.top,10);
  if(o.tie)box(0,1.06,.118,.05,.3,.02,o.tie);if(o.stripe)box(0,1.22,.105,.34,.04,.05,o.stripe);
  for(const s of[-1,1]){ball(s*.235,1.37,0,.064,.064,.064,o.top,6);cyl(s*.245,1.1,0,.046,.27,o.long?o.top:sk,8,.056);if(!o.long)cyl(s*.243,1.24,0,.06,.13,o.top,8,.064);cyl(s*.25,.84,0,.038,.26,o.long?o.top:sk,8,.046);ball(s*.252,.8,0,.046,.052,.04,sk,6)}
  cyl(0,1.42,0,.052,.1,sk,8,.05);ball(0,1.63,0,.12,.138,.126,sk,14);ball(-.042,1.642,.112,.016,.02,.012,"#111827",6);ball(.042,1.642,.112,.016,.02,.012,"#111827",6);box(0,1.572,.118,.05,.01,.012,"#5a2a1e");
  ball(0,1.705,-.035,.125,.1,.122,hair,12);if(o.band)cyl(0,1.71,-.02,.127,.028,o.band,16,.128)}
const PICS={Male:{},Female:{}},HAIR={},MEN={};
// take a photograph of one person standing at the centre, and hand it back as a picture
function snap(w,h,eye,at,fov,bg,drawFn){cv.width=w;cv.height=h;gl.viewport(0,0,w,h);gl.clearColor(bg[0],bg[1],bg[2],1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.BLEND);
  drawFn(mul(persp(fov,w/h,.05,30),look(eye,at,[0,1,0])),eye);return cv.toDataURL("image/jpeg",.92)}
function makePictures(){const bg=[.84,.88,.92];
  for(const k of Object.keys(WOMAN_LOOKS)){const look=WOMAN_LOOKS[k],body=dressPerson(look);HAIR[k]=capture(()=>{for(const b of look.hair)ball(b[0],b[1],b[2],b[3],b[4],b[5],look.hairColor)});
    const draw=(VP,eye)=>{drawPerson(body,VP,ident());drawScene(HAIR[k],VP,eye,false)};
    PICS.Female[k]={face:snap(300,396,[.12,1.63,1.02],[0,1.6,0],.5,bg,draw),body:snap(240,440,[.5,1.05,3.5],[0,.9,0],.5,bg,draw)}}
  for(const k of Object.keys(MAN_LOOKS)){MEN[k]=capture(()=>toyMan(MAN_LOOKS[k]));const draw=(VP,eye)=>drawScene(MEN[k],VP,eye,false);
    PICS.Male[k]={face:snap(300,396,[.12,1.63,1.02],[0,1.6,0],.5,bg,draw),body:snap(240,440,[.5,1.05,3.5],[0,.9,0],.5,bg,draw)}}}
function drawPerson(person,VP,model){const P=NPCP;gl.enable(gl.CULL_FACE);gl.useProgram(P.p);gl.uniformMatrix4fv(P.u.vp,false,VP);gl.uniformMatrix4fv(P.u.model,false,model);gl.activeTexture(gl.TEXTURE0);gl.uniform1i(P.u.t,0);
  for(const q of person.parts){const A=(loc,buf,n,type,norm)=>{gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,n,type||gl.FLOAT,!!norm,0,0)};
    A(P.a.p,q.p,3);A(P.a.n,q.n,3);A(P.a.uv,q.uv,2);A(P.a.paint,q.c,4,gl.UNSIGNED_BYTE,true);gl.uniform1f(P.u.useTint,q.tint?1:0);if(q.tint){gl.uniform3fv(P.u.tint,hex(q.tint).map(v=>v/255));gl.uniform1f(P.u.avg,q.avg)}
    gl.bindTexture(gl.TEXTURE_2D,q.tex);gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,q.i);gl.drawElements(gl.TRIANGLES,q.count,gl.UNSIGNED_SHORT,0)}
  gl.disableVertexAttribArray(P.a.paint)}

/* ================================== playing ================================== */
const me={x:0,z:50,yaw:0,pitch:.03,inside:false,role:"newcomer",cert:null},input={x:0,y:0},keys={};
let busy=false,talking=false,last=0,frames=0,acc=0,slow=0,quality=Math.min(window.devicePixelRatio||1,1.25),toastT=0;
function toast(t){const el=document.getElementById("toast");el.textContent=t;el.hidden=false;clearTimeout(toastT);toastT=setTimeout(()=>el.hidden=true,3200)}
function fadeTo(text,change){if(busy)return;busy=true;const f=document.getElementById("fade");document.getElementById("where").textContent=text;f.classList.add("on");setTimeout(()=>{change();ui();setTimeout(()=>{f.classList.remove("on");busy=false},260)},300)}
function blocked(x,z){const r=.32;if(!me.inside){for(const w of OUT_WALLS)if(x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r)return true;return false}
  for(const w of IN_WALLS){if(w[4]===-1)continue;if(x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r)return true}
  for(const g of GATES){const w=g.r;if(!can(g.key)&&x>w[0]-r&&x<w[2]+r&&z>w[1]-r&&z<w[3]+r){toast(g.msg);return true}}
  return x>15-r||z<-11+r}
const nearViolet=()=>me.inside&&Math.hypot(me.x-VIOLET.x,me.z-2.6)<2.4;
function frame(now){requestAnimationFrame(frame);const t=now/1000,real=t-last||.016,dt=Math.min(.05,real);last=t;
  const ix=input.x+(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),iy=input.y+(keys.w||keys.arrowup?1:0)-(keys.s||keys.arrowdown?1:0);
  if(!busy&&!talking&&(ix||iy)){const sp=(keys.shift?4.6:2.6)*dt,dx=(-Math.sin(me.yaw)*iy+Math.cos(me.yaw)*ix)*sp,dz=(-Math.cos(me.yaw)*iy-Math.sin(me.yaw)*ix)*sp;
    if(!blocked(me.x+dx,me.z))me.x+=dx;if(!blocked(me.x,me.z+dz))me.z+=dz;
    if(!me.inside&&Math.abs(me.x)<1.5&&me.z<12.4&&me.z>11)fadeTo("Delta City Immigration Authority: arrivals hall",()=>{me.inside=true;me.x=0;me.z=9.6;me.yaw=0;me.pitch=.03});
    else if(me.inside&&Math.abs(me.x)<1.5&&me.z>10.55)fadeTo("The border gate",()=>{me.inside=false;me.x=0;me.z=14.4;me.yaw=Math.PI;me.pitch=.03});
    else if(me.inside&&me.x<-15.3&&can("city"))fadeTo("Asaba",()=>{me.x=-12.5;me.z=4.2;me.yaw=-Math.PI/2;toast("You are through. In the full game you would now be standing in Asaba.")})}
  document.getElementById("act").hidden=!(nearViolet()&&!talking&&!busy);
  const w=cv.clientWidth,h=cv.clientHeight,dpr=Math.min(window.devicePixelRatio||1,quality);if(cv.width!==Math.round(w*dpr)||cv.height!==Math.round(h*dpr)){cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr)}
  gl.viewport(0,0,cv.width,cv.height);const eye=[me.x,1.62,me.z],cp=Math.cos(me.pitch),to=[me.x-Math.sin(me.yaw)*cp,1.62+Math.sin(me.pitch),me.z-Math.cos(me.yaw)*cp];
  const VP=mul(persp(w>h?1.05:1.25,w/h,.08,500),look(eye,to,[0,1,0]));
  gl.clearColor(.66,.84,.93,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);
  const parts=me.inside?[IN].concat(DOORS.map(d=>can(d.key)?d.open:d.shut)):[OUT];if(me.inside&&me.cert&&me.role==="citizen")parts.push(GUIDE);for(const S of parts)drawScene(S,VP,eye,me.inside);
  if(me.inside&&VIOLET_BODY)drawPerson(VIOLET_BODY,VP,trans(VIOLET.x,0,VIOLET.z));
  for(const S of parts)drawSceneClear(S,VP,eye,t);
  frames++;acc+=real;if(acc>=.5){const fps=frames/acc;document.getElementById("fps").textContent=Math.round(fps);frames=0;acc=0;
    document.getElementById("info").textContent=(me.inside?"Inside, ":"Outside, ")+Math.round((me.inside?IN.tris+15450:OUT.tris)/1000)+"k triangles, "+cv.width+"x"+cv.height;document.getElementById("info").appendChild(document.createElement("br"));document.getElementById("info").appendChild(document.createTextNode(GPU));
    if(t>3&&fps<48&&quality>.5){slow++;if(slow>=2){quality=Math.max(.5,quality-.2);slow=0}}else slow=0}}
const GPU=(()=>{try{const e=gl.getExtension("WEBGL_debug_renderer_info");return e?String(gl.getParameter(e.UNMASKED_RENDERER_WEBGL)).replace(/ANGLE \(|\)$/g,"").slice(0,34):"graphics unknown"}catch(x){return"graphics unknown"}})();

/* The Certificate of Birth: the same document the Discord bot issues, drawn to the same layout
   (640 x 905 design grid): header and emblems, the two numbered sections, the passport
   photograph, the statement, the registrar's line, the seal. */
function certificateCanvas(c,photo,officer){const W=640,H=905,S=2,out=document.createElement("canvas");out.width=W*S;out.height=H*S;const g=out.getContext("2d");g.scale(S,S);
  const NAVYC="rgb(22,42,74)",SOFT="rgb(60,82,115)",INK="rgb(22,24,28)",LAB="rgb(95,105,120)",LINEC="rgb(160,172,190)",REDC="rgb(140,32,32)",SERIF='Georgia,"Times New Roman",Times,serif';
  const font=(style,size)=>{g.font=(style==="italic"?"italic ":"")+(style==="bold"?"700 ":"400 ")+size+"px "+SERIF};
  const spaced=(x,y,text,style,size,fill,track,align)=>{font(style,size);g.fillStyle=fill;g.textAlign="left";g.textBaseline="alphabetic";const ch=[...text],ws=ch.map(q=>g.measureText(q).width),total=ws.reduce((a,b)=>a+b,0)+track*Math.max(0,ch.length-1);let cx=align==="center"?x-total/2:align==="right"?x-total:x;ch.forEach((q,i)=>{g.fillText(q,cx,y);cx+=ws[i]+track})};
  const text=(x,y,s,style,size,fill,align)=>{font(style,size);g.fillStyle=fill;g.textAlign=align||"left";g.textBaseline="alphabetic";g.fillText(s,x,y)};
  const fit=(style,s,size,maxW,min)=>{while(size>min){font(style,size);if(g.measureText(s).width<=maxW)break;size--}return size};
  const rule=(x1,x2,y,color,w)=>{g.strokeStyle=color||LINEC;g.lineWidth=w||1;g.beginPath();g.moveTo(x1,y);g.lineTo(x2,y);g.stroke()};
  const ring=(cx,cy,r,color,w)=>{g.beginPath();g.arc(cx,cy,r,0,6.2832);g.strokeStyle=color;g.lineWidth=w;g.stroke()};
  const star=(cx,cy,r0,r1,color,w)=>{g.beginPath();for(let i=0;i<10;i++){const rad=i%2===0?r0:r1,a=-Math.PI/2+i*Math.PI/5;g[i?"lineTo":"moveTo"](cx+Math.cos(a)*rad,cy+Math.sin(a)*rad)}g.closePath();g.strokeStyle=color;g.lineWidth=w;g.stroke()};
  const field=(x,y,label,value,width,size)=>{text(x,y,label.toUpperCase(),"regular",8.5,LAB);text(x,y+21,value,"bold",fit("bold",value,size,width,10),INK);rule(x,x+width,y+25,LINEC,.8)};
  const section=(x,y,n,title)=>{spaced(x,y,n+". "+title,"bold",12.5,NAVYC,1.4,"left");rule(x,W-60,y+8,LINEC,.8)};
  // light blue paper with faint cross-hatching, and the watermark
  g.fillStyle="rgb(234,240,248)";g.fillRect(0,0,W,H);g.strokeStyle="rgba(150,175,205,.1)";g.lineWidth=.5;for(let off=-H;off<W+H;off+=9){g.beginPath();g.moveTo(off,0);g.lineTo(off+H,H);g.stroke();g.beginPath();g.moveTo(off+H,0);g.lineTo(off,H);g.stroke()}
  const wm="rgba(22,42,74,.063)";ring(W/2,330,190,wm,2.4);ring(W/2,330,165,wm,2.4);star(W/2,330,130,54,wm,2.2);
  g.strokeStyle=NAVYC;g.lineWidth=2.2;g.strokeRect(20,20,W-40,H-40);g.strokeStyle=SOFT;g.lineWidth=.8;g.strokeRect(26,26,W-52,H-52);
  g.strokeStyle=REDC;g.lineWidth=1.4;g.strokeRect(W-128,34,84,22);spaced(W-86,50,"ORIGINAL","bold",11,REDC,2,"center");
  const emblem=(cx,cy,r,label)=>{ring(cx,cy,r,NAVYC,1.8);ring(cx,cy,r-5,NAVYC,1);star(cx,cy,r*.62,r*.26,NAVYC,1.2);spaced(cx,cy+r+13,label,"regular",6.5,SOFT,1.4,"center")};
  emblem(78,80,30,"REPUBLIC");emblem(W-78,80,30,"OFFICIAL");
  spaced(W/2,60,"DELTA CITY REPUBLIC","bold",19,NAVYC,3,"center");spaced(W/2,78,"OFFICE OF IMMIGRATION & CITIZENSHIP","regular",9.5,SOFT,1.8,"center");rule(60,W-60,94);
  text(W/2,132,"CERTIFICATE OF BIRTH","bold",30,NAVYC,"center");text(W/2,152,"Issued under the Immigration & Citizenship Act of Delta City","italic",10.5,SOFT,"center");rule(60,W-60,166);
  const left=60,pw=108,ph=140,px=W-60-pw,topW=(px-30)-left,topH=(topW-20)/2,botH=((W-60)-left-20)/2,up=s=>String(s||"").trim().toUpperCase();
  section(left,196,1,"PERSONAL INFORMATION");field(left,228,"Full Name",up(c.name),topW,20);field(left,278,"Date of Birth",up(c.dob)||"\u2014",topH,15);field(left+topH+20,278,"Gender",up(c.gender),topH,15);
  g.fillStyle="#fff";g.fillRect(px,196,pw,ph);g.strokeStyle=NAVYC;g.lineWidth=1.6;g.strokeRect(px,196,pw,ph);
  if(photo)g.drawImage(photo,px+4,200,pw-8,ph-8);else{g.fillStyle="rgb(210,218,228)";g.fillRect(px+4,200,pw-8,ph-8)}
  spaced(px+pw/2,196+ph+12,"PASSPORT PHOTOGRAPH","regular",6.3,LAB,1,"center");
  section(left,356,2,"REGISTRATION DETAILS");field(left,388,"Certificate No.",up(c.no),botH,15);field(left+botH+20,388,"Date Registered",up(c.date),botH,15);field(left,438,"Home State",up(c.state),botH,15);field(left+botH+20,438,"Issuing Office","ASABA IMMIGRATION OFFICE",botH,11);
  rule(left,W-60,500,LINEC,.8);
  {const words="This is to certify that the individual named above has been duly registered and granted citizenship of the Delta City Republic, in accordance with the Immigration & Citizenship Act.".split(" "),lines=[];let cur="";font("italic",10.5);
    for(const w of words){const trial=(cur+" "+w).trim();if(g.measureText(trial).width+.2*trial.length<=W-160)cur=trial;else{lines.push(cur);cur=w}}if(cur)lines.push(cur);lines.forEach((l,i)=>spaced(W/2,524+i*17,l,"italic",10.5,SOFT,.2,"center"))}
  g.fillStyle="#fff";g.fillRect(W-160,620,100,100);g.strokeStyle=NAVYC;g.lineWidth=1.2;g.strokeRect(W-160,620,100,100);text(W-110,735,"Scan to verify","italic",8.5,SOFT,"center");
  const sy=H-150,who=String(officer||"Issuing Officer");rule(W/2-140,W/2+140,sy,NAVYC,1);text(W/2,sy-8,who,"bold",fit("bold",who,13,260,9),INK,"center");
  text(W/2,sy+16,"Authorized Registrar, Immigration & Citizenship Office","italic",9,SOFT,"center");text(W/2,sy+32,"Date: "+up(c.date),"regular",8.5,LAB,"center");
  {const cx=96,cy=H-134,r=32;g.fillStyle=NAVYC;for(let i=0;i<20;i++){const a=6.2832*i/20;g.beginPath();g.arc(cx+Math.cos(a)*(r+3),cy+Math.sin(a)*(r+3),3.6,0,6.2832);g.fill()}ring(cx,cy,r+1,NAVYC,1.6);ring(cx,cy,r-6,NAVYC,1);star(cx,cy,r*.5,r*.2,NAVYC,1.2)}
  text(W/2,H-40,"Valid only with the official seal and registrar\u2019s signature \u00b7 Issued in Asaba, Delta City","regular",7.6,SOFT,"center");return out}
// make the certificate picture for a citizen, with the photograph of the character they chose
function issueCertificate(c){return new Promise(done=>{const pic=PICS[me.gender]&&PICS[me.gender][me.outfit],finish=img=>{try{c.image=certificateCanvas(c,img,"Violet").toDataURL("image/jpeg",.9)}catch(e){c.image=null}done(c)};
  if(!pic)return finish(null);const im=new Image();im.onload=()=>finish(im);im.onerror=()=>finish(null);im.src=pic.face})}

/* ------------------------- talking to Violet: registration ------------------------- */
const STATE_CODE={Asaba:"ASB",Warri:"WAR",Ozoro:"OZR",Agbor:"AGB"},form={name:"",dob:"",gender:"",state:""};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function talk(step,extra){talking=true;document.getElementById("guide").hidden=true;const el=document.getElementById("talk");el.hidden=false;let h=`<div class="who">Violet <span>Citizenship Registrar, Immigration Authority</span></div>`;
  if(step==="hello")h+=me.cert?`<p>Welcome back, ${esc(me.cert.name)}. Your birth certificate is on file. Do you want to see it?</p><div class="row"><button data-t="cert">Show my certificate</button><button data-t="close" class="ghost">No, thank you</button></div>`
    :`<p>Good day, and welcome. A new arrival has entered Delta City.</p><p>Citizen registration is required before entry into the city can be granted. I will take your details and issue your birth certificate.</p><div class="row"><button data-t="form">Begin registration</button><button data-t="close" class="ghost">Not now</button></div>`;
  if(step==="form"&&!form.gender&&me.gender)form.gender=me.gender;
  if(step==="form")h+=`<p>Please fill in your details.</p>
    <label>Character name<input id="f_name" maxlength="32" value="${esc(form.name)}" placeholder="First name and surname" autocomplete="off"></label>
    <label>Date of birth<input id="f_dob" maxlength="24" value="${esc(form.dob)}" placeholder="DD Month YYYY, e.g. 01 September 1996" autocomplete="off"></label>
    <div class="lab">Gender</div><div class="row">${["Male","Female"].map(g=>`<button data-g="${g}" class="${form.gender===g?"on":"ghost"}">${g}</button>`).join("")}</div>
    <div class="lab">Home state</div><div class="row">${Object.keys(STATE_CODE).map(s=>`<button data-s="${s}" class="${form.state===s?"on":"ghost"}">${s}</button>`).join("")}</div>
    <p class="err" id="f_err">${esc(extra||"")}</p><div class="row"><button data-t="submit">Submit application</button><button data-t="close" class="ghost">Cancel</button></div>`;
  if(step==="work")h+=`<p>${esc(extra.text)}</p><div class="bar"><i style="width:${extra.pct}%"></i></div>`;
  if(step==="cert"){const c=me.cert;if(!c.image&&!c.making){c.making=true;issueCertificate(c).then(()=>{c.making=false;if(talking)talk("cert",extra)})}h+=`<p>${extra?"Your application is approved. Here is your birth certificate. Welcome to Delta City.":"Here is your certificate."}</p>
    ${c.image?`<img class="certimg" src="${c.image}" alt="Certificate of Birth for ${esc(c.name)}, number ${esc(c.no)}">`:`<p>Preparing the certificate...</p>`}
    ${extra?`<p><b>How to enter the city:</b> turn to your left. Blue arrows on the floor lead to the gate marked CITY ENTRANCE, on the left wall of this hall. Its light is now green. Walk through it.</p>`:""}
    <div class="row">${extra?`<button data-t="way">Show me the way</button>`:""}<button data-t="close" class="${extra?"ghost":""}">${extra?"Thank you":"Close"}</button></div>`}
  el.innerHTML=h;const first=el.querySelector("input");if(first&&step==="form"&&!extra)first.focus()}
function closeTalk(){talking=false;document.getElementById("talk").hidden=true;guide()}
// the line of directions at the top of the screen
function guide(){const el=document.getElementById("guide");let s="";
  if(me.role==="newcomer")s=me.inside?"Step 2 of 3: follow the teal line to Registration and speak to Violet.":"Step 1 of 3: walk through the border gate and into the blue doorway marked Arrivals.";
  else if(me.role==="citizen"&&me.inside)s="Step 3 of 3: you have your birth certificate. Follow the blue arrows on the floor to the CITY ENTRANCE, on the left side of the hall, and walk through.";
  el.textContent=s;el.hidden=!s||talking}
function keepForm(){const n=document.getElementById("f_name"),d=document.getElementById("f_dob");if(n)form.name=n.value;if(d)form.dob=d.value}
function submitForm(){keepForm();const name=form.name.replace(/\s+/g," ").trim(),missing=[];if(!name)missing.push("character name");if(!form.gender)missing.push("gender");if(!form.state)missing.push("home state");
  if(missing.length)return talk("form","Please fill in: "+missing.join(", ")+".");
  const steps=[[15,"Checking your details..."],[40,"Checking that the name is not already in use..."],[65,"Preparing your identity record..."],[90,"Issuing your birth certificate..."],[100,"Done."]];let k=0;
  const next=()=>{if(k<steps.length){talk("work",{pct:steps[k][0],text:steps[k][1]});k++;setTimeout(next,750)}else{
    me.cert={no:"DC-"+STATE_CODE[form.state]+"-"+String(1+Math.floor(Math.random()*9000)).padStart(4,"0"),name,dob:form.dob.replace(/\s+/g," ").trim(),gender:form.gender,state:form.state,date:new Date().toLocaleDateString("en-GB",{day:"2-digit",month:"long",year:"numeric"})};
    issueCertificate(me.cert).then(()=>{me.role="citizen";ui();talk("cert",true);toast("Your birth certificate has been issued. The city entrance is now open to you.")})}};next()}
document.getElementById("talk").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;if(b.dataset.g){keepForm();form.gender=b.dataset.g;return talk("form")}if(b.dataset.s){keepForm();form.state=b.dataset.s;return talk("form")}
  const t=b.dataset.t;if(t==="close")closeTalk();else if(t==="way"){closeTalk();me.yaw=Math.PI/2;me.pitch=-.12;guide()}else if(t==="form")talk("form");else if(t==="submit")submitForm();else if(t==="cert")talk("cert",false)});
document.getElementById("act").addEventListener("click",()=>talk("hello"));

/* ================================ controls ================================ */
const touch=matchMedia("(pointer:coarse)").matches||"ontouchstart" in window;if(touch)document.body.classList.add("touch");
const typing=e=>e.target&&(e.target.tagName==="INPUT"||e.target.tagName==="TEXTAREA");
addEventListener("keydown",e=>{if(typing(e))return;const k=e.key.toLowerCase();keys[k]=true;if((k==="e"||k==="enter")&&nearViolet()&&!talking&&!busy)talk("hello");if(k==="escape"&&talking)closeTalk()});addEventListener("keyup",e=>{keys[e.key.toLowerCase()]=false});
const stick=document.getElementById("stick"),knob=document.getElementById("knob");let stickId=null,lookId=null,lx=0,ly=0;
function stickMove(e){const r=stick.getBoundingClientRect();let dx=(e.clientX-r.left-r.width/2)/(r.width/2),dy=(e.clientY-r.top-r.height/2)/(r.height/2);const l=Math.hypot(dx,dy);if(l>1){dx/=l;dy/=l}input.x=dx;input.y=-dy;knob.style.transform=`translate(${dx*37}px,${dy*37}px)`}
stick.addEventListener("pointerdown",e=>{stickId=e.pointerId;stick.setPointerCapture(e.pointerId);stickMove(e);e.stopPropagation()});stick.addEventListener("pointermove",e=>{if(e.pointerId===stickId)stickMove(e)});
const stickEnd=e=>{if(e.pointerId===stickId){stickId=null;input.x=input.y=0;knob.style.transform=""}};stick.addEventListener("pointerup",stickEnd);stick.addEventListener("pointercancel",stickEnd);
cv.addEventListener("pointerdown",e=>{if(lookId===null){lookId=e.pointerId;lx=e.clientX;ly=e.clientY;cv.setPointerCapture(e.pointerId)}});
cv.addEventListener("pointermove",e=>{if(e.pointerId!==lookId)return;me.yaw+=(e.clientX-lx)*.005;me.pitch=clamp(me.pitch+(e.clientY-ly)*.004,-1.1,1.1);lx=e.clientX;ly=e.clientY});
const lookEnd=e=>{if(e.pointerId===lookId)lookId=null};cv.addEventListener("pointerup",lookEnd);cv.addEventListener("pointercancel",lookEnd);
function ui(){guide();const el=document.getElementById("picks");el.innerHTML="";const add=(label,fn)=>{const b=document.createElement("button");b.textContent=label;b.addEventListener("click",fn);el.appendChild(b);return b};
  add("You are: "+ROLES.find(r=>r[0]===me.role)[1]+"  (tap to change)",()=>{const i=(ROLES.findIndex(r=>r[0]===me.role)+1)%ROLES.length;me.role=ROLES[i][0];
    if(me.role==="newcomer")me.cert=null;else if(!me.cert)me.cert={no:"DC-ASB-0001",name:"Sample Citizen",dob:"01 September 1996",gender:"Female",state:"Asaba",date:"10 October 2026"};ui();
    toast({newcomer:"A new arrival: the public hall only. The city stays shut until Violet issues your certificate.",citizen:"A citizen: the public hall and the city.",officer:"An immigration officer: the restricted side and the Deputy's office, but not the Comptroller-General's.",deputy:"The Deputy Comptroller-General: everywhere.",cg:"The Comptroller-General: everywhere."}[me.role])});
  add("Start again at the border",()=>fadeTo("The border gate",()=>{me.inside=false;me.x=0;me.z=50;me.yaw=0;me.role="newcomer";me.cert=null;form.name=form.dob=form.gender=form.state="";closeTalk()}));
  document.getElementById("tip").textContent=me.inside?(touch?"Left thumb: walk. Drag elsewhere: look. Walk up to Violet at Registration to talk to her.":"Walk with W A S D or the arrow keys, drag to look around. Walk up to Violet at Registration and press E to talk to her.")
    :(touch?"Left thumb: walk. Drag elsewhere: look. Go through the gate and into the blue doorway marked Arrivals.":"Walk with W A S D or the arrow keys, drag to look around. Go through the gate and into the blue doorway marked Arrivals.")}
ui();requestAnimationFrame(frame);
loadPerson({jacket:TEAL,legs:CHAR}).then(p=>{VIOLET_BODY=p}).catch(()=>toast("Violet could not be shown, but you can still talk to her at the Registration counter."));
</script>
</body>
</html>
