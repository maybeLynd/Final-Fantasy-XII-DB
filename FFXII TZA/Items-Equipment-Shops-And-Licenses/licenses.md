---
title: "Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "0x00323EC0, 0x00323C60, 0x00323BB0, 0x002F8FA0, 0x00323890, 0x00323D10, 0x00323910, 0x00328BD0, 0x00328990"
---

## What the player sees

- A character can use an ability or wear a piece of equipment only after buying a square that grants it; one
  square is enough even when several grant the same thing.
- Guests, Espers and enemies never need licenses, and some abilities and items need none for anyone.
- Each Quickening square bought opens the character's next Quickening and adds an MP bar, up to three.
- An Esper square can be bought by one character only, and only once that Esper has been obtained.
- Buying a square costs LP; the squares a character starts with cost nothing.

## How it works

### Who is tested

Two functions answer the question, `0x00323EC0(record, action)` for actions and `0x00323C60(record, item)` for
equipment; both take the member's stats record ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)).
Each first validates the id, refusing an invalid one (`0x00323ED2`-`0x00323EE9`, `0x00323C72`-`0x00323C89`). Then it passes
without reading the board when the record is null, is not a party record (byte `+5` not 0), or belongs to a party
row above 6 (`0x00323EEA`-`0x00323F03`, `0x00323C8A`-`0x00323C9B`). So only party rows 0-6, the six main characters and
Reks, are ever tested.

### Licenses that are not needed

An action whose row has bit 13 of the word `+0x2C` set passes (`0x00323F4D`-`0x00323F58`,
[Action definition row](../Battle-Actions/action-definition-row.md)). A piece of equipment whose row has bit 4 of
`+0x07` set passes (`0x00323CDF`-`0x00323CE3`, [Equipment row](equipment-row.md)).

### The test

Every member record carries 46 bytes of owned-square bits at `+0x194`, bit *n* for node *n*. `0x00323BB0(record,
kind, id)` builds the requirement mask for the id and passes when any byte of it shares a bit with the owned bits
(`0x00323C10`-`0x00323C42`). Actions use kind 1 (`0x00323FE3`-`0x00323FFD`) and equipment kind 0 (`0x00323CE5`-`0x00323CF7`).

`0x002F8FA0(kind, id, mask)` builds the mask by walking every node of the license node table `0x02EBF038`
([License Board](license-board.md)): a node whose category gives the asked kind and whose list of eight ids holds
the id sets its bit (`0x002F8FE5`-`0x002F908D`). So the same ability on several squares sets several bits, and owning
any one of them licenses it.

`0x00323890` turns a node's category byte into its kind, through `0x003241D0` and two jump tables
(`0x00323894`-`0x003238DB`, `0x003241D0`-`0x00324233`):

| Categories | Kind | Used for |
|---|---|---|
| 1-8 | `0` | equipment |
| 9-14, 19, 20 | `1` | actions: magicks, technicks, Quickenings, Espers |
| 15-18 | `2` | augments ([Augments](../Damage-And-Battle-Formulas/augments.md)) |
| 30 | `3` | Second Board |
| any other | none | - |

### Quickenings

Actions `0xD0`-`0xE1` take a counted test instead (`0x00323F6D`-`0x00323FCD`). The member's party row lists its
three Quickenings in bytes `+0x04`-`+0x06`; `0x0030A330` returns the action's place in that list, 0-2, or 3 when it
is not there (`0x0030A330`-`0x0030A36C`). The action passes when that place is below the number of nodes 0-17 the member
owns, counted by `0x00324020`. So the first Quickening square bought opens the first Quickening, whichever of the
eighteen it is.

### Buying a square

`0x00323910(record, node, set, flags)` sets or clears an owned bit (`0x00323910`-`0x00323BA8`). It refuses a null or
non-party record and an invalid node (`0x00323930`-`0x00323953`). With `set`:

1. `0x00323D10(record, node, flags)` must return 0, below (`0x0032395C`-`0x00323979`).
2. Unless bit 0 of `flags` is set, the node's LP cost, its byte `+0x04`, is taken from the record's LP at `+0x190`,
   kept between 0 and 99,999 (`0x0032397E`-`0x003239E1`). The cost is not compared with the LP here.
3. The bit is set (`0x003239E7`-`0x00323A29`); without `set` it is cleared.
4. For a Quickening square, the Quickening in the member's list at the new count is granted through
   `0x00300B80(id, 1)`, the id from the action row's `+0x22` (`0x00323A58`-`0x00323B0D`).
5. The record's MP bars, byte `+0x20`, are raised to the number of Quickening squares owned, or for an Esper square
   to the Mist charges the Esper's action needs (`0x00308FF0`), at most 3 (`0x00323B12`-`0x00323B7C`).
6. The stats are rebuilt with `0x0030FED0(record, 0x97)` (`0x00323B7F`-`0x00323B87`).

Setting or clearing node 229, Brawler, also refreshes the unit's held model and cancels its current action
(`0x00323A30`-`0x00323A48`, `0x00324470`).

### Why a square is refused

`0x00323D10` returns a reason, 0 when the square may be taken (`0x00323D10`-`0x00323EBB`). It tests in this order:

1. No record: 6 (`0x00323D2C`-`0x00323D43`).
2. The node number is not below the table's count: 7 (`0x00323D44`-`0x00323D6A`).
3. The member already owns it: 1 (`0x00323D6B`-`0x00323DAB`).
4. Otherwise the node's byte `+0x06` picks one rule (`0x00323DF0`):
   - 0: a category 30 square (byte `+0x05`) gives 8 while presence bit `0xC01F` is not set; any other square
     passes (`0x00323E88`-`0x00323EA3`);
   - 1: 3 when any of party rows 0-6 that has been active owns it (`0x00324280`), else it passes
     (`0x00323E78`-`0x00323E86`);
   - 2: 4 when the member owns three of nodes 0-17, else it passes (`0x00323E61`-`0x00323E76`);
   - 3: 3 when an active party row owns it, as rule 1; otherwise it passes only for a node *n* of 18-30 whose
     presence bit `0xC000 + n` is set, and any other gives 5 (`0x00323E2C`-`0x00323E5F`);
   - 4 or more: 2 when LP is charged and the cost is above the LP, else 9 (`0x00323E0B`-`0x00323E25`).

The presence bits are the class `0xC` bits of the inventory, read through `0x0030B0E0`. On the shipped nodes, byte
`+0x06` is 2 on nodes 0-17, the Quickenings, 3 on nodes 18-30, the Espers, and 0 elsewhere; node 360, Second
Board, is the one category 30 node.

The script verb `fsmenu_getlicensestatus` (`0x7034`, `0x00511310`) asks for reason 1 only. It pops a node and
then a member and returns `0x00282E80(member, node)`, which is 1 when `0x00323600(member, node)` gives
reason 1, the member owns the square, and 0 otherwise (`0x00511328`-`0x0051133B`, `0x00282E80`).
`0x00323600` takes record `[0x02EBF190] + 8 + member * 0x1C8` for a member up to 39 and no record, reason 6,
above (`0x00323600`-`0x0032362A`).

### Squares a member starts with

When a member record is set up, `BattleStats_InitializeDefinitionRecord` sets every node whose byte `+0x07` has
the bit of the member's party row, without charging LP (`0x0023AE20`-`0x0023AE8A`). The scenario presets grant theirs
the same way (`0x00239D47`-`0x00239D55`, [Scenario presets](../Party/scenario-presets.md)).

### Resetting the boards

Script verb `0x5D6` `resetJobs(member)` calls `0x00328BD0` for main characters 0-5 (`0x00342230`-`0x00342242`,
`0x00328BD0`-`0x00328D77`):

1. It removes all the member's equipment (`0x0031A260`).
2. `0x00328990` walks each of the member's two boards, the bytes `+0x1C3` and `+0x1C4`. It clears every owned square
   the member did not start with and adds its cost back to the LP, clamped to 0-99,999 (`0x00328990`, `0x003289F0`-`0x00328AF2`).
3. It then refreshes the menu state (`0x00559760`), and when the member is the current summoner it dismisses the Esper
   (`0x003137F0`, `0x003138D0(1)`, `0x00313550(0)`) (`0x00328C3A`-`0x00328C59`).
4. It rebuilds the stats with `0x0030FED0(record, 0x97)` (`0x00328C5E`-`0x00328C66`), reloads its gambit preset
   and banks (`0x00327CB0`, `0x00326030`, `0x00327DE0`), clears the record's bytes `+0x68`-`+0x87`, the MP bars and the
   Mist charges, and sets both boards and the byte `+0x1C5` back to none (`0x00328CA3`-`0x00328D5D`). For Vaan and
   Penelo, rows 0 and 5, it also raises the gambit block's slot count `+0xBA` by one, at most 12
   (`0x00328CB4`-`0x00328CF5`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | nameWord | name: bank = word >> 11, entry = word & `0x7FF` |
| `+0x02` | `u16` | w02 | `0x4280`-`0x4289`, one value per group of categories; category 18 has two |
| `+0x04` | `u8` | lpCost | LP the square costs (`0x003239C3`, `0x0031E093`) |
| `+0x05` | `u8` | category | 1-30; gives the requirement kind (`0x002F9049` through `0x00323890`) |
| `+0x06` | `u8` | rule | 0 ordinary, 2 Quickening, 3 Esper; picks the refusal rule (`0x00323DF0`) |
| `+0x07` | `u8` | startMask | bit n: party row n starts owning it (`0x0023AE68`, `0x0031E0E9`) |
| `+0x08` | `u16[8]` | ids | the ids the square grants, at most four on a shipped node, `0xFFFF` for none (`0x002F9060`) |

## Shipped data

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

## Modding notes

- To make an ability free for everyone, set bit 13 of its action row's `+0x2C`; for equipment, bit 4 of `+0x07`.
- A square grants up to eight ids of one kind, set by its category; adding an id to a square's list licenses it.
- A square's cost is its byte `+0x04`; the menu, not the setter, checks that the LP covers it.
- `resetJobs` keeps the squares a member started with and refunds the rest.

## Related

- [License Board](license-board.md) - the board files and the node numbers on them.
- [Command availability](../Battle-Actions/command-availability.md) - the "no license" refusal of a command.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - what the augment squares do.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the owned bits, LP and MP bars.
- [Equipment row](equipment-row.md) - the no-license bit of equipment.
