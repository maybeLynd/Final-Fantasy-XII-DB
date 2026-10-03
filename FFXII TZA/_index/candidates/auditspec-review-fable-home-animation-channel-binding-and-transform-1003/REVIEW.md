# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-animation-channel-binding-and-transform-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ANIMATION-CHANNEL-BINDING-AND-TRA` · Package: `_index/candidates/fable-home-animation-channel-binding-and-transform-1003/` · Page: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 1, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `0059FC20` (entered from `005C0820` + 0x11F): **host fit holds** - the caller is a documented subject (L75, paragraph/list lead: "`005C0820` walks that path. For each binding descriptor it splits the name on `'.'` (`strc ..."). Sentence exact: null `rdx`/`r8` -> 1 (`0059FC36`/`0059FC3B` -> `0059FC8E`); `jae` at `0059FC40` gives 5 for `r8` below `rdx`; `sub ebx, eax` is the 32-bit length; `0059FC5A call 005994A0(rdx, len+1)`; null -> `lea eax, [rdx+0xd]` = 0xD; `0059FC78 mov byte [rbx+rax], 0`; `0059FC7C call 0059FBE0(rcx, buffer)`; 0.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
