// Rolling three-vehicle roster — pure logic tests (VEHROSTER, the same code the browser loads from assets/vehroster.js).
// Covers the exact spawn table from the spec, middle-vehicle manual storage, occupied-vehicle safety,
// failed auto-store leaving state unchanged, and no duplicates after retrieve.
import test from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const V = require("../assets/vehroster.js");
const ids = (r) => r.list.map((e) => e.vid);

test("CAP is three", () => {
  assert.equal(V.CAP, 3);
});

test("spec table: spawn 1..6 rolls the oldest out each time", () => {
  let r;
  r = V.onSpawn([], 1);           assert.deepEqual(ids(r), [1], "spawn 1 -> [1]");
  r = V.onSpawn(r.list, 2);       assert.deepEqual(ids(r), [1, 2], "spawn 2 -> [1,2]");
  r = V.onSpawn(r.list, 3);       assert.deepEqual(ids(r), [1, 2, 3], "spawn 3 -> [1,2,3]");
  r = V.onSpawn(r.list, 4);       assert.deepEqual(ids(r), [2, 3, 4], "spawn 4 -> [2,3,4]");
  assert.deepEqual(r.stowed.map((s) => s.vid), [1], "oldest (1) stored, not 2 or 3");
  r = V.onSpawn(r.list, 5);       assert.deepEqual(ids(r), [3, 4, 5], "spawn 5 -> [3,4,5]");
  assert.deepEqual(r.stowed.map((s) => s.vid), [2], "oldest (2) stored");
  r = V.onSpawn(r.list, 6);       assert.deepEqual(ids(r), [4, 5, 6], "spawn 6 -> [4,5,6]");
  assert.deepEqual(r.stowed.map((s) => s.vid), [3], "oldest (3) stored");
});

test("age is spawn order, never vehicle id or focus", () => {
  // ids deliberately out of numeric order and larger ids spawned first
  let r = V.onSpawn([], 900);
  r = V.onSpawn(r.list, 10);
  r = V.onSpawn(r.list, 500);
  assert.deepEqual(ids(r), [900, 10, 500]);
  r = V.onSpawn(r.list, 7);
  assert.deepEqual(ids(r), [10, 500, 7], "oldest 900 stored although 10/500 are 'smaller ids'");
  assert.deepEqual(r.stowed.map((s) => s.vid), [900]);
});

test("manual store affects ONLY the selected (middle) vehicle", () => {
  let r = V.onSpawn([], 1); r = V.onSpawn(r.list, 2); r = V.onSpawn(r.list, 3);
  r = V.onStore(r.list, 2);
  assert.deepEqual(ids(r), [1, 3], "only vehicle 2 removed");
  assert.deepEqual(r.stowed.map((s) => s.vid), [2]);
  // refilling after a manual store still rolls the oldest of the rest
  r = V.onSpawn(r.list, 4);
  assert.deepEqual(ids(r), [1, 3, 4]);
  r = V.onSpawn(r.list, 5);
  assert.deepEqual(ids(r), [3, 4, 5], "after middle-store, next roll evicts 1 (oldest remaining)");
});

test("occupied (driven) vehicle is never auto-stored; the spawn fails and state is unchanged", () => {
  let r = V.onSpawn([], 1, { occupied: true }); // player is driving car 1
  r = V.onSpawn(r.list, 2); r = V.onSpawn(r.list, 3);
  assert.deepEqual(ids(r), [1, 2, 3]);
  const before = ids(r);
  r = V.onSpawn(r.list, 4);
  assert.ok(r.error, "spawn 4 is refused while 1 is being driven");
  assert.deepEqual(ids(r), before, "state unchanged after refused auto-store");
  assert.deepEqual(r.stowed, [], "nothing was stowed");
  // once 1 is released, the same spawn goes through and rolls 1 out
  const free = V.onSpawn(V.onStore(before, 1).list, 2); // recover a clean state, then
  let r2 = V.onSpawn([], 1); r2 = V.onSpawn(r2.list, 2); r2 = V.onSpawn(r2.list, 3);
  r2 = V.onSpawn(r2.list, 4);
  assert.deepEqual(ids(r2), [2, 3, 4], "after 1 is stored, spawn 4 rolls 1 out");
});

test("occupied vehicle can be stored MANUALLY (player puts their own car away)", () => {
  let r = V.onSpawn([], 1, { occupied: true }); r = V.onSpawn(r.list, 2); r = V.onSpawn(r.list, 3);
  r = V.onStore(r.list, 1); // manual store of the driven car is the player's own action
  assert.deepEqual(ids(r), [2, 3]);
});

test("re-spawning an already-out vehicle moves it to newest, no duplicate", () => {
  let r = V.onSpawn([], 1); r = V.onSpawn(r.list, 2); r = V.onSpawn(r.list, 3);
  r = V.onSpawn(r.list, 2); // car 2 moves to another park
  assert.deepEqual(ids(r), [1, 3, 2], "no duplicate of 2; 2 is now newest");
  assert.deepEqual(r.stowed, [], "nothing stored on a pure move");
  r = V.onSpawn(r.list, 4);
  assert.deepEqual(ids(r), [3, 2, 4], "next roll evicts 1 (oldest), not 2");
  assert.deepEqual(new Set(ids(r)).size, 3, "no duplicates");
});

test("retrieving a stored vehicle into a full roster rolls the oldest once, no duplicates ever", () => {
  let r = V.onSpawn([], 1); r = V.onSpawn(r.list, 2); r = V.onSpawn(r.list, 3);
  r = V.onStore(r.list, 1);                       // store 1 by hand -> [2,3]
  r = V.onSpawn(r.list, 1);                        // retrieve it
  assert.deepEqual(ids(r), [2, 3, 1]);
  r = V.onSpawn(r.list, 1);                        // duplicate retrieve (double tap)
  assert.deepEqual(ids(r), [2, 3, 1], "second retrieve is a no-op move, still no duplicate");
  assert.deepEqual(r.stowed, []);
});

test("input list is never mutated", () => {
  const input = [{ vid: 1 }, { vid: 2 }, { vid: 3 }];
  const snap = JSON.stringify(input);
  V.onSpawn(input, 4);
  assert.equal(JSON.stringify(input), snap, "caller's list untouched");
});