---
title: "MPK map pack: the sections of a map file, the two packs a field loads, how the loader splits and binds them, and what each section holds"
kind: "format"
category: "World, areas and travel"
summary: "One .mpk per zone under plan_master/map_ctrl: a count of 32, 32 section sizes and the sections back to back, each behind a 0x40-byte slot. Entering a field requests two packs, the field's own and its block's, carves each into 32 arena blocks in place, keeps sound, world (YM00), navigation, actor control, lights, pictures and placements, and frees the rest; the YM00, ACTL, SP1, WD and MRP containers are laid out here with their consumers, and the 550 shipped packs are censused."
addresses: ["00331990", "00378A60", "00378030", "0036B980", "00378BC0", "003775D0", "00378120", "00378230", "002F6AB0", "003E8940", "003E8230", "00363B40", "003631B0", "00379870", "003C63A0", "0037AA90"]
---

# MPK map pack: the sections of a map file, the two packs a field loads, how the loader splits and binds them, and what each section holds

## What the player sees

Walking into a new area loads its map pack: the area's sound bank and positional sounds, its world
data (the models, their placement, the lighting and the weather-dependent look), its navigation
mesh, its lights, the switch-driven objects a script controls, and the picture and coordinates the
minimap uses to show where you are. An area that shares a sound bank with its neighbours loads that
bank once from a second, sound-only pack. A section a pack does not carry simply supplies nothing.

## Where it comes from

Each pack is `ps2data/plan_master/map_ctrl/<area>/<zone>/bin/<zone>.mpk`, 550 files. A zone's own
pack is `<zone>.mpk`; the block pack of an area is the one named `<area>00.mpk`, and all 89 of them
carry only the sound sections (slots 0, 1 and 10) or nothing at all.

The packs are namespace-4 resources. `map_ref.bin` names both packs of a field: the field row's
first word is the field's own pack index (`00264F10`), and the first word of the row's 16-byte block
record is the block pack index (`00264F40`); the block record's second word plus 500 is the sound
map number stored at `02ADD078` (`00264FD0`, `00378030`). The row and block layouts are on the
weather page, which reads the same two tables.

## Layouts

### The pack

```struct MpkHeader base=file size=0xC0
+0x00  u32      count   32 in all 550 packs; 0036B980 rejects a count above 32
+0x04  u32[32]  size    section size per slot in slot order; 0 means the slot is absent
+0x84  u8[60]   pad     the header is padded to a multiple of 0x40
```

The header length is `((count + 1) * 4 + 0x3F) & ~0x3F`, 0xC0 for 32 slots. After it, for each slot
whose size is non-zero and in slot order, come a 0x40-byte slot (zero in the file; the loader
overwrites it with an arena block header) and the section's bytes. There are no offsets: a section's
position is the running sum, and `0036B980` refuses the pack when the sum does not equal the loaded
block's size (`0036BA30`-`0036BA45`).

| slot | magic | section | kept by | consumer |
|---|---|---|---|---|
| 0 | `SeSe` | the `SeSep` sound-effect bank | mode 0 (`02ADD080`) | `003635E0` walks it with `002DF070` and frees it |
| 1 | `WD` | a wave bank | neither mode | freed unread (`00378BC0`) |
| 4 | u32 1 | the navigation dataset | mode 1 (`02ADCFE8`, copied) | `00384160` binds it (the navigation mesh page) |
| 8 | `YM00` | world data | mode 1 (`02ADCFE0`), mode 0 (`02ADCFF0`) | `0026E760`, `0026E7D0` build the 0x240-byte world object through `002F6AB0` |
| 9 | `ACTL` | the actor-control table | both (`02ADD0B8`) | `003E8940` publishes it at `02B5D080` |
| 10 | `SPP1` | the map sound list | mode 0 (`02ADD068`) | `003635E0` keeps it at `022CBAF8` (the map sound list page) |
| 13 | `EFB0` | a map effect bank | neither mode | freed; the loose `PS2Data\efb\<zone>.efb` is loaded instead (`00377DC0`) |
| 15 | `MRP` | a menu resource package | both (`02ADD058`) | `00377B90` returns it to `initgauge` (`0034DC70`) |
| 16 | `SP1` | the sound-emitter block | both (`02ADD060`) | `003635C0` keeps it at `022CBAF0` |
| 17 | `LGT2` | the light set | both (`02ADD090`) | `0037AA90(block, 0)` |
| 24 to 27 | `TIM2` | map pictures, one per sub-location | both (`02ADD010` + 8i) | `003C63A0` uploads picture 0 |
| 28 to 31 | `NPS2` | each picture's placement | both (`02ADD030` + 8i) | `00379870` applies placement 0 |

Slots 2, 3, 5 to 7, 11, 12, 14 and 18 to 23 are never read by `00378BC0` (slot 12 is freed), and no
shipped pack fills them.

### YM00, the world data

```struct Ym00Header base=section size=0x14
+0x00  u8[4]   magic     "YM00"
+0x04  u32     stamp     an export value; not read by 002F6AB0, which starts at +0x10
+0x08  u8[8]   author    an export tag; not read by 002F6AB0
+0x10  u32     count     17 in all 461 sections; 002F6AB0 reads it at [base + 0x10]
+0x14  u32[]   index     count + 1 entries of {u24 offset in 16-byte units from +0x10, u8 tag}; the last is the end sentinel with tag 0xFF
```

`002F6AB0(object, kind)` walks the index: an entry whose offset equals the next entry's is skipped,
otherwise its tag selects an arm (`cmp eax, 0x21`, a 34-case jump table). The arms that store or
parse a chunk:

| tag | what 002F6AB0 does with the chunk |
|---|---|
| 0 | `[+0x16C]` = first dword (a count), `[+0x188]` = chunk + 0x10: the 0x40-byte placement rows `002F5550` composes |
| 1 | `[+0x170]` = count, `[+0x190]` = chunk + 0x10, `[+0x1C8]` = an allocation of `count * 4` |
| 9 | `003ED3F0(chunk)`: the three 0x180-byte environment records at `02B5ED94` |
| 11 | `0026E8C0` stores it at `0209A660`; dword 0 to `022D8ED8` unless 0xFFFFFFFF; dword 1 unpacked by `00466140` into the colour `0209A3A0`-`0209A3AC` (scaled by 1/128); dwords 2 and 3 to `0209A6EC` and `0209A6F0` |
| 12 | `00468160(chunk, [+0x150], [+0x1B8])` |
| 14, 26 | `003EC910(6, 0x20, 00467D00)` then `00467D20(buffer, chunk)`; `[+0x150]` = buffer, `00467BF0(buffer, 0)`; tag 26 also sets `[+0x230]` = 1 |
| 17, 31 | `00232380(object + 0xA8 or + 0x40, chunk)`: a six-tag sub-container into the two 0x68-byte sub-records |
| 22 | `[+0x180]` = chunk |
| 23 | `00466E70(chunk)`: the `02EBB6E0` slot family |
| 24 | `[+0x220]` = count, `[+0x198]` = chunk + 0x10, `[+0x1D0]` = an allocation of `count * 0xE0` |
| 25 | `003ED190(chunk)`: field-dependent environment setup |
| 27 | `003ED840(chunk)` |
| 28, 29, 32 | `[+0x1A8]`, `[+0x1B0]`, `[+0x1B8]` = chunk |
| 30 | `[+0x174]` = count, `001806F0(count)`, `[+0x178]` = chunk + 0x10: the 0x30-byte instance records |
| 33 | `002F6740(object, chunk)` |

Every shipped section carries exactly the 17 tags 0, 1, 11, 12, 17, 22 to 33 and the sentinel, so the
skipped tags 2 to 8, 10, 13, 15, 16 and 18 to 21 never occur. After the walk the constructor
allocates `count30 * 0x70` at `[+0x1C0]`, fills each entry from the tag-30 records (colour from the
record's `+0xC` or from the tag-0 row through the `+0x40` sub-record's transform, `00231A90`) and
links the records that carry bit 30 of their `+0xC` word to their tag-24 entry (`word +0x14`).

### ACTL, the actor-control table

```struct ActlHeader base=section size=0x10
+0x00  u8[4]  magic        "ACTL"
+0x04  u16    version      must be 1: 003E8940 clears the pointer otherwise
+0x06  u16    recordSize   0x16 in all 270 sections; 003E8230 and the two walkers advance by it
+0x08  u16    idBound      003E8230 refuses an id at or above it
+0x0A  u16    reserved     0
+0x0C  u16    indexOffset  0x10: the bucket index {u16 bucketCount; {u16 bound, u16 recordOffset}[bucketCount]}
+0x0E  u16    auxOffset    the aux table 003E7EC0 and 003E8D50 pass to the record handlers
```

`003E8230(id)` returns the record of an id:

- bucket = `id / 100`, slot = `id % 100`;
- a miss when the id reaches `idBound`, the bucket reaches `bucketCount` or the slot reaches the
  bucket's bound;
- a hit is `section + recordOffset[bucket] + slot * recordSize`.

`003E7EC0` and `003E8D50(mode)` walk every bucket's records in the same arithmetic and hand each to
`003E8020` or `003E8C50` with the aux table and the weather slot (`00265920`); `003E8D50` skips
records whose byte `+0x15` differs from a non-negative mode.

`003E8020` keeps the record's state in its first word: bit 0 processed (set on first touch, when the
nibbles of bytes `+0x13` and `+0x14` are swapped and `+0x12` is stamped 0x30), bit 1 the alternator,
bits 2 and 3 an override, bit 4 "was active". A first word of 0xFFFF is a tombstone that every
walker skips. The record's other fields and the handlers they drive belong to the actor-control
page.

### SP1, the sound emitters

```struct Sp1Header base=section size=0x20
+0x00  u8[4]  magic            "SP1"
+0x04  u32    listOffset       0x20 in all 456 sections: 00363B40 reads the weather-slot list here when the SPP1 list is absent
+0x08  u32    areasOffset      the listener grid 00362E50 searches
+0x0C  u32    indexOffset      {u16 bound; u16 recordOffset[]}: the emitter index 00362850 passes to 003631B0
+0x10  u32    emittersOffset   a u16 prefix list terminated by bit 15, then the emitter records
+0x14  u32    reserved14       0
+0x18  u16    reserved18       0
+0x1A  u16    reserved1A       0
+0x1C  u32    reserved1C       0
```

`003631B0(listener, list, index, current)` walks a list of index entries, resolves each through the
index into a record at `022CBAF0 + recordOffset`, dispatches on the record's shape byte `+9`
(`& 0x7F`: 0, 1, 2, other), evaluates the volume through `00361810` and starts or updates the voice
through `003638B0`. The emitter record itself is on the map sound list page.

`00363B40` builds the per-weather-slot ambient list from the `SPP1` section's `u16 +0x1A` offset
when it is non-zero, which it is in all 545 shipped lists, else from this header's `+4` list; the
current slot (`00265920`) picks the entry.

### LGT2, the light set

`0037AA90(block, group)` accepts the block when its first dword is `LGT2` (`0x3254474C`) and stores
it in group `group` (0 to 4) of the `0x50`-byte group table at `02EBF420`. It walks the chunk chain
at `block + u16[+4]` (`{u16 size, u16 kind}` chunks, kinds 0 to 3 and 5 to 7 stored to the group's
slots) and remaps a byte of each of the `u16[+0xA]` 0x70-byte records through `01EF94E4`. The
section's own format is on the section-014 page.

### TIM2 pictures and NPS2 placements

`003C63A0(picture)` registers picture 0 as a texture (`0024A480(picture, "navi_Load", 2, …, 0x200)`)
and keeps its width and height (`u16 +0x14` and `+0x16` of the texture header) at `02B457F8` and
`02B457FC`. `00379870(i)` applies placement `i`:

```struct Nps2Placement base=section size=0x40
+0x00  u8[3]   magic   "NPS"
+0x03  u8      version "2" in all 577 shipped records; 00379870 treats "1" as a 256 x 256 picture
+0x04  u8[12]  pad     zero
+0x10  f32     x       world position of the picture (00379870 -> 003C6360)
+0x14  f32     y
+0x18  f32     width   picture extent (00379870 -> 003C6380), read only for version "2"
+0x1C  f32     height
+0x20  u8[32]  pad2    zero
```

### WD and MRP, carried but unread

Slot 1 is a wave bank: a `WD` magic, `u16 +2` bank id (46 distinct values, 0x1FA to 0x251), `u32 +4`
trailing data size (its start is 0x40-aligned), `u32 +8` and `+0xC` record counts (equal in all 46),
`u32 +0x14` flags (0, 0x8000 or 0x10000), an offset table of `count` dwords at `+0x20` with a record
stride of 0x20. `00378BC0` frees the slot in both modes (`00378DBA`, `00378E19`), so nothing reads it.

Slot 15 is an `MRP` relocated-pointer package (the menu resource package page). The pointer
`02ADD058` has four references: the store (`00378F04`), the teardown (`003782EB`, `003782FC`) and the
getter `00377B90`, whose only caller is `initgauge` (`0034DC70`). That verb passes it to `003E9020`,
which passes it as a 32-bit integer to `00408300`, where it becomes the second create parameter of
the gauge task `00406E80`. Only two packs, `rwg0201` and `rwg0202`, carry the slot, with identical
bytes.

## Shipped data

| quantity | value |
|---|---|
| packs | 550; count 32 and a 0xC0 header in every one; the sizes sum to the file length in every one |
| slots used | 0 (545), 1 (46), 4 (461), 8 (461), 9 (270), 10 (545), 13 (387), 15 (2), 16 (456), 17 (212), 24 to 27 (421, 136, 32, 17), 28 to 31 (396, 133, 31, 17) |
| commonest slot sets | {0, 4, 8, 10, 13, 16, 24, 28} 113 packs; with 9 added 48; with 9 and 17 48; with 9, 17, 25, 29 47; {0, 1, 10} 46; {0, 10} 41 |
| block packs | the 89 `<area>00` packs: 46 carry {0, 1, 10}, 41 {0, 10}, 2 nothing; no other pack is sound-only |
| YM00 | 461 sections, median 2.9 MB; count 17 and the same 17 tags in every one; 441 stamps are float-shaped values between 1 and 1000 |
| ACTL | 270 sections, 64 to 1,792 bytes; version 1 and record size 0x16 in all; the index ends where the first record begins and the records end at the aux offset in all 270; 1,822 records, 101 of them tombstones |
| SP1 | 456 sections, 704 to 9,792 bytes; list offset 0x20 in all; the three regions tile areas, emitters, index in 454 (two sections have no emitter index) |
| SPP1 | 545 lists of 1 to 8 entries; the `+0x1A` list offset is non-zero in all 545 |
| TIM2 and NPS2 | one picture per section (`u16 +6` = 1); 577 placements, all version "2" |
| WD | 46 sections, all in `<area>00` packs; record stride 0x20 in the 27 with more than one record |

## Loader behaviour

### Two requests per field

`00331990(field)` requests the block pack in mode 0 and the field's own pack in mode 1 through
`00378A60(field, index, mode)`:

1. Mode 0 returns at once when `02ADD0E0` is non-negative and equals `02ADD0DC`: the block pack
   already bound is kept. Otherwise `00378230(1)` tears the previous packs down (when no load is
   pending, `0032F3D0(0)`) and `003784A0` releases the sound sections.
2. Mode 1 drops the minimap texture (`003C63A0(0)`), stores the index at `02ADD0DC` and tears down
   with `00378230(keep)`, keeping the mode-1 world object only when the same index is loaded again
   with `02ADD0EA` clear.
3. When no load is pending, `00377DC0` requests the loose effect bank `PS2Data\efb\<zone>.efb`
   (completions `003788F0` in mode 1 to `02ADD050`, `003789A0` in mode 0 to `02ADD098`, bind bits
   5 and 6) and `00378030` requests the pack: `0032E400(4, index)` sizes it, `0036A190` allocates an
   arena block tagged `MapNo`, and `0032E620` submits the load with the completion `00378BC0` and the
   argument `block | mode`.
4. Mode 1 names the scene from the pack's path (`00379A10(4, index)`, with five alias pairs at
   `01EF9490`), which `001805D0` receives.

The debug verb `mapload` (0x2001, `0050D4D0`) requests one pack in mode 1 with field 0.

### The split

`00378BC0` first calls `0036B970(block, slots, 32)`, which is `0036B980`:

1. A count above 32 returns 0 (`0036B9BB`).
2. The header length plus the sum of every non-zero size plus 0x40 must equal the arena block's own
   size, and the arena must have a free handle per extra section (`0036BA78`-`0036BAA2`); otherwise
   0 is returned and nothing is split.
3. Each non-zero section's 0x40 slot is overwritten with a copy of the arena block header (owner
   bytes, size `+0x18`, tag) and registered as a block of its own; a zero size yields a null slot.

### The dispatch

With the 32 slot pointers, `00378BC0` keeps or frees each section and marks the kept ones in the
pending word `02ADD0EC` and the bind word `02ADD0F0`:

| slots | mode 1 (the field's own pack) | mode 0 (the block pack) |
|---|---|---|
| 24 to 27, 28 to 31 | stored at `02ADD010 + 8i` and `02ADD030 + 8i`, bits 9 + i and 13 + i | the same |
| 4 | copied into a block tagged `IdMapNo` at `02ADCFE8`, the original freed | neither stored nor freed |
| 8 | `02ADCFE0`, bit 3 | `02ADCFF0`, bit 3 |
| 0, 10 | freed | `02ADD080` and `02ADD068`, bit 0 |
| 1 | freed | stored at `02ADD070` and freed at once |
| 12, 13 | freed | freed |
| 16 | `02ADD060`, bit 7 | the same |
| 17 | `02ADD090`, bit 8 | the same |
| 9 | `02ADD0B8`, bit 4 | the same |
| 15 | `02ADD058`, bit 18 | the same |

It then clears pending bits 0 to 18 one by one and, when the pending word is empty, calls the binder
`003775D0`; `00214B70` ends the completion.

### The bind

`003775D0` consumes the bind word: bit 7 stores the `SP1` block at `022CBAF0` (`003635C0`); bit 0
walks the `SeSep` bank with `002DF070`, frees it and keeps the `SPP1` list at `022CBAF8` with the
sound map number (`003635E0`); bit 4 publishes the `ACTL` block (`003E8940`, cleared again when its
version is not 1); bit 8 binds the lights (`0037AA90(block, 0)`) and refreshes with `003DE920(0, 1)`;
bit 3 runs `00378120`, which:

1. makes the mode-1 `YM00` current (`02ADCFF8`) and uploads picture 0 (`003C63A0`) and placement 0
   (`00379870`);
2. hands the mode-0 `YM00` to `0026E7D0` (its object at `0209A668`, the pack pointer kept at
   `02ADD000`) and the mode-1 one to `0026E760` (its object at `0209A670`), both built by
   `002F6AB0` from a 0x240-byte allocation;
3. binds the navigation copy (`02ADD008`, `00384160`) and copies the current environment record to
   `02ADD10C`-`02ADD114`;
4. applies the world object's tag-11 colour (`003AFD40`) and calls `00332130(0)`.

The teardown `00378230(releaseWorld)` frees every stored section, unbinds the lights
(`0037AA50(0)`), the `ACTL` (`003E8940(0)`) and the navigation data (`00384160(0)`), drops the
pictures and placements and resets the ambient colour; `003784A0` frees the block pack's world
object, the loose effect bank and the two sound sections.

## Modding notes

- A pack is valid when its 32 sizes plus the 0xC0 header and one 0x40 slot per present section add
  up to the file length; the loader checks nothing else about the container.
- A section placed in an unused slot (2, 3, 5 to 7, 11, 14, 18 to 23) stays allocated with no owner;
  slot 13 is always freed, so an edited embedded effect bank changes nothing and the loose `.efb` is
  the file to edit.
- A field's `YM00`, navigation, pictures and lights come from its own pack; its sound bank and map
  sound list come from the block pack, so two fields of one block share them.
- `YM00` must carry its 17 chunks in the tag order the index gives; the parser accepts any order but
  skips a chunk whose offset equals the next one's.
- An `ACTL` with a version other than 1 is dropped silently at bind.

## Related

- [Weather: the three weather slots of an area, the change roll on entering, the setweatherslot verb, the MWeather table, what the slot does to the sky, the map and combat, and the environment variant it selects](weather.md)
- [Zone changes: mapjump and the other jump verbs, the loading flags, the moment the new zone is ready and what names a map](zone-changes-and-mapjump.md)
- [Doors, gates and map changes: the override table the setmapid verbs write, what its floor, wall and mj bits block, the show and hide model masks and when a new map clears them](doors-gates-and-map-changes.md)
- [How a unit finds its way across the navigation mesh](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)
- [The map sound list](../Sound-And-Music/map-sounds.md)
- [The menu-map container](../Game-Files-And-Data-Tables/menu-map-files.md)
- [section_014, the LGT2 light set](../EBP-Script-Files/ebp-lighting-lgt2.md)
- The EFX and EFB effect containers
- [MRP menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md)
