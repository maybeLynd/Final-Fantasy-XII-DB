---
contract: Post-processing subsystem — one lazy initialisation with fixed feature flags, one configured run per post-processed frame, and a licensed library behind a fixed boundary
category: 17-Presentation-Rendering
scope: subsystem
readiness: CONTRACT READY   # the ordering, the flags and the boundary are STATIC; nothing here was observed live
confidence: PROVEN
implements:
  - 17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md
entries: [00193DA0, 0065E5A0, 006CBD20, 006DAA70, 006FF900, 0065E5C0, 006CBEA0, 006DB660, 0070BA00, 006CC090, 006CC1E0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: read from the authority image on 2026-09-25 (FABLE, Claude Opus 5.5) with capstone - every
    call site, constant, guard and flag store cited below was disassembled from that file. The API
    names come from the library's own error strings (`CPostEffect::<method>():`), mapped to the
    function that loads each with Database/Tools/work/FABLE/gg3-scratch/ppfx_api_names.py (control:
    0070BA00 loads the ApplyEffects message). Single-caller claims come from the raw E8/E9 index
    (pub140-scratch/tools/rawcalls.py, which includes the unlisted-code arm and follows 5-byte thunks)
    plus the jcc sweep (tools/jccscan.py) and a stored-VA search.
last_reviewed: 2026-09-29
falsification_passes: 0
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-post-processing-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the post-processing subsystem (FABLE, Claude Opus 5.5)

> **Why this exists.** S-40's verdict row is SCOPE-SHORT: its one contract,
> [effect creation](CONTRACT-ppfx-effect-creation.md), is `operation`-scoped over the catalogue
> build, and *"the pass chain is uncovered"*. This contract is the subsystem view. It covers how the
> game initialises the library, what it hands the library every frame, which features can ever run,
> and where the game stops and the licensed library begins. It relies on the creation contract for
> the catalogue build itself and does not restate it.

## 1. What this contract covers (FABLE)

- **Initialisation**: once, lazily, from the first post-processed frame, through one route with
  constant feature flags (§3).
- **The frame**: one configuration-then-run sequence per post-processed frame (§4).
- **The two player switches**: the `Glare` and `DepthofField` graphics options (§4).
- **The boundary**: what is the game's and what is the library's (§6).

The page with the evidence is [the post-processing effect catalogue](the-post-processing-effect-catalogue.md),
in the sections "The frame half" and "Which families can run at all".

## 2. The objects (FABLE)

| object | where | role |
|---|---|---|
| the post-process render command's parameter block (`cfg`) | `[ctx + 0x10]` of the command `PostProcessObj::Execute` enqueues | every per-frame input below |
| the wrapper | `0x10`-byte object at `[02D38540]`, built lazily by `0065E5D0` | `+0` holds the library context object; `0065E5B0` tests it |
| the library object | `[02EA0B70]` | the `CPostEffect` instance `Initialize` and `ApplyEffects` run on (`006DAA70`, `006DB660`) |
| `CTextureUtil` | refcounted singleton at `02EA1590` / `02EA1598` | the catalogue's handle table (creation contract, `UQ-226`) |
| `GameSettingConfig` | `*(01F82D20)` | `+0x34` Glare, `+0x30` DepthofField (`enum{Off|On}`, default On) |

## 3. Initialisation (FABLE)

**Route, single at every link:** `PostProcessObj::Execute` enqueues `00193DA0` →
`0065E5A0` (sole caller `00193DE8`) → `006CBD20` (reached only by that 5-byte thunk) → `006DAA70`
(sole caller `006CBE0A`) → `Initialize` `006FF900`. Its other caller, `006DE950`, has no route in.

**When:** on a frame whose `cfg+0x99` is clear and whose wrapper holds no library object
(`00193DC9`–`00193DE8`).

**What `006CBD20` does:**
- performs a one-time licence feature registration (`FeatureId = YEBIS_D3D11 …`, guarded by `01F31F70`);
- builds a default parameter block (`006CBBC0`) with aspect `16/9`, `0x780` and 7 qwords of `-1`;
- calls `006DAA70(…, 3, 5, …)` with **fifth argument `0x20001`** (`006CBE02`);
- on failure logs *"Failed to initialize PPFX context."* through `005CDAA0(2, …)` and **continues**.
  *Bounded 2026-09-26 (OPUS):* the continuation's next library call faults unless `Initialize` passed `007009BB`
  (§5 I-5).

## 4. The frame, in order (FABLE)

`00193DA0` runs these calls every post-processed frame:

1. `cfg+0x99` set: `0065E6C0` → `006CC2F0`, two virtual calls on the library object (not named here).
   Otherwise, if there is no library object: the lazy create of §3.
2. **No library object: return.** Nothing below runs (`00193DFC`).
3. `0065E6A0` → `006CC1F0` with `&cfg+0x9C`.
4. `0065E6B0` → `006CC260` with `cfg+0xDC`, `+0xE0`, `+0xE4`.
5. **Glare**: `0065E670` → `006CC1E0`. With the option on it passes `cfg+0x18`/`+0x1C`; off, it passes
   `1.0`/`0.0`. *Confirmed 2026-09-25 (FABLE, Claude Opus 5.5), on `OPUS-REQ-FABLE-S40-CFG-GLARE-VS-DOF-NAMES`:*
   the chain ends in the library's own **`CPostEffect::SetGlareParameters`** (`006CC1E0` → `006DB9A0` →
   `00707560`). Its error path formats `"CPostEffect::SetGlareParameters(): GlareRemapFactor must be greater
   than 0.0."` (`00D93420`, `00707595`). It stores the first float at library `+0x6E4` and the second at
   `+0x6E0` (`007075CB` / `007075D3`), the flag `1` at `+0xC6C`, and the remap factor (the `1.0` fifth
   argument, raised to at least `0.001`) at `+0xC70`. **So `cfg+0x18`/`+0x1C` are glare parameters.** ~~The type~~
   ~~store's names for their source, `PostProcessParamContext` `+0xF4` `dofFocusEnd` / `+0xF8` `dofBlendFalloff`,~~
   ~~rest only on the constructor defaults `0.8f` / `0.1f` and are the ones to rename.~~ *Renamed in the store on
   2026-09-26 to `glareLuminance` / `glareThreshold` from the scene keys below (noted 2026-09-27, FABLE, Claude Opus
   5.5, on OPUS-NOTICE-FABLE-POSTFX-NAMES-ALREADY-RENAMED).* ~~Which glare quantity each
   float is has no name in the image.~~ *They do have names — the scene data's (§4a): `cfg+0x18` is
   `mGlareLuminance` and `cfg+0x1C` is `mGlareThreshold`.*
6. `0065E630` → `006CC170`: `cfg+0x98` gives `2.0` and mode `2`; otherwise `1.0` and mode `±1` from
   `cfg+0x9A`.
7. **Depth of field**: `0065E610` → `006CC090`. On, it passes the enable byte `cfg+0x20`, lens `35.0`
   and focus floats. Off, it passes enable `0`. `006CC090` skips every lens setting when the enable is
   0, and divides the lens value by 1000 (35 mm expressed in metres).
8. **Run**: `0065E5C0` → `006CBEA0` with `cfg[0]`, `cfg[8]` and `cfg[0x10]`, which become the colour
   source, the depth source and the output target. Then `006DB660` → `ApplyEffects` `0070BA00`, then a
   Phyre render-context guard.

## 4a. Where the inputs come from: the authored scene data (FABLE, Claude Opus 5.5, 2026-09-26)

**The glare and depth-of-field inputs are authored per map and per cutscene in the shipped JSON, under their own
names.** Static plus the shipped data. This is the subsystem's script/data relationship.

- **The data.** All 459 files in `jsondata/maps/` and 283 of the 337 in `jsondata/cutscenes/` are scene-parameter
  sets.
  - Among the keys are `mGlareLuminance`, `mGlareThreshold`, `EnableDof`, `mDofFocusDistance` and
    `mDofApertureFnumber`. `EnableDof` is in the cutscene files only, and map files carry
    `mDofSpecialApertureFnumber` instead.
  - All 283 cutscene files give `mGlareLuminance 0.8` and `mGlareThreshold 0.1` in their `"Common"` block. Those
    are exactly the render-parameter block's constructor defaults.
  - The same files carry the scene light's angles and the SSS/AO/shadow settings this contract does not cover.
- **The block.** `cfg` is filled from the `0x4A8`-byte render-parameter block that `00193D50` returns; `01F81300`
  caches the same pointer (`0015CAF0`). The two JSON loaders write it through two setters:
  - `00194310(block, luminance, threshold)` stores `+0xF4` / `+0xF8`. The cutscene loader reads `mGlareThreshold`
    and then `mGlareLuminance` and makes this call (`001C42A6`–`001C42E4`).
  - `00194250(block, enable, focus, aperture, a, b)` stores `+0x110` (the enable byte), `+0x114`, `+0x118`,
    `+0x11C` and `+0x120`. The cutscene loader passes `EnableDof == 1`, `mDofFocusDistance`, `mDofApertureFnumber`,
    the block's own `+0x11C` unchanged, and `35.0` (`001C4179`–`001C42A1`). The map loader calls the same two
    setters, with the enable fixed at 1.
  - *The developer console writes the same block (CF-5, 2026-09-27, FABLE, Claude Opus 5.5).* Sixteen of its command
    arms, 33 call sites, call `00193D50`; the count is in
    [arm catalogue slice D](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md)
    §5.2. For example, id 45 *HBAO Full Resolution* toggles byte `+0x1E8`
    ([slice B](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-B-ids-44-75.md)).
    [What the console tunes](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md) is the
    console side of this relationship.
- **Into `cfg`** (`0018EEE0`):

  | `cfg` | from the block | the scene key |
  |---|---|---|
  | `+0x18` | `+0xF4` | `mGlareLuminance` — the glare setter's first float, library `+0x6E4` (§4 step 5) |
  | `+0x1C` | `+0xF8` | `mGlareThreshold` — the second float, library `+0x6E0` |
  | `+0x20` | `+0x110` | `EnableDof` — the byte step 7 passes as the enable |
  | `+0x24` / `+0x28` | `+0x114` / `+0x118` | `mDofFocusDistance` / `mDofApertureFnumber`; a computed pair replaces them when the caller's `+0x124` is 1 |
  | `+0x2C` | `+0x120` | the `35.0` both loaders pass ~~— the lens length step 7 divides by 1000~~; step 7 does not read it: its lens is the constant `35.0` at `008F312C`, and it passes `cfg+0x21`, `+0x30` and `+0x34` too *(corrected 2026-10-02, OPUS: `00193DA0`+0x150 `movss xmm0, dword ptr [008F312C]`; `00193DA0`+0x126..+0x146 the other arguments)* |

- **So:**
  - The two graphics options only choose whether these authored values reach the library (§4 steps 5 and 7).
  - What the glare looks like, and where the depth of field focuses, is scene data.
  - A reimplementation must load the scene JSON's keys into the block, or every scene falls back to the defaults.
  - *Not established:*
    - which float the map loader passes at `+0x11C`;
    - the computed focus pair's meaning;
    - whether any zone-script verb writes the block (no script route was searched).
  - ~~The type store's names for `+0xF4`/`+0xF8` (`dofFocusEnd`, `dofBlendFalloff`) are wrong and are routed to OPUS.~~ *Done 2026-09-27 (FABLE, Claude Opus 5.5): the store renamed them on 2026-09-26 to `glareLuminance` / `glareThreshold` from the scene-JSON keys `mGlareLuminance` / `mGlareThreshold` (the loader chain in §4a), and the frame copy `PostProcessFrameParams +0x18` / `+0x1C` the same way.*
- **What a live read can and cannot show** *(2026-09-27, FABLE, Claude Opus 5.5, on
  `ASTRA-RETURN-FABLE-S40-DISCRIMINATOR`, `_experiments/evidence/s40-discriminator/`).*
  - **Glare cannot discriminate.** Every cutscene's `0.8` / `0.1` equals the constructor's defaults, so reading
    those values at `+0xF4` / `+0xF8` fits constructor-only state as well as a loaded scene.
  - **`EnableDof` can, but only as a refutation.** Cutscenes such as `alc_a0100` author `EnableDof 0`, against the
    constructor's 1 and the map loader's fixed 1. A 0 at `+0x110` after such a scene activates refutes
    constructor-only state.
  - It does not name the writer: the setter `00194250` has five direct call sites. An execute hit at the cutscene loader's
    own call (`001C42A1`) inside the same bracket is what names it.
  - The claim a live package would test is therefore: *the cutscene loader's `EnableDof` path runs in play and its
    value reaches `cfg+0x20`*. That needs:
    - a prepared save and trigger that is known to activate the scene (a file name is not evidence of that);
    - the real block identity;
    - the three observations above, bracketed in time.
  - A non-null library object with flags `0x20001` is not initialisation evidence by itself; see §3's executed
    refusal.

## 5. Invariants (FABLE)

**I-1 — At most one run per post-processed frame, and none without a library object.**
`ApplyEffects` has one caller (`006DB660`), which has one caller (`006CBEA0`). That is reached only
by the thunk `0065E5C0`, whose only caller is `00193DA0` (`00193F58`), and that call sits after the
`00193DFC` return.
*Falsified by:* a second route to `0070BA00`, or a path to `00193F58` that skips the `00193DFC` test.

**I-2 — The library is initialised with the constant flags `0x20001`, on its only live route.**
§3's route, plus `Initialize` storing its fifth argument at `+0x20C` (`006FFB8C`). No feature bit
above `0x400` is forced inside `Initialize`.
*Falsified by:* a live caller of `006DE950`, or a write to `+0x20C` that sets `0x40000`, `0x4000000`
or `0x8000000`.

**I-3 — Nine optional features can never run in this build.** Lens distortion, aperture Airy disc,
motion blur, geometry blur, Gaussian blur, heat shimmer and chromatic aberration hang off `0x40000`,
ambient occlusion off `0x4000000`, and post-process antialias off `0x8000000`. None of these bits is
ever set. Each feature's "initialised" byte therefore stays 0, and its `Set…Enable` refuses.
*Falsified by:* a pass for one of these features that `ApplyEffects` runs without consulting its
enable or its byte. For motion blur the byte's full reader set is listed on the page; for the others
this is not yet swept (§8).

**I-4 — The two player options change what the setters are handed, never whether they are called.**
Both calls run on both branches (`00193E42`, `00193EC0`). For depth of field, "off" reaches the
library as enable 0 and skips the lens configuration.
*Falsified by:* a branch that skips `0065E670` or `0065E610`.

**I-5 — ~~Library failures do not reach the game.~~ `ApplyEffects` failures do not reach the game; an initialisation
failure before `007009BB` does.** *(Heading corrected 2026-09-26, FABLE, Claude Opus 5.5, on OPUS's execution below;
`00708110` re-read: with `+0x147` clear it dereferences `[+0x108]` at `00708186`, and `+0x108` has its one store at
`007009BB` inside `Initialize`.)* `ApplyEffects` returns an HRESULT (`E_FAIL` inside
a Begin/End scene pair, or with `PFXINIT_RENDERSCENE_EXTERNAL` and no source). `006CBEA0` does not
test it. A failed initialisation is logged and creation continues, but the next library
call (`006CBE27` → `006DB4C0` → `00708110`) faults unless `Initialize` got past `007009BB`.
*Falsified by:* a test of `006DB660`'s return in `006CBEA0`.

*Bounded 2026-09-26 (OPUS), executed in NATIVE-REPLAY:* **an initialisation failure reaches the game when it comes before
`007009BB`**, so this invariant holds for `ApplyEffects` and not for every initialisation failure. Evidence:
[`s40-opus-replay-post-process-init`](../../_index/candidates/s40-opus-replay-post-process-init/README.md), P3 and S1.

*Scope, 2026-09-27 (OPUS, on ASTRA-RETURN-OPUS-S40-INIT-WITNESS-LIMIT): the failing run is a CONTROL counterexample. A disclosed deferred-context model makes `Initialize` return `0x80070057`, so the run shows what a failure before `007009BB` does to creation. It is not a finding that the shipped game fails to initialise or crashes live. The flags `0x20001` are the observed build constants, and a healthy live initialisation needs its own evidence. The MET cell and the device boundary are unchanged, and nothing was re-run.*

The run: `Initialize` refused a device context whose `GetType` said "deferred" (a disclosed one-method model), with
*"CPostEffect::Initialize(): Device context must be immediate context."* and `0x80070057`. `006CBD20` logged and
continued as this section says. Its next library call does not survive the failure: `006CBE27` → `006DB4C0` →
`00708110` faults at `00708186`.

Why:
- `00708110` returns early only when `CPostEffect+0x147` is set; otherwise it dereferences `+0x108` (`00708152`–`00708186`).
- The constructor zeroes `+0x108` (`006FF68E`).
- `Initialize`'s own body writes `+0x108` only at `007009BB`, and at the refusal the field was still 0 (executed).
- `Initialize` sets `+0x147` only at `00700083`, and only when the flags hold `0x800` (`00700077`). The build's
  constant `0x20001` does not hold it.

So creation completes only when `Initialize` got past `007009BB`, and that point lies behind the immediate-context test
at `006FFC56`. The licence failure path (`006DAB3C`) is analogous (static reading): it returns before `CPostEffect` is even allocated,
so `006DB4C0` loads a null object.

## 6. The boundary (FABLE)

- **The game owns:** `00193DA0`, the wrapper forwarders `0065E5A0`–`0065E6C0`, the adapter layer
  `006CB…`/`006CC…` that fixes the constants (`0x20001`, `35.0`/`24.0`, `2.0`/`1.0`), and the two
  options.
- **The library owns:** everything from `006DA…`/`006DB…` inward. That includes `CPostEffect::Initialize`
  and `ApplyEffects` and the 62 API methods named from its own strings.
- **What a reimplementation must match to keep the image:**
  - I-1 to I-5;
  - the fixed feature set (depth of field and glare reachable, the nine features of I-3 absent);
  - the values of §4.

  It is otherwise free to substitute the library. The registry's `deferred` tier describes this layer
  as *"a licensed library behind a catalogue"*, and this contract keeps that line.

## 7. What a reimplementation must not do (FABLE)

- Enable motion blur, SSAO, FXAA or the other I-3 features because the catalogue lists their
  techniques. The shipped initialisation never turns them on.
  - *Nor because the scene data asks for motion blur (2026-09-26, FABLE, Claude Opus 5.5).* The scene JSON's
    `mMotionBlurEnabled` reaches the render-parameter block at `+0x330` through `001944C0`. The block's constructor
    sets that byte to 1; the key is 0 in 283 cutscene files and 1 in one. Across the block's 776-site access census
    (`postprocess-context-accesses.tsv`, cross-call tracked), `+0x330` has only those two writers and no reader. The
    authored switch has nowhere to go, which agrees with I-3.
- Treat the Glare or DepthofField option as skipping a call. It changes the arguments (I-4).
- Let a library error abort the frame. The game ignores it (I-5) *(corrected 2026-10-02, OPUS: an `ApplyEffects` error; an initialisation failure does reach the game - the corrected heading of I-5's section)*.

## 8. What this contract does NOT establish (FABLE)

- Which depth-of-field, bokeh, glare, tone-map and composite techniques `ApplyEffects` runs for a given
  configuration (`UQ-227` stays PARTIAL).
- What steps 1, 3, 4 and 6 configure. Their API names are not in the image.
- ~~Who fills `cfg`~~ *(answered 2026-09-25 by OPUS's type census, `_index/candidates/s40-types-cposteffect-and-cfg.md`:
  `0018EEE0` allocates the `0xF0` block through `001A1470([01F7F4C0])`, fills it (copying `PostProcessParamContext`
  `+0xF4` / `+0xF8` into `+0x18` / `+0x1C` at `0018EFF3` / `0018EFFC`), and `005FEA50` enqueues it as a kind-`0x2F`
  command's `+0x10`)*~~, and which float carries the cutscene focus distance~~. *(answered: see the `cfg` table above - `+0x24` is `mDofFocusDistance`; 2026-10-02, OPUS)*
- For the I-3 features other than motion blur, whether `ApplyEffects` could reach them by a test other
  than their enable.
- Anything live. No frame was observed.

## 9. Evidence (FABLE)

| claim | evidence | tier | confidence |
|---|---|---|---|
| the frame order and the two option gates | `00193DA0` whole; `GameSettingConfig +0x30`/`+0x34` type rows | 1 | PROVEN |
| DOF lens in metres, skipped when disabled | `006CC090` (`006CC0BD`, `006CC144`) | 1 | PROVEN |
| constant flags on the single route | `006CBE02`, `006DAD0A`, `006FFB8C`; single-caller sweeps | 1 | PROVEN |
| feature bits → initialised bytes → setters refuse | `006FFE56`–`00700080`; each setter's first compare | 1 | PROVEN |
| API names | the library's own error strings, control included | 1 | PROVEN |

## 10. Related (FABLE)

- [The post-processing effect catalogue](the-post-processing-effect-catalogue.md): the evidence page.
- [Effect creation](CONTRACT-ppfx-effect-creation.md): the catalogue build this relies on.
- [The ordered render command list](../Render-Command-List/the-ordered-render-command-list.md): where `PostProcessObj::Execute` enqueues the frame.
- [Game settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md): the two options.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

**Platform — CLIENT.** `006253D0`, the platform device set-up, shares the wrapper through
`0065E5D0` and calls `0065E580(wrapper, 1)`. The crossing is the shared wrapper; the frame path does
not call into Platform.

**SaveLoadSettings — PROVIDER.** The `GameSettingConfig` options at `+0x30`/`+0x34` are read, never
written, by `00193DA0`.

**Resource — MECHANICAL.** The creation-failure message goes through `005CDAA0`, the engine's
leveled formatted logger (a 16 KB stack buffer, 77 callers across layers; see
[the game-application page](../../00-Engine-Core-Runtime/Application-Root/game-application.md)).
Resource-layer bodies call the same leaf. It is shared-helper fan-in, and no Resource state is
touched here.

**UI — PROVIDER.** The `cfg` block that step 5 reads is built by `0018EEE0` and handed on through
`005FEA50`, as a kind-`0x2F` command's `+0x10`. This contract relies on two copies in that builder
(`0018EFF3` / `0018EFFC`, the render-parameter block's `+0xF4` / `+0xF8` into `cfg+0x18` / `+0x1C`). It says
nothing else about the builder or the command queue.

**CoreRuntimeScheduling — PROVIDER, at one remove.** The builder allocates the `0xF0` block through
`001A1470` on the arena `[01F7F4C0]`. This contract does not depend on the allocation beyond the block
existing when step 5 runs.

*These two paragraphs cover only the edges the 2026-09-25 "who fills `cfg`" note adds.*

## Falsification pass 1 — 2026-09-29 (OPUS): tested with the contract's own falsifiers

**Attack.** I-1, I-2, I-4 and I-5's "Falsified by" clauses and §3's route became checks. Every edge census is a raw
E8/E9 sweep of `.text` plus an 8-byte stored-address search. Script:
`Tools/analysis-kit/gfz-scripts/falsify_post_processing.py`, output `falsify_post_processing.out`, image `73461d08…`,
0 BROKEN, exit 0. I-3's per-feature pass sweep stays §8's open item, and OPUS's S-40 replay (I-5's bound) is not repeated.

| # | Clause attacked | Result |
|---|---|---|
| Q1 | I-1 | **survives**: every link to `ApplyEffects` is single (`006DB667 jmp`, `006CC031 call`, `0065E5C3 jmp`, `00193F58 call`), none of the four addresses is stored anywhere, and the `00193DFC` return precedes the run call |
| Q2 | I-2, §3 | **survives**: single callers at every link; `0x20001` at `006CBE02`; `Initialize` is reached only from `006DAA70` and the dead `006DE950` (no edges, no stored address); `006FFB8C` stores the flags; nothing in the library writes a forbidden bit to `+0x20C` |
| Q3 | I-4 | **survives**: `00193E42` / `00193EC0` are the Glare / DepthofField option tests; the calls follow at `00193E6C` / `00193F40`, and no conditional jump skips them |
| Q4 | I-5 | **survives**: nothing tests the `006DB660` result before the next call |
| Q5 | I-5's bound | **survives**: `00708110` tests `+0x147` before dereferencing `+0x108`. On its object (`rsi`), `Initialize` writes `+0x108` only at `007009BB` and `+0x147` only at `00700083`, behind the `0x800` test. Its `[rbp + 0x108]` stores are a stack local |

No correction.
