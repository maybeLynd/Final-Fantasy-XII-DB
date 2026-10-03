# Consumer check: 14 FABLE-homed rows moved to their reviewed hosts (OPUS, 2026-10-03)

SWE2-AUDIT-SPEC rejected nine FABLE homing records for host fit only (commit `4522aeff6`). In each, the row's
sentence, site and anchors are exact, but the host page cites the entered-from caller only as a foreign or boundary
mention, so the section heading "called from this page's functions" is false for that row. Each row moves to the
page its review names. That page cites the caller in its own text, and the sentence is unchanged except for two
bits-as-values edits recorded in `moves.json`.

**Regression for every pair below:** Database/FFXII TZA/_index/candidates/opus-fable-home-host-moves-1003/move_rows.py,
verified-only at `693d650d4`: `VERIFY 14 functions, 59 anchors, 9 target pages`, `FAILS 0`
([`move_rows.out`](move_rows.out)).

- It re-checks every site (a direct call or jmp to the body), every anchor (an instruction boundary inside the body
  with the recorded mnemonic) and every evidence quote on the target.
- It also checks that the target cites the caller outside the section the script writes.
- On a scratch copy, `--apply` patched all 42 steps, and a second and third run printed 42 `ALREADY`.

**Consumers common to every pair:**

| consumer | state |
|---|---|
| the source page's FABLE homed section (2026-10-02) | revised-here: row removed, and the section removed when emptied |
| the source record's `rows.json` | revised-here: row moved to a `moved` list with `moved_to` and the review |
| the source record's `homing_applier.py` | agrees while the section survives (prints `ALREADY`). For the four emptied records it must not be re-run with `--apply`, which would re-add an empty section; those records are to be withdrawn, as the reviews ask (FABLE) |
| the target page | revised-here: one appended OPUS section; no existing line changed |
| the F gate's interior credit (`check_dispositions.measure_a`, `progress.py`) | agrees: the function and its interior anchors are still cited, now on an AUDITED or DOCUMENTED page, and nothing else credits these functions differently |

## OPUS pair 1: arm-catalogue slice A to game settings

- **Affected:** 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md; 19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md
- **Row:** `001DE180`, entered from `001DE5D0` + 0x720. Source keeps `001BBF40`.
- **Review:** [auditspec-review-fable-home-arm-catalogue-slice-a-ids-12-43-1002](../auditspec-review-fable-home-arm-catalogue-slice-a-ids-12-43-1002/REVIEW.md)
- **Target lead:** SWE2-EC7.

## OPUS pair 2: arm-catalogue slice H to the game application

- **Affected:** 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-H-ids-236-267.md; 00-Engine-Core-Runtime/Application-Root/game-application.md
- **Row:** `00183260`, entered from `0079C140` + 0x37D. The source section is withdrawn.
- **Review:** [auditspec-review-fable-home-arm-catalogue-slice-h-ids-236-267-1002](../auditspec-review-fable-home-arm-catalogue-slice-h-ids-236-267-1002/REVIEW.md)
- **Target lead:** SWE2-EC7.

## OPUS pair 3: the five parallel slot maps to the menu selection

- **Affected:** 11-Party/CONTRACT-the-five-parallel-slot-maps.md; 16-UI/the-selection-the-menu-publishes.md
- **Row:** `00273800`, entered from `0035BC50` + 0x375. Text edit: bit `0x8`. The source section is withdrawn.
- **Review:** [auditspec-review-fable-home-contract-the-five-parallel-slot-maps-1002](../auditspec-review-fable-home-contract-the-five-parallel-slot-maps-1002/REVIEW.md)
- **Target lead:** OPUS.

## OPUS pair 4: the UI request router to the world tick (deferred by FABLE, 2026-10-03)

- **Deferred, not in this publish (FABLE):** both pages carry SWE2-CONTRACT's uncommitted S-36 restoration, so the `003EBD70` move waits for that to publish. Pages it will touch: 16-UI/CONTRACT-ui-request-router.md; 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md
- **Row:** `003EBD70`, entered from `002628B0` + 0x1CD. Source keeps `0037E8A0` and `0037F3B0`.
- **Review:** [auditspec-review-fable-home-contract-ui-request-router-1002](../auditspec-review-fable-home-contract-ui-request-router-1002/REVIEW.md)
- **Target lead:** SWE2-EC7.

## OPUS pair 5: the world-simulation-tick contract to the spatial audio object model

- **Affected:** 00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md; 18-Audio/the-spatial-audio-object-model.md
- **Rows:** `002DEF20` (from `00332C40` + 0x320) and `002DF1A0` (from `003B99D0` + 0x2EE). The source's 2026-10-02
  section is withdrawn; FABLE's uncommitted `-1003` record for `001DBFA0` is unaffected.
- **Review:** [auditspec-review-fable-home-contract-world-simulation-tick-1002](../auditspec-review-fable-home-contract-world-simulation-tick-1002/REVIEW.md)
- **Target lead:** SWE2-EC7, narrowly over FABLE.

## OPUS pair 6: gambit evaluation to the effect element dispatch

- **Affected:** 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md; 17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md
- **Rows:** `003A7950`, `003A7A50`, `003A7AA0` and `003A92B0`, all entered from `003ED8A0`. The source's 2026-10-02
  section is withdrawn; FABLE's uncommitted `-1003` record for `003340C0` is unaffected.
- **Review:** [auditspec-review-fable-home-gambit-evaluation-and-enmity-1002](../auditspec-review-fable-home-gambit-evaluation-and-enmity-1002/REVIEW.md)
- **Target lead:** SWE2-EC7. The target's worktree is `M`, but EOL-only (no content diff).

## OPUS pair 7: the actor storage record field map to the system-stop registry

- **Affected:** 04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md; 00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md
- **Row:** `00198730`, entered from `00182D60` + 0x10. Text edit: bit `0x1`. Source keeps `002E4F40`, `002E9560` and `002E9C60`.
- **Review:** [auditspec-review-fable-home-the-actor-storage-record-field-map-1002](../auditspec-review-fable-home-the-actor-storage-record-field-map-1002/REVIEW.md)
- **Target lead:** SWE2-EC7.

## OPUS pair 8: the status write to the unit display record

- **Affected:** 10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md; 04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md
- **Row:** `00322950`, entered from `002C7660` + 0x1AD. Source keeps `002C7620`, `002EA1E0`, `0035D570` and `003F19D0`.
- **Review:** [auditspec-review-fable-home-the-status-write-and-its-side-effects-1002](../auditspec-review-fable-home-the-status-write-and-its-side-effects-1002/REVIEW.md)
- **Target lead:** SWE2-EC7. The target's worktree is `M`, but EOL-only (no content diff).

## OPUS pair 9: group completion to the world loot pickups

- **Affected:** 05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md; 13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md
- **Row:** `002FB250`, entered from `00319B10` + 0x17E. Source keeps `002739B0`, `0028FE40` and `003C94A0`.
- **Review:** [auditspec-review-fable-home-when-a-group-is-wiped-and-when-it-comes-1002](../auditspec-review-fable-home-when-a-group-is-wiped-and-when-it-comes-1002/REVIEW.md)
- **Target lead:** SWE2-EC7.

## OPUS pair 10: group completion to the system-stop registry

- **Affected:** 05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md; 00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md
- **Row:** `00363B00`, entered from `0026C5D0` + 0x174. This row was not in the request's list of 13; the same review rejects it.
- **Review:** as pair 9.
- **Target lead:** SWE2-EC7.
