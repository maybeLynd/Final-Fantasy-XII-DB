# Consumer check: 07-Combat-Action contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-07-VALUES-1002. Cloud wave 2 mapped `07-Combat-Action/` from a text snapshot (session
`session_018kFSP47XCyorcYBsfyonGU`; report `cloud-reports/re-readiness/07-action.md` in maybeLynd/Final-Fantasy-XII-DB,
899678f8; rated NOT YET, core MOSTLY). Its 17 value-changing contradictions and 9 count items were page-text only. A
local read-only pass decided them at the shipping image, and OPUS re-checked the deciding instructions
(`action_check.py`). The pages' dated corrections held on almost every item. The bytes add these facts:
- a band-two commit returns 1 without the attacker mask (`0030F8B6`);
- the combo record table is indexed by the stats byte `+4`, not by the kind (`003886A7`);
- the target buffer also lives on the stack, where `+0x01` has a reader (`00308813`);
- the 64-entry queue is drained eight entries at a time;
- the stand window scales with the frame-rate word (`00337B75`);
- the "posture" byte is a parked battle-stats slot index (`00311DA5`, `00385756`).

The draft holds 96 strike edits (`apply_07action.py`). OPUS applies the 20 on its own lines on three pages
(`apply_by_owner.py OPUS`). The rest go to their owners as requests:
- 68 to FABLE;
- 3 to SWE2-EC7;
- 1 to SWE2-CONTRACT;
- 4 to SWE2-FRONTIER, on `applying-a-result-to-a-target.md`. That page is OPUS-led by commits, but it is an overlay
  carrier, which only FRONTIER publishes.

- **Affected:** 07-Combat-Action/CONTRACT-battle-target-buffer.md, 07-Combat-Action/CONTRACT-commit-action.md, 07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the commit and target-buffer contracts and the combo page (OPUS lines) | revised-here |
  | the thirteen FABLE-led 07 pages | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 68 edits) |
  | `Post-Result-Events/the-post-result-events-and-the-battle-message-table.md` | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 3 edits) |
  | the target-buffer contract's outcome-word lines (630ef9be5) | routed-to-SWE2-CONTRACT (request with `apply_by_owner.py SWE2-CONTRACT`, 1 edit) |
  | `applying-a-result-to-a-target.md` (overlay carrier) | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 4 edits) |
  | RE repo `docs/readiness/07-action.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-action-readiness-fixes-1002/action_check.py, verified at 3c1948afc: 22 instructions decode as cited, FAILS 0 ([`action_check.out`](action_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (20), FAILS 0.
