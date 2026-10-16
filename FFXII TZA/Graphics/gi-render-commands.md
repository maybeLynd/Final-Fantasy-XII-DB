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
| `GiBeginScene` | `00904488` | `001FBD80` | 8 | `0016D6A0` | `001FBD70`: device `+0x130` |
| `GiEndScene` | `009044A0` | `001FBE50` | 8 | `0016D6A0` | `001FBE40`: device `+0x128` |
| `GiTrans` | `01CCFA00` | `00862E50` | 8 | `0016D6A0` | `00862D40` |
| `GiTransNz` | `01CCFA18` | `00862FD0` | 8 | `0016D6A0` | `00862EC0` |
| `GiSetTexture` | `01CCFA30` | `00863060` | 0x18 | `0016D6A0` | `00863040`: `00210570` |
| `GiColorRect` | `01CCFAB0` | `00863B40` | 0x70 | `0016D6A0` | `00863850` |
| `GiPrim` | `01CCFAF0` | `008642A0` | 0x68 | `008641B0` | `00863D80` |
| `GiSprite` | `01CCFB08` | `008647C0` | 0xE0 | `00864750` | `00864330` |
| `GiPolyGT4T` | `01CCFB20` | `00864D10` | 0x100 | `00864CA0` | `00864860` |
| `GiZNormalOnOff` | `01CCFB38` | `00864E00` | 0x10 | `0016D6A0` | `00864D70` |
| `GiBeginEff` | `01CCFB78` | `00865130` | 0x90 | `00864F30` | `00864E90` |
| `GiNormal` | `01CCFB90` | `008652B0` | 8 | `0016D6A0` | `008651A0` |
| `GiEndEff` | `01CCFBA8` | `00865320` | 8 | `0016D6A0` | `0016D6A0` |
| `GiSetRtForRtSampling` | `00902F28` | `001F16C0` | 0x18 | `0016D6A0` | `001F16A0`: device `+0x38` |
| `GiScreenImage` | `009068B8` | `0020E9F0` | 0xC0 | `0016D6A0` | `0020E6C0` |
| `GiVmax` | `009007E8` | `001DB220` | 0x640 | `001DB550` | `001DB3D0` |
| `GiResetRenderTargetObj` | `009033D0` | `001F1AF0` | heap 0x20 | destructor | `001F3260` |
| `GiResetDefaultRenderTargetObj` | `009033F0` | `001F1AC0` | heap 0x20 | destructor | `001F3210` |

`0016D6A0` is a bare `ret`, so prepare does nothing for eleven classes and `GiEndEff` does nothing
at all. Most factories also store the new command in a per-class global (`02EAF900`, `02EAF910`,
`02EAF920`, `02EB37F8`, `02EB3828`, `02EB3838`, `02EB3848`, `02EB3858`, `01F82EB8`, `01F83078`,
`01F83088`). `GiVmax`, the command that runs VIF1 packets at emit time, is on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md), and `GiBeginEff`'s
camera snapshot on [Phyre frame](../PhyreEngine/the-frame.md).

### The command arena

The installer `0017D4C0` creates the arena object at `01F7F4C0` (`0017D501`): `001A14E0` gives it
a 32 MB block (`0x2000000`, through `001A1420`), with base `+0x00`, cursor `+0x08`, end `+0x10` and
a mark `+0x18`. `001A1470(arena, size)` rounds the request to `(size & ~0xF) + 0x10`; it returns
the cursor and advances it while the request fits below the end, and otherwise restarts at the
base and returns the base (`001A14A5`–`001A14BD`). Commands are never freed one by one.

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

`0020E630(node, mode)` turns the mode into a class key, 0 → 8, 1 → `0x20`, 2 → `0x40`, 3 → `0x20`
and anything else → 0, and hands `node[0]` and the key through `001FB810` to `001A17F0` on the
handler object `[01F7F4D0]`. That object is created by the installer (`0017D547`) with
`001A17D0`, which stores the vtable `008F5F28` and points its handler field `+0x08` at itself, so
the call reaches slot 0 of `008F5F28`: `001F48B0`.

`001F48B0(handler, command, key)` takes 0x28 bytes from the command arena, builds a
`GeometryInstanceOrderedObject` (`001F4950`: vtable `00903920`, command at `+0x18`, key at
`+0x20`) and appends it to the ordered command list (`001F4940`). The render body's walk later
calls its slot 1, `001F49F0`.

### The display list

Per-draw producers file records instead. The list is created by `003A3670`: `0x190000` bytes
(40,960 records of 0x28) at `02F8F2F8`, a `0xC8028`-byte sort area at `02F8F300`, and a data
arena whose base is `02F8F308` (`003A36BD`); the count is the `u16` at `02F8F2C6`.

`0024D540`, called by the draw `0022B0B0` at `0022B191`, runs the drain `003A3740` and then the
rewind `003A3A00`; the VFX layer passes `00259030` and `002590F0` call the drain alone. The drain sorts the records
with the merge sort `003A3A50` on the `u32` at `+0x08` (`003A3B53`, `003A3C83`) and walks them:

1. when `00180040()` is 1, the record's flag bit 1 is set, `0022BE90()` is 1 and `0022BEA0()` is 0,
   it inserts the post-processing block once (`003A3823`–`003A38AA`);
2. flag bit 0 calls `003A2BD0` first;
3. a non-null function at `+0x10` is called with `+0x00` (`003A38C6`);
4. otherwise, when `+0x00` is null: flag bit 2 clear files the node `+0x18` with `0020E630(node, 2)`
   (`003A38DE`); flag bit 2 set appends the node to the array `02AEF420` (count `02AEF414`).

`003A3A00` sets the count to 0, rewinds the data arena `02F8F2D0` to `02F8F308` and clears bit 0
of `02F8F310`.

### From the ordered list to the render thread

`GeometryInstanceOrderedObject`'s slot 1 `001F49F0(object, device)` calls
`005FEA50(device, 001F4A10, command)`. `005FEA50` reserves a 0x80-byte block in the device's ring
(`+0x50` base, `+0x58` end, `+0x60` cursor, restarting at the base when full), records the pending
range at `+0x88`/`+0x90`, and writes opcode `0x2F` at `+0x00`, the function at `+0x08` and the
command at `+0x10` (`005FEAEE`–`005FEAF8`).

`00607D20` builds a 256-slot block queue with semaphores and per-slot events and starts the thread
`005FE1F0` (`CreateThread` through `005CD1E0`, 64 KB stack); its name string is
`PhyreEngineRenderThread`. `005FE1F0` jumps to `006106A0`, which waits on each slot's event in
turn (`00610724`), runs `0060A410(queue, start, end)` on the slot's range (`00610753`) and releases
the completion semaphore (`00610774`).

`0060A410` fetches the render context once (`0060A46A`: `00624670` → `005FD050`, which returns the
static `02CC0410`, constructing it with `00615840` on first use) and walks the range 0x80 bytes at
a time. For opcode `0x2F` it builds a three-qword frame `{context, &local, block+0x10}` on its stack
and calls `block+0x08` with it (`0060A8BD`–`0060A8D6`). `001F4A10` takes the device as
`context + 0x18C0` (`00624660`) and tail-jumps the command's slot 1 with it (`001F4A35`).

### The device

`00615840` builds the device inside the context: `006C8750(context + 0x18C0)` (`00615B57`) stores
the `PrimitiveRendererD3D11` vtable `00D86960` at `+0x00` and its second vtable `00D86AD0` at
`+0x08`. The first table has 45 slots (`006CA760` to `006CB540`, followed by the locator
`01D38180` at `00D86AC8`); the second has one slot, `006C88A0`.

The `Gi*` execute bodies call twenty of the slots:

| Offset | Body | What it does |
|---|---|---|
| `000` | `006CA760` | returns the vertex staging area `this + 0x10880 + 0x7FE0 × [this+0x18860]`, zeroes the index and keeps the pointer at `+0xB8` |
| `008` | `006CB5E0` | returns `+0xB8` |
| `020` | `006C8C50` | passes the draw to the batcher at `+0x880` (`006DA5A0`) |
| `+0x080`, `+0x088` | `0060D760` | `mov eax, 0x17; ret`: no effect |
| `+0x098`, `+0x0A0`, `+0x0A8`, `+0x0B0` | `006CAB40`, `006CABF0`, `006CAC00`, `006CABE0` | forward to the state object at `+0x208` |
| `128` | `006C9B00` | ends a scene (`006C9B20`, then `006C88B0`) |
| `130` | `006CA7B0` | begins a scene: resets the state bytes at `+0x208F0`, binds the target |
| `138` | `006C9AF0` | stores a byte at `+0x208F8` |

The others used are `+0x030`, `+0x038`, `+0x040`, `+0x048`, `+0x058`, `+0x078`, `+0x0D0` and
`+0x0D8`. The 0x7FE0-byte staging area holds 682 vertices of 0x30 bytes, the same batch size the
GS replay uses.

Every drawing command (`GiColorRect`, `GiNormal`, `GiPolyGT4T`, `GiPrim`, `GiScreenImage`,
`GiSprite`, `GiTrans`, `GiTransNz`) calls `+0x78`, then `+0x98`, then `+0x80`. Only `GiColorRect`,
`GiPolyGT4T`, `GiPrim`, `GiScreenImage` and `GiSprite` take the staging area through `+0x000`;
`GiTrans`, `GiTransNz`, `GiNormal` and `GiZNormalOnOff` only set state.

### Individual commands

- `GiSetTexture`'s execute `00863040` ignores the device and calls `00210570(id, pointer, dword)`
  with its `u16 +0x08`, `+0x10` and `+0x0C`. `00210570` stores `{pointer, dword}` in entry `id` of
  the 16-byte table `01F83580` when `id < 0x4000` as a signed compare, so ids `0x8000`–`0xFFFF`
  write below the table. The GS replay looks textures up in this table.
- `GiPolyGT4T`'s prepare `00864CA0` reads its `+0xF8`; when the id `& 0x3FFF` is `0xE00` it uses
  `0xDFF` while `02EC3ECC` is 0. It stores the record `002D7FA0(id)` returns (from the 0x30-byte
  table `0209E6B0`) at `+0xD0`, and the record `002D7EE0(+0xF8)` returns at `+0xD8` and its dword `+8` at `+0xE0`.
- `GiZNormalOnOff` (`00864D70`) calls `00210560` with 0 or `0x70000` by its `+0x08` and sets device
  state through `+0xA0`, `+0x88` and `+0xA8`.
- The reset commands' executes (`001F3210`, `001F3260`) never read the command: they call
  `00188730` (default target) or `001893C0` on the render manager, closing and reopening the
  context's bit-0 bracket (`00609710`, `00600A60(ctx, 3)`, `005FEFD0(ctx, 0)`) around it.

### Render blocks

The device's ring holds 0x80-byte blocks, `u32` opcode at `+0x00` and payload from `+0x08`.
`0060A410` handles opcodes `0x01`–`0x06` and `0x2F` itself (byte table `0060AAD8`, arm table
`0060AAB8`) and passes `0x07`–`0x2E` to `00607410` (`0060A9D4`), whose table `006078E4` gives 39
of them their own arm; `0x12` takes the table's exit.

Nine level-2 arms decode their payload and then call a body that does nothing: `0x1D`, `0x1E`,
`0x1F`, `0x25`, `0x27`, `0x28`, `0x29` and `0x2B` call `0060D760` (`mov eax, 0x17; ret`), and
`0x2E` calls `005C5230`. Opcode `0x25` is produced: `0060E810` writes it (`0060E8A8`) with a flag
byte at `+0x08` and floats at `+0x0C` and `+0x10`, called from the map draw `001E2AF0` (`001E3091`,
`001E3CD1`) and the character draw `001F5D70` (`001F5E9B`, `001F62CC`), and the arm `006076E9`
discards them.

Producers read for this page: `0x2F` `005FEA50`, `0x16` `005FEFD0`, `0x18` `00600A60`, `0x01` and
`0x02` `0060C020`, `0x03` `006007B0`, `0x25` `0060E810`. The full opcode table is
`gi-render-commands-render-block-opcode-isa.tsv`.

## Layouts

Command arena ([`01F7F4C0`]), `0x20` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | base | 32 MB block |
| `08` | `void*` | cursor |  |
| `10` | `void*` | end |  |
| `18` | `void*` | mark | `001A1460` sets, `001A14D0` rewinds to it |

Display-list record (`02F8F2F8` + `0x28` * i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | argument | passed to +`0x10` |
| `08` | `u32` | sort key | `003A3A50` compares this dword |
| `0C` | `u32` | appender count |  |
| `10` | `void*` | function | called with +`0x00` when non-null |
| `18` | `void*` | node | filed through `0020E630` when +`0x10` and +`0x00` are null |
| `20` | `u8` | flags | bit 0: `003A2BD0` first; bit 1: post-processing point; bit 2: defer to `02AEF420` |

Render block, `0x80` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | opcode | `0x01`-`0x2F` |
| `08` | `...` | payload | for `0x2F`: +`0x08` function, +`0x10` argument |

```
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
| the context's pass-state block `+0x0B50` | `gi-render-commands-render-context-pass-state-block-accesses.tsv` |
| the context's primitive-pass block `+0x07D8` | `gi-render-commands-render-primitive-pass-1e8-accesses.tsv` |

## State

| Address | What |
|---|---|
| `01F7F4C0` | the command arena |
| `01F7F4D0` | the filing handler (`GeometryRenderTargetImmediate`) |
| `02F8F2F8`, `02F8F2C6` | the display list and its count |
| `02CC0410` | the render context; the device at `02CC1CD0` |
| `01F83580` | the texture table `GiSetTexture` fills |

## Modding notes

- A hook on device slot `+0x000` sees the quads and primitives but not `GiTrans`, `GiTransNz`,
  `GiNormal` or `GiZNormalOnOff`; a hook on `+0x78` sees every drawing command.
- `GiSetTexture` never reaches the device, so texture binds are visible only at `00210570`.
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
