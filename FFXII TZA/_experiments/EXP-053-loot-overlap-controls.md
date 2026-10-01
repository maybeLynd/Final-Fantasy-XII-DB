---
experiment: EXP-053
title: overlap pickup order, strict radius and geometry precondition
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies overlap pickup search 002FB150; geometry and selection evidence remain on the loot page.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Six original bodies with synthetic geometry and presence; sqrtf surrogate and cookie checker are controlled.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-053-loot-overlap-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-053: overlap pickup order, strict radius and geometry precondition

**Result:** eleven isolated original-code controls passed; a radius-equality
mutation was detected. ASTRA, 2026-09-11. This supplies the overlap half of CM-5,
alongside [EXP-052](EXP-052-loot-pickup-selection.md)'s nearest-position evidence.
No game process was accessed. Collection and inventory effects are not executed.

## Question and method

The [loot page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md)
lists `002FB150` as unread. The question is whether it chooses the closest pickup
or the first overlap, what constitutes overlap, and what its actor input requires.

[check.py](evidence/EXP-053-loot-overlap-controls/check.py) verifies the certified
EXE hash, extracts and executes these six original bodies in fresh Unicorn memory:

| Body | Bytes | Role |
|---|---:|---|
| `002FB150` | 253 | complete search, including the success branch after the RET |
| `00265020` | 61 | actor position getter |
| `00265090` | 27 | class-gated pair getter |
| `003DA710` | 21 | pair copy leaf |
| `004686D0` | 35 | squared XZ calculation, then tail to sqrt import thunk |
| `00861F14` | 6 | IAT thunk |

The PE import table identifies IAT `008C2BB8` as
`api-ms-win-crt-math-l1-1-0.dll!sqrtf`. The fixture routes that IAT slot to an
explicit **controlled surrogate**: Python square root rounded to binary32.
Inputs used here are exact nonnegative integer squares. This does not validate
native CRT edge cases, floating-point exception handling, or general rounding parity.
The other controlled dependency is security-cookie check `00808C40`; it verifies
the cookie argument and returns while preserving EAX. All actor geometry getters,
distance arithmetic before sqrt, search instructions and return paths are original.

Exact bodies, [disassembly](evidence/EXP-053-loot-overlap-controls/disassembly.txt),
[results](evidence/EXP-053-loot-overlap-controls/result.json) and source hashes are
retained in the [manifest](evidence/EXP-053-loot-overlap-controls/manifest.json).

## Local contract

RCX is the unit input, XMM1 the extra-radius float. Null unit returns `FFFFFFFF`.
Otherwise it gets the actor from unit `+0x10`, obtains position through `00265020`,
and obtains the radius pair through `00265090` into two stack words.

The search scans presence slots **0 through 9 in index order**, at
`022BE7F0 + slot*0x20`. A zero first byte skips the slot; any nonzero byte admits it.
Candidate XYZ starts at presence entry `+0x10`. For each admitted slot, the original
code compares the XZ distance against `max(radius0,radius1) + extraRadius`.
Success requires the radius sum to be **strictly greater** than distance; equality
does not qualify. The first success returns immediately. No success returns -1.
The code does not compare candidate distances to find the nearest slot.

### Class-3 geometry is a precondition of initialized radius outputs

`00265020` supplies position for actor class 1 or 3, using actor `+0xB8` as the
movement pointer. However, `00265090` only writes the radius pair for class 3
(`actor[3] & E0h == 60h`), tail-calling `003DA710` on movement `+0x50`.
For another class it returns without writing either output. The search itself
does not initialize those two stack words before calling the getter.

Two class-1 fixtures keep actor position and pickup unchanged but prefill scratch
with different bytes. Zero scratch yields no match at distance 1; `40h` scratch
makes both floats `40404040h` and yields a match. This proves the local dependence
on unwritten outputs when the class-3 contract is violated. It does **not** prove
that a live caller supplies a class-1 actor, nor that the game has a reachable bug.
The native getter also dereferences the actor before a null test; this package's
nonnull-unit fixtures all supply a valid actor and movement pointer.

## Controls and falsification

| Case | Original result |
|---|---|
| Null unit | -1; no geometry calls or presence scan |
| No present slots | -1 after indices 0–9 |
| Slot 1 at distance 2, slot 2 at distance 0, radius 3 | slot 1; slot 2 is not evaluated |
| Only slot 9 present within radius | slot 9 |
| Distance 3, radius 3 | excluded |
| Same point with extra radius 1 | included |
| Radius pair 4,2 at distance 3 | included; larger first component used |
| Large vertical separation at XZ distance 2 | included |
| Inactive slot 0, presence byte 80h at slot 1 | slot 1 |
| Class 1, zero stack scratch | no match |
| Same class-1 inputs, 40h stack scratch | match from unwritten radius data |

The harness checks the complete index scan, geometry call identities/order and
actor/position arguments, return sentinel and stack, saved RBX/RSI/RDI/XMM6/XMM7,
all non-code fixture pages, and absence of non-stack writes. Raw results include
each sqrt input/output bit pattern and the full instruction trace.

A private mutation changes `JA` to `JAE` at `002FB20C`. The equality fixture
incorrectly returns slot 0 and is rejected. The original code and recorded
expected result are unchanged. The complete run passed on its first execution.

## Integration and remaining scope

Together with EXP-052, this separates nearest linked-list selection from first
overlap by presence index. FABLE can integrate the selection mechanics into CM-5;
OPUS can record the geometry/output preconditions. Live caller-class reachability,
presence publication/lifetime, collection and inventory grants remain outside
these isolated controls. The synthetic registry and stack do not establish their
native producers or scheduling.
