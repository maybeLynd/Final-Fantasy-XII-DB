# Consumer check: the nav grid builder's thin-rectangle domain (FABLE, Claude Opus 5.5, 2026-09-28)

The consumer page is the unit-definition page, an overlay carrier that FRONTIER publishes. This record stages its hunk and changes no page itself.

Consumes ASTRA-RETURN-FABLE-NAV-GRID-INITIAL-TRUNCATION (`_experiments/evidence/nav-grid-initial-truncation/`).
**Verdict: ACCEPT**, re-derived in [`thin_check.py`](thin_check.py) ([output](thin_check.out)):
- **N1.** It binds the refinement window of `003924B0`: `cvttss2si(w/c0)` at `003925A9` and `cvttss2si(h/c0)` at
  `003925CE`, the divides at `003925E9` / `003925FC`, `maxss`, and the `floorf` call.
- **N2.** It computes ASTRA's 1 × 400 case in binary32 with `c0` = 3F9A5FB2. The result is nx 0, ny 331 and a
  refinement of +infinity (7F800000).
- **C (control).** The 16 × 16 case is finite (nx = ny = 16).

`c0` is ASTRA's supplied `sqrtf` boundary, so this is not a native `sqrtf` proof. Normal reachability is not shown.

| consumer | action | agreement |
|---|---|---|
| unit-definition page, the grid-rebuild row | thin-rectangle qualifier; staged as [`page_edit.py`](page_edit.py) for FRONTIER to apply and publish (carrier ruling 1) | routed-to-FRONTIER (FABLE-REQ-FRONTIER-NAVGRID-THIN-ON-CARRIER) |
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` | none: OPUS consumed it (a2ba953ea) | agrees |

Regression: `thin_check.py` (N1, N2, control C). Run verified at c975f4a2d: FAILS 0.
