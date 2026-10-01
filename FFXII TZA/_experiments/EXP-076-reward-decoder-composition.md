---
experiment: EXP-076
title: Native pointer decoding and reward-row address truncation
status: COMPLETE
contract: ../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md
tool: evidence/EXP-076-reward-decoder-composition/check.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-12
date_run: 2026-09-12
---

# EXP-076 — a zero reference is not necessarily a NULL reward pointer

**Result:** seven new composition controls passed on first execution; a private
zero-sentinel mutation was detected. One subsequent, distinct truncation-to-zero
control also passed on first execution. No earlier controls were replayed. ASTRA,
2026-09-12. Isolated original code with eight remaining callee stubs; no live game.

## Question and original boundary

[EXP-075](EXP-075-reward-index-prechecks.md) distinguishes an early invalid-index
rejection from later missing-descriptor/zero-resolution branches. Its resolver
was explicitly a stub, so its arbitrary return values do not establish native
failure conditions. The existing [EXP-063](EXP-063-mp-cost-controls.md) already
executed the real decoder. This experiment composes those original ten bytes with
the 1,808-byte installer, using new reference/base fixtures.

The decoder `0020E600` is exactly:

```asm
mov eax, ecx
add rax, qword ptr [01F83530]
ret
```

It performs `u64(zeroExtend32(reference) + relocationBase)`. It does not validate
a reference, allocation or address range; zero has no special treatment. This
explains a zero **decoder result** precisely, while leaving actual loaded-state
values and allocation lifetime unobserved.

The installer then narrows the row arithmetic. At `0023A994`–`0023A99F`, it loads
word stride and word index, multiplies in ECX and adds **EAX to ECX**, before the
qword store to unit `+E70`. `0023A9DB`–`0023A9E6` does the same for `+E78`.
For a present descriptor and a nonzero decoded base, the stored pointer is:

```text
zeroExtend32(low32(decodedBase) + u16(index) * u16(stride))
```

Consequently, a nonzero decoded base can still produce a **zero stored pointer**.
The order pointer at `+6E0` instead receives RAX directly at `0023A95E`, retaining
all 64 bits. A reconstruction must preserve these different operation widths.

## Method and controls

The [primary checker](evidence/EXP-076-reward-decoder-composition/check.py) derives
from EXP-075's reviewed fixture and oracle. It verifies the full reference EXE
SHA-256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, image
base `120000`, original body and constant bytes. Decoder SHA-256 is
`8bde921e0db5b4c6b16e649c4df8172da2b8b8c3462664b675b377cf37450f65`, identical to
EXP-063. Both original bodies run from their entries to their returns; the hook
records decoder calls without substituting results or register effects.

The same initialized unit, class, definition, descriptors and preinitialized spawn
record are used. Counts are 2/3, indices 1/2 unless stated, stride `38` hex. Each
case has fresh fixture pages and an explicitly planted qword relocation base;
encoded references target the intended low-address fixtures under the tested
arithmetic. Whole-page before/after checks include that global. EXP-075's return,
stack, full nonvolatile register, native store and exact call/selected-argument
checks remain. Raw records retain instruction traces, non-stack reads/writes,
page hashes and byte deltas. Unicorn 2.1.4 and Capstone 5.0.7.

The other eight EXP-075 callees remain recording, no-write RET stubs. Their native
effects, real reset state, full actor construction and death consequences remain
unproved. Synthetic high/negative bases are boundary inputs, not assertions that
the game loads there. Stored reward/order pointers are not dereferenced here, so
an unmapped computed address can be observed without claiming its usability.

All numbers below are hexadecimal. Every unmutated fixture returned EAX=1 locally.

| New condition | Stored `+E70` | Stored `+E78` | Distinction |
|---|---|---|---|
| Base `10000000`, ordinary encoded references | `40005038` | `40006070` | positive control |
| Same base, base-row reference 0 | `10000038` | `40006070` | zero reference decodes to nonzero base |
| Same base, per-level reference 0 | `40005038` | `10000070` | independent second-row control |
| Base 0, base-row reference 0 | 0 | `40006070` | zero decoded base selects NULL branch |
| Base 0, per-level reference 0 | `40005038` | 0 | same on second row |
| Base `FFFFFFFFFFFFF000`, base-row reference `1000` | 0 | `40006070` | nonzero reference can decode to zero by 64-bit wrapping |
| Base `100000000`, ordinary references | `40005038` | `40006070` | high word lost from reward rows; order pointer is `140007000` |
| **Additional control:** base `100000000`, base-row reference 0, base index 0 | 0 | `40006070` | decoded base is nonzero, two decoder calls occur, then 32-bit arithmetic stores zero |

The [additional checker](evidence/EXP-076-reward-decoder-composition/check-pointer-zero.py)
runs only the final row. Its function/fixture code equals the primary checker's
prefix after line-ending normalization; its separate [result](evidence/EXP-076-reward-decoder-composition/result-pointer-zero.json)
preserves the first run of that control without rewriting or replaying the primary
seven-case record.

The private decoder mutant returns zero when ECX is zero and otherwise performs
the same addition. On base `10000000` and base-row reference 0 it installs NULL
instead of `10000038`. EAX=1, stack, nonvolatile registers and guard/store reachability
still agree; the call sequence and complete memory oracle detect the wrong result.

## Scope of correction

Read this together with EXP-075: index rejection, missing descriptor, zero decoded
base and zero after row arithmetic are distinct conditions. Neither a stubbed
resolver returning zero nor a shipped index census proves which occurs in play.
The existing [ARD loader account](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
already records the native decoder's arithmetic; the new evidence is its composition
with this installer's widths and late branches. Peer propagation to reward contracts,
types and semantic pages remains pending. The [row-lookup contract](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md)
currently withholds a lifetime-zero base claim in §2a, while its later §7 note
asserts it from a writer/address census. This experiment does not adjudicate that
proof disagreement: synthetic nonzero bases establish arithmetic, not live values.
Descriptor/storage lifetime likewise requires its own evidence.

[Primary results](evidence/EXP-076-reward-decoder-composition/result.json),
[complete original disassembly](evidence/EXP-076-reward-decoder-composition/disassembly.txt),
both checkers and binary extracts are sealed in the
[manifest](evidence/EXP-076-reward-decoder-composition/manifest.json).

```powershell
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-076-reward-decoder-composition/check.py'
& '.\Collaboration\Tools\analysis\venv\Scripts\python.exe' 'Database/FFXII TZA/_experiments/evidence/EXP-076-reward-decoder-composition/check-pointer-zero.py'
```
