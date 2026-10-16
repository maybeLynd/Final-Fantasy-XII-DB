---
title: "Phyre frame: from the frame tick to the drawn picture, the draw-layer mask and the GS register stream"
kind: "system"
category: "PhyreEngine"
summary: "What the game's draw does once PhyreEngine's frame tick has handed over: the draw routine and its two draws per frame, the per-draw pass mask at 022C7F90 that switches each pass, the PS2 Graphics Synthesizer register batch every frame mode writes, the two 512-record command buffers it is written into and flipped, the menu viewport scaled from 512 x 448, and the camera state the GiBeginEff render command copies when it is prepared."
addresses: ["0022B0B0", "022C7F90", "00358450", "00358510", "0036D400", "003A1D50", "004FE420", "003A1DB0", "0036F360", "02EBEFC0", "00184460", "00864F30", "00864E90", "00678B50", "0016D6A0"]
---

# Phyre frame: from the frame tick to the drawn picture, the draw-layer mask and the GS register stream

## What the player sees

Each frame the world is drawn in named layers: the scene, ambient occlusion, water, post-processing, a
PS2-style depth of field, a Gaussian filter and the visual effects. Each layer has an on/off bit, and a
frame can draw the scene twice with different layers switched on.
Underneath, every frame mode still starts by writing PlayStation 2 Graphics Synthesizer register
settings into a command buffer.

## How it works

### Where the game takes over

PhyreEngine calls the game application's frame tick (slot 4) and render (slot 8); the pump, the seven
frame states and the simulation step are on [game application](../Engine-Core/game-application.md)
and [frame update order](../Engine-Core/frame-update-order.md). The framework side is on
[Phyre application](phyre-application.md). This page covers the draw the frame states call and what it
writes.

The frame bodies mark their phases by passing a label to `0016D6A0`, whose whole body is `ret`: for
example `"[PS2]main loop draw"` at the top of `0022B0B0`, and `PAD CONTROL`, `[PS2]draw`, `CAMERA`,
`FAST MODE`, `ATEL CONTROL` and `SCREEN CAPTURE` in the state handlers. The labels do nothing at run
time.

### The draw and its two passes per frame

`0022B0B0(draw, alternate)` is called three times: with (0, 0) at `0022A82D` and (1, 0) at `0022A8B8`
in the field frame `0022A770`, and with (0, 1) at `0022AF8A` in the screen-capture state. The field
frame runs draw 1 only when entry 1 of the pass mask is non-zero (`00358330(1)` at `0022A83B`); between
the two it waits on the command-state word, runs `00376470` and `00375500(7)` when draw 0's
bit 4 is set, and sets the mask's byte `+8` to 1 (`00358640`).

The draw opens a `mainLoopDraw` scope (`001EB150`) and returns at once when `01FD4A70` is set (clearing
it and setting `02064AE4`). While `02064AE4` is clear it writes the GS register batch (`0036D400`,
below), with both arguments forced to 1 in the alternate draw. It then runs these passes in order, each
behind one bit of its mask entry:

| Bit | Accessor | What it gates in `0022B0B0` |
|---|---|---|
| 0 | `00358380` | `003769E0`, `00377520`, `0036F410`; later `0036FBB0`, `0036F430`, `0036F450` and `00475390` |
| 1 | `003582A0` | `0017F2F0`, `0017F070`, `00332420(2)`; with bit 6, `00332420(3)` and `00332420(0)` |
| 2 | `00358350` | `00377230`; `00258EE0(4)` |
| 3 | `003583B0` | `00252A70`, and `002450B0` when `00357780()`, after the Gaussian filter (normal draw); inside the filter `0017FD70` runs only when bit 3 is clear or in the alternate draw |
| 4 | `003583F0` | `00258EE0` with 1, 2, 3, 5 and 6; `00375500` with 2, 3, 5 and 6; the `mask border 2` scope |
| 5 | `00358300` | the first argument of `0036D400` |
| 6 | `003582C0` | `00332420(1)`; with bit 1, `00332420(3)` and `00332420(0)` |
| 7 | `003582E0` | the second argument of `0036D400` |
| 8 | `003583D0` | a mid-draw block: `0036F2C0`, `00184900`, `0036F2F0` |

The named scopes, in order, are `mask border 0`; `AO render` (when `0017FE10()` and `01FD49E8`);
`Water effect` (when `0017FE20()` and `01FD49E8`, at one of two places); `post-processing render`
(at one of two places chosen by `00180040()`, at most once per draw through `02064AE0`, and in draw 1
only when bits `0x1`, `0x8` and `0x10` of `020926E4` are clear); `PS2 DOF`; `Gaussian Filter`; and
`mask border 2`. In draw 1, `01FD49E8` is 0 unless bit 0 is set, which removes AO, water and
post-processing from the second draw.

### The pass mask

`022C7F90` holds one dword per draw: the low `u16` is the pass bits read above, the high `u16` a second
set of flags. Bytes follow at `022C7F98` (`+8`), `022C7F99` (`+9`) and `022C7F9A` (`+0xA`, the speed
permit byte of [frame update order](../Engine-Core/frame-update-order.md)).

`00358450(draw, on)`
sets bits 0–7 of that draw's pass bits to `on`, clears bit 8 and sets bits 0–3 of its upper word. The
reset `00358510` (called from `0022A0B0`) runs it with on for draw 0 and off for draw 1, then stores
0, 0 and 1 at `+8`, `+9` and `+0xA`. The other writers, their 105 call sites and the values they store
are listed in [the-frame-drawmask-callers.tsv](the-frame-drawmask-callers.tsv).

### The GS register batch

`0036D400(a, b)` is called by the draw and by the state handlers `0022B6E0`, `0022B7E0`, `0022B8C0`,
`0022BC20` and `0022B000`. It writes one A+D GIF packet of PS2 Graphics Synthesizer register
settings sized from the width `022D8EAC` and height `022D8EB4`: FRAME_1, ZBUF_1, XYOFFSET_1,
SCISSOR_1, PRMODECONT, COLCLAMP and DTHE, a screen clear when the value its two arguments select
from the table `00D10F88` is non-zero, and a closing TEST_1. It then flips the command buffers
through `003A1DB0`.

The packet and the hand-off are on
the shared command-state word;
the GIF tag format and the GS replay are on
[PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md).

### The two command buffers

`003A1D50` (called from `0036F4D0`) sets up the two 24-byte buffer records `02EBEFC0` and `02EBEFD8`
through `004FE420`, each with 512 (`0x200`) 16-byte records in the arena at `[01FD4A78]`; `02EBEFF0`
is the index of the buffer being filled. `003A1DB0` flips the index and hands the old buffer's start
and record count to `0036F360`.

`0036F360` does nothing for an empty buffer. Otherwise, when the last record's first dword has bits
`0x70000000` equal to `0x30000000`, it writes the record `{0x10000000, 0}` after it (over it when the
buffer is full). It then stores the buffer address & `0x3FF0` (`0036F3A6`) and the record count
(`0036F3AC`) into the command-state word `02EBA3F8`, reloads that word three times per pass of a
compare loop (`0036F3B2`-`0036F3E9`), and stores `0x100` to it (`0036F3EB`).

The buffers are on
the ordered render command list,
the word on
the shared command-state word.

### The menu viewport

`00184460(x, y, w, h, flag)` maps a rectangle from a reference size (512 × 448, or 1920 × 1080 when
`001B1620()` holds) to the device: y and height scale by device height / reference height; x and
width by device width / reference width, or, when `001DD8C0` reports aspect correction, by device
height × aspect (from `001DD110`, default 1.7777778) / reference width with x centred. It passes the
result to `001B23E0` and `001E9F00`. The full-menu state `0022B8C0` calls it with `[01E0C1D8]` and
`[01E0C1DC]`, which hold `0x200` and `0x1C0`.

### The camera snapshot

`00864F30` is slot 0 (prepare) of the `GiBeginEff` render command (vtable `01CCFB78`, `0x90`
bytes). It copies:

- 64 bytes from `02AEEB20` (returned by `0039D1D0`) to `+0x08`;
- the 64-byte projection matrix at `+0x30` of the camera object from `00186670` on the render manager (adjusted by `+8` when
non-null, then read without a null check) to `+0x48`;
- the floats `02AEEBA0` and `02AEEBA4` to `+0x88` and `+0x8C`.

`00678B50` then rewrites two entries of the copied matrix from the camera's near
(`+0xB8`) and far (`+0xBC`): with element `+0x3C` non-zero, `+0x28 = 1 / (n − f)` and
`+0x38 = n / (n − f)`; otherwise `+0x28 = f / (n − f)` and `+0x38 = n·f / (n − f)`.

Slot 1 (execute, `00864E90`) hands `+0x08` and the two floats to `00210520`, which stores them at
`01FD3620`–`01FD365F`, `01FD3660` and `01FD3664` (the GS replay's vertex matrix and depth bounds),
passes `+0x48` to the device's slot `+0x30`, and sets two device values to 3.0.

## Layouts

```
command buffer record (02EBEFC0, 02EBEFD8), 0x18 bytes
+0x00  ptr   begin
+0x08  ptr   write      advanced by 0x10 per record
+0x10  u32   capacity   0x200 records
+0x14  u32   ready      set by 004FE420
```

```
command record, 0x10 bytes
+0x00  u64   value      register data
+0x08  u64   register   GS register number
```

```
pass mask (022C7F90)
+0x00  u16   draw 0 pass bits
+0x02  u16   draw 0 upper flags
+0x04  u16   draw 1 pass bits
+0x06  u16   draw 1 upper flags
+0x08  u8    current draw byte (00358640)
+0x09  u8    capture byte
+0x0A  u8    speed permit byte
```

```
GiBeginEff render command, 0x90 bytes
+0x00  ptr     vtable    01CCFB78
+0x08  f32[16] block     from 02AEEB20
+0x48  f32[16] projection  camera +0x30, depth terms rewritten by 00678B50
+0x88  f32     near bound  02AEEBA0
+0x8C  f32     far bound   02AEEBA4
```

Instruction-level access tables beside this page:

| Subject | Table |
|---|---|
| the two command buffer records | [the-frame-render-command-buffer-pair-accesses.tsv](the-frame-render-command-buffer-pair-accesses.tsv) |
| a command buffer record | [the-frame-render-command-buffer-accesses.tsv](the-frame-render-command-buffer-accesses.tsv) |
| the 64 records of `0x60` bytes at `02B404E0` | [the-frame-handle-slot-record-accesses.tsv](the-frame-handle-slot-record-accesses.tsv) |
| pass mask writers | [the-frame-drawmask-callers.tsv](the-frame-drawmask-callers.tsv) |
| `PCameraOrthographic` | [the-frame-pcamera-orthographic-accesses.tsv](the-frame-pcamera-orthographic-accesses.tsv) |
| `PCameraProjection` | [the-frame-pcamera-projection-accesses.tsv](the-frame-pcamera-projection-accesses.tsv) |

## State

| Address | What |
|---|---|
| `022C7F90` | the pass mask, two draws and three bytes |
| `02EBEFC0`, `02EBEFD8` | the two command buffer records |
| `02EBEFF0` | index of the buffer `0036D400` fills |
| `01FD4A78` | the arena both buffers point into |
| `02EBA3F8` | the command-state word `0036F360` writes |
| `02064AE0` | post-processing already drawn in this draw |
| `01E0C1D8`, `01E0C1DC` | the menu viewport size, 512 and 448 |

## Modding notes

- Clearing a bit of `022C7F90` for a draw removes that pass from the next draw; bit 4 removes every
  `00258EE0` and `00375500` call. The routines in the callers table rewrite the mask, so a change can
  be overwritten.
- A non-zero draw-1 entry makes the field frame draw twice.
- The 512-record capacity appears twice: in `003A1D50` and in `0036F360`'s full-buffer test.
- The menu viewport is given in 512 × 448 coordinates; a changed reference size must match `01E0C1D8`.

## Related

- [Game application](../Engine-Core/game-application.md): slots 4 and 8, the pump.
- [Frame update order](../Engine-Core/frame-update-order.md): the frame states and the simulation step.
- [PS2 VIF1 and VU1 emulation](../Engine-Core/ps2-vif1-vu1-emulation.md): the GIF tag and the GS replay.
- [Phyre application](phyre-application.md): PhyreEngine's application class.
- [Phyre post-effect classes](phyre-post-effect-classes.md): PhyreEngine's post-effect library.
