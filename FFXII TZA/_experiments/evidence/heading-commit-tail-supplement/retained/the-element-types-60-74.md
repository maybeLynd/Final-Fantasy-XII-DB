---
system: the element types 0x60-0x74
category: 17-Presentation-Rendering
status: PARTIAL — all step/update tails (0045C450, 0045CDC0, 0045D7D0, 0052A8B0 and peers) and 00431770 are not read
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
| `0044B960` | shared PRNG — xorshift-style bit chain over state dword `01EF93E8`, gated by guard dword `022D9138`; called inside the step bodies of `0x0A`, `0x60`–`0x62`, `0x65`, `0x66` before the type tail |
| `003A3E20` | element field setter: `+0x44 = 0xFFFFFFFF`, `+0x42 = dx` (12 B, `0x65`/`0x66` steps) |
| `0024DDD0` | reads global object `+0x13B` byte and calls `003A3FD0`/`003A6BA0` storing two results — config-indexed double lookup (`0x67`, `0x6B` steps) |
| `0024B1C0` | **deferred-free queue**: if count word `02092168` < `0x100`, appends `rcx` to the qword array at `02091150` and increments; else `jmp 003697F0` (immediate free). The `0x6B`/`0x73`/`0x74` sub-seventh entries are wrappers that push element fields (`+0x338`-family) onto this queue — resource release at element teardown |
| `005C5230` | `xor eax,eax; ret` — the shared return-0 stub (page's "null path" confirmed) |
| `0016D6A0` | `_guard_check_icall` — `ret 0`; used as a no-op method slot |
| `0053DD10` | `InputDevice_QueryAvailabilityState_Always1` — `mov eax,1; ret`; as `0x70`'s sub-step simply returns true |

## `0x60` / `0x61` / `0x62` — one family

`0x60` and `0x62` share setup `0053A120`; `0x61` has `0053A060` (a trimmed
variant, not the same shape). All three steps are 87 B = base stepper + PRNG
`0044B960` + own tail (`0045C450` / `0045CDC0` / `0045D7D0`, all `not read`);
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
of **nine** 4-track groups `+0x1C0`–`+0x460`, `00431770@+0x490`, record end
`+0x5F0`. Step `0045FD50`
(968 B — a real body, not a wrapper): calls `0024DDD0` (config-indexed lookups),
`0036A190`/`0036C140`/`0036C1D0` (bank ops), `00532EF0`, tail `0045F600`, then
`004607C0` — and also invokes the seventh dispatcher `002F31C0` itself. Its own
seventh `00460120` (80 B) calls `003697F0` and touches `+0x338`/`+0x3B0`/`+0x3C0`/
`+0x3D0` — teardown of three owned resources.

## `0x68`–`0x6B` — first sub-range cluster

Sub-steps all call base `002F2D60` plus `003A3E20`/`003D8E50` and own tails
(`00523380`/`00524320`/`005263F0`/`00529D50`, `not read`); sub-updates are the
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
  stride `+0x1C0`–`+0x3F0` plus 12 singles and three `00431770` inits
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
tails (`0052A8B0`/`0052B5E0`/`0054C6B0`/`0054E040`, `not read`); `0x72`–`0x74`
also call `00861EBA`. Sub-walks share one call family (`0026EE00`/`002F1F40`/
`0042FDB0`/`004309C0`/`00430B90`/`004314E0`/`00431830`, `0x71`/`0x72` add
`00434900`, `0x73`/`0x74` add `0017FFD0`/`00202D70`/`00203170`/`0024E460`/`0024E640`).

Records are the largest yet — `0x72`/`0x73`/`0x74` carry a `0x50`-stride run of
**nine** 4-track groups (`+0x120`–`+0x3F0` for `0x72`; `+0x90`/`+0xE0`/`+0x130`
start for `0x73`/`0x74` then group runs at `+0x190`–`+0x480`), 14–20 single heads,
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

**Not read (explicit):** all step/update tails (`0045C450`, `0045CDC0`,
`0045D7D0`, `0045E3C0`, `0045F140`, `0045F600`, `004607C0`, `00523380`,
`00524320`, `005263F0`, `00529D50`, `0052A8B0`, `0052B5E0`, `0054C6B0`,
`0054E040`); `00431770` still `not read` (third-variant init used at `0xF0`
stride); the walk emit tails `003970A0`, `00399600`, `0039A9B0`, `003A33B0`,
`003A34D0`, `0039ADE0`, `00202B70`, `00202D50`, `00202D70`, `00203170`,
`0024E460`, `0024E640`, `00462260`, `00540F40`, `00434900`, `0036A190`,
`0036C140`, `0036C1D0`, `00532EF0`, `003697F0`, `0017FFD0`, `003D8E50`,
`003A6E60`, `00541E00`/`00542060`/`005439A0`/`005450E0`/`00545120`/`00547DD0`/
`0054A9C0`, `00808C40`, `00861EBA`. **No player-facing names assigned** — the
emitter call identity still unread.

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

`0053A5D0` (287 B) is the `+0x44 = 0x65` creation arm (`005004C0` stub 38): `00500470` prelude, `0042FCF0`/`004304F0`x8/`00430AF0`x3 over `+0x80`-`+0x5F0`, closed by `00431770` - the eight-group 0x65 setup this page already names.

Interior anchor `0053A5FD` (function `0053A5D0`).

`0053A6F0` (150 B) is the `+0x44 = 0x66` creation arm (`005004C0` stub 39): `00500470` prelude, `0042FCF0`x2/`004304F0`x4/`00430AF0`x2 over `+0x80`-`+0x1F0` - the family's shortest ladder.

Interior anchor `0053A70D` (function `0053A6F0`).

`0053A790` (162 B) is the `+0x44 = 0x67` creation arm (`005004C0` stub 40): `00500470` prelude, `0020E620`x2/`003AA280`x2 pairs, `0042FCF0`/`004304F0`/`00430AF0`x2 over `+0x80`-`+0x210`.

Interior anchor `0053A7AD` (function `0053A790`).

`0053A840` (191 B) is the `+0x44 = 0x68` creation arm (`005004C0` stub 41): `00500470` prelude, `0042FCF0`/`004304F0`/`00430AF0`x3 over `+0x80`-`+0x7E0` - the family's widest field span, closed by `00431770`.

Interior anchor `0053A86B` (function `0053A840`).
