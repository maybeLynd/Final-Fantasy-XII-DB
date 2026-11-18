[Home](../../README.md) / [Game files and data tables](README.md) / Menu resource packages (.mrp)

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Menu resource packages (.mrp): the twelve menu layout files, who loads each one and how a request becomes a relocated list file | format | Game files and data tables | Menu and map files | The standalone mrp_menu/*.mrp files: which screen requests each of the twelve names and with which kind 7 id, the request wrappers that attach the relocation callback, the request groups that tell a screen when all its files have landed, the other carriers of the same format (mrppack_ys.bin and the map packs), the in_sdver copies, the 116 shipped files by name, and the rules for editing or adding one. | 0x00249320, 0x00249350, 0x003933F0, 0x00249210, 0x0208F578, 0x002495C0, 0x00249660, 0x002A00F0, 0x00249580, 0x02090790, 0x00249410, 0x00280980, 0x002DF9A0, 0x01E0280C, 0x003EF830, 0x00393FF0, 0x003F4840, 0x0057B780, 0x00562F90, 0x00404060, 0x00582790, 0x00579AF0, 0x00574E80, 0x002486B0, 0x002494A0 |

## What the player sees

The fixed layout of the title screen, the game-over screen, save and load, the shops, the Clan Primer and its hunt
list, the location map and the World Map menu. Each of those screens loads one `.mrp` file that places its frames,
icons, captions and gauges, cut from texture atlases loaded beside it. Editing the file moves or recolours those
pieces without touching code.

## Where it comes from

The files are resource kind 7 at `ps2data/image/ff12/myoshiok/<locale>/mrp_menu/<name>.mrp`. Every file is
requested as a whole and relocated in place once it lands; the requesting screen keeps the buffer.

| File | Kind 7 id | Requester | Request site |
|---|---|---|---|
| `gameover.mrp` | `0x38` | the game-over task `0x003EF830` | `0x003EF9DE` (through `0x003933F0`) |
| `title.mrp` | `0x3A` | `0x00393FF0` | `0x00394048` |
| `title_menu.mrp` | `0x3B` | no call site passes this id as a constant | |
| `save_load.mrp` | `0x6F` | the save and load setup `0x00582790` | `0x005827D8` (through `0x003933F0`) |
| `E3_Logo.mrp` | `0x89` | no call site passes this id as a constant | |
| `quest.mrp` | `0x92` | the Clan Primer hunt list `0x00579AF0` | `0x00579F73` (through `0x003933F0`) |
| `shop_new.mrp` | `0x96` | the grant list `0x003F4840`; `0x0057B780` | `0x003F492D` (through `0x00249320`), on the create message only when the create record's `+0x18` holds no buffer (`0x003F48FD`), a buffer the list frees on message `0x0F` (`0x003F4A0B`); with a buffer there the list uses that one (`0x003F4906`). `0x0057B7AC` (through `0x003933F0`) |
| `w_menu.mrp` | `0xA6` | `0x00562F90` | `0x00563048` (through `0x00249350`) |
| `Loca.mrp` | `0xBF` | the location-map resources `0x00404060` | `0x00404107` |
| `Party_Book.mrp` | `0xCC` | the Clan Primer back panel `0x00574E80` | `0x00574F94` (through `0x003933F0`) |

Ids are those of the US kind-7 path array (`0x01EC73A0`), which names the `us` copy of every file except
`w_menu.mrp`, taken from `in`. `nowload.mrp` and `title_fore3.mrp` ship but no path string in the executable names
them, so the game never loads them.

## Layouts

All multi-byte fields are little-endian.

A `.mrp` is a UI typed-list file: the magic `MRP`, a prepared byte at `+3`, and three `{count, offset}` tables
that `0x002A00F0` turns from file offsets into pointers in place. The tables are the 20-byte list records (`+0x1C`,
`+0x20`), the 16-byte atlas name records (`+0x04`, `+0x08`), which end the file, and the 12-byte atlas row table
(`+0x24`, `+0x28`). [UI typed lists](ui-typed-lists.md) gives the full layout, the items, and the relocation.

The header, with the values of all 116 shipped files:

| Offset | Type | Field | Shipped | Relocation |
|---|---|---|---|---|
| `+0x00` | `char[3]` | `MRP` | `MRP` | |
| `+0x03` | `u8` | prepared | 0 | read by `0x002A00F0`; set to 1 after the pass |
| `+0x04` | `u32` | atlas name records | the count | |
| `+0x08` | `u32` | their offset, from the file start | the name records, which end the file | rewritten by `0x002A00F0` |
| `+0x0C` | `u32` | | 0 | |
| `+0x10` | `u32` | end of the name records | the file size | |
| `+0x14` | `u32` | | 0 | |
| `+0x18` | `u32` | | the file size | |
| `+0x1C` | `u32` | list records | the count | read by `0x002A1A80` |
| `+0x20` | `u32` | their offset, from the file start | `0x30` | rewritten by `0x002A1A80` |
| `+0x24` | `u32` | row registrations | 0 | read by `0x002A00F0` |
| `+0x28` | `u32` | the row table's offset, from the file start | the file size | rewritten by `0x002A00F0` |
| `+0x2C` | `u32` | | 0 | |

The load checks only byte `+3`: when it is 1, `0x002A00F0` returns at once and the offsets stay as they are.
Otherwise it rewrites `+0x08`, `+0x20` (through `0x002A1A80`) and `+0x28` into the engine's 32-bit encoded
addresses (`0x0020E620`), then the `+0x08` of each of the `+0x24` rows, an offset from the row table's start
(`0x002A0145`-`0x002A014E`), and sets byte `+3` to 1 (`0x002A016A`). No count or offset is compared with the file size.

The same bytes ship in two other carriers:

- `packfiles/mrppack_ys.bin` (kind 7 `0xD3` in the US array, requested by `0x002808D0` through `0x00249180`): for each
  of its 23 units, `0x00280980` fills an empty qword at `[0x0209AC30] + 8 × unit` with `pack + u32[unit]` (the pack is
  at `[0x0209AC30] + 0x3D0`) and relocates the unit with `0x002A00F0`.
- `0x00280980` leaves a qword already set as it is and does not relocate it again (`0x002809A8`); with the pack
  pointer null it fills nothing (`0x00280993`). On both paths it ends by jumping to `0x00280AD0` (`0x002809EE`).
- Slot 15 of the map packs `rwg0201` and `rwg0202`, kept for the map gauge ([Map pack](../World-Areas-And-Travel/mpk-map-pack.md)).

## Shipped data

Measured over every `.mrp` in the archive.

| Fact | Value |
|---|---|
| files | 116, 52 distinct contents, in 10 locale folders: `us`, `de`, `es`, `fr`, `it`, `in` have all 12 names; `ch`, `cn`, `kr`, `in_sdver` have 11, lacking `title_fore3.mrp` |
| header | `MRP\0` at `+0`, list records at `0x30`, atlas names ending at the file end, `+0x0C`, `+0x14`, `+0x24` and `+0x2C` zero, `+0x10`, `+0x18` and `+0x28` equal to the file size, in all 116 |
| sizes | 128 bytes (`nowload.mrp`) to 7,696 bytes (`party_book.mrp`) |
| `e3_logo` | 160 bytes, 1 list record, 1 atlas name (`logo_s_c`) |
| `gameover` | 240 bytes, 3 records, 1 name |
| `loca` | 640 bytes, 5 records, 10 names |
| `nowload` | 128 bytes, 1 record, 1 name (`nowload_c`) |
| `party_book` | 7,696 bytes, 60 records, 13 names |
| `quest` | 3,072 bytes, 22 records, 13 names |
| `save_load` | 2,848 bytes, 9 records, 8 names; `in_sdver` 2,736 bytes, 10 records |
| `shop_new` | 3,072 bytes, 16 records, 8 names |
| `title` | 1,008 bytes, 9 records, 3 names; `in_sdver` 848 bytes, 8 records, 2 names |
| `title_fore3` | 848 bytes, 8 records, 2 names |
| `title_menu` | 224 bytes, 3 records, 2 names |
| `w_menu` | 1,840 bytes, 12 records, 4 names |
| atlas `itemgra_c` | named by `save_load` and `shop_new` |
| every record and item | in the two tables of [UI typed lists](ui-typed-lists.md), with the pack units |

## Loader behaviour

### The request

- `0x00249320(group, kind, id)` and `0x00249350(group, kind, id, heap)` call `0x00249210`, then set the request's
  completion to `0x00249660` and return the buffer. `0x00249320` always allocates from heap 3 (`0x00249324`).
  `0x003933F0(group, out[], ids[], n)` calls `0x00249320` with kind 7 for each id and stores each buffer.
- `0x00249210(group, kind, id, heap, top)` takes a free 40-byte request record from the 48 at `[0x0208F578]` (busy
  bit `0x1` of `+0x20`), zeroes it and sets the bit (`0x00249256`-`0x0024926B`), stores the group at `+0`, gets the
  size from `0x0032E400`, allocates it, files `0x0032E620` with the completion `0x002495C0`, and counts the request on
  the group (`+0x18`). It returns the record, whose `+8` holds the buffer.
- It allocates under arena `heap` with tag `0xC` (`0x0036C1D0`, `0x002492B4`), bottom-up (`0x0036A100`) when `top` is 0
  and top-down (`0x0036A190`) otherwise (`0x002492B9`-`0x002492CC`), then pops the arena (`0x0036C140`). `0x00249320` and
  `0x00249350` give `top` 0 (`0x0024932A`, `0x00249354`); `0x002493D0` gives 1 (`0x002493D6`).
- The completion gets the record's address as a 32-bit value (`0x00249286`), which `0x002495C0` sign-extends
  (`0x002495D9`).
- A size below 1 files nothing, leaves the buffer null and does not count the request on the group; it calls only
  the empty function `0x0016D6A0(0x2000)` (`0x002492A6`). The record stays busy: only the completion
  clears the bit, so each such request loses one of the 48 records for good. With all 48 busy the search
  ends on a null record and the next store writes to address 0.
- `0x002495C0` calls the record's completion at `+0x10` when it is set (`0x002495E3`): `0x00249660` loads the buffer from
  `+8` and jumps to `0x002A00F0`, which relocates the file once (byte `+3` guards a second pass). A record filed
  straight through `0x00249210` keeps the zero the take stores there, so it is only counted. Last, `0x002495C0`
  clears the record's busy bit (`0x00249637`).

### Request groups

A screen takes a group with `0x00249580(widget)`, one of 12 32-byte entries at `0x02090790`, files its requests, and
closes the group with `0x00249410`. `0x00249580` takes the first entry with bit `0x1` of `+0x00` clear, zeroes it, sets
the bit, stores the widget at `+0x08` and returns the entry (`0x002495A3`-`0x002495B7`).

With all 12 taken `0x00249580` returns null (`0x002495A0`). A request filed on that null group then counts itself at
address `0x18` (`0x002492F8`), and closing it writes at address 0 (`0x00249425`).

`0x00249410` sets bit `0x2` of `+0x00`, the closed bit. Each completion increments the group's `+0x1A`; once the
group is closed and the count matches `+0x18`, at the close (`0x00249434`) or at the completion that reaches it
(`0x002495FA`), the widget gets message `0x10` (or the group's function at `+0x10` runs). A screen therefore
sees its `.mrp` relocated before it is told its files are ready: `0x002495C0` runs the record's completion
before it raises the group count.

The message goes to the first slot of the widget's table, with 16 zero bytes after the id, and is skipped for a
null widget or a null slot (`0x0024945D`-`0x0024947D`, `0x00249612`-`0x00249632`). The group is then released: bit `0x1`
is cleared (`0x0024947F`, `0x00249634`).

`0x002486B0(function)` takes a group the same way for a function instead of a widget (`+0x04` = 1, the
function at `+0x10`), and returns null with all 12 taken (`0x002486D0`). A function group is never released: both
sites call the function and return without clearing bit `0x1` (`0x00249440`, `0x00249606`). The two functions given
to `0x002486B0`, by `0x00556500` and `0x00563520`, only store 1 in a flag (`0x00556560`, `0x00563550`).

`0x002494A0` zeroes the twelve groups and, when `[0x0208F578]` is null, points it at the 48 request records at
`0x02090910` and zeroes them.

### The in_sdver copies

`0x002DF9A0`, the kind path setup, replaces the kind-7 entries of all ten `.mrp` names it holds and of
`mrppack_ys.bin` with their `in_sdver` paths when its second argument, the word `[0x01E0280C]`, is 0. That word
ships as 1, so the shipped game loads the locale copies.

The `in_sdver` folder holds 54 files: 11 `.mrp`, 4 `.bin` and 39 `.tm2`. [`mrp-menu-resource-packages-in-sdver-rows.tsv`](mrp-menu-resource-packages-in-sdver-rows.tsv) gives each file's size and SHA-256 prefix against its counterpart under `myoshiok/in/`, with the first picture's width and height for a `.tm2`.

- Only one file matches its `in` counterpart byte for byte; the other 53 differ.
- Every `in_sdver` picture is smaller than the `in` picture in both width and height. In 30 files both sides scale by one factor: 2 in 26, 4 in 3 and 16 in 1. In the other 9 the `in` sheet has another shape, for example `handback_c` 512 x 256 against 2048 x 2048.
- `save_load.mrp` and `title.mrp` hold one record more and one record fewer than the `in` copies (Shipped data, above); the other nine `.mrp` files have the `in` copies' sizes.

## Modding notes

- Edit a file in place under the path its locale's kind-7 array names; the request size comes from the file-size
  tables, so a resized file needs its kind 7 entry changed there.
- Ship byte `+3` as 0. A file with 1 there is used as is, with its offsets left unrelocated.
- `nowload.mrp`, `title_fore3.mrp` and the `in_sdver` copies are not loaded by the shipped game; editing them
  changes nothing.
- A screen draws only the records its code decodes by index, so a new record needs code that asks for it.
- An atlas name must match an atlas the screen registers; `itemgra_c` in `save_load` and `shop_new` is the atlas the
  item pictures are copied into ([.as7](as7-menu-graphics.md)).

## Related

- [UI typed lists](ui-typed-lists.md): the file layout, the items, the atlas registry and the relocation.
- [Menu graphics containers (.as7)](as7-menu-graphics.md): the item pictures drawn into the `itemgra_c` atlas.
- [Map pack (.mpk)](../World-Areas-And-Travel/mpk-map-pack.md): slot 15, the same format inside a map pack.
- [File size tables (.fst)](file-size-tables-fst.md): the kind 7 path arrays and request sizes.
- [File requests and the read queue](file-requests-and-the-read-queue.md): `0x0032E400` and `0x0032E620`.
- [Clan Primer](../Menus-And-HUD/clan-primer.md), [Game over](../World-Areas-And-Travel/game-over.md) and
  [Map screens](../Menus-And-HUD/map-screens.md): screens that load these files.
