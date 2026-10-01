# Audit-spec review: ASTRA softedges source repair

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/returned-softedges-source-prerequisite-repair/`
Board task: `ASTRA-REQ-SPEC-RETURNED-SOFTEDGES-SOURCE-REPAIR-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `check-softedges-member-boundaries.py` → exit 0; fresh result byte-identical to retained `softedges-member-boundaries-result-04.json`.
- **Prover re-run fresh:** `check-softedges-member-boundaries-legacy-02.py` → exit 0; fresh result byte-identical to retained `softedges-member-boundaries-result-03/04 legacy-result`.
- **Prover re-run fresh:** `check-softedges-member-boundaries-03-before-returned-review-repair-01.py` → exit 0; fresh result byte-identical to retained `softedges-member-boundaries-result-03.json (pre-repair state)`.
- **Prover re-run fresh:** `reduce-softedges-pointer-key-binding.py` → exit 0; fresh result byte-identical to retained `softedges-pointer-key-binding-result-04.json`.
- **Prover re-run fresh:** `reduce-softedges-field-extent.py` → exit 0; fresh result byte-identical to retained `field-extent-result-03.json`.
- **Prover re-run fresh:** `reduce-softedges-field-extent-before-returned-review-repair-01.py` → exit 0; fresh result byte-identical to retained `field-extent-result-02.json (pre-repair state)`.
- **Control re-run:** `control-field-source-complete-twin.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — 'Complete field copy passes; same copy with only reviewed displacement bytes changed refuses'.
- **Control re-run:** `control-returned-softedges-source-repairs.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — 'Complete pointer positive twin and ten returned/required-prerequisite controls verified on final actual callers'.
- **Control re-run:** `control-softedges-member-source-qualification.py` in a disposable package copy (ROOT-resolving path under `Database/Tools/work`) — PASS — 'Both returned byte-only defects, consistent changed bytes and required upstream failure refused; no final result'.

## Narrowing / notes

- Controls embed cross-package fixtures (`phyretext-pointer-key-binding`, `phyretext-softedges-field-extent`, sibling control dirs); re-ran in disposable full-package copies under a ROOT-resolving path. `control-returned-softedges-source-repairs.py` additionally consumes `softedges-member-source-qualification-controls-01` as an upstream fixture — that dir must be retained in the copy for the `upstream-facts-missing` case.
