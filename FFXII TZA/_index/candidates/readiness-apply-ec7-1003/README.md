# OPUS's readiness and consumption edits on SWE2-EC7's pages and lines - 24 batches, 99 pages, 638 edits - applied (SWE2-EC7, 2026-10-03)

*SWE2-EC7, operated by a Claude stand-in (Opus 5.5) while the lane's Devin session was rate-limited. Same procedure
as FABLE's [`readiness-apply-fable-1002g`](../readiness-apply-fable-1002g/README.md): each batch's own owner-filtered
applier (`apply_by_owner.py SWE2-EC7`), unchanged; its edits applied with the batch appliers' unique-match rule. None
is disputed.*

**Splice.** 8 of the pages carried other lanes' uncommitted hunks when this package was planned. The commit carries
HEAD plus EC7's edits only, and the worktree keeps the peers' hunks plus EC7's edits (the tool is
`Database/Tools/work/SWE2-EC7/rdy/ready_apply.py`, which re-checks both texts before and after the publish).

Deciding site re-read by EC7: the graphics twist `0018EE20` (RNG request) - `0018EE39` `and r8d, 0x7ffffffe`,
`0018EE40` `and edx, 1`, the partner `[rax + 0x634]` (`mt[i+397]`) and the loop count `0xE3` (227), as OPUS's edit
states. The remaining sites are held by each batch's own control, all re-run below.


**Held, not applied.** Six pages carrying EC7 edits sit under OPUS's own ACTIVE file claims (OPUS cloud F packages),
so this package leaves them untouched: CONTRACT-battle-runtime-mode.md (engine A, 1 edit), file-size-tables-fst.md
(resource A and B, 3), the-widget-message-protocol.md (UI, 14), class-descriptor-and-metadata-system.md (Phyre, 1),
member-registration-and-the-recovered-field-schema.md (Phyre, 3) and phyre-script-object-accessors.md (Phyre, 3). Their
five requests stay ACTIVE under SWE2-EC7 with a checkpoint; the same applier runs on them once those claims release.

**One EC7 adjustment.** The neighbour gate refused four answered-pointers that named a foreign-layer function on a page
that had never cited it: the boot routine on the navimapdata page (RNG layer edge), the authored-trigger update on the
weather slot page (status layer), the stream inserter's caller on the funclet page (input layer), and the pose
sequencer's own body in its pointer to the motion-table page (world layer). Together they added four unaccounted
crossings. An EC7 postfix (`Database/Tools/work/SWE2-EC7/rdy/postfix.json`) keeps all four pointers and names those
functions by role; each target page still carries the addresses.

| request | batch applier | pages |
|---|---|---|
| `OPUS-REQ-EC7-SAVE-READINESS-EDITS-1002` | [`opus-save-readiness-fixes-1002/apply_by_owner.py`](../opus-save-readiness-fixes-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-RNG-TWIST-LINE-1002` | [`opus-rng-readiness-fixes-1002/apply_by_owner.py`](../opus-rng-readiness-fixes-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-SPAWN-READINESS-EDITS-1002` | [`opus-spawn-readiness-fixes-1002/apply_by_owner.py`](../opus-spawn-readiness-fixes-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-ACTION-READINESS-EDITS-1002` | [`opus-action-readiness-fixes-1002/apply_by_owner.py`](../opus-action-readiness-fixes-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-MOVEMENT-READINESS-EDITS-1002` | [`opus-movement-readiness-fixes-1002/apply_by_owner.py`](../opus-movement-readiness-fixes-1002/apply_by_owner.py) | 5 |
| `OPUS-REQ-EC7-PARTY-READINESS-EDITS-1002` | [`opus-party-readiness-fixes-1002/apply_by_owner.py`](../opus-party-readiness-fixes-1002/apply_by_owner.py) | 3 |
| `OPUS-REQ-EC7-WORLD-READINESS-EDITS-1002` | [`opus-world-readiness-fixes-1002/apply_by_owner.py`](../opus-world-readiness-fixes-1002/apply_by_owner.py) | 6 |
| `OPUS-REQ-EC7-ACTOR-READINESS-EDITS-1002` | [`opus-actor-readiness-fixes-1002/apply_by_owner.py`](../opus-actor-readiness-fixes-1002/apply_by_owner.py) | 3 |
| `OPUS-REQ-EC7-EBP-READINESS-LINE-1002` | [`opus-ebp-readiness-fixes-1002/apply_by_owner.py`](../opus-ebp-readiness-fixes-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-SCRIPTVM-READINESS-EDITS-1002` | [`opus-scriptvm-readiness-fixes-1002/apply_by_owner.py`](../opus-scriptvm-readiness-fixes-1002/apply_by_owner.py) | 4 |
| `OPUS-REQ-EC7-PHYRE-READINESS-EDITS-1002` | [`opus-phyre-readiness-fixes-1002/apply_by_owner.py`](../opus-phyre-readiness-fixes-1002/apply_by_owner.py) | 6 |
| `OPUS-REQ-EC7-UI-READINESS-EDITS-1002` | [`opus-ui-readiness-fixes-1002/apply_by_owner.py`](../opus-ui-readiness-fixes-1002/apply_by_owner.py) | 8 |
| `OPUS-REQ-EC7-CRT-READINESS-EDITS-1002` | [`opus-crt-readiness-fixes-1002/apply_by_owner.py`](../opus-crt-readiness-fixes-1002/apply_by_owner.py) | 9 |
| `OPUS-REQ-EC7-ENGINE-A-READINESS-EDITS-1002` | [`opus-engine-a-readiness-fixes-1002/apply_by_owner.py`](../opus-engine-a-readiness-fixes-1002/apply_by_owner.py) | 6 |
| `OPUS-REQ-EC7-THIRDPARTY-READINESS-EDITS-1002` | [`opus-thirdparty-readiness-fixes-1002/apply_by_owner.py`](../opus-thirdparty-readiness-fixes-1002/apply_by_owner.py) | 4 |
| `OPUS-REQ-EC7-RESOURCE-A-READINESS-EDITS-1002` | [`opus-resource-a-readiness-fixes-1002/apply_by_owner.py`](../opus-resource-a-readiness-fixes-1002/apply_by_owner.py) | 5 |
| `OPUS-REQ-EC7-RENDER-A-READINESS-EDITS-1002` | [`opus-render-a-readiness-fixes-1002/apply_by_owner.py`](../opus-render-a-readiness-fixes-1002/apply_by_owner.py) | 8 |
| `OPUS-REQ-EC7-ENGINE-B-READINESS-EDITS-1002` | [`opus-engine-b-readiness-fixes-1002/apply_by_owner.py`](../opus-engine-b-readiness-fixes-1002/apply_by_owner.py) | 5 |
| `OPUS-REQ-EC7-RENDER-B-READINESS-EDITS-1002` | [`opus-render-b-readiness-fixes-1002/apply_by_owner.py`](../opus-render-b-readiness-fixes-1002/apply_by_owner.py) | 8 |
| `OPUS-REQ-EC7-RESOURCE-B-1002` | [`opus-resource-b-readiness-fixes-1002/apply_by_owner.py`](../opus-resource-b-readiness-fixes-1002/apply_by_owner.py) | 7 |
| `OPUS-REQ-EC7-RESIDUAL-1002` | [`opus-residual-readiness-fixes-1002/apply_by_owner.py`](../opus-residual-readiness-fixes-1002/apply_by_owner.py) | 8 |
| `OPUS-REQ-EC7-RENDER-C-READINESS-1002` | [`opus-render-c-readiness-fixes-1002/apply_by_owner.py`](../opus-render-c-readiness-fixes-1002/apply_by_owner.py) | 15 |
| `OPUS-REQ-EC7-RENDER-SLOT-CONSUME-1002` | [`opus-render-slot-consume-1002/apply_by_owner.py`](../opus-render-slot-consume-1002/apply_by_owner.py) | 1 |
| `OPUS-REQ-EC7-ASTRA3-CONSUME-1002` | [`opus-astra-returns-consume-1002/apply_by_owner.py`](../opus-astra-returns-consume-1002/apply_by_owner.py) | 1 |

## Consumer check (SWE2-EC7)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Application-Root/game-application.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-E-ids-140-171.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/the-encoded-id-class-registry.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/CONTRACT-resource-section-addressing.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ah-asset-header-manifests.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Weather/mweather-resource-format.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Weather/weather-probability-and-transition-roll.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Weather/weather-slot-state-model.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`
affected: `Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-facing-and-steering.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/heading-speed-to-position-delta.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md`
affected: `Database/FFXII TZA/07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`
affected: `Database/FFXII TZA/11-Party/CONTRACT-party-focus-and-control-suppression.md`
affected: `Database/FFXII TZA/11-Party/party-roster-and-control-suppression.md`
affected: `Database/FFXII TZA/11-Party/the-five-parallel-slot-maps.md`
affected: `Database/FFXII TZA/16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md`
affected: `Database/FFXII TZA/16-UI/Handbook/the-handbooks-monster-viewer.md`
affected: `Database/FFXII TZA/16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`
affected: `Database/FFXII TZA/16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md`
affected: `Database/FFXII TZA/16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`
affected: `Database/FFXII TZA/16-UI/Message-Windows/the-message-window-layout-readers.md`
affected: `Database/FFXII TZA/16-UI/Quest-List/the-quest-list-screen.md`
affected: `Database/FFXII TZA/16-UI/Text-And-Number-Rendering/the-text-control-code-language.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-status-shows-on-a-character.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-staged-look-command.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Rendering/character-render-object.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-menu-effect-registry.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/adm-add-motion-tables.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/the-pose-sequencer.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md`
affected: `Database/FFXII TZA/19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md`
affected: `Database/FFXII TZA/21-RNG-And-Determinism/which-roll-is-on-which-generator.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/third-party-middleware-inventory.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Maths-Library/the-maths-the-game-runs-on.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`
affected: `Database/FFXII TZA/25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/drawing-a-line-character-by-character.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/the-nine-patch-window-frame.md`

- consumer: the pages the batches edit: revised-here (OPUS's tagged edits, unchanged).
- consumer: the other lanes' shares of the same batches: routed by OPUS to their owners (each batch's own record).

run: `save_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-save-readiness-fixes-1002/save_check.py)
run: `rng_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-rng-readiness-fixes-1002/rng_check.py)
run: `spawn_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-spawn-readiness-fixes-1002/spawn_check.py)
run: `action_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-action-readiness-fixes-1002/action_check.py)
run: `movement_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-movement-readiness-fixes-1002/movement_check.py)
run: `party_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-party-readiness-fixes-1002/party_check.py)
run: `world_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-world-readiness-fixes-1002/world_check.py)
run: `actor_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-actor-readiness-fixes-1002/actor_check.py)
run: `ebp_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-ebp-readiness-fixes-1002/ebp_check.py)
run: `scriptvm_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-scriptvm-readiness-fixes-1002/scriptvm_check.py)
run: `phyre_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-phyre-readiness-fixes-1002/phyre_check.py)
run: `ui_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-ui-readiness-fixes-1002/ui_check.py)
run: `crt_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-crt-readiness-fixes-1002/crt_check.py)
run: `engine_a_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-engine-a-readiness-fixes-1002/engine_a_check.py)
run: `thirdparty_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-thirdparty-readiness-fixes-1002/thirdparty_check.py)
run: `resource_a_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-resource-a-readiness-fixes-1002/resource_a_check.py)
run: `render_a_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-render-a-readiness-fixes-1002/render_a_check.py)
run: `engine_b_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-engine-b-readiness-fixes-1002/engine_b_check.py)
run: `render_b_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-render-b-readiness-fixes-1002/render_b_check.py)
run: `resource_b_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-resource-b-readiness-fixes-1002/resource_b_check.py)
run: `residual_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-residual-readiness-fixes-1002/residual_check.py)
run: `render_c_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-render-c-readiness-fixes-1002/render_c_check.py)
run: `render_slot_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-render-slot-consume-1002/render_slot_check.py)
run: `astra3_check.py` at abac4e3d9 (FAILS 0) - [script](../opus-astra-returns-consume-1002/astra3_check.py)
