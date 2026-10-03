# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-bodies-the-list-cuts-short-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-BODIES-THE-LIST-CUTS-SHORT-EE-100-75FFF` · Package: `_index/candidates/opus-the-bodies-the-list-cuts-short-ee-1003-2/` · Page: `99-Unresolved-Residual/Unlisted-Code/the-bodies-the-list-cuts-short.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00729920` exact: the two home-slot stores, `0075AE30(rcx, &third, &fourth)`, xmm1 to xmm4, k kept in r10d; the eight remaps; `ja` above 0xE to image base + 0x609A58; jump table read from the image at `00729A60`: entries 0/1 -> `00729A58`, 2/4 -> `00729A3A`, 6/8 -> `007299D5`, 0xA -> `007299ED`, 0xE -> `00729A52`.
- Advisory, not a defect: functions.tsv lists the body as 189 B (ending at `007299DD`, inside the instruction at `007299DB`), so 'the listed extent ends with the first instruction at `007299D5`' is approximate; no behaviour claim depends on it.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
