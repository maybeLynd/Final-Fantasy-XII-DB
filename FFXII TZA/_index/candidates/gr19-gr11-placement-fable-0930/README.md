# GR-19 answered and GR-11 narrowed: the drop gate is "could the party leader stand here", and the camera install copies the leader's placement record (FABLE, Claude Opus 5.5, 2026-09-30)

Task `FABLE-GR19-GR12-0930`. Both rows are FABLE's, from the DD gameplay pages (`797b72780`), and follow SWE2-AUDIT-SEM's
review C4 / N2 ([review](../auditsem-review-dd-gameplay-0930/REVIEW.md), applied in
[`dd-gameplay-corrections-fable-0930`](../dd-gameplay-corrections-fable-0930/README.md)). Static only: every step below
is a byte-level read of the shipping image, with the load-bearing instructions pinned by [`gr19_check.py`](gr19_check.py).

## GR-19: what the defeat body's drop gate decides (FABLE)

The drop is rolled only on a nonzero answer from `00319490` (`00312588`-`00312597`).

1. **Who is tested.** `00319490` resolves the party focus actor (`003590D0` -> `003588B0` -> `00263E30`). It passes that
   actor's battle unit only while `02089340` bit `0x10` is set and the unit's first byte has bit 3. Otherwise it passes
   null, and `003377C0` answers 0 for a null unit. The position is `{x, y, z, 1.0}` (`01CEBBA8` holds `1.0f`).
2. **Gather** (`003377C0`). The radius is the first float of `ActorRuntime_GetClass3FloatPair` (`00265090`) on the unit's
   `+0x10` record. The actors near the point are listed by `00391D10`, or by `003920F0` when x is NaN (the `ucomiss`
   self-compares at `0033786A`-`00337889`); both take `0x20` slots and filter word `0x1C`.
3. **Who counts.** Each listed actor is skipped when it is the leader's own actor (`00337915`). It is also skipped when its
   unit's `+0xE68` record class (byte `+0x18` bits 1-3) is 1 while the leader's is 4. `00314EB0(leader, other)` then
   decides. At that call `rdx` still holds the listed actor: it is loaded at `0033790D`, and nothing between writes it
   (check R1). `00314EB0` compares the two actors' movement bodies (`[actor+0xC0]+0x138`) and returns 1 when their layers
   `+6` are equal and the leader's owner `+0x119` is zero or differs from the other's. That is the separation pass's
   pairing rule ([the movement body](../../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)
   2.7). A pairing actor goes to the relation query `00313F80`: a result of 1-3 increments `edi`, anything else `esi`.
4. **The answer.** A nonzero `esi` returns 0, and so does a nonzero `edi` (`0033798D`-`0033799C`, check R2). So any
   pairing actor refuses the drop, and the relation's value never changes the answer. With no pairing actor, or when
   `002EA7F0` refuses the leader (`0033785F`, which skips the gather), the answer is `00337700`'s.
5. **The ground** (`00337700`, check R3):
   - the corridor family's `LQUERY` `00391410`(point, point, radius) must hit nothing;
   - `00384130` must map the point's X/Z to a grid cell (`0xFF` = off-map);
   - `00336390`(point, max(radius A, radius B), leader `+0x1F4`) must return nonzero. It asks the point query `0032A6A0`
     (the corridor family's `DE6A0`, a `jmp 0026E100`) about the point and the four corners `(x ± r, z ± r)`, and all
     five must pass (check R4).

**In game terms:** a kill leaves no loot when the enemy dies where the party leader could not stand. That covers another
colliding body within the leader's radius, static geometry at the point, a point off the map grid, and ground that does
not pass the walkability query around the leader's footprint. There is also no drop at all while there is no party
focus unit with bit 3, or while `02089340` bit `0x10` is clear.

**Not named, and not needed for the answer:** the gather's filter word `0x1C`, what the `+0x1F4` mask selects in
`0032A6A0`, `002EA7F0`'s meaning, and the `+0xE68` class values 1 and 4.

## GR-11: what camera context 0 installs (FABLE)

`0025A180` (check R5) is called at `0025A76A` with the outgoing actor. It takes `[actor+0xC0]`, the movement context, and
its `+0x138`, the movement body from the pool at `02B4E4C0`
([the movement body](../../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) sections 1 and
4). It copies `+0x30` onward, 16 bytes per `movups`, into context `+0x7A0` (`0x860`-byte contexts at `02097D20`). Bytes
`+0x30`..`+0xDF` are the body's **placement record**:
- position, orientation and the two derived positions;
- displacement, the cell and attribute words, and flags;
- the radii and height copies, and the inner shape;
- the ground heights and the requested speed.

So the first question is answered, and the block's writers are the movement body's.

**The second question, narrowed.** [`gr11_pose_readers.py`](gr11_pose_readers.py)
([out](gr11_pose_readers.out)) sweeps `.text` for two kinds of access:
- every rip-relative operand into `+0x6F0`..`+0x79F` of the `0x860`-byte slots at `02097D20`;
- every in-window displacement in the functions that form the base `02097D20`.

The control is that `0025A180` is found forming the base, which it is. Contexts 0 and 1 have one direct reference,
`0025963F` `lea rdi, [ctx0 + 0x708]`. That is the loop `00259620` over contexts 0 and 1: it reads the block only at
`+0x6F0`..`+0x70F` (and `+0x7A0`.. beyond it), then rewrites all of `+0x6F0`..`+0x79F` with `movups`
(`00259742`-`00259797`). The base-forming functions touch the window only by passing `+0x6F0` on (`0025A1D5`, `0025A6EA`).
The other hits fall in slots 2-4, which lie past the two contexts the loop walks; they are other data (for example
`add eax, [slot2 + 0x720]` counters).

Still OPEN: whether a function handed a context pointer reads the `0x90` bytes. The sweep does not follow passed
pointers.

## Controls (FABLE)

run: gr19_check.py at 3cae47364 (FAILS 0; output [`gr19_check.out`](gr19_check.out))

- R1 has a positive control: the same register-write walk, extended to `0033796F`, must see the `mov rdx` at
  `0033795F` and the call at `00337956`. It does.
- The walk covers the address range between the load and the call. Every path between them lies inside that range: the
  branches go forward to `00337953`, or past the call to `00337981`.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`
affected: `Database/FFXII TZA/13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md`
affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`

- consumer: GR-19 - revised-here (ANSWERED). GR-11 - revised-here (narrowed; stays OPEN).
- consumer: the enemy-death page - revised-here (status line, the drop-gate bullet and its box).
- consumer: the party page - revised-here (status line and the section 9 item).
- consumer: DE-4 and the battle-locomotion page's placement-test paragraph - agree (the same `00317DE0` pair; not edited).
- consumer: the battle-unit field map's `00314EB0` note ("`byte[+0x119]` must be zero on the first or equal on both -
  returns 1 on a difference") - routed-to-board-note. As read at `00314F06`-`00314F13`, the test returns 1 when the
  first owner is zero or the two differ, and 0 when both are equal and non-zero. The note's wording can be read either
  way, and the page is outside this publish.
- consumer: the movement body pages - agree (this record cites their layout; not edited).

## Review

Semantic FABLE work, so the review goes to SWE2-AUDIT-SEM (request filed at publish).
