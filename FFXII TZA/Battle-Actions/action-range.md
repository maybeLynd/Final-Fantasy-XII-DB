---
title: "Action range: near, middle and reach distances and how a unit closes in on its target"
kind: "system"
category: "Battle actions"
addresses: "002FEB80, 00309300, 00320D70, 00338140, 00337A50, 003341A0"
---

## What the player sees

When a character or an enemy starts an action, it works out three distances to its target, not one
range:

- **reach** - further than this and it cannot act;
- **middle** - the distance it settles at;
- **near** - closer than this and it may step back.

All three are measured centre to centre: the larger body size of the attacker and the larger body size
of the target are added to each, so big monsters are hit from further away.

Where the numbers come from depends on one flag of the action:

- Most actions (508 of the 543 shipped action rows) carry their own reach; a value of 100 in the
  action row is a reach of 10.0.
- Actions with the weapon flag reach as far as the weapon held: every shipped equipment row of kind 2
  reaches 10.0 to 25.0, and every row of kinds 1, 3, 4 and 5 reaches 1.0 to 3.0.
- For weapon-flag actions the near and middle distances come from the character's own parameters for
  that kind of weapon.
- Equipment kind 2 has no such parameters, and an action whose own near or middle value is 0 has none
  either; then near is 60 % of the reach and middle 80 %.
- An unarmed character holds Unarmed (`1000`<sub>h</sub>, reach byte 10), so its weapon-flag actions take a
  weapon reach of 1.0 (`00309300`), like any other weapon; only a unit whose main-hand id is `FFFF`<sub>h</sub>
  gets a weapon reach of 0.

A unit further away than its middle distance plus 2.0 (or its reach, if that is smaller) walks in; a
unit closer than its near distance may back off. When two units target each other, the one with the
longer middle distance uses the other's near distance, so they do not push each other away.

A party-side character (a party member or a guest, not an Esper) whose action is still charging
can pace its approach instead of sprinting to the target and waiting. It aims for a point 70 % of the
way from its middle distance out to its reach, stands still for the first 30 ticks of the charge (60
at the 60 fps setting), and then walks in at normal speed so that it arrives about when the charge
completes.

If even its fast speed could not get it there in time, it simply goes. This pacing is skipped when the
target is itself targeting a party-side character other than an Esper, and runs only while the
movement step has it switched on.

## How it works

### The builder

`002FEB80` (476 bytes) takes `(actor, target, actionRow, outReach, outMiddle,
outNear)`. It has one caller, the standard-action state machine `00304850`, which calls it at
`00304AB9` with the outputs at unit `+6DC`<sub>h</sub> (reach), `+6D8`<sub>h</sub> (middle) and `+6D4`<sub>h</sub> (near)
(`rsi = unit + 6B0h`, `0030487F`; `00304A7F`-`00304A95`).

A later step of the same machine copies
them to the unit's movement block (unit `+80`<sub>h</sub>, `003048EF`): near to `+120`<sub>h</sub>, middle to `+124`<sub>h</sub>,
reach to `+128`<sub>h</sub>, and sets bit 5 of block `+170`<sub>h</sub> (`00304BF3`-`00304C0F`). Just before, it sets the
block's movement mode `+40`<sub>h</sub> to 1 (`00304BEC`); the movement step `0033BED0` runs the spacing step
only in that mode (`0033BF59`-`0033BF5F`).

1. **The weapon row.** The weapon id is the `u16` at `+50`<sub>h</sub> of the actor's stats record
   (`[unit+698h]`). The equipment row is resolved only when the id is below the equipment table's
   count plus `1000`<sub>h</sub> and the table at `02EBF0F8` is present (`002FEBCA`-`002FEC1D`).
2. **The row address** is the table base (resolved through `0020E600`) plus `(id - 1000h)` times the
   `u16` stride at table `+8`. Otherwise the row is null; the empty hand `FFFF`<sub>h</sub> fails the bound.
3. **Body sizes.** For a class-3 object (byte `[object+3] & E0h` = `60`<sub>h</sub>), `00265090` returns the
   pair of floats at `[object+B8h]+50h` and `+54`<sub>h</sub>; for any other object it leaves the outputs
   unwritten. It is asked for the actor and for the target. The builder takes the larger of each pair and adds the two
   (`002FEC34`-`002FEC7E`).
4. **Inner values.** `a = 00320D70(actor, row, weaponRow, 0)` and `b = 00320D70(..., 1)`
   (`002FEC83`, `002FEC9A`).
5. **The reach.** `R = 00309300(row, weaponId)` (`002FECC6`).
6. **Authored or proportional.** The bands are authored only when both `a` and `b` are non-zero: a
   zero `a` skips the test of `b` (`002FECAA`), a zero `b` fails it (`002FECB1`); an unordered (NaN)
   compare counts as non-zero. Authored: near = `a`, middle = `a + b`, reach = `a + b + R`
   (`002FECD2`-`002FECD9`). Otherwise near = `0.6 R` (`008F3100`), middle = `0.8 R` (`008F3108`),
   reach = `R` (`002FECDF`-`002FECF8`).
7. The body-size sum is added to all three, and each output is stored only when its pointer is
   non-null (`002FECFB`-`002FED32`). The function returns 0.

### The reach

`00309300` (169 bytes) takes `(actionRow, weaponId)`. It tests the weapon id as a
class-6 (equipment) id with `00322C50(6, id, 0)` and resolves its row (`00309319`-`0030935E`). A null
action row gives 0.0 (`00309364`). When bit 26 (`4000000`<sub>h</sub>) of the row's flag word `+0C`<sub>h</sub> is clear,
the reach is the row's byte `+05`<sub>h</sub>; when it is set, the reach is the equipment row's byte `+18`<sub>h</sub>,
or 0.0 when there is no equipment row (`00309377`-`0030938B`). The byte is divided by 10.0
(`008F8180`, `0030939B`).

### The inner values

`00320D70` (146 bytes) takes `(actor, actionRow, equipmentRow, component)`:

- **Bit 26 clear:** the action row's byte `+02h + component`, divided by 10.0 - `+02`<sub>h</sub> is the near
  value and `+03`<sub>h</sub> the middle value (`00320DE1`-`00320DF5`).
- **Bit 26 set:** the equipment row's kind byte `+25`<sub>h</sub> (kind 0 for a null row, `00320DAF`). Kind 2,
  or any kind above 5, gives 0.0 (`00320D93`-`00320DA2`). Otherwise the parameter number is the dword
  at `01EED288 + (component + kind * 2) * 4` (table below), and the value comes from
  `003204E0(object, number, &out)`; a negative return gives 0.0 (`00320DB1`-`00320DD1`).

| Equipment kind | Near parameter | Middle parameter |
|---:|---:|---:|
| 0 | 13 | 12 |
| 1 | 15 | 14 |
| 3 | 19 | 18 |
| 4 | 21 | 20 |
| 5 | 23 | 22 |

`003204E0` reads numbers 12-23 through `002ECE50(object, dword at 01EED320 + number * 4)` (the
character parameter ids `09000D0E`<sub>h</sub>-`09001819`<sub>h</sub>, `01EED350`) and multiplies the result by the float
at `[object+B8h]+28h` (the third output of `00265240`). Numbers 24, 26, 28 and 31 take the
integer path instead: `002ECE80(object, id)` hands the same character record id, with the same null
and -1 guards, to `003E6310` (`002ECE80`-`002ECEA0`), and `003204E0` stores the returned dword as it
is (`00320580`-`00320590`).

`002ECE50` passes the int that `[object+C0h]` points to (returning 0.0 when the pointer is null or the
int is -1) to `003E6150`. That reads the parameter from the character's parameter block (`004FE270`)
and multiplies it by the float at `+26C`<sub>h</sub> of that character's `740`<sub>h</sub>-byte record at `022C6F28`.

### Spacing

`00338140` (839 bytes) runs per step on a movement context `ctx` built by `00336710`:
`ctx+00h` is the unit's own position (block `+60`<sub>h</sub>), `ctx+30h` the reference-target point (block
`+90`<sub>h</sub>, stored by `00319110`), `ctx+40h` the target unit's live position, `ctx+100h` and
`ctx+108h` both the movement block, `ctx+F0h` the acting unit and `ctx+F8h` the target unit
(`00336733`-`003367BB`). Below, "the block" is that movement block.

1. It stops (speed `ctx+B0h` = 0, bits 5-14 of block `+00`<sub>h</sub> cleared) when the unit in the block's
   slot `+177`<sub>h</sub> has the id held at block `+150`<sub>h</sub> (`0033818E`), or when the unit is within 0.1
   (`008C5F6C`, XZ) of the target's live position (`003381AF`).
2. **Mutual targets.** When the target's focus handle `[target+710h]` resolves (`0031B7E0`) to the
   acting unit and the unit's middle (block `+124`<sub>h</sub>) is larger than the target's (target `+1A4`<sub>h</sub>),
   the near value used is the target's (`+1A0`<sub>h</sub>); otherwise its own (block `+120`<sub>h</sub>)
   (`00338201`-`0033823F`).
3. **Too far** when the XZ distance `d` from the unit to the reference-target point
   (`0033826E`) exceeds `min(middle + 2.0, reach)` (`01CEBC08`, `00338253`-`00338266`): bit 1 of
   block `+38`<sub>h</sub> (approach). **Too close** when `d < near + 0.05` (`008F30E8`) and `003341A0`
   agrees: bit 2 of block `+38`<sub>h</sub> (back off) (`00338281`-`0033829B`).
4. Approach is dropped when the block's stop distance `+D0`<sub>h</sub> is larger than `d`, and back-off when
   `d` is larger than it (`0033829F`-`003382DE`). When the pair clearance test `0033D660` returns 0,
   the approach bit is set (`003382F2`-`00338301`).
5. **Approach** runs the pacing step `00337A50` and then `0033A720`; a non-zero pacing result clears
   bits 5-14 of block `+00`<sub>h</sub> (`0033830C`-`00338326`).
6. **Back-off** tests a step with `00335B60`: if it returns 0 the unit moves away at the block's speed
   `+F8`<sub>h</sub> with heading `ctx+B4h` (turn limit `003364D0`), otherwise the back-off bit is cleared
   (`00338339`-`003383BC`).
7. **Neither:** the avoidance manoeuvre `003343D0` runs (and `0033BAA0` when it starts). When neither
   bit of block `+38`<sub>h</sub> is set and bits 5-14 of block `+00`<sub>h</sub> are clear, the unit stops and turns to
   face the target (`003383C2`-`00338442`).

### The back-off condition

`003341A0` returns 1 only when bit 0 of block `+38`<sub>h</sub> is set, both
units exist and differ, `0030BCB0(unit, target, 0)` is 0 (the relationship class from `0030AB40` is
above 1), and the acting unit is not on the enemy side (stats byte `+05`<sub>h</sub> not 1) or has bit 1 of byte
`+21`<sub>h</sub> of its `[unit+E68h]` record set.

### Pacing

`00337A50` (442 bytes) runs only while bit 8 (`100`<sub>h</sub>) of block `+3C`<sub>h</sub> is set, the
acting unit's class from `002F8E70` is 1, the class of the unit the target is focused on is not 1, and
the speed `ctx+B0h` is non-zero; otherwise it clears bit 8 and returns 0 (`00337A74`-`00337ACB`,
`00337BDF`). `002F8E70` returns 1 for a party-side unit (stats byte `+05`<sub>h</sub> = 0) whose type id (byte
`+04`<sub>h</sub>) is outside the Esper band `1B`<sub>h</sub>-`27`<sub>h</sub>, and 2 inside it (`002F8E90`).

1. The aim point is `middle + 0.7 * (reach - middle)` (`008F3104`, `00337ADF`-`00337AFB`); `rem` is
   the XZ distance from the unit to the target's live position minus the aim. A negative `rem`
   returns 0 (`00337B0F`).
2. The remaining charge ticks are `([unit+76Ch] - [unit+768h])` divided by the charge per tick
   `002F9C00(unit)`. If that is not larger than `rem` divided by the fast speed (block `+FC`<sub>h</sub>), pacing
   is abandoned: bit 8 is cleared and 0 returned (`00337B26`-`00337B50`).
3. While the elapsed ticks `[unit+768h] / step` are fewer than `30 * [01DFE0B4]` (`00337B75`), the
   unit stands (speed 0). After that it stands while the remaining ticks exceed `rem` divided by the
   normal speed (block `+F8`<sub>h</sub>), and walks at the normal speed otherwise (`00337B80`-`00337BD7`).
   Either way it returns 1.

`01DFE0B4` is 1 as shipped; `001EDDC0` sets it to 2 (`001EDDF2`) while setting the per-frame scale
`01DFE0BC` to 0.5, so the standing window is 30 ticks at the shipped setting and 60 after that switch.

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+6D4`<sub>h</sub> | `f32` | near | `002FEB80` via `00304AB9` |
| unit `+6D8`<sub>h</sub> | `f32` | middle | `002FEB80` via `00304AB9` |
| unit `+6DC`<sub>h</sub> | `f32` | reach | `002FEB80` via `00304AB9` |
| unit `+1A0`<sub>h</sub> (block `+120`<sub>h</sub>) | `f32` | near, as movement reads it | `00304BF6` |
| unit `+1A4`<sub>h</sub> (block `+124`<sub>h</sub>) | `f32` | middle, as movement reads it | `00304BFF` |
| unit `+1A8`<sub>h</sub> (block `+128`<sub>h</sub>) | `f32` | reach, as movement reads it | `00304C0F` |

## Modding notes

- The action row's byte `+05`<sub>h</sub> is the reach times 10 for actions without bit 26 of `+0C`<sub>h</sub>; bytes
  `+02`<sub>h</sub> and `+03`<sub>h</sub> are near and middle times 10, used only when both are non-zero. In the shipped
  `battle_pack.bin`, 6 action rows set them (`1, 20` three times, `1, 15` twice, `20, 20` once) and
  none of those has bit 26.
- With bit 26 set, these functions use the equipment row instead of the action row's `+05`<sub>h</sub>,
  `+02`<sub>h</sub> and `+03`<sub>h</sub>: the reach is the equipment row's byte `+18`<sub>h</sub> times 10, and near and middle are
  character parameters chosen by the equipment row's kind byte `+25`<sub>h</sub>. 35 shipped action rows have bit 26.
- Shipped equipment reaches by kind (`+18`<sub>h</sub>): kind 1 10-20, kind 2 100-250, kind 3 10-20, kind 4
  10-30, kind 5 10-20; kind 0 (305 rows) 0-90.
- The fallback proportions are the floats at `008F3100` (0.6) and `008F3108` (0.8); the approach
  margin is `01CEBC08` (2.0, a constant shared with other code), the back-off margin `008F30E8`
  (0.05), the pacing aim `008F3104` (0.7), and the pacing wait the immediate `1E`<sub>h</sub> at `00337B75`.

## Related

- [The action definition row](action-definition-row.md) - the 60-byte row
  whose bytes `+02`<sub>h</sub>, `+03`<sub>h</sub>, `+05`<sub>h</sub> and flag word `+0C`<sub>h</sub> these functions read.
- [The battle unit field map](../Characters-And-Objects/battle-unit-fields.md) - where
  the three distances sit on the unit.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement solver that runs the spacing and pacing steps.
- The inner values have a second reader: `00320E10` calls `00320D70` twice (`00320F6A`, `00320F82`)
  for the unit's current action and is used only by the query-record builder `0031ADB0`. It takes
  one object's body size as the larger of its `00265090` pair through `0030A160` (`00320FF6`;
  `0030A16E`-`0030A179`).
- [The FCP character parameter block](../17-Presentation-Rendering/model-files-cm-ca.md
)
  - the per-character parameters behind weapon-flag actions.
