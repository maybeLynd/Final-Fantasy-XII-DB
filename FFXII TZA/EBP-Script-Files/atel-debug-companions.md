[Home](../../README.md) / [EBP script files](README.md) / ATEL debug companions

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| ATEL debug companions: the source, message and symbol files shipped beside the four control scripts, and why the game never opens them | system | EBP script files | Debug files | The .sbn, .msb and .dbg files of the control scripts ctrl, btlctrl, evctrl and mapctrl in `ps2data/image/ff12/<in\|ch>/bin`: the script source text with a paged line map, the debug menu messages, and a symbol database of source files, variables, global variables and native command names. No path in the executable names them, and the sibling loader that knows their extensions asks every size with kind 0xFF, which 0x0032E400 answers with -1, then returns before registering anything. | 0x003306E0, 0x0032E400, 0x0032FCA0, 0x00D10990, 0x0032F6F0 |

## What the player sees

Nothing. The files are development material for the four control scripts (`ctrl`, `btlctrl`,
`evctrl`, `mapctrl`), whose source holds debug menus and debug flags. The game ships them and never
reads them, so editing or deleting them changes nothing in play.

## How it works

### No name reaches them

The executable holds none of the module names (`\ctrl.`, `/ctrl.`, `btlctrl`, `evctrl`, `mapctrl`,
`systemctrl`) and none of `.sbn`, `.msb` or `.dbg` as a terminated string, in ASCII or UTF-16. The
strings `sbn` and `msb` occur once each, and the `sbn`/`msb`/`dbg` entries at `0x00D10994` to `0x00D1099C` are
extension strings in the list `bin dbg sbn msb msf fnt cam camera lgt cml cmi shk skl vld` at `0x00D10990`. `dbg`
occurs twice more, as the end of the section group name `.rdata$zzzdbg` (`0x01D5280A`) and in `dbghelp.dll`
(`0x01DEEA14`).

### The sibling loader stops at its first query

`0x003306E0`, called from `0x0032FCA0` (`0x00330029`), builds sibling names for a script by putting those
extensions on its path (the first six at `0x0033078D` to `0x00330A59`).

Three names go into a subfolder through `0x0032F6F0(path, folder, extension)` (`0x00330AB9`,
`0x00330AE9`, `0x00330C39`), each with the folder `camera` (`0x00D109AC`) and the extension `cam`, `lgt` or
`shk`. `0x0032F6F0` inserts the folder and a backslash before the file name, which starts after the
last `\` or `/`. It then copies the extension over the characters after the last `.`, stopping at
the end of either, or cuts the name at that `.` when the extension is null, and copies the result
back over `path`.

`0x0032F6F0` builds the result in a 272-byte (`0x110`) stack buffer and tests no length (`0x0032F6F6`,
`0x0032F720`-`0x0032F79E`). The search for the `.` runs backward from the last character over the whole built
path, folder and directories included, and stops before the first character (`0x0032F7C3`-`0x0032F7D3`); when it
finds no `.`, the name keeps its extension. A `.` that ends the name leaves it unchanged when an extension is
given (`0x0032F7E0`).

`0x003306E0` then sizes the names with `0x0032E400` from 14 call sites, all passing kind `0xFF` (`0x00330E47` to
`0x00330F71`): the one at `0x00330F48` runs once for each of 16 names (`0x00330F2D`-`0x00330F5E`), and the one at
`0x00330F71` only when the first argument, kept in `r14d` (`0x00330713`), is not 0 (`0x00330F60`).

- `0x0032E400` compares the kind with `0xFF` before any lookup (`0x0032E404`) and returns -1
  (`0x0032E438`).
- The first result is kept in `r15d` (`0x00330E58`); `0x00330F7D` jumps to the epilogue `0x003315E7` when
  it is not positive, and no branch before that point lands beyond it.

So `0x003306E0` returns without registering any file, and no string in the executable names these files.

`0x003306E0(slot, tag value, a, b)` first keeps the answer of `0x00263FF0(slot)` and builds the base path
with `0x0032E3F0(a, b, buffer, 0x103)` (`0x0033072C`-`0x00330744`). The base path takes `bin`; nine copies
take `dbg`, `sbn`, `msb`, `msf`, `fnt`, `cml`, `cmi`, `skl` and `vld`, and three go through `0x0032F6F0`
(`0x0033078D`-`0x00330D51`). Sixteen more copies, `0x104` bytes apart, take the extension that
`0x0017D2E0(out, "m%02d", i)` writes for i = 0 to 15 and then `.mld` at their end
(`0x00330D53`-`0x00330E38`).

Of the sizes `0x0032E400(0xFF, name)` answers, those of `dbg`, `sbn` and `vld` are not kept. The others
are kept: `bin` (the one tested at `0x00330F7A`), `msb`, `msf`, `fnt`, `cam`, `cml`, `shk`, `skl`, `cmi`,
the sixteen `.mld` sizes and, for a slot other than 0, `lgt` (`0x00330E3E`-`0x00330F76`).

The instructions after the exit at `0x00330F7D` load each kept file the same way: `0x0036C750` of the
string `..\..\katano\atelload.c`, which answers the part after the last `\`; `0x0036A100(size)`;
`0x0036C660(the 0x0036A100 answer, the 0x0036C750 answer, line)` for a buffer; then
`0x0032E7B0(name, buffer, size, record)`, and a bit set in the qword `0x022C6E48 + 8 × slot`.

The record holds a dword 0 at `+0x00`, the dword `slot | low dword of the buffer address` at `+0x08`, a
callback at `+0x10` and a null qword at `+0x18` (`0x00330F83`-`0x003315DB`). Every block but the `bin` one
writes 0 over the whole qwords `+0x00` and `+0x08` before those two dwords, and 0 in the qword `+0x20`
(`0x0033104E`-`0x00331062`, `0x00331246`-`0x0033125C` and the like).

The record lies over the first eight `.mld` sizes, and the `bin` block writes only those four fields,
so its dwords `+0x04` and `+0x0C` and its qword `+0x20` still hold `.mld` sizes when the record is handed
to `0x0032E7B0` (`0x00330FB4`-`0x00330FE5`). The body itself reads none of the sixteen `.mld` sizes.

| File | Loaded when its size is | Line | Callback | Bit |
|---|---|---|---|---|
| `bin` | above 0 (the test at `0x00330F7A`) | `0x734` | `0x0032F850` | `0x2` |
| `msb` | above 0 | `0x7D8` | `0x00330190` | `0x10` |
| `msf` | above 0 | `0x7F2` | `0x00330220` | `0x20` |
| `fnt` | above 0 | `0x80D` | `0x00330060` | `0x40` |

| File | Loaded when its size is | Line | Tag | Callback | Bit |
|---|---|---|---|---|---|
| `cam` | 0 or above | `0x82A` | `CAMDAT` | `0x0032FAC0` | `0x80` |
| `cml` | 0 or above | `0x84B` | `CAMCTL` | `0x0032FA10` | `0x100` |
| `shk` | 0 or above | `0x863` | `SHKDAT` | `0x003316B0` | `0x400` |
| `skl` | 0 or above | `0x884` | `SHKCTL` | `0x00331610` | `0x800` |
| `cmi` | 0 or above | `0x89E` | `CHRMDL` | `0x0032FB70` | `0x200` |
| `lgt` | 0 or above, slot other than 0 | `0x8B8` | `LGTDAT` | `0x00330110` | `0x10000` |

A file with a tag is loaded only when its buffer is not null, and the buffer first goes to
`0x0036C660(buffer, tag, tag value)` (`0x00331220`-`0x0033123A`, `0x003312E4`-`0x003312F9`). With a null `cam`
buffer the body calls `0x002566E0(slot, i)` for i = 0 to 3 and `0x002561C0(0, slot)`; with a null `shk`
buffer, `0x0037DC30(slot, i)` for i = 0 to 3 and `0x0037DA90(0, slot)` (`0x0033128E`-`0x003312A7`,
`0x003313E7`-`0x00331406`).

The buffers of the four files without a tag are used with no null test. The
`bin` buffer gets 0 in its first byte, and bit `0x8` of byte `+0x11` of the `0x00263FF0` answer is set
(`0x00330FD3`-`0x00330FE5`).

After `bin` the body calls `0x0036C1D0(n, 5)`: n is 5 for a slot of 0 or less or above 3; for slots 1
and 2 it is `0xD`, and for slot 3 `0xE`, when `0x0036B200` of that number answers non-zero, and 5 when
it answers 0 (`0x00330FFA`-`0x00331034`). When the `fnt` size is above 0, and so inside that block, it
calls `0x00332250(a, b, record dword +0x08, 0)` after the load (`0x003311D1`-`0x003311E5`). The last call is
`0x0036C140()` (`0x003315E2`).

## Layouts

### .sbn, the source text

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | blockCount | 2 (ctrl, evctrl) or 3 (btlctrl, mapctrl) |
| `+0x04` | `u32` | blockOffset[blockCount] | the first is 4 × (blockCount + 1) |

Block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | lineCount |  |
| `+0x04` | `u32` | textOffset | file offset of the block's first line |
| `+0x08` | `...` |  | page[ceil(lineCount / 32)] |

```
page   u16 lineStart[32], then u32 nextPageBase (absent after the last page)
```

Line `j` of page `p` starts at the page's base plus `lineStart[j]`; the first page's base is
`textOffset` and each later base is the `nextPageBase` before it. Lines are NUL-terminated text.

### .msb, the messages

```python
+0x00  u32  entry[n]    (flag << 16) | offset; n = low half of entry 0 / 4
```

Offsets ascend; each message is a byte stream ending in `00` that opens with `0F 24 81 81`.

### .dbg, the symbol database

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `{u32 section; u32 table}[5]` |  | three used; slot 1's section is the name pool |
| `+0x2C` | `u32` | commandTable[16] | one per native command class |
| `+0x6C` | `u32` | n, u32 nameOffset[n] | source files, one per .sbn block |

All name offsets are relative to the pool. Slot 0's table is the module's declared variables
(`{u32 count; u32 nameOffset[count]}`); slot 2's table is its global variables
(`{u32 count; {u32 descriptor; u32 nameOffset}[count]}`, starting with `0x30000000` =
`global_flag[0]`). Command table `k` is `{u32 count; u32 nameOffset[count]}`, and entry `i` names
native command `(k << 12) + i`.

## Shipped data

| Fact | Value |
|---|---|
| files | 8 each of `.sbn`, `.msb`, `.dbg`; the `ch` copy of every file is byte-identical to the `in` copy |
| sizes `.sbn` / `.msb` / `.dbg` | `ctrl` 24,976 / 3,029 / 83,120; `btlctrl` 98,136 / 7,141 / 270,160; `evctrl` 57,816 / 26,953 / 126,112; `mapctrl` 140,128 / 10,864 / 301,776 |
| `.sbn` blocks and lines | `ctrl` 977 + 79; `btlctrl` 2,507 + 79 + 558; `evctrl` 2,456 + 79; `mapctrl` 2,768 + 79 + 557 |
| `.sbn` line starts | every one lands on the text start or just after a NUL, 10,139 of 10,139 |
| `.sbn` block 1 | `systemctrl.ath` (79 lines, opening `#ifndef __SYTEM_CTRL_ATH__`) in all four |
| `.msb` messages | `ctrl` 42, `btlctrl` 48, `evctrl` 47, `mapctrl` 57; flag 1 on 35, 22, 36 and 29 of them |
| `.dbg` source files | the module's own `.src`, the `systemctrl.ath` path, and `mapctrl_mj.src` in `btlctrl` and `mapctrl` |
| `.dbg` declared variables | 56, 92, 115, 127 |
| `.dbg` global variables | 815, 4,950, 943, 4,953 |
| `.dbg` command tables | class 0: 1,410 / 1,389 / 1,436 / 1,407; class 2: 207 / 203 / 211 / 207; class 3: 131 in all; class 7: 103 (0 in `btlctrl`) |
| command names | 7,297 of 7,303 match the shipped verb table; `0x20C8` and `0x20C9` are `debug_set_jfdemo_status` and `debug_get_jfdemo_status` in `ctrl`, `btlctrl` and `mapctrl` |
| every message | one row each in [`atel-debug-companions-msb-rows.tsv`](atel-debug-companions-msb-rows.tsv), 194 rows: file, index, flag, offset, size and the bytes in hex |
| every name | one row each in [`atel-debug-companions-dbg-rows.tsv`](atel-debug-companions-dbg-rows.tsv), 19,364 rows: file, table (source file, declared or global variable, command class), index, the global's descriptor or the command id, and the name |
| every source line | one row each in [`atel-debug-companions-sbn-rows.tsv`](atel-debug-companions-sbn-rows.tsv), 10,139 rows: file, block, line and its text (tabs written `\t`) |

### Columns of atel-debug-companions-dbg-rows.tsv

| Column | Holds |
|---|---|
| `descriptor_or_command` | on a `global_variable` row (11,661 rows), the variable's 32-bit descriptor from slot 2's table, as 8 hexadecimal digits, for example `0x30000000` for `global_flag[0]`; on a `command_class_` row (7,303 rows), the native command id the entry names, `(k << 12) + i` for entry `i` of command table `k`, as 4 hexadecimal digits (`0x2000` is entry 0 of class 2); empty on the 390 `declared_variable` and 10 `source_file` rows |

## Modding notes

- The game reads none of these files; changing a control script means editing its `.ebp`, not its
  companions.
- The `.dbg` command tables give each native command id a name in the scripts' own source spelling,
  which is a check on a verb list.

## Related

- [EBP script container](ebp-script-container.md): the script format the game does load.
- [Script verb table](../Scripts-And-Script-Commands/verb-table.md): the command ids the `.dbg` tables name.
- [Native commands](../Scripts-And-Script-Commands/native-commands.md): the command classes.
- [Script variables](../Scripts-And-Script-Commands/script-variables.md): the variables the `.dbg` tables list.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input: `0x00263FF0` is called by `0x00226BE0`, `0x002E09A0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00263FF0` is called by `0x002E28E0`, `0x00392740`; those functions are documented on
  [native limits](../Engine-Core/native-limits.md),
  [frame update order](../Engine-Core/frame-update-order.md).
