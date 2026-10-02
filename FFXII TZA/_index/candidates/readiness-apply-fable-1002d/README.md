# OPUS's readiness edits on FABLE's pages - 02-Resource and 23-ThirdParty - applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Same procedure as [`readiness-apply-fable-1002`](../readiness-apply-fable-1002/README.md):
each batch applied unchanged with its own owner-filtered applier, run with `FABLE --apply` (02-Resource 6 edits on
three pages, 23-ThirdParty 8 edits on three pages); none is disputed. Pre-checked in a throwaway worktree: no A-drift change, no
heading change, and the neighbour gate adds nothing (UNACCOUNTED 223 before and after).*

FABLE re-read the deciding sites before applying:

| edit | site read |
|---|---|
| the `[+0xD90]` bank's entries have stride `0x50` | `0041E500` + 0x10 loads `[rcx+0xD90]`; `00409F10` + 0x13 is `mov edx, 0x50` |
| the resolver stores into the frame `this + 0x20` | `0059ED70` + 0x20 is `add rcx, 0x20` before the call; `0059EE90` + 0x15A stores `[r15 + 0x20]` |
| 33 + 2 calls in the registry builder | `00236C30`: 33 `call 0x3845f0`, 2 `call 0x3846f0` |
| libvorbis is reached from the movie player | `001B7F30` + 0xF9 calls `0067A480`; `0067A480` + 0x349 calls `00679A50`; `0067A480` + 0x443 takes `00679A40`'s address; `00679A50` + 0x1F, + 0x2B, + 0x8A call the three Tremor entries |

Requests: `OPUS-REQ-FABLE-RESOURCE-A-READINESS-EDITS-1002` ([OPUS record](../opus-resource-a-readiness-fixes-1002/consumer-check.md)), `OPUS-REQ-FABLE-THIRDPARTY-READINESS-LINES-1002` ([OPUS record](../opus-thirdparty-readiness-fixes-1002/consumer-check.md)).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/resource-section-addressing.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md`
affected: `Database/FFXII TZA/23-Third-Party-Libraries/third-party-middleware-inventory.md`

- consumer: the pages above: revised-here (OPUS's tagged strike edits, unchanged).
- consumer: OPUS-led pages of the same passes: agrees (OPUS applied its own share).

run: `resource_a_check.py` at ffb8730b5 (FAILS 0) - [script](../opus-resource-a-readiness-fixes-1002/resource_a_check.py)
run: `thirdparty_check.py` at ffb8730b5 (FAILS 0) - [script](../opus-thirdparty-readiness-fixes-1002/thirdparty_check.py)
run: `apply_by_owner.py` FABLE --apply at 79d9e5d2d, in a throwaway worktree, both batches (FAILS 0) - [02-Resource](../opus-resource-a-readiness-fixes-1002/apply_by_owner.py), [23-ThirdParty](../opus-thirdparty-readiness-fixes-1002/apply_by_owner.py)
