---
title: "Battle orders: the internal order ids 4000ₕ-4166ₕ, their handlers and what each order does"
kind: "reference"
category: "Battle actions"
addresses: "01EEC460, 00305080, 00301830, 002FDDA0, 002FDA60, 002FDC30"
---

## What it lists

A unit's action id `+714`<sub>h</sub> holds either an ordinary action (ids up to `21E`<sub>h</sub>, which carry a target
list) or an internal **order** (`4000`<sub>h</sub>-`4166`<sub>h</sub>, no target list). Orders are what AI order lists and
scripts use for moving, waiting, changing statuses and effect bits and adjusting stats; each comes with
a small order record (the action data `+708`<sub>h</sub>), whose `i16` at `+02`<sub>h</sub> is the order's parameter.
The table lists all 359 order ids with what the game does for each.

### Dispatch

`00305080` (called by the action step `00307BE0` for an id above `21E`<sub>h</sub>) posts
presentation event `2001`<sub>h</sub> - or `2010`<sub>h</sub> for a party-side unit of type id `1A`<sub>h</sub> while bit 1 of
`[02EBF190]+5AE0h` is set - then returns -1 when `id - 4000h` is above `166`<sub>h</sub> or the slot of the
table at `01EEC460` (359 eight-byte pointers, `01EEC460`-`01EECF97`) is empty, and otherwise jumps to
the handler with the unit as argument (`003050A0`-`0030510E`). Handlers keep their progress in the
phase byte `+6B4`<sub>h</sub>; one-shot handlers set it to 2 and return 1 at once.

### Availability

`00301830(unit, record)` refuses an id outside the table or an empty slot, then applies these
id-specific rules (`003018DD`-`00301AA5`); every other id passes:

| Ids | Rule |
|---|---|
| `4051`<sub>h</sub>-`4121`<sub>h</sub> except `4091`<sub>h</sub>, and `414B`<sub>h</sub> | a non-zero parameter is a percentage: refused when the parameter is not above a draw from the gameplay generator (`00328370`) modulo 100 |
| `4022`<sub>h</sub>, `4124`<sub>h</sub> | must have a reachable movement goal (`00312730`, then `0033A120` not yet reporting arrival); `4022`<sub>h</sub> then stores the goal at `+6C0`<sub>h</sub> and `00309A90()` at `+6D0`<sub>h</sub> |
| `4165`<sub>h</sub> | `00312730` must find a goal |
| `414D`<sub>h</sub> | `00308130` (party side) or `00308040(unit, 0)`, tested against unit bit 23 |

## Columns

`battle-orders.tsv`, one row per order id:

| Column | Meaning |
|---|---|
| `order_id` | the order id, `4000`<sub>h</sub>-`4166`<sub>h</sub> |
| `handler` | the function in the order table's slot, or `00000000` for an empty slot |
| `operation` | what the handler does for this id |
| `value` | the id-derived value (status number, effect number, bit, index) or where the parameter comes from |
| `name` | for status orders the status name from `battle_pack.bin`'s status-name table; for effect orders the effect's help text from `listhelp_ability.bin` where it has one |

## Data

The ids fall into these groups (full rows in the `.tsv`):

| Ids | Handler | Operation |
|---|---|---|
| `4000`<sub>h</sub>-`4020`<sub>h</sub>, `4022`<sub>h</sub>-`4024`<sub>h</sub>, `4026`<sub>h</sub>-`4035`<sub>h</sub>, `4124`<sub>h</sub>-`4125`<sub>h</sub>, `414A`<sub>h</sub>, `414E`<sub>h</sub>, `4165`<sub>h</sub> | `002FDA60` | move to the goal `00312730` derives from the order record; ends when `0033A120(movement block, id)` reports it reached. For `4022`<sub>h</sub>, `4024`<sub>h</sub>, `4026`<sub>h</sub>-`4035`<sub>h</sub>, `4124`<sub>h</sub>, `414A`<sub>h</sub>, `414E`<sub>h</sub> and `4165`<sub>h</sub> the goal is refreshed every frame through `00319110`; `4022`<sub>h</sub> and `4124`<sub>h</sub> set bit 8 of `+1F0`<sub>h</sub> while on the way; `414E`<sub>h</sub> moves toward the unit at `+710`<sub>h</sub>. For the other ids a failed navigation step (`00325BB0(unit, 0)` = 0 before arrival) ends the order with -1; the refreshed ids wait instead |
| `4021`<sub>h</sub> | `002FE7D0` | wait until the counter `+75C`<sub>h</sub> reaches `param * (int)(30 * [01DFE0B8])`; clears `+750`<sub>h</sub>-`+757`<sub>h</sub> first; a parameter of 0 never ends |
| `4046`<sub>h</sub>, `4047`<sub>h</sub> | `002FDDA0` | set / clear unit flag bit 15 |
| `4048`<sub>h</sub>-`404F`<sub>h</sub> | `002FDDA0` | set unit byte `+54`<sub>h</sub> to 0-7 |
| `4050`<sub>h</sub> | `002FDDA0` | remove every status (`0030E8F0`) |
| `4051`<sub>h</sub>-`4070`<sub>h</sub> | `002FDDA0` | add status 0-31 (`0030E360` mode 3) |
| `4071`<sub>h</sub>-`4090`<sub>h</sub> | `002FDDA0` | remove status 0-31 (`0030E360` mode 0) |
| `4091`<sub>h</sub> | `002FDDA0` | clear all 128 effect bits of the layer at stats `+68`<sub>h</sub>, then rebuild the stats (`0030FED0`) |
| `4092`<sub>h</sub>-`40D1`<sub>h</sub> | `002FDDA0` | set effect bit 0-63 at stats `+68`<sub>h</sub> (`0030E130` mode 2) |
| `40D2`<sub>h</sub>-`4111`<sub>h</sub> | `002FDDA0` | clear effect bit 0-63 at stats `+68`<sub>h</sub> (`0030E130` mode 0) |
| `4112`<sub>h</sub>-`4115`<sub>h</sub> | `002FDDA0` | enemy side: point `+6E0`<sub>h</sub> at the entry of the table at `02EBF168` named by the `u16` at `[unit+E60h]+50h+2k`, and zero `+6B5`<sub>h</sub>; a selector at or past the table's count (`u16` at `+0`) refuses the order (-1); any other unit ends at once doing nothing |
| `4116`<sub>h</sub>-`4121`<sub>h</sub> | `002FDDA0` | set unit byte `+6B5`<sub>h</sub> to 0-11 |
| `4122`<sub>h</sub>, `4123`<sub>h</sub>, `4149`<sub>h</sub>, `4155`<sub>h</sub>-`4157`<sub>h</sub> | `002FE660` | read-modify-write a register through `00321190`/`00329E60` (kind = record `+06`<sub>h</sub> >> 12, index = its low byte; `4122`<sub>h</sub>/`4123`<sub>h</sub> use kind 10 of the unit at `+710`<sub>h</sub>, the dword at `+B90`<sub>h</sub>): set bit, clear bit, set or add the parameter |
| `4126`<sub>h</sub>-`4127`<sub>h</sub>, `4129`<sub>h</sub>-`4138`<sub>h</sub>, `414B`<sub>h</sub>-`414C`<sub>h</sub>, `4150`<sub>h</sub>-`4154`<sub>h</sub> | `002FDC30` | move by `00312B40` to a goal from the order record, stopping at the larger of the unit's two body sizes; `4127`<sub>h</sub>, `4129`<sub>h</sub>-`4138`<sub>h</sub> and `414B`<sub>h</sub> re-resolve the goal every frame; ends when `0033A120` reports it reached |
| `4139`<sub>h</sub>-`4140`<sub>h</sub> / `4141`<sub>h</sub>-`4148`<sub>h</sub> | `002FDDA0` | set / clear bit 0-7 of the battle flags `022C314C` (`0031A910` / `0031A8C0`, which also call `00469C00`) |
| `414D`<sub>h</sub> | `002FE840` | unless unit bit 24 is set or the phase gate of the running-action check applies, `00313400(unit)`, or `00313480()` when unit bit 23 is set; ends when unit bits 50 and 51 are clear |
| `414F`<sub>h</sub> | `002FE8D0` | `002E73C0(actor, param)` |
| `4158`<sub>h</sub>-`4162`<sub>h</sub> | `002FDDA0` | add the parameter to one `i16` of the stats record (`+08`<sub>h</sub>, `+0A`<sub>h</sub>, `+0C`<sub>h</sub>, `+0E`<sub>h</sub>, `+1E`<sub>h</sub>, `+12`<sub>h</sub>, `+14`<sub>h</sub>, `+10`<sub>h</sub>, `+18`<sub>h</sub>, `+1A`<sub>h</sub>, `+1C`<sub>h</sub>), clamped to +-99, +-100 or +-255, then rebuild (`0030FED0`) |
| `4163`<sub>h</sub> / `4164`<sub>h</sub> | `002FDDA0` | enemy side: set to 1 / add the parameter to the enemy's per-party-member byte table (`[unit+6A0h]+1Ah` indexed by type id) for every living party member (`00321B00`) |
| `4166`<sub>h</sub> | `002FE910` | `0046A6E0(param)` |
| `4025`<sub>h</sub>, `4036`<sub>h</sub>-`4045`<sub>h</sub>, `4128`<sub>h</sub> | none | empty slots: refused by dispatch and availability |

341 slots hold a handler and 18 are empty; 249 ids go to `002FDDA0`.

## Related

- [Action phases](action-phases.md) - the path ordinary actions (ids up to `21E`<sub>h</sub>) take instead.
- [Action commit](action-commit.md) - the two accepted id ranges.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the statuses
  the status orders add and remove.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the AI order
  lists that issue these orders and the per-party-member table of `4163`<sub>h</sub>/`4164`<sub>h</sub>.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement goals of the move orders.
