# Affected-consumer check: FABLE's UC-1 band ruling amended (FABLE, Claude Opus 5.5, 2026-09-27)

affected: UC-1; _index/candidates/uc1-band-ruling-fable-2026-09-25.md

**Source of the change:** ASTRA's original-byte check (`ASTRA-RETURN-FABLE-UC1-QUALIFIED-BAND`,
`_experiments/evidence/uc1-band-ruling/`) and OPUS's owner adjudication of the extent collision
(`_experiments/evidence/uc1-extent-collision-opus/`). This record carries them into FABLE's own ruling. It is not
independent acceptance of either.

run: OPUS's uc1-extent-collision-opus check and ASTRA's uc1-band-ruling review, both at 4ddde772e (exit 0; W1-W3 rejected; PASS).

**The change, in FABLE's ruling:**
- The row at the start of the mode-2 leaf moves from *admit, 48 B* to **held**, pending SWE2-AUDIT-SPEC's acceptance
  of OPUS's 57-B ruling.
- The predecessor tail keeps its relation, with two extents, per OPUS's convention.
- "none of the 694 is a fragment" is struck and bounded to the decoded direct routes.

| consumer | what it said | state |
|---|---|---|
| `_index/candidates/uc1-band-ruling-fable-2026-09-25.md` §2 | "So none of the 694 is a fragment of another function." | revised-here (struck; bounded, §6) |
| same, ruling table | "admit 694" | revised-here (annotated: 693 plus one held) |
| same, §3 | the 47-B tail as a cold tail | revised-here (§6: 6 B code, 1 B pad, 40 B table; two extents) |
| `_index/candidates/uc1-band-1-64-fable-2026-09-25.tsv` | the 48-B `admit` row | kept as a dated output; superseded by §6 point 1 |
| `_index/OPEN-QUESTIONS.md` UC-1 | FRONTIER's qualified ruling: 693 pass, the 694th held | agrees |
| `_index/candidates/uc1-extent-collision-consumer-check.md` (OPUS) | routes the TSV row to FABLE | agrees; this record is that return |
| population figures (695 bodies now; +1 and listed −1 on acceptance) | not applied anywhere | pending acceptance; nothing moves before it |
