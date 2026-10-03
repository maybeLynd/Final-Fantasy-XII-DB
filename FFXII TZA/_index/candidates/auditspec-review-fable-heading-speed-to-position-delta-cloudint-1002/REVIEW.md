# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-heading-speed-to-position-delta-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HEADING-SPEED-TO-POSITION-DELTA-CLOUDI` · Package: `_index/candidates/fable-heading-speed-to-position-delta-cloudint-1002/` · Page: `06-Movement-And-Navigation/heading-speed-to-position-delta.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0.
- Semantic pass: **all 3 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 3 exact. `0022DE60` (0x4D8 bytes) was read in full against its long sentence: the signed 0x5000/0x4000 id split; the mask/value merge at `0209A2D0+0x110+8k` with k = 32 + bits 13-17 and the unsigned `>= 80000000h` skip; the 0x90-byte branch (`381D90`, 3x3 transform, `3810B0` radius, v scaled by L-r); the 32-byte branch (low-3-bits gate, the plane distance s in (-0.001, L) with -0.001 read from `009002EC`, the `22EAC0` call at +0x35E with `r8`=p, the w substitution); the shared +0x30/+0x34 max update and the accumulation into qword +0x28. `00380FA0`'s three-way kind dispatch (0 -> the call at +0x95 = `00381AC0`, 1 -> `00381630`, 2 -> `00381450`) and -1.0 at `01CEBC9C` are also exact.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
