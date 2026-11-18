[Home](../../README.md) / [Enemy AI and gambits](README.md) / Gambit conditions

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Gambit conditions: every target condition with its id, what it tests, which target it picks and its shipped name | reference | Enemy AI and gambits | Party gambits | All 256 gambit target conditions of battle_pack.bin section 7, ids 0x6000-0x60FF: for each, the name and help text the game shows, whether it looks at foes, allies or the character, the test it runs, the second test some conditions make on the character, the rule that picks one target when several match, its place on the gambit menu, and the instructions that show it. | 0x02EBF0D8, 0x00238880, 0x00301AD0, 0x003087E0, 0x00308C20, 0x0031D034, 0x0031D0BE, 0x00327DE0 |

## What it lists

A gambit line pairs a target condition with an action. The conditions are the 256 rows of `battle_pack.bin`
section 7, 32 bytes each, bound to `0x02EBF0D8` by `0x00238880`¹. A condition's id is
`0x6000` + row; the id check accepts `0x6000` up to `0x6000` + row count - 1².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00238895`-`0x0023889E` |
| ² | `0x00322DD4`, `0x0032302E`-`0x0032303B` |

</details>

The name the menu shows comes from the row word `+0x14`: section 61, sub-table `word >> 11`, entry
`word & 0x7FF`¹. Every row uses sub-table 6. The help line comes from the row word
`+0x04`, text id 16000 + row, which is entry `row` of `listhelp_targetchip.bin`². Row 255 has no
help id and no place on the menu.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031D034`-`0x0031D08A` |
| ² | `0x0031D0BE` |

</details>

Enemies are tested the same way: an enemy's own orders carry the same kind of tests a gambit line gets from its
condition, and the same code tests them. Of the 50,050 orders in the shipped area files, 3,336 carry exactly the tests
and flags of one gambit condition.

### How a condition is tested

When a gambit list is built, each line's condition row becomes up to three tests in the walked order
([Gambits](gambits.md) has the layouts). The evaluator `0x00301AD0` runs each test over the candidate units:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The relation filter `0x0030BD00` keeps foes, allies or the character only ([Gambits](gambits.md) has the relation rules, including the enmity a foe must hold). |   |
| 2 | The test keeps the units that pass it; a highest or lowest test instead gives the picker the value to compare and whether the highest or the lowest wins. |   |
| 3 | The target is picked from what the first test kept: the picker first drops the units the action would not change (below), then compares the rest, the nearest winning a tie. A second test only has to keep at least one unit; in 44 of the 46 rows with one, it tests the character itself. | `0x003017BF`, `0x003087E0` |

A row whose test keeps no unit fails the line, and the walk goes on to the next line.

The "on screen" test of rows such as `Foe: nearest visible` keeps a unit only when `0x00322360(unit)` returns
non-zero¹. That test builds a box from the unit's position and size and checks it against
the view-projection matrix `0x02AEDDF0` through `0x0046C0D0`
([Scripted camera](../Graphics/scripted-camera.md)), so it follows the current camera.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00303185`-`0x00303197` |

</details>

### Values worked out once per test

`0x00301AD0` loops over the candidates itself¹. It sets a flag for the first candidate² and clears it before each later one³. Five tests work a value out for the first candidate,
store it in a global and read it back for the others:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030356B`-`0x00303590` |
| ² | `0x00301B55` |
| ³ | `0x0030356B` |

</details>

| Global | Type | Test | Stored for the first candidate |
|---|---|---|---|
| `0x022BE968` | `void*` | 34/35, check 18 | the list `0x022C1788` (`0x003026FE`): the units of party slots 0-3 that are in play (`0x00302710`-`0x00302755`), as in [Enemy order sets](enemy-order-sets.md) |
| `0x022BEB84` | `i32` | 34/35, check 18 | how many units that list holds (`0x0030275F`; read at `0x00302767` and `0x003027B8`) |
| `0x022BED98` | `void*` | 34/35, check 27 | the combatant `0x0031B770` returns for `v` (`0x00302AF0`); each candidate is compared with it (`0x00302B0C`) |
| `0x022C17A8` | `void*` | 38/39 | the unit `0x002367A0` returns for definition selector `s` (`0x00302D2A`; read at `0x00302D43`) |
| `0x022BED94` | `i32` | 64/65 | 1 when `0x00309EC0` reports at least `10 x s` of the line's item, else 0 (`0x003032F8`; read at `0x00303300`) |

The opcode and check numbers are those of [Enemy order sets](enemy-order-sets.md)¹. No
instruction outside `0x00301AD0` reads or writes these five. The clear `0x0030FE60` stops at
`0x022BEB84` and `0x022BED94`, exclusive², so it clears neither.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301EB8`, `0x003024BC` |
| ² | `0x0030FE69`, `0x0030FE89` |

</details>

### How the target is picked

| Rule | Conditions | Sites |
|---|---|---|
| random | "any" conditions (`Foe: any`, `Ally: any`, the gated `any` rows) | `0x00301ECC` sets pick rule 1; `0x00308B0D`-`0x00308B19`, a draw of the shared LCG `0x00328370` ([Random number generators](../Random-Numbers/random-number-generators.md)) |
| highest or lowest HP %, MP % or HP | `HP >= 70%`, `HP < 50%`, `MP < 30%`, `HP < 2,000` and the like | `0x003022C7`, `0x00302EDF` set key type 1 and pick 2 or 3; `0x003089D7`, `0x00308A73` |
| nearest | every other condition, and ties between equal highest or lowest values | `0x00308B2F`-`0x00308B76`, squared distance on the ground plane |

So "Ally: HP < 50%" keeps the allies whose `pct = hp x 100 / max` (`0x003209E0`, 64-bit, 0 for a maximum of 0; `hp`
and `max` as below) is below 50 and picks the lowest `pct`¹, and "Foe: status =
Poison" picks the nearest poisoned foe.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030228A`-`0x003022CE` |

</details>

### HP and MP in a condition

The HP and MP a condition compares are previewed by `0x00308C20`. It starts from current HP (`+0x48`) or MP
(`+0x4C`) and, when the deciding character is a party record and the line's action row has bit `0x1000` (HP) or
bit `0x8000` (MP) of word `+0x2C`, adds the previewed result of every action already committed against the unit
(the mask `+0xEA4`, each attacker's action `+0x714`, `0x00308B90`). The sum is clamped to 0 and the maximum¹. The action row is the `0x02EBF138` row of the action id².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308C86`-`0x00308D7D` |
| ² | `0x00308C26`-`0x00308C80` |

</details>

`0x00308B90(a, b, action, which)` clears a `0x148`-byte result record on its stack with
`0x00861EC0`, sets bit `0x20` of the record's first dword and calls the resolver
`0x00385F60(action, a, b, record)`¹. It answers the record's dword
`+0x24` when `which` is not 0, and otherwise the signed high word of the dword `+0x28`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308BBB`-`0x00308BE3` |
| ² | `0x00308BE8`-`0x00308BF6` |

</details>

The maximum is max HP `+0x24`, doubled under Bubble (bit `0x10000000`), or under Disease (bit `0x10000`,
tested first, so it wins over Bubble) the current HP and at least 1, both bits of `+0x64 | +0x3C`¹. For MP it is max MP `+0x28`, or 0 when augment 39 (Emptiness) is in either layer
([Augments](../Damage-And-Battle-Formulas/augments.md)). MP and max MP are signed 16-bit reads².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308C9C`-`0x00308CBD` |
| ² | `0x00308CC5`, `0x00308CD1` |

</details>

A unit with max MP 0 or augment 39 (Emptiness) never passes an MP percentage test: `(i16)r[+0x28] == 0` fails it,
as do `(i8)r[+0x6C] < 0` and `(i8)r[+0x7C] < 0` (bit `0x80`, augment 39, of either layer), with `r = [unit + 0x698]`
(`0x00302F37`-`0x00302F59`; `cmp byte ptr [rax + 0x6c], r13b` with `r13 = 0`).

### Units the action would not change

The picker `0x003087E0` asks `0x003083B0(unit, candidate, action)` about the units the first test kept, the
candidate being `0x0031B760` of the entry's first qword, and keeps only those it answers 0 for: a unit
answered 1 never becomes the highest, lowest or nearest, and is left out of a random pick¹. A kept entry's 16 bytes are copied to the out list and its count dword `+4`
goes up by 1. When no unit is kept, the order fails², and the walk goes on to the
next line.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308848`-`0x00308AD0` |
| ² | `0x003017C4`-`0x003017CD` |

</details>

Where the pick is by a key, an int (list byte `+0x01` = 1) or a float (`+0x01` = 2) at the entry's `+8`,
an entry whose key is worse than the best so far is passed over with neither call¹. The best starts at the float
`0x02F973B8` for the lowest pick and at its negative for the highest, and at `0x7FFFFFFF` and `0x80000001`
for the int picks²: an entry beyond that start
is never kept, and one equal to it that is answered 0 is added.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003088A0`-`0x003088E4`, `0x00308944`-`0x00308984`, `0x003089F0`-`0x00308A29`, `0x00308A83`-`0x00308ABC` |
| ² | `0x0030892E`, `0x00308882`-`0x0030888A`, `0x00308A73`, `0x003089D7` |

</details>

An entry with a better key that is answered 0 becomes the only kept entry and its key the best; one with
the same key that is answered 0 is added. A keyed list whose byte `+0x02` is neither 3 (highest) nor 2
(lowest) keeps no entry¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308879`, `0x00308925`, `0x003089CE`, `0x00308A6A` |

</details>

`0x003083B0` answers 0 at once when the deciding unit is an enemy (stats `+0x05` = 1), when the action id is
above `0x21E`¹, or when the action row has bit `0x20` of `+0x36` and the candidate's byte
`+0x55` is `0x0D`². Otherwise it answers 1 only when the action
row marks at least one of the four effects below and every effect it marks would
change nothing on the candidate; a row that marks not one of them answers 0³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003083E1`-`0x003083FD` |
| ² | `0x0030844B`-`0x00308457` |
| ³ | `0x003083CD`, `0x0030846A`-`0x003085E6` |

</details>

| Row bit | Effect | Changes nothing when | Sites |
|---|---|---|---|
| `+0x2C` bit `0x1000` | restores HP | current HP `+0x48` is at least the maximum: max HP `+0x24`, doubled under Bubble, or under Disease the current HP and at least 1 | `0x0030846A`-`0x003084B1` |
| `+0x2C` bit `0x8000` | restores MP | current MP `+0x4C` is at least max MP `+0x28`, which counts as 0 when byte `+0x6C` or `+0x7C` is negative | `0x003084B3`-`0x003084E1` |
| `+0x36` bit `0x2` | removes statuses | `0x0031C500` finds none of them on the candidate (the action's mask from `0x003872D0` ANDed with the statuses `+0x64` and `+0x3C`), or each one is also removed by the action of a unit already committed against it | `0x003084EF`-`0x00308565` |
| `+0x36` bit `0x1` | adds statuses | `0x00320AF0` finds no status still to add, or each one is also added by the action of a unit already committed against it | `0x0030856F`-`0x003085DE` |

The units already committed against the candidate are the bits of its mask `+0xEA4`, each unit's action being
its `+0x714` ([Committing an action](../Battle-Actions/action-commit.md); `0x00308520`-`0x00308535`, `0x003085A0`-`0x003085B4`).

`0x00320AF0(user, candidate, action)` returns the action's status mask `+0x18` without the candidate's statuses
`+0x64 | +0x3C`, and 0 when either stats record is missing¹. The mask comes from
`0x003875D0`, which returns it only for a row with bit `0x1` of `+0x36` set and bit `0x200` of `+0x2C` clear². An action row with none of the four bits is never passed over.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00320AF9`-`0x00320B13` |
| ² | `0x00387629` |

</details>

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
  action uses¹.
- Row 255, `0x60FF`, is named "NOT USED no_chip" and is not on the menu. It takes the foe with the highest max
  HP while the summon timer, battle state `+0x5AD8`, is below 20²; every Esper's
  preset starts with it ([Gambits](gambits.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003032C0`-`0x003032F5` |
| ² | `0x00303523`-`0x00303554` |

</details>

### Where each gambit condition comes from

`sources` joins tables already in the database by id, and reads the scripts where a table stops short. It holds one part per kind of source, the parts separated by `;`:

- `shop:` each shop that sells it, by name and number in [Shops](../Items-Equipment-Shops-And-Licenses/shops.md), with the map (region) whose script gives an actor that shop (`setshopname`, the `place` column), and when the list that holds it goes on sale:
  - from the start;
  - from a story progress value, with the story point that writes it ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)), or the value alone where no story script writes it, which is so for 500 (below);
  - from a clan rank, with the rank's shipped name;
  - for the Clan Provisioner's last list, from joining Clan Centurio (below).
- `first join:` the members whose first join adds it, with the count when it is above 1 ([Party table](../Party/party-table.md)).

A shop list goes on sale once it or any list above it on the shop's ladder meets its condition, and the last list is always on sale ([Shops](../Items-Equipment-Shops-And-Licenses/shops.md), "Choosing a list"). The story test is the story counter at least the threshold¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FADF3`-`0x002FAE0D` |

</details>

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 5 calls with 5 other topics</summary>

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0030FE60`](gambit-conditions.md) | is called by | [`0x002341C0`](../World-Areas-And-Travel/traps.md) (on traps) |

**Items, equipment, shops and licenses** (explained on [party table](../Party/party-table.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00309EC0`](gambit-conditions.md) | is called by | [`0x00317930`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) Equipment: check item eligible for slot (on equipping an item) |

**Steam and achievements** (explained on [gil](../Rewards-EXP-Gil-And-Loot/gil.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00309EC0`](gambit-conditions.md) | is called by | [`0x00315E90`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Status effects and KO** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B770`](gambit-conditions.md) Battle unit: find by combatant id | is called by | [`0x00310DB0`](../Battle-Actions/action-results.md) Battle unit: run periodic combat maintenance (on action results) |

**Scripts and script commands** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B760`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) | is called by | [`0x005102D0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |

</details>
