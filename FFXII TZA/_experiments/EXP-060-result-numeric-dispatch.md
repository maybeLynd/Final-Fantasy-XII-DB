---
experiment: EXP-060
title: result numeric dispatch and outgoing flag translation
status: COMPLETE - bounded isolated original-code evidence
contract: ../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original numeric applier segment with injected parent-frame roles and five no-effect setter stubs; no native resource writes.
contract_coverage: Caller-side HP presence, numeric and register-flag translation at 00311608; HP callees are no-effect stubs, so no HP store or lethal transition is established.
tool: evidence/EXP-060-result-numeric-dispatch/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-060: result numeric dispatch and outgoing flag translation

**Result:** 22 isolated original-segment controls passed; a wrong-shift mutant
was detected. ASTRA, 2026-09-11. No game process was accessed.

## Question and method

The current [applier](../07-Combat-Action/applying-a-result-to-a-target.md)
execution-order table describes the numeric calls in steps 10–13. This experiment
checks presence gates, absolute/delta selection, argument widths and outgoing
flags against original instructions, following the local output meanings from
[EXP-059](EXP-059-formula-copyout-controls.md). The two experiments were executed
separately; this is not an executed composition of their fixtures.

[check.py](evidence/EXP-060-result-numeric-dispatch/check.py) verifies the certified
EXE SHA-256 and executes `00311608..00311777`, stopping at `00311778` before
status-layer work. The complete 2040-byte parent `003112F0..00311AE7` is retained
as static context in the [disassembly](evidence/EXP-060-result-numeric-dispatch/disassembly.txt).
Its earlier gates and later effects are not executed.

RBX is an injected result pointer, RDI an injected target stats pointer, R12 and
R15 are the HP/MP delta entry addresses, R13 is zero, and stack `RSP+0x88` holds
the source stats pointer or null. The parent establishes those roles: `003112FF`
saves entry RDX in the later `RSP+0x88` slot, `0031131B` takes target from R8,
and `003114AD`/`003114BB` load the delta entries. The segment fixture tests a
nonzero preserved R14 value without claiming that earlier parent path produced it.

All five setter entries are explicit no-effect stubs. They record register
arguments, clobber volatile RAX/RCX/RDX/R8/R9, then return to the original callsite.
HP calls record RCX, EDX, R8 and R9D; MP/secondary calls record RCX, EDX and R8D.
Additional HP stack arguments are neither measured nor established by this test.
This is not the complete HP callee contract or a full applier ABI test.

## Verified dispatch

Bit numbers are zero-based bits of result flag A at `+0x2C`. In the formulas
below, `bN` is input bit N, and `!bN` is its boolean complement.

| Call, in execution order | Presence | Absolute selector | Delta / absolute entry | Value and outgoing flags |
|---|---|---|---|---|
| Target HP | b8 | b3 | `00300530` / `00300520` | EDX = dword `+0x24`; R9D = `(b19<<8) \| (b10<<5) \| (!b18<<6) \| (!b6<<4)` |
| Target MP | b14 | b4 | `00300CE0` / `00300C90` | EDX = sign-extended word `+0x2A`; R8D = `(b16<<5) \| (!b12<<4)` |
| Secondary target operation | signed byte `+0x1D` nonzero | none | `00300BC0` | EDX = signed target word `+0x28` times signed result byte `+0x1D`; R8D = target-MP flags plus `0x400` if multiplier negative |
| Source HP | source nonnull and b7 | b1 | `00300530` / `00300520` | EDX = dword `+0x20`; R9D = `(!b5<<4) \| (!b17<<6) \| (b9<<5)` |
| Source MP | source nonnull and b13 | b2 | `00300CE0` / `00300C90` | EDX = sign-extended word `+0x28`; R8D = `(!b11<<4) \| (b15<<5)` |

RCX is the respective target/source stats pointer. Target HP receives the source
pointer in R8, including null; source HP receives zero in R8. A null source skips
both source calls. Target-null behavior is outside this injected segment entry.
The original reloads flag A between calls; no-effect stubs do not test callbacks
that mutate the result or reenter the applier.

The fixed HP values `FFFFFFFE` and `80000001` preserve their dword patterns.
Target MP `8001` becomes EDX `FFFF8001`; source MP `FFFF` becomes `FFFFFFFF`.
Thus numeric -1 is forwarded when the presence flag selects a call; these numeric
fields do not have an independent -1 absence guard here. Secondary controls
include negative multiplier -128 with signed resource -2 (product 256), and
positive multiplier 127 with signed resource -32768 (negative product).

## Contradiction and correction scope

Steps 11–13 of the linked applier page currently disagree with these instructions:

| Published input mapping | Verified input mapping |
|---|---|
| Target MP / secondary: b11 to output 5, !b8 to output 4 | b16 to output 5, !b12 to output 4 |
| Source HP: !b1 to output 4, !b11 to output 6, b4 to output 5 | !b5 to output 4, !b17 to output 6, b9 to output 5 |
| Source MP: !b7 to output 4, b10 to output 5 | !b11 to output 4, b15 to output 5 |

The target-HP mapping in step 10 is correct. The discrepancy appears consistent
with treating shift counts as original bit positions while overlooking the
subsequent output mask; that explanation is an inference, not execution evidence.
FABLE receives a contradiction for semantic correction and propagation; OPUS
receives a request to inspect affected structured records. Routing alone does not
close the contradictory canonical claims.

## Controls, falsification and limits

Cases cover no effects, all four delta calls, 15 individual flag-bit changes,
all absolute selectors, null source, both signed secondary controls and all bits
set with a secondary operation. Every case reaches the exact stop, preserves
RSP/RBX/RDI/R13/R14, compares ordered calls and all measured arguments, verifies
no nonstack writes, and compares the entire surrounding result/target/source page.
The [result](evidence/EXP-060-result-numeric-dispatch/result.json) records inputs,
observed/expected calls, writes and instruction visits. Source, binary, disassembly
and results are sealed in the [manifest](evidence/EXP-060-result-numeric-dispatch/manifest.json).

The private mutant changes `SHR EAX,11` at `00311679` to `SHR EAX,6`, making target
MP use input bit 11 instead of 16. With bit 16 independently set, execution reaches
the same stop but outgoing flags differ and the comparison rejects it. All 22
unmodified controls passed on first execution.

No native setter memory effect, lethal transition, clamp, action identity, live
timing or whole-resolution parity is established. This evidence supplies the
local dispatch and register-argument translation required before those effects
can be composed or compared with a live action capture.
