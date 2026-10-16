---
title: "EBP navigation icons: the NAVIICN2 block a field map script carries for its minimap markers"
kind: "format"
category: "EBP script files"
addresses: "00332100, 003DFDC0, 02B59D58, 003DFCC0, 003DFBE0, 003DFDD0, 00400CF0, 00400550, 00352430, 003DFA50, 003DFDA0, 0032A8A0"
---

## What the player sees

The markers the minimap shows during play are listed in the field map script's section 4. Each icon names an object of the
zone, and the minimap draws the icon where that object stands, once the icon's story gate
passes. The same block lets a script move an actor onto the object an icon names.

## Where it comes from

Section 4 is slot 4 of the `.ebp` directory ([EBP script container](ebp-script-container.md)).
The directory walker `003304A0` dispatches it at `0033064B`; the handler `00332100` drops the
manager index from the low four bits of its argument and tail-jumps to `003DFDC0`, which stores
the section address in the single global `02B59D58`. The handler reads no byte of the block, and
there is one global for all managers: the last script loaded with a section 4 wins.

The global is cleared by `003DFDA0` (from the boot `00266D10`) and by `003DFA50` (from the area
unload `002628B0`, at `00262CD4`), which passes a non-null block to `00331880` and nulls it.

## Layouts

The block has the NAVIICN2 layout of the location map's sloc files
([map menu files](../Game-Files-And-Data-Tables/menu-map-files.md)). Offsets are from the
section start, as `003DFCC0` and `003DFBE0` read them:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | magic | "NAVIICN2"; byte +7 must be '2' or above (`32`<sub>h</sub>) |
| `08`<sub>h</sub> | `u16` | kinds | kinds present; a kind k is read only when 1 <= k <= 9 and k < kinds |
| `0A`<sub>h</sub> | `+ 4k` | u16 | offset     kind k's entries, from the section start |
| `0C`<sub>h</sub> | `+ 4k` | u16 | count      kind k's entry count |

Entry (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i16[2]` | from | read only by setposbynaviicon (low bytes) |
| `04`<sub>h</sub> | `i16[2]` | at | not read for section 4 |
| `08`<sub>h</sub> | `i16` | icon | icon number; a negative icon is refused |
| `0A`<sub>h</sub> | `i16` | gate | story gate (`0032A8A0`); 0 always passes, 1 never shows |
| `0C`<sub>h</sub> | `u8[4]` | - | not read |

## Shipped data

| Fact | Value |
|---|---|
| files | 209 field map scripts per language tree, all under `plan_map/`; none in event scripts |
| `kinds` | 10 in every block |
| sizes | 128 to 704 bytes, 128 in most |
| `us` entries | 650: kind 3 93, kind 5 455, kind 6 1, kind 8 13, kind 9 88; kinds 1, 2, 4 and 7 unused |
| `us` icons | kind 3: 1, 2, 21, 22, and -1 once; kind 5: 1 to 28, mostly 12 (one per file), 14 (84) and 20 and 22 (48 each); kind 6: 3; kind 8: 15; kind 9: 17, 24, and -1 twice |
| `us` gates | 0 in 301 entries, 1 in 134, a story flag in 215 |
| `from` equal to `at` | 475 of 650 `us` entries |
| layout checks | every kind's entries follow the directory or the previous kind with no gap, and the bytes after the last entry are zero |
| languages | the same in every tree except four maps (`bhm_a02`, `gil_i01`, `gil_i02`, `naf_b04`), which differ in `ch`, `cn`, `de`, `es`, `in` and `kr`; `de`, `es`, `in`, `kr`, `ch` and `cn` carry 649 entries |

## Loader behaviour

### The accessors

- `003DFCC0(kind)` returns kind `kind`'s count, or 0 when the global is null, byte `+7` is below
  `'2'`, or the kind is 0, above 9 or not below `kinds` (`003DFCCC`-`003DFCE9`).
- `003DFBE0(kind, i, out)` stores the object `003DFDD0(kind, i)` resolves at `out`, applies the same
  tests plus `i < count`, and stores the entry's address at `out + 10h` (`003DFC7D`). It returns 1
  only when the icon is not negative, an object was found, and `0032A8A0(gate)` passes
  (`003DFC81`-`003DFC9C`).

`003DFB50` and `003DFBB0`, which read the same layout from a sloc block passed to them, are the
location map's accessors; they never read `02B59D58`.

### Which object an icon names

`003DFDD0(kind, i)` turns the entry number into an object through a jump table on the kind
(`003DFDF7`):

| Kind | Resolver | Object |
|---|---|---|
| 1, 2 | `00264A40` | entry `i` of list 0 in the zone script's image |
| 3, 5, 8 | `00264CA0` | entry `i` of list 2, 3 or 4 (`00264E40`) |
| 6 | `00264CA0` → `003DFAC0` | entry `i` of table 6 of section 16, the position block at `02B59D48` |
| 4, 7, 9 | none | nothing, so `003DFBE0` refuses every entry |

The lists are the per-class tables of manager 0's bound script image, found through its header
`+70`<sub>h</sub> (`00264AE0`). `002649B0(class, i)` returns `table + 10h + i * 20h`, or null when `i` is
not below the count at `+0`; for classes 0 and 1 it also returns null when the byte at `table + 2Ch + i * 20h`
lacks the bit numbered by `00377860()`.

### The minimap

`00400550(list, 0)`, called by the minimap's list build `003C5130` (`003C5374`), runs
`00400CF0` for kinds 5, 8, 3 and 4 in that order. For each entry `00400CF0`:

1. stops once the list holds 64 icons;
2. skips the entry unless `003DFBE0` returns 1, and skips icon 14 (the caller passes 0 for the
   flag that would keep it);
3. adds it only when its gate is not 1, its icon is not 0, and its gate is 0 or `0032A8A0(gate)`
   passes;
4. takes the icon number from the low byte of `+08`<sub>h</sub> and the position from the first and third
   words of the resolved object, not from the entry's own coordinates.

So kinds 6 and 9 never reach the minimap, and kind 4 entries resolve to nothing. How the
minimap draws the list is on [map screens](../Menus-And-HUD/map-screens.md).

### `setposbynaviicon`

`setposbynaviicon` (`30D`<sub>h</sub>, `00352430`) pops an entry number and a kind and calls `003DFBE0`.
When the entry exists it sets the actor's byte `+0F`<sub>h</sub> to the icon's low byte with bit 6 set and
copies the low bytes of `from` x and y to `+21`<sub>h</sub> and `+22`<sub>h</sub>. When the object exists it pushes
the object's four words and runs `setpos2_20d` (`00350C30`), placing the actor at the object.

## Modding notes

- Keep `NAVIICN2` with byte `+7` at `'2'` and `kinds` above the highest kind used; 10 does for
  every kind.
- An icon must name an existing entry of its kind's list; the minimap draws it at that entry's
  position, and moving `at` changes nothing.
- Use kinds 3, 5 or 8 for minimap markers; kind 6 only serves `setposbynaviicon`, and kinds 4, 7
  and 9 resolve to nothing.
- Icon 14, icon 0, gate 1 and a negative icon are never drawn on the minimap.
- The minimap holds at most 64 icons.
- Only one block is live: a script loaded later for another manager replaces the field's block.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches section 4.
- [Map menu files](../Game-Files-And-Data-Tables/menu-map-files.md): the same block inside the sloc files, read by the location map.
- [Map screens](../Menus-And-HUD/map-screens.md): the minimap that draws the icons.
- [Story flags](../Story-Events-And-Hunts/story-flags.md): the gates the icons name.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): `setposbynaviicon`.
