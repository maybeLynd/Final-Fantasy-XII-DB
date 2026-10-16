---
title: "Game application object: the root object, its vtable and the boot order"
kind: "system"
category: "Engine core"
addresses: "0015BC40, 0017CC70, 0017CEB0, 0017CF30, 0017CCD0, 0017CDE0, 0017CDC0, 0017CE50, 0017D090, 0017D0C0, 0017D120, 0017D160, 0017D1A0, 0017D210, 0017CFD0, 0017D170, 0017CDF0, 0017CE20, 0017D1E0, 0017D000, 0017D4C0, 0017D650, 0017D670, 0017D6B0, 0017D6E0, 0022A490, 0022A580, 00189000, 00189120, 0019A0A0, 001A11B0, 001B7EE0, 001C18A0, 001C2F00, 001D8CD0, 001BDA50, 001C0D40, 001BBFC0, 001A98B0, 00199790, 001997D0, 001E0550, 001E0590, 001E05E0, 001E05F0, 0018A620, 0018A7D0, 00186230, 005C5230, 001999D0, 00199F60, 0019DA30, 0019EB00, 001B9370, 00184F20, 01F82CD8, 001D89D0, 001D8AB0, 001D8700, 001D7A20, 001D8770, 001BAA30, 001E03F0, 00186010, 00187550, 00187860, 001876E0"
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

`GameApplication` is the static object at `01F7E350`, `1140`<sub>h</sub> (4,416) bytes. Its static
initialiser `0015BC40` runs the base constructor `00792350`, installs the vtable `008C5760`,
clears the word at `+113C`<sub>h</sub> (the latch and the run-once byte), registers the object with
`007A1190(app, 9CA5h)`, initialises two framework singletons (`01F2CDF8` and `01F2CE20` through
their vtable slot 1 while `01F2CDF0` is clear) and registers the destructor `008A6970` with
`atexit`.

The deleting destructor, slot 0 (`0017CC70`), re-installs the vtable, runs the base
destructor `00793250` and, with flag bit 0 set, frees: through the guarded indirect call with the size `1140`<sub>h</sub> when bit
2 is set, else `00584730(this)`.

The base is `Phyre::PFramework::PApplication`: `00793250` writes its vtable `01CB2508` into
`[this]`, and the RTTI chain names `PApplication` at displacement 0 and `Phyre::PBase` and
`Phyre::PMemoryBase` at 8. The base vtable has the same 31 slots; the ten slots this class does not
override (1, 12, 13, 17, 18, 19, 20, 28, 29, 30) hold the same addresses in both tables, slot 14 is a
thunk to the base's own body, and slots 11, 26 and 27 are shared stubs in both. So the frame tick,
the archive mount and the latch are game code overriding middleware entry points.

### The vtable

| Slot | Address | What it does |
|---|---|---|
| 0 | `0017CC70` | deleting destructor; states the size `1140`<sub>h</sub> |
| 2 | `0017CEB0` | the archive mount (below) |
| 3 | `0017CF30` | window and device set-up; queues the init job |
| 4 | `0017CCD0` | the frame tick (below) |
| 5 | `0017CDE0` | a thunk to the empty stub: an explicitly empty override |
| 6 | `0017CDC0` | shutdown: `0017D670` (`0019A120`, `001A11F0`, `001DC4E0`, `001993B0` on the input manager, `0022A090`, `0017DAC0(1)`) then the base's slot 6 `0079BF70` |
| 7 | `0017CE50` | input: with a dialog open (`00228480`) it hands the input manager `00198790()` to `001967D0` and returns 0 without reading the latch; otherwise, latched, it calls the handler `00194AF0()` when one is set |
| 8 | `0017D090` | render: 0 while unlatched, else `00187950` on the render manager `00189120()` |
| 9 | `0017D0C0` | resize: copies the viewport size `+D24`<sub>h</sub>/`+D28`<sub>h</sub> into the render manager's `+AD8`<sub>h</sub>/`+ADC`<sub>h</sub>, then the base's `007A05D0` |
| 10 | `0017D120` | sets the render manager's byte `+0` to 1 |
| 14 | `0017D160` | the base's `007A0B40`: stores the argument byte at `+27`<sub>h</sub> |
| 15, 25 | `0017D1A0`, `0017D1E0` | forward a byte to the input manager (`001989D0`, `00198E70`) |
| 16 | `0017D210` | `00227D40(byte)` |
| 21, 22 | `0017CFD0`, `0017D170` | read and write the pause byte at `01F810F0` (`00199780`, `001997E0`); nothing in the game tests it |
| 23, 24 | `0017CDF0`, `0017CE20` | the base's `0079D560` and `0079D5B0` times the time scale `0017E440()` |
| 1, 12, 13, 17-20, 28-30 | the base's | inherited unchanged |
| 11, 26, 27 | `005C5230`, `0016D6A0`, `005C5230` | the shared return-zero and return stubs |

### The boot order

Slot 2, `0017CEB0(this, a, b)`, stores `a` at `+1130`<sub>h</sub> and `b` at `+1138`<sub>h</sub>, moves up three
directories (`0059A770("../../..")`), runs `0019B190()`, mounts `../FFXII_TZA.vbf` on the file system `0019B1F0()`
(`0019B070`), runs the early set-up `0017D6B0` (`0017DAC0(0)`, `001DDA70`, `001D6BE0`, `001BE3E0`,
`0019CDE0`, the debug display `001C2F00`, `001DBA40`) and `00182F70` with the viewport size
`+D24`<sub>h</sub>/`+D28`<sub>h</sub>. The archive path is relative to the executable.

Slot 3, `0017CF30`, configures the device (`0018D850` with `00193D50()`, `00182EB0()`, `00182E80()`
and the device byte `+D48`<sub>h</sub> of `00796E20()`), ensures the two `AsyncJobManager` instances
(`0019A0A0`: `01F810F8` and `01F81100`, `158`<sub>h</sub> bytes each, flags 0 and 1), and queues a job node
`{0017D150, this}` on the first (`00199F10`, `0019A000`).

That job runs `0017D000(app)`: the
manager-init burst `0017D4C0`, the `80`<sub>h</sub>-byte object at `01F7E340` (`0018A840`), the render
manager (`00189000(app + E8h, app + 90h, +D24h, +D28h, [01FD4A9C])`, `DD8`<sub>h</sub> bytes at `01F7F598`),
and then the latch: `+113Ch = 1`. Nothing clears it afterwards.

`0017D4C0(b, a)` builds the managers in order: `001DB500`, the pause flag (`00199790`), four small
objects at `01F7F4C0` (`20`<sub>h</sub>), `01F7F4C8` (`C0`<sub>h</sub>), `01F7F4D0` (`10`<sub>h</sub>) and `01F7F4D8` (`A0`<sub>h</sub>), the
`AsyncLoadManager` (`001A11B0`), `00198750`, `0019EF40`, `001B6BC0`, `001B29F0`, the movie player
(`001B7EE0`, then `001B7850`), the `SaveloadManager` (`001C18A0`, `001C1710`, `001C1940`), `001B5F10`,
`001D6990`, `001D8150`, `001D89D0`, `001831A0`, and the startup constants `0022A0B0(b, a)`
([startup constants](startup-constants.md)).

After the constants come `001B1BA0`, `001B1580`, `0022A4B0`, the screen fade
(`001D8CD0`), a `10`<sub>h</sub>-byte object at `01F7F4E0` (`001D5600`), `001AD3E0`, the procedural-texture
context (`001C0D40`), `001D62D0`, `00194AB0`, `00194AA0(00194AF0())` and `001DB1E0`.

### What the burst builds

| Global | Size | Ensure | Constructor | What the constructor lays down |
|---|---|---|---|---|
| `01F810F8`, `01F81100` | `158`<sub>h</sub> | `0019A0A0` | `001999D0(obj, flag)` | `AsyncJobManager`: a job list at `+50`<sub>h</sub>, a pool of 128 sixteen-byte job nodes at `+90`<sub>h</sub>, the flag at `+150`<sub>h</sub>; `00199F60` then starts its worker |
| `01F81150` | `120`<sub>h</sub> | `0019CDE0` (early set-up) | `0019C7C0` | the loaded-asset registry `0019CE20` returns: a lock at `+00`<sub>h</sub>, a map at `+28`<sub>h</sub> and a pool of 6,144 records at `+60`<sub>h</sub> (`0019C630`) |
| `01F81158` | `188`<sub>h</sub> | `0019EF40` | `0019DA30` | `AssetListManager`: a pool of 192 lists of `130`<sub>h</sub> bytes at `+08`<sub>h</sub> (`0019D5B0`) and a pool of 3,072 entries of `118`<sub>h</sub> bytes at `+C8`<sub>h</sub> (`0019D740`) |
| `01F81240` | `238`<sub>h</sub> | `001BBFC0` | `001B9370` | the model asset cache: three maps, a list and a pool of 384 records of `2A8`<sub>h</sub> bytes at `+E8`<sub>h</sub> (`001B8E90`) |
| `01F7F4D8` | `A0`<sub>h</sub> | `0017D4C0` itself | `001B24D0` | 32 words of 10,000 at `+00`<sub>h</sub>, `+80`<sub>h</sub> pointing at `+00`<sub>h</sub> and `+88`<sub>h</sub> at `+40`<sub>h</sub>; `00862BF0` to `00862C40` read its `+90`<sub>h</sub> and `+94`<sub>h</sub> |
| `01F7F598` | `DD8`<sub>h</sub> | `00189000` | `00184F20` | the render manager (below) |

`00199F60` names the worker thread `"AsyncJobManager Thread"`, or `"AsyncJobManager No Read No
Write Thread"` when the flag is non-zero, starts it (`005CD1E0`) and sets `+154`<sub>h</sub> and `+20`<sub>h</sub>. The destructor body `00199C30` (deleting wrapper `00199D50`, which
frees `158`<sub>h</sub> bytes) clears `+154`<sub>h</sub>, waits for the thread to exit (`005CD330`:
`WaitForSingleObject`, `GetExitCodeThread`), and releases the pools and the job list.

The pools share one template (`001997F0` for the job nodes, `0019D5B0`, `0019D740`,
`001B8E90`): a vector of N records, a set at `+20`<sub>h</sub> filled with the address of every record, a
second set at `+58`<sub>h</sub>, and a lock at `+90`<sub>h</sub> created (`005CD0A0`) when the flag byte `+B8`<sub>h</sub> is set.

The loops `0019CE30`, `0019CEF0`, `0019D100`, `0019D1D0` and `0019D420` copy, move and fill the
`130`<sub>h</sub>-byte lists while the vector is sized; `0019CFA0`, `0019D050`, `0019D350` and `0019D510` do
the same for the `118`<sub>h</sub>-byte entries. The template's destructors (`00199A80`, `0019C870`, `0019DAD0`, `001B3AF0`,
`001E74F0`) are described on [object construction and destruction](../Compiler-And-C-Runtime/object-construction-and-destruction.md).

An asset list is 256 bytes copied as a block, a vector of entry pointers at `+100`<sub>h</sub>, a word at
`+120`<sub>h</sub> and a ready byte at `+128`<sub>h</sub>. `0019EB00(manager, list)` holds when the ready byte is set and
every entry has its byte `+2` set. The map-art update `001A9ED0`, the model asset cache `001BC190`,
the procedural-texture context `001C0DD0` and `001BB120` ask it before they use a list.

In the model asset cache, `001B9A10` finds or inserts a node by a 32-bit key in a map (its caller
`001BAA30` uses it 16 times), `001BA910` empties a map of `58`<sub>h</sub>-byte nodes, and `001BBF40`, from
the cache's update `001BC190`, releases the 32 handles at `+A0`<sub>h</sub> (`00183720`) and zeroes `+A0`<sub>h</sub>
and `+1A0`<sub>h</sub>.

`001BAA30(cache, model)` binds a model's palette textures; `001BC190` calls it, and so does
`001BB120` once the model's asset list (`+08`<sub>h</sub>) is ready (`0019EB00`). It reads the names of the
list in two passes:

1. a texture named `tex_<n>_clut_-1` is palette n: its data address goes to `+1A0h + n × 8`, and a
   handle from `00183780(0, 1 << d, 1, 20h)`, d the digit after `idx` in the name, to `+A0h + n × 8`;
2. a texture `tex_<n>_clut_<m>` with any other m fills the entry of key `n << 16 | (m & FFh)` in the
   map at `+10`<sub>h</sub> (`001B9A10`, which inserts a zeroed entry for a new key): a `_n.dds` name goes to
   `+08`<sub>h</sub>, `_spec.dds` to `+10`<sub>h</sub>, `_diffuseCorrection.dds` to `+18`<sub>h</sub>, each only while that field
   is empty, and any other name to `+00`<sub>h</sub> while it is empty, which then also takes palette n's address at `+20`<sub>h</sub> and its
   handle at `+28`<sub>h</sub>.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | base | the colour texture |
| `08`<sub>h</sub> | `void*` | normal | the `_n.dds` texture |
| `10`<sub>h</sub> | `void*` | specular | the `_spec.dds` texture |
| `18`<sub>h</sub> | `void*` | diffuseCorrection | the `_diffuseCorrection.dds` texture |
| `20`<sub>h</sub> | `void*` | palette | palette n's data |
| `28`<sub>h</sub> | `void*` | paletteHandle | palette n's handle |

`00184F20` builds the render manager: two `338`<sub>h</sub>-byte camera blocks at `+20`<sub>h</sub> and `+358`<sub>h</sub> and a
third at `+690`<sub>h</sub> (`00184CE0`), the viewport size at `+AD8`<sub>h</sub> / `+ADC`<sub>h</sub>, the four callback slots
at `+C38`<sub>h</sub>, 5.0 at `+D14`<sub>h</sub>, the boot argument byte `[01FD4A9C]` at `+DB8`<sub>h</sub>, then `00186CD0`. Its
height query `00186820` answers 2,160 while `+DB8`<sub>h</sub> is set or `+C30`<sub>h</sub> is 3, else `+ADC`<sub>h</sub>.

### The frame tick

Slot 4, `0017CCD0`, returns 0 through the stub while the latch is clear. Otherwise it takes the
frame delta, the double at `+48`<sub>h</sub>, ensures the camera-pair object `01F7F5D0` (`0018A620`, `270`<sub>h</sub>
bytes with two `Phyre::PCameraPerspective` members; the first `0018A670` call hands it the delta), reads the running byte at `[0018A7D0()]`
(the three-byte object `01F7F5D8`), and on its first call runs `0017D650` (`001D6C00`, `001BE3E0`)
and sets the run-once byte `+113D`<sub>h</sub>. The two calls to `0018A670` around that read are a thunk to
the byte getter `00229F90` (`01FD49ED`) whose arguments are unused.

With the running byte clear the pump runs in mode 0. With it set and `01FD4A88` set, the object
`01F7F5E0` is reset (`0018B040`: `0018B3F0(obj, 0)`, `+24`<sub>h</sub> = 0, `+2C`<sub>h</sub> = -1), every element of the
vector `01F7F5E8` is destroyed through its vtable slot 0 and the vector emptied (`0018B810`), the
pump runs in mode 0 and `01FD4A88` is cleared; with it set and `01FD4A88` clear the pump runs in
mode 1. A pump result of 0 returns 9; anything else returns 0.

`0017D6E0(dt, mode)` is the pump. It clears `01F7F4B8`, runs the render manager's deferred
callback ring (`00186230`: one of four slots at `+C38`<sub>h</sub>, index `+CB8`<sub>h</sub>) while `01FD4A68` is clear,
and then loops over passes:

1. `0022CB90()`; when the pacing predicate `001E05F0` holds and this is not the second pass,
   `001E0550` arms `01F82D31` and clears `01F82D30`. The predicate, with `01E02801` set, runs
   `001E03F0()` and holds when `00187540` on the render manager returns 0 and `001E04F0()` is at or
   below `01F82D28`; with `01E02801` clear it resets `01DFDDF8` to the largest double and `01F82D28`
   to 0 and fails;
2. the pause byte's getter `001997D0` is called and its result handed to the return stub
   `0016D6A0`, a compiled-out hook; `01F7F4B0 = dt`; `001A1460(01F7F4C0)`; `001DB600()`; the render manager's `00189CE0` and `00189570`;
3. the recycle queue `001BDAC0` (`01F81248`), the `AsyncLoadManager` `001A1310` (`01F81160`), the
   `AsyncJobManager` through its vtable (`0019A170()`), the map-art context `001A9ED0(ctx, dt)`
   (`01F81168`), the procedural-texture context `001C0DD0` (`01F81258`), the model asset cache
   `001BC190` (`01F81240`), `001CC600()`;
4. the movie player `001B8400(player, dt)` (`01F81218`: `+4` is the status
   `getmoviestatus` reads through `00184860`, `001B82F0` starts a movie);
5. the game step `0022A490(dt, mode != 0)`: it stores the mode at `02064AA0`, runs the main state
   machine `0022A580` (states 0 to 6 at `02064AD3`, [frame update order](frame-update-order.md))
   and increments `02064AD0` when `0022A580` returns non-zero; `0022A490` returns nothing of its
   own, so the pump's result is `0022A580`'s register value surviving the increment;
6. `001D8AB0(001D8A60(), dt)`, the `SaveloadManager` `001C1910` (`01F81260`), the screen fade
   `001D9080` (`01F82CE0`), and the `MultipleDebugDisplay` (`01F81270`): `0022FFE0` when its byte
   `+463C`<sub>h</sub> is set, then `001C2F50`;
7. when `01F82D30` is clear the pump returns (`001E0560`, at the end of `0022A580`, sets it when
   `01F82D31` was armed; states 4 and 6 also call `001E0580` before their handlers); otherwise the frame-end reset `001E0590` runs
   (`00185D80` on the render manager, `0018B040(01F7F5E0)`, `0018C8F0(01F7F5E8)`, `001DB620`,
   `001A14D0(01F7F4C0)`, both bytes cleared), `01F7F4B8` is set, `dt` becomes 0 and the next pass
   starts.

`001E03F0` keeps the pacing balance `01F82D28`. With `01FD4A68` clear it adds the real time since
its last call (`005CC930` minus `02CB60E8`, kept in `01DFDDF8`; nothing on the first call) minus n
frame periods, n = `[01F3DA18]` (`00184950`). The period is 1/60 s when `0017FE30()` (`0079CFA0` on
`001DDAB0()`) is a multiple of 10, else 0.0166833 s. The balance is clamped to plus or minus 4 × n
periods, or 300 × n while the movie player is in state 3, playing (`001B7D20`;
[movies](../Graphics/movies.md)).

The procedural-texture context's update `001C0DD0` does its work once: when its asset list `[ctx]`
is ready (`0019EB00`) it indexes it with `001BF2E0` and sets `ctx + 8`. For each asset name (from byte
3 of the entry) `001BF2E0` drops the directory and the extension, and `001C0670` splits the rest at
its last `_`: the part before is the key; a suffix of exactly `color` clears the second output and
any other suffix sets it; a name without `_` is skipped.

A key that `001C01B0` does not find gets a `28`<sub>h</sub>-byte record, the key and its position, appended to
the vector at `ctx + 58h` (`001BEEF0` grows it) and entered in the map at `ctx + 78h`. For a
non-`color` asset the record's `+20`<sub>h</sub> receives an address inside the asset's object whose class
chain reaches `02CBB900`.

`001CC600` keeps the cutscene bookkeeping: it saves the current cut name `01F81358` to `01F81338`,
rebuilds it as `"Cut "` plus the queued count of the marked event slot (`001C3390` joins the two
strings; its sibling `001C3420` joins a C string to a string), and moves `01F81280` to `01F81281`
before setting `01F81280` to `002F1A20() != 0` and `0022A550() != 0`. `001C53B0` and `001C53D0`
report the rising and the falling edge of that byte.

Each pumped object is a lazily built singleton: a global pointer, an ensure function that
allocates a fixed size and constructs on first use, and a getter. The screen fade `01F82CE0` is a
`38`<sub>h</sub>-byte record built disabled (`+0` = 0, `+10`<sub>h</sub> = 3) whose update steps a level `+1C`<sub>h</sub> by
`+20`<sub>h</sub> up (mode 0) or down (mode 1) and clamps at 255 ([screen fade](../17-Presentation-Rendering/screen-fades.md
)).
Its update draws first: inside a `"ScreenImage"` scope `001D8BB0` emits a quad over the screen
(corners from `001D8B20`) with colour 255, 255, 255 and the level `+1C`<sub>h</sub> as alpha.

### The screen captures

The render pass list `00187950` services two captures through the render manager:

1. `00186010`, when `+CD8`<sub>h</sub> is 1, runs `00188730`, sets `+CD8`<sub>h</sub> to 2, allocates width (`+CF0`<sub>h</sub>) ×
   height × 3 bytes at `+CF8`<sub>h</sub> (the height is `00186820`'s answer) and reads the frame into it
   (`00600070`, the device's slot 2, `00610330`);
2. `00187550`, when `+CD8`<sub>h</sub> is 2, clears it, writes `/capture.tga` (an 18-byte header for an
   uncompressed 24-bit image, then the rows from the last to the first), frees the buffer and
   clears `+CD4`<sub>h</sub>.

Only the constructor (0), `00186010` (2) and `00187550` (0) store to `+CD8`<sub>h</sub>; `00186010` and `00188730`
(`0018874A`) read it.

With the boot byte `+DB8`<sub>h</sub> set, `00187860` also runs a 3840 × 2160 capture, keyed by the state
`+DAC`<sub>h</sub>:

| State | Next | Action |
|---|---|---|
| 1 | 3 | sets `+DA8`<sub>h</sub> to 6 |
| 3 | 4 | grabs the frame (`00185FB0`) and sets `+DA8`<sub>h</sub> to 6 |
| 4 | 0 | writes the grab with `001876E0` |
| 6 | 7 | none |
| 7 | 7 | grabs on the first call (`01F7F5AC` = 1), then on each call writes the last grab and grabs again |

`001876E0` writes `/Capture 4K/capture%03d.tga` (counter `01F7F5A4`), or in state 7
`/Capture 4K/capture_series%03d_%04d.tga` (series `01F7F5A8`, frame `01F7F5AC`): an 18-byte header
and 2,160 rows of `2D00`<sub>h</sub> bytes from `+DB0`<sub>h</sub>, last row first.

### The loading page

The object the pump steps in pass step 6 through `001D8AB0(001D8A60(), dt)` is the `LoadingPage`
at `01F82CD8`, `40`<sub>h</sub> bytes built by `001D89D0` in the init burst with a fade time of 0.264 s at
`+34`<sub>h</sub> and a delay of 5.0 s at `+38`<sub>h</sub>. It is the icon that turns while a load runs:

1. `001831A0` arms it (`001D8A90`: when the start time `+08`<sub>h</sub> is 0, the armed byte `+1D`<sub>h</sub> = 1).
   The save-load post-load sequence and the zone change call `001831A0`.
2. Each update `001D8700` stamps the start time on the first armed pass (`005CC930` minus
   `02CB60E8`); once 5 s have passed it sets the shown byte `+1C`<sub>h</sub>, clears the armed byte and
   restarts the fade timer `+20`<sub>h</sub>.
3. While shown, `001D8690` sets the alpha `+28`<sub>h</sub>: timer / fade time × 255, capped at 255, on the
   way in; 255 minus that on the way out (`+24`<sub>h</sub> set), clearing the shown byte once the timer
   passes the fade time. The update then adds `dt` to the timer and to the clock `+10`<sub>h</sub>, and
   draws with the angle clock × π through `001D7A20`.
4. `001D7A20` draws nothing while the pause flag reads set (`00199780`). Otherwise it sets the
   sprite state (`001D8600`), places the four corners of the layout rectangle of `[01F82CD0]`
   centred for a 1920 × 1080 or 512 × 448 frame, writes the alpha into each, rotates them by the
   angle (`001D8790`) while the running byte `[0018A7D0()]` is 0, and emits them (`001B06D0`, `001B03D0`).
5. `00183070` dismisses it (`001D8770`): it zeroes the start time, clears the armed byte and,
   unless a fade-out already runs, starts one.

A load shorter than 5 s therefore never shows the icon.

## Layouts

```
GameApplication  (static, 01F7E350, 0x1140 bytes; base Phyre::PFramework::PApplication)
+0x000  ptr     vtable 008C5760
+0x027  u8      base byte written by slot 14
+0x048  f64     frame delta, read by the tick
+0x090, +0x0E8  passed to the render manager's constructor
+0xD24  i32     viewport width       +0xD28  i32  viewport height
+0x1130 ptr     slot 2's first argument   +0x1138 i32  slot 2's second argument
+0x113C u8      startup latch: 0 until the init job finishes, 1 after
+0x113D u8      run-once guard of the frame tick

vtables
008C5760  GameApplication, 31 slots (table above)
01CB2508  Phyre::PFramework::PApplication, 31 slots; RTTI locator at 01CB2500

globals
01F7E340  ptr   0x80-byte object built by the init job
01F7F4B0  f64   the frame delta published by the pump   01F7F4B8 u8 second pass flag
01F7F4C0 / 01F7F4C8 / 01F7F4D0 / 01F7F4D8 / 01F7F4E0  the small objects of the init burst
01F7F598  ptr   render manager (0xDD8)       01F7F5D0 ptr camera pair (0x270)   01F7F5D8 ptr running byte (3)
01F7F5E0 / 01F7F5E8  the object reset and the vector emptied on the 01FD4A88 path
01F810F0  ptr   pause flag (1 byte)          01F810F8 / 01F81100  AsyncJobManager (0x158 each)
01F81160  ptr   AsyncLoadManager             01F81168 ptr map-art context (0x520; 01F81170 its 0xA0 list)
01F81218  ptr   movie player (0xBB8; a PCameraPerspective at +0x5A0)        01F81240 ptr model asset cache (0x238)
01F81248  ptr   recycle queue (0x108)        01F81258 ptr procedural-texture context (0x1B8)
01F81260  ptr   SaveloadManager (0xA78)      01F81270 ptr MultipleDebugDisplay (0x4670)
01F82CE0  ptr   screen fade (0x38)           01F82D30 / 01F82D31  u8 second-pass latch pair: armed by 001E0550, set by 001E0560, cleared by 001E0590
01FD4A68  u32   written by the main state machine; gates the callback ring and the pass count
01FD4A88  u8    the reset-then-pump request   02064AA0 u32 the pump mode   02064AD0 u8 game step count
```

`LoadingPage`, `40`<sub>h</sub> bytes at `[01F82CD8]` (`001D89D0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | vtable | `LoadingPage` |
| `08`<sub>h</sub> | `f32` | start | time the arming was stamped, 0 while idle |
| `10`<sub>h</sub> | `f64` | clock | seconds shown |
| `18`<sub>h</sub> | `f32` | angle | clock × π |
| `1C`<sub>h</sub> | `u8` | shown | the icon draws |
| `1D`<sub>h</sub> | `u8` | armed | waiting for the delay |
| `20`<sub>h</sub> | `f32` | fadeTimer | seconds into the fade |
| `24`<sub>h</sub> | `u8` | fadingOut | the fade runs out |
| `28`<sub>h</sub> | `i32` | alpha | 0 to 255 |
| `34`<sub>h</sub> | `f32` | fadeTime | 0.264 |
| `38`<sub>h</sub> | `f32` | delay | 5.0 |


## Shipped data

| Fact | Value |
|---|---|
| object size | `1140`<sub>h</sub> = 4,416 bytes, the immediate of the sized delete in slot 0 |
| archive path | `"../FFXII_TZA.vbf"` after `"../../.."` |
| registration key | `9CA5`<sub>h</sub> in the static initialiser |
| vtable | 31 slots; 18 overridden, 10 inherited, 3 stubs |
| base RTTI | `.?AVPApplication@PFramework@Phyre@@` at `01F47628` |
| singleton classes | `AsyncJobManager`, `AsyncLoadManager`, `Phyre::PCameraPerspective` (the movie player's camera), `SaveloadManager`, `MultipleDebugDisplay`, from the vtables their constructors install |
| procedural-texture context | loads `./GameData/D3D11/ArtData/map/proceduralTexture/proceduralTexture_D3D11.ah` and `proceduralTextureConfigs.txt` |

## Operations

At start: the framework calls slot 2 (mount), slot 3 (device and the init job); the job builds the
managers and closes the latch. Every frame: the framework calls slot 4 (the pump, the game step,
the frame end), slot 7 (input) and slot 8 (render), each gated on the latch. Slots 21 and 22 store
and read back the unused pause byte; slots 23 and 24 scale the framework's time by `0017E440()`.

## State

The latch and the run-once byte; the thirteen singleton pointers and the objects behind them; the
published frame delta and the second-pass flag; the pump mode and the game-step count.

## Modding notes

- Anything driving the application before the latch is set finds slots 4 and 8 returning at once
  and slot 7 serving only an open dialog.
- The archive path is relative, so relocating the executable away from the archive breaks the
  mount.
- Slot 5 is deliberately empty, not missing; a hook that expects an unimplemented slot there finds
  a thunk to the stub.
- A second pump pass runs only while `01F82D30` is set by the pacing predicate; the game step then
  sees a delta of 0 on the second pass.
- The pause byte behind `01F810F0` has no consumer: its getter's only callers are the two slots and
  the pump's compiled-out hook, so a pause has to be done elsewhere.

## Related

- [Startup constants](startup-constants.md): what `0022A0B0` fixes at boot.
- [Frame update order](frame-update-order.md): the main state machine `0022A580` and the field
  frame.
- [Class hierarchy](class-hierarchy.md): the RTTI the base class name comes from.
