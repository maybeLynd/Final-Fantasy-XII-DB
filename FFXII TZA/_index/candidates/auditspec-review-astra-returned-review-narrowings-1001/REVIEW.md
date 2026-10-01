# Audit-spec review: ASTRA returned review narrowings

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/returned-review-narrowings/`
Board task: `ASTRA-REQ-SPEC-RETURNED-REVIEW-NARROWINGS-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-index-domain.py` → exit 0; fresh result byte-identical to retained `index-domain-result-02.json`.
- **Prover re-run fresh:** `prove-index-domain-before-returned-review-01.py` → exit 0; fresh result byte-identical to retained `index-domain-result-01.json (before-state)`.
- **Prover re-run fresh:** `prove-special-override-domain.py` → exit 0; fresh result byte-identical to retained `special-override-domain-result-02.json`.
- **Prover re-run fresh:** `prove-special-override-domain-before-returned-narrowing-01.py` → exit 0; fresh result byte-identical to retained `special-override-domain-result-01.json (before-state)`.
- **Control re-run:** `prove-index-domain-wrong-lookup-model-control-01.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — refuses as designed — 'lookup outside retained FST; not valid Python negative indexing', exit 1, no result.

## Narrowing / notes

- Package omits `capture-index-path.py`, which `prove-special-override-domain*.py` pin by sha256 via the retained capture receipts. The byte-identical helper (sha256 cbfb9b43…a497) was recovered from the sibling `title-queue-pump-boundary` package and injected into a disposable copy; both provers then reproduce exactly. Packaging gap noted for the owner.
