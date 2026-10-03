# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-add-motion-skeleton-and-high-model-tabl-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ADD-MOTION-SKELETON-AND-HIGH-MODE` · Package: `_index/candidates/fable-home-add-motion-skeleton-and-high-model-tabl-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes. The body is one of the nested-record relocators run by the load-side pointer fixup pass `003E1C50`, which this page reads as a body together with that relocator family. The host fits.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 542 and the row (line 548) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0.
- **`0051B120` (0x2D B), read in full.** `mov ecx, [rcx+0x10]` / `call 0020E600` at +0x12 (`0051B132`) / `lea ecx, [rbx + rax]` (the 32-bit sum with the saved `edx`) / `call 0020E620` at +0x1A (`0051B13A`) / `mov [rdi+0x10], eax`. The sentence is exact. All 5 anchors are on these instructions.
- **entered_from.** `003E1C50` + 0x818 = `003E2468`, `call 0051B120`. It is the only caller (raw index). At the site, `rcx` is `0020E600([rdi+0x14])`, the nested record just rebased at `003E2449`-`003E245B`, and `edx` = `esi`, the pass's delta.
- **Host fit.** Line 490 describes `003E1C50` as the load-side fixup pass whose "nested structures recurse through the type-dispatched relocators `00421D20`, `00512A90`, `004719B0`, `0051A380`, `0051B850`, `005161D0` and `0040EEA0`". This body is one more of them, on the nested record's `+0x10` field. Apart from `_index/ADDRESS-INDEX.md`, no other page cites it.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- The twin `00512C50` (the same code on field `+0x30`, from `003E1C50` + 0x717) is homed on `02-Resource-And-Asset-Pipeline/resource-section-addressing.md` by `fable-home-resource-section-addressing-1003`. Both hosts cite `003E1C50` as a body, so neither placement is wrong, but each row would read better if it pointed to the other. Adding `0051B120` to the line-490 relocator list would also help.
