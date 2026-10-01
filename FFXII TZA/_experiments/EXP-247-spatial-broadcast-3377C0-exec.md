# EXP-247 — spatial broadcast `3377C0` real (guard path)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `2d95f2de` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; no new fixture — the path runs on the
existing `ctx4`/`n30` plants; none claim initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..246; asserts retargeted, none weakened — two
asserts *corrected* to the shipped-honest outcome).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

- **`003377C0`** (`l377c0`, ×19 — `v3377c0` bespoke handler removed)
  — the spatial broadcast `319490` tails into from `0x31950C`
  (sole harness-reached caller; the other four call sites at
  `0x334E65`/`0x335093`/`0x339935`/`0x33BE55` are unreached).
  Guards: `rcx==0` or `q[rcx+0x10]==0` → `xor eax,eax` → ret 0.

## Path taken — disclosed

All 19 calls take the **guard early-out**: 17 callers pass `rcx=0`
(`263E30` owner resolve inside real `319490` found nothing), and
`d228-pos`/`d228-pos2` pass `rcx = ctxn30` — the planted `n30`
ctx node — whose `q[+0x10]` link is unplanted (zeroed) → same
early-out, ret 0.

This is the shipped-honest result for the fixture state. The
removed stub returned the synthetic `s9490_ret=1` on pos/pos2,
which drove the downstream `3180F0`/`319CA0` arms — papering over
an incomplete `ctxn30` (no `+0x10`-linked entity). With the real
body, `312280`'s `test eax,eax; je` skips `s80f0`/`s9ca0` — the
asserts were corrected to `×0`, not weakened: the boundary calls
genuinely cannot fire while `q[ctxn30+0x10]==0`.

## Assert retargets

- `by("v3377c0")` → `byr("l377c0")` on `d228-pos`/`d228-pos2`;
  `vv[0][1]==w.ctxn30` arg pin retained (REAL records rcx).
- vec4-w pin: the removed handler snapshotted the caller's
  marshalled `&vec4`; the real body doesn't expose it, so the pin
  now reads the caller's stack frame directly —
  `gm.d(byr("l377c0")[0][2] + 0xC) == 0x3F800000` (rdx = `&vec4`,
  the shipped `1.0f` literal written by `319490` at `0x3194F8`).
- `s80f0`/`s9ca0` on pos/pos2: `×0` (was `×1`/`×0` under the
  synthetic ret) — boundaries remain declared for the future
  deep-path fixture.
- Dead keys `s9490_ret`/`s80f0_ret` left in the case dicts (inert).

## Deep arms — mapped, not exercised

`q[rcx+0x10]` nonzero enters: `265090(&pos,&r, q[rcx+0x10])` →
`236820(b[r14+0xEA9])` → `d[e+8]` → `31ABE0` → `2EA7F0` gate →
zero-vec `391D10` / nonzero-vec `3920F0` spatial query → per-entity
loop (`263E30` → `q[rax+0xE68]`/`b[+0x18]>>1&7` kind checks,
`314EB0(rbp)` gate, `313F80(rbp,ent,&out)` scoring) → ret 2 when
any entity passes (`edi>0`), ret 0 on reject (`esi>0`), or the
`337700(r14,r15)` fallback tail when the result set is empty.
Surfacing this needs an entity-list fixture: `q[ctxn30+0x10]`
linked object, `n30` widened past `+0xEA9`, planted
`d[0x208E6A0]`/`q[0x208E688]` entity pool, and the query containers
behind `391D10`/`3920F0` — all currently unlisted/silent-real and
unprobed.

## Not claimed

- The `265090..313F80` deep arms — ×0, need the entity-list fixture.
- `3180F0`/`319CA0` remain scripted boundaries (`s80f0` ×0,
  `s9ca0` ×0) — the `q[0x23BF0C0]` desc + formation work from the
  earlier triage still stands.
- Live-game reachability — `NATIVE-REPLAY`, `live_game: false`.
- `e130`/`30E130` still ×0.
