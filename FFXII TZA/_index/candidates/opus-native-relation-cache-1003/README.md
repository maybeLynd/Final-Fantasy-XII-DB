# The relation cache consumed: owner block, slot pool, counters, and EXP-091's stub limit (OPUS, 2026-10-03)

*On ASTRA-REQ-OPUS-UQ147-NATIVE-RELATION-CONSUMPTION-1003. ASTRA's `uq147-native-relation-invariant` (`86cdcde10`) was
ACCEPTED by SWE2-AUDIT-SPEC (`auditspec-review-astra-uq147-native-relation-invariant-1003`, `b9502c733`). ASTRA's README
says OPUS owns the cache type, ABI and contract preconditions and the EXP-091 stub-limit wording, and FABLE owns the
semantic UQ-147 framing. OPUS re-read every cited site in `00512F30` / `00512CD0` / `00512EE0` at the bytes: 96 code
addresses, all instruction starts.*

Three appliers, each idempotent ([`.out`](apply_recuts.out) files beside them):
- [`apply_recuts.py`](apply_recuts.py) re-cuts CharacterRenderRecord `+0x650..+0x65F`;
- [`apply_decls.py`](apply_decls.py) declares the pool and the counters;
- [`apply_exp091_note.py`](apply_exp091_note.py) adds one sentence to EXP-091.

## The owner block, CharacterRenderRecord +0x650 (OPUS)

The 16-byte object at `+0x650` is the relation owner block that `00512F30` receives in rcx.
- **`+0x650` / `+0x654` / `+0x658`** replace the 12-byte placeholder `embeddedBlock0650`. They hold one inline
  relation's recipient, actor and target UIDs, which the kind-1 (`00513120..0051313A`) and kind-3
  (`005130D9..005130F3`) arms store.
- **`+0x65C` / `+0x65D` / `+0x65E`** are the head, tail and count of a linked list of slots in the pool. 0xFF means
  empty. The count is decremented with no occupancy test.
- **The low nibble of `+0x65F`** is the inline relation's kind: 3 or 1, and 0 when cleared.

The four existing rows keep their names, because two of them record "Name is FABLE's". Each gains the representation
clause, and the rename is routed to FABLE.

## The pool and counters (OPUS)

- **RelationCacheSlot** (0x10): recipient, actor and target UIDs, then its own index, previous and next indices, and a
  kind nibble.
- **RelationCachePool02CA81F0** (0x201): `RelationCacheSlot[32]` plus the allocation cursor at `02CA83F0`. The
  allocator scans from the cursor, wraps once to slot 0, and gives up when both scans fail.
- **RelationCacheCounters02EBA480** (0x2): the live count at `+1` (incremented at allocation, decremented
  unconditionally on removal) and its unsigned high-water mark at `+0`.

## What is not claimed (OPUS, ASTRA's limits preserved)

These stay open, as ASTRA's limits say:
- live defaults, cache binding, lifetime and reuse, other callers and packet kinds, outside writers to the counters,
  corrupted-list termination, and the natural reachability of the broken-premise witness;
- what the UIDs identify in play, and the full UQ-147 question (FABLE's);
- natural summoner KO / Esper 113, action 714, and timing.

A removed slot's UIDs and links are not cleared. The `00513027` store can update an inactive slot, which is not heap
memory. The double-removal exclusion holds only for coherent packets with live target != recipient; a malformed state
can remove twice and wrap both counts.

## EXP-091 (OPUS)

EXP-091 stubbed `0x512F30` and never executed it. Its stubbed-entries bullet now says that the body's local effects
are established separately by this Method A result. That result is not one of EXP-091's Method B samples, and no case
changes.
