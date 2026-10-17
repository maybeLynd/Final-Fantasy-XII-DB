---
title: "Quickening and Esper list: the thirty-two class-17 ids of the Quickenings, the Espers and Second Board, with their names and the code that reads them"
kind: "reference"
category: "Battle actions"
addresses: "02EBF0C8, 0031C5D0, 0031D814, 00306340, 003064F0, 00325F40, 00252E60, 00323D10"
---

## What it lists

`quickening-and-esper-list.tsv` holds one line for each of the 32 rows of the table that registry slot `02EBF0C8`
reaches (`battle_pack.bin` directory entry `+6C`<sub>h</sub>). Row *n* is id `C000`<sub>h</sub> + *n*, inventory class 17
([Item and ability ids](../Engine-Core/item-and-ability-ids.md)), whose owned state is one bit.

| Ids | Rows | What names them |
|---|---|---|
| `C000`<sub>h</sub>-`C011`<sub>h</sub> | the 18 Quickenings | word `+22`<sub>h</sub> of Quickening actions 208-225 |
| `C012`<sub>h</sub>-`C01E`<sub>h</sub> | the 13 Espers | word `+22`<sub>h</sub> of summon actions 262-274 |
| `C01F`<sub>h</sub> | SecondJob | no action |

The bits gate License Board squares: `00323D10` refuses an Esper square, node *n* 18-30, until bit `C000`<sub>h</sub> + *n*
is owned, and the Second Board square until bit `C01F`<sub>h</sub> is ([Licenses](../Items-Equipment-Shops-And-Licenses/licenses.md)).

### How it is built

`Database/Tools/catalogues/small_tables.py` reads the `st2e` table at entry `+6C`<sub>h</sub> (32 rows of 8 bytes from the
section's `+20`<sub>h</sub>), names each row by its word `+00`<sub>h</sub> through the word banks, and finds the action rows whose
`+22`<sub>h</sub> is the row's id ([Action list](action-list.md)).

| Offset | Type | Field | Read by | Meaning |
|---|---|---|---|---|
| `00`<sub>h</sub> | `u16` | nameWord | `0031C5D0` (`0031D86B`, `0031D8AE`) | the name, bank 0; its row is the number of the action that names the id |
| `02`<sub>h</sub> | `u16` | word02 | `00306340`, on a path no caller takes (below) | 265 + row on every row |
| `04`<sub>h</sub> | `u16` | word04 | none | 0-31, the row number on 25 rows |
| `06`<sub>h</sub> | `u16` | word06 | none | 0 on every row |

`0031C5D0`'s class-17 arm stores the name in the query record `+18`<sub>h</sub>, the owned state `00309EC0(id, 0)` in
`+20`<sub>h</sub>, `0030AE30(id, 0)` in `+24`<sub>h</sub> and -1 in `+2C`<sub>h</sub> (`0031D814`-`0031D8E5`).

### The scope of "no function uses"

The table is loaded by `0031C5D0`, `00306340`, the validator `00322C50` (the row count only) and the loader
`00236C30`; all four were decompiled. `0031C5D0` reads only `+00`<sub>h</sub>.

`00306340(member, id)` takes a magick's action row `+02`<sub>h</sub>, a technick's `+02`<sub>h</sub>, or for a `C000`<sub>h</sub> id the word
`+02`<sub>h</sub> of this table, and hands it to `003064F0`, which asks `003060E0` and `00323EC0` whether the member may use
that action. Its two callers never pass a `C000`<sub>h</sub> id:

1. `002826F0` and `00282A40` hand it the ids of the menu category lists 9 and 8
   ([Party marks](../Menus-And-HUD/party-marks.md)).
2. The only function that adds an id to a category list is `00252E60`, reached from `00325F40`. It chooses the
   list from the id's top nibble through the table at `01EED1B0`: nibble 3 to list 9, nibble 4 to list 8
   (`00D1066E`, `00D1066F`), and it returns at once for a nibble above 10 (`00325F40`).
   - An id already in the list is not added again
   (`00252EE5`); after appending, it calls `002CD650` (`00252F18`), which sets the save-wide category bit
   (`[020927C0] + 3244h`, `00252D40`) of each inventory category whose list is now non-empty
   ([Inventory screen](../Menus-And-HUD/inventory-screen.md)).
3. The other writers of the lists, `002530E0`, `002534C0`, `002535D0` and `00253240`, only move, remove or clear
   ids.

So no `C000`<sub>h</sub> id reaches the word `+02`<sub>h</sub>, and `+04`<sub>h</sub> and `+06`<sub>h</sub> have no reader at all.

### Checks

- The table's header gives 32 rows of 8 bytes, and the TSV has 32 data lines.
- Two runs over the same file give byte-identical output.
- The decoder asserts, for rows 0-30, that exactly one action row has `+22`<sub>h</sub> = the row's id and that it is the row
  of the name word; that nodes 18-30 of the licence table carry the same names, and nodes 0-17 the name Quickening;
  that `+02`<sub>h</sub> is 265 + row and `+06`<sub>h</sub> is 0.
- Rows compared with their readers: `C000`<sub>h</sub> is named Red Spiral, word `00D0`<sub>h</sub>, and action 208 Red Spiral has
  `+22`<sub>h</sub> = `C000`<sub>h</sub>; `C012`<sub>h</sub>, Belias, is named by summon action 262, and licence node 18 is Belias.

## Columns

| Column | Meaning |
|---|---|
| `id`, `name`, `kind` | the id, its shipped name, and Quickening, Esper or Second Board |
| `name_word` | `+00`<sub>h</sub> |
| `action_rows` | the actions whose `+22`<sub>h</sub> is the id |
| `licence_node` | the License Board node the id belongs to |
| `word_02`, `word_04`, `word_06` | the three words, raw |
| `explanation` | a one-line summary |

## Related

- [Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting](quickenings-and-summons.md)
- [Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square](../Items-Equipment-Shops-And-Licenses/licenses.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](action-list.md)
