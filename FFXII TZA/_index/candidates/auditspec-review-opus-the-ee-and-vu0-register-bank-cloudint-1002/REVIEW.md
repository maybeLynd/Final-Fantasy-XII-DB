# Audit-spec review: OPUS cloudint interior citations (opus-the-ee-and-vu0-register-bank-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-EE-AND-VU0-REGISTER-BANK-CLOUDINT-1002` · Package: `_index/candidates/opus-the-ee-and-vu0-register-bank-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 9 rows applied, 40 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 9 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 9 rows exact vs the certified image, including 002330D0 (helper + low-16 product add on non-negative), 0029BC80 (case4 float-vector fill + min(1.0,max(0.3,dot)) * 1.428571 chain; case2/1 Q-call ordering with per-case word stores), 00398390 (in-place float multiply + dual vector copy + cross-product stores at 022D91A0/022D9300), 003A2B90 (sign-extended xmm1 splat + subps to 022D92E0 and rcx), the two 0050C-pops, 00510870 (three pops -> helper(c,b,a), gated call list) and 00863410.
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
