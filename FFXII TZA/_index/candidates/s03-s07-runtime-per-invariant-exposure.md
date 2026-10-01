# S-03 and S-07 runtime: per-invariant stub exposure (OPUS, 2026-09-25, block 297)

Both rows are MIXED, with AUDIT-SEM's qualifier "no per-invariant stub-exposure analysis yet". This note scores
nothing.

## S-03: battle runtime mode ladder (`CONTRACT-battle-runtime-mode.md`)

**EXP-098 has zero scripted boundaries.** Its record says so ("five bodies, ~238 bytes, **zero scripted
boundaries**"; `bodies.json` `stubbed` is empty):

| body | role |
|---|---|
| `0030D9A0` | the ladder |
| `00377C20` | the field-record bit-15 predicate |
| `003148F0` | the index getter |
| `002EF2B0` | the context getter |
| `002EF640` | the context base |

Only data cells are planted: `[02EBF190]` → state, `[02ADD100]` → table, and the index cell `[021654C4]`.

| contract item | executed | substitution reach |
|---|---|---|
| invariant 1: priority, not membership (`0xF` → 5) | `m5-priority`, `m4-over-low`, `m3-over-low` | none; there are no substitutions |
| invariant 2: exactly four bits, in order 3, 2, (bit 15), 1, 0 | all six modes plus the per-arm mutants | none |
| invariant 3: mode 3 comes from authored area data, above bits 1–2 | the predicate `00377C20` is real, over the planted table | none |
| invariant 4: the script-set modes are unreachable from gameplay code | a static caller census | n/a (static) |
| postcondition: the ladder writes nothing | "the predicate does not write the state block under this fixture" | none |
| the bit setters' one-bit writes | **not executed by EXP-098** | coverage, not exposure |

**Exposure set: empty.** The binding gap ("no live capture; … container readiness") is not a stub question.

## S-07: zone-script VM and native bridge

**The runtime cell names only EXP-013 and EXP-106. S-07's four contracts have more execution than that, and one of
the two named records does not execute S-07's subject.**

| contract | executed by | substitutions |
|---|---|---|
| `CONTRACT-interpreter-core.md` (the 100-opcode interpreter `0025E4C0`) | **Section11** (`_experiments/evidence/continuation-section11-script-resume/`, cited in the contract's §13): 146 named assertions and an identical repeat, with the interpreter, family initialiser, selected real callbacks and the full selected-kind request driver | "**zero application substitutions and zero import bridges**" (§13) |
| `CONTRACT-verb-dispatch-abi.md` + `CONTRACT-native-command-lifecycle.md` | **EXP-085**: five executor bodies, "zero stubs of shipped code" | the only planted code is the three **begin / poll / result callbacks**, fixture data by design. What a real verb does on the far side of its callback is out of the contract's scope, so the executor protocol (callback resolution order, argument surface, return handling) is exercised by shipped code |
| `CONTRACT-script-to-native-bridge.md` (VM pop boundaries) | **EXP-013**: 14 original-code calls, all returning at the expected boundary | `008620C0`, the native **error reporter**, is a `ret` stub. It is reached only on the failure paths of §10. It can hide the reporter's effects and whether it returns, not the pop / coerce / depth behaviour the record asserts |
| (EXP-106) | the field runtime pass `0025DF00`, **which scripts the interpreter `0025E4C0` as a boundary** ("own contract's subject") | EXP-106 is evidence for S-13 / S-18's field-runtime-pass contract. **It is not interpreter evidence** |

**Exposure per contract:**
- interpreter-core: none (stub-free);
- verb-dispatch and lifecycle: none on the executor protocol; the callbacks are fixtures by scope;
- bridge: only the failure-path report effect of `008620C0`.

**Stale texts.** The binding gap ("types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract
no longer binds it") contradicts the types cell, which is MET, and the executions above. The runtime cell should cite
Section11 and EXP-085.

`live_game` is false for every record above.
