# OPUS's readiness edits on FABLE's pages - 20-Platform and 24-CRT - applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Same procedure as [`readiness-apply-fable-1002`](../readiness-apply-fable-1002/README.md):
each batch applied unchanged with its own `apply_by_owner.py FABLE --apply` (Platform 3 edits, CRT 6); none is disputed.
Pre-checked in a throwaway worktree: no A-drift change; the neighbour gate refused one new citation of the game's exit
routine on the hardening page, so it is named by role.*

| page | role on the page | address |
|---|---|---|
| image-hardening-cfg-aslr-dep-and-stack-cookies.md | a site in the game's exit routine (calls `ExitProcess`) | `007980A0` + 0x7DF |

Requests: `OPUS-REQ-FABLE-PLATFORM-READINESS-EDITS-1002` ([OPUS record](../opus-platform-readiness-fixes-1002/consumer-check.md)), `OPUS-REQ-FABLE-CRT-READINESS-LINES-1002` ([OPUS record](../opus-crt-readiness-fixes-1002/consumer-check.md)).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`

- consumer: the pages above: revised-here (OPUS's tagged strike edits; one citation named by role).
- consumer: OPUS-led pages of the same passes: agrees (OPUS applied its own share).

run: [`platform_check.py`](../opus-platform-readiness-fixes-1002/platform_check.py) at 6c24cfab8 (FAILS 0)
run: [`crt_check.py`](../opus-crt-readiness-fixes-1002/crt_check.py) at 6c24cfab8 (FAILS 0)
