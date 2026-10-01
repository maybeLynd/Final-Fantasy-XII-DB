---
system: The per-model oscillator subsystem (the 0040ACF0 family)
category: 17-Presentation-Rendering
status: PARTIAL — which pose slot each evaluator owns is not established; the 0x290 records named 2026-09-18 as the skeleton's bone records (the Skeleton_* family strides them)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 86 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-oscillator-pass-1 - ten claims attacked by decoding the image at GN160 and ALL TEN SURVIVED, including the two the page's structure rests on - the reload of ecx from [r14] at 003E0010 rather than from the 0020E600 result, and 0040ED80 being a 5-byte thunk whose whole body is `and byte ptr [rcx+0x3f], 0xf ; ret`. Body extent, the 0036D9E0 bank clear at 003DFFE9, the nibble split, the 02B59D60 flag global, both tail targets, the driver pair, the 003705F9 call site and both callers all hold. No correction
  crossref_clean: false
  reopened_count: 0
---

# The per-model oscillator subsystem (the `0040ACF0` family)

*Player-facing: this is the machinery that makes parts of a model keep moving on their own once the
skeleton pose is final — cloth, hair and hanging gear that sway instead of freezing with the
animation. The engine keeps a per-model list of oscillator entries; every frame the skeleton pass
advances each entry's phase by a randomized speed, works out how far each node has moved, and writes
the result through the VU0 register bank as node matrices.*

## 1. Where it runs

`Skeleton_UpdateFinalPoseAndCombatLook` (`003703A0`) calls `003DFFE0` at `003705F9` with the
skeleton-side record in `r14` (`[r14]` is an encoded id, `+0x5E`/`+0x60`/`+0x63` carry the
oscillator's per-frame controls). `003703A0` itself is called by
`CharacterRenderRecord_UpdateSkeletonFinalPose` (`004242B0`) and
`SkeletonModelGroup_UpdateFinalPoses` (`0046E0F0`) — the subsystem sits inside the final-pose
composition, after motion and before the draw record is consumed.

`003DFFE0` (`003DFFE0`–`003E00BF`):

1. clears the VU0 register bank through `0036D9E0` (`003DFFE9`);
2. resolves `[r14]` via `0020E600`; a null result or a zero byte at `[obj + 6]` early-outs —
   the zero case tail-jumps to `0040ED80`, a 5-byte thunk that touches the record's `+0x3F`
   flags (`003E00AE`–`003E00B4`);
3. runs `0040EE70` on the **raw `[r14]` field** — `ecx` is reloaded from `[r14]` at `003E0010`,
   not the `0020E600` result, and `0040EE70` reads/writes `[rcx+0x3F]` directly — so `[r14]` is
   itself a pointer to the `+0x3F`-flagged record while `0020E600` maps it to a separate object
   checked at `+6` (`003E000B`–`003E002C`);
4. if `[r14 + 0x60]` is nonzero it runs `0040F390(obj)` (entry init/reset) then
   `0040D890(obj, count)` (the sub-stepped driver), then zeroes `+0x60` (`003E0031`–`003E0065`);
5. composes the flag word `dx = [r14 + 0x63] | [02B59D60]` and the two nibbles
   `r8 = [r14 + 0x5E] & 0xF`, `r9 = [r14 + 0x5E] >> 4`, and tail-jumps to
   `0040ACF0(obj, dx, r8, r9)` (`003E0067`–`003E00A9`).

*Placed 2026-09-19 (FABLE):* the *skeleton-side record* in `r14` is the character's **rig**, and this subsystem is its
**controller 0** - [the rig of seventeen controllers](../Character-Render-Records/the-rig-of-seventeen-controllers.md).
The `+0x5E` / `+0x60` / `+0x63` controls are rig fields; `+0x60` is the word the rig's rebind sets to 30, which step 4
below spends as the sub-step count after a reset - thirty steps of sway run at once. That this is there to let a newly
bound character's cloth settle before it is seen is inference.

## 2. The oscillator record

`rdi` inside `0040ACF0` / `0040D890` / `0040F390` is one record (owner type not named — it is
always reached through the `[r14]` encoded-id resolve). Fields read this pass:

| Offset | Type | Use |
|---|---|---|
| `+0x00` | u32 | encoded id resolved by `0020E600` → the `0x30`-stride entry array (`0040AEC1`–`0040AED0`) |
| `+0x04` | u8 | entry count |
| `+0x05` | u8 | if set, `+0x0C` is resolved and *its* `[0]` resolved again before proceeding (a parent indirection, `0040AD0E`–`0040AD28`) |
| `+0x0C` | u32 | parent id (only when `+5` set) |
| `+0x10` | f32 | bank row `022D9390` (VU vector row 31) gets the whole `+0x10` xmmword; `1.0f / [+0x10].x` goes to Q `022D9198` and accumulator `022D9394` (`0040AD28`–`0040AD97`) |
| `+0x1C` | s32 | stored to `022D8FB0`, then the 16-byte row `022D8FB0` is copied to `022D9350` (`0040AD63`–`0040AD88`) |
| `+0x20` / `+0x24` | f32 | phase / speed pair, **global-parameter pair**: advanced only while `02CA4390` is set; wraps at 2π (`009002E0`), raises `+0x3F` bit 0, then speed is re-drawn `+0x24 = 003D8E50([02CA439C]) + [02CA4398]` and amplitude `+0x28 = 003D8E50([02CA4384]) + [02CA4380]` (`0040AE4E`–`0040AEC1`) |
| `+0x2C` | u32 | id → per-record param record `{+4,+8,+0xC,+0x10}` used for the per-record speed re-draw below |
| `+0x30` / `+0x34` | f32 | phase / speed pair, **per-record**: advanced while `+0x3E` is set; wraps at 2π, raises `+0x3F` bit 1, then `+0x34 = 003D8E50(param[+0x10]) + param[+0xC]`, `+0x38 = 003D8E50(param[+8]) + param[+4]` (`0040ADB3`–`0040AE4E`) |
| `+0x38` | f32 | second amplitude re-drawn with `+0x34` |
| `+0x3E` | u8 | per-record phase enable |
| `+0x3F` | u8 | flags: bit0/bit1 = phase-wrap re-draw latches (consumed same frame), bit4 tested at `0040AFE3`, low nibble cleared by `0040F390` |

Each `0x30`-byte entry (`rbx` in the loop at `0040AF00`):

| Offset | Type | Use |
|---|---|---|
| `+0x00` | u8 | sub-entry count read by `0040FF30`/`0040DBB0`-family walkers |
| `+0x02` | u8 | enable — zero skips the entry (`0040AF13`) |
| `+0x08` | u32 | id → sub-object whose `+0x28`-array / `+4`-count the heavy stages walk |
| `+0x20` | f32 | blend factor `t`: `0040F390` initializes it to `1.0` if `+0x2A` bit0 else `0`; `0 < t < 1` selects the blend apply `0040B780`, otherwise `0040DBB0` (`0040B0E3`–`0040B10A`) |
| `+0x24` | u32 | id consumed by stage 2 (`00413C80` resolves it) |
| `+0x29` | u8 | flags: low nibble cleared each pass; bit4 receives `+0x2A` bit0 (`0040AF00`–`0040AF10`); nonzero low nibble enables the blend/`0046FAE0` path (`0040B0B1`) |
| `+0x2A` | u8 | bit0 — "apply directly" flag: selects `0040DBB0` when the low nibble path is off, and gates the sub-stepped apply in `0040D890` |

## 3. Per-frame state machine (`0040ACF0`)

After the bank stores and phase advance, the loop at `0040AF00`–`0040B138` walks every enabled
entry and picks one of three cost tiers:

- `001EDE70` (HALFRATE) is tested first (`0040AF1D`); **halfrate-false** jumps straight to
  `0040B06F`. On the **halfrate-true** path the mode byte `esi` is computed first — `1` when the
  flag word `bp` is nonzero else `2`, forced to `0` when `[record + 7]` is set while `02B59D68`
  is zero (`0040AF2A`–`0040AF45`) — then the 60 fps exception list `001EDCD0` is consulted on
  `02EBB750 + 0x3C` (`0040AF48`–`0040AF5A`): **exception-listed** entries take the mode dispatch
  at `0040AF60`; **not-listed** entries take the `0040AFE3` gate below.
- On the exception-listed dispatch: mode **1 is the null tier** — `esi == 1` skips both the
  scope-open `00415EE0` (`0040AF60`–`0040AF64`) and the stages plus post-step (`0040AFA7`–
  `0040AFAA`). Mode **0** runs the light stage `00413340(record, entry)` then post-step
  `00416AD0(entry, scratch)` (`0040AF8A`–`0040AF9D`); mode **2** runs the heavy triple
  `0040FF30 → 00413C80 → 00411650` (all `(record, entry)`) then `00416AD0` (`0040AFB0`–
  `0040AFD9`). The `00415EE0` scope-open (`0040AF65`–`0040AF85`, storing shared table
  `01FD4A90` to `02CA43C0`) runs for modes 0 and 2 only.
- On the not-listed path (`0040AFE3`): record `+0x3F` **bit4 set** drops only the
  `00415EE0` scope-open and the `00416FB0` post-step — it joins `0040B06F`, where
  `[record + 7]`-or-`02B59D68` still selects `00413340` and `bp == 0` still selects the heavy
  triple (`0040B08B`–`0040B0AC`). **bit4 clear** runs the same `[record + 7]`/`bp` selection
  wrapped by `00415EE0` before and `00416FB0` after (both still skipped when `esi == 1`;
  `0040AFED`–`0040B06D`). `00416FB0` sets `r15`, causing a closing `00415EE0(entry, scratch, 0)`
  at `0040B10F`–`0040B124`.

After the tier dispatch, when the entry's `+0x29` low nibble is nonzero:

- `0046FAE0(entry, mode', nibble_hi)` runs with `mode'` remapped from the `r8` nibble:
  `0 → 0`, `1 → 2`, `2 → 1`, `>= 3` skips the call (`0040B0B7`–`0040B0E3`);
- `t = [entry + 0x20]`: `0 < t < 1` calls the blend apply `0040B780(record, entry, t)`;
  `t >= 1` falls to `0040DBB0`. When the low nibble is zero, `+0x2A` bit0 alone selects
  `0040DBB0` (`0040B0FE`–`0040B10A`).

`0040D890` is the same record shape driven differently: it repeats the whole phase-advance plus
an unconditional heavy-triple pass over all entries `esi` times (`esi` = the `[r14 + 0x60]` count
passed by `003DFFE0`), and calls `0040DBB0` only on the pass where the counter equals `0xB` and
`+0x2A` bit0 is set (`0040DA45`–`0040DAC8`). This is a sub-stepped variant — the heavy math runs
once per sub-step but the node apply happens on one fixed pass.

## 4. What the apply writes — the H1 verdict

`0040DBB0` resolves a four-deep id chain per entry — `[entry + 8]` → object → `[obj + 4]` →
object → `[obj]` → object — and walks a `0x290`-stride record array indexed by a u16. From each
`0x290` record it loads four xmmword rows at `+0x80`–`+0xB0` straight into **VU vector rows 1–4**
(`022D91B0`–`022D91E0`, `0040DC93`–`0040DD2D`) and a second 4×4 at `[sub-obj + 0x150]`–`+0x180`
into rows 5–8 (`022D91F0`–`022D9220`, `0040DE9E`–`0040DEEF`), computes a position delta
`022D9340 − 022D9330 → 022D9310` (`0040DDDA`–`0040DE4A`), reloads vf00 through `0036DD80` and
continues the transform. `0040B780` has the same skeleton with the blend weight from `xmm2`
(`0040B7AA`).

**H1 confirmed**: the outputs are node matrices and delta vectors pushed through the VU0 register
bank — geometry transform work, not light vectors or colour data. No store to a light/slot array
appears anywhere in the apply heads, and the `0x290` records carry four-row matrices at `+0x80`.
H2 (per-model lighting from the weather sun) is unsupported by anything read. The oscillation
inputs are the two phase pairs of §2, whose speeds are re-drawn from `003D8E50` — the same
perturbation helper the weather system uses — which is the concrete mechanism behind wind/gust
sway. What the `0x290` records are *named* (node vs bone vs attachment) is not established; the
four-deep resolve chain's intermediate object types are likewise unnamed.

## 5. The parameter-install path (`0054B1F0`)

`0054B1F0(obj, float params, flags, flags)` — called from `0052B5E0` and `0052BBD0` (both
frontier Presentation bodies) — is the API that arms an oscillator:

1. `[obj + 0x148]` is the oscillator record pointer (`r14`); it resolves `[r14]` → object →
   `[obj + 8]` → the entry-array header `rsi`, then runs `004158F0(record, 1.0)` (`0054B208`–`0054B23F`);
2. copies `params[+0x10]` into `rsi + 0x30`/`+0x38` (`0054B240`–`0054B249`);
3. if the arg triple `params[0]/[4]/[8]` differs from the resolved `[rsi + 4]`-record's
   `+0x3C`/`+0x4C`/`+0x2C`, rewrites them into every `0x50`-stride sub-entry (`+0x3C`, `+0x40`,
   `+0x4C`, `+0x2C`) (`0054B25B`–`0054B2B5`);
4. compares `params[+0xC]` against a third resolved record's `+0x18` and rewrites the
   `0x20`-stride tail entries when different (`0054B2B5`–`0054B2F5`);
5. writes `params[+0x18]`'s `[0]/[4]/[8]` into the record's global pair `+0x20`/`+0x24`/`+0x28`
   — the fields §2 showed the `02CA4390`-gated phase advance uses (`0054B2F5`–`0054B338`);
6. runs `0040AA20(record)` once, again if `flags2 && !001EDDA0()`, then
   `0040FEF0(record, resolved)` — one synchronous heavy-triple pass — unless
   `!001EDDA0() && !flags2 && (flags & 1)` (`0054B339`–`0054B379`).

`001EDDA0` is a second frame/validity gate in the same family as `001EDCD0`/`001EDE70`.

## 6. Members and honest limits

`members/model-oscillator-subsystem.tsv` lists all 36 members with per-function evidence level.
Roles above are read from bodies at the stated addresses; the four heavy stages
(`0040FF30`, `00413C80`, `00411650`, `0040B780`) are translated VU0 assembly read at head +
call-shape level only — their inner loops resolve sub-entries through `0020E600` and stream
through the bank, but the per-sub-entry math is not walked instruction-by-instruction.

Not established this pass:

- the owner type of the `0x40`-byte oscillator record; ~~and the `0x290`-stride node records~~ — **the `0x290` records are the skeleton's bone records (named 2026-09-18, FABLE, by cross-reference):** [the render-event selection evidence](../Character-Render-Records/render-event-selection-evidence.md) walks the same `0x290` array as *bone records*, and every listed function that strides by `0x290` is a skeleton body — `Skeleton_UpdateFinalPoseAndCombatLook` `003703A0`, `Skeleton_ComposeFinalPose` `00373860`, `AddMotion_ApplyBonePose` `003714A0`, `RelationLook_ApplyBoneMatrices` `00514F20`, `Skeleton_ResetConfiguredAdditiveBoneMatrices` `003E3C30`, `SkeletonModelWork_PropagateParentSecondaryTransforms` `00373F40` — so the four-row matrix at `+0x80` is a bone's pose matrix and the apply pushes bone poses, not attachment or node transforms;
- who writes `02CA4380`–`02CA439C`, `02B59D60`, `02B59D68`, and what arms `02CA4390`;
- `0054B1F0`'s two callers `0052B5E0` / `0052BBD0` (frontier Presentation bodies — the weather
  or script site that supplies the params is not identified);
- `0040F390`'s deeper fields beyond the `+0x20`/`+0x29`/`+0x3F` init seen in its head.

## 6a. The `003703A0` exclusive subtree — the final-pose call tree

The exclusive-callee census (FABLE `exclusive_subtrees.tsv`) assigns 55 frontier functions to
`Skeleton_UpdateFinalPoseAndCombatLook` — the largest cited subtree in the program. All were
signature-swept 2026-09-15 (`bshape.py`); the `0040xxxx` band is §3–§6's family, and the rest
decompose into four further clusters:

| cluster | members | role |
|---|---|---|
| cutscene-gate helpers | `001ED0D0`, `001ED1E0`, `001EDCD0` | the shared `001EC560` gate + `01DFE40C`/`01F832B0` actor-state reads; `001EDCD0` is the `02EBB750`-object entry the driver uses (§7) |
| combat-look internals | `00372610` (245 B — `00202FE0` ×4/`00202D70` ×3 over the `02AD9E40`–`02AD9E80` bank), `00373860` (1,170 B — `0020E600` ×7 + the `00202C70`/`00202D70`/`00202FE0`/`00203170`/`00202B10`/`00202D80` helper set, `022C6F28` + `02AD9Exx`) | the combat-look half of the function's name — consumers of the `02AD9Exx` bank family §4's mapping read indexes |
| trig evaluators | `00380260` (`sqrtf` ×2), `00380410` (`sinf`-thunk ×3 + `00861F56`) | per-node angle math shared by `0040B780` and the pose family |
| master pose evaluator | `003E00C0` (1,631 B — `0020E600` ×99 plus ~30 stage calls across the `0047xxxx`/`0051xxxx` band; reads `02B59D60`/`64`; interior verified 2026-09-17, SWE2-FRONTIER — `0020E600` resolve + `0036D9E0` at [`003E00D5`](../../_index/ADDRESS-INDEX.md)/`003E00DD` head the entry loop) | the per-model fan-out: resolves every sub-entry, then invokes the slot evaluators in order |
| `0040xxxx` oscillator band | `0040ACF0`, `0040B180`, `0040B780`, `0040D890`, `0040ED80`, `0040EE70`, `00413340`, `00415EE0`, `00416270`, `00416450`, `00416600`, `004167C0`, `00416910`, `00416AD0`, `00416BE0`, `00416FB0` (16) | §3–§6 — already documented |
| step driver | `003DFFE0` | §3's oscillator gate + flag composition — the member the driver calls at `003705F9` |
| segment-pose evaluators | `00471150`, `00471230`, `004713A0`, `004716A0`, `004717E0`, `00471B60`, `00471E40`, `004723E0`, `00472970`, `00472CD0` (10) and `005121A0`, `005124D0`, `00514F20`, `00515660`, `00516220`, `00516970`, `00517650`, `005186A0`, `005188C0`, `00518D50`, `00518F50`, `00519170`, `00519880`, `00519B60`, `0051A280`, `0051A3C0`, `0051A890`, `0051AA30`, `0051B150`, `0051B330` (20) | the slot evaluators `003E00C0` fans out to. Shared signature: `0020E600` ×N resolves + reads of two parallel banks — `01EF93F0`/`F4`/`F8`/`FC` (runtime pose slots) and the `022D91A0`–`022D9270` baked-parameter region (window varies per evaluator: `00517650` reads `022D91A0`–`022D91EC` plus `022D9240`–`022D9270`, `005186A0` reads `022D9200`–`022D9220` at `0x10` stride). `00519880` (408 B, zero calls) is the family's only call-free leaf. Sizes 140 B–4,173 B (`00517650` largest — `003D8E50` ×5 + `003A6E60` ×2) |

Not established this pass: which pose slot each `0051xxxx`/`0047xxxx` evaluator owns (the
`01EF93Fx`/`022D91xx` bank offsets are the only discriminator seen), and whether `003E00C0`'s
call order is a bone-hierarchy walk or a slot table.

## 7. Key addresses

| Address | Role | Read? |
|---|---|---|
| `003703A0` | `Skeleton_UpdateFinalPoseAndCombatLook` — callsite at `003705F9` | named |
| `003DFFE0` | oscillator gate + flag composition | ✅ full body |
| `0040ACF0` | per-frame driver | ✅ full body |
| `0040D890` | sub-stepped driver twin | ✅ full body |
| `0040F390` | entry init/reset | ◐ head + shape |
| `0040FEF0` | heavy-triple wrapper | ✅ full body (53 B) |
| `0054B1F0` | parameter-install API | ✅ full body |
| `0040FF30` / `00413C80` / `00411650` | heavy stages 1–3 | ◐ head + call shape |
| `00413340` | light stage | ◐ head + call shape |
| `00415EE0` / `00416AD0` / `00416FB0` | scope / post-step pair | ◐ call-site roles |
| `0040B780` / `0040DBB0` | blend / direct node apply | ◐ head + store map |
| `0040AA20` / `0040AAD0` | param setup | ◐ call shape |

### Data addresses

| Address | Kind | Contents |
|---|---|---|
| `009002E0` | `.rdata` f32 | 2π phase wrap (verified `0x40C90FD0`) |
| `01FD4A90` | `.data` ptr | shared table stored to `02CA43C0` by mode-1/0 arms |
| `02B59D60` | `.data` u16 | flag word OR'd into the driver arg |
| `02B59D68` | `.data` u32 | global override tested beside `[record + 7]` |
| `02CA4380`–`02CA439C` | `.data` f32 ×4-ish | global base/amplitude params gated by `02CA4390` |
| `02CA43C0` | `.data` ptr | per-frame shared table install |
| `02EBB750` | `.data` ptr | object whose `+0x3C` feeds `001EDCD0` |
| `022D9198` / `022D9390` / `022D8FB0` / `022D9350` | `.data` | VU0 bank rows Q / row 31 / staging — see the-ee-and-vu0-register-bank §6 |

*SWE2-FRONTIER `FABLE-REQ-SWE2-FRONTIER-MODEL-OSCILLATOR-0040`, 2026-09-15. Evidence:
NATIVE/STATIC reads of the cited bodies against the shipping image; FABLE's `0040ACF0` sketch
verified and refined (the `+0` field is an encoded id resolved by `0020E600`, the `+0x10` scalar
is `1/x` into Q, and `0040D890` is a sub-stepped twin, not a separate record type).*

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`, decoding
with capstone; callers taken from the committed call graph. Instrument:
`Tools/work/OPUS/falsify_oscillator.py`. **Ten claims attacked, ten survived. No correction.**

| claim | the killer | result |
|---|---|---|
| `003DFFE0` spans `003DFFE0`–`003E00BF` | the census giving a different length | **survived** — 224 B, exactly the implied extent |
| clears the VU0 bank through `0036D9E0` at `003DFFE9` | no such call at that address | **survived** — `call 0x36d9e0` |
| `0040ED80` is a **5-byte** thunk touching `+0x3F` | a different size, or no `+0x3F` | **survived** — 5 B, and its entire body is `and byte ptr [rcx + 0x3f], 0xf ; ret` |
| `ecx` is reloaded from `[r14]` at `003E0010`, **not** from the `0020E600` result | that address not being such a load | **survived** — `mov ecx, dword ptr [r14]` |
| `r8 = [r14+0x5E] & 0xF`, `r9 = [r14+0x5E] >> 4` | no `+0x5E` read, no `0xF` mask, or no shift by 4 | **survived** — all three present |
| `dx = [r14+0x63] \| [`02B59D60`]` | the global unreferenced, or `+0x63` never read | **survived** |
| tail-jumps to `0040ACF0`, zero case to `0040ED80` | either target absent | **survived** — and those are the **only** two |
| `[r14+0x60]` nonzero runs `0040F390` then `0040D890` | either call absent | **survived** |
| `003703A0` calls `003DFFE0` at `003705F9` | that address not being such a call | **survived** |
| `003703A0`'s callers are `004242B0` and `0046E0F0` | either missing from the call graph | **survived** — and the graph holds **exactly** those two |

> **The two that matter most both held.** The page builds a structural conclusion on the reload at
> `003E0010` — that `[r14]` is itself the `+0x3F`-flagged record while `0020E600` maps it to a
> different object checked at `+6`. **If that instruction were the `0020E600` result instead, the
> conclusion would go with it.** It is not. And `0040ED80` is claimed as a *5-byte* thunk: a size in
> bytes is the cheapest claim in the world to get wrong, and it is exactly 5, with a body that does
> precisely what the page says and nothing more.

**Not attacked by this pass:** the record's field semantics in §2 beyond the offsets being read —
the `0x30`-stride entry array, the VU bank row assignments, and the Q-register reciprocal are cited
but not independently re-derived here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — CLIENT.** `BattleAction_FindApproachGeometryAroundTarget`, owned by that layer, calls `00203170` on this page. That caller is the approach-geometry search: a `0x160`-byte frame with a stack cookie, working from the caller's `[rcx]` and `[rcx+8]` pair; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (11 edges through 2 of this page's functions).** The Input layer reaches this page at `0022A770`, `001EDE70`. `InputGameplay_ArbitrateDigitalInputAndModalState` is the worked example, read in full - it is the input arbitration, in a `0x118`-byte frame with a stack cookie: it refreshes state only when `byte[02092750]` is not already **3**, and gives up early when the modal query answers non-zero; **1 of the 11 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0022A770` on this page calls `PartyFocus_CommitPendingPackedActorHandle_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00358BC0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `004242B0` on this page calls `ResourceTable_ResolveEntryByIndex`, owned by that layer. What it reaches is the paged resource-table lookup, and it gives the whole shape: the index selects a `0x10`-byte slot in one table and, shifted right by `byte[+0x4C]`, a `0x20`-byte group in another; a `-1` slot resolves to nothing, and everything else lands at the group's base plus `(index & dword[+0x50]) * dword[+0x48]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**StoryEvent — CLIENT.** `FUN_001ed240`, owned by that layer, calls `001EC560` on this page. That caller is a 2,192-byte cutscene-override table: it matches the current area id against hard-coded values such as `0xD70` and `0xD48`, the story-progress word selected by `[01DFE40C]` out of `01F832B0` against a step number, the model's name against string literals such as `g0999` and `c1004`, and the animation time against a window, returning a small override index when all four agree; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (19 edges through 7 of this page's functions).** The UI layer reaches this page at `00203170`, `00202C70`, `00202B10`, `001EDDA0` and 3 more. `FUN_0024b9b0` is the worked example, read in full - it is a 1,500-byte routine whose second argument being **8** short-circuits it to a single arm before any of the rest runs; **3 of the 15 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 69 edges).** 60 edges are the image-pointer fixup
pair `0020E600` (52) / `0020E620` (8) inside this page's 55 oscillator subjects; `001EDE70` (3),
`001EDE80` (1), `001EDDA0` (1) callees; `0022A770`/`001EC760`/`00265860`/`00265880` frame callers.
Relocation infrastructure, not scheduling.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 52 edges).** All 52 edges are Movement bodies sharing the page's
four cited accessors `00202B10`/`00202C70`/`00202FE0`/`00203170`: `PartyFollow_SolveFormation`,
`BattleLocomotion_TestForwardStepClearance`, `BattleLocomotion_TryChooseReachableRandomDetour`,
`Navigation_CheckParallelClearanceRoutesXZ` and ~20 `0033xxxx` steering/locomotion bodies. Pure
shared-accessor fan-in.

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 5 edges).** Audio bodies share the cited helpers; no audio
relationship to the oscillator.
## An authored command blows the sway: command `0x3F` (FABLE, 2026-09-20)

*Three bodies read whole - the handler `00520510` (147 B), its deferred callback `00520E90` (361 B) and the oscillator
routine `0040ABF0` (241 B); counts from the authored-command census.*

The per-record half of an oscillator - the pair this page describes as advanced "while `+0x3E` is set" - is switched
by the animation. Authored command `0x3F`
([the authored-command page](../Authored-Commands/the-authored-presentation-command-handlers.md)) acts only on a root
render record (its word `+6` is -1) and posts a callback across the record's hierarchy with a **preset** (command word
`+2`; `0xFFFF` clears the id), an id and a flag (word `+0x10`: low twelve bits, bit 15) and a **direction** (three
floats `+4`..`+0xC`). For each record the callback resolves the resource entry, its rig
([the rig](../Character-Render-Records/the-rig-of-seventeen-controllers.md)) and the rig's controller 0 - this
object - and calls `0040ABF0(object, preset, &direction, id, flag)`:

- `+0x3E` := the preset - **0 switches the per-record sway off**;
- `+0x40` := the direction, and `+0x50` := its horizontal perpendicular (the cross product with the up vector,
  normalised);
- `+0x2C` := the preset's parameter block, `01EFFA30 + (preset - 1) x 0x20` - the block the per-record pair's speed and
  amplitude re-draws read;
- `+0x3C` := the id, `+0x3F` bit 3 := the flag, bit 1 raised so the pair re-draws at once.

It is authored 3,108 times, in `ability_ready`, `magic_ready` and `magic` blocks of party members, NPCs and summons:
**a directed sway while casting** - robes and hair blown along an authored direction. *"Blown" is a reading of where it
is authored and what it sets; what the presets look like was not examined.*

`00416AD0` (260 B) is the three-pass record merge `0040ACF0` runs: pass 1 copies `byte[rsi]` `x 0x40` records from the `[rsi+8]` array into `[r15+8]` via `00416BE0`; pass 2 blends `byte[rsi+7]` `x 0x60` records at `+0x28` as `dst = dst x 0.5f + src x 0.5f` (`01CEBB70`); pass 3 resolves both `+0x24` arrays per `byte[rsi+0x28]` entry - the half-weight blend the controller applies between two record sets.

Interior anchor `00416B0B` (function `00416AD0`).

`00518D50` (259 B) is the bone-record stamp `003E00C0` runs: `[rcx+0x30]`/`+0x40`/`+0x50` copy into the `022D91B0`/`022D91C0`/`022D91D0` globals, then per `dword[rbx+4]` child (`[rbx+0xC]`-indexed, doubly `0020E600`-resolved) it writes the three globals plus a zero vec4 (`01EF93F0`) into `[child + id x 0x290 + 0x230..0x260]` - the four-vector block every listed `0x290` record receives.

Interior anchor `00518D85` (function `00518D50`).

