# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-widget-object-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-WIDGET-OBJECT-1003` · Package: `_index/candidates/fable-home-contract-widget-object-1003/` · Page: `16-UI/Widget-Object-Model/CONTRACT-widget-object.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 1, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 0 fit, 1 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00299890` (entered from `0029A0A0` + 0x3B1): **host-fit defect** - `0029A0A0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence exact (but see host fit): `test al, 0x10` / `je`; `add word [rcx+0x110], 0x10`; signed `jl` against 0x100; zero `+0x110`, `and ax, 0xffef` stored to `+0xD8`. **Repair:** move the row unchanged to `16-UI/Widget-Object-Model/the-widget-message-protocol.md (`0029A0A0` is a list-item lead there, L1424: "`0029A0A0` sends `{30, value, text state}` to a delegate at `+0x120` ..."; the same page already homes `00297E10`/`00297F60` from that caller)`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
