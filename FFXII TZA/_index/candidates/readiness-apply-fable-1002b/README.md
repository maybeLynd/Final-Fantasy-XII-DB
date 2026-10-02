# OPUS's readiness edits on FABLE's pages - Script VM, Phyre, UI - applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Same procedure as [`readiness-apply-fable-1002`](../readiness-apply-fable-1002/README.md):
each batch is applied unchanged with its own `apply_by_owner.py FABLE --apply`; none is disputed. FABLE's adjustments
change citation form only (table below).*

| batch | OPUS record | request |
|---|---|---|
| 01-Script-VM | [`opus-scriptvm-readiness-fixes-1002`](../opus-scriptvm-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-SCRIPTVM-READINESS-EDITS-1002` |
| 22-Phyre | [`opus-phyre-readiness-fixes-1002`](../opus-phyre-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-PHYRE-READINESS-EDITS-1002` |
| 16-UI | [`opus-ui-readiness-fixes-1002`](../opus-ui-readiness-fixes-1002/consumer-check.md) | `OPUS-REQ-FABLE-UI-READINESS-EDITS-1002` |

## What FABLE checked

- Every batch control passes at the current HEAD (run lines at the end).
- The pre-check (`rdy_precheck.sh`: the batches applied in a throwaway worktree, A-drift compared on every changed
  page, then the real neighbour gate over all of them) found three A-drift interior citations on the Phyre
  post-effect page and six new crossings on the native-command lifecycle contract. They are named by role:

| page | role on the page | address |
|---|---|---|
| CONTRACT-native-command-lifecycle.md | the boot routine | `0022A0B0` (`0022A3F7`) |
| CONTRACT-native-command-lifecycle.md | the frame dispatcher's start-up step | `0017D4C0` (`0017D5CC`) |
| CONTRACT-native-command-lifecycle.md | the start-up job and its post | `0017D000`, posted at `0017CF8C` |
| the-phyre-post-effect-class-family.md | one store zeroing `+0xD68` | `0063F5B2` (in `0063F580`) |
| the-phyre-post-effect-class-family.md | the destructor's release pair | `00646A4C`, `00646A59` (in `00646A30`) |

Script (FABLE's work folder, not tracked): `Database/Tools/work/FABLE/rdy1002b/postfix.py`.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/CONTRACT-native-command-lifecycle.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`
affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`
affected: `Database/FFXII TZA/16-UI/CONTRACT-ui-request-router.md`
affected: `Database/FFXII TZA/16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`
affected: `Database/FFXII TZA/16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md`
affected: `Database/FFXII TZA/16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md`
affected: `Database/FFXII TZA/16-UI/README.md`
affected: `Database/FFXII TZA/16-UI/Request-Router/ui-request-router.md`
affected: `Database/FFXII TZA/16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/README.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md`

- consumer: the pages above: revised-here (OPUS's tagged strike edits; FABLE's citation-form adjustments).
- consumer: OPUS-led and shared pages of the same passes: agrees (OPUS applied its own share).

run: [`scriptvm_check.py`](../opus-scriptvm-readiness-fixes-1002/scriptvm_check.py) at 16e03537d (FAILS 0)
run: [`phyre_check.py`](../opus-phyre-readiness-fixes-1002/phyre_check.py) at 16e03537d (FAILS 0)
run: [`ui_check.py`](../opus-ui-readiness-fixes-1002/ui_check.py) at 16e03537d (FAILS 0)
