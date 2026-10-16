---
title: "Gi render commands: the Gi* command family, the command arena, render blocks and the D3D11 primitive renderer"
kind: "system"
category: "Graphics"
addresses: "01F7F4C0, 001A1470, 001A1460, 001A14D0, 001FB840, 0020E630, 01F7F4D0, 001F48B0, 001F49F0, 005FEA50, 001F4A10, 02CC0410, 005FD050, 00624660, 00D86960, 006C8750, 00607D20, 006106A0, 0060A410, 00607410, 02F8F2F8, 003A3740, 003A3A00, 00210570, 01F83580"
---

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
| `GiBeginScene` | `00904488` | `001FBD80` | 8 | `0016D6A0` | `001FBD70`: device `+130`<sub>h</sub> |
| `GiEndScene` | `009044A0` | `001FBE50` | 8 | `0016D6A0` | `001FBE40`: device `+128`<sub>h</sub> |
| `GiTrans` | `01CCFA00` | `00862E50` | 8 | `0016D6A0` | `00862D40` |
| `GiTransNz` | `01CCFA18` | `00862FD0` | 8 | `0016D6A0` | `00862EC0` |
| `GiSetTexture` | `01CCFA30` | `00863060` | `18`<sub>h</sub> | `0016D6A0` | `00863040`: `00210570` |
| `GiColorRect` | `01CCFAB0` | `00863B40` | `70`<sub>h</sub> | `0016D6A0` | `00863850` |
| `GiPrim` | `01CCFAF0` | `008642A0` | `68`<sub>h</sub> | `008641B0` | `00863D80` |
| `GiSprite` | `01CCFB08` | `008647C0` | `E0`<sub>h</sub> | `00864750` | `00864330` |
| `GiPolyGT4T` | `01CCFB20` | `00864D10` | `100`<sub>h</sub> | `00864CA0` | `00864860` |
| `GiZNormalOnOff` | `01CCFB38` | `00864E00` | `10`<sub>h</sub> | `0016D6A0` | `00864D70` |
| `GiBeginEff` | `01CCFB78` | `00865130` | `90`<sub>h</sub> | `00864F30` | `00864E90` |
| `GiNormal` | `01CCFB90` | `008652B0` | 8 | `0016D6A0` | `008651A0` |
| `GiEndEff` | `01CCFBA8` | `00865320` | 8 | `0016D6A0` | `0016D6A0` |
| `GiSetRtForRtSampling` | `00902F28` | `001F16C0` | `18`<sub>h</sub> | `0016D6A0` | `001F16A0`: device `+38`<sub>h</sub> |
| `GiScreenImage` | `009068B8` | `0020E9F0` | `C0`<sub>h</sub> | `0016D6A0` | `0020E6C0` |
| `GiVmax` | `009007E8` | `001DB220` | `640`<sub>h</sub> | `001DB550` | `001DB3D0` |
| `GiResetRenderTargetObj` | `009033D0` | `001F1AF0` | heap `20`<sub>h</sub> | destructor | `001F3260` |
| `GiResetDefaultRenderTargetObj` | `009033F0` | `001F1AC0` | heap `20`<sub>h</sub> | destructor | `001F3210` |

`0016D6A0` is a bare `ret`, so prepare does nothing for eleven classes and `GiEndEff` does nothing
at all. Most factories also store the new command in a per-class global (`02EAF900`, `02EAF910`,
`02EAF920`, `02EB37F8`, `02EB3828`, `02EB3838`, `02EB3848`, `02EB3858`, `01F82EB8`, `01F83078`,
`01F83088`). `GiVmax`, the command that runs VIF1 packets at emit time, is on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md), and `GiBeginEff`'s
camera snapshot on [Phyre frame](../PhyreEngine/the-frame.md).

### The command arena

The installer `0017D4C0` creates the arena object at `01F7F4C0` (`0017D501`): `001A14E0` gives it
a 32 MB block (`2000000`<sub>h</sub>, through `001A1420`), with base `+00`<sub>h</sub>, cursor `+08`<sub>h</sub>, end `+10`<sub>h</sub> and
a mark `+18`<sub>h</sub>. `001A1470(arena, size)` rounds the request to `(size & ~Fh) + 10h`; it returns
the cursor and advances it while the request fits below the end, and otherwise restarts at the
base and returns the base (`001A14A5`–`001A14BD`). Commands are never freed one by one.

`0019C5A0(size)` and `0020E680()`, which asks for 16 bytes, are bare `001A1470` calls on
`[01F7F4C0]` for the command factories.

Each pass of the pump `0017D6E0` records the cursor as the mark (`001A1460` at `0017D757`), and
the frame-end reset `001E0590` rewinds the cursor to the mark (`001A14D0` at `001E05C7`); the same
two routines run on the `GiVmax` allocator `[01F82D00]` through `001DB600` and `001DB620`.

### Prepare and filing

An emitter stores the new command at `node + 8` and calls `001FB840(node)`, which copies it to
`node + 0` and tail-jumps the command's slot 0. `GiBeginScene`'s factory `001FBD80(mode)` shows
the whole path for a command filed at once:

1. allocate 8 bytes, store the vtable, store the command at `01F83078` = `01F83070 + 8`;
2. `001FB840(01F83070)`;
3. `0020E630(01F83070, mode)`;
4. for a mode other than 3, enqueue a `GiResetRenderTargetObj` (`0018BF00` at `001FBE02`).

`0020E630(node, mode)` turns the mode into a class key, 0 → 8, 1 → `20`<sub>h</sub>, 2 → `40`<sub>h</sub>, 3 → `20`<sub>h</sub>
and anything else → 0, and hands `node[0]` and the key through `001FB810` to `001A17F0` on the
handler object `[01F7F4D0]`. That object is created by the installer (`0017D547`) with
`001A17D0`, which stores the vtable `008F5F28` and points its handler field `+08`<sub>h</sub> at itself, so
the call reaches slot 0 of `008F5F28`: `001F48B0`.

`001F48B0(handler, command, key)` takes `28`<sub>h</sub> bytes from the command arena, builds a
`GeometryInstanceOrderedObject` (`001F4950`: vtable `00903920`, command at `+18`<sub>h</sub>, key at
`+20`<sub>h</sub>) and appends it to the ordered command list (`001F4940`). The render body's walk later
calls its slot 1, `001F49F0`.

`001FB830(node)` is the path for a command that must run at once: `001A1850([01F7F4D0],
node[0])` takes `28`<sub>h</sub> bytes from the arena, wraps the command in a `GeometryInstanceOrderedObject`
(`001F4950`, key 0) and calls its slot 1 straight away with the render manager's device `+08`<sub>h</sub>.

Without a render manager (`00189120` returns 0) it files the command through the handler with key
`40`<sub>h</sub> instead. `001F16C0(a, b)`, called by the render-manager installer `00186CD0`, by `00188B10`
and by `00188DA0`, builds a `GiSetRtForRtSampling` command of `18`<sub>h</sub> bytes (`a` at `+08`<sub>h</sub>, `b` at
`+10`<sub>h</sub>) and runs it this way.

### The display list

Per-draw producers file records instead. The list is created by `003A3670`: `190000`<sub>h</sub> bytes
(40,960 records of `28`<sub>h</sub>) at `02F8F2F8`, a `C8028`<sub>h</sub>-byte sort area at `02F8F300`, and a data
arena whose base is `02F8F308` (`003A36BD`); the count is the `u16` at `02F8F2C6`.

`0024D540`, called by the draw `0022B0B0` at `0022B191`, runs the drain `003A3740` and then the
rewind `003A3A00`; the VFX layer passes `00259030` and `002590F0` call the drain alone. The drain sorts the records
with the merge sort `003A3A50` on the `u32` at `+08`<sub>h</sub> (`003A3B53`, `003A3C83`) and walks them:

1. when `00180040()` is 1, the record's flag bit 1 is set, `0022BE90()` is 1 and `0022BEA0()` is 0,
   it inserts the post-processing block once (`003A3823`–`003A38AA`);
2. flag bit 0 calls `003A2BD0` first;
3. a non-null function at `+10`<sub>h</sub> is called with `+00`<sub>h</sub> (`003A38C6`);
4. otherwise, when `+00`<sub>h</sub> is null: flag bit 2 clear files the node `+18`<sub>h</sub> with `0020E630(node, 2)`
   (`003A38DE`); flag bit 2 set appends the node to the array `02AEF420` (count `02AEF414`).

`003A3A00` sets the count to 0, rewinds the data arena `02F8F2D0` to `02F8F308` and clears bit 0
of `02F8F310`.

### From the ordered list to the render thread

`GeometryInstanceOrderedObject`'s slot 1 `001F49F0(object, device)` calls
`005FEA50(device, 001F4A10, command)`. `005FEA50` reserves a `80`<sub>h</sub>-byte block in the device's ring
(`+50`<sub>h</sub> base, `+58`<sub>h</sub> end, `+60`<sub>h</sub> cursor, restarting at the base when full), records the pending
range at `+88`<sub>h</sub>/`+90`<sub>h</sub>, and writes opcode `2F`<sub>h</sub> at `+00`<sub>h</sub>, the function at `+08`<sub>h</sub> and the
command at `+10`<sub>h</sub> (`005FEAEE`–`005FEAF8`).

`00607D20` builds a 256-slot block queue with semaphores and per-slot events and starts the thread
`005FE1F0` (`CreateThread` through `005CD1E0`, 64 KB stack); its name string is
`PhyreEngineRenderThread`. `005FE1F0` jumps to `006106A0`, which waits on each slot's event in
turn (`00610724`), runs `0060A410(queue, start, end)` on the slot's range (`00610753`) and releases
the completion semaphore (`00610774`).

The queue is the static `02CE4720`, which `005FD0E0` returns, building it on first use (a guarded
static) with `005DC200`: a `PProcessorProfileTimelineCpu` at `+20`<sub>h</sub>, the state `+28`<sub>h</sub>, 256 slots
of `28`<sub>h</sub> bytes from `+30`<sub>h</sub>, two handles at `+2840`<sub>h</sub> and `+2850`<sub>h</sub>, and four `10`<sub>h</sub>-byte records from
`+2860`<sub>h</sub>. It registers `008ADDE0` with `atexit`.

At exit `008ADDE0` stops the thread through
`00610420`, which, while the state is 1, sets it to 2, calls `00609720(queue, 0, 0, 0)`, waits for
the thread (`005CD330`) and closes the 256 slot events and the two handles (`005CD700`,
`CloseHandle`). It then closes the handles of the four records, clears `02CE6FC0` and runs the
members' destructors.

`0060A410` fetches the render context once (`0060A46A`: `00624670` → `005FD050`, which returns the
static `02CC0410`, constructing it with `00615840` on first use) and walks the range `80`<sub>h</sub> bytes at
a time. For opcode `2F`<sub>h</sub> it builds a three-qword frame `{context, &local, block+10h}` on its stack
and calls `block+08h` with it (`0060A8BD`–`0060A8D6`). `001F4A10` takes the device as
`context + 18C0h` (`00624660`) and tail-jumps the command's slot 1 with it (`001F4A35`).

Before the walk `0060A410` also lays a `50`<sub>h</sub>-byte record on its stack with `00615D50(record,
context)`: the context at `+00`<sub>h</sub>, the rest zero.

### The device

`00615840` builds the device inside the context: `006C8750(context + 18C0h)` (`00615B57`) stores
the `PrimitiveRendererD3D11` vtable `00D86960` at `+00`<sub>h</sub> and its second vtable `00D86AD0` at
`+08`<sub>h</sub>. The first table has 45 slots (`006CA760` to `006CB540`, followed by the locator
`01D38180` at `00D86AC8`); the second has one slot, `006C88A0`.

### The context's draw blocks

After it has the D3D11 device and swap chain, the context initialiser `00625830` builds three
blocks of shaders and buffers from shader bytecode embedded in the executable; each blob follows a
length dword, and the size passed to the device is that length minus 2. The device calls go through the `ID3D11Device` vtable at context
`+108`<sub>h</sub>: `+18`<sub>h</sub> CreateBuffer, `+58`<sub>h</sub> CreateInputLayout, `+60`<sub>h</sub> CreateVertexShader, `+68`<sub>h</sub>
CreateGeometryShader, `+78`<sub>h</sub> CreatePixelShader and `+B8`<sub>h</sub> CreateSamplerState.

| Block offset | Builder | Contents |
|---|---|---|
| `07D8`<sub>h</sub> | `00624980` (`00625D37`) | a vertex buffer, one vertex shader (`01F2EEC0`), three pixel shaders, a POSITION/TEXCOORD/TEXCOORD input layout and the `50`<sub>h</sub>-byte `DebugDrawConstantBuffer` |
| `0B50`<sub>h</sub> | `00624C30` (`00625D4E`) | one vertex shader (`01F2FEB4`), eight pixel shaders, the `DrawClearConstantBuffer`, and eight state blocks |
| `18C0`<sub>h</sub> | `006C9CD0` (`00625D65`) | the `PrimitiveRendererD3D11` resources: a `7FE0`<sub>h</sub>-byte and a `8000`<sub>h</sub>-byte buffer (`+90`<sub>h</sub>, `+A8`<sub>h</sub>), a `C0`<sub>h</sub>-byte buffer at `+98`<sub>h</sub> filled through the immediate context (`+110`<sub>h</sub>, Map and Unmap) with a quad spanning −1 to 1, a sampler at `+200`<sub>h</sub>, four vertex, two geometry and ten pixel shaders, two input layouts, the `PrimitiveRendererPsConstantBuffer`, `…VsConstantBuffer` and `…GsConstantBuffer`, two state blocks, and the batcher at `+880`<sub>h</sub> (`006DA850`) |

`0061DE20(state, mask)` turns a state block's descriptions into D3D11 state objects, each made
once: with mask bit 0 the rasterizer state at `+168`<sub>h</sub> and, from the same description with fill
mode 2 (wireframe), a second at `+170`<sub>h</sub>; with bit 1 the blend state at `+180`<sub>h</sub>; with bit 2 the
depth-stencil state at `+178`<sub>h</sub>. `0061C550` names each object (`"BlendState"`,
`"DepthStencilState"`, `"RasterState"` and the buffer names above). `00624C30` passes all bits
for each of its eight blocks.

`006DA850(batcher)` empties the batcher at `+880`<sub>h</sub>: it clears the dword `+08`<sub>h</sub> and the vertex
count word `+8010`<sub>h</sub>. `006C9CD0` calls it at the end of the build and the scene end `006C9B20`
calls it too.

At the end of the build `006C9CD0` calls `006C9C40`, which resets the pending draw state: it zeroes the
`80`<sub>h</sub> bytes from `+10`<sub>h</sub>, sets `+208FC`<sub>h</sub> to −1, clears `+1A0`<sub>h</sub> to `+1BF`<sub>h</sub>, the bytes `+851`<sub>h</sub> and
`+208E8`<sub>h</sub> and the word `+208F7`<sub>h</sub>, stores 0.1 at `+208EC`<sub>h</sub> and `1/1920` and `1/1080` at `+1E8`<sub>h</sub> and
`+1EC`<sub>h</sub>, and then begins a scene through slot `+130`<sub>h</sub>.

### Batching draws

Slot `+020`<sub>h</sub> (`006C8C50`) and slot `+028`<sub>h</sub> (`006C8BF0`, with an index list) first run `006CB2A0`.
While the committed block `+398`<sub>h</sub> is in use (its first dword non-zero) it flushes through
`006C88B0` and commits. Otherwise it flushes through slot `+128`<sub>h</sub> and commits only when a pending
field differs from its committed copy, among them:

- the `80`<sub>h</sub> bytes at `+10`<sub>h</sub> against `+20868`<sub>h</sub>, and `+1A0`<sub>h</sub> to `+1B8`<sub>h</sub> against `+1C0`<sub>h</sub> to
  `+1D8`<sub>h</sub>;
- `+851`<sub>h</sub> against `+850`<sub>h</sub>, `+208E8`<sub>h</sub> against `+854`<sub>h</sub>, `+208EC`<sub>h</sub> against `+858`<sub>h</sub>, and the pair
  `+1E8`<sub>h</sub>/`+1EC`<sub>h</sub> against `+1E0`<sub>h</sub>/`+1E4`<sub>h</sub>.

The commit `006C8920` copies the `190`<sub>h</sub>-byte block at `+208`<sub>h</sub> to `+398`<sub>h</sub> (`006CACA0`, after
`0062BA30` on the old copy) and every pending field to its committed copy, and picks the shader
pair `+190`<sub>h</sub>/`+198`<sub>h</sub> from `+110`<sub>h</sub> to `+148`<sub>h</sub> by the flag `+851`<sub>h</sub> and the word `+852`<sub>h</sub>.

`006DA470(batcher, type, vertices, n, indices, m)` appends an indexed draw:

1. it maps the type to a batch mode (negative and 5 or more to 6, 2 to 4 to 2, 0 and 1 kept) and
   flushes when the batch holds vertices of another mode;
2. it flushes until `n` more vertices stay below 683 and `m` more indices within `4000`<sub>h</sub>;
3. it appends the indices at `+10`<sub>h</sub>, each raised by the batch's vertex count, and the `30`<sub>h</sub>-byte
   vertices at `+8020`<sub>h</sub>, and adds `n` to the count `+8010`<sub>h</sub>.

The scene end `006C9B20` reads that count (`006DA6D0`); when it is non-zero it maps a vertex buffer
(slots `+148`<sub>h</sub>, `+150`<sub>h</sub>) and, with indices, an index buffer (`+158`<sub>h</sub>, `+160`<sub>h</sub>), copies the batch
into them, draws (`006C8CA0`) and empties the batcher (`006DA850`).

Slot `+060`<sub>h</sub> (`006CADB0`) stores its byte at `+855`<sub>h</sub>, or the byte `01F2EEB8` instead while
`02E5BDDC` is set. The render-thread callback `001F3A50` calls it for the
`MonsterGallerySoftParticleEnable` command, whose execute `001F32E0` passes
`001F3A50` and the command to `005FEA50`, and `001F3A50` calls the slot with the command's byte
`+18`<sub>h</sub>, set by the builder `0018CCF0` through the constructor `001F1B50`.

The `Gi*` execute bodies call twenty of the slots:

| Offset | Body | What it does |
|---|---|---|
| `000`<sub>h</sub> | `006CA760` | returns the vertex staging area `this + 10880h + 7FE0h × [this+18860h]`, zeroes the index and keeps the pointer at `+B8`<sub>h</sub> |
| `008`<sub>h</sub> | `006CB5E0` | returns `+B8`<sub>h</sub> |
| `020`<sub>h</sub> | `006C8C50` | passes the draw to the batcher at `+880`<sub>h</sub> (`006DA5A0`) |
| `+080`<sub>h</sub>, `+088`<sub>h</sub> | `0060D760` | `mov eax, 17h; ret`: no effect |
| `+098`<sub>h</sub>, `+0A0`<sub>h</sub>, `+0A8`<sub>h</sub>, `+0B0`<sub>h</sub> | `006CAB40`, `006CABF0`, `006CAC00`, `006CABE0` | forward to the state object at `+208`<sub>h</sub> |
| `128`<sub>h</sub> | `006C9B00` | ends a scene (`006C9B20`, then `006C88B0`) |
| `130`<sub>h</sub> | `006CA7B0` | begins a scene: resets the state bytes at `+208F0`<sub>h</sub>, binds the target |
| `138`<sub>h</sub> | `006C9AF0` | stores a byte at `+208F8`<sub>h</sub> |

The others used are `+030`<sub>h</sub>, `+038`<sub>h</sub>, `+040`<sub>h</sub>, `+048`<sub>h</sub>, `+058`<sub>h</sub>, `+078`<sub>h</sub>, `+0D0`<sub>h</sub> and
`+0D8`<sub>h</sub>. The `7FE0`<sub>h</sub>-byte staging area holds 682 vertices of `30`<sub>h</sub> bytes, the same batch size the
GS replay uses.

Every drawing command (`GiColorRect`, `GiNormal`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`,
`GiSprite`, `GiTrans`, `GiTransNz`) calls `+78`<sub>h</sub>, then `+98`<sub>h</sub>, then `+80`<sub>h</sub>. Only `GiColorRect`,
`GiPolyGT4T`, `GiPrim`, `GiScreenImage` and `GiSprite` take the staging area through `+000`<sub>h</sub>;
`GiTrans`, `GiTransNz`, `GiNormal` and `GiZNormalOnOff` only set state.

### Individual commands

- `GiSetTexture`'s execute `00863040` ignores the device and calls `00210570(id, pointer, dword)`
  with its `u16 +08h`, `+10`<sub>h</sub> and `+0C`<sub>h</sub>. `00210570` stores `{pointer, dword}` in entry `id` of
  the 16-byte table `01F83580` when `id < 4000h` as a signed compare, so ids `8000`<sub>h</sub>–`FFFF`<sub>h</sub>
  write below the table. The GS replay looks textures up in this table.
- `GiPolyGT4T`'s prepare `00864CA0` reads its `+F8`<sub>h</sub>; when the id `& 3FFFh` is `E00`<sub>h</sub> it uses
  `DFF`<sub>h</sub> while `02EC3ECC` is 0. It stores the record `002D7FA0(id)` returns (from the `30`<sub>h</sub>-byte
  table `0209E6B0`) at `+D0`<sub>h</sub>, and the record `002D7EE0(+F8h)` returns at `+D8`<sub>h</sub> and its dword `+8` at `+E0`<sub>h</sub>.
- `GiZNormalOnOff` (`00864D70`) calls `00210560` with 0 or `70000`<sub>h</sub> by its `+08`<sub>h</sub> and sets device
  state through `+A0`<sub>h</sub>, `+88`<sub>h</sub> and `+A8`<sub>h</sub>.

- `0039D410(value)` takes the `GiZNormalOnOff` command from its factory `00864E00`, stores the
  value at its `+08`<sub>h</sub>, and files it with `00864E60(2)`, which runs `001FB840` and
  `0020E630(02EB3820, mode)` on the class's node.
- `GiPrim`'s factory `008642A0(node, n)` gives the command three arrays of `n` 16-byte entries from
  the command arena through `00864210`: positions at `+08`<sub>h</sub>, texture coordinates at `+10`<sub>h</sub> and
  colours at `+18`<sub>h</sub>, with `n` at `+60`<sub>h</sub>. It returns the command plus 8, the address of the
  first array pointer.

- The reset commands' executes (`001F3210`, `001F3260`) never read the command: they call
  `00188730` (default target) or `001893C0` on the render manager, closing and reopening the
  context's bit-0 bracket (`00609710`, `00600A60(ctx, 3)`, `005FEFD0(ctx, 0)`) around it.

### Render blocks

The device's ring holds `80`<sub>h</sub>-byte blocks, `u32` opcode at `+00`<sub>h</sub> and payload from `+08`<sub>h</sub>.
`0060A410` handles opcodes `01`<sub>h</sub>–`06`<sub>h</sub> and `2F`<sub>h</sub> itself (byte table `0060AAD8`, arm table
`0060AAB8`) and passes `07`<sub>h</sub>–`2E`<sub>h</sub> to `00607410` (`0060A9D4`), whose table `006078E4` gives 39
of them their own arm; `12`<sub>h</sub> takes the table's exit.

Nine level-2 arms decode their payload and then call a body that does nothing: `1D`<sub>h</sub>, `1E`<sub>h</sub>,
`1F`<sub>h</sub>, `25`<sub>h</sub>, `27`<sub>h</sub>, `28`<sub>h</sub>, `29`<sub>h</sub> and `2B`<sub>h</sub> call `0060D760` (`mov eax, 17h; ret`), and
`2E`<sub>h</sub> calls `005C5230`. Opcode `25`<sub>h</sub> is produced: `0060E810` writes it (`0060E8A8`) with a flag
byte at `+08`<sub>h</sub> and floats at `+0C`<sub>h</sub> and `+10`<sub>h</sub>, called from the map draw `001E2AF0` (`001E3091`,
`001E3CD1`) and the character draw `001F5D70` (`001F5E9B`, `001F62CC`), and the arm `006076E9`
discards them.

Producers read for this page: `2F`<sub>h</sub> `005FEA50`, `16`<sub>h</sub> `005FEFD0`, `18`<sub>h</sub> `00600A60`, `01`<sub>h</sub> and
`02`<sub>h</sub> `0060C020`, `03`<sub>h</sub> `006007B0`, `25`<sub>h</sub> `0060E810`. The full opcode table is
`gi-render-commands-render-block-opcode-isa.tsv`.

### Target binds and clear values

A target view is 24 bytes: `005DC190(view, target, flag)` stores the target at `+00`<sub>h</sub>, 0 at
`+08`<sub>h</sub> and `+10`<sub>h</sub>, and the flag at `+0C`<sub>h</sub>; `005DC1B0(view)` zeroes it.

- `0060D4F0(ctx, view, slot)` refuses a slot above 7 (3) and any bind while bit 0 of `+08`<sub>h</sub> is
  set (`16`<sub>h</sub>). It keeps the view at `ctx + 140h + 18h × slot`, sets bit `slot` of byte `+218`<sub>h</sub>
  (a null view clears it) and takes the target's width and height into `+14`<sub>h</sub> and `+18`<sub>h</sub> (the
  back buffer's from `005FD050` for a null target).
- It then copies the view into the ring's data area and posts block `0E`<sub>h</sub> with the copy's address
  at `+08`<sub>h</sub> and the slot at `+10`<sub>h</sub>.
- `0060DB50(ctx, view)` does the same for the depth target: `+200`<sub>h</sub>, the byte `+219`<sub>h</sub>, block
  `0F`<sub>h</sub>.
- On the render thread the `0E`<sub>h</sub> arm `0060D4A0(state, view, slot)` keeps the view at `+08h +
  18h × slot` with bit `slot` of `+E0`<sub>h</sub>, then tail-jumps `006283E0`, which returns 5 for a slot
  above 7 and stores the view, or a zeroed one from `005DC1B0` for a null view, at `+570h + 18h ×
  slot`. The `0F`<sub>h</sub> arm `0060DB10` keeps it at `+C8`<sub>h</sub> with the byte `+E1`<sub>h</sub> and tail-jumps
  `00628630`, which stores it at `+630`<sub>h</sub> the same way.

`FastClearObj`'s execute `001F2FB0` unbinds slots 1 and 7, posts the clear colour from its
`+18`<sub>h</sub>–`+24`<sub>h</sub> with `0060D190` (block `09`<sub>h</sub>, kept at `+7C0`<sub>h</sub>–`+7CC`<sub>h</sub> by `00628220`) when its
byte `+29`<sub>h</sub> is set, and the depth value 1.0 with `0060D270` (block `0C`<sub>h</sub>, kept at `+7D0`<sub>h</sub> by
`00628300`) when its byte `+28`<sub>h</sub> is set. It then opens the bracket with `005FEFD0`, passing bit 0
for colour and bit 1 for depth, and restores the default target (`00188730`).

`00609A30(ctx)` posts block `2E`<sub>h</sub>, which has no payload and whose arm does nothing. Its only
producer is `001D5620(marker, ctx)`, which posts it when byte `+08`<sub>h</sub> of the marker object is set;
`RazorMarkerPopObj`'s execute `001F34E0` and several pass executes call it.

`001889C0(manager)` binds what `00188730` binds in its ordinary arm, without the second colour
target: the manager's target `+B08h + 8 × [+C30h]` to slot 0, nothing to slots 1 and 7, the
depth target `+B58`<sub>h</sub>, and a viewport (`0060F6B0`) of the manager's size, or 3,840 × 2,160 while
`+DB8`<sub>h</sub> is set or `+C30`<sub>h</sub> is 3. The post-process build `0018EEE0` calls it twice.

## Layouts

Command arena ([`01F7F4C0`]), `20`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | base | 32 MB block |
| `08`<sub>h</sub> | `void*` | cursor |  |
| `10`<sub>h</sub> | `void*` | end |  |
| `18`<sub>h</sub> | `void*` | mark | `001A1460` sets, `001A14D0` rewinds to it |

Display-list record (`02F8F2F8` + `28`<sub>h</sub> * i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | argument | passed to +`10`<sub>h</sub> |
| `08`<sub>h</sub> | `u32` | sort key | `003A3A50` compares this dword |
| `0C`<sub>h</sub> | `u32` | appender count |  |
| `10`<sub>h</sub> | `void*` | function | called with +`00`<sub>h</sub> when non-null |
| `18`<sub>h</sub> | `void*` | node | filed through `0020E630` when +`10`<sub>h</sub> and +`00`<sub>h</sub> are null |
| `20`<sub>h</sub> | `u8` | flags | bit 0: `003A2BD0` first; bit 1: post-processing point; bit 2: defer to `02AEF420` |

Render block, `80`<sub>h</sub> bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | opcode | `01`<sub>h</sub>-`2F`<sub>h</sub> |
| `08`<sub>h</sub> | `...` | payload | for `2F`<sub>h</sub>: +`08`<sub>h</sub> function, +`10`<sub>h</sub> argument |

```python
render context 02CC0410 (static, constructed by 00615840)
+0x18C0  PrimitiveRendererD3D11   vtables 00D86960 (+0x00) and 00D86AD0 (+0x08)
```

Tables beside this page:

| Subject | Table |
|---|---|
| every `GeometryInstance` class's slots, with the `DynGeo*` classes | `gi-render-commands-geometry-instance-vtable-slots.tsv` |
| `RenderObject`, `MapRenderObject`, `CharacterRenderObject` slots | `gi-render-commands-render-object-vtable-slots.tsv` |
| the render-block opcodes, both levels | `gi-render-commands-render-block-opcode-isa.tsv` |
| the device's fields | `gi-render-commands-primitive-renderer-d3d11-accesses.tsv` |
| the render context | `gi-render-commands-render-context-02cc0410-accesses.tsv` |
| the context's pass-state block `+0B50`<sub>h</sub> | `gi-render-commands-render-context-pass-state-block-accesses.tsv` |
| the context's primitive-pass block `+07D8`<sub>h</sub> | `gi-render-commands-render-primitive-pass-1e8-accesses.tsv` |

## State

| Address | What |
|---|---|
| `01F7F4C0` | the command arena |
| `01F7F4D0` | the filing handler (`GeometryRenderTargetImmediate`) |
| `02F8F2F8`, `02F8F2C6` | the display list and its count |
| `02CC0410` | the render context; the device at `02CC1CD0` |
| `01F83580` | the texture table `GiSetTexture` fills |

## Modding notes

- A hook on device slot `+000`<sub>h</sub> sees the quads and primitives but not `GiTrans`, `GiTransNz`,
  `GiNormal` or `GiZNormalOnOff`; a hook on `+78`<sub>h</sub> sees every drawing command.
- `GiSetTexture` never reaches the device, so texture binds are visible only at `00210570`.
- Commands live in a ring: a frame that allocates more than the arena holds overwrites its own
  earliest commands instead of failing.
- The `Gi*` execute bodies run on PhyreEngine's render thread, not the game thread; anything they
  read can change under them.
- The depth bias carried by opcode `25`<sub>h</sub> has no effect on this renderer.

## Related

- [Render command list](render-command-list.md): the ordered list and the walk that runs the wrappers.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): `GiVmax`, the GS replay and the texture lookup.
- [Phyre frame](../PhyreEngine/the-frame.md): the draw and the `GiBeginEff` camera snapshot.
- [Text drawing](../Menus-And-HUD/text-drawing.md): the `DynGeo*` classes, also drawn from the command arena.
- [Game application](../Engine-Core/game-application.md): the pump and the frame-end reset.
- [Legacy PS2 GS layer](legacy-ps2-gs-layer.md): the texture records `GiPolyGT4T` resolves.
