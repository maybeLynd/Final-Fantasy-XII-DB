---
system: How a character is lit - which lights reach it, and how the ambient term is settled
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the light selector 003ACC10 (2,342 B), the per-character gather 003ABD50 (950 B), the ambient evaluator
    003ACAA0 (358 B) and the small class-filter and lookup bodies disassembled and read whole; the head of the light
    create routine 003AB960 read (the request copy and the handle); field names of a light taken from the selector's
    reads and checked against two requests built elsewhere; accesses to the module's globals found by rip-relative
    sweep; prior art on the weather page joined
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-character-lighting-falsification-pass-1
  note: written by FABLE; static throughout. The five per-kind evaluators, the list builder and the caller of the
    gather were not read and are named as such - so this page says WHICH lights reach a character and how ambient is
    resolved, not what a light of each kind does to a surface; pending first review
---

# How a character is lit

Every character is lit on its own. Once per character the renderer walks the scene's lights, throws out the ones that
are not meant for this character, settles a single ambient colour, and hands the shader **at most six** directional
terms. This page is that choice. It came out of [how a status shows on a character](../Character-Render-Records/how-a-status-shows-on-a-character.md),
whose colour looks turned out to be made of lights.

## 1. What the player sees

- A light can be **private to one character** (a status tint), meant for **everyone but one character**, tied to a
  character's attached objects, or **anchored to the camera** so that it always falls on the character from the
  viewer's side.
- Ambient light is not simply summed. Lights carry a priority; **the highest-priority ambient wins**, a tie going to
  the stronger - unless the winner is of the *additive* sort, in which case the character gets the sum of all additive
  ambients instead.
- Whole classes of light can be switched off at once. Status display denial switches off the status lights; two other
  switches exist.
- A character can be told to treat ambient light specially - multiplied, or pulled toward a colour of its own - and to
  scale every ordinary light that reaches it. Stone and the status tints use both.

## 2. A light

Lights live in a **128-entry pool of `0x70`-byte entries** at `[02B3F528]`. `003AB960` takes a free entry, makes the
handle `counter << 8 | index`, and copies the caller's `0x50`-byte request to entry `+0x20`
([the weather page](../../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md) describes the slot claim);
`003ABD00` (26 B) turns a handle back into that block, checking the whole handle. Entries are chained by a pointer at
entry `+0x10`. The selector reads the block like this - offsets are **into the request**, entry offsets are `0x20` more:

| request | what | values met |
|---|---|---|
| `+0` | **type** | 6 = ambient; 7 = *look in the character's own list*; anything else is a directional kind, 1 to 5, evaluated by the gather |
| `+1` | **priority** | `0x20` for the weather's lights, `0xBF` / `0xBE` for the status lights |
| `+2` | subtype (ambient: how the colour is formed, section 4; 5 = *this entry is a multiplier*) | |
| `+3`, `+4` | **scope** kind and sub-kind, section 3 | |
| `+5` | flags: bit 4 *exempt from the character's ambient mode*; bits 1 to 3 choose the gather's matrix; `0x80` or more *exempt from the character's light scale* | |
| `+7` | flags: bit 0 *exclusive* (not additive); bit 1 *skip*; **bits 2 to 7 the light's class mask** | |
| `+8` | target: a character id, a typed handle or a group mask, by scope | |
| `+0x10` | colour | |

Two makers were checked against this table. The weather's preset rebuild registers up to three lights `0x01002001` -
type 1, priority `0x20`, scope 1 - and one `0x01042006` - ambient, subtype 4 (the weather page has the bodies). The
status tint registers `0x0100BF06` with `+4` = 2, `+5` = `0x90`, `+7` = `0x80`: an ambient of priority `0xBF` for one
character, class 5, exempt from both of that character's own adjustments.

## 3. The selector - `003ACC10`, read whole

`(list head, out: chosen lights, caller's colour scale, out: ambient colour; on the stack: the render record or null,
the character's id, the character's placement)`. It returns the number of directional lights it chose.

**Class filter.** One byte, `02B3F501 | 02B3F520`. A light is skipped when `(its +7 >> 2) & filter` is non-zero, or
when bit 1 of its `+7` is set. `003ACA80` (7 B) ORs bits into `02B3F501` and `003ACA90` (9 B) clears them; by a raw call sweep their callers are
the status display-deny latch (bit 5), the per-frame effect driver and a sibling of it on a test of the system-stop
masks (bit 0), two bodies in the `003B8xxx` run, one of them the event-effect interpreter, and - clearing **bit 3** -
the area unload and the actor manager's definition-payload bind. Nothing in the sweep *sets* bit 3 through the setter;
what class 3 is was not established.

**Scope.** The kind byte decides who the light is for:

| kind `+3` | sub `+4` | the light reaches the character when |
|---:|---:|---|
| 1 | 2 | there is a record and **the target is this character's id** |
| 1 | 8 | there is a record and **the target is *not* this character's id** |
| 1 | 9 | there is a record - and the light is first **re-aimed from the camera** (below) |
| 1 | other | always |
| 2 | 3, 4, 5 | there is a record and the target, a typed handle, passes a predicate of the typed-handle layer against this character's id - one predicate for 3, another for 4, either for 5 |
| 4 | - | there is **no** record and the target equals the id |
| 5 | - | never |
| 0, 3, 6+ | - | always |

**The camera-anchored light (kind 1, sub 9).** The light's float `+0x1C` (request offset) is set from a byte of the
character's resolved object - 1 -> 0, 2 -> 0.25, 3 -> 0.5, otherwise 1.0 - and its vector at request `+0x30` becomes
*camera position minus character position*, normalised, then turned about the vertical by the pair `(a, b)` at request
`+0x40` / `+0x44`: `x' = x + b x + a z`, `z' = z + b z - a x`. Camera position is `02AEDF20`
([how a camera reaches the renderer](../Scripted-Camera/how-a-camera-reaches-the-renderer.md)).

**By type, once in scope:**

- **Anything but 6 or 7** is appended to the chosen list and counted.
- **7** fetches the character's own light list through the object at record `+0x108` and walks it. Its entries are the
  same block without the pool header. Their scope is simpler - kind 1 sub 2 needs the id to match; **kind 3 tests a
  group mask**: `003AED20(id)` gives the character's group bits, sub 7 needs them to meet the target and sub 6 needs them
  not to. Ambient entries are handled as below, with the per-character scale switched off around the evaluator;
  the rest are appended.
- **6, ambient**, is settled in place:
  1. subtype 5 is not a light at all: its colour becomes **the multiplier** applied to the final ambient (last one
     met wins);
  2. otherwise the evaluator of section 4 gives a colour and a strength; while the byte `02B3F503` is set the colour is
     scaled by the global `02B3F51C`;
  3. unless the light's `+5` bit 4 is set, **the character's ambient mode** is applied - record byte `+0x5E0`: 2
     multiplies the colour by record `+0x5DC`; 1 blends it toward the record's colour `+0x5D0` by `+0x5DC` (for additive
     lights the blend is done once, on their sum, at the end);
  4. an **additive** light (bit 0 of `+7` clear) is added to a running sum;
  5. **the priority contest**: a light whose priority is higher than the best so far becomes the base ambient; at equal
     priority the greater strength wins. The winner's *exclusive* bit is remembered.
- At the end: **if the winner was additive, the base is replaced by the additive sum**; the result is multiplied by the
  multiplier and its fourth component set to 1.

So an exclusive, high-priority ambient silences every other ambient on that character; an additive one of the same
priority merely joins the sum.

## 4. The ambient evaluator - `003ACAA0`, read whole

Colour by subtype, with `c` the light's colour and `s` the caller's colour scale: 0 (and any value above 4) -> `c`;
1 -> `s`; 2 -> `c x s.w`; 3 -> `s x s.w`; 4 -> `c x s` channel by channel. The strength it returns is a weighted sum of
the absolute channels of `c`. Then **the character's light scale**: only while the enable byte `02B3F502` is set *and*
the light's `+5` is below `0x80`, colour and strength are multiplied by `02B3F518` - the value the gather copied from
record `+0x5EC`. The enable is a one-byte setter's to write; status display denial clears it.

## 5. The gather - `003ABD50`

Read whole and written up, with its anchors, on
[the status page, section 4a](../Character-Render-Records/how-a-status-shows-on-a-character.md): it stores the scale,
calls the selector, evaluates the chosen lights by kind in runs of falling priority, and writes at most six into a
`0xE0`-byte block - directions negated and normalised in two groups of three, colours at `+0x60`, ambient at `+0xC0`.

## 5a. Two of the five kinds, read (added 2026-09-19)

**Kind 1 is a directional light - `003AD540` (745 B), read whole.** The colour is formed by the same five subtype forms
as ambient (section 4). The direction is the vector at request `+0x30`: copied as it stands, or - when the request's
byte `+6` is 2 - **turned by the matrix the gather installed**, so that a light authored in a local frame follows that
frame. The evaluated record's `+0x20` is set to 1 when the light's scope sub-kind is 9, which is what the gather copies
to the output's `+0xD0`: **`+0xD0` is the index of the camera-anchored light among the six**, or -1. The strength is the
plain sum of the three weighted absolute channels. *The weather's three type-1 lights are directional lights, and Oil's
status light is a directional light with a negative colour.*

**Kind 2 is a point light - `003AE0E0` (991 B), read from its space switch to the end; its head was not read line by
line and is the same colour switch by the fields it touches.** The direction is *character position minus light
position* (request `+0x20` holds the position; the character's position is row 3 of the installed matrix): as given for
byte `+6` = 0, through the matrix for 2, and for 1 the negated position is stored into the light's own direction field
instead. Unless bit 0 of the light's `+5` is set, the colour is scaled by **`1 - d^2 x k`**, where `k` is the float the
create routine precomputed at request `+0x30` as `1 / range^2` from the range at request `+0xC`; **at or beyond the
range the strength is written as zero and the gather drops the light.**

**Both kinds apply the character's light scale under the same two conditions as ambient** - the enable byte `02B3F502`
set, the light's `+5` below `0x80` - and when they do they also store the scale in the evaluated colour's fourth
component.

**Kinds 3, 4 and 5, read the same day from their geometry to the end** (their heads are the same colour switch by the
fields they touch, and were not read line by line; none of the three is anchored). All three begin like the point
light - *character minus light position* in one of the three spaces - share its falloff `1 - d^2 x k` with their own
`k`, skip the falloff under bit 0 of `+5`, and end in the same strength sum and the same two scale conditions.

- **Kind 3, `003AD830`: a point light cut by a plane.** Before the falloff it takes the dot product of that vector
  with the light's axis at request `+0x30`; **when the dot is not positive the strength is written as zero** - the
  character is on the dark side. The dot is a test only; it does not scale the colour. `k` is at request `+0x40`.
- **Kind 4, `003AE4C0`: a spot light.** With both vectors normalised, `cone = min(1, (cos - [+0x44]) x [+0x4C])`, where
  `[+0x4C]` is the reciprocal `1 / ([+0x40] - [+0x44])` the create routine stored - an inner and an outer cone cosine.
  The colour is scaled by `falloff x cone`; either one at or below zero gives zero strength. `k` is at `+0x48`.
- **Kind 5, `003ADC40`: a segment light.** Its two ends are request `+0x20` and `+0x40`. It projects the character's
  position onto the segment with the dot product and reciprocal stored at create, **clamps the parameter to the ends**,
  and then behaves as a point light at `A + t (B - A)`. `k` is at `+0x30`.

So the two shapes the next paragraph calls inference from the precompute were since read in the evaluators themselves.

**The create routine, `003AB960` (506 B), now read whole**, settles two things. *What it precomputes:* `1 / range^2` from
the range at request `+0xC` for every kind from 2 to 5 - into request `+0x30` for kind 2, `+0x40` for kind 3, `+0x48` for
kind 4 and `+0x30` for kind 5; kind 4 also gets the reciprocal of a difference of two of its floats (`+0x40`, `+0x44`), the
usual shape of an inner and an outer cone, and kind 5 a squared axis length, a dot product and a reciprocal built from
two vectors, the usual shape of a segment - both *shapes* are inference, the stores are read. *What the light list is:*
after the copy the entry is appended to a doubly linked list - previous at entry `+8`, next at `+0x10` - whose head is
`02B3F508` and whose tail is `02B3F510`. **The list the gather hands the selector is simply every live light, in the
order it was created.**

## 5b. The gather for things that are not characters - `003AC110` (added 2026-09-19)

The light list has a second walker, 1,876 bytes, called with **an id and an output block and no render record**: the
selector and the gather in one body. Its selection half was read; its second half was not read line by line and
mirrors section 5 by its calls - the same five kind evaluators, the same two ordering routines, the six-light cap, the
`+0xD0` index - with the normalise done inline.

What differs is exactly what a character brings:

- it **forces the light scale `02B3F518` to 1.0** before it starts - nothing dims a non-character;
- the same class filter, but **the scopes that need a character are refused**: kind 1 with sub-kinds 2, 8 and 9 (this
  character, everyone but, camera-anchored) and kind 2 (the typed-handle relation). **Kind 4 is accepted only when the
  light's target equals the caller's id** - the counterpart of the character selector's *no record and target equals
  id* arm, so kind 4 is *a light for one particular non-character object*; kind 5 is refused here too;
- type 7, the pointer into a character's own list, is skipped;
- ambient is the same contest - priority, strength on a tie, additive sum when the winner is additive, the subtype-5
  multiplier, the `02B3F503` / `02B3F51C` scale - **with no ambient mode**, there being no record to carry one.

Its one caller by a raw call sweep and a conditional-jump sweep is a body in the effect-element address band, not read
and not named here: this is, by that placement, how a lit piece of an effect gets its lights.

## 5c. Where the block goes, and where the fade joins it (added 2026-09-19)

The character gather has one caller by raw call and conditional-jump sweeps: **the model instance's draw setup,
`004FD4B0`** (2,261 B; only its head, up to the first render-command write, was read - not anchored). It calls the
gather with the instance's render record (`+0xF8`), its two matrices (`+0xE8`, `+0xF0`), its colour scale (`+0x90`) and a
flag that is the negation of a tag lookup in the record's payload - and skips the call when the instance's id word
`+0xE0` is -1 or it has no first matrix. **The block the gather fills is a global, `02CA8110`**; its ambient term is
therefore at `02CA81D0`.

Straight after the call the setup rewrites that ambient term in place:

```
ambient.rgb  *= instance +0xA0, +0xA4, +0xA8
ambient.a    *= instance +0xAC  x  (signed word +0xB0) / 4096          ( x +0x248 when bit 0 of +0x244 is set )
```

Those are the fields [how a character fades](../Character-Render-Records/how-a-character-fades-the-ten-channels.md)
shows a record's frame writing into its model instance: `+0xA0` the record colour times the `rgbatrans` vector, `+0xAC`
the final opacity, `+0xB0` the Q12 composite. **So a character's fade reaches the renderer as the fourth component of
its ambient light term, and its script colour as a multiplier on that term's colour** (whether the unread rest of the
setup also scales the six directional colours was not checked). By a rip-relative sweep the block's readers are the 9.7 KB model draw and two smaller neighbours of
it; what the shader does with the fourth component was not read.

**Where `+0x244` and `+0x248` come from (added 2026-09-19).** `0041F270` (124 B, read whole) publishes a render
record's **blend override** to its model instance. When bit 1 of record `+0x4A0` is set it sets instance `+0x244`
bit 0, copies record `+0x4A4` into instance `+0x244` bits 1-3 (a three-bit mode), and copies record `+0x4A8`,
`+0x4AC`, `+0x4B0` to instance `+0x248`, `+0x24C`, `+0x250`; when the bit is clear it clears instance `+0x244` bit 0
and leaves the rest as it was. So the extra multiplier on the ambient alpha above is a per-record override, off by
default. *What writes the record's five fields, and what the mode and the other two values do in the draw, were not
read.*

## 6. Behaviour a reimplementation must keep

- Scope is evaluated per character, every time; a light for "everyone but X" and a light for "X only" can share a scene.
- Ambient resolution is a contest, not a sum - and becomes a sum only when the winner is additive.
- The multiplier entry (subtype 5) applies to whatever wins.
- A character's ambient mode and light scale do not touch lights that carry the exemptions, which is how a status light
  stays at full strength on a character whose other lights are dimmed.
- Six directional lights at most, taken in priority order, strongest first within a priority run.

## 7. What is not known

- The heads of four evaluators (kinds 2 to 5) were not read line by line; what the third space mode (byte `+6` = 1) is
  for; the units of range.
- ~~What builds the list the gather passes in.~~ *The create routine does; section 5a.* ~~What the 1,876-byte body
  `003AC110` beside it does with the same list.~~ *The record-less gather; section 5b.* ~~The character gather's one caller.~~ *Its head is read - section 5c; the rest of
  that 2,261-byte body was not.*
- What the two typed-handle predicates test, and what byte of the character's object sets the camera-anchored light's
  float. ~~What `003AED20` derives the group bits from.~~ *Read: it returns the dword at render record `+0x28C`, or 0 for
  id -1 or a free record (45 B). What writes `+0x28C` was not traced.*
- What sets `02B3F520`~~, `02B3F503` and `02B3F51C`~~. *(answered: see the `003AC900` paragraph below for `02B3F503` and `02B3F51C`; 2026-10-02, OPUS)*
- ~~The weights of the strength sum were not converted from their double constants.~~ *Converted 2026-09-19: 0.299,
  0.587 and 0.114 on red, green and blue - **a light's strength is the luminance of its absolute colour.***
- Nothing here was observed running.

## 8. Where each behaviour is in the bytes

| body | what | anchors |
|---|---|---|
| `003ACC10` selector (2,342 B) | class filter; loop head; class and skip tests; scope switch; id tests; handle predicates; camera anchor: float, difference, normalise, turn; type switch; append; own list fetch; group mask; enable cleared; evaluator; ambient mode 2 and 1; additive add; priority contest; tie by strength; main-list ambient; multiplier entry; end blend; additive replacement; multiplier applied | `003ACC33`, `003ACD20`, `003ACD2A`, `003ACD33`, `003ACD3C`, `003ACD6A`, `003ACD9F`, `003ACDE2`, `003ACE05`, `003ACE21`, `003ACE44`, `003ACE83`, `003ACECF`, `003ACEED`, `003ACF2A`, `003ACF40`, `003ACF6A`, `003ACFBF`, `003AD03F`, `003AD046`, `003AD0A0`, `003AD0B6`, `003AD0D0`, `003AD166`, `003AD175`, `003AD1A6`, `003AD205`, `003AD211`, `003AD23E`, `003AD29A`, `003AD359`, `003AD37D`, `003AD39A`, `003AD420`, `003AD49C`, `003AD4EF` |
| `003AD540` kind 1, directional (745 B) | camera-anchored flag; subtype switch and its four other forms; matrix test; direction as given; direction through the matrix; strength; the two conditions; the scale | `003AD543`, `003AD550`, `003AD5A6`, `003AD5EB`, `003AD620`, `003AD656`, `003AD694`, `003AD70B`, `003AD722`, `003AD7BE`, `003AD7DB`, `003AD7E3`, `003AD7EC` |
| `003AB960` create (506 B) | free-entry scan; counter and handle; request copy; kind switch; kind 5, 4, 3 and 2 precompute; empty-list link; append | `003AB970`, `003AB988`, `003AB9AB`, `003AB9B3`, `003AB9DA`, `003ABA02`, `003ABAAC`, `003ABADE`, `003ABAFA`, `003ABB14`, `003ABB1D`, `003ABB3D`, `003ABB50` |
| `003ACAA0` ambient evaluator (358 B) | subtype switch; four colour forms; strength; the two conditions; the scale | `003ACAA3`, `003ACACD`, `003ACB07`, `003ACB41`, `003ACB6A`, `003ACB7A`, `003ACB8E`, `003ACBD0`, `003ACBD2`, `003ACBEE` |

## 9. Related

- [How a status shows on a character](../Character-Render-Records/how-a-status-shows-on-a-character.md) - the status
  lights, the record's three lighting fields, and the gather.
- [Weather](../../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md) - the makers of the area's
  lights.

## Cross-subsystem neighbours

**World / weather - CLIENT.** The weather's preset rebuild is a maker of lights through the create routine; that page
owns the presets, this page owns what a registered light's bytes mean to a character.

**Actor / entity - CLIENT.** Two ActorEntity-filed bodies, the area unload `002628B0` and
`ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`), call the class filter's clear routine `003ACA90` with the mask 8 -
they re-enable light class 3 when an area is dropped and when a definition payload is bound. Only those two call sites
were read; the filter is this page's, the moments are theirs.

**Shared helpers - by role.** The typed-handle predicates, the object resolver, the vector normaliser, the ordering
routines and the character's own-list accessor are described by role and not named, because naming a shared leaf
imports every one of its callers.

**Audio + Movement + UI - MECHANICAL (17 edges, two shared callees one remove away).** The batch-52 sections cite
two shared helpers: `00202C70` (the `004FD4B0` section) and `00202DE0` (the `003AE4C0` section). `00362850` (Audio)
calls both; Movement's `00230790`/`00338490`/`00314F50`/`00335E50` and UI's `002AF960`/`002D2600`/`002D28E0`/`003F26F0`
(plus seven more UI bodies) call one or the other. The crossing is those two leaves being consulted across the
engine — this page owns how a registered light's bytes read on a character, not whatever those layers use the same
helpers for. Edge list from `edges.tsv` (batch-52 audit, SWE2-EC7).

**Input - MECHANICAL (2 edges, one shared callee one remove away).** The batch-87 `003DDC20` section cites the
shared record resolver `00263FF0`; Input's `00226BE0` and `002E09A0` call it too. The crossing is the resolver
being shared — this page owns the `byte[+0x17]` flag write, not whatever Input resolves through the same leaf.
Edge list from `edges_live.tsv` (batch-87 audit, SWE2-EC7).

**CoreRuntimeScheduling - MECHANICAL (SWE2-EC7-172, 2 edges).** The batch-137 `003AC900` section names
`00376BE0`, the sibling render-vector writer the scale commit runs beside; `MainLoop_UpdateAndRenderFrame`
(`0022B8C0`) and `0022BC20` are its callers. The crossing is that writer being driven per frame — this page
owns what the `02B3F51C` scale means to a lit character, not the scheduler that invokes the writer.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Script_VM_Native_Bridge — CLIENT (22 edges).** Two script verb bodies drive this page's flag write directly: `003477E0` and `00347D60` each fetch the current record, take its manager index at `+0x28` and tail into `003DDC20` with 1 and with 0, so one verb sets and the other clears bit 6 of the record's byte `+0x17`. Twenty more Script VM bodies (26 to 157 bytes; among them `0033F7F0`, `00342490`, `00348130`, `0034E460`, `00352D70` and `0050D0C0`, and 14 more) call the slot-array address `00263FF0` (`02098E10` plus the index times `0x288`) that `003DDC20` resolves through. Scripts switch this per-record flag bit, which the lighting callers write, on and off through their own verbs; the other twenty edges are script bodies sharing the manager-slot resolver, not lighting.

## SWE2-EC7-52 update (2026-09-19) - `004FD4B0`

`004FD4B0` (2261 B) is the 2,261-byte light-gather body the page's head-read covered - stack-cookie prolog, `word[rcx+0xE0]`/`[rcx+0xF8]` record, `00202C70` pair/`003E56E0`/`003ABD50`/`005044B0`/`00504450`, `02CA7F80`/`02CA8040`/`02CA8000` tables. Interior anchor `004FD536` (a `00202C70` call).


## SWE2-EC7-52 update (2026-09-19) - `003AD830`

`003AD830` (1034 B) is a call-free kind-3 point light cut by a plane - `byte[rcx+2]` mode switch, `[r8+0xC] dot [r8]` writes `02B3F4F0`. Interior anchor `003AD8D3` (the mode-3 product head).


## SWE2-EC7-52 update (2026-09-19) - `003AE0E0`

`003AE0E0` (991 B) is a call-free kind-2 point light - `byte[rcx+2]` mode switch, `[r8+0xC]`-scaled falloff writes `02B3F4F0`. Interior anchor `003AE17F` (the mode-3 product head).


## SWE2-EC7-52 update (2026-09-19) - `003AC110`

`003AC110` (1876 B) is the record-less light gather - ~~`01FD4A78` list~~ it walks the light list `02B3F508`; `01FD4A78` is a work-area base whose `+0x1000` and `+0x2000` it takes as two sub-areas *(corrected 2026-10-02, OPUS: `003AC110`+0xB1 `mov r10, qword ptr [02B3F508]` and `003AC110`+0xE8 `test r10, r10`; `003AC110`+0x1F, +0x49 and +0x58 for `01FD4A78`)*, `00861EC0`/`003ACAA0`/`003AEBC0` plus per-kind calls `003ADC40`/`003AE4C0`/`003AD830`/`003AE0E0`, `02B3F5xx` slots. Interior anchor `003AC190` (a `00861EC0` call).


## SWE2-EC7-52 update (2026-09-19) - `003ADC40`

`003ADC40` (1172 B) is a call-free kind-5 segment light - `byte[rcx+2]` mode switch, `[r8+0xC]`-scaled ends write `02B3F4F0` (sibling skeleton of `003AD830`/`003AE0E0`). Interior anchor `003ADCF5` (the mode-3 product head).


## SWE2-EC7-52 update (2026-09-19) - `003AE4C0`

`003AE4C0` (1268 B) is the kind-4 spot light - `00202DE0` quadruple plus `00808C40`, normalised-vector cone `(cos - [+0x44]) x [+0x4C]` into `02B3F4F0`. Interior anchor `003AE774` (a `00202DE0` call).

## SWE2-EC7-54 update (2026-09-19) - `003AEBC0`

`003AEBC0` (340 B) is a light-gather body - `003AEBC0` self-recursive call. Interior anchor `003AEC80` (a `003AEBC0` call).


## SWE2-EC7-87 update (2026-09-20) - `003DDC20` resolved-record flag write measured

`003DDC20` (38 B) is the bit-6 flag write the lighting callers
run: `00263FF0(rcx)` resolves the record, `byte[+0x17]` is
cleared of `0x40` then OR-ed with `(edx != 0) << 6`, and the
body tails `003DD6C0` - one flag bit by argument.
Interior anchor `003DDC41` (the `003DD6C0` tail).

## SWE2-EC7-113 update (2026-09-21) - `00862910` measured

`00862910` (31 B) is the
float4-to-int4 conversion
`004FD4B0` runs: four
`cvttss2si` reads take the
`rdx` vector's lanes to
`dword[+0]`, `+4`, `+8`,
`+0xC` of `rcx` -
truncating, call-free.
Interior anchor `00862916`
(the second `cvttss2si`).

`003AC900` (28 B) is the lighting-scale commit the two `00376xxx` render-vector writers (`00376AC0`, `00376BE0`) run mid-body: `xmm0` multiplies the `02B3F51C` global, `02B3F503` is set to 1, and the product lands back in `02B3F51C` - the one-way scale-factor store the lit-character path publishes.

Interior anchor `003AC90C` (function `003AC900`).

`0024E6D0` (242 B) is the class-chained entry probe `003ACC10` runs: `ecx >> 0x1C & 0xF` selects a `020910F0` chain head, `word[+4] == cx` and `word[+6] == [rsp+0x32]` qualify a node else `+0x348` links on; a hit runs `002E9B80`, then a `byte[rbx+0x372]`-counted loop scans `rsi` dwords for `1` - the per-class keyed lookup the lighting path consults.

Interior anchor `0024E79A` (function `0024E6D0`).

`0024E2F0` (205 B) is the bucketed lookup `003ACC10` calls: `arg1 >> 28 & 0xF` selects a chain head from `020911F0`, the walk follows `[node+0x348]` matching `+4`/`+6` words against the id pair, then a `(bucket-1) < 8`-gated jump table at `0024E3C0` picks the compare - `003B0BF0` + `[rax+0x11]==1` -> `edi == [node+8]`, or `002E9B80`-decoded id `== edi`, or a raw `edi == [node+8]` - the kind-aware 'does this record carry arg2' probe

Interior anchor `0024E355` (function `0024E2F0`).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives

**Attack.** Sections 2 to 5b's structural claims became checks at their instructions. Script:
`Tools/analysis-kit/gfz-scripts/falsify_character_lighting.py`, output `falsify_character_lighting.out`, image
`73461d08…`, 0 BROKEN, exit 0. The per-kind evaluators' arithmetic (section 5a's falloff and cone forms) and section 5's
gather, written up on the status page, are carried.

| # | Clause attacked | Result |
|---|---|---|
| G0 | sizes | **survives**: all ten cited sizes |
| G1 | sections 2, 5a (create) | **survives**: the pool `[02B3F528]` in `0x70` steps bounded by `0x80`; handle `[02B3F504] << 8 \| index`; five 16-byte moves (`0x50` bytes) to `entry + 0x20`; `1 / range^2` at `entry + 0x50`; the list `02B3F508` / `02B3F510` |
| G2 | section 3 (class filter) | **survives**: `003ACA80` is `or [02B3F501], cl` and `003ACA90` `not cl; and [02B3F501], cl`; the selector reads both filter bytes |
| G3 | section 3 (ambient, camera) | **survives**: record `+0x5E0` / `+0x5DC` / `+0x5D0`; `02B3F503` / `02B3F51C`; camera `02AEDF20` |
| G4 | section 4 | **survives**: the enable `02B3F502`, scale `02B3F518`, and the `+5 < 0x80` test |
| G5 | section 5b | **survives**: 1.0 is stored to `02B3F518` before the list walk; the only earlier call is the output memset |

No correction.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-character-is-lit-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003477E0` | 26 B | tail-jumps a 38-byte helper with `ecx` = dword `+0x28` of the pointer the 8-byte getter of qword `02099D70` returns and `edx` = 1 | `003477E4`, `003477E9`, `003477EE`, `003477F5` |
| `00347D60` | 23 B | tail-jumps a 38-byte helper with `ecx` = dword `+0x28` of the pointer the 8-byte getter of qword `02099D70` returns and `edx` = 0 | `00347D64`, `00347D69`, `00347D6B`, `00347D72` |
| `003AED20` | 45 B | returns 0 when the word `cx` is -1; otherwise forms the record address qword `022C6F28` plus the sign-extended `cx` times `0x740` and returns 0 when that sum is zero or the record's dword `+0x284` is zero, else the record's dword `+0x28C` | `003AED24`, `003AED2D`, `003AED34`, `003AED3D`, `003AED46` |
| `003DD6C0` | 113 B | calls a 21-byte record-address helper with i for i 0 to 4 and sets a flag when any returned record has bit 0 of byte `+0x10` and bit `0x40` of byte `+0x17` both set; with the flag clear it calls a 7-byte helper with 0 and returns, with it set it calls a 22-byte helper and returns when the result AND `0xFFFFFFFD` is non-zero, else tail-jumps a 31-byte helper with 2 | `003DD6D8`, `003DD6E3`, `003DD6E7`, `003DD6FA`, `003DD715` |
