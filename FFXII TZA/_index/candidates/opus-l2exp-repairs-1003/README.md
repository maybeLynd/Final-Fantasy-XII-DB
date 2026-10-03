# OPUS's share of the L2 expansion repairs: the verdict table, the exclusion criterion, a struck-verdict parser (OPUS, 2026-10-03)

*On `AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003` from SWE2-AUDIT-SPEC's expansion
([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md)), parts (b) and (c); part (d) is in
[`opus-standing-checks-1003`](../opus-standing-checks-1003/README.md); part (a) is below.*

## (b) The verdict table (OPUS)

Applied by [`apply_l2_table.py`](apply_l2_table.py) (idempotent; without `--apply` it checks that all 39 edits, the summary
retirement and the amendment are present). Every change is a positional cell edit of the main table; old verdicts are
struck, never deleted.

| change | rows | source |
|---|---|---|
| contract: reason supplied, stays MET | S-03, S-04, S-06, S-10, S-12, S-14, S-15, S-23, S-33, S-37, S-39, S-46, S-50 | SPEC item 3 task A |
| contract: SCOPE-SHORT | S-01 (VBF mount `0017CEB0`, startup latch writer `0017D074`), S-16 (retirement `002350C0`, keep-bank rotation `00233780`), S-21 (SPEC's text) | SPEC item 3 task A |
| contract: SCOPE-SHORT | S-25 p2, S-29 p1, S-38 p2 | SWE2-AUDIT-SEM's wordings, SPEC concurred |
| contract: SCOPE-SHORT | S-08 (file layer) | OPUS's decision under (c) |
| contract: narrowed, explicit bounded exception | S-17, S-31, S-44 | SPEC item 3 task A |
| L2: MET → NOT MET | S-01, S-08, S-21, S-29, S-38 | follows the contract cell |
| L2: already NOT MET, contract gap recorded | S-16, S-25 | follows the contract cell |
| script/data: N/A → MET (linked) | S-02, S-18, S-19, S-20, S-23, S-38 | SPEC item 3 task B text |
| script/data: N/A → PARTIAL | S-21 (`battle_message.bin` decode not yet censused) | SPEC item 3 task B |
| script/data: N/A kept, reason stated | S-05; S-33 (+ resource link `0024A5A0`) | SPEC item 3 task B |
| summary: the hand-kept "contract column" count table retired | — | it drifted twice; read MET 47 / SCOPE-SHORT 3 against rows 52 / 0 (`checkpoint_consistency.py` C4) |

Two of SPEC's linking claims were re-read at the bytes before adoption: `003495A0` calls `00313120` at `003495B2` (S-20),
and `002E9890` reads word `+0x86` of the movement body (S-19).

**OPUS's two choices.** The "narrow the registry subject" alternatives AUDIT-SEM named for S-25/S-29/S-38 are not taken:
narrowing a system's subject to make it pass is the scoring change the directive forbids. S-08 is SCOPE-SHORT, not a
split row (a split moves the 52-system denominator).

**Effect, all three parsers agreeing** (`progress_report.parse_verdicts`, `goal_gate.py`, `checkpoint_consistency.py`
C3): **L2 31 MET / 21 NOT MET** (was 36 / 16); contract 45 MET / 7 SCOPE-SHORT; script/data 49 MET, 1 PARTIAL, 2 N/A.
`goal_gate.py`: NOT_MET, 21/52 systems NOT MET. A metric moving backwards after better evidence is the intended outcome.

## A parser read a corrected verdict as its old one (OPUS)

`progress_report._cell_verdict` matched `^[\s*~`(]*(MET|...)`: its leading `~` skip let the STRUCK word match, so a
cell written by the correction policy — `~~MET~~ **SCOPE-SHORT — ...**` — read **MET**. At HEAD no cell used that form
(lanes had replaced verdicts instead of striking them), so nothing was misread yet; the first strike-and-correct of a
verdict would have kept its old reading in PROGRESS, the dashboard and the checkpoint. Fixed: leading struck spans are
skipped. Test **T3s** (six cell shapes); the reporter suite is FAILS 0. Verdict-first wording is also used in every cell
written here, so `goal_gate.py`'s own reader (it requires `^MET`) agrees. Four tools parse this table independently
(`progress_report`, `goal_gate`, `readiness_view`, the dashboard's `requirements.py`); unifying them on one parser is routed
to SWE2-FRONTIER (`OPUS-REQ-FRONTIER-ONE-VERDICT-PARSER-1003`).

## (c) The exclusion criterion (OPUS)

Appended to `L2-VERDICTS.md` as "Amendment — an exclusion may not drop registry-subject material": an exclusion is
valid only when the registry subject does not name the excluded material; an excluding cell names each item and cites
the amendment. Mechanism: `checkpoint_consistency.py` **C9** lists every MET/LIVE runtime cell with exclusion wording
and no citation — cells scored before the amendment as a visible worklist (now 12: S-05, S-06, S-08, S-11, S-13, S-22,
S-23, S-26, S-36, S-37, S-40, S-42; routed to SWE2-DATA), any later one as a FAIL.

## (a) The type store — not applied yet (OPUS)

The ~25 declarations, five aliases and two propagations go into `_types/types.tsv` and `fields.tsv`, which hold another
lane's uncommitted edits (the AchievementState rows) with no board claim naming them. Writing under them would publish
or overwrite their work, so (a) waits; the request stays ACTIVE with this reason.

## Review (OPUS)

Non-author review of (b), (c) and the parser fix goes to SWE2-AUDIT-SPEC (the requester).
