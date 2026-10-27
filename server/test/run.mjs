// The live server, tested in Cloudflare's own local runtime (wrangler dev) with a stand-in for Supabase:
// a test signing key served as JWKS, and a characters table. Run: npm test (from server/).
import { spawn } from "node:child_process";
import http from "node:http";
import { webcrypto as crypto } from "node:crypto";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join as pjoin } from "node:path";

let PORT = 8787;
const SUPA = 8799, results = [];
const ok = (name, cond, info) => { results.push([name, !!cond]); console.log((cond ? "PASS " : "FAIL ") + name + (info !== undefined ? "  " + JSON.stringify(info).slice(0, 220) : "")) };
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---- a signing key like Supabase's, and tokens for four players ----
const kp = await crypto.subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, true, ["sign", "verify"]);
const pub = Object.assign(await crypto.subtle.exportKey("jwk", kp.publicKey), { kid: "test-key", alg: "ES256", use: "sig" });
const b64u = b => Buffer.from(b).toString("base64url");
async function token(sub, o = {}) {
  const head = b64u(JSON.stringify({ alg: "ES256", kid: o.kid || "test-key", typ: "JWT" }));
  const body = b64u(JSON.stringify(Object.assign({ sub, role: "authenticated", aud: "authenticated", exp: Math.floor(Date.now() / 1000) + 3600 }, o.body || {})));
  const sig = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, kp.privateKey, new TextEncoder().encode(head + "." + body));
  return head + "." + body + "." + b64u(sig);
}
const PEOPLE = { a: ["Ada Admin", "admin"], b: ["Bola", "citizen"], c: ["Chidi", "citizen"], d: ["Dayo", "citizen"] };
const subOf = k => "00000000-0000-0000-0000-00000000000" + k;

// ---- the stand-in for Supabase ----
const supa = http.createServer((req, res) => {
  const u = new URL(req.url, "http://x"), send = (s, o) => { res.writeHead(s, { "content-type": "application/json" }); res.end(JSON.stringify(o)) };
  if (u.pathname === "/auth/v1/.well-known/jwks.json") return send(200, { keys: [pub] });
  if (u.pathname === "/rest/v1/characters") {
    const owner = (u.searchParams.get("owner") || "").replace("eq.", ""), tok = (req.headers.authorization || "").replace("Bearer ", "");
    const sub = JSON.parse(Buffer.from(tok.split(".")[1] || "", "base64url").toString() || "{}").sub;
    if (sub !== owner) return send(200, []);                    // row-level security: only your own row
    const k = Object.keys(PEOPLE).find(k => subOf(k) === owner);
    return send(200, k ? [{ name: PEOPLE[k][0], gender: "Female", look: "party", role: PEOPLE[k][1], home_state: "Asaba" }] : []);
  }
  send(404, {});
}).listen(SUPA, "127.0.0.1");

// ---- the server, in the local runtime ----
async function startServer(vars) {
  const args = ["wrangler", "dev", "--persist-to", mkdtempSync(pjoin(tmpdir(), "dclive-")), "--port", String(PORT), "--ip", "127.0.0.1", "--var", `SUPABASE_URL:http://127.0.0.1:${SUPA}`, ...Object.entries(vars || {}).flatMap(([k, v]) => ["--var", `${k}:${v}`])];
  const p = spawn("npx", args, { env: Object.assign({}, process.env, { WRANGLER_SEND_METRICS: "false", CI: "1" }), stdio: ["ignore", "pipe", "pipe"], detached: true });
  let log = ""; p.stdout.on("data", d => log += d); p.stderr.on("data", d => log += d);
  for (let i = 0; i < 120; i++) { await sleep(500); try { const r = await fetch(`http://127.0.0.1:${PORT}/`); if (r.ok) return p } catch (e) { } }
  console.log(log.slice(-2000)); throw new Error("the server did not start");
}
function stop(p) { return new Promise(r => { p.once("exit", () => setTimeout(r, 500)); try { process.kill(-p.pid, "SIGTERM") } catch (e) { } setTimeout(() => { try { process.kill(-p.pid, "SIGKILL") } catch (e) { } r() }, 4000) }) }      // the whole group: npx, wrangler and the runtime

// a player: a WebSocket that keeps every message it gets
function player(name) {
  const ws = new WebSocket(`ws://127.0.0.1:${PORT}/ws`), P = { ws, name, got: [], closed: null };
  ws.onmessage = e => { try { P.got.push(JSON.parse(e.data)) } catch (x) { P.got.push({ raw: e.data }) } };
  ws.onclose = e => { P.closed = e.code };
  P.open = new Promise((res, rej) => { ws.onopen = res; ws.onerror = () => rej(new Error("connect failed")) });
  P.send = o => ws.send(typeof o === "string" ? o : JSON.stringify(o));
  P.wait = async (fn, ms = 4000) => { const t = Date.now(); while (Date.now() - t < ms) { const m = P.got.find(fn); if (m) return m; await sleep(30) } return null };
  P.count = fn => P.got.filter(fn).length;
  return P;
}
async function join(k, room, x = 0, z = 0) {
  const P = player(k); await P.open; P.send({ t: "hello", tok: await token(subOf(k)), room });
  P.welcome = await P.wait(m => m.t === "welcome"); P.id = P.welcome && P.welcome.id;
  if (x || z) { P.send({ t: "p", x, z, y: 0, a: 0, m: "s", sp: 0 }); await sleep(260) }
  return P;
}

let srv;
try {
  srv = await startServer();
  ok("the server answers", (await (await fetch(`http://127.0.0.1:${PORT}/`)).text()).includes("running"));

  // logins
  const bad = player("x"); await bad.open; bad.send({ t: "hello", tok: "not.a.token", room: "town:Asaba" }); await sleep(600);
  ok("a made-up token is refused", bad.got.some(m => m.t === "err" && m.code === "login") && bad.closed === 4001, bad.got);
  const old = player("x"); await old.open; old.send({ t: "hello", tok: await token(subOf("b"), { body: { exp: Math.floor(Date.now() / 1000) - 600 } }), room: "town:Asaba" }); await sleep(600);
  ok("an expired login is refused", old.closed === 4001, old.got);
  const anon = player("x"); await anon.open; anon.send({ t: "hello", tok: await token(subOf("b"), { body: { role: "anon" } }), room: "town:Asaba" }); await sleep(600);
  ok("an anonymous token is refused", anon.closed === 4001);
  const early = player("x"); await early.open; early.send({ t: "p", x: 1, z: 1 }); await sleep(500);
  ok("nothing is accepted before hello", early.closed === 4001);

  const A = await join("a", "town:Asaba", 10, 10);
  ok("a signed-in player is welcomed, with their name from Supabase", A.welcome && A.id && A.welcome.room === "town:Asaba", A.welcome);
  const B = await join("b", "town:Asaba", 30, 10);
  ok("the next player sees the first one already there", B.welcome.peers.some(p => p.id === A.id && p.name === "Ada Admin" && p.x === 10));
  ok("the first player is told someone joined", !!(await A.wait(m => m.t === "join" && m.id === B.id && m.name === "Bola")));

  // positions: near, far, too far
  A.got.length = 0; B.got.length = 0;
  A.send({ t: "p", x: 12, z: 10, y: 0, a: 1.2, m: "w", sp: 1.4 });
  ok("a near player's move arrives (20 m)", !!(await B.wait(m => m.t === "p" && m.id === A.id && m.x === 12 && m.m === "w")));
  B.got.length = 0;
  for (let i = 0; i < 10; i++) { A.send({ t: "p", x: 130 + i, z: 10, m: "w", sp: 1.4 }); await sleep(260) }
  const farN = B.count(m => m.t === "p" && m.id === A.id);
  ok("a far player (100 m) is sent less often: at most every 2 s", farN >= 1 && farN <= 3, farN);
  B.got.length = 0;
  for (let i = 0; i < 6; i++) { A.send({ t: "p", x: 400 + i, z: 10, m: "w", sp: 1.4 }); await sleep(260) }
  ok("a player over 250 m away is not sent at all", B.count(m => m.t === "p" && m.id === A.id) === 0);
  B.got.length = 0;
  for (let i = 0; i < 10; i++) A.send({ t: "p", x: 20, z: 10, m: "w", sp: 1.4 });
  await sleep(400);
  ok("a flood of updates is cut to at most 5 a second", B.count(m => m.t === "p") <= 3, B.count(m => m.t === "p"));
  A.send({ t: "p", x: 20, z: 10, m: "d", sp: 8, car: { x: 20, z: 10, a: .5, v: 8, st: .1, dr: 1, l: 1 } });
  ok("a car comes with its driver", !!(await B.wait(m => m.t === "p" && m.car && m.car.v === 8 && m.car.dr === 1)));

  // rooms
  const C = await join("c", "gov:Asaba:uni");
  B.got.length = 0;
  await sleep(250); A.send({ t: "room", room: "gov:Asaba:uni", x: 0, z: 5 });
  ok("leaving a room tells the others there", !!(await B.wait(m => m.t === "leave" && m.id === A.id)));
  ok("entering a room tells the people inside", !!(await C.wait(m => m.t === "join" && m.id === A.id)));
  const rok = await A.wait(m => m.t === "roomok");
  ok("the newcomer to a room gets who is there", rok && rok.peers.some(p => p.id === C.id), rok);
  B.got.length = 0; A.send({ t: "p", x: 1, z: 5, m: "w", sp: 1 }); await sleep(500);
  ok("moves inside a building go only to that room", B.count(m => m.t === "p") === 0 && !!(await C.wait(m => m.t === "p" && m.id === A.id)));
  A.send({ t: "room", room: "town:Asaba", x: 20, z: 10 }); await A.wait(m => m.t === "roomok" && m.room === "town:Asaba");

  // chat
  await sleep(1100); B.got.length = 0; C.got.length = 0;
  A.send({ t: "chat", text: "Hello Asaba \u0007" });
  const line = await B.wait(m => m.t === "chat");
  ok("chat reaches the room, with the sender's name", line && line.name === "Ada Admin" && line.text === "Hello Asaba", line);
  ok("chat stays in its room", C.count(m => m.t === "chat") === 0);
  A.send({ t: "chat", text: "again" }); await sleep(300);
  ok("chat is limited to one line a second", B.count(m => m.t === "chat") === 1);

  // the street
  A.send({ t: "st", ch: { "17": { s: 1, b: .3, at: Date.now() }, "18": { s: 3, x: 5, z: 6 } } });
  ok("a knocked street object reaches the others", !!(await B.wait(m => m.t === "st" && m.ch["17"] && m.ch["17"].s === 1)));
  const D = await join("d", "town:Asaba");
  ok("someone arriving later sees the damage", D.welcome.street["17"] && D.welcome.street["18"].s === 3, D.welcome.street);
  A.send({ t: "st", ch: { "17": null } }); await B.wait(m => m.t === "st" && m.ch["17"] === null);
  const E = await join("d", "town:Asaba");
  ok("a repaired object is gone from the street state", !E.welcome.street["17"] && !!E.welcome.street["18"]);
  ok("the same player in a second window replaces the first", !!(await D.wait(m => m.t === "err" && m.code === "replaced")) && (await sleep(300), D.closed === 4002));

  // usage, for the Chief Admin only
  const ua = await fetch(`http://127.0.0.1:${PORT}/usage`, { headers: { Authorization: "Bearer " + await token(subOf("a")) } }), uj = await ua.json();
  ok("the Chief Admin gets today's figures", ua.status === 200 && uj.requests > 0 && uj.messagesIn > 0 && uj.requestLimit === 100000 && uj.projections.length === 3, uj);
  ok("the figures include 2, 5 and 10 players", uj.projections.map(p => p.players).join() === "2,5,10" && uj.projections[2].requests > uj.projections[0].requests, uj.projections);
  const ub = await fetch(`http://127.0.0.1:${PORT}/usage`, { headers: { Authorization: "Bearer " + await token(subOf("b")) } });
  ok("anyone else is refused", ub.status === 403);
  ok("without a login: refused", (await fetch(`http://127.0.0.1:${PORT}/usage`)).status === 401);

  // leaving
  B.got.length = 0; A.ws.close();
  ok("closing the game tells the others", !!(await B.wait(m => m.t === "leave" && m.id === A.id)));
  for (const P of [B, C, E]) try { P.ws.close() } catch (e) { }
  await stop(srv);

  // the daily limit: the server stops taking live play
  PORT = 8788; srv = await startServer({ STOP_AT: "8" });
  const L1 = await join("a", "town:Asaba"); for (let i = 0; i < 200; i++) L1.send({ t: "p", x: i, z: 0 }); await sleep(800);
  ok("at the daily limit, players are told and disconnected", L1.closed === 4029 || L1.got.some(m => m.code === "over-limit"), { closed: L1.closed });
  const L2 = player("late"); try { await L2.open } catch (e) { } await sleep(600); const refused = L2.closed === 4029 && L2.got.some(m => m.code === "over-limit" && m.until > Date.now())
  ok("and new connections are told why and closed, until 00:00 UTC", refused, L2.got);
} catch (e) { console.log("ERROR", e.stack || e); results.push(["no crash", false]) }
finally { if (srv) await stop(srv); supa.close() }
const bad = results.filter(r => !r[1]);
console.log(`\n${results.length - bad.length} of ${results.length} passed`); process.exit(bad.length ? 1 : 0);
