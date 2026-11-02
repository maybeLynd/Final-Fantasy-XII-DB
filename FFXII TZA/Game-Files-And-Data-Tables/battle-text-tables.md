---
title: "Battle and menu text tables: the word banks in battle_pack.bin, the st2e string tables behind menu and help text, and how a text id becomes a string"
kind: "format"
category: "Game files and data tables"
addresses: "0x003214B0, 0x002B58B0, 0x02EBF170, 0x002F9860, 0x002F9920, 0x02EC3D80, 0x02F973C0, 0x01E09F68, 0x002385D0, 0x002FA560, 0x002F7660, 0x00238640, 0x002F83E0, 0x00248700, 0x0053EB90, 0x01CEB638, 0x003846F0, 0x003845F0, 0x002AC2F0, 0x002491B0, 0x00563520, 0x00292260, 0x002922C0, 0x00292190, 0x002F7680, 0x002F79C0"
---

## What the player sees

Every ability, item, status, place and monster-family name, every gambit target line and every
menu label and help line is a string looked up by number. The battle names live in one block of
`battle_pack.bin`, loaded at start-up; the menu and help text lives in separate files that a menu
loads when it first needs them.

## Where it comes from

- **Word banks:** entry `+0xF8` of `battle_pack.bin` (`word.bin`), bound to the registry slot
  `0x02EBF170` at start-up ([authored data tables](authored-data-tables.md)).
- **Text groups:** kind-2 files under `ps2data/image/ff12/test_battle/<language>/binaryfile/`, one
  per group, listed by the byte table `0x01E09F68`. 26 ship; group 27's file, `menu05`, is named but
  not shipped.

| Groups | Kind-2 ids | Files |
|---|---|---|
| 0 | no id | — |
| 1–4 | 20–23 | `menu_command`, `menu_message`, `help_menu`, `help_action` |
| 5 | 1 | `key_signal` |
| 6–19 | 43–56 | `menu_mapname`, `penelosdiary`, `help_penelosdiary`, `listhelp_common`, `listhelp_action`, `listhelp_sobicategory`, `listhelp_status`, `listhelp_ability`, `listhelp_eventitem`, `listhelp_gambit`, `listhelp_targetchip`, `listhelp_license`, `menu_command_template`, `menu_expansion` |
| 20, 21 | 24, 25 | `listhelp_daijinamono`, `questtitle` |
| 22–27 | 62–67 | `menu00` to `menu05` |

`battle_pack.bin` has entries at the same positions, which the registry builder never reads and
which are not the same tables: the pack's `menu_command` entry is 32 rows of 8 bytes, the file 428
rows of 4.

## Layouts

All multi-byte fields are little-endian.

```python
word (battle_pack +0xF8)   +0x00 u16 bank count, +0x04 u32 bank offsets[count + 1] (from the word block)
word bank                  +0x00 u16 row count, +0x02 u8[2] 0, +0x04 u32 row offsets[count + 1] (from the
                           bank), the last the bank's end
word row                   00 00, then NUL-terminated strings
bank:row word              mask 0xF800 bank, mask 0x7FF row

st2e string table          the shared table header ('st2e', +0x04 rows, +0x08 row bytes, +0x0C rows),
                           each row a u32 text id, group * 10000 + n,
                           +0x14 sub-directory (from the table): u16 count (1), u8[2] 0, u32 text block
                           offset (12), u32 end offset (both from the sub-directory)
text block                 +0x00 u32 string count, +0x04 u32 string offsets[count + 1] (from the block),
                           the last the strings' end, then NUL-terminated strings, then u8[0-3] 0 to a
                           4-byte end
text id                    group * 1000 + row (0x002F9860), or a row's own id (0x002F9920)
```

Binding rewrites each file in place in its buffer; nothing copies it.

- `0x003846F0` adds a directory's address to each of its count + 1 offsets, so they become addresses. At depth 1,
  as for the word block, it first does the same for the directory each of the first count entries names (the
  banks).
- For a text group, `0x003845F0` adds the table's address to each non-zero header field `+0x0C`, `+0x10`,
  `+0x18` and `+0x1C` and to `+0x14`, and `0x003846F0` rewrites the sub-directory's entries and the text
  block's offsets.
- Every rewritten field holds a 32-bit address: `0x0020E600` zero-extends it and adds `[0x01F83530]`, which is 0
  in this build ([global state accessors](../Engine-Core/global-state-accessors.md)).

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

Strings are glyph codes, not ASCII. A byte `0x20` or above is glyph `byte − 0x20` of the language's
font, and a lead byte `0x10`–`0x1F` with the byte after it is a two-byte glyph
([fonts](../Menus-And-HUD/fonts.md)); `0x02` is a line break, `0x04` a space and `0x0F` starts an escape
([text codes](../Menus-And-HUD/text-codes.md)).

In the `us` text, `0x20`–`0x39` are `A`–`Z`, `0x3A`–`0x53`
`a`–`z`, `0xA0` `&`, `0xA7` `,`, `0xA8` `.` and `0xAA` `:`. In `listhelp_daijinamono`, the Korean and
Chinese text is two-byte codes with lead bytes `0x10`–`0x18`, and the Japanese text mixes single-byte
codes, many at `0x80` and above, with two-byte ones.

## Loader behaviour

### Word banks

`0x003846F0` binds the word block at depth 1, so every bank offset and every row offset becomes an
address. `0x003214B0(word)` takes bank `(word >> 11) & 0x1F` and row `word & 0x7FF`, returns 0 when
either is past its count, and otherwise the row's address. Many readers instead index the banks
inline with no bounds test, among them the unit name lookup in `0x0023A570`.

A row starts with two zero bytes. `0x002B58B0(row, k)` skips them and then `k` strings and returns the
string it reaches; a row without the two zero bytes is returned as it is. Of its 59 callers, 14
are interface code reading a row's strings: the gambit screen (`0x00567B60`, `0x0056A890`,
`0x0056BC70`), the licence screens (`0x00558CE0`, `0x005618E0`), the battle menu's title `0x0027D480`
and the party list `0x002986E0` among them ([gambit screen](../Menus-And-HUD/gambit-screen.md),
[battle menu](../Menus-And-HUD/battle-menu.md), [party list](../Menus-And-HUD/party-list.md)).

### Text groups

`0x002F9860(id)` splits the id into group `id / 1000` and row `id % 1000`. It returns the string when the
group is below 28, its file is resident (`0x02EC3D80[group]`), and the row is below the table's
`+0x04`; otherwise, or when the table or its `+0x14` sub-directory is null, it returns the empty string at
`0x01CEB638`. The string is entry `row` of the text block that the table's `+0x14` sub-directory names.

`0x002F9920(id)` is the second form: group `id / 10000`, then a linear search of the table's rows for a
row equal to `id`, returning the text-block string at that row's position, or `0x01CEB638`. A row's
id need not be `group × 10000 + row`: `us` `menu_command` row 5 is `10100`, so that string is both
`1005` and `10100`. In all nine languages 144 files number their rows from `group × 10000` in order
and 90 do not. Both resolvers divide a signed id, so a negative group passes their `< 28` test: an id of −1000
or less for `0x002F9860` (`id / 1000`), and of −10000 or less for `0x002F9920` (`id / 10000`).

A group is loaded on demand:

1. `0x002FA560(group)` passes the group's setter (`0x002F7660` and its neighbours, `0x20` bytes apart) to
   `0x002385D0`, which requests kind-2 file `0x01E09F68[group]` (`0x00384420`); group 0 has no file.
2. On delivery the setter stores the file at `0x02EC3D80[group]` and jumps to `0x00238640`, which binds
   it into `0x02F973C0[group]` with `0x003845F0`.
3. `0x002F83E0(group)` frees the file and clears `0x02EC3D80[group]`.

`0x002FA560` is called from the menu widget handler `0x00248700`, for the group the widget names when
it is not yet resident, and from `0x0053EB90` for groups 25 and 26.

The setters are not in group order: `0x002F7680` serves group 4 and `0x002F79C0` group 21. Each stores
its file at `0x02EC3D80[group]` and jumps to `0x00238640` with the group in `ecx`:

| Groups | Setters |
|---|---|
| 0-6 | `0x002F7660`, `0x002F7900`, `0x002F7980`, `0x002F76A0`, `0x002F7680`, `0x002F76E0`, `0x002F7960` |
| 7-13 | `0x002F79A0`, `0x002F76C0`, `0x002F7740`, `0x002F7720`, `0x002F77E0`, `0x002F7800`, `0x002F7700` |
| 14-20 | `0x002F7780`, `0x002F77A0`, `0x002F7820`, `0x002F77C0`, `0x002F7920`, `0x002F7940`, `0x002F7760` |
| 21-27 | `0x002F79C0`, `0x002F7840`, `0x002F7860`, `0x002F7880`, `0x002F78A0`, `0x002F78C0`, `0x002F78E0` |

Group n's slot is the qword `0x02EC3D80` + n × 8, 0 at load (the zero-filled tail of `.data`). Its setter stores the
delivered file's 32-bit argument sign-extended to 64 bits:

| Group | Global | Set by |
|---|---|---|
| 1 | `0x02EC3D88` | `0x002F7900` (`0x002F7908`) |
| 2 | `0x02EC3D90` | `0x002F7980` (`0x002F7988`) |
| 3 | `0x02EC3D98` | `0x002F76A0` (`0x002F76A8`) |
| 4 | `0x02EC3DA0` | `0x002F7680` (`0x002F7688`) |
| 5 | `0x02EC3DA8` | `0x002F76E0` (`0x002F76E8`) |
| 6 | `0x02EC3DB0` | `0x002F7960` (`0x002F7968`) |
| 7 | `0x02EC3DB8` | `0x002F79A0` (`0x002F79A8`) |
| 8 | `0x02EC3DC0` | `0x002F76C0` (`0x002F76C8`) |
| 9 | `0x02EC3DC8` | `0x002F7740` (`0x002F7748`) |
| 10 | `0x02EC3DD0` | `0x002F7720` (`0x002F7728`) |
| 11 | `0x02EC3DD8` | `0x002F77E0` (`0x002F77E8`) |
| 12 | `0x02EC3DE0` | `0x002F7800` (`0x002F7808`) |
| 13 | `0x02EC3DE8` | `0x002F7700` (`0x002F7708`) |
| 14 | `0x02EC3DF0` | `0x002F7780` (`0x002F7788`) |
| 15 | `0x02EC3DF8` | `0x002F77A0` (`0x002F77A8`) |
| 16 | `0x02EC3E00` | `0x002F7820` (`0x002F7828`) |
| 17 | `0x02EC3E08` | `0x002F77C0` (`0x002F77C8`) |
| 18 | `0x02EC3E10` | `0x002F7920` (`0x002F7928`) |
| 19 | `0x02EC3E18` | `0x002F7940` (`0x002F7948`) |
| 20 | `0x02EC3E20` | `0x002F7760` (`0x002F7768`) |
| 21 | `0x02EC3E28` | `0x002F79C0` (`0x002F79C8`) |
| 22 | `0x02EC3E30` | `0x002F7840` (`0x002F7848`) |
| 23 | `0x02EC3E38` | `0x002F7860` (`0x002F7868`) |
| 24 | `0x02EC3E40` | `0x002F7880` (`0x002F7888`) |
| 25 | `0x02EC3E48` | `0x002F78A0` (`0x002F78A8`) |
| 26 | `0x02EC3E50` | `0x002F78C0` (`0x002F78C8`) |
| 27 | `0x02EC3E58` | `0x002F78E0` (`0x002F78E8`) |

Four functions reach the slots as one array indexed by a sign-extended group: `0x002F8040` answers 1 when a slot is not 0
(`0x002F804C`), `0x002F83E0` frees the file a slot holds and stores 0 (`0x002F83F4`-`0x002F8402`), and both resolvers test
the slot for 0 before they read the bound table at `0x02F973C0` (`0x002F989D` in `0x002F9860`, `0x002F9967` in `0x002F9920`).
`0x002F9860` then takes the row bound `+0x04` of the bound table with an unsigned compare (`0x002F98C7`).

`0x002491B0(request group, group)` hands a group to that handler (`0x00244F50(0xD0, 0x00248700, ...)`) and counts
it on the request group. `0x00292260` asks for groups 10, 20 and 14, `0x002922C0` (from `0x00556500`) for 17, and
`0x00292190` (from `0x0057B780`) for 10, 20, 14 and 16, each only when `0x002F8040(group)` finds
`0x02EC3D80[group]` empty. At start-up `0x0022A4B0` runs `0x00563520`, which takes a request group with the
completion function `0x00563550` (`0x002486B0`), asks for groups 10, 20 and 14 and closes it (`0x00249410`).

## Modding notes

- Keep a word row's two leading zero bytes; without them `0x002B58B0` returns the row itself whatever
  string number is asked for.
- A word bank holds at most 2,048 rows and there are at most 32 banks.
- The `group × 1000` form reaches rows 0–999 only; rows past that need their `group × 10000` id
  (`us` `menu04` has 1,024 rows). An id past the table shows as empty text.
- Strings must be written in the font's glyph codes for the language, not ASCII.

## Related

- [Authored data tables](authored-data-tables.md): the registry slot, the table header and the binders.
- [Fonts](../Menus-And-HUD/fonts.md): how a glyph code becomes a glyph.
- [Text codes](../Menus-And-HUD/text-codes.md): the control and escape codes inside strings.
