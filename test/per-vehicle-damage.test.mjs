// Per-vehicle damage persistence — runs the REAL crashWrite/crashLoad/garResume/garPlace code from
// index.html (extracted into a vm sandbox, same approach as test/vehicle-damage.mjs) against a stubbed
// town. Proves:
//   * crashWrite snapshots EVERY spawned vehicle keyed by its own id — damage to one never overwrites another
//   * switching focus (T.car) and re-writing leaves the other vehicles' snapshots intact
//   * refresh (crashLoad) restores each vehicle's own snapshot
//   * storing + retrieving a damaged vehicle keeps its damage (garResume picks the right snapshot by id)
//   * legacy saves (a single "car" entry, no "cars" map) still restore the old way
// No Supabase involved: this is the client-side overlay; the server side (veh_update/veh_store/veh_merge_damage)
// is already keyed by vehicle id in supabase_vehicles.sql and needs no migration.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";
import test from "node:test";
import assert from "node:assert/strict";

const REPO = fileURLToPath(new URL("..", import.meta.url));
const html = readFileSync(REPO + "/index.html", "utf8");
const blocks = html.match(/<script>([\s\S]*?)<\/script>/g) || [];
let src = "";
for (const b of blocks) {
  const inner = b.replace(/^<script>/, "").replace(/<\/script>$/, "");
  if (inner.length > src.length) src = inner;
}

// same statement extractor as test/vehicle-damage.mjs
function extractStmt(source, name) {
  const pats = [
    new RegExp(`function\\s+${name}\\s*\\(`),
    new RegExp(`const\\s+${name}\\s*=`),
    new RegExp(`let\\s+${name}\\s*=`),
    new RegExp(`var\\s+${name}\\s*=`),
  ];
  for (const re of pats) {
    const m = re.exec(source);
    if (!m) continue;
    let i = m.index, isFn = false, j;
    if (source.slice(i, i + 8).startsWith("function")) {
      isFn = true;
      let k = source.indexOf("(", i), depth = 0;
      for (; k < source.length; k++) {
        const c = source[k];
        if (c === "(") depth++;
        else if (c === ")") { depth--; if (!depth) break; }
      }
      while (source[k + 1] && source[k + 1] !== "{") k++;
      j = k + 1;
    } else j = source.indexOf("=", i) + 1;
    let depth = 0, inS = null, esc = false, lineC = false, blockC = false, opened = !isFn;
    for (; j < source.length; j++) {
      const c = source[j], d = source[j + 1];
      if (lineC) { if (c === "\n") lineC = false; continue; }
      if (blockC) { if (c === "*" && d === "/") { blockC = false; j++; } continue; }
      if (inS) { if (esc) esc = false; else if (c === "\\") esc = true; else if (c === inS) inS = null; continue; }
      if (c === "/" && d === "/") { lineC = true; continue; }
      if (c === "/" && d === "*") { blockC = true; j++; continue; }
      if (c === '"' || c === "'" || c === "`") { inS = c; continue; }
      if (c === "{") depth++;
      else if (c === "}") {
        depth--;
        if (!depth && (isFn || opened)) return source.slice(i, j + 1);
      } else if (!opened) opened = true;
    }
  }
  return null;
}

function makeGame() {
  const store = {};
  const g = {
    console,
    setTimeout: () => 0,
    clearTimeout: () => {},
    localStorage: {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: (k) => { delete store[k]; },
    },
    CRASH: { KEY: "deltaCityCrash" },
    netStreet: () => {},
    netV: () => {},
    DYN: { debris: [] },
    dynProps: () => {},
    dynSet: () => {},
    treeFall: () => {},
    fireCheckD: () => {},
    townOf: (s) => g.TOWNS[s],
    me: { town: "alpha" },
    scene: "town",
    cam: { x: 0, z: 0 },
    PARKLIST: [],
    GAR: { list: [], parks: [], out: [0, 0, "alpha"], skew: 0 },
    TOW: null,
    CARSEQ: null,
    CARUI: { door: { hidden: true } },
    CARS: { sovereign: { name: "Sovereign" } },
    VEH: { gear: "P" },
    carPt: () => [0, 0, 0],
    carDoors: () => ({ driver: { stand: [0, 0, 0] } }),
    driving: null,
    garGone: (T, C) => { if (T.car !== C) return; if (T.cars) { const k = T.cars.indexOf(T.car); if (k >= 0) T.cars.splice(k, 1); } T.car = T.cars && T.cars.length ? T.cars[T.cars.length - 1] : null; },
    toast: () => {},
    vehicleLetGo: () => {},
    sndUpdate: () => {},
    dashUpdate: () => {},
    carD: (C) => { C.dmg = C.dmg || { ver: 0 }; C.v = C.v || 0; C.health = 100; },
    crashSave: () => {},
    TOWNS: { alpha: { map: { dyn: [] }, marks: [], treeInst: [], parks: [{ id: "p1", name: "Lot", bays: [{ i: 0, x: 1, z: 2, yaw: 0 }] }] } },
  };
  vm.createContext(g);
  for (const name of ["crashWrite", "crashLoad", "garMine", "garResume", "garPlace"]) {
    const code = extractStmt(src, name);
    assert.ok(code, `extracted ${name} from index.html`);
    vm.runInContext(code, g, { filename: `extract-${name}.js` });
  }
  return { g, store };
}

// a fresh world with three different vehicles out, each damaged differently
function seed(g, vid, dmg, x) {
  const T = g.TOWNS.alpha;
  T.cars = T.cars || [];
  const C = { x, z: 5, yaw: 0.3, v: 0, vid: vid, token: `t${vid}`, mine: true, abandonedAt: 0 };
  g.carD(C);
  C.dmg = Object.assign(C.dmg, dmg, { ver: 0 });
  T.cars.push(C);
  T.car = C;
  return C;
}

const plain = (d) => JSON.parse(JSON.stringify(d)); // normalise cross-realm objects (vm context)

const dmgA = { bumperF: 0.42, coolant: 0.9 };
const dmgB = { sideR: 0.61, tyre: [0.5, 1, 1, 1] };
const dmgC = { engine: 0.88 };

test("crashWrite snapshots every vehicle under its own id; focus never overwrites the others", () => {
  const { g } = makeGame();
  seed(g, 11, dmgA, 1);
  seed(g, 22, dmgB, 2);
  seed(g, 33, dmgC, 3);

  g.crashWrite();
  let saved = JSON.parse(g.localStorage.getItem(g.CRASH.KEY));
  assert.ok(saved.alpha.cars, "a per-vehicle 'cars' map is written");
  assert.deepEqual(saved.alpha.cars["11"], Object.assign({ ver: 0 }, dmgA), "vehicle 11 keeps its own snapshot");
  assert.deepEqual(saved.alpha.cars["22"], Object.assign({ ver: 0 }, dmgB), "vehicle 22 keeps its own snapshot");
  assert.deepEqual(saved.alpha.cars["33"], Object.assign({ ver: 0 }, dmgC), "vehicle 33 keeps its own snapshot");
  assert.equal(saved.alpha.car.vid, 33, "legacy 'car' slot still holds the focused vehicle");

  // switch focus to vehicle 22 and write again — the others must be untouched
  const T = g.TOWNS.alpha;
  T.car = T.cars[1];
  g.crashWrite();
  saved = JSON.parse(g.localStorage.getItem(g.CRASH.KEY));
  assert.deepEqual(saved.alpha.cars["11"], Object.assign({ ver: 0 }, dmgA), "11 unchanged after focus switched to 22");
  assert.deepEqual(saved.alpha.cars["33"], Object.assign({ ver: 0 }, dmgC), "33 unchanged after focus switched to 22");
  assert.equal(saved.alpha.car.vid, 22, "legacy slot now holds 22");

  // damage the new focus harder — still only 22 changes
  T.car.dmg.bumperR = 0.99;
  g.crashWrite();
  saved = JSON.parse(g.localStorage.getItem(g.CRASH.KEY));
  assert.deepEqual(saved.alpha.cars["11"], Object.assign({ ver: 0 }, dmgA), "11 unchanged after 22 took more damage");
  assert.equal(saved.alpha.cars["22"].sideR, 0.61, "22's own keys preserved");
  assert.equal(saved.alpha.cars["22"].bumperR, 0.99, "22's new damage recorded");
  assert.deepEqual(saved.alpha.cars["33"], Object.assign({ ver: 0 }, dmgC), "33 unchanged");
});

test("refresh restores each vehicle's own snapshot via crashLoad", () => {
  const { g } = makeGame();
  seed(g, 11, dmgA, 1);
  seed(g, 22, dmgB, 2);
  seed(g, 33, dmgC, 3);
  g.crashWrite();

  // simulate a page refresh: brand-new town, same localStorage
  const before = g.localStorage.getItem(g.CRASH.KEY);
  g.TOWNS.alpha = { map: { dyn: [] }, marks: [], treeInst: [], parks: [{ id: "p1", name: "Lot", bays: [{ i: 0, x: 1, z: 2, yaw: 0 }] }] };
  g.localStorage.setItem(g.CRASH.KEY, before);
  g.crashLoad("alpha", g.TOWNS.alpha);

  assert.ok(g.TOWNS.alpha.savedCars, "the per-vehicle map is loaded on refresh");
  assert.deepEqual(plain(g.TOWNS.alpha.savedCars["11"]), Object.assign({ ver: 0 }, dmgA), "11's damage restored");
  assert.deepEqual(plain(g.TOWNS.alpha.savedCars["22"]), Object.assign({ ver: 0 }, dmgB), "22's damage restored");
  assert.deepEqual(plain(g.TOWNS.alpha.savedCars["33"]), Object.assign({ ver: 0 }, dmgC), "33's damage restored");
  assert.ok(g.TOWNS.alpha.savedCar && g.TOWNS.alpha.savedCar.vid === 33, "legacy single-car restore still happens");
});

test("store + retrieve: garResume gives each vehicle its own damage, then consumes the snapshot", () => {
  const { g } = makeGame();
  seed(g, 11, dmgA, 1);
  seed(g, 22, dmgB, 2);
  seed(g, 33, dmgC, 3);
  g.crashWrite();
  const before = g.localStorage.getItem(g.CRASH.KEY);

  // simulate a refresh: brand-new town, same localStorage — the snapshots load ONCE, like a real page load
  g.TOWNS.alpha = { map: { dyn: [] }, marks: [], treeInst: [], parks: [{ id: "p1", name: "Lot", bays: [{ i: 0, x: 1, z: 2, yaw: 0 }] }] };
  const T = g.TOWNS.alpha;
  g.crashLoad("alpha", T);

  const resume = (vid) => {
    // what the server reports for this vehicle: the vehicle row carries its own damage (per-vehicle column)
    g.GAR.list = [{ id: vid, out_by_me: true, token: `t${vid}`, state: "alpha", park: "p1", in_bay: 0, pos: null, damage: {} }];
    T.car = null; // after a real refresh the world is empty until a resume places a vehicle
    g.garResume();
    const C = T.cars.find((q) => q.vid === vid);
    assert.ok(C, `vehicle ${vid} is back in the world after retrieve`);
    return C;
  };

  const c11 = resume(11);
  const dmgKeys = (d) => { const o = plain(d); delete o.ver; delete o.pos; delete o.vid; return o; };
  const snapKeys = (d) => { const o = plain(d); delete o.ver; delete o.pos; delete o.vid; return o; };
  assert.deepEqual(dmgKeys(c11.dmg), Object.assign({}, dmgA), "vehicle 11 retrieved with ITS damage (bumperF 0.42)");
  // 11's snapshot is consumed by its own resume; the other two survive untouched
  assert.equal(T.savedCars["11"], undefined, "11's snapshot consumed after its resume");
  assert.deepEqual(snapKeys(T.savedCars["22"]), Object.assign({}, dmgB), "22's snapshot survived 11's resume");
  assert.deepEqual(snapKeys(T.savedCars["33"]), Object.assign({}, dmgC), "33's snapshot survived 11's resume");
  const c22 = resume(22);
  assert.deepEqual(dmgKeys(c22.dmg), Object.assign({}, dmgB), "vehicle 22 retrieved with ITS damage (sideR 0.61), not 11's");
  assert.equal(T.savedCars["22"], undefined, "22's snapshot consumed after its resume");
  assert.deepEqual(snapKeys(T.savedCars["33"]), Object.assign({}, dmgC), "33's snapshot survived 22's resume");
  const c33 = resume(33);
  assert.deepEqual(dmgKeys(c33.dmg), Object.assign({}, dmgC), "vehicle 33 retrieved with ITS damage (engine 0.88), not the other two");
  assert.equal(T.savedCars["33"], undefined, "33's snapshot consumed after its resume");
  assert.equal(T.savedCars["11"], undefined, "no snapshot re-created for already-resumed vehicle 11");
});

test("legacy save (single 'car', no 'cars' map) still restores via savedCar", () => {
  const { g } = makeGame();
  const legacy = {
    alpha: { dyn: {}, marks: [], trees: [], car: { bumperF: 0.5, vid: 77, pos: [1, 2, 0.3] } },
  };
  g.localStorage.setItem(g.CRASH.KEY, JSON.stringify(legacy));
  const T = g.TOWNS.alpha;
  g.crashLoad("alpha", T);
  assert.ok(T.savedCar && T.savedCar.vid === 77, "legacy single-car slot loaded");
  assert.equal(T.savedCars, undefined, "no cars map invented for a legacy save");

  // resume with only the legacy slot present: the vid still matches and the damage applies
  g.GAR.list = [{ id: 77, out_by_me: true, token: "t77", state: "alpha", park: "p1", in_bay: 0, pos: null, damage: {} }];
  g.garResume();
  const C = T.cars.find((q) => q.vid === 77);
  assert.ok(C, "legacy vehicle resumed");
  assert.equal(C.dmg.bumperF, 0.5, "legacy damage applied, pos/vid stripped");
  assert.equal(C.dmg.vid, undefined, "no stray vid key on the live damage object");
});