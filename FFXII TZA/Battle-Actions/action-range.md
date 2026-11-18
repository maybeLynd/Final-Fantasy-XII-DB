[Home](../../README.md) / [Battle actions](README.md) / Action range

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Action range: near, middle and reach distances and how a unit closes in on its target | system | Battle actions | How an action runs | How starting a battle action computes three distances to the target (back off inside near, settle at middle, act within reach) from the action row or from the weapon and the character, the 60 %/80 % fallback, and how movement uses them to approach, back off and time its arrival to the charge. | 0x002FEB80, 0x00309300, 0x00320D70, 0x00338140, 0x00337A50, 0x003341A0 |

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
- Equipment kind 2 has no such parameters, and an action whose own near or middle value is 0 has no such parameters
  either; then near is 60 % of the reach and middle 80 %.
- An unarmed character holds Unarmed, an equipment entry with a reach of 1.0, so its weapon-flag
  actions take a weapon reach of 1.0, like any other weapon; only a unit with no equipment entry at
  all in its main hand, not even Unarmed, gets a weapon reach of 0.

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

For weapon-flag actions, the kind byte of the weapon's equipment row picks which two of the character's own parameters
give near and middle, and the game reads them from the `@FCP` parameter block of the character's model.

## How it works

### The builder

`0x002FEB80` (476 bytes) takes `(actor, target, actionRow, outReach, outMiddle,
outNear)`. It has one caller, the standard-action state machine `0x00304850`, which calls it at
`0x00304AB9` with the outputs at unit `+0x6DC` (reach), `+0x6D8` (middle) and `+0x6D4` (near)
(`rsi = unit + 0x6B0`, `0x0030487F`; `0x00304A7F`-`0x00304A95`).

A later step of the same machine copies
them to the unit's movement block (unit `+0x80`, `0x003048EF`): near to `+0x120`, middle to `+0x124`,
reach to `+0x128`, and sets bit `0x20` of block `+0x170` (`0x00304BF3`-`0x00304C0F`). Just before, it sets the
block's movement mode `+0x40` to 1 (`0x00304BEC`); the movement step `0x0033BED0` runs the spacing step
only in that mode (`0x0033BF59`-`0x0033BF5F`).

1. **The weapon row.** The weapon id is the `u16` at `+0x50` of the actor's stats record
   (`[unit+0x698]`). The equipment row is resolved only when the id is below the equipment table's
   count plus `0x1000` and the table at `0x02EBF0F8` is present (`0x002FEBCA`-`0x002FEC1D`).
2. **The row address** is the table base (resolved through `0x0020E600`) plus `(id - 0x1000)` times the
   `u16` stride at table `+8`. Otherwise the row is null; the empty hand `0xFFFF` fails the bound.
3. **Body sizes.** For a class-3 object (byte `[object+3] & 0xE0` = `0x60`), `0x00265090` returns the
   pair of floats at `[object+0xB8]+0x50` and `+0x54`; for any other object it leaves the outputs
   unwritten. It is asked for the actor and for the target. The builder takes the larger of each pair and adds the two
   (`0x002FEC34`-`0x002FEC7E`).
4. **Inner values.** `a = 0x00320D70(actor, row, weaponRow, 0)` and `b = 0x00320D70(..., 1)`
   (`0x002FEC83`, `0x002FEC9A`).
5. **The reach.** `R = 0x00309300(row, weaponId)` (`0x002FECC6`).
6. **Authored or proportional.** The bands are authored only when both `a` and `b` are non-zero: a
   zero `a` skips the test of `b` (`0x002FECAA`), a zero `b` fails it (`0x002FECB1`); an unordered (NaN)
   compare counts as non-zero. Authored: near = `a`, middle = `a + b`, reach = `a + b + R`
   (`0x002FECD2`-`0x002FECD9`). Otherwise near = `0.6 R` (`0x008F3100`), middle = `0.8 R` (`0x008F3108`),
   reach = `R` (`0x002FECDF`-`0x002FECF8`).
7. The body-size sum is added to all three, and each output is stored only when its pointer is
   non-null (`0x002FECFB`-`0x002FED32`). The function returns 0.

### The reach

`0x00309300` (169 bytes) takes `(actionRow, weaponId)`. It tests the weapon id as a
class-6 (equipment) id with `0x00322C50(6, id, 0)` and resolves its row (`0x00309319`-`0x0030935E`). A null
action row gives 0.0 (`0x00309364`). When bit `0x4000000` of the row's flag word `+0x0C` is clear,
the reach is the row's byte `+0x05`; when it is set, the reach is the equipment row's byte `+0x18`,
or 0.0 when there is no equipment row (`0x00309377`-`0x0030938B`). The byte is divided by 10.0
(`0x008F8180`, `0x0030939B`).

### The inner values

`0x00320D70` (146 bytes) takes `(actor, actionRow, equipmentRow, component)` and tests bit `0x4000000` of the
action row's flag word `+0x0C` (`0x00320D74`):

- **Bit `0x4000000` clear:** the action row's byte `+0x02 + component`, divided by 10.0 - `+0x02` is the near
  value and `+0x03` the middle value (`0x00320DE1`-`0x00320DF5`).
- **Bit `0x4000000` set:** the equipment row's kind byte `+0x25` (kind 0 for a null row, `0x00320DAF`). Kind 2,
  or any kind above 5, gives 0.0 (`0x00320D93`-`0x00320DA2`). Otherwise the parameter number is the dword
  at `0x01EED288 + (component + kind * 2) * 4` (table below).
- **The parameter's value** comes from `0x003204E0(object, number, &out)`, the object being the first
  argument's `+0x10` (`0x00320DC4`) and `out` preset to 0.0 (`0x00320D86`); a negative return gives 0.0
  (`0x00320DB1`-`0x00320DD1`).

| Equipment kind | Near parameter | Middle parameter |
|---:|---:|---:|
| 0 | 13 | 12 |
| 1 | 15 | 14 |
| 3 | 19 | 18 |
| 4 | 21 | 20 |
| 5 | 23 | 22 |

`0x003204E0` reads numbers 12-23 through `0x002ECE50(object, dword at 0x01EED320 + number * 4)` (the
character parameter ids `0x09000D0E`-`0x09001819`, `0x01EED350`) and multiplies the result by the float
at `[object+0xB8]+0x28` (the third output of `0x00265240`). Numbers 24, 26, 28 and 31 take the
integer path instead: `0x002ECE80(object, id)` hands the same character record id, with the same null
and -1 guards, to `0x003E6310` (`0x002ECE80`-`0x002ECEA0`), and `0x003204E0` stores the returned dword as it
is (`0x00320580`-`0x00320590`).

Each of the three guards makes `0x002ECE80` answer the integer 0 (`0x002ECE9E`), and the
id it passes on is the low word of the dword at `[object + 0xC0]`, zero-extended
(`0x002ECE96`).

`0x002ECE50` returns 0.0 when the object or `[object+0xC0]` is null or the dword there is -1 (`0x002ECE53`-`0x002ECE64`);
otherwise it passes the low 16 bits of that dword, zero-extended (`0x002ECE66`), to `0x003E6150`, which keeps only
those 16 bits (`0x003E615C`). That reads the parameter from the character's parameter block (`0x004FE270`)
and multiplies it by the float at `+0x26C` of that character's `0x740`-byte record at `0x022C6F28`.

### The gap to the near value

`0x00320E10(unit, target)` answers how far the unit stands beyond its near value for the current action. Its one direct
call is the view builder's, with target 0 ([animation-driven
movement](../Movement-And-Pathfinding/animation-driven-movement.md); `0x0031AF77`-`0x0031AF82`).

The object is the target's `+0x10`, or with target 0 the actor `0x003588B0([unit+0x710])` that the unit's focus handle
resolves to while `0x02089340` has bit `0x10`; without an object the answer is 0.0 (`0x00320E2C`-`0x00320E56`).

It answers 0.0 for an action id `+0x714` above `0x21E` or a missing action row (`0x00320E5B`-`0x00320EBC`, `0x0032104C`). It
finds the weapon row as the builder does in steps 1 and 2 (`0x00320EC2`-`0x00320F37`), and answers 0.0 when the action
row's flag word has bit `0x4000000` and the weapon row is missing or has kind byte `+0x25` 2 (`0x00320F39`-`0x00320F50`).

Otherwise it reads `a = 0x00320D70(unit, row, weaponRow, 0)` and `b = 0x00320D70(..., 1)` (`0x00320F6A`, `0x00320F82`) and
answers 0.0 when either is 0 (`0x00320F87`-`0x00320F9B`).

The answer is `max(0, d - a - own - other)`: `d` is the x/z distance `0x004686D0` from the unit's `+0xE0` to the
object's position (`0x00265020`; `0x00320FEE`, `0x00321017`). `own` is the larger of the `0x00265090` pair of the unit's
`[unit+0x10]` (`0x0030A130`, `0x00321027`; `0x0030A134`-`0x0030A14D`) and `other` the larger of the object's pair (`0x0030A160`,
`0x00320FF6`; `0x0030A16E`-`0x0030A179`), the rule of the builder's step 3. When `a` is negative, `other` is added instead
(`0x00320FFB`-`0x00321004`, `0x00321022`-`0x00321043`).

### Spacing

`0x00319110(block, p, q)` copies the 16 bytes at `p` to block `+0x80` and those at `q` to `+0x90`; a null `p` or `q` is
read as the block's own `+0x50` (`0x00319110`-`0x00319130`).

`0x00338140` (839 bytes) runs per step on a movement context `ctx` built by `0x00336710`:
`ctx+0x00` is the unit's own position (block `+0x60`), `ctx+0x30` the reference-target point (block
`+0x90`, stored by `0x00319110`), `ctx+0x40` the target unit's live position, `ctx+0x100` and
`ctx+0x108` both the movement block, `ctx+0xF0` the acting unit and `ctx+0xF8` the target unit
(`0x00336733`-`0x003367BB`). Below, "the block" is that movement block.

1. It stops (speed `ctx+0xB0` = 0, bits `0x7FE0` of block `+0x00` cleared) and returns at once (`0x00338475`-`0x00338485`)
   when the unit in the block's slot `+0x177` has the id held at block `+0x150` (`0x00338178`-`0x00338194`), or when the
   unit is within 0.1 (`0x008C5F6C`, XZ) of the target's live position (`0x003381A1`-`0x003381B3`).
2. **Mutual targets.** When the target's focus handle `[target+0x710]` resolves (`0x0031B7E0`) to the
   acting unit and the unit's middle (block `+0x124`) is larger than the target's (target `+0x1A4`),
   the near value used is the target's (`+0x1A0`); otherwise its own (block `+0x120`)
   (`0x00338201`-`0x0033823F`).
3. **Too far** when the XZ distance `d` from the unit to the reference-target point
   (`0x0033826E`) exceeds `min(middle + 2.0, reach)` (`0x01CEBC08`, `0x00338253`-`0x0033827D`): bit `0x2` of
   block `+0x38` (approach). **Too close** when `d < near + 0.05` (`0x008F30E8`) and `0x003341A0`
   agrees: bit `0x4` of block `+0x38` (back off) (`0x00338281`-`0x0033829B`).
4. Approach is dropped when the block's stop distance `+0xD0` is larger than `d`, and back-off when
   `d` is larger than it (`0x0033829F`-`0x003382DE`). When the pair clearance test `0x0033D660` returns 0,
   the approach bit is set (`0x003382F2`-`0x00338301`).
5. **Approach** runs the pacing step `0x00337A50` and then `0x0033A720`; a non-zero pacing result clears
   bits `0x7FE0` of block `+0x00` (`0x00338305`-`0x00338326`).
6. **Back-off**, when bit `0x2` of block `+0x38` is clear and bit `0x4` set (`0x00338305`-`0x00338333`), tests a step with
   `0x00335B60`: if it returns 0 the unit moves away at the block's speed `+0xF8` with heading `ctx+0xB4` (turn limit
   `0x003364D0`), otherwise the back-off bit is cleared (`0x00338339`-`0x003383BC`).
7. **Neither:** the avoidance manoeuvre `0x003343D0` runs (and `0x0033BAA0` when it starts)
   (`0x003383C2`-`0x003383D1`).
8. **After each of steps 5-7** (`0x003383D6`): when neither bit `0x2` nor bit `0x4` of block `+0x38` is set and bits
   `0x7FE0` of block `+0x00` are clear, the unit stops (speed `ctx+0xB0` = 0) and turns to face the target (`ctx+0xBC`
   takes `0x003364D0(ctx, h)`), `0x0033BC80` runs on the point (own x, 0, own z, 1.0), and bits `0x7FE0` are cleared again
   (`0x003383D6`-`0x00338442`).
9. The `h` of step 8 is the heading between the unit and the target's live position
   `ctx+0x40` (`0x00203080`, `0x004687F0`, `0x003381C1`-`0x003381F7`, passed at `0x003383EC`).

Step 1 reads the unit with no null test (`0x0033818B`); `0x00236820` answers null for a slot not below the count at
`0x0208E6A0` (`0x0023682C`-`0x00236842`), so such a slot faults.

In step 6 the step heading comes from `0x00203080(out, ctx, ctx + 0x40)` with the result's
y set to 0 and `0x004687F0` on it; the test is `0x00335B60(ctx, heading, 0, 0.1, 0.8, 0)`
(`0x00338339`-`0x00338382`). On a 0 answer `ctx+0xB0` takes the dword `+0xF8` of the object
at `ctx+0x108`, `ctx+0xB4` takes that heading and `ctx+0xBC` takes `0x003364D0(ctx, h)`,
h being the heading `0x004687F0` gave earlier for `0x00203080(out, ctx + 0x40, ctx)`
(`0x003381C1`-`0x003381F7`, `0x0033838B`-`0x003383B2`).

### The back-off condition

`0x003341A0` returns 1 only when bit `0x1` of block `+0x38` is set, both
units exist and differ, `0x0030BCB0(unit, target, 0)` is 0 (the relationship class from `0x0030AB40` is
above 1), and the acting unit is not on the enemy side (stats byte `+0x05` not 1, or no stats record at
`+0x698`, `0x003341F5`) or has bit `0x2` of byte
`+0x21` of its `[unit+0xE68]` record set (`0x003341A6`-`0x0033420A`).

### Pacing

`0x00337A50` (442 bytes) runs only while bit `0x100` of block `+0x3C` is set, the
acting unit's class from `0x002F8E70` is 1, the class of the unit the target is focused on is not 1, and
the speed `ctx+0xB0` is non-zero; otherwise it clears bit `0x100` and returns 0 (`0x00337A74`-`0x00337ACB`,
`0x00337BDF`). `0x002F8E70` returns 1 for a party-side unit (stats byte `+0x05` = 0) whose type id (byte
`+0x04`) is outside the Esper band `0x1B`-`0x27`, and 2 inside it (`0x002F8E90`).

1. The aim point is `middle + 0.7 * (reach - middle)` (`0x008F3104`, `0x00337ADF`-`0x00337AFB`); `rem` is
   the XZ distance from the unit to the target's live position minus the aim. A negative `rem`
   returns 0 (`0x00337B0F`).
2. The remaining charge ticks are `([unit+0x76C] - [unit+0x768])` divided by the charge per tick
   `0x002F9C00(unit)`. If that is not larger than `rem` divided by the fast speed (block `+0xFC`), pacing
   is abandoned: bit `0x100` is cleared and 0 returned (`0x00337B26`-`0x00337B50`).
3. While the elapsed ticks `[unit+0x768] / step` are fewer than `30 * [0x01DFE0B4]` (`0x00337B75`), the
   unit stands (speed 0). After that it stands while the remaining ticks exceed `rem` divided by the
   normal speed (block `+0xF8`), and walks at the normal speed otherwise (`0x00337B80`-`0x00337BD7`).
   Either way it returns 1.

`0x01DFE0B4` is 1 as shipped; `0x001EDDC0` sets it to 2 (`0x001EDDF2`) while setting the per-frame scale
`0x01DFE0BC` to 0.5, so the standing window is 30 ticks at the shipped setting and 60 after that switch.

## State

| Field | Width | Meaning | Written by |
|---|---|---|---|
| unit `+0x6D4` | `f32` | near | `0x002FEB80` via `0x00304AB9` |
| unit `+0x6D8` | `f32` | middle | `0x002FEB80` via `0x00304AB9` |
| unit `+0x6DC` | `f32` | reach | `0x002FEB80` via `0x00304AB9` |
| unit `+0x1A0` (block `+0x120`) | `f32` | near, as movement reads it | `0x00304BF6` |
| unit `+0x1A4` (block `+0x124`) | `f32` | middle, as movement reads it | `0x00304BFF` |
| unit `+0x1A8` (block `+0x128`) | `f32` | reach, as movement reads it | `0x00304C0F` |

## Modding notes

- The action row's byte `+0x05` is the reach times 10 for actions without bit `0x4000000` of `+0x0C`; bytes
  `+0x02` and `+0x03` are near and middle times 10, used only when both are non-zero. In the shipped
  `battle_pack.bin`, 6 action rows set them (`1, 20` three times, `1, 15` twice, `20, 20` once) and
  none of those has bit `0x4000000`.
- With bit `0x4000000` set, these functions use the equipment row instead of the action row's `+0x05`,
  `+0x02` and `+0x03`: the reach is the equipment row's byte `+0x18` divided by 10 (`+0x18 / 10.0`,
  `0x0030939B`), and near and middle are
  character parameters chosen by the equipment row's kind byte `+0x25`. 35 shipped action rows have bit `0x4000000`.
- Shipped equipment reaches by kind (`+0x18`): kind 1 10-20, kind 2 100-250, kind 3 10-20, kind 4
  10-30, kind 5 10-20; kind 0 (305 rows) 0-90.
- Unarmed is equipment id `0x1000` with reach byte 10, so `0x00309300` gives an unarmed character's
  weapon-flag actions a reach of 1.0; the empty hand `0xFFFF` fails the bound and gives 0.
- The fallback proportions are the floats at `0x008F3100` (0.6) and `0x008F3108` (0.8); the approach
  margin is `0x01CEBC08` (2.0, a constant shared with other code), the back-off margin `0x008F30E8`
  (0.05), the pacing aim `0x008F3104` (0.7), and the pacing wait the immediate `0x1E` at `0x00337B75`.

## Related

- [The action definition row](action-definition-row.md) - the 60-byte row
  whose bytes `+0x02`, `+0x03`, `+0x05` and flag word `+0x0C` these functions read.
- [The battle unit field map](../Characters-And-Objects/battle-unit-fields.md) - where
  the three distances sit on the unit.
- [Battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)
  - the movement solver that runs the spacing and pacing steps.
- [The gap to the near value](#the-gap-to-the-near-value) - `0x00320E10`, the inner values' second reader.
- [The FCP character parameter block](../Graphics/model-files-cm-ca.md)
  - the per-character parameters behind weapon-flag actions.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x00203080` is called by `0x00362850`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Script VM: `0x00265020` is called by `0x0033FD60`, `0x00344AF0`, `0x00345180`, `0x00345830`, `0x003461B0`, `0x00346710`,
  `0x00346D40`, `0x00347170`, `0x00347580`, `0x003478A0`, `0x00347AB0`, `0x00347FF0`; `0x00265020` is also called by `0x0034BE50`,
  `0x0034CC00`, `0x00350DD0`, `0x003516E0`, `0x003562B0`, `0x00357DE0`, `0x0050E060`, `0x0050F6E0`, `0x00510040`, `0x00510080`,
  `0x005100C0`.
- Script VM: `0x004686D0` is called by `0x00344390`, `0x003448F0`, `0x00345630`; those functions are documented on
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [bestiary](../Enemy-Spawning/bestiary.md).
- Spawn encounter lifecycle: `0x00265020` is called by `0x00234AF0`, `0x00234DA0`, `0x002350C0`; those functions are
  documented on [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [frame update order](../Engine-Core/frame-update-order.md).
