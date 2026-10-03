# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-dyngeo-instance-family-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-DYNGEO-INSTANCE-FAMILY-CLOUDINT-1002` · Package: `_index/candidates/fable-dyngeo-instance-family-cloudint-1002/` · Page: `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 6 rows, 21 anchors; rejected 0, missing 0.
- Semantic pass: **all 6 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). All 6 exact, including the whole of `001EE650`: i = 27a+9b+3c+d by the `lea x,[x+x*2]` chain, 16-byte rows at `00902750`, both remaps (6->0x11, 7->0x12, 2->0xF, 3->0x10 via `esi`=0x10), the a-selected store of 1, the i==10 / sixth-arg override to 5, `(v-3) & ~2 == 0` for 3-or-5, and `movzx r9b` of `rcx>>32` divided by 255.0 at `008C5B40`.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.
