---
title: "License list: every License Board square with its name, kind, LP cost, what it grants, who starts with it and the boards that hold it"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF038, 0x0031C5D0, 0x0031DF90, 0x0031DFAB, 0x00323890, 0x002F8FA0, 0x0023AE68, 0x00556FE7"
---

## What it lists

[`license-list.tsv`](license-list.tsv) holds one line for each of the 361 license nodes that registry slot `0x02EBF038` reaches
(`battle_pack.bin` directory entry `+0x34`). What each field does, and the code that reads it, is on
[Licenses](licenses.md) and [License Board](license-board.md); this page is the shipped content.

By requirement kind there are 176 equipment nodes, 97 action nodes (magicks, technicks, the 18 Quickenings and
the 13 Espers), 87 augment nodes and the one Second Board node, 360. 60 squares are on all twelve boards, and the
14 Quickening nodes not placed on a board are on no board, as [License Board](license-board.md) states.

### Where the values come from

Each line is read from the shipped files in these steps:

1. the `st2e` table at entry `+0x34`: 361 rows of 24 bytes from the section's `+0x20`;
2. the name word `+0x00` through the word banks (`0x0031DF90`), and the kind text `+0x02` through the text groups
   (`0x0031DFAB`-`0x0031DFB4`), "Weapon" to "Gambit";
3. the requirement kind from the category `+0x05`, by the table `0x00323890` gives on [Licenses](licenses.md);
4. the granted ids `+0x08`-`+0x17` (`0x002F8FA0` matches them against the asked id) named by their kind: an equipment
   id `0x1000` + row by the equipment row's name, an action id by the action row's name, an augment id by the augment
   row's name; Second Board's `0x0080` is kept as the id alone;
5. the members who start with the square from the bits of `+0x07` (`0x0023AE68`), party rows 0-6 by the names on
   [Party members](../Party/party-members.md);
6. the boards from the twelve shipped files `board_1.bin`-`board_12.bin`, each named by its job, text id `0x3ED` +
   board (`0x00556FE7`);
7. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

### Properties of the shipped rows

- The table's header gives 361 rows of 24 bytes, one TSV line each.
- The kind counts agree with [Augments](../Damage-And-Battle-Formulas/augments.md), 87 augment nodes, and the board counts
  with [License Board](license-board.md): 60 squares on every board, 14 on no board.
- Example rows: node 182, White Magick 1, costs 15 LP (`+0x04`, which `0x003239C3` takes),
  grants actions 0 and 1, Cure and Blindna, and is held from the start by Ashe, Fran, Penelo and Reks; node 31,
  Essentials, costs 1 LP and every party row 0-6 starts with it; node 360, Second Board, is category 30.

## Columns

| Column | Meaning |
|---|---|
| `node`, `name` | the node number and its shipped name |
| `kind_text` | the shipped text of `+0x02` |
| `lp_cost` | `+0x04` |
| `category`, `requirement_kind` | `+0x05` and the kind it gives: equipment, action, augment or Second Board |
| `rule` | `+0x06`: ordinary, Quickening or Esper |
| `starts_with` | the party members whose bit is set in `+0x07` |
| `grant_ids`, `grants` | the ids `+0x08`-`+0x17` other than `0xFFFF`, and their shipped names |
| `boards` | the jobs whose board holds the square, or "all twelve" |
| `explanation` | a one-line summary: the LP cost and what the square grants |

## Related

- [Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square](licenses.md)
- [License Board: the twelve job board files, the square grid each holds, and the squares every board shares](license-board.md)
- [Augment list: every augment with its name, text, value, the code that reads the value, and its timer](../Damage-And-Battle-Formulas/augment-list.md)
