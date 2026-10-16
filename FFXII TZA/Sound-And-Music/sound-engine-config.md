---
title: "Sound engine configuration: the start-up file that sets the sound categories, the master bus, the macros and the effect presets"
kind: "format"
category: "Sound and music"
summary: "The file sead.win.config: where it is loaded and how the engine copies it whole, its header and chunk directory, the ten chunks with their layouts and the code that reads each field, the category sizes that size the engine's voice pools, the master bus, the three macros, the effect presets and the HCA mixer switch, the shipped values, and what a changed or missing chunk does."
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
3. It fills an initialisation block with the buffer at `+0x38` and calls the engine start `007A4D50` (`00210889`),
   whose result it does not test.
4. It frees its buffer (`002108F1`).

### The engine's copy

`007A4D50` calls `007B0F90` (`007A4E79`):

1. `007AE410` checks the magic `scnf` (`007B0FA8`); a mismatch makes the engine start return -1.
2. It allocates the header's `+0x0C` bytes and copies that many bytes of the file to the block it keeps at `02EAD3E0`
   (`007B0FE8`-`007B1005`).
3. It sums the positive category sizes into `02EAD3E8` (`007B103C`-`007B108A`) and builds the external-parameter
   rows (`007B10B4`-`007B1145`).

All 16 later reads of `02EAD3E0`, in 15 functions, pass it to a chunk finder, so every chunk is read from the copy.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | magic | "scnf" |
| `04` | `u16` | h04 | 0 |
| `06` | `u16` | dirOffset | `0x10` |
| `08` | `u8` | chunkCount | 10 |
| `09` | `u8[3]` | h09 | 0 |
| `0C` | `u32` | copySize | bytes the engine copies; 1,264 |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `char[4]` | tag | the chunk's tag |
| `04` | `u16` | e04 | 0 |
| `06` | `u16` | e06 | `0x10` |
| `08` | `u32` | offset | from the start of the file |
| `0C` | `u32` | e0C | 0 |

Each finder walks `chunkCount` entries from `dirOffset` and compares the tag with its entry in the tag table at
`01CB4928` (`007ADB5A`); a tag not there gives a null chunk. A table chunk starts with a `u8` version, a `u16` at
`+0x02` that locates its element-offset table and a `u16` element count at `+0x04`.

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
| `00` | `u8` | version | 2 |
| `01` | `u8` | c01 | the element index |
| `02` | `u16` | nameAt | offset of the name, `0x10` |
| `04` | `i16` | size | 0 none; above 0 that many sound slots; below 0 shares category -size |
| `06` | `u16` | c06 | the name length |
| `10` | `char` | name | the category name, inline, `+0x06` characters long |

`007AAA40` refuses a chunk with no elements (`007AAA66`). A size of 0 leaves the category empty (`007AAB11`), a
positive size allocates that many slots (`007AA2E3`), and a negative one binds it to another category
(`007AABD1`, `007AA342`). The name goes to the category object's `+0x70` (`007AA137`-`007AA156`). `ctgl` gives only
its element count: each category gets that many plus one volume ramps (`007AAAB2`, `007AA15A`).

### The bus

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | version | 2 |
| `01` | `u8` | busIndex | 0 is the root bus |
| `02` | `u16` | nameAt | `0x20` |
| `04` | `i8` | send0 | a bus to send to, or -1 |
| `05` | `u8` | effectCount | effects on the bus |
| `06` | `u8[4]` | sendTargets | more send buses |
| `0A` | `u8` | sendCount | how many of them |
| `0B` | `u8` | nameLength | places the effect table |
| `0C` | `f32` | level | the bus volume |
| `10` | `f32[4]` | sendLevels | one per send |
| `20` | `char` | name | the bus name, inline, `+0x0B` characters long |

`007AC4F0` builds the buses: `+0x01` picks the slot (`007AC770`), the root bus takes `+0x0C` as its level
(`007ACAAE`, `007ACAE0`), and other buses read their sends (`007AC7AD`-`007AC822`) and effects (`007AC83A`). The
effect table is at `nameAt + ((nameLength + 0x10) & 0xF0)` (`007ADA3F`), and an effect's type byte `+0x01` picks its
class through the jump table at `007ACCF0` (`007AC883`).

| Type | Effect class |
|---:|---|
| 0 | `EmptyEffect` |
| 1 | `SurroundReverb` |
| 2 | `Compressor` |
| 3 | `Filter` |
| 4 | `SideChainInput` |
| 5 | `SimpleFilter` |
| 6 | `Flanger` |
| 7 | `GranularPitchShift` |
| 8 | `HilbertFilter` |
| 10 | `BuildReverb` |

### Macros

`007B31A0` runs macro number N, from the sound's own record (`007B3201`-`007B3226`), when N is below the chunk's count
(`007B3269`). A macro record's `u16` at `+0x02` is the offset of its instruction stream (`007B32D0`). Each instruction
has a header length at `+0x01`, an opcode at `+0x02` and a payload length at `+0x03` (`007B42CF`, `007B33B6`,
`007B42E4`). 22 opcodes have handlers:

| Opcode | Handler | Does |
|---|---|---|
| `0x01` | `007B33DF` | ends the macro |
| `0x10` | `007B33E9` | a step of its own, before the filters |
| `0x11`-`0x18` | from `007B4374` | filter the playing sounds; `0x12` compares a sound's key, or with mode byte `+5` set to 1 this sound's key minus the other's, with `==`, `!=`, `>`, `>=`, `<` or `<=` (`007B3555`); the shipped macros use mode 1 against 0, the same key |
| `0xA0` | `007B3D1D` | when the count of playing sounds passes the test, acts on all, the first, the quietest or the loudest of them with a value |
| `0xA1` | `007B3F2F` | when the count passes the test, refuses the new sound |
| `0xA2`-`0xAB` | from `007B4374` | other actions |

### Effect presets

`007ACD30(mixer, index, fade)` applies preset `index` of `epsp`, from the sound command `0x300` (`007EEF59`). An index
at or above the count logs `[sead][!!error!!]set effect preset number invalid [%d]` (`007ACDB3`). A negative index
passes that test and resets every bus to its `bus ` chunk values and re-enables every effect (`007ACE32`-`007ACFA8`).
A preset's records set a bus ramp (`007AD09E`-`007AD0A9`) or switch an effect on or off, and an effect's settings
come from `eps ` through `007ADDC0`, one section per effect type, with block sizes from `01CB49A0` and `01CB4990`.

### The HCA mixer switch

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | h00 | 0 |
| `01` | `u8` | channels | 16 |
| `02` | `u16` | h02 | `0x10` |
| `04` | `u32` | rate | 44,100 |
| `08` | `u8` | enable | 0 |

`007A4D50` copies `+0x08`, `+0x01` and `+0x04` into its parameters `+0x1C`, `+0x18` and `+0x14` (`007A4F5F`-`007A4F6E`).
Only with `enable` set does `007AC4F0` build the HCA mixer voice (`007ACC6B`-`007ACC9B`). The engine renders at the
constant 48,000 (`007AC691`).

## Shipped data

| Chunk | Size | Holds |
|---|---:|---|
| `ctgr` | `0xA0` | four categories: `dummy0` size 0, `music` 4, `se` 48, `voice` 8 |
| `bus ` | `0x50` | one bus, `Master`, level 1.0, no sends, no effects |
| `mcr ` | `0xA0` | three macros: one that only ends; one that refuses a new sound when one with the same key plays; one that, when two or more with the same key play, posts sound command `0xB` with the value 0.1 on the first of them through `007A84A0` (`007B3D6F`-`007B3D7B`) |
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

The sum of the positive category sizes, 60, sizes the engine's pools (`007A4ED7`-`007A4EFD`, `007A5115`-`007A5160`):

| Pool | Size | Kept at |
|---|---:|---|
| sum + 32 | 92 | `02EAD4C0` |
| twice that | 184 | `02EAD5A0` |
| `min(184, 0x60) + min(0x20, 0x80) + min(0, 0x20)`, from the start block's `+0x20`, `+0x24` and `+0x28` | 128 | the render block |

## Loader behaviour

1. Only the magic is checked. `copySize` is never compared with the file's length.
2. Header `+0x04`, `+0x09`-`+0x0B` and entry `+0x04`, `+0x06`, `+0x0C` are read by none of `007AE410`, `007B0F90`,
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
- The shipped game has no preset to apply, but command `0x300` with a negative index still resets the master bus.

## Related

- [Sound banks](sound-banks.md) - the bank files the engine plays.
