---
title: "Phyre frame: from the frame tick to the drawn picture, the per-draw mask and the GS register batch"
kind: "system"
category: "PhyreEngine"
addresses: "0x0022B0B0, 0x022C7F90, 0x00358450, 0x00358510, 0x0036D400, 0x003A1D50, 0x004FE420, 0x003A1DB0, 0x0036F360, 0x02EBEFC0, 0x00184460, 0x00864F30, 0x00864E90, 0x00678B50, 0x0016D6A0"
---

## What the player sees

Each frame the world is drawn in named layers: the scene, ambient occlusion, water, post-processing, a
PS2-style depth of field, a Gaussian filter and the visual effects. Each layer has an on/off bit, and a
frame can draw the scene twice with different layers switched on.
Underneath, every frame mode still starts by writing PlayStation 2 Graphics Synthesizer register
settings into a command buffer.

The game writes into one of two command lists of 512 records each while the other is handed on. At each flip the
finished list's place and length go into a shared command word, and the other list starts again from its beginning as
the list the game now writes into.

## How it works

### Where the game takes over

PhyreEngine calls the game application's frame tick (slot 4) and render (slot 8); the pump, the seven
frame states and the simulation step are on [game application](../Engine-Core/game-application.md)
and [frame update order](../Engine-Core/frame-update-order.md). The framework side is on
[Phyre application](phyre-application.md). This page covers the draw the frame states call and what it
writes.

The frame bodies mark their phases by passing a label to `0x0016D6A0`, whose whole body is `ret`: for
example `"[PS2]main loop draw"` at the top of `0x0022B0B0`, and `PAD CONTROL`, `[PS2]draw`, `CAMERA`,
`FAST MODE`, `ATEL CONTROL` and `SCREEN CAPTURE` in the state handlers. The labels do nothing at run
time.

### The draw and its two passes per frame

`0x0022B0B0(draw, alternate)` is called three times: with (0, 0) at `0x0022A82D` and (1, 0) at `0x0022A8B8`
in the field frame `0x0022A770`, and with (0, 1) at `0x0022AF8A` in the screen-capture state. The field
frame runs draw 1 only when entry 1 of the pass mask is non-zero (`0x00358330(1)` at `0x0022A83B`); between
the two it waits on the command-state word, runs `0x00376470` and `0x00375500(7)` when draw 0's
bit `0x10` is set, and sets the mask's byte `+8` to 1 (`0x00358640`).

The draw opens a `mainLoopDraw` scope (`0x001EB150`) and returns at once when `0x01FD4A70` is set (clearing
it and setting `0x02064AE4`). While `0x02064AE4` is clear it writes the GS register batch (`0x0036D400`,
below), with both arguments forced to 1 in the alternate draw. It then runs these passes in order, each
behind one bit of its mask entry. `0x00332420(3)` runs first when bit `0x40` or bit `0x2` is set, then the bit `0x4`
pass (`0x00377230`) and the bit `0x1` pass, then `0x00332420(0)` when bit `0x40` or bit `0x2` is set:

| Bit | Accessor | What it gates in `0x0022B0B0` |
|---|---|---|
| `0x1` | `0x00358380` | `0x003769E0`, `0x00377520`, `0x0036F410`; later `0x0036FBB0`, `0x0036F430`, `0x0036F450` and `0x00475390` |
| `0x2` | `0x003582A0` | `0x0017F2F0`, `0x0017F070`, `0x00332420(2)`; this bit or bit `0x40`: `0x00332420(3)` and `0x00332420(0)` |
| `0x4` | `0x00358350` | `0x00377230`; `0x00258EE0(4)` |
| `0x8` | `0x003583B0` | `0x00252A70`, and `0x002450B0` when `0x00357780()`, after the Gaussian filter (normal draw); inside the filter `0x0017FD70` runs only when bit `0x8` is clear or in the alternate draw |
| `0x10` | `0x003583F0` | `0x00258EE0` with 1, 2, 3, 5 and 6; `0x00375500` with 2, 3, 5 and 6; the `mask border 2` scope |
| `0x20` | `0x00358300` | the first argument of `0x0036D400` |
| `0x40` | `0x003582C0` | `0x00332420(1)`; this bit or bit `0x2`: `0x00332420(3)` and `0x00332420(0)` |
| `0x80` | `0x003582E0` | the second argument of `0x0036D400` |
| `0x100` | `0x003583D0` | a mid-draw block: `0x0036F2C0`, `0x00184900`, `0x0036F2F0` |

The named scopes, in order, are `mask border 0`; `AO render` (when `0x0017FE10()` and `0x01FD49E8`);
`Water effect` (when `0x0017FE20()` and `0x01FD49E8`, at one of two places); `post-processing render`
(at one of two places chosen by `0x00180040()`, at most once per draw through `0x02064AE0`, and in draw 1
only when bits `0x1`, `0x8` and `0x10` of `0x020926E4` are clear); `PS2 DOF`; `Gaussian Filter`; and
`mask border 2`. In draw 1, `0x01FD49E8` is 0 unless bit `0x1` is set, which removes AO, water and
post-processing from the second draw.

The draw stores its first argument, the draw index, at `0x01FD4A6C` (`0x0022B0DF`). Each `post-processing render` scope
passes that word to `0x00182970` (`0x0022B4F1`, `0x0022B55D`, the two places), which hands it with the object `0x0018CA40`
returns to `0x0018C610`. `0x003A3740` (from `0x0024D540`, `0x00259030` and `0x002590F0`) opens the same scope and passes the
word the same way (`0x003A3851`).

### The pass mask

`0x022C7F90` holds one dword per draw: the low `u16` is the pass bits read above, the high `u16` a second
set of flags. Bytes follow at `0x022C7F98` (`+8`), `0x022C7F99` (`+9`) and `0x022C7F9A` (`+0xA`, the speed
permit byte of [frame update order](../Engine-Core/frame-update-order.md)).

`0x00358450(draw, on)`
sets the bits under mask `0xFF` of that draw's pass bits to `on`, clears bit `0x100` and sets bits `0xF` of its upper word. The
reset `0x00358510` (called from `0x0022A0B0`) runs it with on for draw 0 and off for draw 1, then stores
0, 0 and 1 at `+8`, `+9` and `+0xA`. The other writers, their 105 call sites and the values they store
are listed in [the-frame-drawmask-callers.tsv](the-frame-drawmask-callers.tsv).

### The GS register batch

`0x0036D400(a, b)` is called by the draw and by the state handlers `0x0022B6E0`, `0x0022B7E0`, `0x0022B8C0`,
`0x0022BC20` and `0x0022B000`. It writes one A+D GIF packet of PS2 Graphics Synthesizer register
settings sized from the width `0x022D8EAC` and height `0x022D8EB4`: FRAME_1, ZBUF_1, XYOFFSET_1,
SCISSOR_1, PRMODECONT, COLCLAMP and DTHE, a screen clear when the value its two arguments select
from the table `0x00D10F88` is non-zero, and a closing TEST_1. It then flips the command buffers
through `0x003A1DB0`.

The packet and the hand-off are on
[the shared command-state word](../Graphics/graphics-thread-handshake.md);
the GIF tag format and the GS replay are on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md).

### The two command buffers

`0x003A1D50` (called from `0x0036F4D0`) sets up the two 24-byte buffer records `0x02EBEFC0` and `0x02EBEFD8`
through `0x004FE420`, each with 512 (`0x200`) 16-byte records in the arena at `[0x01FD4A78]`; `0x02EBEFF0`
is the index of the buffer being filled. It first zeroes both records (`0x004FE3C0`, `0x003A1D5B`, `0x003A1D67`)
and the index (`0x003A1D6F`); the first record starts at arena record 0 (`0x003A1D85`) and the second at
record `0x200`, through its tail jump (`0x003A1D9D`).

`0x004FE420(record, count, offset)` first releases the record's block through `0x003EC8A0` while its `+0x14` is 0
(`0x004FE42F`-`0x004FE43E`); `0x003EC8A0` frees `+0x00` with `0x003697F0` when it is set and zeroes it. It then sets
`+0x14` to 1 and zeroes `+0x00`, `+0x08` and `+0x10` (`0x004FE446`-`0x004FE454`), and a count of 0 leaves the
record so (`0x004FE45B`).

With a non-zero count `0x004FE420` points `+0x00` and `+0x08` at `[0x01FD4A78] + offset * 16` and stores the
count at `+0x10` (`0x004FE463`-`0x004FE485`). When `offset << 5` is above `0x80000` in an unsigned compare, which
includes every negative offset, it first writes 0 to address 0 (`0x004FE46E`-`0x004FE47E`), a deliberate fault.

`0x003A1DB0` flips the index and hands the old buffer's start and record count to `0x0036F360`.
The new index is `1 - old` (`0x003A1DC3`-`0x003A1DCA`) and the count is `(write - begin) >> 4` (`0x003A1DEB`).
After that call it sets the new buffer's write cursor back to its begin and returns that record
(`0x003A1DF4`-`0x003A1DFA`).

`0x0036F360` does nothing for an empty buffer. Otherwise, when the last record's first dword has bits
`0x70000000` equal to `0x30000000`, it writes the record `{0x10000000, 0}` after it (over it when the
buffer is full, `0x200` records or more in a signed compare, `0x0036F386`). It then stores the buffer address
& `0x3FF0` (`0x0036F3A6`) and the record count, one more when the record went after the last one (`0x0036F391`),
(`0x0036F3AC`) into the command-state word `0x02EBA3F8`, reloads that word three times per pass of a
compare loop (`0x0036F3B2`-`0x0036F3E9`), and stores `0x100` to it (`0x0036F3EB`).

The buffers are on
[the ordered render command list](../Graphics/render-command-list.md),
the word on
[the shared command-state word](../Graphics/graphics-thread-handshake.md).

### The menu viewport

`0x00184460(x, y, w, h, flag)` maps a rectangle from a reference size (512 × 448, or 1920 × 1080 when
`0x001B1620()` holds) to the device, with `W` and `H` the device width and height and signed integer division:

- y and height scale by device height / reference height, `y = H * y / refH` (`0x001844C6`-`0x001844D7`);
- x and width by device width / reference width, `x = W * x / refW` (`0x0018457B`-`0x00184590`);
- or, when `0x001DD8C0` reports aspect correction, by device height × aspect (from `0x001DD110`, default 1.7777778)
  over the reference width, `x = (int)(H * x * aspect / refW)` (`0x0018451D`-`0x00184575`);
- in that case with x centred, `x = (int)((W - H * aspect) * 0.5 + x)` (`0x001845C5`-`0x001845EF`).

It passes the result and `flag` to `0x001B23E0` (`0x00184613`), and the result and `flag != 0` to `0x001E9F00`
(`0x00184636`). The full-menu state `0x0022B8C0` calls it with `[0x01E0C1D8]` and `[0x01E0C1DC]`, which hold `0x200` and
`0x1C0`.

### The camera snapshot

`0x00864F30` is slot 0 (prepare) of the `GiBeginEff` render command (vtable `0x01CCFB78`, `0x90`
bytes). It copies:

- 64 bytes from `0x02AEEB20` (returned by `0x0039D1D0`) to `+0x08`;
- the 64-byte projection matrix at `+0x30` of the camera object from `0x00186670` on the render manager (adjusted by `+8` when
non-null, then read without a null check) to `+0x48`;
- the floats `0x02AEEBA0` and `0x02AEEBA4` to `+0x88` and `+0x8C`.

`0x00678B50` then rewrites two entries of the copied matrix from the camera's near
(`+0xB8`) and far (`+0xBC`): with element `+0x3C` non-zero, `+0x28 = 1 / (n − f)` and
`+0x38 = n / (n − f)`; otherwise `+0x28 = f / (n − f)` and `+0x38 = n·f / (n − f)`.

Slot 1 (execute, `0x00864E90`) first calls the device's slot `+0xB0` with 0 (`0x00864EB5`) and stores `0x80` in
`0x01E027B8` (`0x002105A0`, `0x00864EBD`), then hands `+0x08` and the two floats to `0x00210520`, which stores them at
`0x01FD3620`–`0x01FD365F` (rows `0x01FD3620`, `0x01FD3630`, `0x01FD3640` and `0x01FD3650`), `0x01FD3660` and `0x01FD3664`
(the GS replay's vertex matrix and depth bounds),
passes `+0x48` to the device's slot `+0x30`, sets two device values to 3.0 (slots `+0xD8` and `+0xD0`), and
ends by tail-jumping to the device's slot `+0x138` with 0 (`0x00864F22`).

## Layouts

Command buffer record (`0x02EBEFC0`, `0x02EBEFD8`), `0x18` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | begin |  |
| `+0x08` | `void*` | write | advanced by `0x10` per record |
| `+0x10` | `u32` | capacity | `0x200` records |
| `+0x14` | `u32` | ready | set to 1 by `0x004FE420`, which frees `+0x00` first while it is 0 (`0x003EC8A0`) |

Command record, `0x10` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | value | register data |
| `+0x08` | `u64` | register | GS register number |

Pass mask (`0x022C7F90`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | draw 0 pass bits |
| `+0x02` | `u16` |  | draw 0 upper flags |
| `+0x04` | `u16` |  | draw 1 pass bits |
| `+0x06` | `u16` |  | draw 1 upper flags |
| `+0x08` | `u8` |  | current draw byte (`0x00358640`) |
| `+0x09` | `u8` |  | capture byte |
| `+0x0A` | `u8` |  | speed permit byte |

GiBeginEff render command, `0x90` bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | vtable | `0x01CCFB78` |
| `+0x08` | `f32[16]` | block | from `0x02AEEB20` |
| `+0x48` | `f32[16]` | projection | camera `+0x30`, depth terms rewritten by `0x00678B50` |
| `+0x88` | `f32` | near bound | `0x02AEEBA0` |
| `+0x8C` | `f32` | far bound | `0x02AEEBA4` |

Instruction-level access tables beside this page:

| Subject | Table |
|---|---|
| the two command buffer records | [the-frame-render-command-buffer-pair-accesses.tsv](the-frame-render-command-buffer-pair-accesses.tsv) |
| a command buffer record | [the-frame-render-command-buffer-accesses.tsv](the-frame-render-command-buffer-accesses.tsv) |
| the 64 records of `0x60` bytes at `0x02B404E0` | [the-frame-handle-slot-record-accesses.tsv](the-frame-handle-slot-record-accesses.tsv) |
| pass mask writers | [the-frame-drawmask-callers.tsv](the-frame-drawmask-callers.tsv) |
| `PCameraOrthographic` | [the-frame-pcamera-orthographic-accesses.tsv](the-frame-pcamera-orthographic-accesses.tsv) |
| `PCameraProjection` | [the-frame-pcamera-projection-accesses.tsv](the-frame-pcamera-projection-accesses.tsv) |

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PCameraOrthographic` (`0xD8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0xD4` | `u8[4]` | bytesD4 | the bytes after m_height (`+0xD0`) up to the end of the `0xD8`-byte class; no registered member covers it (`0x006ACFF0` registers the `0xD8`-byte class at `0x006AD03A`) |

## State

| Address | What |
|---|---|
| `0x022C7F90` | the pass mask, two draws and three bytes |
| `0x02EBEFC0`, `0x02EBEFD8` | the two command buffer records |
| `0x02EBEFF0` | index of the buffer `0x0036D400` fills |
| `0x01FD4A78` | the arena both buffers point into |
| `0x02EBA3F8` | the command-state word `0x0036F360` writes |
| `0x02064AE0` | post-processing already drawn in this draw |
| `0x01E0C1D8`, `0x01E0C1DC` | the menu viewport size, 512 and 448 |

## Modding notes

- Clearing a bit of `0x022C7F90` for a draw removes that pass from the next draw; bit `0x10` removes the
  `0x00258EE0` calls with 1, 2, 3, 5 and 6 and the `0x00375500` calls with 2, 3, 5 and 6; `0x00258EE0(4)` follows
  bit `0x4`. The routines in the callers table rewrite the mask, so a change can
  be overwritten.
- A non-zero draw-1 entry makes the field frame draw twice.
- The 512-record capacity appears twice: in `0x003A1D50` and in `0x0036F360`'s full-buffer test.
- The menu viewport is given in 512 × 448 coordinates; a changed reference size must match `0x01E0C1D8`.

## Related

- [Game application](../Engine-Core/game-application.md): slots 4 and 8, the pump.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states and the simulation step.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the GIF tag and the GS replay.
- [Phyre application](phyre-application.md): PhyreEngine's application class.
- [Phyre post-effect classes](phyre-post-effect-classes.md): PhyreEngine's post-effect library.
