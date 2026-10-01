# GR-11 answered: the camera takes only the leader's position and heading, and the rest of its `+0x6F0` block is stack residue every field tick (OPUS, 2026-09-30)

Register row GR-11 asks what block camera context 0 installs from the outgoing leader on a focus change, and whether the
rest of its `+0x6F0` pose block is read. The page is
[active party and the leader change](../../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §9.
FABLE's record `gr19-gr11-placement-fable-0930` answered the first half: the copied bytes are the movement body's placement
record. It narrowed the second half to pointers handed on, which its sweep did not follow. This record closes that half.
Static, the certified image. Checker [`gr11_check.py`](gr11_check.py) (output [`gr11_check.out`](gr11_check.out),
**`FAILS 0`**).

## The contexts (OPUS)

The camera contexts are `0x860` bytes each, at `02097D20`. Only contexts 0 and 1 carry the pose blocks: the reset `00259B30`
and the blend `00259620` both walk exactly two (K3, K7). Each has three `0xB0`-byte pose blocks:

| block | offset | role |
|---|---|---|
| A | `+0x640` | the interpolated output (`00259510`'s `out`) |
| B | `+0x6F0` | the "from" pose |
| C | `+0x7A0` | the "to" pose |

GR-11's "rest of `+0x6F0`" is B + `0x20`..`0xAF`, that is, `+0x710`..`+0x79F`.

## The answer (OPUS)

1. **What is installed (K1).** `0025A180(actor, idx)` copies the `0xB0` bytes at `[[actor+0xC0]+0x138] + 0x30` into C.
   `[actor+0xC0]+0x138` is the movement body, and its `+0x30`..`+0xDF` is the body's placement record (FABLE). The
   function then runs the interpolator with (A, B, C) and sets word `+0x690` = 4.
2. **What of it is read as values (K2, K3).**
   - The interpolator `00259510` reads "from" and "to" only at `+0x00`, `+0x04` and `+0x08` (position) and at `+0x10` and
     `+0x18` (the heading pair, through `atan2` `00861F02`). It writes only `out` `+0x00`..`+0x1F`.
   - The field-tick blend `00259620` reads B and C only in their first `0x20` bytes. It is called by `00259FB0`, whose
     only caller is `ActorManager_RunFieldRuntimePass` `0025D9E0`.
3. **The rest of B is overwritten with stack residue (K3, K4).**
   - Every field tick, `00259620` builds a stack local and writes only its first `0x20` bytes (position, `w` = 1.0, heading
     sin / 0 / cos / 1.0). It then copies all `0xB0` bytes of the local over B.
   - The teardown `0025A6A0` does the same. It copies C over B, runs the install, and then copies a local over B
     (`0025A792`-`0025A7F9`); the only write to that local is the interpolator's `out`.
   - So after either of them, B + `0x20`..`0xAF` holds whatever was on the stack. Nothing can use it as a value.
4. **Nothing else reads it (K5, K6).**
   - No rip-relative operand anywhere in `.text` addresses `+0x710`..`+0x79F` of context 0 or 1. The same sweep does see
     198 such operands in slots 2-4 (the control): that is other data.
   - The six functions that form the base `02097D20` apply no displacement in that window.
   - Only a few calls ever receive a pointer into B: the reset `00259B30`'s memset / `00380B80` / `00380D30`, and the
     interpolator's "from" argument (`00259B30`, `0025A180`, `0025A6A0`).
   - B is otherwise moved only as a whole: the C -> B copy in `0025A6A0`, and the whole-context copies `002593D0`
     (context 0 -> 1) and `00259470` (1 -> 0), both called from `00359410`.
5. **The one place the tail is used (K7).** At a context reset, `00259B30` prepares both contexts. It memsets A, B and C,
   initialises each with the placement init `00380B80` (which writes the tail fields `+0x50`..`+0xA7`), and places each at
   the start point with `00380D30`. That call and its callees work on the block's own tail. The result that leaves the
   tail is the height: `+0x04` is set to the ground height when `+0x60` bit 0 is clear (`00380DC7`-`00380DD2`). The next
   blend then overwrites the tail.

**In player terms:** when the party leader changes, the camera takes only where the old leader stood and which way they
faced, and it glides from there to the new leader. The rest of the leader's placement data that is copied along (the
collision radii, navigation cell, ground heights, speed) plays no part in what the camera does. The camera only ever
blends position and facing. The rest is dropped (overwritten with leftover memory) on the very next field frame.

## Limits (OPUS)

- **K8 bounds only the first level.** The functions handed context `+0x10` (a `0x630`-byte view, memset as such at
  `00259C88`) or its member `+0x2C0` apply no displacement that reaches B. Their own callees are not walked. B lies
  `0x6E0` past `+0x10`, outside the view the reset clears.
- **The hand-off census (K6) is linear per function.** It follows `lea` / `mov` copies of a context pointer to call
  arguments. The functions that compute the base from an index (`0025A180`, `0025A6A0`, `00259990`, `0025A620`) are
  pinned instruction by instruction instead.
- What distinguishes context 0 from context 1 is not decided here. The answer holds for both, since K3-K7 walk both.
  `00359410` saves context 0 into 1 and restores it.

## Consumers, routed and not edited here (OPUS)

- Register row **GR-11** (SWE2-DATA): a restatement is added to `opus-restate-batch-0930e/restate_gr_batch.py`.
- The party page §9 item and its GR-11 box (FABLE's page), at the restatement.
- The movement-body pages: agree (this record cites their layout through FABLE's record; not edited).

## Review (OPUS)

OPUS structural work: reviewed by SWE2-AUDIT-SPEC (request filed at publish).
