---
title: "Party marks: which party member cannot wear an item or has learned a magick or technick, the bitmap behind the marks, and when it is rebuilt"
kind: "system"
category: "Menus and HUD"
addresses: "0x002826F0, 0x00282A40, 0x00282F10, 0x00282EE0, 0x003FCAD0"
---

## What the player sees

- In the Status and Equip screen's list, a row of equipment, magicks or technicks carries a mark for each party member.
- A piece of equipment is marked for a member who cannot wear it, and the member who wears it shows that member's own
  mark.
- A magick or technick shows a member's mark when that member has it and holds its license.

## How it works

### The bitmap

The menu root `[0x0209AC30]` keeps one byte per id from `+0xB2E`, with bit value `1 << n` for the party member whose
record `+0x60` is n (`0x002828A7`). An id becomes its byte index the same way in all three functions that touch it
(`0x0028281F`-`0x00282848`, `0x00282F10`):

| Ids | Index |
|---|---|
| `0x1000`-`0x11A4`, equipment | `id - 0x1000` |
| `0x4000`-`0x4018`, technicks | `id - 0x3E5C`, from `0x1A4` |
| `0x3000`-`0x3051`, magicks | `id - 0x2E44`, from `0x1BC` |
| anything else | `0` |

`0x00282F10(id, member)` answers the member's bit. No other function in the image has a memory operand with the
displacement `0xB2E`.
`member` is the member's record: it tests bit value `1 << +0x60`, that field read as a byte, in the id's byte and
answers 1 when it is set and 0 otherwise (`0x00282F4F`-`0x00282F6E`); the three ranges are tested unsigned
(`0x00282F13`-`0x00282F48`).

### Building it

`0x002826F0` rebuilds the bits of every member and `0x00282A40(member)` those of one member. The Party Menu runs
`0x002826F0` from `0x00281AE0` (`0x00281CB0`), and the license board's grid runs `0x00282A40` (`0x0055DA89`;
[License Board screen](license-board-screen.md)). For each member pointer of the nine at `[0x0209AC30] + 0xAC8` whose
record has a member number 0-5 at `+0x60` and bit `0x2` of `+0x00` clear:

1. `0x00282EE0(record)` gives the record's place among the nine `0xC0`-byte records at `[0x0209AC30] + 0x408`, and
   `0x0031C4C0` its party slot.
2. For each id of the category lists 1-4 (`0x00252F40`, `0x00252FA0`,
   [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md)), it clears the bit, fills a class-6 query record
   (`0x0031C5D0`), and sets the bit unless the record's `+0x38` is `0x17`-`0x1A` (`0x002CCA00`) or the member can wear the
   item in its slot `+0x4C` (`0x00317B70`, [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)).
3. For each id of the category lists 9 and 8, it clears the bit and sets it when the member owns the magick or
   technick and holds its license (`0x00306340`, [Command availability](../Battle-Actions/command-availability.md)).

So an equipment bit means "cannot wear" and an ability bit means "has it".

### Showing it

`0x003FCAD0`, the row painter of the equipment list under the Status and Equip screen, sets each member's mark frame
(`0x003FCB9D`):

| Row | Bit | Frame |
|---|---|---|
| any | - | 7, the default |
| equipment | set | 8, or 9 when the board reader `0x003FC900` answers non-zero for either of the member's two license boards (`0x00323670`, `0x00323630`) |
| equipment worn by the member | - | the member's own mark, `0x002C9B30(member, 5) + 1` |
| magick or technick | clear | 8 |
| magick or technick | set | the member's own mark |

`0x003FC900(board, word)` answers 0 for a board number above 11 and for an empty board
slot `0x02EBF1A0 + 8 × board` (`0x003FC909`-`0x003FC939`). Otherwise it walks every cell of
the board; for each cell that is not `0xFFFF` it takes the licence record of that
number: the table the pointer `0x02EBF038` names holds a dword at `+0xC`, which
`0x0020E600` turns into the first record's address, and a size word at `+8`; the record
is read at the low dword of `first + size × number` (`0x003FC9F0`-`0x003FC9F2`).

`0x003FC900` answers 1 as soon as one of the record's eight words
at `+8` equals its second argument's word, and 0 with no match (`0x003FC960`-`0x003FCA66`).

`0x003FCAD0(list, row, first, last)` works on the mark widgets `[list + 0x10]` from `first` to `last`
(`0x003FCAE0`-`0x003FCB22`):

- It gives every one frame 7 at `+0x0A`, clears bit `0x1` of `+0x08` and copies frame 7's palette byte, byte `+0x3F`
  of the mark's group `+0x20`, to `+0x39` (`0x003FCB00`-`0x003FCB1C`). A row whose id `+0x08` is `0xFFFF` stops there
  (`0x003FCB24`-`0x003FCB2E`).
- For each of the nine member slots (`0x00282DF0`) that `0x00282FA0` accepts, a member number 0-5 at `+0x60` and record
  bit `0x2` clear, it sets bit `0x1` of mark `first + slot`, held at `last` (`0x003FCB50`-`0x003FCB81`); the mark index
  moves on for every slot (`0x003FCBEF`).
- It asks `0x0035D330(1, id << 16)` for the query record and `0x00282F10` for the bit (`0x003FCB85`-`0x003FCB9D`). Kind 6
  at the record's `+0x00` is equipment; kinds 8 and 9 are the magicks and technicks, which first get frame 8; other
  kinds keep frame 7 (`0x003FCBA2`-`0x003FCBBC`).
- Equipment runs the worn test whether its bit is set or not, over the five words `+0x9A + 4 x k` of the member
  record (`0x003FCC88`-`0x003FCCBA`); a match gives the member's own mark (`0x003FCBC5`-`0x003FCBE4`). Each frame it writes
  takes its palette byte from the group's record `frame x 8 + 7` (`0x003FCBB5`, `0x003FCC65`, `0x003FCC74`, `0x003FCBDC`).

`0x002C9B30(n, field)` reads field 0-8 of member n's row of seven `0x10`-byte rows at `0x009170C0`, clamping n to 0-6.
Fields 0 to 5 are the row's signed bytes `+0` to `+5`, field 6 the float `+8` cut to an
integer, field 7 the signed byte `+0xC` and field 8 the low dword of the row's own
address; any other field number answers 0 (`0x002C9B52`-`0x002C9BA1`, jump table
`0x002C9BA4`).

## Modding notes

- A new equipment id above `0x11A4`, or a magick or technick past the ranges above, shares byte 0 with the first
  equipment id.
- Equipment whose query record `+0x38` is `0x17`-`0x1A` is never marked as unwearable.

## Related

- [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md) - the wear test.
- [Command availability](../Battle-Actions/command-availability.md) - owning and licensing an ability.
- [License Board screen](license-board-screen.md) - the grid that rebuilds one member's bits.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Platform online achievements: `0x00282FA0` is called by `0x003162E0`, `0x00316760`; those functions are documented on
  [achievements](../Steam-And-Achievements/achievements.md), [gil](../Rewards-EXP-Gil-And-Loot/gil.md).
- Presentation: `0x0035D330` is called by `0x003BBD00`, `0x00506700`; those functions are documented on
  [augments](../Damage-And-Battle-Formulas/augments.md), [battle numbers](battle-numbers.md).
- Save load settings: `0x00282DF0` is called by `0x00583D60`; those functions are documented on
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md).
