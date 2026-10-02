# Audit-spec review: OPUS cloudint interior citations (opus-field-init-weather-to-legacyps2gs-rebuil-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FIELD-INIT-WEATHER-TO-LEGACYPS2GS-REBUIL-CL` · Package: `_index/candidates/opus-field-init-weather-to-legacyps2gs-rebuil-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh → exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 1 rows applied, 5 anchors, rejected/skipped/missing 0.
- Semantic sample: all 1 rows read against the certified image - 00180650 exact: r9b->+0xC0 store, ecx-selects 001A94C0 vs vtable slot+8, 001E3E80/001E3FF0 gate to 001A4FE0.
- Limits hold: body statements only; the cloud draft is a pointer, OPUS's re-read stands.
