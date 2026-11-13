---
title: "Screen layouts: the UISize layout files, every key they set, the loader that binds each key to its cell, and the screens that read them"
kind: "format"
category: "Menus and HUD"
addresses: "0x001C6C00, 0x001CA600, 0x001AF470, 0x001FF4F0, 0x00200B80, 0x0024B120, 0x00184660, 0x001B24B0"
---

## What the player sees

- Every menu, window, gauge and text line sits where the layout file puts it: list heights, offsets, colours of the
  HP gauges, fade band heights, the map overlay's scale and colour.
- The layout fits the screen at any resolution, because positions are given in a fixed 1920 x 1080 frame.

## Where it comes from

### The files

| File (`jsondata/uisize/`) | Size | Keys |
|---|---:|---:|
| `uisize.json` | 7,478 bytes | 231 |
| `uisize_sd.json` | 4,609 bytes | 164, all also in `uisize.json` |

Each is one JSON object of `"Key": number` pairs, with a trailing comma before the closing brace. The image names them
`JsonData/UISize/UISize.json` (`0x008F9EC0`) and `JsonData/UISize/UISize_sd.json` (`0x008F9EE0`).

`parametersmanageruisizestruct.csv` (10,350 bytes) ships in `jsondata/`: the layout editor's schema, with 36 section
labels and 229 sliders, each with a name, decimal places, minimum, maximum and a `disable` flag. The image holds no
string of its name, so the game does not read it.

### Which file is loaded

`0x001C6C00` (reached from `0x001B1580`, `0x001B159B`) loads the layout once:

1. It returns unless the byte `0x01DF6E48` or `0x01F81282` is set (`0x001C6C20`-`0x001C6C30`).
2. With the document `0x01F81318` already parsed, it goes straight to the loader (`0x001C6C44`).
3. Otherwise it reads the byte `[0x01F811E0]` (`0x001B1620`, `0x001C6C4A`): set loads `UISize.json` (`0x001C6C83`), clear loads
   `UISize_sd.json` (`0x001C6D54`). Then it parses the file into `0x01F81318` (`0x00200BF0`) and runs the loader `0x001CA600`.

The byte `[0x01F811E0]` comes from `[0x01E0280C]`, shipped 1, through `0x00184660` and `0x001B24B0` at start-up
(`0x0022A113`-`0x0022A120`). The same call sets the layout frame `0x01E0C1D8` x `0x01E0C1DC` to 1920 x 1080 (`0x0024B124`,
`0x0024B12E`), or 512 x 448 when clear. So the shipped game loads `UISize.json` into a 1920 x 1080 frame.
`0x0024ABC0()` returns the frame width over 512 (`0x01E0C1D8` x `[0x008C5B30]`, 1/512), 3.75 in the 1920 frame; it has
24 call sites, among them the HUD draw `0x003F0610` and `0x00505570`.

### From the file to the cells

The file is converted, not used in place. The JSON reader `0x00200BF0`, which `0x001C6C00` calls with `0x01F81318`
(`0x001C6CFE`, `0x001C6DD4`), opens it and allocates its size plus one byte
(`0x00200C5A`-`0x00200C60`), reads it and ends it with a 0 (`0x00200C73`-`0x00200C7B`), parses the text into the value nodes
of the document `0x01F81318` (`0x00200E60`, called at `0x00200DF9`) and frees the read buffer (`0x00200E01`). A file whose
size reads as -1 or 0 is not parsed (`0x00200C45`-`0x00200C54`). The loader `0x001CA600` then copies each key's value
from the document into its cell, one key at a time.

## Layouts

All multi-byte fields are little-endian.

The files are JSON text. The node table below is the parsed value each key becomes, with offsets from the start of
the node.

The loader `0x001CA600` binds every key by its own code, with no table (1,602 instructions):

1. It stops at once if `mScrollListHeight` is absent (`0x001CA604`-`0x001CA621`).
2. For each key it looks the name up (`0x001FF740`), reads it as an integer (`0x00200B80`) or a float (`0x00200B50`), and
   stores it through a pointer slot (`mov rcx, [rbx + slot]` / `mov [rcx], eax`).
   - `0x001FF740(node, name)` copies the name into a string and calls `0x001FF6B0(node, string)` (`0x001FF761`-`0x001FF81D`).
     A node that is not an object (tag 3) is first passed to `0x002001F0`, which dispatches on its old tag, and then
     gets tag 3 and a new `0x38`-byte map from `0x00210EC0` at `+0x08` (`0x001FF6CF`-`0x001FF713`). The lookup then runs
     in that map: `0x001FF6B0` ends with a jump to `0x001FF4F0(map, string)` (`0x001FF72D`).
   - `0x001FF4F0` walks the map's tree from `+0x18`, ordering keys by `memcmp` over the shorter length and then by
     length (`0x001FF540`-`0x001FF5DB`). A missing key is inserted at the place found, with tag 6, payload 0 and a copy
     of the key, through `0x001FFD40` (`0x001FF5E1`-`0x001FF64C`). Either way it answers the entry's value node at `+0x40`
     (`0x001FF68E`).
3. The slots are `[0x01F811E8] + 0x3B00` onwards, filled by `0x001AF470` (`0x001AF477`-`0x001B00D3`), and three more at
   `[0x01F81200] + 0x2F8`-`+0x308`, filled by `0x001B44A0` (`0x001B4551`-`0x001B4574`), for the three float keys.

| Count | |
|---|---:|
| keys bound | 226 |
| read as integers | 223 |
| read as floats (`FontItalicVal`, `FontItalicScale`, `FontShadowAlphaMuti`) | 3 |
| file keys never bound (`NA_HintMessageIcon_PosX/Y`, `NA_HintMessage_PosX/Y`, `mBtlCommandScrollTableOffsetX`) | 5 |
| slots with no key (cells `0x01F2CA94`-`0x01F2CAA0`) | 4 |

No two keys share a cell, and every cell is in `.data`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | tag | 1 integer, 2 double, 3 object, 6 absent (`0x00200BE0`, `0x001FF5E1`) |
| `+0x08` | `u32[2]` | payload | pointer to the value or the child map (`0x00200B87`, `0x00200B93`) |

An integer read returns the integer for tag 1, the truncated double for tag 2, and 0 otherwise (`0x00200B9C`); a float
read converts either and returns 0.0 otherwise (`0x00200B75`).

## Shipped data

| | |
|---|---:|
| keys read by some screen | 224: 213 at 480 read sites in 124 functions; the ten `mCursor{Right,Down,Left,Up,Open}{X,Y}` through the pointers at `+0x08` and `+0x10` of the hand cursor's kind table `0x01E0C150`, which the hand draw `0x002426F0` reads (`0x00242785`-`0x0024279A`; [Menu sprites](menu-sprites.md)); and `FontShadowAlphaMuti` through the font manager's slot `+0x308` (`0x001B5210`, `0x001B521C`), from the font border filter pass `0x00190260` (`0x00190434`) |
| keys bound but read by nothing | 2: `BattleLogBlackBandH`, `LicenseBlackBandH` |
| shipped values outside their schema range | 0, in either file |
| keys `uisize_sd.json` lacks | 63 of the 226 bound |

| Screen | Keys |
|---|---:|
| battle HUD: help line, target window, gauges, damage and EXP numbers, party window | 59 |
| message windows | 27 |
| battle menu ([Battle menu](battle-menu.md)) | 22 |
| Gambits ([Gambits screen](gambit-screen.md)) | 18 |
| menus: lists, scrolling, help, button signal | 15 |
| the hand cursor ([Menu sprites](menu-sprites.md)) | 10 |
| World Map ([Map screens](map-screens.md)) | 11 |
| dialogs ([Dialogs](dialogs.md)) | 10 |
| map overlay, `TrackMap*` | 8 |
| License Board ([License Board screen](license-board-screen.md)) | 6 |
| others: window frames, menu bands, Clan Primer, portraits, pause menu, location map, text, status window, screen mask, button legend, item screen, auto window, shop | 38 |

The cells' values in the image itself are the 512 x 448 layout: for 157 of the 163 bound keys `uisize_sd.json` holds,
the cell starts at that file's value.

### The key table

[`screen-layouts.tsv`](screen-layouts.tsv) has one row for each key of the two layout files:

| Column | Meaning |
|---|---|
| `key` | the key name, as the loader looks it up (`0x008FB678`-`0x008FCBF0`) |
| `file` | which shipped files hold it |
| `cell` | the global the loader stores it in |
| `type` | integer or float read, and the widths readers use |
| `shipped_value` | the value in `uisize.json` |
| `readers` | each reading function and its read sites |
| `screen` | the screen the readers belong to |
| `uisize_sd_value` | the value in `uisize_sd.json`, or `-` |
| `cell_static_init` | the cell's value in the image before loading |
| `loader_read_site` | the loader instruction that names the key; the typed read follows it |
| `slot` | the pointer slot it is stored through |
| `csv_label` | the schema section it sits under |
| `csv_range` | the schema minimum, maximum and decimal places |
| `reader_widths` | the access widths the readers use: u8, u16 or u32 |

## Loader behaviour

1. A key missing from the loaded file is inserted as absent (tag 6, `0x001FF5E1`) and stored as 0. Loading
   `uisize_sd.json` would therefore set its 63 missing keys to 0, not leave their built-in values.
2. The loader never checks a value against the schema's range.
3. Every reader reads its cell directly by its address, with two exceptions. `0x001B5210` reads
   `FontShadowAlphaMuti` through the font manager's slot `+0x308` (`0x001B521C`), and the hand draw `0x002426F0` reads
   the ten `mCursor` cells as words through the eight-byte pointers that its kind table `0x01E0C150` holds
   (`0x01E0C158`-`0x01E0C1C0`; `0x0024278A`, `0x0024279A`).
4. `EXPLPNumOffsetX` is the one key code writes: `0x0028B24A` overwrites it with `ExpNumOffsetX` or `LpNumOffsetX` before
   its read at `0x0028B5F1`, so its file value never reaches the screen. Its schema row has `disable` set.
5. The `disable` flag is set on six schema rows (`mNumEffectOffsetX1`, `NumEffectOffsetY1`, `mExpEffectOffsetY`,
   `EXPLPNumOffsetX`, `FontBaseWidth`, `FontBaseHeight`); five of them are loaded and read as usual.

## Modding notes

- Edit `uisize.json`; `uisize_sd.json` is not loaded by the shipped game.
- Keep every key the loader binds in the file, because a missing key sets its cell to 0.
- Values are positions and sizes in the 1920 x 1080 frame; colour keys are 0-255.
- The three float keys accept fractions; every other key is truncated to an integer.

## Related

- [Battle menu](battle-menu.md) - the battle screen keys.
- [Map screens](map-screens.md) - the `TrackMap*` keys.
- [Dialogs](dialogs.md) - the dialog keys.
- [Fonts](fonts.md) - the text keys.
- [Menus](menus.md) - the menu screens.
