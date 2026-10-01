# EXP-231 — detach siblings `308270`/`319140`/`319420` real (+ copy/scan leaves)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `f9fac9da` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..230; no new cases — the `b9420`/`b9140`/`b8270`
scripted sinks now execute the shipped bodies; asserts retargeted to
real tags + new state pins)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

The three sibling teardown routines the detach chain (`300FC0` /
`310780` / `3105D0`) calls once per released object — `bc970`'s
callers, now all real; the whole object-teardown subtree is shipped
bytes except the boundaries listed below.

| body | semantics | hits |
|------|-----------|------|
| `00319420` (`l319420`) | `(obj+0x6B0)` — `d[+0xC4]` (= `d[obj+0x774]`) ∉{0,-1} → `2EAEA0(id,1)` (thunk → real `24FE30` id dispatch); then `d[+0xC4]=-1`. Under all fixtures `d[obj+0x774]`=0 → the dispatch arm is empty-operand (`l2eaea0`/`l4fe30` ×0, disclosed). The `d[obj+0x774]=0xFFFFFFFF` write is pinned on `u0fc0-def`. | ×34 |
| `00319140` (`l319140`) | `(obj, edx)` flag pair: `edx&1` → `290B90(d[obj+8])` entity-list flag set — **scripted `s290b90`** (×34 recorded): it derefs `q[0x209BE80]`→`q[+0x10F10]` unconditionally and the shipped cell is BSS-null with no live-list fixture. `edx&2` → `3BBC80(q[obj+0x10])` 64-entry `0x50`-stride ring clear on `q[0x2B457D0]` — real, null-safe early-out (`l3bbc80` ×0 — every call is `edx=1`, empty-operand). | ×34 |
| `00308270` (`l308270`) | `(obj)` — `bt q[obj],0x16` gate: `d[+0x28]`=0 → `30C970(b[obj+0x695])` (real row reset) → `b[+0x695]`=0xFF → `w[obj+0xDC8]`=`w[0x22C1DB0+idx*12]`, `d[obj+0xE58]`=`d[0x22C1DB0+idx*12+4]` (`idx=b[obj+0xEA9]`=0 → row 0, zeroed) → `30EDA0(obj)` → `q[obj] &= 0xFFFFBFFFFFFFBFFFFF` (clears bits 46,22) → `d[obj+0x690]`=0. **Body executed once** — `u0fc0-def` is the only case whose `q[obj]` still has bit22 set when `308270` reads it (`l30eda0` ×1 proves the snapshot copy); the other 33 entries execute the `bt` gate and early-ret (empty-operand). | ×34 |
| `0030EDA0` (`l30eda0`) | 0x480-byte `movups` snapshot copy `q[obj+0xB88]` → `obj+0x730..0xBAF` (9×0x80). Null `q[obj+0xB88]` faults at `0x30EDBD` — the `objb88` fixture plants it. | ×1 |
| `002EAEA0` (`l2eaea0`) | thunk `jmp 24FE30` — real dispatch target; ×0 (gated arm). | ×0 |
| `003BBC80` (`l3bbc80`) | 64-entry ring clear: `q[0x2B457D0]` null → ret; else scans matching `q[e]`/`q[e+8]` pairs and zeroes them. | ×0 |

## Corrections of record

- **`u0fc0-def` `q[obj]`/`d[obj+4]` masks** — `0xFFFFFFF9EFE7FFDD` →
  `0xFFFFBFF9EFA7FFDD`, `0xFFFFFFF9` → `0xFFFFBFF9`: real `308270`'s
  `&=0xFFFFBFFFFFFFBFFFFF` (clears bits 46 and 22; bit46 lives in the
  `d[+4]` high dword) lands — the stub hid the mask.
- **`u0fc0-def` `l30c970` count 1→2** — real `308270` calls
  `30C970(b[obj+0x695]`=0`)` (row-0 reset) before the existing
  `+0x694`/cl=`0x27` no-op call. Both args pinned.
- Assert-site correction: scripted sinks record under `calls`
  (`by()`), not `trace` — `s290b90` is pinned via `by()` (the
  `v3dc780`/`v42fcc0`/`v306570` ×0 checks in EXP-230's `a630r9-swap`
  used `tcount`; harmless for an absence check but the convention is
  now consistent).

## New fixture

`q[obj+0xB88]` → `objb88` (0x600) planted under `objlink` — the
snapshot buffer `30EDA0` copies from; null faults at `0x30EDBD`.
Follows the EXP-227 `+0x1E0`/`+0x1E8` pattern (a linked object carries
its buffers).

## Boundaries (unchanged disclosures)

`00290B90` → `s290b90` (×34 — recorded; real body would fault on the
shipped-null `q[0x209BE80]` head deref; promote when a fixture builds
the entity list). `30E130` (`e130`, ×0), `317E50` (`b7e50`, ×0),
`8632B0` (`b32b0` ×55), `2EB0D0` (`kb0d0` ×26), `319490`, `2E42D0`,
`46AB10`, `426130`/`427320` remain scripted. `live_game: false`.

## Regression triage

541/542 first run → **542/542**. Single-case triage (`u0fc0-def`),
four findings, all shipped-cause: the two `q[obj]` mask corrections,
the +1 `l30c970`, and the `by()`/`tcount` accessor fix. No assertion
weakened; the `0x27` no-op pin survives verbatim on the real tag.
