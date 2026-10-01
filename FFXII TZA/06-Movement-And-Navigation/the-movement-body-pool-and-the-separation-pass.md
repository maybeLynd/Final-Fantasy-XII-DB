---
system: The movement body — the 128-entry pool behind the movement context's +0x138, its placement record, and the per-tick pass that pushes overlapping actors apart
category: 06-Movement-And-Navigation
status: AUDITED — every box closed: cell 0046AD20's geometry (UQ-103) answered 2026-09-18 (x and z from the placement, cell size the body's larger radius, the centre the previous tick's mean of all bodies); the cell attribute fields and the mask table's fill (FZ-11) answered 2026-09-18: map id, ground type and the mj class, the table filled by the setmapid verbs; the mask bits 00314E10 honours (UQ-104) answered 2026-09-18: +0x114 is never written after the allocator zeroes it, 002EC5B0 is the only setter
owner_layer: native
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 63 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-movement-body-pool-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The movement body — the 128-entry pool behind the movement context's +0x138, its placement record, and the per-tick pass that pushes overlapping actors apart

> **Every placed actor owns one of 128 movement bodies.** The body is a `0x130`-byte entry of a
> pool at `02B4E4C0`, attached to the actor's movement context at `+0x138` when its presentation
> is set up and released when the actor is torn down. It carries the actor's field placement
> (position, ground height, cell), its collision shape (an ellipse from the character parameter
> block's body radius, a height and a base offset), a weight, and the bookkeeping of one system:
> **once per world tick the pool is walked, every body is tested against the bodies sharing its
> spatial cells, and overlapping pairs are pushed apart in proportion to their weights**. The push
> accumulates on the body and is consumed by the actor's next candidate position.

## 1. What the player sees

Actors do not stand inside one another. A party member who walks into an NPC, an enemy that
closes on the leader, two enemies converging on the same target — each pair slides apart, the
lighter body yielding more, and an actor flagged immovable does not yield at all. A body is not
pushed by actors on another layer, by a body its owner also owns, or by anything it does not
overlap vertically.

## 2. Native mechanism

### 2.1 The pool

`02B4E4C0` holds **128 entries of `0x130` bytes**, linked through `u16` indices — `+0` previous,
`+2` next, `+4` own index — with `0xFFFF` as the null link. `003DAE30` (from the actor-system
initialiser `00266D10`, `00267141`) threads all 128 onto the free list, zeroes each entry's `+0x10`
and `+7`, clears the 32 cell masks at `02B57CE0` and sets the two list heads to empty
(`003DAE3A`–`003DAF13`). `003DA8A0` unlinks the free head (**`02B57CC4`** — *corrected 2026-09-13; this read `02B525C4`, which is inside the pool*), links the entry onto the
active list (`02B57CC0`), clears its fields — `+0x100`/`+0x108` and the word `+0x88` among them
(`003DA958`–`003DA96E`) — and returns it; `003DAD00` reverses that (`003DAD09`–`003DAD6B`).

### 2.2 Attachment — created after the presentation, released with the actor

The only creator is `002E3500(record)`: it releases any existing body (`002E3515`–`002E352D`),
allocates one (`002E3538`) and stores it at the movement context's `+0x138` (`002E3546`); then
`00269EC0(record, 0)` sets the layer byte `+6` (`00269ED8`), `002682D0` copies the context's
`+0x151` bits 0–1 into the flags `+0x90` (`002682F6`–`0026831A`), `002685F0` copies the context's
float `+0x148` into the weight `+8` (`002685FC`–`0026861A`), and `00268380` sizes the shape
(§2.3). Its callers are the actor's presentation set-up `002E28E0` (`002E2C21`, after
`Actor_RefreshPresentationVisibility`) and `002E3580`, which releases the presentation, sets the
record's byte `+4` to 3 and re-creates (`002E3589`–`002E359A`). The two releasers are `002E3D00`
and `002E3AF0` (`002E3B9D`–`002E3BB5`), both reached from the per-type presentation release
`0025AB30` and `ActorSystem_ReleaseManagerRecords` — so a body lives exactly as long as its actor's
presentation.

### 2.3 The shape — `00268380(record)`

From ~~the secondary context (`+0xB8`) and the movement context (`+0xC0`)~~ the two contexts — *correction 2026-09-18 (FABLE): the labels are swapped; `+0xB8` is the **movement** context (the 0x230-byte region the initialiser plants at record `+0x120`, `00266B2D`) and `+0xC0` the **secondary** context (`00266B1F`), as [the context census](../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md) and the store have them; the offsets in the table below are right, so read its “secondary” as `[+0xB8]` and its “movement” as `[+0xC0]`* — by the record's class
bits (`+3 & 0xE0`, `00268386`–`0026838F`, `002683CD`–`002683E5`):

| field | value | site |
|---|---|---|
| `+0xF0`, `+0xF4` radii | the movement context's (`+0xB8`, per the correction above) float pair at `+0x50` — ~~the character parameter block's body-radius slot ([the FCP page](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md) §6.1)~~ *corrected 2026-09-18 (FABLE): the pair is the actor's radius pair (width, depth) × its x / z scale, written by `0026B2E0` from section 1's slots 67 / 68 (79 / 80 by field bit 15) of [the FCP page](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md) as the bind's default, or from the script's `setradius`; section 9's slot 2 is the battle unit's radius `+0x180`, a different consumer* | `002683A8`, `006C0520` |
| `+0xF8` heading | secondary `+0xA8` (class 2) or `+0x38` (class 1), else 0 | `00268442`–`0026846B` |
| `+0xFC` margin | 0 | `002684B0` |
| `+0xE0` height | secondary `+0xC0 × +0x24` (class 2) or `+0x68` (class 1), else 0 | `00268401`–`0026842B`, `003DB130` |
| `+0xE4` base offset | movement `+0x140 + +0x144` | `0026842B`–`00268437`, `003DB120` |
| `+0x40`…`+0x4C` orientation, `+0x94`…`+0x9C` copies, `+0xA0`…`+0xA8` the inner shape | `003DAF20(body, a, b, c)`: `sin`/`cos` of the heading; the radii and height copied; then `a % × +0xF0`, `c % × +0xF4`, `b % × +0xE0 + +0xE4` — 37 / 37 / 50 for the party class `0x60`, else the secondary context's bytes `+0x104`–`+0x106` | `0026846F`–`002684FD`, `003DAF3C`–`003DB000` |

The movement layer re-sizes the same way from `002E5E10` (`002E5F01`–`002E5F35`, radius through
`003DA850`).

### 2.4 The placement record at `+0x30`

The body's `+0x30` is the actor's **field placement**: `+0x30`/`+0x34`/`+0x38` position,
`+0x40` orientation, `+0x50` and `+0x60` two derived positions (`002ED6A0`: `0026E530` solves
`+0x50` from the position when the record's `+0xB` bit 6 is set, else copies `+0x60`,
`002ED6B2`–`002ED6E4`), `+0x70` the frame displacement, `+0x80`–`+0x8E` the cell words, `+0x90`
flags, `+0xAC` the ground height, `+0xC8` the requested speed. **The position is written by one
function**: `00380D30(&placement, &candidate)` resolves the field cell for the candidate
(`0026E500`, `00233050`, `00233110`), records the cell in `+0x82` — `-2` when the candidate's
cell bit is refused (`00380D75`–`00380D9F`) — copies the candidate's four floats in
(`00380DA1`–`00380DBA`), and stores the ground height at `+0xAC`, also into `+0x34` unless flag
`+0x90` bit 0 holds (`00380DC2`–`00380DD2`). The movement layer reaches it through
`003DB1B0(body, &candidate)`, which returns whether the body landed on a valid cell (`+0x82 ≥ 0`,
`003DB1C7`–`003DB1D9`; from `002E5C90`, `002E5D4C`).

**The cell words.** `00380D30` resolves the candidate's cell through `00233050` and `00233110`
(`00380D5E`–`00380D70`); a cell whose class byte `+0x80` is set in `00232090`'s blocked mask — kept
at `+0x8E` — is refused with `+0x82 = -2` (`00380D7E`–`00380D9F`). Then `003808A0(placement,
field)` (`00380DDD`) reads the cell record — `[field + 0x10] + cell × 32`, its attribute dword
`+0xC` — through the mask table at `0209A2D0` *(corrected 2026-09-17 from `020A22D0`; the reader's own `lea`)* (`00232020`: entry `(attr >> 13) & 0x1F` and entry
`0x40 + ((attr >> 3) & 0xF)`, each `{+0x110 clear, +0x114 set}`) and stores bits 13–17 at `+0x86`
(`003808ED`–`003808FD`), **bits 3–6 at `+0x88`** (`00380901`–`0038090A`), `00231F80`'s five bits at
`+0x8A` (`0038090E`–`00380923`), attribute bit 12 as flag `+0x90` bit 2 (`0038091A`–`00380927`)
and, when the second cell `+0x84` is valid, `00231890`'s height at `+0xC0` with flag bit 3 when it
lies above the ground height (`0038092F`–`00380958`); its tail steps `+0xB0` / `+0xB4` toward the
radius copies `+0x94` / `+0x98` by bounded increments, re-resolving the cell each step
(`00380980`–`00380A27`).

The integrator `Movement_IntegratePositionAndMeasureDisplacement` (`002E5610`) takes the body as
its second argument: with a body it uses `+0x70` as the displacement source and `+0x90` bit 4 as
the mode (`002E5659`–`002E5669`); without one it adds the caller's delta directly
(`002E566B`–`002E5698`). `Movement_SetRequestedSpeed` writes `+0xC8` (`0026D792`) and clears
bit 2 of the mask `+0x110` (`0026D79D`–`0026D7A8`); `002E5180` stores the ground height into the
secondary context's `+0xD4` (`002E521A`–`002E521F`).

### 2.5 Every frame — the body registers itself in its cells

`Movement_UpdateActorFrame` (`002E5030`) loads the body (`002E508A`), integrates, and — when
`002EA7F0` passes (the body's `+0xF0 > 0` and the record's `+8` bit 3, `002EA82B`–`002EA83F`) —
calls `003DB020(body, x, z, 0, &radii)` with the context's position plus its `+0x40`/`+0x48`
offset when `+0x107` bit 1 holds (`002E511A`–`002E5140`). `003DB020` sets `+7` (**active this
tick**, `003DB03D`), and if the two-globals gate `003B7730` holds, computes the body's **cell
bits** `+0x120` through `0046AD20(&cells, x, z, max(radii))` (`003DB04D`–`003DB068`) and ORs the
body's own bit into the 128-bit mask of every cell it touches (`02B57CE0`, sixteen bytes per cell,
`003DB06D`–`003DB0B1`).

### 2.6 Every world tick — the separation pass

`World_UpdateSimulationTick` first calls `003DAA40` (`003140C5`): the 32 cell masks are zeroed
(`003DAA43`–`003DAA77`) and every body's `+7` cleared (`003DAA79`–`003DAAA9`) — so a body that
does not register during the frame is not active for the pass. Its tail calls
`003DAC70(00314F30)` (`00314244`): for each body on the active list (`003DAC98`–`003DACE1`):

1. `003DAAB0(cells, index)` — the **candidate set** at `02B57EE0` is the OR of the masks of the
   body's cells (`003DAAC5`–`003DAAED`) with its own bit and every lower index cleared
   (`003DAAF5`–`003DAB49`), so each pair is visited once.
2. `003DAB50(…, body, callback)` — for every candidate bit, **or every bit still set in the body's
   pair bitmap `+0x18`** (`003DABCF`–`003DABDD`), the pair bit is cleared, the callback is called
   with the two bodies and 1 (`003DABF2`–`003DABF8`), and the bit is set again when it returns
   non-zero (`003DABFF`). ~~The bitmap therefore remembers last tick's contacts across a cell change.~~
   **Corrected** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 337](../_index/candidates/s19-opus-replay-separation-pass/README.md) and [the index probe](../_index/candidates/s19-fable-visit-index-probe/README.md), which executes the shipped walk; `003DAB50` re-read.)*: the walk follows the candidate bits,
   so a remembered bit is visited only below the highest candidate of a non-zero byte. Its body pointer and its
   remembered-bit index also drift apart past byte 0: candidate 9 is remembered at index 1, and candidate 64 alone
   is resolved against body 0. [The contract's P-3](CONTRACT-separation-pass.md) states the cases.

### 2.7 The pair — `00314F50(A, B, 1, &out)`

The resolver refuses the pair, returning 0, unless both bodies have positive radii `+0xF0` and
`+0xF4` (`00314F97`–`00314FCC`), both are active this tick (`00314FD6`–`00314FE4`), their layer
bytes `+6` are equal (`00314FEA`–`00314FF1`), and their owner bytes `+0x119` are not equal and
non-zero (`00314FF7`–`00315008`). Then, with `003DAE00` reading each position
(`0031508C`–`0031509E`), the vertical extents `[y + base, y + base + height]` must overlap
(`003150A3`–`003150DE`), and `003DA5A0` — each body's ellipse extent along the line joining the
two positions, the positions already offset by their accumulated pushes (`003150E0`–`00315152`;
the extent from `003DA730` uses the radii and the heading, plus the margins `+0xFC`) — must return
a negative separation (`00315157`–`0031515A`). On contact:

- the weights `+8` (negated when both are negative, both 1 when equal and zero,
  `00315017`–`0031506E`) go through `00314E10` with the masks `+0x110` / `+0x114`, which returns
  A's share `w` of the separation (`0031522E`–`0031523C`): 0 or 1 marks one body immovable
  (`00315249`–`0031528E`), otherwise both counts `+0xED` advance and `+0xEE` is cleared
  (`00315290`–`003152AB`);
- A receives `w × separation` and B `(1 − w) × separation` along the joining direction, each added
  to `+0x100` (x) and `+0x108` (z), with `+0xE8` the squared length and `+0xEC` set
  (`003152B2`–`00315369`); the return is 1 for a contact, 2, 3 or 4 when the callback ran without
  a mutual push, and the raw separation is written to `out` when the caller did not ask for a push
  (`00315377`).

### 2.8 Consuming the push

`002E5180` (from the world tick's per-slot step `002623A0`, `0026241D`, and `0025E400`): when the
body's `+0xEC` is set it re-runs the integrator with a zero delta and mode 1 (`002E5227`–`002E5257`)
and sets the movement context's `+0x151` bit 2 (`002E5278`); `Movement_PrepareCandidatePosition`
(`002E5380`) adds `+0x100`, `+0x104` and `+0x108` to the candidate delta (`002E53DF`–`002E5413`),
then `003DA9F0` zeroes the accumulators — `+0x100`/`+0x104`/`+0x108`, `+0xE8`, `+0xEC`, `+0xED`,
`+0xEE` (`003DA9F2`–`003DAA0C`, also from `0025D540` and `0026AFE0`). When `+0xEC` is clear
`002E5180` clears them directly and zeroes `+0xEF` (`002E5281`–`002E5289`). So a push moves the
actor on its next candidate position and is gone the tick after.

### 2.9 What the field pass reads — battle-state bit 13

`0025B740` sets bit 13 of the battle-state word for the focus actor only when its body exists
and the body's word `+0x88` is non-zero (`0025B778`, `0025B7A8`–`0025B7BC`; [the world-tick
page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5).
**`+0x88` is the cell attribute nibble** — bits 3–6 of the attribute dword of the actor's current
navimap cell, masked through the table at `0209A2D0` (corrected 2026-09-17) and written at every placement by `003808A0`
(§2.4; FZ-10 answered 2026-09-11). So bit 13 says *the focus actor stands on a cell whose
attribute nibble is non-zero*. What the nibble and its two sibling fields mean, and what fills the
mask table, is **FZ-11**. The allocator zeroes the word (`003DA96E`) until the first placement; the
neighbouring `+0x8A` also has a setter (`002EBC70`, `002EBC88`) and readers (`002E9830`,
`002E9D90`), `+0x86` a reader (`002E9890`), and the mask `+0x110` a setter (`002EC5B0`) and reader
(`002E9BB0`).

## 3. Key addresses

| Address | Name | Size | Role |
|---|---|---|---|
| `02B4E4C0` | — | 128 × `0x130` | the pool |
| `02B525C4` / `02B57CC0` | — | 2 / 2 | free-list head / active-list head |
| `02B57CE0` / `02B57EE0` | — | `0x200` / 16 | the 32 cell masks / the candidate set |
| `003DAE30` | — | 230 B | pool initialiser (← `00266D10`) |
| `003DA8A0` / `003DAD00` | — | 328 / 224 B | allocate / release |
| `002E3500` | — | 128 B | the creator (← `002E28E0`, `002E3580`) |
| `00268380` | — | 420 B | size the shape from the contexts |
| `003DAF20` | — | 243 B | orientation and the inner shape |
| `00380D30` | — | 194 B | write the placement (position, cell, ground height) |
| `003DB1B0` | — | 57 B | place and report a valid cell |
| `003DB020` | — | 168 B | mark active, compute cells, register in the masks |
| `0046AD20` | — | 638 B | cell bits from position and radius |
| `003DAA40` | — | 108 B | tick reset (masks and active flags) |
| `003DAC70` | — | 131 B | the pass over the active list |
| `003DAAB0` / `003DAB50` | — | 155 / 283 B | candidate set / visit candidates and remembered pairs |
| `00314F30` → `00314F50` | — | 25 B / 1,080 B | the pair resolver |
| `003DA5A0` / `003DA730` | — | 246 / 244 B | signed separation of two ellipses / one ellipse's extent |
| `00314E10` | — | 154 B | the weight rule |
| `003DA9F0` | — | 35 B | clear the push accumulators |
| `002E5180` | — | 506 B | consume the push (← `002623A0`, `0025E400`) |

## 4. Data structures and formulas

```
MovementBody (0x130 B)
  +0x000 u16 prev  +0x002 u16 next  +0x004 u16 self   (0xFFFF = none)
  +0x006 u8  layer            00269EC0; pairs need equal layers
  +0x007 u8  activeThisTick   cleared by 003DAA40, set by 003DB020
  +0x008 f32 weight           movement context +0x148
  +0x018 u64[2] pairBits      bodies in contact last tick
  +0x030 placement            f32 pos[3]; +0x40 f32 orient[4]; +0x50 / +0x60 f32[4] derived positions;
                              +0x70 f32 displacement[3]; +0x80 u8 cellClass; +0x82 i16 cell (-2 refused); +0x84 i16 secondCell;
                              +0x86 u16 attrBits13to17; +0x88 u16 attrNibble (bits 3-6; state-word bit 13); +0x8E u16 blockedClassMask;
                              +0x8A u16 attr bits 18-22 masked (00231F80); +0x90 u32 flags (bits 0-1 from context +0x151;
                              bit 2 attr bit 12; bit 3 second height above ground; bit 4 integrator mode);
                              +0x94/+0x98/+0x9C copies of the radii and height; +0xA0/+0xA4/+0xA8 the inner shape;
                              +0xAC f32 groundHeight; +0xC0 f32 secondHeight; +0xC8 f32 requestedSpeed
  +0x0E0 f32 height  +0x0E4 f32 baseOffset  +0x0E8 f32 pushLengthSq
  +0x0EC u8 pushed   +0x0ED u8 contacts     +0x0EE u8 partnerImmovable   +0x0EF u8
  +0x0F0 f32 radiusA +0x0F4 f32 radiusB     +0x0F8 f32 heading           +0x0FC f32 margin
  +0x100 f32 pushX   +0x104 f32 pushY       +0x108 f32 pushZ
  +0x110 u32 maskA   +0x114 u32 maskB       (00314E10)
  +0x119 u8  owner                          (equal non-zero owners never pair)
  +0x120 u32 cellBits                       (0046AD20)
```

```
tick:   clear masks[32], every body.active = 0                      003DAA40
frame:  body.active = 1; body.cells = cells(x, z, max(rA, rB));
        for each cell bit c: masks[c] |= 1 << body.self             003DB020
tick:   for each active body A:
          cand = OR(masks[c] for c in A.cells) & ~(bits <= A.self)  003DAAB0
          for each B in cand | A.pairBits:  A.pairBits &= ~B;   [~~cand | pairBits~~: positions below the
                                         highest candidate of each byte; indices drift past byte 0 - P-3, 2026-09-25]
            if resolve(A, B): A.pairBits |= B                       003DAB50
resolve: same layer, both active, owners differ, vertical overlap,
         separation = |pB' - pA'| - (extentA + extentB + marginA + marginB) < 0
         w = weightRule(A, B); A.push += w * sep * dir; B.push += (1 - w) * sep * dir
next candidate position += push; push = 0                            002E5380, 003DA9F0
```

## 5. Call chain

```
create:  002E28E0 / 002E3580 -> 002E3500 -> 003DA8A0; 00269EC0, 002682D0, 002685F0, 00268380 -> 003DAF20
release: 0025AB30 / ActorSystem_ReleaseManagerRecords -> 002E3D00 / 002E3AF0 -> 003DAD00
frame:   Movement_UpdateActorFrame -> 002E5610(record, body, ..) ; 002EA7F0 ; 003DB020 -> 0046AD20
         002E5C90 -> 003DB1B0 -> 00380D30 (placement)
tick:    World_UpdateSimulationTick -> 003DAA40 ... 003DAC70(00314F30) -> 003DAAB0, 003DAB50 -> 00314F50
         -> 002623A0 -> 002E5180 -> 002E5610 -> Movement_PrepareCandidatePosition -> 003DA9F0
```

## 6. Modding notes

- **Layers and owners are the cheap switches.** Equal layers pair; equal non-zero owners never do.
  Neither has a writer beyond the creator's zero in this reading, so a mod that wants actors to
  ignore one another sets `+6` or `+0x119` after creation.
- **The weight decides who yields.** A zero weight (or a mask bit `00314E10` honours) makes a body
  immovable; the other body takes the whole separation.
- **The pass is capped at 128 bodies** and the candidate set is 128 bits wide; nothing here grows.

## 7. What is not known

- [x] ~~What writes the word `+0x88` that battle-state bit 13 tests.~~ **FZ-10 ANSWERED 2026-09-11:**
      `003808A0`, at every placement — the nibble at bits 3–6 of the cell's attribute dword (§2.4, §2.9).
- [x] What the cell attribute nibble (bits 3–6), the five-bit field at bits 13–17 and `00231F80`'s
      five bits mean, and what fills the mask table at `020A22D0` *(read: `0209A2D0`, see below)* — BSS, no rip-relative writer. **FZ-11.**
      ***NARROWED 2026-09-17 (FABLE): two of the three fields are named by the script verbs that read them, and the mask table's address is corrected.** Body `+0x86` (attribute bits 13..17) is read by the getter `002E9890`, whose caller `00347240` is the handler of [`getmapid_48b`](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md): the field is the cell's **map id** as the script sees it. Body `+0x8A` (`00231F80`'s five bits, attribute bits 18..22 masked) is read by `002E9830`, whose caller `003476B0` is the handler of `getmapgroundtype_48c`, and directly by the footstep chooser `002E9D90` (`002E9F29`) as the surface index into [`soundfoottable.bin`](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md): the field is the cell's **ground type**. The nibble at `+0x88` (bits 3..6) still has one consumer, battle-state bit 13 through `0025B740`, and no name. The mask table is at **`0209A2D0`**, not `020A22D0`: `00232020` and `00231F80` both `lea` that base and index `+0x110 + entry * 8` (`00232024`..`0023204E`, `00231F90`..`00231FD4`), so the 2026-09-13 “no rip-relative writer” was measured at the wrong address. At the right one the block `0209A2D0`..`0209A660` is a movement-globals record (floats at `+0xA0`..`+0x108` written by `0036FBB0` and others, a pointer at `+0x390`) whose entry area `+0x110`.. is read by `00231A90`, `00232020` and `00231F80` and, like before, has no rip-relative writer: the entries are filled through a register base, and that fill is the residue. Static, bodies read.*
      **Narrowed 2026-09-18 (FABLE): the mask table's fill is found, and it is the script's map-id override.* A sweep of every rip-relative reference into the block `0209A2D0`..`0209A660` (37 functions, interior offsets included) shows the entry area at `+0x110` = `0209A3E0` is addressed by exactly six functions. `0026E960` zeroes it at area initialisation (`0026EA05`..`0026EA3B`; called from `0026E760` ← `00378120`, WorldAreaField). The only writers of non-zero content are `0026E880(index, value, shift, width)` — `mask |= field`, `value = (value & ~field) | (v << shift)` on the 8-byte entry `{mask, value}` (`0026E8A1`..`0026E8AC`) — and its clearer `0026E850`, plus the zeroers `0026E130` (one entry) and `0026E150` (a run); each ends in the notify `003278D0`. Their callers are the family `003791D0`..`003795A0`, and those are the tails of the script verbs `00F6`..`010B`: `setmapidfloor` / `setmapidfloorground` / `resetmapidfloor*` address entries 0–31, `setmapidwall*` entries 32–63 (`add ecx, 0x20`, `003795C3`), `setmapidmj*` entries 64–79 (`add ecx, 0x40`, `00379467`; the all-reset passes count `0x10`, `00379224`), so the table is **80 entries of `{mask, value}` in three sub-tables indexed by a cell's map id** (attribute bits 13..17). The fields the verbs set are the attribute bit positions: `setmapidfloorground` writes width 5 at shift 18 (`003791F4`..`003791FE`, the ground-type field of `+0x8A`), the floor verbs one-bit fields at shifts 23 and up (`0037930D`..), the wall verbs bits 30 / 31 (`003795BC`, `003795D7`). Readers apply `(attr & ~mask) | (value & mask)`: `00231F80`, `00232020`, `00231A90` (above) and `0022F8B0`, which folds the entry at `0x20 + (attr >> 13 & 0x1F)` and tests bit 31 (`0022F936`..`0022F95F`). So a script can, per map id, override a cell's ground type, its floor flags and its wall bits, and that is what fills the table. *(Added 2026-09-19, FABLE: the floor bits 23-27 have a second reader - the battle pathfinder asks them, per mover class, whether a gated portal of the navigation mesh is open; see [how a unit finds its way across the navigation mesh](how-a-unit-finds-its-way-across-the-navigation-mesh.md), section 7.)* The `+0x88` nibble (bits 3..6) keeps its one consumer and no name.*
      ***ANSWERED 2026-09-18 (FABLE) — the third field is named the way the first two were, and the fill is the script's override verbs.** Bits 13–17 are the cell's map id (`getmapid`), bits 18–22 its ground type (`getmapgroundtype`), both placed 2026-09-17. The nibble at bits 3–6 is the cell's **mj class**, 0–15: the placement `003808A0` itself indexes the mask table by `0x40 + ((attr >> 3) & 0xF)` (§2.4 above), which is the third sub-table, entries 64–79, the one the verbs `setmapidmj` / `setmapidmj_103` / `setmapidmjground` / `resetmapidmj*` fill (`00379430` adds `0x40` to its index, `00379467`; the all-reset passes count `0x10`, `00379224`) — so the nibble is the same kind of tag as the map id, a per-cell class whose per-class override the script can set. Its one consumer, `0025B740` (from `ActorManager_RunFieldRuntimePass`), tests the focus actor's body word `+0x88` — the stored nibble — and, when non-zero with the other gates held, raises battle-state bit 13 through `00238B20(1)` (`0025B7B4`..`0025B7C8`), the presentation veto the world-tick page lists; so a non-zero mj class under the focus actor is a “no presentation here” cell tag. The table fill was placed earlier today: 80 `{mask, value}` entries in three sub-tables (floor 0–31, wall 32–63, mj 64–79), zeroed by `0026E960` at area initialisation and written only by `0026E880` / `0026E850` behind the verbs `00F6`..`010B`. What “mj” abbreviates is authoring vocabulary the image does not carry; its mechanism is complete. Static: the placement, the verb family, the consumer, the setters.*
- [x] **UQ-103.** The cell geometry of `0046AD20` (a centre at `02CA6040`-region globals, a radius and 32 bits)
      is not read; only that it yields the mask bits.
      **PARTLY READ 2026-09-13 (OPUS), and the first correction is to this bullet: the
      `02CA6040`-region globals are NOT a centre.** They are a running accumulator with a sample
      count, written every call:
      ***ANSWERED 2026-09-18 (FABLE) — the three residues close: the axes come from the caller, the `200.0f` is a neighbour that is never used, and the mean is divided once per simulation tick into the centre the next quantisation subtracts.** *Axes.* The only caller is the per-tick placement `003DB020`, which calls `0046AD20(&cells, x, z, size)` with `xmm1` = the x it was given, `xmm2` = the z, and `xmm3` = `max(radius0, radius1)` of the body's radius pair (`003DB04D`..`003DB068`): the first argument is x, the second z, and the cell size is **the body's own larger radius**, so the 32-way split is a per-body scale, not a world grid. The sums at `02CA6040` and `02CA6048` therefore accumulate x and z (`0046AD59`, `0046AD5E`); nothing adds to `02CA6044`. *The `200.0f`.* `009159FC` is the next constant in `.rdata` and no instruction in `0046AD20` references it — a rip-relative sweep of the body finds `009159F8` (`32.0f`, `0046AE8D`) and not `009159FC` — so it governs nothing here. *The mean.* `0046AFA0` (128 B), called from `World_UpdateSimulationTick` `00314020`, divides the three sums by the sample count `02CA604C` (by `1.0` when the count is 0, `0046AFB3`), stores the quotients as the centre `02CA6034` / `02CA6038` / `02CA603C` and zeroes the sums and the count (`0046AFCF`..`0046B017`): the centre that `0046AD20` subtracts (`0046AD7F`, `0046AD88`) is the mean position of every body placed during the previous tick, y held at 0. The pair-mask bits then follow OPUS's reading: the position relative to that centre, reduced into one radius-sized cell, scaled into 0..31 and shifted into a bit. `004697C0` touches only the neighbouring flag `02CA6030`. Static: the caller, the two bodies, the sweep.*

      ```asm
      0046AD2B  movss xmm0, [02CA6040]        ; running sum X
      0046AD36  movss xmm4, [02CA6048]        ; running sum Y
      0046AD3E  inc   dword [02CA604C]        ; the SAMPLE COUNT
      0046AD59  addss xmm0, xmm8              ; += arg
      0046AD5E  addss xmm4, xmm7              ; += arg
      0046AD66  movss [02CA6040], xmm0        ; stored back
      0046AD6E  movss [02CA6048], xmm4
      ```

      **A sum pair plus an incrementing count is a mean waiting to be divided**, not a centre being
      consulted. **The centre this function actually subtracts from is a different pair**,
      `02CA6034` / `02CA603C` (`subss xmm8, [02CA6034]`, `subss xmm7, [02CA603C]` at `0046AD7F`),
      and all five globals lie past `.data`'s raw size — **loader-zeroed, written only at runtime.**

      **The grid quantisation is a divide-truncate-remultiply**, the standard cell/origin pair:
      `divss xmm0, xmm3` → `cvttss2si eax, xmm0` gives the **cell index**, and
      `cvtdq2ps xmm1` → `mulss xmm1, xmm3` turns it back into the **cell origin**, so `xmm3` is the
      cell size and arrives as an argument rather than a constant.

      **AND THE "32 BITS" ARE LITERALLY 32.** `0046AE8D` multiplies a normalised value by the
      `.rdata` constant at **`009159F8`, which is `32.0f`**, then `cvttss2si` takes the integer and
      `shl r14d, cl` (`0046AEA9`) sets that bit — so the mask is *"scale into 0..32, shift a 1 into
      place"*. The adjacent constant `009159FC` is **`200.0f`**.

      **Still not established:** which argument is which axis, what `200.0f` governs, and what the
      accumulated mean at `02CA6040` is eventually consumed for — **nothing divides it in this
      body.** The bullet stays open for those.
- [x] **UQ-104.** Which mask bits `00314E10` honours (`+0x110` / `+0x114`) and what sets them beyond
      `002EC5B0`.
      **Partly answered 2026-09-14 (FABLE).**
      **Which bits — answered, from the whole 154-byte body.** For each body let `m = [+0x110] | [+0x114]`, and let `u = mA | mB`.
      1. **Bits 8–15 cancel.** Each body keeps only `m & ~(u >> 8) & 0xFF`, so bit `8+k` on either body removes priority bit `k` from both (`00314E50`–`00314E6E`).
      2. **With no priority bit left**, the weights decide: `w = wB / (wA + wB)`.
      3. **Bits 16+ override.** If a surviving priority bit `k` has bit `16+k` set on either body, `w = 0` (`00314E7E`–`00314E86`).
      4. **Otherwise the larger surviving low byte wins.** When the two differ as numbers, A's larger mask gives `w = 0` and B's gives `w = 1` (`00314E87`–`00314E93`).
      5. **Finally, a negative weight** forces `w = 0` for A or `w = 1` for B (`00314E96`–`00314EA3`).
      So only bits 0–7 are priorities, bits 8–15 are per-pair vetoes of them, and bits 16+ are hard-freeze partners of them.
      **What sets `+0x110` — the path is one setter.** A scan of every dword write to `+0x110` / `+0x114`, through a register loaded from `[x + 0x138]` (the body link the setter itself follows), finds **one** store: `002EC5B0`'s. Its 11 call sites pass:
      - `0x10` (`003552D7`, `00356BC3`), `0x10` plus the active field record's bit 15 (`0025B4AF`), 8 (`00358E37`) and 0 (`00356FD3`, `00358B87`, `00358E06`);
      - computed values at `00238E75` and `0025B48E`;
      - from `Movement_SetRequestedSpeed` (`0026D7E9`), and from its sibling at `0026D8D5`, which applies the same rule without the bit-3 clear.
      The §2.4 sentence *"clears bit 2 of the mask"* is incomplete. The function reads the current mask (`002E9BB0`) and clears bit 2, and stops there when the actor's byte `+0x12` is above 3. For byte `+0x12` ≤ 3, it sets bit 2 again when the requested speed is exactly 0; with a non-zero speed, if the actor is the party focus, it sets **bit 10**, the veto of bit 2, and also clears bit 3 when its mode argument is 1 (`0026D7A4`–`0026D7E1`).
      **Not established:**
      - **Who writes `+0x114`.** The provenance scan finds no store. It follows only `[x + 0x138]`-loaded registers, so a store through another path to the body, or through a block copy, is not excluded.
      - **What the bits mean in play.** The mechanism above is exact; the classes are not named.
      ***ANSWERED 2026-09-18 (FABLE) — the second mask word is never written after allocation, so the resolver's `m` is `+0x110` alone and `002EC5B0` is the only setter.** The bits were read on 2026-09-14 (above). The residue, *who writes `+0x114`*, closes by two whole-image sweeps that do not depend on how the body pointer was obtained. Every dword store at displacement `+0x114` — 93 sites in 79 functions — lands on another object: the only one in the body module, `003DA400`, writes a `0x18`-byte slot table (`+0x110`..`+0x124`, indexed by its fourth argument) on an object that carries a table pointer at `+0xD8` and an id at `+0x28`, which a body does not, and its callers are the verb handlers `0034F2F0` / `0034F930`. Every wider store that covers `+0x114` — 354 eight- and sixteen-byte sites — is likewise elsewhere, except two in the body ranges: the body allocator `003DA8A0`'s `mov qword [rdi+0x110], rsi` with `rsi` cleared (`003DA8AD`, `003DA9CD`), which zeroes both words at allocation, and `003D92C0`'s `movdqa [rbx+0x110]`, whose `rbx` is an effect element (`+0x330` counter, `+0x20` pointer; its callers `003D9000` / `003D9040` are effect routines of the type-dispatch family), not a body. So a body's `+0x114` is zero from allocation to release, `m = [+0x110] | [+0x114]` reduces to `[+0x110]`, and the mask the pair resolver `00314E10` honours is written by `002EC5B0` alone through its eleven call sites (`0x10`, `8`, `0`, the field record's bit 15, the speed setter's bit 2 / bit 10, and the two computed values). What the bit classes mean in play beyond those names is a naming residue, not a mechanism one. Static: two displacement sweeps with size-aware operands, the allocator, and the two candidates read.*
- [x] ~~**UQ-105.** Whether `+0x104` (push y) is ever non-zero: the resolver writes only `+0x100` and `+0x108`.~~ **Answered 2026-09-14 (FABLE):** no code the census reaches ever makes it non-zero, so **separation pushes are horizontal**.
      - **Every store that covers `+0x104` in the body code writes zero.** They are the upper half of 8-byte stores at `+0x100`:
        - in the allocator `003DA8A0` (`003DA97A`, `003DA9B9`), with `rsi` zeroed at `003DA8AD`;
        - in the accumulator reset `003DA9F0` (`003DA9F2`).
        A scan of every write at displacements `+0xF5`–`+0x104` in the body module (`003D9000`–`003DC000`), the pair resolver and the movement update (`002E3000`–`002E6000`) finds these three, the resolver's two 4-byte float stores at `+0x100`, and three 4-byte stores to `+0xF8` of the movement context (a different structure).
      - **The whole image has no other candidate.** There are 115 functions with a write at displacement `0x104`, and none is in those ranges. The two that add a vector into `+0x100` / `+0x104` / `+0x108` (`00256C1A`–`00256C35`, `00256F09`) add it to `+0xF0` / `+0xF4` / `+0xF8`, which on a movement body are radii. So they belong to another structure.
      - **Consequence.** The integrator's `+0x104` addition (`002E53DF`–`002E5413`) always adds 0. Bodies are separated in x and z only, never lifted or sunk by a contact.
      - **Not excluded:** a write through an indexed displacement other than `0x104`, or a block copy onto a body.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the pool's geometry, links and heads | `003DAE3A`–`003DAF13`; `003DA8A6`–`003DA96E`; `003DAD09`–`003DAD6B` | 1 |
| the creator and the two releasers | `002E3506`–`002E3546`; `002E3D09`–`002E3D2D`; `002E3B9D`–`002E3BB5`; `002E2C21`; `002E3589`–`002E359A` | 1 |
| the shape from the contexts | `00268386`–`002684FD`; `003DAF3C`–`003DB000`; `003DB120`; `003DB130`; `006C0520` | 1 |
| the placement writer | `00380D45`–`00380DD2`; `003DB1C7`–`003DB1D9` | 1 |
| the frame registration and the cell masks | `002E508A`–`002E5140`; `003DB03D`–`003DB0B1` | 1 |
| the tick reset and the pass | `003140C5`; `00314244`; `003DAA43`–`003DAAA9`; `003DAC98`–`003DACE1`; `003DAAC5`–`003DAB49`; `003DABB0`–`003DAC11` | 1 |
| the pair conditions, the separation and the weighted push | `00314F97`–`00315369` | 1 |
| the push is consumed by the next candidate position and cleared | `002E5227`–`002E5289`; `002E53DF`–`002E5467`; `003DA9F2`–`003DAA0C` | 1 |
| bit 13 reads the body's `+0x88` | `0025B778`; `0025B7A8`–`0025B7BC` | 1 |
| `+0x88` is the cell attribute nibble, written at every placement | `00380DDD`; `003808C2`–`0038090A`; `00232024`–`00232074` | 1 |

## 9. Related

- [`the-movement-and-secondary-context-censuses.md`](../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md) — the context fields the body is built from.
- [`the-world-tick-and-the-field-frame.md`](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — where the tick reset and the pass sit, and bit 13.
- [`fcp-character-parameter-block.md`](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md) — the body-radius slot.
- [`heading-speed-to-position-delta.md`](heading-speed-to-position-delta.md) — the step the push is added to.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| **128 entries of `0x130`** at `02B4E4C0` | the initialiser carries `0x80`, `0x130` and `0xffff` as literals, and **`02B4E4C0 + 128 × 0x130 = 02B57CC0`** — the pool ends on the byte the active-list head begins |
| **32 cell masks, sixteen bytes each**, at `02B57CE0` | **`02B57CE0 + 32 × 16 = 02B57EE0`** — the masks end on the byte the candidate set begins |
| the two list heads are set empty by `003DAE30` | it references `02B57CC0` and `02B57CC4`, with `0xFFFF` as the literal |
| seven stated function sizes | `003DA8A0` 328 · `003DAD00` 224 · `003DAA40` 108 · `003DAC70` 131 · `003DB020` 168 · `00314F50` 1,080 · `00268380` 420 — all present |

**Both extents close on their neighbours.** The pool is bounded by the active head and the cell-mask
table by the candidate set, so "128 × `0x130`" and "32 × 16 bytes" are not two independent numbers
that merely fit — each is confirmed by what starts where it stops.

### The free-list head is `02B57CC4`, not `02B525C4`

`003DA8A0` opens by reading it:

```asm
003DA8A6  movzx edx, word ptr [rip + 0x277d417]   ; -> 02B57CC4   the free head, a u16
003DA8AF  mov   r9d, 0xffff
003DA8B5  cmp   dx, r9w                           ; empty?
003DA8C2  lea   r10, [rip + 0x2773bf7]            ; -> 02B4E4C0   the pool base
```

`003DA8A0` and `003DAD00` between them touch **three** globals — `02B4E4C0`, `02B57CC0` and
`02B57CC4` — and **`02B525C4` appears in neither.**

The corrected address is also the only one that makes sense of §2.1's own next clause. The section
says `003DAE30` "sets the two list heads to empty", and the two heads are adjacent `u16`s at
`02B57CC0` (active) and `02B57CC4` (free), immediately past the pool. **The page describes the pair
correctly in one clause and cites a wrong address for one of them in the next.**

**Why it matters beyond the typo.** `02B525C4` is not merely wrong, it is *inside the pool* —
`02B525C4 − 02B4E4C0 = 0x4104`, which is **entry 54, offset `0xA4`**. A reconstruction taking the
published address would read and write a body's own field as the free-list head, corrupting entry 54
on every allocation while appearing to work until that entry came into use.

*(`003DAE30` also references `02B57CC8` and `02B57CD0`, which §2.1 does not mention. Recorded as
unexplained rather than named.)*

**Not claimed:** nothing here was executed or observed live. §§2.2–2.9 — the attachment chain, the
shape, the per-frame registration, the pair resolver and battle-state bit 13 — were not re-derived;
this pass took the pool layout, the two extents and the list heads.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Two edges, one carrier, and this page is the SERVICE at both.** §295 cites `004697C0` for what it
touches — *"only the neighbouring flag `02CA6030`"* — and two combat-side bodies call it:

- **CombatAI**, `BattleUnit_TrySelectAndCommitAiOrderFromSet` (`00305CC0`) at **`00305E5A`**.
- **CombatAction**, `BattleUnit_AdvanceActionState` (`00307BE0`) at **`00307C57`**.

**What they use it for is the same thing in both cases: a notify on a committed action.** In the
gambit walk it is the third call on the success path — made only when a commit succeeded, the mode is
non-zero and the latched `word[unit+0x714]` is not `0xFFFF` — with the shape
`(rcx = [unit+0x698], rdx = out_target, r8d = word714, r9d = 4)`, where `r9d` is a hardcoded kind
constant. The prologue agrees: `004697D6 movzx edi, dx` and `004697E4 movzx ebp, r8w` take arguments
two and three as **sixteen-bit** values, which is what a target id and that latched word are.

**Nothing in either combat layer is owned here.** The crossing is that both callers reach this
page's flag through the same notify — which is worth stating precisely because the page's own
sentence about `004697C0` is about what it TOUCHES, and this is about who ASKS.

*Both far ends are named by address rather than by symbol alone, and that was measured before
writing: their entire unmentioned-neighbour set is CombatAI and CombatAction, the two layers this
section accounts for, so naming them imports nothing further.*
- **Party - SERVICE (11 edges).** `0025B740`, `0025E400`, `002623A0` reach bodies filed to party: `003590D0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (85 edges).** `00202E10` is also called by bodies filed to presentation: `0040B430`, `0051C3C0`, `00523380` - shared machinery across the layer boundary, no shared ownership.
- **Resource - SERVICE (8 edges).** `002EDBD0`, `00409660` reach bodies filed to resource: `00409660`, `00409F50`, `00409600` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (5 edges).** `002E5180` is also called by bodies filed to World: `0025E400` (ActorManager), `002623A0` (ActorManager); `00314020`, `00378120` reach bodies filed to World: `002623A0` (ActorManager), `003C63A0` (Navigation) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (19 edges).** `002623A0` is also called by bodies filed to WorldAreaField (world area): `00314020`; `00266D10` reaches bodies filed to WorldAreaField (world area): `002342F0`, `00268750`, `0026D910` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

The area initialiser `00266D10` calls into two other layers while it resets the pool. Both calls are **CLIENT**
edges of area set-up, not steps of the separation pass.

- **Audio.** It calls a 516-byte Audio-filed body that reaches the sound entries.
- **Input.** It calls the 1,936-byte Input-filed body that
  [the shared neighbours page](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)
  names as unread.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** The actor-system initialiser this page cites is called from the 978-byte core start-up root.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay + UI — MECHANICAL (2 edges, a shared callee one remove away).** The `002324F0` section cites `00202E10`, a shared helper that the Gameplay layer's `00339630` and the UI layer's `005512B0` also call. The crossing is that one leaf being consulted by three layers — this page owns the movement pool and separation pass, not whatever those layers use `00202E10` for. Edge list from `edges.tsv` (batch-52 audit, SWE2-EC7).

**Save_Load_Settings — SERVICE.** `00266D10` on this page calls `FUN_002ef2d0`, owned by that layer. What it reaches is a 38-byte clear that gives the block a size: **`0x1538` bytes at the persistent payload base**, `002EF640()` plus `0x200`, before it tail-jumps; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00380D30` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00380D30` (~208 B) — `rbx = rcx` body-pool walk (`00380D3F`).

| member | role | interior |
| --- | --- | --- |
| `00232090` | `dx` sign gate, `qword[+0x10]` then `movsx rdx` walk (`00232093`/`002320A0`) | [`00232093`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-22 update (2026-09-18) — five movement-side accessors

`002EC5B0` (31 B) is the null-safe two-hop write the UQ-104 answer names as
that mask field's only setter: `[rcx+0xC0]` -> `[rax+0x138]` -> `edx` stored
at `[rax+0x110]` on the second-hop object — the store the UQ-104 answer
attributes to this body (its `+0x114` is the doc's row offset for the same
mask lane). Interior anchor `002EC5BC` (the second hop).

`003DA5A0` (246 B) is a marshalling body: `rsi = [rsp+0x70]` fifth argument,
`rbp = r8`, `rbx = rdx`, `rdi = r9`, then two `003DA730` + `003A1D30` call pairs
with `rcx` alternating `rbx`/`rdi` — the two-arg-shuffle delegate the pool's
movement-state writers route through. Interior anchor `003DA5DE` (the first
`003DA730` call).

`0026E850` (40 B) is the indexed bit-field clear: `r9 = &0209A3E0[rcx]` selects
the `{mask, value}` entry (`0026E850`..`0026E85A`), `eax = ((1 << r8d) - 1) <<
edx` builds the field mask, `not eax` inverts it, and `and dword[r9], eax`
clears the covered mask bits (`0026E85E`..`0026E870`) — the complement of
`0026E880`'s set, ending in the same `003278D0` notify tail (`0026E873`).
Interior anchor `0026E85E` (the shift setup).

`00231890` (97 B) is the two-level indexed fetch: `r8w` signed index `*0x20`
into `[rcx+0x10]`, that row's `word[+0x10]` `*0x10` into `[rcx+8]`, `comiss`
against `[008C5B2C]`, `[r8+8]` minus `[rdx+8]` — the position-sample compare
the spawn-placement tunable readers call. Interior anchor `0023189B` (the index
sign-extend).

`003E6150` (439 B) is the word-id record lookup over this page's `0x740`-stride
pool at `[022C6F28]`: `002EDBD0` resolve, `di == -1` -> index 0, `id * 0x740 +
base`, `[rcx+0x284]` flag test with `cmove` to null — the same record base and
flag lane the render-pool docs describe from the consumer side. Interior
anchor `003E618A` (the `imul 0x740`).

**Resource — SERVICE (SWE2-EC7 2026-09-18, 2 edges).** `002EDBD0` — the id
resolve `003E6150` opens with — calls `00409660` and `00409F50`, both
Resource-filed. The pool's word-id path resolves through the resource layer;
the crossing is that this page's accessor consults that layer, not that the
pool shares ownership of it.

## SWE2-EC7-27 update (2026-09-18) — `002E9BB0` mask-field getter

`002E9BB0` (34 B) is the read side of `002EC5B0`'s two-hop channel:
`[rcx+0xC0] -> [+0x138] -> dword[+0x110]`, zero on any dead hop — the
mask getter for the field the batch-22 setter writes. Interior anchor
`002E9BC8` (the `+0x110` read).

## SWE2-EC7-43 update (2026-09-19) - `00233110`

`00233110` (285 B) is a movement-pool body - `01F44830`, `00230A40`/`002324F0`/`00808C40`. Interior anchor `002331C0` (a `00230A40` call).

## SWE2-EC7-52 update (2026-09-19) - `002324F0`

`002324F0` (624 B) is a word-indexed record walker - `movsx dx` x0x20 stride over `[rcx+0x10]` table reads `0x10`-byte records, `00861F14`/`00202E10` tail, `01CEBxxx` rdata constants. Interior anchor `00232646` (a `00861F14` call).

## SWE2-EC7-55 update (2026-09-19) - `00230A40`

`00230A40` (279 B) is a call-free bit-field flag resolver - `[rcx+0x10]` + `dx`*0x20 record, `0209A2D0` table, `+0x110`/`+0x114` masks, `bx` switch arms. Interior anchor `00230A61` (the `dx*0x20` record read).

## SWE2-EC7-60 update (2026-09-19) - `0026E530`

`0026E530` (158 B) is the `002ED6A0` solver body the movement-pool page names - `00231A90`/`00380B80`/`00808C40` plus `01F44830`/`0209A670`/`0209A678`. Interior anchor `0026E577` (a `00380B80` call).


## SWE2-EC7-72 update (2026-09-19) - `006C0520` F4W float4 writer measured

`006C0520` (26 B) measured - the page's "F4W float4 default writer" is
exact: stores `xmm1`/`xmm2`/`xmm3` at `+0`/`+4`/`+8` and the fourth
component from stack slot `[rsp+0x28]` at `+0xC`. No branches, no calls -
the pure vec4 store `005049E0` uses for the `1.0` triples and the
movement contexts use for quats.
Interior anchor `006C052B` (the `movss [rcx]` head store).

## SWE2-EC7-87 update (2026-09-20) - `003DA830` magic-tag record init measured

`003DA830` (20 B) is the tag init the pool callers run:
`[rcx]` and `qword[+4]` take `0x3727C5AC` and `dword[+0xC]` is
zeroed - the sentinel that marks a freshly-allocated body slot.
Interior anchor `003DA83B` (the `+4` tag store).

## SWE2-EC7-97 update (2026-09-20) - `002E8E20` measured

`002E8E20` (178 B) is the four-parameter apply `002E28E0` and
`002E6B10` run: `rcx`'s `[+0xC0]` word must resolve, `rbx =
[rcx+0xB8]` supplies the source, then `002EE050` gets the
`+0x20/+0x24/+0x28` triple, `0026B2E0` the `+0x80/+0x84` pair,
and the `byte[+0xDE]`/`byte[+0xDF]` gates arm `0026BBC0`
(`+0x90/+0x94`) and `0026BF60` (`+0x88/+0x8C)` respectively -
the staged four-value publish the separation pass drives.
Interior anchor `002E8E68` (the `002EE050` call).

## SWE2-EC7-98 update (2026-09-20) - `00420D50` measured

`00420D50` (45 B) is the store this page's `002EE050` (and
`002EE290`, `0042F3B0`) tails into: `dword[rcx+0x284]` loses
bit 9 (`& 0xFFFFFDFF`), `xmm1/2/3` land at `+0x160`/`+0x164`/
`+0x168`, and `+0x16C` is stamped `1.0f` - the four-component
publish that completes the compare-then-write path.
Interior anchor `00420D5A` (the first `movss` store).

## SWE2-EC7-105 update (2026-09-20) - `003DA860` + `0025D480` measured

`003DA860` (42 B) is the scaled-pair writer
`00265FF0`, `0026B2E0`, `0026BBC0`,
`0026BEE0` and `0026BF60` call:
`[rcx] = xmm2 * [rsp + 0x28]` and
`[rcx + 4] = xmm3 * [rsp + 0x30]`, and when
`rdx` is non-null the unscaled `xmm2` /
`xmm3` pair is also stored at `[rdx]` /
`[rdx + 4]` - one call emitting both the
weighted result and the raw operands.
Interior anchor `003DA866` (the first
`mulss`).

`0025D480` (69 B) is the four-field reset
`002E26F0`, `002E28E0` and `002E3AF0` run on
`[rcx + 0xC0]` records: qwords `+0x120`,
`+0x128` and `+0x130` are zeroed and bit 2 of
`byte[+0x14F]` cleared - the quiesce pass
the movement arms share, skipped entirely on
a null record.
Interior anchor `0025D493` (the first qword
clear).

`00381EB0` (365 B) is the normalize `0022F8B0` calls: `00202B70` reads `[rcx + 0x50]` into a stack vector, then `dword[rbx]` mode 0/1/2 each compute a magnitude through `00861F14` (sqrt) with mode-specific scaling - the movement record's per-mode length pass.

Interior anchor `00381EDB` (function `00381EB0`).

`003DA730` (244 B) is the steering normalise `003DA5A0` runs: `xmm6 = -[rcx+8]`, the xz delta `r8-rdx`, `00861F08`/`00861F0E` of `xmm6` give the sin/cos pair that forms cross `xmm4 = cos*dz - sin*dx` and along `xmm9 = sin*dz + cos*dx`; when `xmm4^2 + xmm9^2` is nonzero it scales by `1/[rbx]^2` and `1/[rbx+4]^2` and returns the summed correction, else `0.0`

Interior anchor `003DA7C5` (function `003DA730`).
