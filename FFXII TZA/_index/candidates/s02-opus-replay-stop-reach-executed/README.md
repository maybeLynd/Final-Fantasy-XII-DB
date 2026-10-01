# S-02: SS-7's reach executed for all 28 stop slots, with the manager loop (OPUS, 2026-09-25, block 331)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-02's binding gap names three closers: *"`0026A5F0`
run real, SS-7's per-request reach bit isolated, or one live frame"*. Block 287 ran `0026A5F0` real and measured
SS-7's reach, but with three gaps:
- only 23 of 28 ids (ids 0, 12, 13, 15 and 17 faulted through null globals);
- the breadth arithmetic `00226C77..00226C94` was **re-computed by the check**, not executed;
- `00226BE0`'s per-manager loop never ran.

This harness closes all three.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 330. For each slot 0..27 it makes the
prelude's own call, `00226BE0(slot, 0, 0, 0, −1, −1)` as at `0025479D`. That call runs to its return: the record
build `00227680`, the breadth computation, and the per-manager loop through `00263FF0`. **No application stub and no
stop boundary.**

**Three idle objects** are planted as zeroed blocks, the convention of the world's nine:

| cell | why it is needed |
|---|---|
| `[0209BE80]` | the HUD object |
| `[01F7FFE0]` | `00198790`'s object. The record build flags it for ids 12, 13, 15 and 17 through `00182CD0` / `00182CF0`: **this was block 287's fault at `0x3A`** |
| `[0215E6E0]` | the flag word `002DDC30` reads for slot 0. Its bit 3 is run both clear and set |

Each run first clears the slot's bit in the active bitset `01FD46D4`, because `00226C08` skips an already-active
slot.

**2 / 2 pass, and `result.json` is byte-identical over three runs** (md5 `927ce0d68f627c5d63054efc252c3311`).

| case | contract item | observed |
|---|---|---|
| `SS7_reach_executed_all_28_slots` | SS-7 | For **every slot 0..27**, `00226BE0` returns. The breadth is **the value the code computes at `00226C94`**, and equals `(~(A >> 30) & 2) \| 1` of the record the code itself built. The loop asks `00263FF0` for managers `0..breadth−1` exactly. **Only slot 11 reaches 3 managers**; the other 27 reach 1. The slot's active bit is set afterwards |
| `slot0_record_depends_on_flag_bit3` | — | Slot 0's record A is `00000034D4000000` with bit 3 of the flag word clear or set. The flag does not change it |

The five slots block 287 could not measure:

| slot | record A | reach | managers walked |
|---|---|---|---|
| 0 | `00000034D4000000` | 1 | `[0]` |
| 12 | `00000024DD001F01` | 1 | `[0]` |
| 13 | `FFFFFFFFD5FFE0FF` | 1 | `[0]` |
| 15 | `00000034D4000000` | 1 | `[0]` |
| 17 | `FFFFFFFFFFFCFFFF` | 1 | `[0]` |

The other 23 slots reproduce block 287's records.

## What the execution adds

1. **SS-7 is executed end to end for all 28 request slots.** The per-request breadth is built by `00227680`,
   computed by `00226C77..00226C94`, and consumed by the manager loop. The reach table is now complete: **slot 11
   alone reaches 3 managers.** This is the "SS-7 per-request reach bit isolated" closer S-02's gap names.
2. **Block 287's five faults were the unbuilt `01F7FFE0` object,** found in block 327, not a property of those ids.

## Not covered

- the per-actor effects inside the loop (the built world's managers hold no actors);
- the apply `00226280` and cancel for these slots (SS-1..SS-6 are EXP-191's and block 287's);
- a live frame.
