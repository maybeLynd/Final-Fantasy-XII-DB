---
title: "License list: every License Board square with its name, kind, LP cost, what it grants, who starts with it and the boards that hold it"
kind: "reference"
category: "Items, equipment, shops and licenses"
addresses: "02EBF038, 0031C5D0, 0031DF90, 0031DFAB, 00323890, 002F8FA0, 0023AE68, 00556FE7"
---

## What it lists

`license-list.tsv` holds one line for each of the 361 license nodes that registry slot `02EBF038` reaches
(`battle_pack.bin` directory entry `+34`<sub>h</sub>). What each field does, and the code that reads it, is on
[Licenses](licenses.md) and [License Board](license-board.md); this page is the shipped content.

By requirement kind there are 176 equipment nodes, 97 action nodes (magicks, technicks, the 18 Quickenings and
the 13 Espers), 87 augment nodes and the one Second Board node, 360. 60 squares are on all twelve boards, and the
14 Quickening nodes not placed on a board are on none, as [License Board](license-board.md) states.

### How it is built

`Database/Tools/catalogues/license_list.py`, with the shared readers in `ffxii_text.py`:

1. the `st2e` table at entry `+34`<sub>h</sub>: 361 rows of 24 bytes from the section's `+20`<sub>h</sub>;
2. the name word `+00`<sub>h</sub> through the word banks (`0031DF90`), and the kind text `+02`<sub>h</sub> through the text groups
   (`0031DFAB`-`0031DFB4`), "Weapon" to "Gambit";
3. the requirement kind from the category `+05`<sub>h</sub>, by the table `00323890` gives on [Licenses](licenses.md);
4. the granted ids `+08`<sub>h</sub>-`+17`<sub>h</sub> (`002F8FA0` matches them against the asked id) named by their kind: an equipment
   id `1000`<sub>h</sub> + row by the equipment row's name, an action id by the action row's name, an augment id by the augment
   row's name; Second Board's `0080`<sub>h</sub> is kept as the id alone;
5. the members who start with the square from the bits of `+07`<sub>h</sub> (`0023AE68`), party rows 0-6 by the names on
   [Party members](../Party/party-members.md);
6. the boards from the twelve shipped files `board_1.bin`-`board_12.bin`, each named by its job, text id `3ED`<sub>h</sub> +
   board (`00556FE7`);
7. every one-byte text code through the glyph table of the shipped `us` font `font00.dat`
   ([Fonts](../Menus-And-HUD/fonts.md)).

### Checks

- The table's header gives 361 rows of 24 bytes, and the TSV has 361 data lines.
- Two runs over the same files give byte-identical output.
- The kind counts agree with [Augments](../Damage-And-Battle-Formulas/augments.md), 87 augment nodes, and the board counts
  with [License Board](license-board.md): 60 squares on every board, 14 on none.
- Rows compared with their readers: node 182, White Magick 1, costs 15 LP (`+04`<sub>h</sub>, which `003239C3` takes),
  grants actions 0 and 1, Cure and Blindna, and is held from the start by Ashe, Fran, Penelo and Reks; node 31,
  Essentials, costs 1 LP and every party row 0-6 starts with it; node 360, Second Board, is category 30.
- No text field keeps an undecoded `{hh}` byte.

## Columns

| Column | Meaning |
|---|---|
| `node`, `name` | the node number and its shipped name |
| `kind_text` | the shipped text of `+02`<sub>h</sub> |
| `lp_cost` | `+04`<sub>h</sub> |
| `category`, `requirement_kind` | `+05`<sub>h</sub> and the kind it gives: equipment, action, augment or Second Board |
| `rule` | `+06`<sub>h</sub>: ordinary, Quickening or Esper |
| `starts_with` | the party members whose bit is set in `+07`<sub>h</sub> |
| `grant_ids`, `grants` | the ids `+08`<sub>h</sub>-`+17`<sub>h</sub> other than `FFFF`<sub>h</sub>, and their shipped names |
| `boards` | the jobs whose board holds the square, or "all twelve" |
| `explanation` | a one-line summary: the LP cost and what the square grants |

## Related

- [Licenses: what the License Board test asks for an action or a piece of equipment, who is never tested, Quickenings, and buying or resetting a square](licenses.md)
- [License Board: the twelve job board files, the square grid each holds, and the squares every board shares](license-board.md)
- [Augment list: every augment with its name, text, value, the code that reads the value, and its timer](../Damage-And-Battle-Formulas/augment-list.md)
