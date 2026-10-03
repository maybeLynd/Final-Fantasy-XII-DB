# OPUS's readiness edits on SWE2-EC7's six held pages - applied once OPUS's file claims released (SWE2-EC7, 2026-10-03)

*SWE2-EC7, operated by a Claude stand-in (Opus 5.5) while the lane's Devin session was rate-limited. This is the follow-up to
[`readiness-apply-ec7-1003`](../readiness-apply-ec7-1003/README.md), which held these six pages while they sat under OPUS's
ACTIVE file claims (OPUS-CLOUD-F-LOCAL-W42-1002, -W43-1002 and OPUS-CLOUD-F-HOMING-H1-1002, all DONE since OPUS's
`787a4302c`). The same owner-filtered appliers (`apply_by_owner.py SWE2-EC7`) were run unchanged, giving 25 edits. None is
disputed. The commit carries HEAD plus EC7's edits only, so any peer hunks stay in the worktree.*

| request | pages here |
|---|---|
| `OPUS-REQ-EC7-PHYRE-READINESS-EDITS-1002` | class-descriptor-and-metadata-system (1), member-registration-and-the-recovered-field-schema (3), phyre-script-object-accessors (3) |
| `OPUS-REQ-EC7-UI-READINESS-EDITS-1002` | the-widget-message-protocol (14) |
| `OPUS-REQ-EC7-ENGINE-A-READINESS-EDITS-1002` | CONTRACT-battle-runtime-mode (1) |
| `OPUS-REQ-EC7-RESOURCE-A-READINESS-EDITS-1002`, `OPUS-REQ-EC7-RESOURCE-B-1002`, `OPUS-REQ-EC7-HELD-ROUTED-LINES-1002` (its resource-A line) | file-size-tables-fst (3) |

## Consumer check (SWE2-EC7)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md`
affected: `Database/FFXII TZA/16-UI/Widget-Object-Model/the-widget-message-protocol.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
affected: `Database/FFXII TZA/22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

- consumer: the six pages: revised-here (OPUS's tagged edits, unchanged).
- consumer: the other lanes' shares of the same batches: routed by OPUS (each batch's own record).

run: `phyre_check.py` at df40dbfcc (FAILS 0) - [script](../opus-phyre-readiness-fixes-1002/phyre_check.py)
run: `ui_check.py` at df40dbfcc (FAILS 0) - [script](../opus-ui-readiness-fixes-1002/ui_check.py)
run: `engine_a_check.py` at df40dbfcc (FAILS 0) - [script](../opus-engine-a-readiness-fixes-1002/engine_a_check.py)
run: `resource_a_check.py` at df40dbfcc (FAILS 0) - [script](../opus-resource-a-readiness-fixes-1002/resource_a_check.py)
run: `resource_b_check.py` at df40dbfcc (FAILS 0) - [script](../opus-resource-b-readiness-fixes-1002/resource_b_check.py)
