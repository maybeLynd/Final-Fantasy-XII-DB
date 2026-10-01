# S-08 runtime: per-invariant stub exposure for EXP-128 / EXP-146 and the SECTION-02 controls (OPUS, 2026-09-25)

**Row:** S-08 resource request queue. The runtime cell is MIXED, pending the per-invariant analysis (the same
qualifier as S-14 and S-21). The contract is `02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`.
This note scores nothing.

**Which text I1–I7 means here.** The wording is the SECTION-02 overlay, which is owner-merged in the worktree and
waiting for FRONTIER to publish it. Where it differs from the published `HEAD` text, the table names the claim.

**The binding-gap cell ("the pump, requester and builder are all unexecuted") is stale on all three:**
- the pump `0032E070` runs real in **EXP-128**;
- the requester `0032E870` and the builder `0032E620` run real in **EXP-146**, together with the constructor
  `0032E450` and the slot-taker `0032E990`;
- EXP-146 also runs a single-process construct → request → pump → retire → free lifecycle;
- the SECTION-02 native controls (`_experiments/evidence/continuation-section02-resource-queue/`) add the 64-request
  same-call drain and the 65th-request full-pool retry on real recycled slots.

## Method (bounds stated)

These are the same bounded instruments as the S-14 and S-21 notes:
1. **Image-wide direct references** to the queue's state (`data_xref_scan.py`, over `Tools/work/graph/functions.tsv`),
   covering:
   - the slot pool `022C31C0` (64 × 0x80, every slot base);
   - the pending head `022C51C0` and tail `022C51C8`;
   - the free head `022C51D0`;
   - the request counter `01EED498` (read and written at `0032E90D` / `0032E947`);
   - the chunk gate byte `02B5E111`.
2. **Static callee closures** of the scripted set in EXP-128, EXP-146 and SECTION-02:
   - `003EADD0`;
   - `0046E030`, `002DF6C0`;
   - `0046DD50`, `003E9780`, `0036FD50`, `003BB790`;
   - `00862090`;
   - `0017D3E0`, `003691B0`, `00369190`, `0035E7A0`;
   - `001EDE80`, `0017D930`;
   - `0035EA30`, `0035EB70`.

Script: `s08_writes.py` (scratch).

### Findings

- **Only the queue's own functions touch its state.** The census finds:
  - the pool: `0032E450`, `0032E4D0`, `0032E590`, `0032E620`;
  - the heads: `0032E070`, `0032E450`, `0032E520`, `0032E870`, `0032E990`, `0032EC40`;
  - the counter: `0032E450`, `0032E870`.

  No foreign function references any of them.
- **One scripted callee can re-enter the queue.** It is `003EADD0` → `003EADE0`, which the queue page identifies as
  *the script BGM stream's eight-state machine* over the descriptor `02B5E0E0`. The paths are:
  - `003EADE0 → 0032E780` (head-inserting request) `→ 0032E870 → 0032E990` / `0032E070`;
  - `003EADE0 → 0032E4D0`.

  Every other scripted callee's closure is disjoint from the queue's state.
- **The pump calls that machine in two places:**
  - in a state arm at `0032E0BD`, where a **non-zero return ends the pass** (`0032E0C4 → 0032E2A0`, the footer);
  - after the pending list empties (`0032E29B`).
- **The chunk gate `02B5E111` is `BgmStream+0x31` (`streamActive`, `STATIC 0x02B5E0E0`),** the same descriptor's
  byte. `003EADE0` itself tests it (`003EADF4`). It is referenced only by `003EB050` / `003EB0A0` / `003EB0D0` /
  `003EB150`.

## Per invariant

| inv. | claim | can a scripted callee reach it? | owner reading |
|---|---|---|---|
| **I1** | constructor cursor at `slot+0x18`; selective initialisation; the counter resets to 1 | no: `0032E450` is body-local and no foreign function writes the pool or the counter | **not reachable** |
| **I2** | each slot on exactly one list; `022C51D0` is a mutable head | only the queue's own `0032E990` / `0032EC40` write the heads. The one scripted route in is `003EADE0 → 0032E780`, which uses the same, executed list code | **not reachable** for the ownership claim |
| **I3** | no free slot means blocking retry (pump → getter → pacer); a 65th requester can drain all 64 zero-byte requests itself in the same invocation | **Stall order:** body-local. **Same-call drain:** needs the pump's state arm to get 0 from `003EADD0` (`0032E0BD`); a non-zero return ends the pass. In a real run the BGM machine can also **insert a request at the head** through `0032E780`, taking a freed slot first. | ~~**order not reachable; the drain is exposed at `003EADE0`**, which no record executes~~ **order not reachable; the drain holds in every shipped run** *(OPUS, 2026-10-01: executed 2026-09-30 by SWE2-ORACLE, [`s08-bgm-machine-drain-0930`](s08-bgm-machine-drain-0930/README.md), ACCEPTED by SWE2-AUDIT-SPEC ([review](auditspec-review-s08-bgm-0930/REVIEW.md)): the same-call drain holds with the stream inactive, which is every shipped run, and with an active stream waiting for play (state 5). With the stream in a submitting state (1, or 7 with bytes left) and the pool full, the requester re-enters itself through the machine and nothing drains; that is a modded-script domain, like I5's chunking gate.)* |
| **I4** | id = `(counter << 6) + (slot & 0x3F)`; signed `cmovg` reset | body-local in `0032E870`; the counter is written only there and in the constructor | **not reachable** |
| **I5** | chunking follows the gate, not the size | the branch contract is `0032E620`'s own code. The gate's **value** is `BgmStream.streamActive`, written by the BGM stream code. The contract already separates "which states reach the gate" from the branch contract. | **branches not reachable; the gate value is a cross-system input** (S-42) |
| **I6** | offset truncates toward zero to a `0x800` multiple | a body-local instruction sequence | **not reachable** |
| **I7** | recycling does not sanitise | the splice `0032EC40` is real; no foreign function writes the pool | **not reachable** |

## What this means for the cell (for the scorer, not scored here)

- **Six of seven invariants are out of every scripted callee's reach.**
- **I3's same-call drain has one named exposure:** the BGM stream machine `003EADE0`~~, which has not been executed~~. *(OPUS, 2026-10-01: executed 2026-09-30 by SWE2-ORACLE, [`s08-bgm-machine-drain-0930`](s08-bgm-machine-drain-0930/README.md), ACCEPTED by SWE2-AUDIT-SPEC ([review](auditspec-review-s08-bgm-0930/REVIEW.md)): the same-call drain holds with the stream inactive, which is every shipped run, and with an active stream waiting for play (state 5). With the stream in a submitting state (1, or 7 with bytes left) and the pool full, the requester re-enters itself through the machine and nothing drains; that is a modded-script domain, like I5's chunking gate.)* Its
  return decides whether a pump pass continues, and it can enqueue at the head.
- **The same object** supplies I5's gate byte. So the queue's untested edge is a **cross-system contract with S-42**
  (music: `BgmStream`), not a queue-internal gap.
- **What would close it:** the SECTION-02 64/65-request controls with `003EADE0` real, over a planted `BgmStream`,
  once with `streamActive` 0 and once with it non-zero. *(Done 2026-09-30: [`s08-bgm-machine-drain-0930`](s08-bgm-machine-drain-0930/README.md) ran C0, C1, C3 and C4 with a negative control, `s08_bgm_drain.py` FAILS 0.)* `003EADE0` is 512 bytes. Its queue calls are the executed
  `0032E780` / `0032E4D0`. This is ORACLE work in the existing harness, and it is routed.
