# Audit-spec review: ASTRA renderer queue allocator

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/renderer-queue-allocator/`
Board task: `ASTRA-REQ-SPEC-RENDERER-QUEUE-ALLOCATOR-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-renderer-queue-allocator.py` → exit 0; fresh result byte-identical to retained `renderer-queue-allocator-result-02.json`.
- **Control re-run:** `control-renderer-queue-allocator.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — all mutated-source cases refused as documented.

## Narrowing / notes

- `prove-renderer-queue-allocator-before-rip-scale-fix-01.py` refuses at HEAD ('unbound external tail') — per README this is the superseded Prover01 that encoded the wrong null-vs-empty index representation; Prover02 is the operative proof.
