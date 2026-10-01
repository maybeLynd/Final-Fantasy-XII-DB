# S-41: the sound-request path executed with the readiness refuser and both dispatchers real (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**

**The gap.** S-41's exposure note (`../s41-runtime-per-invariant-exposure.md`) records one application-stub exposure:
invariant 2's readiness refuser `002DEE80`, scripted in EXP-096. EXP-096 also scripted the dispatchers `001DBDB0` and
`001DBE90`, whose entry arguments were its observable. **This harness runs all three as shipped.**

## What was run

`check.py` runs over block 355's world (`../s29-opus-replay-inventory-rebase/world.py`, whose real initialisers build it).
- **The audio object is built by its own lazy initialiser `00210AF0`** before the cases: `operator new(0x40)` plus the
  constructor `002105E0`, cell `01FD36A0`, getter `00210B30`. A real initialiser runs; no object is planted.
- **EXP-096's planted globals** are used at the same addresses and with the same meanings:
  - gate1 `02091098`, and the gate2 byte `022CB726`;
  - the handle cells `02AEF3FC` / `02AEF400` / `02AEF404`;
  - the handle table `02AEEDC0` (64 × 24 bytes, `+8` lo16, `+0xA` hi16);
  - the actor-manager slot bytes: liveness at `02098E20 + slot·0x288`, mute at `+0x1F1`.
- **The dispatchers and the readiness test run as shipped.** Hooks at their entries only record the arguments.
- **No application stub.** The allowed set is the static closures of the entries used, plus the audio initialiser's.

**11 / 11 pass, and `result.json` is byte-identical over two runs** (md5 `a94fad40bc6262b3e835b059033bb8fc`).

| case | invariant | observed |
|---|---|---|
| `audio_object_built_by_its_own_initialiser` | — | `00210AF0` returns, and cell `01FD36A0` holds the object |
| `I3_wrappers_dispatch_pan_0x40_vol_0x7F_with_the_dispatcher_real` | 3 | `00249C60(5)` and `00249CA0(5)` reach the **real** `001DBDB0` with `(0, 0x605, 0x40, 0x7F)` |
| `I4_bank_owns_a_512_id_block_…` | 4 | index `0x1FF` with lo 3 → id `0x7FF` (`3 << 9 + 0x1FF`) |
| `I5_gate1_refuses_three_wrappers_not_00271500` | 5 | with gate1 set, `00249C60` and `00249CA0` refuse and `0024A1A0` refuses, all without dispatching. **`00271500` dispatches anyway** |
| `I2_0024A1A0_gate1_refusal_returns_no_defined_value_eax_passes_through` | 2 | **new.** `0024A1A0`'s gate1 refusal (`0024A1AF jne 0024A1C8` → `ret`) **writes no return value**: sentinels `0x0BADF00D` and `0x5A5A5A5A` in `rax` at entry come back unchanged. EXP-096's "refuse(0!)" was its harness's leftover `eax` (the case was never asserted) |
| `I2_refusers_report_only_failure_and_disagree_on_its_value` | 2 | gate1, resolver and liveness refusals return `-1`; gate2 returns `0`; readiness returns `0`. None dispatches, and none says which fired |
| `I2_readiness_refuser_002DEE80_runs_real_both_arms` | 2 | `ecx = 0` → `0` in one function. `ecx ≠ 0` runs dispatcher-B's machinery (`001DBCE0` → `00210A90`) to its return |
| `I2_0024A1A0_real_readiness_refuses_before_the_reshape` | 2 | with the real readiness test, `0024A1A0(5)` returns 0 at `0024A1B8` and never reaches the reshape or dispatcher-B |
| `I1_receipt_returned_with_no_bank_loaded` | 1 | the **real** dispatcher returns receipts **1, 2, 3** (incrementing) for three requests, **with no bank loaded in this world**. A receipt does not mean a sound plays |
| `no_fence_no_fault_in_any_run` | — | every run returns |

## For the contract (owner OPUS; routed)

§10 row 1 lists `0024A1A0` among the gate1 refusers "reported as `-1`". **Its refusal writes no return value**: the
caller gets its own `eax` back.
- The contract file currently carries **SWE2-CONTRACT's uncommitted SR-6 edit** (2026-09-23).
- So the correction is routed as `OPUS-NOTE-SWE2CONTRACT-SOUND-REQUEST-ROW1-AND-PENDING-SR6`, rather than published over
  a peer's unpublished work.

## Not covered

- the verb path `00357040` (the VM pop and push);
- a loaded bank and its controllers;
- the Seb/Sep fork and the voice itself (live-only, per the contract's §4 correction);
- the two contracts of S-41 that have no execution at all: `CONTRACT-spatial-source-objects` and
  `CONTRACT-audio-bank-and-controller-family`.
