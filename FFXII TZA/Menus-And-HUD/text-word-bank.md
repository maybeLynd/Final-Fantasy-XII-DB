---
title: "Word bank: every name string of the battle word banks in all nine languages, with plural forms and articles"
kind: "reference"
category: "Menus and HUD"
addresses: "0x02EBF170, 0x003846F0, 0x003214B0, 0x002B58B0, 0x002B4550, 0x002B49F0, 0x00567B60, 0x00558CE0, 0x0027D480, 0x002986E0, 0x00536280"
---

## What it lists

[text-word-bank.tsv](text-word-bank.tsv) has one row per string of a word-bank row, with the string in each of the
nine language trees: 6,555 rows over 3,837 bank rows. The banks are entry `+0xF8` of `battle_pack.bin`
(`word.bin`), bound at start-up to `0x02EBF170` by `0x003846F0`; their layout, the `bank:row` word and the first rows of
each bank are on [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md).

### Who reads a row

- `0x003214B0(word)` gives the row of bank `(word >> 11) & 0x1F` and row `word & 0x7FF`, and `0x002B58B0(row, k)` its
  string `k`.
- The interface reads names with `0x002B58B0` on a row of these banks: the gambit screen (`0x00567B60`, `0x0056A890`,
  `0x0056BC70`), the licence screens (`0x00558CE0`, `0x005618E0`), the battle menu title `0x0027D480`, the party list
  `0x002986E0` and the battle log's names (`0x00536280`).
- All but the battle log take the row from the name pointer `+0x18` of the query record that `0x0035D330(class, row)`
  fills (`0x00567BB8`-`0x00567BC3`, `0x0056A98E`, `0x0056BD78`, `0x00558DEA`-`0x00558DF5`, `0x00561A7A`, `0x0027D4BD`-`0x0027D4C8`,
  `0x00298920`). The query's class arms split the word against `0x02EBF170` themselves, as the class 21 arm does
  (`0x0031DC58`-`0x0031DC9D`).
- `0x00536280` splits the word itself (`0x00536292`-`0x005362BF`). `0x003214B0` has one caller, at `0x0057617B`.
- The formatter `0x002B49F0` inserts a word row into a message template: as a plain string (`0F 31`), or by count
  with its plural or article (`0F 6C`, `0F 6D`, `0F 6E`; [Text codes](text-codes.md)).

### The strings of a row

A row's strings follow its two leading zero bytes. In the `in`, `kr`, `cn` and `ch` trees every row holds one
string; in `us`, `de`, `es`, `fr` and `it` a row holds up to four:

| `string` | Holds | Read by |
|---:|---|---|
| 0 | the name | every reader above |
| 1 | the plural template | `0x002B4550`, for a count above 1 (`0F 6D`) |
| 2 | the article or phrase written before the name, with its trailing space | `0F 6E`, and `0F 6C` for a count of 1 |
| 3 | a second phrase | `0F 6C` with `(b2 >> 4) & 3` = 1, for a count of 1 |

In `us` bank 3, ten rows (19, 20, 22, 23, 24, 25, 27, 28, 30 and 248) hold a fourth string with a note on the name,
their strings 1 and 2 empty (row 19: `FFTA also used Matius per PDIC`); `de` bank 11 has eight rows with a fourth string, a measure word such as `Klumpen`.

### Reading the plural template

In a plural template `{word}` (byte `09`) stands for the whole name and `{word:HHHH}` (byte `08` and two bytes) for
its first `n` bytes, `n` the two bytes as a little-endian number `& 0x7FFF` (`0x002B4550`, `0x002B4623`-`0x002B46A2`).

`0x002B4550(capacity, out, row)` takes the name as the string after the row's two leading zero bytes and the template
as the next string; a row that does not start with two zero bytes is both its own name and its template
(`0x002B457A`-`0x002B45B0`). An `n` larger than the name's length copies the whole name (`0x002B466F`-`0x002B4685`). Any
other code is copied as it stands, by the length `0x002B1FB0` measures (`0x002B45E3`, `0x002B45FB`-`0x002B461B`).

When a copy or the closing zero would not fit in the capacity, the output is the empty string
(`0x002B4600`-`0x002B4603`, `0x002B4635`-`0x002B4638`, `0x002B4690`-`0x002B4693`, `0x002B46BE`-`0x002B46C8`); a null row leaves it
empty too (`0x002B456B`-`0x002B4574`). Its one call passes a capacity of `0x80` (`0x002B4C62`).

| Row | `us` | `es` | `it` |
|---|---|---|---|
| bank 0, row 82, string 0 | `Potion` | `Poción` | `Pozione` |
| bank 0, row 82, string 1 | `{word}s` | `{word:0480}ones` | `{word:0680}i` |
| bank 0, row 82, string 2 | `a ` | `una ` | `una ` |

The `es` plural is the first 4 bytes of `Poción` and `ones`, `Pociones`; the `it` plural the first 6 bytes of
`Pozione` and `i`, `Pozioni`. Bank 12 row 0, `Rabanastre`, has string 2 `a map of ` in `us` and `une carte de ` in
`fr`.

## Columns

| Column | Meaning |
|---|---|
| `bank` | the word bank, 0 to 14 |
| `row` | the row in the bank; the word is `bank x 0x800 + row` |
| `string` | the string's position in the row, `k` of `0x002B58B0(row, k)` |
| `us` to `ch` | the string in that language tree, decoded with the tree's font |
| `missing` | the languages whose row has no string `string`, or whose bank has no row `row`, comma-separated; empty when all nine have it |
| `same_bytes` | the groups of languages whose string bytes are identical, each group's languages joined by `=` and the groups by `;`; only groups of two or more, and the languages in `missing` take no part |

An empty cell under a language not in `missing` is an empty string. Empty strings per tree: `us` 437, `de` 140, `es`
152, `fr` 436, `it` 406, 0 in `in`, `kr`, `cn` and `ch`.

## Data

Strings per bank in each tree (in `in`, `kr`, `cn` and `ch` also the bank's rows):

| Bank | `us` | `de` | `es` | `fr` | `it` | `in` | `kr` | `cn` | `ch` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 679 | 646 | 640 | 659 | 658 | 545 | 545 | 542 | 542 |
| 1 | 1,339 | 1,346 | 1,356 | 1,470 | 1,280 | 544 | 544 | 531 | 531 |
| 2 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 3 | 392 | 362 | 362 | 362 | 362 | 362 | 362 | 362 | 362 |
| 4 | 63 | 63 | 63 | 63 | 63 | 63 | 63 | 63 | 63 |
| 5 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 | 32 |
| 6 | 788 | 284 | 284 | 852 | 790 | 284 | 284 | 284 | 284 |
| 7 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| 8 | 629 | 629 | 629 | 629 | 629 | 629 | 629 | 626 | 626 |
| 9 | 128 | 128 | 128 | 128 | 128 | 128 | 128 | 128 | 128 |
| 10 | 129 | 129 | 129 | 129 | 129 | 129 | 129 | 90 | 89 |
| 11 | 982 | 986 | 955 | 982 | 1,196 | 512 | 512 | 512 | 512 |
| 12 | 812 | 792 | 816 | 816 | 814 | 512 | 512 | 512 | 512 |
| 13 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| 14 | 64 | 64 | 64 | 64 | 64 | 64 | 64 | 64 | 64 |
| all | 6,070 | 5,494 | 5,491 | 6,219 | 6,178 | 3,837 | 3,836 | 3,778 | 3,777 |

Every Western tree has all 3,837 rows. The `kr` banks lack bank 2's one row; the `cn` banks are 59 rows short of the
`in` banks and the `ch` banks 60 (banks 0, 1, 2, 8 and 10).

## Related

- [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md) - the word-bank layout,
  the `bank:row` word and the first rows of each bank.
- [Text codes](text-codes.md) - the template escapes that insert a row.
- [String tables](text-string-tables.md) - the battle messages that insert names.
- [Gambit screen](gambit-screen.md), [Battle menu](battle-menu.md) and [Party list](party-list.md) -
  screens that show the names.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x002B58B0` is called by `0x0023A570`; those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md).
- Combat AI: `0x00567B60` calls `0x00327C40`; those functions are documented on
  [gambits](../Enemy-AI-And-Gambits/gambits.md).
- Gameplay: `0x0035D330` calls `0x0031C5D0`; those functions are documented on
  [item and ability ids](../Engine-Core/item-and-ability-ids.md).
- Items equipment shops license: `0x005618E0` calls `0x00323630`, `0x00323670`, `0x003236B0`; those functions are documented
  on [license board screen](license-board-screen.md),
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Presentation: `0x002B1FB0` is called by `0x002B4810`; `0x002B58B0` is called by `0x00506700`; `0x0035D330` is called by
  `0x003BBD00`, `0x00506700`; those functions are documented on [text string tables](text-string-tables.md),
  [battle numbers](battle-numbers.md), [augments](../Damage-And-Battle-Formulas/augments.md).
- World area: `0x003846F0` calls `0x003846F0`; `0x003846F0` is called by `0x00236C30`, `0x00238850`, `0x0023A160`, `0x003845F0`,
  `0x003846F0`; those functions are documented on
  [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
