# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-save-image-buffers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-SAVE-IMAGE-BUFFERS-1003` · Package: `_index/candidates/fable-home-contract-save-image-buffers-1003/` · Page: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 5 functions, 25 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 5 row(s), 25 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 2 fit, 3 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `005DE310` (entered from `00616CC0` + 0x58): **host-fit defect** - `00616CC0` appears 1 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `00616CC0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `005DE390` (entered from `00616D20` + 0x58): **host-fit defect** - `00616D20` appears 1 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `00616D20` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `00616140` (entered from `00162370` + 0x21): **host fit holds** - the caller is a documented subject (L1068, table-row first cell: "| `00162370` | 81 B | runs four initialisers, each with the object address in `rcx`: a 139 ..."). Sentence exact: `00616156 call 005DCC10` with `rcx` unchanged; dword 0 at `+0x38`, `0061616B call 00627750(rcx+0x38, 1)`; qwords `+0x88`, `+0x68`..`+0x80` zeroed; returns `rbx` = the incoming `rcx`.
- `006161A0` (entered from `00162370` + 0x2E): **host fit holds** - the caller is a documented subject (L1068, table-row first cell: "| `00162370` | 81 B | runs four initialisers, each with the object address in `rcx`: a 139 ..."). Sentence exact: `006161B6 call 005DCC40`; dword 0 at `+0x30`, `006161CB call 00627800(rcx+0x30, 1)`; qwords `+0xA0`, `+0x78`..`+0x98` zeroed; returns the incoming `rcx`.
- `00623E70` (entered from `0062B1E0` + 0x29): **host-fit defect** - `0062B1E0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence exact (but see host fit): `btr eax, 0x1f` on a copy, `jbe` at `00623E7A`, `cmove rcx, r8` zero for value 0, `shl 6` / `+0x20` with `mov eax, edx` zero-extending. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `0062B1E0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
