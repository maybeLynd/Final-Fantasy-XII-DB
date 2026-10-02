# Audit-spec review: FABLE cloudint interior citations (fable-how-a-script-changes-the-battle-party-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-SCRIPT-CHANGES-THE-BATTLE-PARTY` · Package: `_index/candidates/fable-how-a-script-changes-the-battle-party-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 8 rows applied, 36 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 8 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 8 rows exact: 00324360 (0037CB50 -> 1/0), 0034CDF0 (dword[r8] dispatch: 0->store1+continue, 1->00328B20(byte+4)+003601B0(0x13)+store2+ret1, 2->003596B0 nonzero or 003601C0(0x13)+ret0, else 1), 003596B0 (inverse of ==1), 003596D0/00359740 (n=0031B510/00320800 fill, first-n dword membership, cookie check 00808C40/01F44830), 00359BA0/00359C00 (OR of 1<<d over first n), 0037CB50 (02EBF400/02EBF3FD/02EBF3FE signed-byte ladder).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
