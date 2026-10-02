# Audit-spec review: FABLE cloudint interior citations (fable-the-menu-effect-registry-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-MENU-EFFECT-REGISTRY-CLOUDINT-1002` · Package: `_index/candidates/fable-the-menu-effect-registry-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 6 rows applied, 26 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 6 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 6 rows exact: 00374930 (32 dwords zeroed stride 0x70 from 02EBFA48 while < 02EC0848 signed), 003A7420 (16 slots step 8 re-reading 02EBEFB0, 00332FA0 on non-null qwords), 00460120/005294B0 (003697F0/0024B1C0 on +0x338/+0x3D0 non-null, bit0 of byte+0x3C0 + non-null +0x3B0 -> tail 0024B1C0), 0050D9A0 (ordered call list + 0026B8E0(k) for k 0..3), 0057E950 (ecx4/edx0/bit1-of-+0xC0 arm vs ecx5 arm, record {0xD, byte+0x39A-or-0xFF, edx} -> 00247510, clear bit0 of +0xC0).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
