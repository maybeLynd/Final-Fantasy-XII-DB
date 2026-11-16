---
title: "Startup constants: the random seed, the frame-rate constant, the memory budget and the confirm button mapping"
kind: "system"
category: "Engine core"
addresses: "0x0022A0B0, 0x0022BDF0, 0x001EDDC0, 0x0017D8F0, 0x00229F10, 0x0022A4F0, 0x0017E210, 0x0017E270, 0x0017E410, 0x00314DE0, 0x00184960, 0x001EDEF0, 0x001EDE70, 0x0017D990, 0x0017D9D0, 0x00379CF0, 0x00863D30, 0x00584210, 0x0036D240, 0x00369D30, 0x0036D990, 0x00368A90, 0x0035EB70, 0x0022A770, 0x0022A4B0, 0x0037B3D0, 0x003692D0, 0x00369510, 0x008628E0, 0x00369650, 0x003696D0, 0x00259180, 0x003AC890, 0x002FC200, 0x00375120, 0x00382910, 0x004679C0, 0x00248410"
---

## What the player sees

Two launches of the game roll the same numbers until a save is loaded; loading a save reseeds the
generator from the system clock, so from then on the two launches roll differently. A player who
sets the frame limit to 60 sees every authored duration keep its wall-clock length. Whether Circle
or Cross confirms is set at start into two masks every menu reads, and set again when the Config
screen's confirm button option changes. The game's whole working memory, a quarter of a gigabyte
in eleven blocks, is claimed before the first screen appears.

Some of these values change later in the same launch: the Config screen rewrites the two button
masks, the ticks-per-frame constant is rewritten when an area unloads and by the script command
`mainloopallsyncv`, the 4 MiB block of arena 11 is freed and taken again at a new size, and arenas
13 and 14 are freed and registered again each time an area's managers are bound.

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
   `0x01FD4A78` = the address `0x01FE0000`; `0x002DF9A0(language)`; `0x00184960(1)` (the time-base suppressor, below);
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

The manager-init burst `0x0017D4C0` calls `0x0022A4B0` at `0x0017D5E3`, after the boot fixer (`0x0017D5CC`) and three
more calls (`0x001B1BA0`, `0x001B1C00`, `0x001B1580`; [game application](game-application.md)).

`0x0022A4B0` files the start-up graphics and text requests: `0x00291C80` (the item pictures,
[menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md)), `0x0053DD10` (it returns 1 and the result is
not used), `0x00563520` (the battle text groups 10, 20 and 14, [battle text
tables](../Game-Files-And-Data-Tables/battle-text-tables.md)) and `0x00556500` (the License Board picture `lic_4_c`,
[License Board screen](../Menus-And-HUD/license-board-screen.md)).

Its other calls go to the return stub `0x0016D6A0` and do nothing: one after `0x00291C80` (`0x0022A4B9`), four after
`0x0053DD10` (`0x0022A4C3`-`0x0022A4D2`) and the tail jump at the end (`0x0022A4E5`).

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

The second argument is read on its own as well: `0x00408C30`, the settings-file loader, takes the argument vector from
`0x0017D240` (the pointer and count at `0x01F7F480` and `0x01F7F488`). When there are at least two arguments and the second
is `debug` (the six bytes at `0x00D121F8` with the terminator, compared at `0x00408DA1`-`0x00408DC2`), it stores 0 to the
u16 `0x02B62DB4` (`0x00408DC4`).

With 0 that arm begins a multimedia timer period: `timeGetDevCaps(&caps, 8)`, and only when it returns 0
(`0x001EDE29`-`0x001EDE31`) `timeBeginPeriod(wPeriodMin)`, the period at `0x01F82E40`, `0x01F82E3C` = 1; when `timeGetDevCaps`
fails it begins no period. With 1 it writes the time base, `0x01DFE0B8` = 2.0, `0x01DFE0BC` = 0.5, `0x01F82E38` = 1 and
`0x01DFE0B4` = 2, runs `0x0033F020` and ends any period begun (`timeEndPeriod([0x01F82E40])` and `0x01F82E3C` = 0,
`0x001EDE01`-`0x001EDE17`). Both arms then run `0x0032AE70`, `0x003333D0`, `0x00337A00` and `0x002BDA90`.

Of these, `0x00337A00` sets the formation angle step `0x02EC0F84` to `2 / (30 × [0x01DFE0B4])` ([battle
locomotion](../Movement-And-Pathfinding/battle-locomotion.md)).

`0x01DFE0B4` ships as 1 and has that one writer. Its readers scale authored 30 fps frame counts both ways:
of its 211 reading instructions, 59 multiply by it (`n * [0x01DFE0B4]`, `imul`, the staff roll's fade hold at
`0x0053F000` among them) and 35 divide by it (`n / [0x01DFE0B4]`). The boot fixer then computes
`0x02064ACC = 2 / [0x01DFE0B4]`, 2 at 30 fps and 1 at 60: the number
of pacer ticks the field frame waits per frame (`0x0035EC80([0x02064ACC], 0)`, a jump to
`0x0035EB70`, at the end of `0x0022A770`; the second argument is the stub's 0).

It has a second writer, the setter `0x00229F10`: the manager-unload reset `0x002695A0` (its only caller is the unload
`0x002628B0`) rewrites `2 / [0x01DFE0B4]`, and the verb `mainloopallsyncv` (`0x18F`, `0x003464B0` →
`0x0026DB10`) stores its popped value divided by `[0x01DFE0B4]`, or 2 divided by it when the value is negative
(`0x0026DB12`-`0x0026DB19`), so the verb speaks in 30 fps ticks.

`0x00184960(mode)` sets the suppressor `0x01DFE0C0` to 1 (`0x001EDEF0`) and reads the mode flag `0x01F82E38` (`0x001EDE70`):
with the flag clear it keeps the suppressor and hands `mode` on; with it set and `mode` not 1 it clears the
suppressor; with `mode` 1 it runs the `0x00229EA0` gate when `0x02092748` is non-zero and clears the suppressor when the
gate does not return 1; when `0x02092748` is 0 or the gate returns 1 it keeps the suppressor only while byte `+0x118` of
`0x001EBA40()` is zero.

Every path then passes `mode` (1 on the clearing paths and at boot) to `0x00798E90` and, with a render manager
(`0x00189120()` non-null), tail-jumps to `0x005FEA50([manager + 8], 0x0017ECB0, mode)` (`0x001849BD`-`0x001849D0`); without one
it returns.

### The confirm button and the language

`0x0022A4F0` is the only other writer of the two masks and `0x01FD4A64`; it is the Config screen's path (`0x0017E6E0` and
`0x0023E194`). It repeats step 3: it reads DecideButton through `0x0017E210` (`0x0022A4F4`), stores whether it is non-zero
at `0x01FD4A64` (`0x0022A510`), and stores `0x4000` / `0x2000` to the confirm and cancel masks, swapped when DecideButton
is zero, as 16-bit stores (`0x0022A526`, `0x0022A51F`), like the boot fixer's (`0x0022A119`, `0x0022A10C`). The masks are read
at 86 places, 47 for the confirm mask and 39 for the cancel mask; none of those readers asks the setting itself.

`0x0017E270` turns the language string the settings object names
(`[0x01DF0030 + 8 * [0x01F82D20][0]]`) into an index: `jp` 10, `en` 1, `fr` 2, `de` 3, `it` 4, `es` 5,
`kr` 7, `ch` 8, `cn` 11, anything else 10; it is stored at `0x01E02814` and read by `0x00229E40`,
`0x00229E50` and twice more inside the boot fixer ([languages](../Saving-Loading-And-Settings/languages.md)).

### The build-id files

`0x0017D990` reads two text files through the resource loader (`0x001D6F20`, `0x001D6EE0`, `0x001D6FA0`):
`GameData/code_steam.txt` into `0x01F7F490` and `GameData/data.txt` into `0x01F7F4A0`, each as the bytes from offset 7 of
the file up to the first space (`strcspn`); a file that fails to load logs `load failed!`.

Each file goes through `0x0017D9D0(path, slot)`: it opens the file (`0x001D6F20`), reads it into a stack buffer sized from
`0x001D6EE0`'s result plus one (`0x0017DA23`, `0x001D6FA0`), copies the `strcspn` length with `memcpy` (`0x0017DA73`), writing
no terminator and with no check of the length, not even against the 16 bytes between the two slots, and closes the
file (`0x001D6E80`, `0x0017DA7B`); on a failed open it prints `load failed!` (`0x0017DA11`) and leaves its slot unwritten.

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
| no id | `0x01FD4A20` | `0x80000` | not registered | |
| no id | `0x01FD4A90` | `0x100000` | not registered | |

Every allocation is its registered size plus the slot count in bytes.

The registrar (ids below
15) records the arena in its table at `0x022D7FD0` (stride `0xA8`), zeroes the block's first 64
bytes and writes the arena's name there (`sprintf`), lays a bitmap and a word table at the head of
the block (64-byte aligned, sized from the registered size), then the handle slots: `slotCount`
records of 16 bytes chained by index when the count is non-zero, and finally the arena's free
region, half-split, handed to `0x0036A490` ([memory and
allocation](../Compiler-And-C-Runtime/memory-and-allocation.md)).

Id 10 is never registered; `0x0037B3D0` re-sizes id 11 when `0x02ADD931` differs from `0x02ADD930`: it runs `0x00369760(11)`
and `0x0036D160(11)`, frees the block (`0x0036D250`), takes a new one of `0x3C0000` bytes when `0x02ADD930` is 3, else
`0x400000` (`0x0036D240`, the size alone with no slot bytes added), stores it at `0x01FD4A18` and registers it with that
size and `0x100` slots (`0x0037B3FE`-`0x0037B43D`).

On every call it first runs `0x0036B060(11)`, whose result it does not use, and it ends by setting `0x02ADD932` to 4
(`0x0037B442`; [resource arenas and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)).
Ids 12 to 14 are registered elsewhere. The unregistered 1 MiB block at `0x01FD4A90` is the per-model oscillator table;
the 0.5 MiB block at `0x01FD4A20` is stored and never read. `0x0036B060(id)` returns an arena's table entry, `0x022D7FD0 +
id × 0xA8`, or null for an id of 15 or more.

### The PS2 boot shims

Step 8 replays the PlayStation 2 boot against stubs. `0x003692D0` walks seven module records at `0x01EF9290` (stride
`0x18`, the first `sio2man.irx`): `sio2man.irx`, `sio2d.irx`, `dbcman.irx`, `pad2/ds2o.irx` twice, `mcman.irx` and
`mcserv.irx`, each with the empty argument string `0x01CEB638`.

`0x00369510(name, out, host, demo)` builds each path: the prefix `host0:/image/FF12/modules/` (`0x01EF9338`) when `host`
is set, the empty string (`0x01EF9348`) otherwise, `DEMO/` when `demo` is set, then the name, upper-cased (the letters
`a` to `z`) unless `host` is set, then a suffix that is the empty string on both arms (`0x01EF9340`, `0x01EF9350`); unless
`host` is set, every `/` of the whole path then becomes `\` (`0x00369621`-`0x00369640`). Both callers (`0x0036937F`,
`0x00369693`) give `host` and `demo` the value 0, so each path is the upper-cased name alone, such as `PAD2\DS2O.IRX`.

A record is loaded only when bit `0x1` of its byte `+0x10` is clear, which holds for all seven
(`0x00369353`-`0x0036935C`). Its argument string, each `$` turned into a terminator, goes to the loader with its length,
or a null pointer when it is empty (`0x0036938C`-`0x003693D6`).

The loader `0x008628E0(path, length, arguments, &result)` stores 0 through its fourth argument and returns 0, so every
module counts as loaded: the walk stores the loader's return value in the handle `0x022D7FC0 + 4 × h` for the record's
signed byte `h` at `+0x13` when `h` is not negative (`0x00369494`-`0x003694A0`; 0 into `0x022D7FC0` for `mcman.irx` and into
`0x022D7FC4` for `mcserv.irx`), and sets `0x022D7FCC |= 1 << b` for the record's signed byte `b` at `+0x12` when `b` is
not negative (`0x003694A5`-`0x003694B8`; bits `0x1` and `0x2` for the two `pad2/ds2o.irx` records).

A negative return repeats the load, except that a return of -200 or a result of 1 gives the record up the first time
either happens in the walk and repeats the load every later time; giving up also clears the flag that lets a record
with a non-zero byte `+0x11` load (`0x00369360`-`0x00369369`, `0x00369402`-`0x00369421`). The stub never takes these paths.

Before the walk, `0x003692D0` makes a stub call, runs `0x00474680` and `0x004746C0(1)`, clears `0x022D7FCC` (`0x00369318`),
resets the FF12CONFIG block with `0x00408BA0` (`0x00369323`), runs `0x00369650` and sets the three handles `0x022D7FC0` to
`0x022D7FC8` to -1 (`0x0036932D`, `0x0036933F`). `0x00369650` performs the I/O processor reset with `ioprp300.img`
(`0x01EF9360`): it builds that path with `0x00369510` (`0x00369693`); its other calls are stub calls (`0x0016D6A0`, and
`0x005C5230`, which returns 0), `0x003691E0` and `0x0046E000`, which also sets `0x02CA6074` and `0x02CA6114` to -1. `0x004746C0`
is four stub calls.

After the walk `0x003692D0` calls `0x008624C0`, which runs `0x00862A40` and returns 0, so the settings loader `0x00408C30`
always runs (it is skipped only for -101, `0x0036943A`) and its result is `0x003692D0`'s return value ([game
settings](../Saving-Loading-And-Settings/game-settings.md)); then it runs `0x0035F260`, `0x0032EA90` and the sound state reset
`0x002DE360` (`0x00369451`), which among its stores sets the spatial-sound behind ratio `0x0215EFD0` ([spatial
sound](../Sound-And-Music/spatial-sound.md)), and ends with a stub call with `0x65` (`0x0036945B`).

`0x00474680`, called first (`0x00369306`), makes two stub calls (`0x0016D6A0`) and copies the first eight bytes of the
`memset` import stub `0x00861EC0` to `0x02CA6C88` and `0x02CA6C8C`; the only reference to `0x02CA6C88` is that write
(`0x0047469E`).

`0x0036FD70` clears `0x02AD9E00` and runs `0x003696D0`, which after two stub calls walks the three handles at `0x022D7FC0` to
`0x022D7FC8` from the last down (`0x003696F0`-`0x00369746`): it skips a negative one; for each other one it calls the stub
`0x005C5230(handle, 0, 0, &status)` until the answer is not negative (with `0x0035EA30(0)` between tries; the stub returns
0, so it is called once), then `0x005C5230(handle)`, and sets the handle to -1; two more `0x005C5230` calls end it. At
boot the module walk has left 0 in `0x022D7FC0` and `0x022D7FC4` and -1 in `0x022D7FC8`, so the first two are released.

`0x003694D0` fills the two 256-byte tables `0x022C5AF0` (`0x0032EAF0`) and `0x022C59F0` (`0x0032EB10`, which also sets bit
`0x80` of its byte `0x1F`) with 0: it passes 0 to both fillers (`0x003694D4`, `0x003694DB`), which fill with -1 only for
a non-zero argument. It then makes a stub call with 1 when the byte `0x02B62DAA` is 1 (`0x00408B50`), else with 0.

### The subsystem resets

The step-8 calls `0x00266D10` and `0x00259180` return the field's fixed tables to their boot state.
`0x00259180` runs under arena 8 (`0x0036C1D0(8, 10)` … `0x0036C140`, which pops the arena stack at
`0x022D89C0`); the ones that allocate select arena 6 or 9 the same way and allocate (`0x0036A100`) only
when their pointer is null:

| Reset | What it does |
|---|---|
| `0x003CD6E0` | allocates `0x800` at `0x02B47790` and `0x2800` at `0x02B47798`, each only while its pointer is null and under arena 6 (`0x0036C1D0(6, 6)` … `0x0036C140`, `0x003CD6E4`-`0x003CD739`); stores 0 in the dword `0x02B47774`, the qwords `0x02B47778` and `0x02B47780` and the byte `0x02B47770`, in the dword `+0x04` of each of the 32 records of `0x40` bytes in the first block and in the dword `+0x30` of each of the 128 records of `0x50` bytes in the second (`0x003CD745`-`0x003CD7AB`) |
| `0x003AC890` | allocates `0x3800` at `0x02B3F528`; `0x02B3F518` = 1.0; one 8-byte store of `0x10000` at `0x02B3F500` (`0x003AC8D0`) sets the serial counter `0x02B3F504` to 0 and the byte `0x02B3F502` to 1, and `0x02B3F520` = 0 (`0x003AC8DB`); then the tail jump to `0x003ABB60` (`0x003AC8E6`), which stores 0 in the dword `+0x00` and the byte `+0x20` of each of its 128 records of `0x70` bytes (`0x003ABB6A`-`0x003ABB8D`), in the byte `0x02B3F500` (`0x003ABB91`) and in the 16 bytes of `0x02B3F508` and `0x02B3F510` (`0x003ABBA0`), takes the first as a type-7 record with the next serial from `0x02B3F504` (1 to `0xFFFFFF`, so 1 after this reset, `0x003ABBE0`-`0x003ABC06`), sets the byte `0x02B3F500` to 1 (`0x003ABBFC`), and makes it the list `0x02B3F508` / `0x02B3F510`; per frame `0x003AC870` resets the factor `0x02B3F51C` to 1.0 and `0x003AC900(f)` multiplies it by f |
| `0x003B4790` | allocates `0x1800` at `0x02B404E0` while it is null, under arena 6 (`0x0036C1D0(6, 6)` … `0x0036C140`, `0x003B479B`-`0x003B47BD`); sets the pairs (3, `0x00D11520`) and (5, `0x00D11538`); stores 0 in the first dword of each of the 64 records of `0x60` bytes, in the bytes `0x02B404C0` and `0x02B404C1`, the dword `0x02B404C4` and the qwords `0x02B404C8` and `0x02B404D0` (`0x003B47FB`-`0x003B482C`) |
| `0x00376A80` | clears `0x02ADBB30`, `0x02ADBB34` and the first word of 8 records at `0x02ADBB40` (stride `0x90`) |
| `0x0024C970` | clears `0x1670` bytes from `0x020910A0`; sets the five u16 `0x0209215E` to `0x02092166` to `0x3FF` and `0x020926F4` = `0x4003C`; under arena 8 clears the four soft-particle tables and reads them and `softparticle_bg.csv` ([Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md)); clears bits `0x1`, `0x8` and `0x40` of the word `0x020926E4` (`0x0024CA69`-`0x0024CB11`); `0x02092700` = −1 |
| `0x003D7F10` | stores 0 in the dword `+0x00` of each of the 32 records from `0x02EBBA00` (stride `0x84`; `0x003D7F20`) |
| `0x003D8C30` | points `0x02B4E3D0` to `0x02B4E3E8` at the data of four blocks, `0x01EFE3A0`, `0x01EFE520`, `0x01EFE6A0` and `0x01EFE820`, each with its length in the dword 8 bytes before it, and runs `0x0050C450` over each data range; `0x02B4D7B8` = 1.0; stores 0 in the dword `+0x04` of each of the 32 records of `0x60` bytes from `0x02B4D7D0`, in the word `0x02B4D7A1`, the byte `0x02B4D7A0`, the dword `0x02B4D7A4` and the qwords `0x02B4D7A8` and `0x02B4D7B0` (`0x003D8D0B`-`0x003D8D4F`) |
| `0x003773C0`, `0x003B3E10` | `0x003773C0` stores 0 in the dword `0x02ADBFC4`, in the first dword of each of the 128 `0x20`-byte records from `0x02ADBFE0` to `0x02ADCFC0`, in the byte `0x02ADBFC0` and in the qwords `0x02ADBFC8` and `0x02ADBFD0` (`0x003773C9`-`0x003773EC`); `0x003B3E10` stores 0 in the byte `+0`, the word `+2` and the dword `+4` of each of the 32 records of 8 bytes from `0x02EBCC80` up to `0x02EBCD80` (`0x003B3E10`-`0x003B3E30`) |
| `0x00259250` | makes 31 stores in the block from `0x02096810` to `0x02096D28` and no fill, so every other byte of the span keeps its value: 1.0 at `0x02096810`, `0x02096814` and `0x02096818`; (0, 0, 0, 1) at `0x020968A0`; 0.5 at `0x020968BC`; `0x80808080` at `0x020968B0` and `0x80000080` at `0x020968B4`; the qword `0x02096884` = `0x1011000`, the dword `0x02096892` = `0x200`, the words `0x02096896` = `0x8040` and `0x020968B8` = 1; bit `0x1` of the byte `0x02096C60` cleared and the byte `0x020968C8` set to its value AND `0xF5`, OR 5; the dword `0x02096D28` = 1; and 0 at the bytes `0x02096844`, `0x0209688C`, `0x020968EE` and `0x02096D21`, the word `0x020968EC`, the dwords `0x0209688E`, `0x020968E8`, `0x020969F0`, `0x020969F8`, `0x02096A00`, `0x02096A08`, `0x02096B3C`, `0x02096BA8` and `0x02096C78`, the qword `0x02096BA0`, the 16 bytes at `0x02096B40` and the float `0x02096D24` (`0x00259250`-`0x00259358`) |
| `0x0039CD50` | under arena 9, and every time rather than only when null: allocates `0x20000` at `0x02AEED50`; runs `0x003970D0`; `0x0039AED0(2048.0, 2048.0)` and `0x0039AF20(512.0)`, which store `0x02EBEFFC`, `0x02EBEFF8`, `0x02EBF000` and copy 64 bytes from `0x02AEDD30` to `0x02AEE5A0`; `0x02AEE910` = 8, and 0 in the dword `0x02AEE900` and the qword `0x02AEE908` (`0x0039CD9B`-`0x0039CDA8`) |
| `0x003A3670` | under arena 9, and every time rather than only when null: allocates `0x190000` at `0x02F8F2F8`, `0xC8028` at `0x02F8F300`, and `[0x02F8F2C0]` = `0x0036B080(9)` bytes at `0x02F8F2D0` (also `0x02F8F308`), with `0x02F8F2D8` = `[0x02F8F2D0]` + (s / 16) × 16 for s = `[0x02F8F2C0]`, the division signed and toward zero; `0x02F8F2E0` = `[0x01FD4A78]`; clears `0x02F8F2C5`, `0x02F8F2C6`, `0x02F8F2CC`, `0x02F8F2E8`, `0x02F8F2F0` and the low two bits of `0x02F8F310` |
| `0x00375120` | clears the handle `+0x68` of the 32 fade-pool records at `0x02EBF9E0` (stride `0x70`, the dwords from `0x02EBFA48`, `0x00375133`; [screen fades](../Graphics/screen-fades.md)); sets the class enables `0x02EC07E0` to `0x02EC07E5` to 1 (`0x0037514F`, `0x0037515C`) and the handle counter `0x02EC07E8` to 0 (`0x00375149`); writes a 16-step grey ramp (step `0x11`, alpha `0x80`) at `0x02ADB6E0` and eight 32-step ramps after it, from `0x02ADB720`: ramp n holds the grey levels 32n to 32n + 31 with alpha `0x80`, its entries 8 to 15 holding 32n + 16 to 32n + 23 and its entries 16 to 23 holding 32n + 8 to 32n + 15 (`0x003751A0`-`0x00375266`) |
| `0x002FC200` | under arena 8 (`0x0036C1D0(8, 10)` … `0x0036C140`): zeroes the 48 records of `0x38` bytes at `0x02EC32E0`, sets each one's first word to its index with `0x10000000`, and chains them into a list (`0x02EC3D70`) through `+0x28` (the next record, 0 on the last) and `+0x30` (the previous, 0 on the first) (`0x002FC230`-`0x002FC334`); clears the 16 bytes at `0x02EC3D60`, the word `0x02EC3D78` and the byte `0x02EC3D7C`; runs `0x0024C460(1)`; clears `0x02EC19C0` (`0x1000` bytes) and copies 401 five-bit values from `0x01EEBB10` into it, one per 8 bytes, into the low five bits of the u16 at `+4` of each 8-byte slot (`0x002FC2E0`-`0x002FC2FD`); clears the byte `0x02EC3D7D` (`0x002FC2FF`) |
| `0x003B0660` | under arena 8, pushed and popped twice (`0x0036C1D0(8, 10)` at `0x003B0671` and `0x003B06DB`, `0x0036C140` at `0x003B0752` and `0x003B075F`): zeroes `+0x00`-`+0x03`, `+0x08`-`+0x0F` and `+0x11` of the 36 records of `0x18` bytes from `0x02EBEC00` and clears the low three bits of each `+0x13`; clears bit `0x1` of `0x02EBEF68` and the eight bytes at `0x02EBEF60` (`0x003B06B3`), whose low dword is the serial the request handles are numbered from (`0x003B03BB`-`0x003B03C9`); runs `0x0024C460` for 5, 6 and 9; then, when `0x0032E400(10, 0)` returns n > 0, calls `0x0032E620(10, 0, [0x01FD4A30], n, 0)` and `0x0032E520(0)`, passes a zeroed `0x890`-byte request with type 5 to `0x0024B3A0`, and calls `0x003EDAD0([0x01FD4A30], its dword +0xC)` |
| `0x003B16B0` | under arena 8 (`0x0036C1D0(8, 10)` … `0x0036C140`): clears the 32 records of `0x30` at `0x02EBE5E0` (one fill of `0x600` bytes, `0x003B16D0`) and `0x02EBEBE0` / `0x02EBEBE4`, and calls `0x0024C460(7)` (`0x003B16EB`) |
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

Among its own stores the reset zeroes the byte `0x02099DA2` (`0x00267166`, `sil` cleared at `0x00266D3E`). No other
RIP-relative, image-base-relative or address-forming reference names it, and the bytes beside it, `0x02099DA1` and
`0x02099DA3`, are read and written one byte at a time.

The `0x48`-byte records are the [script gauges](../Menus-And-HUD/script-gauges.md)' record pool, which `0x003E7DF0`
(called at `0x00266E3D`) builds; its layout is on that page.

The eight pairs are the countdown slots: `0x14`-byte records at `0x02B5EBC0`, whose fields are laid out on
[chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md). `0x003EBAB0` (called at `0x00266D95`) sets
each slot's start `+0x00`, target `+0x04` and value `+0x08` to 0 and stores the word `0x100` at `+0x10`, so the
running byte `+0x10` is 0 and the expired byte `+0x11` is 1 (`0x003EBAB2`-`0x003EBB5D`).

The step `0x003EB9A0`, from the field tick `0x00314020` (`0x00314056`), runs when its gates pass
(`0x003EB9A4`-`0x003EB9F1`) and walks all eight slots. For each slot that is running and not expired it adds the step
`+0x0C` times the integer `0x0035E790()` returns to the value; once the value reaches the target `+0x04` it stores
the target as the value and sets the expired byte (`0x003EBA17`-`0x003EBA6B`).

| Slot | Record | Who drives it |
|---|---|---|
| 0 | `0x02B5EBC0` | the enemy respawn clock `0x0032A100` ([enemy respawning](../Enemy-Spawning/enemy-respawning.md)): `0x003EBB70` (`0x0032A106`), `0x003EBBB0(0, 0, 1)` (`0x0032A117`), `0x003EBD00` (`0x0032A11E`), `0x003EBA90` (`0x0032A125`) |
| 1 | `0x02B5EBD4` | the chocobo ride: `0x00304060` (`0x003040DA`, `0x003040E4`), `0x00304790` (`0x003047A7`, `0x003047B5`), and the ride tick `0x00304440` reads its value and its expired byte (`0x00304479`, `0x003044B4`) |
| 2 | `0x02B5EBE8` | the chocobo turbo: `0x00303F00` (`0x00303FBE`, `0x00303FC8`), `0x00304060` (`0x003040FF`, `0x00304109`), `0x003047C0` (`0x003047CE`, `0x003047DC`), `0x00304440` (`0x00304492`, `0x003044F1`); the summon countdown: `0x00313600` (`0x00313622`, `0x0031362C`), `0x00313760` (`0x00313797`, `0x003137B0`), `0x003139D0` (`0x003139E7`, `0x003139F5`) ([party control modes](party-control-modes.md)) |
| 3, 4 | `0x02B5EBFC`, `0x02B5EC10` | the event-timer verbs, whose slot is their argument plus 3, held to 3 or 4: `seteventtimer` (`0x0034F1A0`, `0x003EBBB0` at `0x0034F1FD`), `starteventtimer` (`0x00350620`, `0x003EBD00` at `0x0035063F` and `0x00350654`), `istermeventtimer` (`0x0034F730`, `0x003EBB70` at `0x0034F75C`), `geteventtimer` (`0x0034FD30`, `0x003EBA90` at `0x0034FD5C`), `pauseeventtimer` (`0x00350100`: `0x003EBB90` at `0x00350148` when its first argument is non-zero, else `0x003EBD00` at `0x00350157`) |
| 5, 6, 7 | `0x02B5EC24`, `0x02B5EC38`, `0x02B5EC4C` | the reset `0x003EBAB0` and the step `0x003EB9A0` |

The accessors, each taking the slot index: `0x003EBBB0(slot, start, target)` and `0x003EBC50(slot, value, target)`
load a slot, `0x003EBD00` starts it (or marks it expired when start and target already agree), `0x003EBB90` clears its
running byte, `0x003EBA90` returns its value and `0x003EBB70` its expired byte.

`0x0036F4D0` runs `0x00382910`, which clears the first word of 8 records at `0x02AED700` (stride `0xE0`), sets the
four-float vectors `0x02AEDF70` and `0x02AEDF80` to (0, 0, 0, 1.0) and the words `0x02AEDF90`, `0x02AEDF98` and `0x02AEDF9C` to
0 (`0x0038295A`-`0x00382980`), and builds two view records with `0x004679C0(record, width, height)`: `0x02AED4A0` for the
frame size `[0x022D8EAC]` × `[0x022D8EB4]` and `0x02AED500` for 2000 × 2000. Last it sets the focus render index `0x02AEDFA0`
to -1 (`0x003829A4`; [post-processing](../Graphics/post-processing.md)).

A view record holds the integer size at `+0x44` / `+0x48`, the depth limits `near` = 1024 and `far` = 16,776,191 at
`+0x4C` / `+0x50`, and `0x00229D20()` at `+0x40`. It sets `+0x00 = width × 0.5` and `+0x14 = height × -0.5`
(`0x00467A0F`-`0x00467A26`), the depth scale `+0x28 = (far - near) × -0.5` and offset `+0x38 = (far + near) × 0.5`
(`0x00467A2B`-`0x00467A62`), 2048 at `+0x30` / `+0x34` as the screen offset and 1.0 at `+0x3C`, and zeroes `+0x04` to
`+0x13`, `+0x18` to `+0x27` and `+0x2C` (`0x004679FC`-`0x00467A08`, `0x00467A30`).

Step 4's `0x00184660` ends with `0x00248410`, which sets `0x0208ECC0` / `0x0208ECC4` to minus half of `[0x01E0C1D8]` /
`[0x01E0C1DC]` (as floats) and, for each of the four objects at `0x0208EA20` to `0x0208EA38` that is not null, stores 0 at
`+0x98` and that size as two 16-bit words at `+0x9C` / `+0x9E` (`0x00248454`-`0x002484EE`), and `0x0024B100`, which copies
the size into the halfwords `0x01E0C1D4` / `0x01E0C1D6`.

## Layouts

Globals written by the boot fixer:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x02EB4234` | `u8` |  | generator first-use latch |
| `0x02EB3870` | `u32[624]` | Mersenne Twister state |  |
| `0x01DFE0B4` | `u32` |  | frame base 1 or 2 |
| `0x01DFE0B8` | `f32` |  | time base 1.0 / 2.0 |
| `0x01DFE0BC` | `f32` |  | time base 1.0 / 0.5 |
| `0x01F82E38` | `u32` |  | 60 fps mode flag |
| `0x01DFE0C0` | `u32` |  | the mode suppressor |
| `0x01F82E3C` | `u8` |  | timer period begun |
| `0x01F82E40` | `u32` |  | the period |
| `0x02064ACC` | `u32` |  | pacer ticks per frame: 2 / [`0x01DFE0B4`] |
| `0x01E0C2A0` | `u16` |  | confirm mask |
| `0x01E0C2A4` | `u16` |  | cancel mask |
| `0x01FD4A64` | `u32` | DecideButton non-zero |  |
| `0x01E02814` | `u32` |  | language index |
| `0x01E0281C` | `u32` | 10 |  |
| `0x01F7F490` | `...` |  | the code_steam.txt id |
| `0x01F7F4A0` | `...` |  | the data.txt id |
| `0x01FD49F0` | `void*` |  | block of arena 5 |
| `0x01FD49F8` | `void*` |  | block of arena 2 |
| `0x01FD4A00` | `void*` |  | block of arena 3 |
| `0x01FD4A08` | `void*` |  | block of arena 4 |
| `0x01FD4A10` | `void*` |  | block of arena 6 |
| `0x01FD4A18` | `void*` |  | block of arena 11 |
| `0x01FD4A20` | `void*` |  | the unregistered `0x80000` block |
| `0x01FD4A30` | `void*` |  | block of arena 7 |
| `0x01FD4A38` | `void*` |  | block of arena 8 |
| `0x01FD4A40` | `void*` |  | block of arena 9 |
| `0x01FD4A90` | `void*` |  | the unregistered 1 MiB block, the per-model oscillator table |
| `0x02064AA4` | `u32` |  | the main state machine's cell |
| `0x02064AC0` | `...` |  | the main state machine's cells `0x02064AC0` to `0x02064AD4` |
| `0x01FD4A78` | `void*` |  | `0x01FE0000` (`0x01FE4A9F` rounded down to 64 KiB, `0x0022A13F`-`0x0022A152`) |
| `0x022C2528` | `u32` |  | the -nologo flag |
| `0x022D7FD0` | `...` |  | arena table, `0xA8` per id, 15 ids |

## Shipped data

| Fact | Value |
|---|---|
| default seed, boot seed | `0x1571` (5489), `0x11B9` (4537) |
| reload seed | `(((low + 0x2B5A5) * 0x21 + high) & 0x7FFFFFFF) + [0x01FD4A80] * 600` from `_time64` |
| time base at 60 fps | `0x01DFE0B4` 2, `0x01DFE0B8` 2.0 (`0x01CEBC08`), `0x01DFE0BC` 0.5 (`0x01CEBB70`) |
| ticks per frame | 2 at 30 fps, 1 at 60 |
| masks | confirm `0x4000`, cancel `0x2000`; swapped when DecideButton is 0 |
| registered arenas | 255.6 MiB in nine; 257.1 MiB allocated in eleven |
| command line | `-nologo` in any argument, as an exact eight-byte match; `debug` as the second argument, which zeroes `0x02B62DB4` |

[The command-line switches](startup-constants-inputs.tsv) table gives each switch's values, what else sets the
same state, when it takes effect, what reads it, what the player sees and when it changes nothing. `-nologo` sets
the first-start flag that the title screen script tests through `isFirstStartDone()` (verb `0x5A7`), so the first
title screen of a launch comes without the SQUARE ENIX logo and the autosave notice. `debug` changes nothing in the
shipped game, because the start-up field it clears is read only when `0x01E02804` is not negative, and it is -1.

### Columns of startup-constants-inputs.tsv

| Column | Holds |
|---|---|
| `label` | how the input is given: `command-line switch -nologo` or `second command-line argument debug` |
| `domain` | which arguments count: `-nologo` in any argument as an exact eight-byte match with its terminator (`0x0022BE40`-`0x0022BE52`); `debug` as the exact second argument (compared at `0x00408DA1`-`0x00408DC2`) |
| `precedence` | the other writers of the same state: for `-nologo`, verb `0x5A8` and the zone restore path `0x00314530`, which also store 1 in the first-start flag `0x022C2528`; for `debug`, that it overrides the FF12CONFIG start-up field copied to `0x02B62DB4` |
| `consumers` | the code that reads the state: verb `0x5A7` `isFirstStartDone`, which the title screen script `ttl_a01` tests; the start-up field selection `0x003318C4`-`0x003318FE` |
| `visible_effect` | what the player sees: for `-nologo`, the first title screen of a launch without the SQUARE ENIX logo and the autosave notice; for `debug`, that the shipped game shows no change |
| `inert_when` | when the input does nothing: for `-nologo`, every later visit to the title screen in the same launch; for `debug`, always, because `0x02B62DAD` is 1 only when `0x01E02804` is not negative, and it is -1 in the image |

## Operations

Once per launch, inside the init job, before the startup latch closes: the frame-rate selection,
the masks, the language, the state-machine cells, the eleven allocations and nine registrations,
the one-time initialisers of every subsystem, and the seed. The field frame reads the ticks-per-frame
constant every frame; the time base is read wherever a frame count is converted.

## State

The generator latch and state; the time-base triple, the mode flag and its suppressor; the
ticks-per-frame constant; the masks and the DecideButton flag; the language index; the block
pointers and the arena table.

The countdown slots, field by field:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02B5EBD4`, `0x02B5EBE8`, `0x02B5EBFC`, `0x02B5EC10`, `0x02B5EC24`, `0x02B5EC38`, `0x02B5EC4C` | `i32` | 0 (zero-filled tail of `.data`) | `+0x00` start of countdown slots 1 to 7 | `0x003EBAB0` (`0x003EBACA`, `0x003EBAD7`, `0x003EBAE4`, `0x003EBAF1`, `0x003EBAFE`, `0x003EBB0B`, `0x003EBB18`, 0); `0x003EBBB0` (`0x003EBBC8`); `0x003EBC50` (`0x003EBC79`, the value truncated) | `0x003EBBB0` (`0x003EBBEC`); `0x003EBC50` (`0x003EBC98`); `0x003EBD00` (`0x003EBD12`) |
| `0x02B5EBC4`, `0x02B5EBD8`, `0x02B5EBEC`, `0x02B5EC00`, `0x02B5EC14`, `0x02B5EC28`, `0x02B5EC3C`, `0x02B5EC50` | `i32` | 0 (zero-filled tail of `.data`) | `+0x04` target of slots 0 to 7; the reset clears it together with the `f32` value `+0x08` in one 8-byte store | target: `0x003EBAB0` (`0x003EBAB2`, `0x003EBAC3`, `0x003EBAD0`, `0x003EBADD`, `0x003EBAEA`, `0x003EBAF7`, `0x003EBB04`, `0x003EBB11`); `0x003EBBB0` (`0x003EBBCB`); `0x003EBC50` (`0x003EBC74`). value: the same reset stores; `0x003EBBB0` (`0x003EBC14`); `0x003EBC50` (`0x003EBCC0`, `0x003EBCDC`); `0x003EB9A0` (`0x003EBA4A`, `0x003EBA5B`) | target: `0x003EBBB0` (`0x003EBBEF`); `0x003EBC50` (`0x003EBC9B`); `0x003EBD00` (`0x003EBD0E`); `0x003EB9A0` (`0x003EBA3A`). value: `0x003EB9A0` (`0x003EBA45`); `0x003EBA90` (`0x003EBA9E`) |
| `0x02B5EBE4`, `0x02B5EBF8`, `0x02B5EC0C`, `0x02B5EC20`, `0x02B5EC34`, `0x02B5EC48`, `0x02B5EC5C` | `u8` | 0 (zero-filled tail of `.data`) | `+0x10` running byte of slots 1 to 7; the reset's `u16` store of `0x100` also sets the expired byte `+0x11` to 1 | running: `0x003EBAB0` (`0x003EBB27`, `0x003EBB30`, `0x003EBB39`, `0x003EBB42`, `0x003EBB4B`, `0x003EBB54`, `0x003EBB5D`); `0x003EBBB0` (`0x003EBC0F`, 0); `0x003EBC50` (`0x003EBCBB`, 0); `0x003EBD00` (`0x003EBD17`, 1); `0x003EBB90` (`0x003EBB9E`, 0). expired: the same reset stores; `0x003EBBB0` (`0x003EBC24`, `0x003EBC34`); `0x003EBC50` (`0x003EBCD0`, `0x003EBCD7`); `0x003EBD00` (`0x003EBD1D`); `0x003EB9A0` (`0x003EBA60`) | running: `0x003EB9A0` (`0x003EBA1C`). expired: `0x003EB9A0` (`0x003EBA29`); `0x003EBB70` (`0x003EBB7E`) |

## Modding notes

- Determinism from boot holds for the Mersenne Twister only; the loot generator is a separate
  counter-seeded LCG ([which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md)),
  and a save load reseeds the Twister from the clock.
- A port must reproduce the 4537 seed and the exact reload formula to match the shipped stream.
- The time base is a published triple that over a hundred readers divide or multiply by; changing
  FrameLimit at run time without rewriting all four cells leaves the engine inconsistent.
- The masks are read as masks against the pad word; swapping them is the whole of the confirm
  button setting.
- Arenas 2 to 9 keep their boot blocks. Arena 11 is re-sized by `0x0037B3D0`. Arenas 13 and 14 are freed and
  registered again, from arena 5 blocks of `0x100000` and `0x19000` bytes, by `0x0025A990` and `0x0025AA30`, which
  the manager bind `0x0026C8C0` calls (`0x0026CA29`, `0x0026CA39`). Arena 12 is registered by the script command
  `setexpandvoicememory` (`0x0395`, `0x003E9AA0`, `0x003E9AEF`).

## Related

- [Game application](game-application.md): the init job that calls the boot fixer.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): FrameLimit and DecideButton in the
  settings object.
- [Random number generators](../Random-Numbers/random-number-generators.md): the Mersenne
  Twister and its seeders.
- [Frame update order](frame-update-order.md): the state machine whose cells are initialised here.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Gameplay: `0x00304440` calls `0x0030D9A0`; those functions are documented on
  [frame update order](frame-update-order.md).
- Story event quest hunt: `0x0026C8C0` calls `0x00377440`; those functions are documented on
  [actor managers](../Characters-And-Objects/actor-managers.md).
