---
title: "Battle and menu text tables: the word banks in battle_pack.bin, the st2e string tables behind menu and help text, and how a text id becomes a string"
kind: "format"
category: "Game files and data tables"
addresses: "003214B0, 002B58B0, 02EBF170, 002F9860, 002F9920, 02EC3D80, 02F973C0, 01E09F68, 002385D0, 002FA560, 002F7660, 00238640, 002F83E0, 00248700, 0053EB90, 01CEB638, 003846F0, 003845F0, 002AC2F0, 002491B0, 00563520, 00292260, 002922C0, 00292190, 002F7680, 002F79C0"
---

## What the player sees

Every ability, item, status, place and monster-family name, every gambit target line and every
menu label and help line is a string looked up by number. The battle names live in one block of
`battle_pack.bin`, loaded at start-up; the menu and help text lives in separate files that a menu
loads when it first needs them.

## Where it comes from

- **Word banks:** entry `+F8`<sub>h</sub> of `battle_pack.bin` (`word.bin`), bound to the registry slot
  `02EBF170` at start-up ([authored data tables](authored-data-tables.md)).
- **Text groups:** kind-2 files under `ps2data/image/ff12/test_battle/<language>/binaryfile/`, one
  per group, listed by the byte table `01E09F68`. 26 ship; group 27's file, `menu05`, is named but
  not shipped.

| Groups | Kind-2 ids | Files |
|---|---|---|
| 0 | none | — |
| 1–4 | 20–23 | `menu_command`, `menu_message`, `help_menu`, `help_action` |
| 5 | 1 | `key_signal` |
| 6–19 | 43–56 | `menu_mapname`, `penelosdiary`, `help_penelosdiary`, `listhelp_common`, `listhelp_action`, `listhelp_sobicategory`, `listhelp_status`, `listhelp_ability`, `listhelp_eventitem`, `listhelp_gambit`, `listhelp_targetchip`, `listhelp_license`, `menu_command_template`, `menu_expansion` |
| 20, 21 | 24, 25 | `listhelp_daijinamono`, `questtitle` |
| 22–27 | 62–67 | `menu00` to `menu05` |

`battle_pack.bin` has entries at the same positions, which the registry builder never reads and
which are not the same tables: the pack's `menu_command` entry is 32 rows of 8 bytes, the file 428
rows of 4.

## Layouts

```python
word (battle_pack +0xF8)   +0x00 u16 bank count, +0x04 u32 bank offsets[count + 1] (from the word block)
word bank                  +0x00 u16 row count, +0x04 u32 row offsets[count] (from the bank)
word row                   00 00, then NUL-terminated strings
bank:row word              bits 11-15 bank, bits 0-10 row

st2e string table          the shared table header ('st2e', +0x04 rows, +0x08 row bytes, +0x0C rows),
                           each row a u32 text id, group * 10000 + n,
                           +0x14 sub-directory: u16 count (1), u32 offset of the text block
text block                 +0x00 u32 string count, +0x04 u32 string offsets[count] (from the block),
                           then NUL-terminated strings
text id                    group * 1000 + row (002F9860), or a row's own id (002F9920)
```

## Shipped data

The `us` word banks, with their first rows:

| Bank | Rows | First rows |
|---|---|---|
| 0 | 545 | Cure, Blindna… |
| 1 | 544 | Unarmed, Broadsword |
| 2 | 1 | dummy |
| 3 | 362 | Red Spiral, White Whorl |
| 4 | 63 | Attack, Magicks |
| 5 | 32 | KO, Stone |
| 6 | 284 | Foe: party leader's target, Foe: nearest visible |
| 7 | 16 | NOT USED |
| 8 | 629 | No name, Vaan |
| 9 | 128 | Antidote Set, Unassuming Surcoat |
| 10 | 129 | NOT USED |
| 11 | 512 | Teleport Stone, Reserve |
| 12 | 512 | Rabanastre, Nalbina Fortress |
| 13 | 16 | Hume, Humanoid |
| 14 | 64 | Titantoise, Gator |

All 3,837 rows use the packed form. Two `us` text groups, for scale: `menu_command` has 428 strings
(`Yes`, `No`, `-`, …) and `listhelp_ability` 64 (`Improves chance to hit.` at row 2).

Strings are glyph codes, not ASCII. A byte `20`<sub>h</sub> or above is glyph `byte − 20h` of the language's
font, and a lead byte `10`<sub>h</sub>–`1F`<sub>h</sub> with the byte after it is a two-byte glyph
([fonts](../Menus-And-HUD/fonts.md)); `02`<sub>h</sub> is a line break, `04`<sub>h</sub> a space and `0F`<sub>h</sub> starts an escape
([text codes](../Menus-And-HUD/text-codes.md)).

In the `us` text, `20`<sub>h</sub>–`39`<sub>h</sub> are `A`–`Z`, `3A`<sub>h</sub>–`53`<sub>h</sub>
`a`–`z`, `A0`<sub>h</sub> `&`, `A7`<sub>h</sub> `,`, `A8`<sub>h</sub> `.` and `AA`<sub>h</sub> `:`. In `listhelp_daijinamono`, the Korean and
Chinese text is two-byte codes with lead bytes `10`<sub>h</sub>–`18`<sub>h</sub>, and the Japanese text mixes single-byte
codes, many at `80`<sub>h</sub> and above, with two-byte ones.

## Loader behaviour

### Word banks

`003846F0` binds the word block at depth 1, so every bank offset and every row offset becomes an
address. `003214B0(word)` takes bank `(word >> 11) & 1Fh` and row `word & 7FFh`, returns 0 when
either is past its count, and otherwise the row's address. Many readers instead index the banks
inline with no bounds test, among them the unit name lookup in `0023A570`.

A row starts with two zero bytes. `002B58B0(row, k)` skips them and then `k` strings and returns the
string it reaches; a row without the two zero bytes is returned as it is.

### Text groups

`002F9860(id)` splits the id into group `id / 1000` and row `id % 1000`. It returns the string when the
group is below 28, its file is resident (`02EC3D80[group]`), and the row is below the table's
`+04`<sub>h</sub>; otherwise, or when the table or its `+14`<sub>h</sub> sub-directory is null, it returns the empty string at
`01CEB638`. The string is entry `row` of the text block that the table's `+14`<sub>h</sub> sub-directory names.

`002F9920(id)` is the second form: group `id / 10000`, then a linear search of the table's rows for a
row equal to `id`, returning the text-block string at that row's position, or `01CEB638`. A row's
id need not be `group × 10000 + row`: `us` `menu_command` row 5 is `10100`, so that string is both
`1005` and `10100`. In all nine languages 144 files number their rows from `group × 10000` in order
and 90 do not. Both resolvers divide a signed id, so an id below −999 gives a negative group that
passes their `< 28` test.

A group is loaded on demand:

1. `002FA560(group)` passes the group's setter (`002F7660` and its neighbours, `20`<sub>h</sub> bytes apart) to
   `002385D0`, which requests kind-2 file `01E09F68[group]` (`00384420`); group 0 has no file.
2. On delivery the setter stores the file at `02EC3D80[group]` and jumps to `00238640`, which binds
   it into `02F973C0[group]` with `003845F0`.
3. `002F83E0(group)` frees the file and clears `02EC3D80[group]`.

`002FA560` is called from the menu widget handler `00248700`, for the group the widget names when
it is not yet resident, and from `0053EB90` for groups 25 and 26.

The setters are not in group order: `002F7680` serves group 4 and `002F79C0` group 21. Each stores
its file at `02EC3D80[group]` and jumps to `00238640` with the group in `ecx`:

| Groups | Setters |
|---|---|
| 0-6 | `002F7660`, `002F7900`, `002F7980`, `002F76A0`, `002F7680`, `002F76E0`, `002F7960` |
| 7-13 | `002F79A0`, `002F76C0`, `002F7740`, `002F7720`, `002F77E0`, `002F7800`, `002F7700` |
| 14-20 | `002F7780`, `002F77A0`, `002F7820`, `002F77C0`, `002F7920`, `002F7940`, `002F7760` |
| 21-27 | `002F79C0`, `002F7840`, `002F7860`, `002F7880`, `002F78A0`, `002F78C0`, `002F78E0` |

`002491B0(request group, group)` hands a group to that handler (`00244F50(D0h, 00248700, ...)`) and counts
it on the request group. `00292260` asks for groups 10, 20 and 14, `002922C0` (from `00556500`) for 17, and
`00292190` (from `0057B780`) for 10, 20, 14 and 16, each only when `002F8040(group)` finds
`02EC3D80[group]` empty. At start-up `0022A4B0` runs `00563520`, which takes a request group with the
completion function `00563550` (`002486B0`), asks for groups 10, 20 and 14 and closes it (`00249410`).

## Modding notes

- Keep a word row's two leading zero bytes; without them `002B58B0` returns the row itself whatever
  string number is asked for.
- A word bank holds at most 2,048 rows and there are at most 32 banks.
- The `group × 1000` form reaches rows 0–999 only; rows past that need their `group × 10000` id
  (`us` `menu04` has 1,024 rows). An id past the table shows as empty text.
- Strings must be written in the font's glyph codes for the language, not ASCII.

## Related

- [Authored data tables](authored-data-tables.md): the registry slot, the table header and the binders.
- [Fonts](../Menus-And-HUD/fonts.md): how a glyph code becomes a glyph.
- [Text codes](../Menus-And-HUD/text-codes.md): the control and escape codes inside strings.
