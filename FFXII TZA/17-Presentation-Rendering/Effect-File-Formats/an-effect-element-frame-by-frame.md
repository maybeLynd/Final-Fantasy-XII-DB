---
system: An effect element, frame by frame - the per-frame update of element types 0x00-0x0A, its cull, its release and its child spawns
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the ten per-type tails (00442600, 004428F0, 00445B50, 00447830, 00448800, 00449560, 0044A180, 0044B3C0,
    0044C850, 0044B960), the cull test 005002E0, the release dispatcher 002F31C0, the child-spawn slot routine 003A8950
    and the motion-aligned matrix builder 002F35C0 with its wrapper 002F3570 disassembled from the authority image and
    read whole, 2026-09-19; the expiry arm of the base update 002F2530 re-read at its two calls; prior art on the
    dispatch page, the distance-fade node's page and rng-streams joined
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-effect-element-falsification-pass-1
  note: written by FABLE; static throughout. Scope is the UPDATE side only. What a type draws is the walk method's
    business and stays on the element-types page, which is PARTIAL on exactly that. Not read and named as such - the
    sub-resource spawner the slots call, the matrix builder the motion alignment ends in, the track samplers; first review = the 0929 promotion sweep: promoted DOCUMENTED -> AUDITED
    2026-09-29 by SWE2-AUDIT-SPEC: falsification pass-1 (opus-effect-element) FAILS 0 reproduced;
    the five refuted clauses corrected in place with strike+attribution (verified: four->five steps,
    002F31C0 release, 0044B960 shared-helper); two classified neighbour edges; no standing killer;
    zero open boxes
  crossref_clean: true
  reopened_count: 0
---

# An effect element, frame by frame

A spell effect is a tree of **elements** - points, lines, sprites, trails, shapes. Every game frame each live element is
*updated* and then, separately, *drawn*. This page is the update for the ten basic types `0x00`-`0x0A`: what it
computes, how an element decides it should no longer exist, and how it gives birth to children. The draw is on
[the element types 0x00-0x0A](the-element-types-00-0a.md).

## 1. The shape of an update

An update is **the base, then the type's tail**
([the dispatch page](effect-element-type-dispatch.md) reads the base, `002F2530`):

1. **The base** runs at most once per game frame, advances the element's age `+0x3C` / `+0x44`, and handles **expiry**:
   with a lifetime `+0x4C` set and the age past it, it runs the child-spawn slots with **trigger 3** and then
   **releases** the element (section 3) - the tail never runs on that frame. *(Added 2026-09-29, OPUS falsification
   pass 1, `CON-179`.)* The lifetime is not the only end. The base's floor arm 2 compares the height `002F3750` with
   element `+0x64` and, when above it, runs the same trigger-3 slots and the same release (`002F2A5F` to
   `002F2D37`..`002F2D52`).
2. **The tail** samples the definition's tracks at the element's age and leaves the results in the element for the
   draw to use (sections 2 and 4).
3. **The tail ends in a fork** (section 3): a cull test; an element that fails it is released on the spot, one that
   passes runs its child-spawn slots with **trigger 2**.
4. **Type `0x00` has no tail** *(added 2026-09-29, OPUS falsification pass 1, `CON-179`)*. The update dispatcher `002F3910` sends type `0x00` to the base alone (`002F393C`). The
   element's type byte `+0` is the definition's `+0x44` (`002F30F2` / `002F30F6`). *(Precision 2026-09-29, OPUS, on
   SWE2-AUDIT-SPEC's [batch-7 review](../../_index/candidates/auditspec-review-opus-batch7-0929/REVIEW.md) section 2: two bytes are read, not one. The dispatcher tests the element's byte 0; the base's
   trigger-2 gate re-reads the definition, `002F2C51` `cmp byte [[element + 0x20] + 0x44], 0`. They agree through the
   constructor's copy at `002F30F2`. No rewrite of byte 0 or of `+0x20` was found in the bodies the reviewer swept;
   that is a bounded negative, not an image-wide one.)* With that byte zero the base itself
   shifts the position history and copies the colour (`002F3890`), then runs the child-spawn slots with trigger 2
   (`002F2C4D`..`002F2C76`) - **with no cull test**; the base never calls `005002E0`. Type `0x09` goes to the
   dispatcher's default arm `0043EAB0`, which this page does not read.

**What a reimplementation must keep:** an element that leaves its cull window is *destroyed*, not skipped; child
spawns happen only for elements that passed the cull on that frame, or that are expiring ~~; and~~ **- for the nine
types with a tail. A type-`0x00` element runs its trigger-2 slots in the base with no cull at all (item 4; corrected 2026-09-29, OPUS falsification pass 1, `CON-179`);**
and the orientation mode of
section 4 changes whether the parent's rotation reaches the element at all.

## 2. The three simplest tails: types `0x01`, `0x03`, `0x08`

**What every tail shares** is most of what a tail is:

- they sample the definition's tracks (`[element + 0x20]`) at the element's time `+0x44`;
- they shift the position history - `+0x70` to `+0x80`, the new position to `+0x70`;
- every colour they produce is multiplied by the instance colour `+0x1F0` unless that is the neutral `80808080`;
- when the definition's byte `+0x49` is `0x20` or more, the alpha of each colour is scaled by the percent track at
  definition `+0x30` (skipped at 100);
- the first colour is copied to `+0x1F4`;
- **they all end in the same fork**: the cull test `005002E0(definition, position)` - *zero* **releases** the element
  through the seventh method `002F31C0`, *non-zero* runs its child-spawn slots through `003A8950` with trigger 2.
  Section 3 reads all three bodies.

**Type `0x01` - `00442600` (346 B): one point, one colour.** Position `+0x230` := the element's own `+0x60`,
transformed through the parent's matrix (`[+0x10] + 0x40`) when there is a parent; texture frame `+0x244` from the
track at definition `+0xD0`; colour `+0x240` from the colour track at `+0x80`. Its draw, `00442550`
([the distance-fade node's page](../Position-To-Scalar/how-a-position-becomes-a-single-number.md), section 13),
multiplies that colour by the distance fade and emits one projected primitive.

**Type `0x03` - `004428F0` (1,587 B): two points, two colours - a segment that can streak.** A rotation vector
(track `+0x80`, accumulated onto `+0xE0` when definition `+0x49` bit 3) and a scale vector (track `+0xC0`, multiplied by
`+0x100` when bit 2) are composed into a matrix - by one of two composers on definition `+0x4B` bit 1 - then through the
parent and the workbench view matrix. The first point `+0x230` is the offset track `+0x100` plus the element's
position, transformed. **The second point `+0x240` has three modes** (definition byte `+0x230`, bits 1-2): 0, a second
offset track `+0x140` plus the position, transformed; 1, that track's value as it stands; 2, **the first point's
previous position `+0x80` plus the track value** (scaled by the frame-rate float unless the half-rate predicate holds;
on the element's first frame the current first point is used instead) - a streak behind a moving point. Colours
`+0x250` and `+0x254` come from the tracks at `+0x190` and `+0x1E0`, or are the same colour when bit 0 of that byte is
set. Texture frame `+0x258` from `+0x180`. Its draw `004427D0` asks the distance-fade node once per end.

**Type `0x08` - `0044B3C0` (1,273 B): the track-dense one.** Eight vector tracks, two scalar tracks (`+0x1C0`,
`+0x1D0` into `+0x260` / `+0x264`), three integer tracks (`+0x2C0`, `+0x2D0`, `+0x2E0` into `+0x270`..`+0x278`), and **a
loop of four colour tracks** (definition `+0x2F0`, stride `0x50`, into `+0x2B0`..`+0x2BC`). Two components of the vector at
`+0x290` are converted **from tenths of a degree to radians** (`x 0.00174533`). It builds its own matrix at `+0x2C0`
from the rotation `+0x110` and the scale `+0x120`, through the parent, and places itself at the track `+0x180` plus its
position. Four colours suggest four corners; ~~its draw was not read, so that stays a suggestion.~~ **Confirmed 2026-09-29 (FABLE,
GI-8):** the walk `0044A620` interpolates them bilinearly across the grid ([the element types 0x00-0x0A](the-element-types-00-0a.md#what-every-walk-draws-and-who-authors-it-gi-8-2026-09-29-fable)).

| body | anchors |
|---|---|
| `00442600` type `0x01` tail (346 B) | `00442624`, `0044263B`, `0044264A`, `00442660`, `00442682`, `00442697`, `004426A9`, `004426C5`, `004426D7`, `0044270D`, `00442713`, `00442723`, `00442732` |
| `004428F0` type `0x03` tail (1,587 B) | `00442934`, `00442944`, `004429DD`, `004429F1`, `00442A85`, `00442AAA`, `00442AAF`, `00442AD5`, `00442AED`, `00442B0A`, `00442BA5`, `00442BAA`, `00442BCE`, `00442C32`, `00442C76`, `00442CBF`, `00442D02`, `00442DC2`, `00442DF3`, `00442E1C`, `00442E55`, `00442ED1`, `00442EF9`, `00442F08` |
| `0044B3C0` type `0x08` tail (1,273 B) | `0044B3F3`, `0044B413`, `0044B433`, `0044B451`, `0044B45A`, `0044B4F8`, `0044B50C`, `0044B5A6`, `0044B5C5`, `0044B5DC`, `0044B5F3`, `0044B61C`, `0044B692`, `0044B6E7`, `0044B708`, `0044B741`, `0044B776`, `0044B801`, `0044B825`, `0044B878`, `0044B888`, `0044B897` |

## 3. The fork at the end of every tail: cull, then release or spawn

*Drawing is not in the tail at all; it is the walk method's business -
[the element types 0x00-0x0A](the-element-types-00-0a.md).*

**`005002E0(definition, position)` (389 B, read whole) is a cull test; 1 means keep, 0 means cull.** Its rules come from
a **cull record**: the one at `+0x2E0` of the effect container currently being drawn (`[02F97348]`), or - when that
record's first byte is `0xFF` - the definition's own at `+0x60`.

| record field | meaning |
|---|---|
| byte `+0` | distance mode: `1` full 3D distance, `2` the same with Y (lane 1) zeroed on both points, anything else no distance test |
| float `+4`, `+8` | the window: cull when the distance is below `+4` or above `+8` |
| byte `+1` bit 0 | also test the screen: project the position through `02AEECB0`, cull if the clip routine rejects it or if the projected x or y word is outside `0x6000`..`0xA000` |

The distance is measured from the stashed point `02AED5F0` to the position after the workbench transform
(`02AEEA20`) - the same stash and the same matrix as the distance-fade node of
[how a position becomes a single number](../Position-To-Scalar/how-a-position-becomes-a-single-number.md). *Whose
position the stash holds is that page's open runtime item, not settled here.*

**On 0 the tail calls the seventh method `002F31C0(element, owner)`, and that is the element's release** (233 B, read
whole): the per-type teardown through the jump table, then the element is unlinked from its owner's active list (head
`+0x118`, tail `+0x128`, links at element `+0x28` / `+0x30`) and pushed onto the owner's free list `+0x120`. **An element
that leaves its cull window is destroyed, not hidden for a frame** - a reimplementation that merely skips drawing it
would keep emitters alive that the game kills.

**On 1 the tail calls `003A8950(2, element)` (394 B, read whole): the child-spawn slots.** The element's source record
(`[element + 0x18]`) has eight slots - a tag byte at `+0x298 + i`, a sub-resource index word at `+0x288 + 2i`, a start
word at `+0x2A0 + 2i`, a parameter word at `+0x2C6 + 2i` - and the element keeps a last-fired frame per slot at
`+0x1D0 + 4i` (-1 = never). With `f = trunc(element +0x3C)`:

| tag | fires when |
|---|---|
| 0 | never (empty slot) |
| 1 | **once**: never fired, and `f` has reached the start word |
| 2 | **repeatedly**, only on trigger 2, and not on odd frames (`+0x40` bit 0) while the frame-cadence predicate is off: first when `f` reaches the start word, then whenever the time since the last firing reaches an interval sampled from a track of the indexed sub-resource (`[[02EBEF90]][index] + 0x10`, through `004314E0`) |
| 3 | only on trigger 3 - ~~the expiry path of the base update, which calls this routine with 3 just before the release~~ **either end path of the base update, the lifetime arm or floor arm 2's height exit; each calls this routine with 3 just before the release (corrected 2026-09-29, OPUS falsification pass 1, `CON-179`)** |
| other | on every call |

Firing calls the sub-resource spawner `003A8AE0` with the index, the parameter word, the constant 2, a time (the
element's age, or for tags 1 and 3 the age less `+0x40`), two fields of the owner (`+0x1C`, byte `+0x1A`) and the element
as parent. **So trigger 2 is "this element lived another frame" and trigger 3 is "this element is ending"** - trails and
death bursts respectively. *The spawner itself was not read here.*

| body | anchors |
|---|---|
| `005002E0` cull test (389 B) | `0050030A`, `0050030F`, `00500319`, `00500348`, `0050036E`, `0050037B`, `005003C4`, `005003D9`, `005003F4`, `00500403`, `0050041A`, `00500442`, `00500448` |
| `003A8950` child-spawn slots (394 B) | `003A8981`, `003A89B0`, `003A89DF`, `003A89E8`, `003A89F2`, `003A8A01`, `003A8A2A`, `003A8A39`, `003A8A4A`, `003A8A58`, `003A8A97`, `003A8AA7` |

## 4. The other seven tails: types `0x02`, `0x04`, `0x05`, `0x06`, `0x07`, `0x0A`

*Counts (corrected 2026-09-29, OPUS falsification pass 1, `CON-179`): this section has six tails, not seven, and the method's "ten per-type tails" are nine tails
plus `0044B960`. That body is a shared random helper with 48 direct call sites, not a tail.*

All ~~seven~~ six read whole. Everything in "what every tail shares" (section 2) holds for them too, with one exception noted under `0x05`.
Three things are new and shared.

**1. Definition byte `+0x4A`, bits 2-4, is an orientation mode** (`(byte >> 2) & 7`; the tails test the mask `0x1C`).

| mode | what the tail does |
|---|---|
| 0 | the authored rotation is turned into a matrix (a composer taking the rotation vector `+0x110` and the definition's byte `+0x48`), and **when there is a parent that matrix is combined with the parent's** (`[+0x10] + 0x40`) |
| non-zero | the parent's matrix is *not* combined in - the position alone goes through the parent |
| 3 | additionally the matrix is multiplied by one **aligned to the element's motion**: `002F3570`, a wrapper that hands the world position history (`+0x70` newest, `+0x80` previous) to the builder below |
| 6 | the same from a **second, pre-parent position history** at `+0x90` / `+0xA0` - local motion. Only type `0x05` keeps that history and only it tests for 6 |

**The builder `002F35C0` (387 B, read whole).** After the first frame (`+0x40` non-zero) it subtracts the previous position
from the newest and **keeps the difference in the element at `+0x130` only when its length exceeds 0.001** - so an
element that stops keeps its last heading. *The difference is stored as it is; whether the matrix builder `003A2570`
normalises it was not read.* On the first frame it clears that direction and instead
prepares an up vector at `+0x140` - a vector read from the global `02064AB0`, its second lane then set to 1.0, carried
through the owner's matrix (`[+8] + 0x40`). Either way it then builds the matrix from the direction and the up vector.
*What that global holds was not established.*

**2. The scale is applied by one of two routines on definition `+0x4B` bit 1**, as in type `0x03`, and the finished
matrix gets the position as its fourth row with `w` = 1.0.

**3. "Round up to a multiple."** Types `0x04`, `0x06` and `0x07` each take one sampled integer `v` and a definition word
`m`: when `m` is 1 nothing happens; when `m >= v` the value becomes `m`; otherwise it becomes `(v / m + 1) x m` - **the next
multiple above, even when `v` already is one**. It reads like a segment count that must be a multiple of the shape's
symmetry; ~~the walks that would confirm that were not read.~~ **Confirmed 2026-09-29 (FABLE, GI-8):** the walks repeat the
texture `m` times around the shape, so the segment count must be a multiple of `m` ([the element types 0x00-0x0A](the-element-types-00-0a.md#what-every-walk-draws-and-who-authors-it-gi-8-2026-09-29-fable)).

**Type `0x02` - `00449560` (965 B).** Position `+0x270` is the element's `+0x60`, plus the offset track `+0x190` when
definition byte `+0x4E` is non-zero; in a non-zero orientation mode it goes through the parent at once. Integer track
`+0x150` into `+0x284`. **The colour track `+0x80` is sampled at a delayed time: the age `+0x44` minus the element's
word `+0x28C`, floored at zero** - into `+0x280`, then the instance colour and percent rules. The rotation track `+0xD0`
is skipped when definition byte `+0x180` has bit 5. In mode 0 only, the matrix at `+0x230` is built, combined with the
parent, scaled, and given the position (`+0x260`). The fork is reached by tail jumps, not calls.

**Type `0x04` - `00445B50` (1,269 B).** Rotation `+0x80`, scale `+0xC0`, offset `+0x100` into `+0x230`; **five float
tracks** (`+0x160`, `+0x170`, `+0x180`, `+0x140`, `+0x150` into `+0x240`..`+0x250`); integer `+0x190` into `+0x254`, **rounded
up to a multiple of definition word `+0x670`**; integer `+0x1A0` into `+0x258`; **three colours** (tracks from `+0x1B0`,
stride `0x50`, into `+0x25C`..`+0x264`), the *second* of which is the one copied to `+0x1F4`; float `+0x2A0` into
`+0x268`. Matrix at `+0x290`, position row `+0x2C0`. Mode 3 only.

**Type `0x05` - `0044A180` (1,071 B).** Rotation `+0xD0`, scale `+0x110`, offset `+0x150` into `+0x230`, integer
`+0x1A0` into `+0x290`, colour `+0x80` into `+0x240`. **The exception: it applies the percent track without testing
definition byte `+0x49`.** Matrix at `+0x250`, position row `+0x280`. It shifts the pre-parent history (`+0x90` to
`+0xA0`, the position before the parent transform to `+0x90`) and is the one type that handles both modes 3 and 6.

**Type `0x06` - `00447830` (1,436 B).** Rotation, scale, offset as `0x04`; **ten float tracks** (`+0x1C0`, `+0x1D0` into
`+0x240`, `+0x244`; `+0x140`..`+0x160` into `+0x254`..`+0x25C`; `+0x170`..`+0x190` into `+0x248`..`+0x250`; `+0x1A0`, `+0x1B0`
into `+0x260`, `+0x264`); integers `+0x1F0` into `+0x268` (**rounded up to a multiple of definition word `+0x6D0`**),
`+0x200` into `+0x26C`, `+0x210` into `+0x270`; three colours from `+0x220` into `+0x274`..`+0x27C`, the second copied to
`+0x1F4`, with the percent applied in floating point (`x percent / 100.0`, truncated); float `+0x1E0` into `+0x280`.
Matrix `+0x2B0`, position row `+0x2E0`. Mode 3 only.

**Type `0x07` - `00448800` (1,387 B).** The same frame as `0x06` with a different parameter set: eight float tracks
(`+0x140`..`+0x1B0` into `+0x24C`..`+0x268`), integer `+0x1F0` into `+0x26C`, then **a loop of two** - float tracks `+0x1C0`,
`+0x1D0` into `+0x240`, `+0x244` and integer tracks `+0x200`, `+0x210` into `+0x270`, `+0x274` - the second of those
integers being the one rounded up to a multiple of `+0x6D0`; three colours from `+0x220` into `+0x29C`..`+0x2A4`; float
`+0x1E0` into `+0x278`. Matrix `+0x2B0`, position row `+0x2E0`. Mode 3 only.

**Type `0x0A` - `0044C850` (959 B): a trail.** Position `+0x230` is the offset track `+0x180` plus `+0x60`, through the
parent; integer `+0x1C0` into `+0x450`; colour `+0x1D0` into `+0x240`; rotation `+0x80` (skipped on definition
`+0x2A4` bit 3) and scale `+0x100`. **Then a 32-entry position history at `+0x250`..`+0x44F`, newest first:** at age 0 all
32 entries are set to the current position; afterwards the newest entry is overwritten every frame, and the 31 older
ones are shifted down one place **only on cadence frames** - every frame when the frame-cadence predicate is on, odd
frames (`+0x40` bit 0) otherwise. No matrix is built.
**The step-only body `0044B960` (212 B)**, whose return the step stores at `+0x458`: when the mode word `022D9138` is
set it advances the render-local random stream `01EF93E8`
([rng-streams](../../21-RNG-And-Determinism/rng-streams.md)) ~~four~~ **five** steps (corrected 2026-09-29, OPUS falsification pass 1, `CON-179`: five recurrence
blocks precede the single state store at `0044BA00`) - each step keeps the float exponent bits, so
the state is always a float in [1, 2) - and returns that float's bits; otherwise it returns 1.0. **One random number
per trail, from the stream that is not world RNG**; ~~what the walk does with it was not read.~~ **Read 2026-09-29 (FABLE,
GI-8):** the walk `0044BAC0` seeds the render-local stream with it before drawing the trail's sprites and restores the
stream after, so each trail's random rotation and scale jitter is stable for that element.

| body | anchors |
|---|---|
| `00449560` type `0x02` tail (965 B) | `0044957C`, `0044959A`, `00449632`, `00449654`, `0044966E`, `0044967A`, `00449693`, `004496AF`, `004496F3`, `00449704`, `00449720`, `004497AE`, `004497CA`, `00449854`, `0044985A`, `00449872`, `0044989F`, `004498B2`, `004498C6`, `004498EA`, `0044990E`, `00449920` |
| `00445B50` type `0x04` tail (1,269 B) | `00445B91`, `00445C3A`, `00445CE8`, `00445D00`, `00445D20`, `00445D37`, `00445D4E`, `00445D65`, `00445D7C`, `00445D91`, `00445DAE`, `00445DBF`, `00445DEB`, `00445E13`, `00445E5E`, `00445E64`, `00445E9B`, `00445F36`, `00445F48`, `00445F63`, `00445F76`, `00445FB2`, `00445FB7`, `00445FE6` |
| `0044A180` type `0x05` tail (1,071 B) | `0044A1BB`, `0044A1D2`, `0044A260`, `0044A30E`, `0044A326`, `0044A343`, `0044A37E`, `0044A3C7`, `0044A3CF`, `0044A453`, `0044A466`, `0044A483`, `0044A494`, `0044A4AE`, `0044A4BA`, `0044A4BE`, `0044A4D8`, `0044A4E7`, `0044A523`, `0044A528`, `0044A555`, `0044A55F` |
| `00447830` type `0x06` tail (1,436 B) | `00447875`, `0044791E`, `004479CC`, `004479E4`, `00447A04`, `00447A1B`, `00447A32`, `00447A49`, `00447A60`, `00447A77`, `00447A8E`, `00447AA5`, `00447ABC`, `00447AD3`, `00447AE8`, `00447AFD`, `00447B31`, `00447B3D`, `00447B66`, `00447BC3`, `00447BE6`, `00447C1D`, `00447CB8`, `00447CEC`, `00447CF8`, `00447D34`, `00447D39`, `00447D65` |
| `00448800` type `0x07` tail (1,387 B) | `00448841`, `004488E6`, `00448994`, `004489AC`, `004489CC`, `004489E3`, `004489FA`, `00448A11`, `00448A28`, `00448A3F`, `00448A56`, `00448A6D`, `00448A96`, `00448AAB`, `00448ACE`, `00448AF0`, `00448B18`, `00448B40`, `00448B8D`, `00448BC4`, `00448C5F`, `00448C91`, `00448C9D`, `00448CD9`, `00448CDE`, `00448D09` |
| `0044C850` type `0x0A` tail (959 B) | `0044C883`, `0044C917`, `0044C940`, `0044C95E`, `0044C969`, `0044C985`, `0044C9A1`, `0044C9E5`, `0044C9F6`, `0044CA12`, `0044CAA0`, `0044CABC`, `0044CB46`, `0044CB4C`, `0044CB7C`, `0044CB85`, `0044CB8B`, `0044CBB4`, `0044CBC9` |
| `0044B960` type `0x0A` step-only random (212 B) | `0044B967`, `0044B96D`, `0044B975`, `0044BA00`, `0044BA0E`, `0044BA1D` |
| `002F35C0` motion-aligned matrix (387 B) | `002F35CA`, `002F35D4`, `002F35F1`, `002F364A`, `002F3687`, `002F368C`, `002F369A`, `002F36AE`, `002F36BC`, `002F36DC`, `002F370F` |

## 5. The half-rate mode, in one place

Three things on this page depend on "the frame-cadence predicate". That predicate is the engine's
**half-rate test** ([game settings and runtime config](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)):
it returns 0 only in half-rate mode (`01F82E38` non-zero and `01DFE0C0` zero). So **in half-rate mode** repeating child
slots (tag 2) are skipped on odd element frames, and a type `0x0A` trail shifts its history on odd frames only; at
full rate both happen every frame.

## Cross-subsystem neighbours

**CoreRuntimeScheduling - SERVICE.** `003A8950`, `0044C850` and the base update call `001EDDA0`, the 27-byte half-rate
test owned by that layer (read whole: two global compares, returns 0 or 1). The elements only ask it; nothing of theirs
is stored there. The crossing is that call, not a shared responsibility.

**Audio - SHARED LEAF.** The clamp pair `003A2A10` calls, `0036DDA0` and `0036DD90`, are also invoked by Audio bodies
`00361DE0` and `003623C0`. The elements only borrow the clamps; Audio's own use of them is not claimed here. The
crossing is those calls, not a shared responsibility.

**Movement - SERVICE (1 edge; FABLE 2026-09-29).** The floor probe `002F3750`, whose height the base's floor arms compare with `+0x64`, calls `00264670`, a 35-byte getter filed to that layer: for a class-3 actor it returns the float at `+0xD4` of the context behind the actor's `+0xB8`, otherwise 0.0 (`00264670`-`00264692`). The probe uses it only when the definition's `+0x4B` bit 2 is set and the low seven bits of its `+0x4F` choose an anchor: it resolves an actor from the `0x740`-stride table at `[022C6F28]`, adds the getter's float to the definition's `+0x70` and caches the sum at `+0x220` (`002F37B1`-`002F3823`); with bit 2 clear the floor is `+0x70` alone, and with `+0x4F` bit 7 set the cached `+0x220` is reused once the element is past its first frames (`002F378A`-`002F37AB`). So a floor-armed element can take its floor from an anchor actor's movement context; the element reads that field and never writes it. The context at `+0xB8` is the movement context ([the movement body pool](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md), after its 2026-09-18 label correction). Read from the shipping bytes.

## SWE2-EC7-56 update (2026-09-19) - `003A2570`

`003A2570` (285 B) is an effect-element body - `00250010`/`00398470`/`003A27C0`/`00808C40` plus `01F44830` cookie. Interior anchor `003A25AA` (a `00250010` call).


## SWE2-EC7-68 update (2026-09-19) - `002F3570` element transform compose

`002F3570` (69 B) is the compose wrapper the element readers run:
`002F35C0(&stack, rdx+0x80, rdx+0x70)` fills a scratch `0x40`-byte
block from the element's `+0x80`/`+0x70` fields, then four `movaps`
pairs copy the block verbatim into `rcx` and the body returns it.
Interior anchor `002F3589` (the `002F35C0` call).

## SWE2-EC7-90 update (2026-09-20) - `003A2A10` staged division transform measured

`003A2A10` (261 B) is the SSE transform the element callers
run: the `[rcx]` vec4 is staged through `022D92E0`, each
component divides by `edx` (`cvtdq2ps`) into `022D9300`,
`022D9198`, `022D92F0`, `022D9304`, `022D9308`, and every
zero-test arm runs the `0036DDA0`/`0036DD90` clamp pair before
the staged vec4 returns into `[rbx]` - a normalized-division
record build with clamped denominators.
Interior anchor `003A2A93` (the first `0036DDA0` call).

## Falsification pass 1 — 2026-09-29 (OPUS): the tails, the cull, the release and the spawn slots survive; type 0x00, the second end, the step count and two counts do not

**Attack.** Sections 1 to 5 were turned into checks at their cited instructions, and so were the dispatch page's
reading of the base. Competing case: the update dispatcher's own mapping for all eleven types. Script:
`Tools/analysis-kit/gfz-scripts/falsify_effect_element.py`, output `falsify_effect_element.out`, image `73461d08…`,
0 BROKEN, exit 0. What sections 3 and 4 leave unread stays open: the spawner `003A8AE0`, whether `003A2570`
normalises, and the draws.

| # | Clause attacked | Result |
|---|---|---|
| E11 | section 1's "child spawns happen only for elements that passed the cull on that frame, or that are expiring" | **refuted** (`CON-179`). The dispatcher sends type `0x00` to the base alone. With the type byte (definition `+0x44`) zero, the base runs `002F3890` and `003A8950(2)` at `002F2C76`, and the base never calls the cull test. The clause holds for the nine tail types |
| E12 | section 1 and the tag-3 row: expiry as the lifetime arm | **refuted** (`CON-179`). Floor arm 2's height exit (`002F2A5F` to `002F2D37`..`002F2D52`) is a second trigger-3 + release |
| E10 | section 4: `0044B960` advances the stream "four steps" | **refuted** (`CON-179`). Five recurrence blocks precede its single store at `0044BA00` |
| E13 | the method's "ten per-type tails"; section 4's "other seven" | **refuted** (`CON-179`). There are nine tails plus the shared helper `0044B960` (48 call sites), and section 4 lists six |
| E15 | the dispatch page: "released (`002F3890`)", "the 394-byte kind-3 release" | **refuted** (`CON-179`). `002F3890` is the history shift and colour copy. The 394-byte body is the spawn slots. The release is `002F31C0` |
| E0 | sizes | **survives**: all nineteen |
| E1 | section 2 / 4: the fork | **survives**: the order is cull, then release, then spawn(2) in all nine tails, and type `0x02` reaches the last two by tail-jump. Only `0x05` skips the `+0x49` test |
| E2 | section 3: the cull test | **survives**: the record at `[02F97348] + 0x2E0`, or definition `+0x60` on `0xFF`. Mode 2 zeroes lane 1 on both points. The window is `+4` / `+8`; the screen window is `0x6000`..`0xA000` |
| E3 | section 3: the release | **survives**: links `+0x28` / `+0x30`, head `+0x118`, tail `+0x128`, free list `+0x120` |
| E4 | section 3: the spawn slots | **survives**: eight slots at the cited offsets. Tag 2 needs trigger 2 and has the odd-frame skip; tag 3 needs trigger 3. Each firing calls `003A8AE0` with 2 |
| E5 | section 4: the builder | **survives**: the 0.001 threshold; the first-frame up vector from `02064AB0` with lane 1 = 1.0 |
| E6 | section 4: modes 3 and 6 | **survives**: mode 3 is in types `0x04`–`0x07`; only `0x05` tests mode 6, on `+0x90` / `+0xA0` |
| E7 | section 4: round-ups, delayed time, degrees | **survives**: `+0x670` / `+0x6D0`; the floor at zero; `0.00174533` |
| E8 | section 4: the trail history | **survives**: 32 entries filled at age 0, 31 shifted on cadence frames |
| E9 | section 5: the half-rate test | **survives** |
| E14 | competing case for E11 | **survives**: type `0x00` is the base alone; each of the nine types runs the base and then its cited tail; `0x09` goes to the default arm |

Corrected in place: sections 1, 3 and 4 of this page, plus UQ-206's item 4 and completion clause on the dispatch page.
The same wording in OPEN-QUESTIONS UQ-206 is routed to SWE2-DATA, which holds that file. The consumer record is
`_index/candidates/effect-element-falsification-pass-1-0929/`.
