# Audit-spec review: FABLE cloudint interior citations (fable-the-staged-look-command-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-THE-STAGED-LOOK-COMMAND-CLOUDINT-1002` · Package: `_index/candidates/fable-the-staged-look-command-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 20 rows applied, 82 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 20 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 20 rows exact vs the certified image, including 003E36F0/003E3720/003E37A0/003E37C0 (bitfield replaces: bits 9-11 + 16-byte record copy to +0x20 vs +0x30 by edx; bit5 of +0x1C via the shl/xor/and/xor idiom with conditional 00513150; bits 30-31 from dx bit0 + bts 0x1E; bit 26 + bit 4), 0042D970 and the initializer globals (002EFA20's 022BDD5C-022BDEB8 block, 002F1A00, 0036C5A0's 15-entry 0xA8-stride +0xA0 store, 003DD7E0's 5x16 0x1C-stride writes).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
