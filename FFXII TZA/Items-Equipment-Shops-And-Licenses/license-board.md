---
title: "License Board: the twelve job board files, the square grid each holds, and the squares every board shares"
kind: "format"
category: "Items, equipment, shops and licenses"
addresses: "02EBF1A0, 00238260, 02EBF038, 00328990, 0055B3F0, 00556F90"
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

`BattleStorage_InitializeWorkArrays` clears the twelve board slots at `02EBF1A0` and asks `00238260(k)` for
each board *k* from 0 to 11 (`002369E5`-`00236A24`). When slot *k* is empty, `00238260` requests file index
`0x47 + k` (`0023836A`-`0023837D`), so board *k* is `board_{k+1}.bin`; that board's callback stores the loaded
file's address in slot *k*, releasing a board already there with `003844F0` first (`00238390`-`002383AA` for
board 0). No request for index 70 is made by the calls to the
file request functions `00384420` and `003843F0`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[4]` | magic | "licd"; no code compares it |
| `04` | `u16` | width | 24 on every board |
| `06` | `u16` | height | 24 on every board |
| `08` | `u16[576]` | cells | row-major, cell(col, row) = cells[row * width + col]; `0xFFFF` = no square |

A cell holds a node number, 0-360, an index into the license node table: section 12 of `battle_pack.bin`, bound
to `02EBF038` by the battle data binder (`00236D5C`-`00236D67`), 361 records of 24 bytes. The id check
`00322C50` bounds a node number by that table's count (`00322FCB`-`00322FD9`). What a node record holds and what
buying a square does are on [Licenses](licenses.md).

### The readers

Six functions read cells with the formula above, each returning `0xFFFF` for a column or row outside the board:

| Function | Sites |
|---|---|
| `00328990` | `003289F0`-`00328A14` |
| `0055E2C0` | `0055E32D`-`0055E345` |
| `0055E600` | `0055E764`-`0055E788`, `0055E864` |
| `00560070` | `005600F3`-`00560113`, `0056015B` |
| `0055F830` | `0055F8E7`-`0055F95A` |
| `003FC900` | `003FC94E`-`003FC9B4` |

The board view `0055B3F0` reads the width and height as bytes and keeps each plus one at `+0x559` and `+0x55A`
(`0055B484`-`0055B4A2`). The board's title and description are text ids `0x3ED + board` and `0x838 + board`
(`00556FE7`, `00557010`), rows 5-16 of `menu_command.bin` for the titles.

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

## Loader behaviour

1. `BattleStorage_InitializeWorkArrays` zeroes the twelve slots and requests each board once (`002369E5`-`00236A24`).
2. A slot that already holds a board is not requested again (`00238320`-`00238327`).
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
