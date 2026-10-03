# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-font-painters-public-api-h7-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-FONT-PAINTERS-PUBLIC-API-H7-1` · Package: `_index/candidates/fable-home-the-font-painters-public-api-h7-1003/` · Page: `99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md` (published in `a7755a0b2`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 4 anchors / ALREADY / FAILS 0` (exit 0). 
- `rows.json`: 1 row(s), 4 anchors; mechanically rejected 0, missing 1.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00213090` (entered from `001E9380` + 0x19): **host fit holds** - the caller is a documented subject (L380, table-row first cell: "| `001E9380` | 51 B | `0017FC50` + 0x10 | calls the site `001E9380` + 0x19 on each of 0x40 ..."). Sentence exact: `mov byte [rcx+0x20], 1`, then dword 0x3F800000 to `+0x30`, `+0x2C`, `+0x28`, `+0x24` in that order; `ret`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
