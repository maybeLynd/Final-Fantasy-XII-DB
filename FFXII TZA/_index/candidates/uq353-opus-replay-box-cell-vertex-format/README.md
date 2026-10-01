# UQ-353: the box cell drawer emits 48-byte immediate-mode vertices as triangle strips (OPUS, 2026-09-26)

**Question.** What is the exact vertex format `002DC7F0` emits?

**Answer.** It builds four 0x30-byte `ImmediateVertex` records on its stack and hands them to the strip emitter
`00181460(vertices, 4)`. That emitter feeds the n-2 triangles, vertex by vertex, to `001B06D0`, which copies each
record into the immediate renderer's current batch. The record's fields are fixed by the code that consumes it at
flush.

| off | type | field | who fixes it |
|---|---|---|---|
| `+0x00` | float | x | the consumer passes `+0x00..+0x0C` as one position to `001FBBF0` (`001FBBB0`). The cell stores `(v*M).x / (v*M).w` |
| `+0x04` | float | y | `(v*M).y / (v*M).w` |
| `+0x08` | float | z | 0.0 from the cell |
| `+0x0C` | float | w | 1.0 from the cell, after it has already divided x and y |
| `+0x10`..`+0x1C` | int32 x4 | red, green, blue, alpha | one byte each, widened: the colour's bytes 0-3. At flush `002157C0` outputs `c * (1/128) * scale * (1/128)`, with the scale at the batch object's `+0x144..+0x150`; `0x80` = 1.0 |
| `+0x20` / `+0x24` | float x2 | u, v in texels | `002160A0` divides them by the bound texture's width and height (object `+0x28` / `+0x2C`). The cell stores 0 |
| `+0x28` | u32 | producer flags | the cell's flags argument, with bit 2 or bit 3 cleared. **The per-vertex conversion does not read it**: `00216160`'s three callees stop at `+0x24` |
| `+0x2C` | 4 bytes | unwritten | copied with the rest; no reader found |

**The strip shapes.**
- **Plain quad.** Taken for flags bit 2 (which is then cleared) or for no bit 3. One strip of four vertices: TL, BL,
  TR, BR, which is two triangles.
- **Corner blend.** Taken for bit 3 with bit 2 clear; bit 3 is then cleared.
  - The first strip is TL, BL, **centre**, BR.
  - The second (static: after the recorded boundary) is BR, TR, centre, TL (`002DCCE7`-`002DCE09`, then the emission at
    `002DD063`).
  - That makes four triangles around the centre.
  - The centre colour is `(((c0 + c1)/2 + c2)/2 + c3)/2` per channel. That is **weighted 1/8, 1/8, 1/4, 1/2 toward
    corner 3, not an average** (executed).

## The replay (`check.py`)

Evidence class **NATIVE-REPLAY** (unicorn), `live_game: false`. It uses `world.py`'s Session (the world of blocks
318-353) with **no application stub**.
- `002DC7F0` runs with every callee real up to `00181460`. That is a **recorded stop boundary**: its callee writes into
  the immediate renderer singleton `[01F811E8]`, which this world does not build.
- The vertex array is read from `rcx` at the boundary.

| case | what is asserted |
|---|---|
| Q | flags 0, identity matrix: four vertices at `(x,y) (x,y+h) (x+w,y) (x+w,y+h)`, z 0, w 1.0, channels = colour bytes 0-3, u,v 0, flags 0 |
| F | flags `0x14`: the same quad with bit 2 cleared (`0x10`). Flags `0x10` is carried |
| B | flags `0x18`: TL, BL, centre `(x+w/2, y+h/2)`, BR. The centre colour is the halving blend, and bit 3 is cleared |
| M | matrix {x*2, translate (5,7), w 2}: x = (2x+5)/2 and y = (y+7)/2. That is a row vector times the matrix, then a divide by w |

**Runs.** 5/5 pass, and two runs give an identical `result.json` (md5 `ca0bfa3e04c763d822cba51d1bf8dd2e`). `probe.py`
holds the shared runner and an exploratory listing.

**Declared:** `ImmediateVertex` (0x30) in `_types`. The strip emitter has 15 direct callers, including the live box
drawer `002DC290` and the rectangle primitive `002DBDD0`. Only `002DC7F0` is executed here; the record's fields come
from its consumer, which is the same for all of them.

**Not claimed:**
- what the other 14 producers put in `+0x28`;
- the batch object's colour scale values;
- the second blend strip as executed (it is static).
