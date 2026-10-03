# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-script-to-native-calling-convention-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-SCRIPT-TO-NATIVE-CALLING-CONV` · Package: `_index/candidates/fable-home-the-script-to-native-calling-convention-1003/` · Page: `01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `003BB320` (entered from `00393EA0` + 0xBA): **host fit holds** - the caller is a documented subject (L797, heading: "## SWE2-EC7-41 update (2026-09-19) - `00393EA0` ..."). Sentence exact: byte copy loop including the terminator to `02B4055C`; dword 9 `02B40E1C`, 0 to `02B40FE4`/`02B40554`/`02B40EC0`, 1 to `02B40E10`, qword 1 to `02B40E14`; `eax` = 0.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
