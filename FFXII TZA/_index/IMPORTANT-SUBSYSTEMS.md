# The important subsystems — the set the reconstruction gate answers for

*Authored by FABLE (semantic/architecture lead), 2026-09-11, against
[RECONSTRUCTION-CHARTER](../../../RECONSTRUCTION-CHARTER.md) sections 26 and 27, at OPUS's request
(`OPUS-REQ-FABLE-IMPORTANT-SUBSYSTEMS`). Machine-readable twin:
[`important-subsystems.tsv`](important-subsystems.tsv). This is a judgement, stated so it can be
challenged row by row; it is not a count of pages and it is not a completion claim.*

> **Section 26 gates a subsystem; section 27 gates the database over its important subsystems. Neither
> names the set.** A `system:` page is not a subsystem — most are field maps, format sheets, censuses
> and helpers that *feed* one — and a contract is one family's answer, so counting either measures
> the wrong thing. The set below is what the shipped game's behaviour is made of at runtime: each row
> owns state, has a lifecycle, and would have to be reproduced for the game to play as shipped.
> **Forty-six subsystems in three tiers; thirty-three have at least one contract; thirteen have none.**
>
> *Corrected 2026-09-13 (OPUS, `OPUS-SUBSYS-INDEX-RECONCILE`). This sentence read *"twenty-five … twenty-one"*, the figures from before FABLE's same-day reconciliation (`689ea6a`) mapped eight existing contracts onto nine rows. **The summary table in §7 was updated and this headline was not** — and this is the sentence a reader quotes. An independent census run here, matching every `CONTRACT-*.md` on disk against the machine-readable twin, reproduces FABLE's result exactly: **32 rows naming a contract, 14 naming none, 38 distinct contracts named, every named contract present on disk, and exactly four contracts on disk that no row names** — the three Phyre contracts and the Lua chunk-loader — which is not drift but §1's rule working, since categories 22–26 contribute no rows. **A mapped contract is still not a finished subsystem**; see §7.*

> *Corrected again 2026-09-20 (OPUS, `OPUS-SUBSYS-ORPHAN-CONTRACT-DRIFT`). The figures above read
> *"thirty-two … fourteen"* and the note below read **"exactly four"** unnamed contracts. Both had
> drifted, and **the cause is dated rather than guessed**: the 2026-09-13 reconciliation
> (`689ea6aa5`) landed at **03:49** and five further contracts were committed between **05:32 and
> 06:52 the same day**, so its count was right when written and stale within three hours. A fresh
> census of every `CONTRACT-*.md` against the machine-readable twin now reports **48 on disk, 41
> distinct named by a row, 0 named-but-missing, and SEVEN named by no row**. Of the seven, four are
> the §1 exclusions this note already describes — the three Phyre contracts and the Lua chunk-loader
> — and **three are not**: `CONTRACT-efx-source-rebase` and `CONTRACT-resource-entry-tree`
> (category 02, both implementing a page no row names) and `CONTRACT-authored-command-ramp-channels`
> (category 17). Those three are a membership question under §1 and are routed to FABLE as
> `OPUS-REQ-FABLE-THREE-CONTRACTS-NO-ROW-NAMES` rather than decided here. **Two of the five were
> decided by measurement, not judgement**: `CONTRACT-save-container-transform` and
> `CONTRACT-storage-read-completion` both declare `implements:` the save-image-buffers page that
> **S-43 already names** among its `primary_pages`, so S-43 now names three contracts. The count
> also moves because **S-33 gained its first contract** the same day
> (`CONTRACT-world-loot-pickup-pool.md`), which is what takes the contract-less set from fourteen to
> thirteen: S-01, S-04, S-06, S-08, S-10, S-12, S-14, S-16, S-21, S-31, S-37, S-39, S-40.*

## 1. How a row earned its place

A subsystem is listed when all three hold:

1. **It owns runtime state** — a pool, a record, a table it fills, a state word — rather than only
   describing a file or a type that another row consumes.
2. **It has a lifecycle the engine drives** — initialised, ticked or invoked, torn down — so section
   26's questions about initialisation, update ordering and lifetime are askable of it.
3. **The player's experience depends on it** — a reconstruction that stubbed it would play visibly
   or measurably differently.

Field maps, format sheets and censuses are listed **under** the row they serve as its *types* or
*inputs*, never as rows. Categories 22–26 and 99 (PhyreEngine middleware, third-party libraries, the
CRT, the two container formats, the residual) contribute no rows: they are reproduced by linking or
by a format reader, not by reconstructing a game subsystem — with one exception noted in §4.

**Tiers.** *Core*: the game does not play without it. *Supporting*: the game plays but not as
shipped (audio, presentation, platform, tooling paths the shipped game exercises). *Deferred*:
present in the executable, exercised by developers or by no shipped content; a reconstruction may
stub it and say so. A deferral is *local* when stubbing it changes nothing another row depends on;
every deferred row below states why.

## 2. The set

Columns: the primary page(s) a researcher starts from; the contract(s) that implement it, or **none**;
tier; a note on the row's edge. Pages are the database's, so their statuses (DOCUMENTED / PARTIAL /
REOPENED) are the row's honest state, not this table's.

### 00 — Engine core and frame

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-01 | **Application root and boot** — the VBF mount, the startup latch, what boot fixes and loads | [game-application](../00-Engine-Core-Runtime/Application-Root/game-application.md); [what-the-engine-fixes-at-boot](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md) | none | core |
| S-02 | **The world tick and the field frame** — the per-frame order on the battle layer and the one-word update gate | [the-world-tick-and-the-field-frame](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md); [one-word-decides-which-fifteen-subsystems-tick](../00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md); [the-time-stop-and-system-stop-registry](../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) *(added 2026-09-12: which actors a frame advances)* | [CONTRACT-per-frame-update-gate](../00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md) *(mapped 2026-09-13)* | core |
| S-03 | **Battle runtime mode ladder** — who owns the party (script, area, combat, UI) | [battle-runtime-mode-ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) | [CONTRACT-battle-runtime-mode](../00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md) *(mapped 2026-09-13)* | core |
| S-04 | **Encoded-id space and class registry** — the fifteen inventory classes behind `id >> 12`, the query record | [the-encoded-id-space-and-the-query-record](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md); [the-encoded-id-class-registry](../00-Engine-Core-Runtime/the-encoded-id-class-registry.md) | none | core |
| S-05 | **Shared transform workbench** — the matrix area four subsystems pass arguments through | [the-shared-transform-workbench](../00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md) | [CONTRACT-transform-workbench-save-restore](../00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md); [CONTRACT-transform-primitives](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) *(mapped 2026-09-13)* | core |
| S-06 | **Developer tuning console** — 282 commands over the render-settings block | [the-282-command-parameter-console](../00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md) | none | deferred — developer-only; nothing in the shipped player path reads its outputs except the render-settings block S-38 also writes |

### 01 — Script VM

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-07 | **The zone-script VM** — the 100-opcode interpreter, verb dispatch and parameter encoding, the native command lifecycle (begin / poll / result) | [worldactor-scriptvm-interpreter](../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md); [scriptvm-verb-dispatch-and-parameter-encoding](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md); [native-command-lifecycle](../01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md) | [CONTRACT-script-to-native-bridge](../01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md); [CONTRACT-verb-dispatch-abi](../01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md) *(mapped 2026-09-13)* | core |

### 02 — Resources

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-08 | **The resource request queue and file layer** — 64 slots, the file-size table, loose files then the archive, the BigFile index | [the-resource-request-queue](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md); [file-size-tables-fst](../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md); [how-the-bigfile-index-loads-and-is-verified](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md) | none | core |
| S-09 | **The authored-data table registry** — the 63 slots, the `.ard` binder, section addressing, row lookup | [authored-data-table-registry](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md); [how-the-ard-loader-binds-area-battle-data](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md); [resource-section-addressing](../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) | [CONTRACT-authored-table-row-lookup](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) | core |
| S-10 | **The authored expression evaluator** — how an authored number gets its randomness | [how-an-authored-number-gets-its-randomness](../02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md) | none | core |
| S-47 | **Resource-entry tree and arena reference lifetime** — ordered-tree membership, the EFX source rebase, who owns a loaded resource | [authored-reference-lifetime-evidence](../02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md) | [CONTRACT-resource-entry-tree](../02-Resource-And-Asset-Pipeline/CONTRACT-resource-entry-tree.md); [CONTRACT-efx-source-rebase](../02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md) | core |

### 03 — World, area, field

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-11 | **Field records and area transition** — `navimapdata.bin`, trigger points, the environment variant | [field-record-table-navimapdata](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md); [walking-into-an-authored-trigger-point](../03-World-Area-Field/walking-into-an-authored-trigger-point.md); [choosing-the-field-environment-variant](../03-World-Area-Field/choosing-the-field-environment-variant.md) | [CONTRACT-field-record-accessors](../03-World-Area-Field/CONTRACT-field-record-accessors.md) | core |
| S-12 | **Weather** — the slot state model, the probability roll, the apply | [weather-slot-state-model](../03-World-Area-Field/Weather/weather-slot-state-model.md); [weather-probability-and-transition-roll](../03-World-Area-Field/Weather/weather-probability-and-transition-roll.md); [weather-apply-and-environment-materialization](../03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md) | none | supporting |

### 04 — Actors

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-13 | **Actor storage, manager slots and the unit pool** — the record behind every actor, the five manager slots, the battle-unit slot pool and actor class | [the-record-behind-every-actor](../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md); [the-actor-manager-record-field-map](../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md); [battleunit-slot-pool-and-actor-class](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) | [CONTRACT-actor-record-pool-and-region-map](../04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md); [CONTRACT-manager-slot-entry-tables](../04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md) | core |
| S-14 | **Battle-unit construction from its definition** — the two tables, the two paths, every field the installer writes | [how-a-battle-unit-is-built-from-its-definition](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md); type: [the-battle-unit-field-map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) | none | core |
| S-15 | **The field runtime pass** — how one frame drives every actor's script | [the-field-runtime-pass](../04-Actor-Entity/the-field-runtime-pass.md) | [CONTRACT-field-runtime-pass](../04-Actor-Entity/CONTRACT-field-runtime-pass.md) *(mapped 2026-09-13)* | core |

### 05 — Spawn and encounter lifecycle

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-16 | **Spawn placement, the keep window and retirement** | [spawn-placement-and-retirement](../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md); [spawn-placement-height-and-authored-tunables](../05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md); type: [the-spawn-keep-entry-field-map](../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) | none | core |
| S-17 | **Group completion and respawn** — the dead-member ledger and the cooldown clock | [when-a-group-is-wiped-and-when-it-comes-back](../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md); [why-the-enemies-you-killed-come-back](../05-Spawn-Encounter-Lifecycle/why-the-enemies-you-killed-come-back.md) | [CONTRACT-group-completion-and-respawn](../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md) | core |

### 06 — Movement

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-18 | **Locomotion and steering** — heading and speed to position, facing, movement mode, battle locomotion | [heading-speed-to-position-delta](../06-Movement-And-Navigation/heading-speed-to-position-delta.md); [how-a-character-turns](../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md); [battle-locomotion-steering-and-recovery](../06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md) | [CONTRACT-facing-and-steering](../06-Movement-And-Navigation/CONTRACT-facing-and-steering.md) | core |
| S-19 | **The movement body pool and the separation pass** | [the-movement-body-pool-and-the-separation-pass](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) | [CONTRACT-movement-body-pool](../06-Movement-And-Navigation/CONTRACT-movement-body-pool.md) | core |
| S-51 | **The navigation mesh and the corridor-query layer** — the authored mesh dataset, the region query, A* search, portal costs, the step-follower | [how-a-unit-finds-its-way-across-the-navigation-mesh](../06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md) | [CONTRACT-corridor-query-family](../06-Movement-And-Navigation/CONTRACT-corridor-query-family.md) | core |

### 07 — Combat action

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-20 | **Command commit and action dispatch** — the moment an action is committed, the native command seam, the handler table, availability and reason codes, combos | [the-moment-an-action-is-committed](../07-Combat-Action/the-moment-an-action-is-committed.md); [native-command-seam](../07-Combat-Action/Command-And-Action-Seam/native-command-seam.md); [battle-action-handler-table](../07-Combat-Action/Action-Dispatch/battle-action-handler-table.md); [how-a-combo-continues-and-what-it-blocks](../07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md) | [CONTRACT-commit-action](../07-Combat-Action/CONTRACT-commit-action.md); [CONTRACT-battle-target-buffer](../07-Combat-Action/CONTRACT-battle-target-buffer.md) | core |
| S-21 | **Result application and post-result events** — the result record, the applier, the battle message table | [applying-a-result-to-a-target](../07-Combat-Action/applying-a-result-to-a-target.md); [the-post-result-events-and-the-battle-message-table](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md); type: [the-result-record-field-map](../07-Combat-Action/Result-Record/the-result-record-field-map.md) | none | core |

### 08 — Combat formula

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-22 | **The formula step table and calculator slots** — recipes, the preparation family, the evaluation context, the scratch block, elemental and weather scaling | [combat-formula-step-table](../08-Combat-Formula/Step-Table/combat-formula-step-table.md); [attack-defense-preparation-and-stat-scaling](../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md); [ranged-weapon-recipes](../08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md); [weather-terrain-element-scaling](../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md) | [CONTRACT-preparation-step-family](../08-Combat-Formula/CONTRACT-preparation-step-family.md) | core |
| S-23 | **The HP write and the lethal transition** | [the-hp-write-and-the-lethal-transition](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) | [CONTRACT-hp-write-and-lethal-transition](../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md) | core |
| S-24 | **Stat derivation and the auto-status rebuild** — where a stat number comes from, equipment's single rebuild | [where-a-stat-number-comes-from](../08-Combat-Formula/where-a-stat-number-comes-from.md); [the-auto-status-rebuild](../08-Combat-Formula/the-auto-status-rebuild.md); [equipment-slots-and-the-single-stat-rebuild](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) | [CONTRACT-auto-status-rebuild](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) | core |

### 09 — AI and gambits

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-25 | **Gambit evaluation, set selection and enmity** | [gambit-evaluation-and-enmity](../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md); [which-gambit-set-fires-and-how-a-command-switches-it](../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md) | [CONTRACT-gambit-walk](../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md) | core |

### 10 — Status and periodic

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-26 | **The status write and the two-layer effect model** | [the-status-write-and-its-side-effects](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md); [two-layer-effect-model](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) | [CONTRACT-status-write](../10-Status-Periodic-Terminal/CONTRACT-status-write.md) *(mapped 2026-09-13)* | core |
| S-27 | **The periodic tick** — regen, drain, MP, what ends a status | [what-the-periodic-tick-does](../10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md); [where-mp-comes-from](../10-Status-Periodic-Terminal/where-mp-comes-from.md) | [CONTRACT-status-write](../10-Status-Periodic-Terminal/CONTRACT-status-write.md) *(mapped 2026-09-13)* | core |

### 11 — Party

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-28 | **Party roster, control suppression and the leader change** — the five slot maps, the reserve | [party-roster-and-control-suppression](../11-Party/party-roster-and-control-suppression.md); [active-party-reserve-and-the-moment-the-leader-changes](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md); [the-five-parallel-slot-maps](../11-Party/the-five-parallel-slot-maps.md); type: [the-battle-state-block-field-map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) | [CONTRACT-party-slot-assignment](../11-Party/CONTRACT-party-slot-assignment.md) | core |

### 12 — Items, equipment, shops, licences

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-29 | **Inventory, item use and equipment compatibility** | [using-an-item-is-an-action-that-costs-an-item](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md); [item-id-encoding-and-equipment-compatibility](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md) | [CONTRACT-inventory-class-storage](../12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md) *(mapped 2026-09-13)* | core |
| S-30 | **Shops and the bazaar** — stock ladders, the loot-sold tally, purchase | [the-shop-table-and-its-stock-gates](../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md); [the-bazaar-recipe-unlock-and-purchase](../12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md) | [CONTRACT-bazaar-unlock-and-purchase](../12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md) | core |
| S-31 | **The licence board and the licence check** | [license-check-what-the-board-actually-tests](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md); [license-board-grid-format](../12-Items-Equipment-Shops-License/license-board-grid-format.md) | none | core |

### 13 — Rewards and progression

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-32 | **Enemy death and its rewards** — experience and LP division, loot drops, the chain, gil, level-up | [what-happens-when-an-enemy-dies](../13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md); [how-experience-is-computed-and-divided](../13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md); [loot-drops-and-enemy-chain](../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md); [gil-storage-clamp-and-every-path-that-moves-it](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md); [what-happens-when-a-character-levels-up](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md) | [CONTRACT-experience-and-licence-award](../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md) | core |
| S-33 | **World loot pickups** — the ten-slot pool, the blink, the despawn | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) | none | core |

### 14 — Story and events

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-34 | **Persistent flag banks and event memory** | [persistent-flag-banks](../14-Story-Event-Quest-Hunt/persistent-flag-banks.md); [event-memory-at-actor-bind](../14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md) | [CONTRACT-persistent-flag-banks](../14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md) | core |

### 15 — Input

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-35 | **The input stack, binding profiles and the capability policy** — devices, channels, the name registry, the 16 × 32-bit inhibition policy, the R2 toggle | [input-stack-device-channel-and-bindings](../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md); [binding-profiles-remapping-and-control-state](../15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md); [capability-inhibition-policy](../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) | [CONTRACT-binding-profiles](../15-Input/Binding-Profiles/CONTRACT-binding-profiles.md); [CONTRACT-input-name-registry](../15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md) | core |

### 16 — UI

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-36 | **The widget object model, its message protocol and the request router** | [the-widget-constructor-and-object-sizes](../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md); [the-widget-message-protocol](../16-UI/Widget-Object-Model/the-widget-message-protocol.md); [ui-request-router](../16-UI/Request-Router/ui-request-router.md) | [CONTRACT-widget-object](../16-UI/Widget-Object-Model/CONTRACT-widget-object.md) | core |
| S-37 | **Text rendering and the control-code language, DynGeo drawing** | [the-text-control-code-language](../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md); [dyngeo-instance-family](../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md) | none | supporting |

### 17 — Presentation

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-38 | **Character rendering** — the render object, the render record array, transform publish, the coast-down latch | [character-render-object](../17-Presentation-Rendering/Character-Rendering/character-render-object.md); [the-character-render-record-array](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) | [CONTRACT-character-transform-publish](../17-Presentation-Rendering/CONTRACT-character-transform-publish.md); [CONTRACT-coast-down-latch](../17-Presentation-Rendering/CONTRACT-coast-down-latch.md); [CONTRACT-render-record-pool-lifecycle](../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md) | supporting |
| S-39 | **The render command list and the graphics-thread handshake** | [the-ordered-render-command-list](../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md); [the-shared-command-state-word](../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md) | none | supporting |
| S-40 | **Post-processing** — the Yebis effect catalogue | [the-post-processing-effect-catalogue](../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md) | none | deferred — a licensed library behind a catalogue; stubbing it changes the image, not any state another row reads |
| S-48 | **Authored command ramp channels** — the channel state machine the presentation layer replays | [presentation layer index](../17-Presentation-Rendering/README.md) | [CONTRACT-authored-command-ramp-channels](../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md) | supporting |

### 18 — Audio

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-41 | **Sound request to voice** — the audio boundary, the bank and controller family, fades, the spatial model | [how-a-sound-request-becomes-a-voice](../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md); [audio-bank-and-controller-family](../18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md); [the-spatial-audio-object-model](../18-Audio/the-spatial-audio-object-model.md) | [CONTRACT-sound-request](../18-Audio/Audio-Boundary/CONTRACT-sound-request.md) *(mapped 2026-09-13)* | supporting |
| S-42 | **Field music selection** — the area's ladder, the mode overrides, the bank file | [how-the-music-changes-when-you-change-area](../18-Audio/how-the-music-changes-when-you-change-area.md); [the-music-control-file-and-the-bgm-stream](../18-Audio/the-music-control-file-and-the-bgm-stream.md) | [CONTRACT-field-music-selection](../18-Audio/CONTRACT-field-music-selection.md) | supporting |

### 19 — Save, load, settings

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-43 | **The save image** — buffers, header and payload, capture, what loading normalises | [save-image-buffers-header-and-payload](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md); [version-stamps-and-what-loading-normalises](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md); type: [the-save-payload-field-map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) | [CONTRACT-save-image-buffers](../19-Save-Load-Settings/CONTRACT-save-image-buffers.md) | core |
| S-44 | **Game settings and locale** | [game-settings-ini-and-runtime-config](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md); [language-selection-and-locale-ids](../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md) | [CONTRACT-game-setting-config](../19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md) | supporting |

### 20 – 21 — Platform and RNG

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-45 | **Steam integration and achievements** | [steam-integration-and-achievement-catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) | [CONTRACT-achievement-counters](../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md) | deferred — platform service; stubbing it changes no gameplay state, and the counters it reads are S-32's |
| S-46 | **RNG streams and which roll is on which generator** | [rng-streams](../21-RNG-And-Determinism/rng-streams.md); [which-roll-is-on-which-generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) | [CONTRACT-gameplay-generators](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) | core |

### 22 — PhyreEngine middleware

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-49 | **Phyre asset container and class-descriptor surface** — cluster header, packed namespace, reflection metadata FFXII consumes | [the-cluster-header-and-what-the-loader-rejects](../22-Middleware-PhyreEngine/Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md); [the-packed-namespace-and-the-file-side-schema](../22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md); [class-descriptor-and-metadata-system](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) | [CONTRACT-phyre-cluster-header](../22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md); [CONTRACT-phyre-packed-namespace](../22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md); [CONTRACT-phyre-class-descriptor](../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md) | supporting |

### 23 — Third-party libraries

| id | subsystem | primary pages | contract | tier |
|---|---|---|---|---|
| S-50 | **Lua core loader surface** — the chunk loader and what it accepts | [the-lua-loader-and-what-it-accepts](../23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md) | [CONTRACT-lua-chunk-loader](../23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md) | deferred — licensed library, accepted as black box |

## 3. What the set says about the gate

| | |
|---|---|
| rows | ~~46: 36 core, 7 supporting, 3 deferred~~ **51: 38 core, 9 supporting, 4 deferred** — S-47..S-51 registered in the tsv and reconciled into this table 2026-09-21 (FRONTIER) |
| rows with at least one contract | ~~25 (21 core, 3 supporting — S-38, S-42, S-44 — and 1 deferred — S-45)~~ ~~32 (27 core, 4 supporting — S-38, S-41, S-42, S-44 — and 1 deferred — S-45), reconciled 2026-09-13 (FABLE): eight existing contracts, covering nine rows, were missing from this table — see the note below~~ **46 (38 core, 6 supporting — S-38, S-41, S-42, S-44, S-48, S-49 — and 2 deferred — S-45, S-50)**, re-derived from the tsv `contracts` column 2026-09-21 — the tsv is the authoritative binding (see the contract-column ruling in `L2-VERDICTS.md`) |
| core rows with **no contract** | ~~**15**: S-01, S-02, S-03, S-04, S-08, S-10, S-14, S-15, S-16, S-21, S-26, S-27, S-29, S-31, S-33~~ ~~**9**: S-01, S-04, S-08, S-10, S-14, S-16, S-21, S-31, S-33~~ **0** — every core row is now contracted per the tsv |
| core rows whose primary page is PARTIAL or REOPENED | S-03, S-04, S-08, S-10, S-16 (REOPENED), S-20 (combos), S-22 (recipes), S-24, S-25, S-29, S-30, S-35 (policy REOPENED), S-36, S-47 |

> **Reconciled 2026-09-13 (FABLE).** A census of every `CONTRACT-*.md` against this table found **12 contracts the table did not
> list**. Eight belong to rows here and are now mapped, to nine rows: `CONTRACT-per-frame-update-gate` (S-02), `CONTRACT-battle-runtime-mode`
> (S-03), `CONTRACT-transform-primitives` (S-05, beside the workbench contract), `CONTRACT-verb-dispatch-abi` (S-07, beside the
> bridge contract), `CONTRACT-field-runtime-pass` (S-15), `CONTRACT-status-write` (S-26 and S-27 — its `implements:` names the
> periodic-tick page), `CONTRACT-inventory-class-storage` (S-29, scope *family*, readiness BEHAVIORALLY UNDERSTOOD) and
> `CONTRACT-sound-request` (S-41). The remaining four — three Phyre contracts and the Lua chunk-loader contract — have no row in this set.
> **Updated 2026-09-21 (FRONTIER):** they do now — S-49 carries the three Phyre contracts and S-50 the Lua chunk-loader.
> **A mapped contract is not a finished subsystem**: each covers the operation or family its own `scope:` states, and the
> paragraph below about which uncovered rows matter first now reads S-14 and S-21 for the first minute of play, S-01 for frame
> ordering.

~~**So contract coverage over the core set is 21 of 36, and the fifteen uncovered core rows are the
denominator the gate has been missing.**~~ *(superseded by the reconciliation: 27 of 36, nine uncovered)* They are not equal: S-14 (unit construction), S-21 (result
application), S-26 (the status write) and S-27 (the periodic tick) are the four whose absence would
show in the first minute of play; S-01, S-02 and S-15 are frame-ordering rows a reconstruction needs
before any other row can run at all.

**This set does not make the gate closer.** Section 26 is answered per row by its pages and
contracts, and the two criteria OPUS measured as denied — runtime validation and observable behaviour
— are denied for every row here whose evidence is static, which is nearly all of them (27 of the 235
pages in categories 00–21 cite an experiment record at all). Under the phase control of 2026-09-11 the
team stays database-first; this list is the denominator for the readiness checkpoint that will be
published through the normal workflow when the gate is believed satisfied, and a reason it is not
believed satisfied now.

## 4. Rows deliberately not listed

- **Field maps and censuses** (battle unit, actor storage, spawn record, stats record, result record,
  evaluation context, save payload, battle-state block): types. Each is named under the row it serves.
- **Format sheets** (`.fst`, `.ard`, `.nmb`, `.sab`, `.cm` / `.ca`, TIM2, `sloc` / `lmap`, EFX / EFB, the
  license grid): inputs of S-08 / S-09 / S-38 / S-41; a reconstruction reads them, it does not *be* them.
- **Category 22 PhyreEngine, 23 third-party, 24 CRT**: linked or replaced, not reconstructed. The one
  exception with a contract, [CONTRACT-lua-chunk-loader](../23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md),
  describes a library boundary the shipped game crosses and is scored with the supporting tier if the
  scorer wants it; it is not a row because the game's behaviour does not live in it.
- **Category 25 / 26 containers** and **99 residual**: formats and unassigned functions.
- **The developer console (S-06) is listed but deferred**, so that its exclusion is a stated decision
  rather than an omission.

## 5. How to challenge a row

Add, split, merge or re-tier a row by naming the state it owns and the lifecycle that drives it; a
row without both is a type or a format and belongs in §4. Record the change here and in the TSV in
the same commit, and say which of section 26's questions the change makes askable or unaskable.
