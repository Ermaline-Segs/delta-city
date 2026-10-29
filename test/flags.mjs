// Client multiplayer flag guard for index.html. Run from the repo root: node test/flags.mjs
//
// The per-feature flags live on one line in index.html. This test pins their
// shipped defaults and makes sure no bare NET_EXTRAS token survives, so a
// future edit cannot accidentally flip a live feature on or off.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const html = readFileSync(join(root, "index.html"), "utf8");
const results = [];
const ok = (name, cond, info) => { results.push([name, !!cond]); console.log((cond ? "PASS " : "FAIL ") + name + (info !== undefined ? "  " + JSON.stringify(info).slice(0, 200) : "")) };

// the one line that declares all four flags
const m = html.match(/const NET_EXTRAS_CARS=(true|false),NET_EXTRAS_STREET=(true|false),NET_EXTRAS_INDOORS=(true|false),NET_EXTRAS_CHAT=(true|false);/);
ok("the four per-feature flags are declared on one line", !!m);

// expected shipped defaults: cars on, street and chat off, indoors on
// (indoors was already live and ungated in v1, so this flag only adds control)
if (m) {
  ok("NET_EXTRAS_CARS ships on", m[1] === "true", m[1]);
  ok("NET_EXTRAS_STREET ships off", m[2] === "false", m[2]);
  ok("NET_EXTRAS_INDOORS ships on", m[3] === "true", m[3]);
  ok("NET_EXTRAS_CHAT ships off", m[4] === "false", m[4]);
}

// no bare NET_EXTRAS left: every use must be one of the four per-feature flags
const bare = html.match(/NET_EXTRAS(?![A-Z_])/g);
ok("no bare NET_EXTRAS token remains", !bare, bare && bare.length);

// each flag is actually wired: referenced somewhere besides its declaration
for (const f of ["NET_EXTRAS_CARS", "NET_EXTRAS_STREET", "NET_EXTRAS_INDOORS", "NET_EXTRAS_CHAT"]) {
  const uses = html.split(f).length - 1;
  ok(`${f} is referenced more than once`, uses >= 2, uses);
}

const failed = results.filter(([, c]) => !c).length;
console.log(failed === 0 ? `ALL ${results.length} FLAG CHECKS PASS` : `${failed} of ${results.length} FLAG CHECKS FAILED`);
process.exit(failed === 0 ? 0 : 1);