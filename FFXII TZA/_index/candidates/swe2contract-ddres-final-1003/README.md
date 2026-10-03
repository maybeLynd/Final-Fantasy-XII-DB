# DD prose-residue closure: final receipt over the 87 KEEP-PARTIAL pages (SWE2-CONTRACT for OPUS, 2026-10-03)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929` (batches 1-21 published through `85718f321`/`097a3a739`).
Run at HEAD `c7e2bb2a1` by the Claude stand-in operating SWE2-CONTRACT while the lane's Devin session was rate-limited.

**Receipt.** `status-currency-ruling-fable/documented_rule.py` over every page of
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv) with `recommend = KEEP-PARTIAL`
([`pages.txt`](pages.txt), 87 pages): **TALLY PARTIAL=8 READY=59 READY-WITH-POINTER=20 of 87, FAILS 0**, self-test S PASS
(full output: [`documented_rule.out`](documented_rule.out)). No page is NEEDS-POINTER, UNKNOWN-ID or EVIDENCE-UNTRACKED.

**READY for OPUS's owner read: 79 pages** (every READY / READY-WITH-POINTER line of the output). READY is not DOCUMENTED:
the owner still confirms the template sections and tier citations (`dd-owner-read-0929/README.md`, "What closes DD").

**Still PARTIAL: 8 pages, each only on registered live rows** (runtime remainders under ASTRA routing; no unregistered prose
residue remains on any of them, so this request has nothing left to close on them):

| page | live rows | open boxes |
|---|---|---|
| `01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md` | OV-10 | 0 |
| `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` | OV-42 | 0 |
| `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` | OV-19 , OV-33 | 0 |
| `13-Rewards-Progression-Economy/experience-and-license-point-award.md` | GR-18 | 1 |
| `13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md` | GR-18 | 0 |
| `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md` | SD-194 | 0 |
| `17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md` | OV-42 | 0 |
| `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` | GR-18 | 0 |

Three of the eight carry uncommitted peer edits in the working tree at this run (the script-binds page, the resource
request queue, the memory page); the receipt reads the working-tree bytes, as `documented_rule.py` always does. Checked against HEAD for those three:
the live id each is PARTIAL on (OV-10, OV-19, GR-18) is named the same number of times at HEAD as in the worktree, and
none has an open box at HEAD, so the verdicts do not depend on the peer edits.
