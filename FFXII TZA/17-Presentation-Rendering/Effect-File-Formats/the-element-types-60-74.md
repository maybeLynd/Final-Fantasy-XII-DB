---
system: the element types 0x60-0x74
category: 17-Presentation-Rendering
status: "DOCUMENTED — GI-10 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: all step/update tails (0045C450, 0045CDC0, 0045D7D0, 0052A8B0 and peers) and 00431770 are not read"
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

# Element types `0x60`–`0x74` — the mid-range main types and the first sub-range cluster

Package: `FABLE-REQ-SWE2-FRONTIER-EFFECT-TYPE-CLASSES` (group 2 of N).
Coordinates: `members/effect-type-methods.tsv`; architecture and helper vocabulary:
[effect-element-type-dispatch](effect-element-type-dispatch.md) +
[the-element-types-00-0a](the-element-types-00-0a.md) §2. Evidence class
**NATIVE/STATIC**; authority EXE `73461D08…21F8`.

The band splits in two: `0x60`–`0x67` are **main-range** types (own step/update/
walk/setup through `002F3BC0`/`002F3910`/`002F4020`/`005004C0`), while `0x68`–`0x74`
are **sub-range** types — the main tables dispatch them `default` and the
`0x42`–`0xAB` sub-dispatchers carry their `sub-step`/`sub-setup`/`sub-update`/
`sub-walk`/`sub-seventh` methods. Types `0x63`, `0x64`, `0x6C`–`0x6F` have **no
handler in any table** — fully default/absent.

New helper identifications this group (all read from the shipped body):

| helper | role |
|---|---|
| `0044B960` | shared PRNG — xorshift-style bit chain over state dword `01EF93E8`, gated by guard dword `022D9138`; called inside the step bodies of `0x0A`, `0x60`–`0x62`, `0x65`, `0x66` before the type tail, except in `0x0A`'s, where it runs ~~before~~ after its tail *(corrected 2026-10-02, OPUS: `0044BA80`+0x1B calls the tail `0044C850`, +0x20 the PRNG)* |
| `003A3E20` | element field setter: `+0x44 = 0xFFFFFFFF`, `+0x42 = dx` (12 B, `0x65`/`0x66` steps) |
| `0024DDD0` | reads global object `+0x13B` byte and calls `003A3FD0`/`003A6BA0` storing two results — ~~config-indexed double lookup~~ **(corrected 2026-09-29, FABLE, GI-10: the effect's owner actor `003A3FD0` and target actor `003A6BA0`, for the birth gate `0045F600`)** (`0x67`, `0x6B` steps) |
| `0024B1C0` | **deferred-free queue**: if count word `02092168` < `0x100`, appends `rcx` to the qword array at `02091150` and increments; else `jmp 003697F0` (immediate free). The `0x6B`/`0x73`/`0x74` sub-seventh entries are wrappers that push element fields (`+0x338`-family) onto this queue — resource release at element teardown |
| `005C5230` | `xor eax,eax; ret` — the shared return-0 stub (page's "null path" confirmed) |
| `0016D6A0` | `_guard_check_icall` — `ret 0`; used as a no-op method slot |
| `0053DD10` | `InputDevice_QueryAvailabilityState_Always1` — `mov eax,1; ret`; as `0x70`'s sub-step simply returns true |

## `0x60` / `0x61` / `0x62` — one family

`0x60` and `0x62` share setup `0053A120`; `0x61` has `0053A060` (a trimmed
variant, not the same shape). All three steps are 87 B = base stepper + PRNG
`0044B960` + own tail (`0045C450` / `0045CDC0` / `0045D7D0`, all read 2026-09-29, GI-10);
all updates are the 56 B base + same tail. `0053A120`'s record: four 3-track
groups `+0x80`–`+0x140`, three 4-track groups `+0x180`/`+0x1D0`/`+0x220`, three
single heads `+0x270`–`+0x290`. `0x61`'s `0053A060` drops the fourth 3G (three
at `+0x80`/`+0xC0`/`+0x100`), moves the 4Gs to `+0x140`/`+0x190`/`+0x1E0`, and
carries **four** singles `+0x230`/`+0x240`/`+0x250`/`+0x260` — one extra single
over `0x60`/`0x62`, record end `+0x290`. Walks are ~1.1–1.2 KB and identical in
call family —
`0026EE00`/`002F1F40`/`0039B620` workbench compose, then `003970A0`, `00397910`
(**the second transform primitive** — a vector through the workbench matrix),
`00398030`, `00399600`, `0039A9B0`, `0039B550`. Three sibling types differing in
record tail and step tail.

## `0x65` / `0x66` — large records with a repeated tail block

Both steps are 112 B = base + `003A3E20` (field reset) + PRNG + tail
(`0045E3C0` / `0045F140`). Setups (`0053A1E0` 455 B / `0053A3B0` 535 B) share a
long record: four 3-track groups `+0x80`–`+0x140`, then a **nested 3×3 loop**
(`rbp=3` outer, `rdi=3` inner, `add rbx,+0x50`) of **nine** 4-track groups
`+0x180`–`+0x400`, two further 4Gs `+0x450`/`+0x4A0`, a run of 14 (`0x65`:
`+0x4F0`–`+0x5C0`) or 20 (`0x66`: `+0x4F0`–`+0x620`) single heads, **two**
`00431770` inits at `0xF0` stride (`0x65`: `+0x5D0`/`+0x6C0`; `0x66`:
`+0x630`/`+0x720`), then a trailing 3-track group at `+0x7B0` (`0x66`: `+0x810`)
— records end `+0x880`/`+0x8F0`, the second-largest of the group. `0x66`'s walk calls
`0017FFD0` + `0024E640` (the VU0-path helpers type `0x05` uses) — same geometry
family as `0x05`.

## `0x67` — the only main-range type here with a seventh method

Setup `0053A5D0` (287 B): three 3-track groups `+0x80`–`+0x100`, **eight**
singles `+0x140`–`+0x1B0`, then a nested 3×3 loop (`rbp`/`rdi`, `rbx += 0x50`)
of **nine** 4-track groups ~~`+0x1C0`–`+0x460`~~ starting `+0x1C0`–`+0x440` *(corrected 2026-10-02, OPUS: `0053A5D0`+0xBE `lea rbx, [r14 + 0x1c0]`, nine passes of +0xD5..+0xED)*, `00431770@+0x490`, record end
`+0x5F0`. Step `0045FD50`
(968 B — a real body, not a wrapper): calls `0024DDD0` ~~(config-indexed lookups)~~,
`0036A190`/`0036C140`/`0036C1D0` (bank ops), `00532EF0`, ~~tail `0045F600`, then~~
`004607C0` — and also invokes the seventh dispatcher `002F31C0` itself. **Corrected 2026-09-29 (FABLE, GI-10):**
`0045F600` is not a tail but a **birth gate** - a body-separation test between the effect's owner and target (both from
`0024DDD0`), on definition word `+0x5C6` bit 13; the tail is `004607C0` ([the tails](#the-tails-the-emits-and-who-authors-them-gi-10-2026-09-29-fable)). Its own
seventh `00460120` (80 B) calls `003697F0` and touches `+0x338`/`+0x3B0`/`+0x3C0`/
`+0x3D0` — teardown of three owned resources.

## `0x68`–`0x6B` — first sub-range cluster

Sub-steps all call base `002F2D60` ~~plus `003A3E20`/`003D8E50`~~ and own tails
(`00523380`/`00524320`/`005263F0`/`00529D50`, ~~`not read`~~ *read 2026-09-29*) **(corrected 2026-09-29, FABLE, GI-10:
`003A3E20` is in `0x68`'s step only; `0x6B`'s calls neither)**; sub-updates are the
56 B base+tail form. Record sizes jump — sub-setups reach `+0x7C0` (`0x68`),
`+0x430` (`0x69`), `+0x3C0`+four groups (`0x6A`), `+0x730` (`0x6B`).

- `0x68` sub-walk `00522D80` (1531 B): `00202B70` + `00462260` + `00540F40` + the
  usual compose; touches a `+0x78`/`+0x7C`/`+0x80` chain.
- `0x69` sub-step touches `+0x230`–`+0x875` (deep record); sub-walk `00523D30`
  same call family as `0x68`.
- `0x6A` sub-step `00525D50` does its own `0020E600`/`0020E620` pointer fixups and
  calls seventh dispatcher `002F31C0`; sub-seventh `00526040` (55 B) resolves the
  `+0x248` pointer. Sub-walk `00526080` adds `00202D70`/`00203170`/`0024E460`.
- `0x6B` sub-step `00529200` calls `0024DDD0` + `0036A190` + `00532EF0` (the `0x67`
  config family); setup carries **nine** `0042FCF0` 4-track groups at `0x50`
  stride ~~`+0x1C0`–`+0x3F0`~~ starting `+0x1C0`–`+0x440` *(corrected 2026-10-02, OPUS: `0054F7C0`+0x84 to +0xF4, the last at `lea rcx, [rdi + 0x440]`)* plus 12 singles and three `00431770` inits
  (`+0x550`/`+0x640`/`+0x730`, 0xF0 stride — three repeated sub-blocks); sub-seventh
  `005294B0` pushes `+0x338`/`+0x3B0`/`+0x3C0` onto the deferred-free queue
  `0024B1C0`.

## `0x70` — the degenerate type (confirmed)

Only its **setup** `0054F270` (212 B) is real: base + three singles
`+0x80`/`+0x90`/`+0xA0`, a 3-track group `+0xB0`, 4-track `+0xF0`,
`00431770@+0x3C0`, then an **8-iteration loop** writing `1T@+0x140+i·0x10` +
`3G@+0x1C0+i·0x40` — eight singles `+0x140`–`+0x1B0` and eight 3Gs
`+0x1C0`–`+0x380`, the record's largest region; record end `+0x4BC`. Every
runtime method is
a stub — sub-step `0053DD10` returns 1, sub-update `005C5230` and sub-walk
`0016D6A0` (`_guard_check_icall`, `ret 0`) and sub-seventh `0016D6A0` are no-ops.
The page's warning was right: `0x70` is a **definition-only type** — it parses a
record and does nothing per-frame. Whatever it contributes is entirely in the
authored fields the setup rebases.

## `0x71`–`0x74` — the densest records

All four sub-steps call base + `0036A190` + `002F31C0` (seventh dispatcher) + own
tails (`0052A8B0`/`0052B5E0`/~~`0054C6B0`/`0054E040`~~, ~~`not read`~~) **(corrected 2026-09-29, FABLE, GI-10: `0054C6B0` /
`0054E040` are birth-only piece generators; the `0x73` / `0x74` update tails are `0052E270` → `0054C440` and `0052F400` →
`0054DD30`)**; `0x72`–`0x74`
also call `00861EBA`. Sub-walks share one call family (`0026EE00`/`002F1F40`/
`0042FDB0`/`004309C0`/`00430B90`/`004314E0`/`00431830`, `0x71`/`0x72` add
`00434900`, `0x73`/`0x74` add `0017FFD0`/`00202D70`/`00203170`/`0024E460`/`0024E640`).

Records are the largest yet — `0x72`/`0x73`/`0x74` carry a `0x50`-stride run of
**nine** 4-track groups (`+0x120`–`+0x3F0` for `0x72`; `+0x90`/`+0xE0`/`+0x130`
start for `0x73`/`0x74` ~~then group runs at `+0x190`–`+0x480`~~, which carry only those three 4-track groups and then 1-track / 3-track pairs from `+0x180` *(corrected 2026-10-02, OPUS: `0054FFF0`+0x2B, +0x39 and +0x47 are its only `0042FCF0` calls, likewise in `00550200`)*), 14–20 single heads,
and **three–four `00431770` inits at `0xF0` stride** (`0x71`: `+0x570`/`+0x660`/
`+0x750`; `0x72`: `+0x500`/`+0x5F0`/`+0x6E0`; `0x73`: `+0x4E0`/`+0x5D0`/`+0x6C0`/
`+0x7B0`; `0x74`: `+0x4C0`/`+0x5B0`/`+0x6A0`/`+0x790`) — repeated equal-size
sub-structures, consistent with per-emitter or per-sub-element slots. Sub-seventh
for `0x73`/`0x74` (`0052D8E0`/`0052EA50`, 54 B each) queue `+0x380`/`+0x388` /
`+0x3D0`/`+0x3D8` through `0024B1C0`; `0x71`/`0x72` sub-seventh are 17 B field
writes (`+0x3C8`/`+0x3F0`).

## What this group establishes — and what it does not

**Established:** the sub-range types use the same method vocabulary as main-range
(base stepper/advance + rebase setup + workbench walk), just reached through the
`0x42`–`0xAB` dispatchers; sub-seventh is the resource-release hook (deferred-free
queue `0024B1C0`, array `02091150`, count `02092168`); `0x70` is definition-only;
the `0x50`-stride 4-track-group runs and `0xF0`-stride `00431770` blocks make the
`0x6B`–`0x74` records regular arrays of repeated structures.

~~**Not read (explicit):**~~ ~~all step/update tails (`0045C450`, `0045CDC0`,
`0045D7D0`, `0045E3C0`, `0045F140`, `0045F600`, `004607C0`, `00523380`,
`00524320`, `005263F0`, `00529D50`, `0052A8B0`, `0052B5E0`, `0054C6B0`,
`0054E040`); `00431770` still `not read` (third-variant init used at `0xF0`
stride);~~ *(tails read 2026-09-29 - [the tails](#the-tails-the-emits-and-who-authors-them-gi-10-2026-09-29-fable); `00431770`
read 2026-09-19 on [the element types 0x00-0x0A](the-element-types-00-0a.md))*; ~~the walk emit tails `003970A0`, `00399600`, `0039A9B0`, `003A33B0`,
`003A34D0`, `0039ADE0`, `00202B70`, `00202D50`, `00202D70`, `00203170`,
`0024E460`, `0024E640`, `00462260`, `00540F40`, `00434900`, `0036A190`,
`0036C140`, `0036C1D0`, `00532EF0`, `003697F0`, `0017FFD0`, `003D8E50`,
`003A6E60`, `00541E00`/`00542060`/`005439A0`/`005450E0`/`00545120`/`00547DD0`/
`0054A9C0`, `00808C40`, `00861EBA`.~~ *(Each type's program and primitive
identity is answered under GI-10 - the section below; the transform primitives and the shared helpers are documented on the
shared pages, and `00808C40`/`00861EBA` are the CRT stack-cookie check and the block copy.)* ~~**No player-facing names assigned** — the
emitter call identity still unread.~~ *(Each type's program and primitive: [the emits](#the-tails-the-emits-and-who-authors-them-gi-10-2026-09-29-fable), 2026-09-29.)*

## The tails, the emits, and who authors them (GI-10, 2026-09-29, FABLE)

*Static reads of the shipping image plus an authored-data census; nothing executed. Reader: FABLE (Claude Opus 5.5),
with a Claude Opus 5.5 sub-reader for the tail bodies, spot-checked against the bytes. The step method is the element's
**birth** (`002F2D60` zeroes the age; [what these types are](the-element-types-40-42-a0-ab-d0-d1.md#what-these-seven-types-are-gi-9-2026-09-29-fable)),
and element `+0x48` counts updates, so a tail testing `+0x48 == 0` is running at birth. Checks: [`type_census.py`](members/type_census.py) (C1-C7, FAILS 0) and [`gi_effects_checks.py`](../../_index/candidates/gi-0929-effects/gi_effects_checks.py) (K1-K18, FAILS 0).*

"The common head" below is the frame-by-frame template ([an effect element, frame by frame](an-effect-element-frame-by-frame.md)):
rotation / scale / offset vector tracks, position through the parent, mode-0 parent fold, mode-3 motion alignment,
instance colour, percent alpha, `+0x1F4` copy.

| type | per-frame tail | what it makes the element do | cull fork | program / primitive (UQ-213) | authored: chunks / assets |
|---|---|---|---|---|---:|
| `0x60` | `0045C450` (1,155 B) | common head (colour track `+0x180`); **two random seeds `+0x244` / `+0x248` re-rolled on authored intervals** (timer words `+0x24C` / `+0x24E`, reload definition words `+0x2BC` / `+0x2BE`, the second gated by `+0x2C0` bit 0), which the walk hands to its program (`0045C00E`–`0045C024`) | `0045C882` | `004B1190`: line strip + textured strip | 84 / 22 |
| `0x61`, `0x62` | `0045CDC0`, `0045D7D0` | the same code; four operands differ (colour `+0x140` for `0x61`; timer words `+0x280`–`+0x284` / `+0x2C8`–`+0x2CC`) | yes | `004B9EA0`, `004BC320`: line strips | 9 / 7; 2 / 2 |
| `0x65`, `0x66` | `0045E3C0`, `0045F140` (1,213 B; three operands differ) | common head + three seeds; **after the cull passes**, a target offset (track `+0x140`) is resolved into a **target point** `+0x240` by `002F3360` from the sub-record at definition `+0x7B0` (`+0x810`): own position (optionally latched at birth), through the matrix of an object found by `003A8240`, or a point queried from `003A56F0`; the walk sends `+0x230` and `+0x240` as the two ends | `0045E7EA` (target resolved between cull and spawn) | `004EF940`, `004F7070`: textured strips | 169 / 38; 414 / 81 |
| `0x67`, `0x6B` | `004607C0` (894 B), `00529D50` (917 B) | common head without colour or mode 3, then **one step of the streamer chain `00533B20`** (N streamers of 32 points, see [the four cores](#the-four-simulation-cores-and-the-ability-names-gi-10-2026-09-29-fable); a pre-warm of N + 2 / N + 1 steps at birth; **32 extra steps** on a settle request `+0x3D8` / `+0x3D4` set by `0045FD00` / `00529D40` from the commit dispatcher `0043EE70`); the births are gated by `0045F600`, which refuses the element when **caster and target touch** (their authored body boxes as ellipsoids) | `00460AFB`; tail jumps `0052A0CE` / `0052A0E0` | `004E7D90` (+ `004E31E0`): textured strips | 364 / 176; 258 / 87 |
| `0x68` | `00523380` (2,160 B) | a **bolt travelling from a start point to a resolved target** along a bent curve: each end gets a fixed random slot on a ring around the line, `00540FD0` integrates head and tail into the travelling point `+0x90` (dropped when it runs off either end), wobble re-rolled every definition word `+0x89C` frames | **none** - spawn(2) every frame | `004DF440` (compute) → `004E0F70` strip | 162 / 68 |
| `0x69` | `00524320` (1,122 B) | a **two-edge trail on an actor's bone or linked model** (five frame modes, definition byte `+0x876`), pushed into 32-entry histories by `00542740`, which also builds each sample's bend direction (the strip itself is built by the VU1 program) | **none** | `004DCC00` → `004DDDF0` strip | 58 / 19 |
| `0x6A` | `005263F0` (1,405 B) | a **water surface**: texture window and scroll, up to three disturbance pokes, then 0-5 steps (int track `+0x3C0`) of the damped 2-D wave equation `00545650`, whose coefficients the birth's `00545120` computes: `k = c²dt²/h²`, `(4 − 8k)/(μdt + 2)`, `(μdt − 2)/(μdt + 2)`, `2k/(μdt + 2)` | **none at all** | `004D7BF0` strip | 395 / 66 |
| `0x70` | - | definition-only (unchanged) | - | none | **0** |
| `0x71` | `0052A8B0` (1,273 B) | common head without colour; 21 float tracks into six per-texture-layer triples (component i = layer i, read only by the packet builder `005480E0`) + two scalars of the block `+0x280`; **one step of the streamer chain `00548A00`** (32 extra on `+0x434`) - the same ring-root advance as `00533B20`, without impulse mode, plus a periodic seed and lifetime re-roll; the birth's `00547DD0` places the streamer roots on a horizontal ring, evenly spaced or at random angles | `0052AD67` | `004D40E0` strip: **streamers flowing from a ring** | 28 / 10 |
| `0x72` | `0052B5E0` | arms the per-model **sway oscillator** through its parameter install `0054B1F0` ([the per-model oscillator subsystem](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md) section 6b) | - | `004D0FA0` strip | 89 / 47 |
| `0x73` | update `0052E270` → `0054C440` (375 + 621 B) | a **model shattering**: pieces (generated at birth by `0054C6B0`, distance-ordered) are released by two authored fronts (tracks `+0x330` / `+0x350`, bands `+0x340` / `+0x360`), then move, spin and fall (gravity track `+0x320`) | **none** | `004C8320`: flat / textured triangles and strips | 14 / 5 |
| `0x74` | update `0052F400` → `0054DD30` (341 + 778 B) | the same with one front, a random per-piece gravity factor and optional local-frame motion (pieces from birth-only `0054E040`) | **none** | `004C8320` | 4 / 2 |

The "arc", "beam", "bolt", "trail", "water", "streamer" and "shatter" words are readings of the read mechanics, not game
names. **`00431770`** is the texture-layer bundle rebase read 2026-09-19 on [the element types 0x00-0x0A](the-element-types-00-0a.md);
the `0xF0`-stride runs of this band's records are its bundles. The runtime reads definition fields past the quoted
sub-setup reach: to `+0x8BC` (`0x68`), `+0x882` (`0x69`), `+0x886` (`0x6B`).

## The four simulation cores and the ability names (GI-10, 2026-09-29, FABLE)

*Static reads of the shipping image; nothing executed. Reader: FABLE (Claude Opus 5.5). The four bodies were read
whole, with the VU0 register bank named per [the EE and VU0 register bank](../../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md).
Checks: [`gi10_cores_check.py`](../../_index/candidates/gi-0929-effects/gi10_cores_check.py) (139 checks, FAILS 0) and
[`gi10names.py`](../../_index/candidates/gi-0929-effects/gi10names.py) (18 checks, FAILS 0; table `gi10names.tsv`). The `0x71` layer values below
were read in the x86-translated VU1 program `004D40E0`, which works on the emulated VU memory `02064E30`.*

**`00545650` (2,196 B, `0x6A`) - one explicit damped height-field wave step.** Each 16-byte cell of the W × H grid
(`S+0x14` × `S+0x10`, base `S+0x18`) holds `(h_n, h_{n−1}, ∂v, ∂u)`. The step runs three passes:
1. `y ← k1·x + k2·y + k3·(sum of the four neighbours' x)`, interior cells only, two cells per iteration, with the
   coefficients `S+0x30` from `00545120` (`00545760`–`00545A94`);
2. the new height's central differences into `z` / `w`, and the `x ↔ y` exchange one row behind (`00545AE0`–`00545D80`);
3. the last row's exchange (`00545DA0`–`00545E9E`).

The rim is never written, so the edge is a fixed zero boundary. The draw program `004D7BF0` gets the heights and the
gradients.

**`00542740` (4,603 B, `0x69`) - the trail's histories and bend, not its geometry.** It pushes three 32-sample histories
- edge point P1 (`S+0xB0`), edge point P0 (`S+0x2B0`), and a unit bend direction plus the head's travel (`S+0x4B0`) - and
a turn-angle array (`S+0x6B0`). For each new sample:
- the angle is `acos` of successive edge directions (the table `00D12590`, `005434ED`–`005434FF`);
- a quarter turn about their cross product (`005435AB`–`00543649`) bends the head's motion into
  `Q = ½(A0 + A1) + t·0.2·lenA·angle`, whose direction is stored (`005436F9`–`00543874`);
- a clamped speed-excess accumulator is kept (`005437FA`–`00543845`);
- width-like scalars `max(len, 0.8·len·angle)` are stored (`0054387D`–`005438DE`).

It builds no vertices; the VU1 program `004DCC00` → `004DDDF0` does.

**`00533B20` (9,526 B, `0x67` / `0x6B`) - N streamers of 32 points, not a cloth solver.** For each of the definition's
N strands (`S+0xB0`, records of `0x440` bytes):
- every point takes the previous slot's position plus its own velocity, plus the anchor's motion when attached:
  `P[j] ← P[j−1] + D[j−1] + Δ` (`00534548`–`00535FC8`);
- the head is the strand's root on a horizontal ring, carried through the element matrix;
- the head velocity is an outward push plus `amplitude·cos(phase)` vertically, and the phase advances each step;
- an optional impulse mode (definition `+0x5C6` bit 14) rebuilds the velocities each step from two damped 32-entry
  histories (factors definition `+0x5D8` / `+0x5DC`, `00533C45`–`0053453A`).

There is no neighbour constraint: no pass reads `P[j+1]`.

**`00548A00` (7,298 B, `0x71`) - the same streamer advance.**
- It runs over `P+0x140` records of `0x450` bytes, without the impulse mode (`00548B50`–`0054A596`).
- Every `P+0x7C` updates it re-rolls each record's seed and lifetime (`0054A604`–`0054A66E`), which the draw reads.
- **The six triples are 3 texture layers × 6 scalars**, transposed: component i belongs to layer i. They are read only
  by the packet builder `005480E0`, which sends them per layer to VU1 packet dwords `02AE8848`–`02AE885C`
  (`005487D8`–`0054895D`).
- The layers are the definition's `0xF0` texture bundles at `+0x570` / `+0x660` / `+0x750`. The walk `0052A360`
  enables one when its kind is 2 or 4 and its texture resolves.

**What the six per-layer values do, read in `004D40E0`.** Each layer's block is unpacked to VU cells `0x46` / `0x47`: the
template head built by `004D3FE0` carries `UNPACK V4-32, 9 cells, to cell 0x46` (`004D4011`). The program loads them in
its per-layer path (`004D63CF`–`004D63ED`, `004D6893`–`004D689C`). Here `run` is the trail distance, which grows per
sample (`004D78F9`–`004D793F`).

| value (definition source) | effect on the strip |
|---|---|
| triple 0 (`+0x4E0..`) | **U offset**: added to each vertex's `s` (`004D74AA`–`004D74B6`), or to the screen-projected `u` in mode 1 |
| triple 1 (`+0x510..`) | **V offset**: the `t` of the strip's first edge (`004D74DB`), or the screen-projected `v`'s offset in mode 1 |
| triple 2 (`+0x480..`) | **U advance along the trail**: `s = triple 0 + triple 2 × run` (`004D74E3`, `004D7503`), × `02064BCC` when byte `P+0x63+i` is 0 (`004D69FD`–`004D6A15`) |
| triple 3 (`+0x4B0..`) | **V span across the strip**: `t` = triple 1, + ½·triple 3, + triple 3 at the three vertices across it (`004D74C6`–`004D7516`) |
| triple 4 (`+0x450..`) | a **colour-transition factor**: when t4 ≥ 0, `run / t4` interpolates between two sets of working colours (`004D6AEA`–`004D6B4B`); *the colour sets and the t4 < 0 branch `004D6F46` are not traced - interpretation* |
| triple 5 (`+0x540..` × definition `+0x140`) | **alpha multiplier**: it scales the `w` lanes that become the alpha of the three clamped vertex colours (`004D6943`–`004D69F5`, `004D72C9`–`004D737B`) |
| mode byte `P+0x60+i` (1 for a bundle of kind 4, 0 for kind 2) | **0 maps the texture along the trail; non-zero projects it from the screen**: `u = (x − 1792)/512`, `v = (y − 1824)/512`, plus triples 0 / 1 (`004D7411`, `004D75E5`–`004D7687`) |

**Ability names (an exact join).**
- `BattleAction_GetPresentationParameter` (`0030A190`) returns action-row word `+0x24`, or `+0x28` for ids `0xD0`–`0xF1`
  while the special-sequence state `022C2160` is 5 (the cinematic on screen) or 6 (ending), per
  [the battle runtime mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2d
  (`0030A1FB`–`0030A209`). So a Quickening (`0xD0`–`0xE1`) or a Concurrence (`0xE2`–`0xF1`) uses its `+0x28` effect
  during its cinematic and `+0x24` otherwise.
- That number is loaded as resource kind 11 / 38.
- The two path arrays `01E18670` / `01EBE740` map it to `magic\mNNNN.efx` by index.

That gives the actions whose effect file holds each type:

| type | actions (effect file) |
|---|---|
| `0x61` | Gravity, Gravity Mote (`m0080`); Graviga, Piercing Graviga (`m0081`); Dark Matter (`m0176`); Hell Blaster (`m0275`); `m0082` is named by no action row |
| `0x69` | Kamikaze (`m0239`), Self-Sacrifice (`m0319`), Spiral Cut (`m0321`), Mind Lash (`m0324`), Snake Lash (`m0325`), Tail Swipe (`m0331`), Slice Thrice (`m0364`), Sentence (`m0371`); through `+0x28`: Shatterheart (`m0125`), Ruin Impendent (`m0130`), Heaven's Wrath (`m0133`) |
| `0x71` | Monarch Sword (`m0367`), Mach Wave (`m0387`), Azure Vortice (`m0388`), Crimson Vortice (`m0389`) |
| `0x73` | Sword Dance (`m0360`), Force of Will (`m0386`); through `+0x28`: Ruin Impendent (`m0130`), Resplendence (`m0137`) |
| `0x74` | through `+0x28`: Flame Purge (`m0131`) |

**Coverage limits (not residue).**
- 23 of the 24 band-carrying magic files get an action name.
- The `+0x28` names are the ones used during the Quickening / Concurrence cinematic.
- The band also occurs in 41 non-magic paths (event cut-scene effects, `.efb` / map packs, monster models, `chara`
  effects), which no ability-keyed table reaches. They get no name, so types `0x60`, `0x62`, `0x65`–`0x68`, `0x6A`,
  `0x6B` and `0x72` have none by this join.
- A name says the action's effect file holds the element, not that the element is the visible part.

*Nothing of GI-10 remains open (2026-09-29). The coverage limit on names above is not a residue: no ability-keyed
table reaches effects that are not magic effects.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT.** `FUN_003b99d0`, owned by that layer, calls `001EDDA0` on this page. That caller is a 1,501-byte state machine driven by `byte[+8]`, decremented case by case in a `0xE0`-byte frame with a stack cookie; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleAction_FindApproachGeometryAroundTarget`, owned by that layer, calls `00203170` on this page. That caller is the approach-geometry search: a `0x160`-byte frame with a stack cookie, working from the caller's `[rcx]` and `[rcx+8]` pair; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (6 edges through 2 of this page's functions).** The Input layer reaches this page at `0053DD10`, `0022B6E0`. `FUN_002e09a0` is the worked example, read in full - it is a 1,002-byte sweep that walks its indices through one per-index query; **1 of the 6 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022B6E0` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `0022B6E0` on this page calls `SaveRuntime_ResetActiveImageAndRebindState`, owned by that layer. What it reaches is a 50-byte reset that names the buffer: it zeroes **`0x56690` bytes at `02164280`** - the active save image - then re-runs the rebind sequence and tail-jumps into the state reset; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 20 edges).** All 20 edges are the single shared
accessor `00203170` called by twenty Movement bodies (`PartyFollow_SolveFormation`,
`BattleLocomotion_TestForwardStepClearance`, `BattleLocomotion_TryChooseReachableRandomDetour`,
`0033xxxx` steering helpers, …). This page cites `00203170`; the Movement layer cites it too. Pure
shared-accessor fan-in — no locomotion relationship to these element types.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 18 edges).** 14 edges are the
`0020E600`/`0020E620` image-pointer pair inside this page's step bodies, 3 are `001EDDA0` via
`002F3BC0`/`002F4020`/`00524320`, and the last is `0022B6E0` calling `0053DD10`.

**UI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 10 edges).** `UI.Transform.Evaluator` `00368010` shares `00203170`/
`00397910` (2 edges); `UI.Transform.Keyframed` `002C7B10` shares `0017FFD0`;
`UI.Transform.EvaluatorWithAudio` `0024B9B0` shares `001EDDA0`;
`UI.Geometry.SegmentedTransformRecordInitialization` `003F26F0`, `UI.RadialGeometry.Generation`
`003F2A70`, `003C5500`, `UI.Grid.PackedElementCellLayoutAndRenderOrchestration` `002D28E0` and
`UI.Transform.AudioArm` `002D2600` share `00203170`; `003C80C0` shares `0053DD10`. The UI transform
evaluators use the same generic helpers these element steps cite — fan-in.

`0053A120` (178 B) is the `+0x44 = 0x60`/`0x62` shared creation arm (`005004C0` stubs 33 and 35): `00500470` prelude, then `0042FCF0`x3/`004304F0`x3/`00430AF0`x4 over `+0x80`-`+0x2D0` - the two-type shared field-init ladder this page already names.

Interior anchor `0053A13D` (function `0053A120`).

`0053A060` (178 B) is the `+0x44 = 0x61` creation arm (`005004C0` stub 34): `00500470` prelude, then `0042FCF0`x3/`004304F0`x4/`00430AF0`x3 over `+0x80`-`+0x290` - the trimmed 0x61 sibling this page already names.

Interior anchor `0053A07D` (function `0053A060`).

`0053A5D0` (287 B) is the ~~`+0x44 = 0x65`~~ **`+0x44 = 0x67` (corrected 2026-09-29, FABLE, GI-10: `005004C0`'s table and `members/effect-type-methods.tsv`)** creation arm (`005004C0` stub 38): `00500470` prelude, `0042FCF0`/`004304F0`x8/`00430AF0`x3 over `+0x80`-`+0x5F0`, closed by `00431770` - the eight-group ~~0x65~~ `0x67` setup *(corrected 2026-10-02, OPUS: the arm's type was corrected to `0x67` at the head of this paragraph)* this page already names.

Interior anchor `0053A5FD` (function `0053A5D0`).

`0053A6F0` (150 B) is the ~~`+0x44 = 0x66`~~ **`+0x44 = 0xA0` (corrected 2026-09-29, FABLE, GI-10)** creation arm (`005004C0` stub 39): `00500470` prelude, `0042FCF0`x2/`004304F0`x4/`00430AF0`x2 over `+0x80`-`+0x1F0` - the family's shortest ladder.

Interior anchor `0053A70D` (function `0053A6F0`).

`0053A790` (162 B) is the ~~`+0x44 = 0x67`~~ **`+0x44 = 0xA1` (corrected 2026-09-29, FABLE, GI-10)** creation arm (`005004C0` stub 40): `00500470` prelude, `0020E620`x2/`003AA280`x2 pairs, `0042FCF0`/`004304F0`/`00430AF0`x2 over `+0x80`-`+0x210`.

Interior anchor `0053A7AD` (function `0053A790`).

`0053A840` (191 B) is the ~~`+0x44 = 0x68`~~ **`+0x44 = 0xA2` (corrected 2026-09-29, FABLE, GI-10; `0x68` has no main-range setup)** creation arm (`005004C0` stub 41): `00500470` prelude, `0042FCF0`/`004304F0`/`00430AF0`x3 over `+0x80`-`+0x7E0` - the family's widest field span, closed by `00431770`.

Interior anchor `0053A86B` (function `0053A840`).

*Added 2026-09-29 (FABLE, GI follow-up): the layers the GI answers newly brought into this page's audit.*

**CombatAction — CLIENT (2 edges).** `BattleAction_GetPresentationParameter` (`0030A190`), which this page cites for the word it returns (action-row `+0x24`, or `+0x28` for ids `0xD0`–`0xF1`), is called by the action layer's own bodies `0030C890` and `0030CBE0`, both of which also call `BattleAction_SelectGlobalSequencePresentationEvent`. The action layer reads that presentation parameter for its sequence events; the effect elements on this page consume the same word, so the crossing is a shared reader of one action-row field, not shared ownership.

**Party — SERVICE (1 edge).** The point query `003A56F0` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) on one arm and gives up when it returns 0, so for that target mode the queried point belongs to the player's current focus character. The effect reads the party layer's focus handle; it does not change the focus.

**ActorEntity — SERVICE, MECHANICAL (7 edges).** The registry's 2026-09-14 GENUINELY-IRRELEVANT verdict for this pair covered one edge: the actor state-interpolation body `003F1E90` calling the SIMD helper `00203170`, which is shared math. The GI answer adds six more, all from the point query `003A56F0`: it calls `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`), `ActorHandle_EncodeRegistryEntry` (`003589B0`), `ActorManager_GetRecordByOrdinal` (`00358940`), `Actor_GetWorldPosition` (`00265020`) and two small actor accessors, `00263C30` and `00263FF0`, which are named in the census only — their bodies are the actor layer's pages' scope. The point query turns an actor reference into a world position through the actor layer's handle, record and position accessors; the effect reads actor state and writes none of it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`): the layers pass 22 still reported for this page at HEAD `9a4cd5784`. Every edge was listed in full and the cited function's body was read.*

**Resource — MECHANICAL (7 edges).** `0036A190` (10 B) sets `edx = 1` and tail-jumps to the pool allocation it fronts. That allocation takes `ecx` bytes from the pool whose index sits in a global, and stamps the block header. So it is a general allocation entry, not an effect-bank operation of its own. The same seven Resource bodies call it: `00249210`, `0024A1D0`, `00259DF0`, `0032E7C0`, `00379E90`, `00384420` and `0051ED10`. The `0x6B` sub-steps and those loaders share the allocator and nothing else.

**Script_VM_Native_Bridge — MECHANICAL (18 edges).** Seventeen script-verb bodies call `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`, `mov eax, 1; ret`): `00341840`, `00341F90`, `00345250`, `00346AA0`, `00347660`, `003499C0`, `0034B030`, `0034B8D0`, `0034D740`, `0034EF60`, `0034F770`, `003541B0`, `00354E10`, `00355570`, `0050CCB0`, `0050D1C0` and `00512160`. In `00341840` the call is a gate whose false arm can never run (`00341871`–`00341878`). The one other edge is `00356160` calling `00203170`, which fills 64 bytes at `[rcx]` with four 16-byte image constants, the first of them starting with `1.0f`. The page's `0x70` sub-step uses the same stub, and its sub-walks use the same matrix fill. Both are shared helpers, and no script state reaches the effect elements through them.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-element-types-60-74-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `004B0F60` | 553 B | `004B1190` + 0x5057 | with W = word `02064B0C`, a = float `02064CB0` and b = float `02064CB4`: stores `0x3F000000` to dword `02064B04`, W+1 to word `02064DC8`, W+`0xE0` to word `02064DD8` and a - b to `02064B10`, and returns when word `02064DD0` is W+1; else ANDs `02064DD8` with word `02064B10` and sets `02064DC8` to W+`0x118`; if `02064DD8` is now W and word `02064DD4` is not, it returns, first adding word `02064DCC` minus 1 to `02064DC8` unless `02064DCC` is W; if both are W, it stores q = a/b (`0x7F7FFFFF` if b is 0) to `02064B00`, subtracts trunc(q + float `01E02830`) times b from a (the product to `02064CC0`) and calls the site `004B0F60` + 0x103; then, on that path or when `02064DD8` is not W: if `02064DCC` is not W, it truncates a to an integer in place and, from index `02064DC8`, subtracts the word `+0` of each 16-byte record at `02064E34` (each to `02064DD0`) until the 16-bit remainder is negative, storing the last index to `02064DC8` and the remainder to `02064DD4`; if it is W, it stores r = a/float `02064CB8` (`0x7F7FFFFF` for zero) to `02064B00` and r + float `01E02834` to b, calls the site + 0x1F1 when b is 0 and + 0x203 when negative, and truncates b in place | Interior anchor `004B0F94`; Interior anchor `004B0FC6`; Interior anchor `004B1063`; Interior anchor `004B10C1`; Interior anchor `004B1174` |
| `004B97F0` | 66 B | `004B1190` + 0x566F | returns 1.0 (`01CEBBA8`) in `xmm0` when dword `02064AFC` is 0; otherwise replaces dword `01E02828` with `((v AND 0x3FFFFF) OR 0x1FC00000) * 2` OR bit 0 of `((v >> 18) XOR v) >> 4` (v its old value) and returns the new value as a float in `xmm0` | Interior anchor `004B97F9`; Interior anchor `004B980D`; Interior anchor `004B9817`; Interior anchor `004B9823`; Interior anchor `004B9829` |
| `004B9840` | 46 B | `004B1190` + 0x67D1 | stores the sums of the three floats at `rdx+0`, `+4`, `+8` and the three at `r8+0`, `+4`, `+8` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9844`; Interior anchor `004B9849`; Interior anchor `004B9858`; Interior anchor `004B9868` |
| `004B9870` | 32 B | `004B1190` + 0x6AA1 | stores `xmm1` divided by `xmm2` to the float at `rcx`, except that when `xmm2` compares equal to 0.0 it stores the float `0x7F7FFFFF` (`00900360`) instead | Interior anchor `004B9873`; Interior anchor `004B9882`; Interior anchor `004B9887`; Interior anchor `004B988B` |
| `004B9890` | 55 B | `004B1190` + 0x6C46 | multiplies each of the three floats at `rdx+0`, `+4`, `+8` by 16.0 (`01CEBC84`), truncates them to integers and stores them to the dwords at `rcx+0`, `+4`, `+8` | Interior anchor `004B9894`; Interior anchor `004B989C`; Interior anchor `004B98A0`; Interior anchor `004B98B3`; Interior anchor `004B98C3` |
| `004B98F0` | 21 B | `004B1190` + 0x6FF8 | copies the word at `02064E34` plus `edx * 16` (the 32-bit product sign-extended) to the word at `rcx` | Interior anchor `004B98F6`; Interior anchor `004B98FD`; Interior anchor `004B9901` |
| `004B99D0` | 20 B | `004B1190` + 0x6786 | copies the dword at `02064E34` plus `edx * 16` (the 32-bit product sign-extended) to the dword at `rcx+4` | Interior anchor `004B99D6`; Interior anchor `004B99DD`; Interior anchor `004B99E0` |
| `004B99F0` | 22 B | `004B1190` + 0x6600 | copies the qword at `02064E38` plus `edx * 16` (the 32-bit product sign-extended) to the qword at `rcx+8` | Interior anchor `004B99F6`; Interior anchor `004B99FD`; Interior anchor `004B9A01` |
| `004B9A10` | 22 B | `004B1190` + 0x659C | adds the float at `rdx+0xC` times the float at `r8+4` to the float at `rcx+0xC` | Interior anchor `004B9A15`; Interior anchor `004B9A1B`; Interior anchor `004B9A20` |
| `004B9A30` | 82 B | `004B1190` + 0x6A3D | adds each of the four floats at `rdx+0` to `+0xC` times the float at `r8+4` to the float at the same offset of `rcx` | Interior anchor `004B9A36`; Interior anchor `004B9A3E`; Interior anchor `004B9A52`; Interior anchor `004B9A67`; Interior anchor `004B9A7C` |
| `004B9A90` | 82 B | `004B1190` + 0x6A5B | adds each of the four floats at `rdx+0` to `+0xC` times the float at `r8+8` to the float at the same offset of `rcx` | Interior anchor `004B9A96`; Interior anchor `004B9A9E`; Interior anchor `004B9AB2`; Interior anchor `004B9AC7`; Interior anchor `004B9ADC` |
| `004B9AF0` | 95 B | `004B1190` + 0x6A80 | stores each of the four floats at `rdx+0` to `+0xC` times the float at `r8+0xC`, plus the matching float at `02064B20`, `02064B24`, `02064B28` or `02064B2C`, to the float at the same offset of `rcx` | Interior anchor `004B9AF6`; Interior anchor `004B9AFA`; Interior anchor `004B9B02`; Interior anchor `004B9B41`; Interior anchor `004B9B49` |
| `004B9B50` | 46 B | `004B1190` + 0x655E | stores the element-wise products of the three floats at `rdx+0`, `+4`, `+8` and the three at `r8+0`, `+4`, `+8` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9B54`; Interior anchor `004B9B59`; Interior anchor `004B9B68`; Interior anchor `004B9B78` |
| `004B9B80` | 59 B | `004B1190` + 0x6A1F | stores each of the four floats at `rdx+0` to `+0xC` times the float at `r8` to the float at the same offset of `rcx` | Interior anchor `004B9B84`; Interior anchor `004B9B89`; Interior anchor `004B9B97`; Interior anchor `004B9BA6`; Interior anchor `004B9BB5` |
| `004B9BC0` | 35 B | `004B1190` + 0x65F1 | stores `xmm2` times each of the three floats at `rdx+0`, `+4`, `+8` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9BC6`; Interior anchor `004B9BCA`; Interior anchor `004B9BD3`; Interior anchor `004B9BD8`; Interior anchor `004B9BDD` |
| `004B9BF0` | 47 B | `004B1190` + 0x66B4 | stores each of the three floats at `rdx+0`, `+4`, `+8` times the float at `r8+0xC` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9BF4`; Interior anchor `004B9BFA`; Interior anchor `004B9C09`; Interior anchor `004B9C19` |
| `004B9C20` | 47 B | `004B1190` + 0x67AB | stores each of the three floats at `rdx+0`, `+4`, `+8` times the float at `r8+4` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9C24`; Interior anchor `004B9C2A`; Interior anchor `004B9C39`; Interior anchor `004B9C49` |
| `004B9C50` | 77 B | `004B1190` + 0x6613 | stores 1.0 (`01CEBBA8`) to the float at `rcx` when dword `02064AFC` is 0; otherwise replaces dword `01E02828` with `((v AND 0x3FFFFF) OR 0x1FC00000) * 2` OR bit 0 of `((v >> 18) XOR v) >> 4` (v its old value) and stores the new value to the float at `rcx` | Interior anchor `004B9C64`; Interior anchor `004B9C74`; Interior anchor `004B9C7E`; Interior anchor `004B9C8A`; Interior anchor `004B9C98` |
| `004B9CA0` | 79 B | `004B1190` + 0x7197 | stores 1.0 (`01CEBBA8`) to the float at `rcx+4` when dword `02064AFC` is 0; otherwise replaces dword `01E02828` with `((v AND 0x3FFFFF) OR 0x1FC00000) * 2` OR bit 0 of `((v >> 18) XOR v) >> 4` (v its old value) and stores the new value to the float at `rcx+4` | Interior anchor `004B9CB4`; Interior anchor `004B9CC5`; Interior anchor `004B9CCF`; Interior anchor `004B9CDB`; Interior anchor `004B9CE9` |
| `004B9CF0` | 79 B | `004B1190` + 0x67F3 | stores 1.0 (`01CEBBA8`) to the float at `rcx+8` when dword `02064AFC` is 0; otherwise replaces dword `01E02828` with `((v AND 0x3FFFFF) OR 0x1FC00000) * 2` OR bit 0 of `((v >> 18) XOR v) >> 4` (v its old value) and stores the new value to the float at `rcx+8` | Interior anchor `004B9D04`; Interior anchor `004B9D15`; Interior anchor `004B9D1F`; Interior anchor `004B9D2B`; Interior anchor `004B9D39` |
| `004B9D80` | 171 B | `004B1190` + 0x2D29 | compares the floats at `rdx+0`, `+4`, `+8` (a0, a1, a2) with those at `r8+0`, `+4`, `+8` (b0, b1, b2) and stores to the word at `rcx` the sum of `0x80` if b0 > a0, `0x40` if b1 > a1, `0x20` if b2 > a2, 8 if a0 = b0, 4 if a1 = b1 and 2 if a2 = b2 (an unordered pair adds nothing) | Interior anchor `004B9D99`; Interior anchor `004B9DE7`; Interior anchor `004B9E00`; Interior anchor `004B9E0D`; Interior anchor `004B9E22` |
| `004B9E30` | 41 B | `004B1190` + 0x6539 | stores each of the three floats at `rdx+0`, `+4`, `+8` minus `xmm2` to the floats at `rcx+0`, `+4`, `+8` | Interior anchor `004B9E34`; Interior anchor `004B9E38`; Interior anchor `004B9E45`; Interior anchor `004B9E53` |
| `004B9E60` | 50 B | `004B1190` + 0x7051 | compares the float at `rdx+4` (a) with the float at `r8+0xC` (b) and stores to the word at `rcx` the sum of `0x40` if b > a and 4 if a = b (an unordered pair stores 0) | Interior anchor `004B9E6D`; Interior anchor `004B9E79`; Interior anchor `004B9E82`; Interior anchor `004B9E8A`; Interior anchor `004B9E8E` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-element-types-60-74-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0034B8D0` | 201 B | with `e` = `rdx`: takes `a` = `002E97B0(e)` and calls `00263A30(byte [e+0x15], word [e])`; when `a` and `s` = qword [a+8] are non-null: if `002E4C30(s, 002E9C00(e))` is greater than 0 (signed), calls `002EAC90(e)` and, when byte [e+0xD] is 0x80 or more (unsigned), `002EB380(e)`; otherwise, when `k` = `002E9C00(e)` (called again) and `002EB9D0(s, k)` are both not negative, calls `00314D40(1)` and returns 1; in every other case returns 0 when `0053DD10()` returns non-zero, else calls `0016D6A0(1)` and returns 1 | `0034B8E7`, `0034B8F6`, `0034B916`, `0034B945`, `0034B96D` |
| `0052E270` | 375 B | with `d` = qword [rcx+0x20], `s` = `rcx`+0x230, F(o) = the float `004309C0(d+o, dword [rcx+0x44])` and V(o) = the 16 bytes at `00430B90(&stack, d+o, dword [rcx+0x44])` (the dword read before each call), stores in order: float s+0x58 = F(0x1D0), s+0x80 = V(0x1E0), float s+0x5C = F(0x220), s+0x70 = V(0x230), float s+0x90 = F(0x270), s+0xB0 = V(0x280), float s+0x94 = F(0x2C0), s+0xA0 = V(0x2D0), floats s+0xC0, s+0xC4, s+0xFC, s+0x3C, s+0x9C = F(0x320), F(0x330), F(0x340), F(0x350), F(0x360); then tail-jumps to `0054C440(s)` | `0052E297`, `0052E2B1`, `0052E2F4`, `0052E36A`, `0052E3E2` |
| `0052F400` | 341 B | with `d` = qword [rcx+0x20], `s` = `rcx`+0x230, F(o) = the float `004309C0(d+o, dword [rcx+0x44])` and V(o) = the 16 bytes at `00430B90(&stack, d+o, dword [rcx+0x44])` (the dword read before each call), stores in order: float s+0xA8 = F(0x1D0), s+0x100 = V(0x1E0), float s+0xAC = F(0x220), s+0xF0 = V(0x230), float s+0xB4 = F(0x270), s+0x120 = V(0x280), float s+0xB8 = F(0x2C0), s+0x110 = V(0x2D0), floats s+0xBC, s+0xC0, s+0xD8 = F(0x320), F(0x330), F(0x340); then tail-jumps to `0054DD30(s)` | `0052F427`, `0052F444`, `0052F48A`, `0052F503`, `0052F550` |
| `0054C440` | 621 B | with `c` = `rcx`, `a` = float [c+0xC4], `b` = float [c+0x3C], `t1` = (1 - `a`) times float [c+0xFC] + `a` and `t2` = (1 - `b`) times float [c+0x9C] + `b`: for each i below word [c+0x52], with `p` = qword [c+0x108] + 0xA0 i and only when qword [p+0x30] equals `p`, uses set A when `a` >= float [p+0xC] or `b` >= float [p+0x98], else set B when `t1` >= float [p+0xC] or `t2` >= float [p+0x98] (NaN compares fail), else skips `p`; with (G, A0, A1, A2, V, D) = c's floats (+0x58, +0x80, +0x84, +0x88, +0x70 to +0x78, +0x5C) for A and (+0x90, +0xB0, +0xB4, +0xB8, +0xA0 to +0xA8, +0x94) for B: subtracts float [c+0xC0] times float [c+0x44] times G times A1 from float [p+0x24], adds the new value times G times A1 to float [p+0x74], G times float [p+0x28] times A2 to float [p+0x78] and G times float [p+0x20] times A0 to float [p+0x70], adds V.j times float [p+0x10+4j] times D to float [p+4j] for j = 0 to 2, and calls `0046D560(p+0x40)` | `0054C478`, `0054C4BB`, `0054C50E`, `0054C5D7`, `0054C679` |
| `0054DD30` | 778 B | with `c` = `rcx`, `a` = float [c+0xC0] and `t` = (1 - `a`) times float [c+0xD8] + `a`: for each i below dword [c+0xA4] (unsigned), with `p` = qword [c+0x190] + 0xA0 i, uses set A when `a` >= float [p+0xC], else set B when `t` >= float [p+0xC] (NaN compares fail), else skips `p`; with (K, M0, M1, M2, V, D) = c's floats (+0xA8, +0x100, +0x104, +0x108, +0xF0 to +0xF8, +0xAC) for A and (+0xB4, +0x120, +0x124, +0x128, +0x110 to +0x118, +0xB8) for B: adds -(float [c+0x68] times float [p+0x7C]) times float [c+0xBC] times K times M1 to float [p+0x24]; forms the stack vector `v` = (K float [p+0x20] M0, K (new [p+0x24]) M1, K float [p+0x28] M2), passed through `00202B90(&v, c+0x150, &v)` when byte [c+0x9C] has bit `0x2`, and adds it to floats [p+0x70] to [p+0x78]; adds V.j times float [p+0x10+4j] times D to float [p+4j] for j = 0 to 2 and calls `0046D560(p+0x40)` (stack cookie `01F44830` checked by `00808C40`) | `0054DD7B`, `0054DDB0`, `0054DE42`, `0054DED0`, `0054DFF6` |

### Crossings into other layers - functions this page's newest interior rows name (OPUS, 2026-10-03)

- **CombatAI - SERVICE (1 edge).** `002E9C00` is also called by `003014C0`, filed to combatai - shared machinery across the layer boundary, no shared ownership.
