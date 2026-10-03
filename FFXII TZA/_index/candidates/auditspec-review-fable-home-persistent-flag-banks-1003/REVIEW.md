# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-persistent-flag-banks-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-PERSISTENT-FLAG-BANKS-1003` · Package: `_index/candidates/fable-home-persistent-flag-banks-1003/` · Page: `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 2 row(s), 10 anchors; mechanically rejected 1, missing 3.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 2 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `003EB200` (entered from `003EC5B0` + 0x2D): **host fit holds** - the caller is a documented subject (L1459, table-row first cell: "| `003EC5B0` | 56 B | `002FB560` + 0x33 | calls `003EC5B0` + 0x8 with the incoming `ecx` a ..."). Sentence exact: `003EB21D call 002EAE20(edx, 0)`; null -> 0; `003EB23A call 003EB190(ecx, ptr, r8d, r9d, [rsp+0x60] = the incoming fifth)`; its value.
- `003EB910` (entered from `003EC770` + 0x44): **host fit holds** - the caller is a documented subject (L1461, table-row first cell: "| `003EC770` | 73 B | `002FB560` + 0x12A | keeps the incoming floats `xmm1`, `xmm2` and `x ..."). Sentence exact: null `rcx` or signed-negative dword `+0x10` -> no call; `movzx ecx, word [rcx+0x10]`; `[rsp+0x20]` = 1; `003EB92B call 003EC260` with `rdx`/`r8`/`r9` untouched.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
