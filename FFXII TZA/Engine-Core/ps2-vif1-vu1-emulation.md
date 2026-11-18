[Home](../../README.md) / [Engine core](README.md) / PS2 VIF1 and VU1 emulation

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| PS2 VIF1 and VU1 emulation: the packet decoder, the recompiled microprograms and the GS replay | system | Engine core | PlayStation emulation | The second PlayStation 2 layer the remaster keeps: a VIF1 command decoder at 0x0022C970 over a 16 KB emulated VU1 memory, 57 vector-unit microprograms recompiled to x64 and installed by MPG as function pointers, the 77 packet templates two boot hubs build and the registrars that build packets per draw, the GiVmax render command that runs a packet at emit time and collects its GS output, and the GS replay that turns GIF packets into D3D11 vertices and indices for twenty honoured GS registers. | 0x0022C970, 0x0022C940, 0x0022BFF0, 0x0022C8D0, 0x0022C930, 0x0022CC40, 0x0022CC30, 0x0037DF90, 0x0037E0F0, 0x008631E0, 0x008631D0, 0x001DB840, 0x001DB550, 0x001DB660, 0x001DB3D0, 0x001FB840, 0x001DB7E0, 0x003A34D0, 0x003A35E0, 0x003A33B0, 0x003A2F70, 0x0020E630, 0x0020F310, 0x00210320, 0x0020F3E0, 0x0020FCA0, 0x00210230, 0x0020EA50, 0x0020FE70, 0x0020FBA0, 0x0020EC80, 0x0020EB60, 0x0020F250, 0x004EF860, 0x00476C80 |

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

`0x0022C940(packet, bytes, callback, context, flag)` passes the VU memory base `0x02064E30` to
`0x0022C970`, which walks the packet one 32-bit word at a time and switches on the top byte. The
cases are VIF1 commands with VIF1's field layout:

| Code | VIF1 command | What `0x0022C970` does |
|---|---|---|
| `0x01` | STCYCL | low byte to CYCLE `0x02088E40`, next byte to WL `0x02088E3C` |
| `0x02` | OFFSET | `data & 0x3FF` to `0x02088E34`, clears bit `0x40` of the status word `0x02088E38`, copies BASE to TOPS `0x02064E28` |
| `0x03` | BASE | `data & 0x3FF` to `0x02088E30` |
| `0x14`, `0x15` | MSCAL, MSCALF | runs `0x0022C8D0`, then the program installed at the largest address not above the requested one, called with the callback and the context (`0x0022CB1E`); when the installed list is empty or holds no address at or below the requested one, the search keeps its start value 0 and the table entry for address 0 is called (`0x0022CADD`, `0x0022CAE5`); the test of the result against `0x10000` (`0x0022CB07`) never matches, since the list holds 16-bit addresses |
| `0x4A` | MPG | 4 bytes are skipped and the next 8 are an x64 function pointer, stored at `0x02068E30 + imm16 × 8`, so the command takes 16 bytes (`0x0022CA42`-`0x0022CA5D`); the address is appended to the list `0x02088E50` (count `0x02088E44`) |
| `0x50`, `0x51` | DIRECT, DIRECTHL | calls the callback with the data pointer, the context and the flag, then skips `count × 16` bytes |
| `0x60` to `0x7F` | UNPACK | `0x0022BFF0` with the format from the bits under mask `0xF000000`, the unsigned flag bit `0x4000`, the add-TOPS flag bit `0x8000`, NUM from the bits under mask `0xFF0000` and the address from the low ten bits; the mask flag bit `0x10000000` has no effect |
| anything else | NOP, FLUSH, FLUSHE, FLUSHA, STMASK, STROW … | advances four bytes |

On the console MPG uploads microcode. Here it uploads a pointer to a function that already is
that microcode, compiled, and MSCAL calls it with the callback and context as arguments. The MPG
address is stored unmasked; the table holds 16,384 entries up to `0x02088E30`, so an address of
`0x4000` or more would overrun into the VIF registers, and every shipped packet uses address 0.

The code tests are looser than the names: UNPACK is any code with bits `0x20` and `0x40` set (so `0xE0` to
`0xFF`, the interrupt forms, decode as UNPACK too), DIRECT is `code - 0x50 < 2` and MSCAL
`code - 0x14 < 2`, so MSCNT (`0x17`) takes the four-byte default.

`0x0022C8D0` is the double-buffer step the console does on MSCAL: it copies TOPS into TOP
`0x02064E1C`, then sets TOPS to BASE and clears status bit `0x40` if that bit was set, or to
BASE + OFFSET and sets the bit otherwise. `0x0022C930` zeroes only the installed count (`0x02088E44`); `0x001DB550` calls it
before every packet list, so MSCAL's search sees only the list's own installs, but the program table `0x02068E30` keeps
its pointers: a search that finds nothing calls the entry for address 0, the last program any list installed there
(`0x0022CAE5`, `0x0022CB1E`).

### VU memory and the unit's state

| Address | Size | Role |
|---|---|---|
| `0x02064E30` to `0x02068E2F` | `0x4000` | VU memory, 1,024 cells of 16 bytes |
| `0x02068E30` to `0x02088E2F` | `0x20000` | the installed-program table, one x64 pointer per VU address |
| `0x02088E30` to `0x02088E47` | — | BASE, OFFSET, status, WL, CYCLE, installed count |
| `0x02088E50` onwards | 4 per entry, the first `0x02088E50` to `0x02088E53` | the installed list: one VU address per MPG since the last clear, stored at `0x02088E50 + count × 4` with no bound check (`0x0022CA53`-`0x0022CA60`); the next global the image addresses is the visited list `0x02088FE0` of the [collision walk](../Movement-And-Pathfinding/collision-mesh-movement.md), 100 entries on |
| `0x02064E1C`, `0x02064E28` | u16 each | TOP and TOPS |
| `0x02064B00` to `0x02064E2F` | — | the microprograms' own working words: 16-bit cell indices (`0x02064B0C`, `0x02064DB0`, `0x02064DB4`, `0x02064DB8`, `0x02064DD0`) and float scratch |
| `0x02064DEC` | u16 | the sticky status flags: `0x0022CC40` sets `0x40` (zero) and `0x0022CC30` sets `0x80` (sign); they are its only writers, and 40 functions call each of them at 116 sites: 33 microprograms and the shared subroutines `0x004753B0`, `0x004825F0`, `0x00487D60`, `0x0048D240`, `0x004B0CF0`, `0x004B0F60` and `0x004EB910` |

The boot routine `0x0022CB90` zeroes the VU memory, TOP, TOPS, the status word and the words
`0x02088E30` to `0x02088E38`, and `0x0017D6E0` runs it again on every restart pass
([PS2 CPU emulation](ps2-cpu-emulation.md)).

### UNPACK

`0x0022BFF0(vuMem, vn, vl, unsigned, addTops, num, addr, data)` writes `num` elements into VU
cells starting at `addr`, plus TOPS when the flag is set, with WL elements per cycle and CYCLE
cells between cycle starts. It returns 0 without writing when CYCLE is below WL.

The thirteen formats are `vn` = S, V2, V3, V4 by `vl` = 32, 16, 8, with V4-5 as the last:

- S broadcasts one value to all four lanes, but its three arms move the destination 4 bytes per element instead of 16
  (`0x0022C10B`, `0x0022C1BB`, `0x0022C24D`), so inside a cycle each element overwrites three lanes of the one before; V2
  writes x and y and leaves z and w; V3 writes three lanes; V4 four;
- V4-5 expands a 16-bit colour as `r = (v & 0x1F) << 3`, `g = (v >> 2) & 0xF8`,
  `b = (v >> 7) & 0xF8`, `a = (v >> 8) & 0x80`;
- the 16- and 8-bit formats sign-extend unless the unsigned flag is set;
- the return value is the packed size rounded up to whole 32-bit words,
  `((32 >> vl) × (vn + 1) × num + 31) / 32 × 4`, which the decoder adds to its cursor.

Two arms read their source at the wrong stride: V2-32 advances four bytes per element against a
packed eight, and V4-5 advances eight against a packed two. Every packet the game builds is
V4-32, so neither arm runs on shipped content.

### Microprograms and the three ways a packet is built

A microprogram is an x64 function that reads and writes VU memory through the 16-bit index words above and hands each
finished GS packet to the callback.

`0x004EF860(callback, context)` is the packet leaf that `0x004EF940` and `0x004F7070` reach through `0x004EDB50` and
`0x004F5360`. 18 other programs call one of its nine copies (`0x002EFE70`, `0x00479370`, `0x004C4C40`, `0x004C7F00`, `0x004CF3B0`,
`0x004D7B10`, `0x004DB270`, `0x004DF360`, `0x004E78A0`), which differ from it only in the two buffer offsets (`0x2A8` and
`0x168` below); `0x00478280` and `0x004ECC50` call the variant `0x004ECB70`, and the other 35 programs call none of them.

`0x004EF860` writes `word[0x02064DB8] + 0x8000` (the 16-bit sum, zero-extended to 32 bits, `0x004EF89C`-`0x004EF8B6`) into the
cell at `0x02064DB0`, resets `0x02064DB8` to the word `0x02064B0C` (`0x004EF8C0`), copies twelve bytes of the cell at
`0x02064DD0` beside it (staged at `0x02064C60`), sets `0x02064DB4` to `0x02064B0C + 0x2A8`, or `+ 0x168` when `0x02064B0C`
differs from `0x02064DB0 - 0x168`, calls `callback(cell address, context, 0)` (`0x004EF90A`-`0x004EF910`), then sets
`0x02064DB0` to `0x02064B0C + 0x02064DB4` and `0x02064DB4` one past it.

The image installs 57 distinct programs at 141 call sites ([ps2-vif1-vu1-emulation-programs.tsv]
([`ps2-vif1-vu1-emulation-programs.tsv`](ps2-vif1-vu1-emulation-programs.tsv)), resolved from the `lea` that loads each site's program
argument). Three routes build the packets that carry them:

- **77 boot templates.** `0x0037DF90` makes 28 calls and `0x0037E0F0` 49, each `lea rcx, object;
  call builder` with a distinct zero-initialised object at `0x02ADEF40` to `0x02AED330` (76 distinct
  builders; `0x004E3110` is called twice); each hub reaches its last builder by a tail jump
  (`0x0037E0E3` to `0x004A8860`, `0x0037E33F` to `0x004C3610`). A builder fills its packet with immediate stores.
- **Template contents.** The decoded command streams are in
  [ps2-vif1-vu1-emulation-templates.tsv](ps2-vif1-vu1-emulation-templates.tsv) and the GIF tags
  they carry in [ps2-vif1-vu1-emulation-gif-tags.tsv](ps2-vif1-vu1-emulation-gif-tags.tsv).
- **Template headers.** 37 builders call `0x008631E0(object, program, 0)`, which stamps the word 1 at `+0` and kind
  `0x30` at `+3`, appends `{0x4A000000 | addr, program}` to the record table `0x02EAF930` (count `0x02EB37B0`) and stores
  the record's handle at `+4`: the low 32 bits of the record's address minus `[0x01F83530]` (`0x0020E620`,
  `0x00863226`-`0x0086322B`; [global state accessors](global-state-accessors.md)).

  29 of them call it first; the other 8 clear the object with `memset` (thunk `0x00861EC0`) before it. The templates
  install 35 programs.
- **Plain headers.** `0x008631D0(object, count)` stamps the plain kind `0x10` header: the count as a word at `+0`, the
  kind at `+3` and 0 at `+4` (`0x008631D0`-`0x008631D7`).
- **Per-draw registrars.** `0x003A34D0` (45 sites) and `0x003A33B0` (22) append a `0x28`-byte record
  to the sorted draw list `[0x02F8F2F8]` (count `0x02F8F2C6`) and hold the command for a later
  submit; `0x003A35E0` (27) and `0x003A2F70` (10) submit it at once through `0x0020E630(node, 2)`. All
  four build through `0x001DB840` and together install 44 programs, 22 of them shared with the
  templates.
- **Registrar arguments.** Each registrar takes a 16-byte node from `0x0020E680` and hands `0x001DB840`
  the two VIF words, the program and a payload. `0x003A33B0` and `0x003A2F70` hand on a second payload;
  `0x003A34D0` and `0x003A35E0` give it 0 (`0x003A35A0`, `0x003A362E`). `0x003A35E0` and `0x003A2F70` pass
  flag and context 0 (`0x003A2FA9`, `0x003A3619`).
- **Sorted registrars' blend.** `0x003A34D0` and `0x003A33B0` pass flag 1 and, as the context, the blend
  word `0x01EFAC20[0x02AEE900]` (`0x003A3460`, `0x003A3470`, `0x003A3583`, `0x003A3593`), which the replay
  stores as `ALPHA_1`.
- **Sorted records.** `0x003A34D0` and `0x003A33B0` write `+0x00` = 0, `+0x08` = the first argument's low
  24 bits with `0x02AEE910 << 4` ORed into its top byte, `+0x0C` = 8, `+0x10` = 0 and `+0x20` =
  (`0x02AEF41C` × 2 | b) × 2, b being 1 when `0x0024E460()` returns non-zero or `0x02AEF418` is non-zero
  (`0x003A33FE`-`0x003A343E`), and `+0x18` = the node once `0x001DB840` returns (`0x003A34B3`, `0x003A35CB`).
- **Record count.** The count `0x02F8F2C6` is raised with no bound check (`0x003A33F6`, `0x003A3515`).
- **Effect elements.** `0x001DB7E0` (callers `0x00540DB0`, `0x00540C70`, the finalisers every effect
  element type reaches) constructs the same command with no packets and stores it at its
  argument's `+8` (`0x001DB818`), or stores 0 there when the allocation returns 0 (`0x001DB827`); it
  does not run the command. The element appends its own packet, which carries its own MPG.

### Shared subroutines of the microprograms

The programs share 58 subroutines, listed with their callers in
[ps2-vif1-vu1-emulation-subroutines.tsv](ps2-vif1-vu1-emulation-subroutines.tsv). They work on the same words:

- `0x004A6780` clears the float and index words at the start of 14 programs;
- `0x0047BFB0` and `0x00487F90` evaluate a sine series and `0x0048F790` wraps an angle by whole turns;
- `0x004825F0`, `0x0048D240`, `0x004B0CF0`, `0x004B0F60` and `0x00487D60` look a frame up in a table of per-frame counts in VU
  memory;
- `0x004753B0` and `0x004AD9E0` clip edges and `0x004EB910` builds a sprite;
- `0x004ECB70` emits a GS packet like `0x004EF860`, and the nine copies of `0x004EF860` (`0x002EFE70`, `0x00479370`, `0x004C4C40`,
  `0x004C7F00`, `0x004CF3B0`, `0x004D7B10`, `0x004DB270`, `0x004DF360`, `0x004E78A0`) emit it with other buffer offsets;
  `0x004EDB50` and `0x004F5360` work the cells for `0x004EF940` and `0x004F7070` and end in `0x004EF860`;
- the 30 small ones from `0x004B97F0` to `0x004B9E30`, with `0x004B9E60`, `0x004CF230`, `0x004CF280` and `0x004CF350`, are lane
  arithmetic, comparisons, cell loads and stores and the random generator `0x01E02828` (`0x004B97F0`), which returns 1.0
  while `0x02064AFC` is 0.

`0x00476C80` is a template read end to end. It holds `0x008631E0` with program `0x004758E0`, BASE 0 and OFFSET 0
(`0x03000000`, `0x02000000`), then a sub-header `0x008631D0(object + 0x10, 0x43)` (`0x00476CAF`: the word `0x43` at
`+0x10`, kind `0x10` at `+0x13`, 0 at `+0x14`), then STCYCL 4,4 (`0x01000404`) and UNPACK V4-32 of 66 quadwords
(`0x6C420000`).

The UNPACK payload, `+0x20` to `+0x43F`, starts with the GS screen centre 2048.0 (`0x45000000`) in the quadwords
(2048.0, 2048.0, 260.0, 228.0) and (0, `0x30000000`, `0x412`, 0). It then holds, four times (`0x00476D01`-`0x00476DFF`,
from `+0x40` at a stride of `0xF0`), a vertex block and an A+D GIF tag (NLOOP 5, NREG 1, REGS `0xE`) writing CLAMP_1,
TEX0_1, ALPHA_1 and TEST_1 to 0 and PRIM to `0x5D`.

The vertex block is nine quadwords: (0, 0, `0xFFFFFF`, 0), (0, 0, 256.0, 224.0), (1.0, 1.0, 1.0, 0),
(1.0, 1.0, 0, 0), (0, 0, 1.0, 1.0) and four quadwords of the integers (128, 128, 128, 128).

The payload ends with the register pairs ST, CLAMP_1, RGBAQ, XYZF2 = 0 as its last four quadwords (`+0x400` to `+0x43F`); then come MSCALF 0
(`0x15000000` at `+0x440`), FLUSHA (`0x13000000` at `+0x444`) and the zero words at `+0x448` and `+0x44C` (`0x00476E57`,
`0x00476E62`).

`0x004B0000(object)` (555 bytes), the builder of `startup/7`, which `0x0037DF90` calls with the object `0x02AE31F0`, is
another template read end to end, and makes no test. It clears the object's `0x140` bytes with `memset` (`0x00861EC0`),
calls `0x008631E0(object, 0x004ADD10, 0)`, stores BASE 170 (`0x030000AA`) at the object's `+0x08` and OFFSET 421
(`0x020001A5`) at its `+0x0C`, calls `0x008631D0(object + 0x10, 0x12)`, and stores STCYCL 4,4 (`0x01000404`) at `+0x18`
and UNPACK V4-32 of 18 quadwords to address 0 (`0x6C120000`) at `+0x1C` (`0x004B0000`-`0x004B004D`).

In the UNPACK payload, `+0x20` to `+0x13F`, the first quadword stays 0; the second holds only `0x8000` at `+0x3C`,
then come the integers (128, 128, 128, 128) at `+0x40` and (0.5, 0.5, 0, 0) at `+0x50` (`0x004B0054`-`0x004B007E`). The
same sixteen words are stored twice, at `+0x60` to `+0x9F` and at `+0xB0` to `+0xEF` (`0x004B0085`-`0x004B019A`).

To six significant figures, the sixteen words are the quadwords (0.999998, -0.000574693, 0.00191565, 0), (0,
-0.957826, -0.287347, 0), (-0.00200000, -0.287347, 0.957825, 0) and (5.96046e-08, -1.52588e-05, 522.016, 1.0); between
the two copies, `+0xA0` to `+0xAF` holds (4090.0, 4090.0, 16777000.0, 255.0) (`0x457FA000`, `0x4B7FFF28`,
`0x437F0000`).

The payload's last five quadwords are GIF data (`0x004B01A4`-`0x004B021A`). At `+0xF0` an A+D tag (NLOOP 2, EOP, NREG 1,
REGS `0xE`) is followed by two pairs, `object + 0x100` and `object + 0x110`, that write 0 to CLAMP_1 and TEX0_1
(registers 8 and 6). At `+0x120` and `+0x130` come two tags with NLOOP 0, EOP, PRE set, NREG 3 and REGS `0x412` (ST,
RGBAQ, XYZF2): PRIM `0x5C`, a triangle strip, and PRIM `0x5D`, a triangle fan.

`0x004B0000` writes nothing past `+0x13F` and returns (`0x004B0225`-`0x004B022A`). The draw `0x0045AEE0` of effect element
type `0x94` goes on to its arm `0x0045AEF0`; its test of the type byte `+0x00` against 0 is never met, since its one
caller, the draw dispatcher `0x002F4020` (`0x002F42A8`), calls it for type `0x94` only (`0x0045AEE0`-`0x0045AEE3`).

The arm first hands the two copies to `0x00397910`, which writes the 4x4 product of its first two arguments, sixteen
floats, over its third: `0x00397910(local, local, 0x02AE32A0)` for `+0xB0` and `0x00397910(0x02AEDDF0, local, 0x02AE3250)` for
`+0x60` (`0x0045AFBC`-`0x0045AFF6`, `0x00397A75`-`0x00397AE0`).

The rest of the arm runs only when the element's definition (element `+0x20`) has byte `+0x240` equal to 2 or 4
(`0x0045AFFB`-`0x0045B006`) and `0x00431830(definition + 0x1A0, local, 0, element dword +0x44)` answers non-zero
(`0x0045B00C`-`0x0045B02E`). The arm then stores the two qwords that call left in the local as the A+D data, the first at
`+0x110` and the second at `+0x100` (`0x0045B06D`, `0x0045B078`).

It sets `+0x50` to `0x004309C0(definition + 0x1A0, element dword +0x44) + element float +0x29C` and `+0x54` to
`0x004309C0(definition + 0x1B0, element dword +0x44) + element float +0x2A0` (`0x0045B07F`-`0x0045B0D4`). Each of `+0x40` to
`+0x4C` then takes one byte of a local colour built by `0x002F1F40(element, element + 0x230, local)`,
`0x0026EE00(local, element + 0x240, local)`, `0x0042FDB0(definition + 0x1E0, element dword +0x44)` and a second `0x0026EE00`
(`0x0045B0DC`-`0x0045B13A`).

A registrar runs only when `0x0020E600(definition dword [+0x2A0 + 4 * element dword +0x298])` is non-zero
(`0x0045B140`-`0x0045B159`): `0x003A2F70` when bits `0x7` of the definition's byte `+0x24A` are clear, else `0x003A33B0`,
which, with bit `0x1` of the definition's byte `+0x4B` clear, runs only when `0x00399600(element + 0x230, local)`
returns 0 (`0x0045B15F`-`0x0045B1CC`).

Both registrars get the template's words `+0x08` and `+0x0C`, the program `0x004ADD10` and the template's `+0x18`,
`0x128` bytes from `0x02AE3208` (`0x0045B173`-`0x0045B227`; [Templates the type arms
patch](../Graphics/effect-element-types.md#templates-the-type-arms-patch)). The word `+0x3C`, the
quadword `+0xA0` and the three GIF tags keep the builder's values.

### Columns of ps2-vif1-vu1-emulation-programs.tsv

One row per installed program, 57 rows. The three counts add up to the 141 call sites.

| Column | Holds |
|---|---|
| `template_sites` | how many boot templates install the program through `0x008631E0`: 0, 1 or 2 (37 sites in all) |
| `sorted_registrar_sites` | how many `0x003A34D0` and `0x003A33B0` sites install it, the registrars that append to the sorted draw list and submit later: 0 to 2 (67 sites in all) |
| `unsorted_registrar_sites` | how many `0x003A35E0` and `0x003A2F70` sites install it, the registrars that submit at once: 0 to 4 (37 sites in all) |

### Columns of ps2-vif1-vu1-emulation-templates.tsv

One row per boot template, 77 rows, decoded from the stores each builder makes.

| Column | Holds |
|---|---|
| `family` | `startup/N` or `startup-ext/N`, where N is the builder's place in the boot calls: 0 to 27 in the calls of `0x0037DF90`, 28 to 76 in those of `0x0037E0F0`; `startup-ext` marks the nine builders that lie below `0x00480000` (rows 18, 32, 51 to 54, 64, 68 and 69) |
| `memset_size` | the byte count of the builder's first `memset` clear (thunk `0x00861EC0`), in decimal, for example 304 for `0x004B0B70` (`mov r8d, 0x130`): at the object's start, except in `startup/6` (`+0xBC0`), `startup/13` (`+0x1E8`), `startup/61` (`+0x60`), `startup/65` (`+0x90`) and `startup/71` (`+0xE0`), where the clear starts inside the object; empty on the 58 builders that do not call it |
| `obj_header` | the header at the object's start: `0x30` where `0x008631E0(object, program, 0)` stamps the kind with a record handle (37 rows), `0x10 w=N` where `0x008631D0(object, N)` stamps the plain kind with a word count N; empty when the builder writes no header |
| `sub_headers` | each further `0x008631D0` header inside the object, as offset and word count in hex, for example `+10:w=11` for `0x008631D0(object + 0x10, 0x11)`; empty when there is no such header |
| `mpg_program` | the program address `0x008631E0` is handed (its second argument); empty on the 40 rows without that header |
| `mpg_addr` | the VU address `0x008631E0` is handed (its third argument): 0 on all 37 rows that have one |
| `command_sequence` | every VIF command the builder stores, as object offset and decoded command (BASE, OFFSET, NOP, STCYCL, UNPACK with format, count and address, DIRECT, MSCALF, FLUSH, FLUSHA, SUBHDR for a sub-header), separated by ` ; ` |
| `gif_writes` | the GS register writes of the A+D data in the packet a DIRECT command carries: `CLAMP_1=0x0` on `startup/28` (`0x004C2040`); empty on the other 76, among them the 28 other rows whose command sequence holds a DIRECT command |
| `tail_reg_pairs` | the register and value pairs the builder stores after its looped blocks, just before MSCALF: `ST`, `CLAMP_1`, `RGBAQ` and `XYZF2` set to 0 on `0x00476C80` (`+0x400` to `+0x43F`) and `0x0047BAF0`; empty on the other 75 |
| `unattributed_stores` | the builder's stores that fall in no command and no payload: 0 on all 77 rows |
| `payload_stores` | how many store instructions of the builder and its callees put a non-zero value inside the UNPACK payloads or a DIRECT packet, immediate or register, each instruction counted once (30 for `0x004B0B70`: 28 immediates and two stores of `rax` = `0x8000000080` at `0x004B0BB3` and `0x004B0BB7`; its four other register stores write a zeroed register) |

### Columns of ps2-vif1-vu1-emulation-gif-tags.tsv

One row per GIF tag inside a template payload, 124 rows.

| Column | Holds |
|---|---|
| `unpack_at` | the object offset of the UNPACK command whose payload holds the tag: `+0x1C` (111 rows) after a header, or `+0xC` (13 rows) in a template without one |
| `prim_raw` | the tag's 11-bit PRIM field in hex, which `prim`, `iip`, `tme`, `fge` and `abe` decode; `0x000` with `prim` reading `(PRE=0, PRIM unwritten)` on the 64 tags whose PRE bit is 0 |
| `ad_payload` | for the 61 A+D tags (`regs` reads `A+D`), each register the following data quadwords write and its value, as `NAME=value` separated by semicolons (an address in hex, such as `0x0E`, where the register has no name); empty on the other 63 |

### Columns of ps2-vif1-vu1-emulation-subroutines.tsv

| Column | Holds |
|---|---|
| `called_from` | the programs that call the subroutine, separated by commas; all 47 addresses that occur are programs of ps2-vif1-vu1-emulation-programs.tsv, and 33 subroutines are called from `0x004B1190` alone |

### The GiVmax render command

`0x001DB840(node, word1, word2, program, payload, size, payload2, size2, flag, ctx)` allocates the `0x640`-byte `GiVmax`
command (RTTI `.?AVGiVmax@@`, vtable `0x009007E8`), stores it at `node + 8` (`0x001DB89B`) and fills its chunk list with
pointer and length pairs: `0x01F82D08` for 8 bytes (the two VIF words, rewritten there on every call), `0x01DFD038` for 16
bytes (the image constant `0x4A000000`, MPG, with the program pointer stored at `0x01DFD040`), then the payloads through
`0x001DB340`, the second only when `payload2` is not 0 (`0x001DB9F8`).

Both scratch chunks are image-wide and `0x001DB840` is their only writer, so the packet must be consumed inside the
call. It also sets `+0x630` to 1 when `0x0024D140` returns non-zero and `+0x634` to the float that call writes
(`0x001DB8AC`, `0x001DB8BF`), `+8` to `flag` and `+0x10` to `ctx` (`0x001DB8CE`, `0x001DB8D9`), and, after the payloads,
`+0x638` to `0x002105C0()`, the byte `0x01FD3698` (`0x001DBA12`). When the allocation returns 0 the constructor is skipped
and these stores go through a null pointer (`0x001DB894`, `0x001DB8AC`).

It is: `0x001DB840` ends by calling `0x001FB840(node)`, which tail-jumps the command's vtable slot 0,
`0x001DB550`. That runs the packet list at emit time: it zeroes the two output counts, stores the
flag `0x02EC3ECC == 0` at `+0x639`, resets the installed count, and calls `0x0022C940` once per chunk
with the callback `0x001DB640`.

The callback's body `0x001DB660` sizes the GS output with `0x0020F310`, copies it into a buffer from the allocator at
`0x01F82D00`, and appends the pointer to the paged list at `+0x228` (count `+0x224`, page size `+0x220` = 1,024) and the
callback's flag byte to the list at `+0x430` (count `+0x42C`, page size `+0x428` = 1,024).

It appends the flag first (`0x001DB729`) and the pointer second (`0x001DB7AB`), and when the current page of either list
is not yet allocated it takes one from the allocator at `0x01F7F4C0` (`0x001DB6F7`, `0x001DB76F`); a page number of 64 or
more stores to address 0 (`0x001DB6D1`, `0x001DB746`). The constructor `0x001DB220` sets all three page sizes to 1,024 and
allocates the first page of each list (`0x4000`, `0x2000` and `0x400` bytes).

Slot 1, `0x001DB3D0`, replays later, when the frame's render pass list drains the command: device slot `+0x58` with the
byte `+0x630` and the float `+0x634` (`0x001DB416`), `0x00210510(+0x10)` and `0x00210560(0x51001)` when `+8` is set
(`0x001DB41D`), `0x002105B0(+0x638)`, `0x002104D0(+0x639)`, then `0x00210320(copy, device, flag)` for every collected copy,
with the flag byte of the same index, then `0x002104E0`, `0x002105B0(0)` and a tail jump to the device slot `+0x58` with
(0, 0.1) (`0x001DB4ED`).

`0x00210510` stores its argument as `ALPHA_1` (`0x01FC35D8`) and `0x00210560` as `TEST_1` (`0x01FC35C8`), each setting
`0x01FC3603`; `0x002105B0` stores `0x01F83560`; `0x002104D0` stores `0x01FD3610` and clears `0x01FC3607`; `0x002104E0` calls the
device's `TEXFLUSH` slot `+0x128` when `0x01FC3607` is set and then tail-jumps `0x0020ED30`.

### GIF packets and the GS replay

`0x0020F310` sizes a GIF packet by walking its tags: NLOOP is bits `0x7FFF`, EOP bit `0x8000` ends the walk, FLG bits
under mask `0xC00000000000000` and NREG bits under mask `0xF000000000000000` (0 means 16). PACKED tags are `(NREG ×
NLOOP + 1) × 16` bytes, REGLIST `NREG × NLOOP` rounded up to even, times 8, plus 16, and IMAGE and FLG 3 alike
`(NLOOP + 1) × 16` (`0x0020F3AB`-`0x0020F3B5`); the result is the sum of the tag sizes, the EOP tag's included
(`0x0020F3B8`, `0x0020F3C7`).

The gate byte `0x01E027C0` is 1 in the image and has no writer, so the sizing and the replay always run; with the gate
at 0 the sizing returns 16 (`0x0020F322`) and the replay returns at once (`0x00210336`).

`0x00210320` walks the same tags for the replay. It stores the device at `0x01FC35F8` and the flag at `0x01FD3611`, and for
each tag with NLOOP above 0 reads PRE (bit `0x400000000000`), PRIM (mask `0x3FF800000000000`), FLG and NREG, and
resets Q (`0x01E027B0`) to 1.0. A tag with NLOOP 0 is stepped over as 16 bytes with only its EOP bit read (`0x002103BE`,
`0x00210426`). A PACKED tag flushes the batch, applies PRIM through `0x0020FE70` and sets `0x01FC3603` when PRE is set
(`0x0021043B`-`0x00210447`), then runs `0x0020F3E0`; on a REGLIST or IMAGE tag PRE is not applied.

A REGLIST tag with NLOOP above 0 ends the walk through the flush. An IMAGE tag, and a tag with FLG 3, skips `NLOOP ×
16` bytes (`0x00210478`-`0x00210486`). EOP ends the walk, and a final `0x0020EC80` flushes.

`0x0020F3E0` handles a PACKED tag register by register, flushing the batch first for any descriptor
other than 1 to 5 or `0xE`. The descriptors with handlers are PRIM, RGBAQ, ST, UV, XYZF2, XYZ2,
TEX0_1, TEX0_2, CLAMP_1, CLAMP_2, FOG and A+D.

ST sets Q from its third float and stores S/Q and
T/Q at `0x01FCB604` and `0x01FCB600`; RGBAQ stores the four colour bytes at `0x01FC361C` and `(int) Q` at
`0x01FC3618`; UV stores its two 14-bit values at `0x01FCB60C` and `0x01FCB608`; XYZF2 clears the fog
byte `0x01F83563` and FOG sets it from its field times 0.0625. The same switch carries the A+D
register numbers as arms a 4-bit descriptor can never reach.

The A+D handler `0x0020FCA0` keeps the data qword at `0x01FC3608` and the register number at `0x01FC3610` (`0x0020FCA7`,
`0x0020FCB3`), and flushes the batch and sets `0x01FC3603` before any register other than 1 to 5 (`0x0020FCC3`, `0x0020FCD6`).

Its jump table (`0x0020FCF1`) then honours PRIM (a tail jump to `0x0020FE70`), TEX0_1, TEX0_2, CLAMP_1, CLAMP_2, TEXA
(`0x3B`, stored at `0x01E027B8`), FOGCOL (`0x3D`, its three low bytes to `0x01FC3604` to `0x01FC3606`), TEXFLUSH (`0x3F`, a
tail jump to device slot `+0x128`), ALPHA_1, ALPHA_2 (`0x42`, `0x43`), TEST_1, TEST_2 (`0x47`, `0x48`) and ZBUF_1,
ZBUF_2 (`0x4E`, `0x4F`).

The numbers 1 to 5 (RGBAQ, ST, UV, XYZF2, XYZ2) and every number above `0x4F` reach no arm
(the table for 1 to 5, `0x0020FCE1` above `0x4F`). An A+D write of 1 to 5 stores only the two words; one above `0x4F`
also flushes the batch and sets `0x01FC3603` (`0x0020FCC3`, `0x0020FCD6`).

Twenty registers in all; FRAME, SCISSOR, XYOFFSET, TEX1, PRMODE, COLCLAMP, DTHE, FBA, PABE, DIMX, TEXCLUT, MIPTBP and
PRIM's AA1 bit `0x80` are ignored.

PRIM (`0x0020FE70`) stores the type at `0x01F83562` and the IIP, TME, FGE, ABE, FST, CTXT and FIX bits
at `0x01FC3600`, `0x01F8357C` to `0x01F8357F`, `0x01FC3601` and `0x01FC3602`, then `0x0020FBA0` clears the fan
flag `0x01F83561` (`0x0020FBA7`) and sets the
vertices a primitive needs at `0x01F83570`, the carry at `0x01F8356C` and the index kind at
`0x01F83578` by the table below; type 7 matches no arm and keeps the three previous values
(`0x0020FC78`). The phase `0x01F83574` and vertex count `0x01F83568` restart at 0 (`0x0020FEF5`,
`0x0020FEFB`):

| PRIM type | needs | carry | kind |
|---|---|---|---|
| 0 point | 1 | 0 | 0 |
| 1 line | 2 | 0 | 1 |
| 2 line strip | 2 | 1 | 1 |
| 3 triangle | 3 | 0 | 2 |
| 4 triangle strip | 3 | 2 | 2 |
| 5 triangle fan | 3 | 2 | 2, and the fan flag `0x01F83561` |
| 6 sprite | 2 | 0 | 2 |

### Vertices, indices and the batch

XYZF2 and XYZ2 raise the phase, saturating at the requirement, flush at 682 vertices, and convert
the vertex with `0x00210230` into the 48-byte slot `0x01FC3620 + n × 48`. On the packed path X and Y
are the low 16 bits of each dword times 0.0625 (the GS 12.4 fixed point) and Z is bits `0xFFFFFF0` of
the second qword, clamped to the upper bound `0x01FD3664` and then the lower `0x01FD3660`; with
`0x01FD3611` set three floats are taken directly.

`0x0020EA50` then builds `(X, Y, Z, 1)`, writes the
four RGBAQ bytes `0x01FC361C` to `0x01FC361F` as unnormalised floats at `+0x10`, red `0x01FC361F` at
`+0x10` through alpha `0x01FC361C` at `+0x1C` (`0x0020EABF`-`0x0020EACE`), multiplies by the matrix, `v = v × M` with
`M` at `0x01FD3620` through `0x00202B70` (`0x0020EAD3`), and divides x, y, z and w by w, `x = x / w` to `w = w / w`
(`0x0020EAD8`-`0x0020EB0C`).

It then copies the UV pair selected by the FST bit from `0x01FCB600` to `0x01FCB60C` into `+0x20`: with FST set U
`0x01FCB60C` and V `0x01FCB608` (`0x0020EB1A`-`0x0020EB2F`), with it clear S/Q `0x01FCB604` and T/Q `0x01FCB600`
(`0x0020EB3A`-`0x0020EB4F`).

The vertex counts only when bit `0x800000000000` of its second qword (ADC) is clear and the phase has reached
the requirement; the phase then drops to the carry and the index arm runs, appending 16-bit
indices to `0x01FCB610` (count `0x01F83564`) with n the new vertex count: a point writes n-1; a line
or line strip n-2, n-1; a triangle or triangle strip n-3, n-2, n-1; a fan 0, n-2, n-1; a sprite
duplicates its two corner vertices into four and writes six indices for two triangles.

`0x0020EC80` flushes: when indices are pending it selects state through `0x0020ED30` and submits through
`0x0020EB60(lastIndex + 1, device)`, lastIndex being the last index written (`0x0020EC9A`) and the device the one at
`0x01FC35F8`, then zeroes the index count;

when the vertex count `0x01F83568` is 682 or more (`0x0020ECC2`) it moves the primitive's unfinished trailing vertices to
the front (for a fan, after vertex 0): the last carry `0x01F8356C` vertices, or all of them when there are fewer, become
the new count (`0x0020ECDE`, `0x0020ED1A`), and a fan with more vertices than the carry keeps vertex 0 and moves carry - 1
behind it (`0x0020ECEC`-`0x0020ECF3`).

Among the state `0x0020ED30` selects, `0x0020FF10` decodes the GS TEST register of the current context
(`0x01FC35C8`, or `0x01FC35D0` while `0x01FC3601` is set): ATE bit `0x1`, ATST bits under mask `0xE`, AREF bits under mask `0xFF0`,
AFAIL bits `0x1000` and `0x2000`, DATE bit `0x4000`, DATM bit `0x8000`, ZTE bit `0x10000`, ZTST bits `0x20000` and `0x40000`, into `0x01FD3668` to
`0x01FD3684`. It hands the device (its vtable `+0x88`) the alpha test with AREF / 255 and the method
`0x0020F2A0(ATST)`, which maps 1 to 7 onto 7, 4, 6, 3, 2, 1, 5 and anything else onto 0.

`0x0020EB60` looks TEX0_1 or TEX0_2 (by the CTXT bit `0x01FC3601`) up in the 16-byte texture table `0x01F83580` by `(TEX0 >>
37) & 0x3FFF` when TME is set and the format field is at least `0x300000`, copying the entry to `0x01FD3688`
(`0x0020EBCD`); with TME set and a lower format it zeroes the first eight bytes of `0x01FD3688` instead (`0x0020EBD6`), and
with TME clear it leaves `0x01FD3688` as it is.

It copies the vertices and indices into buffers from the device object's slots `+0` and `+0x10`, and draws through its
slot `+0x28` with the index kind, the result of slot `+0x18`, the index count, the result of slot `+8` and the vertex
count (`0x0020EC67`). The device object is the one `0x00210320` stored at `0x01FC35F8`, the embedded
`PrimitiveRendererD3D11` at `0x02CC1CD0`.

## Layouts

The working words below VU memory (`0x02064B00`, `0x330` bytes) that have a role beyond a microprogram register; the other cells and index words are rows of the state table (Working cells and index words):

`Vu1RegisterBank02064B00` (`0x330` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A0` | `f32[4]` | cellA0 | float working cell 8 of the 32 at `0x02064B20`-`0x02064D1F` (`0x02064BA0`), a microprogram register like its neighbours: `0x002F0280` stores a whole cell into it (`0x002F0868`, `0x002F0AC4`); 316 direct references in 35 functions (154 reads, 162 writes, 0 address loads) |
| `+0x160` | `f32[4]` | tagStage | float working cell 20 of the 32 at `0x02064B20`-`0x02064D1F` (`0x02064C60`): the packet leaf `0x004EF860` stages here the cell named by the index word `0x02064DD0` (`0x004EF866`-`0x004EF8C8`) and copies its upper twelve bytes beside the GIF tag it writes (`0x004EF8DB`-`0x004EF8F2`); 519 direct references in 45 functions (262 reads, 257 writes, 0 address loads) |
| `+0x190` | `f32[4]` | cell190 | float working cell 23 of the 32 at `0x02064B20`-`0x02064D1F` (`0x02064C90`), a microprogram register: `0x002F0280` stores a lane (`0x002F058B`) and `0x004758E0` a whole cell (`0x0047699A`); 582 direct references in 37 functions (253 reads, 329 writes, 0 address loads) |
| `+0x1A0` | `f32[4]` | cell1A0 | float working cell 24 of the 32 at `0x02064B20`-`0x02064D1F` (`0x02064CA0`), a microprogram register: `0x002F0280` stores whole cells into it (`0x002F04DC`, `0x002F0706`); 669 direct references in 40 functions (345 reads, 324 writes, 0 address loads) |
| `+0x2B0` | `u8[4]` | outputCell | the 16-bit index word `0x02064DB0` in its 4-byte slot: the VU memory cell where the next GS packet's GIF tag goes; `0x004EF860` writes the tag there (`0x004EF88B`-`0x004EF8B6`) and after the callback moves it to `0x02064B0C` + `0x02064DB4` (`0x004EF913`-`0x004EF924`); 196 direct references in 67 functions (69 reads, 115 writes, 12 address loads) |
| `+0x2B4` | `u8[4]` | bufferOffset | the 16-bit index word `0x02064DB4` in its 4-byte slot: `0x004EF860` sets it to `0x02064B0C` + `0x2A8`, or + `0x168` when `0x02064B0C` differs from `0x02064DB0` - `0x168` (`0x004EF8B8`-`0x004EF902`), alternating the packet between two halves of VU memory, and to the new `0x02064DB0` + 1 after the callback (`0x004EF92B`-`0x004EF92E`); 341 direct references in 68 functions (120 reads, 221 writes, 0 address loads) |
| `+0x2B8` | `u8[4]` | loopCount | the 16-bit index word `0x02064DB8` in its 4-byte slot: the packet's loop count, which `0x004EF860` writes into the GIF tag with the end-of-packet bit `0x8000` (`0x004EF89C`-`0x004EF8B6`) and then resets to the word `0x02064B0C` (`0x004EF8C0`); 244 direct references in 63 functions (100 reads, 144 writes, 0 address loads) |
| `+0x2C0` | `u8[4]` | index2C0 | the 16-bit index word `0x02064DC0` in its 4-byte slot, a microprogram integer register: `0x002F0280` stores it (`0x002F033E`) and reads it back (`0x002F154E`); 110 direct references in 26 functions (50 reads, 60 writes, 0 address loads) |
| `+0x2CC` | `u8[4]` | index2CC | the 16-bit index word `0x02064DCC` in its 4-byte slot, a microprogram integer register: `0x002F0280` stores it (`0x002F07FA`) and reads it (`0x002F09FB`); 260 direct references in 50 functions (44 reads, 208 writes, 8 address loads) |
| `+0x2D0` | `u8[4]` | tagTemplateCell | the 16-bit index word `0x02064DD0` in its 4-byte slot: the VU memory cell holding the GIF tag template whose upper twelve bytes `0x004EF860` copies beside each tag (`0x004EF866`-`0x004EF886`); 152 direct references in 74 functions (31 reads, 121 writes, 0 address loads) |
| `+0x2DC` | `u8[4]` | index2DC | the 16-bit index word `0x02064DDC` in its 4-byte slot, a microprogram integer register: `0x002F0280` stores it (`0x002F13DB`), as does `0x004758E0` (`0x004766D2`); 105 direct references in 41 functions (36 reads, 69 writes, 0 address loads) |
| `+0x2E0` | `u8[4]` | index2E0 | the 16-bit index word `0x02064DE0` in its 4-byte slot, a microprogram integer register: `0x002F0280` stores it (`0x002F046E`, `0x002F0496`); 89 direct references in 31 functions (29 reads, 60 writes, 0 address loads) |
| `+0x2E8` | `u8[4]` | index2E8 | the 16-bit index word `0x02064DE8` in its 4-byte slot, a microprogram integer register: `0x002F0280` stores it (`0x002F02DC`, `0x002F13BB`); 66 direct references in 26 functions (4 reads, 62 writes, 0 address loads) |

```python
VIF command word     [31:24] code, [23:0] parameters
MPG on this port     0x4A000000 | addr, 4 skipped bytes, u64 x64 function pointer (the console: NUM microcode words)
UNPACK word          [27:24] format (vn << 2 | vl), bit 0x8000 add TOPS, bit 0x4000 unsigned, [23:16] NUM, [9:0] address
program call         0x02068E30[ max { a in 0x02088E50 : a <= requested } ](callback, context)
VU memory            0x02064E30 + cell * 16, cell 0..1023; TOP 0x02064E1C, TOPS 0x02064E28
VIF registers        0x02088E30 BASE, 0x02088E34 OFFSET, 0x02088E38 status (bit 0x40 = second buffer), 0x02088E3C WL, 0x02088E40 CYCLE, 0x02088E44 count, 0x02088E50 list
template object      +0 u16 word, +3 kind (0x10 plain, 0x30 registered), +4 record handle; packet words from +8
record table         0x02EAF930 + n * 16: u32 0x4A000000 | addr, u64 program; count 0x02EB37B0
GiVmax (0x640)       +8 flag, +0x10 ctx, +0x18 chunk page size (1,024), +0x1C chunk count, +0x20.. 64 chunk pages of {ptr, len} x16 B
                     +0x220/+0x224/+0x228 GS copy list, +0x428/+0x42C/+0x430 flag list, +0x630/+0x634 device state, +0x638, +0x639 bytes
GIF tag              [14:0] NLOOP, 15 EOP, 46 PRE, [57:47] PRIM, [59:58] FLG, [63:60] NREG, [127:64] REGS (4 bits each)
vertex (48 B)        +0 x y z w (after the divide), +0x10 r g b a, +0x20 u v; buffer 0x01FC3620, 682 slots; indices 0x01FCB610
```

## Shipped data

| Fact | Value |
|---|---|
| boot template calls | 77 (28 + 49), 76 builders, 77 objects |
| template builders that register a program | 37 |
| registrar call sites | 104: `0x003A34D0` 45, `0x003A35E0` 27, `0x003A33B0` 22, `0x003A2F70` 10 |
| distinct microprograms | 57: 35 by template, 44 by registrar, 22 by both |
| functions calling the sticky-flag helpers | 40: 33 microprograms and 7 shared subroutines |
| GS registers honoured | 20 |
| vertex batch | 682 slots of 48 bytes; only the fan arm range-checks the index count (`0x8000` bytes) |
| GS coordinate scale | 0.0625 |

## Operations

At boot: `0x0022CB90`, then the two hubs build the 77 templates. On a draw that uses the layer: a
registrar or effect finaliser builds a `GiVmax`, `0x001DB550` runs its packets at once (MPG installs
the program, UNPACK fills VU memory, MSCAL runs the program, each GS packet is copied), and the
frame's render pass list later runs `0x001DB3D0`, which replays the copies into D3D11 vertex and
index batches.

## State

VU memory and the VIF registers (one set, shared by every packet), the program table and its
list (reset per packet list), the GS replay's register words at `0x01F83561` to `0x01F8357F` and
`0x01FC3580` to `0x01FC3610`, the vertex and index buffers, the texture table `0x01F83580` and the
device pointer `0x01FC35F8`.

### The GS register words

The replay keeps each GS register it honours in a word of its own. The A+D handler `0x0020FCA0` stores a register
by its number, and the PACKED handler `0x0020F3E0` stores the descriptors a 4-bit field can name. `0x0020ED30` and
`0x0020FF10` read the words when they select D3D11 state, choosing the `_1` or `_2` register by the `CTXT` bit
`0x01FC3601`.

| Global | Register or field | Used for |
|---|---|---|
| `0x01FC3588`, `0x01FC3590` | `TEX0_1`, `TEX0_2` | the texture lookup in `0x0020EB60` and `0x0020ED30` |
| `0x01FC35B8`, `0x01FC35C0` | `CLAMP_1`, `CLAMP_2` | the calls of `0x0018AA30` and `0x001EE650` |
| `0x01FC35D8`, `0x01FC35E0` | `ALPHA_1`, `ALPHA_2` | the blend `0x001EE650` |
| `0x01FC35E8`, `0x01FC35F0` | `ZBUF_1`, `ZBUF_2` | stored; no instruction reads them |
| `0x01FC3604` to `0x01FC3606` | `FOGCOL` red, green, blue | stored; no instruction reads them |
| `0x01F8357D`, `0x01F8357E` | `PRIM` bits `FGE`, `ABE` | `ABE` goes to the device's slot `+0x78`; `FGE` is never read |
| `0x01FC361D`, `0x01FC361E` | `RGBAQ` blue, green | the vertex colour in `0x0020EA50` |
| `0x01FD366C` to `0x01FD3680` | `TEST` fields `ATST`, `AREF`, `AFAIL`, `DATE`, `DATM`, `ZTE` | the alpha, destination-alpha and depth tests |
| `0x01FC3608` | the data qword of the A+D register being handled | the `PRIM` and `FOGCOL` arms |

Four more words steer the replay:

- `0x01FC3603` is 1 when the D3D11 state must be selected again; `0x0020ED30` selects state only then and clears it.
- `0x01FC3607` is 1 when the last texture has base pointer 0; the replay then ends with the device's `TEXFLUSH`
  slot `+0x128`.
- `0x01FD3610` holds the command's flag `+0x639`; while it is set, texture id `0xE00` is looked up as `0xDFF`.
- `0x01F83560` holds the command's byte `+0x638`; while it is set, the GS's ordinary alpha blend `(Cs - Cd) × As + Cd`
  becomes D3D11's MAX operation. Type `0x02`'s draw `0x004490D0` and `0x004559C0` set the latch `0x01FD3698` around their
  sprite draws (through `0x003A3D00`, a jump to `0x002105D0`); `0x001DB840` copies it into `+0x638` (`0x001DBA0A`-`0x001DBA12`),
  and slot 1 `0x001DB3D0` stores `0x01F83560` through `0x002105B0`.

`0x01FD3688` is the copy of the texture-table entry `0x0020F250` returns for the current `TEX0`: for a
format field (`TEX0 & 0x3F00000`) of `0x300000` or more it copies entry `(TEX0 >> 37) & 0x3FFF` of
`0x01F83580` there (`0x0020F27F`), otherwise it zeroes the first eight bytes (`0x0020F287`), and on both
paths it returns `0x01FD3688`; `0x0020EB60` makes the same copy while TME is set. `0x01F82D0C` is the
second VIF word of the scratch chunk `0x01F82D08`, which `0x001DB840` rewrites on every call.

### The microprograms' constant vector

`0x01E02830` holds `(0, 0, 0, 1)` in the image and is the microprograms' constant register. `0x0022CB90` writes all
four lanes at boot: x and y 0 (`0x0022CBDF`), z 0 (`0x0022CBEA`) and w 1.0 (`0x0022CBA5`). `0x0022CC20` copies
`(0, 0, 0, 1)` back from `0x008C5FD0`, and a program calls it after it
stores into the vector: `0x004BF500` stores lanes x and y at `0x004C07DA` and `0x004C07E2` and calls it at
`0x004C07EA`.

### Working cells and index words

Below VU memory, `0x02064B20` to `0x02064D1F` are 32 float working cells of 16 bytes, and `0x02064DB0` to `0x02064DE8`
hold 16-bit integer words, the page's cell indices, four bytes apart. The microprograms use them as their
registers: a program loads a cell or word, computes, and stores the result for its next instruction. The
shared subroutines receive the cells' addresses: `0x004B1190` passes `0x02064CB0` (`0x004B3E86`) to `0x004B9D80`
(`0x004B3EB9`). A cell's value lives only until the next program overwrites it.

The halfwords `0x02064B12` to `0x02064B1E`, just below the cells, are 16-bit integer words of the same kind.

### The lens-flare program's words

The lens-flare microprogram `0x004C0EA0`, which the lens-flare draw `0x00461270` installs (`0x004620E3`), keeps its
integer words in `.data` at `0x02CA7F40` to `0x02CA7F78` instead of in the index words:

- `0x02CA7F58` walks the input records, 3 cells each, and `0x02CA7F50` counts the records left in a pass;
- `0x02CA7F68` and `0x02CA7F6C` walk the current record's parts, 4 cells and one count per part;
- `0x02CA7F48` is the output cursor: it starts at cell `0xBC` and moves 9 cells per part;
- `0x02CA7F4C` counts the parts, and at the end the program writes it, with the end-of-packet bit `0x8000`, into
  the GIF tag in cell `0xBB` (`0x02CA7F44`); `0x02CA7F54` holds the packet's first cell, `0xB9`.

### Every written word

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [ps2-vif1-vu1-emulation-state.tsv](ps2-vif1-vu1-emulation-state.tsv), one per address; its `place` names the register, field, cell or lane at that address, for example `PRIM ABE`, `TEX0_1`, `cell 0x02064B20 lane z`, `index word` (22 rows) or `lens-flare program word` (12 rows) | the row's `type` | the row's `start` | the row's `meaning` | the row's `set_by` | the row's `read_by` |

## Modding notes

- Only the twenty registers above reach the PC. A packet that relies on FRAME, SCISSOR, XYOFFSET,
  TEX1 or PRMODE has that part ignored, which is where to look for PS2-versus-PC differences.
- The templates are immediates in the builders; patching a word changes the packet every draw
  from that template sends.
- An MPG word in a hand-built packet needs 4 skipped bytes and then an x64 function pointer, not microcode.
- `0x0022C930` empties the installed list before each `GiVmax` runs, but not the program table: an MSCAL with no install
  at or below its address calls the table entry for address 0, which keeps the last program installed there by any
  list.

## Related

- [PS2 CPU emulation](ps2-cpu-emulation.md): the vector unit 0 register bank the other
  translated assembly uses, and the boot routine shared with this layer.
- [Game application](game-application.md): the render pass list that drains the commands.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Menus and HUD** (explained on [menu lists](../Menus-And-HUD/menu-lists.md))

| Function | | Functions |
|---|---|---|
| `0x00397910` | is called by | `0x00368010` |

</details>
