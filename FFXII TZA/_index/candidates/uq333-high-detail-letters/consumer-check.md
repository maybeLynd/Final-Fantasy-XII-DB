# Affected-consumer check: UQ-333 — `C`, `N`, `S` are the high-detail model tables (FABLE, Claude Opus 5.5, 2026-09-26)

affected: UQ-333; 25-EBP-Script-Container/Sections/section-012.md (the UQ-333 box)

**Regression:** `uq333_letters.py` beside this file (5 checks, FAILS 0).

run: uq333_letters.py at b63aae1d4 (FAILS 0), 2026-09-26.

**The correction.** The UQ-333 box said "no `obj_finish` category matches them". The engine's own model-id decoder
sends `C`, `N` and `S` to resource-path kinds 15, 20 and 24. Their installed path arrays are the
`obj_finish\in\high` models `hc*.cm`, `hn*.cm` and `hs*.cm` (48, 87 and 5 entries), and every section-012 id of those
letters falls inside its table.

| consumer | what it says | state |
|---|---|---|
| `25-EBP-Script-Container/Sections/section-012.md` UQ-333 box | "no `obj_finish` category matches them" | revised-here (struck; answer with limits) |
| `_index/OPEN-QUESTIONS.md` UQ-333 | the same phrase in the question cell; status OPEN | revised-here (status restated ANSWERED; the question cell is left as asked) |
| `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md` kind table (15, 20, 24 = `obj_finish/high/*`) | high-detail variants | agrees |

**Limits.**
- The section's reader is unlocated.
- The lowercase ids do not follow the decoder's block order, so the reader translates them somehow.
- The uppercase direct-index reading rests on an exact range fit, not on a traced read.
