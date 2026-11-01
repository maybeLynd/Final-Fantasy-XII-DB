---
title: "Control script messages: the debug menu text of the .msb files beside the four control scripts"
kind: "reference"
category: "Menus and HUD"
addresses: "0x003306E0, 0x0032E400, 0x002AC5F0"
---

## What it lists

[text-control-messages.tsv](text-control-messages.tsv) has one row per message of the files `ctrl.msb`,
`btlctrl.msb`, `evctrl.msb` and `mapctrl.msb` in `ps2data/image/ff12/<in|ch>/bin`: 194 rows. They are the debug menus
and notices of the four control scripts, mostly Japanese, written in the game's text codes.

The game never opens them: the sibling loader `0x003306E0` asks `0x0032E400` for each companion file's size with resource kind `0xFF`, which
answers -1, and gives up at the first answer ([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md),
which also gives the file layout).

Only the `in` and `ch` trees ship the files, and the `ch` copy of each is byte for byte the `in` copy. The table keeps
both columns: the `in` column is the text through the Japanese font, the one it is written for, and the `ch` column
shows the same bytes through the Chinese font.

### Reading the text

Each message is decoded with the tree's font and its text codes written as placeholders (the `placeholder`
column of [Text codes](text-codes.md)). Every message opens with `{spacing:8181}`. A choice list is written
`{choice:n}` followed by its `n` options in square brackets, separated by a bar; `hidden=` gives the mask of options
the list hides. The start of `ctrl.msb` message 0, the top debug menu, in the `in` column:

```
{spacing:8181}{speed:8180}{size%:81CB}{choice:23}[やめ|イベントきかくメニュー|マップきかくメニュー|バトルきかくメニュー|マップジャンプ|...
```

The menu's 23 options start with `やめ` (quit) and the event, map and battle planning menus. `btlctrl.msb` message 2,
`{spacing:8181}{speed:8180}{size%:81D1}{color:BB8080FF}{icon:P:82}：ページ{line}きりかえ`, tells the player to switch
pages with the button icon `P`.

## Columns

| Column | Meaning |
|---|---|
| `file` | the `.msb` file |
| `index` | the message's entry in the file's offset table, from 0 |
| `in` | the message decoded with the Japanese font |
| `ch` | the same bytes decoded with the Chinese font |
| `missing` | empty in every row: both trees ship all four files |
| `same_bytes` | `in=ch` in every row |

## Data

| File | Messages |
|---|---:|
| `btlctrl.msb` | 48 |
| `ctrl.msb` | 42 |
| `evctrl.msb` | 47 |
| `mapctrl.msb` | 57 |
| all | 194 |

The 194 messages hold 112 choice lists, 71 argument inserts (`{arg:..}`) and 484 size codes (`{size24:..}`).

## Related

- [ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md) - the `.msb` layout, its source
  and symbol siblings, and why the game never opens them.
- [Text codes](text-codes.md) - the text codes and their placeholders.
- [Message windows](message-windows.md) - how the game's own script messages and choice lists are shown.
