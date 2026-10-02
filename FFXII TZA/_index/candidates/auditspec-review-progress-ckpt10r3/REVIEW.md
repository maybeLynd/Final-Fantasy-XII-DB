# Audit-spec review: progress package (CKPT10R3 executed re-review)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FRONTIER-REQ-AUDITSPEC-EXECUTED-REVIEW-PROGRESS-CKPT10R3`
Target: `Database/FFXII TZA/_index/progress/` · Gate dependency: `cd6bd7f58`
(record `_index/candidates/data-review-my-progress-metrics-1001/readme.md`)

## Verdict: ACCEPT

## Executed receipts (all re-run this review)

- `python _index/progress/test_progress_report.py` → **FAILS 0** — all T1–T42 checks pass,
  including the live-corpus checks (T2 vendored classifier == live instrument over 1820 rows, zero
  diffs; T34b live `page_boxes` obligation contract; T35 struck-id row → WITHDRAWN/STRUCK with live
  `UNKNOWN = 0`; T41a–d export pin / later-commit isolation / mixed-ZIP refusal / mid-export failure).
- `python Database/Tools/analysis-kit/gfz-scripts/test_generation.py` → **FAILS 0**
  (G1–G15, E1–E8, C1, R1–R8).
- `python Database/Tools/dashboard/test_requirements.py` → **FAILS 0** (MP1–MP17 fixtures green).
- `progress_report.py status` → coherent live report:
  `OQ open 5 partial 7 | L2 MET 52/52 | tasks open 207 | fp a72e7c0fdb71`.
- `progress_report.py check` → `STALE: generated ... fp a72e7c0fdb71 vs current 8ca39629f8a4`, rc 1 —
  correct derived-data behaviour: the committed generation names its inputs' fingerprint and refuses
  to masquerade as current once the corpus moved (g20261002T081334Z is deliberately dated).

## Source-verified items

- The audited() dedup repair is real at source: `requirements.py::audited` (line 432) delegates to
  the canonical `progress.audit_pass_recorded` (line 353), eliminating the hand-copied drift hazard
  the gate review identified. No second copy remains.
- The generation machinery self-tests its failure modes: INCOMPLETE on missing inputs, mid-build
  source-move abort, last-COMPLETE retention — all exercised and PASS in T12–T14/T40.

## Scope

Executed re-review of the progress-report package only. Counts (register ANSWERED, page obligations,
family figures) are live-corpus-derived and move with the docs; this review verifies the method and
the machinery, not frozen figures — same distinction the gate review drew. No claim on
doc-content correctness beyond the reporter's own parsers.
