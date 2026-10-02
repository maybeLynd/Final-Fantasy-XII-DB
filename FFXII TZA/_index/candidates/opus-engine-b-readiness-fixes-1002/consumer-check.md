# Consumer check: 00-Engine contradictions (part B) from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-00-VALUES-1002, part B. Part A (C-V1..C-V82) published in 76c2055a3. A local read-only
pass took the rest of the cloud map's §3.1 value items (C-V83 on), its §3.1.C counts and its §3.2 stale and banner
items. It decided the value items at the shipping image, including a vtable census built from the image's RTTI
locators. About twenty items that need an instrument re-run or tool history are left. OPUS re-checked a sample
(`engine_b_check.py`).

Corrected at the bytes:
- the third vf00 writer (`0036DD80+0x7`);
- the CLIP word (`0025A8E0+0xE`);
- the console thunk `008AB7C0`, a `lea` then `jmp`;
- the one store to `01F82D20`;
- the save window's real contents;
- table sizes and site counts.

The pass drafted 141 strike edits (`apply_00engine_b.py`). OPUS applies 99 of them across 29 pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 2 on `derived-call-signatures.md` are held until that page's OPUS F-interior section publishes
  (`apply_by_owner.py OPUS-HELD`).
- 18 go to SWE2-EC7.
- 12 go to FABLE.
- 7 go to SWE2-CONTRACT.
- 3 go to FRONTIER.

- **Affected:** 00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md, 00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md, 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md, 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md, 00-Engine-Core-Runtime/CONTRACT-transform-primitives.md, 00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/ARM-CATALOGUE-WORK-DIVISION.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-B-ids-44-75.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-C-ids-76-107.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-D-ids-108-139.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-E-ids-140-171.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-F-ids-172-203.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-G-ids-204-235.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/the-282-command-parameter-console.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/the-second-console-table.md, 00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md, 00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md, 00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md, 00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md, 00-Engine-Core-Runtime/Per-Frame-Update-Gate/one-word-decides-which-fifteen-subsystems-tick.md, 00-Engine-Core-Runtime/README.md, 00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md, 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md, 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md, 00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md, 00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 29 OPUS-led and shared 00 pages (OPUS lines) | revised-here |
  | `ABI-Recovery/derived-call-signatures.md` | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 2 edits) |
  | EC7's primitives, hubs, ownership and world-tick pages and its line | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 18 edits) |
  | the workbench contract and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 12 edits) |
  | the event-slot page and SWE2-CONTRACT's lines | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 7 edits) |
  | FRONTIER's lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 3 edits) |
  | the opcode TSV rows | routed-to-SWE2-DATA (regenerate) |
  | RE repo `docs/readiness/00-engine.md` | routed-to-OPUS (filed from this commit, with the part A and part B byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-engine-b-readiness-fixes-1002/engine_b_check.py, verified at 76c2055a3: 5 instructions decode as cited, FAILS 0 ([`engine_b_check.out`](engine_b_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (99), FAILS 0.

**Pass-22 neighbours (2026-10-02, OPUS).** `check_publish_neighbours.py` refused the first form of these edits. Some corrections cited another layer's function by address, and that adds an unaccounted crossing. Those functions are now named by role or by their ledger name on the page, with the offset kept. The applier's `ROLE_NAMES` pass makes the same change to its NEW text, so re-runs stay idempotent. The full deciding addresses remain in the applier's comments and in this record. `Tools/work/OPUS/nb_page.py` shows no new hit.
