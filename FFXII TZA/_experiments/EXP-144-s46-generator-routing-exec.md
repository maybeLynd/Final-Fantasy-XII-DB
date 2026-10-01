---
experiment: EXP-144
title: S-46 generator routing executed — one representative consumer
  per claimed route, all four generator states planted
  distinguishably, every case snapshots which state advances or is
  read; both LCG census populations (inliner + call-site) executed
contract: 21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md
requests:
  - FABLE-REQ-ORACLE-S46-WHICH-GENERATOR-EACH-CONSUMER-ACTUALLY-ADVANCES
method: B
live_game: false
tool: evidence/s46-generator-routing/check.py
---
# EXP-144 — s46-generator-routing

**Status:** complete · **9 cases, zero failures, stable ×3**
**Evidence:** `evidence/s46-generator-routing/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

The contract's runtime cell was UNLINKED — the routing (which
consumer draws from which generator) had never been executed.
For each claimed route, run one representative consumer on
shipped bytes with **all four generator states planted
distinguishably**, and record which state advances or is read —
including the I6 claim that a formula roll leaves the LCG
unmoved while an AI-decision roll steps it.

## States planted per case

| generator | state | planted value |
|---|---|---|
| gameplay MT | `02EB3870`+idx `02EB4230` | real seeder `00863D30(0xACE1)` — native init, index 624 |
| shared LCG | `022C256C` | `0x11111111` |
| presentation PRNG | `01EF93E8` | `0x22222222` |
| graphics MT | `01F7F600` | pattern `0x33333333+i`; cursor `q[01F7FFC0]`, count `d[01F7FFC8]` |

## Executed routing table

| case | consumer | route claim | observed delta | verdict |
|---|---|---|---|---|
| `lcg-loot-inliner` | `003185D0` `Loot_RollNormalSlotChance` | LCG inliner | `022C256C: 0x11111111 → 0x15EAB4E4`; nothing else | **LCG** |
| `lcg-yaw` | `00239210` random-yaw | LCG call-site | same `→ 0x15EAB4E4`; nothing else | **LCG** |
| `mt-weather-2` | `0025ABA0(2)` | MT, `current==2` arm | `mt_idx 624→1`, full twist; nothing else | **MT** |
| `mt-weather-1` | `0025ABA0(1)` | deterministic arm | **zero delta, zero accesses** | no draw |
| `mt-roll-20000` | `0038DB10` | MT (combat-roll module) | `mt_idx 624→1`, twist; nothing else | **MT** |
| `mt-roll-100` | `00389670` | MT percent-gate | same MT draw; nothing else | **MT** |
| `prng-render` | `004005E0` | presentation PRNG | `01EF93E8: 0x22222222 → 0x3FC44444`; nothing else | **PRNG** |
| `gfxmt-seed` | `0015BCF0` | graphics MT | gfx state rewritten at `01F7F600`; gameplay MT untouched | **gfx MT** |
| `gfxmt-draw` | `0018D740(01F7F600, 0x5555AAAA)` | graphics MT | `state[0]=0x5555AAAA` + twist-fill; nothing else | **gfx MT** |

## Findings

- **I3 executed — both census populations advance ONE stream.**
  The inliner `003185D0` and the call-site consumer `00239210`
  (via `enter328370`) each advance `022C256C` through exactly the
  same three ANSI-C rounds: `0x11111111 → 0x15EAB4E4`,
  bit-identical to the reference recurrence. The two-census
  methodology (I2) is confirmed behaviorally — different
  discovery, same stream.
- **I6's split executed.** A formula-side roll (`0038DB10`,
  `00389670`) and the weather draw advance ONLY `02EB3870`; the
  loot and AI-side draws advance ONLY `022C256C`. The
  correlation boundary is exactly where the contract draws it.
- **Conditional drawing executed, not just read.** `0025ABA0(1)`
  performs the probability call (`002658B0`, unloaded-script
  fallback 33) and touches **no** generator — the slot-1 arm is
  fully deterministic. `0025ABA0(2)` draws at `0025ABB8` before
  testing eligibility, matching the contract's "yes, before
  testing eligibility" correction.
- **I1 executed — the two Mersennes are disjoint.** The graphics
  seeder chain `_time64 → clock → 0018D680 → 0018D740 →
  0018EE20` writes exclusively to `01F7F600`; `02EB3870` is never
  read or written. The gameplay consumers never touch
  `01F7F600`.
- **I5 resolved — the graphics MT state address IS fixed.**
  `0015BCF0` loads it by `lea rcx, [rip+…] → 01F7F600` for both
  the init (`0018D740`) and twist (`0018EE20`) calls; the
  consumer at `001946E0` uses `q[01F7FFC0]` (cursor) +
  `d[01F7FFC8]` (remaining count) + the same twist call. I5's
  "no rip-relative operand → no fixed address" was true of the
  twist body but not of the instance.
- **First-draw semantics executed**: after seeding (index=624),
  the first draw re-twists all 624 dwords then consumes index
  0→1 — `mt_idx 624→1` with a full-state hash change, consistent
  with textbook MT19937 exhaustion-triggered twist.

## Fixture disclosure

- `lcg-loot-inliner`: planted descriptor `q[02EBF0C0] →
  {count=4, stride=4, row=0}` and encoded-table base
  `q[01F83530] → table` (the `0020E600` resolver base — runtime
  BSS cell). Probability byte `table[1·4+2]=80`; verdict =
  `roll%100 < 80`. MODEL-PROVEN fixture; the descriptor cell is
  the S-01/S-04 family cell.
- `lcg-yaw`: planted `obj.q[+0x30] → sub.q[+0x6A0] → buf`;
  `xmm1=-1.0f` selects the drawing branch (`comiss` skips the
  roll for non-negative inputs).
- `prng-render`: `d[022D9138]=1` draw-enable guard (BSS).
- `gfxmt-seed`: `_time64`/`clock` IAT stubs return fixed
  `0x1BADD00D`/`0x0C0FFEE`; the mix, init and twist bodies are
  shipped bytes.
- Gameplay MT seeded by its real `00863D30` body each case.
- Evidence class: **NATIVE-REPLAY** over shipped bytes with
  disclosed fixtures. No reachability claim — `001946E0`'s
  Phyre-boundary heavyweight consumer was not run; the seeding
  path and the draw/init bodies executed instead.
