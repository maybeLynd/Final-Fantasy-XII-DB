# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-save-payload-field-map-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SAVE-PAYLOAD-FIELD-MAP-1003` · Package: `_index/candidates/fable-home-the-save-payload-field-map-1003/` · Page: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 2 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 2 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 0 fit, 1 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `001B00E0` (entered from `00180E50` + 0x10): **host-fit defect** - `00180E50` appears 1 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `00180E50` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
