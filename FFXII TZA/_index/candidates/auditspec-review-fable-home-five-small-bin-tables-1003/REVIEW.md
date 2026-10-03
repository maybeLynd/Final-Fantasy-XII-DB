# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-five-small-bin-tables-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-FIVE-SMALL-BIN-TABLES-1003` · Package: `_index/candidates/fable-home-five-small-bin-tables-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The sentence, site and anchors are exact. **The host is wrong.**

- The caller `0029E110` is the NG-signal widget procedure, the legend host that publishes itself at `0209C498`.
- This page names it only as one of "the menus" that call its legend copier (line 206), and in a neighbour list that ends "No menu behaviour is claimed here. The menus' own pages own it." (lines 543-548).
- The body builds two `0x148`-byte child widgets of the `0209C498` object. That is menu behaviour, and it belongs on `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`, which reads `0029E110` as the legend's host (lines 504-506).

The only row is mis-homed.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 587 and the row (line 593) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0.
- **`0029D4D0` (0x72 B).**
  - `00245000([0209C498] + 0x160, 0x148, 0029D550, 0)` at +0x21 and `00245000([0209C498] + 0x2A8, 0x148, 0029D550, 0)` at +0x43.
  - Then `00244960([0209C498], that + 0x160)` at +0x56, and a tail `jmp 00244960` at +0x6D with `+0x2A8`.
  - `0209C498` is re-read before each call.
  - Exact. "the address loaded by the `lea` at `0029D4DB`" is `0029D550`.
- **entered_from.** `0029E110` + 0x203 = `0029E313`, `call 0029D4D0`. It is the only caller (raw index).
- **Host fit: the defect.**
  - `0029E110` is the `NgSignal…` reader `P` on `16-UI/Battle-Hud/the-battle-hud-layout-readers.md` (line 93) and on `ui-layout-parameters-and-editor-schema.md` (line 210). The latter also says "the one reader is the legend's host ... publishes itself at `0209C498`" (lines 504-506).
  - This page's subject is the shipped bin tables and their readers. It touches `0209C498` only through the legend copy into `[0209C498]+0x158` (line 206).
  - It explicitly disclaims the menus' behaviour, so `0029E110` is not one of this page's functions.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the row from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home the row on `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`, which cites `0029E110` in its own text. `16-UI/Battle-Hud/the-battle-hud-layout-readers.md` is the alternative. Name the procedure in the sentence: replace "the address loaded by the `lea` at `0029D4DB`" with "the procedure `0029D550`".
