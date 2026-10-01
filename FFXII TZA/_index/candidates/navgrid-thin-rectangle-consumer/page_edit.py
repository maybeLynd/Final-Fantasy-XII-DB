"""page_edit.py - FABLE's hunk for the unit-definition page (an overlay carrier: FRONTIER publishes it). Idempotent:
inserts the thin-rectangle qualifier after the grid-rebuild row's refinement clause, once. Run from the repository root.
"""
import sys
P = "Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md"
ANCHOR = "refines it to `max(w/trunc(w/c0), h/trunc(h/c0))` and stores `floorf` of that `+ 1.0` as `NavGridParams.cellSize`;"
ADD = (" *(qualified 2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-RETURN-FABLE-NAV-GRID-INITIAL-TRUNCATION: `trunc(w/c0)` "
       "(`003925A9`) or `trunc(h/c0)` (`003925CE`) is 0 when that side is shorter than `c0`, and the divide at `003925E9` / "
       "`003925FC` then gives +infinity under masked exceptions, so `maxss` and `floorf` receive +infinity. ASTRA's thin "
       "case, 1 × 400 with `c0` = 3F9A5FB2, gives nx 0, ny 331 and +infinity (the original prefix run under an emulator with a "
       "supplied `sqrtf` value; re-derived in `_index/candidates/navgrid-thin-rectangle-consumer/`). Positive extents alone "
       "therefore do not guarantee a finite cell size; whether any loaded map has such a shape is not shown.)*")
s = open(P, encoding="utf-8", newline="").read()
if ADD.strip() in s: print("already applied"); sys.exit(0)
if s.count(ANCHOR) != 1: sys.exit("REFUSE: anchor not found once")
s = s.replace(ANCHOR, ANCHOR + ADD)
open(P, "w", encoding="utf-8", newline="").write(s); print("applied")
