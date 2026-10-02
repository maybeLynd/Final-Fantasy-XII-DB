# Audit-spec review: OPUS cloudint interior citations (opus-static-initialization-order-and-injectio-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-STATIC-INITIALIZATION-ORDER-AND-INJECTIO-CL` · Package: `_index/candidates/opus-static-initialization-order-and-injectio-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 5 rows applied, 23 anchors, rejected/skipped/missing 0.
- Semantic pass: every one of the 5 rows checked sentence-by-sentence against the shipping body in the certified image (SHA256 73461D08...) — all 5 rows exact: the three initializer triplets 00163DB0/00163E30/00163EA0 (00631A60/00631C40/00631E20 calls with verified table args, bit1-clear+bit3-set dword updates, three qword stores, vtable store, tail 00808B90 with stub address), 00164180 (006318A0 + dword 0 at 02CF82A8 + vtable 00D582D0), 001E0F70 (InputManager singleton -> MaterializeRuntimeBindingProfiles + tail RestoreDefaultBindingProfiles).
- Limits hold: body statements only; static/native verification, no engine-in-loop or replay claims.
