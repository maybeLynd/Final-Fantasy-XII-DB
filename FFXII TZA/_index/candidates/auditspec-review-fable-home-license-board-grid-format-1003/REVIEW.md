# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-license-board-grid-format-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-LICENSE-BOARD-GRID-FORMAT-1003` · Package: `_index/candidates/fable-home-license-board-grid-format-1003/` · Page: `12-Items-Equipment-Shops-License/license-board-grid-format.md` (published in `005d10e7c`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). 
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00282F10` (entered from `003FCAD0` + 0xCD): **host fit holds** - the caller is a documented subject (L460, table-row first cell: "| `003FCAD0` | 495 B | for k from `r8d` to `r9d` (signed) takes `E` = qword `[rcx+0x10]`[k ..."). Sentence exact: the three range maps (`ecx-0x1000` <= 0x1A4; `ecx-0x4000` <= 0x18 giving `ecx-0x3E5C`; `ecx-0x3000` <= 0x51 giving `ecx-0x2E44`; else 0), all unsigned (`ja`); `test byte [i + [0209AC30] + 0xB2E], 1 << byte [rdx+0x60]`; `setne al`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
