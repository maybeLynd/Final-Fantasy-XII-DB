# UQ-204 — what each effect element type puts on screen

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Table: `uq204-element-type-emits.tsv` (65 rows). Control: `uq204_emits.py` (5 checks, FAILS 0).
Correction record: [`consumer-check.md`](consumer-check.md).

**The question.** UQ-204 asks what each of the 47 + 18 element types *is*, and which authored data selects it.
SWE2-DATA answered the selector on 2026-09-16: the `0xA00` chunk's record-header byte `+0xE`. This record answers the
other half, what each type puts on screen.

**The population** is the 65 types of
[`effect-type-methods.tsv`](../../../17-Presentation-Rendering/Effect-File-Formats/members/effect-type-methods.tsv) that
have at least one handler address. Each gets one row, with these columns:
- the type and its walk (or sub-walk), the method where drawing happens;
- `emits`: the emit path, followed by the call chain that proves it;
- `what`: a plain phrase for what the type is on screen;
- `evidence`: the instruction addresses of the key calls and constants;
- a confidence and a note.

**The answer, by emit path.**

| emit path | types | what they are |
|---|---:|---|
| GiPrim, through the constructor `008642A0` and the emit front ends | 7 | `0x01` a point (kind 0); `0x03` a line (kind 1); `0x04`, `0x06`, `0x07`, `0x08` grids of textured quads (kind 4 / `GiPolyGT4T`); `0x05` a resource mesh through the composer `004355D0` (triangles, quads, fans) |
| a sprite request to the frame drawers `00501A50` / `00502280` | 2 | `0x02`, `0x0A`: camera-facing sprites (`GiSprite` or quads) |
| a GiVmax command that runs a VU1 microprogram, registered by `003A34D0` / `003A35E0` / `003A33B0` / `003A2F70` | 31 | `0x60`–`0x62`, `0x65`–`0x67`, `0x80`–`0x96` except `0x81`, `0x8A` and `0x93`, and `0xA1`, `0xA2`, `0xA5`, `0xA7`, `0xAA`. Each row names the program the call passes. |
| the draw list through a type-specific `0054xxxx` pair, then `00540F40` / `00540DB0`, wrapped as a GiVmax | 12 | `0x68`–`0x6B`, `0x71`–`0x74`, `0xA3`, `0xA6`, `0xA8`, `0xAB` |
| a raw GS packet in the frame arena, not wrapped as a GiVmax (`003A3010`, `003A31A0`, or `00540C20` for `0xA9`) | 6 | `0x81`, `0x8A`, `0x97`, `0xA0`, `0xA4`, `0xA9`: see below |
| nothing: state only | 7 | `0x00` (the base element), `0x40`, `0x41`, `0x42`, `0x70`, `0xD0`, `0xD1` |

For the 43 VU1 types (31 registered plus 12 through a pair), *what shape* the program draws is **UQ-213**, which stays
open: "what each of the 47 microprograms draws". This table gives UQ-213 the element type behind each program it
names, so the residue sits in the register under that row, per program.

**The six raw-packet types — built, queued, and never submitted on PC.**
- Their walks build a PS2-style GS packet in the frame arena. `003A3010` / `003A31A0` append a sort-list entry whose
  `+0` is the packet and whose callback `+0x10` is 0: `rbx`, zeroed at `003A3094`, is stored at `003A310A`.
- The drain `003A3740` calls `+0x10` when it is set. Otherwise it submits `+0x18` only when `+0` is 0 (`cmp [rbx], r15`
  at `003A38CA`; `r15` zeroed at `003A37B0`). It passes over these entries.
- Their "mode 0" alternative, `003A2D80` / `003A2E30`, copies the packet into the scratch base (`[02F8F2E0]`, set from
  `[01FD4A78]` at `003A371A`). It then publishes the shared state word `02EBA3F8 = 0x100`, which
  [the shared command-state word](../../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md)
  shows is a console-side fossil.

**What the six build, read from their stores** ([`raw-packet-residue.md`](raw-packet-residue.md)).
- **The shared prefix.** `003A3010` and `003A31A0` lay the same prefix before every packet: a DMA `cnt` tag, VIF
  `DIRECT 3`, and a GIF tag with PRE 0, NREG 2 and A+D. It writes only `ALPHA_1` and `TEST_1`, and sets no primitive.
- **`0x81`, `0x8A`, `0xA0`.** Their packet blocks (`02AE0850`, `02AE5B90`, `02ADEDF0`) carry no GIF tag or PRIM write
  at all. The walks fill them with floats, colours and a matrix: microprogram-style input, not a drawable GS stream.
- **`0x97`** hands over the resource's own prebuilt packet (def `+0x2A0`: entry `+0x10` pointer, `+0x14` size).
- **`0xA4`** holds register values in the layout of `0xA9`'s `CLAMP_1` / `TEX0_1` / `ALPHA_1` / `TEST_1` block, but
  the tag and register-address halves are never written.
- **`0xA9`** is the one with a primitive: GIF tag PRIM `0x5C`, a textured, Gouraud-shaded, alpha-blended triangle strip
  with registers ST, RGBAQ and XYZF2. It comes from template `02AE8CF0`, built by `004795D0` (`00479613`, `0047961A`).

**The mode-0 copy is never read as packet data.** The scratch base is the static `01FE0000`, set at `0022A152`. Every
read of `[+0, +0x800)` in its 15 users reads a structure the same function or its callee wrote first: light lists,
the drain's own merge-sort temporary (`003A3A50`, which overwrites from `+0`), and render-submit command buffers.
The copiers themselves only write. The control: the same follower finds the sprite request at `+0x800` in all six
effect functions.

**So on PC these six types put nothing on screen,** whatever the PS2 build drew with them. The walks run and build their
packets, but no code submits or reads them. This is a static reading: the drain's branch is exact, and the scratch
census is a linear register follower.
- **One conditional read is not excluded.** `0037358C` reads dword `+0`, as another structure's field.
- **The staged range is wider than read.** `0x8A`'s copy reaches `+0x11C0`, and the reads in `+0x800`–`+0x11C0` are
  listed in the record but not classified.

**How the rows were made, and what checks them.**
- **Drafting.** A subagent pass (Claude Opus 5.5, under FABLE) drafted the rows, and a second pass read the raw-packet
  residue.
- **FABLE's own reads.** I checked the drain branch, the two `0xA4` / `0xA7` calls, `003A2D80`'s writes and the
  arena-base readers against the bytes.
- **The control** re-derives what the bytes decide:
  - **E1:** the population and walks.
  - **E2:** every cited address, call edge and call site, with planted false entries refused.
  - **E3:** each row's class agrees with the emitters the type's methods reach (depth-5 closure), and a "none" row
    reaches none.
  - **E4:** the `0xA4` / `0xA7` calls.
  - **E5:** the callback and drain instructions above.

**Corrections, all checked in the bytes.**
- **FABLE's own, corrected here.**
  - [The dispatch page](../../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md) said, on
    2026-09-20, "`0xA4` and `0xA7` emit nothing … put nothing on the draw list". Both do: `00522300` calls `003A3010`
    at `005227C5` (a raw packet), and `00526A10` calls `003A34D0` at `00526D2D` (program `004ECC50`).
  - The page's own later interior citations already name both calls.
- **Routed to FRONTIER.**
  - The VU1 region census (`members/vu1-region-functions.tsv`) classes four functions as VU helpers, not
    microprograms: `0049B9E0`, `0049D540`, `004A0090`, `004B0230`. Each is passed as the program to `003A33B0` (in
    `r9`) or `003A2F70`: by type `0x8E` at `00456AC7`, `0x8F` at `004573DF`, its worker at `00457928`, and `0x95` at
    `0045B60A`.
  - The 0x80–0x97 page places type `0x90`'s `+0x330 == 0` arm inline; it is its own function, `00458010` (program
    `004A33B0`).
  - The transform-workbench page calls `0039E6B0` a "byte-channel vector converter". It also builds a 3-vertex GiPrim
    of kind 3, a triangle.
