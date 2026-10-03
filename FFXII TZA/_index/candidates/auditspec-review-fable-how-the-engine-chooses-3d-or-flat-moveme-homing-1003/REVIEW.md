# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-how-the-engine-chooses-3d-or-flat-moveme-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-THE-ENGINE-CHOOSES-3D-OR-FLAT-MOVE` · Package: `_index/candidates/fable-how-the-engine-chooses-3d-or-flat-moveme-homing-1003/` · Page: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` (commit b7c6eb07d)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...), call offsets resolved:
  - `003DD8D0` exact: `02B581A4 + ((sx edx << 4) + sx r8d) * 0x1C` compared with 4 (`003DD905`); then `002E9560(rcx)` at `+0x3E` -> `xmm1` of `002E4F40` at `+0x49`; `or byte [rcx+0xD], 1`; `byte [rcx+0xF5] = sil` (low byte of sign-extended `r8d`); `002E8170(rcx, bit 7 of byte +0xD of 00263F40(rcx))` at `+0x6B`; `002EB080(rcx, ((edx << 4) | r8d) << 16 | r9d, 0)` at `+0x88` with `xmm3` = the stack float `[rsp+0x50]` (the fifth argument at entry).
- Limits hold: body statements only, static evidence; the draft and FABLE's re-read are not independent review, this record is.
