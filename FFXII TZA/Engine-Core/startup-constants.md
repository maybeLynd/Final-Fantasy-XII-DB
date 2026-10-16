---
title: "Startup constants: the random seed, the frame-rate constant, the memory budget and the confirm button mapping"
kind: "system"
category: "Engine core"
summary: "What the boot fixer decides once and the rest of the game reads thereafter: the Mersenne Twister seeded from a literal and reseeded from the wall clock only on a save load, the frame-rate time base and the ticks-per-frame constant derived from FrameLimit, the confirm and cancel button masks derived from DecideButton, the language index, the two build-id files, the eleven heap blocks of the memory budget and the nine arenas registered from them, and the order in which the boot fixer runs the engine's one-time initialisers."
addresses: ["0022A0B0", "0022BDF0", "001EDDC0", "0017D8F0", "00229F10", "0022A4F0", "0017E210", "0017E270", "0017E410", "00314DE0", "00184960", "001EDEF0", "001EDE70", "0017D990", "0017D9D0", "00379CF0", "00863D30", "00584210", "0036D240", "00369D30", "0036D990", "00368A90", "0035EB70", "0022A770", "0022A4B0", "0037B3D0"]
---

# Startup constants: the random seed, the frame-rate constant, the memory budget and the confirm button mapping

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
   `+0x64`) is non-zero; the masks `01E0C2A0`/`01E0C2A4` = `0x4000`/`0x2000`, swapped to
   `0x2000`/`0x4000` when it is zero ([game settings](../Saving-Loading-And-Settings/game-settings.md));
4. `00184660([01E0280C])`, the PS2 emulation reset `0036D990` (the `vf00` image `01EF93F0` =
   `{0, 0, 0, 1}` and two log lines through `0017D280`), `0022CB90`, `0037DF90`, `0037E0F0`;
   `01FD4A78` = `0x1FE0000`; `002DF9A0(language)`; `00184960(1)` (the time-base suppressor, below);
   `00862BD0(language)`; the build-id files (below);
5. a call to the return stub `0016D6A0` with `0x7D` after `00184960(1)`, a compiled-out hook; two
   more such calls follow the state cells and precede `00266D10`;
6. the main state machine's cells: `02064AD2` = 0, `02064AD4` = 1.0, the state `02064AD3` = 0,
   the ticks-per-frame constant `02064ACC = 2 / [01DFE0B4]`, `02064AD1` = 0, `02064AC0`, `02064AC4`
   and `02064AC8` = 1.0 ([frame update order](frame-update-order.md));
7. `00368A90` (`02EC0B39` = 0, `02EC0B38` = `0xFF`), then the memory budget (below);
8. `0037B390`, `00360370`, `00358510`, `00379D40`, `003692D0` (its byte result goes to
   `003694D0(byte, 0, 0)` after `0036D260`, `00368ED0`, `0036ECE0` and `00379D00`), `0032EAE0`,
   `0036FD70` (the stub returns 0, so always), `0036EFD0`, `0036D8B0`, a ret-stub call, the actor
   system `00266D10`, `0036F4D0`, `003325C0`, `00259180`;
9. the seed `00379CF0(0x11B9)` (below); `00253970`, the spawn banks `002368D0`, `002EA520`,
   `00259DF0`, `0035B270`, `00379E90`, `00379D20`, `0036E310`, `0037CCC0`, `0036FFF0`; the game-step
   count `02064AD0` = 0; a drain loop over `00364200` / `0032E040` / `0035EA30(0)` gated on
   `005C5230()` being non-zero never runs.

### The random seed

`00379CF0` is a five-byte thunk to `00863D30(seed)`, the Mersenne Twister seeder: with the first-use
latch `02EB4234` clear it seeds the 624-word state at `02EB3870` with `0x1571` (5489, the library
default), sets the latch, and then seeds with the argument ([random number
generators](../Random-Numbers/random-number-generators.md)). Boot passes `0x11B9` (4537),
a literal in the instruction stream: no clock, no entropy, no input. So the stream is identical
on every launch until a save is loaded.

The thunk's only other caller is the save-load normaliser `00584210`, which ends with
`_time64(NULL)` and seeds `(((low + 0x2B5A5) * 0x21 + high) & 0x7FFFFFFF) + [01FD4A80] * 600`,
`low` and `high` the two halves of the clock value. Loading a save therefore rerolls the generator
from the wall clock, not from the save; loading the same save twice does not give the same stream.

### The frame-rate constants

`0022BDF0(argc, argv)` reads FrameLimit (`0017D8F0`, the settings object's `+0x48`), scans every
command-line argument for the eight bytes `"-nologo"` with its terminator (`00314DE0(1)` stores 1
at `022C2528` on a match; the loop does not stop at one), and calls `001EDDC0(FrameLimit == 1)`.

With 0 that arm begins a multimedia timer period (`timeGetDevCaps`, `timeBeginPeriod(wPeriodMin)`,
the period at `01F82E40`, `01F82E3C` = 1); with 1 it writes the time base, `01DFE0B8` = 2.0,
`01DFE0BC` = 0.5, `01F82E38` = 1 and `01DFE0B4` = 2, runs `0033F020` and ends any period begun.
Both arms then run `0032AE70`, `003333D0`, `00337A00` and `002BDA90`.

`01DFE0B4` ships as 1 and has that one writer; its readers divide authored 30 fps frame counts by
it. The boot fixer then computes `02064ACC = 2 / [01DFE0B4]`, 2 at 30 fps and 1 at 60: the number
of pacer ticks the field frame waits per frame (`0035EC80([02064ACC], 0)`, an identical copy of
`0035EB70`, at the end of `0022A770`; the second argument is the stub's 0).

It has a second writer, the setter `00229F10`: the manager-unload reset `002695A0` (its only caller is the unload
`002628B0`) rewrites `2 / [01DFE0B4]`, and the verb `mainloopallsyncv` (`0x18F`, `003464B0` →
`0026DB10`) stores its popped value divided by `[01DFE0B4]`, so the verb speaks in 30 fps ticks.

`00184960(mode)` sets the suppressor `01DFE0C0` to 1 (`001EDEF0`) and reads the mode flag
`01F82E38` (`001EDE70`): with the flag clear it keeps the suppressor and hands `mode` on; with it
set and `mode` not 1 it clears the suppressor; with `mode` 1 and `02092748` non-zero it runs the
`00229EA0` gate and clears the suppressor when the gate does not return 1, otherwise it keeps the
suppressor only while byte `+0x118` of `001EBA40()` is zero. Every path then passes `mode` (1 on
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
| 2 | `01FD49F8` | `0x1DC0010` | `0x1DC0000` (29.75 MiB) | `0x10` |
| 3 | `01FD4A00` | `0xD20100` | `0xD20000` (13.12 MiB) | `0x100` |
| 4 | `01FD4A08` | `0x100010` | `0x100000` (1 MiB) | `0x10` |
| 5 | `01FD49F0` | `0x1C0100` | `0x1C0000` (1.75 MiB) | `0x100` |
| 6 | `01FD4A10` | `0x6C00400` | `0x6C00000` (108 MiB) | `0x400` |
| 7 | `01FD4A30` | `0x3000100` | `0x3000000` (48 MiB) | `0x100` |
| 8 | `01FD4A38` | `0x2000100` | `0x2000000` (32 MiB) | `0x100` |
| 9 | `01FD4A40` | `0x1200010` | `0x1200000` (18 MiB) | `0x10` |
| 11 | `01FD4A18` | `0x400100` | `0x400000` (4 MiB) | `0x100` |
| none | `01FD4A20` | `0x80000` | not registered | |
| none | `01FD4A90` | `0x100000` | not registered | |

Every allocation is its registered size plus the slot count in bytes.

The registrar (ids below
15) records the arena in its table at `022D7FD0` (stride `0xA8`), zeroes the block's first 64
bytes and writes the arena's name there (`sprintf`), lays a bitmap and a word table at the head of
the block (64-byte aligned, sized from the registered size), then the handle slots: `slotCount`
records of 16 bytes chained by index when the count is non-zero, and finally the arena's free
region, half-split, handed to `0036A490` ([memory and
allocation](../Compiler-And-C-Runtime/memory-and-allocation.md)).

Id 10 is never registered; `0037B3D0` re-sizes id 11 when `02ADD931` differs from `02ADD930`,
freeing the block (`0036D250`) and registering a new one of `0x3C0000` when `02ADD930` is 3, else
`0x400000`; ids 12 to 14 are registered elsewhere. The unregistered 1 MiB block at `01FD4A90` is the per-model oscillator table; the
0.5 MiB block at `01FD4A20` is stored and never read.

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
| default seed, boot seed | `0x1571` (5489), `0x11B9` (4537) |
| reload seed | `(((low + 0x2B5A5) * 0x21 + high) & 0x7FFFFFFF) + [01FD4A80] * 600` from `_time64` |
| time base at 60 fps | `01DFE0B4` 2, `01DFE0B8` 2.0 (`01CEBC08`), `01DFE0BC` 0.5 (`01CEBB70`) |
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
- The arenas are fixed at boot; only id 11 is re-sized, by `0037B3D0`.

## Related

- [Game application](game-application.md): the init job that calls the boot fixer.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and DecideButton in the
  settings object.
- [Random number generators](../Random-Numbers/random-number-generators.md): the Mersenne
  Twister and its seeders.
- [Frame update order](frame-update-order.md): the state machine whose cells are initialised here.
