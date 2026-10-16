---
title: "Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "00323EC0, 00323C60, 00323BB0, 002F8FA0, 00323890, 00323D10, 00323910, 00328BD0, 00328990"
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

Two functions answer the question, `00323EC0(record, action)` for actions and `00323C60(record, item)` for
equipment; both take the member's stats record ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)).
Each first validates the id, refusing an invalid one (`00323ED2`-`00323EE9`, `00323C72`-`00323C89`). Then it passes
without reading the board when the record is null, is not a party record (byte `+5` not 0), or belongs to a party
row above 6 (`00323EEA`-`00323F03`, `00323C8A`-`00323C9B`). So only party rows 0-6, the six main characters and
Reks, are ever tested.

### Licenses that are not needed

An action whose row has bit 13 of the word `+2C`<sub>h</sub> set passes (`00323F4D`-`00323F58`,
[Action definition row](../Battle-Actions/action-definition-row.md)). A piece of equipment whose row has bit 4 of
`+07`<sub>h</sub> set passes (`00323CDF`-`00323CE3`, [Equipment row](equipment-row.md)).

### The test

Every member record carries 46 bytes of owned-square bits at `+194`<sub>h</sub>, bit *n* for node *n*. `00323BB0(record,
kind, id)` builds the requirement mask for the id and passes when any byte of it shares a bit with the owned bits
(`00323C10`-`00323C42`). Actions use kind 1 (`00323FE3`-`00323FFD`) and equipment kind 0 (`00323CE5`-`00323CF7`).

`002F8FA0(kind, id, mask)` builds the mask by walking every node of the license node table `02EBF038`
([License Board](license-board.md)): a node whose category gives the asked kind and whose list of eight ids holds
the id sets its bit (`002F8FE5`-`002F908D`). So the same ability on several squares sets several bits, and owning
any one of them licenses it.

`00323890` turns a node's category byte into its kind, through `003241D0` and two jump tables
(`00323894`-`003238DB`, `003241D0`-`00324233`):

| Categories | Kind | Used for |
|---|---|---|
| 1-8 | `0` | equipment |
| 9-14, 19, 20 | `1` | actions: magicks, technicks, Quickenings, Espers |
| 15-18 | `2` | augments ([Augments](../Damage-And-Battle-Formulas/augments.md)) |
| 30 | `3` | Second Board |
| any other | none | - |

### Quickenings

Actions `D0`<sub>h</sub>-`E1`<sub>h</sub> take a counted test instead (`00323F6D`-`00323FCD`). The member's party row lists its
three Quickenings in bytes `+04`<sub>h</sub>-`+06`<sub>h</sub>; `0030A330` returns the action's place in that list, 0-2, or 3 when it
is not there (`0030A330`-`0030A36C`). The action passes when that place is below the number of nodes 0-17 the member
owns, counted by `00324020`. So the first Quickening square bought opens the first Quickening, whichever of the
eighteen it is.

### Buying a square

`00323910(record, node, set, flags)` sets or clears an owned bit (`00323910`-`00323BA8`). It refuses a null or
non-party record and an invalid node (`00323930`-`00323953`). With `set`:

1. `00323D10(record, node, flags)` must return 0, below (`0032395C`-`00323979`).
2. Unless bit 0 of `flags` is set, the node's LP cost, its byte `+04`<sub>h</sub>, is taken from the record's LP at `+190`<sub>h</sub>,
   kept between 0 and 99,999 (`0032397E`-`003239E1`). The cost is not compared with the LP here.
3. The bit is set (`003239E7`-`00323A29`); without `set` it is cleared.
4. For a Quickening square, the Quickening in the member's list at the new count is granted through
   `00300B80(id, 1)`, the id from the action row's `+22`<sub>h</sub> (`00323A58`-`00323B0D`).
5. The record's MP bars, byte `+20`<sub>h</sub>, are raised to the number of Quickening squares owned, or for an Esper square
   to the Mist charges the Esper's action needs (`00308FF0`), at most 3 (`00323B12`-`00323B7C`).
6. The stats are rebuilt with `0030FED0(record, 97h)` (`00323B7F`-`00323B87`).

Setting or clearing node 229, Brawler, also refreshes the unit's held model and cancels its current action
(`00323A30`-`00323A48`, `00324470`).

### Why a square is refused

`00323D10` returns a reason, 0 when the square may be taken (`00323D10`-`00323EBB`). The node's byte `+06`<sub>h</sub>
picks the rule:

| Reason | When | Sites |
|---:|---|---|
| `6` | no record | `00323D2C`-`00323D43` |
| `7` | the node number is not below the table's count | `00323D44`-`00323D6A` |
| `1` | the member already owns it | `00323D6B`-`00323DAB` |
| `4` | a byte `+06`<sub>h</sub> = 2 square while the member owns three of nodes 0-17 | `00323E61`-`00323E76` |
| `3` | a byte `+06`<sub>h</sub> = 1 or 3 square that any of party rows 0-6 that has been active owns (`00324280`) | `00323E2C`-`00323E3C`, `00323E78`-`00323E86` |
| `5` | a byte `+06`<sub>h</sub> = 3 square whose node *n*, 18-30, does not yet have presence bit `C000h + n` set, or any other node | `00323E3E`-`00323E5F` |
| `8` | a category 30 square while presence bit `C01F`<sub>h</sub> is not set | `00323E88`-`00323EA3` |
| `2`, `9` | a byte `+06`<sub>h</sub> of 4 or more: 2 when LP is charged and the cost is above the LP, else 9 | `00323E0B`-`00323E25` |

The presence bits are the class `C`<sub>h</sub> bits of the inventory, read through `0030B0E0`. On the shipped nodes, byte
`+06`<sub>h</sub> is 2 on nodes 0-17, the Quickenings, 3 on nodes 18-30, the Espers, and 0 elsewhere; node 360, Second
Board, is the one category 30 node.

The script verb `fsmenu_getlicensestatus` (`7034`<sub>h</sub>, `00511310`) asks for reason 1 only. It pops a node and
then a member and returns `00282E80(member, node)`, which is 1 when `00323600(member, node)` gives
reason 1, the member owns the square, and 0 otherwise (`00511328`-`0051133B`, `00282E80`).
`00323600` takes record `[02EBF190] + 8 + member * 1C8h` for a member up to 39 and no record, reason 6,
above (`00323600`-`0032362A`).

### Squares a member starts with

When a member record is set up, `BattleStats_InitializeDefinitionRecord` sets every node whose byte `+07`<sub>h</sub> has
the bit of the member's party row, without charging LP (`0023AE20`-`0023AE8A`). The scenario presets grant theirs
the same way (`00239D47`-`00239D55`, [Scenario presets](../Party/scenario-presets.md)).

### Resetting the boards

Script verb `5D6`<sub>h</sub> `resetJobs(member)` calls `00328BD0` for main characters 0-5 (`00342230`-`00342242`,
`00328BD0`-`00328D77`):

1. It removes all the member's equipment (`0031A260`).
2. `00328990` walks each of the member's two boards, the bytes `+1C3`<sub>h</sub> and `+1C4`<sub>h</sub>. It clears every owned square
   the member did not start with and adds its cost back to the LP, clamped to 0-99,999 (`00328990`, `003289F0`-`00328AF2`).
3. It then refreshes the menu state (`00559760`), and when the member is the current summoner it dismisses the Esper
   (`003137F0`, `003138D0(1)`, `00313550(0)`) (`00328C3A`-`00328C59`).
4. It rebuilds the stats with `0030FED0(record, 97h)` (`00328C5E`-`00328C66`), reloads the member's gambit preset
   and banks, clears the record's bytes `+68`<sub>h</sub>-`+87`<sub>h</sub>, the MP bars and the
   Mist charges, and sets both boards and the byte `+1C5`<sub>h</sub> back to none (`00328CA3`-`00328D5D`). For Vaan and
   Penelo, rows 0 and 5, it also raises the gambit block's slot count `+BA`<sub>h</sub> by one, at most 12
   (`00328CB4`-`00328CF5`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16` | nameWord | name: bank = word >> 11, entry = word & `7FF`<sub>h</sub> |
| `02`<sub>h</sub> | `u16` | w02 | `4280`<sub>h</sub>-`4289`<sub>h</sub>, one value per group of categories; category 18 has two |
| `04`<sub>h</sub> | `u8` | lpCost | LP the square costs (`003239C3`, `0031E093`) |
| `05`<sub>h</sub> | `u8` | category | 1-30; gives the requirement kind (`002F9049` through `00323890`) |
| `06`<sub>h</sub> | `u8` | rule | 0 ordinary, 2 Quickening, 3 Esper; picks the refusal rule (`00323DF0`) |
| `07`<sub>h</sub> | `u8` | startMask | bit n: party row n starts owning it (`0023AE68`, `0031E0E9`) |
| `08`<sub>h</sub> | `u16[8]` | ids | the ids the square grants, at most four on a shipped node, `FFFF`<sub>h</sub> for none (`002F9060`) |

## Shipped data

| Node | Name | LP | Category | Rule | Grants |
|---:|---|---:|---:|---:|---|
| 0-17 | Quickening | 50 to 150 | 19 | 2 | nothing by id; counted |
| 18-30 | the thirteen Espers, Belias first | 20 to 200 | 20 | 3 | the summon action, Belias `106`<sub>h</sub> |
| 31 | Essentials | 1 | 18 | 0 | `72`<sub>h</sub> |
| 360 | Second Board | 30 | 30 | 0 | `80`<sub>h</sub> |

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

- To make an ability free for everyone, set bit 13 of its action row's `+2C`<sub>h</sub>; for equipment, bit 4 of `+07`<sub>h</sub>.
- A square grants up to eight ids of one kind, set by its category; adding an id to a square's list licenses it.
- A square's cost is its byte `+04`<sub>h</sub>; the menu, not the setter, checks that the LP covers it.
- `resetJobs` keeps the squares a member started with and refunds the rest.

## Related

- [License Board](license-board.md) - the board files and the node numbers on them.
- [Command availability](../Battle-Actions/command-availability.md) - the "no license" refusal of a command.
- [Augments](../Damage-And-Battle-Formulas/augments.md) - what the augment squares do.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the owned bits, LP and MP bars.
- [Equipment row](equipment-row.md) - the no-license bit of equipment.
