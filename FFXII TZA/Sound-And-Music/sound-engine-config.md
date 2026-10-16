---
title: "Sound engine configuration: the start-up file that sets the sound categories, the master bus, the macros and the effect presets"
kind: "format"
category: "Sound and music"
addresses: "00210760, 007A4D50, 007B0F90, 007AE410, 007ADB20, 007AC4F0, 007B31A0, 007ACD30"
---

## What the player sees

- Music, sound effects and voices are mixed as separate categories, each with its own number of sounds that can play
  at once.
- The file changes nothing during play; it is read once when the game starts.

## Where it comes from

The file is `ps2data/sound/sead.win.config`, 1,264 bytes, the only `.config` file the game ships.

### Loading

`00210760` builds the path from `PS2Data/sound/sead` (`009068E0`) and `.win.config` (`00906A38`) at `002107A0`. It runs
once at start-up, reached from `0017CEB0` through `0017D6B0` and `001DBA40`.

1. It opens the file (`002107C0`); when that fails it returns without starting the sound engine.
2. It takes the size from the file layer (`002107E8`), not from the header, allocates that plus one byte
   (`002107F2`), reads the file and closes it.
3. It fills an initialisation block with the buffer at `+38`<sub>h</sub> and calls the engine start `007A4D50` (`00210889`),
   whose result it does not test.
4. It frees its buffer (`002108F1`).

### The engine's copy

`007A4D50` calls `007B0F90` (`007A4E79`):

1. `007AE410` checks the magic `scnf` (`007B0FA8`); a mismatch makes the engine start return -1.
2. It allocates the header's `+0C`<sub>h</sub> bytes and copies that many bytes of the file to the block it keeps at `02EAD3E0`
   (`007B0FE8`-`007B1005`).
3. It sums the positive category sizes into `02EAD3E8` (`007B103C`-`007B108A`) and builds the external-parameter
   rows (`007B10B4`-`007B1145`).

All 16 later reads of `02EAD3E0`, in 15 functions, pass it to a chunk finder, so every chunk is read from the copy.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | magic | "scnf" |
| `04`<sub>h</sub> | `u16` | h04 | 0 |
| `06`<sub>h</sub> | `u16` | dirOffset | `10`<sub>h</sub> |
| `08`<sub>h</sub> | `u8` | chunkCount | 10 |
| `09`<sub>h</sub> | `u8[3]` | h09 | 0 |
| `0C`<sub>h</sub> | `u32` | copySize | bytes the engine copies; 1,264 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | tag | the chunk's tag |
| `04`<sub>h</sub> | `u16` | e04 | 0 |
| `06`<sub>h</sub> | `u16` | e06 | `10`<sub>h</sub> |
| `08`<sub>h</sub> | `u32` | offset | from the start of the file |
| `0C`<sub>h</sub> | `u32` | e0C | 0 |

Each finder walks `chunkCount` entries from `dirOffset` and compares the tag with its entry in the tag table at
`01CB4928` (`007ADB5A`); a tag not there gives a null chunk. A table chunk starts with a `u8` version, a `u16` at
`+02`<sub>h</sub> that locates its element-offset table and a `u16` element count at `+04`<sub>h</sub>.

| Tag | Class | Finder | Read by |
|---|---|---|---|
| `ctgr` | `CategoryChunk` | `007ADB20` | `007A4D50`, `007B0F90` |
| `ctgl` | `CategoryLayerChunk` | `007ADBB0` | `007A4D50` |
| `bus ` | `BusChunk` | `007AD9A0` | `007AC4F0`, `007ACD30` |
| `mcr ` | `MacroChunk` | `007AE1D0` | `007B31A0` |
| `evt ` | `EventChunk` | `007ADF90` | `007A4D50` |
| `epsp` | `EffectPresetPackChunk` | `007ADE80` | `007ACD30` |
| `eps ` | `EffectPresetChunk` | `007ADD30` | `007AD240` |
| `curv` | `CurveChunk` | `007ADCA0` | nine curve binders, such as `007BDFA0` |
| `expr` | `ExternalParameterChunk` | `007AE080` | `007B0F90` |
| `hcam` | `HCAMXSettings` | `007AE110` | `007A4D50` |

The class names are the run-time type names of each chunk's wrapper.

### Categories

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | version | 2 |
| `01`<sub>h</sub> | `u8` | c01 | the element index |
| `02`<sub>h</sub> | `u16` | nameAt | offset of the name, `10`<sub>h</sub> |
| `04`<sub>h</sub> | `i16` | size | 0 none; above 0 that many sound slots; below 0 shares category -size |
| `06`<sub>h</sub> | `u16` | c06 | the name length |
| `10`<sub>h</sub> | `char` | name | the category name, inline, `+06`<sub>h</sub> characters long |

`007AAA40` refuses a chunk with no elements (`007AAA66`). A size of 0 leaves the category empty (`007AAB11`), a
positive size allocates that many slots (`007AA2E3`), and a negative one binds it to another category
(`007AABD1`, `007AA342`). The name goes to the category object's `+70`<sub>h</sub> (`007AA137`-`007AA156`). `ctgl` gives only
its element count: each category gets that many plus one volume ramps (`007AAAB2`, `007AA15A`).

`007ADAB0` gives one category element, by index for version 0 and through the offset table otherwise. `007AAA40`
builds one `88`<sub>h</sub>-byte `Driver::Category` per element (`007A96F0`; `007A9760` destroys one) and keeps the pointers at
`02EAD008`. `007AA010` gives each category a handle list with as many nodes as its size.

### How a category limits its sounds

`007A9A10(category, handle)` adds a starting sound, music or instrument to its category, or to the one a negative size
shares (`+58`<sub>h</sub>):

1. While the list is full, it walks it from its oldest entry and finds the one with the lowest priority, slot 25 of the
   object, which for a sound is byte `+07`<sub>h</sub> of its sound record (`007BD980`).
2. When the new object's priority is lower than that one's, it refuses the new one (returns 1).
3. Otherwise it stops the lowest one at once (slot 2, no fade) and takes it out of the list; an entry with no object
   prints "list remove invalid iterator".
4. It gives the new object the category's volume (`007A9F40`, slot 5) and pitch (`007A9D30`, slot 6), pauses it when
   the category's pause count `+64`<sub>h</sub> is above 0, and appends its handle at the newest end (`007BB9A0`).

`007A9F40` multiplies the category's volume ramps `+38`<sub>h</sub> and its master volume `+48`<sub>h</sub>; `007A9D30` multiplies its
pitch ramps `+40`<sub>h</sub> and its master pitch `+4C`<sub>h</sub>. Each driver pass `007AAEA0` advances the master volume ramp
`01F403E0` (type 5, `007AAD90`) and the master pitch ramp `01F40410` (type 6, `007AAC80`) and stores them into every
category (`007AA540` at `+48`<sub>h</sub>, `007AA530` at `+4C`<sub>h</sub>). `007AA550` sets a pitch ramp (type 4), and `007AA510`, run by
a macro, the first volume ramp.

### The bus

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | version | 2 |
| `01`<sub>h</sub> | `u8` | busIndex | 0 is the root bus |
| `02`<sub>h</sub> | `u16` | nameAt | `20`<sub>h</sub> |
| `04`<sub>h</sub> | `i8` | send0 | a bus to send to, or -1 |
| `05`<sub>h</sub> | `u8` | effectCount | effects on the bus |
| `06`<sub>h</sub> | `u8[4]` | sendTargets | more send buses |
| `0A`<sub>h</sub> | `u8` | sendCount | how many of them |
| `0B`<sub>h</sub> | `u8` | nameLength | places the effect table |
| `0C`<sub>h</sub> | `f32` | level | the bus volume |
| `10`<sub>h</sub> | `f32[4]` | sendLevels | one per send |
| `20`<sub>h</sub> | `char` | name | the bus name, inline, `+0B`<sub>h</sub> characters long |

`007AC4F0` builds the buses: `+01`<sub>h</sub> picks the slot (`007AC770`), the root bus takes `+0C`<sub>h</sub> as its level
(`007ACAAE`, `007ACAE0`), and other buses read their sends (`007AC7AD`-`007AC822`) and effects (`007AC83A`). The
effect table is at `nameAt + ((nameLength + 10h) & F0h)` (`007ADA3F`), and an effect's type byte `+01`<sub>h</sub> picks its
class through the jump table at `007ACCF0` (`007AC883`).

`007AD950` gives one bus element, by index for version 0 and through the offset table otherwise.
`007AC410(mixer, bus)` gives a bus's voice; a bus number below 0 or past the count prints "bus access overrun! use
master bus" and gives bus 0's. `007AC4D0(mixer, port)` gives a master port: 1 is bus 0's voice and 2 the voice at
mixer `+18`<sub>h</sub>. The mixer object, `Driver::Audio`, is built once at `02EAD0A8` (`007AC360`).

| Type | Effect class | Builder |
|---:|---|---|
| 0 | `EmptyEffect` | |
| 1 | `SurroundReverb` | `007D2150` |
| 2 | `Compressor` | `007D85E0` |
| 3 | `Filter` | `007D0AC0` |
| 4 | `SideChainInput` | `007D80E0` |
| 5 | `SimpleFilter` | `007D9530` |
| 6 | `Flanger` | |
| 7 | `GranularPitchShift` | |
| 8 | `HilbertFilter` | `007DAAB0` |
| 10 | `BuildReverb` | `007DAFF0` |

Each builder installs its class's vtable and zeroes its ramps; `007AC4F0` calls it for its type (`007AC8F6`-`007ACA48`).

### Macros

`007B31A0` runs macro number N, from the sound's own record (`007B3201`-`007B3226`), when N is below the chunk's count
(`007B3269`). A macro record's `u16` at `+02`<sub>h</sub> is the offset of its instruction stream (`007B32D0`). Each instruction
has a header length at `+01`<sub>h</sub>, an opcode at `+02`<sub>h</sub> and a payload length at `+03`<sub>h</sub> (`007B42CF`, `007B33B6`,
`007B42E4`). 22 opcodes have handlers:

| Opcode | Handler | Does |
|---|---|---|
| `01`<sub>h</sub> | `007B33DF` | ends the macro |
| `10`<sub>h</sub> | `007B33E9` | a step of its own, before the filters |
| `11`<sub>h</sub>-`18`<sub>h</sub> | from `007B4374` | filter the playing sounds; `12`<sub>h</sub> compares a sound's key, or with mode byte `+5` set to 1 this sound's key minus the other's, with `==`, `!=`, `>`, `>=`, `<` or `<=` (`007B3555`); the shipped macros use mode 1 against 0, the same key |
| `A0`<sub>h</sub> | `007B3D1D` | when the count of playing sounds passes the test, acts on all, the first, the quietest or the loudest of them with a value |
| `A1`<sub>h</sub> | `007B3F2F` | when the count passes the test, refuses the new sound |
| `A2`<sub>h</sub>-`AB`<sub>h</sub> | from `007B4374` | other actions |

`007AE1A0` gives one macro element. The filters compare whole numbers with `007B2BD0` and floats with `007B2C40`, by a
code 0 to 5 for `==`, `!=`, `>`, `>=`, `<` and `<=`. With mode byte `+5` set to 1, one action adds its value to the
sound's current one and wraps the sum into -1 to 1 by steps of 2 (`007B4800`, called at `007B3C46`).

### Effect presets

`007ACD30(mixer, index, fade)` applies preset `index` of `epsp`, from the sound command `300`<sub>h</sub> (`007EEF59`). An index
at or above the count logs `[sead][!!error!!]set effect preset number invalid [%d]` (`007ACDB3`). A negative index
passes that test and resets every bus to its `bus ` chunk values and re-enables every effect (`007ACE32`-`007ACFA8`).
A preset's records set a bus ramp (`007AD09E`-`007AD0A9`) or switch an effect on or off, and an effect's settings
come from `eps ` through `007ADDC0`, one section per effect type, with block sizes from `01CB49A0` and `01CB4990`.

`007ADE50` gives one preset, `007ADF10` one of its effect records and `007ADA80` one of its bus records.

### Events

An `evt ` element is a timed list of commands. `007ADF60` gives one element; `007B67E0` wraps each in an
`EventData` and builds a pool of 64 running events. Command `33`<sub>h</sub> starts one (`007B6350`): `007EE910` builds the
`Event` and `007EE990` sets it running (state 1) and runs its first step. `007EEA00(event, seconds)` counts its wait
down and then runs commands until one waits. A command has a header length at `+01`<sub>h</sub>, an opcode at `+02`<sub>h</sub> and a
payload length at `+04`<sub>h</sub>:

| Opcode | Does |
|---|---|
| `001`<sub>h</sub> | ends the event (state 2) |
| `002`<sub>h</sub> | waits `+08`<sub>h</sub> milliseconds |
| `003`<sub>h</sub>-`006`<sub>h</sub> | plays (`007A78B0`), stops, pauses or resumes the sound with id `+08`<sub>h</sub> |
| `007`<sub>h</sub> | posts a name (`007A5380`) |
| `100`<sub>h</sub>-`103`<sub>h</sub> | music commands `1D`<sub>h</sub>, `21`<sub>h</sub>, `27`<sub>h</sub> and `28`<sub>h</sub> on the music with id `+08`<sub>h</sub>; `102`<sub>h</sub> first creates it from its bank (`007A4A10`) |
| `200`<sub>h</sub>-`205`<sub>h</sub> | category volume, pitch, pause, resume and the two byte pairs |
| `300`<sub>h</sub> | applies an effect preset |
| `301`<sub>h</sub> | sets a bus value |

Reading past the element's total size prints "Event::Update exceeded TotalCommandSize" and ends the event.

### External parameters

`007B0F90` builds one `40`<sub>h</sub>-byte row per `expr` element at `02EAD3F8`, their count at `02EAD3EC`. `007B0E90(out, name)`
gives the ramped value of the row whose name matches, or -1; a switched sound reads its value through it
([Sound variations](sound-variations.md)). `007B1380` advances every row's ramp on each driver pass.

### The HCA mixer switch

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8` | h00 | 0 |
| `01`<sub>h</sub> | `u8` | channels | 16 |
| `02`<sub>h</sub> | `u16` | h02 | `16` |
| `04`<sub>h</sub> | `u32` | rate | 44,100 |
| `08`<sub>h</sub> | `u8` | enable | 0 |

`007A4D50` copies `+08`<sub>h</sub>, `+01`<sub>h</sub> and `+04`<sub>h</sub> into its parameters `+1C`<sub>h</sub>, `+18`<sub>h</sub> and `+14`<sub>h</sub> (`007A4F5F`-`007A4F6E`).
Only with `enable` set does `007AC4F0` build the HCA mixer voice (`007ACC6B`-`007ACC9B`). The engine renders at the
constant 48,000 (`007AC691`).

## Shipped data

| Chunk | Size | Holds |
|---|---:|---|
| `ctgr` | `A0`<sub>h</sub> | four categories: `dummy0` size 0, `music` 4, `se` 48, `voice` 8 |
| `bus ` | `50`<sub>h</sub> | one bus, `Master`, level 1.0, no sends, no effects |
| `mcr ` | `A0`<sub>h</sub> | three macros: one that only ends; one that refuses a new sound when one with the same key plays; one that, when two or more with the same key play, posts sound command `B`<sub>h</sub> with the value 0.1 on the first of them through `007A84A0` (`007B3D6F`-`007B3D7B`) |
| `epsp` | `10`<sub>h</sub> | no presets |
| `eps ` | `1E0`<sub>h</sub> | eleven sections; 1, 2, 3, 4, 9 and 10 hold one block each |
| `curv` | `50`<sub>h</sub> | one curve of two points |
| `expr` | `10`<sub>h</sub> | no parameters |
| `hcam` | `10`<sub>h</sub> | 16, 44,100, switch off |
| `evt ` | `10`<sub>h</sub> | no events |
| `ctgl` | `40`<sub>h</sub> | one layer, `default` |

The chunks follow the directory at `B0`<sub>h</sub> with no gaps and end at the file's end; `copySize` is the file's length.
Sections 5 and 7 of `eps ` each declare one preset of `10`<sub>h</sub> bytes, and those bytes are the headers of sections 6
and 8.

### The voice pools

The sum of the positive category sizes, 60, sizes the engine's pools (`007A4ED7`-`007A4EFD`, `007A5115`-`007A5160`):

| Pool | Size | Kept at |
|---|---:|---|
| sum + 32 | 92 | `02EAD4C0` |
| twice that | 184 | `02EAD5A0` |
| `min(184, 60h) + min(20h, 80h) + min(0, 20h)`, from the start block's `+20`<sub>h</sub>, `+24`<sub>h</sub> and `+28`<sub>h</sub> | 128 | the render block |

## Loader behaviour

1. Only the magic is checked. `copySize` is never compared with the file's length.
2. Header `+04`<sub>h</sub>, `+09`<sub>h</sub>-`+0B`<sub>h</sub> and entry `+04`<sub>h</sub>, `+06`<sub>h</sub>, `+0C`<sub>h</sub> are read by none of `007AE410`, `007B0F90`,
   the ten finders or the 16 reads of `02EAD3E0`.
3. No directory offset, element offset, bus index or send count is range-checked.
4. Only the curve and external-parameter element readers check the index (`007ADC51`, `007AE031`).
5. A missing chunk gives a null pointer. The `ctgr` and `bus ` users read it at once and fault (`007B104F`,
   `007AC69F`); `mcr ` and `epsp` fault when used (`007B3269`, `007ACDB3`); the others are skipped.

## Modding notes

- A category's size is the number of its sounds that can play at once; raising one also grows the shared pools.
- A `ctgr` with no elements stops the engine from starting (`007AAA66`), and a category that shares a missing one
  reads a null pointer (`007AA35A`).
- A `copySize` larger than the file reads past the buffer; a smaller one leaves later chunks outside the copy.
- Setting the `hcam` switch builds the HCA mixer voice with the file's 16 and 44,100.
- The shipped game has no preset to apply, but command `300`<sub>h</sub> with a negative index still resets the master bus.

## Related

- [Sound banks](sound-banks.md) - the bank files the engine plays.
- [Sound driver objects](sound-driver-objects.md) - the pools the category sizes set, and the category commands.
