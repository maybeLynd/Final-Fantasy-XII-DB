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
answers -1, and returns before registering anything because the first answer is not positive
([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md),
which also gives the file layout).

Only the `in` and `ch` trees ship the files, and the `ch` copy of each is byte for byte the `in` copy. The table keeps
both columns: the `in` column is the text through the Japanese font, the one it is written for, and the `ch` column
shows the same bytes through the Chinese font.

### Reading the text

Each message is decoded with the tree's font and its text codes written as placeholders (the `placeholder`
column of [Text codes](text-codes.md)). Every message opens with `{spacing:8181}`. A choice list is written
`{choice:n}` followed by its `n` options in square brackets, separated by a bar; `hidden=` gives the mask of options
the list hides. `ctrl.msb` message 33, in the `in` column, asks to save or load and offers quit, load and save:

```
{spacing:8181}{speed:8180}セーブもしくはロード{line}{choice:3}[やめ|ロード|セーブ]
```

Message 0, the top debug menu, is a list of 23 options that starts with `やめ` (quit) and the event, map and battle
planning menus. `btlctrl.msb` message 2,
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032E400` is called by `0x0032FCA0`, `0x00330310`, `0x003306E0`; `0x003306E0` calls `0x002566E0`, `0x00263FF0`,
  `0x0037DC30`; `0x003306E0` is called by `0x0032FCA0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Actor entity: and on [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md).
- Core runtime: `0x002AC5F0` calls `0x00229E40`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Presentation: `0x002AC5F0` calls `0x003A1DB0`; `0x002AC5F0` is called by `0x002AAE40`; `0x0032E400` is called by `0x003B2310`,
  `0x003B53C0`; `0x003306E0` calls `0x002561C0`; those functions are documented on
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [message windows](message-windows.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).
- Presentation: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md).
- Resource: `0x0032E400` is called by `0x00249210`, `0x0024AC30`, `0x00259DF0`, `0x00379E90`, `0x00384420`, `0x0039C3F0`,
  `0x003EADE0`, `0x0051ED10`; `0x003306E0` calls `0x0032E400`.
- Resource: those functions are documented on
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Resource: and on [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Script VM: `0x0032E400` is called by `0x0050DF70`.
- World area: `0x0032E400` is called by `0x00378540`; those functions are documented on
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- World area: `0x0032E400` is called by `0x00268750`, `0x003319D0`, `0x00378030`, `0x00379A10`, `0x003EA820`; those functions are
  documented on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
- World area: and on [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md).
