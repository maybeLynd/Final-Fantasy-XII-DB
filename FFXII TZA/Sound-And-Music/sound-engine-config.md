---
title: "Sound engine configuration: the start-up file that sets the sound categories, the master bus, the macros and the effect presets"
kind: "format"
category: "Sound and music"
addresses: "0x00210760, 0x007A4D50, 0x007B0F90, 0x007AE410, 0x007ADB20, 0x007AC4F0, 0x007B31A0, 0x007ACD30, 0x007AAA40, 0x007AA110, 0x007AC360, 0x007B1210"
---

## What the player sees

- Music, sound effects and voices are mixed as separate categories, each with its own number of sounds that can play
  at once.
- The file changes nothing during play; it is read once when the game starts.

## Where it comes from

The file is `ps2data/sound/sead.win.config`, 1,264 bytes, the only `.config` file the game ships.

### Loading

`0x00210760` builds the path from `PS2Data/sound/sead` (`0x009068E0`) and `.win.config` (`0x00906A38`) at `0x002107A0`. It runs
once at start-up, reached from `0x0017CEB0` through `0x0017D6B0` and `0x001DBA40`.

1. It opens the file (`0x002107C0`); when that fails it returns without starting the sound engine, with the value 1
   (`0x002107CD`).
2. It takes the size from the file layer (`0x002107E8`), not from the header, allocates that plus one byte
   (`0x002107F2`), ends the buffer with a 0 byte (`0x00210803`), reads the file (`0x00210807`) and closes it
   (`0x0021080F`).
3. It fills an initialisation block with the buffer at `+0x38` and calls the engine start `0x007A4D50` (`0x00210889`),
   whose result it does not test.
4. It builds the object manager with `0x002216B0(0x400, 0x400)` (`0x00210895`; [Audio manager](audio-manager.md)),
   starts the spatial layer `0x007A5B50` from a second block (`0x002108AD`-`0x002108DE`;
   [Spatial sound](spatial-sound.md)) and sets the `Lay` handle at its argument's `+0x34` to 0 (`0x007A5B20`,
   `0x002108E9`).
5. It frees its buffer (`0x002108F1`) and returns 0 (`0x002108FE`).

### The engine's copy

`0x007A4D50` calls `0x007B0F90` (`0x007A4E79`):

1. `0x007AE410` checks the magic `scnf` (`0x007B0FA8`); a mismatch makes the engine start return -1.
2. It allocates the header's `+0x0C` bytes and copies that many bytes of the file to the block it keeps at `0x02EAD3E0`
   (`0x007B0FE8`-`0x007B1005`).
3. It sums the positive category sizes into `0x02EAD3E8` (`0x007B103C`-`0x007B108A`) and builds the external-parameter
   rows (`0x007B10B4`-`0x007B1145`); without an `expr` chunk it builds no rows (`0x007B10C0`).
4. It returns 0 (`0x007B11E5`), and -1 only for the magic mismatch (`0x007B0FB8`).

All 16 later reads of `0x02EAD3E0`, in 15 functions, pass it to a chunk finder, so every chunk is read from the copy.

### What the engine builds from the copy

The start `0x007A4D50` builds these objects from the copy; they keep pointers into it for names and elements rather
than copying them:

| Object | Size | Kept at | Built by | Filled from |
|---|---:|---|---|---|
| the copy | `copySize` | `0x02EAD3E0` | `0x007B0F90` | the whole file |
| sum of the positive category sizes | `i32` | `0x02EAD3E8` | `0x007B0F90` (`0x007B1047`-`0x007B108A`) | `ctgr` sizes |
| category table, one pointer per element | 8 × count | `0x02EAD008`, count `0x02EAD000` | `0x007AAA40` (`0x007AAA60`-`0x007AAAA2`) | `ctgr` count |
| `Driver::Category` | `0x88` | a slot of the category table | `0x007AAA40`, `0x007A96F0`, `0x007AA110` | a `ctgr` element, the `ctgl` count |
| a category's volume and pitch ramps | 8 + `0x30` × n | category `+0x38`, `+0x40` | `0x007AA110` | the `ctgl` count |
| a category's handle-list nodes | 8 + `0x28` × size | category `+0x18` | `0x007AA010` | the category size |
| bus table, one pointer per bus | 8 × count | `Driver::Audio` `+0x08`, count `+0x10` | `0x007AC4F0` (`0x007AC55D`-`0x007AC59D`) | `bus ` count |
| bus | `0x128` | a slot of the bus table | `0x007AC4F0` | a `bus ` element |
| effect | by type | bus `+0x10` to `+0x28` | `0x007AC4F0` | an effect record's type byte |
| external-parameter row | `0x40` | `0x02EAD3F8`, count `0x02EAD3EC` | `0x007B0F90` | an `expr` element |
| `EventData` | `0x38` | table `0x02EAD760`, count `0x02EAD754` | `0x007B67E0` | an `evt ` element |
| start parameters | `0x20` | the stack of `0x007A4D50` | `0x007A4D50` | `hcam` |

Each table, ramp array and node array is a block of the engine's allocators: the tables from `0x007AD550`, which puts
a 16-byte header before the block, and the arrays from `0x007AD460`, with an 8-byte element count before the first
element (`0x007AA1A5`, `0x007AA0AB`).

`mcr `, `epsp`, `eps ` and `curv` build nothing. `mcr ` is read where it lies each time a macro runs (`0x007B31A0`),
`epsp` and `eps ` each time a preset is applied (`0x007ACD30`, `0x007AD240`), and `curv` by the curve binders.

## Layouts

All multi-byte fields are little-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "scnf" |
| `+0x04` | `u16` | h04 | 0 |
| `+0x06` | `u16` | dirOffset | `0x10` |
| `+0x08` | `u8` | chunkCount | 10 |
| `+0x09` | `u8[3]` | h09 | 0 |
| `+0x0C` | `u32` | copySize | bytes the engine copies; 1,264 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | tag | the chunk's tag |
| `+0x04` | `u16` | e04 | 0 |
| `+0x06` | `u16` | e06 | `0x10` |
| `+0x08` | `u32` | offset | from the start of the file |
| `+0x0C` | `u32` | e0C | 0 |

Each finder walks `chunkCount` entries from `dirOffset` and compares the tag with its entry in the tag table at
`0x01CB4928` (`0x007ADB5A`); a tag not there gives a null chunk.

| File field | Becomes |
|---|---|
| magic | compared with "scnf" (`0x007AE410`) |
| `copySize` | the size of the engine's block and the number of bytes copied into it (`0x007B0FE8`-`0x007B1005`) |
| `dirOffset`, `chunkCount` | read from the copy by every finder on every call (`0x007ADB2A`, `0x007ADB2F`) |
| entry tag | compared in place with the finder's tag (`0x007ADB5A`) |
| entry offset | relocated on every call: the finder returns the copy's address plus the offset (`0x007ADB86`-`0x007ADB92`); no object keeps the chunk pointer |
| `h04`, `h09`, `e04`, `e06`, `e0C` | not read (see Loader behaviour) |

A table chunk starts with a `u8` version, a `u16` at
`+0x02` that locates its element-offset table and a `u16` element count at `+0x04`.

| Tag | Class | Finder | Read by |
|---|---|---|---|
| `ctgr` | `CategoryChunk` | `0x007ADB20` | `0x007A4D50`, `0x007B0F90` |
| `ctgl` | `CategoryLayerChunk` | `0x007ADBB0` | `0x007A4D50` |
| `bus ` | `BusChunk` | `0x007AD9A0` | `0x007AC4F0`, `0x007ACD30` |
| `mcr ` | `MacroChunk` | `0x007AE1D0` | `0x007B31A0` |
| `evt ` | `EventChunk` | `0x007ADF90` | `0x007A4D50` |
| `epsp` | `EffectPresetPackChunk` | `0x007ADE80` | `0x007ACD30` |
| `eps ` | `EffectPresetChunk` | `0x007ADD30` | `0x007AD240` |
| `curv` | `CurveChunk` | `0x007ADCA0` | nine curve binders, such as `0x007BDFA0` |
| `expr` | `ExternalParameterChunk` | `0x007AE080` | `0x007B0F90` |
| `hcam` | `HCAMXSettings` | `0x007AE110` | `0x007A4D50` |

The class names are the run-time type names of each chunk's wrapper.

### Categories

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | version | 2 |
| `+0x01` | `u8` | c01 | the element index |
| `+0x02` | `u16` | nameAt | offset of the name, `0x10` |
| `+0x04` | `i16` | size | 0 no slots; above 0 that many sound slots; below 0 shares category -size |
| `+0x06` | `u16` | c06 | the name length |
| `+0x10` | `char` | name | the category name, inline, `+0x06` characters long |

`0x007AAA40` refuses a chunk with no elements (`0x007AAA66`). A size of 0 builds no category: its slot in the table is
null (`0x007AAB11`, `0x007AAB6C`-`0x007AAB73`). A positive size allocates that many slots (`0x007AA2E3`), and a negative one
binds it to another category (`0x007AABD1`, `0x007AA342`). The name goes to the category object's `+0x70` (`0x007AA137`-`0x007AA156`). `ctgl` gives only
its element count: each category gets that many plus one volume ramps (`0x007AAAB2`, `0x007AA15A`).

`0x007ADAB0(chunk, out, i)` gives category element `i`. With `C` the chunk and `B = C + u16[C + 0x02]`:

```python
C[0] >= 1:  element i = C + u32[B + 4 * i]  # 0x007ADAB8-0x007ADAD2
C[0] == 0:  element i = B + 0x20 * i  # 0x007ADAE4-0x007ADAF3
```

The shipped `ctgr` has version 1, `B = C + 0x10` and the offsets `0x20`, `0x40`, `0x60` and `0x80`. `0x007AAA40`
builds one `0x88`-byte `Driver::Category` per element (`0x007A96F0`; `0x007A9760` destroys one) and keeps the pointers at
`0x02EAD008`. `0x007AA010` gives each category a handle list with as many nodes as its size.

| File field | Becomes |
|---|---|
| chunk `+0x00` version | picks how element `i` is found, on every call of `0x007ADAB0` |
| chunk `+0x02`, element offsets | relocated on every call of `0x007ADAB0` (`0x007ADAB8`-`0x007ADAD2`) |
| chunk `+0x04` count | copied to `0x02EAD000` (`0x007AAA60`), the length of the category table |
| element `version` | picks where the name is: from 2 at `nameAt`, at 1 at `+0x10`, at 0 no name (`0x007AA137`-`0x007AA14F`) |
| `nameAt` | relocated: the element's address plus `nameAt` is stored at category `+0x70` (`0x007AA13E`-`0x007AA156`) |
| `size` above 0 | the handle-list capacity, category `+0x10` (`0x007AA2EC`-`0x007AA2F3`, stored at `0x007AA075`), and added to `0x02EAD3E8` (`0x007B108A`) |
| `size` 0 | no category; a null table slot (`0x007AAB6C`-`0x007AAB73`) |
| `size` below 0 | negated and looked up: category `-size` is stored at `+0x58` (`0x007AA342`-`0x007AA356`); no handle list |
| `name` | read in place through category `+0x70` |
| `c01`, `c06` | not read by `0x007AAA40`, `0x007AA110`, `0x007AA320` or `0x007B0F90` |
| `ctgl` chunk `+0x04` count | plus one, the number of volume ramps, category `+0x78` (`0x007AAAB2`, `0x007AA15A`-`0x007AA165`); a missing `ctgl` counts as 1 (`0x007AAAB9`) |

#### The category object

`0x007AAA40` allocates `0x88` bytes (`0x007AAB18`-`0x007AAB23`), clears them (`0x007AAB3B`), runs the constructor `0x007A96F0`
and stores the pointer in the table (`0x007AAB61`); `0x007AA110(category, index, element, ctgl count)` then fills it from
the element. When the allocation `0x007AD460` gives null, the slot gets 0 and `0x007AA110` is still called with it
(`0x007AAB4D`, `0x007AAB65`).

| Offset | Type | Name | Meaning | Set by |
|---|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CB4490` | `0x007A96F7` |
| `+0x08` | `void*` | listVtable | the handle list's vtable `0x01CB4480`; the list is `+0x08`-`+0x37` | `0x007A9701` |
| `+0x10` | `i32` | capacity | the category size, the most sounds it holds; 0 for a size below 0 | `0x007AA075` |
| `+0x14` | `i32` | inUse | sounds in the list | 0 at `0x007AA061`, `0x007B6AF5` |
| `+0x18` | `void*` | nodes | the node array, `size` nodes of `0x28` bytes | `0x007AA0E5` |
| `+0x20` | `void*` | firstFree | the first free node | `0x007B6AAA` |
| `+0x28` | `void*` | oldest | the first node in use, the oldest sound | `0x007B6AEB` |
| `+0x30` | `void*` | newest | the last node in use | `0x007B6AF1` |
| `+0x38` | `void*` | volumeRamps | the volume ramps | `0x007AA1E7` |
| `+0x40` | `void*` | pitchRamps | the pitch ramps | `0x007AA2A6` |
| `+0x48` | `f32` | masterVolume | 1.0, then the master volume ramp's value | `0x007A9743`; `0x007AA540` |
| `+0x4C` | `f32` | masterPitch | 1.0, then the master pitch ramp's value | `0x007A974A`; `0x007AA530` |
| `+0x50` | `u8` | volumeChanged | 1 when `+0x48` was written, cleared by the pass `0x007AA770` | `0x007AA547`; `0x007AA7A5` |
| `+0x51` | `u8` | pitchChanged | 1 when `+0x4C` was written, cleared by `0x007AA770` | `0x007AA537`; `0x007AA80D` |
| `+0x52` | `u8[6]` | | zeroed by the clear; no access in the category code | `0x007AAB3B` (0) |
| `+0x58` | `void*` | shared | the category a negative size shares | `0x007AA356` |
| `+0x60` | `i32` | index | the element's index | `0x007AA128` |
| `+0x64` | `i32` | pauseCount | the category's pause count | `0x007AA680`, `0x007AA3E0` |
| `+0x68` | `f32` | pauseFade | the fade of the pause that started the count, counted down by each pass and handed to a sound added while paused | `0x007AA74B`; `0x007AA865`-`0x007AA87B` |
| `+0x6C` | `u8[4]` | | zeroed by the clear; no access in the category code | `0x007AAB3B` (0) |
| `+0x70` | `void*` | name | the category name in the copy | `0x007AA156` |
| `+0x78` | `i32` | volumeRampCount | the `ctgl` count plus one | `0x007AA165` |
| `+0x7C` | `i32` | pitchRampCount | 2 | `0x007AA15E` |
| `+0x80` | `u8[4]` | commandBytes | two byte pairs that the driver's commands `0x07` and `0x08` store: `0x007AA4E0` stores `+0x80` and `+0x81`, `0x007AA4D0` stores `+0x82` and `+0x83`, both called from `0x007AB5C0` (`0x007AB78C`, `0x007AB7B3`); no read in the category code | `0x007A973A` (0); `0x007AA4E0`; `0x007AA4D0` |
| `+0x84` | `u8[4]` | | zeroed by the clear; no access in the category code | `0x007AAB3B` (0) |

The constructor zeroes `+0x10`-`+0x47`, `+0x50`-`+0x51`, `+0x58`-`+0x6B` and `+0x70`-`+0x83` (`0x007A9705`-`0x007A973A`).

A category's bytes `+0x52`-`+0x57` and `+0x6C`-`+0x6F` are written only by the `0x88`-byte clear in `0x007AAA40`
(`0x007AAB3B`) before `0x007A96F0` runs, and read by no instruction; nothing fixes their width.

A handle-list node holds its vtable `0x01CB4530` at `+0x00`, the previous node at `+0x08`, the next at `+0x10`, its slot
number at `+0x18` (-1 when built, `0x007AA0CC`; renumbered by `0x007B6AC4`), a word whose bit `0x1` marks it in use at `+0x1C`
and the sound's handle at `+0x20` (`0x007BBA76`, `0x007BBA7B`). `0x007B6AA0` links the array into the free chain.

Each ramp is an `AudioParameterRamp` of `0x30` bytes; `0x007AA110` builds the two arrays (`0x007AA16B`-`0x007AA2DD`):

| Offset | Type | Name | As built |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CB44A0` (`0x007AA1C0`) |
| `+0x08` | `f32` | start | 0 |
| `+0x0C` | `f32` | target | 1.0 (`0x007AA20F`, `0x007AA2BC`) |
| `+0x10` | `f32` | elapsed | 0 |
| `+0x14` | `f32` | duration | 0, so the value is the target |
| `+0x18` | `u8[4]` | | not written |
| `+0x1C` | `i32` | curve | 0 |
| `+0x20` | `u8` | active | 0 |
| `+0x21` | `u8[3]` | | not written |
| `+0x24` | `u32` | limited | 0 |
| `+0x28` | `f32` | riseRate | not written by the builder; the category code starts its ramps only through `0x007CA560` (from `0x007AA4F0`, `0x007AA510`, `0x007AA550`, `0x007AA570`), which reads `+0x28` and `+0x2C` only when `+0x24` is 1 (`0x007CA5D2`), and nothing in the category code writes `+0x24` |
| `+0x2C` | `f32` | fallRate | not written by the builder; read under the same `+0x24` test |

The volume ramps number `+0x78`, the pitch ramps 2. Each array comes from `0x007AD460`, or from `0x00210EC0` with 8
bytes for a count of 0 (`0x007AA173`, `0x007AA23D`). A null block leaves the array pointer 0 (`0x007AA1E1`, `0x007AA2A1`),
and the fill loops that follow still run (`0x007AA1EB`, `0x007AA2AA`). `0x007AA110` then gives a category whose `size` is
above 0 its handle list, `0x007AA010` with the category's `+0x08` and the size (`0x007AA2E3`-`0x007AA2F3`), and returns
0 (`0x007AA2FD`).

The binding is `0x007AA320(category, element)`, called by `0x007AAA40` (`0x007AABED`) after every category is built. That
second walk over the elements calls it only for an element whose size, negated as a 16-bit number, is above 0
(`0x007AABD1`-`0x007AABDB`). For an element whose `i16` size (`+4` of the element data the argument's `+8` points to)
is negative it looks up category `-size` (`0x007AAA20`: an index below the count `0x02EAD000`, else 0) and keeps it at
the category's `+0x58`.

When the capacity `+0x10` of that category is 0, as it is for a category whose own size is below 0, it prints
"[sead][!!error!!]Category::InitializeRefCategory referenced category is not initialized( or reference is looping )!"
and returns -1. That ends `0x007AAA40` at once with -1 (`0x007AABF4`), before the master ramps are set, and the start
takes it as a failure (`0x007A50F0`). Otherwise, and for a size of 0 or more, it returns 0. When both walks finish,
`0x007AAA40` sets the master ramps and returns 0 (`0x007AAC09`-`0x007AAC43`, `0x007AAC10`).

### How a category limits its sounds

`0x007A9A10(category, handle)` adds a starting sound, music or instrument to its category, or to the one a negative size
shares (`+0x58`):

1. While the list is full, it walks it from its oldest entry and finds the one with the lowest priority, slot 25 of the
   object, which for a sound is byte `+0x07` of its sound record (`0x007BD980`).
2. When the new object's priority is lower than that one's, it refuses the new one (returns 1).
3. Otherwise it stops the lowest one at once (slot 2, no fade) and takes it out of the list; an entry with no object
   prints "list remove invalid iterator".
4. It gives the new object the category's volume (`0x007A9F40`, slot 5) and pitch (`0x007A9D30`, slot 6), pauses it when
   the category's pause count `+0x64` is above 0, and appends its handle at the newest end (`0x007BB9A0`).

`0x007A9F40` multiplies the category's volume ramps `+0x38` and its master volume `+0x48`; `0x007A9D30` multiplies its
pitch ramps `+0x40` and its master pitch `+0x4C`. Each driver pass `0x007AAEA0` advances the master volume ramp
`0x01F403E0` (type 5, `0x007AAD90`) and the master pitch ramp `0x01F40410` (type 6, `0x007AAC80`) and stores them into every
category (`0x007AA540` at `+0x48`, `0x007AA530` at `+0x4C`). `0x007AA550` sets a pitch ramp (type 4), and `0x007AA510`, run by
a macro, the first volume ramp.

### The bus

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | version | 2 |
| `+0x01` | `u8` | busIndex | 0 is the root bus |
| `+0x02` | `u16` | nameAt | `0x20` |
| `+0x04` | `i8` | send0 | a bus to send to, or -1 |
| `+0x05` | `u8` | effectCount | effects on the bus |
| `+0x06` | `u8[4]` | sendTargets | more send buses |
| `+0x0A` | `u8` | sendCount | how many of them |
| `+0x0B` | `u8` | nameLength | places the effect table |
| `+0x0C` | `f32` | level | the root bus's volume; for another bus, the level of `send0` |
| `+0x10` | `f32[4]` | sendLevels | one per send target |
| `+0x20` | `char` | name | the bus name, inline, `+0x0B` characters long |

`0x007AC4F0` builds the buses: `+0x01` picks the slot (`0x007AC770`), the root bus takes `+0x0C` as its level
(`0x007ACAAE`, `0x007ACAE0`), and other buses read their sends (`0x007AC7AD`-`0x007AC822`) and effects (`0x007AC83A`). The
effect table is at `nameAt + ((nameLength + 0x10) & 0xF0)` (`0x007ADA3F`), and an effect's type byte `+0x01` picks its
class through the jump table at `0x007ACCF0` (`0x007AC883`).

`0x007AD950(chunk, out, i)` gives bus element `i` by the same rule, with `B = C + u16[C + 0x02]`:

```python
C[0] >= 1:  element i = C + u32[B + 4 * i]  # 0x007AD962, 0x007AD981-0x007AD98B
C[0] == 0:  element i = B + 0x20 * i  # 0x007AD968-0x007AD96C
```

The shipped `bus ` has version 2, `B = C + 0x10` and one offset, `0x20`.

| File field | Becomes |
|---|---|
| chunk `+0x00` version | picks how element `i` is found (`0x007AD950`); below 1 the engine adds a bus 0 of its own before the elements, with level 1.0 and no effects (`0x007AC569`-`0x007AC570`, `0x007AC6D9`-`0x007AC6FE`) |
| chunk `+0x04` count | added to the mixer's bus count `+0x10` (`0x007AC55D`-`0x007AC565`), which sizes the bus table; also handed to the voice set-up `0x007AEF30` (`0x007AC69F`, `0x007AC6B9`) |
| element `version` | where the name is: from 2 at `nameAt`, at 1 at `+0x20`, at 0 no name (`0x007AC77B`-`0x007AC798`); where the effect table is: from 2 as above, below 2 at the `u16` `+0x02` itself (`0x007ADA34`-`0x007ADA55`) |
| `busIndex` | the bus-table slot the element fills (`0x007AC770`-`0x007AC774`); 0 takes the root path (`0x007ACAA9`) |
| `nameAt` | relocated: the element's address plus `nameAt` is stored at bus `+0x30` (`0x007AC787`-`0x007AC79B`) |
| `send0` | 0 or above: the first send, to the voice of bus `send0` (`0x007AC7AD`-`0x007AC7D3`); below 0, no first send |
| `effectCount` | the number of effect records built (`0x007AC83A`, `0x007ACA83`) |
| `sendTargets` | each the bus whose voice is a further send (`0x007AC800`-`0x007AC81E`) |
| `sendCount` | the number of `sendTargets` read (`0x007AC7E4`, `0x007AC82A`) |
| `nameLength` | places the effect table (`0x007ADA3F`) |
| `level` | root bus: its voice's level (`0x007ACAAE`) and ramp 0's target (`0x007ACAE0`-`0x007ACAEC`); another bus: the level of `send0` (`0x007AC7D7`), ramp 0's target |
| `sendLevels` | the level of each further send (`0x007AC822`), the target of the next ramp (`0x007ACB50`-`0x007ACC1F`) |
| `name` | read in place through bus `+0x30` |
| effect record `+0x01` type | the class built, through the jump table `0x007ACCF0` (`0x007AC883`-`0x007AC89B`); the bus build reads no other byte of the record |

The root bus reads no sends (`0x007AC7A4`). A send takes the voice the target bus has at that moment (`0x007AC7CC`,
`0x007AC81A`), and a bus's voice is 0 until its own element has been built (`0x007AC636`). The voice of a bus with sends
is made by `0x007AEC10`:

1. It receives the send list the builder gathered on its stack (`0x007ACB16`), the send count (`0x007ACB13`) and the
   level list (`0x007ACB0F`).
2. It takes a voice from the pool `0x02EAD250` (`0x007AEC43`-`0x007AEC5C`; 0 when the pool is empty, `0x007AEC61`).
3. `0x007E0130` fills the voice: the level list goes to `+0x90` (`0x007E0153`-`0x007E0173`) and the send list to
   `+0x28`, sixteen bytes per send (`0x007E0184`-`0x007E01A2`), with no test of any entry.

A send to a bus whose element comes later is therefore copied in as a null voice.

#### The bus object

`0x007AC4F0` allocates `0x128` bytes for every slot of the bus table before it reads any element (`0x007AC5C0`-`0x007AC5CC`),
clears them (`0x007AC5E4`) and stores the pointers (`0x007AC62A`):

| Offset | Type | Name | Meaning | Set by |
|---|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CB4700` | `0x007AC5EE` |
| `+0x08` | `void*` | voice | the bus's mix voice: the root's from `0x007AE930`, another's from `0x007AEC10`, which gets this field's address (`0x007ACB06`-`0x007ACB1A`); 0 until the element is built | `0x007AC636`; `0x007ACAD8` |
| `+0x10` | `void*[4]` | effects | the built effects in record order; slots past the last stay 0 | `0x007AC642`-`0x007AC66A`; `0x007ACA67` |
| `+0x30` | `void*` | name | the bus name in the copy | `0x007AC79B` |
| `+0x38` | `AudioParameterRamp[5]` | levels | ramp k is the level of output k: the root bus's own level, or `send0` (when present) and then each send target in order; each ramp has vtable `0x01CB44A0` and is cleared (`0x007AC600`-`0x007AC61C`), and a level ramp gets start 0, target the level, duration 0, curve 0, not active, not limited | `0x007ACAEC`-`0x007ACAFE`; `0x007ACB50`-`0x007ACC1F` |

An effect takes only its type from the file. `0x007AC4F0` sets its byte `+0x10` to 1 (`0x007ACA70`) and hands its interface
`+0x08` to the bus voice; its settings come from `eps ` when a preset is applied: `0x007AD240` finds the effect's block in
the copy (`0x007ADDC0`) and hands its address to the effect's slot `+0x30` (`0x007AD2E9`). Effect classes:
[Audio effects](audio-effects.md).

The mixer, `Driver::Audio`, `0x20` bytes at `0x02EAD0A8`, built by `0x007AC360`:

| Offset | Type | Name | Meaning | Set by |
|---|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CB4710` | `0x007AC38F` |
| `+0x08` | `void*` | buses | the bus table | `0x007AC59D` |
| `+0x10` | `i32` | busCount | 0, then the `bus ` count, plus 1 for a version-0 chunk | `0x007AC398`; `0x007AC565`, `0x007AC570` |
| `+0x14` | `i32` | preset | -1, then the preset last applied | `0x007AC39B`; `0x007AD196` |
| `+0x18` | `void*` | port2 | master port 2's voice, built when byte `+0x50` of the start block is set | `0x007AC3A2`; `0x007ACC61` |

`0x007AC410(mixer, bus)` gives a bus's voice; a bus number below 0 or past the count prints "bus access overrun! use
master bus" and gives bus 0's. `0x007AC4D0(mixer, port)` gives a master port: 1 is bus 0's voice and 2 the voice at
mixer `+0x18`. The mixer object, `Driver::Audio`, is built once at `0x02EAD0A8` (`0x007AC360`).

`0x007AC360` returns 0 at once when `0x02EAD0A8` is already set (`0x007AC364`). Otherwise it takes `0x20` bytes from
`0x007AD460` (`0x007AC378`), writes the fields above, stores the object and returns 0 (`0x007AC3A6`, `0x007AC3AD`); when
the allocation gives null it stores 0 at `0x02EAD0A8` and returns -1 (`0x007AC3B4`-`0x007AC3BB`).

| Type | Effect class | Builder | Size |
|---:|---|---|---:|
| 0 | `EmptyEffect` | `0x007AC4F0` itself (`0x007AC89D`-`0x007AC8CE`) | `0x18` |
| 1 | `SurroundReverb` | `0x007D2150` | `0x1230` |
| 2 | `Compressor` | `0x007D85E0` | `0x170` |
| 3 | `Filter` | `0x007D0AC0` | `0x170` |
| 4 | `SideChainInput` | `0x007D80E0` | `0x60` |
| 5 | `SimpleFilter` | `0x007D9530` | `0x80` |
| 6 | `Flanger` | `0x007D99E0` | `0x10140` |
| 7 | `GranularPitchShift` | `0x007DA0A0` | `0x708A0` |
| 8 | `HilbertFilter` | `0x007DAAB0` | `0x178` |
| 10 | `BuildReverb` | `0x007DAFF0` | `0x610` |

Each builder installs its class's vtable and zeroes its ramps; `0x007AC4F0` allocates the size and calls it for its type
(`0x007AC89D`-`0x007ACA48`). Type 9 and types above 10 build nothing and take no effect slot (`0x007AC88A`, the table's
entry 9 `0x007ACA78`).

### Macros

`0x007B31A0` runs macro number N, from the sound's own record (`0x007B3201`-`0x007B3226`), when N is below the chunk's count
(`0x007B3269`). N is byte `+0x0A`, `+0x0B` or `+0x4F` of the record for the call's second argument 0, 1 or 3, `+0x4F`
only from record version `0x0E`. A macro record's `u16` at `+0x02` is the offset of its instruction stream
(`0x007B32D0`). Each instruction has a header length at `+0x01`, an opcode at `+0x02` and a payload length at `+0x03`
(`0x007B42CF`, `0x007B33B6`, `0x007B42E4`).

The macro runs as this loop, from the stream's first instruction:

```python
offset = 0, result = 0, running = 1  # 0x007B338E-0x007B339B
repeat:
    instr = stream + offset  # 0x007B33B0-0x007B33B3
    run the handler of opcode instr[+0x02]  # 0x007B33B6-0x007B33DD
    offset = offset + instr[+0x01] + instr[+0x03]  # 0x007B42CF-0x007B42F9
while running  # 0x007B42EF-0x007B42FD
return result  # 0x007B42CB, 0x007B430C
```

- Opcode `0x01` alone clears `running` (`0x007B33DF`), and its own lengths are still added before the loop ends. The
  loop has no other exit and never compares `offset` with the stream's end, so a stream without `0x01` runs on into
  the bytes after it.
- `0xA1`, and `0xA0` when it refuses the new sound, set `result` to 4 and go on to the next instruction
  (`0x007B3F4B`-`0x007B3F54`, `0x007B3E3B`-`0x007B3E44`, `0x007B3EDB`-`0x007B3EE4`); nothing sets it back, so a macro that
  refuses once returns 4.
- An instruction whose two lengths add up to 0 runs again at the same offset on every pass: unless it is `0x01`, the
  macro never ends, as nothing counts the passes.
- Before the loop, the macro returns 0 for a sound waiting for its bank (slot 38, `0x007B31C9`-`0x007B31D5`) and for
  N = 0 (`0x007B322C`), and -1 for N at or above the count (`0x007B326F`).

The jump table `0x007B4374`, indexed through the bytes at `0x007B43D0` by opcode - 1 (`0x007B33B6`-`0x007B33DD`),
gives 22 opcodes a handler; every other opcode, 0 and those above `0xAB` included, is skipped (`0x007B42CB`). An action
reads a test code `+0x04`, a count `+0x05`, a selector `+0x06` and two `f32` values `+0x08` and `+0x0C`.

A filter reads a test code `+0x04`, a mode `+0x05` and a value `+0x08`, a `u32` for `0x11`-`0x15` and an `f32` for
`0x16`-`0x18`. It walks the selection from its first sound (`0x02EAD590`): a sound that fails the test is taken out of
the selection (`0x007B2880`) and one that passes stays, so an empty selection stays empty.

In `0x11`-`0x17`, mode 0 tests each selected sound's own value and mode 1 this sound's value minus the selected
sound's; any other mode leaves the selection as it is (`0x007B34E2`, `0x007B35FF`, `0x007B3732`, `0x007B383C`, `0x007B398D`,
`0x007B3AB3`, `0x007B3B97`).

`0x11`, `0x13`, `0x14` and `0x15` test with `0x007B2BD0`, which compares signed 32-bit numbers (`cmp edx, r8d` with
`setg`/`setl`, `0x007B2BEC`-`0x007B2C12`); their mode-1 differences subtract zero-extended byte or `u16` fields at 32 bits
(`0x007B3517`, `0x007B3767`, `0x007B38C0`, `0x007B39EE`), so they are exact. `0x16` and `0x17` test with `0x007B2C40`, which
compares `f32` values (`ucomiss`/`comiss`, `0x007B2C5B`-`0x007B2C8B`); their mode-1 differences are `f32` subtractions
(`0x007B3AE0`, `0x007B3BD9`). With either comparator, a code above 5 fails every sound and empties the selection
(`0x007B2C16`, `0x007B2C92`):

| Opcode | Handler | Does |
|---|---|---|
| `0x01` | `0x007B33DF` | ends the macro |
| `0x10` | `0x007B33E9` | selects every other playing sound again, with no operands: it empties the selection (`0x007B6AA0`) and refills it as the macro's start does (`0x007B32F3`-`0x007B336C`), with each sound of the sound list `0x02EAD560` that is not this one, answers state 2 (slot 21, `0x007BD9A0`) and is not waiting for its bank (slot 38); later filters start again from all of them |
| `0x11` | `0x007B3471` | tests each selected sound's category, byte `+0x06` of its sound record (`0x007B349C`), against the value (`0x007B3494`-`0x007B34A4`); with mode 1, this sound's category minus the selected sound's (`0x007B34E8`-`0x007B3519`) |
| `0x12` | `0x007B3555` | tests each selected sound's key, the bank header's `param` (`u16` `+0x0A`, see [sound banks](sound-banks.md)) over the sound number (record `u16` `+0x08`) (`0x007BD5E0`, called at `0x007B3578`), against the value with its own unsigned `==`, `!=`, `>`, `>=`, `<` or `<=` (`0x007B357D`-`0x007B35BF`); with mode 1, this sound's key minus the selected sound's: both keys and the value are zero-extended from 32 bits (`0x007B360D`, `0x007B362C`, `0x007B3624`), subtracted at 64 bits (`0x007B3631`) and compared as signed 64-bit numbers (`0x007B3651`-`0x007B367C`); a code above 5 fails every sound here too (`0x007B3584`, `0x007B363B`), and a sound whose bank is not ready has key -1 (`0x007BD602`-`0x007BD609`) |
| `0x13` | `0x007B36BA` | tests byte `+0x07` of each selected sound's sound record (`0x007B36EC`) against the value; with mode 1, this sound's byte minus the selected sound's (`0x007B3738`-`0x007B3769`) |
| `0x14` | `0x007B37A5` | tests each selected sound's macro number for this call, the same byte `+0x0A`, `+0x0B` or `+0x4F` of its own sound record (`0x007B37C9`-`0x007B37EF`), 0 for `+0x4F` in a record below version `0x0E` (`0x007B37F1`), against the value; with mode 1, this sound's number minus the selected sound's (`0x007B3842`-`0x007B38C2`) |
| `0x15` | `0x007B38FE` | tests each selected sound's bank `param`, the `u16` `+0x0A` of its bank's `.sab` header read through the bank's slot 5 (`0x007B391A`-`0x007B3936`), the high half of `0x12`'s key, against the value; with mode 1, this sound's `param` minus the selected sound's (`0x007B3993`-`0x007B39F0`) |
| `0x16` | `0x007B3A3C` | tests each selected sound's play time, the `f32` `+0x504` to which its update `0x007BF0A0` adds each pass's seconds in state 5 (playing, set at `0x007BD20F`) or 6 (stopping, set at `0x007BEEF7`) (`0x007BF891`-`0x007BF8A2`), against the value (`0x007B3A6D`-`0x007B3A75`); with mode 1, this sound's play time minus the selected sound's (`0x007B3AB9`-`0x007B3AE8`) |
| `0x17` | `0x007B3B24` | tests each selected sound's volume, slot 26 `0x007BDBB0` (`0x007B3B47`), against the value; with mode 1, this sound's volume minus the selected sound's (`0x007B3B9D`-`0x007B3BDD`) |
| `0x18` | `0x007B3C19` | keeps the sounds whose pan lies in a stretch of the pan circle. A sound's pan is the first of the three panning values of slot 28 (`0x007BD6F0`), its ramp `+0x1B8` wrapped into -1 to 1 by steps of 2 (`0x007BD837`-`0x007BD879`). The stretch starts at the value, or with mode 1 at this sound's pan plus the value, wrapped by `0x007B4800`; any other mode uses the value as it is (`0x007B3C2C`-`0x007B3C4B`). It runs on for the `f32` `+0x0C`, going on from -1 past 1 (`0x007B3C90`-`0x007B3CCC`); both ends count as inside (`0x007B3CA6`-`0x007B3CB5`), and a length of 0 or less holds no sound (`0x007B3C79`-`0x007B3C87`). Code 0 keeps the sounds inside, code 1 the sounds outside, and any other code keeps every sound (`0x007B3CD2`-`0x007B3CE4`) |
| `0xA0` | `0x007B3D1D` | stops with fade `+0x08` (command `0x0B`, `0x007A84A0`) every selected sound (`+0x06` = 0), the first (1), the quietest by slot 26 `0x007BDBB0` (2) or the one with the largest `distance` value, slot 31 `+0x508` (3); in modes 2 and 3 a new sound quieter or farther than all of them is refused instead (`0x007B3E3B`, `0x007B3EDB`) |
| `0xA1` | `0x007B3F2F` | refuses the new sound (the macro returns 4, `0x007B3F4B`) |
| `0xA2` | `0x007B3F59` | ramps the first volume ramp of category `+0x06` (`0x007AAA20`, `0x007AA510`) to `+0x08` over `+0x0C` seconds |
| `0xA3` | `0x007B3F9E` | ramps the volume ramp `+0x148` of every selected sound to `+0x08` over `+0x0C` seconds (`0x007BE4D0`) |
| `0xA4` | `0x007B3FFB` | ramps this sound's volume ramp `+0x148` the same way (`0x007B4024`) |
| `0xA5` | `0x007B402E` | sets this sound's start delay `+0x51C` to `n * (+0x08)`, plus `+0x0C` when the action's byte `+0x00` is not 0 (`0x007B4070`-`0x007B408E`) |
| `0xA6` | `0x007B409D` | sets this sound's `default` value `+0x514` to `n * (+0x08) + (+0x0C)` through slot 17 (`0x007BEAE0`, `0x007B40F7`) |
| `0xA7` | `0x007B4102` | ramps the second pitch ramp of category `+0x06` (`0x007AA4F0`) to `+0x08` over `+0x0C` seconds |
| `0xA8` | `0x007B4147` | pauses category `+0x06` with fade `+0x08` (`0x007AA680`), as command `0x01` does |
| `0xA9` | `0x007B4187` | resumes category `+0x06` with fade `+0x08` (`0x007AA3E0`), as command `0x02` does |
| `0xAA` | `0x007B41C7` | with `+0x06` = 0, pauses every selected sound with fade `+0x08` (command `0x0C`, `0x007A8590`); any other `+0x06` does nothing (`0x007B41E3`) |
| `0xAB` | `0x007B424D` | with `+0x06` = 0, resumes every selected sound with fade `+0x08` (command `0x0D`, `0x007A7A20`); any other `+0x06` does nothing (`0x007B4265`) |

Every action from `0xA0` to `0xAB` first compares the number of selected sounds (`0x02EAD57C`) with `+0x05` by the code
`+0x04` (`0x007B2BD0`) and does nothing when the test fails. `0xA5` and `0xA6` then take `n`, the count past that
threshold (`0x007B404E`-`0x007B406C`, `0x007B40BD`-`0x007B40DB`):

```python
code 0 (==):          n = 1
code 2 (>):           n = count - (+0x05)
code 3 (>=):          n = count - (+0x05) + 1
codes 1, 4 and 5:     n = count
```

The targets are these:

- A category's volume is the product of its volume ramps (`0x007A9F40`) and its pitch the product of its two pitch
  ramps (`0x007A9D30`, count 2 from `0x007AA15E`); command `0x04` drives the first pitch ramp and command `0x03` the
  volume ramps after the first.
- A sound's volume is its record's `+0x0C` times its four ramps `+0x88`, `+0xC8`, `+0x108` and `+0x148`
  (`0x007BDBFC`-`0x007BDCD2`). `0xA3` and `0xA4` are the only calls of `0x007BE4D0`, the setter of the fourth, which
  also clears the ramp's curve pointer `+0x180` and passes curve 0, so the ramp is linear (`0x007BE4D4`-`0x007BE4EB`).
- The trigger `0x007BD240` hands the start delay `+0x51C` to each sequence it arms (`0x007BD317`, `0x007E7300`).
- The `default` value `+0x514` is what a switched sound reads for the name `default` (`0x007BDA63`).

`0x007AE1A0(chunk, out, i)` gives macro element `i` through the offset table whatever the version byte:
`element i = C + u32[C + u16[C + 0x02] + 4 * i]` (`0x007AE1A7`-`0x007AE1BA`). The shipped `mcr ` has version 0 and the
offsets `0x20`, `0x40` and `0x70`; the only filter its three streams use is `0x12`, in the second and third macros,
with code 0, mode 1 and value 0.

The filters compare a sound's whole number, signed, with `0x007B2BD0` and its float with `0x007B2C40`, as
`sound's value <code> value` by a code 0 to 5 for `==`, `!=`, `>`, `>=`, `<` and `<=`. With mode byte `+5` set to 1,
`0x18` adds its value to this sound's pan and wraps the sum into -1 to 1 by steps of 2 (`0x007B4800`, called at
`0x007B3C46`).

### Effect presets

`0x007ACD30(mixer, index, fade)` applies preset `index` of `epsp`, from the sound command `0x300` (`0x007EEF59`). An index
at or above the count logs `[sead][!!error!!]set effect preset number invalid [%d]` (`0x007ACDB3`). A negative index
passes that test and resets every bus to its `bus ` chunk values and re-enables every effect (`0x007ACE32`-`0x007ACFA8`).
A preset's records set a bus ramp (`0x007AD09E`-`0x007AD0A9`) or switch an effect on or off, and an effect's settings
come from `eps ` through `0x007ADDC0`, one section per effect type, with block sizes from `0x01CB49A0` and `0x01CB4990`.

`0x007ADE50` gives one preset, `0x007ADF10` one of its effect records and `0x007ADA80` one of its bus records.

### Events

An `evt ` element is a timed list of commands. `0x007ADF60` gives one element; `0x007B67E0` wraps each in an
`EventData` and builds a pool of 64 running events.

An `EventData` is `0x38` bytes (`0x007B68C0`-`0x007B68CA`) whose only field from the file is the element's address at
`+0x18` (`0x007B6917`-`0x007B691B`). The rest are its vtables `0x01CB4ED8`, `0x01CB4EE8` and `0x01CB4920` at `+0x00`, `+0x08`
and `+0x10`, -1 at `+0x20` and 0 at `+0x28` and `+0x30` (`0x007B6905`-`0x007B6935`). Their pointers go to the table at
`0x02EAD760`, one per element, with the chunk's count at `0x02EAD754` (`0x007B6861`-`0x007B6876`, `0x007B695A`); with no `evt `
chunk no `EventData` is built (`0x007B680F`).

Command `0x33` starts an event (`0x007B6350`): `0x007EE910` builds the `Event` and `0x007EE990` sets it running (state 1) and runs its first step. `0x007EEA00(event, seconds)` counts its wait
down and then runs commands until one waits. A command has a header length at `+0x01`, an opcode at `+0x02` and a
payload length at `+0x04`:

| Opcode | Does |
|---|---|
| `0x001` | ends the event (state 2) |
| `0x002` | waits `+0x08` milliseconds |
| `0x003`-`0x006` | plays (`0x007A78B0`), stops, pauses or resumes the sound with id `+0x08` |
| `0x007` | posts a name (`0x007A5380`) |
| `0x100`-`0x103` | music commands `0x1D`, `0x21`, `0x27` and `0x28` on the music with id `+0x08`; `0x102` first creates it from its bank (`0x007A4A10`) |
| `0x200`-`0x205` | category volume, pitch, pause, resume and the two byte pairs |
| `0x300` | applies an effect preset |
| `0x301` | sets a bus value |

Reading past the element's total size prints "Event::Update exceeded TotalCommandSize" and ends the event.

### External parameters

`0x007B0F90` builds one `0x40`-byte row per `expr` element at `0x02EAD3F8`, their count at `0x02EAD3EC`. `0x007B0E90(out, name)`
gives the ramped value of the row whose name matches, or -1; a switched sound reads its value through it
([Sound variations](sound-variations.md)). `0x007B1380` advances every row's ramp on each driver pass.

`0x007AE020(chunk, out, i)` gives element `i` as `C + u32[C + u16[C + 0x02] + 4 * i]` whatever the version, and a null
element for `i` below 0 or at or above the count (`0x007AE02C`-`0x007AE046`). An element, as the code reads it (the shipped
chunk has no elements):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | version | 1 or more lets `+0x04` apply |
| `+0x02` | `u16` | nameAt | offset of the name from the element |
| `+0x04` | `u8` | limited | 1: changes keep to the rates below |
| `+0x10` | `f32` | riseRate | the most the value rises per second |
| `+0x14` | `f32` | fallRate | the most the value falls per second |
| `nameAt` | `char` | name | the parameter name, ending in a 0 byte |

| File field | Becomes |
|---|---|
| chunk `+0x04` count | copied to `0x02EAD3EC` (`0x007B10C6`-`0x007B10CE`); the table is that many times `0x40` bytes (`0x007B10D4`-`0x007B10E5`) |
| the element's address | row `+0x08` (`0x007B1120`-`0x007B112B`) |
| `version`, `limited` | row `+0x34` is 1 when `version` is 1 or more and `limited` is 1, else 0 (`0x007B1140`-`0x007B114E`, `0x007B117F`) |
| `riseRate`, `fallRate` | copied to row `+0x38` and `+0x3C` when `+0x34` is 1 (`0x007B1155`-`0x007B116E`, `0x007B118C`-`0x007B1192`) |
| `nameAt`, `name` | read in place through row `+0x08`, compared byte by byte up to the 0 (`0x007B0ED2`-`0x007B0EF4`, `0x007B1240`-`0x007B1262`) |

The row:

| Offset | Type | Name | Meaning | Set by |
|---|---|---|---|---|
| `+0x00` | `u8[8]` | | | no writer |
| `+0x08` | `void*` | element | the `expr` element in the copy | `0x007B112B` |
| `+0x10` | `u8[8]` | | | no writer |
| `+0x18` | `f32` | start | the value the ramp starts from; 0 | `0x007B1196`; `0x007B12DD` |
| `+0x1C` | `f32` | target | the value set; 0 | `0x007B1196`; `0x007B12E3` |
| `+0x20` | `f32` | elapsed | time so far, stopped at the duration | `0x007B119B`; `0x007B12E9`, `0x007B13A9`, `0x007B13B1` |
| `+0x24` | `f32` | duration | 0 snaps to the target | `0x007B119B`; `0x007B12E9`, `0x007B1329`, `0x007B135A` |
| `+0x28` | `u8[4]` | | | no writer |
| `+0x2C` | `i32` | curve | 0, linear | `0x007B11A0`; `0x007B12F2` |
| `+0x30` | `u8` | active | 1 while the ramp runs | `0x007B11A4`; `0x007B12FA`, `0x007B13B7`, `0x007B13BE` |
| `+0x31` | `u8[3]` | | | no writer |
| `+0x34` | `u32` | limited | from the element, as above | `0x007B118C` |
| `+0x38` | `f32` | riseRate | from the element when `+0x34` is 1 | `0x007B118C` |
| `+0x3C` | `f32` | fallRate | from the element when `+0x34` is 1 | `0x007B1192` |

When `+0x34` is 0, `+0x38` and `+0x3C` take whatever the builder's stack held (`0x007B117F`-`0x007B1192`); they are read
only when `+0x34` is 1 (`0x007B12D8`).

The value is the ramp: `start` when `duration` is 0 gives `target` (`0x007B0F23`-`0x007B0F2E`), else
`start + curve(elapsed / duration) * (target - start)` (`0x007B0F4A`-`0x007B0F6F`).

`0x007B1210(name, value)`, the driver's command `0x32`, sets one: the present value becomes `start`, `value` the
target, `elapsed` and `duration` 0, `curve` 0 and `active` 1 (`0x007B12D8`-`0x007B12FA`); with `+0x34` 1 the duration
becomes the change over `riseRate` when rising, or over `fallRate` when falling, each taken as its absolute value
(`0x007B1301`-`0x007B135A`). A name that matches no row returns -1 (`0x007B1274`).

A value above the present one is rising, `(value - present) / |riseRate|`, and any other is falling,
`(present - value) / |fallRate|`; the duration takes that result only when it is above 0 (`0x007B131B`, `0x007B1354`),
so an equal value keeps the duration 0. A matched row returns 0 (`0x007B1327`, `0x007B1366`).

### The HCA mixer switch

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | h00 | 0 |
| `+0x01` | `u8` | channels | 16 |
| `+0x02` | `u16` | h02 | `16` |
| `+0x04` | `u32` | rate | 44,100 |
| `+0x08` | `u8` | enable | 0 |

`0x007A4D50` copies `+0x08`, `+0x01` and `+0x04` into its parameters `+0x1C`, `+0x18` and `+0x14` (`0x007A4F5F`-`0x007A4F6E`).
That parameter block is `0x20` bytes on the start's stack, handed to `0x007AC4F0` (`0x007A4F81`-`0x007A4F85`); its other
fields come from the start block, not from the file.

| File field | Becomes |
|---|---|
| `h00`, `h02` | not read by `0x007A4D50` |
| `channels` | widened to 32 bits into parameter `+0x18` (`0x007A4F67`-`0x007A4F6B`), then the HCA mixer's channel count (`0x007ACC7B`-`0x007ACC80`) |
| `rate` | copied to parameter `+0x14` (`0x007A4F6E`-`0x007A4F71`), then the HCA mixer's rate (`0x007ACC72`-`0x007ACC77`) |
| `enable` | converted: any value but 0 gives 1 in the byte `+0x1C` (`0x007A4F5F`-`0x007A4F63`); with no `hcam` chunk it is 0 and `+0x14`, `+0x18` are not set (`0x007A4F76`) |

Only with `enable` set does `0x007AC4F0` build the HCA mixer voice (`0x007ACC6B`-`0x007ACC9B`). The engine renders at the
constant 48,000 (`0x007AC691`).

### The master ramps

The master volume ramp `0x01F403E0` and the master pitch ramp `0x01F40410` are laid out alike: `+0x00` the value the
ramp starts from, then the fields below. When the configuration is loaded, `0x007AAA40` sets each to start 0, target
1.0, time 0 and duration 0 (the vector `0x008C5F90`, `0x007AAC12`, `0x007AAC20`) and the other fields to 0.

Command `0x05` starts the volume ramp (`0x007AAD90`, from `0x007AB751`) and command `0x06` the pitch ramp (`0x007AAC80`, from
`0x007AB765`): the current value becomes the start, the argument the target and the duration, time 0, curve 0, and
the ramp runs. Each driver pass advances both (`0x007AAEA0`, from `0x007A54B2`).

Each ramp is a static `SQEX::Sd::DynamicValue<0>` whose vtable word sits 8 bytes before it, at `0x01F403D8` and
`0x01F40408`; the file holds the vtable `0x01CB44A0` in both. At exit, `0x008B8690` and `0x008B8680` store the base vtable
`0x01CB4470`, `SQEX::Sd::SeadObject<0,8>`, in them. `0x00169710` and `0x00169700`, which run from the C++ initialiser table
(its entries `0x008C4940` and `0x008C4948`), register the two stubs with `atexit` (`0x00808B90`; [Static initialisation and
teardown](../Compiler-And-C-Runtime/static-initialisation-and-teardown.md)).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F403D8` | `void*` | `0x01CB44A0` | the volume ramp's vtable word | `0x008B8690`, `0x01CB4470` at exit (`0x008B8697`) | no instruction names it |
| `0x01F40408` | `void*` | `0x01CB44A0` | the pitch ramp's vtable word | `0x008B8680`, `0x01CB4470` at exit (`0x008B8687`) | no instruction names it |
| `0x01F403E4` | `f32` | 0 | the volume ramp's target | `0x007AAA40` (`0x007AAC12`); `0x007AAD90` (`0x007AAE05`) | `0x007AAD90` (`0x007AADB4`, `0x007AADD5`); `0x007AAEA0` (`0x007AAF18`, `0x007AAF31`) |
| `0x01F403E8` | `f32` | 0 | its time so far; the pass adds its time step and stops at the duration (`0x007AAEDB`-`0x007AAEF0`) | `0x007AAA40` (`0x007AAC12`); `0x007AAD90`, 0 (`0x007AAE15`); `0x007AAEA0` (`0x007AAEE6`, `0x007AAEF0`) | `0x007AAD90` (`0x007AADBE`); `0x007AAEA0` (`0x007AAED1`) |
| `0x01F403EC` | `f32` | 0 | its duration; with a duration of 0 the value is the target | `0x007AAA40` (`0x007AAC12`); `0x007AAD90` (`0x007AAE0D`, `0x007AAE53`, `0x007AAE86`) | `0x007AAD90` (`0x007AADA7`); `0x007AAEA0` (`0x007AAEB0`) |
| `0x01F403F4` | `i32` | 0 | its curve, handed to `0x007A9E50` with `time / duration` | `0x007AAA40`, 0 (`0x007AAC19`); `0x007AAD90`, 0 (`0x007AAE1F`) | `0x007AAD90` (`0x007AADC6`); `0x007AAEA0` (`0x007AAF22`) |
| `0x01F403F8` | `u8` | 0 | 1 while the ramp runs; the pass clears it when the time reaches the duration | `0x007AAA40`, 0 (`0x007AAC27`); `0x007AAD90`, 1 (`0x007AAE29`); `0x007AAEA0` (`0x007AAEFB`, `0x007AAF04`) | `0x007AAEA0` (`0x007AAEBB`) |
| `0x01F403FC` | `i32` | 0 | with 1, a start shortens the duration to the change over the rate `0x01F40400` (rising) or `0x01F40404` (falling) (`0x007AAE30`-`0x007AAE86`); only `0x007AAA40` writes it, with 0 | `0x007AAA40` (`0x007AAC2E`) | `0x007AAD90` (`0x007AADFE`) |
| `0x01F40414` | `f32` | 0 | the pitch ramp's target | `0x007AAA40` (`0x007AAC20`); `0x007AAC80` (`0x007AACF5`) | `0x007AAC80` (`0x007AACA4`, `0x007AACC5`); `0x007AAEA0` (`0x007AAFA1`, `0x007AAFBA`) |
| `0x01F40418` | `f32` | 0 | its time so far | `0x007AAA40` (`0x007AAC20`); `0x007AAC80`, 0 (`0x007AAD05`); `0x007AAEA0` (`0x007AAF77`, `0x007AAF81`) | `0x007AAC80` (`0x007AACAE`); `0x007AAEA0` (`0x007AAF62`) |
| `0x01F4041C` | `f32` | 0 | its duration | `0x007AAA40` (`0x007AAC20`); `0x007AAC80` (`0x007AACFD`, `0x007AAD43`, `0x007AAD76`) | `0x007AAC80` (`0x007AAC97`); `0x007AAEA0` (`0x007AAF50`) |
| `0x01F40424` | `i32` | 0 | its curve | `0x007AAA40`, 0 (`0x007AAC35`); `0x007AAC80`, 0 (`0x007AAD0F`) | `0x007AAC80` (`0x007AACB6`); `0x007AAEA0` (`0x007AAFAB`) |
| `0x01F40428` | `u8` | 0 | 1 while it runs | `0x007AAA40`, 0 (`0x007AAC3C`); `0x007AAC80`, 1 (`0x007AAD19`); `0x007AAEA0` (`0x007AAF8C`, `0x007AAF95`) | `0x007AAEA0` (`0x007AAF5B`) |
| `0x01F4042C` | `i32` | 0 | its rate switch, with the rates `0x01F40430` and `0x01F40434`; only `0x007AAA40` writes it, with 0 | `0x007AAA40` (`0x007AAC43`) | `0x007AAC80` (`0x007AACEE`) |

No other instruction reaches these fields. The nearby addresses that `0x007A5B50` and `0x0079E520` take,
`0x01F403D0` and `0x01F403A8`, belong to other objects.

## Shipped data

| Chunk | Size | Holds |
|---|---:|---|
| `ctgr` | `0xA0` | four categories: `dummy0` size 0, `music` 4, `se` 48, `voice` 8 |
| `bus ` | `0x50` | one bus, `Master`, level 1.0, no sends, no effects |
| `mcr ` | `0xA0` | three macros: one that only ends; one that refuses a new sound when one with the same key plays; one that, when two or more with the same key play, posts sound command `0xB` with the value 0.1 on the first of them through `0x007A84A0` (`0x007B3D6F`-`0x007B3D7B`) |
| `epsp` | `0x10` | no presets |
| `eps ` | `0x1E0` | eleven sections; 1, 2, 3, 4, 9 and 10 hold one block each |
| `curv` | `0x50` | one curve of two points |
| `expr` | `0x10` | no parameters |
| `hcam` | `0x10` | 16, 44,100, switch off |
| `evt ` | `0x10` | no events |
| `ctgl` | `0x40` | one layer, `default` |

The chunks follow the directory at `0xB0` with no gaps and end at the file's end; `copySize` is the file's length.
Sections 5 and 7 of `eps ` each declare one preset of `0x10` bytes, and those bytes are the headers of sections 6
and 8.

### The voice pools

The sum of the positive category sizes, 60, sizes the engine's pools (`0x007A4ED7`-`0x007A4EFD`, `0x007A5115`-`0x007A5160`):

| Pool | Size | Kept at |
|---|---:|---|
| sum + 32 | 92 | `0x02EAD4C0` |
| twice that | 184 | `0x02EAD5A0` |
| `min(184, 0x60) + min(0x20, 0x80) + min(0, 0x20)`, from the start block's `+0x20`, `+0x24` and `+0x28` | 128 | the render block |

## Loader behaviour

1. In the header only the magic is checked. `copySize` is never compared with the file's length.
2. Header `+0x04`, `+0x09`-`+0x0B` and entry `+0x04`, `+0x06`, `+0x0C` are read by none of `0x007AE410`, `0x007B0F90`,
   the ten finders or the 16 reads of `0x02EAD3E0`.
3. No directory offset, element offset, or bus index or send count of a bus element is range-checked; the preset
   records are (item 10).
4. Only the curve and external-parameter element readers check the index (`0x007ADC51`, `0x007AE031`).
5. A missing chunk gives a null pointer. The `ctgr` and `bus ` users read it at once and fault (`0x007B104F`,
   `0x007AC69F`); `mcr ` and `epsp` fault when used (`0x007B3269`, `0x007ACDB3`); the others are skipped. A missing `ctgl`
   counts as one element (`0x007AAAB9`), and a missing `hcam` leaves the HCA mixer off (`0x007A4F76`).
6. A `ctgr` with no elements fails the start (`0x007AAA66`).
7. A negative category size must name a category with a positive size. One with a size below 0, itself included,
   prints the `InitializeRefCategory` error and fails the start (`0x007AA35A`-`0x007AA3B5`, `0x007AABF4`); one with size 0,
   or an index at or above the count, is a null pointer that faults (`0x007AAA20`, `0x007AA35A`).
8. A bus holds at most four effects (`+0x10`-`+0x28`): a fifth built effect is stored over the name pointer `+0x30`
   (`0x007ACA67`). It has five level ramps (`0x007AC5E9`), so `send0` and the send targets together are at most five, and
   `sendLevels` holds four levels. A send target whose element comes after the sending bus is copied in as a null voice (The bus).
9. An effect record of type 9 or above 10 builds nothing (`0x007AC88A`).
10. A preset's bus record is skipped when its bus is at or above the bus count or its ramp is not 0 to 4
    (`0x007AD09E`, `0x007AD0A9`); an effect record when its bus is at or above the count, its slot is 4 or more or the slot
    is empty (`0x007AD13D`-`0x007AD15A`).
11. An `expr` element limits its changes only with `version` 1 or more and `limited` exactly 1 (`0x007B1140`-`0x007B114C`).

## Modding notes

- A category's size is the number of its sounds that can play at once; raising one also grows the shared pools.
- A `ctgr` with no elements stops the engine from starting (`0x007AAA66`), and a category that shares a missing one
  reads a null pointer (`0x007AA35A`).
- A `copySize` larger than the file reads past the buffer; a smaller one leaves later chunks outside the copy.
- Setting the `hcam` switch builds the HCA mixer voice with the file's 16 and 44,100.
- The shipped game has no preset to apply, but command `0x300` with a negative index still resets the master bus.

## Related

- [Sound banks](sound-banks.md) - the bank files the engine plays.
- [Sound driver objects](sound-driver-objects.md) - the pools the category sizes set, and the category commands.
