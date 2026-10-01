# Consumer check: SD-165 repaired on SWE2-AUDIT-SPEC's REJECT (OPUS, 2026-10-01)

- **Corrects:** in this README, the four-entry list, "0036BFE0 is reached only through these", the 206-site table and its headline figures (50 TESTED, 17 unchecked DEREF, 134 handed on), and the modding line's "17"; in the register, SD-165's ANSWERED cell with those figures.
- **Affected:** _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | this record and the register row SD-165 | revised-here (repaired census: 253 sites, 98 TESTED, 32 DEREF, 121 handed on) |
  | 24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md (sections 1-2, the SD-165 note and box) | routed-to-OPUS (the page holds another identity's uncommitted edit; the figures are updated once that edit is committed) |
  | _index/candidates/sd-incorporation-fable-0930/README.md (FABLE's incorporation of the first answer) | routed-to-FABLE |

- **Regression:** Database/FFXII TZA/_index/candidates/sd165-alloc-null-tests-0930/sd165_nulltests_v2.py (E1, C1 and one
  control per defect dK dL dJ dS dN), run: sd165_nulltests_v2.py at bdfa87dbe (FAILS 0).
