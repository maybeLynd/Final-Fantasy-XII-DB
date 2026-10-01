# UQ-46 — the last six object sizes, read from each packet's own length

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `uq46_packet_ends.py` (4 checks, FAILS 0).

**What was open.** The 2026-09-17 narrowing determined 42 of the 48 sizes from each builder's last store. It left six
objects: five whose last store stops short of the next pointer, and the last object `02AED330`, which has no next
pointer.

**The witness used here.** Every one of these objects is a startup-built PS2 packet template, and a packet states its
own length in one of two ways:
- **A DMA cnt tag.** `008631D0(tag, qwc)` writes the qword count and the id byte `0x10`. The packet then ends at
  `tag + 0x10 + qwc × 16`.
- **An UNPACK header.** Where the builder writes no tag, the `UNPACK V4_32` header at `+0x1C` covers `count × 16` bytes
  from `+0x20`. One closing qword follows; for `02AE1DA0` it is `MSCALF` / `FLUSHA` / pad.

| object | read from | packet end | the 2026-09-17 bracket |
|---|---|---:|---|
| `02AE06B0` | UNPACK, 24 qwords, then the closing qword | `0x1A0` | [0x1A0, 0x2F0] |
| `02AE1DA0` | UNPACK, 18 qwords, then `MSCALF` / `FLUSHA` | `0x150` | [0x150, 0x2E0] |
| `02AE4F20` | cnt tag at `+0x10`, qwc 197 | `0xC70` | [0xC70, 0x1A30] |
| `02AE9EE0` | cnt tag at `+0`, qwc 20 | `0x150` | [0x150, 0x390] |
| `02AEC660` | cnt tag at `+0x10`, qwc 30 | `0x200` | [0x10, 0x200] |
| `02AED330` | cnt tag at `+0x10`, qwc 17 | `0x130` | no next pointer |

**P2, positive control.** The same reading of `02ADFD00`, one of the 42 measured-exact objects, gives its measured
`0x190`.

**The five brackets resolve:**
- **`02AE06B0`, `02AE1DA0`, `02AE4F20`, `02AE9EE0` — the object is the lower bound.** The tail is the next variable
  (P3). The one function that references each tail touches nothing inside the object, and its references start at
  or past the packet end. For `02AE1DA0` they start 8 bytes later, at `+0x158`; for `02AE9EE0` exactly at `+0x150`,
  a 0xA0-byte template `003B6020` copies.
- **`02AEC660` — the object is the whole gap, and the census under-read it.** Its builder writes the header, then
  tail-jumps to a second builder with `rcx = object + 0x10`. That builder's tag and stores run to `+0x1FF`. The
  extent census did not follow the jump.
- **The addressing form matters (P4).** `003B6020` reaches `02AE9EE0 + 0x150` only through `rbx` = the image base
  (`lea rbx, [rip - 0x2960AD]`, then `[rbx + 0x29CA030]`). A rip-only reading of it starts at `+0x1F0`, and this
  record's first draft wrongly called `+0x150`..`+0x1EF` unreferenced on that basis. The control now counts both forms.
- **`02AED330`** is bounded by its own tag: `0x130`, which is the builder's extent.

With the 42 determined on 2026-09-17, all 48 sizes are now determined.
