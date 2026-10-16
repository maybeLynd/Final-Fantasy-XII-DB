---
title: "PS2 VIF1 and VU1 emulation: the packet decoder, the recompiled microprograms and the GS replay"
kind: "system"
category: "Engine core"
summary: "The second PlayStation 2 layer the remaster keeps: a VIF1 command decoder at 0022C970 over a 16 KB emulated VU1 memory, 57 vector-unit microprograms recompiled to x64 and installed by MPG as function pointers, the 77 packet templates two boot hubs build and the registrars that build packets per draw, the GiVmax render command that runs a packet at emit time and collects its GS output, and the GS replay that turns GIF packets into D3D11 vertices and indices for twenty honoured GS registers."
addresses: "0022C970, 0022C940, 0022BFF0, 0022C8D0, 0022C930, 0022CC40, 0022CC30, 0037DF90, 0037E0F0, 008631E0, 008631D0, 001DB840, 001DB550, 001DB660, 001DB3D0, 001FB840, 001DB7E0, 003A34D0, 003A35E0, 003A33B0, 003A2F70, 0020E630, 0020F310, 00210320, 0020F3E0, 0020FCA0, 00210230, 0020EA50, 0020FE70, 0020FBA0, 0020EC80, 0020EB60, 0020F250, 004EF860, 00476C80"
---

## What the player sees

Particle effects, weapon trails and the other PlayStation 2 era effect drawing look as they did on
the console. On the PlayStation 2 that drawing was fed to the second vector unit, VU1, as command
packets for its interface, VIF1, and the unit's microprograms wrote primitives for the Graphics
Synthesizer.

The remaster keeps the packets and the programs: a decoder reads the same command words, the
microprograms run as translated x64 functions over an emulated VU memory, and the primitives they
emit are replayed through a translator that understands twenty of the GS registers and ignores
the rest.

## How it works

### The decoder

`0022C940(packet, bytes, callback, context, flag)` passes the VU memory base `02064E30` to
`0022C970`, which walks the packet one 32-bit word at a time and switches on the top byte. The
cases are VIF1 commands with VIF1's field layout:

| Code | VIF1 command | What `0022C970` does |
|---|---|---|
| `0x01` | STCYCL | low byte to CYCLE `02088E40`, next byte to WL `02088E3C` |
| `0x02` | OFFSET | `data & 0x3FF` to `02088E34`, clears bit 6 of the status word `02088E38`, copies BASE to TOPS `02064E28` |
| `0x03` | BASE | `data & 0x3FF` to `02088E30` |
| `0x14`, `0x15` | MSCAL, MSCALF | runs `0022C8D0`, then the program installed at the largest address not above the requested one |
| `0x4A` | MPG | the next 8 bytes are an x64 function pointer, stored at `02068E30 + imm16 × 8`; the address is appended to the list `02088E50` (count `02088E44`) |
| `0x50`, `0x51` | DIRECT, DIRECTHL | calls the callback with the data pointer, the context and the flag, then skips `count × 16` bytes |
| `0x60` to `0x7F` | UNPACK | `0022BFF0` with the format from bits 24 to 27, the unsigned flag bit 14, the add-TOPS flag bit 15, NUM from bits 16 to 23 and the address from the low ten bits; the mask flag bit 28 has no effect |
| anything else | NOP, FLUSH, FLUSHE, FLUSHA, STMASK, STROW … | advances four bytes |

On the console MPG uploads microcode. Here it uploads a pointer to a function that already is
that microcode, compiled, and MSCAL calls it with the callback and context as arguments. The MPG
address is stored unmasked; the table holds 16,384 entries up to `02088E30`, so an address of
`0x4000` or more would overrun into the VIF registers, and every shipped packet uses address 0.

The code tests are looser than the names: UNPACK is any code with bits 5 and 6 set (so `0xE0` to
`0xFF`, the interrupt forms, decode as UNPACK too), DIRECT is `code - 0x50 < 2` and MSCAL
`code - 0x14 < 2`, so MSCNT (`0x17`) takes the four-byte default.

`0022C8D0` is the double-buffer step the console does on MSCAL: it copies TOPS into TOP
`02064E1C`, then sets TOPS to BASE and clears status bit 6 if that bit was set, or to
BASE + OFFSET and sets the bit otherwise. `0022C930` zeroes the installed count; `001DB550` calls
it before every packet list, so programs live only for the list that installed them.

### VU memory and the unit's state

| Address | Size | Role |
|---|---|---|
| `02064E30` to `02068E2F` | `0x4000` | VU memory, 1,024 cells of 16 bytes |
| `02068E30` to `02088E2F` | `0x20000` | the installed-program table, one x64 pointer per VU address |
| `02088E30` to `02088E53` | — | BASE, OFFSET, status, WL, CYCLE, installed count, installed list |
| `02064E1C`, `02064E28` | 4 each | TOP and TOPS |
| `02064B00` to `02064E2F` | — | the microprograms' own working words: 16-bit cell indices (`02064B0C`, `02064DB0`, `02064DB4`, `02064DB8`, `02064DD0`) and float scratch |
| `02064DEC` | u16 | the sticky status flags: `0022CC40` sets `0x40` (zero) and `0022CC30` sets `0x80` (sign); they are its only writers, and 40 microprograms call them at 116 sites each |

The boot routine `0022CB90` zeroes the VU memory, TOP, TOPS, the status word and the words
`02088E30` to `02088E38`, and `0017D6E0` runs it again on every restart pass
([PS2 CPU emulation](ps2-cpu-emulation.md)).

### UNPACK

`0022BFF0(vuMem, vn, vl, unsigned, addTops, num, addr, data)` writes `num` elements into VU
cells starting at `addr`, plus TOPS when the flag is set, with WL elements per cycle and CYCLE
cells between cycle starts. It returns 0 without writing when CYCLE is below WL.

The thirteen formats are `vn` = S, V2, V3, V4 by `vl` = 32, 16, 8, with V4-5 as the last:

- S broadcasts one value to all four lanes; V2 writes x and y and leaves z and w; V3 writes
  three lanes; V4 four;
- V4-5 expands a 16-bit colour as `r = (v & 0x1F) << 3`, `g = (v >> 2) & 0xF8`,
  `b = (v >> 7) & 0xF8`, `a = (v >> 8) & 0x80`;
- the 16- and 8-bit formats sign-extend unless the unsigned flag is set;
- the return value is the packed size rounded up to whole 32-bit words,
  `((32 >> vl) × (vn + 1) × num + 31) / 32 × 4`, which the decoder adds to its cursor.

Two arms read their source at the wrong stride: V2-32 advances four bytes per element against a
packed eight, and V4-5 advances eight against a packed two. Every packet the game builds is
V4-32, so neither arm runs on shipped content.

### Microprograms and the three ways a packet is built

A microprogram is an x64 function that reads and writes VU memory through the 16-bit index words
above and hands each finished GS packet to the callback. `004EF860` is the leaf most of them end
in: it writes `word[02064DB8] + 0x8000` into the cell at `02064DB0`, copies twelve bytes of the
cell at `02064DD0` beside it (staged at `02064C60`), sets `02064DB4` to `02064B0C + 0x2A8`, or
`+ 0x168` when `02064B0C` differs from `02064DB0 - 0x168`, calls the callback with the cell's
address, then sets `02064DB0` to `02064B0C + 02064DB4` and `02064DB4` one past it.

The image installs 57 distinct programs at 141 call sites ([ps2-vif1-vu1-emulation-programs.tsv]
(ps2-vif1-vu1-emulation-programs.tsv), resolved from the `lea` that loads each site's program
argument). Three routes build the packets that carry them:

- **77 boot templates.** `0037DF90` makes 28 calls and `0037E0F0` 49, each `lea rcx, object;
  call builder` with a distinct zero-initialised object at `02ADEF40` to `02AED330` (76 distinct
  builders; `004E3110` is called twice). A builder fills its packet with immediate stores.
- **Template contents.** The decoded command streams are in
  [ps2-vif1-vu1-emulation-templates.tsv](ps2-vif1-vu1-emulation-templates.tsv) and the GIF tags
  they carry in [ps2-vif1-vu1-emulation-gif-tags.tsv](ps2-vif1-vu1-emulation-gif-tags.tsv).
- **Template headers.** 37 builders start with `008631E0(object, program, 0)`, which stamps kind
  `0x30` at `+3`, appends `{0x4A000000 | addr, program}` to the record table `02EAF930` (count
  `02EB37B0`) and stores the record's handle at `+4`; `008631D0(object, count)` stamps the plain
  kind `0x10` header. The templates install 35 programs.
- **Per-draw registrars.** `003A34D0` (45 sites) and `003A33B0` (22) append a `0x28`-byte record
  to the sorted draw list `[02F8F2F8]` (count `02F8F2C6`) and hold the command for a later
  submit; `003A35E0` (27) and `003A2F70` (10) submit it at once through `0020E630(node, 2)`. All
  four build through `001DB840` and together install 44 programs, 22 of them shared with the
  templates.
- **Effect elements.** `001DB7E0` (callers `00540DB0`, `00540C70`, the finalisers every effect
  element type reaches) constructs the same command with no packets, and the element appends its
  own packet, which carries its own MPG.

`00476C80` is a template read end to end: `008631E0` with program `004758E0`, BASE 0 and OFFSET 0
(`0x03000000`, `0x02000000`), a sub-header, STCYCL 4,4 (`0x01000404`), UNPACK V4-32 of 66
quadwords (`0x6C420000`) whose payload starts with the GS screen centre 2048.0 (`0x45000000`)
and holds, four times, a vertex block and an A+D GIF tag (NLOOP 5, NREG 1, REGS `0xE`) writing
CLAMP_1, TEX0_1, ALPHA_1 and TEST_1 to 0 and PRIM to `0x5D`; then the register pairs ST, CLAMP_1,
RGBAQ, XYZF2 = 0, MSCALF 0 (`0x15000000` at `+0x440`) and FLUSHA (`0x13000000` at `+0x444`).

### The GiVmax render command

`001DB840(node, word1, word2, program, payload, size, payload2, size2, flag, ctx)` allocates the
`0x640`-byte `GiVmax` command (RTTI `.?AVGiVmax@@`, vtable `009007E8`) and fills its chunk list
with pointer and length pairs: `01F82D08` for 8 bytes (the two VIF words, rewritten there on
every call), `01DFD038` for 16 bytes (the image constant `0x4A000000`, MPG, with the program
pointer stored at `01DFD040`), then the payloads through `001DB340`. Both scratch chunks are
image-wide and `001DB840` is their only writer, so the packet must be consumed inside the call.

It is: `001DB840` ends by calling `001FB840(node)`, which tail-jumps the command's vtable slot 0,
`001DB550`. That runs the packet list at emit time: it zeroes the two output counts, stores the
flag `02EC3ECC == 0` at `+0x639`, resets the installed count, and calls `0022C940` once per chunk
with the callback `001DB640`.

The callback's body `001DB660` sizes the GS output with `0020F310`,
copies it into a buffer from the allocator at `01F82D00`, and appends the pointer to the paged
list at `+0x228` (count `+0x224`, page size `+0x220` = 1,024) and the callback's flag byte to the
list at `+0x430` (count `+0x42C`, page size `+0x428` = 1,024). The constructor `001DB220` sets all
three page sizes to 1,024 and allocates the first page of each list (`0x4000`, `0x2000` and
`0x400` bytes).

Slot 1, `001DB3D0`, replays later, when the frame's render pass list drains the command: device
slot `+0x58` with the bytes `+0x630` and `+0x634`, `00210510` and `00210560(0x51001)` when `+8` is
set, `002105B0(+0x638)`, `002104D0(+0x639)`, then `00210320(copy, device, flag)` for every
collected copy, then `002104E0`, `002105B0(0)` and the device slot `+0x58` again with (0, 0.1).

### GIF packets and the GS replay

`0020F310` sizes a GIF packet by walking its tags: NLOOP is bits 0 to 14, EOP bit 15 ends the
walk, FLG bits 58 to 59 and NREG bits 60 to 63 (0 means 16). PACKED tags are
`(NREG × NLOOP + 1) × 16` bytes, REGLIST `NREG × NLOOP` rounded up to even, times 8, plus 16, and
IMAGE `(NLOOP + 1) × 16`. The gate byte `01E027C0` is 1 in the image and has no writer, so the
sizing and the replay always run.

`00210320` walks the same tags for the replay. It stores the device at `01FC35F8` and the flag at
`01FD3611`, and for each tag with NLOOP above 0 reads PRE (bit 46), PRIM (bits 47 to 57), FLG and
NREG, and resets Q (`01E027B0`) to 1.0. A PACKED tag flushes the batch and applies PRIM through `0020FE70` when PRE is set, then
runs `0020F3E0`. A REGLIST tag with NLOOP above 0 ends the walk through the flush. An IMAGE tag
skips `NLOOP × 16` bytes. EOP ends the walk, and a final `0020EC80` flushes.

`0020F3E0` handles a PACKED tag register by register, flushing the batch first for any descriptor
other than 1 to 5 or `0xE`. The descriptors with handlers are PRIM, RGBAQ, ST, UV, XYZF2, XYZ2,
TEX0_1, TEX0_2, CLAMP_1, CLAMP_2, FOG and A+D.

ST sets Q from its third float and stores S/Q and
T/Q at `01FCB604` and `01FCB600`; RGBAQ stores the four colour bytes at `01FC361C` and `(int) Q` at
`01FC3618`; UV stores its two 14-bit values at `01FCB60C` and `01FCB608`; XYZF2 clears the fog
byte `01F83563` and FOG sets it from its field times 0.0625. The same switch carries the A+D
register numbers as arms a 4-bit descriptor can never reach.

The A+D handler `0020FCA0` flushes the batch before any register other than 1 to 5, then honours
PRIM, TEX0_1,
TEX0_2, CLAMP_1, CLAMP_2, TEXA (`0x3B`), FOGCOL (`0x3D`), TEXFLUSH (`0x3F`, device slot
`+0x128`), ALPHA_1, ALPHA_2 (`0x42`, `0x43`), TEST_1, TEST_2 (`0x47`, `0x48`) and ZBUF_1, ZBUF_2
(`0x4E`, `0x4F`). Twenty registers in all; FRAME, SCISSOR, XYOFFSET, TEX1, PRMODE, COLCLAMP,
DTHE, FBA, PABE, DIMX, TEXCLUT, MIPTBP and PRIM's AA1 bit 7 are ignored.

PRIM (`0020FE70`) stores the type at `01F83562` and the IIP, TME, FGE, ABE, FST, CTXT and FIX bits
at `01FC3600`, `01F8357C` to `01F8357F`, `01FC3601` and `01FC3602`, then `0020FBA0` sets the
vertices a primitive needs at `01F83570`, the carry at `01F8356C` and the index kind at
`01F83578`, and the phase `01F83574` and vertex count `01F83568` restart at 0:

| PRIM type | needs | carry | kind |
|---|---|---|---|
| 0 point | 1 | 0 | 0 |
| 1 line | 2 | 0 | 1 |
| 2 line strip | 2 | 1 | 1 |
| 3 triangle | 3 | 0 | 2 |
| 4 triangle strip | 3 | 2 | 2 |
| 5 triangle fan | 3 | 2 | 2, and the fan flag `01F83561` |
| 6 sprite | 2 | 0 | 2 |

### Vertices, indices and the batch

XYZF2 and XYZ2 raise the phase, saturating at the requirement, flush at 682 vertices, and convert
the vertex with `00210230` into the 48-byte slot `01FC3620 + n × 48`. On the packed path X and Y
are the low 16 bits of each dword times 0.0625 (the GS 12.4 fixed point) and Z is bits 4 to 27 of
the second qword, clamped to the upper bound `01FD3664` and then the lower `01FD3660`; with
`01FD3611` set three floats are taken directly.

`0020EA50` then builds `(X, Y, Z, 1)`, writes the
four RGBAQ bytes `01FC361C` to `01FC361F` as unnormalised floats at `+0x10`, multiplies by the
matrix at `01FD3620` through `00202B70`, divides x, y, z and w by w, and copies the UV pair
selected by the FST bit from `01FCB600` to `01FCB60C` into `+0x20`.

The vertex counts only when bit 47 of its second qword (ADC) is clear and the phase has reached
the requirement; the phase then drops to the carry and the index arm runs, appending 16-bit
indices to `01FCB610` (count `01F83564`) with n the new vertex count: a point writes n-1; a line
or line strip n-2, n-1; a triangle or triangle strip n-3, n-2, n-1; a fan 0, n-2, n-1; a sprite
duplicates its two corner vertices into four and writes six indices for two triangles.

`0020EC80` flushes: when indices are pending it selects state through `0020ED30` and submits
through `0020EB60(lastIndex + 1, device)`, then zeroes the index count; when the vertex buffer is
past 682 it moves the primitive's unfinished trailing vertices to the front (for a fan, after
vertex 0).

Among the state `0020ED30` selects, `0020FF10` decodes the GS TEST register of the current context
(`01FC35C8`, or `01FC35D0` while `01FC3601` is set): ATE bit 0, ATST bits 1 to 3, AREF bits 4 to 11,
AFAIL bits 12 and 13, DATE bit 14, DATM bit 15, ZTE bit 16, ZTST bits 17 and 18, into `01FD3668` to
`01FD3684`. It hands the device (its vtable `+0x88`) the alpha test with AREF / 255 and the method
`0020F2A0(ATST)`, which maps 1 to 7 onto 7, 4, 6, 3, 2, 1, 5 and anything else onto 0.

`0020EB60` looks TEX0_1 or TEX0_2 (by the CTXT bit `01FC3601`) up in the 16-byte texture table
`01F83580` by
`(TEX0 >> 37) & 0x3FFF` when TME is set and the format field is at least `0x300000`, copies the
vertices and indices into buffers from the device object's slots `+0` and `+0x10`, and draws
through its slot `+0x28` with the index kind. The device object is the one `00210320` stored at
`01FC35F8`, the embedded `PrimitiveRendererD3D11` at `02CC1CD0`.

## Layouts

```
VIF command word     [31:24] code, [23:0] parameters
MPG on this port     0x4A000000 | addr, then a u64 x64 function pointer (the console: NUM microcode words)
UNPACK word          [27:24] format (vn << 2 | vl), bit 15 add TOPS, bit 14 unsigned, [23:16] NUM, [9:0] address
program call         02068E30[ max { a in 02088E50 : a <= requested } ](callback, context)
VU memory            02064E30 + cell * 16, cell 0..1023; TOP 02064E1C, TOPS 02064E28
VIF registers        02088E30 BASE, 02088E34 OFFSET, 02088E38 status (bit 6 = second buffer), 02088E3C WL, 02088E40 CYCLE, 02088E44 count, 02088E50 list
template object      +0 u16 word, +3 kind (0x10 plain, 0x30 registered), +4 record handle; packet words from +8
record table         02EAF930 + n * 16: u32 0x4A000000 | addr, u64 program; count 02EB37B0
GiVmax (0x640)       +8 flag, +0x10 ctx, +0x18 chunk page size (1,024), +0x1C chunk count, +0x20.. 64 chunk pages of {ptr, len} x16 B
                     +0x220/+0x224/+0x228 GS copy list, +0x428/+0x42C/+0x430 flag list, +0x630/+0x634 device state, +0x638, +0x639 bytes
GIF tag              [14:0] NLOOP, 15 EOP, 46 PRE, [57:47] PRIM, [59:58] FLG, [63:60] NREG, [127:64] REGS (4 bits each)
vertex (48 B)        +0 x y z w (after the divide), +0x10 r g b a, +0x20 u v; buffer 01FC3620, 682 slots; indices 01FCB610
```

## Shipped data

| Fact | Value |
|---|---|
| boot template calls | 77 (28 + 49), 76 builders, 77 objects |
| template builders that register a program | 37 |
| registrar call sites | 104: `003A34D0` 45, `003A35E0` 27, `003A33B0` 22, `003A2F70` 10 |
| distinct microprograms | 57: 35 by template, 44 by registrar, 22 by both |
| programs calling the sticky-flag helpers | 40 |
| GS registers honoured | 20 |
| vertex batch | 682 slots of 48 bytes; only the fan arm range-checks the index count (`0x8000` bytes) |
| GS coordinate scale | 0.0625 |

## Operations

At boot: `0022CB90`, then the two hubs build the 77 templates. On a draw that uses the layer: a
registrar or effect finaliser builds a `GiVmax`, `001DB550` runs its packets at once (MPG installs
the program, UNPACK fills VU memory, MSCAL runs the program, each GS packet is copied), and the
frame's render pass list later runs `001DB3D0`, which replays the copies into D3D11 vertex and
index batches.

## State

VU memory and the VIF registers (one set, shared by every packet), the program table and its
list (reset per packet list), the GS replay's register words at `01F83561` to `01F8357F` and
`01FC3580` to `01FC3610`, the vertex and index buffers, the texture table `01F83580` and the
device pointer `01FC35F8`.

## Modding notes

- Only the twenty registers above reach the PC. A packet that relies on FRAME, SCISSOR, XYOFFSET,
  TEX1 or PRMODE has that part ignored, which is where to look for PS2-versus-PC differences.
- The templates are immediates in the builders; patching a word changes the packet every draw
  from that template sends.
- An MPG word in a hand-built packet needs an x64 function pointer after it, not microcode.
- A program is reachable only within the packet list that installed it; `0022C930` empties the
  list before each `GiVmax` runs.

## Related

- [PS2 CPU emulation](ps2-cpu-emulation.md): the vector unit 0 register bank the other
  translated assembly uses, and the boot routine shared with this layer.
- [Game application](game-application.md): the render pass list that drains the commands.
