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

A battle name's number splits into a bank and a row of that block. A menu or help line's number is its file's group
times 1,000 plus its row, and a line whose file is not loaded yet shows as empty text. Each string is a run of glyph
numbers that the language's font turns into letters.

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

`0x003214B0` also returns 0 while the word block slot `0x02EBF170` is null (`0x003214C8`-`0x003214CB`). The bank count is
the `u16` at the block's `+0`, the bank's row count the `u16` at the bank's `+0`, both compared signed after
subtracting 1 (`0x003214CD`-`0x003214ED`).

A row starts with two zero bytes. `0x002B58B0(row, k)` skips them and then `k` strings and returns the
string it reaches; a row without the two zero bytes is returned as it is. Of its 59 callers, 14
are interface code reading a row's strings: the gambit screen (`0x00567B60`, `0x0056A890`,
`0x0056BC70`), the licence screens (`0x00558CE0`, `0x005618E0`), the battle menu's title `0x0027D480`
and the party list `0x002986E0` among them ([gambit screen](../Menus-And-HUD/gambit-screen.md),
[battle menu](../Menus-And-HUD/battle-menu.md), [party list](../Menus-And-HUD/party-list.md)).

`0x002B58B0` returns 0 for a null row (`0x002B58B0`-`0x002B58B7`); the unit name lookup `0x0023A570` gives it a null row
while the word block slot `0x02EBF170` is null (`0x0023A860`-`0x0023A868`, `0x0023A8DA`-`0x0023A8E1`). A `k` of 0 or below
returns the first string, the row's address plus 2 (`0x002B58C3`-`0x002B58C9`).

### Text groups

`0x002F9860(id)` splits the id into group `id / 1000` and row `id % 1000`. It returns the string when the
group is below 28, its file is resident (`0x02EC3D80[group]`), and the row is below the table's
`+0x04`; otherwise, or when the table or its `+0x14` sub-directory is null, it returns the empty string at
`0x01CEB638`. The string is entry `row` of the text block that the table's `+0x14` sub-directory names.

`0x002F9920(id)` is the second form: group `id / 10000`, then a linear search of the table's rows for a
row equal to `id`, returning the text-block string at that row's position, or `0x01CEB638`. A row's
id need not be `group × 10000 + row`: `us` `menu_command` row 5 is `10100`, so that string is both
`1005` and `10100`. In all nine languages 144 files number their rows from `group × 10000` in order
and 90 do not.

Both resolvers divide a signed id, so a negative group passes their `group < 28` test (`0x002F9879`, `0x002F9939`):
an id of −1000
or less for `0x002F9860` (`id / 1000`), and of −10000 or less for `0x002F9920` (`id / 10000`). `0x002F9860` takes the
row as `id − group × 1000` (`0x002F98A8`-`0x002F98BD`), which is negative for every negative id that is not a multiple
of 1000; when the group's slot and table are present, its unsigned compare with the table's `+0x04` refuses that
row and the call returns `0x01CEB638` (`0x002F98C7`-`0x002F98CA`, `0x002F9902`).

A group is loaded on demand:

1. `0x002FA560(group)` passes the group's setter (`0x002F7660` and its neighbours, `0x20` bytes apart) to
   `0x002385D0`, which requests kind-2 file `0x01E09F68[group]` (`0x00384420`); group 0 has no file.
2. On delivery the setter stores the file at `0x02EC3D80[group]` and jumps to `0x00238640`, which binds
   it into `0x02F973C0[group]` with `0x003845F0`.
3. `0x002F83E0(group)` frees the file and clears `0x02EC3D80[group]`.

`0x002FA560` is called from the menu widget handler `0x00248700`, for the group the widget names when
it is not yet resident, and from `0x0053EB90` for groups 25 and 26, each when not yet resident
(`0x0053EC64`-`0x0053EC8B`). For a group outside 0 to 27 `0x002FA560` returns at `0x002FA73B` with no request.

`0x002385D0` returns 0 with no request when the group is above 27 as an unsigned number (`0x002385D9`-`0x002385DC`) or
its byte has bit `0x80` set, as group 0's `0xFF` does (`0x002385EC`-`0x002385EE`). Otherwise it returns what
`0x00384420` returns, called with the id, the setter, the name `MMSG` (`0x00914698`), 3 (the return of `0x008478A0`), 8
and 4 (`0x002385F5`-`0x0023861E`).

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
it on the request group, adding 1 to its `u16` at `+0x18` (`0x002491F5`). It does not test the request group, so a
null one faults there.

The handler's message 1 stores the request group and the group at its `+0xC0` and `+0xC8`, requests the group
through `0x002FA560` when `0x002F8040` finds it empty and then sets the dword `+0xCC` to 1, and calls
`0x00247950(handler, 0)` (`0x0024875B`-`0x00248792`). The widget starts zero-filled (`0x00246626`), so `+0xCC` stays 0 for
a group that is already resident.

On message 2 with `+0xCC` set, the handler returns until `0x002F8040` answers 1. Then it calls
`0x002494F0(request group, 1)`, which adds 1 to the `u16` at `+0x1A` (`0x0024950C`). Once the group is closed
(bit `0x2` of `+0`) and the two counts are equal, `0x002494F0` runs the group's completion: the function at `+0x10`
when the dword `+4` is set, otherwise message 16 to the widget at `+8` (`0x00249510`-`0x00249564`).

The handler then releases itself (`0x00245020`, `0x00248722`-`0x0024874E`). With `+0xCC` at 0 it releases itself on
message 2 without the `0x002494F0` call. Other messages go to `0x005C5230` (`0x0024871D`).

A request group is one of twelve `0x20`-byte records at `0x02090790`. `0x00249580(widget)` takes one whose completion
is message 16 to that widget at `+8` (`0x002495A3`-`0x002495B7`); `0x002486B0(function)` takes one whose completion is
that function at `+0x10`, with the dword `+4` set to 1 (`0x002486D3`-`0x002486EE`). In each of the ten functions
listed below, the record goes only to `0x002491B0`, to the file loaders (`0x00249210`, directly or through
`0x00249180`, `0x00249320`, `0x002493D0` or `0x0057A2D0`) and to `0x00249410`, which closes it.

At start-up `0x0022A4B0` runs `0x00563520`, which takes a request group with the
completion function `0x00563550` (`0x002486B0`), asks for groups 10, 20 and 14 and closes it (`0x00249410`), and then
`0x00556500`, which does the same with `0x00556560` for group 17 and one file (`0x0055650D`-`0x00556555`).
`0x002486B0` returns 0 when its twelve records at `0x02090790` are all taken (`0x002486C0`-`0x002486D2`), and `0x00563520`
passes its result to `0x00292260` without a test (`0x0056352D`-`0x00563538`), as `0x00556500` does to `0x002922C0`
(`0x0055650D`-`0x00556518`).

`0x00563550` sets the dword `0x02CA96D4` to 1 and `0x00556560` sets `0x02CA8F94` to 1. `0x00565E00` reads `0x02CA96D4`
once and then tests the register in a loop (`0x0056615D`-`0x00566165`), and `0x00560910` does the same with
`0x02CA8F94` (`0x00560A55`-`0x00560A62`): a 0 read there never ends the loop. Neither completion function clears bit
`0x1` of its record, and the function branches of `0x00249410` and `0x002494F0` do not either (`0x00249440`-`0x00249455`,
`0x00249525`-`0x0024953A`), so both records stay taken; the widget branch clears it (`0x0024947F`, `0x00249564`).

When a group is resident at `0x002491B0`, the handler leaves `+0xCC` at 0 and never calls `0x002494F0`, so `+0x1A`
stays below `+0x18`; the completion then never runs, since only `0x00249410`, `0x002494F0` and `0x002495C0` run it,
each when the counts are equal. Only `0x0024950C` in `0x002494F0` and `0x002495ED` in `0x002495C0` add to `+0x1A`, and a
decode of all 38,161 listed functions finds no other word increment at `+0x1A`.

`0x002495C0` is the file-load callback that `0x00249210` registers (`0x00249274`) for the file it counts at
`0x002492F8`. `0x002494F0` is called only at `0x00248746` and at `0x00558BFF` in `0x00558BB0`, a widget that adds its own
1 to `+0x18` on message 1 (`0x00558C26`). Message 18 is what `0x00245020` sends to a widget it releases and to each
widget below it (`0x00245050`-`0x0024505A`, `0x002473C2`-`0x002473D3`).

The slots `0x02EC3D80[group]` are written only by the 28 setters and by `0x002F83E0` (`0x002F8402`); no other
instruction reaches them, rip-relative or from the image base, besides the reads in `0x002F8040` and the two
resolvers. The setters are reached only through `0x002FA560`, whose callers are `0x00248700` and `0x0053EB90`. The
frees, through `0x002F83E0`, are listed after the callers.

Groups 1, 2, 3, 4, 5, 9, 12, 13, 18 and 19 are handed only by `0x00253780` and freed by no function. The HUD
root's one creation site is `0x002539EC` in `0x00253970`, after `0x002494A0` clears the records (`0x002539A6`);
`0x00253970` is called only from `0x0022A0B0` (`0x0022A415`), and `0x0022A0B0` only from `0x0017D4C0` (`0x0017D5CC`). A
second run would find these groups resident.

Group 6 is also handed by `0x003BC2D0`, after a test, and that widget frees it on message 18 when it set bit `0x1`
(`0x003BC522`-`0x003BC530`). The widget's procedure `0x003BC4E0` is named only at `0x003BC482` in `0x003BC450`, which is
called from `0x002BA040` (`0x002BA15C`), `0x003CB440` (`0x003CB4CC`) and `0x003BC440` (`0x003BC44A`).

Group 21 is handed only by `0x0037F4D0` and freed only in `0x0037F860`, and the widget is single (`0x02AED490`,
`0x0037F3C3`, `0x0037F456`, `0x0037F614`, `0x0037F51E`). It can be resident at a later widget's message 1: a release
that reaches the widget as message 18 before `0x0037F860` has run goes to `0x0037FA00`, which frees no group
(`0x0037F50B`-`0x0037F517`).

`0x0037E4F0` can also run `0x0037F860` while the group is still loading, since message 1 clears bit `0x80` of
`+0xE0` (`0x0037F62B`, `0x0037E514`-`0x0037E531`). `0x002F83E0` then finds the slot 0 and frees nothing
(`0x002F83F8`-`0x002F83FB`) and `0x0037F8A1` clears bit `0x40`. `0x002491B0` keeps no pointer to the widget that made
the request (`0x002491F0`-`0x002491F5`), and that widget's setter stores the slot on delivery (`0x002F79C8`).

Then the later widget's completion never runs: it does not reach its message 16 branch, `0x0037F1F0` does not
notify the widget at its `+0xC0`, and `0x02AED490` stays set, so `0x0037F3B0` and `0x0037F440` create no other one
(`0x0037F3C3`-`0x0037F3CB`, `0x0037F456`-`0x0037F45E`) until `0x0037E4F0` closes it, which it does when `0x0037F860`
returns 1 (`0x0037E531`-`0x0037E54F`).

The `0x002491B0` calls sit in ten functions, at 28 sites:

- `0x00253780`, the field HUD root's message 1: its own widget's record (`0x0025383C`); groups 1, 18, 2, 6, 19, 5, 3,
  4, 12, 9 and 13 with no residency test (`0x0025384C`-`0x002538CE`); closed at `0x0025393F`. Its message 16 runs
  `0x00280980`, `0x002C8EE0`, `0x0017F770`, `0x0029CF10` and `0x0035C630` and creates the `0x290`-byte widget with
  procedure `0x00252030` (`0x002537BF`-`0x00253815`).
- `0x0037F4D0`, message 1: its own widget's record (`0x0037F608`); group 21 with no residency test when bit `0x8` of
  `+0xE0` is set, from the third byte of its creation argument (`0x0037F69F`-`0x0037F6AD`, `0x0037F70D`-`0x0037F71E`);
  it then sets bit `0x40` (`0x0037F723`) and closes at `0x0037F782`.
- `0x0037F4D0`, message 16: runs `0x0037F1F0`, which in state 0 sends message 16 to the widget at its `+0xC0`
  (`0x0037F205`-`0x0037F248`), and sets its state `+0xE5` to 1 (`0x0037F52A`-`0x0037F546`).
- `0x00576F50`, from message 1 of `0x005771F0` (`0x005772B4`): it tests groups 7 and 8 with `0x002F8040` first and keeps
  each empty answer as bit `0x10` or `0x20` of `+0x100` (`0x00576F59`-`0x00576F7C`); it takes its widget's record
  and hands a group only when its bit is set (`0x00576F9C`-`0x00576FCB`); closed at `0x00577085`.
- `0x005771F0`, message 16: runs `0x00577180` unless bit `0x1` is set (`0x005772D1`-`0x005772EF`). When bits `0x4`,
  `0x10` and `0x20` are all clear, `0x00576F50` returns 0 with no record and `0x005771F0` calls `0x00577180` at once
  (`0x00576F83`-`0x00576F93`, `0x005772B9`-`0x005772C4`).
- `0x003BC2D0`, from message 1 of `0x003BC4E0` (`0x003BC936`): its widget's record (`0x003BC2EC`); groups 6 and 23, each
  after a test, setting bit `0x1` or `0x2` of `+0xD0` (`0x003BC37A`-`0x003BC3B3`); closed at `0x003BC3D1`. Message 16
  in state 0 sets state 1 and sends message 16 with `0x100` to its `+0xC0` (`0x003BC6CB`-`0x003BC71E`).
- `0x00572D80`, from the first message 16 of `0x00572E10` (`0x00572F23`-`0x00572F68`): its widget's record; group 24
  after a test, setting bit `0x2` of `+0x11D0` (`0x00572DB1`-`0x00572DCA`); closed at `0x00572E08`. The next message
  16 runs `0x00572F74`-`0x00572FDE`, which ends with `0x00246AD0(+0xC0, widget)`.
- `0x0057B780`, from message 1 of `0x0057B890` (`0x0057B944`): its widget's record, passed to `0x00292190`
  (`0x0057B7C9`), which asks for groups 10, 20, 14 and 16, each after a test; group 22 after a test, setting bit
  `0x1` of `+0x150` (`0x0057B7CE`-`0x0057B7E7`); closed at `0x0057B7FB`. Message 16 is `0x0057B977`.
- `0x00292210`, from message 1 of `0x005691E0`: that widget's record (`0x00569532`); groups 10 and 16, each after a
  test; closed at `0x00569545`. Message 16 is `0x0056955F`.
- `0x00292260`, from `0x00563520`, and `0x002922C0`, from `0x00556500`: groups 10, 20 and 14, and group 17, each after
  a test.

`0x002F83E0` has 14 call sites in seven functions:

- `0x002922F0`: group 17 while `0x02CA8F94` is 0, groups 10, 20 and 14 while `0x02CA96D4` is 0, and group 16, each
  when resident (`0x002922F4`-`0x0029237D`); called by `0x00560910`, `0x00565E00`, and on message 18 by `0x005691E0`
  (`0x00569236`) and `0x0057B890` (`0x0057BC88`).
- `0x0037F860`: group 21 when bit `0x40` of `+0xE0` is set, then it clears the bit (`0x0037F88D`-`0x0037F8A1`); run
  on message 16 in state 3 (`0x0037F58F`) and by `0x0037E4F0` (`0x0037E531`).
- `0x003BC4E0` on message 18: group 6 when bit `0x1` of `+0xD0` is set and group 23 when bit `0x2` is
  (`0x003BC522`-`0x003BC543`).
- `0x0053EEA0`: groups 25 and 26 when resident (`0x0053EF39`-`0x0053EF64`).
- `0x00572E10` on message 18: group 24 when bit `0x2` of `+0x11D0` is set (`0x00573294`, `0x005732CC`-`0x005732D8`).
- `0x005777C0`, from message 2 of `0x005771F0` (`0x0057735E`): group 7 when bit `0x10` of `+0x100` is set and group 8
  when bit `0x20` is (`0x005777C6`-`0x005777F9`).
- `0x0057B890` on message 18: group 22 when bit `0x1` of `+0x150` is set (`0x0057BC8D`-`0x0057BC9B`).

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- RNG random selection: `0x0022A0B0` calls `0x00379CF0`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Save load settings: `0x0017D4C0` calls `0x001C1710`, `0x001C18A0`, `0x001C18E0`; `0x00245020` is called by `0x0057E4D0`;
  `0x00253970` calls `0x002EF640`.
- Save load settings: those functions are documented on
  [game application](../Engine-Core/game-application.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
