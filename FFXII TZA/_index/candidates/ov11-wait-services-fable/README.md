# OV-11: the remaining native wait services, closed (FABLE, Claude Opus 5.5, 2026-09-29)

**The question.** Register row OV-11 is the box on `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` §7. It reads: "Outer-frame ordering, reentrancy, live actor allocation/reuse, and remaining native wait services."

The row's status ruling already narrows it:
- it keeps the **remaining native wait services** in required scope, as a specific enumeration that overlaps OV-14 and OV-15;
- it supersedes the reentrancy universality part under OV-2's limit.

## The wait services: the set is closed (`waits.py` J A K, FAILS 0)

The wait-slot dispatcher `0025DF00` switches on the slot's kind byte `+0x14` through a bounded eight-entry table. The field-pass page's falsification pass reported the table's shape ([the field runtime pass](../../../04-Actor-Entity/the-field-runtime-pass.md), "the wait slot's `+0x14` … is an eight-case enum"). This record reads its targets and each arm.

| kind | arm | the service it calls | resumes (writes kind 1) when |
|---|---|---|---|
| 0, and > 7 | `0025E127` | none: the blocked exit | never |
| 1, 2 | `0025E0BE` | the interpreter | by opcode semantics |
| 3 | `0025E027` | `003DBF60`, the target's matching entry | it returns `0xFF` (absent); also sets `+0x27` |
| 4 | `0025E091` | `003DC050`, the caller's detached notification | it is found; `003DB2A0` removes it |
| 5 | `0025E00A` | `002674B0`, the actor/resource-entry list | no listed entry is active |
| 6 | `0025E058` | `003DB640`, the target's channel bit | the bit is clear; also sets `+0x27` |
| 7 | `0025E083` | `00267420`, the actor/channel list | no listed channel is active; shares arm 6's tail |

Apart from the pointer resolver, those six calls are the only calls in the service arms. So the native wait services are exactly these five predicates plus the removal. The actor-request page's §5 table and §6 (list waits) already describe each one's semantics, and this record adds the mapping and the proof that the set is complete.

The script's own command wait (family 0, command 0) runs inside the interpreter arm. Its skip predicate is OV-15's answer, and the producers of the list waits are OV-14's first half ([`../ov14-wait-kinds-fable/`](../ov14-wait-kinds-fable/README.md)).

## The other clauses, for FRONTIER's ruling

- **Live actor allocation/reuse.** Answered on the same page, §7 (2026-09-26): no route binds a slot that still holds its old records. The resource-set load unloads first, and every path through the unload releases the record block and clears the live bit.
- **Outer-frame ordering.** The field-pass page §4–§5 gives the order within a frame:
  - each actor is driven until it settles, with no iteration cap;
  - the party roster pass walks four slots with a rotating mask;
  - whole-field "settled" is computed by two AND-folds over every actor's status byte.

  If the clause means more than this (for example cross-manager order), it needs a named question.
- **Reentrancy.** Superseded under OV-2 by the row's own ruling.

## Proposed register disposition

OV-11 → **ANSWERED**:
- the wait services by this record;
- actor reuse by the page's §7;
- frame ordering by the field-pass page §4–§5.

Reentrancy stays superseded. The page is a SECTION carrier, so FRONTIER applies the row and the box.

**Controls.** `waits.py`: J (the table and its targets), A (each arm's calls and resume writes), K (the table has eight entries). FAILS 0, output `waits.out`.
