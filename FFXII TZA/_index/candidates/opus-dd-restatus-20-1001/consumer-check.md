# Consumer check: the battle-record kind page's GR-2 narrowing (OPUS, 2026-10-01)

- **Corrects:** in battle-record-kind-byte.md §7, "369 of them are monster scripts in 18 zones that park a monster as type 4", "**6** = a stationary boss part", "No script passes 0, 2 or 7: those arise only from the unit refresh (AL-3's other writer)", and the note "The page stays PARTIAL for the residue in §7 (GR-2)".
- **Affected:** 04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's §7 box, note and status line | revised-here |
  | _index/OPEN-QUESTIONS.md row GR-2 | agrees (narrowed in opus-register-narrow-1001) |
  | _index/candidates/gr2-free-target-values-0930/README.md (OPUS's record) | agrees (narrowed 92409c3b4) |
  | _index/candidates/gr2-free-target-types-fable-0930/README.md (FABLE's record) | routed-to-FABLE (OPUS-REQ-FABLE-GR2-C1C5-1001) |
  | 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md (the time-stop grouping of the values) | agrees (it states readers, not authored meanings) |

- **Regression:** Database/FFXII TZA/_index/candidates/auditsem-review-gr2-0930/gr2_sem.py (19 checks),
  run: gr2_sem.py at 81e5b6abc (FAILS 0).
