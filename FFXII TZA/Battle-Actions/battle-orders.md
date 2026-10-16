---
title: "Battle orders: the internal order ids 0x4000-0x4166, their handlers and what each order does"
kind: "reference"
category: "Battle actions"
summary: "Every internal battle order id from 0x4000 to 0x4166 - moves, waits, adding and removing statuses, setting and clearing effect bits, stat adjustments, flag and register changes - with the handler the order table sends it to, its parameter, the status or effect it names, and the availability chance check AI order lists apply."
addresses: "01EEC460, 00305080, 00301830, 002FDDA0, 002FDA60, 002FDC30"
---

## What it lists

A unit's action id `+0x714` holds either an ordinary action (ids up to `0x21E`, which carry a target
list) or an internal **order** (`0x4000`-`0x4166`, no target list). Orders are what AI order lists and
scripts use for moving, waiting, changing statuses and effect bits and adjusting stats; each comes with
a small order record (the action data `+0x708`), whose `s16` at `+0x02` is the order's parameter.
The table lists all 359 order ids with what the game does for each.

### Dispatch

`00305080` (called by the action step `00307BE0` for an id above `0x21E`) posts
presentation event `0x2001` - or `0x2010` for a party-side unit of type id `0x1A` while bit 1 of
`[02EBF190]+0x5AE0` is set - then returns -1 when `id - 0x4000` is above `0x166` or the slot of the
table at `01EEC460` (359 eight-byte pointers, `01EEC460`-`01EECF97`) is empty, and otherwise jumps to
the handler with the unit as argument (`003050A0`-`0030510E`). Handlers keep their progress in the
phase byte `+0x6B4`; one-shot handlers set it to 2 and return 1 at once.

### Availability

`00301830(unit, record)` refuses an id outside the table or an empty slot, then applies these
id-specific rules (`003018DD`-`0030199A`); every other id passes:

| Ids | Rule |
|---|---|
| `0x4051`-`0x4121` except `0x4091`, and `0x414B` | a non-zero parameter is a percentage: refused when the parameter is not above a draw from the gameplay generator (`00328370`) modulo 100 |
| `0x4022`, `0x4124` | must have a reachable movement goal (`00312730`, then `0033A120` not yet reporting arrival); `0x4022` then stores the goal at `+0x6C0` and `00309A90()` at `+0x6D0` |
| `0x4165` | `00312730` must find a goal |
| `0x414D` | `00308130` (party side) or `00308040(unit, 0)`, tested against unit bit 23 |

## Columns

`battle-orders.tsv`, one row per order id:

| Column | Meaning |
|---|---|
| `order_id` | the order id, `0x4000`-`0x4166` |
| `handler` | the function in the order table's slot, or `00000000` for an empty slot |
| `operation` | what the handler does for this id |
| `value` | the id-derived value (status number, effect number, bit, index) or where the parameter comes from |
| `name` | for status orders the status name from `battle_pack.bin`'s status-name table; for effect orders the effect's help text from `listhelp_ability.bin` where it has one |

## Data

The ids fall into these groups (full rows in the `.tsv`):

| Ids | Handler | Operation |
|---|---|---|
| `0x4000`-`0x4020`, `0x4022`-`0x4024`, `0x4026`-`0x4035`, `0x4124`-`0x4125`, `0x414A`, `0x414E`, `0x4165` | `002FDA60` | move to the goal `00312730` derives from the order record; ends when `0033A120(movement block, id)` reports it reached. For `0x4022`, `0x4024`, `0x4026`-`0x4035`, `0x4124`, `0x414A`, `0x414E` and `0x4165` the goal is refreshed every frame through `00319110`; `0x4022` and `0x4124` set bit 8 of `+0x1F0` while on the way; `0x414E` moves toward the unit at `+0x710`. For the other ids a failed navigation step (`00325BB0(unit, 0)` = 0 before arrival) ends the order with -1; the refreshed ids wait instead |
| `0x4021` | `002FE7D0` | wait until the counter `+0x75C` reaches `param * (int)(30 * [01DFE0B8])`; clears `+0x750`-`+0x757` first; a parameter of 0 never ends |
| `0x4046`, `0x4047` | `002FDDA0` | set / clear unit flag bit 15 |
| `0x4048`-`0x404F` | `002FDDA0` | set unit byte `+0x54` to 0-7 |
| `0x4050` | `002FDDA0` | remove every status (`0030E8F0`) |
| `0x4051`-`0x4070` | `002FDDA0` | add status 0-31 (`0030E360` mode 3) |
| `0x4071`-`0x4090` | `002FDDA0` | remove status 0-31 (`0030E360` mode 0) |
| `0x4091` | `002FDDA0` | clear all 128 effect bits of the layer at stats `+0x68`, then rebuild the stats (`0030FED0`) |
| `0x4092`-`0x40D1` | `002FDDA0` | set effect bit 0-63 at stats `+0x68` (`0030E130` mode 2) |
| `0x40D2`-`0x4111` | `002FDDA0` | clear effect bit 0-63 at stats `+0x68` (`0030E130` mode 0) |
| `0x4112`-`0x4115` | `002FDDA0` | enemy side: point `+0x6E0` at the entry of the table at `02EBF168` named by the `u16` at `[unit+0xE60]+0x50+2k`, and zero `+0x6B5`; a selector at or past the table's count (`u16` at `+0`) refuses the order (-1); any other unit ends at once doing nothing |
| `0x4116`-`0x4121` | `002FDDA0` | set unit byte `+0x6B5` to 0-11 |
| `0x4122`, `0x4123`, `0x4149`, `0x4155`-`0x4157` | `002FE660` | read-modify-write a register through `00321190`/`00329E60` (kind = record `+0x06` >> 12, index = its low byte; `0x4122`/`0x4123` use kind 10 of the unit at `+0x710`, the dword at `+0xB90`): set bit, clear bit, set or add the parameter |
| `0x4126`-`0x4127`, `0x4129`-`0x4138`, `0x414B`-`0x414C`, `0x4150`-`0x4154` | `002FDC30` | move by `00312B40` to a goal from the order record, stopping at the larger of the unit's two body sizes; `0x4127`, `0x4129`-`0x4138` and `0x414B` re-resolve the goal every frame; ends when `0033A120` reports it reached |
| `0x4139`-`0x4140` / `0x4141`-`0x4148` | `002FDDA0` | set / clear bit 0-7 of the battle flags `022C314C` (`0031A910` / `0031A8C0`, which also call `00469C00`) |
| `0x414D` | `002FE840` | unless unit bit 24 is set or the phase gate of the running-action check applies, `00313400(unit)`, or `00313480()` when unit bit 23 is set; ends when unit bits 50 and 51 are clear |
| `0x414F` | `002FE8D0` | `002E73C0(actor, param)` |
| `0x4158`-`0x4162` | `002FDDA0` | add the parameter to one `s16` of the stats record (`+0x08`, `+0x0A`, `+0x0C`, `+0x0E`, `+0x1E`, `+0x12`, `+0x14`, `+0x10`, `+0x18`, `+0x1A`, `+0x1C`), clamped to +-99, +-100 or +-255, then rebuild (`0030FED0`) |
| `0x4163` / `0x4164` | `002FDDA0` | enemy side: set to 1 / add the parameter to the enemy's per-party-member byte table (`[unit+0x6A0]+0x1A` indexed by type id) for every living party member (`00321B00`) |
| `0x4166` | `002FE910` | `0046A6E0(param)` |
| `0x4025`, `0x4036`-`0x4045`, `0x4128` | none | empty slots: refused by dispatch and availability |

341 slots hold a handler and 18 are empty; 249 ids go to `002FDDA0`.

## Related

- [Action phases](action-phases.md) - the path ordinary actions (ids up to `0x21E`) take instead.
- [Action commit](action-commit.md) - the two accepted id ranges.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the statuses
  the status orders add and remove.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the AI order
  lists that issue these orders and the per-party-member table of `0x4163`/`0x4164`.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement goals of the move orders.
