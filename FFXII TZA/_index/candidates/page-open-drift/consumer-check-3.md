# Affected-consumer check, third pass — B-2/a on the memory page (FABLE, Claude Opus 5.5, 2026-09-26)

The second pass (`consumer-check-2.md`) noted two lines outside its batch. `where-the-games-memory-comes-from.md` calls
`B-2/a` an open question in two places:
- §4 says the reasoning "sharpens open question B-2/a rather than closing it";
- the related-documents list reads "open question **B-2/a**, which §4 of this document partially answers".

The register closed B-2/a on 2026-09-07, "ANSWERED IN THE NEGATIVE": the population folded onto the stub is everything
whose body is `ret 0`, and `/OPT:ICF` destroyed the distinction. That is exactly the reasoning §4 gives, so the page
agrees in substance and only its status words are stale.

| consumer | state |
|---|---|
| `24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md` §4 and the related list | revised-here (the stale words struck, closure noted) |
| `_index/OPEN-QUESTIONS.md` B-2/a | agrees (CLOSED 2026-09-07) |
| `24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md` | not re-read in this pass; the scan did not flag it |

**Regression:** `page_open_drift.py` no longer lists the two lines.
