# FA-5's register cell: 32-entry status arrays, not 33 (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Found by check_questions' premise-drift report (retracted class): register row
FA-5 still said "both 33-entry status arrays", which FABLE corrected on the owning page on 2026-09-29.*

The result-record initialiser `003848E0` fills the two status arrays in one loop. Its counter is `r8 + 0x21` with `r8` set
to -1 just before, so the loop runs 32 times: 32 dwords from `+0x5C` and 32 words from `+0xDC`
([`fa5_check.py`](fa5_check.py), [out](fa5_check.out), FAILS 0, with the memset size as control).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: register row FA-5: revised-here (struck and restated in the question cell; ANSWERED unchanged).
- consumer: [the result-record field map](../../../07-Combat-Action/Result-Record/the-result-record-field-map.md): agrees (corrected to 32 on 2026-09-29).

run: fa5_check.py at d7350f841 (FAILS 0)
