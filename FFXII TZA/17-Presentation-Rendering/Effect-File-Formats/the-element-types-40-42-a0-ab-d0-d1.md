---
system: the element types 0x40-0x42, 0xA0-0xAB, 0xD0-0xD1
category: 17-Presentation-Rendering
status: "DOCUMENTED — GI-9 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the table/record interiors are not read everywhere; 00464090 read 2026-09-18 (an 8-byte setter of bit 1 in the element's +0x248, not a walk)"
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every cited body disassembled from the authority image (NATIVE/STATIC) for
    FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES; address-resolution re-verified
    2026-09-15 with verify_doc_addresses (0 flags)
last_reviewed: 2026-09-15
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: SWE2-AUDIT-SEM reviews FRONTIER-REQ-AUDITSEM-EFFECT-TYPES-00-0A /
    -EFFECT-TYPES-2; defect batch repaired same day (AUDITSEM-CONTRA-FRONTIER-EFFECT-TYPES-00-0A)
  falsification_passes: 1
  last_falsification: 2026-09-14
  last_falsification_by: SWE2-AUDIT-SEM
  falsification_result: nine defects in REVIEW-effect-types-2 (REJECT), repaired e23db2ab
  crossref_clean: true
  reopened_count: 0
---

# Element types `0x40`–`0x42`, `0xA0`–`0xAB`, `0xD0`–`0xD1` — the stragglers and the special pair

Package: `FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES` (group 4 of 4 — completes
the 65 handled types). Coordinates: `members/effect-type-methods.tsv`; helper
vocabulary: [the-element-types-00-0a](the-element-types-00-0a.md) §2 and
[the-element-types-60-74](the-element-types-60-74.md). **NATIVE/STATIC**;
authority EXE `73461D08…21F8`.

## `0x40` / `0x41` — minimal main-range types with a seventh

- `0x40`: step `00463FF0` (81 B; base + `00377190` + tail `004649A0`), update the
  56 B base+tail, walk `00464090` (8 B — *read 2026-09-18 (FABLE): not a walk at all; the whole body is `or byte ptr [rcx+0x248], 2; ret`, a setter of bit 1 in the element's byte `+0x248`*), setup
  `0053AAC0` (80 B: base + `3G@+0x80` + `1T@+0xC0` + `4G@+0xD0`; the `lea rax,
  [rdi+0x130]` is the record-end return value, not a call),
  seventh `00464050` (50 B) ~~calls `003ABCA0` on `+0x244`/`+0x24C`.~~ **Corrected 2026-09-29 (FABLE, GI-9):** two
  different handles - it removes the light `+0x244` through `003ABCA0` and releases the registry slot `+0x24C` by
  tail-jumping `00377360` ([what these types are](#what-these-seven-types-are-gi-9-2026-09-29-fable)).
- `0x41`: even smaller — update `00464F10` is a **5 B stub** (shared with `0xD0`),
  walk `00464BC0` 8 B, setup `0053AB10` 52 B (base + `4G@+0x80` only; `lea rax,
  [rdi+0xE0]` is the record-end return value — there is no `+0xE0` call),
  seventh `00464B80` (50 B) calls `003B42B0` on `+0x234`/`+0x238`. These are the
  thinnest handled types: nearly everything falls through to base/no-op.

## `0x42` — the lone bottom of the sub-range

Sub-range only (main dispatchers all `default`). Sub-step `0047BE20` (331 B —
the largest sub-step wrapper, calls `0020E620`, `003D7FF0`, `003D8D70`,
`003D8DE0`, `00808C40`); sub-setup `0050C450` (80 B, `3G@+0x80`-family);
sub-update `0047BDA0` (128 B — **not** the 56 B base form; calls `002F2530` plus
`003D8D70`/`003D8DE0` directly); sub-walk `0047BFA0` (8 B); sub-seventh
`0047BF70` (36 B) calls `003D8300` on `+0x230`/`+0x234`. Its methods reach a
`003D8xxx` helper family no other type in the band uses.

## `0xA0`–`0xAB` — the top of the type space

Main-range `0xA0`/`0xA1`/`0xA2`/`0xA5`; sub-range `0xA3`/`0xA4`/`0xA6`–`0xAB`
(`0xAC`+ are entirely absent — the tables admit them but every slot is default).

| type | methods | notes |
|---|---|---|
| `0xA0` | step `00460B80` (54 B: base+PRNG+tail `00460F30`), walk `00460BC0` 874 B, setup `0053A6F0` | compact record (`+0x80`–`+0x1F0`); walk calls `00398F90` (point transform) + `0039AF70` + `003A2D80`/`003A3010` |
| `0xA1` | step `00461090` (441 B heavy), walk `00461270` **3820 B** — the largest walk in the whole matrix | calls `001827B0`/`00182830` and the `00376350`–`00377100` helper family; seventh `00461250` touches `+0x1B4`/`+0x294`; setup has a resource store + `+0x1B0`/`+0x1B1` flag bytes |
| `0xA2` | step `00462480` (177 B, `003D8E50`-family), walk `00462540` 2921 B | `0017FFD0`+`0024E2E0`/`0024E460`/`0024E640` VU0-path calls; setup reaches `+0x7E0` |
| `0xA5` | step `004633A0` (same 177 B shape), walk `00463460` 2216 B | same walk family as `0xA2` |
| `0xA3` | sub-step `00524800` 527 B (own `0020E600`/`0020E620` fixups + `002F31C0`), sub-walk `00524A50` 462 B | sub-seventh `00524A10` resolves `+0x294` |
| `0xA4` | sub-step `005222D0` 43 B, sub-walk `00522300` 1268 B | setup to `+0x390` |
| `0xA6`/`0xA8`/`0xAB` | sub-steps `00524D70`/`00527110`/`0052BFB0` (177 B `003D8E50`-shape), sub-setups `0054EED0`/`0054F350`/`0054FE00` (401–485 B, identical field pattern `+0x350`/`+0x390`/`+0x3D0`/`+0x410`/`+0x450`), sub-walks `00524E30`/`005271D0`/`0052C070` (2966/3026/3790 B) | **one record family, three emit-size variants** — `0xAB`'s sub-walk is the second-largest in the matrix (after `0xA1`'s 3820 B `00461270`) |
| `0xA7`/`0xAA` | sub-steps `005269B0`/`00528AF0` (96 B: `001EDDA0` + base + `00314960` + PRNG + tail), sub-setups `0054F1B0`/`0054F700` (192 B), sub-walks `00526A10`/`00528B50` (844/907 B) | a second, smaller sibling pair |

## `0xD0` / `0xD1` — the special entries at the top of the range

Both sit past the nominal element bound (`0xD1` is the dispatcher's `ja` limit)
and behave unlike every other type:

- `0xD0`: step `00464F20` (501 B — iterates a byte array at `+0x140`–`+0x146`
  and the `+0x230` family); update is the 5 B `00464F10` stub; walk `00465680`
  is 13 B; ~~**the payload is the seventh method**~~ the seventh method `00465120` (963 B) — calls
  `00263C30`, `00263FF0`, `002E9B80`, `00358940`, `003589B0`, `003590D0`,
  `003A3FD0`, `003A4220`, `003A6BA0`, tail `00465510`. ~~Whatever `0xD0` is, its
  work happens on the seventh-method phase, not per-frame.~~ **Corrected 2026-09-29 (FABLE, GI-9):** the seventh
  method is the *release*: it walks the targets and restores them through `00465510`, then unregisters. The per-frame
  payload is `00465690`, called by the registry walker `00377230` from the main loop ([what these types are](#what-these-seven-types-are-gi-9-2026-09-29-fable)).
- `0xD1`: step `003D9040` (119 B; `002EA8B0` + `003A3E20` + tail `003D92C0`;
  touches `+0x2D0`/`+0x330`/`+0x338`/`+0x37A` and globals `02BBE2B2`/`02BBE2C4`),
  update base+tail `003D9000`, **walk is the `0016D6A0` no-op**, seventh
  `003D90C0` (134 B) calls `002EA8B0`/`00314960` and writes globals
  `01CB9527`-family + `02BBE22C`/`02BBE256`. Like `0x70`, `0xD1` does not emit
  on walk; unlike `0x70` its step and seventh are real.

## Package status — all 65 handled types now have a first read

With this page, every handled type in both dispatch mechanisms has its method
table, record map, and call signature on a page. ~~Still `not read` everywhere:
the step/update tail helpers (the per-type per-frame math), the walk emit tails
(the actual draw-list writes), `00431770`, and the identity of the `0054xxxx`/
`0052xxxx` sub-range tails. Naming any type player-facing still needs the emit
calls traced to draw-list ops or the EFX record linkage — explicitly out of
scope for this pass.~~ **Narrowed 2026-09-29 (FABLE, GI-9):** what each of this page's types is, and which record
fields drive it, is in [what these seven types are](#what-these-seven-types-are-gi-9-2026-09-29-fable); the
emits are on [UQ-204's table](../../_index/candidates/uq204-element-type-emits/README.md); `00431770` is read on
[the element types 0x00-0x0A](the-element-types-00-0a.md).

## What these seven types are (GI-9, 2026-09-29, FABLE)

*Static reads of the shipping image plus an authored-data census; nothing executed. Reader: FABLE (Claude Opus 5.5);
the `0x42` request floats, the `0xD0` target arms and the head of `0xD1`'s tail were settled by FABLE from the bytes. Checks: [`type_census.py`](members/type_census.py) (C1-C7, FAILS 0) and [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py) (K1-K18, FAILS 0).*

**The step is the element's birth.** Every step first calls `002F2D60`, which zeroes the age `+0x3C` / `+0x40` and the
update count `+0x48` (`002F30DA`, `002F30DE`, `002F3128`); the step dispatcher's one driver `00441B30` runs it on an
element it has just taken off the owner's free list `+0x120` (`00441BEC`–`00441C0D`, call `00441E71`). **At birth
`0x40`, `0x41`, `0x42` and `0xD0` register in a 128-slot registry** at `02ADBFE0` (`0x20` bytes a slot, handle
`serial << 8 | slot`, element at `+8`; `00377190`, whose four raw callers are exactly those births); their releases
unregister through `00377360`. **`00377230` walks the registry once per drawn frame** (callers `MainLoop_Draw` and
`MainLoop_UpdateAndRenderFrame`): it computes each element's visibility (`0024D4E0` and `0024D770`, `00377292`–`003772A7`),
stores it in the element's "shown" bit and calls the type's apply body - `004640A0` (`0x40`, `00377336`), `00464BD0`
(`0x41`, `00377317`), `0047BD30` (`0x42`, `003772FB`), `00465690` (`0xD0`, `003772EA`). The 8-byte walks of these types
only set that same bit. (A fifth arm, `0046EDD0` for byte `0xF0`, is unreachable: types stop at `0xD1` and nothing else
writes the registry.)

**`0x40` is an effect light.** The tail `004649A0` (392 B) places it (vector track `+0x80` + position, through the
parent) and colours it (colour track `+0xD0`, percent alpha), then runs the spawn slots with no cull. The apply
`004640A0` (804 B) fills a light request in the layout of [how a character is lit](../Character-Rendering/how-a-character-is-lit.md)
§2 and **creates** it with `003AB960` the first time (handle at `+0x244`, `00464390`), **updates** it with `003AC920` after
(`004643A0`). Definition byte `+0x120` picks the kind: 0 a **point light** (request word `0x8002`, `0046410A`), 1 a
**directional light** (`00464650`, word `0x8001`), 2 an **ambient** (`004643D0`, word `0x8006`). Range = float track
`+0xC0` (`00464166`); colour = the element colour × definition `+0x128` × 1/128, **negated when `+0x121` bit 1** (a
darkening light) and × the alpha while shown (`004641B0`–`004642A5`); position through `02AEEA20` (`004641E1`–`00464208`);
scope and target from `+0x122`–`+0x125` (an actor, the party-focus actor, or the context's, `004642DB`–`00464360`).

**`0x41` is a character colour filter.** The apply `00464BD0` (828 B) keeps one record in a 64-slot pool (`02B404E0`,
`0x60` bytes; issuer `003B4160`): colour track `+0x80` as floats (`00464CB8`–`00464CE5`), its alpha × the element's
(`00464CFC`–`00464D24`), kind 3 or 0 by definition `+0xD0`, scope and target from `+0xD1`–`+0xD6` - the lights' target
vocabulary (`00464D41`–`00464E52`). `003B4A50` collects the records whose scope matches a character, and `003B4310` -
called for `CharacterRenderRecord_UpdateViewDependentPresentationFactors` through `003E4E70` - returns the one with the
**lowest luminance `0.299 R + 0.587 G + 0.114 B` × strength** as that character's RGBA multiplier, `1,1,1,1` when none
(`003B434A`–`003B435F`, `003B4666`–`003B46C8`). Where several overlap, the darkest wins.

**`0x42` is a camera shake source.** The birth `0047BE20` (331 B) takes a slot in the 32-slot pool `02B4D7D0`
(`003D7FF0`, the pool authored command `0x2A` also uses) with a request `{f0, f1, f2, flag bytes, kind 1, encoded
pointer to the definition's track group +0x80}` (`0047BE64`–`0047BF04`), which `003D7FF0` copies to slot `+0x30`–`+0x4F`:
- `f0` (definition `+0x124`) → slot `+0x30`, the **intensity**: it multiplies the offset components in `003D83A0`
  (`003D89ED`, `003D8A24`, `003D8A3E`, `003D8A43`), and the apply `0047BD30` overwrites it every frame with the element's
  alpha × 1/128, or 0 while hidden (`0047BD7E`) - the authored value matters only until the first apply;
- `f1` (definition `+0x128`, or the frame-rate word `01DFE0BC` in contexts below 10) → slot `+0x34`, the **time rate**:
  the pool clock `003D8190` adds `2 × f1` to the slot time `+0` per tick (`003D81F3`–`003D8200`) and frees the slot when
  the group's duration `+0x94` is set and reached (`003D8204`–`003D827E`); it also advances two phases `+0x20`/`+0x24` by
  `+0x28`/`+0x2C` (from group `+0x98`/`+0x9C`, `003D80CD`–`003D80E4`) and re-rolls `+0x48` = rand(2.0) (`003D82C1`);
- `f2` (definition `+0x12C`) → slot `+0x38`, the **radius scale**: the allocator sets `+0x44` = group `+0x90` × `f2` (the
  radius R), `+0x48` = 1.2, `+0x4C` = 1/R (`003D80FF`–`003D811C`).

The update `0047BDA0` keeps the source position in slot `+0x10` (`0047BE02`). The pool's list walker `003D83A0` (2,190 B),
called only from `0037D970` - the writer of the per-draw camera **shake accumulator row** that the Screen Shake option
gates ([how a camera reaches the renderer](../Scripted-Camera/how-a-camera-reaches-the-renderer.md) §4a) - evaluates the
group at the slot's time, shapes each channel with a waveform chosen by group byte `+0xA0` (a sine from `01F004E0`, a
ramp, a square, a constant; `003D84FF`–`003D8688`), **attenuates linearly from 1 at the source to 0 at distance R from
the camera** (`1 − min(d, R) × (1/R)`, `003D88D9`–`003D88F5`; skipped when group byte `+0xA1` ≥ `0x40`, `003D8785`),
applies the intensity and **adds** a camera position offset and a target offset into its output (`003D8A6C`–`003D8B35`),
all × the global scale `02B4D7B8` (`003D8BC3`–`003D8C1C`).

**`0xA0`** - tail `00460F30` (275 B): two colours `+0x230` (track `+0xC0`) and `+0x234` (track `+0x110`) with the percent
alpha, and **no cull, no release, no spawn**. Its walk builds a GS packet PC never submits (UQ-204), and **no shipped
effect authors it**.

**`0xAB` draws up to four textured fans and one flat fan per element.** Its sub-walk is the `0x68` family's slot
sweep; the packet comes from the builder `0054B3E0` (2,389 B, read whole; its one caller is the sub-walk at `0052CB4D`),
sized by `0054B3A0` as `0x4F0` plus `0x2D0` for the first set slot and `0x2E0` for each further one. It writes a table
of nine 16-byte descriptors and three payload groups into the frame packet arena:

| descriptor | what it carries |
|---|---|
| `+0x00`, `+0x10` | the head of template `02AE9BC0` - the template that installs UQ-213's program `004DA8A0` - and its body `02AE9BE0` by reference (`0054B5A6`–`0054B5DA`) |
| `+0x20` | a default block at `+0x90` (`0x2D0` bytes): template `02AE9EE0` without its first 16 bytes, then `02AE9D50` with its A+D data preset to `0x42` / `0x1001` / `0x45` at `+0x130` / `+0x140` / `+0x150` (`0054B6B8`–`0054B836`) |
| `+0x30`, `+0x40` | the head of template `02AEC4B0` - the one that installs `004CF490` - and its body at `+0x360` (`0x190` bytes) carrying the caller's matrix `[rdx+0x18]`, vector `[rdx]` and float `[rdx+0x10]` (`0054B84C`–`0054B90E`) |
| `+0x50`, `+0x60` | `02AE9BC0` and `02AE9BE0` **again** (`0054B66D`–`0054B695`) |
| `+0x70` | the per-slot blocks from `+0x4F0`, its length patched at the end (`0054BD16`) |
| `+0x80` | an inline closing descriptor of length 0 |

For each of four slots (the walk's owner `+0x30 + i × 0x110`, skipped when the slot's first dword is 0,
`0054B920`–`0054BCF5`) it appends a `02AE9EE0` block and a `02AE9D50` block. The `02AE9EE0` block carries texture terms
from the slot's floats `+0x20` / `+0x24`: `2u − 1`, `2v − 1`, `u`, `v` when slot `+0x28` is set, else fixed 0 / 0.5. The
first set slot omits the block's first 16 bytes, which is the measurer's `0x10` difference. The `02AE9D50` block carries
the slot's vectors and matrix and **five A+D data words from slot `+0xE0`–`+0x104`**. UQ-213 reads that cell as
`CLAMP_1`, `TEX0_1`, `ALPHA_1`, `TEST_1`, `PRIM`, so the walk supplies each fan's texture, blend and primitive.

- **`004CF490`** (flat 4-vertex fans, additive or subtractive) runs once per element, on the caller's matrix block.
- **`004DA8A0`** (a ten-vertex textured fan, `ST` / `RGBAQ` / `XYZF2`) runs once per set slot, up to four.
- Because `02AE9BC0` is uploaded again *after* `02AEC4B0`, the per-slot fans find `004DA8A0`'s own list tag in cell 0.
  This settles the upload order UQ-213 left open for `0xAB`.
- *The default block before `02AEC4B0` carries zero geometry and the preset A+D words; calling it a state primer is
  inference.*

Authored in 3 assets: events `e0065`, `e0066`, magic `m0136`.

**`0xD0` overrides the appearance of chosen characters and the scene.** The apply `00465690` works from the flag word
`+0x232`: bit 0 multiplies the **global scene colour `020926C0`** by colour track `+0x80` × alpha (`0046572C`–`0046578F`);
bits `0x712` select per-character work - a colour (track `+0xD0`, bit 1), two floats (tracks `+0x130`/`+0x120`, bit 4).
The characters are chosen by byte `+0x230` (bounded 9 at `00465867`; table at `00465CA8`), with the action context
`02F97348` (`+8` the acting unit, `+0x10 + 4i` the target handles, `+0x372` their count; `+0x378` bit `0x200` selects the
alternate lists `02096A20` / `02096A24` counted by `02096B24`):

| `+0x230` | arm | characters |
|---|---|---|
| 0 | `00465883` | every character (all four actor managers, any record with a render record) |
| 1 | `004659D8` | the acting unit (`003A3FD0` on the instance's slot byte, per-slot override at context `+0x90`) |
| 2, 7 | `00465B6F` | the second switch `00465B6F`–`00465C53`: mode 2 (`00465B95`) one target when the context has more than one and the instance's `+0x138` bit 2 is set, otherwise every target; mode 7 (`00465C17`) every target |
| 3 | `004659D8` then `00465B6F` | the acting unit, then the targets by the mode-2 rule |
| 4 | `00465A0D` | one participant by index byte `+0x231` through `003A4220`, and nothing more |
| 5 | `00465A25` | the party leader (`PartyFocus_GetCurrentPackedActorHandle`) |
| 6 | `00465A44` | the units the context's four-list sweep marks (`0046B560`, then `0046BA90` / `0046BA50` per list; root records only), or in the alternate mode the `02096AA4` list |
| 8 | `004659D8` then `00465B6F` | the acting unit, then every target |
| 9 | `00465915` | every character except the acting unit, root records only |

Each chosen character goes through `RenderRecord_ApplyPresentationBlendState` `00465CD0` (650 B, read whole) on its
character render record (`022C6F28 + id × 0x740`): the **colour multiplier `+0x220`–`+0x22C`** (`00465D22`–`00465D3D`); the
blend block `+0x4A0` bit 1 with `+0x4A8`–`+0x4B0` and `+0x4A4` bits 0-2 from definition `+0x143` (`00465D43`–`00465E52`); a
two-bit render field through `00428AF0`; **forced local LOD thresholds** (every level at 1000: full detail while the effect
lives, `00465EDB`, `00465F07`); `00428CD0` with byte `+0x235`. The seventh method `00465120` restores each field through
`00465510` (colour back to `1,1,1,1`, `00465552`–`00465570`; LOD override off, `00465625`) and unregisters (`004654DE`).

**Where the blend block goes.** In `00465CD0` the block is `+0x4A0` bit 1 (set when the value `v` is non-zero),
`+0x4A8` = `1 − v`, `+0x4AC` = `v` and `+0x4B0` = `w` (`00465D43`–`00465E27`). Here `v` is float track `+0x120` × the
element's alpha and `w` is float track `+0x130` (`00465825`–`00465840`).
`CharacterRenderRecord_PublishBlendStateToModelInstance` `0041F270` (124 B, read whole) is called from the root and child
LOD-and-presentation updates. It copies the block into the character's model instance: `+0x244` bit 0, the 3-bit
selector from definition `+0x143` into bits 1-3, and `+0x248` / `+0x24C` / `+0x250` (`0041F28A`–`0041F2D2`). The
instance's draw setup `004FD4B0` uses them, read at the cited instructions:
- it multiplies the **ambient alpha of the character's light block by `1 − v`** (`004FD620`–`004FD631`);
- the selector picks a 16-byte entry of the GS state table `02AEECF0` for the draw command (`004FDAA9`–`004FDACC`), and
  selector value 2 switches a second register word (`004FDAD3`–`004FDB12`);
- `w` goes into the command as it stands (`004FDB1C`);
- `v` scales the record's presentation channel 4 into it (`004FDB28`–`004FDB64`).

**What it produces on screen (GI-9, 2026-09-29, FABLE).** `0xD0`'s blend block is a **screen-refraction effect on the
chosen characters** on PC. `0053AB50` passes it to `CharacterRenderObject` slot 24 (`001FA1A0`):
- `refractionPower` = track `+0x130`;
- `refractionAlpha` = track `+0x120` × alpha × presentation channel 4, clamped to 0..2;
- `RefractionSampler`.

The body's own alpha fades by `1 − v` through the ambient term. **The 3-bit selector (definition `+0x143`) only picks the
sampled texture:** 0 is the live scene target; any other value is the front-buffer copy that
`CopyFrontBufferForChrRefraction` (`001F2C50`) makes on request. Shipped effects use 0 (37 definitions) and 1 (8)
([`d0_selector_census.py`](../../_index/candidates/gi-0929-effects/d0_selector_census.py), P1, P2, R1, FAILS 0).

The PS2-shaped packet that `004FD4B0` builds from the same selector goes into the render-command buffer, and nothing in
this executable reads that buffer (CG-6): `TEX0` from the frame-buffer table `02AEECF0`, region `CLAMP`, normal
`ALPHA`, `TEST` Z `GEQUAL`.

**`0xD1` is the effect camera.** The tail `003D92C0` (1,301 B, read whole) opens with the standard element transform
head - translate track `+0x100` into `+0x110` (`003D931F`–`003D93A2`), scale track `+0x140` into `+0x120`
(`003D93CD`–`003D9450`), rotation track `+0x80` into the frame-parity half of a double-buffered camera pair
(`+0x230 + parity × 0x20`, parity `+0x330`, `003D946C`–`003D9491`), the matrix at `+0x290` (`003D949B`), the parent's
transform unless definition `+0x4A` bits 2-4 are set (`003D951B`–`003D9545`), the position history, mode-3 composition and
the scale (`003D9567`–`003D95F0`) - so the camera record's position is the element's composed world position. It then
samples the scalars `+0x320`/`+0x328` (tracks `+0x180`/`+0x190`, `003D9600`–`003D9632`) and the second vector through
`002F3360`, and **publishes the element as the current effect camera `02092628`** (`003D9698`). `00258B90` (472 B) copies it into the camera block `02096FA0` each frame (`00258CC4`–`00258D45`) and clears the
pointer. The release `003D90C0` sets `02092631` / `02092632`, on which `00258B90` **switches cameras 6 and 4 off** through
`CameraSystem_SetCameraActive` (`00258BBE`, `00258BD3`); the birth `003D9040` and the release bracket the field context's
`+0x37A` counter with `002EA8B0` (3, 1 / 0).

**Who authors them** (the dispatch page §2.8 census): `0x40` 2,254 chunks in 687 assets (magic, events, map banks,
models); `0x41` 425 / 280; `0x42` 613 / 295; `0xD0` 1,437 / 447; `0xD1` 765 / 131 (297 event files, 109 magic files); `0xAB`
7 / 3; `0xA0` none.

*Nothing of GI-9 remains open (2026-09-29): the last item, what `0xD0`'s blend selector produces on screen, is
answered above.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `FUN_0031adb0`, owned by that layer, calls `003589B0` on this page. That caller is a 1,790-byte routine with a stack cookie and a `0x80`-byte frame; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**ActorEntity — MECHANICAL (SWE2-CONTRACT 2026-09-15, 79 edges).** All 79 edges are ActorEntity bodies sharing the
page's cited accessors: `00263FF0`/`00358940`/`003589B0`/`003590D0`/`00263C30`/`002E9B80` are the
actor-record getters and handle codecs the element steps use, and 66 ActorEntity neighbours
(`ActorResource_FinalizeManagerRuntimeAfterLoads`, `ActorResource_AllocateAndSubmitEntry`,
`ActorManager_RunFieldRuntimePass`, `ActorEntity.ManagerPopulationFiltering` `0046BAC0`,
`003B6F80`, `0035A990`, `0035A590`, `0035A7A0`, `003DB1F0`, `00264010`, `00268D10`, `00264050`,
`ActorHandle_ResolveRegistryEntryByPackedId`, …) call the same six. Element steps resolve their
host actor through the same accessors the whole entity layer uses — fan-in, not a second owner.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 25 edges).** 19 edges are the `0020E600`/`0020E620`
image-pointer pair inside the step bodies; 4 are `001EDDA0` via `002F2530`/`003D92C0`/`005269B0`/
`00528AF0`; the last two are `00265860`/`00265880` reaching `001EDDA0`.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 17 edges).** All caller fan-in: `00392740` shares `00263FF0`/
`00358940`; `Movement.CharacterPresentation.BindingInitialization` `002E28E0` shares `00263FF0`;
`002EBFA0`/`Movement_IntegratePositionAndMeasureDisplacement` share `003589B0`; ten movement bodies
(`Movement_UpdateSteeringTowardTarget`, `BattleUnit_CanAdvanceCombatNavigation`, `0026C3E0`,
`0026D810`, `00345430`, `00319490`, `002E5180`, `00326BB0`, …) share `003590D0`; `001EDDA0` is shared
with `WorldActor_UpdateRuntimeAndScriptExecutionState`.

**Party — MECHANICAL (SWE2-CONTRACT 2026-09-15, 12 edges).** `PartyRoster_AssignActorToSlot` shares `003589B0`/
`003590D0` (2 edges); `PartyFocus_EncodeActorAndSetTemporaryControlledActorOverride`,
`VMPartyCommand_SetSecondaryFocusActorFromActorIndex`, `PartyFocus_SelectAndRequestDefaultActor`,
`PartyRoster_AssignActorAndCommitFocusWhenEligible` share `003589B0`; `PartyFocus_IsCurrentPackedActorHandle`,
`00327270`, `BattleUnit_GetPartyLeader`, `003272F0`, `PartyRoster_GetActorBySlotOrCurrentFocus` share
`003590D0`; `00465120` calls `PartyFocus_GetCurrentPackedActorHandle`. Shared accessor fan-in.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 5 edges).** Audio bodies share the cited helpers; no audio
relationship to these element types.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (118 edges).** `00263C30`, `00263FF0`, `00264010`, `00264050` (+10 more) are called by bodies filed to Script_VM_Native_Bridge: WorldActorScriptVM_InterpretBytecode (`0025E4C0`), VMNativeCommand_ExecuteLifecycle (`002621D0`), ScriptVM_WaitList_HasAnyActorChannelActive (`00267420`), ScriptVM_WaitList_HasAnyActorResourceEntryActive (`002674B0`) (+101 more); `00345430` reaches bodies filed to Script_VM_Native_Bridge: VMValueStack_PopNumericDiscard (`00267DB0`), VMValueStack_PushFloat32Bits (`00267F60`) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (6 edges).** `002E5180`, ActorManager_GetRecordByOrdinal (`00358940`), PartyFocus_GetCurrentPackedActorHandle (`003590D0`) are called by bodies filed to World: `0025E400`, `002623A0` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (7 edges).** `00392740`, `003ABCA0`, `003DB1F0` are called by bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`), World_UpdateSimulationTick (`00314020`), `00378230`; `00268D10`, `0026C3E0`, `002E28E0` reach bodies filed to WorldAreaField: `00377700`, FieldData_GetActiveFieldRecordBit15 (`00377C20`) - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - SERVICE and MECHANICAL (5 edges).** `00234590` reaches `BattlePerception_AdvanceCandidateCacheGeneration` (`00325060`) and `BattlePerception_ResetSpatialVisibilityCacheFrameState` (`0032A650`); three AI bodies (`003014C0`, `00301AD0`, `00305AB0`) call `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **CombatFormula - MECHANICAL (1 edge).** `BattleStats_ModifyHPAndProcessLethalState` (`00300530`) calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **InputGameplay - SERVICE and MECHANICAL (2 edges).** `00234590` reaches `00313A00`; `00313A00` also calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`).
- **Items_Equipment_Shops_License - MECHANICAL (2 edges).** both edges are item bodies (`Inventory_QueryOwnedCountIncludingReservedActionItems` `00309FB0`, `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10`) calling `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.
- **Spawn_Encounter_Lifecycle - SERVICE (1 edge).** `00234590` reaches `SpawnGroup_DispatchPendingCompletionSignals` (`00307030`).
- **Status_Periodic_Terminal - SERVICE and MECHANICAL (4 edges).** `00234590` reaches `BattleUnit_ResetActionControlForStatusTransition` (`00300140`); three status bodies (`0030E360`, `0030F690`, `00310DB0`) call `FieldData_GetActiveFieldRecordBit15` (`00377C20`) - accessor fan-in.

## Interior read — frontier hub `0024E460` (2026-09-17, SWE2-EC7) — evidence only

`0024E460` — 79 B, 27 frontier callers at census. Read against the shipping image (page is
PARTIAL — no disposition claimed): a capability probe. `00862C40` fills a two-dword out-record on
the stack; when that answers zero it consults `dword [02F97340]` — if the global is non-null and
`byte [g] == 7`, it returns `1` iff `word [g+4] - 0x240 <= 0x133` (a `0x240..0x373` id window).
Pure predicate; no writes escape.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 3): the layers pass 22 still reported for this page. Every edge was listed in full and each cited body was read.*

**Script_VM_Native_Bridge — MECHANICAL (64 edges).** The script layer calls five small actor accessors that this page's element handlers also use. `00263FF0` returns the address of actor-manager slot `idx` (stride `0x288`). `00263C30` returns that slot's dword at `+0x20` when bit 0 of its `+0x10` is set, else 0. `ActorManager_GetRecordByOrdinal` (`00358940`) does a bounds-checked index into a manager's record array. `ActorHandle_EncodeRegistryEntry` (`003589B0`) packs a record's `+0x16` low 11 bits, `+0x15` low nibble and `+0` word into a handle. `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) returns one global dword. The 58 distinct callers are the interpreter `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), `VMNativeCommand_ExecuteLifecycle` (`002621D0`) and 56 other script-layer bodies, mostly verb handlers (`0033F7F0` to `0050E060`), each resolving the actor the script acts on. They are shared accessors: no script state reaches an effect element through them.

**World — MECHANICAL (4 edges).** `0025E400` and `002623A0` call `00358940` and `003590D0`, the same record lookup and party-focus handle read. They share the accessors and nothing else.

**WorldAreaField — MECHANICAL (1 edge).** `00378230` walks three handle dwords and passes each non-zero one to `003ABCA0` (`00378437`–`0037843D`). That routine finds the node with that handle in a linked list, clears it, decrements the list count and unlinks it. It is the light removal this page's `00464050` uses on `+0x244` (FABLE, GI-9). The field body releases its own lights through the same call.
