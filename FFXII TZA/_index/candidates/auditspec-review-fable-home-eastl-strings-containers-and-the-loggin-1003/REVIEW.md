# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-eastl-strings-containers-and-the-loggin-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-EASTL-STRINGS-CONTAINERS-AND-THE` · Package: `_index/candidates/fable-home-eastl-strings-containers-and-the-loggin-1003/` · Page: `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 3 functions, 15 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 3 row(s), 15 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 2 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `001A3F10` (entered from `001A6A20` + 0xF8): **host fit holds** - the caller is a documented subject (L568, paragraph/list lead: "`001A6A20` (669 B) is a runtime `eastl::basic_string` build around the `008F67B0` literal  ..."). Sentence exact: the `memcmp` (`00861ED2`) descent over the shorter length with the length tie-break (`001A3F78`-`001A3F93`), `+8` on smaller else `+0`; `rcx+8` with smaller when the root is null (`mov al, 1`); the `[rcx+0x10]` fast insert (`001A3FBA`); the predecessor `0016D720` compare at `001A3FE8` storing `p`, 0 unless `p` is smaller; the two insert paths `001A3100` / `001A3190` / `0016D840(node, n, rcx+8, flag)`, `inc dword [rcx+0x28]`, `rdx` returned.
- `001BC950` (entered from `001BD1B0` + 0xA0): **host-fit defect** - `001BD1B0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `001BD1B0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `001BD340` (entered from `001BD1B0` + 0xD0): **host-fit defect** - `001BD1B0` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `001BD1B0` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
