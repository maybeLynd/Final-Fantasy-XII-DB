# Audit-spec review: ASTRA title cleanup count selector

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/title-cleanup-count-selector/`
Board task: `ASTRA-REQ-SPEC-TITLE-CLEANUP-COUNT-SELECTOR-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-title-cleanup-count-selector.py` → exit 0; fresh result byte-identical to retained `title-cleanup-count-selector-result-01.json`.
- **Control re-run:** `control-title-cleanup-count-selector.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — 'Missing second return branch, false field offset and wrong root metadata refused; positive reused'.

## Narrowing / notes

- Package omits the `prepare-residue-packet-publication.py` helper the control imports; injected the byte-identical helper from `title-queue-pump-boundary` into the disposable copy. Packaging gap noted for the owner.
