# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-the-music-changes-when-you-change-a-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-THE-MUSIC-CHANGES-WHEN-YOU-CH` · Package: `_index/candidates/fable-home-how-the-music-changes-when-you-change-a-1002/` · Page: `18-Audio/how-the-music-changes-when-you-change-area.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 3 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 3 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0046DE50`: `cmp ecx, 2; jge` (signed, so negatives pass); `movsxd`; `rcx*5 << 5` = 0xA0 stride; qword store 0 at `02CA6080 + ecx*0xA0`.
- Host: `0032EB40` is cited in the page's own `DG-6` answer as one of the two size readers. That is weak for a store to `02CA6080`, but it is not disclaimed, so it stands.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
