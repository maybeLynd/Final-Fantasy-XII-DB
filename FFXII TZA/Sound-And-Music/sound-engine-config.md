---
title: "Sound engine configuration: the start-up file that sets the sound categories, the master bus, the macros and the effect presets"
kind: "format"
category: "Sound and music"
addresses: "0x00210760, 0x007A4D50, 0x007B0F90, 0x007AE410, 0x007ADB20, 0x007AC4F0, 0x007B31A0, 0x007ACD30"
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

1. It opens the file (`0x002107C0`); when that fails it returns without starting the sound engine.
2. It takes the size from the file layer (`0x002107E8`), not from the header, allocates that plus one byte
   (`0x002107F2`), reads the file and closes it.
3. It fills an initialisation block with the buffer at `+0x38` and calls the engine start `0x007A4D50` (`0x00210889`),
   whose result it does not test.
4. It frees its buffer (`0x002108F1`).

### The engine's copy

`0x007A4D50` calls `0x007B0F90` (`0x007A4E79`):

1. `0x007AE410` checks the magic `scnf` (`0x007B0FA8`); a mismatch makes the engine start return -1.
2. It allocates the header's `+0x0C` bytes and copies that many bytes of the file to the block it keeps at `0x02EAD3E0`
   (`0x007B0FE8`-`0x007B1005`).
3. It sums the positive category sizes into `0x02EAD3E8` (`0x007B103C`-`0x007B108A`) and builds the external-parameter
   rows (`0x007B10B4`-`0x007B1145`).

All 16 later reads of `0x02EAD3E0`, in 15 functions, pass it to a chunk finder, so every chunk is read from the copy.

## Layouts

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
`0x01CB4928` (`0x007ADB5A`); a tag not there gives a null chunk. A table chunk starts with a `u8` version, a `u16` at
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
| `+0x04` | `i16` | size | 0 none; above 0 that many sound slots; below 0 shares category -size |
| `+0x06` | `u16` | c06 | the name length |
| `+0x10` | `char` | name | the category name, inline, `+0x06` characters long |

`0x007AAA40` refuses a chunk with no elements (`0x007AAA66`). A size of 0 leaves the category empty (`0x007AAB11`), a
positive size allocates that many slots (`0x007AA2E3`), and a negative one binds it to another category
(`0x007AABD1`, `0x007AA342`). The name goes to the category object's `+0x70` (`0x007AA137`-`0x007AA156`). `ctgl` gives only
its element count: each category gets that many plus one volume ramps (`0x007AAAB2`, `0x007AA15A`).

`0x007ADAB0` gives one category element, by index for version 0 and through the offset table otherwise. `0x007AAA40`
builds one `0x88`-byte `Driver::Category` per element (`0x007A96F0`; `0x007A9760` destroys one) and keeps the pointers at
`0x02EAD008`. `0x007AA010` gives each category a handle list with as many nodes as its size.

The binding is `0x007AA320(category, element)`, called by `0x007AAA40` (`0x007AABED`) after every category is built. For
an element whose `i16` size (`+4` of the element data the argument's `+8` points to) is negative it looks up category
`-size` (`0x007AAA20`: an index below the count `0x02EAD000`, else 0) and keeps it at the category's `+0x58`. When the
dword `+0x10` of that category is 0 it prints
"[sead][!!error!!]Category::InitializeRefCategory referenced category is not initialized( or reference is looping )!"
and returns -1; otherwise, and for a size of 0 or more, it returns 0.

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
| `+0x0C` | `f32` | level | the bus volume |
| `+0x10` | `f32[4]` | sendLevels | one per send |
| `+0x20` | `char` | name | the bus name, inline, `+0x0B` characters long |

`0x007AC4F0` builds the buses: `+0x01` picks the slot (`0x007AC770`), the root bus takes `+0x0C` as its level
(`0x007ACAAE`, `0x007ACAE0`), and other buses read their sends (`0x007AC7AD`-`0x007AC822`) and effects (`0x007AC83A`). The
effect table is at `nameAt + ((nameLength + 0x10) & 0xF0)` (`0x007ADA3F`), and an effect's type byte `+0x01` picks its
class through the jump table at `0x007ACCF0` (`0x007AC883`).

`0x007AD950` gives one bus element, by index for version 0 and through the offset table otherwise.
`0x007AC410(mixer, bus)` gives a bus's voice; a bus number below 0 or past the count prints "bus access overrun! use
master bus" and gives bus 0's. `0x007AC4D0(mixer, port)` gives a master port: 1 is bus 0's voice and 2 the voice at
mixer `+0x18`. The mixer object, `Driver::Audio`, is built once at `0x02EAD0A8` (`0x007AC360`).

| Type | Effect class | Builder |
|---:|---|---|
| 0 | `EmptyEffect` | |
| 1 | `SurroundReverb` | `0x007D2150` |
| 2 | `Compressor` | `0x007D85E0` |
| 3 | `Filter` | `0x007D0AC0` |
| 4 | `SideChainInput` | `0x007D80E0` |
| 5 | `SimpleFilter` | `0x007D9530` |
| 6 | `Flanger` | `0x007D99E0` |
| 7 | `GranularPitchShift` | `0x007DA0A0` |
| 8 | `HilbertFilter` | `0x007DAAB0` |
| 10 | `BuildReverb` | `0x007DAFF0` |

Each builder installs its class's vtable and zeroes its ramps; `0x007AC4F0` calls it for its type (`0x007AC8F6`-`0x007ACA48`).

### Macros

`0x007B31A0` runs macro number N, from the sound's own record (`0x007B3201`-`0x007B3226`), when N is below the chunk's count
(`0x007B3269`). A macro record's `u16` at `+0x02` is the offset of its instruction stream (`0x007B32D0`). Each instruction
has a header length at `+0x01`, an opcode at `+0x02` and a payload length at `+0x03` (`0x007B42CF`, `0x007B33B6`,
`0x007B42E4`). 22 opcodes have handlers:

| Opcode | Handler | Does |
|---|---|---|
| `0x01` | `0x007B33DF` | ends the macro |
| `0x10` | `0x007B33E9` | a step of its own, before the filters |
| `0x11`-`0x18` | from `0x007B4374` | filter the playing sounds; `0x12` compares a sound's key, or with mode byte `+5` set to 1 this sound's key minus the other's, with `==`, `!=`, `>`, `>=`, `<` or `<=` (`0x007B3555`); the shipped macros use mode 1 against 0, the same key |
| `0xA0` | `0x007B3D1D` | when the count of playing sounds passes the test, acts on all, the first, the quietest or the loudest of them with a value |
| `0xA1` | `0x007B3F2F` | when the count passes the test, refuses the new sound |
| `0xA2`-`0xAB` | from `0x007B4374` | other actions |

`0x007AE1A0` gives one macro element. The filters compare whole numbers with `0x007B2BD0` and floats with `0x007B2C40`, by a
code 0 to 5 for `==`, `!=`, `>`, `>=`, `<` and `<=`. With mode byte `+5` set to 1, one action adds its value to the
sound's current one and wraps the sum into -1 to 1 by steps of 2 (`0x007B4800`, called at `0x007B3C46`).

### Effect presets

`0x007ACD30(mixer, index, fade)` applies preset `index` of `epsp`, from the sound command `0x300` (`0x007EEF59`). An index
at or above the count logs `[sead][!!error!!]set effect preset number invalid [%d]` (`0x007ACDB3`). A negative index
passes that test and resets every bus to its `bus ` chunk values and re-enables every effect (`0x007ACE32`-`0x007ACFA8`).
A preset's records set a bus ramp (`0x007AD09E`-`0x007AD0A9`) or switch an effect on or off, and an effect's settings
come from `eps ` through `0x007ADDC0`, one section per effect type, with block sizes from `0x01CB49A0` and `0x01CB4990`.

`0x007ADE50` gives one preset, `0x007ADF10` one of its effect records and `0x007ADA80` one of its bus records.

### Events

An `evt ` element is a timed list of commands. `0x007ADF60` gives one element; `0x007B67E0` wraps each in an
`EventData` and builds a pool of 64 running events. Command `0x33` starts one (`0x007B6350`): `0x007EE910` builds the
`Event` and `0x007EE990` sets it running (state 1) and runs its first step. `0x007EEA00(event, seconds)` counts its wait
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

### The HCA mixer switch

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | h00 | 0 |
| `+0x01` | `u8` | channels | 16 |
| `+0x02` | `u16` | h02 | `16` |
| `+0x04` | `u32` | rate | 44,100 |
| `+0x08` | `u8` | enable | 0 |

`0x007A4D50` copies `+0x08`, `+0x01` and `+0x04` into its parameters `+0x1C`, `+0x18` and `+0x14` (`0x007A4F5F`-`0x007A4F6E`).
Only with `enable` set does `0x007AC4F0` build the HCA mixer voice (`0x007ACC6B`-`0x007ACC9B`). The engine renders at the
constant 48,000 (`0x007AC691`).

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

1. Only the magic is checked. `copySize` is never compared with the file's length.
2. Header `+0x04`, `+0x09`-`+0x0B` and entry `+0x04`, `+0x06`, `+0x0C` are read by none of `0x007AE410`, `0x007B0F90`,
   the ten finders or the 16 reads of `0x02EAD3E0`.
3. No directory offset, element offset, bus index or send count is range-checked.
4. Only the curve and external-parameter element readers check the index (`0x007ADC51`, `0x007AE031`).
5. A missing chunk gives a null pointer. The `ctgr` and `bus ` users read it at once and fault (`0x007B104F`,
   `0x007AC69F`); `mcr ` and `epsp` fault when used (`0x007B3269`, `0x007ACDB3`); the others are skipped.

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
