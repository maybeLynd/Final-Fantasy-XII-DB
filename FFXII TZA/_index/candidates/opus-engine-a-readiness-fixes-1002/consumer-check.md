# Consumer check: 00-Engine contradictions (part A) from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-00-VALUES-1002, part A. Cloud wave 5 mapped `00-Engine-Core-Runtime/` from a text
snapshot (session `session_01CZqFVU5oUoW88c6NELytjK`; report `cloud-reports/re-readiness/00-engine.md` in
maybeLynd/Final-Fantasy-XII-DB; rated NOT YET). Its value items were page-text only. A local read-only pass took
C-V1 to C-V82 (report lines 1835-2350). It decided 81 of them at the shipping image and left one, C-V4, because it
needs a census re-run. OPUS re-checked a sample of the deciding instructions (`engine_a_check.py`).

Corrected at the bytes:
- the boot store of `01FD4A90`;
- the console tables' lea and call counts (49 and 28, against "46" and "thirty");
- the ladder's bit-0 clear;
- the battle-runtime mode ladder's 22 call sites;
- the class-16 arm site;
- the size of `00306760` (911 B plus a switch table).

Part B (from report line 2350) follows separately.

The pass drafted 99 strike edits (`apply_00engine_a.py`). OPUS applies the 48 on its own lines across 14 pages
(`apply_by_owner.py OPUS`). The rest go to their owners as requests:
- 34 to SWE2-EC7;
- 15 to FRONTIER and SWE2-FRONTIER, including the overlay carrier `the-encoded-id-space-and-the-query-record.md`;
- 2 to SWE2-CONTRACT.

- **Affected:** 00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md, 00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md, 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md, 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md, 00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md, 00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md, 00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md, 00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md, 00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md, 00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md, 00-Engine-Core-Runtime/the-basis-column-helpers.md, 00-Engine-Core-Runtime/the-encoded-id-class-registry.md, 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the fourteen OPUS-led and shared 00 pages (OPUS lines) | revised-here |
  | the tick, game-application and accessor-hub pages and EC7's lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 34 edits) |
  | the encoded-id-space carrier and FRONTIER's mode-ladder lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER` and `FRONTIER`, 15 edits) |
  | the event-slot page and SWE2-CONTRACT's registry line | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 2 edits) |
  | C-V4 (the console arms' step constants) and the part-B items | routed-to-OPUS (later) |
  | RE repo `docs/readiness/00-engine.md` | routed-to-OPUS (filed after part B, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-engine-a-readiness-fixes-1002/engine_a_check.py, verified at 7007648d0: 4 instructions decode as cited, FAILS 0 ([`engine_a_check.out`](engine_a_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (48), FAILS 0.
