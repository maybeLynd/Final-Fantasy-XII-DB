---
experiment: EXP-075
title: Reward indices are checked before installation; zero counts and missing tables differ
status: COMPLETE
contract: ../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md
tool: evidence/EXP-075-reward-index-prechecks/check.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-12
date_run: 2026-09-12
---

# EXP-075 — distinguish invalid reward indices from missing reward tables

**Result:** fourteen original-code fixture controls passed on first execution;
both private guard mutations were detected. ASTRA, 2026-09-12. This is isolated
original-code evidence with nine explicit callee stubs, not a live installation
or a death/reward observation.

## The claim being challenged

`OPUS-NOTICE-REWARDNULL` and the [reward contract](../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md)
§10 claim an out-of-range reward index builds a unit successfully, storing NULL,
then faults when killed. The [unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
§2.2 already describes earlier checks. Reading the complete original 1,808-byte
`BattleUnit_ApplyUnitDefinition` at `0023A570` confirms that the late NULL branches
were attributed to the wrong condition.

The original reward-index checks, before spawn-record lookup, are:

```text
0023A72C..0023A747: load slot 02EBF148; count = slot ? dword[slot+4] : 0
                  zero-extend word[definition+22]; compare to u32(count-1)
                  JA 0023A63A -> EAX=0, common epilogue, return
0023A74D..0023A768: same for slot 02EBF140 and word[definition+24]
0023A76E..0023A776: only then call SpawnKeep_ResolvePrimaryEntry
```

For a **positive count**, an index at or above that count returns failure before
the reward stores. The base-row check precedes the per-level check. For count
zero, `DEC ECX` wraps to `FFFFFFFF`; no zero-extended 16-bit index is above it.
A missing descriptor supplies that same zero count. Those cases therefore need
separate treatment from a positive-count index error.

The late branches at `0023A96F` / `0023A97C` and `0023A9B6` / `0023A9C3` test the
descriptor pointer and the result of `0020E600`, respectively. **There is no
count comparison in either late row-resolution block.** Failure selects zero
at `0023A9A3` / `0023A9EA`, then stores at `0023A9A5` / `0023A9F4`.

## Instrument, initialized state and limits

The [checker](evidence/EXP-075-reward-index-prechecks/check.py) reuses the established
Unicorn original-code technique. It checks the complete reference EXE SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` and image base
`120000`, extracts all 1,808 bytes and the three original float constants, and
runs from the actual entry to its actual return. Unicorn 2.1.4 / Capstone 5.0.7.

Each case gets fresh initialized pages: unit at `40000000`, definition at
`40001000`, class row at `40002000`, and an already-initialized spawn record at
`40003000`. Unit flags initially contain bit 26 only; its stats pointer is zero,
the two reward-pointer fields are `A5A5A5A5A5A5A5A5`, and the battle-system gate is
one. Definition id is `0100`. Descriptor counts, strides and resolver tokens are
explicit; class and order indices are valid zero. The spawn record's bit 0 skips
the fresh-record initialization/history branch. Its stats status fields are zero.
All fixture pages and seeded nonvolatile registers are read back before execution.

The nine **recording RET stubs** are `00236A60` (reset), `00303EC0` (selection
query), `00322050` (re-key), `0020E600` (opaque-token resolver), `00236100`
(spawn lookup), `002B58B0` (text), `00328FF0`, `00237040` and `002FEAB0`.
They do no memory writes. The resolver returns only the specified fixture bases
or zero; spawn lookup returns the specified record. All volatile integer registers
and XMM0–5 are clobbered at each stub. **None of their native effects is proved.**
In particular, unchanged reward sentinels on rejection describe this no-write
reset fixture, not what the real reset leaves in a real unit.

Checks compare EAX, exact call order and selected arguments, both guard/store
paths, complete fixture and constant pages, actual return address, stack balance,
eight nonvolatile integer registers and full 128-bit XMM6–15 values. Raw evidence
includes every visited instruction, non-stack memory read/write, before/after
page hashes and byte deltas. The oracle computes the unsigned decrement separately
and expects explicit native field writes. MXCSR starts at `1F80`; flag fidelity
and the unexecuted paths are not claimed.

## Controls and observed distinctions

Default counts are base=2, per-level=3; indices are their last rows, 1 and 2.
The independent row bases are `40005000` and `40006000`, each stride `38`.

| Case(s) | Local original result |
|---|---|
| Both valid last rows | EAX=1; pointers `40005038` / `40006070`; both stores reached |
| Base index=2, or per-level index=3 | EAX=0; no reward store and no spawn lookup |
| Both invalid | Base guard rejects; per-level guard is not reached |
| Index=FFFF, count=65535, each table separately | EAX=0, the corresponding early guard rejects |
| Index=FFFF, count=65536, each table separately | EAX=1; arithmetic produces base+FFFF×38 |
| Index=FFFF, count=0, each table separately | EAX=1; same unchecked row-address arithmetic after count underflow |
| Missing descriptor, index=FFFF, each table separately | EAX=1; corresponding reward pointer stored as zero |
| Descriptor present and index valid, resolver returns zero, each table separately | EAX=1; corresponding reward pointer stored as zero |

The large-count fixtures deliberately supply headers and row bases without
allocating 65,536 reward rows. The installer computes and stores these addresses;
it does not dereference the reward rows on this path. These controls prove that
arithmetic and the comparison boundary, not that the synthetic pointers are usable
reward data. Likewise, EAX=1 is the original local result under the stated callee
substitutions, not successful integrated actor construction.

Two private mutations replace `JA` with `JB` at the base and per-level guards,
one at a time. Each uses the corresponding index-equals-count case. Both now
return 1 and store a row pointer; EAX, call sequence, memory image and guard/store
path checks fail. Both still return normally with correct stack and nonvolatile
registers, so a normal return alone would miss the defect.

## Correction and remaining question

The absence of NULL checks in the reward consumers is a separate existing finding.
This experiment does not execute those consumers or establish a crash on death.
It refutes the proposed **positive-count out-of-range index → successful NULL
installation** path, while exposing the actual zero-count and resolution cases.

FABLE's current page reports all 2,292 shipped enemy selectors in range across
332 ARD files. That existing census was not rerun here and is not treated as proof
that registry descriptors and their resolved storage are always available during
gameplay. Runtime/loader reachability of the remaining failure conditions stays
open. OPUS must review and propagate the contract and executable claim-map
correction; FABLE must qualify the relevant installer prose. Consumer closure is
pending their integration, not inferred from this experiment's PASS.

[Raw results](evidence/EXP-075-reward-index-prechecks/result.json),
[complete disassembly](evidence/EXP-075-reward-index-prechecks/disassembly.txt),
extracted bytes and source are sealed by the
[manifest](evidence/EXP-075-reward-index-prechecks/manifest.json). Only private
emulator memory is modified; no game, save, registry file or original EXE is written.

```powershell
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-075-reward-index-prechecks/check.py'
```
