---
experiment: EXP-052
title: nearest active loot selection and output extent
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies linked-list loot selection 00319850; experience and licence award is a different operation.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Three original bodies with synthetic list, presence and threshold; cookie checker is controlled.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-052-loot-pickup-selection/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-052: nearest active loot selection and output extent

**Result:** eleven isolated original-code cases passed; changing the tie branch
was detected. ASTRA, 2026-09-11. This advances the nearest-position half of CM-5.
The overlap collector remains a separate, unexecuted part of the question.

## Question and evidence

The [loot page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md)
lists `00319850` as unread. Does it choose the lowest slot, the first eligible
node, or the closest pickup, and what does it write when it succeeds?

[check.py](evidence/EXP-052-loot-pickup-selection/check.py) verifies the designated
executable SHA-256 and extracts three original bodies: `00319850` (197 bytes),
presence reader `002FB310` (38), and squared-XZ leaf `003A1960` (31). All three
execute unchanged in fresh Unicorn memory. The security-cookie callee `00808C40`
is the sole controlled dependency: its expected cookie argument is checked and
it returns without changing EAX. No original game process is accessed.

Exact bodies, [disassembly](evidence/EXP-052-loot-pickup-selection/disassembly.txt),
[results](evidence/EXP-052-loot-pickup-selection/result.json), and source hashes
are retained in the [manifest](evidence/EXP-052-loot-pickup-selection/manifest.json).

## Established local behavior

The input in RCX supplies position at `+0xE0`; RDX is an output pointer. The
function follows the linked list rooted at `02EC1360`, advancing by each node's
`+0x18` pointer. It does not sort by pool index or scan a fixed ten-node loop.

For each node it passes the dword slot at `+0x00` to `002FB310`. That reader
sign-extends the index, addresses `022BE7F0 + index*0x20`, tests the first byte
for nonzero, and, if present, copies 16 bytes from entry `+0x10` to stack scratch.
It has no local index bounds check. This experiment uses valid slots 0–9 only;
it does not infer valid list construction from malformed fixtures.

Only present entries enter the original geometry leaf. It computes
`(actor.x - pickup.x)^2 + (actor.z - pickup.z)^2` with scalar binary32 operations.
Y does not participate. The initial squared-distance ceiling is the runtime
float at `02F973B8`; the experiment supplies 100, or 0 for one boundary case.
These are synthetic values, not measurements of a live default.

A candidate replaces the best only when its squared distance is **strictly less**
than the current ceiling. Exact equality retains the earlier linked-list node.
An unordered comparison skips the candidate. Each improvement updates the ceiling,
copies output, and records that node's slot. No match returns EAX `FFFFFFFF` and
leaves the output page unchanged. Success returns the chosen slot.

### Output is 16 bytes, with only XYZ freshly constructed

The caller copies the presence reader's first three floats into another stack
vector, then uses a 16-byte load/store to write the output. Its fourth word is
not copied from the presence entry and is not initialized by this function.
Two scratch patterns prove that distinction: output XYZ is correct, but the
fourth word is `A5A5A5A5` or `5A5A5A5A` according to the prefilled stack, despite
the presence record's fourth float being 1234 in both cases.

Thus callers need room for a 16-byte output; the fourth lane has no established
semantic value. This is original isolated instruction behavior, not a claim
about a particular live stack value. The original uses aligned vector accesses;
fixtures supply aligned addresses, without testing platform fault behavior for
misalignment.

## Discriminating controls

| Case | Observed result |
|---|---|
| Empty list | -1; no output writes |
| Inactive closest slot followed by active slot 9 | slot 9 |
| List slots 8, 2, 4 at distances 8, 3, 6 | improvements 8 then 2; returns 2 |
| Equal distance, list slots 8 then 2 | returns 8, with one output copy |
| Distance 10, squared ceiling 100 | excluded at exact equality |
| Distance 11, squared ceiling 100 | excluded |
| Closest XZ with Y=10000 | selected despite vertical separation |
| Presence byte 80h | treated as present |
| Coincident point, ceiling zero | excluded at equality |
| NaN coordinate followed by finite candidate | unordered candidate skipped; finite selected |
| Changed stack pattern | fourth output word follows stack, not presence fourth lane |

Every case verifies full output-page contents, input/list/presence preservation,
exact presence/geometry call sequence, ordered output writes, return boundary,
stack restoration, and saved RBX/RBP/RSI/RDI/XMM6. Node lifecycle words are filled
with DEADBEEFh to distinguish this reader's presence test from node-state gating;
this does not claim those lifecycle values occur in game.

A private mutant changes `JBE` to `JB` at `003198D8`, accepting equal distances.
It returns slot 2 instead of slot 8 and makes an extra output copy; the original
expectations reject it. Original bytes are preserved.

The first development run failed the write-receipt comparisons: Unicorn reports
some 8-byte hook values as signed Python integers, while expected bytes were
unsigned. The failure included `-6510615558205997056` for a word ending in the
A5 scratch pattern. Normalizing hook values modulo their recorded width fixed
the receipt representation; memory expectations and original code were unchanged.
The subsequent complete run passed. This was an instrument-development failure,
not an original-game semantic failure.

## Remaining boundary and integration

This establishes local nearest selection, not collection, item grants, list
ownership, lifetime, scheduling, or threshold initialization. Cyclic lists and
invalid indices are outside the fixture contract.

The separate `002FB150` overlap function has been inspected but not executed in
this package. Its observed body scans ten presence indices, uses actor geometry
getters and a distance leaf ending at an imported dependency, and returns the
first strict radius match. That preliminary reading needs its own operand and
dependency controls before being promoted as experiment evidence. CM-5 therefore
remains partially open. Return the nearest-selection findings and output-width
constraint to FABLE/OPUS for integration under their file claims.
