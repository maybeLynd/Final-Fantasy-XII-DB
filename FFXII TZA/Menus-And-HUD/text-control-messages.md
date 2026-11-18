[Home](../../README.md) / [Menus and HUD](README.md) / Control script messages

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Control script messages: the debug menu text of the .msb files beside the four control scripts | reference | Menus and HUD | Game text tables | Every message of the four .msb files shipped beside the control scripts ctrl, btlctrl, evctrl and mapctrl: the Japanese debug menus and notices of the development build, which the game never opens, with the message count per file, why the in and ch trees hold the same bytes, and how to read the choice lists, sizes and colours in the text. | 0x003306E0, 0x0032E400, 0x002AC5F0 |

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 29 calls with 13 other topics</summary>

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md), [debug menu](../Engine-Core/debug-menu.md), [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) | calls | [`0x002566E0`](../EBP-Script-Files/ebp-script-container.md) (on ebp script container)<br>[`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0037DC30`](../EBP-Script-Files/ebp-script-container.md) (on ebp script container) |
| [`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) | is called by | [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |

**Graphics** (explained on [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [message windows](message-windows.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | calls | [`0x003A1DB0`](../PhyreEngine/the-frame.md) Render command: submit current buffer and swap (on the frame) |
| [`0x002AC5F0`](text-drawing.md) (on text drawing) | is called by | [`0x002AAE40`](text-drawing.md) (on text drawing) |
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x003B2310`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x003B53C0`](../Game-Files-And-Data-Tables/small-bin-tables.md) (on small bin tables) |
| [`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) | calls | [`0x002561C0`](../EBP-Script-Files/ebp-camera-tables.md) (on ebp camera tables) |

**Game files and data tables** (explained on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [startup constants](../Engine-Core/startup-constants.md), [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00249210`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages)<br>[`0x0024AC30`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue)<br>[`0x00259DF0`](../Game-Files-And-Data-Tables/ps2data-bin-families.md) (on ps2data bin families)<br>[`0x00379E90`](../Game-Files-And-Data-Tables/small-bin-tables.md) (on small bin tables)<br>[`0x00384420`](../Game-Files-And-Data-Tables/authored-data-tables.md) (on authored data tables)<br>[`0x0039C3F0`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x003EADE0`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue)<br>[`0x0051ED10`](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md) (on file requests and the read queue) |
| [`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) | calls | [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) |

**Scripts and script commands**

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x0050DF70`](../Game-Files-And-Data-Tables/resource-lifecycle.md) (on resource lifecycle) |

**World, areas and travel** (explained on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [frame update order](../Engine-Core/frame-update-order.md), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md), [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md), [item and ability ids](../Engine-Core/item-and-ability-ids.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00378540`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) |
| [`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list) | is called by | [`0x00268750`](../Game-Files-And-Data-Tables/ps2data-bin-families.md) Map ref: begin load resources (on ps2data bin families)<br>[`0x003319D0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00378030`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00379A10`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list)<br>[`0x003EA820`](../Game-Files-And-Data-Tables/ard-area-battle-data.md) Area ard: load or unload field resource (on ard area battle data) |

</details>
