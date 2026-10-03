---
system: How a character fades - the ten channels of a character render record
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every body that addresses record +0x4C0..+0x50F by displacement was found with an image-wide
    displacement sweep restricted to the character-render band and disassembled whole (the stepper, the ramp
    starter, the immediate setter, the three-way reset, the evaluator, the composite, the vector builder);
    every direct call to the three index-taking functions was read for its channel constant by a members
    script whose three call counts are checked against an independent raw E8/E9 sweep (22 = 22); the two
    script verbs were joined through the verb table
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-fade-channels-falsification-pass-1
  note: written by FABLE from the uncredited-body breakdown (five unresolved bodies of 600 to 960 bytes sat
    in this band); pending first review
---

# How a character fades - the ten channels

A character on screen does not have one opacity. Its render record carries **ten independent fade channels**,
each a small linear ramp in 4.12 fixed point, and what is drawn is a **product of several of them**. Distance
fade, the fade that stops the viewer looking through a body it is standing inside, the show/hide of an attached
piece, and the script verb `rgbatrans` all write *different* channels, which is why they never fight: a script
can fade a character out while the distance fade is fading it in, and the result is simply the product.

The record is the `0x740`-byte character render record of
[the character render record array](the-character-render-record-array.md); this page is its bytes
`+0x4C0`..`+0x50F` and the word at `+0x4B4`.

## 1. What the player sees

- A character far away fades in over a band of distance instead of popping, and is gone in one frame when
  culled (channel 0).
- A character the viewer moves into fades out over three frames and back in over three when the viewer leaves
  (channel 4).
- A piece attached to a character (a record of kind `0x1C` or above whose owner's kind is `0x11`..`0x15`) can
  be hidden at once or over five frames from its owner's state (channel 1).
- A script recolours or fades an actor over a number of frames with `rgbatrans(r, g, b, a, frames)` - four
  channels at once (6, 7, 8, 9).

## 2. One channel

```c
struct FadeChannel {            /* 8 bytes; ten of them at record + 0x4C0 */
    int16_t base;               /* +0  Q12: the value the ramp started from           */
    int16_t delta;              /* +2  Q12: target - base                             */
    int16_t progress;           /* +4  Q12: 0 .. 0x1000                               */
    int16_t step;               /* +6  Q12: added to progress each frame; 0 = at rest */
};

value(c) = c.base + ((c.delta * c.progress) >> 12);          /* every reader computes exactly this */
```

**Starting a ramp - `003E5D60`** `(record, channel, float target, int frames)` (182 B). It first *collapses* the
channel - `base += (delta * progress) >> 12`, so a ramp interrupted half way continues from where it is, not
from where it began - then sets `delta = (int)(target * 4096) - base` and
`step = 0x1000 / (max(frames, 1) * [01DFE0B4])`, the last factor being the engine's frame-rate multiplier.
`progress` restarts at `step`, **except for channel 1, where it restarts at 0**; and when the global dword
`01F82E38` (read through the seven-byte getter `001EDE70`) is non-zero a second `step` is added at once.

**Setting a value - `003E5D00`** `(record, channel, float value)` (44 B): `base = value * 4096`, the other three
words zero. `CharacterRenderRecord_ResetDefaults` calls it for all ten channels with `1.0`.
**`003E5D30`** `(record)` (34 B) puts channels 0, 1 and 4 back to exactly `1.0` with three qword stores.

**One frame - `003E4370`** `(record)` (88 B), called from the root and the child animation-presentation-phase
updates. For each of the ten channels with a non-zero `step`: if `progress` has reached `0x1000` the ramp is
finished - `base += delta`, and `progress` and `step` are cleared together - otherwise `progress += step`,
clamped to `0x1000`. A channel at rest costs one test.

## 3. Who writes which channel

Read from every call site ([fade_channel_census.py](members/fade_channel_census.py),
[fade-channel-census.tsv](members/fade-channel-census.tsv); 11 ramp starts, 3 immediate sets, 8 evaluations):

| channel | offset | written by | meaning |
|---:|---|---|---|
| 0 | `+0x4C0` | `CharacterRenderRecord_UpdateDistanceFadeAndCull` (`0042E850`) | **distance fade.** Inside the fade band the target is `sin(t * pi/2)` of the normalised distance left, otherwise `1.0`, over 1 frame; when the record's cull bits (`+0xD3` and `0x0B`) are up, `0.0` over 1 frame |
| 1 | `+0x4C8` | `0042E1F0`, `0042F880`; *and, added 2026-09-19,* authored presentation command `0x23` (`00520180`, 47 B) through a second forwarder `004293C0` (67 B) | **attached-piece visibility.** `0042E1F0` sets it to `0.0` at once when the owner's flag `0x08000000` of `+0x284` is up or the owner's `+0xCC` low twelve bits equal `0x35`; otherwise to `1.0` at once, or a ramp to `0.0` over 5 frames, by bits 0-1 of `+0x40B` |
| 2 | `+0x4D0` | the actor-service forwarder `002E8B10` `(actor, value, frames)` (77 B), through `00428940` | *Corrected 2026-09-19 - this row first said* nothing. **The time stop's set 5** ([the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md), section 5): for every actor queued on its manager the per-actor pass `00226640` calls the forwarder with `0.0` together with the registry's 0.0 arm and with `1.0` together with its 1.0 arm, over *fade + 1* frames - **the actors a time stop removes fade out, and fade back in afterwards**, while the effects dim on the same clock. *Added 2026-09-19; that page had the call sites all along and called the value an animation rate* |
| 3 | `+0x4D8` | **nothing found** | reset to `1.0`; no writer in the sweeps of this page, *which have now missed writers twice - see the correction under this table* |
| 5 | `+0x4E8` | the status looks of the second block, through `00428940` | *Corrected 2026-09-19.* **Invisibility**: held at `1 - (0.6 + 0.2 p) x envelope`, a pulsing 20 to 40 percent opacity ([how a status shows](how-a-status-shows-on-a-character.md) section 4); back to `1.0` when the look leaves or status display is denied |
| 4 | `+0x4E0` | `0042E850` | **viewer-inside fade.** When the viewer's horizontal distance is under `0.15 + [record+0x2A8]` and its height is inside the body's band, ramp to `0.0` over 3 frames; otherwise to `1.0` over 3 frames; bit 5 of `+0x4B7` remembers which. Skipped unless bit 4 of the render-record system tail's flag byte `+0x48818` is up (section 4c) |
| 6, 7, 8, 9 | `+0x4F0`..`+0x508` | `00428C40` `(record, r, g, b, a, frames)` (131 B) | **script colour.** Four ramps started together with one frame count |

### 3a. The other writer of channel 1: completing a pending attachment

`0042F880` (608 B) is the handler of dirty bit 19 of the record's `+0x290`, and it was read whole because this page
cites it. A record waiting to be attached carries its **owner's record index at `+0x3CE`** and an **attachment slot id
at `+0x3CC`**. The handler:

1. takes the owner from the record array and gives up unless the owner is live (`+0x284` non-zero) and **both** records'
   resource entries resolve (index `+0x18` in the table at `+0xD98` of each one's resolved base) - so a piece whose
   model is not loaded yet stays pending: every early exit leaves bit 19 set;
2. for slot **`0x10A`** on a piece of kind `0x1C` or above whose owner's linked record (`+0x2C8`) has a kind in
   `0x11`..`0x15`: notes whether bits 0-1 of the owner's `+0x40B` are both clear, and re-targets the attachment to that
   linked record (falling back to the original owner when the link does not resolve);
3. if the piece is attached to a different record already, detaches it (`004288B0`); if it has any parent, sets bit 6
   of `+0x3D1` and runs `0042F4C0`;
4. attaches: `004215A0(owner, slot, piece)`;
5. **if step 2 found the two bits clear, sets channel 1 to `0.0` at once** - the piece arrives hidden, the same rule
   `0042E1F0` applies every frame afterwards, which would otherwise take five frames to hide it;
6. for slot **`0x7FFF`**: copies `00421CD0(owner)` into the piece's model instance at `+0xB6` and resolves each of the
   owner's `+0xC2` entries at `+0x90` through the table at `+0xDA0`;
7. commits: `piece+6 = owner's id`, `piece+0x2C4 = owner's +0x18`, clears bit 19, and calls `00426E40(owner, piece)`.

> **Correction 2026-09-19 (FABLE): channels 2 and 5 are written; this page said no body in the image writes them.**
> `00428940` `(record, channel, value, frames)` (20 B) is a forwarder: `frames <= 1` goes to the setter `003E5D00`, anything
> else - for a non-null record - to the ramp starter `003E5D60`. **It reaches both by conditional jumps** (`jle`, `jne`),
> and the census this section rests on counted `call` and `jmp` sites only, so its 11 + 3 sites were never the whole
> story. The forwarder has six callers by a raw sweep: five in the status looks' second block (channel 5) and the
> actor-service forwarder `002E8B10` (channel 2). **An image-wide sweep of conditional jumps into the setter and the ramp
> starter, run for this correction, finds exactly two such forwarders**: this one and `004293C0` `(record, channel, value,
> frames, flag)` (67 B), which with flag 1 redirects to the record's attached child at `+8`; its one caller is authored
> presentation command `0x23` (`00520180`), reached through the command table, which passes channel 1 with the value,
> frame count and flag of its command record. The members census is left as it was generated, with this note as its
> erratum; the lesson - sweep conditional jumps to a setter before writing *never* - was already in my notes and was
> not applied.

Channels 6-9 are reached from the script verbs **`rgbatrans`** (`03B2`, five arguments) and
**`puppetrgbatrans`** (`0535`, six) through the two actor-service forwarders `002E84B0` and `002E8500`, each of
which tail-jumps into `00428C40`. The names are the game's own.

## 4. Who reads them

**`CharacterRenderRecord_EvaluateQ12PresentationChannel` - `003E48E0`** `(record, selector)` (604 B). Its body is
four copies of the formula of section 2 and nothing else:

| selector | returns |
|---|---|
| 0..9 | `value(selector)` - one channel (any selector other than the three below is used as a channel index unchecked) |
| `0x0B` | `value(0) * value(1) * value(2) * value(3) * value(4)` |
| `0x0D` | `value(1) * value(2) * value(3) * value(5)` - **everything but the two view-dependent fades** |
| `0x0E` | `value(0) * .. * value(5)` - all six |

each product renormalised with `>> 12` after every factor. ~~Since channels 2, 3 and 5 are never written, in this
build `0x0B` and `0x0E` are both `distance * piece * viewer-inside` and `0x0D` is the piece channel alone.~~
*Corrected 2026-09-19:* channel 3 alone is a constant one. **`0x0B` leaves out channel 5, so whatever asks for
`0x0B` ignores invisibility; `0x0D` and `0x0E` carry it; all three carry channel 2.**
`UpdateRootLODAndPresentationState` asks for `0x0D` and `0x0E`; `0042FB20` `(handle)` (85 B) returns selector `0x0B`
as a float, or `1.0` for handle -1 or a record whose `+0x284` is zero; three large Presentation bodies read
channel 4 alone.

**`CharacterRenderRecord_UpdateCompositePresentationFactorQ12` - `003E4240`** `(record, parent)` (269 B) computes the
six-channel product inline and stores it in the word at **`+0x4B4`**; given a parent record it multiplies by the
parent's `+0x4B4` first, so **an attached piece inherits its owner's fade**.
`ComputeCompositePresentationScalar` (`003E4730`) turns that word into the float
`(+0x4B4 / 4096) * [+0x22C] * [+0x2EC] / 255`, and its sibling `003E4780` takes the last factor from its caller
instead of `+0x2EC`.

**`CharacterRenderRecord_BuildPresentationChannelVector4` - `003E51F0`** `(record, float out[4])` (701 B) is the
evaluator inlined in a loop over selectors 6, 7, 8 and 9, each divided by 4096: the `rgbatrans` colour as four
floats. The three product branches are compiled into the loop and can never be taken, because the loop variable
only runs from 6 to 9.

## 4a. Where the numbers go: an attached record's frame

`CharacterRenderRecord_UpdateChildLODAndPresentationState` (`0042CBF0`, 884 B) is where the channels leave the record
and reach the model instance the renderer draws. It was read whole. It runs for a record whose `+0x284` has bit 2 up,
whose `+0x2AE` has bit 1 down and whose parent index at `+6` is valid.

1. **The parent.** The parent is looked up in the record array and counts only if live (`+0x284` non-zero);
   `SelectLODForViewDepth` is called with it. **If the parent is gone the record orphans itself** - `+6` := -1,
   `+0x2F0` := `0xFFFF` - and computes its own projected origin and view-dependent factors like a root.
2. **Otherwise it borrows the parent's view.** It copies the parent's `+0x2D0` and `+0x2D4`, takes the parent's sort depth
   `+0x2D8` **plus 2.0** as its own - an attached piece always sorts just behind its owner - and climbs the parent chain
   to the top, remembering the last ancestor whose `+0x284` has bit 14 up. If that ancestor's `+0x2CA` names this record
   and a lookup on the record's id succeeds, the record computes its own view-dependent factors; if not it copies the
   ancestor's block at `+0x2E0`.
3. **The fade.** `UpdateCompositePresentationFactorQ12(record, parent)` - the six-channel product times the parent's, into
   `+0x4B4`; `BuildPresentationChannelVector4` - the `rgbatrans` colour; and
   **`+0x49C` := `ComputeCompositePresentationScalar` x the colour's alpha**. That float is the record's final opacity.
4. **Into the model instance** (from `CharacterRenderRecord_ResolveModelInstance`): instance `+0x90` := the record's
   colour at `+0x210`; instance `+0xA0` := the record's second colour at `+0x220` x the `rgbatrans` colour; instance
   `+0xB0` := the Q12 word `+0x4B4`. **With bit 26 of `+0x284` up and a live parent, the parent's colours are used
   instead**: `+0x90` from the parent's `+0x210`, and `+0xA0` from the parent instance's `+0xA0` times this record's own
   product. The opacity is also handed to the record's effect object, when it has one.
5. **Sort key and matrix.** The sort depth, truncated toward zero and saturated to a 32-bit integer, goes to instance
   `+4` (and to the global `022D9144`); a negative key has `0x7FFFFFFF` added. Instance `+0x50` receives the record's
   matrix at `+0x1C0` when bit 13 of `+0x284` is up and the shared matrix at `02AEDDB0` otherwise.
6. **Last.** A valid phase entry index at `+0x450` is published to instance `+0x1E4` with its resolved sub-block at
   `+0x1E8`; the opacity **times the parent's opacity** goes to the record's four auxiliary handles
   (`PublishScalarToAuxHandles4`); a record with a **render-object handle** at `+0x288` has bit 2 of that object's table entry (`+0x30`) set from a value of
   its own and bit 1 raised (`003B33A0`, 46 B; *this step first called `+0x288` a distance-fade entry, a name taken from the
   struct tiers - it is the handle into the render-object table of section 4d*); and the parent's blend state
   (`+0x4A0`..`+0x4B3`) is copied down and published.

So an attached piece is faded three times over by its owner - through the Q12 composite, through the owner's colours
when bit 26 asks for them, and through the owner's opacity on the auxiliary handles - which is why a weapon never
outlasts the hand that holds it.

## 4b. The projected origin, and why channel 4's point is the camera

`CharacterRenderRecord_UpdateProjectedOriginState` (`0041EC00`, 480 B), which a root record and an orphaned piece run
(section 4a, step 1), was read whole, and it settles two things this page had left open.

It multiplies the record's world matrix `+0x180` by the matrix at **`02AEDDB0`** and sends the origin `(0, 0, 0, 1)`
through the product into `+0x2D0`..`+0x2DC`, then divides the first three components by the fourth: `02AEDDB0` is the
**world-to-clip (view-projection) matrix**, `+0x2D0`..`+0x2D8` the record's projected origin, and `+0x2D8` the **sort
depth** that an attached piece inherits plus 2.0. It then takes the vector from **`02AEDF20`..`02AEDF28`** to the record's
position (`+0x1B0`), measures its length, builds the view-space point `(0, 0, -length)`, and sends it through the matrix
at **`02AEDEF0`** and then through `02AEDDB0` to obtain a reference `w`, which replaces `+0x2DC` - with the sign of the
record's own `w` kept - when its magnitude clears a small threshold.

A point on the view axis goes through `02AEDEF0` *before* the world-to-clip matrix, so **`02AEDEF0` is the camera's
view-to-world matrix**, and `02AEDF20` is that matrix's fourth row - its translation. **The point channel 4 measures
against is the camera position.** (This page first gave the block's start as `02AEDF00`; that is the matrix's second
row. The matrix has no rip-relative store in the image and is filled by a copy.)

## 4c. The cull decision that drives channel 0

This page took credit for `0042E850` on the strength of its second half. Its first half was read afterwards, with the
two bodies under it, and is what decides the three cull bits of `+0xD3`.

**The settings are the render-record system's, not the camera's.** `+0x48818`..`+0x4882C` are offsets from the record
array's base `[022C6F28]` - 160 records of `0x740` bytes end at `0x48800`, so these are fields of the system tail: a flag
byte at `+0x48818` (bit 0 *culling on*, bit 4 *camera-inside fade on*), the **clip distance** `+0x4881C` (where the distance fade
starts), the near limit `+0x48820`, the **fade range** `+0x48824` (how far past the clip distance a character is gone) and a
**reference record index** at `+0x4882C`. *Relabelled 2026-09-19: this sentence called `+0x4881C` "the fade band" and
`+0x48824` "the far limit" - the reverse of what the script verbs below put there. The arithmetic on this page was
right throughout; only the two names were swapped.* *(The channel table above said
"the camera block's `+0x48818`"; that was wrong.)*

**Who reads bit 0 (added 2026-09-19, on `OPUS-REQ-FABLE-PHOOK-BIT0-WHO-READS-IT`).** An image-wide sweep of the
displacement `0x48818` finds ten bodies touching the word. Bit 0 is *set and cleared* by the distance-cull enable
family (`002E8CC0`, `002EBBB0`, `002EBBF0`) and the initialiser, and **read by this routine alone** - three tests.
This routine's one caller `0042D7A0` has no call site: it is the per-record callback of the distance-fade *system
phase* (taken by `lea` at `0042650E`). *Read whole 2026-09-19 (100 B): it runs only for a live root record - record
`+0x284` bit 2 set, `+0x2AE` bit 1 clear, no parent - calls this routine, then a second per-record step, and when a third
predicate holds and the handle at `+0x288` is not -1 tail-calls a setter on that handle with a value computed from the
record. ~~The two steps and the setter were not read.~~*

**That tail is the character's half of an effect handshake (read whole 2026-09-19, FABLE).** The step is `00421030`
(157 B): it keeps record flag bit 6 equal to a **chain test** - bits 3, 4 and 5 of `+0x284` all up on this record *and
on every ancestor up the parent chain* (`+6`) - and drops the pending bit 10 the first time the test passes. The
predicate is `004210D0` (72 B): **flag bit 4 up on the record and on every ancestor.** When it holds and the record
has an effect handle, the setter `003B33A0` (46 B) finds the handle's entry in the 64-entry table `02EBD480`, **raises
the entry's bit 1 and sets its bit 2** from `00420FB0` (81 B), which is the same chain test as the step's. Bit 1 is
the one-frame permission the effect draw consumes
([the six VFX display layers](../Effect-File-Formats/the-six-vfx-display-layers.md),
section 1b): **an effect hung on a character is drawn exactly while the character and everything it is attached to is
flagged shown, renewed every frame.** ~~What bits 3, 4 and 5 are called was not established.~~ *The setter's two other callers, both record phases, ~~were~~*
*~~not read~~.* *(answered: see the setter `003B33A0` has three callers, `0042CBF0`+0x330, `0042D7A0`+0x59 and `0042D830`+0x3A; `0042CBF0` is read whole in section 4a; 2026-10-02, OPUS)*

**The three bits, by their setters (added the same day; a displacement sweep finds one setter each).** **Bit 3 is
"not culled this frame"**: `00421010` (29 B, read whole) is called by this page's fade-and-cull routine with 1 when
none of the cull bits 0, 1 and 3 of `+0xD3` is up and with 0 otherwise. **Bit 4 is "display requested"**: `00420F90`
(29 B, read whole) is called by the dirty-state pass, on dirty bit 4 of `+0x290`, with bit 1 of the requested-state
word `+0x304`. Both setters tail-jump into the chain step `00421030`, so bit 6 is re-derived at once. **Bit 5** has
one setter, which mirrors it into bit 2 of the record's model resource entry; ~~*what it means was not established.*~~
So the permission needs *display requested* on the character and every ancestor, ~~and the flag handed over with it
says whether the whole chain is also unculled.~~

**Corrected 2026-09-19 (FABLE): bit 5 has no live source, so that second flag is always 0.** The setter `0041FBF0`
(135 B, read whole) is called only by the propagation `00429D40` (271 B, read whole) and its descendant callback
`0042DE50` (59 B): the value is **bit 2 of the requested-state word `+0x304`**, applied to the record, its child and
their descendants. `00429D40` runs only under **dirty bit 5 of `+0x290`**. Neither end is alive in this image: of the
instructions with displacement `0x304`, the mask operations cover bits 0, 1 and 3-31 and **none touches bit 2**;
the record is zero-filled at creation; and nothing raises dirty bit 5. So bit 5 is never set, the three-bit chain
test `00420FB0` returns 0 for every record, **the handle entry's bit 2 is constant 0**, and the chain step never
sets record bit 6 through that test. The permission itself (bit 1, from bit 4 alone) is unaffected. *A bounded
negative: whole-image displacement sweeps; a writer through a shifted base would escape them.* The record pool's promotion path clears bit 0, runs the *animation presentation*
phase `0042C410` on the new record, and puts the bit back
([the pool lifecycle contract](../CONTRACT-render-record-pool-lifecycle.md)); a breadth-first search of the static
call graph from `0042C410` reaches 276 bodies and **none of the ten**. So by static evidence nothing under that call
reads or writes the bit it is protected from. *Not followed: the presentation-entry callbacks that phase dispatches
indirectly.*

**The switch is a veto mask (added 2026-09-19; the three setters read whole - 32, 50 and 64 bytes).** Bit 0 is never
set directly: it is derived from the byte `0215FD56`, in which **each requester owns one bit**.
`002EBBF0(requester, enable)` clears that requester's bit to enable and sets it to disable; `002EBBB0(enable)` is the
same for bit 0; `002E8CC0` only re-derives. After any of them the flag bit is 1 exactly when the byte is zero - **culling
is on only while nobody objects**, and two systems that both switched it off must both switch it back on.

| requester | who | evidence |
|---|---|---|
| 0 | the script verb **`setcharclipall`** (call id `0x156`; its handler pops one integer and tail-jumps to the bit-0 setter) | 714 calls with `0` and 479 with `1`, in 287 of the 1,114 decompiled scripts - cutscenes switch the cull off so distant actors stay drawn |
| 1 | bit 35 of a 64-bit state word, applied by the world tick's state applier | only the call site was read (`002265C8`..`002265D6`) |

*A reimplementation that keeps one boolean instead of the mask will re-enable culling too early whenever a script and
the tick both hold a veto.*

**The script's side of the two distances (added 2026-09-19; four verb handlers and their setters read whole).**

| verb (call id) | handler | what it does |
|---|---|---|
| `setcharclipdistance` (`0x327`), two numbers | `00348B00` | pops the **range**, then the **distance**, and writes both live: the distance to `+0x4881C`, the range to `+0x48824` |
| `setcharclipdefaultdistance` (`0x33E`), one number | `00348700` | stores it as the **default** distance (`021641F4`) *and* as the live one |
| `setcharclipdefaultfaderange` (`0x33F`), one number | `003497D0` | the same for the range (default at `021641F8`) |
| `setcharclipdefaultdistance`, two-number form (`0x340`) | `00348F20` | both defaults and both live values |

The system starts at **34.0 and 4.0**. In the 1,114 decompiled scripts the two-number verb is called with (22, 3) 103
times, (27, 3) 15, (28, 2) 13, (20, 3) 6, (50, 2) 5, and 15 times with `getcharclipdefaultdistance()` as its first
argument - putting the default back; the defaults themselves are changed three times, to (33, 2), (28, 2) and (23, 2).
**So areas pull the clip distance IN from 34 to the low twenties and keep the fade range at 2 or 3**, and the veto verb
above is how a cutscene escapes it altogether.

**The routine.** It clears bits 0, 1 and 3 of `+0xD3`; builds a unit box (-0.5..+0.5) and the frame of
[the focus point](the-focus-point-of-a-character.md) (`003E5FA0`); takes the two horizontal extents from `003E4DD0` and keeps the
larger as a radius; and, unless the model's primary config block has bit 4 of `+0x134` up, tests the box
with `0046C180`. It multiplies the frame by the matrix at **`02AEDDF0`** and reads the product's translation as the
record's position relative to the camera: depth from its third component, distance from its length - **unless** the
tail's reference record is live with bit 2 of `+0x284` up, in which case distance is measured from that record's point
instead, and is 0 for the reference record itself.

| cull bit of `+0xD3` | set when (tail bit 0 up throughout) |
|---|---|
| 0 - outside the view | bit 21 of `+0x284`, bit 0 of `+0xD2`, and the box test failed |
| 1 - too far | bit 4 of `+0xD2` and bit 1 of `+0xD2`, and distance is at or beyond clip distance + fade range |
| 3 - behind | bit 21 of `+0x284`, bit 3 of `+0xD2`, and depth + radius is below minus near |

A non-zero `+0x6E0` cancels all three - *and `+0x6E0` is "this record belongs to the handbook's monster viewer"
(named 2026-09-19, FABLE: its one setter is the viewer's model loader;
[the handbook's monster viewer](../../16-UI/Handbook/the-handbooks-monster-viewer.md)), so in the world it is always 0.* (A second cancel is keyed on the return of `005C5230`, which is a folded stub
that returns 0 in this build, so that arm is dead.) Any bit left up ramps channel 0 to `0.0` in one frame.

**The box test.** `0046C180` `(box, frame)` (91 B) multiplies the frame by `02AEDDF0`, installs the product as the
classifier's matrix at `02B403F0` (`003B4140`, a 15-byte copy), and calls
`RenderBounds_ClassifyViewFrustumIntersection` (`003B3F10`, 416 B): the eight corners of the box, picked by a table of
min/max selectors at `00D114C0`, are each transformed and given a six-bit outcode - `x > |w|`, `x < -|w|`, and the same
for `y` and `z`. The return is 2 when some plane has **every** corner outside it, 1 when **any** corner is outside some
plane, 0 when the box is wholly inside; `0046C180` and its sibling `0046C0D0` (162 B, the same test on a box placed at a
position) report *not culled* for 0 and 1. The rolling word at `02B404B0` keeps the last four corners' outcodes; nothing
read here consumes it.

*Left open at first, settled the same day:* the same matrix `02AEDDF0` serves an outcode test against `|w|`, which wants
a projection, and a distance taken from the product's translation, which looks like a view matrix's job. The block's
only builder is the camera update `003820C0` (2,125 B, one caller; ~~**not read whole** - only its calls and the~~ *(answered: see how-a-camera-reaches-the-renderer.md section 4, read instruction by instruction 2026-09-19; 2026-10-02, OPUS)* - here only its calls and the
addresses it hands them). It builds a matrix into `02AEDDF0` from the working camera's parameters (`003CBB30` on
`02AED560`, called just after a field-of-view tangent is stored there - a projection by its inputs; its body was not
read), copies the working camera's view matrix from `02AED580` to `02AEDE70` and ~~adjusts eight of its elements~~, only when the device override predicate `00181DD0` is true, replaces eight of its elements *(corrected 2026-10-02, OPUS: `003820C0`+0x5BF `call 00181DD0`, +0x5CE `je` past the eight stores)*, and
then **replaces `02AEDDF0` with the product of that view matrix and the projection**; `02AEDDB0` is the same view matrix
times `02AEDD30`, itself a product that includes the projection. So **`02AEDDF0` is a world-to-clip matrix**, the outcode
test is the ordinary clip test, and the routine's *distance* is the length of the record's **clip-space** position - its
`x` and `y` carry the projection's scale - with *depth* the clip `z`. The clip distance and fade range are therefore compared
against a projection-scaled length, not a Euclidean distance from the camera; off the view axis the two differ. What the
extra factor in `02AEDD30` is, and the camera update itself, are on
[how a camera reaches the renderer](../Scripted-Camera/how-a-camera-reaches-the-renderer.md).

## 4d. A root record's frame, and what the selectors `0x0D` and `0x0E` are for

`CharacterRenderRecord_UpdateRootLODAndPresentationState` (`0042D050`, 1,776 B) is section 4a's counterpart for a
record with **no parent** (`+6` = -1; the other two entry conditions are the same). It was read whole. It clears bit 11
of `+0x284`, selects the level of detail, computes the projected origin (section 4b) and the view-dependent factors -
which return a scalar kept for step 3 - and then:

*Identified 2026-09-19, from prior art I had written myself and not searched for:* the side object of step 2 below,
behind the handle `+0x114`, is **the character's shadow** - the shadow-object pool at `02B40528`, 160 entries of `0xE0`
bytes ([the authored-command ramp channels](../CONTRACT-authored-command-ramp-channels.md), `UQ-191`, which also reads
the shadow draw: entry `+0x2C` is a factor of the shadow's gain and `+0x44` of its quad scale). So step 2 makes the
shadow fade with the character and scale with it.

*Where these instance fields go (added 2026-09-19):* the model instance's draw setup multiplies the character's ambient
light term by them - colour by `+0xA0`, the fourth component by `+0xAC` x `+0xB0` / 4096 -
[how a character is lit](../Character-Rendering/how-a-character-is-lit.md) section 5c.

1. **The fade, as in 4a but without a parent.** Instance `+0x90` := the record's colour `+0x210`; the six-channel
   composite into `+0x4B4`; the `rgbatrans` vector; instance `+0xA0` := `+0x220` x that vector; **`+0x49C` :=
   composite scalar x the vector's alpha**; instance `+0xB0` := the Q12 word; the opacity to the effect object; the
   sort key to instance `+4`.
2. **Two handle-addressed side objects get a scalar.** The handle at `+0x114` indexes a table of `0xE0`-byte entries
   behind the pointer `02B40528` by its low byte, the entry's `+0x10` holding the full handle as a check:
   `003B6BB0` (28 B) stores the entry's `+0x2C` and `003B6BD0` (28 B) its `+0x44`. The first receives *composite
   scalar with the view factor as multiplier x alpha* - or the record's `+0x274` instead when bit 2 of `+0xC0` is up -
   the second a value from the record times `+0x278`. The handle at `+0x118` indexes the 32-entry `0x70`-stride table at
   `02B3F570` the same way: `003AFD50` (37 B) stores the same scalar at `+8`, and `003AFD80` (73 B) is given a vector
   built from the record's scale `+0x160`, its second scale `+0x260`..`+0x268` and `+0x278`, of which it keeps the
   middle component at `+0x10` and its reciprocal at `+0x14`, only when that component has changed.
3. **A scaled character is flagged on its resource.** If any of the six scale components (`+0x160`..`+0x168`,
   `+0x260`..`+0x268`) lies outside `[0.99, 1.01]`, bit 0 of the resource entry's byte `+0xA6` is set; otherwise that
   byte is cleared except for its bit 1.
4. The opacity goes to the four auxiliary handles - *read 2026-09-19 (FABLE): `003E70F0` (76 B) walks the four
   dwords at `+0x438`..`+0x444`, skips `0xFFFF`, and `0051CDC0` (27 B) stores the float at `+8` of the handle's entry
   in the `0x3C0`-stride pool `02CA8420`, after checking the entry's own handle at `+0`. An entry is created with
   `+8` = 1.0. **The four objects come from the model's FCP section 4**: `003E6770` (276 B, read whole) builds one
   per `0x50`-byte descriptor there, at most four, when the record is enabled, and switches them off when it is
   disabled - 202 of the 216 blocks that have a section 4 are weapons. It is the pool whose byte `+5`
   [the time-stop page](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)
   reaches through set 3; what its entries are, and what reads the float, was not established - **established the
   same day: they are [bone trails](the-bone-trails.md), and the float is multiplied into the trail's alpha by its
   draw*** - ; instance `+0x50` gets the record's matrix `+0x1C0` (bit 13 of
   `+0x284`) or the shared world-to-clip matrix; the phase entry is published; the record binds its own model-instance
   reference state and publishes its blend state. Instance `+8` bit 1 is set when bit 2 of the system tail's flag byte
   `+0x48818` and bit 23 of `+0x284` are both up, and cleared otherwise.
5. **The two alphas.** When the instance's handle at `+0x240` is not -1, the evaluator is asked twice, on the record the
   instance points back to at `+0xF8`: selector **`0x0D`** and selector **`0x0E`**. Each result, as a fraction of 4096,
   is multiplied by the instance's `+0xAC`, clamped to the 0..255 range and packed into a colour word, and both words go
   to `003B30D0` (139 B). That function finds an object in a 64-entry handle table at `02EBD480` (stride `0x38`, low six
   bits of the handle, full handle checked) and stores the `0x0E` word at the object's `+0x334` and the `0x0D` word at
   `+0x398`, **forcing the three colour bytes of each to `0x80`** - so only the alpha of each survives - and raising bit 3
   of the object's `+0x368`. If bit 3 of the object's `+0x36A` is up both alphas are forced to `0x80` too and the dirty
   bit is dropped again.

So this is what the two products were built for: **one side object of a character carries two alphas, one that fades
with distance and with the camera entering the body (`0x0E`), and one that does not (`0x0D`)**. *Corrected the same day, from prior art I had not searched:* the table at `02EBD480` is the **render-object handle
table** that [the battle runtime mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md)
already describes - entry `+0` the handle, `+0x10` the render object - and the record's own `+0x288` is a handle into
it. So the two alphas are fields of **the character's own render object**, `+0x334` and `+0x398`; my first guess here,
something left on the ground, was wrong and had no evidence behind it. ~~What distinguishes the two fields inside the render
object - which draws use which - was not read.~~ **Read 2026-09-19:** the object is a *class-3 effect container* - the
effects that belong to the character - and the two alphas are spent by the distance-fade node `002F1F40` when one of its
elements is drawn: an element of kind `0x40` is multiplied by `+0x398`, every other kind by `+0x334`
([how a position becomes a single number, section 12](../Position-To-Scalar/how-a-position-becomes-a-single-number.md)).
So a character's effects fade with the character, except the kind that is exempt from distance altogether.

## 5. Behaviour a reimplementation must keep

1. **Ten channels, multiplied, never overwritten by one another.** Each system owns its channel.
2. **A new ramp starts from the current value**, not from the previous target.
3. **Frame counts are scaled by the frame-rate multiplier**; a count below 1 is 1.
4. **Channel 1's ramp starts a frame later than the others'** (its progress restarts at 0).
5. **A child's composite is multiplied by its parent's.**
6. ~~Channels 2, 3 and 5 exist, are part of the products, and are always `1.0`.~~ Channel 3 is; channel 5 is the
   Invisible status and channel 2 an actor-service fade (*corrected 2026-09-19*).

## 6. What is not known

- What ~~channels 2, 3 and 5 were for. No body writes them; nothing in this executable can say.~~ channel 3 is for: no body writes it *(corrected 2026-10-02, OPUS: section 3's 2026-09-19 correction - channels 2 and 5 are written, through the forwarder `00428940`)*.
- What the owner states behind channel 1 are in the player's vocabulary (`+0x284` bit 27, the value `0x35` in
  `+0xCC`, bits 0-1 of `+0x40B`), and which kinds `0x11`..`0x15` and `0x1C` and above are.
- What `+0x22C` and `+0x2EC` are beyond being 0..255-scaled factors of the final scalar.
- ~~The root record's counterpart of section 4a.~~ *Read; section 4d.* What the two handle tables of 4d and the object
  in the table at `02EBD480` are *(answered: see section 4d - the render-object handle table; 2026-10-02, OPUS)*; what the effect object ~~and the four auxiliary handles~~ is *(answered: see section 4d - the four auxiliary handles are bone trails; 2026-10-02, OPUS)*; what bit 14 of `+0x284`
  and the word `+0x2CA` mean in the climb of step 2.
- What the three large bodies that read channel 4 alone do with it.
- ~~That the point channel 4 measures against is the camera.~~ *Settled 2026-09-19 in section 4b: it is the
  translation row of the camera's view-to-world matrix at `02AEDEF0`.* ~~What fills that matrix was not traced.~~ *(answered: see how-a-camera-reaches-the-renderer.md - the camera update `003820C0` copies the capped-field-of-view copy's matrix into it; 2026-10-02, OPUS)*
- What attachment slots `0x10A` and `0x7FFF` are in the game's vocabulary, and what `0042F4C0`, `004215A0` and
  `00426E40` do beyond the roles their arguments show in section 3a.
- ~~What the global `01F82E38` is~~ *(answered: see an-effect-element-frame-by-frame.md - the half-rate flag; `001EDDC0`, the frame-rate switch, stores 2.0 to `01DFE0B8` (+0x18), 0.5 to `01DFE0BC` (+0x20) and 1 to `01F82E38` (+0x28) on its non-zero arm; the image holds 1.0, 1.0 and 0; 2026-10-02, OPUS)*, whose non-zero value gives a new ramp a head start of one step.
- Nothing here was observed running; the page is static evidence throughout.

## 7. Evidence

| claim | source | tier |
|---|---|---|
| the channel layout and formula | `003E5D60`, `003E5D00`, `003E4370`, `003E48E0` disassembled whole | 1 |
| ten channels, not seven | the stepper's loop count `0xA`; `ResetDefaults` loops to `0xA` | 1 |
| who writes which channel | members census, 22 sites, counts equal to a raw call sweep *(scope named 2026-10-02, OPUS: direct `call` / `jmp` sites only; the conditional-jump forwarders `00428940` (six callers) and `004293C0` (one) add channels 2 and 5 - section 3's 2026-09-19 correction)* | 1 |
| ~~channels 2, 3, 5 have no writer~~ channel 3 has no writer *(corrected 2026-10-02, OPUS: 2 and 5 are written through the conditional-jump forwarder `00428940`, section 3)* | displacement sweep `+0x4C0`..`+0x4F8` over the band: nine functions, all read here; the two index-taking writers are called with constant channels 0, 1, 4, 6, 7, 8, 9 and the reset loop | 1 |
| the verb names | `scriptvm-verb-table.tsv` rows `03B2`, `0535` | 1 |

*Limit of the no-writer claim:* the sweep covers displacement-addressed accesses inside `003E0000`..`00430000`;
a store through a pointer computed elsewhere would not be seen.

## 7a. Where each behaviour is in the bytes

The statements above were read at these instructions; each address is an instruction boundary inside the body named.

| body | what is there | at |
|---|---|---|
| `003E5D60` ramp starter (182 B) | target scaled by -4096 | `003E5D6A` |
| | collapse: `base += (delta * progress) >> 12` | `003E5DAE` |
| | `delta` stored | `003E5DCC` |
| | `0x1000 / frames` (`idiv`), `step` stored | `003E5DD5`, `003E5DD8` |
| | the channel-1 exception (`cmp r11d, 1`), `progress` stored | `003E5DE1`, `003E5DE9` |
| | getter call and the second `step` | `003E5DF2`, `003E5E03` |
| `003E48E0` evaluator (604 B) | the three selector tests | `003E48E5`, `003E48EE`, `003E48F7` |
| | one channel: indexed loads and the formula | `003E48FF`..`003E4920` |
| | selector `0x0E`, six factors | `003E4923`..`003E4A04` |
| | selector `0x0D`, rebased to channel 1 (`add r9, 0x4C8`), channels 1, 2, 3, 5 | `003E4A08`..`003E4A7F` |
| | selector `0x0B`, five factors | `003E4A83`..`003E4B38` |
| `003E4240` composite (269 B) | six-channel product | `003E4240`..`003E4325` |
| | no parent: store to `+0x4B4` | `003E432D` |
| | parent: multiply by the parent's `+0x4B4`, store | `003E4336`, `003E4344` |
| `003E51F0` vector builder (701 B) | `1/4096` loaded, loop variable set to 6 | `003E51FF`, `003E5216` |
| | the three never-taken product branches | `003E5227`, `003E5231`, `003E523B` |
| | divide and store `out[i]`, loop to 4 | `003E5487`, `003E548B`, `003E5493` |
| `00428C40` four-ramp starter (131 B) | frames truncated from the sixth argument | `00428C4A` |
| | channels 6, 7, 8 by call, 9 by tail jump | `00428C6E`, `00428C81`, `00428C94`, `00428CBE` |
| `0042E1F0` piece visibility (269 B) | own kind `>= 0x1C`, owner kind in `0x11`..`0x15` | `0042E222`, `0042E250` |
| | owner's bit 27 of `+0x284`, and `+0xCC` low twelve bits against `0x35` | `0042E26B`, `0042E286` |
| | set `0.0` at once / set `1.0` at once | `0042E297` (from `0042E28C` / from `0042E2DC`) |
| | `+0x40B` bits 0-1 test, ramp to `0.0` over 5 frames | `0042E2B8`, `0042E2D7` |
| `0042F880` pending-attachment handler (608 B) | owner from `+0x3CE`, liveness test | `0042F889`, `0042F8B9` |
| | both resource entries must resolve, else leave pending | `0042F8F4`, `0042F923`, `0042F932`, `0042F93B` |
| | slot `0x10A`, own kind, linked owner kind, the `+0x40B` test | `0042F95B`, `0042F96C`, `0042F98F`, `0042F997` |
| | detach from a different parent; parent bookkeeping | `0042FA01`, `0042FA0D`, `0042FA17` |
| | attach; channel 1 to `0.0` when the test passed | `0042FA29`, `0042FA2E`, `0042FA3E` |
| | slot `0x7FFF`: model-instance word and the owner's entry list | `0042FA48`, `0042FA64`, `0042FA92` |
| | commit and clear dirty bit 19 | `0042FAAE`, `0042FAB8`, `0042FABE`, `0042FAC8` |
| `0042D050` root record's frame (1,776 B) | entry conditions; bit 11; level of detail, origin, view factors | `0042D078`, `0042D080`, `0042D08D`, `0042D09C`, `0042D0B5`, `0042D0BD`, `0042D0C5` |
| | colours, composite, opacity, Q12 word, sort key | `0042D0EC`, `0042D0F3`, `0042D103`, `0042D136`, `0042D15A`, `0042D162`, `0042D18B` |
| | the `+0x114` handle's two scalars; the `+0x118` handle's scalar and vector | `0042D1A4`, `0042D1BA`, `0042D1D8`, `0042D1FF`, `0042D268` |
| | the six scale tests; resource byte `+0xA6` | `0042D26D`..`0042D2E9`, `0042D31C`, `0042D325` |
| | auxiliary handles; matrix; phase entry; instance `+8` bit 1 | `0042D337`, `0042D362`, `0042D375`, `0042D3A2`, `0042D3C3`, `0042D3C9` |
| | selector `0x0D`, scale by `+0xAC`, clamp and pack | `0042D3CD`, `0042D3E6`, `0042D40D`, `0042D4A6`..`0042D500`, `0042D54B` |
| | selector `0x0E`, the same; both words to the handle table | `0042D580`, `0042D59F`, `0042D6DD`, `0042D716` |
| `003B30D0` two alphas into a handle object (139 B) | handle check; the two stores; colour bytes forced; the override | `003B30E3`, `003B310C`, `003B3112`, `003B3125`, `003B312B`, `003B313B` |
| `0042CBF0` attached record's frame (884 B) | the three entry conditions; parent lookup; orphaning | `0042CC05`, `0042CC15`, `0042CC22`, `0042CC53`, `0042CC70` |
| | borrowed view data, sort depth + 2.0, the climb, own factors or the ancestor's block | `0042CC9E`, `0042CCB8`, `0042CCD0`, `0042CD14`, `0042CD41` |
| | composite, colour vector, opacity into `+0x49C` | `0042CD6A`, `0042CD77`, `0042CD7F`, `0042CD8A` |
| | bit 26 and the parent's colours; instance `+0x90`, `+0xA0`, `+0xB0` | `0042CD97`, `0042CDC6`, `0042CDCD`, `0042CDE9`, `0042CDFC`, `0042CE0B` |
| | sort key saturation, global, instance `+4`; matrix choice | `0042CE45`, `0042CE77`, `0042CE7D`, `0042CE8C`, `0042CEAA` |
| | phase entry; opacity x parent's to the four handles; render-object entry flag; blend state copied down | `0042CEBD`, `0042CEE4`, `0042CEF6`, `0042CF20`, `0042CF34`, `0042CF47` |
| `0042E850` first half | cull bits cleared; unit box; focus frame; extents and radius | `0042E8AA`, `0042E8B6`, `0042E8D5`, `0042E8DF`, `0042E903` |
| | config exemption; box test; frame x `02AEDDF0` | `0042E918`, `0042E92E`, `0042E94F` |
| | reference record; distance from it, or from the product's translation | `0042E954`, `0042E98A`, `0042E9F8`, `0042EA3A` |
| | the three cull bits | `0042EA65`, `0042EAAA`, `0042EAE7` |
| `0046C180` box test (91 B) | product, install, classify, `<= 1` | `0046C1A7`, `0046C1B1`, `0046C1B9`, `0046C1C0` |
| `003B3F10` frustum classifier (416 B) | corner selectors; transform | `003B3F73`, `003B3FBF`, `003B3FD5` |
| | the six outcode tests; rolling word; any / every | `003B3FF2`..`003B4030`, `003B4042`, `003B404F`, `003B4055`, `003B4064`..`003B4078` |
| `0041EC00` projected origin (480 B) | world x view-projection; origin through it; the perspective divide | `0041EC53`, `0041EC63`, `0041EC88`..`0041ECA8` |
| | camera position loaded; vector to the record; its length | `0041ECB0`, `0041ECC4`, `0041ED28` |
| | view-axis point through the camera matrix, then world-to-clip | `0041ED39`, `0041ED57`, `0041ED6D` |
| | reference `w` chosen and stored | `0041ED80`, `0041ED8F`, `0041ED9C` |
| `0042E850` distance fade and cull (1,238 B) | cull bits test | `0042EB05` |
| | band test, `sin`, channel 0 ramp over 1 frame | `0042EB43`, `0042EB54`, `0042EB6C` |
| | ~~viewer block~~ system-tail flag bit 4 *(corrected 2026-10-02, OPUS: `0042E850`+0x329 `test byte ptr [rsi + 0x48818], 0x10`, `rsi` the record array base - the tail's camera-inside fade bit, section 4c)*, horizontal distance, `0.15 + [+0x2A8]` | `0042EB79`, `0042EBB1`, `0042EBCB` |
| | channel 4 to `0.0` / to `1.0` over 3 frames, bit 5 of `+0x4B7` | `0042EC4D`, `0042EC78`, `0042EC52`, `0042EC7D` |
| | culled: channels 0 and 4 to `0.0` over 1 frame | `0042ECC3`, `0042ECD8` |

## 8. Related

- [The character render record array](the-character-render-record-array.md) - the record these bytes live in.

## Cross-subsystem neighbours

**Script VM - SERVICE.** The two verbs reach this page's `00428C40` through actor-service forwarders; the verb
handlers themselves belong to the script bridge and are named here only by verb and call id. The crossing is
one-way: scripts start colour ramps, and nothing on this page calls back into the script layer.

**Core runtime scheduling - SERVICE.** The ramp starter `003E5D60` calls the getter `001EDE70`, which returns the
global dword `01F82E38` and does nothing else. A one-way read of one value.

**Input - INCIDENTAL.** The same getter `001EDE70` is also called by the input arbiter `00253C70`. The two share a
reader of one global and nothing else; the edge is here only because this page names the getter.

**Resource - SERVICE.** `0042F880` (section 3a) will not attach a piece until both records' resource entries resolve, and it resolves them through
`ResourceTable_ResolveEntryByIndex` (`002ED570`) and `ResourceTable_ResolveEntryBySignedIndex16` (`004780B0`). Those
lookups gate the attachment; they are not part of the fade arithmetic.

**Movement - INCIDENTAL.** The detach helper `004288B0` of section 3a is also called by the binding update `002E3110`,
a Movement-owned body. The two callers share the helper and nothing else; the edge is recorded because the helper is
named here.

**Gameplay - MECHANICAL (SWE2-EC7-59, 1 edge).** `00203170` — a shared helper this page's `0046C0D0` section cites —
is also called by `00339630` on the Gameplay layer. Shared-helper fan-in; no gameplay relationship to the fade.

**Audio - MECHANICAL (SWE2-EC7-84, 2 edges).** `00421E20` — the stack-table probe this page's `004201F0`
section cites — is also called by Audio bodies `00332C40` and `003B99D0`. Shared-helper fan-in; no audio
relationship to the fade.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**UI - MECHANICAL (24 edges).** Sixteen UI bodies call `00202C90`, the 7-byte copy of one 16-byte vector that the `+0x2E0` hand-off tails into (among them `002915C0`, `002C7660`, `003F26F0`, `003F9720` and `005528C0`, and 11 more); seven call `00203170`, the 44-byte store of a 4x4 identity matrix (`00247AE0`, `002D2600`, `002D28E0`, `00368010`, `003C5500`, `003F26F0` and `003F2A70`); and `00247AE0` also calls `00229DA0`, the 51-byte mode-to-factor lookup that answers 1.1547, 1.3333 or 1.0966 for modes 2, 3 and 4 and 1.0 otherwise. All three are general vector and constant helpers the fade code shares with menu drawing; the UI's use of them has nothing to do with the ten fade channels.

## SWE2-EC7-59 update (2026-09-19) - `0046C0D0`

`0046C0D0` (162 B) is the `0046C180` sibling box test the fades page names - `00202D70`/`00203170`/`003B3F10`/`003B4140`/`00808C40` plus `01F44830`/`02AEDDF0`. Interior anchor `0046C0FA` (a `00203170` call).

## SWE2-EC7-61 update (2026-09-19) - `003E4DD0`

`003E4DD0` (154 B) is a call-free mode-dispatched 4-factor product - `edx` 1 -> `[+0x264]*[+0x164]*[+0x26C]*[r8+0x118]`; 2 -> `[+0x268]*[+0x168]*[+0x26C]*[r8+0x11C]`; else 0 (a fade-channel weight). Interior anchor `003E4DFB` (the `+0x268` mode-2 load).


## SWE2-EC7-73 update (2026-09-19) - `003E6D40` + `003E5D00` + `003E57D0` + `003E5770` channel helpers measured

`003E6D40` (57 B) is the gated accumulation: `dword[+0x300] > 0` runs
`0020E600([+0x2FC])` -> `003AB7F0` and adds `[+0x300]` to its result;
else 0 - the channel count plus resolved-context sum.
Interior anchor `003E6D58` (the `0020E600` resolve).

`003E5D00` (44 B) is the scaled channel init: `xmm2 * float[00915258]`,
`cvttss2si`, the word lands at `[rcx + idx*8 + 0x4C0]` with the
`[+0x4C2]` dword zeroed and ~~the word echoed at `[+0x4C6]`~~ the word at `[+0x4C6]` zeroed too *(corrected 2026-10-02, OPUS: `003E5D00`+0x18 `xor eax, eax` comes before `003E5D00`+0x22 `mov word ptr [rcx + r8*8 + 0x4c6], ax`)* - an 8-byte
stride element restamp.
Interior anchor `003E5D0F` (the `+0x4C0` word store).

`003E57D0` (54 B) is the `+0x18`-gated forwarder: `ebx = [+0x18]` -1
returns 0; otherwise `0020E600([+0x10])` -> `[rax+0xD98]` and tails
`002ED570(rcx, ebx)`.
Interior anchor `003E57E1` (the `0020E600` resolve).

`003E5770` (25 B) is the triple-product helper: `[+0x260] * [+0x160] *
[+0x26c]` returned in `xmm0` - the channel scale triple the fade math
shares.
Interior anchor `003E5778` (the first `mulss`).

## SWE2-EC7-81 update (2026-09-20) - `00521400` vec4 element-multiply measured

`00521400` (62 B) is the component-wise multiply the fade callers
share: `[rcx+i] = [rdx+i] * [r8+i]` for `i` in 0, 4, 8, 0xC - a
four-float scale with no other work.
Interior anchor `00521404` (the first `mulss`).

## SWE2-EC7-83 update (2026-09-20) - `0042E7F0` record-link measured

`0042E7F0` (83 B) is the fade-record link the channel callers run:
`003E55B0(rcx)` resolves the record and a live one takes `+0xF8` =
`rdx`, `word[rdx]` at `+0xE0`, `+0xE8` = `rdx+0x180`, and
`004221F0(rdx)`'s result at `+0xF0` - four fields from one argument.
Interior anchor `0042E82C` (the `004221F0` call).

## SWE2-EC7-84 update (2026-09-20) - the `0042CBF0`/`0042D050` callee row measured

`00421CD0` (75 B) is the first-valid-word getter the fade callers
run: `003E55F0()` yields the record, `byte[rax] >= 3` gates, and
the first non-`0xFFFF` of `word[+0x3A]`/`+0x3C`/`+0x3E` returns - 0
when all three are -1.
Interior anchor `00421CD8` (the `003E55F0` call).

`004210D0` (72 B) is the `word[+6]`-chain verifier the same callers
run: `+0x284` bit `0x10` gates, then each linked record at the 0x740
stride must keep the same bit (a zeroed `+0x284` folds the pointer
to 0 and the test fails) - 1 only when the chain ends at -1.
Interior anchor `004210F1` (the `imul` chain step).

`00420FB0` (81 B) is the stricter sibling: `+0x284` bit 3 plus
`(flags & 0x30) == 0x30` gate the same `word[+6]` walk, continuing
while ~~bit 3 persists~~ bit 3 and `(flags & 0x30) == 0x30` both hold on each linked record *(corrected 2026-10-02, OPUS: `00420FB0`+0x46 `jne` returns to the mask test at `00420FB0`+0x14)* - 1 at chain end, else 0.
Interior anchor `00420FC4` (the `& 0x30` mask test).

`004209C0` (38 B) is the `+0x2E0`-block hand-off: `003E55B0()` yields
the shared record and `00202C90(rax+0xD0, rcx+0x2E0)` copies the
caller's block into it.
Interior anchor `004209E1` (the `00202C90` tail).

`004201F0` (648 B) is the `0x524F4640`-tagged progress evaluator the
fade callers run: `0020E600([rcx+0x10])` -> `[rax+0xDA0]` ->
`004780B0(word[rcx+0x64])` yields the block; `+0x208` != -1 and
`+0x1F8` != 0 gate the `ROF@` tag check. The `+0x3A` count plus one
scales, `00421E20(0x100)`/`(0x101)` probes fill the stack table
(falling back to `0046D100`/`0046D350`/`0046D0C0`), the
`[rsi+0x208]` threshold counts through the `+0xA0`/`+0xB0` float
list, `(count+1 - hits)/(count+1)` lands at `+0x2A4`,
`word[+0x90]` refreshes `+0x64`, `003E57D0` syncs `0x2000` by
`+0x284` bit `0x100`, and `00421280(1)` tails - stack-cookie framed.
Interior anchor `00420274` (the `0x524F4640` tag compare).

`0041F270` (124 B) is the `+0x4A0` bit-1 field commit the same
callers run: `003E55B0()` yields the record; when `[rbx+0x4A0] & 2`
is set, `+0x244` gains bit 0 and `(rec+0x4A4)*2` merges into its
bits 1-3 while `+0x4A8`/`+0x4AC`/`+0x4B0` copy to
`+0x248`/`+0x24C`/`+0x250` - otherwise bit 0 of `+0x244` clears.
Interior anchor `0041F28A` (the `or +0x244, 1`).

`0041E960` (662 B) is the four-channel ramp writer the fade callers
run: `003E4E70(&stack)` stages the input and `+0x284` bit
`0x20000000` gates the whole pass; on it `003ED0E0(&stack)` plus
three global-byte constants feed the scalar SSE web that writes
`+0x2E0`/`+0x2E4`/`+0x2E8`/`+0x2EC` clamped against `0x437F0000`
(255.0f); off it the block zeroes except `+0x2EC = 255.0f` -
stack-cookie framed, the channel fade's per-element evaluator.
Interior anchor `0041EA2D` (the first `+0x2EC` store).

## SWE2-EC7-86 update (2026-09-20) - `003E70F0` + `003E5790` measured

`003E70F0` (76 B) is the aux-handle scalar publish the fade
callers run: over the four dword handle slots at `[rcx+0x438]`
(+4 stride) every handle not equal to `0xFFFF` receives
`0051CDC0(handle, xmm1)` - one scalar broadcast to the live
aux set.
Interior anchor `003E711D` (the `0051CDC0` publish call).

`003E5790` (25 B) is the triple-product getter the fade and
movement callers run: `float[rcx+0x264] * float[rcx+0x164] *
float[rcx+0x26C]` - three record scales folded into one
coefficient, call-free.
Interior anchor `003E57A0` (the second `mulss`).

## SWE2-EC7-87 update (2026-09-20) - `003E4730` + `003E4370` measured

`003E4730` (66 B) is the fixed-point channel evaluator the fade
callers run: `movsx word[+0x4B4]` is converted to double and
multiplied by `00D117C0` (~~2^-13~~ the double 2^-12, 1/4096) *(corrected 2026-10-02, OPUS: read from the image; `00D117C8` is the double 1/255, so this is the `/4096 ... /255` formula above; the multiplies are `003E4730`+0x25 and `003E4730`+0x35)*, `float[+0x22C]`, `float[+0x2EC]`
and `00D117C8`, then `cvtpd2ps` back to float - one channel
weight, call-free.
Interior anchor `003E4755` (the first `mulsd`).

`003E4370` (88 B) is the ten-channel ramp step the fade's callers
run: over the 8-stride word records at `[rcx+0x4C0]` (10 slots)
each live `word[+6]` step adds into `word[+4]` until it reaches
`0x1000`, where ~~`word[+0]` takes `word[+2]`~~ `word[+2]` is added into `word[+0]` *(corrected 2026-10-02, OPUS: `003E4370`+0x2D `add word ptr [rax], cx`)* and the `+4` counter
resets - the per-channel tick that drives the fade.
Interior anchor `003E43A6` (the accumulate arm).

## SWE2-EC7-89 update (2026-09-20) - `003B33A0` keyed flag merge measured

`003B33A0` (46 B) is the keyed flag write the fade callers run:
`ecx & 0x3F` picks the 0x38-stride slot in `02EBD480`, and when
the slot key matches, `byte[+0x30]` gets bit 2 written from `dl`
and bit 1 armed - a two-bit merge on the slot's flag byte.
Interior anchor `003B33B8` (the merge sequence).

## SWE2-EC7-97 update (2026-09-20) - `002EE050` measured

`002EE050` (120 B) is the compare-then-publish `002E3110` and
`003BA150` call: `cx == -1` early-outs, the `0x740`-stride record
at `[022C6F28]` must be live (`[+0x284] != 0`), and the incoming
`xmm1/2/3` are compared against `[+0x160]/[+0x164]/[+0x168]` -
all three equal returns without touching anything; any
difference writes the triple into `[+0x330]/[+0x334]/[+0x338]`,
stamps `+0x33C = 1.0f`, and tails `00420D50`.
Interior anchor `002EE0A0` (the first `movss` store).

## SWE2-EC7-108 update (2026-09-20) - `00229D60` measured

`00229D60` (58 B) is the sibling
select `003820C0` and `003CBB30`
call, keyed on `byte[02064AD1]`
instead of an argument: values 2,
3, 4 answer the same
`float[00908D50]` (1.1547),
`float[00908D54]` (1.3333),
`float[00908D48]` (1.0972)
constants, else `1.0` - the
global-mode twin of `00229DA0`.
Interior anchor `00229D76` (the
`1.0` default load).

`004215A0` (754 B) is the dirty-bit-19 handler `0042F880` calls: `0020E600` x9 resolves with `002ED570` x2, `004219C0` x2, `003E3CA0`, `003E5AD0`, `0046E640`, `00422380`, `00422D50` x2, `0041CFC0` x2, `00512C80`, `003326C0`, `0041F010`, `003E5CF0`, `003B30A0`, `00422310`, `004218A0` and `003E5D30` - the channel rebuild's widest resolve fan-out.

Interior anchor `004215C9` (function `004215A0`).

`00512C80` (78 B) is the detach helper `004215A0` calls (the record-pool lifecycle pass also reaches it): `byte[rcx+0xC]` is the chain head (-1 = none), the loop walks `02CA81F0` 16-byte records by `+0xE` next-indices clearing `+0xF`'s low nibble on each, then `+0xC` <- 0xFFFF, `+0xE` <- 0 and the `02EBA481` counter decrements - the fade chain's unlink-and-clear, call-free.

Interior anchor `00512CA3` (function `00512C80`).

`00422380` (111 B) is the index-to-word remap `004215A0` calls (the audio layer's descriptor property getter shares it): `ecx` bands - `0x100`/`0x101` -> 0x1D00/0x1D, `0x200` -> 0x65E, `0x201` -> 0x656, `0x1000` -> 3, other `>=0x100` -> 0xFFFF, below that `word[01F00060 + ecx*2]` - the channel-id class resolver, call-free.

Interior anchor `004223D7` (function `00422380`).

`00422310` (107 B) is the index-to-name resolver `004215A0` calls (the same audio getter shares it): `0x100` -> "n_hara", `0x101` -> "model", `0x200` -> "j_blade", `0x201` -> "n_grip", `0x1000` -> "j_kao", other `>=0x100` -> "__naiyo__", below that `qword[01EFFFB0 + ecx*8]` - the attachment-point name table, call-free.

Interior anchor `0042234E` (function `00422310`).

`004218A0` (281 B) is the pair-bind `004215A0` calls (the movement-mode selection path also binds through it): two `+0x10`-indexed resolves through `0020E600` -> `+0xD98` -> `002ED570`, both present -> `word[+0x2F2]` cleared, `+0x284` bit 0x4000000 set when no third arg else `00372760` checks, then `0046E590` links the pair's `+4` fields and the flagged record is re-seeded - the channel-pair link step.

Interior anchor `004218C7` (function `004218A0`).

`0041F010` (602 B) is the table emit `004215A0` calls (the render-record array's apply shares it): `003E5CF0` counts (cap 0x16 into `byte[+0x40C]`), `+0x284` bit 0x8000000 gates, then a 0x16-entry loop with `003E55F0`/`003E5AD0`/`003E5CD0`/`004211B0` and float mul-accumulates into `[rbx+0x158]`, `word[+0x2CA]` copied - the channel table's per-slot fill.

Interior anchor `0041F035` (function `0041F010`).

`003E5D30` (34 B) is the default seeder `004215A0` and `004218A0` call (an ownerless resolve pair calls it too): `qword[+0x4C0]`, `+0x4C8`, `+0x4E0` <- 0x1000 each - the three-field init, call-free.

Interior anchor `003E5D3B` (function `003E5D30`).

`003B30A0` (36 B) is the keyed-slot setter `004215A0` calls (the record-pool lifecycle writes through it too): `ecx & 0x3F` x 0x38 buckets into `02EBD480`, `+0` key match and non-null `+0x10` -> `edx` stored at `[+0x10]+8` - the 64-bucket flag write, call-free.

Interior anchor `003B30B6` (function `003B30A0`).

`0040D890` (610 B) is the channel-rate emit `003DFFE0` calls: `byte[+5]` opens the double `0020E600` id-resolve, `1.0/[rdi+0x10]` and `movsxd [rdi+0x1C]` publish into `022D9198`/`022D9390`/`022D8FB0`/`022D9350`/`022D9394`, zero/compare run `0036DDA0`/`0036DD90`, then the `esi`-counted loop `0040DBB0`/`0040FF30`/`00411650`/`00413C80` - the fade record's step write.

Interior anchor `0040D8AF` (function `0040D890`).

`00421280` (351 B) is the channel setter `004201F0`/`00420E70` call: `003E55B0` yields the record; `edx` set with `[rdi + 0x284] & 0xC0 == 0xC0` sets bit 0 of `[rax + 8]` else clears it; `[rdi + 0x114]` live, `[rdi + 0xC0] & 0x18` clear, `edx` set, bit 0 set, `[rdi + 0x284] & 0x1000` picks `003B6900(4|6)`, then `003AFD00`/`003E6D40`/`0051C380`/`0051D2F0` - the fade-channel flag write.

Interior anchor `00421294` (function `00421280`).

`003E4B50` (350 B) is the tint multiply `0042E850` calls: `004234B0` resolves the source (or `[rdi + 0x400]`'s `word[+2] + edx + 0x114` fallback), then `[+0x260..268]` x `[+0x160..168]` x `[+0x26C]` writes the scaled triple to `rsi` - the fade channel's intensity application.

Interior anchor `003E4B67` (function `003E4B50`).

`00370FA0` (309 B) is the mode-gated pose apply `00421E20` calls: `dword[rcx+0x9C]==2` runs `003737C0` else returns `-1`; a `-1` result exits 0, else `0020E600` decodes `dword[rbx+0x84]` and `003725A0(word ax)` gates the write; `esi-1` then picks the arm - both sides staging the `(0,0,0,1.0)` quat constants (`0090xxxx`/`01CEBBA8`) into the stack record before their tails - the stack-table probe's pose publish on the render record.

Interior anchor `00370FF6` (function `00370FA0`).

`003737C0` (160 B) is the tag-index search `00370FA0`/`00372800`/`00373160` call on `dword[rcx+0xA0]`'s handle table: two `0020E600` decodes fetch the table (null exits `0xFFFF`), then `dword[+0xC]` entries iterate - each slot resolves through `00409270` + `00409250` and the first entry whose `word` tag equals `edx` with `dword[+4] & 0x100` ~~clear~~ **set** returns its index *(corrected 2026-10-01, OPUS: `003737C0` takes the record when bit 8 is set - the authored-commands page's GI-15 section)*, else `0xFFFF` - the pose publish's record lookup.

Interior anchor `00373815` (function `003737C0`).

`00370E30` (292 B) is the sibling pose apply `00421E20` calls: `00372760` resolves the target id (a `-1` exits 0), `0020E600` decodes `dword[rbx+0x84]` into `r14` and `003725A0(word si)` gates the write; `edi-1` picks the arm - arm 2 consults `dword[rbx+0x9C]==2` before the `(0,0,0,1.0)` constant block at `rsp+0x20` adjusts through `00373640`, then `rbp = si*0x290 + r14 + 0x80` and `0046D0D0(r15, rbp, rsp+0x20)` commit the record - `00370FA0`'s mode-1/2 counterpart on the same render record.

Interior anchor `00370F2C` (function `00370E30`).

`00409250` (22 B) is the slot-field reader `003737C0`'s per-entry loop runs beside `00409270`: `dword[rcx+4] & 0x40000000` set returns `word[+8]` (the tag half), clear returns `dword[0] & 0xFFF` (the index half) - the two-lane decode the tag search applies to every `0x4C`-stride candidate.

Interior anchor `00409259` (function `00409250`).

`00372760` (157 B) is the name-index lookup `00370180`/`00370E30`/`004218A0` call: `dword[rcx+0xA0]` decodes through `0020E600` (null exits `0xFFFF`), a second `0020E600` on the same field gives the table whose `dword[+0xC]` counts `0x4C`-stride entries at `+0x30`; each entry's head is inline-strcmp'd byte-wise against `rdx`'s string (difference or NUL ends the compare) and the first equal entry returns its index in `di`, else `0xFFFF` - the render record's name-to-channel resolver.

Interior anchor `0037278E` (function `00372760`).

`003725A0` (109 B) is the word-membership scan `00370E30`/`00370FA0`/`00370180`/`00373160` consult: `dword[rcx+0x84]` decodes through `0020E600`, `sword[rbx+0x88] x 0x290` selects the row, and `sword[rbx+0x8A]` counts the u16 entries linearly compared against `dx` - 1 on a hit, 0 on exhaustion; the row-gated id test that decides whether the pose write may proceed.

Interior anchor `003725B6` (function `003725A0`).

`00409250` (22 B) is the slot-field reader `003737C0`'s per-entry loop runs beside `00409270`: `dword[rcx+4] & 0x40000000` set returns `word[+8]` (the tag half), clear returns `dword[0] & 0xFFF` (the index half) - the two-lane decode the tag search applies to every `0x4C`-stride candidate.

Interior anchor `00409259` (function `00409250`).

`00372760` (157 B) is the name-index lookup `00370180`/`00370E30`/`004218A0` call: `dword[rcx+0xA0]` decodes through `0020E600` (null exits `0xFFFF`), a second `0020E600` on the same field gives the table whose `dword[+0xC]` counts `0x4C`-stride entries at `+0x30`; each entry's head is inline-strcmp'd byte-wise against `rdx`'s string (difference or NUL ends the compare) and the first equal entry returns its index in `di`, else `0xFFFF` - the render record's name-to-channel resolver.

Interior anchor `0037278E` (function `00372760`).

`003725A0` (109 B) is the word-membership scan `00370E30`/`00370FA0`/`00370180`/`00373160` consult: `dword[rcx+0x84]` decodes through `0020E600`, `sword[rbx+0x88] x 0x290` selects the row, and `sword[rbx+0x8A]` counts the u16 entries linearly compared against `dx` - 1 on a hit, 0 on exhaustion; the row-gated id test that decides whether the pose write may proceed.

Interior anchor `003725B6` (function `003725A0`).

`003E4CB0` (280 B) is the keyed emit `0042E850` runs on the `[rcx+0x400]` asset record: `byte[record] >= 3` gates the read and the first non-`0xFFFF` of `word[+0x3A]`/`+0x3C`/`+0x3E` supplies the id (all three `-1` bails); `[rdi+0x18]` indexes through `0020E600([rdi+0x10])` into the `[+0xD98]` table for `002ED570`, and a resolved object runs `003710E0(obj, id, 0, &out)` with `1.0f` staged on the stack - the `0046D110`/`00421E20(0x100)`/`0x101` fallback serves handle-less records, the same ladder `004221F0` keeps.

Interior anchor `003E4D3C` (function `003E4CB0`).

`004221F0` (273 B) is the keyed emit `0042E7F0`'s link runs beside `003E4CB0`: `003E55F0` supplies the record, `dword[rbx+0x18]` must stay a live index through `0020E600([rbx+0x10])` into the `[+0xD98]` table for `002ED570`, and a `byte[record] >= 3` with `word[+0x3A] != 0xFFFF` fires `003710E0(obj, id, 0, &out)` under a `1.0f` stage; anything else falls to `00421E20(rbx, 0x100, 0, &out)` retried as `0x101` - the resolve-or-default sequence the fade channels share.

Interior anchor `004222A2` (function `004221F0`).

`004211B0` (198 B) is the two-reference record linker `0041EDE0` mode 1 and `0041F010` emit: each of `[rdx+0x18]` and `[rcx+0x18]` is a `-1`-guarded word index resolved via `0020E600` -> `[rax+0xD98]` -> `002ED570`; when both resolve and the first record's flag byte has bit `0x80` set it calls `0046E640` with `[rdi+4]`, `[rbx+4]` and the caller's mode `r15d`, then copies `[r14]` into `[rbp+6]` - the keyed cross-row write the emit arms share

Interior anchor `00421200` (function `004211B0`).

`003E5CD0` (32 B) is the record-slot reader the same two emitters call: it loads `rdx = [rcx+0x400]` and returns 0 when the pointer is null or its `+6` word is zero, else `rdx + [rdx+6]` - a self-relative sub-record pointer, null-safe in both directions

Interior anchor `003E5CDF` (function `003E5CD0`).

`003E3CA0` (196 B) is the paired field-resolve `004215A0` runs on a fade record: word `+0x68` (and, when not `-1`, word `+0x6C`) selects a `0x740`-stride row in the `022C6F28` table gated on `[row+0x284]`; each accepted row is `0020E620`-resolved into `+0x70`/`+0x74` and `0020E600` -> `00421D20` -> `0020E620` into `+0x78`/`+0x7C` - four computed dwords per call

Interior anchor `003E3CE2` (function `003E3CA0`).

`0046E590` (161 B) is the paired resolve-and-commit `004218A0` runs: `edx`/`ebp` ids each pass `002ED570` on `rsi` (`-1` leaves null), and when both records exist `00370180(rbx, rdi, r14d)` runs, `[rbx+8]` resolves the same way and `0020E620` writes its answer at `[rbx+0xC]` before the `0046E6F0` tail

Interior anchor `0046E5EB` (function `0046E590`).

`00370180` (519 B) is the paired-record channel copy `0046E590` runs: it resolves `[r14+0xA0]` and both `+0x84` ids through `0020E600`, copies `[r15+4]` to `[r14+8]` (and `[r14+4]` to `[r15+0x10]` when `r8d == -1`, else stamps `r13w` at `[r14+0x14]`), then walks `[r14+0x8A]`-count `0x290`-stride rows - each row's `[rbx+0x27E]`-selected `0x4C` sub-record with kind word `1`/`7` at `[+0x22]` gets `00372760`-queried and `003725A0`-applied

Interior anchor `00370199` (function `00370180`).

`003E6910` (142 B) is the `+0x448`/`+0x44C` counter service this page's `0042C410` update calls: the two phase slots are read, `003D8DE0` dispatches on the record's element state, and actor/application state is resolved through `0020E600`/`0051B9E0`/`003D8D70` before the slot pair is advanced - the per-record phase step the render-record update runs beside `003E70F0`'s `+0x438` quad feed.

Interior anchor `003E695A` (function `003E6910`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Section 7a's sizes, section 2's channel arithmetic and section 3's writers became checks at their
instructions. Script: `Tools/analysis-kit/gfz-scripts/falsify_fade_channels.py`, output `falsify_fade_channels.out`,
image `73461d08…`, 0 BROKEN, exit 0. The call-site census (`fade_channel_census.py`) and sections 4a to 4d's frame
bodies beyond their sizes are carried.

| # | Clause attacked | Result |
|---|---|---|
| C0 | section 7a sizes | **survives**: all twenty-one |
| C1 | section 2 (the ramp) | **survives**: the target scaled by `00D117DC` = −4096; the collapse `base += (delta × progress) >> 12`; `step = 0x1000 / (max(frames, 1) × [01DFE0B4])`; channel 1's progress restarts at 0; the getter `001EDE70` adds a second step |
| C2 | section 2 (one frame) | **survives**: ten channels from `+0x4C0`, the `0x1000` finish test |
| C3 | section 2 | **survives**: three qword stores of `0x1000` at `+0x4C0`, `+0x4C8`, `+0x4E0` (channels 0, 1, 4) |
| C4 | sections 3, 7a | **survives**: channels 6, 7, 8 by call and 9 by tail-jump, at the four cited sites |
| C5 | section 3 | **survives**: `+0x2A8` read; ramps over 3 and 1 frames |

No correction.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-character-fades-the-ten-channels-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002915C0` | 389 B | walks the list headed at qword `rcx+0x10F20` (next pointer at node `+0x9B0`) and returns the first node whose dword `+0x980` equals `r9d`; otherwise allocates through a 258-byte routine (0, qword (qword `0209BE80`)+0x10FC0, `0x9D0`), returning null when that fails, and on the new node calls a 28-byte zero-fill helper (node, `0x9D0`) twice, then either a 7-byte 16-byte-copy helper (node+0x960, `r8`) when `r8` is non-null or ORs 2 into byte `+0x991`, stores `r9d` at `+0x980` and calls a 49-byte helper (node+0x960, `r9d`); stores `dl` at byte `+0x990`, ORs 4 into byte `+0x991` when the fifth (stack) argument is non-zero, stores the sixth (stack) float at `+0x9A8`, fills qword `rcx+0x10F50` with a 75-byte helper's result for qword `01E0C1E0` when it is null and copies it to `+0x988`, calls a 150-byte helper on a stack buffer and a 234-byte helper (node, that buffer), sets word `+0x9C0` to 1, stores a 65-byte helper's result for (old list head, node) as the new head and returns the node | `002915F1`, `00291624`, `0029166E`, `002916B3`, `0029171F` |
| `002E84B0` | 72 B | when `rcx` is non-null, its qword `+0xC0` is non-null and the dword it points to is not -1 with a low word that is not -1, takes that sign-extended word times `0x740` plus qword `022C6F28` and, when the result is non-null and its dword `+0x284` is non-zero, tail-jumps a 131-byte routine with `rcx` set to that address (`xmm1` and the other arguments unchanged); every other path returns without a call | `002E84B8`, `002E84C4`, `002E84D6`, `002E84E6`, `002E84F2` |
| `002E8500` | 60 B | when `rcx` is non-null and the dword at `rcx` is not -1 with a low word that is not -1, takes that sign-extended word times `0x740` plus qword `022C6F28` and, when the result is non-null and its dword `+0x284` is non-zero, tail-jumps a 131-byte routine with `rcx` set to that address (`xmm1` and the other arguments unchanged); every other path returns without a call | `002E8508`, `002E8510`, `002E851A`, `002E852A`, `002E8536` |
| `002EBBB0` | 50 B | clears bit 0 of byte `0215FD56` when `ecx` is non-zero and sets it when `ecx` is zero, stores the byte back, then ORs 1 into dword `+0x48818` of the object at qword `022C6F28` when the whole byte is now zero and clears that bit 0 otherwise | `002EBBBB`, `002EBBBF`, `002EBBC1`, `002EBBD2`, `002EBBDA` |
| `002EBBF0` | 64 B | builds the mask `1 << cl` and clears it in byte `0215FD56` when `edx` is non-zero or sets it when `edx` is zero, stores the byte back, then ORs 1 into dword `+0x48818` of the object at qword `022C6F28` when the whole byte is now zero and clears that bit 0 otherwise | `002EBBFD`, `002EBC07`, `002EBC0F`, `002EBC20`, `002EBC28` |
| `00348700` | 42 B | reads one float with `VMValueStack_PopNumericDiscard(r9)`, calls `002EDA70` with it in `xmm0` and tail-jumps `CharacterRenderSystem_SetFadeStartDistance` with the same float in `xmm0` | `0034870C`, `00348714`, `00348725` |
| `00348B00` | 56 B | reads two floats with two `VMValueStack_PopNumericDiscard(r9)` calls, calls `CharacterRenderSystem_SetFadeStartDistance` with the second in `xmm0` and tail-jumps `002E83A0` with the first in `xmm0` | `00348B11`, `00348B1C`, `00348B21`, `00348B33` |
| `00348F20` | 85 B | reads two floats with two `VMValueStack_PopNumericDiscard(r9)` calls, then passes them in `xmm0` in this order: the second to `002EDA70`, the first to `002EDA80`, the second to `CharacterRenderSystem_SetFadeStartDistance`, and tail-jumps `002E83A0` with the first | `00348F41`, `00348F49`, `00348F51`, `00348F59`, `00348F70` |
| `003497D0` | 42 B | reads one float with `VMValueStack_PopNumericDiscard(r9)`, calls `002EDA80` with it in `xmm0` and tail-jumps `002E83A0` with the same float in `xmm0` | `003497DC`, `003497E4`, `003497F5` |
| `00373160` | 534 B | returns at once when `ImageAddress_ResolveRuntimePointer(dword rcx+0xA0)` is null; otherwise decodes table A from dword `rcx+0x84` and table E from dword `rdx+0x84` with the same resolver, copies dword `rdx+4` to `rcx+8`, stores `r8w` at word `rcx+0x14` when `r8d` is not -1 or else copies dword `rcx+4` to `rdx+0x10`, then walks the signed word `rcx+0x8A` count of word indices stored from the start of A's `0x290`-stride entry `word rcx+0x88`; for each indexed A entry it copies word `+0x270` to `+0x28E` and, only when `r8d` is -1, `dword rdx+0x9C` is 2 and dword `+4` of a 34-byte helper's result for (the `rcx+0xA0` table, word `+0x27E`) has bit `0x100`, takes a 160-byte helper's result for (`rdx`, a 22-byte helper's result for that pointer); when that is not -1 and a 109-byte helper (`rdx`, it) returns non-zero, it stores `RuntimePointer_EncodeImageAddress(A entry)` at `+0x278` and the A entry's word `+0x27E` at `+0x27C` of E's entry of that index, calls `0046D100` to copy the 64 bytes at E's entry `+0xC0` and `+0x150` over the A entry's `+0xC0` and `+0x150`, and ORs 2 into the A entry's word `+0x280` (first setting its `+0x270` to -1 and copying E's `+0x270` to its `+0x276` when its `+0x270` names an A entry whose `+0x28E` is -1) | `00373244`, `00373255`, `0037327F`, `003732F7`, `00373331` |
| `003AFD50` | 37 B | takes the `0x70`-stride entry of `02B3F570` indexed by `cl` and, when its dword `+4` equals `ecx`, stores `xmm1` at its `+8`; otherwise stores nothing | `003AFD53`, `003AFD63`, `003AFD66`, `003AFD6F` |
| `003AFD80` | 73 B | takes the `0x70`-stride entry of `02B3F570` indexed by `cl` and, when its dword `+4` equals `ecx` and its float `+0x10` differs from float `rdx+4` (or the compare is unordered), stores that float at `+0x10` and 1.0 (`01CEBBA8`) divided by it at `+0x14`; otherwise stores nothing | `003AFD95`, `003AFDAB`, `003AFDBA`, `003AFDBE`, `003AFDC3` |
| `003B6BB0` | 28 B | takes the `0xE0`-stride entry indexed by `cl` in the table at qword `02B40528` and, when its dword `+0x10` equals `ecx`, stores `xmm1` at its `+0x2C`; otherwise stores nothing | `003B6BB3`, `003B6BC1`, `003B6BC6` |
| `003B6BD0` | 28 B | takes the `0xE0`-stride entry indexed by `cl` in the table at qword `02B40528` and, when its dword `+0x10` equals `ecx`, stores `xmm1` at its `+0x44`; otherwise stores nothing | `003B6BD3`, `003B6BE1`, `003B6BE6` |
| `003E4780` | 59 B | returns, computed in double and converted to float, the signed word `rcx+0x4B4` times 0.000244140625 (`00D117C0`) times float `rcx+0x22C` times `xmm1` times 0.003921568859 (`00D117C8`) | `003E4787`, `003E479E`, `003E47AA`, `003E47AE`, `003E47B6` |
| `0041FBF0` | 135 B | when dword `rcx+0x18` is not -1 takes `ResourceTable_ResolveEntryByIndex(qword ImageAddress_ResolveRuntimePointer(dword rcx+0x10)+0xD98, dword rcx+0x18)` as a pointer (null otherwise); when `edx` is 1 ORs `0x20` into dword `rcx+0x284`, ORs 4 into the dword at that pointer when it is non-null and calls `00422F80(rcx)`, otherwise clears those two bits and calls `00422F30(rcx)`; then tail-jumps `00421030(rcx)` | `0041FC22`, `0041FC30`, `0041FC42`, `0041FC49`, `0041FC72` |
| `00420F90` | 29 B | ORs `0x10` into dword `rcx+0x284` when `edx` is 1 and clears that bit otherwise, then on both paths tail-jumps `00421030(rcx)` | `00420F95`, `00420F9C`, `00420FA1`, `00420FA8` |
| `004293C0` | 67 B | tail-jumps `003E5D00` with its arguments unchanged when `r9d` is at most 1 (signed); otherwise, when the fifth (stack) argument is 1, replaces `rcx` with the sign-extended word `rcx+8` times `0x740` plus qword `022C6F28` (returning when that word is -1, and using null when that entry's dword `+0x284` is zero), and then tail-jumps `003E5D60` when `rcx` is non-null and returns otherwise | `004293C4`, `004293CA`, `004293DF`, `004293F5`, `004293FC` |
| `0042DE50` | 59 B | when a 183-byte helper (`rcx`, qword `rdx+8`) returns zero, calls `0041FBF0(rcx, dword rdx+0x38)` and then `00421030(rcx)`; otherwise calls neither | `0042DE64`, `0042DE6D`, `0042DE73`, `0042DE7B` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-how-a-character-fades-the-ten-channels-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0042E540` | 8 B | tail-jumps to `00420E70(rcx, dword rdx+0x74)` with the incoming `rcx` | Interior anchor `0042E543` |
