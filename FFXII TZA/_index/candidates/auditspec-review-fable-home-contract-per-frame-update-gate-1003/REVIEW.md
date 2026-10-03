# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-per-frame-update-gate-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-PER-FRAME-UPDATE-GATE-10` · Package: `_index/candidates/fable-home-contract-per-frame-update-gate-1003/` · Page: `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 3 functions, 15 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 3 row(s), 15 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 0 fit, 3 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `001BC010` (entered from `0017F040` + 0x21): **host-fit defect** - `0017F040` appears 1 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `0017F040` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `003F65C0` (entered from `003F62D0` + 0x1A): **host-fit defect** - `003F62D0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `003F62D0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `003F6A10` (entered from `003F62D0` + 0x88): **host-fit defect** - `003F62D0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `003F62D0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
