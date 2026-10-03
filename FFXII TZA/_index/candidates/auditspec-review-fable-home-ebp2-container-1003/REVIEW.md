# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ebp2-container-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-EBP2-CONTAINER-1003` · Package: `_index/candidates/fable-home-ebp2-container-1003/` · Page: `25-EBP-Script-Container/Container/ebp2-container.md` (published in `a7755a0b2`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). 
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 2.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00474070` (entered from `003545B0` + 0x94): **host fit holds** - the caller is a documented subject (L764, table-row first cell: "| `003545B0` | 184 B | calls `002640C0` with the incoming registers (result p), then reads ..."). Sentence exact: the fifth and sixth arguments at `[rsp+0x80]`/`[rsp+0x88]` after the 0x58 frame; the sixth to `02CA6C78` (`004740BF`); `00244F50` (+0x63) with `ecx` 0x1D8, `rdx` = `00474100` (`lea` at `004740A4`) and `r8` -> {dword 0, rcx, pointer to {edx, r8d, r9d, fifth}}; the result to `02CA6C80`, `02CA6C78` zeroed; cookie `01F44830`, checked by `00808C40` at +0x82.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
