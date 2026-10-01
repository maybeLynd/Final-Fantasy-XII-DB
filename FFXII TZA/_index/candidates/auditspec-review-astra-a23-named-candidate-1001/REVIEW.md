# Audit-spec review: ASTRA a23 named candidate

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/a23-release-candidate-059ee3a6c/`
Board task: `ASTRA-REQ-SPEC-A23-NAMED-CANDIDATE-AND-PREREQUISITE-1001`

## Verdict: ACCEPT

## What was checked

- **Control re-run:** `retained/check.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — refuses at HEAD with 'current verifier is not candidate verifier' — by design it pins the candidate's generation.py identity
- **ZIP claim independently verified:** `Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip` sha256 = `23256f18c501f7678e3b88ffe26c74e9bc26b7b532de9cb41840d78b359157c7` — byte-exact match to the retained result.json.
- Retained `result.json` carries the complete SCOPED_RELEASE_SNAPSHOT_SOURCE_CHECKED receipt (candidate commit `059ee3a6c`, manifest sha `865299843d…`, 35 members).

## Narrowing / notes

- The package is a scoped snapshot/source verification, explicitly not full A23 acceptance — the README's own limits ('full A23 remains unaccepted', moving CURRENT not compared) are preserved by this review.
