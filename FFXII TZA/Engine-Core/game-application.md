---
title: "Game application object: the root object, its vtable and the boot order"
kind: "system"
category: "Engine core"
addresses: "0x0015BC40, 0x0017CC70, 0x0017CEB0, 0x0017CF30, 0x0017CCD0, 0x0017CDE0, 0x0017CDC0, 0x0017CE50, 0x0017D090, 0x0017D0C0, 0x0017D120, 0x0017D160, 0x0017D1A0, 0x0017D210, 0x0017CFD0, 0x0017D170, 0x0017CDF0, 0x0017CE20, 0x0017D1E0, 0x0017D000, 0x0017D4C0, 0x0017D650, 0x0017D670, 0x0017D6B0, 0x0017D6E0, 0x0022A490, 0x0022A580, 0x00189000, 0x00189120, 0x0019A0A0, 0x001A11B0, 0x001B7EE0, 0x001C18A0, 0x001C2F00, 0x001D8CD0, 0x001BDA50, 0x001C0D40, 0x001BBFC0, 0x001A98B0, 0x00199790, 0x001997D0, 0x001E0550, 0x001E0590, 0x001E05E0, 0x001E05F0, 0x0018A620, 0x0018A7D0, 0x00186230, 0x005C5230, 0x001999D0, 0x00199F60, 0x0019DA30, 0x0019EB00, 0x001B9370, 0x00184F20, 0x01F82CD8, 0x001D89D0, 0x001D8AB0, 0x001D8700, 0x001D7A20, 0x001D8770, 0x001BAA30, 0x001E03F0, 0x00186010, 0x00187550, 0x00187860, 0x001876E0, 0x0017E720, 0x0017E4E0, 0x00229590, 0x00250540, 0x001D72F0, 0x0022A770"
---

## What the player sees

The moment the game finds its data. Everything a player ever sees comes through one archive,
`FFXII_TZA.vbf`, opened once at start by the application object; a few steps later one byte is set
that the rest of the application waits on. Before it is set the window exists but nothing runs;
after it, every frame goes through the same tick: the managers are pumped in a fixed order, the
game's own state machine advances, the screen fade is stepped, and the frame ends. Scaling the application's time passes through this object; a pause byte the framework keeps here
is never read by the game.

## How it works

### The object and its class

`GameApplication` is the static object at `0x01F7E350`, `0x1140` (4,416) bytes. Its static
initialiser `0x0015BC40` runs the base constructor `0x00792350`, installs the vtable `0x008C5760`,
clears the word at `+0x113C` (the latch and the run-once byte), registers the object with
`0x007A1190(app, 0x9CA5)`, initialises two framework singletons (`0x01F2CDF8` and `0x01F2CE20` through
their vtable slot 1 while `0x01F2CDF0` is clear) and registers the destructor `0x008A6970` with
`atexit`.

The deleting destructor, slot 0 (`0x0017CC70`), re-installs the vtable, runs the base
destructor `0x00793250` and, with flag bit 0 set, frees: through the guarded indirect call with the size `0x1140` when bit
2 is set, else `0x00584730(this)`.

The base is `Phyre::PFramework::PApplication`: `0x00793250` writes its vtable `0x01CB2508` into
`[this]`, and the RTTI chain names `PApplication` at displacement 0 and `Phyre::PBase` and
`Phyre::PMemoryBase` at 8. The base vtable has the same 31 slots; the ten slots this class does not
override (1, 12, 13, 17, 18, 19, 20, 28, 29, 30) hold the same addresses in both tables, slot 14 is a
thunk to the base's own body, and slots 11, 26 and 27 are shared stubs in both. So the frame tick,
the archive mount and the latch are game code overriding middleware entry points.

### The vtable

| Slot | Address | What it does |
|---|---|---|
| 0 | `0x0017CC70` | deleting destructor; states the size `0x1140` |
| 2 | `0x0017CEB0` | the archive mount (below) |
| 3 | `0x0017CF30` | window and device set-up; queues the init job |
| 4 | `0x0017CCD0` | the frame tick (below) |
| 5 | `0x0017CDE0` | a thunk to the empty stub: an explicitly empty override |
| 6 | `0x0017CDC0` | shutdown: `0x0017D670` (`0x0019A120`, `0x001A11F0`, `0x001DC4E0`, `0x001993B0` on the input manager, `0x0022A090`, `0x0017DAC0(1)`) then the base's slot 6 `0x0079BF70` |
| 7 | `0x0017CE50` | input: with a dialog open (`0x00228480`) it hands the input manager `0x00198790()` to `0x001967D0` and returns 0 without reading the latch; otherwise, latched, it calls the handler `0x00194AF0()` when one is set |
| 8 | `0x0017D090` | render: 0 while unlatched, else `0x00187950` on the render manager `0x00189120()` |
| 9 | `0x0017D0C0` | resize: copies the viewport size `+0xD24`/`+0xD28` into the render manager's `+0xAD8`/`+0xADC`, then the base's `0x007A05D0` |
| 10 | `0x0017D120` | sets the render manager's byte `+0` to 1 |
| 14 | `0x0017D160` | the base's `0x007A0B40`: stores the argument byte at `+0x27` |
| 15, 25 | `0x0017D1A0`, `0x0017D1E0` | forward a byte to the input manager (`0x001989D0`, `0x00198E70`) |
| 16 | `0x0017D210` | `0x00227D40(byte)` |
| 21, 22 | `0x0017CFD0`, `0x0017D170` | read and write the pause byte at `0x01F810F0` (`0x00199780`, `0x001997E0`); `0x0017E4E0` reads it for the frame and the console draw `0x001D7A20` tests it |
| 23, 24 | `0x0017CDF0`, `0x0017CE20` | the base's `0x0079D560` and `0x0079D5B0` times the time scale `0x0017E440()` |
| 1, 12, 13, 17-20, 28-30 | the base's | inherited unchanged |
| 11, 26, 27 | `0x005C5230`, `0x0016D6A0`, `0x005C5230` | the shared return-zero and return stubs |

### The boot order

Slot 2, `0x0017CEB0(this, a, b)`, stores `a` at `+0x1130` and `b` at `+0x1138`, moves up three
directories (`0x0059A770("../../..")`), runs `0x0019B190()`, mounts `../FFXII_TZA.vbf` on the file system `0x0019B1F0()`
(`0x0019B070`), runs the early set-up `0x0017D6B0` (`0x0017DAC0(0)`, `0x001DDA70`, `0x001D6BE0`, `0x001BE3E0`,
`0x0019CDE0`, the debug display `0x001C2F00`, `0x001DBA40`) and `0x00182F70` with the viewport size
`+0xD24`/`+0xD28`. The archive path is relative to the executable.

`0x0017DAC0(on)` reads the Sticky Keys settings (`SystemParametersInfoW` action `0x3A`) and, when
their hot-key bit 2 differs from `on`, writes them back with that bit changed (action `0x3B`): the
boot turns the Sticky Keys shortcut off and the shutdown's `0x0017DAC0(1)` turns it on
(platform). `0x001DBA40` starts the sound engine
([sound engine config](../Sound-And-Music/sound-engine-config.md)).

Slot 3, `0x0017CF30`, configures the device (`0x0018D850` with `0x00193D50()`, `0x00182EB0()`, `0x00182E80()`
and the device byte `+0xD48` of `0x00796E20()`), ensures the two `AsyncJobManager` instances
(`0x0019A0A0`: `0x01F810F8` and `0x01F81100`, `0x158` bytes each, flags 0 and 1), and queues a job node
`{0x0017D150, this}` on the first (`0x00199F10`, `0x0019A000`).

That job runs `0x0017D000(app)`: the
manager-init burst `0x0017D4C0`, the `0x80`-byte object at `0x01F7E340` (`0x0018A840`), the render
manager (`0x00189000(app + 0xE8, app + 0x90, +0xD24, +0xD28, [0x01FD4A9C])`, `0xDD8` bytes at `0x01F7F598`),
and then the latch: `+0x113C = 1`. Nothing clears it afterwards.

`0x0017D4C0(b, a)` builds the managers in order: `0x001DB500`, the pause flag (`0x00199790`), four small
objects at `0x01F7F4C0` (`0x20`), `0x01F7F4C8` (`0xC0`), `0x01F7F4D0` (`0x10`) and `0x01F7F4D8` (`0xA0`), the
`AsyncLoadManager` (`0x001A11B0`), `0x00198750`, `0x0019EF40`, `0x001B6BC0`, `0x001B29F0`, the movie player
(`0x001B7EE0`, then `0x001B7850`), the `SaveloadManager` (`0x001C18A0`, `0x001C1710`, `0x001C1940`), `0x001B5F10`,
`0x001D6990`, `0x001D8150`, `0x001D89D0`, `0x001831A0`, and the startup constants `0x0022A0B0(b, a)`
([startup constants](startup-constants.md)).

After the constants come `0x001B1BA0`, `0x001B1580`, `0x0022A4B0`, the screen fade
(`0x001D8CD0`), a `0x10`-byte object at `0x01F7F4E0` (`0x001D5600`), `0x001AD3E0`, the procedural-texture
context (`0x001C0D40`), `0x001D62D0`, `0x00194AB0`, `0x00194AA0(0x00194AF0())` and `0x001DB1E0`.

### What the burst builds

| Global | Size | Ensure | Constructor | What the constructor lays down |
|---|---|---|---|---|
| `0x01F810F8`, `0x01F81100` | `0x158` | `0x0019A0A0` | `0x001999D0(obj, flag)` | `AsyncJobManager`: a job list at `+0x50`, a pool of 128 sixteen-byte job nodes at `+0x90`, the flag at `+0x150`; `0x00199F60` then starts its worker |
| `0x01F81150` | `0x120` | `0x0019CDE0` (early set-up) | `0x0019C7C0` | the loaded-asset registry `0x0019CE20` returns: a lock at `+0x00`, a map at `+0x28` and a pool of 6,144 records at `+0x60` (`0x0019C630`) |
| `0x01F81158` | `0x188` | `0x0019EF40` | `0x0019DA30` | `AssetListManager`: a pool of 192 lists of `0x130` bytes at `+0x08` (`0x0019D5B0`) and a pool of 3,072 entries of `0x118` bytes at `+0xC8` (`0x0019D740`) |
| `0x01F81240` | `0x238` | `0x001BBFC0` | `0x001B9370` | the model asset cache: three maps, a list and a pool of 384 records of `0x2A8` bytes at `+0xE8` (`0x001B8E90`) |
| `0x01F7F4D8` | `0xA0` | `0x0017D4C0` itself | `0x001B24D0` | 32 words of 10,000 at `+0x00`, `+0x80` pointing at `+0x00` and `+0x88` at `+0x40`; `0x00862BF0` to `0x00862C40` read its `+0x90` and `+0x94` |
| `0x01F7F598` | `0xDD8` | `0x00189000` | `0x00184F20` | the render manager (below) |

`0x00199F60` names the worker thread `"AsyncJobManager Thread"`, or `"AsyncJobManager No Read No
Write Thread"` when the flag is non-zero, starts it (`0x005CD1E0`) and sets `+0x154` and `+0x20`. The destructor body `0x00199C30` (deleting wrapper `0x00199D50`, which
frees `0x158` bytes) clears `+0x154`, waits for the thread to exit (`0x005CD330`:
`WaitForSingleObject`, `GetExitCodeThread`), and releases the pools and the job list.

The pools share one template (`0x001997F0` for the job nodes, `0x0019D5B0`, `0x0019D740`,
`0x001B8E90`): a vector of N records, a set at `+0x20` filled with the address of every record, a
second set at `+0x58`, and a lock at `+0x90` created (`0x005CD0A0`) when the flag byte `+0xB8` is set.

The loops `0x0019CE30`, `0x0019CEF0`, `0x0019D100`, `0x0019D1D0` and `0x0019D420` copy, move and fill the
`0x130`-byte lists while the vector is sized; `0x0019CFA0`, `0x0019D050`, `0x0019D350` and `0x0019D510` do
the same for the `0x118`-byte entries. The template's destructors (`0x00199A80`, `0x0019C870`, `0x0019DAD0`, `0x001B3AF0`,
`0x001E74F0`) are described on [object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md).

An asset list is 256 bytes copied as a block, a vector of entry pointers at `+0x100`, a word at
`+0x120` and a ready byte at `+0x128`. `0x0019EB00(manager, list)` holds when the ready byte is set and
every entry has its byte `+2` set. The map-art update `0x001A9ED0`, the model asset cache `0x001BC190`,
the procedural-texture context `0x001C0DD0` and `0x001BB120` ask it before they use a list.

In the model asset cache, `0x001B9A10` finds or inserts a node by a 32-bit key in a map (its caller
`0x001BAA30` uses it 16 times), `0x001BA910` empties a map of `0x58`-byte nodes, and `0x001BBF40`, from
the cache's update `0x001BC190`, releases the 32 handles at `+0xA0` (`0x00183720`) and zeroes `+0xA0`
and `+0x1A0`.

`0x001BAA30(cache, model)` binds a model's palette textures; `0x001BC190` calls it, and so does
`0x001BB120` once the model's asset list (`+0x08`) is ready (`0x0019EB00`). It reads the names of the
list in two passes:

1. a texture named `tex_<n>_clut_-1` is palette n: its data address goes to `+0x1A0 + n × 8`, and a
   handle from `0x00183780(0, 1 << d, 1, 0x20)`, d the digit after `idx` in the name, to `+0xA0 + n × 8`;
2. a texture `tex_<n>_clut_<m>` with any other m fills the entry of key `n << 16 | (m & 0xFF)` in the
   map at `+0x10` (`0x001B9A10`, which inserts a zeroed entry for a new key): a `_n.dds` name goes to
   `+0x08`, `_spec.dds` to `+0x10`, `_diffuseCorrection.dds` to `+0x18`, each only while that field
   is empty, and any other name to `+0x00` while it is empty, which then also takes palette n's address at `+0x20` and its
   handle at `+0x28`.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | base | the colour texture |
| `+0x08` | `void*` | normal | the `_n.dds` texture |
| `+0x10` | `void*` | specular | the `_spec.dds` texture |
| `+0x18` | `void*` | diffuseCorrection | the `_diffuseCorrection.dds` texture |
| `+0x20` | `void*` | palette | palette n's data |
| `+0x28` | `void*` | paletteHandle | palette n's handle |

`0x00184F20` builds the render manager: two `0x338`-byte camera blocks at `+0x20` and `+0x358` and a
third at `+0x690` (`0x00184CE0`), the viewport size at `+0xAD8` / `+0xADC`, the four callback slots
at `+0xC38`, 5.0 at `+0xD14`, the boot argument byte `[0x01FD4A9C]` at `+0xDB8`, then `0x00186CD0`. Its
height query `0x00186820` answers 2,160 while `+0xDB8` is set or `+0xC30` is 3, else `+0xADC`.

### The frame tick

Slot 4, `0x0017CCD0`, returns 0 through the stub while the latch is clear. Otherwise it takes the
frame delta, the double at `+0x48`, ensures the camera-pair object `0x01F7F5D0` (`0x0018A620`, `0x270`
bytes with two `Phyre::PCameraPerspective` members; the first `0x0018A670` call hands it the delta), reads the running byte at `[0x0018A7D0()]`
(the three-byte object `0x01F7F5D8`), and on its first call runs `0x0017D650` (`0x001D6C00`, `0x001BE3E0`)
and sets the run-once byte `+0x113D`. The two calls to `0x0018A670` around that read are a thunk to
the byte getter `0x00229F90` (`0x01FD49ED`) whose arguments are unused.

With the running byte clear the pump runs in mode 0. With it set and `0x01FD4A88` set, the object
`0x01F7F5E0` is reset (`0x0018B040`: `0x0018B3F0(obj, 0)`, `+0x24` = 0, `+0x2C` = -1), every element of the
vector `0x01F7F5E8` is destroyed through its vtable slot 0 and the vector emptied (`0x0018B810`), the
pump runs in mode 0 and `0x01FD4A88` is cleared; with it set and `0x01FD4A88` clear the pump runs in
mode 1. A pump result of 0 returns 9; anything else returns 0.

`0x0017D6E0(dt, mode)` is the pump. It clears `0x01F7F4B8`, runs the render manager's deferred
callback ring (`0x00186230`: one of four slots at `+0xC38`, index `+0xCB8`) while `0x01FD4A68` is clear,
and then loops over passes:

1. `0x0022CB90()`; when the pacing predicate `0x001E05F0` holds and this is not the second pass,
   `0x001E0550` arms `0x01F82D31` and clears `0x01F82D30`. The predicate, with `0x01E02801` set, runs
   `0x001E03F0()` and holds when `0x00187540` on the render manager returns 0 and `0x001E04F0()` is at or
   below `0x01F82D28`; with `0x01E02801` clear it resets `0x01DFDDF8` to the largest double and `0x01F82D28`
   to 0 and fails;
2. the pause byte's getter `0x001997D0` is called and its result handed to the return stub
   `0x0016D6A0`, a compiled-out hook; `0x01F7F4B0 = dt`; `0x001A1460(0x01F7F4C0)`; `0x001DB600()`; the render manager's `0x00189CE0` and `0x00189570`;
3. the recycle queue `0x001BDAC0` (`0x01F81248`), the `AsyncLoadManager` `0x001A1310` (`0x01F81160`), the
   `AsyncJobManager` through its vtable (`0x0019A170()`), the map-art context `0x001A9ED0(ctx, dt)`
   (`0x01F81168`), the procedural-texture context `0x001C0DD0` (`0x01F81258`), the model asset cache
   `0x001BC190` (`0x01F81240`), `0x001CC600()`;
4. the movie player `0x001B8400(player, dt)` (`0x01F81218`: `+4` is the status
   `getmoviestatus` reads through `0x00184860`, `0x001B82F0` starts a movie);
5. the game step `0x0022A490(dt, mode != 0)`: it stores the mode at `0x02064AA0`, runs the main state
   machine `0x0022A580` (states 0 to 6 at `0x02064AD3`, [frame update order](frame-update-order.md))
   and increments `0x02064AD0` when `0x0022A580` returns non-zero; `0x0022A490` returns nothing of its
   own, so the pump's result is `0x0022A580`'s register value surviving the increment;
6. `0x001D8AB0(0x001D8A60(), dt)`, the `SaveloadManager` `0x001C1910` (`0x01F81260`), the screen fade
   `0x001D9080` (`0x01F82CE0`), and the `MultipleDebugDisplay` (`0x01F81270`): `0x0022FFE0` when its byte
   `+0x463C` is set, then the auto-test walker `0x001C2F50`
   ([event scenes](../Scripts-And-Script-Commands/event-scenes.md));
7. when `0x01F82D30` is clear the pump returns (`0x001E0560`, at the end of `0x0022A580`, sets it when
   `0x01F82D31` was armed; states 4 and 6 also call `0x001E0580` before their handlers); otherwise the frame-end reset `0x001E0590` runs
   (`0x00185D80` on the render manager, `0x0018B040(0x01F7F5E0)`, `0x0018C8F0(0x01F7F5E8)`, `0x001DB620`,
   `0x001A14D0(0x01F7F4C0)`, both bytes cleared), `0x01F7F4B8` is set, `dt` becomes 0 and the next pass
   starts.

`0x001E03F0` keeps the pacing balance `0x01F82D28`. With `0x01FD4A68` clear it adds the real time since
its last call (`0x005CC930` minus `0x02CB60E8`, kept in `0x01DFDDF8`; nothing on the first call) minus n
frame periods, n = `[0x01F3DA18]` (`0x00184950`). The period is 1/60 s when `0x0017FE30()` (`0x0079CFA0` on
`0x001DDAB0()`) is a multiple of 10, else 0.0166833 s. The balance is clamped to plus or minus 4 × n
periods, or 300 × n while the movie player is in state 3, playing (`0x001B7D20`;
[movies](../Graphics/movies.md)).

The procedural-texture context's update `0x001C0DD0` does its work once: when its asset list `[ctx]`
is ready (`0x0019EB00`) it indexes it with `0x001BF2E0` and sets `ctx + 8`. For each asset name (from byte
3 of the entry) `0x001BF2E0` drops the directory and the extension, and `0x001C0670` splits the rest at
its last `_`: the part before is the key; a suffix of exactly `color` clears the second output and
any other suffix sets it; a name without `_` is skipped.

A key that `0x001C01B0` does not find gets a `0x28`-byte record, the key and its position, appended to
the vector at `ctx + 0x58` (`0x001BEEF0` grows it) and entered in the map at `ctx + 0x78`. For a
non-`color` asset the record's `+0x20` receives an address inside the asset's object whose class
chain reaches `0x02CBB900`.

`0x001CC600` keeps the cutscene bookkeeping: it saves the current cut name `0x01F81358` to `0x01F81338`,
rebuilds it as `"Cut "` plus the queued count of the marked event slot (`0x001C3390` joins the two
strings; its sibling `0x001C3420` joins a C string to a string), and moves `0x01F81280` to `0x01F81281`
before setting `0x01F81280` to `0x002F1A20() != 0` and `0x0022A550() != 0`. `0x001C53B0` and `0x001C53D0`
report the rising and the falling edge of that byte.

Each pumped object is a lazily built singleton: a global pointer, an ensure function that
allocates a fixed size and constructs on first use, and a getter. The screen fade `0x01F82CE0` is a
`0x38`-byte record built disabled (`+0` = 0, `+0x10` = 3) ([screen fade](../Graphics/screen-fades.md)).

Its update `0x001D9080` draws first: inside a `"ScreenImage"` scope `0x001D8BB0` emits a quad over the screen
(corners from `0x001D8B20`) with colour 255, 255, 255 and the level `+0x1C` as alpha.

It then steps the float level `+0x1C` by the mode `+0x10`: `level += [+0x20]` in mode 0,
`level -= [+0x20]` in mode 1 (`0x001D90B5`-`0x001D90D0`). It adds 1 to the counter `+0x0C`; in mode 0
with `+0x0C >= +0x14` it sets `level = min(level, 255)` and the mode to 2, and in mode 1 with
`+0x0C >= +0x18` it sets `level = max(level, 0)` and calls `0x001D8C80` (`0x001D90D5`-`0x001D911F`).

### The screen captures

The render pass list `0x00187950` services two captures through the render manager:

1. `0x00186010`, when `+0xCD8` is 1, runs `0x00188730`, sets `+0xCD8` to 2, allocates width (`+0xCF0`) ×
   height × 3 bytes at `+0xCF8` (the height is `0x00186820`'s answer) and reads the frame into it
   (`0x00600070`, the device's slot 2, `0x00610330`);
2. `0x00187550`, when `+0xCD8` is 2, clears it, writes `/capture.tga` (an 18-byte header for an
   uncompressed 24-bit image, then the rows from the last to the first), frees the buffer and
   clears `+0xCD4`.

Only the constructor (0), `0x00186010` (2) and `0x00187550` (0) store to `+0xCD8`; `0x00186010` and `0x00188730`
(`0x00188748`) read it.

With the boot byte `+0xDB8` set, `0x00187860` also runs a 3840 × 2160 capture, keyed by the state
`+0xDAC`:

| State | Next | Action |
|---|---|---|
| 1 | 3 | sets `+0xDA8` to 6 |
| 3 | 4 | grabs the frame (`0x00185FB0`) and sets `+0xDA8` to 6 |
| 4 | 0 | writes the grab with `0x001876E0` |
| 6 | 7 | none |
| 7 | 7 | grabs on the first call (`0x01F7F5AC` = 1), then on each call writes the last grab and grabs again |

`0x001876E0` writes `/Capture 4K/capture%03d.tga` (counter `0x01F7F5A4`), or in state 7
`/Capture 4K/capture_series%03d_%04d.tga` (series `0x01F7F5A8`, frame `0x01F7F5AC`): an 18-byte header
and 2,160 rows of `0x2D00` bytes from `+0xDB0`, last row first.

### The loading page

The object the pump steps in pass step 6 through `0x001D8AB0(0x001D8A60(), dt)` is the `LoadingPage`
at `0x01F82CD8`, `0x40` bytes built by `0x001D89D0` in the init burst with a fade time of 0.264 s at
`+0x34` and a delay of 5.0 s at `+0x38`. It is the icon that turns while a load runs:

1. `0x001831A0` arms it (`0x001D8A90`: when the start time `+0x08` is 0, the armed byte `+0x1D` = 1).
   The save-load post-load sequence (`0x00582860`) and the zone change's restore path (`0x00314530`,
   [zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) call `0x001831A0`.
2. Each update `0x001D8700` stamps the start time on the first armed pass (`0x005CC930` minus
   `0x02CB60E8`); once 5 s have passed it sets the shown byte `+0x1C`, clears the armed byte and
   restarts the fade timer `+0x20`.
3. While shown, `0x001D8690` sets the alpha `+0x28`: timer / fade time × 255, capped at 255, on the
   way in; 255 minus that on the way out (`+0x24` set), clearing the shown byte once the timer
   passes the fade time. The update then adds `dt` to the timer and to the clock `+0x10`, and
   draws with the angle clock × π through `0x001D7A20`.
4. `0x001D7A20` draws nothing while the pause flag reads set (`0x00199780`). Otherwise it sets the
   sprite state (`0x001D8600`), places the four corners of the layout rectangle of `[0x01F82CD0]`
   centred for a 1920 × 1080 or 512 × 448 frame, writes the alpha into each, rotates them by the
   angle (`0x001D8790`) while the running byte `[0x0018A7D0()]` is 0, and emits them (`0x001B06D0`, `0x001B03D0`).
5. `0x00183070` dismisses it (`0x001D8770`): it zeroes the start time, clears the armed byte and,
   unless a fade-out already runs, starts one. The actor drive pass `0x0025D9E0` calls it, and so do
   six functions of the script layer, among them the handlers of `fadesync` (`0x00B9`, `0x0033F4C0`) and `calltelepoeffect`
   (`0x333`, `0x00344170`) ([native commands](../Scripts-And-Script-Commands/native-commands.md)).

A load shorter than 5 s therefore never shows the icon.

## Layouts

### The statics at 0x01F7F490

These cells sit in the static block at `0x01F7F490`; each row names the cell's own address first.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x38` | `void*` | containerCell | 0x01F7F4C8: the 0xC0-byte object the init burst 0x0017D4C0 builds (0x0017D4FC-0x0017D524) with 0x001A16E0, which runs 0x001A1500(object, 5000, 0): an EASTL vector of 16-byte elements at +0x00 grown to 5,000, two EASTL sets at +0x20 and +0x58, a lock at +0x90 and the byte +0xB8 = 0; no instruction reads the cell back |
| `+0x40` | `void*` | immediateTarget | 0x01F7F4D0: the 0x10-byte GeometryRenderTargetImmediate (vtable 0x008F5F28, RTTI) that 0x001A17D0 builds in the init burst, its +0x08 pointing at itself (0x0017D51F-0x0017D547). 0x001FB810(node, n) calls its +0x08's slot 0, 0x001F48B0, which wraps the node in a 0x28-byte GeometryInstanceOrderedObject from the ring allocator +0x30 and files it on [0x01F7F5E0] (0x001F48DE-0x001F4940); 0x001FB830 runs 0x001A1850, which with a render manager (0x00189120) wraps the node the same way and hands it to the new object's slot 1 with the manager's +0x08, and otherwise calls slot 0 with 0x40 (0x001A186F-0x001A190E). 0x0020E630(node, kind) submits through it (0x0020E63C-0x0020E66A) |
| `+0x48` | `void*` | sceneBracket | 0x01F7F4D8: the 0xA0-byte object 0x001B24D0 builds in the init burst (0x0017D542-0x0017D565) that brackets each effect layer (Effect element runtime): 0x00862C10 opens a layer with 0x001B2530, which stores the pass id at +0x90 and the layer at +0x94; 0x00862C30 closes it with 0x001B2600; 0x00862BF0, 0x00862C00 and 0x00862C40 return the two words |
| `+0x74` | `u32` | earlyWaterDraw | 0x01F7F504: the area's mEarlyWaterDraw setting, 1 when the scene config holds 1 (0x001C913A-0x001C9146 through 0x00182FE0); MainLoop_Draw reads it (0x0017FE20 at 0x0022B0ED) and, when it is set, draws the "Water effect" pass (0x0017F330, 0x00180A30) right after effect layer 3 (0x0022B416-0x0022B431), otherwise later in the frame (0x0022B46A-0x0022B48A) |
| `+0x78` | `u32` | nextRenderKey | 0x01F7F508: the key the next render record takes: each presentation set-up stores its model entry's id (entry +0x14) here just before 0x0042FB80 creates the render record (0x002E2980, 0x002E334D, 0x002EE2B3, 0x003EB2DE; the monster viewer's loader stores 0x02164210 at 0x002EE55F) and restores it after (0x002E299D, 0x002E3360, 0x002EE2C5, 0x002EE57E, 0x003EB2EF); the record's initialiser 0x00420480 copies it, when not 0, into the render record's key +0x6B0 (0x00420636-0x00420640) |
| `+0x7C` | `u8` | opaquePosted | 0x01F7F50C: once-per-frame latch of the RenderOpaqueObj command: 0x0017F070, called by MainLoop_Draw (0x0022B38F), posts the command on the render command vector (0x0018C580) only while this is 0 and the vector exists, and sets it to 1 (0x0017F074-0x0017F09A); 0x0017F270 (0x0022B331) clears it with +0x7D |
| `+0x7D` | `u8` | mapOpaquePosted | 0x01F7F50D: the same latch for the RenderMapOpaqueObj command, posted by 0x001809A0 (0x001809A4-0x001809CA; Map art); while it is set, +0x7E is 0 and the map-art context's +0x419 is 0, the map command's draw 0x001F3570 draws the characters' opaque objects before the map's (0x001F3586-0x001F35D0) and RenderOpaqueObj's draw 0x001F36B0 leaves them out (0x001F36B9-0x001F36D7) |
| `+0x7E` | `u8` | charsWithOpaque | 0x01F7F50E: 1 when the effect group draw 0x0024D370 runs with the open layer [0x01F7F4D8] + 0x94 at 2 and 0x003AA2E0 answers non-zero (0x0024D448-0x0024D45E, through 0x00183060); MainLoop_Draw clears it on a pass whose first argument is not 1 (0x0022B10D-0x0022B14D). While it is set both opaque draws leave the characters to RenderOpaqueObj (0x0017FE50 at 0x001F3586 and 0x001F36B9) |
| `+0xAC` | `f32` | parkedCubemapIntensity | 0x01F7F53C: mCubemapIntensity parked while the Bestiary's monster viewer is open: 0x001846F0 (0x0057025A) copies 0x02CB8138 here and zeroes 0x02CB8138 (0x001846FD-0x00184710); 0x001846B0 copies it back (0x001846C6-0x001846CE) |
| `+0xC0` | `f32[16]` | flareMatrix | 0x01F7F550: the lens-flare pass's corner matrix: 0x0017ED50 multiplies each row of the matrix it is given by the render manager's matrix +0x6C8 (0x0017E7E0 at 0x0017EDE4-0x0017EE20) and stores the four rows here (0x0017EE41-0x0017EF01), returning this address (0x0017EE3A); its only caller 0x00376470 transforms the flare's corners by it (0x00202D70 at 0x00376843-0x00376850; Lens flares) |

### The main loop cells at 0x02064AA0

These cells sit in the static block at `0x02064AA0`, the main loop cells of [Frame update order](frame-update-order.md); each row names the cell's own address first.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | bootStubResult | 0x02064AA4: written once at boot by 0x0022A0B0 with the result of 0x005C5230, which returns 0 (0x0022A0BB-0x0022A0C0; Startup constants); read by no function |
| `+0x33` | `i8` | battleRuntimeMode | 0x02064AD3: the main state 0x0022A580 dispatches on (Frame update order): 0 start-up 0x0022B6E0, 1 title and loading 0x0022B7E0, 2 the field frame 0x0022A770 (also any other value), 3 the full menu 0x0022B8C0, 4 the capture before a menu 0x0022AF50, 5 the capture-backed frame 0x0022BC20, 6 a second capture 0x0022B000. 0 at boot (0x0022A1A0); the handlers move it on (0x0022B74E to 1, 0x0022B85B to 2, 0x0022AFF2 to 3, 0x0022B097 to 5, 0x0022BB81 and 0x0022BDC5 to 2); 0x00229F00 sets it and 0x00229EA0 returns it |
| `+0x34` | `f32` | bootOne | 0x02064AD4: 1.0, stored once at boot (0x0022A190); read by no function |
| `+0x44` | `u32` | drawSkipped | 0x02064AE4: 1 when MainLoop_Draw returned at once on the skip request 0x01FD4A70, clearing the request (0x0022B196-0x0022B1A4); the field frame clears it before each draw (0x0022A824, r12d = 0 from 0x0022A78B). While it is set the next draw runs 0x00182370 in place of the GS register batch (0x0022B1C0-0x0022B1D2) |
| `+0x48` | `u32` | monsterShown | 0x02064AE8: 1 while the Bestiary's monster viewer shows a monster in the full menu frame (0x00181DD0 at 0x0022BA5D, set at 0x0022BA66); on the first frame without one 0x0022B8C0 clears it and runs 0x00314370(1) and 0x0036F510 (0x0022BA9A-0x0022BAB2) |
| `+0x4C` | `u32` | endOfPassCallback | 0x02064AEC: the end-of-pass callback word: 0x0022A580 tests it as a dword after the state handler and, when it is set, clears it (0x0022A731-0x0022A73F); no instruction stores a non-zero value |
| `+0x54` | `u8[3]` | vuClipFlags | 0x02064AF4: the emulated VU1 clip flags, four 6-bit judgements: each clip step in the VU1 programs shifts the word left by 6, clears its top byte +0x57 and sets bits 0 to 5 from comparing x, y and z with +w and -w (0x00476506-0x0047650D, 0x00476635-0x004766BC); the programs read its low word (0x00476622, 0x004766C3) |
| `+0x57` | `u8` | vuClipTop | 0x02064AF7: the top byte of the clip word at +0x54, cleared after every 6-bit shift so the flags keep 24 bits (0x0047650D, 0x00476641) |
| `+0x5C` | `u32` | vuRandomOn | 0x02064AFC: the switch of the emulated VU1 random generator: while it is 0, 0x004B97F0 and 0x004B9C50 return 1.0 without stepping the seed 0x01E02828 (0x004B97F0-0x004B9801, 0x004B9C50-0x004B9C68); VU1 programs set it (0x0047C6B4 and 0x004884F3 store 1; 0x00482B24 and 0x004EC23A store a register) and read it (0x0047C8EE, 0x0048347D, 0x004D47C7, 0x004EC8FE) |

### The device-check pane

The pane is the `0xD0`-byte widget at `0x02CA99D0` with procedure `0x0057E8D0` that the save and load screen `0x00582860` builds.

`DeviceCheckPane` (`0xD0` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057E8D0` |
| `+0xC0` | `u32` | flags | bit 1: the device check runs in save mode, bit 0 of `0x0057EA40`'s second argument (`0x0057EAAD`-`0x0057EAC2`); 0 at construction (`0x0057E914`) |
| `+0xC4` | `u8[4]` | pad0C4 | read and written by no function; nothing fixes its width |
| `+0xC8` | `void*` | controller | the first argument of the device check `0x0057EA40`, the save and load screen that runs it (`0x0057EAB4`); 0 at construction (`0x0057E90A`) |

### The application object

The application object and its parts are laid out as follows.

GameApplication  (static, `0x01F7E350`, `0x1140` bytes; base Phyre::PFramework::PApplication):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0000` | `void*` | vtable 0x008C5760 |  |
| `+0x0027` | `u8` | base byte written by slot 14 |  |
| `+0x0048` | `f64` | frame delta, read by the tick |  |
| `+0x0090` | `...` | passed to the render manager's constructor | with `+0x0E8` |
| `+0x00E8` | `...` | passed to the render manager's constructor | with `+0x090` |
| `+0x0D24` | `i32` | viewport width |  |
| `+0x0D28` | `i32` | viewport height |  |
| `+0x1130` | `void*` | slot 2's first argument |  |
| `+0x1138` | `i32` | slot 2's second argument |  |
| `+0x113C` | `u8` | startup latch: 0 until the init job finishes, 1 after |  |
| `+0x113D` | `u8` | run-once guard of the frame tick |  |

Vtables:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x008C5760` | `...` | GameApplication, 31 slots (table above) |  |
| `0x01CB2508` | `...` | Phyre::PFramework::PApplication, 31 slots; RTTI locator at 0x01CB2500 |  |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01F7E340` | `void*` | 0x80-byte object built by the init job |  |
| `0x01F7F4B0` | `f64` | the frame delta published by the pump |  |
| `0x01F7F4B8` | `u8` | second pass flag |  |
| `0x01F7F4C0` | `...` | the small objects of the init burst | with `0x01F7F4C8` and `0x01F7F4D0` and `0x01F7F4D8` and `0x01F7F4E0` |
| `0x01F7F4C8` | `...` | the small objects of the init burst | with `0x01F7F4C0` and `0x01F7F4D0` and `0x01F7F4D8` and `0x01F7F4E0` |
| `0x01F7F4D0` | `...` | the small objects of the init burst | with `0x01F7F4C0` and `0x01F7F4C8` and `0x01F7F4D8` and `0x01F7F4E0` |
| `0x01F7F4D8` | `...` | the small objects of the init burst | with `0x01F7F4C0` and `0x01F7F4C8` and `0x01F7F4D0` and `0x01F7F4E0` |
| `0x01F7F4E0` | `...` | the small objects of the init burst | with `0x01F7F4C0` and `0x01F7F4C8` and `0x01F7F4D0` and `0x01F7F4D8` |
| `0x01F7F598` | `void*` | render manager (0xDD8) |  |
| `0x01F7F5D0` | `void*` | camera pair (0x270) |  |
| `0x01F7F5D8` | `void*` | running byte (3) |  |
| `0x01F7F5E0` | `...` | the object reset on the 0x01FD4A88 path |  |
| `0x01F7F5E8` | `...` | the vector emptied on the 0x01FD4A88 path |  |
| `0x01F810F0` | `void*` | pause flag (1 byte) |  |
| `0x01F810F8` | `void*` | AsyncJobManager (0x158 each) | with `0x01F81100` |
| `0x01F81100` | `void*` | AsyncJobManager (0x158 each) | with `0x01F810F8` |
| `0x01F81160` | `void*` | AsyncLoadManager |  |
| `0x01F81168` | `void*` | map-art context (0x520) |  |
| `0x01F81170` | `void*` | the map-art context's 0xA0 list |  |
| `0x01F81218` | `void*` | movie player (0xBB8; a PCameraPerspective at +0x5A0) |  |
| `0x01F81240` | `void*` | model asset cache (0x238) |  |
| `0x01F81248` | `void*` | recycle queue (0x108) |  |
| `0x01F81258` | `void*` | procedural-texture context (0x1B8) |  |
| `0x01F81260` | `void*` | SaveloadManager (0xA78) |  |
| `0x01F81270` | `void*` | MultipleDebugDisplay (0x4670) |  |
| `0x01F82CE0` | `void*` | screen fade (0x38) |  |
| `0x01F82D30` | `u8` | second-pass latch pair: armed by 0x001E0550, set by 0x001E0560, cleared by 0x001E0590 | with `0x01F82D31` |
| `0x01F82D31` | `u8` | second-pass latch pair: armed by 0x001E0550, set by 0x001E0560, cleared by 0x001E0590 | with `0x01F82D30` |
| `0x01FD4A68` | `u32` | written by the main state machine; gates the callback ring and the pass count |  |
| `0x01FD4A88` | `u8` | the reset-then-pump request |  |
| `0x02064AA0` | `u32` | the pump mode |  |
| `0x02064AD0` | `u8` | game step count |  |

`LoadingPage`, `0x40` bytes at `[0x01F82CD8]` (`0x001D89D0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `LoadingPage` |
| `+0x08` | `f32` | start | time the arming was stamped, 0 while idle |
| `+0x10` | `f64` | clock | seconds shown |
| `+0x18` | `f32` | angle | clock × π |
| `+0x1C` | `u8` | shown | the icon draws |
| `+0x1D` | `u8` | armed | waiting for the delay |
| `+0x20` | `f32` | fadeTimer | seconds into the fade |
| `+0x24` | `u8` | fadingOut | the fade runs out |
| `+0x28` | `i32` | alpha | 0 to 255 |
| `+0x34` | `f32` | fadeTime | 0.264 |
| `+0x38` | `f32` | delay | 5.0 |

### The render manager

The render manager (`0xDD8` bytes at `[0x01F7F598]`, built by `0x00184F20`, its render targets made by the installer `0x00186CD0` through `0x001EE040(width, height, format, samples)`): the fields below are the ones the manager's functions use beyond those named above.

`RenderManager` (`0xDD8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[2]` | pendingRequests | two request bytes the pass list `0x00187950` serves at its end (`0x001885DB`-`0x001885F5`): byte `+0x00` (set to 1 by `0x0017D120`, the application's slot 10, by `0x001825A0` and by the installer `0x00186CD0` at `0x00187191`) runs `0x00188B10`, which clears both (`0x00188B22`); otherwise byte `+0x01` (set by `0x00189520`(manager, n) with the new multisample count at `+0xDC8`, `0x00189520`-`0x00189524`) runs `0x00188DA0`, which clears it (`0x00188DA6`) and re-applies the count to the targets; while `+0x01` is set the pass list publishes `+0xDC8` to `0x01DF0900` (`0x00187A6D`-`0x00187A7A`); 0 from the constructor `0x00184F20` (`0x00184F43`) |
| `+0x002` | `u8` | frameDone | set to 1 by `0x00183260` (`0x00183273`) and by the installer (`0x00187194`), cleared at the end of each pass list (`0x001885FA`); `0x00187540` returns it to the frame pump; 0 from the constructor (`0x00184F48`) |
| `+0x018` | `u32` | settingD50 | the settings object's `+0xD50` ([`0x02EA5368`] through `0x00796E20`), copied by the installer `0x00186CD0` (`0x00186D42`-`0x00186D4D`); every test of it sits behind `0x005C5230`, which returns 0 (`0x005C5230` xor eax, eax), so it decides nothing (`0x00186139`-`0x00186142`, `0x00186420`-`0x00186429`, `0x00186EC8`-`0x00186ED1`, `0x00187FA8`-`0x00187FB5`, `0x0018848C`-`0x00188495`); 0 from the constructor (`0x00184F56`) |
| `+0x01E` | `u8[2]` | span001E | the two bytes between the bank selector `+0x1D` and the first camera block `+0x20` |
| `+0xAE4` | `i32` | viewportX | x of the saved viewport: `0x00188AC0` hands `+0xAE4`, `+0xAE8`, `+0xAEC` and `+0xAF0` to the device's viewport setter `0x0060F6B0` as x, y, width and height when `+0xAE0` is non-zero (`0x00188AC4`-`0x00188AF7`); called from `0x001F29E0` (`0x001F29F8`) |
| `+0xAE8` | `i32` | viewportY | y of the saved viewport (`0x00188ADA`) |
| `+0xAEC` | `i32` | viewportWidth | width of the saved viewport (`0x00188AD3`) |
| `+0xAF0` | `i32` | viewportHeight | height of the saved viewport (`0x00188ACD`) |
| `+0xB00` | `u8[8]` | span0B00 | the eight bytes between the qword `+0xAF8` and the render-target table `+0xB08` |
| `+0xB08` | `void*` | sceneTarget | the scene render target in use, element 0 of the target table `+0xB08`-`+0xB28` that `0x001867B0` and `0x00186910` index with `+0xC30` (`0x001867B6`, `0x0018695D`); the installer sets it to `+0xB28` (`0x00186E0D`-`0x00186E14`), the pass list resets it to `+0xB28` (`0x00187A33`-`0x00187A3A`, `0x00188606`-`0x0018860D`) and `0x00189530` picks `+0xB28` or `+0xB30` by its flag (`0x0018953B`, `0x0018954A`) |
| `+0xB10` | `void*` | targetB10 | element 1 of the target table: a screen-size render target made by `0x001EE040` (`0x00186E1B`-`0x00186E57`) in format `0x02CF7480`, or `0x02CF76E8` when the settings byte `+0xD48` is set; `0x001867C0` returns it |
| `+0xB18` | `void*` | targetB18 | element 2 of the target table: a screen-size render target with the multisample count `0x02CB8084` (`0x00186E5E`-`0x00186E8D`); `0x00188DA0` re-applies the count to it (`0x00188DD9`-`0x00188DED`); `0x001867A0` returns it |
| `+0xB28` | `void*` | targetB28 | element 4 of the target table: the screen-size multisampled scene target (sample count from the settings' `+0xD3C`, format by its `+0xD48`; `0x00186D37`-`0x00186DD6`); `0x001868F0` returns it for a non-zero argument (`0x001868F4`); `0x00188DA0` re-applies the count (`0x00188DC6`) |
| `+0xB30` | `void*` | targetB30 | the screen-size single-sample counterpart of `+0xB28` (`0x00186DDD`-`0x00186E06`); `0x001868F0` returns it for 0 (`0x001868FC`) |
| `+0xB38` | `void*` | targetB38 | a render target the installer makes only when `0x005C5230`() is non-zero and `+0x18` is 0 (`0x00186EC8`-`0x00186F03`); `0x005C5230` returns 0, so the installer skips it; read by `0x00188730` (`0x001888A8`) and `0x001893C0` (`0x001893F4`) |
| `+0xB48` | `void*` | pingTargetA | first of the screen-size targets the getters index with `+0xDD0` (`0x00186FC4`-`0x00186FED`): `0x00186840` and its siblings return [`+0xB48` + 8 * index], or [`+0xB50` + 8 * index] when `+0xDBB` is set and `0x0017F280` agrees (`0x00186862`-`0x0018688A`) |
| `+0xB50` | `void*` | pingTargetB | second of those targets (`0x00186FF4`-`0x0018701D`), element 1 of the `+0xB48` pair and element 0 of the `+0xB50` pair (`0x00186875`, `0x001869EC`) |
| `+0xB58` | `void*` | resolveTarget | the target in use from the pair `+0xB60` (multisampled) and `+0xB68`: `+0xB60` while `+0xDB9` is clear and `+0xDBA` set, else `+0xB68` (`0x00187A41`-`0x00187A66`, `0x00188E16`-`0x00188E38`); the installer starts it at `+0xB60` (`0x00186FB6`-`0x00186FBD`); `0x00186660` returns it |
| `+0xB70` | `u8[8]` | span0B70 | the eight bytes between the target `+0xB68` and the target `+0xB78` |
| `+0xB78` | `void*` | viewportTarget | a render target at the viewport size `+0xAD8` x `+0xADC`, or 3840 x 2160 when the boot byte `+0xDB8` is set or `+0xC30` is 3 (`0x00187024`-`0x00187077`); `0x00186A80` returns it |
| `+0xB88` | `u8` | byte0B88 | the byte after the qword `+0xB80`, before `+0xB89` |
| `+0xB89` | `u8[7]` | span0B89 | the seven bytes between the byte `+0xB88` and the target array `+0xB90` |
| `+0xB90` | `void*[10]` | fixedTargetsA | ten fixed-size render targets the installer makes from the size table `0x008C5D80` (50 x 60, 100 x 60, 150 x 60, 200 x 60, 360 x 60, 960 x 60, 1920 x 108, 1920 x 220, 1920 x 540, 1920 x 1080; `0x00187090`-`0x001870C2`); `0x00186800` returns entry i, the last for i of 10 or more (`0x00186800`-`0x00186810`) |
| `+0xBE0` | `void*[10]` | fixedTargetsB | a second set of ten targets of the same sizes (`0x001870AE`-`0x001870D4`); `0x001867E0` returns entry i, the last for i of 10 or more (`0x001867E0`-`0x001867F0`) |
| `+0xCD5` | `u8[3]` | span0CD5 | the three bytes between the byte `+0xCD4` and the capture state `+0xCD8` |
| `+0xCDC` | `u8[4]` | span0CDC | the four bytes between the capture state `+0xCD8` and the capture colour target `+0xCE0` |
| `+0xCE0` | `void*` | captureColourTarget | the colour target `0x00188730` binds while the capture state `+0xCD8` is 1 (`0x00188748`-`0x00188788`), its width `+0x28` and height `+0x2C` giving the viewport (`0x0018879B`-`0x001887D8`); 0 from the installer (`0x001870FF`) |
| `+0xCE8` | `void*` | captureDepthTarget | the depth target `0x00188730` binds with it (`0x0018876A`-`0x00188796`); 0 from the installer (`0x00187106`) |
| `+0xCF4` | `u8[4]` | span0CF4 | the four bytes between the capture width `+0xCF0` and the capture buffer `+0xCF8` |
| `+0xD00` | `f32` | clearArg0 | first of the four float arguments of the last FastClearObj command, kept by `0x00185CD0` (`0x00185D01`) before it forwards them to `0x0018B710` (`0x00185D71`); called from `0x00182280` (`0x001822E6`); 0 from the installer (`0x0018717C`) |
| `+0xD04` | `f32` | clearArg1 | second FastClearObj argument (`0x00185D0A`) |
| `+0xD08` | `f32` | clearArg2 | third FastClearObj argument (`0x00185D13`); 0 from the installer (`0x00187183`) |
| `+0xD0C` | `f32` | clearArg3 | fourth FastClearObj argument (`0x00185D1B`) |
| `+0xD11` | `u8[3]` | span0D11 | the three bytes between the byte `+0xD10` and the float `+0xD14` (5.0 from the constructor) |
| `+0xD19` | `u8[47]` | span0D19 | the 47 bytes between the byte `+0xD18` and the byte `+0xD48` |
| `+0xD48` | `u8` | byte0D48 | the byte after the 47-byte span `+0xD19`, before `+0xD49` |
| `+0xD49` | `u8[19]` | span0D49 | the 19 bytes between the byte `+0xD48` and the byte `+0xD5C` |
| `+0xD5D` | `u8[67]` | span0D5D | the 67 bytes between the byte `+0xD5C` and the dword `+0xDA0` |
| `+0xDA8` | `u32` | captureStep | set to 6 by the 4K capture driver `0x00187860` when it moves from state 1 to 3 and from 3 to 4 (`0x0018789B`, `0x001878BD`) |
| `+0xDC6` | `u8[2]` | span0DC6 | the two bytes between the byte `+0xDC5` and the pending multisample count `+0xDC8` |
| `+0xDCD` | `u8[3]` | span0DCD | the three bytes between the byte `+0xDCC` and the dword `+0xDD0` |
| `+0xDD4` | `u8[4]` | span0DD4 | the last four bytes of the `0xDD8`-byte manager, after the dword `+0xDD0` |


## Shipped data

| Fact | Value |
|---|---|
| object size | `0x1140` = 4,416 bytes, the immediate of the sized delete in slot 0 |
| archive path | `"../FFXII_TZA.vbf"` after `"../../.."` |
| registration key | `0x9CA5` in the static initialiser |
| vtable | 31 slots; 18 overridden, 10 inherited, 3 stubs |
| base RTTI | `.?AVPApplication@PFramework@Phyre@@` at `0x01F47628` |
| singleton classes | `AsyncJobManager`, `AsyncLoadManager`, `Phyre::PCameraPerspective` (the movie player's camera), `SaveloadManager`, `MultipleDebugDisplay`, from the vtables their constructors install |
| procedural-texture context | loads `./GameData/D3D11/ArtData/map/proceduralTexture/proceduralTexture_D3D11.ah` and `proceduralTextureConfigs.txt` |

## Operations

At start: the framework calls slot 2 (mount), slot 3 (device and the init job); the job builds the
managers and closes the latch. Every frame: the framework calls slot 4 (the pump, the game step,
the frame end), slot 7 (input) and slot 8 (render), each gated on the latch. Slots 21 and 22 store
and read back the unused pause byte; slots 23 and 24 scale the framework's time by `0x0017E440()`.

## State

The latch and the run-once byte; the thirteen singleton pointers and the objects behind them; the
published frame delta and the second-pass flag; the pump mode and the game-step count.

### The cut-name strings

The cutscene bookkeeping of `0x001CC600` keeps two static EASTL strings (`+0x00` begin, `+0x08` end, `+0x10`
capacity end), which start-up initialisers build empty and `atexit` destructors free:

- `0x01F81358`, the current cut name (initialiser `0x0015C560`, destructor `0x008A69F0`): `0x001CC600` reads its end
  (`0x001CC622`) and rebuilds it as `"Cut "` plus the count through `0x001A5760` (`0x001CC715`). `0x001CC800` (`0x001CC843`,
  `0x001CC890`, `0x001CC8C8`), `0x001CC920` (`0x001CC94F`) and the cutscene scene-config reader `0x001C3D50` (`0x001C3E9F`) pass it to the
  scene-map lookup `0x001FF6B0`, which compares names in `0x001FF4F0`.
- `0x01F81338`, the previous cut name (initialiser `0x0015CB10`, destructor `0x008A6BF0`): `0x001CC600` assigns the current
  name to it through `0x001A5760` (`0x001CC630`).

`0x001A5760` (assign) and `0x001A52A0` (grow), which it calls, reach the fields through the string's address.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F81348` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the previous cut name `0x01F81338` | `0x0015CB10` (`0x0015CB2E`, `0x0015CB99`, `0x0015CBBE`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A6BF0` (`0x008A6BFD`) |
| `0x01F81360` | `void*` | 0 (zero-filled tail of `.data`) | `+0x08` end of the current cut name `0x01F81358` | `0x0015C560` (`0x0015C593`, `0x0015C5D9`, `0x0015C607`, `0x0015C624`); `0x001A52A0` (`0x001A538E`, `0x001A53D3`); `0x001A5760` (`0x001A57BC`) | `0x001A52A0` (`0x001A52C0`, `0x001A5318`, `0x001A53A0`, `0x001A53B7`, `0x001A53C5`, `0x001A53D3`); `0x001A5760` (`0x001A5774`, `0x001A5798`, `0x001A57BC`, `0x001A57C2`, `0x001A57CF`); `0x001CC600` (`0x001CC622`); `0x001FF4F0` (`0x001FF530`, `0x001FF59E`, `0x001FF60D`) |
| `0x01F81368` | `void*` | 0 (zero-filled tail of `.data`) | `+0x10` capacity end of the current cut name `0x01F81358` | `0x0015C560` (`0x0015C57E`, `0x0015C5E9`, `0x0015C60E`); `0x001A52A0` (`0x001A537F`) | `0x001A52A0` (`0x001A52BB`, `0x001A534C`, `0x001A535E`); `0x008A69F0` (`0x008A69FD`) |

No other instruction reaches these words: no other RIP-relative, image-base-relative or disp32 reference names them.

### The latch word

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F7F48C` | `u16` | 0 (zero-filled tail of `.data`) | `+0x113C` of the object `0x01F7E350`, the startup latch, with the run-once byte `+0x113D`; the initialiser clears both with one 16-bit store | `0x0015BC40` (`0x0015BC68`, 0); through the object, `0x0017D000` (`0x0017D074`, 1 in `+0x113C`) and `0x0017CCD0` (`0x0017CD31`, 1 in `+0x113D`) | through the object: `+0x113C` by `0x0017CCD0` (`0x0017CCD6`), `0x0017CE50` (`0x0017CE77`) and `0x0017D090` (`0x0017D094`); `+0x113D` by `0x0017CCD0` (`0x0017CD1E`) |

No other instruction has the displacement `0x113C` or `0x113D`.

## Modding notes

- Anything driving the application before the latch is set finds slots 4 and 8 returning at once
  and slot 7 serving only an open dialog.
- The archive path is relative, so relocating the executable away from the archive breaks the
  mount.
- Slot 5 is deliberately empty, not missing; a hook that expects an unimplemented slot there finds
  a thunk to the stub.
- A second pump pass runs only while `0x01F82D30` is set by the pacing predicate; the game step then
  sees a delta of 0 on the second pass.
- The pause byte behind `0x01F810F0` is reached through `0x001997D0` (returns the pointer at `0x01F810F0`) and `0x00199780`
  (returns the byte). Its writers and readers:
  - `0x0017E720(flag)` stores `flag != 0` through `0x001997E0` (`0x0017E728`, `0x0017E73B`). Its only caller is the pause
    overlay `0x00229590`, which passes 0 at `0x002297B0` (after the policy-bit clears `0x002E1CA0` at `0x0022979C` and
    `0x002297A9`) and 1 at `0x002298C1` (after setting `0x01E027FC` = 1 at `0x002298B7`) ([pause screen](../Menus-And-HUD/pause-screen.md)).
  - The vtable slots 21 and 22 (`0x0017CFD0`, `0x0017D170`) read and write it too, each after `0x001997D0`'s null test
    (`0x0017CFD9`).
  - `0x0017E4E0()` returns the byte (`0x0017E4E4`-`0x0017E4F1`). The pre-dispatch step `0x0022A580` copies it to `0x02F974A0`
    (`0x0022A67A`) and, with no second pass armed (`0x01FD4A68` = 0), tests the copy at `0x0022A713`: clear, it runs
    `0x001E05E0()` and, when that is 0, `0x001832F0()`, before `0x00375B80(0)`; set, it goes to `0x00375B80(0)` at once.
  - The field frame `0x0022A770` runs `0x002506D0` only while the byte is set (`0x0022A8CA`,
    [frame update order](frame-update-order.md)).
  - The UI tick `0x00250540` tests it at `0x00250570`-`0x00250577`. While the byte is set (paused) it runs only the short
    block `0x00250579`-`0x002505C4`: the `0x00184950()` add into `0x0208F570` when the pump's flag `0x02064AA0` is clear,
    `0x002481A0`, `0x00248030` and `0x00244970` on `0x0208EA48`, `0x00248190`, `0x002481C0`, `0x00250CA0`, then the tail `0x003676B0(1)`.
  - While it is clear the tick continues at `0x002505C9`: it adds 1 or 2 (by `0x001EDE70()` and `0x00181DD0()`,
    `0x00250546`-`0x00250565`) to `0x0208F570`, zeroes `0x020927DC` (`0x002505D0`), tail-jumps to `0x002508E0` when `0x00229EA0()` is 5
    (`0x002505EA`), and otherwise runs the full tick from `0x002505EF` (`0x003C9FD0(3)`, `0x00254CC0`, `0x002481A0`, the `0x0208EA20`
    loop with `0x00248030`, to `0x002508D0`).
  - Both paths of `0x00250540` call `0x002481A0`, the parity flip of `0x0208ED5C` ([widgets](../Menus-And-HUD/widgets.md)).
  - Two console drawers read it through `0x001997D0` and `0x00199780` directly: `0x001D7A20` draws nothing while it is set
    (`0x001D7A56`-`0x001D7A65` to `0x001D7DA2`), and the second-picture drawer `0x001D72F0` returns without drawing
    (`0x001D7319`-`0x001D7328` to its epilogue `0x001D7678`).
  - The pump `0x0017D6E0` reads the pointer at `0x0017D73B` only to hand it to `0x0016D6A0`, the compiled-out hook, which is a
    bare `ret`.

## Related

- [Startup constants](startup-constants.md): what `0x0022A0B0` fixes at boot.
- [Frame update order](frame-update-order.md): the main state machine `0x0022A580` and the field
  frame.
- [Class hierarchy](class-hierarchy.md): the RTTI the base class name comes from.
