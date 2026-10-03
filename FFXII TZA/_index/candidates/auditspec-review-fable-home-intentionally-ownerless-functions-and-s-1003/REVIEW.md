# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-intentionally-ownerless-functions-and-s-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-INTENTIONALLY-OWNERLESS-FUNCTIONS` · Package: `_index/candidates/fable-home-intentionally-ownerless-functions-and-s-1003/` · Page: `00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md` (published in `005d10e7c`)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` re-run fresh from the package directory with the analysis venv python -> `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0` (exit 0). 
- `rows.json`: 2 row(s), 10 anchors; mechanically rejected 0, missing 12.
- Host fit: each caller tested against the page with a replica of FABLE's own `documented_subjects()` (`homing_pack.py`, 2026-10-03): the caller must be a table-row first cell, an address in a heading, or the lead of a paragraph or list item; struck lines and the package's own homed rows excluded. Result: 2 fit, 0 misfit.
- Sentences: every fitting row read clause by clause against raw capstone output of the certified image (SHA256 73461D08...), plus any misfit row noted below as read.

## SWE2-AUDIT-SPEC rows

- `00311E90` (entered from `00346EB0` + 0x6): **host fit holds** - the caller is a documented subject (L1060, table-row first cell: "| `00346EB0` | 57 B | calls the function at `00346EB0+0x6`, then for `ebx` = 0 to 3 calls  ..."). Sentence exact: four iterations of `0031B810(esi)`; null P or null `[P+0x698]` skips; `[Q+0x64] | [Q+0x3C]` tested against 0x80000003 with `00377C20(that OR)` zero skipping; the `cmp rdi, 4` / `jge` store guard into `022C1788` and the count; then `or dword [P+4], 0x600` over the first count non-null entries.
- `0041C770` (entered from `00423380` + 0x39): **host fit holds** - the caller is a documented subject (L1065, table-row first cell: "| `00423380` | 71 B | returns 0.0 in `xmm0` when dword `rcx+0xc4` is -1 or when `0051B9E0` ..."). Sentence exact: `movsx` word `+0x28`; k from 1 while k < n (signed); the byte pointer starts at `rcx+0x165` = `rcx+0xC5+1*0xA0` and steps 0xA0; the match returns float `rcx+0x3C+k*0xA0` (`lea rcx, [rax+rax*4]` / `shl 5`); `xorps` 0.0 otherwise.

## SWE2-AUDIT-SPEC limits

Body statements and host fit only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is. A host that documents the caller through a previously homed row (a homing-table first cell) counts under the published rule; that chaining is noted, not ruled on.
