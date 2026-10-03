---
system: the element types 0x80-0x97
category: 17-Presentation-Rendering
status: "DOCUMENTED — GI-11 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: the shared tails and emit calls (0045AA50, 00454480 and peers) are not read"
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

# Element types `0x80`–`0x97` — the shared-method band

Package: `FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES` (group 3 of N).
Coordinates: `members/effect-type-methods.tsv`; helper vocabulary:
[effect-element-type-dispatch](effect-element-type-dispatch.md) +
[the-element-types-00-0a](the-element-types-00-0a.md) §2 +
[the-element-types-60-74](the-element-types-60-74.md). **NATIVE/STATIC**;
authority EXE `73461D08…21F8`.

All 23 handled types in `0x80`–`0x97` are **main-range** (no sub-range methods in
this band). `0x93` and `0x98`–`0x9F` are all-default/absent. The band's signature
is **method sharing across type ids**: three or four types frequently share one
step + update + setup and differ only in walk or not at all — the type byte here
selects parameter variants, not separate classes.

## Two record families

| family | setup shape | types |
|---|---|---|
| A | base + 3–5 three-track groups from `+0x80`, 4-track groups mid-record, singles, optional `003AA280`+`0020E620` resource stores | `0x80`–`0x8B` |
| B | base + `4G@+0x80` + `3G@+0xD0` + `3G@+0x110` + `3G@+0x150` + `1T@+0x190` (`0x91`/`0x92` also `1T@+0x1A0`) + `00431770` init(s) + one resource store | ~~`0x8C`–`0x92`, `0x94`–`0x97`~~ `0x8C`–`0x92`, `0x94`, `0x95`, `0x97`; `0x96` is family A *(corrected 2026-10-02, OPUS: `005004C0`'s table (`005004C0`+0x5B..+0x6F) sends type `0x84` and `0x96` to the same setup `00539980`)* |

## Shared-method clusters

- `0x80`/`0x82`/`0x83` — identical step `0044CC10` (54 B = base + ~~PRNG `0044B960` +~~
  tail `00450CE0` + PRNG `0044B960` *(corrected 2026-10-02, OPUS: `0044CC10`+0x1B calls the tail, +0x20 the PRNG)*), identical update `00450480`, identical setup `00539320`
  (family A: `3G`×3 `+0x80`–`+0x100`, `4G` `+0x140`/`+0x190`, singles `+0x1E0`/
  `+0x1F0`). They differ **only in walk**: `0044CC50` / `0044DD00` / `0044E530`
  (1071/1106/1089 B) — same call family (`003970A0`/`00397910`/`00398030`/
  `00399600`/`0039A9B0`/`0039B550`/`0039B620`/`003A34D0`), three emit variants.
- `0x8C`/`0x94`/`0x95` **(and `0x97`, corrected 2026-09-29, FABLE, GI-11: same birth, update `0045B260` and tail `0045B640`)** — identical step `00455390` (419 B: base + `0020E600` +
  `003A6E60` + `003D8E50` + ~~PRNG + tail `0045B640`~~ tail `0045B640` + PRNG *(corrected 2026-10-02, OPUS: `00455390`+0xB4 and +0xB9)*), identical update `0045B260`,
  identical setup `00539B30` (family B + `00431770@+0x1A0`). Walks differ and are
  all **variant selectors** (below): `00455540` (28 B), `0045AEE0` (10 B),
  `0045B2A0` (10 B).
- `0x8F`/`0x90` — identical step `00457E10` (452 B, same heavy-step shape as
  `00455390`, tail `00457980`), identical update `00456EF0`, identical setup
  `00539DA0` (family B with **two** `00431770` inits, `+0x1A0` and `+0x290`).
  `0x8F` walk `00456F30` is full-size (1393 B); `0x90` walk
  `00457FE0` is a 41 B selector.
- `0x91`/`0x92` — share setup `00539E90` only; `0x92` step `0045A050` (419 B) is
  the `00455390` shape with tail `0045AA50`; `0x91` step `00459420` same shape,
  tail `00459BD0`, ~~plus a `0020E610` call~~ **(corrected 2026-09-29, FABLE, GI-11: `0020E610`, an `x == 0` test, *replaces*
  both `0020E600` calls and inverts the fallback scan; the birth is 403 B)**. `0x92` walk `0045A200` (28 B) is a
  selector; `0x91` walk `004595C0` is full-size (1542 B, adds `00394DA0`).
- `0x84`/`0x96` — share setup `00539980` (family A + two resource stores); own
  step/update/walk each.

## The variant-selector walks

~~Four~~ Six walks in this band are not emitters at all — they test the element's
definition record and tail-jump into a shared emit body:

| walk | gate | targets |
|---|---|---|
| `0045AEE0` (`0x94`) | `*rcx != 0` | `0045AEF0` shared tail |
| `0045B2A0` (`0x95`) | `*rcx != 0` | ~~shared tail `0045B640`~~ its own body `0045B2B0` (902 B) *(corrected 2026-10-02, OPUS: `0045B2A0`+0x3 `jne 0045B2B0`; `0045B640` is the step's tail)* (read 2026-09-29, GI-11 group B1) |
| `00455540` (`0x8C`) | record `[+0x20] + 0x294 & 6` | `004559C0` vs `00455560` |
| `0045A200` (`0x92`) | record `[+0x20] + 0x2A4 & 6` | `0045A6A0` vs `0045A220` |
| `00457FE0` (`0x90`) | record `[+0x20] + 0x337`, then `+0x330` — **three-way**: `+0x330 == 0` falls into ~~an inline body at~~ its own function `00458010` | `004584E0` vs `00458CA0` (or inline `00458010`) |
| `0045BAD0` (`0x97`) | `*rcx != 0` | ~~shared tail `0045B640`~~ its own body `0045BAE0` (1,068 B) *(corrected 2026-10-02, OPUS: `0045BAD0`+0x3 `jne 0045BAE0`)* (read 2026-09-29, GI-11 group B1) |

The `[element+0x20]` record flag bytes `+0x294`, `+0x2A4`, `+0x330`, `+0x337`
therefore carry authored mode bits that choose between emit paths — the first
concrete authored-data→behavior link in the walk layer.

## The remaining full-size walks

`0x81` `0044D4A0` (926 B), `0x84` `0044EDD0` (1772 B), `0x85` `0044F970` (1869 B),
`0x86` `00450550` (1007 B), `0x87` `00451180` (938 B), `0x88` `004518D0`
(1858 B), `0x89` `00452540` (1831 B), `0x8A` `00453150` (1725 B),
`0x8B` `00454930` (1623 B), `0x8D` `00455DB0` (1276 B, calls `002F1D90`; interior read 2026-09-17, SWE2-FRONTIER: `00434A70` first at [`00455E38`](../../_index/ADDRESS-INDEX.md), `004309C0`/`0039B960` ×3 + `00430B90`/`0020E600` — the workbench-armed evaluator),
`0x8E` `00456720` (985 B), `0x91` `004595C0` (1542 B), `0x96` `00453CF0`
(1935 B) — all the same call family: workbench compose (`0026EE00`/`002F1F40`),
transform primitives `00397910`/`00399600`/`0039A9B0`/`0039B550`/`0039B620`,
then an emit variant (`003A34D0`, `003A35E0`, `003A2D80`, `003A3010`,
`003A2B20`, `0042FDB0`, `004309C0`). One emitter family with per-type emit call —
~~billboard-quad-style elements, pending the emit calls' own reads (`not read`).~~ **Read 2026-09-29 (FABLE, GI-11):** the
programs differ by type - line bundles with points, textured quads, textured strips and a fan ([the tails and
emits](#the-tails-and-the-emits-gi-11-2026-09-29-fable)).

## Steps

Thin (54–64 B): base `002F2D60` + PRNG `0044B960` + tail (`0044D840`,
`0044F4C0`, `004500C0`, `00450CE0`, `00452020`, `00453810`, ~~`00454890`~~ `00452C70`,
`00454F90`, `0045B640`, `004562B0`, `00456B00`, `00457980`, `00459BD0`,
`0045AA50`, `00454480` — ~~all `not read`~~ *all read 2026-09-29*). **Corrected 2026-09-29 (FABLE, GI-11):** `00454890` is
not a function and not an instruction start (it falls inside an 8-byte `lea` of `00454480`'s epilogue); the missing tail
is `0x89`'s `00452C70`. The order is base, then tail, then `0044B960`. Heavy (419–452 B) on
`0x8C`/`0x8F`/`0x90`/`0x91`/`0x92`: additionally `0020E600`/`003A6E60`/`003D8E50`
and field traffic at `+0x264`–`+0x2AC`. `0x86` step `004504C0` (131 B) adds
`003A6E60`; ~~`0x8A`~~ **`0x89` (corrected 2026-09-29, FABLE, GI-11; `0x8A`'s step is the 54-B `00453110`)** step `004524C0` (113 B) same. Every update is the 56 B
base+tail form.

## Former "not read" list — every item settled or scoped (SWE2-FRONTIER repair, per the SWE2-AUDIT-SEM review, 2026-10-01)

~~All step/update tails listed above;~~ *(tails read 2026-09-29 - [the tails and emits](#the-tails-and-the-emits-gi-11-2026-09-29-fable))*;
~~emit calls `00394DA0`, `003970A0`,
`00398030`, `00399600`, `0039A9B0`, `0039B550`, `0039B620`, `003A2B20`,
`003A2D80`, `003A3010`, `003A34D0`, `003A35E0`, `0042FDB0`, `004309C0`,
`003A6E60`, `003D8E50`, `0020E610`, `0017FFD0`, `002F1D90`;~~ *(each type's program
and primitive identity is answered under GI-11 - same section; the transform primitives `00399600`/`0039A9B0`/`0039B550`/`0039B620`
and the workbench save/restore `002F1D90` are documented on [the two transform primitives](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md)
and [the shared transform workbench](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md); `0017FFD0`/`003D8E50`/`003A6E60`/`0020E610`
are shared helpers documented where the neighbour pages name them)*; ~~selector targets
`0045AEF0`, `004559C0`, `00455560`, `0045A6A0`, `0045A220`, `004584E0`,
`00458CA0`,~~ *(the emit-path arms all funnel through the shared mid-ladder helper `003A2F70` - `0020E680` marshal, `001DB840` second
stage - catalogued on [the dispatch page](effect-element-type-dispatch.md); their per-branch interiors are that page's scope,
not this one's)*; the `0045B2A0`/`0045BAD0` shared tail is `0045B640`, read under GI-11 group B1; ~~`00431770`, `003AA280`~~
*(`00431770` read 2026-09-19 on [the element types 0x00-0x0A](the-element-types-00-0a.md); `003AA280` is documented on
[CONTRACT-transform-primitives](../../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md))*.
~~**No player-facing names assigned.**~~ *(What each type draws: [the tails and emits](#the-tails-and-the-emits-gi-11-2026-09-29-fable), 2026-09-29.)*

## The tails and the emits (GI-11, 2026-09-29, FABLE)

*Static reads of the shipping image plus an authored-data census; nothing executed. Reader: FABLE (Claude Opus 5.5),
with a Claude Opus 5.5 sub-reader for the tail bodies (instruction diffs between siblings), spot-checked against the
bytes. Checks: [`type_census.py`](members/type_census.py) (C1-C7, FAILS 0) and [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py) (K1-K18, FAILS 0).*

**Eight tail shapes serve the 23 types, and all fifteen tails end in the standard fork** (cull `005002E0`, release
`002F31C0` or spawn `003A8950(2)`).

| group | tails (types) | what the tail does each frame | fork (first member) |
|---|---|---|---|
| A1 | `00450CE0` (`0x80`/`82`/`83`/`86`/`87`), `00452020` (`0x88`), `00452C70` (`0x89`), `00453810` (`0x8A`) - 1,118 B, definition offsets differ only | rotation / scale / offset tracks → the element's **full world matrix `+0x250`–`+0x28F`** with the position as row 3; parent rotation in orientation mode 0 only; mode-3 motion alignment; **two colours** `+0x240` / `+0x244` | `004510ED` |
| A2 | `00454F90` (`0x8B`) | A1 with one colour (track `+0x170`) | `00455339` |
| A3 | `0044F4C0` (`0x84`), `00454480` (`0x96`) - one constant apart | one colour (`+0x140`); **parent rotation always folded**; a camera-facing select `00434C50` from definition word `+0x232` (`0x84`: none or `02AEEC30`; `0x96`: the full eight-way set incl. look-at `00434900` and yaw-only `00434A70`); **alpha × (p/100)²** - the percent applied twice (`0044F84D`–`0044F881`) | `0044F899` |
| A4 | `0044D840` (`0x81`) | two **local** points `+0x230` / `+0x240` never through the parent, matrix `+0x260` always parent-combined, colours `+0x250` / `+0x254` | `0044DCAF` |
| A5 | `004500C0` (`0x85`) | **type `0x0A`'s trail tail `0044C850`** with two changes: parent transform only in modes 1-2, rotation always sampled | `00450439` |
| B1 | `0045B640` (`0x8C`/`94`/`95`/`97`), `00457980` (`0x8F`/`90`), `0045AA50` (`0x92`) - 1,154 B | **type `0x05`'s mesh tail `0044A180`** + a **per-axis random mirror** of the scale from element byte `+0x2A4` (`+0x2AC` for `0x8F`/`90`) (`0045B731`–`0045B791`); modes 3 and 6; texture / context integer `+0x290` | `0045BA72` |
| B2 | `00459BD0` (`0x91`) | B1 without the pre-parent history and mode 6 | `00459FBD` |
| B3 | `004562B0` (`0x8D`), `00456B00` (`0x8E`) | `0x05`'s tail without mirror, pre-parent history or mode 6 | `00456648` |

**Births roll per-element variety once.** The heavy births `00455390` (`0x8C`/`94`/`95`/`97`), `0045A050`, `00459420`,
`00457E10` roll the three mirror coins (`003A6E60(2)`), one or two random float offsets (`003D8E50`) the walks add to two
sampled parameters, and **a random pick among up to 32 authored resources** into element `+0x298` (`004554C2`–`00455531`).
The coin births `004504C0` (`0x86`) and `004524C0` (`0x89`) turn a 2-bit authored field into `+0x294`, **2 meaning "0 or 1
at random"**. `0x8D` / `0x8E` always draw **resource 0**: their births store `+0x298 := 0` (`00455DA0`, `00456710`), and no
other element body writes `+0x298`.

| types | program(s) (UQ-213) | primitive | on screen | authored: chunks / assets |
|---|---|---|---|---:|
| `0x80`, `0x82`, `0x83`, `0x86`, `0x87` | `004958A0`, `0047E4F0`, `004804A0`, `00485790`, `004930A0` + POINT programs `004C6DE0`, `004C5DF0`, `004C4D20`, `004C37C0`, `004C2160` | Gouraud LINE `0x049` + POINT `0x040` | line bundles with points | 875 / 334; 617 / 156; 80 / 47; 115 / 87; 175 / 51 |
| `0x84`, `0x88`, `0x89`, `0x8B`, `0x96` | `0048AF70`, `0048F8C0`, `00482860`, `0047C360`, `0048D4B0` | flat textured quad strip `0x054` | textured quads placed by the world matrix | 1,972 / 443; 41 / 31; 36 / 8; 1 / 1; 268 / 65 |
| `0x85` | `00488340` | textured strip `0x05C` | a ribbon along the 32-sample path | 78 / 41 |
| `0x8C`–`0x92`, `0x95` | `00497AC0` / `00499A20`, `004BF500`, `0049B9E0`, `0049D540` / `004A0090`, `004A4410` / `004A33B0` / `004A1E30`, `004A6C20`, `004A8B00` / `004AAFC0`, `004B0230` | textured strip `0x05C` | a prebuilt strip resource, randomly mirrored | `0x8C` 7,509 / 889; `0x8D` 1,170 / 503; `0x8E` 136 / 74; `0x8F` 1,663 / 376; `0x90` 765 / 307; `0x91` 12 / 7; `0x92` 84 / 45; `0x95` 456 / 216 |
| `0x94` | `004ADD10` | triangle fan `0x05D` | a textured fan | 2,344 / 357 |
| `0x81`, `0x8A`, `0x97` | raw GS packets | - | **nothing on PC** (UQ-204), and **no shipped effect authors them** | 0 |

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT.** `FUN_003b99d0`, owned by that layer, calls `001EDDA0` on this page. That caller is a 1,501-byte state machine driven by `byte[+8]`, decremented case by case in a `0xE0`-byte frame with a stack cookie; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 33 edges).** 32 of the 33 edges are
the image-pointer fixup pair `0020E600` `ImageAddress_ResolveRuntimePointer` (26) and `0020E620`
`RuntimePointer_EncodeImageAddress` (6) inside this page's step/walk bodies; the last is the
`001EDDA0` frame helper called by `004500C0`. Mechanical infrastructure, below any scheduling
relationship.

*Added 2026-09-29 (FABLE, GI follow-up): the layer the GI answers newly brought into this page's audit.*

**WorldAreaField — SERVICE (1 edge).** The element body `00497AC0` calls `WorldTransition_GetTransitionFieldId` (`00314910`, the persistent payload's `+0x105C`) at its head and takes a special path only when the field is `0x11E`, `0x2B6` or `0x2B7` and a further mode query answers 2. The effect element specialises its behaviour for three fields by asking the world layer which field is current; it owns no field state.
