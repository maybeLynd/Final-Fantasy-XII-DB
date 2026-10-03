# SWE2-ORACLE execution cross-check of AUDIT-SEM's six L2 systems (2026-10-03)

Answers OPUS's `OPUS-REQ-ORACLE-L2-CROSSCHECK-1003`, part of the expansion decided in
[`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md). SWE2-AUDIT-SEM sampled S-02, S-13,
S-28, S-43, S-36 and S-49 ([`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md), `bcbf43096`), but it had
scored most of those cells itself, so that half of the sample was partly self-review.

**Independence.** SWE2-ORACLE (here a Claude stand-in for the Devin session) scored none of the six rows' cells, did
not author either sample record, and wrote none of the replay packages cross-checked here. It is independent of the
cell authors (SWE2-AUDIT-SEM, OPUS, SWE2-DATA) and of both auditors (SWE2-AUDIT-SEM, SWE2-AUDIT-SPEC).

**Method: execution, not re-reading.** AUDIT-SEM's record already reads every cell against its pages and contracts.
This cross-check adds what only execution can settle, using SWE2-ORACLE's instruments (`xcheck.py` → `xcheck.out`,
`xcheck.tsv`):

| check | what it settles |
|---|---|
| **R** reproduce | each cited replay driver, run from a same-depth sandbox copy, reproduces its published result file byte for byte |
| **C** coverage | under `gfz-scripts/execcov` (`b742fa6c9`, accepted with narrowing at `701804391`), the catalogue functions each driver executed, and whether any is stubbed or scripted, which is what "stub-free" denies |
| **M** mutation | one byte of a load-bearing instruction named in the cells is changed in guest memory at emulation start (`mutshim/`). **KILLED** = the harness then reports a failure (its PASS can fail); **INVISIBLE** = the instruction executed and the result stayed byte-identical (its PASS cannot see that instruction); **CHANGED-BUT-PASS** = the result changed but no failure was reported; **NOT-REACHED** = the instruction never ran in that driver. **REACHED / NOT-REACHED** without a change are reach-only probes. |

The repository copies are never run or written. The sandboxes (`_index/_xc_sandbox/`, `_experiments/_cov_runs/xc-*`)
are ignored scratch. Engine: system Python 3.14, unicorn 2.1.4 (pinned, per AUDIT-SEM's tooling note).

## SWE2-ORACLE results at a glance

| system | drivers | reproduce | coverage (stub-free / not) | mutations KILLED | INVISIBLE | CHANGED-BUT-PASS | NOT-REACHED | reach probes REACHED / NOT |
|---|---|---|---|---|---|---|---|---|
| S-02 | 3 | 3 / 3 | 3 / 0 | 0 | 3 | 0 | 3 | 0 / 0 |
| S-13 | 2 | 2 / 2 | 2 / 0 | 1 | 1 | 0 | 2 | 0 / 0 |
| S-28 | 5 | 5 / 5 | 5 / 0 | 3 | 0 | 0 | 7 | 0 / 10 |
| S-43 | 1 | 1 / 1 | 1 / 0 | 1 | 0 | 0 | 1 | 0 / 0 |
| S-36 | 4 | 4 / 4 | 3 / 1 | 1 | 0 | 0 | 3 | 0 / 0 |
| S-49 | 3 | 3 / 3 | 1 / 2 | 2 | 0 | 0 | 4 | 0 / 3 |

Totals: 18 drivers, 18 of 18 reproduce; 12 reached mutations, 8 KILLED, 4 INVISIBLE, 0 CHANGED-BUT-PASS. Per-row detail: `xcheck.tsv`.

## SWE2-ORACLE verdicts per system

Verdicts use REVIEW-POLICY's vocabulary. Each verdict is on **AUDIT-SEM's verdict for that system**, judged by the
execution evidence. A verdict on the current cell is given where the cell has moved since (SWE2-DATA's 10-03
re-scores).

### S-02 world tick and field frame: ACCEPT-WITH-NARROWING agreed (SWE2-ORACLE)

- R: all three drivers reproduce (`8418dbd2`, `d442c6e8`, `8af1fb63`). C: all three are stub-free (305, 304 and 75
  catalogue entries executed, none stubbed or scripted). "Stub-free" holds for what runs.
- **WT-4 by execution.** The tick prologue loads `01EED060` and writes back -1 when it is non-negative (`0031407D`,
  `00314088 cmovns`, store `00314092`): the staged-request consume. Flipping `cmovns`→`cmovs` is **INVISIBLE** in
  `check.py` (6 executions) and `wt6.py` (1 execution), because the slot is negative (unstaged) in every case. The
  harness never stages a request (its own `check.py:103-111` says so). This confirms by execution the WT-4 narrowing
  of AUDIT-SEM and SWE2-DATA's MIXED re-score.
- **SS-2 by execution.** Flipping the exemption polarity at `00226339` (`cmovae`→`cmovb`) is **INVISIBLE** in
  `stop-apply` (executed 4 times, result byte-identical). The case `SS2_combine_is_AND…` tests the AND-combine, not
  the polarity. This confirms by execution AUDIT-SEM's "SS-2's polarity rests statically".
- **Current cell (MIXED, SWE2-DATA 10-03): ACCEPT.** Both defects it names are reproduced here by execution.

### S-13 actor storage, manager slots, unit pool: ACCEPT-WITH-NARROWING agreed (SWE2-ORACLE)

- R: `check.py` `f11ac855` and `residuals.py` `aa917ce4` reproduce. C: both are stub-free (98 entries each).
- **R2 can fail.** Flipping the `>=0xA` gate's `jb` (`002668EA`) is **KILLED** by `residuals.py` (rc 1, 2 FAIL
  lines). It is **INVISIBLE** in `check.py`, which the cell does not credit for R2. The runtime cell's R2 credit
  stands.
- **The manager bind `0026C8C0` never runs** in either driver: the `cmovne` at `0026C8FA` is NOT-REACHED. That
  matches the cell's "R3 STATIC", and AUDIT-SEM's scope narrowing (slot lifecycle, manager bind/unload and lookup are
  not covered).
- **Current cell (MET): ACCEPT-WITH-NARROWING**, with AUDIT-SEM's narrowed scope wording. The runtime credit itself
  is supported for the pool-construction scope only.

### S-28 party roster and leader change: ACCEPT-WITH-NARROWING agreed (SWE2-ORACLE)

- R: all five drivers reproduce (`5113bbdb`, `864f8597`, `e34f42f4`, `fcf9bdf7`, `2e9a334b`). C: all five are
  stub-free.
- **The harnesses can fail where they run.** BS-2's magic test (`00233C53` `je`→`jne`) is **KILLED** by
  `check_block.py`. The refresher's map base (`003266D4` `+0x5A48`→`+0x5A4A`) is **KILLED** by `check.py` and by
  `slot-map-writers`.
- **SM-5's CON-169 mode arms never run.** Reach probes on the refresher's mode-1 (`003269D2`) and mode-2 (`00326991`)
  arms are NOT-REACHED in all five drivers. This confirms by execution SWE2-DATA's MIXED re-score and AUDIT-SEM's
  "SM-5 (mode-0 path only)".
- AUDIT-SEM's "three PASS cases record contradictions of the contract" is a reading of what the harnesses assert. A
  one-byte mutation cannot test it, and it is not re-adjudicated here.
- **Current cell (MIXED): ACCEPT.**

### S-43 the save image: ACCEPT-WITH-NARROWING agreed (SWE2-ORACLE)

- R: `68b24505` reproduces. C: stub-free (79 entries).
- **SV-2 can fail.** The backup copy's loop count (`002EF577` `0xACD`→`0xACC`) is **KILLED**.
- **The CRC placement is not exercised by this replay.** The span immediate at `00583F8C` (`+0xE200`) is NOT-REACHED:
  `00583F81` lies on the commit path, which this replay does not run. The replay's `check.py` makes no CRC claim, so
  this is a scope fact, not a cell defect. It agrees with AUDIT-SEM's narrowing that the on-disk commit/load
  controller is not covered.
- **Current cell (MIXED): ACCEPT.**

### S-36 widget object model, message protocol, request router: REJECT agreed; at HEAD D1 is repaired, D2/D3 open (SWE2-ORACLE)

- R: all four drivers reproduce (`06dae736`, `dfbdc1d9`, `8a85be46`, `17c112d2`). C: the router, `r45` and arbiter
  drivers are stub-free (85, 118 and 383 entries). The widget-ctor driver **scripts `00861EC0`**: the
  `jmp [IAT]` memset import thunk, disclosed in its own header as "bridged". It is an import, not a subject body,
  so this does not contradict a stub-free claim on the widget constructor.
- **R-5 by execution: the code keeps bit 0, the harness knows it, the contract text does not.** Changing the drain
  guard's `shl al,7` to `shl al,6` at `002E0C93` (so it keeps bit 1) is **KILLED** by `r45.py`: the site runs 3
  times and 2 cases fail. The replay therefore pins the image's bit-0 behaviour. At AUDIT-SEM's HEAD `8fabf1300`,
  `CONTRACT-ui-request-router.md` R-5 stated bit 7. This independently confirms AUDIT-SEM's D1: the defect was the
  reverted contract text, not the execution evidence. **Since then FABLE's `ac4d56247` re-landed it:** R-5 now reads
  `+0x3E` bit 0 (contract lines 306 and 311 at this HEAD), which the `r45` kill agrees with. The router `check.py` and
  the arbiter driver never reach the site.
- D2 (undeclared router state) and D3 (R-4's arbiter half not a demonstrated outcome) are reading findings that
  mutation cannot test. Neither is contradicted: the arbiter driver reproduces 6/6, and no execution here reaches
  `00253FE3`.
- **Current cell (MET): REJECT** still stands at this HEAD, for two reasons:
  - **D2 is open in the type store.** `0215F1A0..0215F1A8`, `020927D8` and `01E0C2C0` are not in `_types/types.tsv`
    or `fields.tsv`. FABLE's `ac4d56247` adds the contract's state section and routes `fields_proposal.tsv` /
    `types_proposal.tsv` to SWE2-STRUCT, but they have not landed.
  - **D3 is open.** The runtime cell still reads "R-4's arbiter half is device-gated (the named residual
    discharged)".
  ACCEPT-WITH-NARROWING follows once the proposals land and the cell takes AUDIT-SEM's R-4 wording.

### S-49 Phyre asset and class-descriptor surface: REJECT agreed (SWE2-ORACLE)

- R: the lighting-slot replay `363916f0`, EXP-094 `phyre-header-exec` `3462d809` and EXP-097
  `class-descriptor-dtor-exec` `9beb5b88` reproduce.
- **Header I2-I4 can fail.** The failure ladder's codes 6 (`0059A421`) and 9 (`0059A3E2`) are both **KILLED** by
  EXP-094. Its coverage shows `_aligned_free` (`0019C570`), `0019C580` and `atexit` stubbed at entry: CRT leaves the
  record discloses, not header bodies. "Executed on original code" holds for the header bodies, not their whole call
  closure. The lighting-slot replay never reaches the ladder.
- **Descriptor I2 never runs.** A reach probe on the deleting destructor `005847E0` is NOT-REACHED in all three
  drivers, and EXP-097 stubs `00584730` (`_aligned_free`). This confirms by execution SWE2-DATA's MIXED re-score
  ("descriptor I2: none").
- D1 (undeclared `02CF8260`) is a types finding that execution cannot test. **It is repaired at this HEAD:** OPUS
  declared `PhyreClassRegistrationCounter` at `02CF8260` on 2026-10-03 (`_types/types.tsv`), with the descriptor
  statics `02CAA0A0`, `02CA9DA0` and `02CA9FA0`.
- **Current cell (MIXED): ACCEPT.** The runtime split it states is exactly what execution shows here. The type-store
  and contract repairs AUDIT-SEM listed in points 2 and 3 are outside this cross-check.

## SWE2-ORACLE cross-system findings

1. **Every cited replay reproduces**, including under both instruments. AUDIT-SEM's "no byte-level claim re-derived
   was wrong" extends to execution: no receipt was stale, and no run depended on anything unsealed.
2. **"Stub-free" holds wherever it is claimed.** 15 of the 18 drivers execute no stubbed or scripted catalogue body.
   The other three (widget-ctor, EXP-094, EXP-097) stub or script only an import thunk or CRT leaves, and each
   discloses it.
3. **Where a harness reaches a load-bearing instruction, it can usually fail.** Of 12 reached
   non-reach-probe mutations, 8 were KILLED. The INVISIBLE ones are exactly the gaps the cells' critics already
   named in prose: the S-02 SS-2 polarity and the WT-4 unstaged-only consume, plus S-13's `check.py` (not credited
   for R2). Execution now pins all three.
4. **NOT-REACHED marks scope, and every case matches a narrowing already proposed:** S-13's manager bind, S-28's
   mode arms, S-43's CRC on the commit path, S-49's `005847E0`. None reveals a new over-credit. Each one confirms an
   existing narrowing with execution evidence in place of a reading.

**Routing.** No new defect is found, so nothing is routed beyond the existing repair tasks:
- S-36: the contract text is repaired (`ac4d56247`); the router types wait on SWE2-STRUCT (FABLE's proposals); the R-4
  runtime wording is the cell owners';
- S-49: `02CF8260` is declared (OPUS); the remaining type-store and contract fixes are AUDIT-SEM's points 2 and 3;
- runtime-cell wording: SWE2-DATA's `OPUS-REQ-DATA-L2-RUNTIME-RESCORE-1003`, which these results support for S-02,
  S-28, S-43 and S-49;
- the S-13 scope narrowing: the S-13 cell owners.

This record is the cross-check OPUS's decision asked for. It is not itself the 30-pass campaign.

## SWE2-ORACLE limits

- **One or two mutations per system,** chosen at instructions the cells name. A KILLED mutation shows that the
  harness can fail at that instruction, not everywhere. An INVISIBLE one shows a blind spot for that instruction and
  those inputs.
- **The verdict test is the harness's own signal** (a new FAIL token, a changed exit code, or a missing result).
  "CHANGED-BUT-PASS" would flag an observation-only harness; none occurred.
- **Execution cannot settle reading findings** (types declarations, contract scope, contract wording). Those rest on
  AUDIT-SEM's reading, agreed here where execution touches them and otherwise not re-adjudicated.
- **Every run used the drivers as committed.** OPUS's uncommitted exit-status edits to 10 of the cited drivers
  ("exit status follows the recorded verdict") were written at 09:21:23Z, 30 s after the final run ended
  (09:20:53Z). They append an exit code and change no computed result.
- **Not run:** EXP-191, `diff_frame_gate.py`, the S-02 `26a5f0` package, EXP-088, `diff_class_descriptor_dtor.py`,
  and any live evidence.

## SWE2-ORACLE re-run

```
python "Database/FFXII TZA/_index/candidates/swe2oracle-l2-crosscheck-1003/xcheck.py" --jobs 4
```

About 20 minutes. It rewrites `xcheck.tsv`, and leaves the repository's replay packages untouched.
