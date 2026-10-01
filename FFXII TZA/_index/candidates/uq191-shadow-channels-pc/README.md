# UQ-191: what the shadow-object channels control on screen - nothing, in the PC build (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UQ-191):** "What any channel controls on screen." The ramp channels are floats in the character
shadow-object pool (`02B40528`, 160 × `0xE0`). Earlier narrowings mapped what the shadow draw `003B62D0` does with each
channel:
- channel 0 is the rotated anchor offset;
- channel 1 is the quad's own rotation;
- channel 2 scales the quad;
- channel 3 is a gain into `out+0x28`;
- `+0x43` is a cross-fade weight.

The residual was the name of the draw's output fields.

**Answer: in the PC build the channels control nothing visible.** Their one consumer, the shadow draw, writes only into
the PS2 command ring, and nothing on PC reads that ring. The mapping above is what the channels meant to the PS2 blob
shadow. `out+0x28` is a component of a VU data vector in a packet no PC code consumes, so it has no PC-observable name.

## The chain, static (`uq191_consumers.py`, 5 checks, FAILS 0)

1. **Who reads the pool.** The pool is referenced only inside the shadow module, 21 functions in
   `003B5600`..`003B6C00`, including the pool allocator `003B56D0` (C1).
2. **Who consumes the channels.** Only `003B62D0` reads current channel values it does not also write. The others are
   the tween steppers and setters (C2).
3. **Where the draw's output goes.** `003B62D0`'s one caller is `003B6020`, reached through the thunk `00521440`.
   `003B6020` calls only `003B62D0` and the ring submit `003A1DB0`, and copies the 0x50-byte output record into the ring
   at the current cursor. The ring descriptors are at `02EBEFC0`, image base + `0x2D9EFC0` indexed by `02EBEFF0` (C3).
4. **What the ring does with it** (C4):
   - The submit reads the descriptor's base and cursor only to count.
   - Its publisher `0036F360` reads only the last qword before the cursor, the DMA tag. It then writes offset, count and
     `0x100` into the single dword `02EBA3F8`, so no address survives for a consumer.
   - The VIF1/VU1 page's section 2 records the same absence for this ring, its staging pointer and the kick cell, and
     this record extends that census to image-base-relative forms. The 37 functions that reference the descriptors are
     emitters (they take the cursor, write, and submit), the submit, the setup (`003A1D50`, `003A1E10`) and the
     write-buffer getter `005044B0`. That classification is FABLE's reading of the enumerated list, not a machine check.
5. **The shared scratchpad.** The rings are carved from the emulated scratchpad `[01FD4A78]` (`004FE420`:
   base + offset × 16). The two other functions that address it at `+0x1000` / `+0x2000`, `003ABD50` and `003AC110`,
   write those areas before reading them (C5).

## Limits

- **Static only.** Nothing was executed, and "no consumer" is bounded by the census above: rip-relative and
  image-base-relative references to the ring descriptors, plus the scratch-base users.
- **The PC's own shadows.** Whatever draws character shadows on PC does not read these channels (C1/C2). How the PC
  draws its shadows is outside this row.
- **The PS2 meanings stand as mechanism.** They describe what the channels would drive if the ring were consumed.

## Files

- `uq191_consumers.py`, the control.
- `consumer-check.md`.
