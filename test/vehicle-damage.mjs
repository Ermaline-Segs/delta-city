import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";
const REPO = fileURLToPath(new URL("..", import.meta.url));
function gameScript(html){
  const m = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
  let best = "";
  for (const blk of m) { const inner = blk.replace(/^<script>/, "").replace(/<\/script>$/, ""); if (inner.length > best.length) best = inner; }
  return best;
}
function extractStmt(src, name){
  const pats = [new RegExp(`function\\s+${name}\\s*\\(`), new RegExp(`const\\s+${name}\\s*=`), new RegExp(`let\\s+${name}\\s*=`), new RegExp(`var\\s+${name}\\s*=`), new RegExp(`const\\s+${name}\\b`), new RegExp(`let\\s+${name}\\b`)];
  for (const re of pats){
    const m = re.exec(src);
    if (!m) continue;
    let i = m.index, isFn = false, j;
    if (src.slice(i, i + 8).startsWith("function")){
      isFn = true;
      let k = src.indexOf("(", i), depth = 0;
      for (; k < src.length; k++){ const c = src[k]; if (c === "(") depth++; else if (c === ")"){ depth--; if (!depth) break; } }
      while (src[k + 1] && src[k + 1] !== "{") k++;
      j = k + 1;
    } else j = src.indexOf("=", i) + 1;
    let depth = 0, inS = null, esc = false, lineC = false, blockC = false, opened = !isFn;
    for (; j < src.length; j++){
      const c = src[j], d = src[j + 1];
      if (lineC){ if (c === "\n") lineC = false; continue; }
      if (blockC){ if (c === "*" && d === "/"){ blockC = false; j++; } continue; }
      if (inS){ if (esc) esc = false; else if (c === "\\") esc = true; else if (c === inS) inS = null; continue; }
      if (c === "/" && d === "/"){ lineC = true; continue; }
      if (c === "/" && d === "*"){ blockC = true; j++; continue; }
      if (c === '"' || c === "'" || c === "`"){ inS = c; continue; }
      if (c === "(" || c === "{" || c === "["){ depth++; if (depth > 0) opened = true; }
      else if (c === ")" || c === "}" || c === "]"){ depth--; if (depth === 0 && opened && isFn && c === "}") { j++; break; } if (depth < 0) break; }
      else if (c === ";" && depth === 0){ j++; break; }
    }
    return src.slice(i, j);
  }
  throw new Error(`symbol not found: ${name}`);
}
const SYMS = ["CRASH", "CARPARTS", "carDmg0", "clamp01", "clamp", "carModelId", "isBike", "carD", "crashCar", "bikeCrash", "VEHICLES", "vehParts", "vehPrice", "vehMins", "repairItems", "repairFull", "carHealth", "driverHurt", "TYRENAME", "dmgChance"];
function buildSandbox(src){
  const code = SYMS.map((s) => extractStmt(src, s)).join("\n;\n") + "\n;this.__x={carDmg0,clamp01,carModelId,isBike,carD,crashCar,CRASH,VEHICLES,vehParts,vehPrice,vehMins,repairItems,repairFull,carHealth,driverHurt,TYRENAME,dmgChance,VEH};";
  const ctx = vm.createContext({ console, Math, JSON, crashSave(){}, fireStart(){}, setTimeout(){ return 0; }, localStorage: { getItem(){ return null; }, setItem(){}, removeItem(){} }, fxSparks(){}, fxEmit(){}, carWorld(){ return [0, 0, 0]; }, CARFX: { batt: [0, 0, 0], rad: [0, 0, 0], sump: [0, 0, 0], fuel: [0, 0, 0] }, VEH: { model: null, helmet: false } });
  vm.runInContext(code, ctx, { filename: "game-extract.js" });
  return ctx.__x;
}
function runVehicle(X, model, v, scenario){
  const vMs = v / 3.6;
  const C = { model };
  X.carD(C);
  if (scenario === "wall"){
    const F = X.CRASH.fixed.wall;
    const dv = (1 + F.e) * vMs;
    X.crashCar(C, dv, { zone: "F", x: 0, z: 0, w: F.w, low: F.low, hard: true });
  } else {
    for (let i = 0; i < 2; i++) X.crashCar(C, vMs, { zone: "F", x: 0, z: 0, w: 0.4, low: true });
  }
  return X.carHealth(C.dmg);
}
function dmgParts(X, model, v, scenario){
  const vMs = v / 3.6;
  const C = { model };
  X.carD(C);
  if (scenario === "wall"){
    const F = X.CRASH.fixed.wall;
    const dv = (1 + F.e) * vMs;
    X.crashCar(C, dv, { zone: "F", x: 0, z: 0, w: F.w, low: F.low, hard: true });
  } else {
    for (let i = 0; i < 2; i++) X.crashCar(C, vMs, { zone: "F", x: 0, z: 0, w: 0.4, low: true });
  }
  const parts = X.vehParts(model).parts.map(p => p[0]);
  const out = {};
  for (const k of parts) out[k] = +(C.dmg[k] || 0).toFixed(4);
  out.dead = !!C.dmg.dead;
  out.burnt = !!C.dmg.burnt;
  out.fire = !!C.dmg.fire || !!C.dmg.fireNext;
  return out;
}
const failures = [];
function check(name, cond, detail){
  if (cond) console.log("PASS  " + name);
  else { console.log("FAIL  " + name + (detail ? "  (" + detail + ")" : "")); failures.push(name); }
}
const cur = buildSandbox(gameScript(readFileSync(`${REPO}/index.html`, "utf8")));

// --- real wall path proof: restitution factor 1.12 (e=0.12, hard=true) ---
const WF = cur.CRASH.fixed.wall;
check("wall path: CRASH.fixed.wall.e === 0.12 (dv = (1+e)*speed => 1.12x)", WF.e === 0.12, "e=" + WF.e);
check("wall path: CRASH.fixed.wall.w === 1.6 (fixture width; handler passes hard:true to crashCar)", WF.w === 1.6, "w=" + WF.w);

// --- BIKE acceptance rows (six) ---
const bikeAcc = [
  ["bump", 10, 99, 100, "bike bump 10 km/h >= 99"],
  ["bump", 20, 95, 96, "bike bump 20 km/h in 95-96"],
  ["bump", 30, 85, 88, "bike bump 30 km/h in 85-88"],
  ["wall", 40, 64, 70, "bike wall 40 km/h in 64-70"],
  ["wall", 50, 42, 48, "bike wall 50 km/h in 42-48"],
  ["wall", 60, 18, 26, "bike wall 60 km/h in 18-26"],
];
console.log("\nBIKE acceptance rows:");
for (const [sc, v, lo, hi, label] of bikeAcc){
  const h = runVehicle(cur, "m_bike", v, sc);
  check(label, h >= lo && h <= hi, `health=${h}, want ${lo}-${hi}`);
  console.log(`      ${sc} ${v} km/h -> ${h}% (want ${lo}-${hi})`);
}

// --- monotonic: health never increases with speed, 5..70 both scenarios ---
for (const sc of ["bump", "wall"]){
  let prev = null, ok = true;
  for (let v = 5; v <= 70; v += 5){
    const h = runVehicle(cur, "m_bike", v, sc);
    if (prev != null && h > prev) ok = false;
    prev = h;
  }
  check(`bike ${sc} health monotonic non-increasing 5..70 km/h`, ok);
}

// --- SOVEREIGN GT: 12 rows, exact health + per-part (baseline 9531b51) ---
const GT = {
  "10 bump":  { h: 98, p: { bumperF: 0.311, under: 0.0167 } },
  "10 wall":  { h: 99, p: { bumperF: 0.178 } },
  "20 bump":  { h: 92, p: { radiator: 0.1333, bumperF: 0.686, grille: 0.147, under: 0.4333, oilLeak: 0.1167 } },
  "20 wall":  { h: 97, p: { bumperF: 0.388, bonnet: 0.0933, grille: 0.15, ws: 0.0125 } },
  "30 bump":  { h: 80, p: { radiator: 0.55, bumperF: 1, grille: 0.4095, under: 0.85, oilLeak: 0.605, elec: 0.03, steer: 0.075, ws: 0.1313 } },
  "30 wall":  { h: 90, p: { radiator: 0.15, bumperF: 0.598, bonnet: 0.28, grille: 0.36, elec: 0.06, steer: 0.075, ws: 0.1875, hlL: 1, hlR: 1 } },
  "40 bump":  { h: 68, p: { susp: 0.2427, radiator: 0.9667, bumperF: 1, bonnet: 0.1333, grille: 0.672, under: 1, oilLeak: 1, elec: 0.28, steer: 0.2833, ws: 0.2875 } },
  "40 wall":  { h: 81, p: { susp: 0.1633, radiator: 0.3833, bumperF: 0.808, bonnet: 0.4667, grille: 0.57, oilLeak: 0.1867, elec: 0.2, steer: 0.1917, ws: 0.3625, hlL: 1, hlR: 1 } },
  "50 bump":  { h: 54, p: { engine: 0.165, chassis: 0.05, susp: 0.6218, radiator: 1, bumperF: 1, bonnet: 0.3417, grille: 0.9345, under: 1, oilLeak: 1, elec: 0.53, steer: 0.4917, ws: 0.4438, hlL: 1, hlR: 1 } },
  "50 wall":  { h: 67, p: { engine: 0.195, chassis: 0.1, susp: 0.3267, radiator: 0.6167, bumperF: 1, bonnet: 0.6533, grille: 0.78, oilLeak: 0.3733, elec: 0.34, steer: 0.3083, ws: 0.5375, hlL: 1, hlR: 1 } },
  "60 bump":  { h: 35, p: { engine: 0.54, chassis: 0.3, susp: 1, radiator: 1, bumperF: 1, bonnet: 0.55, grille: 1, under: 1, oilLeak: 1, elec: 0.78, steer: 0.7, ws: 0.6, hlL: 1, hlR: 1 } },
  "60 wall":  { h: 53, p: { engine: 0.405, chassis: 0.24, susp: 0.49, radiator: 0.85, bumperF: 1, bonnet: 0.84, grille: 0.99, oilLeak: 0.56, elec: 0.48, steer: 0.425, ws: 0.7125, hlL: 1, hlR: 1 } },
};
console.log("\nSOVEREIGN GT 12 rows (expected = baseline 9531b51, byte-identical per-part):");
for (const v of [10, 20, 30, 40, 50, 60]){
  for (const sc of ["bump", "wall"]){
    const key = v + " " + sc;
    const d = dmgParts(cur, "m_sgt", v, sc);
    const h = runVehicle(cur, "m_sgt", v, sc);
    const exp = GT[key];
    const partNames = Object.keys(d).filter(k => !["dead", "burnt", "fire"].includes(k));
    const partBad = partNames.filter(k => Math.abs((d[k] || 0) - ((exp.p[k] !== undefined ? exp.p[k] : 0)) > 1e-9));
    check(`GT ${key} health === ${exp.h}`, h === exp.h, `got ${h}`);
    check(`GT ${key} per-part identical to baseline`, partBad.length === 0, "differing parts: " + partBad.map(k => `${k} got=${d[k]} want=${exp.p[k] ?? 0}`).join(", "));
    console.log(`      ${key} H=${h} expected=${exp.h}`);
  }
}

// --- Rule B repairs ---
function repairFor(X, model, frac){
  const C = { model };
  X.carD(C);
  const { parts } = X.vehParts(model);
  for (const [k] of parts) C.dmg[k] = frac;
  C.dmg.engine = frac; C.dmg.chassis = frac; C.dmg.susp = frac; C.dmg.brakes = frac; C.dmg.radiator = frac;
  let price, mins;
  try { const r = X.repairFull(C.dmg); price = r.price ?? r.cost; mins = r.mins ?? r.time; } catch (e) {}
  if (price == null){
    const list = X.repairItems(C.dmg);
    price = list.reduce((a, it) => a + (it.price || it.cost || 0), 0);
    mins = list.reduce((a, it) => a + (it.mins || it.time || 0), 0);
  }
  return { price, mins: Math.round(mins * 10) / 10 };
}
console.log("\nRule B repairs:");
const reps = [
  ["m_bike", 1, 90000, 15], ["m_bike", 0.5, 44500, 8], ["m_bike", 0.1, 13500, 3],
  ["m_sgt", 1, 270000, 15], ["m_sgt", 0.5, 134500, 7], ["m_sgt", 0.1, 47000, 3],
];
for (const [m, f, wantP, wantM] of reps){
  const r = repairFor(cur, m, f);
  check(`repair ${m} ${f * 100}% price K${wantP.toLocaleString("en-US")}`, r.price === wantP, `got K${r.price}`);
  check(`repair ${m} ${f * 100}% mins ${wantM} (rounded)`, Math.round(r.mins) === wantM, `got ${r.mins}`);
  console.log(`      ${m} ${f * 100}% -> K${r.price.toLocaleString("en-US")} / ${r.mins} min (want K${wantP.toLocaleString("en-US")} / ${wantM} min)`);
}

// --- helmet ON/OFF driverHurt (real wall path, 1.12x restitution) ---
console.log("\nHelmet driverHurt (bike wall crash, real dv = 1.12 * v/3.6):");
for (const v of [30, 50, 60]){
  const dv = 1.12 * (v / 3.6);
  for (const on of [true, false]){
    cur.VEH.model = "m_bike"; cur.VEH.helmet = on;
    const hurt = cur.driverHurt(dv);
    const want = on ? "injured (helmet on)" : "badly hurt (no helmet)";
    check(`helmet ${on ? "ON" : "OFF"} wall ${v} km/h driverHurt === ${JSON.stringify(want)}`, hurt === want, `got ${JSON.stringify(hurt)}`);
    console.log(`      ${v} km/h ${on ? "ON " : "OFF"} -> ${JSON.stringify(hurt)} (dv=${dv.toFixed(3)})`);
  }
}

console.log("");
if (failures.length){ console.log(`RESULT: ${failures.length} FAILURE(S)`); process.exit(1); }
console.log("RESULT: ALL CHECKS PASSED");