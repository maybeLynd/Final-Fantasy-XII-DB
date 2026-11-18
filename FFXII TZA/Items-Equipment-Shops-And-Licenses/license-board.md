[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / License Board

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| License Board: the twelve job board files, the square grid each holds, and the squares every board shares | format | Items, equipment, shops and licenses | Licenses | The licd board file: its 8-byte header and its 24 by 24 grid of two-byte node numbers, what a node number indexes and the empty-square value, which file each language loads and how, the six functions that read the grid, the twelve job boards with their square counts and Second Board square, the sixty squares on every board and the fourteen Quickening nodes on no board. | 0x02EBF1A0, 0x00238260, 0x02EBF038, 0x00328990, 0x0055B3F0, 0x00556F90 |

## What the player sees

- Each of the twelve jobs has its own License Board, a grid of squares the character buys one at a time.
- Sixty squares are on every board: the Espers, the Quickenings' first four squares, Essentials, the accessory
  squares with Ribbon, the gambit slots, eight augment squares (Martyr, Inquisitor, Headsman, Spellbound,
  Swiftness, +190 HP, +230 HP and +270 HP) and Second Board, which opens a second job.
- The boards are the same in every language.

## Where it comes from

The boards are the files `board_1.bin` to `board_12.bin`. Every language's file path table names them at indices
71-82, and the old single board `license_board.bin`, a file of the same format, at index 70. Nine tables, those of
the Japanese, US, French, German, Italian, Spanish, UK, ASIA and IN languages, point at the copies in
`test_battle/in/BinaryFile/`, and the Korean and the two Chinese tables at `test_battle/ch/BinaryFile/`; the two
sets are identical. The copies in the `cn` and `kr` folders differ and are not named by any table.

The `cn` and `kr` copies of each board file are byte-identical too. A `cn` or `kr` board differs from the read one in
two cells only: it holds the Second Board, node 360 (`0x168`), in another square, and leaves the read board's Second
Board square empty (`0xFFFF`).

`BattleStorage_InitializeWorkArrays` clears the twelve board slots at `0x02EBF1A0` and asks `0x00238260(k)` for
each board *k* from 0 to 11 (`0x002369E5`-`0x00236A24`). When slot *k* is empty, `0x00238260` requests file index
`0x47 + k` (`0x0023836A`-`0x0023837D`), so board *k* is `board_{k+1}.bin`; that board's callback stores the loaded
file's address in slot *k*, releasing a board already there with `0x003844F0` first (`0x00238390`-`0x002383AA` for
board 0). No request for index 70 is made by the calls to the
file request functions `0x00384420` and `0x003843F0`.

A board file only places squares on a grid: each square holds a number that points to a row of the license list inside
`battle_pack.bin`, and that row gives the square's name, LP cost and what it grants. Which squares a character owns is
saved with that character, not in the board files.

## Layouts

All multi-byte fields are little-endian.

Offsets are from the start of the file. The board's slot holds the loaded file's address as the callback stores it
(`0x002383AA`), and the readers index the file directly: the width at `+0x04` (`0x003289F0`), the height at `+0x06`
(`0x00328A03`) and a cell at `+0x08` plus twice `row * width + col` (`0x00328A0C`-`0x00328A14`).

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

Seven functions read cells with the formula above, `cells[row * width + col]`, and only when `col < width` and
`row < height`, the `u16` width and height compared as signed ints in six and as `u16` in `0x003FC900`
(`0x00328A01`/`0x00328A0A`, `0x0055C0B7`/`0x0055C0C0`, `0x0055E333`/`0x0055E33B`, `0x0055E773`/`0x0055E77C`,
`0x005600FB`/`0x00560105`, `0x0055F941`/`0x0055F94A`, `0x003FC99B`/`0x003FC9A2`).

For a column or row outside the board, six return `0xFFFF` and `0x0055BFF0` returns its fourth argument (`0x0055C0D3`).
`0x0055BFF0` takes its board from the slot array at
`0x02EBF1A0` + 8 x a signed slot byte (`0x0055C0A0`), addressed relative to the image base (`0x0055C0A8`):

| Function | Sites |
|---|---|
| `0x00328990` | `0x003289F0`-`0x00328A14` |
| `0x0055BFF0` | `0x0055C0B0`-`0x0055C0CC` |
| `0x0055E2C0` | `0x0055E32D`-`0x0055E345` |
| `0x0055E600` | `0x0055E764`-`0x0055E788`, `0x0055E864` |
| `0x00560070` | `0x005600F3`-`0x00560113`, `0x0056015B` |
| `0x0055F830` | `0x0055F8E7`-`0x0055F95A` |
| `0x003FC900` | `0x003FC94E`-`0x003FC9B4` |

The board view `0x0055B3F0` reads the width and height as bytes and keeps each plus one at `+0x559` and `+0x55A`
(`0x0055B484`-`0x0055B4A2`). The board's title and description are text ids `0x3ED + board` and `0x838 + board`
(`0x00556FE7`, `0x00557010`), rows 5-16 of `menu_command.bin` for the titles.

`0x0055F830(view)` first walks the six qwords from the view's `+0x150`: a pointer that is not null goes
to `0x003697F0` and its qword is set to 0 (`0x0055F83D`-`0x0055F878`). The member count is the signed byte
`+0xB2C` of `[0x0209AC30]`; with 0 or less the body returns (`0x0055F87A`-`0x0055F899`). For each member
index i it asks `0x00282DF0` for the dword at view `+0x120 + 4 × i` and `0x003236B0` for the answer's
byte `+0x60`; an answer byte of `0xFF` leaves that member's qword at 0 (`0x0055F8C0`-`0x0055F8D5`).

Otherwise the board is `[0x02EBF1A0 + 8 × byte]`, the byte taken signed. `0x002497B0` is asked for
`4 × width × height` bytes, the board's words `+0x04` and `+0x06`; `0x00861EC0(buffer, 0, size)`
follows, and the buffer goes to the view's qword `+0x150 + 8 × i` (`0x0055F8DB`-`0x0055F90C`). The buffer
takes one 4-byte entry per square, row by row (`0x0055F910`-`0x0055F9DF`).

The buffer address is used with no null test (`0x0055F8F7`-`0x0055F90C`). A square's grid word is the
board's word `+0x08 + 2 × (width × row + column)` (`0x0055F94C`-`0x0055F95A`).

A square whose grid word is `0xFFFF` gets word `+0x00` = `0xFFFF` and word `+0x02` = 0
(`0x0055F95A`-`0x0055F962`, `0x0055F9B5`-`0x0055F9BD`). So does a square for which
`0x00323600(byte +0x60, grid word, 0)` answers 3, 4, 5 or 8, and a square with a grid word of `0x10A`
to `0x113` while `0x00283730(0x4B9)` answers 0 (`0x0055F964`-`0x0055F99A`). Any other square gets that
`0x00323600` answer in word `+0x00` and, in word `+0x02`, the byte `+0x21` of the record that
`0x0035D330(0x19, grid word)` answers, read with no null test (`0x0055F99C`-`0x0055F9AF`).

## Shipped data

| Board | File | Job | Squares | Second Board at | Second Board in the cn and kr copies |
|---:|---|---|---:|---|---|
| 0 | `board_1.bin` | White Mage | 139 | row 9, column 14 | row 4, column 18 |
| 1 | `board_2.bin` | Uhlan | 132 | row 13, column 12 | row 5, column 17 |
| 2 | `board_3.bin` | Machinist | 128 | row 6, column 9 | row 6, column 19 |
| 3 | `board_4.bin` | Red Battlemage | 143 | row 8, column 7 | row 4, column 15 |
| 4 | `board_5.bin` | Knight | 138 | row 10, column 10 | row 6, column 17 |
| 5 | `board_6.bin` | Monk | 135 | row 5, column 13 | row 8, column 18 |
| 6 | `board_7.bin` | Time Battlemage | 136 | row 9, column 13 | row 5, column 16 |
| 7 | `board_8.bin` | Foebreaker | 137 | row 11, column 15 | row 12, column 17 |
| 8 | `board_9.bin` | Archer | 128 | row 15, column 12 | row 8, column 17 |
| 9 | `board_10.bin` | Black Mage | 138 | row 10, column 9 | row 8, column 15 |
| 10 | `board_11.bin` | Bushi | 134 | row 7, column 9 | row 4, column 19 |
| 11 | `board_12.bin` | Shikari | 138 | row 8, column 7 | row 5, column 15 |

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
[Licenses](licenses.md)). Each board's square count and Second Board square in it agree with the table above.

`license_board.bin`, the single 24 x 24 board at index 70, ships in `ch`, `cn`, `in` and `kr`, four identical
1,160-byte copies. No call site requests index 70: the one kind-2 request `0x00384420` is reached only from the
pack, board and text-group loads (`0x0038440A`, `0x0023837D`, `0x0023861E`).

The pack holds the same board as its entry `+0x11C`, equal to the file for its 1,160 bytes; the battle-pack load
stores its address at `0x02EBF200` (`0x00237031`), and no instruction reads that slot
([Authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md)). The board screen reads only
the twelve job boards above.

[`license-board-legacy.tsv`](license-board-legacy.tsv) lists all 576 cells of that board, row by row: 300 hold a node
and the other 276 the empty marker `0xFFFF`. The node names and LP costs are those of the current node table, entry
`+0x34`, read the same way as for the twelve job boards. The file's sha256 is
`236b1ab4d59a6d78f399b7e231d13800f7947f28b5bb95f2670f97bcfc2f3ab0`.

| Column | Meaning |
|---|---|
| `row`, `column` | the cell, 0 to 23 each |
| `cell` | the raw `u16`, `0xFFFF` for an empty square |
| `name`, `lp_cost` | the node's name and LP cost; `-` for an empty square |

## Loader behaviour

1. `BattleStorage_InitializeWorkArrays` zeroes the twelve slots and requests each board once (`0x002369E5`-`0x00236A24`).
2. A slot that already holds a board is not requested again (`0x00238320`-`0x00238327`).
3. The grid is used as loaded: nothing writes a board file, and the header's width and height are trusted by
   every reader.

## Modding notes

- A board is plain data: change a cell to move or add a square, `0xFFFF` to remove one. Every node number must
  stay below the node table's count, 361.
- Edit the `in` and `ch` copies together; the `cn` and `kr` copies are never loaded. Each board is read at the
  size its language's size table gives, 1,160 bytes, so a board of another size needs index `0x47 +` board changed
  in every `.fst` ([File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)).
- The loader accepts any four bytes in place of `licd`.

## Related

- [Licenses](licenses.md) - the node records, buying a square and the license test.
- [Party members](../Party/party-members.md) - the catch-up that counts owned licenses.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Presentation: `0x0035D330` is called by `0x003BBD00`, `0x00506700`; those functions are documented on
  [augments](../Damage-And-Battle-Formulas/augments.md), [battle numbers](../Menus-And-HUD/battle-numbers.md).
- Save load settings: `0x00282DF0` is called by `0x00583D60`; those functions are documented on
  [native limits](../Engine-Core/native-limits.md).
- Story event quest hunt: `0x00283730` calls `0x0032A8A0`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
