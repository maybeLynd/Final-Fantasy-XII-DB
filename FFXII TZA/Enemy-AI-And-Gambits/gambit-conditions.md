---
title: "Gambit conditions: every target condition with its id, what it tests, which target it picks and its shipped name"
kind: "reference"
category: "Enemy AI and gambits"
addresses: "02EBF0D8, 00238880, 00301AD0, 003087E0, 00308C20, 0031D034, 0031D0BE, 00327DE0"
---

## What it lists

A gambit line pairs a target condition with an action. The conditions are the 256 rows of `battle_pack.bin`
section 7, 32 bytes each, bound to `02EBF0D8` by `00238880` (`00238895`-`0023889E`). A condition's id is
`6000`<sub>h</sub> + row; the id check accepts `6000`<sub>h</sub> up to `6000`<sub>h</sub> + row count - 1 (`00322DD4`, `0032302E`-`0032303B`).

The name the menu shows comes from the row word `+14`<sub>h</sub>: section 61, sub-table `word >> 11`, entry
`word & 7FFh` (`0031D034`-`0031D08A`). Every row uses sub-table 6. The help line comes from the row word
`+04`<sub>h</sub>, text id 16000 + row, which is entry `row` of `listhelp_targetchip.bin` (`0031D0BE`). Row 255 has no
help id and no place on the menu.

### How a condition is tested

When a gambit list is built, each line's condition row becomes up to three tests in the walked order
([Gambits](gambits.md) has the layouts). The evaluator `00301AD0` runs each test over the candidate units:

1. The relation filter `0030BD00` keeps foes, allies or the character only ([Gambits](gambits.md) has the
   relation rules, including the enmity a foe must hold).
2. The test keeps the units that pass it, or, for a highest or lowest test, the units with the best value.
3. The target is picked from what the first test kept (`003017BF`, `003087E0`). A second test only has to
   keep at least one unit; in 44 of the 46 rows with one, it tests the character itself.

A row whose test keeps no unit fails the line, and the walk goes on to the next line.

### How the target is picked

| Rule | Conditions | Sites |
|---|---|---|
| random | "any" conditions (`Foe: any`, `Ally: any`, the gated `any` rows) | `00301ECC` sets pick rule 1; `00308B0D`-`00308B19` |
| highest or lowest HP %, MP % or HP | `HP >= 70%`, `HP < 50%`, `MP < 30%`, `HP < 2,000` and the like | `003022C7`, `00302EDF` set key type 1 and pick 2 or 3; `003089D7`, `00308A73` |
| nearest | every other condition, and ties between equal highest or lowest values | `00308B2F`-`00308B76`, squared distance on the ground plane |

So "Ally: HP < 50%" picks the ally with the lowest HP percentage among those under half, and "Foe: status =
Poison" picks the nearest poisoned foe.

### HP and MP in a condition

The HP and MP a condition compares are previewed by `00308C20`. It starts from current HP (`+48`<sub>h</sub>) or MP
(`+4C`<sub>h</sub>) and, when the deciding character is a party record and the line's action row has bit 12 (HP) or
bit 15 (MP) of word `+2C`<sub>h</sub>, adds the previewed result of every action already committed against the unit
(the mask `+EA4`<sub>h</sub>, each attacker's action `+714`<sub>h</sub>, `00308B90`). The sum is clamped to 0 and the maximum
(`00308C86`-`00308D7D`).

The maximum is max HP `+24`<sub>h</sub>, doubled under Bubble, or under Disease the current HP and at least 1. For MP it
is max MP `+28`<sub>h</sub>, or 0 when effect 39 is in either layer ([Augments](../Damage-And-Battle-Formulas/augments.md)). A
unit with max MP 0 or effect 39 never passes an MP percentage test (`00302F37`-`00302F59`).

### Units the action would not change

The picker `003087E0` asks `003083B0(unit, candidate, action)` about every unit the first test kept and keeps
only those it answers 0 for: a unit answered 1 never becomes the highest, lowest or nearest, and is left out of
a random pick (`00308848`-`00308AD0`). When no unit is kept, the order fails (`003017C4`-`003017CD`), and the
walk goes on to the next line.

`003083B0` answers 0 at once when the deciding unit is an enemy (stats `+05`<sub>h</sub> = 1), when the action id is
above `21E`<sub>h</sub> (`003083E1`-`003083FD`), or when the action row has bit 5 of `+36`<sub>h</sub> and the candidate's byte
`+55`<sub>h</sub> is `0D`<sub>h</sub> (`0030844B`-`00308457`). Otherwise it answers 1 only when every effect the action row marks
would change nothing on the candidate (`0030846A`-`003085E6`):

| Row bit | Effect | Changes nothing when | Sites |
|---|---|---|---|
| `+2C`<sub>h</sub> bit 12 | restores HP | current HP `+48`<sub>h</sub> is at least the maximum: max HP `+24`<sub>h</sub>, doubled under Bubble, or under Disease the current HP and at least 1 | `0030846A`-`003084B1` |
| `+2C`<sub>h</sub> bit 15 | restores MP | current MP `+4C`<sub>h</sub> is at least max MP `+28`<sub>h</sub>, which counts as 0 when byte `+6C`<sub>h</sub> or `+7C`<sub>h</sub> is negative | `003084B3`-`003084E1` |
| `+36`<sub>h</sub> bit 1 | removes statuses | `0031C500` finds none of them on the candidate (the action's mask from `003872D0` ANDed with the statuses `+64`<sub>h</sub> and `+3C`<sub>h</sub>), or each one is also removed by the action of a unit already committed against it | `003084EF`-`00308565` |
| `+36`<sub>h</sub> bit 0 | adds statuses | `00320AF0` finds none still to add, or each one is also added by the action of a unit already committed against it | `0030856F`-`003085DE` |

The units already committed against the candidate are the bits of its mask `+EA4`<sub>h</sub>, each unit's action being
its `+714`<sub>h</sub> ([Committing an action](../Battle-Actions/action-commit.md); `00308520`-`00308535`, `003085A0`-`003085B4`).

`00320AF0(user, candidate, action)` returns the action's status mask `+18`<sub>h</sub> without the candidate's statuses
`+64h | +3Ch`, and 0 when either stats record is missing (`00320AF9`-`00320B13`). The mask comes from
`003875D0`, which returns it only for a row with bit 0 of `+36`<sub>h</sub> set and bit 9 of `+2C`<sub>h</sub> clear
(`00387629`). An action row with none of the four bits is never passed over.

So an "Ally: status = Poison" line whose action removes Poison skips an ally whose Poison an action already
committed against it removes, and an "Ally: any" line whose action restores HP skips allies at full HP.

### Threshold tables

| Test | Values | Table |
|---|---|---|
| HP % | `90`, `80`, `70`, `60`, `50`, `40`, `30`, `20`, `10`, `0` | `00D102E0` |
| HP | `100,000`, `50,000`, `10,000`, `5,000`, `3,000`, `2,000`, `1,000`, `500` | `00D10350` |
| MP % | ten times the row's sub-selector byte | `003032AF`-`003032B4` |
| item count | ten times the sub-selector byte | `003032EE`-`003032F5` |
| summon timer | `20`, `30`, `60`, `90`, `120` | `00D10380` |

### Conditions that test something narrower or wider than their help line

- **Foe: targeted by ally** and **Foe: not targeted by ally** take the foe with the most or fewest units
  committed against it (`+EA8`<sub>h</sub>, `00302123`). With no foe targeted, "targeted by ally" still matches every
  foe and picks the nearest.
- **Foe: fire-vulnerable** and the other seven "-vulnerable" rows admit a foe that does not absorb the
  element (stats `+41`<sub>h</sub> bit clear, `003023C9`), whether or not it is weak to it.
- **Self: 2+ foes present** and the other "present" rows count the units in the character's own perception
  list (`+BC4`<sub>h</sub>, `003031C4`-`00303216`), for the Ally and Foe forms too.
- **Ally: item AMT >= 10**, **Foe: item AMT >= 10** and **Self: item AMT >= 10** count the item the line's
  action uses (`003032C0`-`003032F5`).
- Row 255, `60FF`<sub>h</sub>, is named "NOT USED no-chip" and is not on the menu. It takes the foe with the highest max
  HP while the summon timer, battle state `+5AD8`<sub>h</sub>, is below 20 (`00303523`-`00303554`); every Esper's
  preset starts with it ([Gambits](gambits.md)).

## Columns

`gambit-conditions.tsv`, one row per condition:

| Column | Meaning |
|---|---|
| `condition_id` | `6000`<sub>h</sub> + row |
| `row` | the row of section 7, 0-255 |
| `name` | the name the gambit menu shows |
| `help_text` | the help line, or `-` |
| `target` | Foe, Ally or Self: which units the first test looks at |
| `test` | what the first test keeps; stats offsets are the unit's stats record ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) |
| `also_needs` | the second test, which must find at least one unit, or `-` |
| `pick` | the rule that chooses one target from what the first test kept |
| `menu_position` | column and row on the gambit menu grid built by `00238880` (`002389DA`-`002389F9`), or `-` |
| `sites` | the evaluator cases that show the row, and the relation filter |

## Related

- [Gambits](gambits.md) - the walk, the relation rules and the gambit layouts.
- [Enemy AI](enemy-ai.md) - the same tests used by enemy orders.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the stats offsets the tests read.
- [Elements](../Damage-And-Battle-Formulas/elements.md) - the weak and absorb bytes.
