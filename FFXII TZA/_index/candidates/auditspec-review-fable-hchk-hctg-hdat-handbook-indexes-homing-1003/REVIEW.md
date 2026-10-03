# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-hchk-hctg-hdat-handbook-indexes-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HCHK-HCTG-HDAT-HANDBOOK-INDEXES-HOMING` · Package: `_index/candidates/fable-hchk-hctg-hdat-handbook-indexes-homing-1003/` · Page: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `005792F0` exact: the 9-object loop over the words at `00D238A0` sets bit 0 of dword `+8` from `seta sil` on byte `+0xC5` (non-zero) (`00579342`/`00579346`); byte `+0xC5` zero -> `002F9860(0x868 + (byte +0xC4 != 0))` (`005793D2`-`005793E2`) and `002D8910(r8, 0, 0, result, 0)` at `+0x10B` (`005793FB`), return 1; otherwise k = `r9d`, or word `[[+0xC8]+0xE8]` - `r9d` - 1 when byte `+0xC4` != 1 (`00579366`-`00579377`); returns 0 when `byte +0xC0 & 3` and k equals byte `+0xC1` of `[[02CA9748]+0x128]` (-1 when null, `00579398`); else `00577C30(byte +0xC4, rdx, k, 00D237C0, qword +0xD0)` (`005793C9`), return 1.
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
