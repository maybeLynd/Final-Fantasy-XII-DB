---
title: "Startup constants: the random seed, the frame-rate constant, the memory budget and the confirm button mapping"
kind: "system"
category: "Engine core"
addresses: "0x0022A0B0, 0x0022BDF0, 0x001EDDC0, 0x0017D8F0, 0x00229F10, 0x0022A4F0, 0x0017E210, 0x0017E270, 0x0017E410, 0x00314DE0, 0x00184960, 0x001EDEF0, 0x001EDE70, 0x0017D990, 0x0017D9D0, 0x00379CF0, 0x00863D30, 0x00584210, 0x0036D240, 0x00369D30, 0x0036D990, 0x00368A90, 0x0035EB70, 0x0022A770, 0x0022A4B0, 0x0037B3D0, 0x003692D0, 0x00369510, 0x008628E0, 0x00369650, 0x003696D0, 0x00259180, 0x003AC890, 0x002FC200, 0x00375120, 0x00382910, 0x004679C0, 0x00248410"
---

## What the player sees

Two launches of the game roll the same numbers until a save is loaded, after which they never
agree again. A player who sets the frame limit to 60 sees every authored duration keep its
wall-clock length. Whether Circle or Cross confirms is settled once, at start, into two masks every
menu reads. The game's whole working memory, a quarter of a gigabyte in eleven blocks, is claimed
before the first screen appears. None of it is revisited until the next launch.

## How it works

### The boot fixer

`0x0022A0B0(b, a)` runs once, from the manager-init burst of the application's init job
([game application](game-application.md)), with the two arguments the framework handed to the
archive mount. It runs these in order:

1. `0x0022BDF0(b, a)`: the frame-rate selection and the command line (below);
2. `0x02064AA4` = 0 (the shared stub's result); `0x01E02814` = the language index `0x0017E270()`;
   `0x01E0281C` = 10 (`0x0017E410`); `0x002AB7D0()`;
3. the confirm mapping: `0x01FD4A64` = whether DecideButton (`0x0017E210`, the settings object's
   `+0x64`) is non-zero; the masks `0x01E0C2A0`/`0x01E0C2A4` = `0x4000`/`0x2000`, swapped to
   `0x2000`/`0x4000` when it is zero ([game settings](../Saving-Loading-And-Settings/game-settings.md));
4. `0x00184660([0x01E0280C])`, the PS2 emulation reset `0x0036D990` (the `vf00` image `0x01EF93F0` =
   `{0, 0, 0, 1}` and two log lines through `0x0017D280`), `0x0022CB90`, `0x0037DF90`, `0x0037E0F0`;
   `0x01FD4A78` = `0x1FE0000`; `0x002DF9A0(language)`; `0x00184960(1)` (the time-base suppressor, below);
   `0x00862BD0(language)`; the build-id files (below);
5. a call to the return stub `0x0016D6A0` with `0x7D` after `0x00184960(1)`, a compiled-out hook; two
   more such calls follow the state cells and precede `0x00266D10`;
6. the main state machine's cells: `0x02064AD2` = 0, `0x02064AD4` = 1.0, the state `0x02064AD3` = 0,
   the ticks-per-frame constant `0x02064ACC = 2 / [0x01DFE0B4]`, `0x02064AD1` = 0, `0x02064AC0`, `0x02064AC4`
   and `0x02064AC8` = 1.0 ([frame update order](frame-update-order.md));
7. `0x00368A90` (`0x02EC0B39` = 0, `0x02EC0B38` = `0xFF`), then the memory budget (below);
8. `0x0037B390`, `0x00360370`, `0x00358510`, `0x00379D40`, `0x003692D0` (its byte result goes to
   `0x003694D0(byte, 0, 0)` after `0x0036D260`, `0x00368ED0`, `0x0036ECE0` and `0x00379D00`), `0x0032EAE0`,
   `0x0036FD70` (the stub returns 0, so always), `0x0036EFD0`, `0x0036D8B0`, a ret-stub call, the actor
   system `0x00266D10`, `0x0036F4D0`, `0x003325C0`, `0x00259180`;
9. the seed `0x00379CF0(0x11B9)` (below); `0x00253970`, the spawn banks `0x002368D0`, `0x002EA520`,
   `0x00259DF0`, `0x0035B270` (the vibration slot reset, [vibration](../Controls-And-Input/vibration.md)), `0x00379E90`, `0x00379D20`, `0x0036E310`, `0x0037CCC0`, `0x0036FFF0`; the game-step
   count `0x02064AD0` = 0; a drain loop over `0x00364200` / `0x0032E040` / `0x0035EA30(0)` gated on
   `0x005C5230()` being non-zero never runs.

### The random seed

`0x00379CF0` is a five-byte thunk to `0x00863D30(seed)`, the Mersenne Twister seeder: with the first-use
latch `0x02EB4234` clear it seeds the 624-word state at `0x02EB3870` with `0x1571` (5489, the library
default), sets the latch, and then seeds with the argument ([random number
generators](../Random-Numbers/random-number-generators.md)). Boot passes `0x11B9` (4537),
a literal in the instruction stream: no clock, no entropy, no input. So the stream is identical
on every launch until a save is loaded.

The thunk's only other caller is the save-load normaliser `0x00584210`, which ends with
`_time64(NULL)` and seeds `(((low + 0x2B5A5) * 0x21 + high) & 0x7FFFFFFF) + [0x01FD4A80] * 600`,
`low` and `high` the two halves of the clock value. Loading a save therefore rerolls the generator
from the wall clock, not from the save; loading the same save twice does not give the same stream.

### The frame-rate constants

`0x0022BDF0(argc, argv)` reads FrameLimit (`0x0017D8F0`, the settings object's `+0x48`), scans every
command-line argument for the eight bytes `"-nologo"` with its terminator (`0x00314DE0(1)` stores 1
at `0x022C2528` on a match; the loop does not stop at one), and calls `0x001EDDC0(FrameLimit == 1)`.

With 0 that arm begins a multimedia timer period (`timeGetDevCaps`, `timeBeginPeriod(wPeriodMin)`,
the period at `0x01F82E40`, `0x01F82E3C` = 1); with 1 it writes the time base, `0x01DFE0B8` = 2.0,
`0x01DFE0BC` = 0.5, `0x01F82E38` = 1 and `0x01DFE0B4` = 2, runs `0x0033F020` and ends any period begun.
Both arms then run `0x0032AE70`, `0x003333D0`, `0x00337A00` and `0x002BDA90`. Of these,
`0x00337A00` sets the formation angle step `0x02EC0F84` to `2 / (30 × [0x01DFE0B4])`
([battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).

`0x01DFE0B4` ships as 1 and has that one writer; its readers divide authored 30 fps frame counts by
it. The boot fixer then computes `0x02064ACC = 2 / [0x01DFE0B4]`, 2 at 30 fps and 1 at 60: the number
of pacer ticks the field frame waits per frame (`0x0035EC80([0x02064ACC], 0)`, an identical copy of
`0x0035EB70`, at the end of `0x0022A770`; the second argument is the stub's 0).

It has a second writer, the setter `0x00229F10`: the manager-unload reset `0x002695A0` (its only caller is the unload
`0x002628B0`) rewrites `2 / [0x01DFE0B4]`, and the verb `mainloopallsyncv` (`0x18F`, `0x003464B0` →
`0x0026DB10`) stores its popped value divided by `[0x01DFE0B4]`, so the verb speaks in 30 fps ticks.

`0x00184960(mode)` sets the suppressor `0x01DFE0C0` to 1 (`0x001EDEF0`) and reads the mode flag
`0x01F82E38` (`0x001EDE70`): with the flag clear it keeps the suppressor and hands `mode` on; with it
set and `mode` not 1 it clears the suppressor; with `mode` 1 and `0x02092748` non-zero it runs the
`0x00229EA0` gate and clears the suppressor when the gate does not return 1, otherwise it keeps the
suppressor only while byte `+0x118` of `0x001EBA40()` is zero. Every path then passes `mode` (1 on
the clearing paths and at boot) to `0x00798E90` and, with a render manager, to `0x005FEA50`.

### The confirm button and the language

`0x0022A4F0` is the only other writer of the two masks and `0x01FD4A64`; it is the Config screen's path
(`0x0017E6E0` and `0x0023E194`). The masks have about 90 read sites across the menus; the engine never
asks the setting again. `0x0017E270` turns the language string the settings object names
(`[0x01DF0030 + 8 * [0x01F82D20][0]]`) into an index: `jp` 10, `en` 1, `fr` 2, `de` 3, `it` 4, `es` 5,
`kr` 7, `ch` 8, `cn` 11, anything else 10; it is stored at `0x01E02814` and read by `0x00229E40`,
`0x00229E50` and twice more inside the boot fixer ([languages](../Saving-Loading-And-Settings/languages.md)).

### The build-id files

`0x0017D990` reads two text files through the resource loader (`0x001D6F20`, `0x001D6EE0`, `0x001D6FA0`):
`GameData/code_steam.txt` into `0x01F7F490` and `GameData/data.txt` into `0x01F7F4A0`, each as the
bytes from offset 7 of the file up to the first space (`strcspn`); a file that fails to load logs
`load failed!`.

### The memory budget

Eleven blocks are taken from the C runtime heap (`0x0036D240` is `malloc`), and nine are registered
as arenas with `0x00369D30(id, block, size, slotCount)`:

| Id | Block | Allocated | Registered size | Slots |
|---|---|---|---|---|
| 2 | `0x01FD49F8` | `0x1DC0010` | `0x1DC0000` (29.75 MiB) | `0x10` |
| 3 | `0x01FD4A00` | `0xD20100` | `0xD20000` (13.12 MiB) | `0x100` |
| 4 | `0x01FD4A08` | `0x100010` | `0x100000` (1 MiB) | `0x10` |
| 5 | `0x01FD49F0` | `0x1C0100` | `0x1C0000` (1.75 MiB) | `0x100` |
| 6 | `0x01FD4A10` | `0x6C00400` | `0x6C00000` (108 MiB) | `0x400` |
| 7 | `0x01FD4A30` | `0x3000100` | `0x3000000` (48 MiB) | `0x100` |
| 8 | `0x01FD4A38` | `0x2000100` | `0x2000000` (32 MiB) | `0x100` |
| 9 | `0x01FD4A40` | `0x1200010` | `0x1200000` (18 MiB) | `0x10` |
| 11 | `0x01FD4A18` | `0x400100` | `0x400000` (4 MiB) | `0x100` |
| none | `0x01FD4A20` | `0x80000` | not registered | |
| none | `0x01FD4A90` | `0x100000` | not registered | |

Every allocation is its registered size plus the slot count in bytes.

The registrar (ids below
15) records the arena in its table at `0x022D7FD0` (stride `0xA8`), zeroes the block's first 64
bytes and writes the arena's name there (`sprintf`), lays a bitmap and a word table at the head of
the block (64-byte aligned, sized from the registered size), then the handle slots: `slotCount`
records of 16 bytes chained by index when the count is non-zero, and finally the arena's free
region, half-split, handed to `0x0036A490` ([memory and
allocation](../Compiler-And-C-Runtime/memory-and-allocation.md)).

Id 10 is never registered; `0x0037B3D0` re-sizes id 11 when `0x02ADD931` differs from `0x02ADD930`,
freeing the block (`0x0036D250`) and registering a new one of `0x3C0000` when `0x02ADD930` is 3, else
`0x400000`; ids 12 to 14 are registered elsewhere. The unregistered 1 MiB block at `0x01FD4A90` is the per-model oscillator table; the
0.5 MiB block at `0x01FD4A20` is stored and never read. `0x0036B060(id)` returns an arena's table
entry, `0x022D7FD0 + id × 0xA8`, or null for an id of 15 or more.

### The PS2 boot shims

Step 8 replays the PlayStation 2 boot against stubs. `0x003692D0` walks seven module records at
`0x01EF9290` (stride `0x18`, the first `sio2man.irx`). `0x00369510(name, out, host, demo)` builds each
path: the prefix `host0:/image/FF12/modules/` when `host` is set, another prefix otherwise, `DEMO/`
when `demo` is set, then the name, upper-cased with `/` turned into `\` unless `host` is set.

The loader `0x008628E0` stores 0 through its fourth argument and returns 0, so every module counts as
loaded and the walk sets `0x022D7FCC |= 1 << b` for the record's signed byte `b` at `+0x12` when `b`
is not negative (`0x003694A5`-`0x003694B8`).

Before the walk, `0x00369650` performs the I/O processor
reset with `ioprp300.img` (`0x01EF9360`): only stub calls, `0x003691E0` and `0x0046E000`, which also
sets `0x02CA6074` and `0x02CA6114` to -1. `0x004746C0` is four stub calls. After the walk `0x003692D0`
runs the sound state reset `0x002DE360` (`0x00369451`), which among its stores sets the spatial-sound
behind ratio `0x0215EFD0` ([spatial sound](../Sound-And-Music/spatial-sound.md)).

`0x00474680`, called first (`0x00369306`), makes two stub calls (`0x0016D6A0`) and copies the first eight bytes of the
`memset` import stub `0x00861EC0` to `0x02CA6C88` and `0x02CA6C8C`; the only reference to `0x02CA6C88` is that write
(`0x0047469E`).

`0x0036FD70` clears `0x02AD9E00` and runs `0x003696D0`, which releases the three handles at `0x022D7FC0` to
`0x022D7FC8` (retrying while the stub reports busy) and sets each to -1. `0x003694D0` fills the two
256-byte tables `0x022C5AF0` (`0x0032EAF0`) and `0x022C59F0` (`0x0032EB10`, which also sets bit 7 of its
byte `0x1F`) with -1 for a non-zero argument, else 0.

### The subsystem resets

The step-8 calls `0x00266D10` and `0x00259180` return the field's fixed tables to their boot state.
`0x00259180` runs under arena 8 (`0x0036C1D0(8)` … `0x0036C140`, which pops the arena stack at
`0x022D89C0`); the ones that allocate select arena 6 or 9 the same way and allocate (`0x0036A100`) only
when their pointer is null:

| Reset | What it does |
|---|---|
| `0x003CD6E0` | allocates `0x800` at `0x02B47790` and `0x2800` at `0x02B47798`; clears 32 and 128 records in them |
| `0x003AC890` | allocates `0x3800` at `0x02B3F528`; `0x02B3F518` = 1.0; `0x003ABB60` clears its 128 records, takes the first as a type-7 record with the next serial from `0x02B3F504` (1 to `0xFFFFFF`), and makes it the list `0x02B3F508` / `0x02B3F510`; per frame `0x003AC870` resets the factor `0x02B3F51C` to 1.0 and `0x003AC900(f)` multiplies it by f |
| `0x003B4790` | allocates `0x1800` at `0x02B404E0`; sets the pairs (3, `0x00D11520`) and (5, `0x00D11538`); clears 64 records |
| `0x00376A80` | clears `0x02ADBB30`, `0x02ADBB34` and the first word of 8 records at `0x02ADBB40` (stride `0x90`) |
| `0x0024C970` | clears `0x1670` bytes from `0x020910A0`; sets the five u16 `0x0209215E` to `0x02092166` to `0x3FF` and `0x020926F4` = `0x4003C`; under arena 8 clears the four soft-particle tables and reads them and `softparticle_bg.csv` ([Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)); `0x02092700` = −1 |
| `0x003D7F10` | clears a word in each of 32 records from `0x02EBBA00` (stride `0x84`) |
| `0x003D8C30` | points `0x02B4E3D0` to `0x02B4E3E8` at the four data blocks `0x01EFE3A0`, `0x01EFE510`, `0x01EFE690`, `0x01EFE810` and runs `0x0050C450` over each; `0x02B4D7B8` = 1.0; clears 32 records |
| `0x003773C0`, `0x003B3E10` | clear 128 records ending at `0x02ADCFC0`, and the 8-byte records from `0x02EBCC80` to `0x02EBCD84` |
| `0x00259250` | resets the block at `0x02096810` to `0x02096D28` (white at `0x02096810`, 0.5 at `0x020968BC`, `0x80808080` at `0x020968B0`) |
| `0x0039CD50` | allocates `0x20000` at `0x02AEED50`; `0x0039AED0(2048.0, 2048.0)` and `0x0039AF20(512.0)`, which store `0x02EBEFFC`, `0x02EBEFF8`, `0x02EBF000` and copy 64 bytes from `0x02AEDD30` to `0x02AEE5A0`; `0x02AEE910` = 8 |
| `0x003A3670` | under arena 9, and every time rather than only when null: allocates `0x190000` at `0x02F8F2F8`, `0xC8028` at `0x02F8F300`, and `[0x02F8F2C0]` = `0x0036B080(9)` bytes at `0x02F8F2D0` (also `0x02F8F308`), with `0x02F8F2D8` = `[0x02F8F2D0]` + (s / 16) × 16 for s = `[0x02F8F2C0]`, the division signed and toward zero; `0x02F8F2E0` = `[0x01FD4A78]`; clears `0x02F8F2C5`, `0x02F8F2C6`, `0x02F8F2CC`, `0x02F8F2E8`, `0x02F8F2F0` and the low two bits of `0x02F8F310` |
| `0x00375120` | clears 32 records at `0x02EBFA48`; writes a 16-step grey ramp (step `0x11`, alpha `0x80`) at `0x02ADB6E0` and eight 32-step ramps after it |
| `0x002FC200` | chains the 48 records of `0x38` bytes at `0x02EC32E0` into a list (`0x02EC3D70`); clears `0x02EC19C0` (`0x1000` bytes) and copies 401 five-bit values from `0x01EEBB10` into it, one per 8 bytes |
| `0x003B0660` | zeroes `+0x00`-`+0x03`, `+0x08`-`+0x0F` and `+0x11` of the 36 records of `0x18` bytes from `0x02EBEC00` and clears the low three bits of each `+0x13`; clears bit 0 of `0x02EBEF68` and the word `0x02EBEF60`; runs `0x0024C460` for 5, 6 and 9; then, when `0x0032E400(10)` returns n > 0, calls `0x0032E620(10, 0, [0x01FD4A30], n, 0)` and `0x0032E520(0)`, passes a zeroed `0x890`-byte request with type 5 to `0x0024B3A0`, and calls `0x003EDAD0([0x01FD4A30], its word +0xC)` |
| `0x003B16B0` | clears the 32 records of `0x30` at `0x02EBE5E0` and `0x02EBEBE0` / `0x02EBEBE4` |
| `0x0026F9F0` | fills 96 bytes at `0x02F8F23C` with 3 and sets `0x02F8F29C` = `0x100` |
| `0x003B3160` | links two lists of 32 records of `0x38` bytes, at `0x02EBCD80` (head `0x02EBDB88`) and `0x02EBD480` (head `0x02EBDBA0`): each record's first word takes its index and `0x30000000`, `+0x20` points to the next and `+0x28` to the previous; clears `0x02EBDB80`, `0x02EBDB90`, `0x02EBDB98`, `0x02EBDBA8`, `0x02EBDBB0`, `0x02EBDBB4`; then `0x0024C550(3)` |
| `0x003CBFF0(0x02096ED0)` | (call at `0x002591F2`) clears `+0xC0` of the camera `0x02096ED0` and runs `0x003CBBE0` on it |
| `0x0025A600(0.1, 1000.0)` | stores the two floats `0x02098DE0` / `0x02098DE4` |

After the last call it stores three words directly: `0x022D92E0` = `0x01EF93E8` = `0x458DC800` (4537.0)
and `0x022D9138` = 1 (`0x0025920C`, `0x00259216`, `0x00259220`). They are the presentation generator's last
sample, its state and its enable word ([Random number generators](../Random-Numbers/random-number-generators.md)).

`0x00266D10`, the actor-system reset, runs among others `0x00314940` (`0x022C2544` = 1.0), `0x002556F0`
(five groups of four `0x2E0`-byte records from `0x02092810`, plus one more, each through `0x003CBFF0`;
`0x020964FC` = 1.0, `0x02096514` = `0x20`), `0x002F1A00` (zeroes `0x022BE7C0`, `0x022BE7C8`, `0x022BE7D0`),
`0x003DD7E0`, `0x003DDD10`, `0x003DE710`, `0x003DF030`, `0x003E7DF0`, `0x003EBAB0` and `0x003EBE40`.

Those last seven number and clear the tables from `0x02B581A0` to `0x02B5EC88`: 5 × 16 slots, four records with
`0x13602` and colour `0x80FFFFFF`, 16 records, 5 × 8 slots, 32 records numbered `0x20` to `0x3F`
with a 28-node list, and eight pairs of 0 and `0x100`.

`0x0036F4D0` runs `0x00382910`, which clears 8 records at `0x02AED700` (stride `0xE0`) and builds two
view records with `0x004679C0(record, width, height)`: `0x02AED4A0` for the frame size
`[0x022D8EAC]` × `[0x022D8EB4]` and `0x02AED500` for 2000 × 2000.

A view record holds the integer size at `+0x44` / `+0x48`, the depth limits `near` = 1024 and `far` =
16,776,191 at `+0x4C` / `+0x50`, and `0x00229D20()` at `+0x40`. It sets `+0x00 = width × 0.5` and
`+0x14 = height × -0.5` (`0x00467A0F`-`0x00467A26`), the depth scale `+0x28 = (far - near) × -0.5` and
offset `+0x38 = (far + near) × 0.5` (`0x00467A2B`-`0x00467A62`), 2048 at `+0x30` / `+0x34` as the
screen offset and 1.0 at `+0x3C`.

Step 4's `0x00184660` ends with `0x00248410`, which sets `0x0208ECC0` / `0x0208ECC4` to minus half of
`[0x01E0C1D8]` / `[0x01E0C1DC]` and writes that size into the four objects at `0x0208EA20` to `0x0208EA38`
(`+0x9C` / `+0x9E`), and `0x0024B100`, which copies the size into the halfwords `0x01E0C1D4` /
`0x01E0C1D6`.

## Layouts

```
globals written by the boot fixer
0x02EB4234  u8    generator first-use latch        0x02EB3870  u32[624] Mersenne Twister state
0x01DFE0B4  u32   frame base 1 or 2               0x01DFE0B8 / 0x01DFE0BC  f32 time base 1.0 / 2.0 and 1.0 / 0.5
0x01F82E38  u32   60 fps mode flag                 0x01DFE0C0  u32  the mode suppressor
0x01F82E3C  u8    timer period begun               0x01F82E40  u32  the period
0x02064ACC  u32   pacer ticks per frame: 2 / [0x01DFE0B4]
0x01E0C2A0  u32   confirm mask                     0x01E0C2A4  u32  cancel mask       0x01FD4A64 u32 DecideButton non-zero
0x01E02814  u32   language index                   0x01E0281C  u32  10
0x01F7F490 / 0x01F7F4A0  the code_steam.txt and data.txt ids
0x01FD49F0 .. 0x01FD4A40, 0x01FD4A18, 0x01FD4A20, 0x01FD4A90  the eleven block pointers
0x02064AA4, 0x02064AC0 .. 0x02064AD4  the main state machine's cells     0x01FD4A78 u32 0x1FE0000
0x022C2528  u32   the -nologo flag                 0x022D7FD0  arena table, 0xA8 per id, 15 ids
```

## Shipped data

| Fact | Value |
|---|---|
| default seed, boot seed | `0x1571` (5489), `0x11B9` (4537) |
| reload seed | `(((low + 0x2B5A5) * 0x21 + high) & 0x7FFFFFFF) + [0x01FD4A80] * 600` from `_time64` |
| time base at 60 fps | `0x01DFE0B4` 2, `0x01DFE0B8` 2.0 (`0x01CEBC08`), `0x01DFE0BC` 0.5 (`0x01CEBB70`) |
| ticks per frame | 2 at 30 fps, 1 at 60 |
| masks | confirm `0x4000`, cancel `0x2000`; swapped when DecideButton is 0 |
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
- The arenas are fixed at boot; only id 11 is re-sized, by `0x0037B3D0`.

## Related

- [Game application](game-application.md): the init job that calls the boot fixer.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and DecideButton in the
  settings object.
- [Random number generators](../Random-Numbers/random-number-generators.md): the Mersenne
  Twister and its seeders.
- [Frame update order](frame-update-order.md): the state machine whose cells are initialised here.
