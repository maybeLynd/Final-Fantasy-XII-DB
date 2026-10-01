# Presentation / Rendering

**Engine category.** Rendering, effects, cameras, CharacterRender, and the retained PlayStation 2 GS/VIF compatibility layer.

| | |
|---|---|
| Classification source | PrimaryOwner: Presentation |
| Functions | 1,564 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Authored-Commands/the-authored-presentation-command-handlers.md`](Authored-Commands/the-authored-presentation-command-handlers.md) —
  **PARTIAL, tier 1.** The **28-body `00520xxx` family**: authored presentation commands dispatched
  two tables deep — `01EFFAF0[id]` generated invoker → `02CA4410[id]` bank slot → handler — all 25
  `CharacterRenderSystem_Initialize` registrations instruction-exact, plus the deferred-work pair
  (`00520100` → `00520E90`) and the shared helper `00520010`.
- [`CONTRACT-authored-command-ramp-channels.md`](CONTRACT-authored-command-ramp-channels.md) -
  **SPECIFIED, tier 1, not differentially tested.** 160 slot records of `0xE0` bytes (`0x8C00`
  exactly), each with **five linear ramp channels**. Four authored-command classes `0x0D`-`0x10` drive
  four of them, and **two of the four setters are absent from the function census** - precisely the
  two reached by a tail `jmp` rather than a `call`. `steps == 0` means immediate, not 256, and the
  value is **never clamped** to its target.
- [`Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md`](Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md) -
  **PARTIAL, tier 1.** `setResolutionSize` logs the request and **tail-jumps into the arithmetic**, and
  the arithmetic - `001DDAC0` - **is not in the function census**. It fits the requested shape against
  **`16/9` and `16/3`**, clamping height below the first bound and width above the second. **The
  middle branch is not built like the other two**: two integer divides where the others write `1.0f`,
  and one field it never writes at all. What that does on screen is **not** established.
- [`Scripted-Camera/the-scripted-camera-player.md`](Scripted-Camera/the-scripted-camera-player.md) —
  **DOCUMENTED, tier 1 (2026-09-12).** How a script's `camerastart` becomes a camera move: four
  channels per actor-manager slot, the `CAM7` **key/segment command stream** (`00258350`), 13 eased
  timing channels, cubic paths with arc-length tables, five interpolation kinds (linear, orbit,
  flat orbit, turn, flat turn; two path-follow kinds with no shipped user), actor/joint attachment,
  and hand-off to **camera record 5** of the eight-record priority stack.

- [`Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`](Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md) —
  **DOCUMENTED, tier 1 (2026-09-12).** The **seven screen-fade layers** at `022BDD60` — one starter
  `002EFA70(layer, frames, direction, white)` behind the `fadeout` / `whiteout` / `fadein` verbs,
  the field transitions and the cutscene skip's instant black — and the **49-row movie fade
  schedule** at registry slot 0, decoded from `battle_pack.bin`.
- [`Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md`](Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** The twenty-four `cutin*` / `moveblur*` / `setsoftfocusmode` verbs and the
  native module under them: staging blocks, play / clear / per-frame bodies, one-shot screen-effect descriptors. Motion
  blur is one idiom used 2,304 times, a held captured frame behind the *obtained* message during which the scene draw is
  skipped; soft focus is only ever switched off.
- [`Character-Render-Records/the-rig-of-seventeen-controllers.md`](Character-Render-Records/the-rig-of-seventeen-controllers.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** A character's procedural controllers - sway, bone physics, look, eyes,
  **lip flap, nod, head shake** (the three verbs a third of all scripts use, some 55,000 calls), and the **Float,
  Immobilize and Confuse** motions switched by the status push, whose arms are indexed by status bit. Beside it:
  [the staged look command](Character-Render-Records/the-staged-look-command.md),
  [how a character fades](Character-Render-Records/how-a-character-fades-the-ten-channels.md) and
  [the focus point](Character-Render-Records/the-focus-point-of-a-character.md).
- [`Character-Render-Records/how-a-status-shows-on-a-character.md`](Character-Render-Records/how-a-status-shows-on-a-character.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** A body shows **one status colour look at a time**, the lowest index of a
  fourteen-entry list winning (Stone first, HP Critical last); a look must leave before the next arrives; **Poison,
  Silence, Sap, Disable and Disease share one pulsing tint**; Immobilize, Slow, Invisible and Stop run through a second
  block; control denial holds the look still.
- [`Character-Rendering/how-a-character-is-lit.md`](Character-Rendering/how-a-character-is-lit.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** Lights are chosen **per character**: a class filter, then scope (this
  character only, everyone but, camera-anchored, a character's own list); **ambient is a priority contest** that turns
  into a sum only when the winner is additive; six directional lights at most. A light's request bytes are named.
  The status tints are private ambient lights of this system.
- [`Effect-File-Formats/an-effect-element-frame-by-frame.md`](Effect-File-Formats/an-effect-element-frame-by-frame.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** The per-frame update of effect element types `0x00`-`0x0A`: what each
  type's tail samples, the orientation mode (authored, or aligned to the element's own motion), and the fork every
  tail ends in - **an element outside its cull window is destroyed, not hidden; one that passes fires its child-spawn
  slots**. The draws are not on it.
- [`Model-And-Motion-Formats/the-pose-sequencer.md`](Model-And-Motion-Formats/the-pose-sequencer.md) —
  **DOCUMENTED, tier 1.** FCP section 7: eight events, random choices of {duration, end action, value} frames,
  an eight-slot sequencer per character, and the add-motion group its value selects. Format tested on all
  1,066 FCP blocks.
- [`Character-Render-Records/the-bone-trails.md`](Character-Render-Records/the-bone-trails.md) —
  **DOCUMENTED, tier 1.** FCP section 4: up to four trails per model, each a bone's base and tip sixteen samples
  deep; authored command `0x11` switches them on and off through the record hierarchy; fade in, fade out, self-free;
  the draw hands the histories to an unread VU1 program. Descriptor format tested on all 216 blocks.
- [`Effect-File-Formats/the-six-vfx-display-layers.md`](Effect-File-Formats/the-six-vfx-display-layers.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** Effects are drawn six times a frame, once per layer, and the engine's
  own debug markers name the layers: first, after BG, `TsEffMan_Layer_AfterOBJ`, in EFF, after EFF & MENU. Layer 3
  has its own path, beside the depth-sorted display list.
- [`Character-Render-Records/how-a-presentation-entry-picks-its-track.md`](Character-Render-Records/how-a-presentation-entry-picks-its-track.md) —
  **DOCUMENTED, tier 1 (2026-09-19), static.** A character's authored command stream has several tracks; this is how a
  track state is set up (the start cursor sits after a `0xFFFF` marker), how a reset keeps only the primary, and the two
  commands that switch tracks - one direct with a deferred mode, one through a selector whose choice **an attached
  model copies from its parent**.


- [`Render-Command-List/the-ordered-render-command-list.md`](Render-Command-List/the-ordered-render-command-list.md) —
  **DOCUMENTED, tier 1, crossref-clean.** Every render pass is **an object appended to a list**, not a
  function that draws. **36 command classes** on a shared `OrderedObject` base whose third vtable slot
  returns a **draw-order key** — `1` for scene begin, `0x10` for the ordinary passes, `0x80` for video.
  Carries the complete **frame scope → wrapper → enqueue → constructor → vtable → RTTI class** map for
  every named pass, and the byte switches that turn each effect off.
- [`Gi-Render-Commands/gi-render-command-family.md`](Gi-Render-Commands/gi-render-command-family.md) —
  **DOCUMENTED, tier 1.** Eighteen classes carrying the **PlayStation 2 drawing vocabulary**
  into the remaster, in **four shapes**. The PS2 naming survives into the bodies: four
  fixed-quad commands hardcode a vertex count of 4, and the one generic primitive reads it.
- [`Character-Rendering/character-render-object.md`](Character-Rendering/character-render-object.md) —
  **DOCUMENTED, tier 1.** The **1,640-byte object that draws a character**: a complete
  31-slot vtable, one construction site, and a **ready flag at `+0x4B4`** with one writer
  at the end of setup and twelve readers at method entry.
- [`Legacy-PS2-GS/texture-mip-local-memory-budget.md`](Legacy-PS2-GS/texture-mip-local-memory-budget.md) - the 4 MiB GS local-memory texture budget still live in the PC port

### [`Post-Processing/`](Post-Processing/) — **documented**

- [`ppfx-function-identification.md`](Post-Processing/ppfx-function-identification.md) —
  **DOCUMENTED, tier 2.** **147 post-processing functions named** from authored diagnostics
  (317 references, 0 unattributed, 23 cross-validated against RTTI). Covers `CPostEffect`,
  `IGPUDevice`, `CDepthOfField`, `CRenderGlare`, `CTextureUtil` and more — the Yebis
  middleware behind FFXII's bloom, depth of field and glare. Identity only; no body read yet.

Undocumented sub-families with existing CodeDomain labels: `Presentation.Rendering` (26), `Presentation.UI` (7), `Presentation.CharacterRender` (7), `Presentation.Geometry` (5), `Presentation.LegacyPS2Effect` (4, the VIF/VU path), `Presentation.ProceduralPose` (4), `Presentation.EffectFont` (4), `Presentation.Camera*` (4), `Presentation.Cutscene` (2).

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.

## Systems in this category

- [`Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md`](Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md) —
  **PARTIAL, tier 2.** ~150 authored parameter names (shadows, SAO/HBAO, DOF f-number, water,
  eyes, tonemap) and the 15 `.phyre` shader assets that consume them. The look of FFXII is data.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE.** `00258350` on this page calls `FUN_00230b60`, owned by that layer. What it reaches is a 154-byte frame assembler with a stack cookie: it lays out a frame carrying the `.text` callback `0022CC50`, two 16-byte vectors from its third and fourth arguments and a word/dword pair from the stack, hands it to `0022F430`, and returns a signed word from the frame or `-1`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**SaveLoad — CLIENT.** `FUN_00280140`, owned by that layer, calls `002EFA70` on this page. That caller is the save/load screen's message handler: message 1 picks save or load from `(qword[+0x10] & 0x7FFF)` and takes the state block at `[0209AC30] + 0x3F8`, message 2 runs the image operation and records the outcome in that block's `byte[+8]`, and message `0x10` tears the screen down and clears `[0209AC30] + 0xC0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `00520E90` on this page — the posted deferred worker for the authored-command
family — calls `002ED570`, the resource-table entry lookup, resolving the record's
`dword[+0x18]`/`dword[+0x10]` indices. The crossing is the worker's resource fetch; descent, not
shared ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).
- **ActorEntity - CLIENT (1 edge).** `002EFA70` is called by bodies filed to ActorEntity: ActorManager_RunFieldRuntimePass (`0025D9E0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (6 edges).** `002EFA70` is called by bodies filed to Script_VM_Native_Bridge: `003559B0`, `00355EB0`, `00356270`, `00356650` (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (6 edges).** `002EFA70` is called by bodies filed to WorldAreaField: WorldTransition_RequestFieldTransition (`00314440`), WorldTransition_RequeueCurrentFieldForRestore (`00314530`), WorldTransition_StageFieldTransition (`003145E0`); `00280140` reaches bodies filed to WorldAreaField: WorldTransition_RequeueCurrentFieldForRestore (`00267C90`), WorldPersistence_ResetBanksAndMarkInitializationState (`00268320`), WorldTransition_RequestFieldTransition (`00314440`) - shared machinery across the layer boundary, no shared ownership.

