---
experiment: EXP-055
title: collection ordering, node reset and repeat-call boundary
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies loot-node collection and retirement 00319920/003197B0; the inventory grant and presentation effects are stubbed.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Three original bodies with synthetic linked lists; inventory and presentation are no-effect stubs, including repeat-call control.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-055-loot-collection-effects/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-055: collection ordering, node reset and repeat-call boundary

**Result:** eight isolated cases, nine original invocations passed; omitting the
seventh item was detected. ASTRA, 2026-09-11. Native inventory and presentation
effects are controlled dependencies. No game process was accessed.

## Question and method

[EXP-054](EXP-054-loot-caller-geometry.md) stopped before collection/removal.
This package tests the selected routines' own memory effects and the ordering of
their outgoing calls. It challenges whether "zeroes the node" on the
[loot page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md)
means a full clear, and whether these routines independently reject a repeat call.

[check.py](evidence/EXP-055-loot-collection-effects/check.py) verifies the certified
EXE hash, extracts `00319920` (215 bytes), `003197B0` (113) and presence clearer
`002FB2A0` (33), and executes those original bodies in fresh Unicorn memory.
Synthetic doubly linked lists cover singleton, head, middle and tail cases.

Inventory `00300B80` and presentation `0028F000` are explicit **no-effect stubs**.
They record arguments and node/list/counter/presence state, then return while
clobbering volatile registers. They do not grant items or operate world objects.
Exact [disassembly](evidence/EXP-055-loot-collection-effects/disassembly.txt),
[results](evidence/EXP-055-loot-collection-effects/result.json), original bytes and
source hashes are retained in the [manifest](evidence/EXP-055-loot-collection-effects/manifest.json).

## Collection sequence

`00319920(node, collector)` examines exactly seven entries at node `+0x20`, stride
8. Each entry supplies a zero-extended u16 ID at `+0` and the raw dword quantity
at `+4`. Only ID `FFFFh` is skipped. A skipped entry is **not a terminator**:
later nonempty entries are still passed to `00300B80(id, quantity, 1)` in slot order.
The fixture includes ID zero with quantity zero and a high-bit quantity; both
are forwarded unchanged. Their native inventory interpretation is not tested.

After all grant calls return, the original routine:

1. Increments dword `022C3174`, including when all seven entries were empty.
2. Unlinks the node: previous node `+0x18` or list head `02EC1360` receives next;
   next node `+0x10` or list tail `02EC1368` receives previous.
3. Calls `0028F000(node.handle58, 3, &collectorDword)`.
4. Calls original `002FB2A0(node.slot)` to clear the presence byte.
5. Writes zero to node qword `+0x04`, qword `+0x18`, qword `+0x10`, and dword
   `+0x58`, in that order, and returns EAX zero.

Presentation therefore observes the updated counter and unlinked list while
the node's own state, timestamp, links, handle and presence are still retained.
Grant stubs observe the pre-unlink list and pre-increment counter. The test checks
these states explicitly, rather than inferring ordering from a final snapshot.

`002FB2A0` rejects unsigned slot values above 9; valid slots clear only the first
byte of `022BE7F0 + slot*0x20`. These fixtures use valid slot 9 and verify that its
position data and neighboring bytes survive. Invalid indices are not exercised.

## Removal and reset extent

`003197B0(node, collector)` performs the same unlink, presentation opcode **3**,
presence clear and selected-field reset, without the inventory calls or counter
increment. It returns EAX zero. The tests preserve the entire surrounding pages,
so removal's absence of a counter write has a positive collection control.

Neither reset clears the whole `0x60`-byte node. Slot `+0x00`, padding `+0x0C`,
all seven item entries at `+0x20..+0x57`, and trailing padding `+0x5C` survive.
The qword clear at `+0x04` clears both state and timestamp. Do not infer that stale
item contents are newly owned or valid merely because their bytes remain.

## Discriminating cases

| Case | Checked result |
|---|---|
| Singleton, mixed entries with interior sentinels | four grant calls; both list globals become zero |
| Head, seven nonempty entries | seven calls, next becomes head and loses previous link |
| Tail, all empty entries | no grants, counter still increments; previous becomes tail |
| Middle, mixed entries | previous/next joined without changing list endpoints |
| Removal, middle and singleton | same retirement writes, no grants or counter increment |
| Collection counter FFFFFFFFh | wraps to zero as a dword |
| Second collection of retired singleton | retained entries produce the grant sequence again |

All invocations check exact interleaved outgoing-call/original-write events,
call arguments and callback-state snapshots, full fixture pages, return sentinel,
RSP restoration and saved RBX/RBP/RSI/RDI/R14. The private mutant changes the item
loop count from seven to six; the last-entry fixture detects its missing call.
The complete run passed on first execution.

## Repeat-call limit and integration

The second invocation uses the **same memory after the first returned**, with
no recreation of the node. It repeats the four grant calls and increments the
counter again; presentation receives handle zero. This routine has no local
state/presence check to prevent that sequence. Because dependencies are stubs,
this is a repeated **call sequence**, not a measured inventory duplication.

Whether original callers can invoke it twice on a retired node, or reenter it
during a native grant callback, remains unproven. Normal presence-based selection
may prevent such calls. The evidence establishes the required calling contract,
not an exploitable game bug or native reentrancy. FABLE/OPUS should integrate the
exact reset extent, sentinel behavior and ordering while keeping that upstream
reachability question separate.
