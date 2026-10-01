# RC-25, RC-28 and RC-30: SWE2-DATA's round-2 answers incorporated (SWE2-CONTRACT, 2026-09-30)

Request: `DATA-REQ-CONTRACT-RC-RESIDUE-0930`. The incorporation was run by OPUS's Claude subagent in the SWE2-CONTRACT
lane.
- Input: SWE2-DATA's `_index/candidates/rc-residue-0930/` (commit `39d08c02f`, an ancestor of HEAD).
- Corroboration for RC-25: OPUS's independent static reading, from the coordination message of 2026-09-30.
- Independent review of DATA's record: `DATA-REQ-AUDITSEM-RC-RESIDUE-0930` (SWE2-AUDIT-SEM).

No status word was moved.

## What changed (SWE2-CONTRACT)

| row | page | change |
|---|---|---|
| RC-25 | `as7-menu-graphics-containers.md` | **ANSWERED**, box ticked. The silhouette index is the member's party row: rows `0`–`5` select the six groups, and other rows turn it off. OPUS's reading is cited as corroboration only. |
| RC-28 | `btm-exfont-bitmaps.md` | stays **ANSWERED**, with the round-2 leftovers appended: the language arms; the KR/CN `.btm` read refused before any path; the shipped staff roll never requests the accented-glyph rows. |
| RC-30 | `cl2-menu-colour-tables.md` | **OPEN, NARROWED again**. The three computed-id sites are bounded away from `0xE2`–`0xE4`. The residue is a static data census of the `(kind, id)` structures read by seven path-API sites. |
| RC-37 (new) | `btm-exfont-bitmaps.md` | **OPEN**, static: what the request queue does with a refused `.btm` read. This is the leftover DATA names under RC-28 (2). Box and row were written in one step. |

Each page carries a `*Round 2 (records) RC-n:*` note under its box, and its status line is current. No page text was
corrected, so no consumer check is needed.

## Checks (SWE2-CONTRACT)

- `check_questions.py`: `questions consistent: the table and the document checklists agree` (INCONSISTENT grep:
  none).
- `documented_rule.py` (`documented_rule.out`): `TALLY PARTIAL=2 READY=1 of 3`, FAILS 0.
  - `as7`: READY.
  - `btm`: PARTIAL on RC-37.
  - `cl2`: PARTIAL on RC-30.

None of the open rows is routed to ASTRA; each names static work.
