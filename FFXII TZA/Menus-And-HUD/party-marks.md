---
title: "Party marks: which party member cannot wear an item or has learned a magick or technick, the bitmap behind the marks, and when it is rebuilt"
kind: "system"
category: "Menus and HUD"
addresses: "002826F0, 00282A40, 00282F10, 00282EE0, 003FCAD0"
---

## What the player sees

- In the Status and Equip screen's list, a row of equipment, magicks or technicks carries a mark for each party member.
- A piece of equipment is marked for a member who cannot wear it, and the member who wears it shows that member's own
  mark.
- A magick or technick shows a member's mark when that member has it and holds its license.

## How it works

### The bitmap

The menu root `[0209AC30]` keeps one byte per id from `+0xB2E`, with bit n for the party member whose record `+0x60`
is n (`002828A7`). An id becomes its byte index the same way in all three functions that touch it (`0028281F`-`00282848`,
`00282F10`):

| Ids | Index |
|---|---|
| `0x1000`-`0x11A4`, equipment | `id - 0x1000` |
| `0x4000`-`0x4018`, technicks | `id - 0x3E5C`, from `0x1A4` |
| `0x3000`-`0x3051`, magicks | `id - 0x2E44`, from `0x1BC` |
| anything else | `0` |

`00282F10(id, member)` answers the member's bit. A scan of every listed function for a memory operand with the
displacement `0xB2E` finds only `002826F0`, `00282A40` and `00282F10`.

### Building it

`002826F0` rebuilds the bits of every member and `00282A40(member)` those of one member. The Party Menu runs
`002826F0` from `00281AE0` (`00281CB0`), and the license board's grid runs `00282A40` (`0055DA89`;
[License Board screen](license-board-screen.md)). For each member pointer of the nine at `[0209AC30] + 0xAC8` whose
record has a member number 0-5 at `+0x60` and bit 1 of `+0x00` clear:

1. `00282EE0(record)` gives the record's place among the nine `0xC0`-byte records at `[0209AC30] + 0x408`, and
   `0031C4C0` its party slot.
2. For each id of the category lists 1-4 (`00252F40`, `00252FA0`), it clears the bit, fills a class-6 query record
   (`0031C5D0`), and sets the bit unless the record's `+0x38` is `0x17`-`0x1A` (`002CCA00`) or the member can wear the
   item in its slot `+0x4C` (`00317B70`, [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)).
3. For each id of the category lists 9 and 8, it clears the bit and sets it when the member owns the magick or
   technick and holds its license (`00306340`, [Command availability](../Battle-Actions/command-availability.md)).

So an equipment bit means "cannot wear" and an ability bit means "has it".

### Showing it

`003FCAD0`, the row painter of the equipment list under the Status and Equip screen, sets each member's mark frame
(`003FCB9D`):

| Row | Bit | Frame |
|---|---|---|
| any | - | 7, the default |
| equipment | set | 8, or 9 when the board reader `003FC900` answers non-zero for either of the member's two license boards (`00323670`, `00323630`) |
| equipment worn by the member | - | the member's own mark, `002C9B30(member, 5) + 1` |
| magick or technick | clear | 8 |
| magick or technick | set | the member's own mark |

`002C9B30(n, field)` reads field 0-8 of member n's row of seven `0x10`-byte rows at `009170C0`, clamping n to 0-6.

## Modding notes

- A new equipment id above `0x11A4`, or a magick or technick past the ranges above, shares byte 0 with the first
  equipment id.
- Equipment whose query record `+0x38` is `0x17`-`0x1A` is never marked as unwearable.

## Related

- [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md) - the wear test.
- [Command availability](../Battle-Actions/command-availability.md) - owning and licensing an ability.
- [License Board screen](license-board-screen.md) - the grid that rebuilds one member's bits.
