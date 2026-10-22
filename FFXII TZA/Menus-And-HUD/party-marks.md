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

The menu root `[0x0209AC30]` keeps one byte per id from `+0xB2E`, with bit n for the party member whose record `+0x60`
is n (`0x002828A7`). An id becomes its byte index the same way in all three functions that touch it (`0x0028281F`-`0x00282848`,
`0x00282F10`):

| Ids | Index |
|---|---|
| `0x1000`-`0x11A4`, equipment | `id - 0x1000` |
| `0x4000`-`0x4018`, technicks | `id - 0x3E5C`, from `0x1A4` |
| `0x3000`-`0x3051`, magicks | `id - 0x2E44`, from `0x1BC` |
| anything else | `0` |

`0x00282F10(id, member)` answers the member's bit. A scan of every listed function for a memory operand with the
displacement `0xB2E` finds only `0x002826F0`, `0x00282A40` and `0x00282F10`.

### Building it

`0x002826F0` rebuilds the bits of every member and `0x00282A40(member)` those of one member. The Party Menu runs
`0x002826F0` from `0x00281AE0` (`0x00281CB0`), and the license board's grid runs `0x00282A40` (`0x0055DA89`;
[License Board screen](license-board-screen.md)). For each member pointer of the nine at `[0x0209AC30] + 0xAC8` whose
record has a member number 0-5 at `+0x60` and bit 1 of `+0x00` clear:

1. `0x00282EE0(record)` gives the record's place among the nine `0xC0`-byte records at `[0x0209AC30] + 0x408`, and
   `0x0031C4C0` its party slot.
2. For each id of the category lists 1-4 (`0x00252F40`, `0x00252FA0`), it clears the bit, fills a class-6 query record
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

`0x002C9B30(n, field)` reads field 0-8 of member n's row of seven `0x10`-byte rows at `0x009170C0`, clamping n to 0-6.

## Modding notes

- A new equipment id above `0x11A4`, or a magick or technick past the ranges above, shares byte 0 with the first
  equipment id.
- Equipment whose query record `+0x38` is `0x17`-`0x1A` is never marked as unwearable.

## Related

- [Equipment](../Items-Equipment-Shops-And-Licenses/equipment.md) - the wear test.
- [Command availability](../Battle-Actions/command-availability.md) - owning and licensing an ability.
- [License Board screen](license-board-screen.md) - the grid that rebuilds one member's bits.
