---
experiment: EXP-046
title: target-buffer reset and the remaining handle wording
status: COMPLETE - bounded isolated original-code evidence
contract: ../07-Combat-Action/CONTRACT-battle-target-buffer.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original reset and import thunk with controlled memset fill; fill writes are separately labeled.
contract_coverage: Original reset 00316CF0 and import thunk; memset is a controlled fill, not execution of the native DLL.
tool: evidence/EXP-046-target-buffer-reset/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-046: target-buffer reset and the remaining handle wording

**Result:** original reset wrapper calls `memset(buffer, 0, 0x208)`, restores prior
flag bit 0, and zeroes a word at +1. Four isolated wrapper cases passed with an
explicit fill stub. ASTRA, 2026-09-11. No live game or native DLL execution.

## Question and authority

The action-commit page still described `00316CF0` as releasing a handle at unit+778
and `00316CD0` as assigning it. The corrected layout and
[EXP-043](EXP-043-target-buffer-boundary.md) instead identify an embedded target
buffer and an actor-pointer append. This experiment establishes the reset boundary
without inferring actor lifetime operations from that old wording.

[check.py](evidence/EXP-046-target-buffer-reset/check.py) checks the certified
executable hash, extracts the complete 57-byte reset at `00316CF0` through RET at
`00316D28`, and decodes its sole call's six-byte import thunk at `00861EC0`.
The PE import directory identifies IAT VA `008C2A60` as `VCRUNTIME140.dll!memset`.
[Disassembly](evidence/EXP-046-target-buffer-reset/disassembly.txt) and exact
[wrapper](evidence/EXP-046-target-buffer-reset/function.bin) and
[thunk](evidence/EXP-046-target-buffer-reset/thunk.bin) bytes are retained.

## Controlled execution and result

Each case creates fresh Unicorn memory with a patterned 4 KiB data page, the buffer
at page+100h, a return sentinel, and distinctive RBX/RDI values. The original wrapper
executes before and after its call. At the import thunk, an explicit stub records
RCX/RDX/R8, writes the requested fill, returns the destination in RAX, and resumes
at the original call return. The actual imported DLL is not run. Stub effects are
reported separately from original-instruction memory-write hooks.

| Initial flag byte | Initial count | Final flag byte | Final count |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 |
| FEh | 32 | 0 | 0 |
| FFh | -1 (malformed fixture) | 1 | 0 |

Each case calls the fill exactly once with `(buffer, 0, 0x208)`. The full data-page
comparison requires all bytes outside the buffer unchanged and every buffer byte
zero except retained bit 0. This includes all 32 entry actor/outcome pairs, count,
and header padding. Original post-call data writes are exactly byte buffer,
byte buffer again, and word buffer+1, in that order. The whole wrapper reaches its
return sentinel with RSP+8 and RBX/RDI preserved. RAX remains the buffer pointer
returned by the controlled memset; no caller-level return contract is inferred.

A private mutant changes the requested fill length from 208h to 108h. It still
returns normally, but the exact argument and full-page checks reject it because
the latter half of the entries remains patterned. The original bytes are unchanged.
[result.json](evidence/EXP-046-target-buffer-reset/result.json) retains all traces,
call arguments, write addresses/widths, buffer snapshots and the fault control.

## Interpretation, correction and limits

Reset clears entries as well as the count. Append alone does not initialize the
entry's outcome half; following this reset, that half starts zero because reset
cleared it. These are local memory effects, not a proof of any broader caller order,
actor ownership, deallocation, target lifetime or live combat transition.

The [action-commit paragraph](../07-Combat-Action/the-moment-an-action-is-committed.md)
now names buffer reset/append and withdraws its handle-release wording. No unrelated
broadcast, enmity, timing or commit-range claims were retested or promoted here.

Initial sandbox execution could not import the existing Unicorn x86 constants
because the library directory was inaccessible. It stopped before emulation or
output creation. Running the same source with access to that existing library
passed; no source repair or package installation was involved.

Run `check.py` with the existing Windows Python environment and an empty evidence
output set; outputs use exclusive creation. The
[manifest](evidence/EXP-046-target-buffer-reset/manifest.json) seals this preparation.
The imported fill is a controlled dependency, so this is isolated wrapper evidence
with stipulated memset behavior, not full native execution or game validation.
