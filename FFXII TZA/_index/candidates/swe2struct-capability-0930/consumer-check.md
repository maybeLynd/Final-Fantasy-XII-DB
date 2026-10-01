# Consumer check: corrections on the capability policy page (SWE2-STRUCT for OPUS, 2026-10-01)

The falsification pass and the null-leader narrowing on the REOPENED capability page (this folder's README) struck and
re-stated five statements on that page.

- **Corrects:** in capability-inhibition-policy.md, §2's "when clear and no BattleUnit is selected, the tail reconciles a separate bit-5 gate via 002E1C40"; §7 C-7's "every row-2 bit but 1, 5 and 10" and "bit 5 goes through 002E1C40 ... indistinguishable from 0, 2, 3, 6 and 8"; the UQ-147 box's "Whether it reaches a KO counterpart during a summon is not queued"; §12's "Condition (2) is satisfied in the structural sense" and "so condition (2) holds at the loop level too, and only condition (1) remains"; the 2026-09-18 evidence-only read's 002E1CD0 polarity ("|= 0x139203 when ecx != 0, &= ~0x139203 when ecx == 0").
- **Affected:** 15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's own sections (§2, §7, §11 boxes, §12, the evidence-only read) | revised-here |
  | 03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md (002E1CD0: ecx != 0 clears, ecx == 0 sets) | agrees |
  | 11-Party/party-roster-and-control-suppression.md (0023B040 gate, the leader lookup) | agrees (it makes no claim on condition (2) or on 002E1C40) |
  | _index/OPEN-QUESTIONS.md row C-7 ("one condition for all but 1 / 5 / 10") | routed-to-OPUS (register owner; replacement: "all but 1 / 10; bit 5 is in the selection set, 002E1C40 writes 0215F1AC / 0215F1B4") |
  | _index/OPEN-QUESTIONS.md row UQ-147 ("whether it reaches a KO counterpart during a summon is not queued") | routed-to-OPUS (register owner; the request FABLE-REQ-ASTRA-UQ147-KO-SUMMONER-DURING-A-SUMMON is READY) |
  | 00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md (002E1C40 "the pair-write the policy page's inhibit bits correspond to") | routed-to-OPUS (the mechanism it states agrees; the gloss ties 002E1C40 to the policy table, which F5 refutes) |
  | _index/candidates/fable-astra-live-facts-0930/README.md row LEADER-STATS-NULL, and the board request FABLE-REQ-ASTRA-LEADER-STATS-NULL ("down to a single path-satisfiability question") | routed-to-FABLE (condition (2) fails at 003272CB; a hit would now show a writer outside the typed census) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2struct-capability-0930/cap_policy.py (23 checks: P1-P2 controls,
  F1-F8, L1-L11, M1), run: cap_policy.py at 48557d9d2 (FAILS 0).
