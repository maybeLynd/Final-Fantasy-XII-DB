---
system: the element types 0x00-0x0A
category: 17-Presentation-Rendering
status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-14 answered 2026-10-01 (OPUS, static - the six tail helpers, the line emitter and the blend value's consumer read, see the GI-14 section; review requested from SWE2-AUDIT-SEM). History: PARTIAL on GI-14 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930). GI-8 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS, ACCEPT, d998217e2). Was PARTIAL on: seven of the ten walks (the draws) are not read, so what those types look like on screen is not established; 0x01 is a point, 0x02 a sprite and 0x03 a line (2026-09-19); the update side (all ten tails, the cull test, the release, the child-spawn slots) is read whole and has its own page, an-effect-element-frame-by-frame"
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
  falsification_result: six defect classes in REVIEW-effect-types-00-0a (REJECT), repaired d177d73c
  crossref_clean: true
  reopened_count: 0
---

# Element types `0x00`–`0x0A` — the base element and the first derived types

Package: `FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES` (group 1 of N — `0x01`–`0x07`+base).
Coordinates: `members/effect-type-methods.tsv`; dispatcher architecture:
[effect-element-type-dispatch](effect-element-type-dispatch.md). Evidence class
**NATIVE/STATIC** throughout; authority EXE `73461D08…21F8`. Every row below was read
from the shipped body, not inferred from the table.

## 1. The method vocabulary

Reading the group shows all ten types share one architecture — the dispatch byte
selects a *variant*, not an independent implementation:

- **`step` is base + tail.** Every derived step calls the type-`0x00` stepper
  `002F2D60` (1111 B) first, then a type-specific tail helper (`00442600` for
  `0x01`, `004428F0` for `0x03`, `0044B3C0` for `0x08`, `00449560`/`0044A180`/
  `00447830`/`00448800` for `0x02`/`0x05`/`0x06`/`0x07`, `0044C850`+`0044B960`
  for `0x0A`) — and in the 0x04/0x05/0x06/0x07 steps the tail is followed by
  extra helper work. All steps are 43–310 B **except `0x02`'s `00448DE0`
  (739 B)**. ~~The tail helpers `00442600`, `004428F0`, `0044B3C0`, `00449560`,
  `00447830` and `00448800` were not instruction-read this pass — registered as
  **GI-14**.~~ *(Read 2026-10-01, OPUS - the GI-14 section at the end of this page.)* (`0044A180` and `0044C850` are the shared `0x05`/`0x0A` tails, read
  2026-09-29 under GI-11, groups B1 and A5.)
- **`update` is base + same tail.** Every derived update is exactly 56 B **except
  `0x02`'s `00448D70` (103 B)**: call the type-`0x00` update `002F2530` (2094 B —
  the frame-advance the dispatch page already names), then the *same* tail helper
  the step uses. Step and update therefore share each type's per-frame tail; they
  differ in the base phase they bracket.
- **`setup` is base + a per-type record map.** All setups call the type-`0x00`
  setup `00500470` first, then rebase the element record's encoded pointers with
  three helpers (§2). The **number and placement of rebase calls is the per-type
  record layout** — the definition record is pointer-rich authored data.
- **`walk` is a transform-workbench user.** Each walk (173–3483 B) composes the
  element's transform through the shared workbench (`0026EE00` — a
  colour-modulate `min(255, (a·b)>>7)` body whose *callee* wraps it in the
  workbench save/restore pair; `002F1F40` primitive, `0039AF70`
  SetWorkbenchMatrix family, `0039B620`) and
  evaluates authored tracks with `004314E0` (the authored-number evaluator) before
  emitting type-specific draw state.
- Type `0x00` has **no `walk`** (table row `-`): the base element steps and updates
  but emits nothing itself.

## 2. The setup helpers — element-record field kinds

All four rebase helpers resolve stored dword offsets through
`ImageAddress_ResolveRuntimePointer` (`0020E600`), add the definition-record base in
`edx`, and re-encode with `RuntimePointer_EncodeImageAddress` (`0020E620`). The
authored record therefore stores **image-relative offsets** that setup converts to
runtime pointers.

| helper | span | role (read from body) |
|---|---|---|
| `004304F0` | one head, returns `rcx+0x10` | rebase one **track head** = the pair `{encPtrA @+0, encPtrB @+4}`; head is 0x10 bytes `{ptrA, ptrB, …, countA @+0xC, countB @+0xD}` |
| `00430AF0` | three heads, returns `rcx+0x40` | rebase a **track group** = 3 heads at `+0`/`+0x10`/`+0x20` of a 0x40-byte block |
| `0042FCF0` | four heads | rebase a **four-track group** (heads at `+0`/`+0x10`/`+0x20`/`+0x30`) |
| `00431040` | group | float-scale all three tracks of a group by `xmm1` via `00430A60` |
| `00430A60` | head | scale one keyframe array: resolves `+0`, multiplies each 8-byte entry's `+4` float by `xmm1`, entry count = byte `+0xC`; then the same for `+4`/byte `+0xD`. **So each track head owns two 8-byte-record keyframe arrays (`{u32, f32}` entries)** |
| `00431580` | head | same loop with integer `imul` — scale int keyframes by `edx` (type `0x03` passes `0x64`) |
| `00431770` | head | ~~same shape, third variant — `not read` further~~ *read 2026-09-19: not an init variant but the rebase of a `0xF0`-byte track bundle; see the dated section* |
| `003AA280` + `0020E620` | — | resolve one authored pointer and store a resource handle into the element (two stores in `0x02`/`0x08`/`0x0A`, one at `+0x5A0` in `0x05`) |

## 3. Per-type rows

Legend for the setup column: `4G` = four-head group (`0042FCF0`), `3G` = three-head
group (`00430AF0`), `1T` = single track head (`004304F0`), `RS` = resource store
(`003AA280`+`0020E620`), `×f` = `00431040` float scale, `×i` = `00431580` int scale.

### Type `0x00` — the base element

| method | address | what it does |
|---|---|---|
| setup | `00500470` | rebases **four** single track heads at element `+0x00`, `+0x10`, `+0x20`, `+0x30` and returns `element+0x80` — the base record opens with four scalar tracks (`+0x00`–`+0x3F`) and derived-type groups begin at `+0x80` |
| step | `002F2D60` | the base stepper (1111 B): touches `+0x10`…`+0x4C` including the `+0x3C` frame counter; calls `00250010`, `00398F90` (point transform), `0039AF70` (SetWorkbenchMatrix), `003A8240`, `003A8950`, `004314E0`, `00432300`, `00441EA0` |
| update | `002F2530` | the base frame-advance (2094 B): touches `+0x10`…`+0x4C`; calls seventh-method base `002F31C0`, `002F3750`, `002F3890`, `003A2900`, `003A2B20` |
| walk | — | none (table `-`) |

### Type `0x01`

setup `00538A60` = base + `4G@+0x80` + `1T@+0xD0`. Adds one four-track group and one
scalar track to the base record.

| method | address | what it does |
|---|---|---|
| step | `00442520` | base stepper + tail `00442600` (GI-14) |
| update | `004424E0` | base advance + same tail `00442600` |
| walk | `00442550` | resolves a workbench slot from element `+0x244` (`0039B620`), writes `1.0f` to element `+0x23C`, runs transform primitive `002F1F40` on the `+0x230` matrix field, and calls `0026EE00` (the colour-modulate body wrapped internally in the bank save/restore); evaluates the record `+0x30` track with `004314E0` and stores the result to global `02AEE908`; stores record `+0x49 >> 5` to global dword `02AEE900`; copies the `+0x230` row to the stack and emits via `0039C550` |

### Type `0x02`

setup `00538AB0` = base + `4G@+0x80` + `3G@+0xD0` + `3G@+0x110` + `1T@+0x150` +
`1T@+0x170` + **two** `RS` + `4G@+0x190`. Largest low-type record: two authored
resources plus ~13 tracks.

| method | address | what it does |
|---|---|---|
| step | `00448DE0` | 739 B own body: base + tail `00449560` run **first** (`00448E1D`), then the `003A6E60`/`0020E600` work follows; touches `+0x10`…`+0x18C`; also calls `001EDDA0`, `00314960` |
| update | `00448D70` | base advance + tail `00449560`; also touches `+0x180`, `+0x2A1` |
| walk | `004490D0` | 1157 B; workbench compose plus `003992B0`, `0039B550` (second transform primitive path), `003A3D00` |

### Type `0x03`

setup `00538B80` = base + `3G@+0x80` + `3G@+0xC0` + `3G@+0x100` + `3G@+0x140` +
`1T@+0x180` + `4G@+0x190` + `4G@+0x1E0`, then **unit conversion at load**: three
groups (`+0x80`/`+0x100`/`+0x140`) float-scaled by image constants and `+0x180`
int-scaled by `0x64`. The authored data for this type is stored in units the runtime
rescales — the only low type that does.

| method | address | what it does |
|---|---|---|
| step | `004427A0` | base + tail `004428F0` (GI-14) |
| update | `00442760` | base + tail `004428F0` |
| walk | `004427D0` | 277 B; workbench compose (`0026EE00`, `002F1F40`, `0039B620`, `004314E0`) + `0039C4C0` and import-side `00808C40`; touches `+0x68`–`+0x70` and `+0x230`–`+0x254` |

### Type `0x04`

setup `00538C80` = base + `3G@+0x80` + `3G@+0xC0` + `3G@+0x100` + **seven** `1T`
`+0x140`–`+0x1A0` + `4G@+0x1B0` + `4G@+0x200` + `4G@+0x250` + `1T@+0x2A0` + a
**4-iteration `00431770` loop** at `+0x2B0`, stride `0xF0` (`+0x2B0`/`+0x3A0`/
`+0x490`/`+0x580`).

| method | address | what it does |
|---|---|---|
| step | `00445310` | 177 B; base + tail `00445B50`, then a 4-iteration loop of conditional `003D8E50` calls (`00445348`–`004453A2`) |
| update | `004452D0` | base + tail `00445B50` |
| walk | `004453D0` | 1914 B; full workbench chain — `00398030`, `00399110`, `00399B80`, `0039A150`, `0039AF70`, `0039B550` |

### Type `0x05`

setup `00538DB0` = base + `4G@+0x80` + `3G@+0xD0` + `3G@+0x110` + `3G@+0x150` +
`1T@+0x190` + `1T@+0x1A0` + a **4-iteration `00431770` loop** at `+0x1B0` +
`RS@+0x5A0` — the record ~~reaches `+0x5A0`, the largest of the group~~ ends at `+0x620`, and types `0x06`/`0x07`'s at `+0x6E0` is larger *(corrected 2026-10-02, OPUS: `00538DB0`+0xE7 `lea rax, [rbp + 0x620]`; `00538EB0`+0x15E `lea rax, [rbp + 0x6e0]`)*. Its walk's helper set (`00394B70`–`00396F20`, `0039E6B0`–`0039F9F0`,
`00432300`, `00432CC0`) is already identified by
[the ee-and-vu0-register-bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md)
§"effect element type 5's walker helpers" as **translated MMI / VU0 loops over ACC
and the vector rows** — this type's geometry runs on the emulated VU0 path.

| method | address | what it does |
|---|---|---|
| step | `00449970` | 310 B; base + tail `0044A180` first (`004499AA`), then `003D8E50`×2, `003A6E60`, `0020E600`×3; touches `+0x278`–`+0x5A0` |
| update | `00449930` | base + tail `0044A180` |
| walk | `00449AB0` | 1741 B; workbench compose + `0017FFD0`, `0024E640`, `0042FDB0`, `004309C0` + the VU0/MMI helper family above |

### Types `0x06` / `0x07` — shared setup, distinct tails

Both use setup `00538EB0` (373 B) = base + `3G@+0x80` + `3G@+0xC0` + `3G@+0x100` +
**fourteen** `1T` `+0x140`–`+0x210` + `4G@+0x220` + `4G@+0x270` + `4G@+0x2C0` +
a **4-iteration `00431770` loop** at `+0x310`, stride `0xF0` (`+0x310`/`+0x400`/
`+0x4F0`/`+0x5E0`). Same record layout → variants of one element class; they
differ only in step/walk tails.

| type | step | update | walk |
|---|---|---|---|
| `0x06` | `00446F60` (177 B; base + tail `00447830`, then a 4-iteration conditional `003D8E50` loop — same shape as `0x04`'s step) | `00446F20` (base + `00447830`) | `00447020` (2062 B; `00398030`/`00399110`/`00399B80`/`0039A150`/`0039AF70`/`0039B550` chain) |
| `0x07` | `00447E10` (same shape, tail `00448800` + `003D8E50` loop) | `00447DD0` (base + `00448800`) | `00447ED0` (2350 B; same workbench family + `+0x34`/`+0x4A` extra fields) |

### Type `0x08`

setup `00539030` = base + **nine** `3G` `+0x80`–`+0x280` + `1T@+0x2C0`–`+0x2E0` +
`4G@+0x2F0` + `4G@+0x340` + `4G@+0x390` + `4G@+0x3E0` + two `RS`. The most
track-dense low type.

| method | address | what it does |
|---|---|---|
| step | `0044A5F0` | base + tail `0044B3C0` (GI-14) |
| update | `0044A5B0` | base + tail `0044B3C0` |
| walk | `0044A620` | 3483 B — largest low-type walk; uses bank writers `003697F0`, `0036A190`, `0036DD80` (one of only three `vf00` writers, per the register-bank page) + `00397ED0`, `00398480` |

### Type `0x0A`

setup `00539170` = base + five `3G` `+0x80`–`+0x180` + `1T@+0x1C0` + `4G@+0x1D0` +
`4G@+0x220` + `1T@+0x270` + `1T@+0x290` + two `RS`.

| method | address | what it does |
|---|---|---|
| step | `0044BA80` | 54 B; base + shared tail `0044C850`, then step-only `0044B960` whose return goes to `+0x458` (in `0044BA80`'s tail) |
| update | `0044BA40` | base + tail `0044C850` (the step's extra `0044B960` is step-only) |
| walk | `0044BAC0` | 3461 B; uses the bank **save/restore pair `0036D930`/`0036D8E0`** plus `0036DD80` (`vf00`), `0036D8E0`, `003A2B20`, `0039B620` |

## 4. What this group establishes — and what it does not

**Established (NATIVE/STATIC, cited bodies):**

- Type `0x00` is the base class: it owns the shared stepper `002F2D60`, frame
  advance `002F2530`, and setup `00500470`; it emits nothing (no walk).
- The element record opens with **four base track heads** at `+0x00`–`+0x3F`
  (0x10 each: two keyframe-array pointers + two counts) — the stepper's
  `+0x10`–`+0x4C` field span *is* this head array plus the fields just past it —
  then a per-type tail of heads arranged in 0x40 three-track and four-track
  groups from `+0x80`; setup rebases every pointer pair against the
  definition-record base.
- Types are record-layout variants: `0x06`/`0x07` share one setup; `0x03` is the
  only low type that unit-scales authored data at load; `0x08` is the most
  track-dense; `0x02`/`0x05`/`0x08`/`0x0A` carry authored resource handles.
- Type `0x05`'s walk runs the translated VU0/MMI helper family (already bank-cited).

## The update side moved to its own page (2026-09-19, FABLE)

All ~~ten~~ nine step/update tails and the shared helper `0044B960` *(corrected 2026-10-02, OPUS: CON-179 on an-effect-element-frame-by-frame.md; `0044B960` has 48 call sites)*, the cull test, the release and the child-spawn slots were read whole and are described on
[an effect element, frame by frame](an-effect-element-frame-by-frame.md). This page keeps the method matrix, the
setups and the walks.

**`00431770` (177 B) is not a third init variant; it is a rebase.** Given a `0xF0`-byte track bundle and the load base,
it rebases the bundle's two sub-tracks (`+0x00`, `+0x40`) through their own rebase routines, adds the base to the four
encoded pointers at `+0x90`, `+0x94`, `+0xE0` and `+0xE4` (resolve, add, re-encode), clears byte `+0xA9` unless bits 4-5
of `+0xAA` are set, runs a finishing routine, and **returns the address of the next bundle** - which is why the setups
call it four times in a row.

| body | anchors |
|---|---|
| `00431770` bundle rebase (177 B) | `0043177F`, `0043178A`, `0043179A`, `004317B4`, `004317CE`, `004317E8`, `004317F7`, `0043180A`, `00431814` |

## Two walks traced to the render command, 2026-09-19 (FABLE): `0x01` is a point, `0x03` is a line

**Type `0x03`'s walk `004427D0` (277 B, read whole)** - type `0x01`'s `00442550` was read whole on
[the distance-fade node's page](../Position-To-Scalar/how-a-position-becomes-a-single-number.md), section 13, and has
the same shape with one end. Skipped when the element's first byte is zero. It adds the element's texture-frame
integer (`+0x258`) to a base and publishes the sum as the current texture index (a 13-byte helper), sets `w` = 1.0 on both
points, **publishes two globals for the emitter - `02AEE900` := definition byte `+0x49 >> 5`, `02AEE908` := the value of
the definition's `+0x30` track at the element's time** - asks the distance-fade node once per end, multiplies each
result into that end's colour (`+0x250`, `+0x254`), and calls `0039C4C0(point 1, point 2, colour 1, colour 2)`.

**The emit front ends `0039C550` (121 B, one point) and `0039C4C0` (134 B, two points), read whole.** Select the
projection matrix `02AEECB0`, project-and-clip each point - **a line is dropped whole if either end is rejected** - then
choose one of two emitters on `02AEE900`.

*Where in the frame these draws happen - six layer requests, named by the engine's own markers - is on
[the six VFX display layers](the-six-vfx-display-layers.md).*

**What is emitted is a `GiPrim` command** ([the Gi render command family](../Gi-Render-Commands/gi-render-command-family.md)):
its constructor `008642A0` (133 B, read whole) allocates the `0x68`-byte record for `n` vertices and returns the
record `+ 8`. The emitters write the projected positions through a vertex writer, **each colour as four floats**
(bytes converted, not normalised) into the record's colour array, and the **primitive kind** at record `+0x48` - the
index the `GiPrim` draw looks up in its topology table `01F44D20` (`0, 1, 6, 2, 3, 4, ...`):

| type | vertices | kind | so |
|---|---:|---:|---|
| `0x01` | 1 | 0 | **a point** |
| `0x03` | 2 | 1 | **a line** - and with mode 2 of its second point ([frame by frame](an-effect-element-frame-by-frame.md), section 2), a streak behind a moving point |

*The kind numbering matches the PS2 GS primitive codes (0 point, 1 line, 2 line strip, 3 triangle ...) and the table is
then the map to the PC renderer's topology enum. That is a reading of six table values, not of the renderer.*

**`02AEE900` - definition byte `+0x49`, bits 5-7 - is a blend mode.**

| mode | emitter | what it does |
|---|---|---|
| 0 | `0039D890` (point, 224 B), `0039D5A0` (line, 286 B), both read whole | builds the primitive on the current command list and submits it at once; the point emitter also clears record `+0x58`, which the constructor sets to 1 |
| 1-7 | `0039D970` (point, 348 B, read whole); ~~the line's `0039D6C0` (457 B) **not read (GI-14)**~~ the line's `0039D6C0` (457 B, read 2026-10-01 by OPUS - the GI-14 section) | first **appends a `0x28`-byte entry to the depth-sorted display list** (`[02F8F2F8]`, count word `02F8F2C6` - the Gi page's section 11): callback and argument null, its own command list at `+0x18`, **sort key `+8` := the projected point's third word (after the x and y words the cull test reads - so depth, by position), with the pass nibble `02AEE910` or-ed into bits 28-31**, a flag dword at `+0x20` from three predicates not read. Then the primitive, with record `+0x4C` := 1 and **record `+0x38` := a blend value** |

The blend value is `01EFAC20[mode]`, eight qwords: `0x44`, `0x48`, `0x42`, `0x44`, `0x49`, `0x46`, then two values that
do not look like members (`0x80000000A8`, `4`). **Mode 6 does not use the table: it takes `02AEE908`, the `+0x30` track
value** - an authored, animatable blend value. *The table values have the layout of a PS2 GS `ALPHA` register -
`0x44` = (Cs - Cd) x As + Cd, normal; `0x48` = Cs x As + Cd, additive; `0x42` = Cd - Cs x As, subtractive; `0x49` = Cd x As
+ Cd; `0x46` = Cd x (1 - As) - **an inference from the encoding; ~~the consumer of record `+0x38` was not read (GI-14)~~ ~~the value sits at the GiPrim command's `+0x30` and GiPrim hands it to its render context's vtable `+0x40` - the GI-14 section, corrected 2026-10-01, OPUS~~ record `+0x38` is right: `GiPrim` translates it through the GS ALPHA translator `001EE650` - the GI-14 section, re-corrected 2026-10-01, OPUS**, and mode
7 indexes past the six plausible entries.*

**This explains a threshold in the tails.** They apply the `+0x30` percent track to alpha only when definition `+0x49`
is `0x20` or more - that is, only in a non-zero blend mode, where alpha matters. (In mode 6 the same track is both the
alpha percent and the blend value; whether any shipped effect uses mode 6 was not checked.)

| body | anchors |
|---|---|
| `004427D0` type `0x03` walk (277 B) | `004427E5`, `00442805`, `00442825`, `00442840`, `0044284A`, `00442850`, `00442864`, `0044287A`, `00442890`, `004428C3` |
| `0039C4C0` two-point emit front end (134 B) | `0039C4EB`, `0039C4F8`, `0039C509`, `0039C512`, `0039C524`, `0039C52B` |
| `0039D890` point emitter, mode 0 (224 B) | `0039D8B9`, `0039D8C9`, `0039D8DF`, `0039D8E2`, `0039D93B`, `0039D93F`, `0039D943`, `0039D94E` |
| `0039D5A0` line emitter, mode 0 (286 B) | `0039D5BB`, `0039D5CB`, `0039D5DF`, `0039D690`, `0039D694`, `0039D69C`, `0039D6A9` |
| `0039D970` point emitter, blended (348 B) | `0039D986`, `0039D990`, `0039D9A4`, `0039D9B5`, `0039D9BE`, `0039D9D6`, `0039D9F1`, `0039DA05`, `0039DA0C`, `0039DA24`, `0039DA7A`, `0039DA82`, `0039DA89`, `0039DA90`, `0039DA9E`, `0039DAAC`, `0039DAB0` |
| `008642A0` `GiPrim` constructor (133 B) | `008642C5`, `008642CA`, `008642D4`, `008642F3`, `008642F8`, `008642FC` |

## Type `0x02`'s walk, read 2026-09-19 (FABLE): a sprite

**`004490D0` (1,157 B, read whole) draws nothing itself.** It fills a **draw request** - a block at `[01FD4A78] + 0x800` -
and hands it, with a resource, to a frame drawer. Skipped when the element's first byte or definition byte `+0x184` is
zero.

1. **Facing along screen motion - definition word `+0x180`, bit 5.** It projects two points through `02AEECB0` - the
   position `+0x270`, and the position plus the element's vector `+0xB0` - and takes the difference of their screen x and
   y words. **When `|dx| + |dy|` is under 10 the last angle (`+0x288`) is reused**; otherwise the angle is
   `-atan2(dy, dx)`, stored as the rotation's z (`+0x118`) and as the new last angle. *This is why the tail skips the
   rotation track on the same bit.*
2. **Colour.** The distance-fade node at the position, multiplied with the element's colour `+0x280`, written straight
   into the request. **If the resulting alpha byte is zero nothing is drawn.**
3. **The request.**

   | request field | from |
   |---|---|
   | `+0x38` matrix pointer | the element's matrix `+0x230`, in orientation mode 0 |
   | `+0x00` position | the element's position, in any other mode |
   | `+0x10`, `+0x20` | scale `+0x120`, rotation `+0x110` |
   | `+0x40` | the colour of step 2 |
   | `+0x46` bit 0 | definition `+0x4A` bit 2 - the drawer then builds the matrix itself from position, rotation z and scale, against the view |
   | `+0x46` bits 1-3 | the blend mode, definition `+0x49` bits 5-7 |
   | `+0x46` bits 4, 5 | the element's bytes `+0x28E`, `+0x28F` - **mirror x, mirror y** |
   | `+0x46` bit 6 | definition word `+0x180` bit 13 |
   | `+0x47` | definition byte `+0x48`, the rotation order |
   | `+0x44` frame, `+0x30` offset | see 5 |

4. Unless the blend mode is 6 it publishes `02AEE900` / `02AEE908` exactly as the walks of `0x01` and `0x03` do.
5. **Which frame.** With definition byte `+0x160` set there is an **animation bundle**: the resource of definition
   `+0x188` is resolved, asked for its table, and the bundle is sampled at the element's time - the high half of the
   result is a frame index handed to the animated drawer; a failed lookup skips the draw.
   - **By number (`+0x185` zero):** the frame word is `age / 2` when definition word `+0x180` has bit 11, else 0, **plus the
     element's byte `+0x290`** unless that is `0xFF`. The plain drawer is bracketed by a state call taking definition byte
     `+0x74` and then 0. **When bit 2 of `+0x180` is set, bit 3 clear, and the drawer returns 0, the element is released** -
     a one-shot sprite animation that ends the element when it runs out of frames.
   - **By name (`+0x185` non-zero):** a lookup in a second resource (definition `+0x18C`) with the string at element
     `+0x2A0`; the entry gives the frame word (`+0xA`) and two offset dwords (`+0`, `+4`). **A name that is not found
     releases the element.**

**What a frame is - from the first half of the plain drawer (1,793 B; its first `0x340` bytes read, the rest skimmed for
calls, so it is not anchored here).** The frame number selects an entry; the drawer then loops over **parts**, each
with four corner vectors (to which the request's offset is added), a colour multiplied with the request's, four
texture-coordinate qwords, texture page bytes, and a flag byte whose low bits end the list. Request flag `0x10` negates
the corners' x. Each part goes out through quad emit front ends that sit beside the point and line ones. **So type
`0x02` is a sprite: one frame of a multi-part sprite sheet**, either placed by the element's matrix or built facing the
view.

| body | anchors |
|---|---|
| `004490D0` type `0x02` walk (1,157 B) | `0044910B`, `0044911C`, `00449129`, `0044915E`, `004491CA`, `004491D9`, `004491EA`, `0044921B`, `00449220`, `0044923D`, `00449249`, `00449259`, `00449273`, `00449288`, `0044928D`, `00449298`, `004492AD`, `004492BE`, `004492F8`, `0044930B`, `0044931F`, `00449326`, `0044933D`, `0044935D`, `0044936A`, `0044937E`, `00449395`, `004493C1`, `004493D6`, `004493E8`, `00449401`, `00449444`, `00449455`, `0044947B`, `00449489`, `004494AA`, `004494B1`, `004494C6`, `004494D3`, `00449506`, `0044951B` |

**Not read (explicit):** ~~every step/update tail helper~~ *(all ten read 2026-09-19 - [an effect element, frame by frame](an-effect-element-frame-by-frame.md))*;
~~**every walk except those of `0x01`, `0x02` and `0x03`** - and the sprite frame drawers the `0x02` walk calls - the draws, where what a type looks like is decided;~~ *(every walk read 2026-09-29 - [what every walk draws](#what-every-walk-draws-and-who-authors-it-gi-8-2026-09-29-fable))*; the blended line
emitter ~~`0039D6C0`~~ *(answered: see the GI-14 section - read 2026-10-01; 2026-10-02, OPUS)*;
~~`00431770`;~~ `003AA280`'s internals; ~~`0039C550`, `0039C4C0`,~~ `003992B0`,
`00398030`, `00399110`, `00399B80`, `0039A150`, `003697F0`, `0036A190`,
`00397ED0`, `00398480`, `003A3D00`, `003A2B20`, `0017FFD0`, `0024E640`,
`0042FDB0`, `004309C0`, `003A6E60`, `003D8E50`, `001EDBB0`, `001EDDA0`,
`00250010`, `003A8240`, ~~`003A8950`~~, ~~`00432300`~~ *(answered: see effect-mesh-records-kind-54.md §8 - the PS2 colour modulate; 2026-10-02, OPUS)*, `00441EA0`, `002F3750`,
`002F3890`, `003A2900`, `00808C40`. ~~**Player-facing names: three primitive names only (`0x01` a point, `0x02` a sprite, `0x03` a line), none from authored data** — no
EFX data or caller evidence read this pass names any of these types; naming needs
the emit calls (`0039C550` family) traced to draw-list ops or EFX records.~~ **Answered 2026-09-29 (FABLE, GI-8):** every
type of the band now has its primitive, its shape and its authored usage - [what every walk draws](#what-every-walk-draws-and-who-authors-it-gi-8-2026-09-29-fable).

**Globals written:** `02AEE900` (mode/flag dword from record `+0x49 >> 5`) and
`02AEE908` (track-eval result qword) by type-`0x01` walk — draw-state args,
~~unconfirmed consumers~~ *(answered: see the walks of `0x01` and `0x03` above - mode 6 takes `02AEE908`, the others `02AEE900` chooses an emitter; 2026-10-02, OPUS)*.

## What every walk draws, and who authors it (GI-8, 2026-09-29, FABLE)

*Static reads of the shipping image (`73461D08…21F8`) plus an authored-data census; nothing executed. Reader: FABLE
(Claude Opus 5.5). The primitive class of each type was already on [UQ-204's table](../../_index/candidates/uq204-element-type-emits/README.md);
this section adds the shapes, the fields that drive them, and who uses each type. `0x05`'s walk `00449AB0` is read on
[the dispatch page](effect-element-type-dispatch.md). Checks: [`type_census.py`](members/type_census.py) (C1-C7, FAILS 0) and [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py) (K1-K18, FAILS 0).*

| type | primitive | on screen | authored: chunks / distinct assets |
|---|---|---|---:|
| `0x00` | none (no walk) | the base element: moves and spawns children, draws nothing | 1,446 / 400 |
| `0x01` | GiPrim kind 0 | a **point** | 476 / 244 |
| `0x02` | frame drawers `00501A50` / `00502280` | a **sprite** (one frame of a multi-part sheet) | 7,523 / 1,007 |
| `0x03` | GiPrim kind 1 | a **line / streak** | **0** |
| `0x04` | quad grid (`004434D0` / `00444340`) | a **ring or cone band** | 173 / 81 |
| `0x05` | model composer `004355D0` | a **resource mesh** | 5,204 / 323 |
| `0x06` | quad grid | a **column or vortex** | 25 / 7 |
| `0x07` | quad grid | a **dome or sphere** | **0** |
| `0x08` | GiPrim kind 4 quads, or one sprite frame over the grid | a **waving sheet** | **0** |
| `0x0A` | frame drawers (as `0x02`) | a **sprite trail** | 40 / 37 |

**`0x04` - `004453D0` (1,914 B, read whole): a ring or cone band.** Three concentric rings of `n + 1` vertices
(`n` = `+0x254`), each vertex `(sin θ·R, Y, cos θ·R)` with `θ` stepping `+0x240 / n`: ring 0 at radius `+0x24C`, height 0;
ring 2 at `+0x24C + L·cos φ`, height `L·sin φ` (`L` = `+0x250`, `φ` = `+0x248`); ring 1 the same at fraction `+0x268`
(`00445560`–`00445665`). `φ` = 0 gives a flat annulus on the ground, 90° a cylinder wall, anything between a cone;
`+0x240` below 2π an arc. One colour per ring (`+0x25C`, `+0x260`, `+0x264`, `0044568B`–`00445735`); V = 0, `k·+0x244`,
`+0x244` per ring; U repeats definition word `+0x670` times around (`004457A4`–`00445845`) - which is what the tail's
round-up to a multiple of `+0x670` is for.

**`0x06` - `00447020` (2,062 B, read whole): a column or vortex.** `+0x26C` rows of `+0x268`-segment rings; per row the
radius, the height step and the start angle each advance as a difference series (R from `+0x254` += `+0x258` += `+0x25C`;
Y += `+0x248` += `+0x24C` += `+0x250`; twist `+0x260` += `+0x264`) (`00447290`–`00447313`): a tube, a funnel, a tornado or a
spiral from one type. V = row × `+0x244 / rows`; U repeats `+0x6D0` times; three colours + `+0x280` go to `00446050` (a
row gradient by its call shape - that body is translated VU0 code, not read line by line; registered GI-14).

**`0x07` - `00447ED0` (2,350 B, read whole): a dome or sphere.** Latitude from π/2 downwards by `+0x240 / rows`, longitude
span `+0x244`; vertex `(sin θ·R·cos φ, H·sin φ, cos θ·R·cos φ)` with R and H both starting at `+0x24C` and advancing by
their own series (`00448180`–`004482CD`). Definition byte `+0x6D2` bit 2 maps the texture from above,
`((x + R)/2R, (z + R)/2R)` (`004481FF`–`0044825F`).

**`0x08` - `0044A620` (3,483 B, read whole): a waving sheet.** A centred `(+0x270 + 1) × (+0x274 + 1)` grid of size
`+0x260` × `+0x264`; each vertex's height is a sine chosen by definition byte `+0x430` bits 3-4 (`0044A798`): a diamond
ripple `A·sin(f·(|x|+|z|) + p)`, a **circular ripple** `A·sin(f·√(x²+z²) + p)` (`0044A9B0`–`0044AA0C`), or the sum of an x
and a z wave; colour is bilinear across the four corner colours `+0x2B0`–`+0x2BC` (`0044ACDA`–`0044AF9A`). With a
sprite-sheet resource at definition `+0x438` one frame's UV rectangle is spread over the cells (`00502160`); a missing
frame with `+0x430` bit 0 releases the element (`0044B147`, `0044B184`).

**`0x0A` - `0044BAC0` (3,461 B, read whole): a sprite trail.** `+0x2A6` sprites through the `0x02` frame drawers, laid
along the element's own 32-entry position history `+0x250` (`0044C30F`, `0044C39A`) - on every other sample
(definition word `+0x2A4` bit 6) or at a fixed arc length, the float track `+0x270`, walked with `sqrtf`
(`0044C390`–`0044C526`); rotation, scale and colour step from start to end in `N - 1` steps (`0044BF1A`–`0044BF36`); bit
10 a random rotation per sprite, bit 11 a random scale jitter of `+0x2A0`. The walk seeds the render-local stream from
the element's `+0x458` and restores it after (`0044BBD5`–`0044BBF7`, `0044C6E3`–`0044C700`).

**The shared grid emitter `004434D0` (3,681 B, read whole; `00444340` has the same call sequence).** Up to four texture
layers (the four `0xF0` bundles `00431770` rebases): per layer `02AEE900` := its blend mode and `02AEE908` := its texture
(`00443578`–`00443587`); an optional per-vertex deformation; a UV source (`+0x1B0`: the walk's UVs, or 2 = **the vertex's
projected screen position**, `00443A21`–`00443A90`; 1, 3, 4 through the workbench matrices, not named here); a UV scroll;
then **layer kind 5 = untextured GiPrim kind-4 quads** (`00443D1D`, `00443E1D`), any other kind textured GiPolyGT4T
(`0044400B`, `0044421B`) - the split is the one compare at `00443C51`.

**Who authors them** ([`type_census.py`](members/type_census.py), every EFX stream in the extract - see the dispatch
page §2.8): `0x04` lives mostly in map effect banks (`.efb` / `.mpk` of `gil*`, `dor*`, `rbl*`, `rwg*`, `mfr*`, `rui*`) plus
events `e0065`/`e0066` and magic `m0136`; `0x06` in events `e0031`, `e0046`, `e0130`, `e0133`, `e0134` and magic
`m0395`/`m0396`; `0x0A` in magic `m0001`–`m0017` and about twenty others. **`0x03`, `0x07` and `0x08` are in no shipped
effect** - live walks nothing reaches.

*Not in this answer (named, not needed for the row):* what UV sources 1, 3 and 4 compute, and `00446050`'s exact colour
interpolation.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE.** `002F3750` on this page calls `FUN_00264670`, owned by that layer. What it reaches is a 35-byte float getter gated on the kind bits `byte[+3] & 0xE0 == 0x60`: it hands back the float at `[[+0xB8] + 0xD4]`, and zero for anything else; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** `003B99D0` shares `001EDDA0`/`003A8240` (2 edges);
`00361DE0`/`00363FD0`/`003623C0` share `0036DD80` (3); `00332C40` shares `003A8240` (1). Shared
helper fan-in only.

**CoreRuntimeScheduling — SERVICE (SWE2-CONTRACT 2026-09-15, 30 edges).** Two shares: the
`001EDDA0` helper is both called by eight cited element bodies and reached from `00265860`/
`00265880`; and fifteen of the cited bodies use the runtime pointer codec —
`ImageAddress_ResolveRuntimePointer` `0020E600` and `RuntimePointer_EncodeImageAddress`
`0020E620`. Shared-helper fan-in only.

## Evidence-only read — frontier hub `0017FFD0` (2026-09-18, SWE2-EC7)

`0017FFD0` — 105 B, 8 A-measured callers; the float ratio the element passes divide through.
Read against the shipping image (page stays PARTIAL — evidence-only): `001DDAB0()` supplies a
shared object; when non-null `001DD110(obj)` yields the numerator float, else the constant at
`008C5B38`; the denominator is `001DD120(obj)` on a second fetch, divided at
[`00180014`](../../_index/ADDRESS-INDEX.md). When the second fetch returns null the code divides by literal `0.0f`
at `00180028` — deliberately producing +inf rather than branching, so "no second source" reads
as an unbounded ratio downstream.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`): the layers pass 22 still reported for this page at HEAD `9a4cd5784`. Every edge was listed in full and the cited function's body was read.*

**Resource — MECHANICAL (7 edges).** `0036A190` (10 B) sets `edx = 1` and tail-jumps to the pool allocation it fronts. That allocation takes `ecx` bytes from the pool whose index sits in a global, and stamps the block header. So it is a general allocation entry, not an effect-bank operation of its own. Seven Resource bodies allocate through the same entry: `00249210`, the image member callback `0024A1D0`, `00259DF0`, `0032E7C0`, `00379E90`, `00384420` and `0051ED10`. `0032E7C0`, for example, measures a NUL-terminated string and allocates length + 1 (`0032E800`–`0032E80E`). The effect walk and those loaders share the allocator and nothing else.

**World — MECHANICAL (1 edge).** `00378540` (943 B, filed to no owner, resolved by the audit to World) allocates through `0036A190` (`00378586`). It shares the allocator and no effect state.

**WorldAreaField — MECHANICAL (4 edges).** `MapRef_BeginLoadResources` (`00268750`), `00377DC0`, `00378030` and `00378BC0` allocate through `0036A190`. `00268750` calls it at `002687C7`. Field resource loading and the effect walk share the allocator and nothing else.

## GI-14: the six tail helpers, the line emitter and the blend consumer read (OPUS, 2026-10-01)

Static, read whole from the shipping image. `def` is the element's definition (`[element + 0x20]`), and the frame index
every curve read takes is the element's `+0x44`. `004309C0` returns a float curve value (`movss` into the field),
`004314E0` an integer one (`mov` from `eax`), and `0042FDB0` a packed colour (skipped when it returns `0x80808080`, then
modulated by the element's `+0x1F0` through `0026EE00`). Every tail ends the same way. When `def + 0x49 >= 0x20` it
scales alpha by the `def + 0x30` percent track. It mirrors the colour, then calls `005002E0(def, ...)`, which selects
either `002F31C0(element, [element + 8])` or the per-element command interpreter `003A8950(2, element)`.

| helper (type) | what it reads into the element | what it composes |
|---|---|---|
| `00442600` (`0x01`) | `def+0xD0` integer -> `+0x244`; colour `def+0x80` -> `+0x240` (mirrored to `+0x1F4`) | position `+0x60` -> `+0x230`, through the parent's matrix (`0039AF70` / `00398F90`) when `[+0x10]` is set; history `+0x70` -> `+0x80` |
| `004428F0` (`0x03`) | rows `+0x110` / `+0x120` (`00430B90`); integer `def+0x180` -> `+0x258`; `003A2B20` -> `+0x240`; colours `def+0x190` -> `+0x250` and `def+0x1E0` -> `+0x254` | `00398480(+0x110)`, `003970F0`, `0039ADE0`, `00397ED0`, `0039AF70` / `00398F90` |
| `0044B3C0` (`0x08`) | rows `+0x230`, `+0x240` (then `0043EEB0`), `+0x120`, `+0x280`, `+0x290` (`00430B90`); floats `def+0x1C0` -> `+0x260`, `def+0x1D0` -> `+0x264`; integers `def+0x2C0` -> `+0x270`, `def+0x2D0` -> `+0x274`, `def+0x2E0` -> `+0x278`; `003A2A10(+0x240)` | `00398480(+0x110)`, `0039AF70` / `00398F90` / `00397ED0`, `003970F0` and `0039ADE0` on `+0x2C0` into `+0x2F0` |
| `00449560` (`0x02`) | integer `def+0x150` -> `+0x284`; colour `def+0x80` -> `+0x280`; rows `+0x110` / `+0x120` (`00430B90`) | `00398480(+0x110)`, `0039AF70` / `00398F90` / `00397ED0`, `0039ADE0(+0x230)` into `+0x260` |
| `00447830` (`0x06`) | rows `+0x110` / `+0x120` (`00430B90`); ten floats `def+0x140`..`def+0x1D0` -> `+0x240`..`+0x264` (~~each `def+0x10*k` to its own field~~ `+0x1C0`/`+0x1D0` to `+0x240`/`+0x244`, `+0x140`..`+0x160` to `+0x254`..`+0x25C`, `+0x170`..`+0x190` to `+0x248`..`+0x250`, `+0x1A0`/`+0x1B0` to `+0x260`/`+0x264` *(corrected 2026-10-02, OPUS: `00447830`+0x1B4..+0x29B)*); integers `def+0x1F0` -> `+0x268`, `def+0x200` -> `+0x26C`, `def+0x210` -> `+0x270`; colour -> `+0x274`; float `def+0x1E0` -> `+0x280` | `00398480(+0x110)`, `0039AF70` / `00398F90` / `00397ED0` into `+0x80`, `002F3570`, `00397910`, `003970F0`, `0039ADE0` into `+0x2E0` |
| `00448800` (`0x07`) | the same ladder as `0x06` one slot along: floats `def+0x140`..`def+0x1B0` -> `+0x24C`..`+0x268`, integer `def+0x1F0` -> `+0x26C`, `def+0x1C0` / `def+0x200` read, colour -> `+0x29C`, float `def+0x1E0` -> `+0x278` | the same compose chain as `0x06`, into `+0x80` and `+0x2E0` |

**The mode 1-7 line emitter `0039D6C0` (457 B).** It appends a `0x28`-byte entry to the depth-sorted display list
`[02F8F2F8]` (count word `02F8F2C6`):
- callback null;
- a fresh command list (`0020E680`) at `+0x18`;
- sort key `+8` = the lesser of the two endpoints' depth words, with the pass nibble `02AEE910` in bits 28-31;
- `+0xC` = 1;
- a flag dword `+0x20` = `003A2C70()` OR 2 when `0024E460()` or `003A3D20()` is non-zero.

It then builds a two-vertex `GiPrim` (`008642A0(list, 2)`, then `0039CDC0`) and writes each endpoint's four colour bytes
as floats. It stores the blend value - `01EFAC20[mode]`, or the `+0x30` track `02AEE908` in mode 6 - at ~~the command's
`+0x30`~~ `+0x30` of the pointer `008642A0` returns, which is the GiPrim object plus 8, so object `+0x38`; it also sets that pointer's `+0x44`, object `+0x4C`, to 1 *(re-corrected 2026-10-01, OPUS)*. It closes the list (`0020E670`). It is the line twin of the point emitter `0039D970`, which stores the
blend value at the same offset (`0039DAAC`).

~~**Where the blend value goes.** The value the section above calls record `+0x38` is the `GiPrim` command's `+0x30`.
`GiPrim` (`00863D80`) reads it as a dword (`00863FF9`) and passes it as the fifth argument of its render context's
vtable `+0x40` call (`00864029`). **Still open (GI-14, narrowed):** which class implements that slot, and so how the
GS-ALPHA-shaped value becomes the actual blend state.~~

**Where the blend value goes (re-corrected 2026-10-01, OPUS - the paragraph above was off by 8).** `008642A0` returns the new `GiPrim` object plus 8 (`lea rax, [rbx + 8]`), and both emitters address the command through that pointer. So their `+0x30` store is object `+0x38`, the record `+0x38` the section above names, and their `+0x44 = 1` is object `+0x4C`. `GiPrim` (`00863D80`, called with the object itself) tests `+0x4C`. When it is set, `GiPrim` passes `+0x38` to `001EE650`, the GS ALPHA to D3D11 blend translator of BC-1 (81-entry table `00902750` indexed `27·A + 9·B + 3·C + D`; [the BC-1 record](../../_index/candidates/bc1-selector-enum/README.md)). It then applies the result through the device's slot `+0x78`. So the value is a PS2 GS ALPHA register, and the port turns it into blend state as the GS would. The dword at object `+0x30` that `GiPrim` passes to the device's slot 8 (`PrimitiveRendererD3D11`, `006CAEB0`, stored at renderer `+0x208FC`) is a different field. **GI-14 is answered.**
