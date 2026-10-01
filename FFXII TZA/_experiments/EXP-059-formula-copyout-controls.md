---
experiment: EXP-059
title: numeric scratch copy-out, absence flags and absolute overrides
status: COMPLETE - bounded isolated original-code evidence
contract: none - Numeric scratch copy-out is outside the preparation-step family contract for calculator slots 60-79; no preparation member executes.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original numeric copy-out segment with injected result pointer and fallback; no stubs, earlier resolver and later result work omitted.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-059-formula-copyout-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-059: numeric scratch copy-out, absence flags and absolute overrides

**Result:** thirteen isolated original-segment controls passed; a zero-as-absent
mutant was detected. ASTRA, 2026-09-11. No game process was accessed.

## Question and boundaries

The [scratch page](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md)
and [result page](../07-Combat-Action/Result-Record/the-result-record-field-map.md)
map the numeric words and result flag A. This experiment tests how absent inputs
become flags and output numbers, the subtraction direction, absolute override
precedence, and the destruction of the input sentinel during copy-out. These
are local contracts needed to interpret a later event-anchored live capture.

[check.py](evidence/EXP-059-formula-copyout-controls/check.py) verifies the certified
EXE hash and executes the original 642-byte segment `0038643F..003866C0` inside
`00385F60`. RBX is an injected result pointer, scratch globals hold synthetic
values, and stack dword `RSP+0x38` is an explicit fallback input. Execution stops
at `003866C1`, before failure-kind handling, status classification, later field
copies and native callees. No dependencies are stubbed because none are called
inside this segment. Earlier resolver gates and calculator slots are not executed.

The [results](evidence/EXP-059-formula-copyout-controls/result.json) preserve initial
scratch bytes, per-case overrides, final scratch/result bytes, original and expected
write sequences, and instruction visits. Original bytes and
[disassembly](evidence/EXP-059-formula-copyout-controls/disassembly.txt) are sealed
with the executed source in the
[manifest](evidence/EXP-059-formula-copyout-controls/manifest.json).

## Four numeric groups

Every input below is read as a dword. The helper notation `N(x)` means zero when
`x == FFFFFFFF`, otherwise the unchanged dword bit pattern.

| Result | Subtracted input | Added input | Absolute override | Final width |
|---|---|---|---|---|
| target HP `+0x24` | `02AEE004` | `02AEE008` | `02AEE02C` | dword |
| source HP `+0x20` | `02AEE014` | `02AEE018` | `02AEE024` | dword |
| target MP `+0x2A` | `02AEE00C` | `02AEE010` | `02AEE030` | word |
| source MP `+0x28` | `02AEE01C` | `02AEE020` | `02AEE028` | word |

The initial output is `N(added) - N(subtracted)`, reduced to the result width.
The target-HP fixture `100 / 25` therefore produces dword `FFFFFFB5` (-75), while
the source-HP fixture `10 / 35` produces 25. MP subtraction and stores keep only
the low 16 bits; high-word inputs are neither rejected nor saturated here.

Only exact `FFFFFFFF` is absent. Explicit zero and `FFFFFFFE` both count as present.
An absolute input other than `FFFFFFFF` replaces the computed difference, even
when it is zero or has its high bit set. Tests combine all four overrides with
nonzero differences and check their exact dword/word truncation.

## Flag A construction before normalization

The segment ORs these masks into result dword `+0x2C`, using the **original**
pre-normalized inputs. It preserves existing flags unless an absolute override
explicitly clears a bit later.

| Group | Any of three inputs present | Added input present | Either difference input present |
|---|---:|---:|---:|
| target HP | bit 8 | bit 10 | bit 6 |
| source HP | bit 7 | bit 9 | bit 5 |
| target MP | bit 14 | bit 16 | bit 12 |
| source MP | bit 13 | bit 15 | bit 11 |

Target-MP bit 12 is also ORed when dword `02AEE000` is nonzero, even if both
MP difference inputs are absent. In this segment, bit 18 is ORed when target-HP
**subtracted input `02AEE004`** is present, or any of the four modifier dwords
`02AEE034..02AEE040` is present. A target added-input-only or source-HP-only fixture
does not independently set bit 18 here. The current result-page shorthand
"any HP or stat-modifier word" needs that narrower local qualification. Later
status processing may also set bit 18 and is outside this segment.

For each present absolute override, the original overwrites the numeric result
and updates flag A as follows:

| Override | Set absolute bit | Clear difference bit |
|---|---:|---:|
| target HP | 3 | 6 |
| source HP | 1 | 5 |
| target MP | 4 | 12 |
| source MP | 2 | 11 |

The earlier presence and added-input bits remain. An all-absent fixture starting
with `FFFFFFFF` flags retains them: this fragment does not independently reset
flag A or make an already-used record fresh.

## Scratch mutations and additional byte output

After flags are determined, the original writes `N(x)` back to each of the eight
difference-input scratch dwords. An originally absent value is now zero. The four
absolute inputs and modifier inputs remain unchanged within this segment.

The two private dwords also normalize: `02AEDFFC == FFFFFFFF` becomes zero;
`02AEDFF8 == FFFFFFFF` becomes the injected stack fallback from `RSP+0x38`.
Result byte `+0x1D` receives low8(normalized `02AEDFFC` minus normalized `02AEDFF8`).
The fallback and wrap controls establish that arithmetic without assigning an
upstream semantic meaning to either private word or the stack value.

A scratch snapshot after these writes cannot recover whether a zero difference
input originally meant absent or explicit zero. The result presence flags retain
that distinction. This is a timing/interpretation consequence of the local write
sequence, not a live observation of when previews or resolutions execute.

## Controls and integration

Cases cover all absent, zero present, negative-two present, both HP pairs, MP word
wrap, mixed absolute overrides, absolute-only zero, forced target-MP flag, zero
modifier, private fallback, private byte wrap, and pre-existing flags. Every case
compares the exact original write sequence and complete surrounding scratch/result
pages; RSP and RBX remain at the injected values and the expected stop is reached.
Other registers are working registers inside the parent function, so this segment
is not presented as a complete callable ABI or full resolver return.

The private mutant changes the added target-HP sentinel comparison at `003864A4`
from `-1` to zero. It runs to the same stop but omits the bit-10 write for an
explicit zero. Exact event/memory comparison rejects it. All controls passed on
first execution.

FABLE/OPUS receive the precise flags, widths, subtraction direction and destructive
sentinel normalization. The experiment does not determine which authored recipe
produces a particular input, execute the pre-copy suppression branch, apply HP/MP
to a unit, or establish a whole-resolution/native parity claim. Future live work
must associate scratch and result with source, target and effective action identity.
