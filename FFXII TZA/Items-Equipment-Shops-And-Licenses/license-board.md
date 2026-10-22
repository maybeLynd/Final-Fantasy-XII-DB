---
title: "License Board: the twelve job board files, the square grid each holds, and the squares every board shares"
kind: "format"
category: "Items, equipment, shops and licenses"
addresses: "0x02EBF1A0, 0x00238260, 0x02EBF038, 0x00328990, 0x0055B3F0, 0x00556F90"
---

## What the player sees

- Each of the twelve jobs has its own License Board, a grid of squares the character buys one at a time.
- Some squares are on every board: the Espers, the Quickenings' first four squares, Essentials, the accessory
  squares, the gambit slots and Second Board, which opens a second job.
- The boards are the same in every language.

## Where it comes from

The boards are the files `board_1.bin` to `board_12.bin`. Every language's file path table names them at indices
71-82, and the old single board `license_board.bin`, a file of the same format, at index 70. Seven tables, those
of the `us`, `uk`, `in`, `fr`, `de`, `es` and `it` languages, point at the copies in `test_battle/in/BinaryFile/`,
and the three Asian tables at `test_battle/ch/BinaryFile/`; the two sets are byte for byte the same. The copies in the `cn` and `kr` folders
differ and are not named by any table.

`BattleStorage_InitializeWorkArrays` clears the twelve board slots at `0x02EBF1A0` and asks `0x00238260(k)` for
each board *k* from 0 to 11 (`0x002369E5`-`0x00236A24`). When slot *k* is empty, `0x00238260` requests file index
`0x47 + k` (`0x0023836A`-`0x0023837D`), so board *k* is `board_{k+1}.bin`; that board's callback stores the loaded
file's address in slot *k*, releasing a board already there with `0x003844F0` first (`0x00238390`-`0x002383AA` for
board 0). No request for index 70 is made by the calls to the
file request functions `0x00384420` and `0x003843F0`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "licd"; no code compares it |
| `+0x04` | `u16` | width | 24 on every board |
| `+0x06` | `u16` | height | 24 on every board |
| `+0x08` | `u16[576]` | cells | row-major, cell(col, row) = cells[row * width + col]; `0xFFFF` = no square |

A cell holds a node number, 0-360, an index into the license node table: section 12 of `battle_pack.bin`, bound
to `0x02EBF038` by the battle data binder (`0x00236D5C`-`0x00236D67`), 361 records of 24 bytes. The id check
`0x00322C50` bounds a node number by that table's count (`0x00322FCB`-`0x00322FD9`). What a node record holds and what
buying a square does are on [Licenses](licenses.md).

### The readers

Six functions read cells with the formula above, each returning `0xFFFF` for a column or row outside the board:

| Function | Sites |
|---|---|
| `0x00328990` | `0x003289F0`-`0x00328A14` |
| `0x0055E2C0` | `0x0055E32D`-`0x0055E345` |
| `0x0055E600` | `0x0055E764`-`0x0055E788`, `0x0055E864` |
| `0x00560070` | `0x005600F3`-`0x00560113`, `0x0056015B` |
| `0x0055F830` | `0x0055F8E7`-`0x0055F95A` |
| `0x003FC900` | `0x003FC94E`-`0x003FC9B4` |

The board view `0x0055B3F0` reads the width and height as bytes and keeps each plus one at `+0x559` and `+0x55A`
(`0x0055B484`-`0x0055B4A2`). The board's title and description are text ids `0x3ED + board` and `0x838 + board`
(`0x00556FE7`, `0x00557010`), rows 5-16 of `menu_command.bin` for the titles.

## Shipped data

| Board | File | Job | Squares | Second Board at |
|---:|---|---|---:|---|
| 0 | `board_1.bin` | White Mage | 139 | row 9, column 14 |
| 1 | `board_2.bin` | Uhlan | 132 | row 13, column 12 |
| 2 | `board_3.bin` | Machinist | 128 | row 6, column 9 |
| 3 | `board_4.bin` | Red Battlemage | 143 | row 8, column 7 |
| 4 | `board_5.bin` | Knight | 138 | row 10, column 10 |
| 5 | `board_6.bin` | Monk | 135 | row 5, column 13 |
| 6 | `board_7.bin` | Time Battlemage | 136 | row 9, column 13 |
| 7 | `board_8.bin` | Foebreaker | 137 | row 11, column 15 |
| 8 | `board_9.bin` | Archer | 128 | row 15, column 12 |
| 9 | `board_10.bin` | Black Mage | 138 | row 10, column 9 |
| 10 | `board_11.bin` | Bushi | 134 | row 7, column 9 |
| 11 | `board_12.bin` | Shikari | 138 | row 8, column 7 |

Every file is 1,160 bytes, magic `licd`, 24 by 24, and no node number appears twice on one board. The names are
the node records' own name words.

| Squares | Nodes |
|---|---|
| on every board | 0-3 Quickening, 18-30 the thirteen Espers, 31 Essentials, 161-180 Accessories 1-20, 181 Ribbon, 220 Martyr, 221 Inquisitor, 222 Headsman, 228 Spellbound, 236 Swiftness, 265 +190 HP, 266-275 Gambit Slot, 300 +230 HP, 301 +270 HP, 353-354 Accessories 21-22, 360 Second Board |
| on no board | 4-17, all named Quickening |
| on some boards | the other 287 nodes: 106 on one board, 35 on two, 29 on three, 57 on four, 23 on five, 10 on six, 7 on seven, 6 on eight, 1 on nine, 9 on ten, 4 on eleven |

[`license-board-squares.tsv`](license-board-squares.tsv) lists all 1,626 filled squares of the twelve boards, one
line each: the board, its file and job, the row and column (0-23, row first, as the grid is stored from `+8`), the
node number, and the node's name and LP cost from the node record (`+0x00` name word, `+0x04` LP;
[Licenses](licenses.md)). It is produced by `Database/Tools/catalogues/license_boards.py`, which checks each board's
square count and Second Board square against the table above.

## Loader behaviour

1. `BattleStorage_InitializeWorkArrays` zeroes the twelve slots and requests each board once (`0x002369E5`-`0x00236A24`).
2. A slot that already holds a board is not requested again (`0x00238320`-`0x00238327`).
3. The grid is used as loaded: nothing writes a board file, and the header's width and height are trusted by
   every reader.

## Modding notes

- A board is plain data: change a cell to move or add a square, `0xFFFF` to remove one. Every node number must
  stay below the node table's count, 361.
- Edit the `in` and `ch` copies together; the `cn` and `kr` copies are never loaded.
- The loader accepts any four bytes in place of `licd`.

## Related

- [Licenses](licenses.md) - the node records, buying a square and the license test.
- [Party members](../Party/party-members.md) - the catch-up that counts owned licenses.
