# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-character-render-object-h8-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CHARACTER-RENDER-OBJECT-H8-1003` · Package: `_index/candidates/fable-home-character-render-object-h8-1003/` · Page: `17-Presentation-Rendering/Character-Rendering/character-render-object.md` (published in `005d10e7c`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0). 
- `rows.json`: 1 row(s), 5 anchors; mechanically rejected 0, missing 1.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 1 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `001E2250` (entered from `001E5370` + 0x81): **host fit holds** - the caller is a documented subject (L1296, table-row first cell: "| `001E5370` | 182 B | computes `n` = (qword `[rcx+8]` minus qword `[rcx]`) / 0x18 (signed ..."). Sentence exact at the level stated: the unsigned 32-bit capacity test (`ja` at `001E22A5` on (C-E)/0x18 by the 0x2AAAAAAAAAAAAAAB reciprocal); the stack copy with vtable `009010D8`; the `jae` split on `t` (`001E22F2`), `001E2250`+0xC6 / +0x19F = `001E1440`, the field-assignment shift loop, +0x149 / +0x1E8 = `00212C50` on the copy; the growth arm's `cmova` max, slot +0x10 of `[rcx+0x18]` at +0x238 (`001E2488`), the three construction loops writing vtable `009010B8`, the two fields, then `009010D8` and skipping null slots (`001E24B0`-`001E24C7`), slot 0 on each old element, the free through slot +0x18 at +0x36A (`001E25BA`), and the B/E/C stores.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
