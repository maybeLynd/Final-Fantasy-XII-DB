---
experiment: EXP-056
title: save normalization copies, restore gate and seed ordering
status: COMPLETE - bounded isolated original-code evidence
contract: ../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original normalization body to seed tail boundary; getters, clock and native dependencies controlled, flag intervention labeled.
contract_coverage: MT seed caller 00584210 arithmetic and tail argument at 00379CF0, explicitly described in contract section 7; MT seeder and native normalization dependencies omitted.
tool: evidence/EXP-056-save-normalize-roundtrip/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-056: save normalization copies, restore gate and seed ordering

**Result:** twelve isolated original-code cases passed; a wrong seed-mask-order
mutant was detected. ASTRA, 2026-09-11. No game process was accessed.

## Question and method

The [normalization page](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
describes a stash/restore operation followed by reseeding. This experiment asks
which bytes the body itself moves, what actually admits restoration, and whether
bit 31 is cleared before or after the timer contribution. Distinguishing controls
are the four mode/flag combinations, a carried-buffer roundtrip and a seed whose
timer term makes the final high bit nonzero.

[check.py](evidence/EXP-056-save-normalize-roundtrip/check.py) verifies the certified
EXE SHA-256, extracts and executes all 456 bytes at `00584210..005843D7`, and stops
at the outgoing tail target `00379CF0`. It uses a patterned synthetic `0x50000`-byte
save buffer, a synthetic `0x8000`-byte battle block, isolated global pages and stack.
Both `002EF640` calls return the same save buffer. Mode, accumulator result, time
and timer are controlled inputs. These getter results are fixtures, not evidence
about native allocation or changing getter identity.

All outgoing dependencies are explicit **no-effect stubs**, with RAX/RCX/RDX
clobbered on return. The script records consumed arguments and interleaved original
memory writes; it does not execute native accumulator reset/set, field transition,
substructure cleanup, common normalization or PRNG initialization. The PE import
lookup independently resolves IAT `008C3060` to
`api-ms-win-crt-time-l1-1-0.dll!_time64`; the clock call receives null RCX and returns
a controlled 64-bit value. It does not consult the host clock.

Exact [disassembly](evidence/EXP-056-save-normalize-roundtrip/disassembly.txt),
[results](evidence/EXP-056-save-normalize-roundtrip/result.json), original bytes
and [manifest](evidence/EXP-056-save-normalize-roundtrip/manifest.json) preserve
instrument identity, inputs, expected/observed events and instruction visits.

## Local path and byte contracts

Only mode AL is compared. Mode `0x103` therefore follows the same path as 3.
Only bit 0 of save byte `+0x57` selects whether a stash exists.

| Mode AL | Flag bit 0 | Path |
|---|---|---|
| 3 | 0 | stash |
| 3 | 1 | neither |
| other | 0 | neither |
| other | 1 | restore |

Stash copies qword `+0x10` to `+0x70`, word `+0x18` to `+0x78`, bytes `+0x1A/+0x1B`
to `+0x7A/+0x7B`, then stores controlled `00320D50()` EAX in dword `+0x7C`.
Five dwords `+0x1244..+0x1254` copy to `+0x80..+0x90`. It then clears dword
`+0x1248`, clears bit 0 of battle-block dword `+0x5B04`, zeros save qword `+0x10`
and **dword** `+0x18` (including bytes `+0x1A/+0x1B`), calls `00322200()`, zeros
save dword `+0x0C`, and calls `00314DC0(0x483)`.

Restore copies the qword, word and two bytes back; dword `+0x0C` receives stash
`+0x7C`, and `00329E40(stash7C)` is called. The five dwords copy back to
`+0x1244..+0x1254`, followed by `00269A20(save+0xE240)`, clearing bit 0 of save
byte `+0x57`, and `002EF410(save+0x4E660)`. Dword global `01E0C3EC` becomes zero,
battle-block dword `+0x5B04` loses bit 0, and `0023A390(0)` is called. Flag patterns
`A4/A5` demonstrate that other flag bits survive the local clear.

All paths then call `00316810()`, call the controlled time import, calculate the
seed, restore saved registers/stack and tail-jump to `00379CF0(seedECX)`.

## Roundtrip and flag boundary

The original stash branch contains **no direct write setting save flag bit 0**.
With no-effect native dependencies, changing mode from 3 to 0 after stashing does
not restore anything. A second control uses the same resulting save and battle
buffers but explicitly sets flag `A4 -> A5` between invocations. The original
restore branch then restores the twelve bytes at `+0x10..+0x1B` and all five
payload dwords. Dword `+0x0C` becomes the controlled accumulator result
`FEDCBA98`, not its initial value. The stash bytes themselves remain present.

This is a conditional roundtrip of selected bytes, not an identity transform of
the save or battle block. The intervening flag set is a labeled intervention;
native callees may establish it during normal operation. The experiment neither
identifies its native writer nor proves a missing flag in the game.

## Exact seed expression

Let `t` be the time return bit pattern, `timer` the dword at `01FD4A80`, and `u32`
mean reduction modulo 2^32. The local instructions produce:

```text
time_term = u32(33 * u32(t + 0x2B5A5) + (t >> 32)) & 0x7FFFFFFF
seed      = u32(time_term + 0x258 * timer)
```

The original uses a 64-bit arithmetic right shift for the high word, whose low
32 bits match the expression above. Crucially, `BTR ECX,31` at `005843BE` precedes
`ADD ECX,EAX` at `005843C2`. The final seed is **not guaranteed below 0x80000000**.
The high-timer fixture distinguishes this from masking the completed sum.

The private mutant swaps those two operations while preserving their six-byte
extent. It reaches the same tail boundary with identical memory effects but
produces the wrongly masked seed, and the expected event comparison rejects it.
Time controls include zero, all-one bits and `8000000000000000`; timer controls
include zero, one, `00400000` and `FFFFFFFF`. These are arithmetic controls, not
claims about reachable wall-clock times or native timer range.

## Validation and integration limits

Six mode/flag cases, three additional time/timer cases and three carried-buffer
invocations passed on the first execution. Every invocation checks full save,
battle and global regions, exact call/write order and arguments, expected seed,
tail destination, unchanged caller return address, original RSP, and restored
RBX/RSI/RDI. The mutant is a behavioral failure with successful execution, not an
invalid or incomplete run.

FABLE should clarify seed-mask placement on the normalization page and retain the
native flag-writer boundary. OPUS should preserve exact copy/reset widths and the
conditional nature of the roundtrip. No live save/load transition, native callee
effects, PRNG sequence, field-483 meaning or complete persistence contract is
promoted by this isolated execution.
