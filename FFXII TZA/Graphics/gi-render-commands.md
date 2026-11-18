[Home](../../README.md) / [Graphics](README.md) / Gi render commands

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Gi render commands: the Gi* command family, the command arena, render blocks and the D3D11 primitive renderer | system | Graphics | Render pipeline | The eighteen Gi* render command classes that carry the PS2-era drawing vocabulary (scene brackets, sprites, rectangles, screen images, primitives, state toggles, VU1 packets) into the PC renderer: the ring arena they are allocated from, the prepare and filing steps, the draw list that sorts per-draw records, the GeometryInstanceOrderedObject wrapper that puts them on the ordered command list, the 0x80-byte render blocks executed on PhyreEngine's render thread, and the PrimitiveRendererD3D11 device whose vtable they call. | 0x01F7F4C0, 0x001A1470, 0x001A1460, 0x001A14D0, 0x001FB840, 0x0020E630, 0x01F7F4D0, 0x001F48B0, 0x001F49F0, 0x005FEA50, 0x001F4A10, 0x02CC0410, 0x005FD050, 0x00624660, 0x00D86960, 0x006C8750, 0x00607D20, 0x006106A0, 0x0060A410, 0x00607410, 0x02F8F2F8, 0x003A3740, 0x003A3A00, 0x00210570, 0x01F83580 |

## What the player sees

The scene brackets, sprites, coloured rectangles, screen images, generic primitives and the
PS2-style effect packets are drawn by a family of small command objects named after the PS2
drawing vocabulary (`GiPolyGT4T`: Gouraud, textured, four vertices). The game thread creates them
each frame; PhyreEngine's render thread later runs each one against the D3D11 primitive renderer.

## How it works

### The classes

RTTI names eighteen `Gi*` classes. Sixteen have two virtual slots, slot 0 prepare and slot 1
execute(command, device), and no destructor; the two reset commands are three-slot
`OrderedObject`s ([render command list](render-command-list.md)).

| Class | Vtable | Factory | Arena size | Slot 0 | Slot 1 |
|---|---|---|---:|---|---|
| `GiBeginScene` | `0x00904488` | `0x001FBD80` | 8 | `0x0016D6A0` | `0x001FBD70`: device `+0x130` |
| `GiEndScene` | `0x009044A0` | `0x001FBE50` | 8 | `0x0016D6A0` | `0x001FBE40`: device `+0x128` |
| `GiTrans` | `0x01CCFA00` | `0x00862E50` | 8 | `0x0016D6A0` | `0x00862D40` |
| `GiTransNz` | `0x01CCFA18` | `0x00862FD0` | 8 | `0x0016D6A0` | `0x00862EC0` |
| `GiSetTexture` | `0x01CCFA30` | `0x00863060` | 0x18 | `0x0016D6A0` | `0x00863040`: `0x00210570` |
| `GiColorRect` | `0x01CCFAB0` | `0x00863B40` | 0x70 | `0x0016D6A0` | `0x00863850` |
| `GiPrim` | `0x01CCFAF0` | `0x008642A0` | 0x68 | `0x008641B0` | `0x00863D80` |
| `GiSprite` | `0x01CCFB08` | `0x008647C0` | 0xE0 | `0x00864750` | `0x00864330` |
| `GiPolyGT4T` | `0x01CCFB20` | `0x00864D10` | 0x100 | `0x00864CA0` | `0x00864860` |
| `GiZNormalOnOff` | `0x01CCFB38` | `0x00864E00` | 0x10 | `0x0016D6A0` | `0x00864D70` |
| `GiBeginEff` | `0x01CCFB78` | `0x00865130` | 0x90 | `0x00864F30` | `0x00864E90` |
| `GiNormal` | `0x01CCFB90` | `0x008652B0` | 8 | `0x0016D6A0` | `0x008651A0` |
| `GiEndEff` | `0x01CCFBA8` | `0x00865320` | 8 | `0x0016D6A0` | `0x0016D6A0` |
| `GiSetRtForRtSampling` | `0x00902F28` | `0x001F16C0` | 0x18 | `0x0016D6A0` | `0x001F16A0`: device `+0x38` |
| `GiScreenImage` | `0x009068B8` | `0x0020E9F0` | 0xC0 | `0x0016D6A0` | `0x0020E6C0` |
| `GiVmax` | `0x009007E8` | `0x001DB220` | 0x640 | `0x001DB550` | `0x001DB3D0` |
| `GiResetRenderTargetObj` | `0x009033D0` | `0x001F1AF0` | heap 0x20 | destructor | `0x001F3260` |
| `GiResetDefaultRenderTargetObj` | `0x009033F0` | `0x001F1AC0` | heap 0x20 | destructor | `0x001F3210` |

`0x0016D6A0` is a bare `ret`, so prepare does nothing for eleven classes and `GiEndEff` does nothing
at all. Most factories also store the new command in a per-class global (`0x02EAF900`, `0x02EAF910`,
`0x02EAF920`, `0x02EB37F8`, `0x02EB3828`, `0x02EB3838`, `0x02EB3848`, `0x02EB3858`, `0x01F82EB8`, `0x01F83078`,
`0x01F83088`). `GiVmax`, the command that runs VIF1 packets at emit time, is on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md), and `GiBeginEff`'s
camera snapshot on [Phyre frame](../PhyreEngine/the-frame.md).

### The command arena

The installer `0x0017D4C0` creates the arena object at `0x01F7F4C0` (`0x0017D501`): `0x001A14E0` gives it
a 32 MB block (`0x2000000`, through `0x001A1420`), with base `+0x00`, cursor `+0x08`, end `+0x10` and
a mark `+0x18`.

`0x001A1470(arena, size)` rounds the request to `r = (size & ~0xF) + 0x10` (`0x001A147E`-`0x001A1489`); it returns
the cursor and advances it while the request fits below the end, `[arena + 0x08] + r < [arena + 0x10]`
(`0x001A149F`), and otherwise restarts at the base and returns the base, leaving the cursor at the base plus the
rounded size, `[arena + 0x08] = [arena] + r` (`0x001A14A5`–`0x001A14BD`).
It never answers 0. Commands are never freed one by one.

`0x0019C5A0(size)` and `0x0020E680()`, which asks for 16 bytes, are bare `0x001A1470` calls on
`[0x01F7F4C0]` for the command factories.

Each pass of the pump `0x0017D6E0` records the cursor as the mark (`0x001A1460` at `0x0017D757`), and
the frame-end reset `0x001E0590` rewinds the cursor to the mark (`0x001A14D0` at `0x001E05C7`); the same
two routines run on the `GiVmax` allocator `[0x01F82D00]` through `0x001DB600` and `0x001DB620`.

### Prepare and filing

An emitter stores the new command at `node + 8` and calls `0x001FB840(node)`, which copies it to
`node + 0` and tail-jumps the command's slot 0. `GiBeginScene`'s factory `0x001FBD80(mode)` shows
the whole path for a command filed at once:

1. allocate 8 bytes, store the vtable, store the command at `0x01F83078` = `0x01F83070 + 8`;
2. `0x001FB840(0x01F83070)`;
3. `0x0020E630(0x01F83070, mode)`;
4. for a mode other than 3, enqueue a `GiResetRenderTargetObj` (`0x0018BF00` at `0x001FBE02`).

Before step 1 it opens a render-list scene when no scene is open (`0x00182560` returns `0x01F7F538`, 0) and the
mode is not 3: it files `BegineScene0Obj` (`0x00182250`) and sets `0x01F83064` to 1, recording that it opened the
scene (`0x001FBD9B`). At the end it keeps the mode at `0x01F83068` and sets `0x01F83060` to 1 (`0x001FBE07`,
`0x001FBE0D`); `0x001FBE20` and `0x001FBE30` return them.

`GiEndScene`'s factory `0x001FBE50` clears `0x01F83060` (`0x001FBEC6`). When `0x01F83064` is set and the mode is not
3, it clears that too and closes the scene with `EndSceneObj` (`0x001FBED7`, tail jump to `0x001823B0`;
[render command list](render-command-list.md)).

`0x0020E630(node, mode)` turns the mode into a class key, 0 → 8, 1 → `0x20`, 2 → `0x40`, 3 → `0x20`
and anything else → 0, and hands `node[0]` and the key through `0x001FB810` to `0x001A17F0` on the
handler object `[0x01F7F4D0]`. That object is created by the installer (`0x0017D547`) with
`0x001A17D0`, which stores the vtable `0x008F5F28` and points its handler field `+0x08` at itself, so
the call reaches slot 0 of `0x008F5F28`: `0x001F48B0`.

`0x001F48B0(handler, command, key)` takes 0x28 bytes from the command arena, builds a
`GeometryInstanceOrderedObject` (`0x001F4950`: vtable `0x00903920`, command at `+0x18`, key at
`+0x20`) and appends it to the ordered command list (`0x001F4940`). The render body's walk later
calls its slot 1, `0x001F49F0`.

`0x001FB830(node)` is the path for a command that must run at once: `0x001A1850([0x01F7F4D0],
node[0])` takes 0x28 bytes from the arena, wraps the command in a `GeometryInstanceOrderedObject`
(`0x001F4950`, key 0) and calls its slot 1 straight away with the render manager's device `+0x08`.

Without a render manager (`0x00189120` returns 0) it files the command through the handler with key
`0x40` instead. `0x001F16C0(a, b)`, called by the render-manager installer `0x00186CD0`, by `0x00188B10`
and by `0x00188DA0`, builds a `GiSetRtForRtSampling` command of 0x18 bytes (`a` at `+0x08`, `b` at
`+0x10`) and runs it this way.

### The draw list

Per-draw producers file records instead, in the [draw list](effect-drawing.md#the-draw-list). The list is created by `0x003A3670`: `0x190000` bytes
(40,960 records of 0x28) at `0x02F8F2F8`, a `0xC8028`-byte sort area at `0x02F8F300`, and a packet
arena whose base is `0x02F8F308` (`0x003A36BD`); the count is the `u16` at `0x02F8F2C6`.

`0x0024D540`, called by the draw `0x0022B0B0` at `0x0022B191`, runs the drain `0x003A3740` and then the
rewind `0x003A3A00`; the VFX layer passes `0x00259030` and `0x002590F0` call the drain alone. The drain sorts the records
with the merge sort `0x003A3A50` on the `u32` at `+0x08` (`0x003A3B53`, `0x003A3C83`) and walks them:

1. when `0x00180040()` is 1, the record's flag bit `0x2` is set, `0x0022BE90()` is 1 and `0x0022BEA0()` is 0,
   it inserts the post-processing block once (`0x003A3823`–`0x003A38AA`);
2. flag bit `0x1` calls `0x003A2BD0` first;
3. a non-null function at `+0x10` is called with `+0x00` (`0x003A38C6`);
4. otherwise, when `+0x00` is null: flag bit `0x4` clear files the node `+0x18` with `0x0020E630(node, 2)`
   (`0x003A38DE`); flag bit `0x4` set appends the node to the array `0x02AEF420` (count `0x02AEF414`).

An empty list skips all of this (`0x003A374E`). Before the walk the drain copies bit `0x1` of `0x02F8F310` into bit
`0x4` and opens with `0x00862FD0` and `0x00863010(2)` while bit `0x1` is set, else `0x00862E50` and `0x00862E90(2)`
(`0x003A3765`-`0x003A37A4`). After it, it stores 0 as the count, the drained count at `0x02F8F2CC` and its peak at
`0x02F8F2CE`, the packet bytes used at `0x02F8F2E8` and their peak at `0x02F8F2F0` (`0x003A3929`-`0x003A3973`). Every exit
clears bit `0x1` of `0x02F8F310` (`0x003A397F`).

The post-processing insert files `0x00865320` and `0x00865360(2)`, closes the bracket, runs `0x00182970([0x01FD4A6C])`
inside the marker `post-processing render`, and reopens the bracket with the saved pass id and the layer with bit
`0x10` set. It then opens with the same pair again, files `0x00865130` and `0x00865170(2)` and sets `0x02064AE0` through
`0x0022BFA0(1)`; `0x0022BEA0` returns that word, so later entries skip the insert (`0x003A3823`-`0x003A38AA`).

`0x003A3A00` sets the count to 0, rewinds the packet arena `0x02F8F2D0` to `0x02F8F308` and clears bit `0x1`
of `0x02F8F310`. It also sets the arena end `0x02F8F2D8` to the base plus `[0x02F8F2C0]` / 16 × 16 (the division
signed, toward zero) and zeroes the byte `0x02F8F2C5` (`0x003A3A07`-`0x003A3A42`).

### From the ordered list to the render thread

`GeometryInstanceOrderedObject`'s slot 1 `0x001F49F0(object, device)` calls
`0x005FEA50(device, 0x001F4A10, command)`. `0x005FEA50` reserves a 0x80-byte block in the device's ring
(`+0x50` base, `+0x58` end, `+0x60` cursor, restarting at the base when full), records the pending
range at `+0x88`/`+0x90` (the block at `+0x88` only while `+0x88` is 0, the block's end at `+0x90`),
and writes opcode `0x2F` at `+0x00`, the function at `+0x08` and the
command at `+0x10` (`0x005FEAEE`–`0x005FEAF8`), and returns 0.

A null function returns 1 at once (`0x005FEA6D`). Before reserving, `0x005FEA50` asks `0x00600B30(device, 0, 1)`
whether one more block fits in the ring without running past its limit `+0x68`; when it does not, it first
calls the device's slot 2 (`+0x10`, `0x005FEA95`), which is `0x00600D20`, the posting routine below, in the
tables `0x00D498F0` and `0x00D49930`. When even a block at the base would pass the end, it leaves the cursor at
the base, writes nothing and returns `0xD` (`0x005FEB11`).

Three of the callbacks below are posted the same way, through `0x005FEA50`. Each is called with the three-qword
frame the decoder `0x0060A410` builds (below), not the block; the frame's `+0x10` holds a copy of the value
posted, loaded from the block's `+0x10` (`0x0060A8CA`). `0x00185A90` instead adds `0x0017ECC0` and its pointer to
one of four vectors at `+0xC38`, and `0x00186230` calls it with the pointer itself (`0x00186277`):

| Callback | Posted by | Does |
|---|---|---|
| `0x0017ECB0` | `0x00184960` | stores the posted dword at `0x01DF08F8` |
| `0x0017ECC0` | `0x00183720` | calls `0x005DE250` and frees the pointer it is called with |
| `0x00189090` | `0x00186130` | clears byte `+0x09` of the posted object |
| `0x00189110` | `0x00186410`, `0x00187950` | copies the posted object's byte `+0x08` into byte `+0x09` of the object it points at |

`0x00607D20` builds a 256-slot block queue with semaphores and per-slot events and starts the thread
`0x005FE1F0` (`CreateThread` through `0x005CD1E0`, 64 KB stack); its name string is
`PhyreEngineRenderThread`. `0x005FE1F0` jumps to `0x006106A0`, which waits on each slot's event in
turn (`0x00610724`), runs `0x0060A410(queue, start, end)` on the slot's range (`0x00610753`) and releases
the completion semaphore (`0x00610774`).

`0x00607D20(queue)` returns 0 at once when the state `+0x28` is already 1 (`0x00607D36`). Otherwise it zeroes
`+0x298C`, creates the semaphore `+0x2840` with 256 of 256 counts and `+0x2850` with 1 of 1
(`CreateSemaphoreA` through `0x005CD160`), and the 256 slot events as manual-reset events that start
unsignalled (`CreateEventA` through `0x005CD0E0`, `0x00607D90`-`0x00607DA6`).

It sets the byte after each handle
to 1 (`+0x2848`, `+0x2858`, each event's `+0x08`, the thread's `+0x18`). A non-zero answer from any of these
calls is returned as it is; when the thread starts, the state becomes 1 and the call returns 0 (`0x00607DFC`).

The thread `0x006106A0(queue)` first stores `GetCurrentThreadId()` at `+0x298C` (`0x005CC920`, `0x006106CC`)
and calls `0x005C5230(queue + 0x20, "RenderThread", 0x2000)` and `0x005C5230(0x01F2ED08, queue + 0x20)`;
`0x005C5230` is `xor eax, eax; ret`, so the two calls change nothing. Each
pass takes the slot that the index `+0x2830` names, `queue + 0x30 + 0x28 × i` for `i = [queue + 0x2830]`
(`0x00610700`-`0x00610716`), and moves the index on modulo 256, `i + 1 == 0x100 ? 0 : i + 1` (`0x0061070A`-`0x0061071E`),
waits on the slot's event (`WaitForSingleObject` through `0x005CD840`) and reads the state `+0x28`:

- state 1: resets the event (`ResetEvent` through `0x005CD500`), runs `0x0060A410`, clears the slot's start,
  end and `+0x20`, and releases the semaphore that `+0x20` pointed at when it was set
  (`0x0061073F`-`0x00610774`);
- state 0: resets the event and logs `Render thread running without initialize() being called.`
  (`0x005CDAA0`, `0x00610790`);
- state 2: ends the loop after this pass (`0x0061073A`); any other state does neither.

Every pass then releases one count of `+0x2840` (`0x006107A3`), the handle `0x00600D20` waits on. After
the loop it makes the second call again and returns 0 (`0x006107BC`).

The queue is the static `0x02CE4720`, which `0x005FD0E0` returns, building it on first use (a guarded
static) with `0x005DC200`: a `PProcessorProfileTimelineCpu` at `+0x20`, the state `+0x28`, 256 slots
of 0x28 bytes from `+0x30`, two handles at `+0x2840` and `+0x2850`, and four 0x10-byte records from
`+0x2860`. It registers `0x008ADDE0` with `atexit`.

`PRenderer`'s slot 2, `0x00600D20`, posts a range to the queue. It waits on the handle at `+0x2840` (`0x005CD840`),
fills the slot that the index `0x02CE6F54` (`+0x2834`) names with the start and end of the pending blocks (renderer
`+0x88`, `+0x90`) at slot `+0x00` and `+0x08` and the renderer's `+0x78` at `+0x20` (`0x00600DC5`-`0x00600DD9`),
moves the index on modulo 256, `[0x02CE6F54] = i + 1 == 0x100 ? 0 : i + 1` (`0x00600DDE`-`0x00600DEB`), and signals the
slot's event at `+0x10` (`0x005CD5E0`).

At exit `0x008ADDE0` stops the thread through
`0x00610420`, which, while the state is 1, sets it to 2, calls `0x00609720(queue, 0, 0, 0)`, waits for
the thread (`0x005CD330`) and closes the 256 slot events and the two handles (`0x005CD700`,
`CloseHandle`). It then closes the handles of the four records, clears `0x02CE6FC0` and runs the
members' destructors.

`0x0060A410` fetches the render context once (`0x0060A46A`: `0x00624670` → `0x005FD050`, which returns the
static `0x02CC0410`, constructing it with `0x00615840` on first use, a guarded static, and registering
`0x008ADDD0`, which runs `0x00616560` on `0x02CC0410`, with `atexit`, `0x005FD0AD`) and walks the range 0x80 bytes at
a time.

For opcode `0x2F` `0x0060A410` builds a three-qword frame on its stack: the context, the address of a local and
the qword at the block's `+0x10`, the posted value itself (`0x0060A8CA`), and calls `block+0x08` with it
(`0x0060A8BD`–`0x0060A8D6`). `0x001F4A10` takes the device as
`context + 0x18C0` (`0x00624660`) and tail-jumps the command's slot 1 with it (`0x001F4A35`).

Before the walk `0x0060A410` also lays a 0x50-byte record on its stack with `0x00615D50(record,
context)`: the context at `+0x00`, the rest zero.

### The device

`0x00615840` builds the device inside the context: `0x006C8750(context + 0x18C0)` (`0x00615B57`) stores
the `PrimitiveRendererD3D11` vtable `0x00D86960` at `+0x00` and its second vtable `0x00D86AD0` at
`+0x08`. The first table has 45 slots (`0x006CA760` to `0x006CB540`, followed by the locator
`0x01D38180` at `0x00D86AC8`); the second has one slot, `0x006C88A0`.

`0x006C8750` also zeroes 23 fields from `+0x90` to `+0x200` (`0x006C8775`-`0x006C8803`, `0x006C8852`, `0x006C8859`),
sets the four state descriptions at `+0x208`, `+0x398`, `+0x528` and `+0x6B8` to their start values with
`0x00615ED0` (changed mask `+0x00` 0, fill mode `+0x04` 3), and builds the record at `+0x880` with
`0x006DA450(record, device + 0x08)`, which stores that pointer at `+0x880` and zeroes the dword `+0x888` and
the word `+0x8890`. It returns the device (`0x006C884F`).

Slots `+0xB8` and `+0xE8` (`0x006CAC90`, `0x006CAFB0`) step to the state description at `+0x208` and edit
it. Its dword `+0x00` marks what changed, with the bit meanings of the `0x0061DE20` mask below (`0x1`
rasterizer, `0x4` depth-stencil); a `D3D11_RASTERIZER_DESC` follows at `+0x04` and a
`D3D11_DEPTH_STENCIL_DESC` at `+0x2C`:

- slot `+0xB8`, `0x00629560(desc, wire)`, sets the fill mode: 2 (wireframe) when `wire` is 1, else 3
  (solid), and sets bit `0x1`;
- slot `+0xE8`, `0x0062A9E0`, sets the stencil half: the enable at `+0x38`, the read and write masks at
  `+0x3C` and `+0x3D`, the front face's three operations and its comparison at `+0x40` to `+0x4C` and the
  back face's at `+0x50` to `+0x5C`, and sets bit `0x4`. `0x0061C010` turns each comparison and `0x0061C150`
  each operation from a code 0 to 7 into the D3D11 value.

### The context's draw blocks

After it has the D3D11 device and swap chain, the context initialiser `0x00625830` builds three
blocks of shaders and buffers from shader bytecode embedded in the executable; each blob follows a
length dword, and the size passed to the device is that length minus 2. The device calls go through the `ID3D11Device` vtable at context
`+0x108`: `+0x18` CreateBuffer, `+0x58` CreateInputLayout, `+0x60` CreateVertexShader, `+0x68`
CreateGeometryShader, `+0x78` CreatePixelShader and `+0xB8` CreateSamplerState.

| Block offset | Builder | Contents |
|---|---|---|
| `+0x07D8` | `0x00624980` (`0x00625D37`) | a vertex buffer, one vertex shader (`0x01F2EEC0`), three pixel shaders, a POSITION/TEXCOORD/TEXCOORD input layout and the `0x50`-byte `DebugDrawConstantBuffer` |
| `+0x0B50` | `0x00624C30` (`0x00625D4E`) | one vertex shader (`0x01F2FEB4`), eight pixel shaders, the `DrawClearConstantBuffer`, and eight state blocks |
| `+0x18C0` | `0x006C9CD0` (`0x00625D65`) | the `PrimitiveRendererD3D11` resources: a `0x7FE0`-byte and a `0x8000`-byte buffer (`+0x90`, `+0xA8`), a `0xC0`-byte buffer at `+0x98` filled through the immediate context (`+0x110`, Map and Unmap) with a quad spanning −1 to 1, a sampler at `+0x200`, four vertex, two geometry and ten pixel shaders, two input layouts, the `PrimitiveRendererPsConstantBuffer`, `…VsConstantBuffer` and `…GsConstantBuffer`, two state blocks, and the batcher at `+0x880` (`0x006DA850`) |

`0x0061DE20(state, mask)` turns a state block's descriptions into D3D11 state objects, each made once: with mask bit
`0x1` the rasterizer state at `+0x168` and, from the same description with fill mode 2 (wireframe), a second at
`+0x170`; with bit `0x2` the blend state at `+0x180`; with bit `0x4` the depth-stencil state at `+0x178`. `0x0061C550`
names these objects, all but the wireframe state at `+0x170` (`"BlendState"`, `"DepthStencilState"`, `"RasterState"`
and the buffer names above). `0x00624C30` passes all bits for each of its eight blocks.

`0x006DA850(batcher)` empties the batcher at `+0x880`: it clears the dword `+0x08` and the vertex
count word `+0x8010`. `0x006C9CD0` calls it at the end of the build and the scene end `0x006C9B20`
calls it too.

At the end of the build `0x006C9CD0` calls `0x006C9C40`, which resets the pending draw state: it zeroes the
`0x80` bytes from `+0x10`, sets `+0x208FC` to −1, clears `+0x1A0` to `+0x1BF`, the bytes `+0x851` and
`+0x208E8` and the word `+0x208F7`, stores 0.1 at `+0x208EC` and `1/1920` and `1/1080` at `+0x1E8` and
`+0x1EC`, and then begins a scene through slot `+0x130`.

### Batching draws

Slot `+0x020` (`0x006C8C50`) and slot `+0x028` (`0x006C8BF0`, with an index list) first run `0x006CB2A0`.
While the committed block `+0x398` is in use (its first dword non-zero) it flushes through
`0x006C88B0` and commits. Otherwise it flushes through slot `+0x128` and commits only when a pending
field differs from its committed copy, among them:

- the `0x80` bytes at `+0x10` against `+0x20868`, and `+0x1A0` to `+0x1B8` against `+0x1C0` to
  `+0x1D8`;
- `+0x851` against `+0x850`, `+0x208E8` against `+0x854`, `+0x208EC` against `+0x858`, and the pair
  `+0x1E8`/`+0x1EC` against `+0x1E0`/`+0x1E4`.

The commit `0x006C8920` copies the `0x190`-byte block at `+0x208` to `+0x398` (`0x006CACA0`, after
`0x0062BA30` on the old copy) and every pending field to its committed copy, and picks the shader
pair `+0x190`/`+0x198` from `+0x110` to `+0x148` by the flag `+0x851` and the word `+0x852`.

`0x006DA470(batcher, type, vertices, n, indices, m)` appends an indexed draw:

1. it maps the type to a batch mode (negative and 5 or more to 6, 2 to 4 to 2, 0 and 1 kept) and
   flushes when the batch holds vertices of another mode;
2. it flushes until `n` more vertices stay below 683 and `m` more indices within `0x4000`;
3. it appends the indices at `+0x10`, each raised by the batch's vertex count, and the `0x30`-byte
   vertices at `+0x8020`, and adds `n` to the count `+0x8010`.

The scene end `0x006C9B20` reads that count (`0x006DA6D0`); when it is non-zero it maps a vertex buffer
(slots `+0x148`, `+0x150`) and, with indices, an index buffer (`+0x158`, `+0x160`), copies the batch
into them, draws (`0x006C8CA0`) and empties the batcher (`0x006DA850`).

Slot `+0x060` (`0x006CADB0`) stores its byte at `+0x855`, or the byte `0x01F2EEB8` instead while
`0x02E5BDDC` is set. The render-thread callback `0x001F3A50` calls it for the
`MonsterGallerySoftParticleEnable` command, whose execute `0x001F32E0` passes
`0x001F3A50` and the command to `0x005FEA50`, and `0x001F3A50` calls the slot with the command's byte
`+0x18`, set by the builder `0x0018CCF0` through the constructor `0x001F1B50`.

The `Gi*` execute bodies call twenty of the slots:

| Offset | Body | What it does |
|---|---|---|
| `+0x000` | `0x006CA760` | returns the vertex staging area `this + 0x10880 + 0x7FE0 × [this+0x18860]`, zeroes the index and keeps the pointer at `+0xB8` |
| `+0x008` | `0x006CB5E0` | returns `+0xB8` |
| `+0x020` | `0x006C8C50` | passes the draw to the batcher at `+0x880` (`0x006DA5A0`) |
| `+0x080`, `+0x088` | `0x0060D760` | `mov eax, 0x17; ret`: no effect |
| `+0x098`, `+0x0A0`, `+0x0A8`, `+0x0B0` | `0x006CAB40`, `0x006CABF0`, `0x006CAC00`, `0x006CABE0` | forward to the state object at `+0x208` |
| `+0x128` | `0x006C9B00` | ends a scene (`0x006C9B20`, then `0x006C88B0`) |
| `+0x130` | `0x006CA7B0` | begins a scene: resets the state bytes at `+0x208F0`, binds the target |
| `+0x138` | `0x006C9AF0` | stores a byte at `+0x208F8` |

The others used are `+0x030`, `+0x038`, `+0x040`, `+0x048`, `+0x058`, `+0x078`, `+0x0D0` and
`+0x0D8`. The 0x7FE0-byte staging area holds 682 vertices of 0x30 bytes, the same batch size the
GS replay uses.

Every drawing command (`GiColorRect`, `GiNormal`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`,
`GiSprite`, `GiTrans`, `GiTransNz`) calls `+0x78`, then `+0x98`, then `+0x80`. Only `GiColorRect`,
`GiPolyGT4T`, `GiPrim`, `GiScreenImage` and `GiSprite` take the staging area through `+0x000`;
`GiTrans`, `GiTransNz`, `GiNormal` and `GiZNormalOnOff` only set state.

### Individual commands

- `GiSetTexture`'s execute `0x00863040` ignores the device and calls `0x00210570(id, pointer, dword)`
  with its `u16 +0x08`, `+0x10` and `+0x0C`. `0x00210570` stores `{pointer, dword}` in entry `id` of
  the 16-byte table `0x01F83580` when `id < 0x4000` as a signed compare, so ids `0x8000`–`0xFFFF`
  write below the table. The GS replay looks textures up in this table.
- `GiPolyGT4T`'s prepare `0x00864CA0` reads its `+0xF8`; when the id `& 0x3FFF` is `0xE00` it uses
  `0xDFF` while `0x02EC3ECC` is 0. It stores the first qword of the record `0x002D7FA0(id)` returns
  (from the 0x30-byte table `0x0209E6B0`) at `+0xD0` (`0x00864CD3`-`0x00864CD6`), and the first qword of the
  record `0x002D7EE0(+0xF8)` returns at `+0xD8` (`0x00864CE9`-`0x00864CEC`) and that record's dword `+8` at `+0xE0`.
- `GiZNormalOnOff` (`0x00864D70`) calls `0x00210560` with 0 or `0x70000` by its `+0x08` and sets device
  state through `+0xA0`, `+0x88` and `+0xA8`.

- `0x0039D410(value)` takes the `GiZNormalOnOff` command from its factory `0x00864E00`, stores the
  value at its `+0x08`, and files it with `0x00864E60(2)`, which runs `0x001FB840` and
  `0x0020E630(0x02EB3820, mode)` on the class's node.
- `GiPrim`'s factory `0x008642A0(node, n)` gives the command three arrays of `n` 16-byte entries from
  the command arena through `0x00864210`: positions at `+0x08`, texture coordinates at `+0x10` and
  colours at `+0x18`, with `n` at `+0x60`. It returns the command plus 8, the address of the
  first array pointer.

- The reset commands' executes (`0x001F3210`, `0x001F3260`) never read the command: they call
  `0x00188730` (default target) or `0x001893C0` on the render manager, closing and reopening the
  context's bit `0x1` bracket (`0x00609710`, `0x00600A60(ctx, 3)`, `0x005FEFD0(ctx, 0)`) around it.

### Render blocks

The device's ring holds 0x80-byte blocks, `u32` opcode at `+0x00` and payload from `+0x08`.
`0x0060A410` handles opcodes `0x01`–`0x06` and `0x2F` itself (byte table `0x0060AAD8`, arm table
`0x0060AAB8`) and passes `0x07`–`0x2E` to `0x00607410` (`0x0060A9D4`), whose table `0x006078E4` gives 39
of them their own arm; `0x12` takes the table's exit.

Opcodes `0x05` and `0x06` (`0x0060A8DE`, `0x0060A958`) copy 32 bytes of their payload and call
`0x00608F20(state, ...)`. It fills the next of two `0x70`-byte records at `0x02CBC590`, picked by the index
`0x02CB7FC8`, which it then sets to `(index - 1) & 1`, so the two records alternate (`0x00608F38`-`0x00608F57`).
Against the record bound before it sets bits `0x1`-`0x8` for each of `+0x38`, `+0x40`, `+0x48` and `+0x50`
that differs, or all four when `+0x28` differs (`0x00608FBF`-`0x00609010`), and passes that mask on
(`0x0060B860`, `0x0060EC80`).

Nine level-2 arms decode their payload and then call a body that does nothing: `0x1D`, `0x1E`,
`0x1F`, `0x25`, `0x27`, `0x28`, `0x29` and `0x2B` call `0x0060D760` (`mov eax, 0x17; ret`), and
`0x2E` calls `0x005C5230`. Opcode `0x25` is produced: `0x0060E810` writes it (`0x0060E8A8`) with a flag
byte at `+0x08` and floats at `+0x0C` and `+0x10`, called from the map draw `0x001E2AF0` (`0x001E3091`,
`0x001E3CD1`) and the character draw `0x001F5D70` (`0x001F5E9B`, `0x001F62CC`), and the arm `0x006076E9`
discards them.

Producers read for this page: `0x2F` `0x005FEA50`, `0x16` `0x005FEFD0`, `0x18` `0x00600A60`, `0x01` and
`0x02` `0x0060C020`, `0x03` `0x006007B0`, `0x25` `0x0060E810`. The full opcode table is
[`gi-render-commands-render-block-opcode-isa.tsv`](gi-render-commands-render-block-opcode-isa.tsv).

### Target binds and clear values

A target view is 24 bytes: `0x005DC190(view, target, flag)` stores the target at `+0x00`, 0 at
`+0x08` and `+0x10`, and the flag at `+0x0C`; `0x005DC1B0(view)` zeroes it.

- `0x0060D4F0(ctx, view, slot)` refuses a slot above 7 (3) and any bind while bit `0x1` of `+0x08` is
  set (`0x16`). It keeps the view at `ctx + 0x140 + 0x18 × slot`, sets bit `slot` of byte `+0x218`
  (a null view clears it) and takes the target's width and height into `+0x14` and `+0x18` (the
  back buffer's from `0x005FD050` for a null target).
- It then copies the view into the ring's data area and posts block `0x0E` with the copy's address
  at `+0x08` and the slot at `+0x10`.
- `0x0060DB50(ctx, view)` does the same for the depth target: `+0x200`, the byte `+0x219`, block
  `0x0F`.
- On the render thread the `0x0E` arm `0x0060D4A0(state, view, slot)` keeps the view at `+0x08 +
  0x18 × slot` with bit `slot` of `+0xE0`, then tail-jumps `0x006283E0`, which returns 5 for a slot
  above 7 and stores the view, or a zeroed one from `0x005DC1B0` for a null view, at `+0x570 + 0x18 ×
  slot`. The `0x0F` arm `0x0060DB10` keeps it at `+0xC8` with the byte `+0xE1` and tail-jumps
  `0x00628630`, which stores it at `+0x630` the same way.

`FastClearObj`'s execute `0x001F2FB0` unbinds slots 1 and 7, posts the clear colour from its
`+0x18`–`+0x24` with `0x0060D190` (block `0x09`, kept at `+0x7C0`–`+0x7CC` by `0x00628220`) when its
byte `+0x29` is set, and the depth value 1.0 with `0x0060D270` (block `0x0C`, kept at `+0x7D0` by
`0x00628300`) when its byte `+0x28` is set. It then opens the bracket with `0x005FEFD0`, passing bit `0x1`
for colour and bit `0x2` for depth, and restores the default target (`0x00188730`).

`0x00609A30(ctx)` posts block `0x2E`, which has no payload and whose arm does nothing. Its only
producer is `0x001D5620(marker, ctx)`, which posts it when byte `+0x08` of the marker object is set;
`RazorMarkerPopObj`'s execute `0x001F34E0` and several pass executes call it.

`0x001889C0(manager)` binds what `0x00188730` binds in its ordinary arm, without the second colour
target: the manager's target `+0xB08 + 8 × [+0xC30]` to slot 0, nothing to slots 1 and 7, the
depth target `+0xB58`, and a viewport (`0x0060F6B0`) of the manager's size, or 3,840 × 2,160 while
`+0xDB8` is set or `+0xC30` is 3. The post-process build `0x0018EEE0` calls it at `0x0018F3C3`, and before that at
`0x0018F338` when byte `+0x98` of the command it builds is set (`0x0018F323`-`0x0018F32A`).

## Layouts

Command arena ([`0x01F7F4C0`]), `0x20` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | base | 32 MB block |
| `+0x08` | `void*` | cursor |  |
| `+0x10` | `void*` | end |  |
| `+0x18` | `void*` | mark | `0x001A1460` sets, `0x001A14D0` rewinds to it |

Display-list record (`0x02F8F2F8` + `0x28` * i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | argument | passed to `+0x10` |
| `+0x08` | `u32` | sort key | `0x003A3A50` compares this dword |
| `+0x0C` | `u32` |  | appender count |
| `+0x10` | `void*` | function | called with `+0x00` when non-null |
| `+0x18` | `void*` | node | filed through `0x0020E630` when `+0x10` and `+0x00` are null |
| `+0x20` | `u8` | flags | bit `0x1`: `0x003A2BD0` first; bit `0x2`: post-processing point; bit `0x4`: defer to `0x02AEF420` |

Render block, `0x80` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | opcode | `0x01`-`0x2F` |
| `+0x08` | `...` | payload | for `0x2F`: `+0x08` function, `+0x10` argument |

```python
render context 0x02CC0410 (static, constructed by 0x00615840)
+0x18C0  PrimitiveRendererD3D11   vtables 0x00D86960 (+0x00) and 0x00D86AD0 (+0x08)
```

Tables beside this page:

| Subject | Table |
|---|---|
| every `GeometryInstance` class's slots, with the `DynGeo*` classes | [`gi-render-commands-geometry-instance-vtable-slots.tsv`](gi-render-commands-geometry-instance-vtable-slots.tsv) |
| `RenderObject`, `MapRenderObject`, `CharacterRenderObject` slots | [`gi-render-commands-render-object-vtable-slots.tsv`](gi-render-commands-render-object-vtable-slots.tsv) |
| the render-block opcodes, both levels | [`gi-render-commands-render-block-opcode-isa.tsv`](gi-render-commands-render-block-opcode-isa.tsv) |
| the device's fields | [`gi-render-commands-primitive-renderer-d3d11-accesses.tsv`](gi-render-commands-primitive-renderer-d3d11-accesses.tsv) |
| the render context | [`gi-render-commands-render-context-02cc0410-accesses.tsv`](gi-render-commands-render-context-02cc0410-accesses.tsv) |
| the context's pass-state block `+0x0B50` | [`gi-render-commands-render-context-pass-state-block-accesses.tsv`](gi-render-commands-render-context-pass-state-block-accesses.tsv) |
| the context's primitive-pass block `+0x07D8` | [`gi-render-commands-render-primitive-pass-1e8-accesses.tsv`](gi-render-commands-render-primitive-pass-1e8-accesses.tsv) |

### Columns of the slot tables and the opcode table

In gi-render-commands-geometry-instance-vtable-slots.tsv (145 rows) and
gi-render-commands-render-object-vtable-slots.tsv (29 rows) each row is one vtable slot; its `body` is the
pointer at `vtable + 8 × slot` on all 174 rows.

| Column | Holds |
|---|---|
| `role` | what the body does: `calls A,B,C +N` names its first three distinct direct callees in call order, and `+N` how many more it has (73 rows); `leaf` and the body's first instruction for a body with no call (61 rows); `no-op ret stub (folded)` for the shared body `0x0016D6A0`, a lone `ret` (20 rows); `dtor + free` for a destructor that frees through `0x00809950` (7 rows); `scalar-deleting dtor via` and the destructor it calls (2 rows); `setter this[+0xN] = arg` for a body that stores its argument at that offset (11 rows) |
| `cite` | one instruction of the body that shows the role: a call or tail jump on the `calls` rows (the first one in 70 of 73), the body's start on the `leaf` rows |

In gi-render-commands-render-block-opcode-isa.tsv each row is one block opcode, 47 rows: `level` 1 for the seven
that `0x0060A410` handles, 2 for the 40 it passes to `0x00607410`.

| Column | Holds |
|---|---|
| `handler_note` | the whole body of a handler that does nothing: `mov eax,0x17; ret` for `0x0060D760` (8 rows), `xor eax,eax; ret` for `0x005C5230` (`0x2E`), and for `0x12` that its arm is the dispatcher's shared exit; empty on the other 37 |
| `payload_read` | the block offsets the level-2 arm reads, in the order it reads them, with the payload from `+0x8`; empty on the 7 level-1 rows and on `0x12`, `0x19`, `0x1A` and `0x2E` |
| `render_emitters` | the functions that write the opcode into a block they take straight from the device ring (ring at context `+0x50` to `+0x58`, cursor `+0x60`), separated by commas; empty on 30 rows |

## State

| Address | What |
|---|---|
| `0x01F7F4C0` | the command arena |
| `0x01F7F4D0` | the filing handler (`GeometryRenderTargetImmediate`) |
| `0x02F8F2F8`, `0x02F8F2C6` | the draw list and its count |
| `0x02CC0410` | the render context; the device at `0x02CC1CD0` |
| `0x01F83580` | the texture table `GiSetTexture` fills |

## Modding notes

- A hook on device slot `+0x000` sees the quads and primitives but not `GiTrans`, `GiTransNz`,
  `GiNormal` or `GiZNormalOnOff`; a hook on `+0x78` sees every drawing command.
- `GiSetTexture` never reaches the device, so texture binds are visible only at `0x00210570`.
- Commands live in a ring: a frame that allocates more than the arena holds overwrites its own
  earliest commands instead of failing.
- The `Gi*` execute bodies run on PhyreEngine's render thread, not the game thread; anything they
  read can change under them.
- The depth bias carried by opcode `0x25` has no effect on this renderer.

## Related

- [Render command list](render-command-list.md): the ordered list and the walk that runs the wrappers.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): `GiVmax`, the GS replay and the texture lookup.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw and the `GiBeginEff` camera snapshot.
- [Text drawing](../Menus-And-HUD/text-drawing.md): the `DynGeo*` classes, also drawn from the command arena.
- [Game application](../Engine-Core/game-application.md): the pump and the frame-end reset.
- [Legacy PS2 GS layer](legacy-ps2-gs-layer.md): the texture records `GiPolyGT4T` resolves.
