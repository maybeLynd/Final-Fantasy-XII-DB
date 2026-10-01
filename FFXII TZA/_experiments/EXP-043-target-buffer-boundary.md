---
experiment: EXP-043
title: original target-buffer append boundaries
status: COMPLETE - bounded isolated original-code evidence
contract: ../07-Combat-Action/CONTRACT-battle-target-buffer.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original append, synthetic buffer, no stubs; negative counts are deliberate invalid-state controls.
contract_coverage: Complete original append 00316CD0; synthetic buffer boundaries, no actor dereference or consumer execution.
tool: evidence/EXP-043-target-buffer-boundary/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-043: original target-buffer append boundaries

**Status:** ten isolated original-code cases passed; one private stride fault detected.
**Owner:** ASTRA. **Date:** 2026-09-11. No live game used.

## Question and original authority

The corrected BattleTargetBuffer layout has 32 sixteen-byte entries starting at buffer+8, inside
a `0x208`-byte object. The former eight-byte interpretation was withdrawn. This experiment asks
which bytes the original appender actually writes, what bounds it enforces and what it returns.
It supports the current unit-map/type integration without repeating their broader embedding analysis.

[check.py](evidence/EXP-043-target-buffer-boundary/check.py) verifies the certified executable
SHA-256 and extracts the complete 24-byte function at `00316CD0`.
[Original bytes](evidence/EXP-043-target-buffer-boundary/function.bin) and
[disassembly](evidence/EXP-043-target-buffer-boundary/disassembly.txt) show:

```text
00316CD0  movsxd rax, dword ptr [rcx+4]
00316CD4  cmp eax, 0x20
00316CD7  jge return
00316CD9  add rax, rax
00316CDC  mov qword ptr [rcx+rax*8+8], rdx
00316CE1  inc dword ptr [rcx+4]
00316CE4  mov eax, dword ptr [rcx+4]
00316CE7  ret
```

Each case gets a fresh Unicorn instance, patterned memory with a 256-byte prefix before the buffer,
an injected return address and RCX/RDX inputs. The actor value has distinctive high bits and no
mapped referent. No calls, stubs, process memory reads or native game objects are involved. Every
case must reach the return sentinel with RSP advanced by eight and fewer than 20 visited instructions.
The test compares the entire mapped data page and exact write address/width/order, not only changed
byte values. That distinguishes a same-value store from no store and detects writes outside the buffer.

## Actual results

| Input | Original writes | Count/result EAX |
|---|---|---|
| Count 0 | Actor qword at +8, then count dword at +4 | 1 |
| Count 1 | Actor qword at +24, then count | 2 |
| Count 31 | Actor qword at +504, then count | 32 |
| Count 32 | None | 32 |
| Count 33, `INT32_MAX` | None | Original count |
| Count -1 (malformed) | Actor qword at **-8**, then count | 0 |
| Count -2 (malformed) | Actor qword at **-24**, then count | `0xFFFFFFFF` (-1 as int32) |
| Count 0, null actor | Zero qword at +8, then count | 1 |
| Count 1, actor already in entry 0 | Same actor stored in entry 1, then count | 2 |

Accepted valid-count cases preserve every byte except the eight-byte actor slot and four-byte
count. In particular, the other eight bytes of the sixteen-byte entry are **not initialized or
cleared by append**. There is no actor dereference, null rejection or duplicate search in this helper.

The signed upper-bound comparison rejects positive over-capacity counts but has no lower-bound
check. Negative fixtures are deliberately malformed state; their writes before the buffer do not
prove that the engine ever constructs such a count. A valid caller contract still needs an initialized
nonnegative count and valid storage. The tested `-1`/`-2` cases are not a claim about all malformed
addresses or the behavior of access violations.

The return is not a unique success boolean: both appending the 32nd entry and refusing an already
full buffer leave EAX=32. The result records full RAX, including zero extension after the final
EAX load. Caller use of that result and any lifetime meaning remain outside this experiment.

## Falsification and retained failure

A private mutant replaces only `add rax,rax` with three NOPs. The count-1 test then writes at the
eight-byte-stride location and fails the full-page/write-footprint comparison. This demonstrates
detection of the actual historical stride error. The original bytes remain unchanged. It is a local
fault control, not a complete mutation campaign or reconstruction-parity certification.

The first preparation attempt asserted encoding `48 01 C0` for the ADD instruction; the certified
image instead uses the equivalent encoding `48 03 C0`. The assertion stopped **before emulation**.
[Initial source](evidence/EXP-043-target-buffer-boundary/initial-source.py) and
[failure receipt](evidence/EXP-043-target-buffer-boundary/initial-failure.json) preserve that error.
The corrected assertion uses the observed bytes; no expected behavior or reference byte was changed.

[Results](evidence/EXP-043-target-buffer-boundary/result.json) preserve exact traces, writes, raw
buffer/prefix snapshots and the private mutant. The
[manifest](evidence/EXP-043-target-buffer-boundary/manifest.json) seals the package. Return the
bounded contract evidence to OPUS; no shared type rows are edited here. FFXII automation remains
paused, and this experiment establishes no live target selection, outcome initialization or enemy death.
