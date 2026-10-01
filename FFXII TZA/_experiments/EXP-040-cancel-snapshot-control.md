---
experiment: EXP-040
title: original cancellation stores and command snapshots
status: COMPLETE - bounded isolated original-code evidence
contract: ../07-Combat-Action/CONTRACT-commit-action.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original entry gates and two separately entered local blocks; no stubs, but intervening native calls are omitted.
contract_coverage: Optional cancellation dependency 003105D0 gates and selected local stores only; 0030F760 commit and omitted cancellation callees are not executed.
tool: evidence/EXP-040-cancel-snapshot-control/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-040: original cancellation stores and command snapshots

**Status:** PASS for isolated original-code gates/local stores; no live game and no native callees.
**Owner:** ASTRA. **Date:** 2026-09-11.

## Question and existing evidence

FABLE's command-state return identifies `BattleUnit_CancelAndResetCurrentAction` at `003105D0`
as a writer of the fields sampled by [EXP-032](EXP-032-command-snapshot.md).
Can the certified instructions produce the expected live-command reset while retaining the
previous 24-byte block? Does cancellation always reach those writes? This tests local effects
before the [EXP-037](EXP-037-command-observer.md) observer is used live; it cannot explain the
stalled attack in [EXP-027](EXP-027-ordinary-kill-control.md), which did not sample these fields.

## Original bytes and method

[extract.py](evidence/EXP-040-cancel-snapshot-control/extract.py) verifies the certified executable
SHA-256 and finds the PE runtime-function record containing the known cancel call at `00310618`.
That unwind extent is **a fragment**, `003105EF..0031076C`, not the entire function. Its original
[bytes](evidence/EXP-040-cancel-snapshot-control/function.bin),
[identity](evidence/EXP-040-cancel-snapshot-control/identity.json) and
[disassembly](evidence/EXP-040-cancel-snapshot-control/disassembly.txt) are preserved.
Inspection of adjacent original instructions establishes entry `003105D0`, both early-exit jumps,
the shared epilogue and final `ret` at `00310771`; the next function begins at `00310780`.
The complete contiguous 418 bytes and [disassembly](evidence/EXP-040-cancel-snapshot-control/full-disassembly.txt)
are retained separately as `full-function.bin` and `full-disassembly.txt`.

[check.py](evidence/EXP-040-cancel-snapshot-control/check.py) uses a fresh Unicorn instance per
case, a patterned synthetic `0xF50`-byte unit, high-bit context and target values, distinct retained
bytes and a controlled stack. It executes three independent scopes, stopping at explicit boundaries:

1. **Entry gates:** run from `003105D0`. Null RCX and a unit with null qword `+0x698` reach the
   injected return sentinel with expected RSP and no unit-memory changes. A nonnull stats pointer
   stops at `00310605`, **before** the first native call `00310780`. It is not dereferenced here.
2. **Unnamed byte:** run `0031060A..00310618`, stopping before the first resource-release call.
   It changes only byte `+0x6B6` to zero in the fixture unit.
3. **Command stores:** run `003106B9..0031072F`, stopping before call `003291B0`. Inject RBX=unit,
   RSI=unit+`0x80`, RBP=0; the original body sets EBP=0 at `00310649`, but the intervening native
   calls and their effects are not executed or credited. EXP-032's actual reader decodes before
   and after. Each case compares the whole unit against the expected local changes.

No calls are replaced by stubs. The two local blocks start after omitted calls; they are conditional
local-effect tests, **not execution of a complete active-unit cancellation**. The early-return
cases do execute the original path through return.

## Observed local effects

All three command-store cases passed with initial live flags `0`, `3` and `0xFFFFFFFF`, covering
low-bit clearing and retention of high flag bits. Each reaches the boundary after 19 executed
instructions, with 14 memory writes; the recorded trace also contains the stopped boundary.

| Field/span | Effect in the tested block |
|---|---|
| `+0x700` dword | AND `0xFFFFFFFC`; other flag bits retained |
| `+0x708` qword | Zero, including high 32 bits |
| `+0x710` dword | Zero target handle |
| `+0x714` word | `0xFFFF` action ID |
| `+0x6B4` byte | Zero phase |
| `+0x6B7` word | Zero |
| `+0x718..+0x72F` | Unchanged by this block |
| `+0x730..+0x747` | Exact copy of the retained `+0x718..+0x72F` bytes |
| `+0x6D0`, `+0x6D8`, `+0x760`, `+0x768` qwords | Zero |
| `+0x75C` dword | Zero |

All other unit bytes were unchanged in these local cases. The separate earlier block clears
`+0x6B6`; it is intentionally not attributed to the later block. The full-body disassembly contains
no direct stores into `+0x718..+0x72F`, but omitted callees are outside this experiment's proof.

[Raw results](evidence/EXP-040-cancel-snapshot-control/result.json) include executed addresses,
write ranges, before/after command snapshots, copied bytes and changed offsets. The null-unit,
null-stats and nonnull-stats gate traces have 4, 11 and 12 visited addresses respectively, including
the stop boundary. They do not establish whether the stats pointer denotes a live object globally.

## Falsification control and implications

[width_control.py](evidence/EXP-040-cancel-snapshot-control/width_control.py) changes only a private
copy's REX prefix at `00310722` from `0x48` to `0x40`, reducing the context store from 64 to 32 bits.
The original produces zero; the mutant leaves `0xFEDCBA9800000000`, detected as incorrect.
Both executions reach the expected pre-call boundary. [Results](evidence/EXP-040-cancel-snapshot-control/width-control.json)
retain both code hashes; the certified original remains unchanged. This is one relevant local
fault control, not a complete mutation campaign or integrated replacement test.

The local reset pattern and retained-copy behavior now compose with the actual snapshot decoder.
The additional `+0x730` copy is observable evidence of another command-record destination; its
consumer and lifetime are not established here. Snapshot labels remain raw: these values alone
cannot uniquely identify cancellation, its cause, execution timing or enemy death. In particular,
null stats bypass cancellation writes entirely, and a retained block is not proof of an active command.

The [manifest](evidence/EXP-040-cancel-snapshot-control/manifest.json) seals scripts, original bytes,
results and source identities. FABLE receives the bounded result for semantic integration; shared
semantic/type files are not modified here. Live command transitions, handler hits and the loaded
armed-deadline control remain pending UI resumption. No reference-game process was used.
