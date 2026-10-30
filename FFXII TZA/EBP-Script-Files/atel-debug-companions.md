---
title: "ATEL debug companions: the source, message and symbol files shipped beside the four control scripts, and why the game never opens them"
kind: "system"
category: "EBP script files"
addresses: "0x003306E0, 0x0032E400, 0x0032FCA0, 0x00D10990, 0x0032F6F0"
---

## What the player sees

Nothing. The files are development material for the four control scripts (`ctrl`, `btlctrl`,
`evctrl`, `mapctrl`), whose source holds debug menus and debug flags. The game ships them and never
reads them, so editing or deleting them changes nothing in play.

## How it works

### No name reaches them

The executable holds none of the module names (`\ctrl.`, `/ctrl.`, `btlctrl`, `evctrl`, `mapctrl`,
`systemctrl`) and none of `.sbn`, `.msb` or `.dbg` as a terminated string, in ASCII or UTF-16. The
bare strings `sbn` and `msb` occur once each and `dbg` twice, and the `sbn`/`msb`/`dbg` entries at
`0x00D10994` to `0x00D1099C` are extension strings in the list `bin dbg sbn msb msf fnt cam camera lgt cml
cmi shk skl vld` at `0x00D10990`.

### The sibling loader stops at its first query

`0x003306E0`, called from `0x0032FCA0` (`0x00330029`), builds sibling names for a script by putting those
extensions on its path (the first six at `0x0033078D` to `0x00330A59`).

Three names go into a subfolder through `0x0032F6F0(path, folder, extension)` (`0x00330AB9`,
`0x00330AE9`, `0x00330C39`), each with the folder `camera` (`0x00D109AC`) and the extension `cam`, `lgt` or
`shk`. `0x0032F6F0` inserts the folder and a backslash before the file name, which starts after the
last `\` or `/`. It then copies the extension over the characters after the last `.`, stopping at
the end of either, or cuts the name at that `.` when the extension is null, and copies the result
back over `path`.

`0x003306E0` then sizes the names with `0x0032E400`, 14 calls that all pass kind `0xFF` (`0x00330E47` to
`0x00330F71`).

- `0x0032E400` compares the kind with `0xFF` before any lookup (`0x0032E404`) and returns -1
  (`0x0032E438`).
- The first result is kept in `r15d` (`0x00330E58`); `0x00330F7D` jumps to the epilogue `0x003315E7` when
  it is not positive, and no branch before that point lands beyond it.

So `0x003306E0` returns without registering any file, and no string in the executable names these files.

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
| `+0x08` | `...` | page[ceil(lineCount / 32)] |  |

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
| `+0x00` | `{u32 section; u32 table}[5]` | three used; slot 1's section is the name pool |  |
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
| `.dbg` command tables | class 0: 1,410 / 1,389 / 1,436 / 1,407; class 2: 207 / 203 / 211 / 207; class 3: 131 in all; class 7: 103 (none in `btlctrl`) |
| command names | 7,297 of 7,303 match the shipped verb table; `0x20C8` and `0x20C9` are `debug_set_jfdemo_status` and `debug_get_jfdemo_status` in `ctrl`, `btlctrl` and `mapctrl` |
| every message | one row each in [`atel-debug-companions-msb-rows.tsv`](atel-debug-companions-msb-rows.tsv), 194 rows: file, index, flag, offset, size and the bytes in hex |
| every name | one row each in [`atel-debug-companions-dbg-rows.tsv`](atel-debug-companions-dbg-rows.tsv), 19,364 rows: file, table (source file, declared or global variable, command class), index, the global's descriptor or the command id, and the name |
| every source line | one row each in [`atel-debug-companions-sbn-rows.tsv`](atel-debug-companions-sbn-rows.tsv), 10,139 rows: file, block, line and its text (tabs written `\t`) |

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
