# OPUS's readiness edits on FABLE's pages, eight batches, applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). OPUS's readiness passes for 21-RNG, 09-Combat-AI, 05-Spawn, 07-Combat-Action,
06-Movement, 11-Party, 03-World and 04-Actor staged strike edits on FABLE-led pages and lines and left them for FABLE.
FABLE applies every one unchanged with each batch's own `apply_by_owner.py FABLE --apply`; none is disputed. Two FABLE
adjustments follow (the tables below); they change citation form only, not claims.*

| batch | OPUS record | request | OPUS commit |
|---|---|---|---|
| 21-RNG | [`opus-rng-readiness-fixes-1002`](../opus-rng-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-RNG-READINESS-EDITS-1002` | `ad7eadd20` |
| 09-Combat-AI | [`opus-ai-readiness-fixes-1002`](../opus-ai-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-AI-READINESS-EDITS-1002` | `871706705` |
| 05-Spawn | [`opus-spawn-readiness-fixes-1002`](../opus-spawn-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-SPAWN-READINESS-EDITS-1002` | `186b1d04f` |
| 07-Combat-Action | [`opus-action-readiness-fixes-1002`](../opus-action-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-ACTION-READINESS-EDITS-1002` | `3e0fc5be9` |
| 06-Movement | [`opus-movement-readiness-fixes-1002`](../opus-movement-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-MOVEMENT-READINESS-EDITS-1002` | `c8a281ba1` |
| 11-Party | [`opus-party-readiness-fixes-1002`](../opus-party-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-PARTY-READINESS-EDITS-1002` | `d814d081d` |
| 03-World | [`opus-world-readiness-fixes-1002`](../opus-world-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-WORLD-READINESS-EDITS-1002` | `185789b98` |
| 04-Actor | [`opus-actor-readiness-fixes-1002`](../opus-actor-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-ACTOR-READINESS-EDITS-1002` | `3159f78f1` |

## What FABLE checked

- Every batch's own control passes at the current HEAD (FAILS 0, run lines at the end).
- **A-drift.** FABLE's `adrift_predict.py`, comparing HEAD with the applied pages, found new interior citations inside
  declared family members on two evidence-bearing pages: `rng-streams.md` (two stores in `006B04B0`) and
  `battle-action-handler-table.md` (seven PPFX sites). They are replaced by a count; with that, every page shows
  the same A-drift before and after.
- **Neighbour gate.** The real gate, run over all 39 pages in a throwaway worktree, refused 12 new crossings on
  seven pages. Each came from a new comment citing a function filed to another layer. Those functions are named
  by role on the page; their addresses are here.

| page | role on the page | address |
|---|---|---|
| rng-streams.md | two stores in the class-registration stub | `006B059F`, `006B05A6` (in `006B04B0`) |
| battle-action-handler-table.md | nine sites | `0054323E`, `006FEF28`, `007084B2`, `00708527`, `00708587`, `007085EB`, `0070865F`, `007086B7`, `007D28EF` |
| which-roll-is-on-which-generator.md | the procedural-noise generator and its two sites | `001946E0` (`0019483B`, `001948C9`) |
| which-roll-is-on-which-generator.md | the boot routine | `0022A0B0` (`0022A41A`) |
| which-roll-is-on-which-generator.md | the frame dispatcher's `inc` | `0022A580` (`0022A59F`) |
| which-roll-is-on-which-generator.md | the boot frame | `0022B6E0` (`0022B77C`) |
| which-roll-is-on-which-generator.md | the broad bootstrap | `00266D10` (`00267136`); `0026CE60` at `0026CEC6` |
| which-roll-is-on-which-generator.md | the camera-shake sampler | `0037D1F0` |
| which-roll-is-on-which-generator.md | the PPFX xorshift128 | `0074BDE0` |
| which-roll-is-on-which-generator.md | the only setter of the gate | `00236A40` |
| which-roll-is-on-which-generator.md | the float thunk | `00379CE0` |
| CONTRACT-authored-trigger-points.md | the movement call that reads the height | `003A1920` |
| CONTRACT-field-environment-variant.md | the save-lifecycle function that stores `dil` | `00280140` (`00280213`) |
| field-record-bit15-action-permission.md | the boot routine | `0022A0B0` (`0022A3F7`) |
| CONTRACT-navigation-search-and-follow.md | the tails of the nineteen verbs | `003791D0`..`003795A0` |
| CONTRACT-the-five-parallel-slot-maps.md | the status function's call | `0031117A` (in `00310DB0`) |

Scripts (FABLE's work folder, not tracked): `Database/Tools/work/FABLE/rdy1002/postfix.py` and `postfix2.py`.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/03-World-Area-Field/CONTRACT-authored-trigger-points.md`
affected: `Database/FFXII TZA/03-World-Area-Field/CONTRACT-field-environment-variant.md`
affected: `Database/FFXII TZA/03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`
affected: `Database/FFXII TZA/04-Actor-Entity/CONTRACT-actor-storage-record-initialisation.md`
affected: `Database/FFXII TZA/04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md`
affected: `Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`
affected: `Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/why-the-enemies-you-killed-come-back.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-battle-locomotion-turn-limiter.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-navigation-search-and-follow.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-separation-pass.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/README.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md`
affected: `Database/FFXII TZA/06-Movement-And-Navigation/how-an-animation-moves-and-turns-a-character-toward-its-target.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Dispatch/battle-action-handler-table.md`
affected: `Database/FFXII TZA/07-Combat-Action/CONTRACT-battle-action-handler-table.md`
affected: `Database/FFXII TZA/07-Combat-Action/CONTRACT-combo-continuation.md`
affected: `Database/FFXII TZA/07-Combat-Action/CONTRACT-native-command-seam.md`
affected: `Database/FFXII TZA/07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md`
affected: `Database/FFXII TZA/07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`
affected: `Database/FFXII TZA/07-Combat-Action/README.md`
affected: `Database/FFXII TZA/07-Combat-Action/Result-Record/the-result-record-field-map.md`
affected: `Database/FFXII TZA/07-Combat-Action/how-an-action-gathers-its-targets.md`
affected: `Database/FFXII TZA/07-Combat-Action/how-close-a-unit-must-stand-to-act.md`
affected: `Database/FFXII TZA/07-Combat-Action/the-moment-an-action-is-committed.md`
affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/CONTRACT-enmity.md`
affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md`
affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`
affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md`
affected: `Database/FFXII TZA/11-Party/Battle-State-Block/CONTRACT-battle-state-block.md`
affected: `Database/FFXII TZA/11-Party/Battle-State-Block/the-battle-state-block-field-map.md`
affected: `Database/FFXII TZA/11-Party/CONTRACT-the-five-parallel-slot-maps.md`
affected: `Database/FFXII TZA/11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`
affected: `Database/FFXII TZA/11-Party/the-five-parallel-slot-maps.md`
affected: `Database/FFXII TZA/21-RNG-And-Determinism/rng-streams.md`
affected: `Database/FFXII TZA/21-RNG-And-Determinism/which-roll-is-on-which-generator.md`

- consumer: the 39 pages above: revised-here (OPUS's tagged strike edits; FABLE's citation-form adjustments).
- consumer: OPUS-led and shared pages of the same passes: agrees (OPUS applied its own share in each batch commit).
- consumer: SWE2-EC7 / STRUCT / FRONTIER pages named by the passes: routed-to- those lanes by OPUS's requests; not edited here.

run: [`rng_check.py`](../opus-rng-readiness-fixes-1002/rng_check.py) at 31f29775a (FAILS 0)
run: [`ai_check.py`](../opus-ai-readiness-fixes-1002/ai_check.py) at 31f29775a (FAILS 0)
run: [`spawn_check.py`](../opus-spawn-readiness-fixes-1002/spawn_check.py) at 31f29775a (FAILS 0)
run: [`action_check.py`](../opus-action-readiness-fixes-1002/action_check.py) at 31f29775a (FAILS 0)
run: [`movement_check.py`](../opus-movement-readiness-fixes-1002/movement_check.py) at 31f29775a (FAILS 0)
run: [`party_check.py`](../opus-party-readiness-fixes-1002/party_check.py) at 31f29775a (FAILS 0)
run: [`world_check.py`](../opus-world-readiness-fixes-1002/world_check.py) at 31f29775a (FAILS 0)
run: [`actor_check.py`](../opus-actor-readiness-fixes-1002/actor_check.py) at 31f29775a (FAILS 0)
