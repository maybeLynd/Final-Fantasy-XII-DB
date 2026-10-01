# CG-6 — the render-command double buffer has no reader in this executable

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `cg6_no_consumer.py` (7 checks, FAILS 0).

CG-6 asks where the GIF command buffers are consumed: the double buffer `02EBEFC0` / `02EBEFD8`, with the current
index in `02EBEFF0`, carved from the arena at `01FD4A78`
([what happens between two frames](../../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §2.5).
The row was bounded by seven refuted leads. OPUS added an eighth on 2026-09-13, the arena alias `01EF9438`, which was
never read through.

## The answer

**Nothing in this executable reads a finished batch's records.** The only code that touches a finished half is the
submit, and it reads one dword.

**The descriptor.** Each half is `{begin, cursor, capacity, initialised}` at `+0`, `+8`, `+0x10` and `+0x14`.

**The submit (C1).** `RenderCommand_SubmitCurrentBufferAndSwap` (`003A1DB0`) is the only place the finished half is
formed:
- it flips the index;
- it counts the finished half's records as `(cursor − begin) >> 4`;
- it passes `(begin, count)` to `0036F360`;
- it resets the new half's cursor to its begin.

**What `0036F360` does with the batch (C2).** It calls nothing and reads exactly one dword of it: the last record's
first dword (`0036F372`). It uses that to append, or overwrite with, an end tag `{0x10000000, 0}`. Everything else it
writes goes to the single cell `02EBA3F8`: the address masked `& 0x3FF0`, the count, then `0x100`. That is UQ-211's
reading on the handshake page — PS2 DMA channel registers (MADR, QWC, CHCR) collapsed onto one word. The DMA
controller that would walk the chain is not in this image.

**Every other access appends (C3–C5, C7).**
- **Current half only.** The 36 functions that reference the pair or its index form the descriptor from the *current*
  index at 21 sites. Only the submit forms the finished one (C3).
- **Begin reads.** The current-descriptor getter `005044B0` has seven callers. They read `begin` in only two ways
  (C4):
  - as an end bound, `begin + capacity × 16`;
  - as a used count, `(cursor − begin) >> 4`, taken just before the flush `00504450`. The flush appends the end tag
    and tail-jumps to the submit.
- **The shared emitter** `003A22A0` reads the cursor `[desc + 8]` and advances it by `0x10` (C5).
- **Every site that passes the descriptor on** passes it to that emitter (C7): `00474600`, `0051BC70`, and
  `003649A0` through the thunk `00474650`.

**OPUS's alias lead, followed (C6).** `01EF9438` is pointed at one of two things by `00426090` / `004262E0`:
- the arena itself (`00370DF0`);
- a static buffer at `02AD9EC0` (`00370DE0`).

Its readers `00370BD0` and `00370CD0` do not walk command records. They write 12-byte list nodes
`{index, prev, next = −1}` and a count at `+0x1804` into whichever memory the alias names. The render-record code is
borrowing the arena as scratch.

## What this changes in the row

The row's seventh lead said the mid-draw flush submits "to `005C5230`". OPUS then showed that is the image's shared
return-zero, which proves nothing specific. This record does not rest on `005C5230`. The submit path that exists is
`003A1DB0` → `0036F360`, and it hands the records to nothing.

## What this does not claim

- **The staging buffers at `[02F8F2E0]`.** `003A2D80` / `003A2E30` copy into them; that is the handshake page's other
  open end and not this buffer.
- **What the records would have meant** to the absent receiver.
- **How the game draws anyway.** The VIF page's `GiVmax` replay path through `00210320` is a separate route.
- **Indirect reach beyond the census.** The census is every function holding a rip-relative reference to the pair or
  its index, plus the functions they hand the descriptor to. A read reaching the arena by an address built with no
  such reference would not appear.
