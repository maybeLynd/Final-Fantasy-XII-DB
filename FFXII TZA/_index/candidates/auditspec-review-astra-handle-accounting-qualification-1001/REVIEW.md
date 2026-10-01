# Audit-spec review: ASTRA handle accounting qualification

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/handle-accounting-qualification/`
Board task: `ASTRA-REQ-SPEC-HANDLE-ACCOUNTING-QUALIFICATION-1001`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-handle-accounting-qualification-03.py` → exit 0; fresh result byte-identical to retained `handle-accounting-qualification-result-03.json`.
- **Control re-run:** `control-handle-accounting-qualification-02.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — 'Three distinct actual refusals; prior upstream refusal reused, coherent guard/preimage controls finished'.

## Narrowing / notes

- README directs `prove-handle-accounting-qualification-03.py`; drivers -01/-02 are retained refused superseded drivers and correctly refuse at HEAD.
- `control-handle-accounting-qualification.py` case `changed-guard-clear` still refuses but the expected error string drifted: the strengthened `validate-title-source-annotations.py` now rejects the mutation at the access-annotation gate ('memory/address/access annotation disagrees at 0x36c61a') before the pinned 'reference byte identity changed' check. Refusal is preserved and arguably stronger; control text is stale, not the gate. Bounded note for the owner; -02 reproduces cleanly.
