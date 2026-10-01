# S-20: the battle-action handler-table dispatch executed over every id (OPUS, 2026-09-25, block 350)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-battle-action-handler-table.md`](../../../07-Combat-Action/CONTRACT-battle-action-handler-table.md) §13 reads
*"None. No experiment executes this dispatch."* This harness runs the dispatcher
`BattleUnit_AdvanceExtendedActionState` (`00305080`) against HT-1..HT-6:
- over **all 359 ids** of the table `01EEC460`;
- past both ends: `0x3FFF`, `0x4167`, `0xFFFF` and 0.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 347. **No application
stub.**

**Stop boundaries (recorded, never stubbed):** the entry of each of the eight handlers.
- The contract's subject ends at the dispatcher's `jmp rdx`, and the handlers' bodies belong to other contracts.
- At each stop, the entry and `rcx` are recorded.

**Fixtures:**
- six idle objects at `0x76300000`;
- the unit: `+0x10` a zeroed handle object, `+0x698` battle-state row 0 (`+4` type, `+5` kind), `+0x714` the order id;
- the battle-state block's `+0x5AE0` bit 1, where a case sets it.

**4 / 4 pass, and `result.json` is byte-identical over three runs** (md5 `15a8462043a752ed8dc10fad00bb6418`).

| case | contract item | observed |
|---|---|---|
| `HT1_HT2_table_shape` | HT-1, HT-2 | See the table-shape list below |
| `HT3_HT5_tail_call_and_minus_one` | HT-3, HT-5 | See the dispatch list below |
| `HT6_event_before_dispatch` | HT-6 | See the HT-6 list below |
| `HT4_one_table_one_bound` | HT-4 | **Static only:** the dispatcher (`003050E1`) and the availability check (`003018F0`) both resolve `01EEC460`, and both bound at `0x166` (`003050D8`, `003018E3`). The availability body is not executed |

**The table's shape (HT-1, HT-2).**
- 359 slots, 341 non-null, **8 distinct handlers**: `002FDDA0` ×249, `002FDA60` ×57, `002FDC30` ×25, `002FE660` ×6, and
  `002FE7D0` / `002FE840` / `002FE8D0` / `002FE910` ×1 each.
- The qword past the bound is `0000000400000002`.

**The dispatch (HT-3, HT-5).**
- Every non-empty id stops at **exactly** `table[id − 0x4000]`, with `rcx` = the unit and nothing else passed.
- The 18 empty slots and the four out-of-range ids return **−1** from the dispatcher itself.

**HT-6, the event.**
- `003299B0` posts **before** the tail-call.
- It posts `0x2010` only for a party record (kind 0) of type `0x1A` when bit 1 of the block's `+0x5AE0` is set, and
  `0x2001` otherwise (bit clear, type `0x19`, or kind 1).
- The posted event lands in unit `+0x5C`.

## What the execution adds

- **HT-1 to HT-3, HT-5 and HT-6 hold as stated,** now executed over the whole id space.
- **HT-2 has a distribution the contract did not tabulate.** It said "then 25 and 6, with four further handlers on the
  remaining slots". Those four serve **one id each**.
- **The event's destination is named.** `003299B0` stores the event in unit `+0x5C` and forwards it through
  `002EB030(q[unit+0x10], event)`.

Routed to FABLE (§13 can cite this block).

## Not covered

- the handler bodies;
- the availability body `00301830` (HT-4 is checked from the instructions only);
- a live game.
