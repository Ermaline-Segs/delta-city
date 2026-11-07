/* ---- the rolling three-vehicle roster: the same pure logic the game (index.html) and the server (veh_spawn in
   supabase_vehicles.sql, mirrored in migrations/garage_v2_rolling_three.sql) follow. Only three of a citizen's
   vehicles can be out in the world at once; when a fourth is spawned, the OLDEST by spawn order goes back to
   its bay automatically. A vehicle that is being driven (occupied) is never stored or removed. Loaded in the
   browser as a classic script (sets globalThis.VEHROSTER) and imported by test/rolling-three-cars.test.mjs. */
(function (G) {
  "use strict";
  const CAP = 3;
  const clone = (l) => l.map((e) => ({ vid: e.vid, occupied: !!e.occupied }));
  function onSpawn(list, vid, opts) {
    opts = opts || {};
    const l = clone(list);
    const i = l.findIndex((e) => e.vid === vid);
    if (i >= 0) {                       // already out: it just moved here, so keep it newest
      const e = l.splice(i, 1)[0];
      e.occupied = !!opts.occupied;
      l.push(e);
      return { list: l, stowed: [] };
    }
    if (l.length >= CAP) {              // the roster is full: the OLDEST car (front of the list) goes back —
      if (l[0].occupied)                 // never one that is being driven, and never a newer one in its place
        return { error: "your other car cannot be put away right now: someone is driving it. Store it first.", list: l, stowed: [] };
      const [st] = l.splice(0, 1);
      l.push({ vid: vid, occupied: !!opts.occupied });
      return { list: l, stowed: [{ vid: st.vid }] };
    }
    l.push({ vid: vid, occupied: !!opts.occupied });
    return { list: l, stowed: [] };
  }
  function onStore(list, vid) {         // manual store: exactly the named vehicle, never any other
    const l = clone(list);
    const i = l.findIndex((e) => e.vid === vid);
    if (i < 0) return { list: l, stowed: [] };
    const [st] = l.splice(i, 1);
    return { list: l, stowed: [{ vid: st.vid }] };
  }
  const api = { CAP: CAP, onSpawn: onSpawn, onStore: onStore };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  G.VEHROSTER = api;
})(typeof globalThis !== "undefined" ? globalThis : this);