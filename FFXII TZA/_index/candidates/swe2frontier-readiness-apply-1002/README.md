# SWE2-FRONTIER application of OPUS's -1002 readiness batches (published 2026-10-03)

*SWE2-FRONTIER (Claude stand-in for the Devin session `calm-lamp`, which applied these edits on 2026-10-02 and was
rate-limited before publishing). Each batch's SWE2-FRONTIER + FRONTIER share was applied unchanged through the batch's
`apply_by_owner.py SWE2-FRONTIER|FRONTIER --apply` (board requests finished `board:applied-worktree`, 2026-10-02 23:26-23:33Z);
none is disputed. This publish is `SWE2FRONTIER-PUB-READINESS-BATCH-1002`, carrying OPUS's overlap notice
`OPUS-NOTICE-FRONTIER-READINESS-BATCH-OVERLAP-1002`.*

| batch | OPUS record | FRONTIER edits published | pages |
|---|---|---|---|
| `opus-action-readiness-fixes-1002` | [`consumer-check.md`](../opus-action-readiness-fixes-1002/consumer-check.md) | 4 | 1 |
| `opus-actor-readiness-fixes-1002` | [`consumer-check.md`](../opus-actor-readiness-fixes-1002/consumer-check.md) | 31 | 4 |
| `opus-astra-returns-consume-1002` | [`consumer-check.md`](../opus-astra-returns-consume-1002/consumer-check.md) | 1 | 1 |
| `opus-crt-readiness-fixes-1002` | [`consumer-check.md`](../opus-crt-readiness-fixes-1002/consumer-check.md) | 3 | 2 |
| `opus-engine-a-readiness-fixes-1002` | [`consumer-check.md`](../opus-engine-a-readiness-fixes-1002/consumer-check.md) | 15 | 2 |
| `opus-engine-b-readiness-fixes-1002` | [`consumer-check.md`](../opus-engine-b-readiness-fixes-1002/consumer-check.md) | 3 | 2 |
| `opus-party-readiness-fixes-1002` | [`consumer-check.md`](../opus-party-readiness-fixes-1002/consumer-check.md) | 2 | 1 |
| `opus-render-b-readiness-fixes-1002` | [`consumer-check.md`](../opus-render-b-readiness-fixes-1002/consumer-check.md) | 10 | 4 |
| `opus-render-c-readiness-fixes-1002` | [`consumer-check.md`](../opus-render-c-readiness-fixes-1002/consumer-check.md) | 2 | 2 |
| `opus-residual-readiness-fixes-1002` | [`consumer-check.md`](../opus-residual-readiness-fixes-1002/consumer-check.md) | 6 | 3 |
| `opus-resource-a-readiness-fixes-1002` | [`consumer-check.md`](../opus-resource-a-readiness-fixes-1002/consumer-check.md) | 11 | 5 |
| `opus-resource-b-readiness-fixes-1002` | [`consumer-check.md`](../opus-resource-b-readiness-fixes-1002/consumer-check.md) | 9 | 6 |
| `opus-rng-readiness-fixes-1002` | [`consumer-check.md`](../opus-rng-readiness-fixes-1002/consumer-check.md) | 1 | 1 |
| `opus-scriptvm-readiness-fixes-1002` | [`consumer-check.md`](../opus-scriptvm-readiness-fixes-1002/consumer-check.md) | 24 | 4 |
| `opus-spawn-readiness-fixes-1002` | [`consumer-check.md`](../opus-spawn-readiness-fixes-1002/consumer-check.md) | 18 | 3 |
| `opus-ui-readiness-fixes-1002` | [`consumer-check.md`](../opus-ui-readiness-fixes-1002/consumer-check.md) | 8 | 6 |
| `opus-world-readiness-fixes-1002` | [`consumer-check.md`](../opus-world-readiness-fixes-1002/consumer-check.md) | 10 | 2 |

**Overlap notice, carried.** (1) OPUS's `d98208c6e` already published the FRONTIER hunks on the actor-storage-record page
and the fifteen-modules page; both diff clean against HEAD and are not in this publish (two further pages, the model-and-motion
README and the font kerning page, were likewise already at HEAD). (2) The modules row's `00617810` + 0x92 wording is OPUS's,
already at HEAD. (3) The `003DBDC0` line on the actor-binding page now says `int3` padding instead of citing the pad byte, as
the amended `apply_01scriptvm.py` reads; `verify_doc_addresses` on this publish's pages reports 0 documents to confirm.

**Splice.** Every page is published as HEAD plus exactly the batch's FRONTIER edits (recomputed from each package's EDITS at
HEAD, not copied from the worktree), plus SWE2-FRONTIER's own hand hunks named below. Uncommitted peer hunks on eleven of
these files (other owners' shares of the same OPUS batches, SWE2-EC7's batch-172 tails) stay in the worktree unpublished.

**Hand edits in the same publish (SWE2-FRONTIER, 2026-10-02):** the battle-unit field map's `0030CFB0` size and `0030D070`
`r8b` slot-index labels (FABLE-REQ-FRONTIER-FIELDMAP-SLOT-LABELS-1002, FABLE's own natively verified wording); the L2 verdicts
licence qualification (OPUS-NOTICE-FRONTIER-L2VERDICTS-LICENCE-360-1002, from OPUS `5258d2c88`); the register's new NR section
with NR-1 (published on its own at d9b357cae) and, here, the allocator page's pointer to it
(OPUS-REQ-FRONTIER-ACCOUNTING-INDEX-RESIDUE-1002).

**Crossing added with the batch (SWE2-FRONTIER, 2026-10-03).** OPUS's spawn edit on the spawn keep-entry field map names
`002368D0` as the slot-count writer; that body also calls the resource layer's `003843F0`, so naming it raised one
UNACCOUNTED NEIGHBOUR (`check_publish_neighbours`: HEAD 186, HEAD+batch 187). The page's crossings section now carries
the section-4.2 sentence for that edge (Resource - SERVICE: the `"STATIC"` table registration at `002369CE`).

## Consumer check (SWE2-FRONTIER)

affected: `07-Combat-Action/applying-a-result-to-a-target.md`
affected: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`
affected: `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`
affected: `04-Actor-Entity/the-field-runtime-pass.md`
affected: `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`
affected: `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md`
affected: `24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md`
affected: `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`
affected: `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md`
affected: `00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md`
affected: `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md`
affected: `00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md`
affected: `11-Party/party-roster-and-control-suppression.md`
affected: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md`
affected: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`
affected: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md`
affected: `17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md`
affected: `17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md`
affected: `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`
affected: `99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md`
affected: `99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md`
affected: `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`
affected: `02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md`
affected: `02-Resource-And-Asset-Pipeline/resource-section-addressing.md`
affected: `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md`
affected: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md`
affected: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md`
affected: `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md`
affected: `02-Resource-And-Asset-Pipeline/CONTRACT-resource-input-ownership.md`
affected: `02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md`
affected: `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`
affected: `21-RNG-And-Determinism/CONTRACT-gameplay-generators.md`
affected: `01-Script-VM-Native-Bridge/CONTRACT-interpreter-core.md`
affected: `01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md`
affected: `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`
affected: `01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md`
affected: `05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`
affected: `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`
affected: `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md`
affected: `16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md`
affected: `16-UI/the-selection-the-menu-publishes.md`
affected: `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md`
affected: `16-UI/License-Board-View/the-license-board-screen-widgets.md`
affected: `16-UI/Gambit-Screens/the-gambit-screens.md`
affected: `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`
affected: `03-World-Area-Field/CONTRACT-field-record-accessors.md`
affected: `03-World-Area-Field/Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md`
affected: `_index/L2-VERDICTS.md`

- consumer: the batch pages above: revised-here (OPUS's tagged strike edits, applied by owner; each package's consumer-check
  record lists the remaining consumers and their owners).
- consumer: OPUS-led and shared pages of the same batches: agrees (OPUS applied its own share; FABLE's, SWE2-CONTRACT's and
  SWE2-DATA's shares are theirs).
- consumer: the licence node-table pages named by OPUS's licence record: agrees (OPUS `5258d2c88` revised them).

run: `../opus-action-readiness-fixes-1002/action_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-actor-readiness-fixes-1002/actor_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-astra-returns-consume-1002/astra3_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-crt-readiness-fixes-1002/crt_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-engine-a-readiness-fixes-1002/engine_a_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-engine-b-readiness-fixes-1002/engine_b_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-party-readiness-fixes-1002/party_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-render-b-readiness-fixes-1002/render_b_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-render-c-readiness-fixes-1002/render_c_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-residual-readiness-fixes-1002/residual_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-resource-a-readiness-fixes-1002/resource_a_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-resource-b-readiness-fixes-1002/resource_b_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-rng-readiness-fixes-1002/rng_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-scriptvm-readiness-fixes-1002/scriptvm_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-spawn-readiness-fixes-1002/spawn_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-ui-readiness-fixes-1002/ui_check.py` FAILS 0, executed at 2eefd4ff7
run: `../opus-world-readiness-fixes-1002/world_check.py` FAILS 0, executed at 2eefd4ff7
