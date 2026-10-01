# S-02 runtime, re-judged against EXP-191 per invariant (OPUS, 2026-09-25)

The goal gate names S-02 first. Its `types` cell is MET (AUDIT-SEM, 2026-09-25), and its binding gap is
`runtime` alone. The runtime paragraph in `L2-VERDICTS.md` §"S-02 — the world tick and the field frame
(OPUS)" was written before EXP-191. It says *"the exercised body is one function of three pages"*: only
the update gate `0028E290` had run. **EXP-191** (`_experiments/EXP-191-s02-world-tick-stop-registry-exec.md`,
37/37, stable ×3, NATIVE-REPLAY, `live_game: false`) now executes the other two pages:

- the world tick `00314020` (WT-1..WT-6);
- the system-stop registry `00226B30` / `00225CD0` / `00225EB0` / `00226280` (SS-1..SS-7).

This note scores nothing. It gives the scorer the per-invariant exposure the table's own qualifier asks
for. The S-01 precedent (`L2-VERDICTS.md`, S-01 cell) is that runtime MET has been granted only to
execution with **no callee stubs** (S-10's EXP-070). Runs with stubs have moved to MIXED, and the question
per invariant is *how far the scripted boundary can reach it*.

## Can a stubbed callee touch an invariant's state? A static cross-check

Every function that references the invariants' state was found image-wide (`data_xref_scan.py`, control
`02AEEDC0`):

| state | direct referencers (image-wide) | stubbed in EXP-191? |
|---|---|---|
| registry `01FD4160`–`01FD46D8` | `00225CD0`, `00225EB0`, `00226280`, `00226B10`, `00226B30`, `00226BA0`–`00226BE0`, small accessors `002260A0`–`00226260`, `00227370`–`00227640`, `00227D40` | **none**. The stubbed effectors (`226640`, `2E24C0`, `2E24E0`, `2EA8B0`, `2EA8E0`, `25A5D0`, `2547C0`, `254840`, `35B4B0`, `35B510`, `2DF370`, `2DF640`, `2EBBF0`) and messages (`182D40`, `182D60`, `182DA0`, `2DDC30`) do not reference it directly. |
| tick latch pair `01EED060` / `01EED064` | `00314020`, `00314410`, `00314440`, `00314530`, `003145E0`, `00314970` | **none** (`00314410` ran real) |
| `WorldTickActiveFlag` `022C2548` | `00314020`, `00314960` | **none** (`00314960` is not on the executed paths and is absent from the harness) |
| drain mask `02099ABC` | `0025BFB0` (the drain, real), `0025E4C0` (the interpreter), `00266D10`, **`0026A5F0`** | **`0026A5F0` is stubbed**: it is the latch callee `00314410` calls with 4 |

**Bound on this check.** It covers direct (rip-relative) references only. A stub's own callees, and
pointer-based access, are outside it. That is the standard absence caveat, stated rather than assumed
away.

## Per invariant

| inv. | EXP-191 | can a stub reach the claim? | owner reading |
|---|---|---|---|
| SS-1 (apply never reads the active bitset) | executed: memory-read hook, zero reads, bitset-invariance | only through a stubbed effector's own reads. No stubbed effector references `01FD46D4` directly. | **not reachable on direct references** |
| SS-2 (AND combine), SS-3 (28-slot cursor), SS-5 (`recB` bit 41) | executed | no: body-local arithmetic on registry state no stub references | **not reachable** |
| SS-4 (min-fade) | executed; the value is passed to stubbed `226640` | the claim is the value **passed**, computed in the body | **not reachable** |
| SS-6 (dirty-gated apply) | executed | no | **not reachable** |
| SS-7 (per-request reach) | ~~**partial**: the 3-manager loop ran, but the reach bit was not isolated~~ **NOT executed** (corrected in block 260: the loop EXP-191 ran is `00225CD0`'s hard-wired `cmp r12d, 3`, while SS-7's computation is in `00226BE0`, which no record executes) | — | **open** |
| WT-1, WT-5 (mode consults; 5 × 16 loop bounds) | executed | the mode-dependent call **sets** are control flow on `ecx`. The tail branches `228480` / `362DA0` depend on stub returns, and EXP-191 drove both polarities. | **not reachable** for the stated claims |
| WT-2 (drain precedes the first mode test) | executed | ordering is body-local; the mask **content** is fixture-supplied | **ordering not reachable**; mask content is fixture |
| WT-3 (`022C2548` 1 → 0 in every mode) | executed in-body; the image-wide count is static | no | **not reachable** |
| WT-4 (latch consumed once; deferred request; first-writer-wins) | executed | **yes, one path**: `00314410`'s first-writer-wins calls stubbed `0026A5F0(4)`, a direct referencer of the drain mask `02099ABC`. What `0026A5F0` does to the mask is **not executed**. | **exposed at `0026A5F0`** |
| WT-6 (slot-0-only chains) | executed with 5 real bodies, ~95 leaves scripted | leaf behaviour is scripted; the slot gating is real | **gating not reachable**; leaf effects are scripted |

## What this means for the cell (for the scorer, not scored here)

- By the table's committed qualifier (no stubs → MET), EXP-191 moves S-02's runtime from "one body of
  three" to **all three pages executed, with stubs**, which is the MIXED class S-01 received.
- **The exposure is narrow and named.** Every stop-registry invariant except SS-7 is out of any stub's
  direct reach. So are all world-tick invariants except WT-4's `0026A5F0` path.
- **What would close it:**
  - one execution with `0026A5F0` real (it is a direct referencer of the drain mask, so its effect is
    checkable in the same harness);
  - SS-7: an execution of `00226BE0` itself ("start a request"), with record A bit 31 clear and set (block 260);
  - or a live capture of one frame.

The first two are ORACLE work in the existing EXP-191 harness. They are routed; OPUS does not run them.

## Addendum (OPUS, 2026-09-25, block 243): the `0026A5F0` exposure, closed statically

WT-4's one exposure is the stubbed `0026A5F0(4)` that `00314410` calls on the first-writer-wins path
(`00314421`–`00314426`, taken when the latch `01EED060` is negative). The whole callee was re-read:

| site | effect |
|---|---|
| `0026A601` | `n == 0` first recurses for 1, 2, 3 (not taken for `n = 4`) |
| `0026A61C`–`0026A620` | `d[02099ABC] \|= 1 << n`, which is **`\|= 0x10`** for `n = 4` |
| `0026A626` → `002E15D0` (28 B, no calls) | `b[0215F1A0] = 0`, `d[0215F1A4] = 0`, `d[0215F1A8] = 0`, `b[0215F1A1] = 0`: the request mailbox's pending byte and its two argument cells (world-tick page, §"request mailbox") |
| `0026A635` → `002E1690` (8 B, tail jump) | `b[0215F1A1] = 1` |

Neither helper makes a call, and neither is in the direct-referencer sets of the latch pair, `022C2548` or the
registry. **Statically, `0026A5F0(4)`'s complete effect on S-02's state is one OR of `0x10` into the drain
mask.** The mailbox cells it clears belong to the request mailbox, which is outside WT-1..WT-6 and SS-1..SS-7.

This is a static closure (NATIVE/STATIC), **not an execution**. It makes the exposure a named, bounded effect
rather than an unknown one. The execution request (`OPUS-REQ-ORACLE-S02-CLOSE-26A5F0-AND-SS7`) stands.
Predicted result for it: the mask gains exactly bit 4, and `0215F1A0 = 0`, `0215F1A1 = 1`, `0215F1A4 = 0`, `0215F1A8 = 0`.

## Addendum (OPUS, 2026-09-25, block 253): SS-7's reach bound, closed statically

EXP-191 marks SS-7 **partial**. ~~Its fixture walked all three managers (bit 31 clear).~~ **Corrected in block 260:** the
three-manager walk EXP-191 ran is `00225CD0`'s, whose bound is the constant 3 (`00225E02 cmp r12d, 3`). SS-7's
computation is in `00226BE0`, the contract's "start a request" entry, which **no record executes**. So SS-7 is
unexecuted, not partial. The bytes settle how the bit bounds the walk:

| site | effect |
|---|---|
| `00226C77`–`00226C94` | `reach = (~(A >> 30) & 2) \| 1` from record A's low dword, stored **once** to `[rsp+0x30]` |
| `00226C99`–`00226C9B` | manager index `[rsp+0xB8] = 0` |
| `00226CA4`–`00226CB5` | per index: `00263FF0(i)` resolves the manager; `b[mgr+0x10] & 1` clear skips straight to the increment |
| `0022733A`–`0022734E` | `i++`; `cmp i, [rsp+0x30]`; `jl` back to `00226CA2` |

`[rsp+0x30]` is the 7th-argument slot of the outgoing-call area. Across the whole loop (`00226C99`–`00227354`) the
only access to it is the compare at `0022734A`, so no call inside the loop overwrites the bound. **Therefore the walk
covers indices 0..reach−1: three managers when bit 31 is clear, one when it is set.** A manager whose enable bit is
clear still consumes an index.

This is static (NATIVE/STATIC). It gives SS-7 a closed static reading. What is missing is an execution of `00226BE0` itself
(block 260), not merely one more case. The execution
request stands with a named prediction: with record A bit 31 set, `00263FF0` is called exactly once, with `ecx = 0`.
