---
title: "Gambit conditions: every target condition with its id, what it tests, which target it picks and its shipped name"
kind: "reference"
category: "Enemy AI and gambits"
summary: "All 256 gambit target conditions of battle_pack.bin section 7, ids 0x6000-0x60FF: for each, the name and help text the game shows, whether it looks at foes, allies or the character, the test it runs, the second test some conditions make on the character, the rule that picks one target when several match, its place on the gambit menu, and the instructions that show it."
addresses: ["02EBF0D8", "00238880", "00301AD0", "003087E0", "00308C20", "0031D034", "0031D0BE", "00327DE0"]
---

# Gambit conditions: every target condition with its id, what it tests, which target it picks and its shipped name

## What it lists

A gambit line pairs a target condition with an action. The conditions are the 256 rows of `battle_pack.bin`
section 7, 32 bytes each, bound to `02EBF0D8` by `00238880` (`00238895`-`0023889E`). A condition's id is
`0x6000` + row; the id check accepts `0x6000` up to `0x6000` + row count - 1 (`00322DD4`, `0032302E`-`0032303B`).

The name the menu shows comes from the row word `+0x14`: section 61, sub-table `word >> 11`, entry
`word & 0x7FF` (`0031D034`-`0031D08A`). Every row uses sub-table 6. The help line comes from the row word
`+0x04`, text id 16000 + row, which is entry `row` of `listhelp_targetchip.bin` (`0031D0BE`). Row 255 has no
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

The HP and MP a condition compares are previewed by `00308C20`. It starts from current HP (`+0x48`) or MP
(`+0x4C`) and, when the deciding character is a party record and the line's action row has bit 12 (HP) or
bit 15 (MP) of word `+0x2C`, adds the previewed result of every action already committed against the unit
(the mask `+0xEA4`, each attacker's action `+0x714`, `00308B90`). The sum is clamped to 0 and the maximum
(`00308C86`-`00308D7D`).

The maximum is max HP `+0x24`, doubled under Bubble, or under Disease the current HP and at least 1. For MP it
is max MP `+0x28`, or 0 when effect 39 is in either layer ([Augments](../Damage-And-Battle-Formulas/augments.md)). A
unit with max MP 0 or effect 39 never passes an MP percentage test (`00302F37`-`00302F59`).

### Threshold tables

| Test | Values | Table |
|---|---|---|
| HP % | 90, 80, 70, 60, 50, 40, 30, 20, 10, 0 | `00D102E0` |
| HP | 100,000, 50,000, 10,000, 5,000, 3,000, 2,000, 1,000, 500 | `00D10350` |
| MP % | ten times the row's sub-selector byte | `003032AF`-`003032B4` |
| item count | ten times the sub-selector byte | `003032EE`-`003032F5` |
| summon timer | 20, 30, 60, 90, 120 | `00D10380` |

### Conditions that test something narrower or wider than their help line

- **Foe: targeted by ally** and **Foe: not targeted by ally** take the foe with the most or fewest units
  committed against it (`+0xEA8`, `00302123`). With no foe targeted, "targeted by ally" still matches every
  foe and picks the nearest.
- **Foe: fire-vulnerable** and the other seven "-vulnerable" rows admit a foe that does not absorb the
  element (stats `+0x41` bit clear, `003023C9`), whether or not it is weak to it.
- **Self: 2+ foes present** and the other "present" rows count the units in the character's own perception
  list (`+0xBC4`, `003031C4`-`00303216`), for the Ally and Foe forms too.
- **Ally: item AMT >= 10**, **Foe: item AMT >= 10** and **Self: item AMT >= 10** count the item the line's
  action uses (`003032C0`-`003032F5`).
- Row 255, `0x60FF`, is named "NOT USED no-chip" and is not on the menu. It takes the foe with the highest max
  HP while the summon timer, battle state `+0x5AD8`, is below 20 (`00303523`-`00303554`); every Esper's
  preset starts with it ([Gambits](gambits.md)).

## Columns

`gambit-conditions.tsv`, one row per condition:

| Column | Meaning |
|---|---|
| `condition_id` | `0x6000` + row |
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
