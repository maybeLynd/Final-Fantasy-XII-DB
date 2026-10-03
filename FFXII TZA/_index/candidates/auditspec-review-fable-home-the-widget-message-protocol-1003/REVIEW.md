# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-widget-message-protocol-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-WIDGET-MESSAGE-PROTOCOL-1003` · Package: `_index/candidates/fable-home-the-widget-message-protocol-1003/` · Page: `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 2 row(s), 10 anchors; mechanically rejected 1, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 2 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00297E10` (entered from `0029A0A0` + 0x4C5): **host fit holds** - the caller is a documented subject (L1424, paragraph/list lead: "- `0029A0A0` sends `{30, value, text state}` to a delegate at `+0x120`, and draws that tex ..."). Sentence exact: both compares (`00297E18`, `00297E20`) -> 0; object = `[[rcx+0x60]+0x30]`; signed max via `cmp r8d, ebx` / `jle`; `0029F4B0` then `00225580(obj, edx)`; 1.
- `00297F60` (entered from `0029A0A0` + 0x529): **host fit holds** - the caller is a documented subject (L1424, paragraph/list lead: "- `0029A0A0` sends `{30, value, text state}` to a delegate at `+0x120`, and draws that tex ..."). Sentence exact: equal `+0xEC` -> no store; `00296600(edx)`, `cmove` to the incoming `r8`; `X`/`A`/`R` chain with `R` = 0 for null `A` (`00297FA4`); `[R+0x18]` = result; `0020E620(0)` to dword `[R+0x20]`; `edx` to `+0xEC`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
