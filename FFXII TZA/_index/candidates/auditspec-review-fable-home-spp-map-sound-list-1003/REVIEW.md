# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-spp-map-sound-list-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-SPP-MAP-SOUND-LIST-1003` · Package: `_index/candidates/fable-home-spp-map-sound-list-1003/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` (published in `3a65dc239`)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0). This package carries the applier from before the host-fit rule was enforced, so its `FAILS 0` says nothing about host fit.
- `rows.json`: 2 row(s), 10 anchors; mechanically rejected 0, missing 0.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 1 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00210D90` (entered from `001DBF50` + 0x32): **host-fit defect** - `001DBF50` appears 2 time(s) on the page outside the homed rows, never as a documented subject (no table-row first cell, heading or paragraph/list lead). Sentence not read: the host fails first. A whole-database scan (`hostfind.py`, same test) finds **no page** documenting `001DBF50` as a subject, so no caller-host home exists. **Repair:** withdraw the row from this page's homed section; the body returns to the unhomed pool (the caller-uncited class of the three-way split).
- `003DF360` (entered from `003DF2C0` + 0x83): **host fit holds** - the caller is a documented subject (L436, table-row first cell: "| `003DF2C0` | 154 B | Uses the sign-extended `ecx` as a record pointer, calls `0036B970`  ..."). Sentence exact: `cmp edx, 7` / `ja`; `s` = `02B59360` + (`movsxd ecx`*8 + `movsxd edx`)*0x38 (`003DF380`/`003DF384`); null `r8` exits; `r8` to `s+8`; `q` = `r9` or `r8` + dword `[r8+0xc]`; `002DEE90(-1)`, `002DF070(q, [r8+8])` to dword `[s]`, `002DEE90(-1)`, byte 4 at `s+0x10`.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
