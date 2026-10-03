# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-resource-section-addressing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-RESOURCE-SECTION-ADDRESSING-1003` · Package: `_index/candidates/fable-home-resource-section-addressing-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/resource-section-addressing.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes, and its body belongs with the section-address pass `003E1C50`, which this page describes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 903 and the row (line 909) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 1 (`0046C1E0`, "already cited by" `the-character-render-record-array.md`; that page does cite it), skipped 0, missing 0.
- **`00512C50` (0x2D B), read in full.**
  - `mov ecx, [rcx+0x30]` / `call 0020E600` / `lea ecx, [rbx + rax]` (the 32-bit sum with the saved `edx`) / `call 0020E620` / `mov [rdi+0x30], eax`. `rax` is not touched after the second call, so the value returned is the value stored.
  - The sentence is exact. All 5 anchors are on these instructions.
- **entered_from.** `003E1C50` + 0x717 = `003E2367`, `call 00512C50`. It is the only caller (raw index and `edges.tsv`). At the site, `rcx` is `0020E600([rdi+4])` (the nested record just rebased at `003E2348`-`003E235A`) and `edx` = `esi`, the pass's delta.
- **Host fit.** The page describes `003E1C50` as the record walk behind the section address pass (line 863), with its nested `0020E600`/`0020E620` rebases (lines 867-875). This body is one more such rebase, applied to the nested record's `+0x30` field. It fits.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- `0051B120`, homed by `fable-home-add-motion-skeleton-and-high-model-tabl-1003` on `add-motion-skeleton-and-high-model-tables.md` from `003E1C50` + 0x818, has the same code on field `+0x10`. The two rows would read better if each pointed to the other.
- README: "No page cited these 2 functions" counts the rejected `0046C1E0`, which a page does cite. "these 1 function" (or "the staged function") would be accurate.
