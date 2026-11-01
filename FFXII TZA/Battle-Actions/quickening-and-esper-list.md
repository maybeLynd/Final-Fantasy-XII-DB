---
title: "Quickening and Esper list: the thirty-two class-17 ids of the Quickenings, the Espers and Second Board, with their names and the code that reads them"
kind: "reference"
category: "Battle actions"
addresses: "0x02EBF0C8, 0x0031C5D0, 0x0031D814, 0x00306340, 0x003064F0, 0x00325F40, 0x00252E60, 0x00323D10"
---

## What it lists

[`quickening-and-esper-list.tsv`](quickening-and-esper-list.tsv) holds one line for each of the 32 rows of the table that registry slot `0x02EBF0C8`
reaches (`battle_pack.bin` directory entry `+0x6C`). Row *n* is id `0xC000` + *n*, inventory class 17
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)), whose owned state is one bit.

| Ids | Rows | What names them |
|---|---|---|
| `0xC000`-`0xC011` | the 18 Quickenings | word `+0x22` of Quickening actions 208-225 |
| `0xC012`-`0xC01E` | the 13 Espers | word `+0x22` of summon actions 262-274 |
| `0xC01F` | SecondJob | no action |

The bits gate License Board squares: `0x00323D10` refuses an Esper square, node *n* 18-30, until bit `0xC000` + *n*
is owned, and the Second Board square until bit `0xC01F` is ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)).

### Where the values come from

Each line is a row of the `st2e` table at entry `+0x6C` (32 rows of 8 bytes from the section's `+0x20`), named by
its word `+0x00` through the word banks, with the action rows whose `+0x22` is the row's id
([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `+0x00` | `u16` | nameWord | `0x0031C5D0` (`0x0031D86B`, `0x0031D8AE`) | the name, bank 0; its row is the number of the action that names the id |
| `+0x02` | `u16` | word02 | `0x00306340`, on a path no caller takes (below) | 265 + row on every row |
| `+0x04` | `u16` | word04 | none | 0-31, the row number on 25 rows |
| `+0x06` | `u16` | word06 | none | 0 on every row |

`0x0031C5D0`'s class-17 arm stores the name in the query record `+0x18`, the owned state `0x00309EC0(id, 0)` in
`+0x20`, `0x0030AE30(id, 0)` in `+0x24` and -1 in `+0x2C` (`0x0031D814`-`0x0031D8E5`).

### Who reads the table

The table is loaded by `0x0031C5D0`, `0x00306340`, the validator `0x00322C50` (the row count only) and the loader
`0x00236C30`. `0x0031C5D0` reads only `+0x00`.

`0x00306340(member, id)` takes a magick's action row `+0x02`, a technick's `+0x02`, or for a `0xC000` id the word
`+0x02` of this table, and hands it to `0x003064F0`, which asks `0x003060E0` and `0x00323EC0` whether the member may use
that action. Its two callers never pass a `0xC000` id:

1. `0x002826F0` and `0x00282A40` hand it the ids of the inventory lists 9 and 8
   ([Party marks](../Menus-And-HUD/party-marks.md)).
2. The only function that adds an id to a category list is `0x00252E60`, reached from `0x00325F40`. It chooses the
   list from the id's top nibble through the table at `0x01EED1B0`: nibble 3 to list 9, nibble 4 to list 8
   (`0x00D1066E`, `0x00D1066F`), and it returns at once for a nibble above 10 (`0x00325F40`).
   - An id already in the list is not added again
   (`0x00252EE5`); after appending, it calls `0x002CD650` (`0x00252F18`), which sets the save-wide category bit
   (`[0x020927C0] + 0x3244`, `0x00252D40`) of each inventory category whose list is now non-empty
   ([Inventory screen](../Menus-And-HUD/inventory-screen.md)).
3. The other writers of the lists, `0x002530E0`, `0x002534C0`, `0x002535D0` and `0x00253240`, only move, remove or clear
   ids.

So no `0xC000` id reaches the word `+0x02`, and `+0x04` and `+0x06` have no reader at all.

### Properties of the shipped rows

- The table's header gives 32 rows of 8 bytes, one TSV line each.
- For rows 0-30, exactly one action row has `+0x22` = the row's id, and it is the row of the name word. Nodes 18-30
  of the licence table carry the same names, and nodes 0-17 the name Quickening. `+0x02` is 265 + row and `+0x06`
  is 0.
- Example rows: `0xC000` is named Red Spiral, word `0x00D0`, and action 208 Red Spiral has
  `+0x22` = `0xC000`; `0xC012`, Belias, is named by summon action 262, and licence node 18 is Belias.

### How an Esper is obtained

Fourteen scripts share one grant block, the thirteen fight scenes and `pos_z0000` (event 427): it reads the map the scene plays on (`nowmap`) and adds that map's Esper when it is not held, and on Belias's map the Second Board too, which the `pos_z0000` copy leaves out. The opening setup scene `pre_z0000` (event 212) sets the battle bytes of twelve Espers from 0 to 1; Famfrit's (`0x0A1E`) is set to 1 by `dgl_g01` after the battle with Dr. Cid. Each fight runs while its byte is 1. The `obtained` column gives each fight.

For the optional Espers the `obtained` column also gives the way in: the exits into the fight map, the floor groups,
switches, key items, waystones and story counter values that open them, with their listing lines. Walk results come
from the collision floor of the map before the fight map: which entrances reach the exit on foot under each floor
setting the scripts make. Wall records are not modelled, so these results say what the floor allows, not that no
wall stands in the way.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name`, `kind` | the id, its shipped name, and Quickening, Esper or Second Board |
| `name_word` | `+0x00` |
| `action_rows` | the actions whose `+0x22` is the id |
| `licence_node` | the License Board node the id belongs to |
| `word_02`, `word_04`, `word_06` | the three words, raw |
| `explanation` | a one-line summary |
| `obtained` | for an Esper, the map of its fight, the scene step that grants it, how the map is entered, the way in (for the optional Espers) and the story progress the fight tests or sets ("How an Esper is obtained" above); `-` for a Quickening |

## Related

- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](quickenings-and-summons.md)
- [Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square](../Items-Equipment-Shops-And-Licenses/licenses.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](action-list.md)
