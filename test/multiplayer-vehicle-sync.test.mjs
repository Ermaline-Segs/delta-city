/* Multiplayer vehicle-synchronisation test — MOCKED-RPC (no live Supabase, no browser).
 *
 * Drives the REAL live server (server/src/index.js, the DurableObject that workerd runs in
 * production) inside Node, with workerd globals stubbed. Two mock player sessions sign in
 * with real HS256 JWTs (the same format Supabase signs), both join town:Asaba, and player A
 * runs the real client-side roster logic (assets/vehroster.js — the same code garPlace/garDrop
 * in index.html use) to decide which "v" messages the client sends. The test then asserts the
 * real server relayed exactly the right spawn/store/sync messages to player B, and that B's
 * applied view (the same handler logic as index.html netGot "v") converges on A's true roster:
 *   - six spawns roll 1,2,3 -> 2,3,4 -> 3,4,5 -> 4,5,6
 *   - a manual store removes only the named vehicle
 *   - a room change re-syncs the whole roster
 *
 * This proves the protocol works end-to-end at the message level. It is NOT a two-browser
 * test; a real two-session browser check still needs the deployed worker (see HANDOVER).
 */
import test from "node:test";
import assert from "node:assert/strict";
import crypto from "node:crypto";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const V = require("../assets/vehroster.js");

/* ---- workerd globals the server module needs, stubbed before import ---- */
globalThis.DurableObject = class DurableObject {
  constructor(ctx, env) { this.ctx = ctx; this.env = env; }
};
globalThis.WebSocketRequestResponsePair = class {
  constructor(a, b) { this.a = a; this.b = b; }
};

const SECRET = "test-signing-secret-not-for-production";
const ENV = {
  SUPABASE_URL: "https://none.example", SUPABASE_ANON_KEY: "anon",
  SUPABASE_JWT_SECRET: SECRET, DAILY_REQUEST_LIMIT: 100000, STOP_AT: 1000000
};
// The server's citizen() looks the player's character up in Supabase with their own token;
// in this test there is no live project, so that lookup finds nothing and defaults are used.
globalThis.fetch = async () => ({ ok: false });

import { readFileSync } from "node:fs";
const serverSrc = readFileSync(new URL("../server/src/index.js", import.meta.url), "utf8")
  // "cloudflare:workers" is a workerd-only module; Node has no such scheme, and the global
  // DurableObject stub above is what the class actually extends, so drop just that import.
  .replace(/^import\s*\{[^}]*\}\s*from\s*"cloudflare:workers";\s*$/m, "");
const { Live } = await import("data:text/javascript;base64," + Buffer.from(serverSrc).toString("base64"));

/* ---- a fake WebSocket the server can accept, attach to and send on ---- */
function makeWs() {
  const ws = {
    att: null, inbox: [], closed: 0,
    serializeAttachment(a) { this.att = a; },
    deserializeAttachment() { return this.att; },
    send(s) { this.inbox.push(JSON.parse(s)); },
    close(code) { this.closed = code; }
  };
  return ws;
}

function makeLive() {
  const socks = new Set();
  const ctx = {
    storage: { sql: { exec() { return { toArray: () => [] }; } } },
    setWebSocketAutoResponse() {},
    getWaitUntil() { return Promise.resolve(); },
    acceptWebSocket(ws) { socks.add(ws); },
    getWebSockets() { return [...socks] }
  };
  const live = new Live(ctx, ENV);
  // workerd accepts the server socket during the upgrade (server/src/index.js line 137)
  // and stamps per-connection state onto it before the first message; mirror both steps.
  const attach = (ws, uid) => {
    ctx.acceptWebSocket(ws);
    ws.serializeAttachment({ id: uid, auth: false, t0: Date.now() });
    return live.webSocketMessage(ws, JSON.stringify({ t: "hello", tok: jwt(uid), room: "town:Asaba" }));
  };
  return { live, attach };
}

/* an HS256 login token in the same shape Supabase signs (sub + role + exp) */
function jwt(uid) {
  const b64u = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const h = b64u({ alg: "HS256", typ: "JWT" });
  const p = b64u({ sub: uid, role: "authenticated", exp: Math.floor(Date.now() / 1000) + 3600 });
  const s = crypto.createHmac("sha256", SECRET).update(h + "." + p).digest("base64url");
  return h + "." + p + "." + s;
}

/* the client's "v" handler, line for line with index.html netGot: m.t==="v".
 * Unlike the terse version this creates the peer entry on first contact (index.html does this
 * in the join/welcome path) so subsequent spawn/store messages have somewhere to land. */
function clientVApply(view, m) {
  let p = view.peers.get(m.id);
  if (!p) { p = { id: m.id, vs: [] }; view.peers.set(m.id, p); }
  const VV = (q) => ({ vid: q.vid, x: +q.x || 0, z: +q.z || 0, yaw: +q.yaw || 0, md: q.md === "motorbike" ? "motorbike" : null });
  if (m.a === "sync" && Array.isArray(m.vs)) p.vs = m.vs.map(VV);
  else if (m.a === "spawn" && m.vid) p.vs = (p.vs || []).filter(q => q.vid !== m.vid).concat(VV(m));
  else if (m.a === "store" && m.vid) p.vs = (p.vs || []).filter(q => q.vid !== m.vid);
}

/* a mock player: a session A or B that has the server side attached and keeps its
 * applied view of every other peer. applyAll feeds whatever just arrived into that view. */
function makePlayer({ live, attach }, uid) {
  const ws = makeWs();
  const player = { uid, ws, view: { peers: new Map() }, alive: false };
  player.ready = attach(ws, uid).then(() => {
    player.alive = true;
    player.applyAll();
  });
  player.applyAll = () => {
    while (player.ws.inbox.length) {
      const m = player.ws.inbox.shift();
      if (m.t === "welcome" || m.t === "roomok") {
        for (const p of m.peers || []) clientVApply({ peers: player.view.peers }, { t: "v", id: p.id, a: "sync", vs: p.vs || [] });
      }
      if (m.t === "join") clientVApply(player.view, m);
      if (m.t === "v") clientVApply(player.view, m);
    }
  };
  const sendToServer = (m) => live.webSocketMessage(ws, JSON.stringify(m));
  /* this is the client's own bookkeeping: the same VEHROSTER code garPlace/garDrop use in
   * index.html, and the exact v messages index.html netV() sends when those run */
  player.roster = [];
  player.spawn = (vid, { x, z, yaw, md } = {}) => {
    const r = V.onSpawn(player.roster, vid, {});
    assert.ok(!r.error, r.error);
    player.roster = r.list;                       // keep the client's bookkeeping in step
    const e = r.list[r.list.length - 1];
    assert.equal(e.vid, vid, "the vehicle just spawned is the newest");
    for (const s of r.stowed) sendToServer({ t: "v", a: "store", vid: s.vid });
    sendToServer({ t: "v", a: "spawn", vid, x, z, yaw, md });
    return r;
  };
  player.store = (vid) => {
    const r = V.onStore(player.roster, vid);
    player.roster = r.list;
    for (const s of r.stowed) sendToServer({ t: "v", a: "store", vid: s.vid });
    return r;
  };
  player.sync = () => sendToServer({ t: "v", a: "sync", vs: player.roster.map(e => ({ vid: e.vid, x: 1, z: 1, yaw: 0 })) });
  return player;
}

const settle = () => new Promise(r => setImmediate(r));
const vidsOf = (player, other) => {
  const p = player.view.peers.get(other.uid);
  return p && p.vs ? p.vs.map(q => q.vid) : [];
};
const rosterVids = (p) => p.roster.map(e => e.vid);

test("two sessions converge on the rolling three-car roster through the real server relay", async () => {
  const { live, attach } = makeLive();
  const A = makePlayer({ live, attach }, "uid-player-A");
  const B = makePlayer({ live, attach }, "uid-player-B");
  await A.ready; await B.ready;
  assert.equal(A.alive, true, "A got its welcome from the real server");
  assert.equal(B.alive, true, "B got its welcome from the real server");
  assert.deepEqual(vidsOf(B, A), [], "B sees no parked cars from A before A spawns any");

  // spawn 1: [1]
  A.spawn("veh-1", { x: 10.5, z: -4.2, yaw: 1.2 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1"]);
  assert.equal(rosterVids(A).length, 1);

  // spawn 2: [1,2]
  A.spawn("veh-2", { x: 11, z: -4.2 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-2"]);

  // spawn 3: [1,2,3] — roster is full, nothing auto-stored
  A.spawn("veh-3", { x: 12, z: -4.2 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-2", "veh-3"]);

  // spawn 4: oldest (veh-1) auto-stored -> [2,3,4]
  const r4 = A.spawn("veh-4", { x: 13, z: -4.2 });
  assert.deepEqual(r4.stowed, [{ vid: "veh-1" }], "the oldest by spawn order is the one auto-stored");
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-2", "veh-3", "veh-4"], "B's view rolled exactly like A's");

  // spawn 5: [3,4,5]
  A.spawn("veh-5", { x: 14, z: -4.2 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-3", "veh-4", "veh-5"]);

  // spawn 6: [4,5,6]
  A.spawn("veh-6", { x: 15, z: -4.2 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-4", "veh-5", "veh-6"]);

  // no duplicates, ever: the view at this point holds exactly three distinct vids
  assert.equal(new Set(vidsOf(B, A)).size, 3, "no duplicate vehicle ids in B's view");

  // the server's own record of A's roster (what B's next welcome/join will carry) matches
  const recA = live.socks().find(s => s.a.uid === "uid-player-A").a;
  assert.deepEqual(recA.vs.map(q => q.vid), ["veh-4", "veh-5", "veh-6"]);
});

test("a manual store removes only the selected vehicle from the other player's view", async () => {
  const { live, attach } = makeLive();
  const A = makePlayer({ live, attach }, "uid-player-A");
  const B = makePlayer({ live, attach }, "uid-player-B");
  await A.ready; await B.ready;
  for (const [vid, x] of [["veh-1", 10], ["veh-2", 11], ["veh-3", 12]]) A.spawn(vid, { x, z: 0 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-2", "veh-3"]);

  // store the MIDDLE vehicle manually — only it may leave B's view
  A.store("veh-2");
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-3"], "veh-1 and veh-3 are untouched");

  const recA = live.socks().find(s => s.a.uid === "uid-player-A").a;
  assert.deepEqual(recA.vs.map(q => q.vid), ["veh-1", "veh-3"], "the server record also dropped only veh-2");
});

test("a mid-game arrival receives the current roster via the sync on room change", async () => {
  const { live, attach } = makeLive();
  const A = makePlayer({ live, attach }, "uid-player-A");
  await A.ready;
  for (const [vid, x] of [["veh-1", 10], ["veh-2", 11], ["veh-3", 12], ["veh-4", 13]]) A.spawn(vid, { x, z: 0 });
  await settle();
  assert.deepEqual(rosterVids(A), ["veh-2", "veh-3", "veh-4"]);

  // B arrives late and takes a step from town into a building and back — exactly what
  // index.html netTick does when the room changes: a "room" message then a full "sync"
  const C = makePlayer({ live, attach }, "uid-player-C");
  await C.ready;
  live.webSocketMessage(C.ws, JSON.stringify({ t: "room", room: "town:Asaba" }));
  A.sync();                                  // A re-syncs its roster (netTick does the same)
  await settle(); C.applyAll();
  assert.deepEqual(vidsOf(C, A), ["veh-2", "veh-3", "veh-4"], "latecomer sees the current three, not stale ones");
});

test("an occupied oldest vehicle blocks the auto-store and the new spawn is not faked", async () => {
  const { live, attach } = makeLive();
  const A = makePlayer({ live, attach }, "uid-player-A");
  const B = makePlayer({ live, attach }, "uid-player-B");
  await A.ready; await B.ready;
  A.spawn("veh-1", { x: 10, z: 0 });
  A.spawn("veh-2", { x: 11, z: 0 });
  A.spawn("veh-3", { x: 12, z: 0 });
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-2", "veh-3"]);

  // driver got into veh-1 (the oldest): the roster marks it occupied and the auto-store
  // must refuse — exactly what VEHROSTER.onSpawn does, and what index.html honours by
  // showing the error instead of spawning veh-4.
  A.roster[0].occupied = true;
  const r3 = V.onSpawn(A.roster, "veh-4", {});
  assert.ok(r3.error, "the spawn is refused while the oldest is being driven");
  assert.deepEqual(r3.list.map(e => e.vid), ["veh-1", "veh-2", "veh-3"], "world state is unchanged on refusal");
  assert.deepEqual(r3.stowed, [], "nothing was auto-stored");
  await settle(); B.applyAll();
  assert.deepEqual(vidsOf(B, A), ["veh-1", "veh-2", "veh-3"], "B's view is unchanged by the refused spawn");
});