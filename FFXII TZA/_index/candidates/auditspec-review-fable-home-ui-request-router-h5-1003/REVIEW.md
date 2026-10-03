# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ui-request-router-h5-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-UI-REQUEST-ROUTER-H5-1003` · Package: `_index/candidates/fable-home-ui-request-router-h5-1003/` · Page: `16-UI/Request-Router/ui-request-router.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 13.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `002899A0` (entered from `002D5060` + 0x2A): **host fit holds** - the caller is a documented subject (L1000, table-row first cell: "| `002D5060` | 67 B | `00290740` + 0x1A | calls `002D5060` + 0x2A with dword `01E0C1D8` (0 ..."). Sentence exact: record dword 0 / `movsxd ecx` / `movsxd edx` at `+0`/`+8`/`+0x10`; `002899E1 call 00244F50(0xd0, 0028B860, &record)`; `and 0xfffffffd` / `or (r8d&1)*2` on `+0xC4`; cookie `01F44830` / `00808C40`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
