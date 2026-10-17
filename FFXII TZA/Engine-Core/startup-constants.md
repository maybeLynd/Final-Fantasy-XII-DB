---
title: "Startup constants: the random seed, the frame-rate constant, the memory budget and the confirm button mapping"
kind: "system"
category: "Engine core"
addresses: "0022A0B0, 0022BDF0, 001EDDC0, 0017D8F0, 00229F10, 0022A4F0, 0017E210, 0017E270, 0017E410, 00314DE0, 00184960, 001EDEF0, 001EDE70, 0017D990, 0017D9D0, 00379CF0, 00863D30, 00584210, 0036D240, 00369D30, 0036D990, 00368A90, 0035EB70, 0022A770, 0022A4B0, 0037B3D0, 003692D0, 00369510, 008628E0, 00369650, 003696D0, 00259180, 003AC890, 002FC200, 00375120, 00382910, 004679C0, 00248410"
---

## What the player sees

Two launches of the game roll the same numbers until a save is loaded, after which they never
agree again. A player who sets the frame limit to 60 sees every authored duration keep its
wall-clock length. Whether Circle or Cross confirms is settled once, at start, into two masks every
menu reads. The game's whole working memory, a quarter of a gigabyte in eleven blocks, is claimed
before the first screen appears. None of it is revisited until the next launch.

## How it works

### The boot fixer

`0022A0B0(b, a)` runs once, from the manager-init burst of the application's init job
([game application](game-application.md)), with the two arguments the framework handed to the
archive mount. It runs these in order:

1. `0022BDF0(b, a)`: the frame-rate selection and the command line (below);
2. `02064AA4` = 0 (the shared stub's result); `01E02814` = the language index `0017E270()`;
   `01E0281C` = 10 (`0017E410`); `002AB7D0()`;
3. the confirm mapping: `01FD4A64` = whether DecideButton (`0017E210`, the settings object's
   `+64`<sub>h</sub>) is non-zero; the masks `01E0C2A0`/`01E0C2A4` = `4000`<sub>h</sub>/`2000`<sub>h</sub>, swapped to
   `2000`<sub>h</sub>/`4000`<sub>h</sub> when it is zero ([game settings](../Saving-Loading-And-Settings/game-settings.md));
4. `00184660([01E0280C])`, the PS2 emulation reset `0036D990` (the `vf00` image `01EF93F0` =
   `{0, 0, 0, 1}` and two log lines through `0017D280`), `0022CB90`, `0037DF90`, `0037E0F0`;
   `01FD4A78` = `1FE0000`<sub>h</sub>; `002DF9A0(language)`; `00184960(1)` (the time-base suppressor, below);
   `00862BD0(language)`; the build-id files (below);
5. a call to the return stub `0016D6A0` with `7D`<sub>h</sub> after `00184960(1)`, a compiled-out hook; two
   more such calls follow the state cells and precede `00266D10`;
6. the main state machine's cells: `02064AD2` = 0, `02064AD4` = 1.0, the state `02064AD3` = 0,
   the ticks-per-frame constant `02064ACC = 2 / [01DFE0B4]`, `02064AD1` = 0, `02064AC0`, `02064AC4`
   and `02064AC8` = 1.0 ([frame update order](frame-update-order.md));
7. `00368A90` (`02EC0B39` = 0, `02EC0B38` = `FF`<sub>h</sub>), then the memory budget (below);
8. `0037B390`, `00360370`, `00358510`, `00379D40`, `003692D0` (its byte result goes to
   `003694D0(byte, 0, 0)` after `0036D260`, `00368ED0`, `0036ECE0` and `00379D00`), `0032EAE0`,
   `0036FD70` (the stub returns 0, so always), `0036EFD0`, `0036D8B0`, a ret-stub call, the actor
   system `00266D10`, `0036F4D0`, `003325C0`, `00259180`;
9. the seed `00379CF0(11B9h)` (below); `00253970`, the spawn banks `002368D0`, `002EA520`,
   `00259DF0`, `0035B270` (the vibration slot reset, [vibration](../Controls-And-Input/vibration.md)), `00379E90`, `00379D20`, `0036E310`, `0037CCC0`, `0036FFF0`; the game-step
   count `02064AD0` = 0; a drain loop over `00364200` / `0032E040` / `0035EA30(0)` gated on
   `005C5230()` being non-zero never runs.

### The random seed

`00379CF0` is a five-byte thunk to `00863D30(seed)`, the Mersenne Twister seeder: with the first-use
latch `02EB4234` clear it seeds the 624-word state at `02EB3870` with `1571`<sub>h</sub> (5489, the library
default), sets the latch, and then seeds with the argument ([random number
generators](../Random-Numbers/random-number-generators.md)). Boot passes `11B9`<sub>h</sub> (4537),
a literal in the instruction stream: no clock, no entropy, no input. So the stream is identical
on every launch until a save is loaded.

The thunk's only other caller is the save-load normaliser `00584210`, which ends with
`_time64(NULL)` and seeds `(((low + 2B5A5h) * 21h + high) & 7FFFFFFFh) + [01FD4A80] * 600`,
`low` and `high` the two halves of the clock value. Loading a save therefore rerolls the generator
from the wall clock, not from the save; loading the same save twice does not give the same stream.

### The frame-rate constants

`0022BDF0(argc, argv)` reads FrameLimit (`0017D8F0`, the settings object's `+48`<sub>h</sub>), scans every
command-line argument for the eight bytes `"-nologo"` with its terminator (`00314DE0(1)` stores 1
at `022C2528` on a match; the loop does not stop at one), and calls `001EDDC0(FrameLimit == 1)`.

With 0 that arm begins a multimedia timer period (`timeGetDevCaps`, `timeBeginPeriod(wPeriodMin)`,
the period at `01F82E40`, `01F82E3C` = 1); with 1 it writes the time base, `01DFE0B8` = 2.0,
`01DFE0BC` = 0.5, `01F82E38` = 1 and `01DFE0B4` = 2, runs `0033F020` and ends any period begun.
Both arms then run `0032AE70`, `003333D0`, `00337A00` and `002BDA90`. Of these,
`00337A00` sets the formation angle step `02EC0F84` to `2 / (30 × [01DFE0B4])`
([battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).

`01DFE0B4` ships as 1 and has that one writer; its readers divide authored 30 fps frame counts by
it. The boot fixer then computes `02064ACC = 2 / [01DFE0B4]`, 2 at 30 fps and 1 at 60: the number
of pacer ticks the field frame waits per frame (`0035EC80([02064ACC], 0)`, an identical copy of
`0035EB70`, at the end of `0022A770`; the second argument is the stub's 0).

It has a second writer, the setter `00229F10`: the manager-unload reset `002695A0` (its only caller is the unload
`002628B0`) rewrites `2 / [01DFE0B4]`, and the verb `mainloopallsyncv` (`18F`<sub>h</sub>, `003464B0` →
`0026DB10`) stores its popped value divided by `[01DFE0B4]`, so the verb speaks in 30 fps ticks.

`00184960(mode)` sets the suppressor `01DFE0C0` to 1 (`001EDEF0`) and reads the mode flag
`01F82E38` (`001EDE70`): with the flag clear it keeps the suppressor and hands `mode` on; with it
set and `mode` not 1 it clears the suppressor; with `mode` 1 and `02092748` non-zero it runs the
`00229EA0` gate and clears the suppressor when the gate does not return 1, otherwise it keeps the
suppressor only while byte `+118`<sub>h</sub> of `001EBA40()` is zero. Every path then passes `mode` (1 on
the clearing paths and at boot) to `00798E90` and, with a render manager, to `005FEA50`.

### The confirm button and the language

`0022A4F0` is the only other writer of the two masks and `01FD4A64`; it is the Config screen's path
(`0017E6E0` and `0023E194`). The masks have about 90 read sites across the menus; the engine never
asks the setting again. `0017E270` turns the language string the settings object names
(`[01DF0030 + 8 * [01F82D20][0]]`) into an index: `jp` 10, `en` 1, `fr` 2, `de` 3, `it` 4, `es` 5,
`kr` 7, `ch` 8, `cn` 11, anything else 10; it is stored at `01E02814` and read by `00229E40`,
`00229E50` and twice more inside the boot fixer ([languages](../Saving-Loading-And-Settings/languages.md)).

### The build-id files

`0017D990` reads two text files through the resource loader (`001D6F20`, `001D6EE0`, `001D6FA0`):
`GameData/code_steam.txt` into `01F7F490` and `GameData/data.txt` into `01F7F4A0`, each as the
bytes from offset 7 of the file up to the first space (`strcspn`); a file that fails to load logs
`load failed!`.

### The memory budget

Eleven blocks are taken from the C runtime heap (`0036D240` is `malloc`), and nine are registered
as arenas with `00369D30(id, block, size, slotCount)`:

| Id | Block | Allocated | Registered size | Slots |
|---|---|---|---|---|
| 2 | `01FD49F8` | `1DC0010`<sub>h</sub> | `1DC0000`<sub>h</sub> (29.75 MiB) | `10`<sub>h</sub> |
| 3 | `01FD4A00` | `D20100`<sub>h</sub> | `D20000`<sub>h</sub> (13.12 MiB) | `100`<sub>h</sub> |
| 4 | `01FD4A08` | `100010`<sub>h</sub> | `100000`<sub>h</sub> (1 MiB) | `10`<sub>h</sub> |
| 5 | `01FD49F0` | `1C0100`<sub>h</sub> | `1C0000`<sub>h</sub> (1.75 MiB) | `100`<sub>h</sub> |
| 6 | `01FD4A10` | `6C00400`<sub>h</sub> | `6C00000`<sub>h</sub> (108 MiB) | `400`<sub>h</sub> |
| 7 | `01FD4A30` | `3000100`<sub>h</sub> | `3000000`<sub>h</sub> (48 MiB) | `100`<sub>h</sub> |
| 8 | `01FD4A38` | `2000100`<sub>h</sub> | `2000000`<sub>h</sub> (32 MiB) | `100`<sub>h</sub> |
| 9 | `01FD4A40` | `1200010`<sub>h</sub> | `1200000`<sub>h</sub> (18 MiB) | `10`<sub>h</sub> |
| 11 | `01FD4A18` | `400100`<sub>h</sub> | `400000`<sub>h</sub> (4 MiB) | `100`<sub>h</sub> |
| none | `01FD4A20` | `80000`<sub>h</sub> | not registered | |
| none | `01FD4A90` | `100000`<sub>h</sub> | not registered | |

Every allocation is its registered size plus the slot count in bytes.

The registrar (ids below
15) records the arena in its table at `022D7FD0` (stride `A8`<sub>h</sub>), zeroes the block's first 64
bytes and writes the arena's name there (`sprintf`), lays a bitmap and a word table at the head of
the block (64-byte aligned, sized from the registered size), then the handle slots: `slotCount`
records of 16 bytes chained by index when the count is non-zero, and finally the arena's free
region, half-split, handed to `0036A490` ([memory and
allocation](../Compiler-And-C-Runtime/memory-and-allocation.md)).

Id 10 is never registered; `0037B3D0` re-sizes id 11 when `02ADD931` differs from `02ADD930`,
freeing the block (`0036D250`) and registering a new one of `3C0000`<sub>h</sub> when `02ADD930` is 3, else
`400000`<sub>h</sub>; ids 12 to 14 are registered elsewhere. The unregistered 1 MiB block at `01FD4A90` is the per-model oscillator table; the
0.5 MiB block at `01FD4A20` is stored and never read. `0036B060(id)` returns an arena's table
entry, `022D7FD0 + id × A8h`, or null for an id of 15 or more.

### The PS2 boot shims

Step 8 replays the PlayStation 2 boot against stubs. `003692D0` walks seven module records at
`01EF9290` (stride `18`<sub>h</sub>, the first `sio2man.irx`). `00369510(name, out, host, demo)` builds each
path: the prefix `host0:/image/FF12/modules/` when `host` is set, another prefix otherwise, `DEMO/`
when `demo` is set, then the name, upper-cased with `/` turned into `\` unless `host` is set.

The loader `008628E0` stores 0 through its fourth argument and returns 0, so every module counts as
loaded and the walk sets `022D7FCC |= 1 << b` for the record's signed byte `b` at `+12`<sub>h</sub> when `b`
is not negative (`003694A5`-`003694B8`).

Before the walk, `00369650` performs the I/O processor
reset with `ioprp300.img` (`01EF9360`): only stub calls, `003691E0` and `0046E000`, which also
sets `02CA6074` and `02CA6114` to -1. `004746C0` is four stub calls. After the walk `003692D0`
runs the sound state reset `002DE360` (`00369451`), which among its stores sets the spatial-sound
behind ratio `0215EFD0` ([spatial sound](../Sound-And-Music/spatial-sound.md)).

`00474680`, called first (`00369306`), makes two stub calls (`0016D6A0`) and copies the first eight bytes of the
`memset` import stub `00861EC0` to `02CA6C88` and `02CA6C8C`; the only reference to `02CA6C88` is that write
(`0047469E`).

`0036FD70` clears `02AD9E00` and runs `003696D0`, which releases the three handles at `022D7FC0` to
`022D7FC8` (retrying while the stub reports busy) and sets each to -1. `003694D0` fills the two
256-byte tables `022C5AF0` (`0032EAF0`) and `022C59F0` (`0032EB10`, which also sets bit 7 of its
byte `1F`<sub>h</sub>) with -1 for a non-zero argument, else 0.

### The subsystem resets

The step-8 calls `00266D10` and `00259180` return the field's fixed tables to their boot state.
`00259180` runs under arena 8 (`0036C1D0(8)` … `0036C140`, which pops the arena stack at
`022D89C0`); the ones that allocate select arena 6 or 9 the same way and allocate (`0036A100`) only
when their pointer is null:

| Reset | What it does |
|---|---|
| `003CD6E0` | allocates `800`<sub>h</sub> at `02B47790` and `2800`<sub>h</sub> at `02B47798`; clears 32 and 128 records in them |
| `003AC890` | allocates `3800`<sub>h</sub> at `02B3F528`; `02B3F518` = 1.0; `003ABB60` clears its 128 records, takes the first as a type-7 record with the next serial from `02B3F504` (1 to `FFFFFF`<sub>h</sub>), and makes it the list `02B3F508` / `02B3F510`; per frame `003AC870` resets the factor `02B3F51C` to 1.0 and `003AC900(f)` multiplies it by f |
| `003B4790` | allocates `1800`<sub>h</sub> at `02B404E0`; sets the pairs (3, `00D11520`) and (5, `00D11538`); clears 64 records |
| `00376A80` | clears `02ADBB30`, `02ADBB34` and the first word of 8 records at `02ADBB40` (stride `90`<sub>h</sub>) |
| `0024C970` | clears `1670`<sub>h</sub> bytes from `020910A0`; sets the five u16 `0209215E` to `02092166` to `3FF`<sub>h</sub> and `020926F4` = `4003C`<sub>h</sub>; under arena 8 clears the four soft-particle tables and reads them and `softparticle_bg.csv` ([Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)); `02092700` = −1 |
| `003D7F10` | clears a word in each of 32 records from `02EBBA00` (stride `84`<sub>h</sub>) |
| `003D8C30` | points `02B4E3D0` to `02B4E3E8` at the four data blocks `01EFE3A0`, `01EFE510`, `01EFE690`, `01EFE810` and runs `0050C450` over each; `02B4D7B8` = 1.0; clears 32 records |
| `003773C0`, `003B3E10` | clear 128 records ending at `02ADCFC0`, and the 8-byte records from `02EBCC80` to `02EBCD84` |
| `00259250` | resets the block at `02096810` to `02096D28` (white at `02096810`, 0.5 at `020968BC`, `80808080`<sub>h</sub> at `020968B0`) |
| `0039CD50` | allocates `20000`<sub>h</sub> at `02AEED50`; `0039AED0(2048.0, 2048.0)` and `0039AF20(512.0)`, which store `02EBEFFC`, `02EBEFF8`, `02EBF000` and copy 64 bytes from `02AEDD30` to `02AEE5A0`; `02AEE910` = 8 |
| `003A3670` | under arena 9, and every time rather than only when null: allocates `190000`<sub>h</sub> at `02F8F2F8`, `C8028`<sub>h</sub> at `02F8F300`, and `[02F8F2C0]` = `0036B080(9)` bytes at `02F8F2D0` (also `02F8F308`), with `02F8F2D8` = `[02F8F2D0]` + (s / 16) × 16 for s = `[02F8F2C0]`, the division signed and toward zero; `02F8F2E0` = `[01FD4A78]`; clears `02F8F2C5`, `02F8F2C6`, `02F8F2CC`, `02F8F2E8`, `02F8F2F0` and the low two bits of `02F8F310` |
| `00375120` | clears 32 records at `02EBFA48`; writes a 16-step grey ramp (step `11`<sub>h</sub>, alpha `80`<sub>h</sub>) at `02ADB6E0` and eight 32-step ramps after it |
| `002FC200` | chains the 48 records of `38`<sub>h</sub> bytes at `02EC32E0` into a list (`02EC3D70`); clears `02EC19C0` (`1000`<sub>h</sub> bytes) and copies 401 five-bit values from `01EEBB10` into it, one per 8 bytes |
| `003B0660` | zeroes `+00`<sub>h</sub>-`+03`<sub>h</sub>, `+08`<sub>h</sub>-`+0F`<sub>h</sub> and `+11`<sub>h</sub> of the 36 records of `18`<sub>h</sub> bytes from `02EBEC00` and clears the low three bits of each `+13`<sub>h</sub>; clears bit 0 of `02EBEF68` and the word `02EBEF60`; runs `0024C460` for 5, 6 and 9; then, when `0032E400(10)` returns n > 0, calls `0032E620(10, 0, [01FD4A30], n, 0)` and `0032E520(0)`, passes a zeroed `890`<sub>h</sub>-byte request with type 5 to `0024B3A0`, and calls `003EDAD0([01FD4A30], its word +Ch)` |
| `003B16B0` | clears the 32 records of `30`<sub>h</sub> at `02EBE5E0` and `02EBEBE0` / `02EBEBE4` |
| `0026F9F0` | fills 96 bytes at `02F8F23C` with 3 and sets `02F8F29C` = `100`<sub>h</sub> |
| `003B3160` | links two lists of 32 records of `38`<sub>h</sub> bytes, at `02EBCD80` (head `02EBDB88`) and `02EBD480` (head `02EBDBA0`): each record's first word takes its index and `30000000`<sub>h</sub>, `+20`<sub>h</sub> points to the next and `+28`<sub>h</sub> to the previous; clears `02EBDB80`, `02EBDB90`, `02EBDB98`, `02EBDBA8`, `02EBDBB0`, `02EBDBB4`; then `0024C550(3)` |
| `003CBFF0(02096ED0)` | (call at `002591F2`) clears `+C0`<sub>h</sub> of the camera `02096ED0` and runs `003CBBE0` on it |
| `0025A600(0.1, 1000.0)` | stores the two floats `02098DE0` / `02098DE4` |

After the last call it stores three words directly: `022D92E0` = `01EF93E8` = `458DC800`<sub>h</sub> (4537.0)
and `022D9138` = 1 (`0025920C`, `00259216`, `00259220`). They are the presentation generator's last
sample, its state and its enable word ([Random number generators](../Random-Numbers/random-number-generators.md)).

`00266D10`, the actor-system reset, runs among others `00314940` (`022C2544` = 1.0), `002556F0`
(five groups of four `2E0`<sub>h</sub>-byte records from `02092810`, plus one more, each through `003CBFF0`;
`020964FC` = 1.0, `02096514` = `20`<sub>h</sub>), `002F1A00` (zeroes `022BE7C0`, `022BE7C8`, `022BE7D0`),
`003DD7E0`, `003DDD10`, `003DE710`, `003DF030`, `003E7DF0`, `003EBAB0` and `003EBE40`.

Those last seven number and clear the tables from `02B581A0` to `02B5EC88`: 5 × 16 slots, four records with
`13602`<sub>h</sub> and colour `80FFFFFF`<sub>h</sub>, 16 records, 5 × 8 slots, 32 records numbered `20`<sub>h</sub> to `3F`<sub>h</sub>
with a 28-node list, and eight pairs of 0 and `100`<sub>h</sub>.

`0036F4D0` runs `00382910`, which clears 8 records at `02AED700` (stride `E0`<sub>h</sub>) and builds two
view records with `004679C0(record, width, height)`: `02AED4A0` for the frame size
`[022D8EAC]` × `[022D8EB4]` and `02AED500` for 2000 × 2000.

A view record holds the integer size at `+44`<sub>h</sub> / `+48`<sub>h</sub>, the depth limits `near` = 1024 and `far` =
16,776,191 at `+4C`<sub>h</sub> / `+50`<sub>h</sub>, and `00229D20()` at `+40`<sub>h</sub>. It sets `+00h = width × 0.5` and
`+14h = height × -0.5` (`00467A0F`-`00467A26`), the depth scale `+28h = (far - near) × -0.5` and
offset `+38h = (far + near) × 0.5` (`00467A2B`-`00467A62`), 2048 at `+30`<sub>h</sub> / `+34`<sub>h</sub> as the
screen offset and 1.0 at `+3C`<sub>h</sub>.

Step 4's `00184660` ends with `00248410`, which sets `0208ECC0` / `0208ECC4` to minus half of
`[01E0C1D8]` / `[01E0C1DC]` and writes that size into the four objects at `0208EA20` to `0208EA38`
(`+9C`<sub>h</sub> / `+9E`<sub>h</sub>), and `0024B100`, which copies the size into the halfwords `01E0C1D4` /
`01E0C1D6`.

## Layouts

```
globals written by the boot fixer
02EB4234  u8    generator first-use latch        02EB3870  u32[624] Mersenne Twister state
01DFE0B4  u32   frame base 1 or 2               01DFE0B8 / 01DFE0BC  f32 time base 1.0 / 2.0 and 1.0 / 0.5
01F82E38  u32   60 fps mode flag                 01DFE0C0  u32  the mode suppressor
01F82E3C  u8    timer period begun               01F82E40  u32  the period
02064ACC  u32   pacer ticks per frame: 2 / [01DFE0B4]
01E0C2A0  u32   confirm mask                     01E0C2A4  u32  cancel mask       01FD4A64 u32 DecideButton non-zero
01E02814  u32   language index                   01E0281C  u32  10
01F7F490 / 01F7F4A0  the code_steam.txt and data.txt ids
01FD49F0 .. 01FD4A40, 01FD4A18, 01FD4A20, 01FD4A90  the eleven block pointers
02064AA4, 02064AC0 .. 02064AD4  the main state machine's cells     01FD4A78 u32 0x1FE0000
022C2528  u32   the -nologo flag                 022D7FD0  arena table, 0xA8 per id, 15 ids
```

## Shipped data

| Fact | Value |
|---|---|
| default seed, boot seed | `1571`<sub>h</sub> (5489), `11B9`<sub>h</sub> (4537) |
| reload seed | `(((low + 2B5A5h) * 21h + high) & 7FFFFFFFh) + [01FD4A80] * 600` from `_time64` |
| time base at 60 fps | `01DFE0B4` 2, `01DFE0B8` 2.0 (`01CEBC08`), `01DFE0BC` 0.5 (`01CEBB70`) |
| ticks per frame | 2 at 30 fps, 1 at 60 |
| masks | confirm `4000`<sub>h</sub>, cancel `2000`<sub>h</sub>; swapped when DecideButton is 0 |
| registered arenas | 255.6 MiB in nine; 257.1 MiB allocated in eleven |
| command line | only `-nologo` is honoured, as an exact eight-byte match |

## Operations

Once per launch, inside the init job, before the startup latch closes: the frame-rate selection,
the masks, the language, the state-machine cells, the eleven allocations and nine registrations,
the one-time initialisers of every subsystem, and the seed. The field frame reads the ticks-per-frame
constant every frame; the time base is read wherever a frame count is converted.

## State

The generator latch and state; the time-base triple, the mode flag and its suppressor; the
ticks-per-frame constant; the masks and the DecideButton flag; the language index; the block
pointers and the arena table.

## Modding notes

- Determinism from boot holds for the Mersenne Twister only; the loot generator is a separate
  counter-seeded LCG ([which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md)),
  and a save load reseeds the Twister from the clock.
- A port must reproduce the 4537 seed and the exact reload formula to match the shipped stream.
- The time base is a published triple that over a hundred readers divide or multiply by; changing
  FrameLimit at run time without rewriting all four cells leaves the engine inconsistent.
- The masks are read as masks against the pad word; swapping them is the whole of the confirm
  button setting.
- The arenas are fixed at boot; only id 11 is re-sized, by `0037B3D0`.

## Related

- [Game application](game-application.md): the init job that calls the boot fixer.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and DecideButton in the
  settings object.
- [Random number generators](../Random-Numbers/random-number-generators.md): the Mersenne
  Twister and its seeders.
- [Frame update order](frame-update-order.md): the state machine whose cells are initialised here.
