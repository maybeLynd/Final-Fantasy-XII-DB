# Audit-spec review: OPUS cloudint interior citations (opus-mh-movie-seek-index-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MH-MOVIE-SEEK-INDEX-CLOUDINT-1002` · Package: `_index/candidates/opus-mh-movie-seek-index-cloudint-1002/`

## Verdict: ACCEPT

## What was checked

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY`/`FAILS 0` (idempotent).
- `rows.json` reconciles with the README: 2 rows applied, 10 anchors, rejected/skipped/missing 0.
- Semantic pass: both rows exact vs the certified image: 001D9F90 (unsigned edx>1 ret; lock xadd -1 at +0x24+edx*4; float at +0x8C = (005CC930()-02CB60E8)+2.0 via 01DFCFE0) and 0035CF50 (qword 022CA468==0 or dword 022CA45C!=0 -> 002E1CA0(8,0)+002E1CA0(8,0xB)+00252D90()+zero 022CA45C; else no work).
- Limits hold: body statements only.
