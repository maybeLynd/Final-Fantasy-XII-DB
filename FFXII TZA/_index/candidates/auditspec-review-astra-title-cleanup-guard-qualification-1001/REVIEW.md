# Audit-spec review: ASTRA title cleanup guard qualification

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/title-cleanup-guard-and-annotation-prerequisite/`
Board task: `ASTRA-REQ-SPEC-TITLE-CLEANUP-GUARD-QUALIFICATION-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-title-cleanup-guard-scope.py` → exit 0; fresh result byte-identical to retained `title-cleanup-guard-scope-result-01.json`.
- **Prover re-run fresh:** `prove-title-cleanup-guard-scope-02.py` → exit 0; fresh result byte-identical to retained `title-cleanup-guard-scope-result-03.json`.

## Narrowing / notes

- `control-title-annotation-prerequisite.py` cannot re-run standalone: it references `*-frozen-ready` folders (e.g. `title-tracker-boundary-frozen-ready`) that lived in the authoring work dir, not the published leaf. Retained invocation receipt `title-annotation-prerequisite-control-invocation-01.status.json` (exit 0) and per-case receipts under `title-annotation-prerequisite-controls-01/` were inspected instead; both positive provers reproduce exactly.
