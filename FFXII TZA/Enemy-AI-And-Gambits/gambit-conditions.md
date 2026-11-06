---
title: "Gambit conditions: every target condition with its id, what it tests, which target it picks and its shipped name"
kind: "reference"
category: "Enemy AI and gambits"
addresses: "0x02EBF0D8, 0x00238880, 0x00301AD0, 0x003087E0, 0x00308C20, 0x0031D034, 0x0031D0BE, 0x00327DE0"
---

## What it lists

A gambit line pairs a target condition with an action. The conditions are the 256 rows of `battle_pack.bin`
section 7, 32 bytes each, bound to `0x02EBF0D8` by `0x00238880` (`0x00238895`-`0x0023889E`). A condition's id is
`0x6000` + row; the id check accepts `0x6000` up to `0x6000` + row count - 1 (`0x00322DD4`, `0x0032302E`-`0x0032303B`).

The name the menu shows comes from the row word `+0x14`: section 61, sub-table `word >> 11`, entry
`word & 0x7FF` (`0x0031D034`-`0x0031D08A`). Every row uses sub-table 6. The help line comes from the row word
`+0x04`, text id 16000 + row, which is entry `row` of `listhelp_targetchip.bin` (`0x0031D0BE`). Row 255 has no
help id and no place on the menu.

### How a condition is tested

When a gambit list is built, each line's condition row becomes up to three tests in the walked order
([Gambits](gambits.md) has the layouts). The evaluator `0x00301AD0` runs each test over the candidate units:

1. The relation filter `0x0030BD00` keeps foes, allies or the character only ([Gambits](gambits.md) has the
   relation rules, including the enmity a foe must hold).
2. The test keeps the units that pass it, or, for a highest or lowest test, the units with the best value.
3. The target is picked from what the first test kept (`0x003017BF`, `0x003087E0`). A second test only has to
   keep at least one unit; in 44 of the 46 rows with one, it tests the character itself.

A row whose test keeps no unit fails the line, and the walk goes on to the next line.

The "on screen" test of rows such as `Foe: nearest visible` keeps a unit only when `0x00322360(unit)` returns
non-zero (`0x00303185`-`0x00303197`). That test builds a box from the unit's position and size and checks it against
the view-projection matrix `0x02AEDDF0` through `0x0046C0D0`
([Scripted camera](../Graphics/scripted-camera.md)), so it follows the current camera.

### Values worked out once per test

`0x00301AD0` loops over the candidates itself (`0x0030356B`-`0x00303590`). It sets a flag for the first candidate
(`0x00301B55`) and clears it before each later one (`0x0030356B`). Five tests work a value out for the first candidate,
store it in a global and read it back for the others:

| Global | Type | Test | Stored for the first candidate |
|---|---|---|---|
| `0x022BE968` | `void*` | 34/35, check 18 | the list `0x022C1788` (`0x003026FE`): the units of party slots 0-3 that are in play (`0x00302710`-`0x00302755`), as in [Enemy order sets](enemy-order-sets.md) |
| `0x022BEB84` | `i32` | 34/35, check 18 | how many units that list holds (`0x0030275F`; read at `0x00302767` and `0x003027B8`) |
| `0x022BED98` | `void*` | 34/35, check 27 | the combatant `0x0031B770` returns for `v` (`0x00302AF0`); each candidate is compared with it (`0x00302B0C`) |
| `0x022C17A8` | `void*` | 38/39 | the unit `0x002367A0` returns for definition selector `s` (`0x00302D2A`; read at `0x00302D43`) |
| `0x022BED94` | `i32` | 64/65 | 1 when `0x00309EC0` reports at least `10 x s` of the line's item, else 0 (`0x003032F8`; read at `0x00303300`) |

The opcode and check numbers are those of [Enemy order sets](enemy-order-sets.md) (`0x00301EB8`, `0x003024BC`). No
instruction outside `0x00301AD0` reads or writes these five. The clear `0x0030FE60` stops at
`0x022BEB84` and `0x022BED94`, exclusive (`0x0030FE69`, `0x0030FE89`), so it clears neither.

### How the target is picked

| Rule | Conditions | Sites |
|---|---|---|
| random | "any" conditions (`Foe: any`, `Ally: any`, the gated `any` rows) | `0x00301ECC` sets pick rule 1; `0x00308B0D`-`0x00308B19`, a draw of the shared LCG `0x00328370` ([Random number generators](../Random-Numbers/random-number-generators.md)) |
| highest or lowest HP %, MP % or HP | `HP >= 70%`, `HP < 50%`, `MP < 30%`, `HP < 2,000` and the like | `0x003022C7`, `0x00302EDF` set key type 1 and pick 2 or 3; `0x003089D7`, `0x00308A73` |
| nearest | every other condition, and ties between equal highest or lowest values | `0x00308B2F`-`0x00308B76`, squared distance on the ground plane |

So "Ally: HP < 50%" keeps the allies whose `pct = hp x 100 / max` (`0x003209E0`, 64-bit, 0 for a maximum of 0; `hp`
and `max` as below) is below 50 and picks the lowest `pct` (`0x0030228A`-`0x003022CE`), and "Foe: status =
Poison" picks the nearest poisoned foe.

### HP and MP in a condition

The HP and MP a condition compares are previewed by `0x00308C20`. It starts from current HP (`+0x48`) or MP
(`+0x4C`) and, when the deciding character is a party record and the line's action row has bit `0x1000` (HP) or
bit `0x8000` (MP) of word `+0x2C`, adds the previewed result of every action already committed against the unit
(the mask `+0xEA4`, each attacker's action `+0x714`, `0x00308B90`). The sum is clamped to 0 and the maximum
(`0x00308C86`-`0x00308D7D`). The action row is the `0x02EBF138` row of the action id (`0x00308C26`-`0x00308C80`).

The maximum is max HP `+0x24`, doubled under Bubble (bit `0x10000000`), or under Disease (bit `0x10000`,
tested first, so it wins over Bubble) the current HP and at least 1, both bits of `+0x64 | +0x3C`
(`0x00308C9C`-`0x00308CBD`). For MP it is max MP `+0x28`, or 0 when augment 39 (Emptiness) is in either layer
([Augments](../Damage-And-Battle-Formulas/augments.md)). MP and max MP are signed 16-bit reads (`0x00308CC5`, `0x00308CD1`).

A unit with max MP 0 or augment 39 (Emptiness) never passes an MP percentage test: `(i16)r[+0x28] == 0` fails it,
as do `(i8)r[+0x6C] < 0` and `(i8)r[+0x7C] < 0` (bit `0x80`, augment 39, of either layer), with `r = [unit + 0x698]`
(`0x00302F37`-`0x00302F59`; `cmp byte ptr [rax + 0x6c], r13b` with `r13 = 0`).

### Units the action would not change

The picker `0x003087E0` asks `0x003083B0(unit, candidate, action)` about every unit the first test kept and keeps
only those it answers 0 for: a unit answered 1 never becomes the highest, lowest or nearest, and is left out of
a random pick (`0x00308848`-`0x00308AD0`). When no unit is kept, the order fails (`0x003017C4`-`0x003017CD`), and the
walk goes on to the next line.

`0x003083B0` answers 0 at once when the deciding unit is an enemy (stats `+0x05` = 1), when the action id is
above `0x21E` (`0x003083E1`-`0x003083FD`), or when the action row has bit `0x20` of `+0x36` and the candidate's byte
`+0x55` is `0x0D` (`0x0030844B`-`0x00308457`). Otherwise it answers 1 only when every effect the action row marks
would change nothing on the candidate (`0x0030846A`-`0x003085E6`):

| Row bit | Effect | Changes nothing when | Sites |
|---|---|---|---|
| `+0x2C` bit `0x1000` | restores HP | current HP `+0x48` is at least the maximum: max HP `+0x24`, doubled under Bubble, or under Disease the current HP and at least 1 | `0x0030846A`-`0x003084B1` |
| `+0x2C` bit `0x8000` | restores MP | current MP `+0x4C` is at least max MP `+0x28`, which counts as 0 when byte `+0x6C` or `+0x7C` is negative | `0x003084B3`-`0x003084E1` |
| `+0x36` bit `0x2` | removes statuses | `0x0031C500` finds none of them on the candidate (the action's mask from `0x003872D0` ANDed with the statuses `+0x64` and `+0x3C`), or each one is also removed by the action of a unit already committed against it | `0x003084EF`-`0x00308565` |
| `+0x36` bit `0x1` | adds statuses | `0x00320AF0` finds no status still to add, or each one is also added by the action of a unit already committed against it | `0x0030856F`-`0x003085DE` |

The units already committed against the candidate are the bits of its mask `+0xEA4`, each unit's action being
its `+0x714` ([Committing an action](../Battle-Actions/action-commit.md); `0x00308520`-`0x00308535`, `0x003085A0`-`0x003085B4`).

`0x00320AF0(user, candidate, action)` returns the action's status mask `+0x18` without the candidate's statuses
`+0x64 | +0x3C`, and 0 when either stats record is missing (`0x00320AF9`-`0x00320B13`). The mask comes from
`0x003875D0`, which returns it only for a row with bit `0x1` of `+0x36` set and bit `0x200` of `+0x2C` clear
(`0x00387629`). An action row with none of the four bits is never passed over.

So an "Ally: status = Poison" line whose action removes Poison skips an ally whose Poison an action already
committed against it removes, and an "Ally: any" line whose action restores HP skips allies at full HP.

### Threshold tables

| Test | Values | Table |
|---|---|---|
| HP % | `90`, `80`, `70`, `60`, `50`, `40`, `30`, `20`, `10`, `0`; no condition uses `0` | `0x00D102E0` |
| HP | `100,000`, `50,000`, `10,000`, `5,000`, `3,000`, `2,000`, `1,000`, `500` (the next table starts at `0x00D10370`, read on its own at `0x00302F20`) | `0x00D10350` |
| MP % | ten times the row's sub-selector byte | `0x003032AF`-`0x003032B4` |
| item count | ten times the sub-selector byte | `0x003032EE`-`0x003032F5` |
| summon timer | `20`, `30`, `60`, `90`, `120` | `0x00D10380` |

### Conditions that test something narrower or wider than their help line

- **Foe: targeted by ally** and **Foe: not targeted by ally** take the foe with the most or fewest units
  committed against it (`+0xEA8`, `0x00302123`). With no foe targeted, "targeted by ally" still matches every
  foe and picks the nearest.
- **Foe: fire-vulnerable** and the other seven "-vulnerable" rows admit a foe that does not absorb the
  element (stats `+0x41` bit clear, `0x003023C9`), whether or not it is weak to it.
- **Self: 2+ foes present** and the other "present" rows count the units in the character's own perception
  list (`+0xBC4`, `0x003031C4`-`0x00303216`), for the Ally and Foe forms too.
- **Ally: item AMT >= 10**, **Foe: item AMT >= 10** and **Self: item AMT >= 10** count the item the line's
  action uses (`0x003032C0`-`0x003032F5`).
- Row 255, `0x60FF`, is named "NOT USED no_chip" and is not on the menu. It takes the foe with the highest max
  HP while the summon timer, battle state `+0x5AD8`, is below 20 (`0x00303523`-`0x00303554`); every Esper's
  preset starts with it ([Gambits](gambits.md)).

### Where each gambit condition comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [Shops](../Items-Equipment-Shops-And-Licenses/shops.md), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or the value alone where no story script writes it, which is so for 500 (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](../Items-Equipment-Shops-And-Licenses/shops.md), "Choosing a list"). The story test is the story counter at least the threshold (`0x002FADF3`-`0x002FAE0D`).

No script writes story progress 500. The values the scripts write go from 490 (After the captive Penelo) to 520 (After the floating continent), so a list that waits on 500 goes on sale at 520.

The Clan Provisioner is a Mysterious Merchant in Muthru Bazaar (Rabanastre) until bit `0x1` of script global byte `0x041D` is set; only then does its actor take the shop's name (`rbn_a02`). Montblanc sets that bit the first time the player talks to him in The Clan Hall (Rabanastre), with the message "You are now a member of Clan Centurio!" (`rbn_a14`).

`-` means that none of these tables names a source. No treasure chest gives a gambit condition: the chest records' item words name items, equipment, loot, magicks and technicks ([Treasure chests](../World-Areas-And-Travel/treasure-chests.md)).

## Columns

[`gambit-conditions.tsv`](gambit-conditions.tsv), one row per condition:

| Column | Meaning |
|---|---|
| `condition_id` | `0x6000` + row |
| `row` | the row of section 7, 0-255 |
| `name` | the name the gambit menu shows; the font glyph `≧` (byte `0xC4`) is written `>=` |
| `help_text` | the help line, or `-` |
| `target` | Foe, Ally or Self: which units the first test looks at |
| `test` | what the first test keeps; stats offsets are the unit's stats record ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) |
| `also_needs` | the second test, which must find at least one unit, or `-` |
| `pick` | the rule that chooses one target from what the first test kept |
| `menu_position` | column and row on the gambit menu grid built by `0x00238880` (`0x002389DA`-`0x002389F9`), or `-` |
| `sites` | the evaluator cases that show the row, and the relation filter |
| `sources` | where the gambit condition is obtained, one part per kind of source, with each shop's place and opening, clan ranks by name ("Where each gambit condition comes from" above); `-` when no table names a source |

## Related

- [Gambits](gambits.md) - the walk, the relation rules and the gambit layouts.
- [Enemy AI](enemy-ai.md) - the same tests used by enemy orders.
- [Enemy order sets](enemy-order-sets.md) - every opcode of the selector `0x00301AD0`, beyond the shipped gambit conditions.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the stats offsets the tests read.
- [Elements](../Damage-And-Battle-Formulas/elements.md) - the weak and absorb bytes.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Core runtime: `0x0030FE60` is called by `0x002341C0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Items equipment shops license: `0x00309EC0` is called by `0x00317930`; those functions are documented on
  [party table](../Party/party-table.md).
- Platform online achievements: `0x00309EC0` is called by `0x00315E90`; those functions are documented on
  [gil](../Rewards-EXP-Gil-And-Loot/gil.md).
- Status periodic terminal: `0x0031B770` is called by `0x00310DB0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
