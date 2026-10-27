/* Delta City live server.

   One Worker in front of ONE Durable Object ("game") that holds every room: each town ("town:Asaba") and each inside
   ("gov:Asaba:uni", "hosp:Warri:3", "bank:Ozoro", "imm", "border"). One object instead of one per room keeps the
   running time far under the free plan's 13,000 GB-s a day. The object uses WebSocket Hibernation: between messages
   it sleeps and is not charged; what it must remember about each player lives on that player's socket (its
   "attachment"), and the street's damage and the day's usage live in its SQLite storage.

   Supabase stays in charge of logins, money, ownership and saving. A player signs in with Supabase, opens a WebSocket
   here and sends their Supabase login token first; the token is checked against the project's public signing keys
   (JWKS) before anything else is accepted. Nothing secret is needed for that.

   Messages are small JSON objects. From a player:
     {t:"hello", tok, room}                      first message: who I am and where
     {t:"p", x,z,y,a,m,sp, car?}                 where I am (about 2 a second while moving, none while still)
     {t:"room", room}                            I went into another room
     {t:"st", ch:{id: state|null}}               street objects I damaged (null: put right again)
     {t:"chat", text}
   To players:
     {t:"welcome", id, room, peers, street, usage}   {t:"roomok", room, peers, street}
     {t:"join", ...peer}  {t:"p", id, ...}  {t:"leave", id}  {t:"st", ch}  {t:"chat", id, name, text}  {t:"err", msg}

   Each player is sent only the players near them: inside a building, everyone in that room; in a town, players
   within 60 m at every update, players 60 to 250 m away at most once every 2 s, and nobody further away.

   The free plan allows 100,000 requests a day; incoming WebSocket messages count 20 to 1, outgoing ones are free.
   The object counts its own use; at STOP_AT it closes live play until 00:00 UTC and the game carries on
   single-player ("Offline mode"). GET /usage (Chief Admin only) returns today's figures and what 2, 5 and 10 players
   would use; with CF_ANALYTICS_TOKEN and CF_ACCOUNT_ID set it also asks Cloudflare for its own count. */
import { DurableObject } from "cloudflare:workers";

const NEAR = 60, FAR = 250, FAR_EVERY = 2000;          // metres, metres, ms
const MAX_MSG = 4096, MAX_CHAT = 200;
const ROOM_RE = /^[a-z]{3,8}(:[A-Za-z0-9_-]{1,20}){0,2}$/;
const GB = 0.128;                                       // a Durable Object is billed as 128 MB while awake

const cors = r => { const h = new Headers(r.headers); h.set("Access-Control-Allow-Origin", "*"); h.set("Access-Control-Allow-Headers", "authorization, content-type"); h.set("Access-Control-Allow-Methods", "GET, OPTIONS");
  return new Response(r.body, { status: r.status, headers: h }) };
const json = (o, status = 200) => cors(new Response(JSON.stringify(o), { status, headers: { "content-type": "application/json" } }));
const today = () => new Date().toISOString().slice(0, 10);
const nextMidnight = () => { const d = new Date(); d.setUTCHours(24, 0, 0, 0); return d.getTime() };

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === "OPTIONS") return cors(new Response(null, { status: 204 }));
    if (url.pathname === "/") return cors(new Response("Delta City live server: running\n", { headers: { "content-type": "text/plain" } }));
    if (url.pathname === "/ws" || url.pathname === "/usage") return env.LIVE.get(env.LIVE.idFromName("game")).fetch(req);
    return json({ error: "not found" }, 404);
  }
};

/* ---------------------------------------- logins ---------------------------------------- */
const b64u = s => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4)), c => c.charCodeAt(0));
const txt = s => new TextDecoder().decode(b64u(s));

export class Live extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`create table if not exists usage(day text primary key, msgs integer default 0, conns integer default 0, http integer default 0,
      active_ms integer default 0, player_ms integer default 0, peak integer default 0)`);
    this.sql.exec(`create table if not exists street(room text, id text, v text, at integer, primary key(room, id))`);
    ctx.setWebSocketAutoResponse(new WebSocketRequestResponsePair("ping", "pong"));       // keep-alives: answered without waking the object
    this.jwks = null; this.jwksAt = 0; this.lastAt = Date.now(); this.dirty = 0;
    this.loadUsage();
  }

  /* ---- the day's usage: kept in memory, written to SQLite every 50 messages and when someone leaves ---- */
  loadUsage() {
    const d = today(), r = this.sql.exec("select * from usage where day = ?", d).toArray()[0];
    this.u = r ? { day: d, msgs: r.msgs, conns: r.conns, http: r.http, active_ms: r.active_ms, player_ms: r.player_ms, peak: r.peak } : { day: d, msgs: 0, conns: 0, http: 0, active_ms: 0, player_ms: 0, peak: 0 };
  }
  saveUsage() {
    const u = this.u; this.dirty = 0;
    this.sql.exec(`insert into usage(day, msgs, conns, http, active_ms, player_ms, peak) values (?, ?, ?, ?, ?, ?, ?)
      on conflict(day) do update set msgs = excluded.msgs, conns = excluded.conns, http = excluded.http, active_ms = excluded.active_ms, player_ms = excluded.player_ms, peak = excluded.peak`,
      u.day, u.msgs, u.conns, u.http, u.active_ms, u.player_ms, u.peak);
    this.sql.exec("delete from usage where day < ?", new Date(Date.now() - 40 * 864e5).toISOString().slice(0, 10));
  }
  tick(kind) {                                            // one incoming request or message
    if (this.u.day !== today()) { this.saveUsage(); this.loadUsage() }
    const now = Date.now(); this.u.active_ms += Math.min(now - this.lastAt, 10000); this.lastAt = now;
    this.u[kind]++; if (++this.dirty >= 50) this.saveUsage();
  }
  requests() { const u = this.u; return u.conns + u.http + Math.ceil(u.msgs / 20) }
  over() { if (this.u.day !== today()) { this.saveUsage(); this.loadUsage() } return this.requests() >= +(this.env.STOP_AT || 95000) }

  async verify(tok) {
    const p = String(tok || "").split("."); if (p.length !== 3) throw new Error("not a login token");
    const head = JSON.parse(txt(p[0])), body = JSON.parse(txt(p[1])), data = new TextEncoder().encode(p[0] + "." + p[1]), sig = b64u(p[2]);
    let ok = false;
    if (head.alg === "HS256") {
      if (!this.env.SUPABASE_JWT_SECRET) throw new Error("this Supabase project still signs logins with its legacy secret; switch it to JWT signing keys (server/README.md, step 5)");
      const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(this.env.SUPABASE_JWT_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
      ok = await crypto.subtle.verify("HMAC", k, sig, data);
    } else {
      const find = () => this.jwks && this.jwks.find(k => k.kid === head.kid);
      if (!find() && Date.now() - this.jwksAt > 60000) {
        const r = await fetch(this.env.SUPABASE_URL + "/auth/v1/.well-known/jwks.json"); this.jwksAt = Date.now();
        if (r.ok) this.jwks = (await r.json()).keys || [];
      }
      const jwk = find(); if (!jwk) throw new Error("unknown signing key");
      const alg = head.alg === "ES256" ? { name: "ECDSA", namedCurve: "P-256", hash: "SHA-256" } : head.alg === "RS256" ? { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" } : null;
      if (!alg) throw new Error("unsupported token type " + head.alg);
      const k = await crypto.subtle.importKey("jwk", jwk, alg, false, ["verify"]);
      ok = await crypto.subtle.verify(alg, k, sig, data);
    }
    if (!ok) throw new Error("the login token's signature is wrong");
    if (!body.sub || body.role !== "authenticated") throw new Error("not a signed-in player");
    if (!(body.exp * 1000 > Date.now() - 60000)) throw new Error("the login has expired");
    return body.sub;
  }
  async citizen(tok, uid) {                               // the player's own character, read with their own login
    try {
      const r = await fetch(`${this.env.SUPABASE_URL}/rest/v1/characters?select=name,gender,look,role,home_state&owner=eq.${uid}`,
        { headers: { apikey: this.env.SUPABASE_KEY, Authorization: "Bearer " + tok } });
      const rows = r.ok ? await r.json() : []; return rows && rows[0] || null;
    } catch (e) { return null }
  }

  /* ---------------------------------------- requests ---------------------------------------- */
  async fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/usage") return this.usage(req);
    if (req.headers.get("Upgrade") !== "websocket") return json({ error: "expected a WebSocket" }, 426);
    if (this.over()) return json({ error: "over-limit", until: nextMidnight() }, 429);
    this.tick("conns");
    const [client, server] = Object.values(new WebSocketPair());
    this.ctx.acceptWebSocket(server);
    server.serializeAttachment({ id: crypto.randomUUID().slice(0, 8), auth: false, t0: Date.now() });
    return new Response(null, { status: 101, webSocket: client });
  }

  socks() { return this.ctx.getWebSockets().map(ws => ({ ws, a: ws.deserializeAttachment() || {} })) }
  send(ws, o) { try { ws.send(JSON.stringify(o)) } catch (e) { } }
  peer(a) { return { id: a.id, name: a.name, g: a.g, look: a.look, x: a.x, z: a.z, y: a.y, a: a.a, m: a.m, sp: a.sp, car: a.car || null } }
  roomPeers(room, except) { return this.socks().filter(s => s.a.auth && s.a.room === room && s.a.id !== except).map(s => this.peer(s.a)) }
  street(room) {
    if (!room.startsWith("town:")) return {};
    const old = Date.now() - 2 * 3600e3; this.sql.exec("delete from street where at < ?", old);
    const o = {}; for (const r of this.sql.exec("select id, v from street where room = ?", room).toArray()) o[r.id] = JSON.parse(r.v); return o;
  }
  toRoom(room, o, except) { const s = JSON.stringify(o); for (const { ws, a } of this.socks()) if (a.auth && a.room === room && a.id !== except) try { ws.send(s) } catch (e) { } }

  async webSocketMessage(ws, msg) {
    this.tick("msgs");
    if (this.over()) { this.send(ws, { t: "err", code: "over-limit", until: nextMidnight() }); ws.close(4029, "daily limit reached"); return }
    if (typeof msg !== "string" || msg.length > MAX_MSG) return;
    let m; try { m = JSON.parse(msg) } catch (e) { return }
    const a = ws.deserializeAttachment() || {}, now = Date.now();
    if (!a.auth) {
      if (m.t !== "hello") return ws.close(4001, "say hello first");
      let uid; try { uid = await this.verify(m.tok) } catch (e) { this.send(ws, { t: "err", code: "login", msg: e.message }); return ws.close(4001, "login refused") }
      // one connection per player: an older one (another tab) is closed
      for (const s of this.socks()) if (s.a.uid === uid && s.ws !== ws) { this.send(s.ws, { t: "err", code: "replaced", msg: "You are playing in another window." }); try { s.ws.close(4002, "replaced") } catch (e) { } }
      const c = await this.citizen(m.tok, uid);
      const room = ROOM_RE.test(m.room || "") ? m.room : "border";
      Object.assign(a, { auth: true, uid, name: (c && c.name) || "New arrival", g: (c && c.gender) || "Female", look: (c && c.look) || "", role: (c && c.role) || "newcomer", room, x: 0, z: 0, y: 0, a: 0, m: "s", sp: 0, car: null, farAt: 0, lastP: 0, lastChat: 0 });
      ws.serializeAttachment(a);
      const live = this.socks().filter(s => s.a.auth).length; if (live > this.u.peak) this.u.peak = live;
      this.send(ws, { t: "welcome", id: a.id, room, peers: this.roomPeers(room, a.id), street: this.street(room), usage: { requests: this.requests(), limit: +(this.env.DAILY_REQUEST_LIMIT || 100000) } });
      this.toRoom(room, Object.assign({ t: "join" }, this.peer(a)), a.id);
      return;
    }
    if (m.t === "p") {
      if (now - a.lastP < 200) return;                    // at most 5 a second are relayed, whatever a client sends
      a.lastP = now;
      for (const k of ["x", "z", "y", "a", "sp"]) if (typeof m[k] === "number" && isFinite(m[k])) a[k] = Math.round(m[k] * 100) / 100;
      if (typeof m.m === "string") a.m = m.m.slice(0, 2);
      a.car = m.car && typeof m.car === "object" ? { x: +m.car.x || 0, z: +m.car.z || 0, a: +m.car.a || 0, v: +m.car.v || 0, st: +m.car.st || 0, dr: (m.car.dr | 0) & 255, l: (m.car.l | 0) & 3, d: m.car.d ? 1 : 0 } : null;
      const far = now - a.farAt >= FAR_EVERY; let sentFar = false;
      const out = JSON.stringify(Object.assign({ t: "p" }, this.peer(a))), town = a.room.startsWith("town:");
      for (const s of this.socks()) {
        if (!s.a.auth || s.a.room !== a.room || s.a.id === a.id) continue;
        const d = town ? Math.hypot((s.a.x || 0) - a.x, (s.a.z || 0) - a.z) : 0;
        if (d <= NEAR || (d <= FAR && far)) { try { s.ws.send(out) } catch (e) { } if (d > NEAR) sentFar = true }
      }
      if (sentFar) a.farAt = now;
      ws.serializeAttachment(a); return;
    }
    if (m.t === "room") {
      if (!ROOM_RE.test(m.room || "") || m.room === a.room) return;
      this.toRoom(a.room, { t: "leave", id: a.id }, a.id);
      a.room = m.room; a.car = null; if (typeof m.x === "number") { a.x = m.x; a.z = m.z }
      ws.serializeAttachment(a);
      this.send(ws, { t: "roomok", room: a.room, peers: this.roomPeers(a.room, a.id), street: this.street(a.room) });
      this.toRoom(a.room, Object.assign({ t: "join" }, this.peer(a)), a.id); return;
    }
    if (m.t === "st") {
      if (!a.room.startsWith("town:") || !m.ch || typeof m.ch !== "object") return;
      const ch = {}; let n = 0;
      for (const [id, v] of Object.entries(m.ch)) {
        if (++n > 24 || !/^\d{1,6}$/.test(id)) break;
        const s = v === null ? null : JSON.stringify(v); if (s && s.length > 2000) continue;
        if (s === null) this.sql.exec("delete from street where room = ? and id = ?", a.room, id);
        else this.sql.exec("insert into street(room, id, v, at) values (?, ?, ?, ?) on conflict(room, id) do update set v = excluded.v, at = excluded.at", a.room, id, s, now);
        ch[id] = v;
      }
      this.toRoom(a.room, { t: "st", ch, by: a.id }, a.id); return;
    }
    if (m.t === "chat") {
      const text = String(m.text || "").replace(/[\u0000-\u001f\u007f]/g, " ").trim().slice(0, MAX_CHAT);
      if (!text || now - a.lastChat < 1000) return;
      a.lastChat = now; ws.serializeAttachment(a);
      const o = { t: "chat", id: a.id, name: a.name, text, at: now };
      this.toRoom(a.room, o, null); return;                // everyone in the room, the sender too (their own line comes back)
    }
  }
  bye(ws) {
    const a = ws.deserializeAttachment() || {};
    this.u.player_ms += Date.now() - (a.t0 || Date.now()); this.saveUsage();
    if (a.auth) this.toRoom(a.room, { t: "leave", id: a.id }, a.id);
  }
  async webSocketClose(ws, code) { this.bye(ws); try { ws.close(code === 1005 ? 1000 : code, "bye") } catch (e) { } }
  async webSocketError(ws) { this.bye(ws) }

  /* ---------------------------------------- the Chief Admin's usage figures ---------------------------------------- */
  async usage(req) {
    this.tick("http");
    const tok = (req.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
    let uid; try { uid = await this.verify(tok) } catch (e) { return json({ error: e.message }, 401) }
    const c = await this.citizen(tok, uid); if (!c || c.role !== "admin") return json({ error: "Only the Chief Admin can see this." }, 403);
    this.saveUsage();
    const u = this.u, now = Date.now(), live = this.socks().filter(s => s.a.auth);
    const playerMs = u.player_ms + live.reduce((t, s) => t + (now - (s.a.t0 || now)), 0), hours = playerMs / 3600e3;
    const reqs = this.requests(), gbs = u.active_ms / 1000 * GB;
    // what one player uses in an hour: measured today once there is enough play, otherwise the design figure
    // (moving half the time at 2 updates a second: 3,600 messages, so 180 requests, plus a few connections)
    const perHour = hours >= .25 ? Math.max(1, (reqs - u.http) / hours) : 185, playHours = 2;
    const projections = [2, 5, 10].map(n => ({ players: n, hoursEach: playHours, requests: Math.round(n * playHours * perHour),
      gbs: Math.round(Math.min(24, n * playHours) * 3600 * GB) }));
    let cloudflare = null;
    if (this.env.CF_ANALYTICS_TOKEN && this.env.CF_ACCOUNT_ID) cloudflare = await this.cfAnalytics().catch(e => ({ error: String(e.message || e) }));
    return json({ day: u.day, resetsAt: nextMidnight(), requests: reqs, requestLimit: +(this.env.DAILY_REQUEST_LIMIT || 100000), stopAt: +(this.env.STOP_AT || 95000),
      messagesIn: u.msgs, connections: u.conns, gbs: Math.round(gbs * 10) / 10, gbsLimit: +(this.env.DAILY_GBS_LIMIT || 13000),
      playersNow: live.length, peakToday: u.peak, playerHoursToday: Math.round(hours * 100) / 100, requestsPerPlayerHour: Math.round(perHour), projections, cloudflare });
  }
  async cfAnalytics() {
    const d = today(), q = `query($a:String!,$d:Date!){viewer{accounts(filter:{accountTag:$a}){
      workers:workersInvocationsAdaptive(limit:50,filter:{date:$d}){sum{requests} dimensions{scriptName}}
      objects:durableObjectsInvocationsAdaptiveGroups(limit:50,filter:{date:$d}){sum{requests}}
      periodic:durableObjectsPeriodicGroups(limit:50,filter:{date:$d}){sum{activeTime inboundWebsocketMsgCount}}}}}`;
    const r = await fetch("https://api.cloudflare.com/client/v4/graphql", { method: "POST", headers: { "content-type": "application/json", Authorization: "Bearer " + this.env.CF_ANALYTICS_TOKEN },
      body: JSON.stringify({ query: q, variables: { a: this.env.CF_ACCOUNT_ID, d } }) });
    const j = await r.json(); if (j.errors && j.errors.length) return { error: j.errors.map(e => e.message).join("; ") };
    const acc = j.data && j.data.viewer && j.data.viewer.accounts && j.data.viewer.accounts[0]; if (!acc) return { error: "no data for this account" };
    const sum = (L, k) => (L || []).reduce((t, x) => t + ((x.sum && x.sum[k]) || 0), 0);
    const active = sum(acc.periodic, "activeTime");               // microseconds the objects were awake
    return { workerRequests: sum((acc.workers || []).filter(x => !x.dimensions || x.dimensions.scriptName === "delta-city-live"), "requests"),
      objectRequests: sum(acc.objects, "requests"), wsMessagesIn: sum(acc.periodic, "inboundWebsocketMsgCount"), gbs: Math.round(active / 1e6 * GB * 10) / 10 };
  }
}
