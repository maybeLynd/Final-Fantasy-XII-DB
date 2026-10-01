# Render-record residue: 0042A580 read (its return is an uninitialised stack dword), and the shadow-float consumers pointed to UQ-191 (OPUS, 2026-09-30)

DD prose residue on [the character render record array](../../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md).
The page is not re-statused here. Two residue items remain, and they go to the batch-12 lane
(`Tools/work/OPUS/lane_brief_dd_b12.md`): the semantic names of the three model-declared special bones, and the meaning
of `+0x414`. This record closes two other items. Static, the certified image. The checker is
[`a580_check.py`](a580_check.py) (output [`a580_check.out`](a580_check.out), **`FAILS 0`**).

## 0042A580, the +0x294 bit-20 handler (OPUS)

- **A1.** `RenderRecords_ProcessDirtyState` `00427DE0` is its only caller. It runs it when `+0x294` bit 20 is set, clears
  the bit, and keeps the return in `edi` (`004282DB`-`004282F3`).
- **A2.** It walks the record's node (word `+0`), its first child (`+8`) and their subtrees (`0042EF90` with the callback
  `0042E4B0`) through the `0x740`-byte pool. Every per-node call goes to `0016D6A0`, which is `ret 0`, the same empty
  function as the other two handlers the page reads. Its only lasting store clears `+0x294` bit 20.
- **A3.** The flag it returns is its local `[rsp+0x78]`:
  - it is read at `0042A5EA` before anything stores to it;
  - it is set to 0 only when a visited node's `+6` is -1 (the `cmove`s, and `0042E4B0`'s `[rdx+0x58] = 0`, where
    `rdx` is the local context);
  - otherwise it returns an **uninitialised stack dword**, and so does the early exit (`0042A5A7`).
- **A4.** `00427DE0` uses `edi` as its rebuild flag: it is `00429E50`'s second argument (`00428465`) and the gate for
  `00427100` (`00428482`). A later handler in the same pass (bits `0x20`, `0x20000`, `0x800`) sets it to 1 and
  overrides it.

**In player terms:** the handler's per-node work is compiled out on PC, so what it leaves behind is a yes/no that
decides whether the character's render record is rebuilt this frame. That answer is "no" when a node in the chain is a
root (`+6` is -1), and whatever happened to be on the stack otherwise. The worst case is an extra or a skipped rebuild
of that record's derived state, not a crash.

## The pool-A tweened floats (OPUS)

The page's "what is not read: the consumers of the pool-A entry's tweened floats (the shadow draw itself)" is stale.
UQ-191 ([`uq191-shadow-channels-pc`](../uq191-shadow-channels-pc/README.md), FABLE) names the one consumer: the shadow
draw `003B62D0`, which is called only from `003B6020`. Its output goes to the PS2 command ring, and no PC code reads that
ring back. A pointer note was added in place.

## Limits (OPUS)

- A3 is a static reading of the frame. What value the stack slot holds at run time is not observed.
- The special-bone names and `+0x414` are left open here, as stated at the top.

## Review (OPUS)

Reviewed by SWE2-AUDIT-SPEC (request filed at publish).
