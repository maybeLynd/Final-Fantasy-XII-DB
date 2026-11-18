[Home](../../README.md) / [EBP script files](README.md) / EBP navigation icons

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| EBP navigation icons: the NAVIICN2 block a field map script carries for its minimap markers | format | EBP script files | Script sections | Section 4 of a field map's .ebp script: the NAVIICN2 icon block bound to one global, the accessors that read it, how each icon kind names a position entry of the zone script, which kinds and icons the minimap shows and where it places them, the verb that moves an actor to an icon's object, the shipped blocks, and the rules an edit must follow. | 0x00332100, 0x003DFDC0, 0x02B59D58, 0x003DFCC0, 0x003DFBE0, 0x003DFDD0, 0x00400CF0, 0x00400550, 0x00352430, 0x003DFA50, 0x003DFDA0, 0x0032A8A0 |

## What the player sees

The markers the minimap shows during play are listed in the field map script's section 4. Each icon names an object of the
zone, and the minimap draws the icon where that object stands, once the icon's story gate
passes. The same block lets a script move an actor onto the object an icon names.

The object an icon names is an entry in one of the lists of the zone script's image (section 0), and the minimap takes
the marker's position from that entry, not from the icon itself.

## Where it comes from

Section 4 is slot 4 of the `.ebp` directory ([EBP script container](ebp-script-container.md)).
The directory walker `0x003304A0` dispatches it at `0x0033064B`; the handler `0x00332100` drops the
manager index from the low four bits of its argument and tail-jumps to `0x003DFDC0`, which stores
the section address in the single global `0x02B59D58`. The handler reads no byte of the block, and
there is one global for all managers: the last script loaded with a section 4 wins.

The global is cleared by `0x003DFDA0` (from the boot `0x00266D10`) and by `0x003DFA50` (from the area
unload `0x002628B0`, at `0x00262CD4`), which passes a non-null block to `0x00331880` and nulls it.

## Layouts

All multi-byte fields are little-endian.

The block has the NAVIICN2 layout of the location map's sloc files
([map menu files](../Game-Files-And-Data-Tables/menu-map-files.md)). Offsets are from the
section start, as `0x003DFCC0` and `0x003DFBE0` read them:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[8]` | magic | "NAVIICN2"; byte +7 must be '2' or above (`0x32`) |
| `+0x08` | `u16` | kinds | kinds present; a kind k is read only when 1 <= k <= 9 and k < kinds |
| `+0x0E` | `u16[9][2]` | kindTable | per kind k, 1 to 9, the pair at `+0x0A` + 4k: the offset of the kind's entries from the section start, then their count |

Entry (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16[2]` | from | read only by setposbynaviicon (low bytes) |
| `+0x04` | `i16[2]` | at | not read for section 4 |
| `+0x08` | `i16` | icon | icon number; a negative icon is refused |
| `+0x0A` | `i16` | gate | story gate (`0x0032A8A0`); 0 always passes, 1 never shows |
| `+0x0C` | `u8[4]` | - | not read |

The block is used in place inside the loaded `.ebp`: `0x02B59D58` holds its address, which `0x003DFDC0` stores and
`0x003DFCC0`¹ and `0x003DFBE0`² read. The boot clear `0x003DFDA0` nulls it³. The area
unload `0x003DFA50` reads it⁴, passes a non-null block to the free `0x00331880` and nulls it⁵; the
free runs only when `0x005C5230(5)` returns non-zero⁶, which it never does.
The boot clear `0x003DFDA0` also zeroes the two field roots `0x02B59D48` and `0x02B59D50`
with one 16-byte store⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFCC0` |
| ² | `0x003DFC14` |
| ³ | `0x003DFDA3` |
| ⁴ | `0x003DFA8A` |
| ⁵ | `0x003DFA9B` |
| ⁶ | `0x003318A2`-`0x003318A9` |
| ⁷ | `0x003DFDAE` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| files | 209 field map scripts per language tree, all under `plan_map/`; 0 in event scripts |
| `kinds` | 10 in every block |
| sizes | 128 to 704 bytes, 128 in most |
| `us` entries | 650: kind 3 93, kind 5 455, kind 6 1, kind 8 13, kind 9 88; kinds 1, 2, 4 and 7 unused |
| `us` icons | kind 3: 1, 2, 21, 22, and -1 once; kind 5: 1 to 28, mostly 12 (one per file), 14 (84) and 20 and 22 (48 each); kind 6: 3; kind 8: 15; kind 9: 17, 24, and -1 twice |
| `us` gates | 0 in 301 entries, 1 in 134, a story flag in 215 |
| `from` equal to `at` | 475 of 650 `us` entries |
| layout checks | every kind's entries follow the directory or the previous kind with no gap, and the bytes after the last entry are zero |
| languages | the same in every tree except four maps (`bhm_a02`, `gil_i01`, `gil_i02`, `naf_b04`), which differ in `ch`, `cn`, `de`, `es`, `in` and `kr`; `de`, `es`, `in`, `kr`, `ch` and `cn` carry 649 entries |

[`ebp-navigation-icon-entries.tsv`](ebp-navigation-icon-entries.tsv) lists every entry of section 4 in all nine
language trees, 5,844 rows, 650 of them in `us`. Every block sits in a script named `global/<zone>.ebp`, so a zone has
one block per language. A row keeps the entry's own coordinates apart from those of the object it names.

The object comes from section 0 of the same `.ebp`, the zone script that manager 0 loads¹. In `us` 366
entries name an object. Another 195, kinds 3 and 5, ask for an entry at or past the count of their list, and
`0x002649B0` returns null for those².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00314020` |
| ² | `0x002649D1` |

</details>

The status column applies the tests that do not depend on the save: `0x00400550` lists kinds 5, 8, 3 and 4, and
`0x00400CF0` needs an object, an icon that is not negative, 0 or 14, and a gate other than 1. Of the 650 `us` entries
154 pass: 121 with gate 0, and 33 that show only once their gate passes. The others are 195 without an object,
131 with gate 1, 81 with icon 14 and 89 of kinds 6 and 9.

No file has more than 6 entries that pass. The list holds 64 icons, and the actors' entries come first in it¹, so what fits depends on how many actors are present.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003C5130` |

</details>

The minimap's sprite is a record of `battle_4_c`, entry 0 of `tex2pack_ys.bin`: set 4, group 0, frame = the icon's low
byte¹. In `us`, group 0 holds 19 frames, so a higher icon number reads the records of the
groups after it. The location map draws the same icon numbers from another atlas
([map menu files](../Game-Files-And-Data-Tables/menu-map-files.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0040043B`-`0x0040046E` |

</details>

The table is produced by `Database/Tools/catalogues/navi_icons.py`.

| Column | Meaning |
|---|---|
| `tree`, `script` | the language tree, and the path under it |
| `kind`, `entry`, `file_offset` | the kind, the entry's number in it, and its offset in the file |
| `from_x`, `from_y`, `at_x`, `at_y` | the words at `+0x00` to `+0x07` |
| `icon`, `gate`, `bytes_0c` | the words `+0x08` and `+0x0A`, and the four bytes at `+0x0C` in hex |
| `gate_kind` | as `0x0032A8A0` reads the gate: `always`, `never`, `primary` (a flag of the Primary bank) or `schedule` |
| `gate_id` | for `primary` the `id`, for `schedule` the `encoded_id` of the tables on [story flag ids](../Story-Events-And-Hunts/story-flag-ids.md) and [story flags](../Story-Events-And-Hunts/story-flags.md); `-` otherwise |
| `list`, `list_count` | the list the kind reads, and that list's count in this file; `-` for a kind with no list |
| `object_state` | `object`, `past_list`, `older_table` for kind 6 (`0x003DFAC0`), or `no_resolver` for kinds 4, 7 and 9 |
| `object_offset` | the object's offset in the file |
| `object_x`, `object_y`, `object_z`, `object_w` | the object's four floats; the minimap draws at `object_x`, `object_z` |
| `object_bits`, `object_tail` | the same four floats as stored, then the object's other 16 bytes, in hex |
| `minimap_static` | `eligible`, or the first test the entry fails: `kind_not_listed`, `no_object`, `icon_negative`, `gate_never`, `icon_14`, `icon_zero` |
| `needs_gate` | 1 when an `eligible` entry still needs its gate at run time |
| `sprite` | x, y, width and height of its sprite record; `-` for a kind the minimap does not list or a negative icon |

Four `primary` ids, `0x005D`, `0x009C`, `0x00C4` and `0x00C5`, have no row on the story flag ids table.

</details>

## Loader behaviour

### The accessors

- `0x003DFCC0(kind)` returns kind `kind`'s count, or 0 when the global is null, byte `+7` is below
  `'2'`, or the kind is 0, above 9 or not below `kinds`¹.
- `0x003DFBE0(kind, i, out)` stores the object `0x003DFDD0(kind, i)` resolves at `out`, applies the same
  tests plus `i < count`, and stores the entry's address at `out + 0x10`². It returns 1
  only when the icon is not negative, an object was found, and `0x0032A8A0(gate)` passes
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFCCC`-`0x003DFCE9` |
| ² | `0x003DFC7D` |
| ³ | `0x003DFC81`-`0x003DFC9C` |

</details>

`0x003DFBE0` first zeroes the three qwords at `out`¹ and calls the resolver before
any test². When `i` is not below the count it returns 0 with `out + 0x10` still null³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFC01`-`0x003DFC0B` |
| ² | `0x003DFC0F` |
| ³ | `0x003DFC49`-`0x003DFC4F` |

</details>

`0x003DFB50` and `0x003DFBB0`, which read the same layout from a sloc block passed to them, are the
location map's accessors; they never read `0x02B59D58`.

### Which object an icon names

`0x003DFDD0(kind, i)` turns the entry number into an object through a jump table on the kind¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFDF7` |

</details>

| Kind | Resolver | Object |
|---|---|---|
| 1, 2 | `0x00264A40` | entry `i` of list 0 in the zone script's image |
| 3, 5, 8 | `0x00264CA0` | entry `i` of list 2, 3 or 4 (`0x00264E40`) |
| 6 | `0x00264CA0` → `0x003DFAC0` | an older-layout table that `0x003DFAC0` looks for in section 16 at the offset in its `+0x08`; in an `FF12POS3` section that word is `size`, so the lookup reads past the records ([Position entries](ebp-position-entries.md)) |
| 4, 7, 9 | no resolver | nothing, so `0x003DFBE0` refuses every entry |

`0x003DFDD0(kind, i, out)` zeroes `out` and `out + 8`¹ and stores the object at
`out`. For kinds 1 and 2 it also stores `object + 0x10` at `out + 8` when the object is non-null². It returns 1 when the object at `out` is non-null³.
Kinds 4 and 7 jump straight to that test, and kind 9 and kind 0 lie outside the table⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DFDDF`, `0x003DFDE5` |
| ² | `0x003DFE0D`-`0x003DFE16` |
| ³ | `0x003DFE24`-`0x003DFE2C` |
| ⁴ | `0x003DFDE9` |

</details>

The lists are the per-class tables of manager 0's bound script image, found through its header
`+0x70`¹. `0x002649B0(class, i)` returns `table + 0x10 + i * 0x20`, or null when `i` is
not below the count at `+0`; for classes 0 and 1 it also returns null when the byte at `table + 0x2C + i * 0x20`
lacks the bit numbered by `0x00377860()`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00264AE0` |

</details>

### The minimap

`0x00400550(list, 0)`, called by the minimap's list build `0x003C5130`¹, runs
`0x00400CF0` for kinds 5, 8, 3 and 4 in that order. For each entry `0x00400CF0`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003C5374` |

</details>

1. stops once the list holds 64 icons;
2. skips the entry unless `0x003DFBE0` returns 1, and skips icon 14 (the caller passes 0 for the
   flag that would keep it);
3. adds it only when its gate is not 1, its icon is not 0, and its gate is 0 or `0x0032A8A0(gate)`
   passes;
4. takes the icon number from the low byte of `+0x08` and the position from the first and third
   words of the resolved object, not from the entry's own coordinates.

`0x00400550` returns at once when its second argument is non-zero¹, and passes each call's
returned index to the next as the first index². The count is the dword at
`list + 0`, and icon `n` fills the 32 bytes at `list + 0x10 + n * 0x20`³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00400552` |
| ² | `0x00400585`, `0x0040059F`, `0x004005B9` |
| ³ | `0x00400D0B`-`0x00400D47` |

</details>

| Offset | Value |
|---|---|
| `+0x00` | the dword with bit `0x10000` and bit `0x40000` set and bit `0x20000` cleared; its low byte is 5 for kinds 5 and 8, 6 for kind 3 and 7 for kind 4 (`0x00400D86`-`0x00400DA7`) |
| `+0x01` | the icon byte (`0x00400DE6`) |
| `+0x04` | the running index (`0x00400D8D`) |
| `+0x08`, `+0x0C` | the position (`0x00400DF5`, `0x00400E00`) |
| `+0x10` | 0 (`0x00400D94`) |

The stores at `+0x00`, `+0x04` and `+0x10` come before the gate and icon tests, so a refused entry writes
them into the next free slot without counting it¹. A non-zero sixth
argument sets x = `[0x003C8060() + 0x10] + entry.s16[2]` and z = `[0x003C8060() + 0x14] + entry.s16[3]`
instead²; `0x00400550` passes 0 in every call³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00400DB7`-`0x00400DDB`, `0x00400E43` |
| ² | `0x00400E05`-`0x00400E3E` |
| ³ | `0x00400568`, `0x0040057E`, `0x00400598`, `0x004005B2` |

</details>

So kinds 6 and 9 never reach the minimap, and kind 4 entries resolve to nothing. How the
minimap draws the list is on [map screens](../Menus-And-HUD/map-screens.md).

### `setposbynaviicon`

`setposbynaviicon` (`0x30D`, `0x00352430`) pops an entry number and a kind and calls `0x003DFBE0`.
When the entry exists it sets the actor's byte `+0x0F` to the icon's low byte with bit `0x40` set and
copies the low bytes of `from` x and y to `+0x21` and `+0x22`. When the object exists it pushes
the object's four words and runs `setpos2_20d`¹, placing the actor at the object.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00350C30` |

</details>

It ignores the value `0x003DFBE0` returns and reads the entry and the object straight from the output¹, so a story gate that fails or a negative icon does not stop either step. The four
words are pushed as floats through `0x00267F60`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00352476`, `0x00352497` |
| ² | `0x003524A1`-`0x003524CF` |

</details>

`0x00350C30` pops four floats with `0x00267DB0`: the facing first, then z, y and x¹. It calls `0x0026B0C0(actor, x, y, z)`, `0x0026B620(actor, facing)`
and `0x0025D540(actor)`, and ends in a jump to `0x0026AE90(actor, 0)`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00350C53`-`0x00350C75` |
| ² | `0x00350C86`-`0x00350CBE` |

</details>

## Modding notes

- Keep `NAVIICN2` with byte `+7` at `'2'` and `kinds` above the highest kind used; 10 does for
  every kind.
- An icon must name an existing entry of its kind's list; the minimap draws it at that entry's
  position, and moving `at` changes nothing.
- Use kinds 3, 5 or 8 for minimap markers and for `setposbynaviicon`; kind 6 resolves through `0x003DFAC0`,
  which does not read `FF12POS3` records, and kinds 4, 7 and 9 resolve to nothing.
- Icon 14, icon 0, gate 1 and a negative icon are never drawn on the minimap.
- The minimap holds at most 64 icons.
- Only one block is live: a script loaded later for another manager replaces the field's block.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches section 4.
- [Map menu files](../Game-Files-And-Data-Tables/menu-map-files.md): the same block inside the sloc files, read by the location map.
- [Map screens](../Menus-And-HUD/map-screens.md): the minimap that draws the icons.
- [Story flags](../Story-Events-And-Hunts/story-flags.md): the gates the icons name.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): `setposbynaviicon`.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 2 calls with 1 other topic</summary>

**Battle actions** (explained on [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0026B0C0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x0026B620`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |

</details>
