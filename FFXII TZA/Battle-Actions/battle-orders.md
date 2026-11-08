---
title: "Battle orders: the internal order ids 0x4000-0x4166, their handlers and what each order does"
kind: "reference"
category: "Battle actions"
addresses: "0x01EEC460, 0x00305080, 0x00301830, 0x002FDDA0, 0x002FDA60, 0x002FDC30"
---

## What it lists

A unit's action id `+0x714` holds either an ordinary action (ids up to `0x21E`, which carry a target
list) or an internal **order** (`0x4000`-`0x4166`, no target list). Orders are what AI order lists and
scripts use for moving, waiting, changing statuses and augment bits and adjusting stats; each comes with
a small order record (the action context `+0x708`), whose `i16` at `+0x02` is the order's parameter.
The table lists all 359 order ids with what the game does for each.

### Dispatch

`0x00305080` (called by the action step `0x00307BE0` for an id above `0x21E`) posts
presentation event `0x2001` - or `0x2010` for a party-side unit of type id `0x1A` while bit `0x2` of
`[0x02EBF190]+0x5AE0` is set - then returns -1 when `id - 0x4000` is above `0x166` or the slot of the
table at `0x01EEC460` (359 eight-byte pointers, `0x01EEC460`-`0x01EECF97`) is empty, and otherwise jumps to
the handler with the unit as argument (`0x003050A0`-`0x0030510E`). Handlers keep their progress in the
phase byte `+0x6B4`; one-shot handlers set it to 2 and return 1 at once.

### Availability

`0x00301830(unit, record)` refuses an id outside the table or an empty slot, then applies these
id-specific rules (`0x003018DD`-`0x00301AA5`); every other id passes:

| Ids | Rule |
|---|---|
| `0x4051`-`0x4121` except `0x4091`, and `0x414B` | a non-zero parameter is a percentage: refused when the parameter is not above a draw from the gameplay generator (`0x00328370`) modulo 100 |
| `0x4022`, `0x4124` | must have a reachable movement goal (`0x00312730`, and `0x0033A120` must not report arrival); `0x4022` then stores the goal at `+0x6C0` and `0x00309A90()` at `+0x6D0` |
| `0x4165` | `0x00312730` must find a goal |
| `0x414D` | `0x00308130` (party side) or `0x00308040(unit, 0)`, tested against unit bit `0x800000` |

## Columns

[`battle-orders.tsv`](battle-orders.tsv), one row per order id:

| Column | Meaning |
|---|---|
| `order_id` | the order id, `0x4000`-`0x4166` |
| `handler` | the function in the order table's slot, or `00000000` for an empty slot |
| `operation` | what the handler does for this id |
| `value` | the id-derived value (status number, effect number, bit, index) or where the parameter comes from |
| `name` | for status orders the status name from `battle_pack.bin`'s status-name table; for augment orders the augment's name in the database, the `term` column of the [augment list](../Damage-And-Battle-Formulas/augment-list.md) (its license's name or the modding community's name, not the game's stored name or help text) |

## Data

The ids fall into these groups (full rows in the `.tsv`):

| Ids | Handler | Operation |
|---|---|---|
| `0x4000`-`0x4020`, `0x4022`-`0x4024`, `0x4026`-`0x4035`, `0x4124`-`0x4125`, `0x414A`, `0x414E`, `0x4165` | `0x002FDA60` | move to the goal `0x00312730` derives from the order record; ends when `0x0033A120(movement block, id)` reports it reached. On phase 0 (`+0x6B4`) a goal that `0x00312730` cannot find ends the order with -1; otherwise the stop distance, its third output, goes to the movement block's (unit `+0x80`) `+0xD0`, `0x003291B0` resets the movement with its two points and the phase becomes 1 (`0x002FDAB8`-`0x002FDB03`). On that frame and every later one the block's mode `+0x40` and `+0x160` are zeroed (`0x002FDB14`-`0x002FDB1B`). For `0x4022`, `0x4024`, `0x4026`-`0x4035`, `0x4124`, `0x414A`, `0x414E` and `0x4165` the goal is refreshed every frame through `0x00319110`, from the second frame on, and a refresh that `0x00312730` cannot find ends the order with -1 (`0x002FDB70`-`0x002FDBB6`); `0x4022` and `0x4124` set bit `0x100` of `+0x1F0` while on the way; `0x414E` moves toward the unit at `+0x710`, which it copies to block `+0x150` with mode 2 (`0x002FDB5B`-`0x002FDB68`). For the other ids a failed navigation step (`0x00325BB0(unit, 0)` = 0 before arrival) ends the order with -1; the refreshed ids wait instead (`0x002FDBE4`-`0x002FDBF4`). Arrival sets the phase to 2 and returns 1, and a phase above 1 returns 1 at once (`0x002FDBFE`, `0x002FDAB3`) |
| `0x4021` | `0x002FE7D0` | wait until the counter `+0x75C` reaches `param * (int)(30 * [0x01DFE0B8])`; clears `+0x750`-`+0x757` first; a parameter of 0 never ends |
| `0x4046`, `0x4047` | `0x002FDDA0` | set / clear unit flag bit `0x8000` |
| `0x4048`-`0x404F` | `0x002FDDA0` | set unit byte `+0x54` to 0-7 |
| `0x4050` | `0x002FDDA0` | remove every status (`0x0030E8F0`) |
| `0x4051`-`0x4070` | `0x002FDDA0` | add status 0-31 (`0x0030E360` mode 3) |
| `0x4071`-`0x4090` | `0x002FDDA0` | remove status 0-31 (`0x0030E360` mode 0) |
| `0x4091` | `0x002FDDA0` | clear all 128 augment bits of the layer at stats `+0x68`, then rebuild the stats (`0x0030FED0`) |
| `0x4092`-`0x40D1` | `0x002FDDA0` | set augment 0-63 in the layer at stats `+0x68` (`0x0030E130` mode 2) |
| `0x40D2`-`0x4111` | `0x002FDDA0` | clear augment 0-63 in the layer at stats `+0x68` (`0x0030E130` mode 0) |
| `0x4112`-`0x4115` | `0x002FDDA0` | enemy side: point `+0x6E0` at the entry of the table at `0x02EBF168` named by the `u16` at `[unit+0xE60]+0x50+2k`, and zero `+0x6B5`; a selector at or past the table's count (`u16` at `+0`) refuses the order (-1); any other unit ends at once doing nothing |
| `0x4116`-`0x4121` | `0x002FDDA0` | set unit byte `+0x6B5` to 0-11 |
| `0x4122`, `0x4123`, `0x4149`, `0x4155`-`0x4157` | `0x002FE660` | read-modify-write a register through `0x00321190`/`0x00329E60` (kind = record `+0x06` >> 12, index = its low byte; `0x4122`/`0x4123` use kind 10 of the unit at `+0x710`, the dword at `+0xB90`): set bit, clear bit, set or add the parameter |
| `0x4126`-`0x4127`, `0x4129`-`0x4138`, `0x414B`-`0x414C`, `0x4150`-`0x4154` | `0x002FDC30` | turn in place to the facing `0x00312B40` derives from the order record, seeded with the unit's yaw (block `+0xE0`, unit `+0x160`): on phase 0 the facing goes to the movement block's (unit `+0x80`) `+0x150` with goal kind `+0x160` = 2 and mode `+0x40` = 0, the stop distance `+0xD0` is the larger of the unit's two body sizes (`0x00265090`), `0x003291B0` resets the movement with the unit's own position `+0x60` as both points, and the phase becomes 1 (`0x002FDC85`-`0x002FDCFD`); `0x4127`, `0x4129`-`0x4138` and `0x414B` re-resolve the facing every frame from the second on (`0x002FDD08`-`0x002FDD4D`); a facing that `0x00312B40` cannot give ends the order with -1 (`0x002FDC9E`, `0x002FDD41`); each frame before the end runs the navigation step `0x00325BB0(unit, 0)` and returns 0 whatever it answers (`0x002FDD64`-`0x002FDD6E`); ends when `0x0033A120` reports it reached, which for goal kind 2 needs the yaw within 0.001 (`0x008C5B2C`) of the facing (`0x00335681`-`0x003356AF`), and then sets the phase to 2 and returns 1; a phase above 1 returns 1 at once (`0x002FDC77`, `0x002FDD7B`) |
| `0x4139`-`0x4140` / `0x4141`-`0x4148` | `0x002FDDA0` | set / clear one of the bits `0x1`-`0x80` of the battle flags `0x022C314C`, in id order (`0x0031A910` / `0x0031A8C0`, which also call `0x00469C00`) |
| `0x414D` | `0x002FE840` | unless unit bit `0x1000000` is set or the phase gate of the running-action check applies, `0x00313400(unit)`, or `0x00313480()` when unit bit `0x800000` is set; ends when unit bits `0x4000000000000` and `0x8000000000000` are clear |
| `0x414F` | `0x002FE8D0` | `0x002E73C0(actor, param)` |
| `0x4158`-`0x4162` | `0x002FDDA0` | add the parameter to one `i16` of the stats record (`+0x08`, `+0x0A`, `+0x0C`, `+0x0E`, `+0x1E`, `+0x12`, `+0x14`, `+0x10`, `+0x18`, `+0x1A`, `+0x1C`), clamped to +-99, +-100 or +-255, then rebuild (`0x0030FED0`) |
| `0x4163` / `0x4164` | `0x002FDDA0` | enemy side: set to 1 / add the parameter to the enemy's per-party-member byte table (`[unit+0x6A0]+0x1A` indexed by type id) for every living party member (`0x00321B00`) |
| `0x4166` | `0x002FE910` | `0x0046A6E0(param)` |
| `0x4025`, `0x4036`-`0x4045`, `0x4128` | `00000000` | empty slots: refused by dispatch and availability |

341 slots hold a handler and 18 are empty; 249 ids go to `0x002FDDA0`.

## Related

- [Action phases](action-phases.md) - the path ordinary actions (ids up to `0x21E`) take instead.
- [Action commit](action-commit.md) - the two accepted id ranges.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the statuses
  the status orders add and remove.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the AI order
  lists that issue these orders and the per-party-member table of `0x4163`/`0x4164`.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement goals of the move orders.
