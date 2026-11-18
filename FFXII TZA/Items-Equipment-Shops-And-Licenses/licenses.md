[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Licenses

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square | system | Items, equipment, shops and licenses | Licenses | How licenses work: who the test applies to and who always passes, the action and equipment bits that need no license, the owned-square bits every member carries and the requirement mask built from the license nodes, the four requirement kinds a node's category gives, the counted rule for Quickenings, the reasons a square can be refused, what buying a square costs and grants (LP, Quickenings, and the MP bars: how many Mist charges a member can hold), the squares each member starts with, and the resetJobs verb that refunds both boards. | 0x00323EC0, 0x00323C60, 0x00323BB0, 0x002F8FA0, 0x00323890, 0x00323D10, 0x00323910, 0x00328BD0, 0x00328990 |

## What the player sees

- A character can use an ability or wear a piece of equipment only after buying a square that grants it; one
  square is enough even when several grant the same thing.
- Guests, Espers and enemies never need licenses, and some abilities and items need no license for anyone.
- Each Quickening square bought opens the character's next Quickening and raises the character's MP bars, the
  number of Mist charges the character can hold, to the number of Quickening squares owned, up to three; an
  Esper square raises them to the Mist charges that Esper needs.
- An Esper square can be bought by one character only, and only once that Esper has been obtained.
- Buying a square costs LP; the squares a character starts with cost nothing.

## How it works

### Who is tested

Two functions answer the question, `0x00323EC0(record, action)` for actions and `0x00323C60(record, item)` for
equipment; both take the member's stats record ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)).
Each first validates the id, refusing an invalid one¹. Then it passes
without reading the board when the record is null, is not a party record (byte `+5` not 0), or belongs to a party
row above 6². So only party rows 0-6, the six main characters and
Reks, are ever tested.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323ED2`-`0x00323EE9`, `0x00323C72`-`0x00323C89` |
| ² | `0x00323EEA`-`0x00323F03`, `0x00323C8A`-`0x00323C9B` |

</details>

### Licenses that are not needed

An action whose row has bit `0x2000` of the word `+0x2C` set passes (`0x00323F4D`-`0x00323F58`,
[Action definition row](../Battle-Actions/action-definition-row.md)). A piece of equipment whose row has bit `0x10` of
`+0x07` set passes (`0x00323CDF`-`0x00323CE3`, [Equipment row](equipment-row.md)).

`0x00323C60` forms the equipment row address in 32 bits, `base + (item - 0x1000) × size`,
from the answer of `0x0020E600` and the row size word¹; with no equipment
table, `[0x02EBF0F8]` null or `0x0020E600` answering null, the row address is 0 and the
bit test reads the byte at address 7².
A member that needs the license gets the answer of `0x00323BB0(record, 0, item)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323CC5`-`0x00323CD9` |
| ² | `0x00323CA7`, `0x00323CB4`, `0x00323CDD`-`0x00323CDF` |
| ³ | `0x00323CE5`-`0x00323CF7` |

</details>

### The test

Every member record carries 46 bytes of owned-square bits at `+0x194`, bit value `1 << (n % 8)` of byte `n / 8`
for node *n*. `0x00323BB0(record,
kind, id)` builds the requirement mask for the id and passes when any byte of it shares a bit with the owned bits¹. Actions use kind 1² and equipment kind 0³.
`0x00323BB0` answers 1 or 0⁴, and builds its mask with `0x002F8FA0(kind, id, mask)`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323C10`-`0x00323C42` |
| ² | `0x00323FE3`-`0x00323FFD` |
| ³ | `0x00323CE5`-`0x00323CF7` |
| ⁴ | `0x00323C42`, `0x00323C2D` |
| ⁵ | `0x00323BFC` |

</details>

`0x002F8FA0(kind, id, mask)` builds the mask by walking every node of the license node table `0x02EBF038`
([License Board](license-board.md)): a node whose category gives the asked kind and whose list of eight ids holds
the id sets its bit, bit value `1 << (n % 8)` of mask byte `n / 8` for node `n`¹. So the
same ability on several squares sets several bits, and owning any one of them licenses it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F8FE5`-`0x002F908D` |

</details>

The kind is the node's category byte `+0x05` through `0x00323890`, and the ids are the eight words from `+0x08`¹. The builder returns the number of nodes that hold the id². With
no node table bound at `0x02EBF038` it clears 0 bytes, walks no node and returns 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F9045`-`0x002F9070` |
| ² | `0x002F9089`, `0x002F90A8` |
| ³ | `0x002F8FCB`-`0x002F8FFF` |

</details>

The two sides size the mask differently:

- `0x00323BB0` holds the mask in 46 bytes on its stack, zeroed at `0x00323BD4`-`0x00323BF5`, and compares 46 bytes
  (`0x00323C27`: `cmp rax, 0x2E`).
- `0x002F8FA0` clears `(count + 7) / 8` bytes, `count` being the node table's row count `[0x02EBF038] + 4`, before
  setting bits¹, and sets the bit of any node below `count`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F8FD3`-`0x002F8FE0` |

</details>

The shipped node table has 361 rows in every language's `battle_pack.bin`, so the builder clears exactly 46 bytes
and sets only the bits of nodes 0-360; nothing is written past the 46 bytes, and the bits of nodes 361-367 stay 0.
`0x00323BB0` is the builder's only caller.

`0x00323890` turns a node's category byte into its kind, through `0x003241D0` and two jump tables¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323894`-`0x003238DB`, `0x003241D0`-`0x00324233` |

</details>

| Categories | Kind | Used for |
|---|---|---|
| 1-8 | `0` | equipment |
| 9-14, 19, 20 | `1` | actions: magicks, technicks, Quickenings, Espers |
| 15-18 | `2` | augments ([Augments](../Damage-And-Battle-Formulas/augments.md)) |
| 30 | `3` | Second Board |
| any other | `-1`, no kind (`0x003238DB`) | - |

### Quickenings

Actions `0xD0`-`0xE1` take a counted test instead¹. The member's party row lists its
three Quickenings in bytes `+0x04`-`+0x06`; `0x0030A330` returns the action's place in that list, 0-2, or 3 when it
is not there². The action passes when that place is below the number of nodes 0-17 the member
owns, counted by `0x00324020`. So the first Quickening square bought opens the first Quickening, whichever of the
eighteen it is.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323F6D`-`0x00323FCD` |
| ² | `0x0030A330`-`0x0030A36C` |

</details>

### Buying a square

`0x00323910(record, node, set, flags)` sets or clears an owned bit¹. It refuses a null or
non-party record and an invalid node². With `set`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323910`-`0x00323BA8` |
| ² | `0x00323930`-`0x00323953` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x00323D10(record, node, flags)` must return 0, below. | `0x0032395C`-`0x00323979` |
| 2 | Unless bit `0x1` of `flags` is set, the node's LP cost, its byte `+0x04`, is taken from the record's LP at `+0x190`, kept between 0 and 99,999. The cost is not compared with the LP here. | `0x0032397E`-`0x003239E1` |
| 3 | The bit is set; without `set` it is cleared. | `0x003239E7`-`0x00323A29` |
| 4 | For a Quickening square, the Quickening in the member's list at the new count is granted through `0x00300B80(id, 1)`, the id from the action row's `+0x22`. | `0x00323A58`-`0x00323B0D` |
| 5 | The record's MP bars, byte `+0x20`, the number of Mist charges the member can hold, are raised when lower to the number of Quickening squares owned, or for an Esper square to the Mist charges the Esper's action needs (`0x00308FF0`: the action row's byte `+0x0A` for a category `+0x1E` of 5 or 6, else 0), at most 3. | `0x00323B12`-`0x00323B7C` |
| 6 | The stats are rebuilt with `0x0030FED0(record, 0x97)`. The rebuild copies the MP bars, at most 3, to the battle stats' `+0x37` (`0x002FF89F`, from `0x003103AD`) and keeps the Mist pool `+0x06` at most max MP times `+0x37`; the Mist charges `+0x4E` are the pool divided by max MP. | `0x00323B7F`-`0x00323B87`<br>`0x00310541`-`0x0031058E`<br>`0x0030E0B5`-`0x0030E0BD` |

Each refusal, and a non-zero answer of `0x00323D10` in step 1, makes `0x00323910` answer -1¹; after the rebuild of step 6 it answers 0².
In step 4 a Quickening square is a node of `0x11` or below³; the grant runs
only when the action `0x0030A310` gives for the answer of `0x00324020` less 1 is `0xD0`
to `0xE1`⁴. An Esper square in step 5 is a node from `0x12` to `0x1E`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323935`, `0x00323976` |
| ² | `0x00323B8C` |
| ³ | `0x00323A58` |
| ⁴ | `0x00323A61`-`0x00323A69`, `0x00323AAC`-`0x00323AC2` |
| ⁵ | `0x00323B12`-`0x00323B18` |

</details>

Setting or clearing node 229, Brawler, also refreshes the unit's held model and cancels its current action¹. `0x00324470` removes the unit with `0x00300E40(unit, 0)` when it has no stats
record `+0x698`, or when its status words `+0x3C | +0x64` hold any bit of `0x80000003` outside a town (`0x00313F60`
answers 0), unless unit flag bit `0x2` is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323A30`-`0x00323A48`, `0x00324470` |
| ² | `0x00324495`-`0x003244C1` |

</details>

### Why a square is refused

`0x00323D10` returns a reason, 0 when the square may be taken¹. It tests in this order:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323D10`-`0x00323EBB` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | No record: 6. | `0x00323D2C`-`0x00323D43` |
| 2 | The node number is not below the table's count: 7. | `0x00323D44`-`0x00323D6A` |
| 3 | The member already owns it: 1. | `0x00323D6B`-`0x00323DAB` |
| 4 | Otherwise the node's byte `+0x06` picks one rule:<br>• 0: a category 30 square (byte `+0x05`) gives 8 while presence bit `0xC01F` is not set; any other square passes;<br>• 1: 3 when any of party rows 0-6 that has been active owns it, else it passes;<br>• 2: 4 when the member owns three of nodes 0-17, else it passes;<br>• 3: 3 when an active party row owns it, as rule 1; otherwise it passes only for a node *n* of 18-30 whose presence bit `0xC000 + n` is set, and any other gives 5;<br>• 4 or more: 2 when LP is charged and the cost is above the LP, else 9. | `0x00323DF0`<br>`0x00323E88`-`0x00323EA3`<br>`0x00324280`<br>`0x00323E78`-`0x00323E86`<br>`0x00323E61`-`0x00323E76`<br>`0x00323E2C`-`0x00323E5F`<br>`0x00323E0B`-`0x00323E25` |

The presence bits are the class `0xC` bits of the inventory, read through `0x0030B0E0`. On the shipped nodes, byte
`+0x06` is 2 on nodes 0-17, the Quickenings, 3 on nodes 18-30, the Espers, and 0 elsewhere; node 360, Second
Board, is the one category 30 node.

The script verb `fsmenu_getlicensestatus` (`0x7034`, `0x00511310`) asks for reason 1 only. It pops a node and
then a member and returns `0x00282E80(member, node)`, which is 1 when `0x00323600(member, node)` gives
reason 1, the member owns the square, and 0 otherwise¹.
`0x00323600` takes record `[0x02EBF190] + 8 + member * 0x1C8` for a member up to 39 and no record, reason 6,
above².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00511328`-`0x0051133B`, `0x00282E80` |
| ² | `0x00323600`-`0x0032362A` |

</details>

### Squares a member starts with

When a member record is set up, `BattleStats_InitializeDefinitionRecord` sets every node whose byte `+0x07` has
the bit of the member's party row, without charging LP¹. The scenario presets grant theirs
the same way (`0x00239D47`-`0x00239D55`, [Scenario presets](../Party/scenario-presets.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AE20`-`0x0023AE8A` |

</details>

### Resetting the boards

Script verb `0x5D6` `resetJobs(member)` calls `0x00328BD0` for main characters 0-5¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00342230`-`0x00342242`, `0x00328BD0`-`0x00328D77` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | It removes all the member's equipment. | `0x0031A260` |
| 2 | `0x00328990` walks each of the member's two boards, the bytes `+0x1C3` and `+0x1C4`. It clears every owned square the member did not start with and adds its cost back to the LP, clamped to 0-99,999.<br>• `0x00328990(record, row, board)` takes the board byte sign-extended and returns -1 with nothing changed for a board above 11 as an unsigned number, so an empty board `0xFF` is not walked; otherwise it returns 0.<br>• Each square's node goes through the class-`0x20` query `0x0031C5D0`, and a node the query refuses (a `0xFFFF` cell among them) is passed over. The square counts as owned when bit value `1 << (node & 7)` of the record's byte `+0x194 + node / 8` is set.<br>• The member started with it when bit value `1 << row` of the node's startMask `+0x07` is set; the cost added back is the node's lpCost `+0x04`. A negative sum stores 0 in the LP `+0x190`. | `0x00328990`, `0x003289F0`-`0x00328AF2`<br>`0x00328C16`, `0x00328C28`<br>`0x003289A4`-`0x003289A8`, `0x00328B07`<br>`0x00328A24`-`0x00328A3C`<br>`0x00328A3E`-`0x00328A59`<br>`0x00328A5B`-`0x00328A68`<br>`0x00328A7E`-`0x00328A83`<br>`0x00328AE4` |
| 3 | It then calls `0x00559760(member)`, and when the member is the current summoner it dismisses the Esper (`0x003137F0`, `0x003138D0(1)`, `0x00313550(0)`):<br>• `0x00559760` finds the member's record through `0x00282E10`, which compares the word `+0x60` of the nine record pointers at `[0x0209AC30] + 0xAC8`, skips null pointers and reads `[0x0209AC30]` without a null test (a null `[0x0209AC30]` faults at `0x00282E24`). With no match `0x00559760` returns and writes nothing.<br>• With a match it stores 0 in the bank-8 entries `w + 0x4D` and `3 × w + 0x53` to `3 × w + 0x55`, w being the matched word `+0x60` (`0x002527B0(8, index, 0)`, `0x00559786`, `0x005597A3`): the dwords at `[0x020927C0] + 0x90`. The last three are the member's Quickening order the [license board](../Menus-And-HUD/license-board-screen.md) shows. | `0x00328C3C`<br>`0x00328C3A`-`0x00328C59`<br>`0x00559771` |
| 4 | It rebuilds the stats with `0x0030FED0(record, 0x97)` and reloads its gambit preset. | `0x00328C5E`-`0x00328C66`<br>`0x00327CB0`, `0x00328CA3`-`0x00328CAA` |
| 5 | For Vaan and Penelo, rows 0 and 5, it raises the gambit block's slot count `+0xBA` by one, at most 12, when the record's kind byte `+5` is 0; the banks copy this raised count (dword `+0xB8`, `0x0032608E`). | `0x00328CB4`-`0x00328CF5`<br>`0x00328CDC` |
| 6 | It reloads the banks, clears the record's bytes `+0x68`-`+0x87`, the MP bars and the Mist charges, calls `0x00283270(1)`, and sets both boards and the byte `+0x1C5` back to empty. | `0x00326030`, `0x00327DE0`<br>`0x00328D4D`<br>`0x00328CFB`-`0x00328D5D` |

## Layouts

<details>
<summary>Show the memory layouts</summary>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | nameWord | name: bank = word >> 11 into the word-text table `0x02EBF170`, entry = word & `0x7FF` (bank 3 on all 361 rows); read by the class query `0x0031C5D0` (`0x0031DF56`, `0x0031DF90`) and by `0x002960B0` (`0x002961D9`, `0x00296212`) |
| `+0x02` | `u16` | typeTextId | the square's type label, a text id for `0x002F9860`: `listhelp_license.bin` rows 24-33, Weapon (`0x4280`, 105 rows), Armor (`0x4281`, 39), Shield (`0x4282`, 10), Accessory (`0x4283`, 23), Magick (`0x4284`, 43), Technick (`0x4285`, 24), Quickening (`0x4286`, 18), Esper (`0x4287`, 13), Augment (`0x4288`, 76), Gambit (`0x4289`, 10), one label per category except category 18, which has Weapon and Gambit; read only by the class query `0x0031C5D0` (`0x0031DFAB`), which keeps the string at its record `+0x10` |
| `+0x04` | `u8` | lpCost | LP the square costs (`0x003239C3`, `0x0031E093`) |
| `+0x05` | `u8` | category | 1-30; gives the requirement kind (`0x002F9049` through `0x00323890`) |
| `+0x06` | `u8` | rule | 0 ordinary, 2 Quickening, 3 Esper; picks the refusal rule (`0x00323DF0`) |
| `+0x07` | `u8` | startMask | bit value `1 << n`: party row n starts owning it (`0x0023AE68`, `0x0031E0E9`) |
| `+0x08` | `u16[8]` | ids | the ids the square grants, at most four on a shipped node, `0xFFFF` for no id (`0x002F9060`) |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Node | Name | LP | Category | Rule | Grants |
|---:|---|---:|---:|---:|---|
| 0-17 | Quickening | 50 to 150 | 19 | 2 | nothing by id; counted |
| 18-30 | the thirteen Espers, Belias first | 20 to 200 | 20 | 3 | the summon action, Belias `0x106` |
| 31 | Essentials | 1 | 18 | 0 | `0x72` |
| 360 | Second Board | 30 | 30 | 0 | `0x80` |

| Party row | Quickenings, in order |
|---|---|
| 0 Vaan | Red Spiral, White Whorl, Pyroclasm |
| 1 Ashe | Nordswain's Glow, Heaven's Wrath, Maelstrom's Bolt |
| 2 Fran | Feral Strike, Whip Kick, Shatterheart |
| 3 Balthier | Fires of War, Tides of Fate, Element of Treachery |
| 4 Basch | Fulminating Darkness, Ruin Impendent, Flame Purge |
| 5 Penelo | Intercession, Evanescence, Resplendence |

| Start mask | Squares |
|---|---|
| every member, rows 0-6 | Essentials |
| some members | Swords 1, Swords 2, Bows 1, Guns 1, Daggers 1, Shields 1, Light Armor 1 and 2, Heavy Armor 1, Mystic Armor 1, Accessories 2, White Magick 1, Black Magick 1 and 2, Steal, Libra, First Aid |

</details>

## Modding notes

- To make an ability free for everyone, set bit `0x2000` of its action row's `+0x2C`; for equipment, bit `0x10` of `+0x07`.
- A square grants up to eight ids of one kind, set by its category; adding an id to a square's list licenses it.
- A square's cost is its byte `+0x04`; the menu, not the setter, checks that the LP covers it.
- `resetJobs` keeps the squares a member started with and refunds the rest.
- The license test holds 368 nodes, nodes 0 to 367: the mask and the owned bits at `+0x194` are 46 bytes, and nodes
  368 and up are never compared.
- A node table of 369 to 384 rows makes `0x002F8FA0` write one or two bytes past the mask, into the two unused stack
  bytes after it (`[rsp+0x4E]`, `[rsp+0x4F]` of `0x00323BB0`).
- At 385 rows or more it also writes the saved stack cookie at `[rsp+0x50]`¹; the cookie check
  `0x00808C40` then fails unless the bytes written equal the ones there, and the process ends
  ([Image hardening](../Compiler-And-C-Runtime/image-hardening.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00323BC0` |

</details>

## Related

- [License Board](license-board.md) - the board files and the node numbers on them.
- [Command availability](../Battle-Actions/command-availability.md) - the "no license" refusal of a command.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - what the augment squares do.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the owned bits, LP and MP bars.
- [Equipment row](equipment-row.md) - the no-license bit of equipment.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 10 calls with 6 other topics</summary>

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00313F60`](equipping-an-item.md) (on equipping an item) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |

**Movement and pathfinding** (explained on [game over](../World-Areas-And-Travel/game-over.md), [party slots](../Party/party-slots.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00313F60`](equipping-an-item.md) (on equipping an item) | is called by | [`0x0031BAC0`](../Party/party-slots.md) (on party slots)<br>[`0x00326D60`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00329A80`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x003911D0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) |

**Graphics** (explained on [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md), [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002527B0`](../Menus-And-HUD/dialogs.md) (on dialogs) | is called by | [`0x00579420`](../Menus-And-HUD/status-and-equip-screen.md) (on status and equip screen) |
| [`0x00300E40`](equipping-an-item.md) Battle unit: teardown and despawn (on equipping an item) | calls | [`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over) |

**Steam and achievements** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00316930`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Saving, loading and settings** (explained on [game application](../Engine-Core/game-application.md), [native limits](../Engine-Core/native-limits.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00283270`](../Menus-And-HUD/menu-screens.md) (on menu screens) | is called by | [`0x00582860`](../Saving-Loading-And-Settings/saving-and-loading-screen.md) (on saving and loading screen)<br>[`0x005844A0`](../Saving-Loading-And-Settings/save-data-fields.md) Save transition: prepare runtime image for capture (on save data fields) |

</details>

---

[← Equipping an item](equipping-an-item.md) | [Buying a license →](buying-a-license.md)
