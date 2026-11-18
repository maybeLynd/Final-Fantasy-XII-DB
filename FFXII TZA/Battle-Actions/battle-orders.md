[Home](../../README.md) / [Battle actions](README.md) / Battle orders

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Battle orders: the internal order ids 0x4000-0x4166, their handlers and what each order does | reference | Battle actions | Action tables | Every internal battle order id from 0x4000 to 0x4166 - moves, waits, adding and removing statuses, setting and clearing augment bits, stat adjustments, flag and register changes - with the handler the order table sends it to, its parameter, the status or augment it names, and the availability chance check AI order lists apply. | 0x01EEC460, 0x00305080, 0x00301830, 0x002FDDA0, 0x002FDA60, 0x002FDC30 |

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
the handler with the unit as argument¹. Handlers keep their progress in the
phase byte `+0x6B4`; one-shot handlers set it to 2 and return 1 at once.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003050A0`-`0x0030510E` |

</details>

`0x00307BE0(unit)` answers -1 when the action context `+0x708` is null¹. Otherwise it clears bit
`0x100` of the unit's `+0x1F0`, runs `0x00304850(unit)` for an action id `+0x714` up to `0x21E` and `0x00305080(unit)`
above it, and adds 1 to the counter `+0x75C` when the dword `+0x768` is not below `+0x76C`, a signed compare; it
answers that call's answer². An answer of 1 first calls
`0x004697C0(stats record +0x698, action id, 0xFFFF, 0)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307BE6`-`0x00307BF3` |
| ² | `0x00307BFC`-`0x00307C35`, `0x00307C5C` |
| ³ | `0x00307C3B`-`0x00307C57` |

</details>

`0x002FDDA0` tests that phase byte first: when it is not 0 on entry it returns 1 and does nothing else¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FDDB7`-`0x002FDDCE` |

</details>

### Availability

`0x00301830(unit, record)` refuses an id outside the table or an empty slot, then applies these
id-specific rules¹; every other id passes:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003018DD`-`0x00301AA4` |

</details>

| Ids | Rule |
|---|---|
| `0x4051`-`0x4121` except `0x4091`, and `0x414B` | a non-zero parameter is a percentage: refused when the parameter is not above a draw from the gameplay generator (`0x00328370`) modulo 100 |
| `0x4022`, `0x4124` | must have a movement block `+0xD4` that is not negative (`0x00301978`) and a reachable movement goal (`0x00312730`, and `0x0033A120` must not report arrival); `0x4022` then stores the goal at `+0x6C0` and `0x00309A90()` at `+0x6D0` |
| `0x4165` | `0x00312730` must find a goal |
| `0x414D` | `0x00308130` (party side) or `0x00308040(unit, 0)`, tested against unit bit `0x800000` |

`0x00301830` reads the id as the record's word `+0x00`, zero-extended, and the parameter as its word `+0x02`, read
signed, and works on a copy: it copies `0x610` bytes of the unit's movement block from `+0x80` to its stack, and no
rule writes the unit's own block¹. It answers 0 for an id whose `id - 0x4000` is above `0x166`
or whose slot of the order table `0x01EEC460` is null, then picks the rule by id, and answers 1 for an id with no rule².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301857`-`0x003018DA` |
| ² | `0x003018DD`-`0x00301935`, `0x00301A1B`-`0x00301A36` |

</details>

An id of `0x4051`-`0x4121` except `0x4091`, or `0x414B` (the first row of the table above), with a parameter of 0
answers 1. Otherwise it takes `0x00328370() % 100`, signed, and answers 0 when that value is not below the parameter, a
signed compare, and 1 when it is¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030193B`-`0x0030196B` |

</details>

For `0x4022` and `0x4124` it answers 0 when the copy's float `+0xD4` is below 0¹ or when
`0x00312730(unit, record, copy + 0x80, copy + 0x90, copy + 0xD0)` answers 0². It then adds 0.4³ to the copy's stop distance `+0xD0`, zeroes the copy's dwords `+0x40` and `+0x160`, and answers 0 when
`0x0033A120(copy, id)` answers non-zero⁴. Otherwise `0x4124` answers 1, and `0x4022` stores
`0x00309A90()` at the unit's float `+0x6D0` and the copy's 16 bytes `+0x80` at the unit's `+0x6C0` and answers 1⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301970`-`0x00301980` |
| ² | `0x00301986`-`0x003019B0` |
| ³ | `0x009153EC` |
| ⁴ | `0x003019B6`-`0x003019EB` |
| ⁵ | `0x003019F1`-`0x00301A16` |

</details>

`0x4165` answers `0x00312730(unit, record, copy + 0x80, copy + 0x90, copy + 0xD0)`¹. `0x414D`
calls `0x00308130(unit)` when the stats record `+0x698` is not null and its byte `+0x05` is 0, and `0x00308040(unit, 0)`
otherwise, and answers, as 0 or 1, that call's answer exclusive-or unit bit `0x800000`, the unit's dword `+0x00`². Every way out of `0x00301830` passes the stack-cookie check `0x00808C40(cookie)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301A38`-`0x00301A60` |
| ² | `0x00301A62`-`0x00301AA2` |
| ³ | `0x00301AA4`-`0x00301AB1` |

</details>

Besides those two stores of `0x4022`, `0x414D` writes the unit through `0x00308130`, the engagement test of [force fight
mode](../Engine-Core/force-fight-mode.md#what-fleeing-changes), which tells its paths. Its first call, the
engagement update `0x00307D10(unit)`, sets or clears bit `0x10000` of the unit's dword `+0x04` on every path, and each
path that clears it first clears bits `0x200` and `0x400`; the fleeing path also clears bits `0x2` and `0x4` of
`0x022C1F48` and zeroes the qword `0x022C1F40` and the unit's dword `+0xDCC`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307D1D`-`0x00307DE2` |

</details>

`0x00308130` then calls `0x003081E0(unit)` only when the stats record's dword `+0x64` or `+0x3C` has a bit of `0x8000020`
or `0x00253B90()` answers 0, bit `0x10000` of the unit's dword `+0x04` is clear, and bit `0x1` of `0x022C1F48` is set¹. That call stores a new `+0xDCC` when unit bit `0x800000` is clear and `+0xDCC` is 0, and its
draw `0x00328370()` writes the generator state `0x022C256C`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030814C`-`0x00308192` |
| ² | `0x003081E6`-`0x0030825C` |

</details>

## Columns

[`battle-orders.tsv`](battle-orders.tsv), one row per order id:

| Column | Meaning |
|---|---|
| `order_id` | the order id, `0x4000`-`0x4166` |
| `handler` | the function in the order table's slot, or `00000000` for an empty slot |
| `operation` | what the handler does for this id |
| `value` | the id-derived value (status number, effect number, bit, index) or where the parameter comes from |
| `name` | for status orders the status name from `battle_pack.bin`'s status-name table; for augment orders the augment's name in the database, the `term` column of the [augment list](../Damage-And-Battle-Formulas/augment-list.md) (the name that page explains, not the game's stored name or help text) |

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

`0x0033A120(block, id)` builds a movement context with `0x00336710(context, block, 1)`¹. It answers
1 when the block's dword `+0x40` has any bit other than `0x2` set². It answers 0 when
`0x004686D0(context, context + 0x30)` is above the context's float `+0xAC`, and, for the id `0x4124`, when
`0x0033D3E0(context, context + 0x20, block byte +0x174)` answers 1³. Otherwise it answers 1 when
`0x00335640(context, id)` is not 0, and 0 when it is⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0033A13B`-`0x0033A14C` |
| ² | `0x0033A151`-`0x0033A160` |
| ³ | `0x0033A162`-`0x0033A1A7` |
| ⁴ | `0x0033A1A9`-`0x0033A1BE` |

</details>

`0x003291B0(block, first, second)` calls `0x003839F0(block + 0x180)`, then copies 16 bytes from `first` to the block's
`+0x80` and from `second` to its `+0x90`, a null pointer being replaced by the block's own `+0x50`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003291C5`-`0x003291F8` |

</details>

`0x00312B40(unit, record, &facing, &kind)` derives the facing of a turn order from the record's id `+0x00` and its
parameter `+0x02`, read signed, and answers 1, or 0 when it can give none¹. It
stores kind 2 first; an id below `0x4126` or above `0x4154`, and the ids `0x4128`, `0x4139`-`0x414A` and
`0x414D`-`0x414F`, keep that kind and answer 0 (`0x00312B67`-`0x00312B9C`, the jump table `0x00312D88` and its index bytes
`0x00312DB4`). `0x4126` gives `0x00316DA0(parameter * 2pi / 360.0, 0)`, the parameter in degrees, wrapped².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00312B57`-`0x00312B5D`, `0x00312D6F` |
| ² | `0x00312B9E`-`0x00312BC7` |

</details>

`0x4127`, `0x4129`-`0x4138` and `0x414B` give, with kind 3, the bearing `0x0031AC90(unit + 0xE0, other + 0xE0, facing)`
to another unit: the party leader `0x003272A0()`, the unit `0x002367A0(id - 0x4129)` or the unit
`0x0031B7E0(unit dword +0x710)`. They answer 0 when that unit is null, and the last two also when it is the unit itself¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00312BCC`-`0x00312C58` |

</details>

`0x414C` copies the dword `+0x70` of the record at the unit's `+0x6A0` as the facing, and answers 0 unless the unit is
not null, its stats record `+0x698` is not null and that record's byte `+0x05` is 1¹. `0x4150`
turns the facing by `(draw % 340 + 10) * 2pi / 360.0` with `0x00316DA0(facing, turn)`, the draw `0x00328370()` from the
gameplay generator `0x022C256C` and `draw % 340` a signed one². `0x4151`, `0x4152` and `0x4153`
turn it by -pi/2, pi/2 and pi with `0x00316DA0(facing, angle)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00312C5A`-`0x00312C8E` |
| ² | `0x00312C93`-`0x00312CDF` |
| ³ | `0x00312CE4`-`0x00312D36` |

</details>

`0x4154` gives, with kind 1, the bearing `0x0031AC90(unit + 0xE0, &point, facing)` to the point that
`0x00320940(parameter, &point)` fills, and answers 0 when that call answers below 0¹. Every way
out passes the stack-cookie check `0x00808C40(cookie)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00312D38`-`0x00312D6D` |
| ² | `0x00312D71`-`0x00312D79` |

</details>

`0x00313400(unit)` calls `0x002ECF10(unit qword +0x10, 1, 1)`, sets unit bit `0x800000`, stores 0 at the unit's `+0xDCC`
and stores at its `+0x6E8` the address `0x01EEC3C0` when the stats record `+0x698` has a byte `+0x05` of 0, and
`0x01EEC410` for any other byte or no record¹. It then sets unit bits `0x1000000` and
`0x4000000000000` and ends with a jump to `0x00312EE0(unit)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00313406`-`0x00313458` |
| ² | `0x0031345F`-`0x00313471` |

</details>

## Related

- [Action phases](action-phases.md) - the path ordinary actions (ids up to `0x21E`) take instead.
- [Action commit](action-commit.md) - the two accepted id ranges.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the statuses
  the status orders add and remove.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - the AI order
  lists that issue these orders and the per-party-member table of `0x4163`/`0x4164`.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement goals of the move orders.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 3 calls with 2 other topics</summary>

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00253B90`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) | is called by | [`0x00313A00`](action-phases.md) (on action phases) |

**Menus and HUD** (explained on [action definition row](action-definition-row.md), [battle menu](../Menus-And-HUD/battle-menu.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B7E0`](../Engine-Core/identifier-spaces.md) (on identifier spaces) | is called by | [`0x0031EB20`](action-definition-row.md) Battle menu: build command entry list (on action definition row) |
| [`0x003272A0`](../World-Areas-And-Travel/treasure-chests.md) Battle unit: get party leader (on treasure chests) | is called by | [`0x00318CD0`](../Menus-And-HUD/battle-menu.md) (on battle menu) |

</details>
