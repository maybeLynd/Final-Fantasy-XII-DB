# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-what-the-engine-calls-to-make-a-sound-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-WHAT-THE-ENGINE-CALLS-TO-MAKE-A-S` · Package: `_index/candidates/fable-home-what-the-engine-calls-to-make-a-sound-1003/` · Page: `18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `003DEFC0` (entered from `003DEC90` + 0x160): **host fit holds** - the caller is a documented subject (L699, heading: "## SWE2-EC7-40 update (2026-09-19) - `003DEC90` ..."). Sentence exact: `003697F0` on non-null `+8` and `+0x18`, each zeroed after; byte 0 at `+0x10`; `shl eax, cl` / `not` / `and` on `02B59C20` + `movsxd edx`*4.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
