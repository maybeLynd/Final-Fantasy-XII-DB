# Audit-spec review: OPUS mapctrl interior citations

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-MAPCTRL-INTERIOR-1001` · Package: `_index/candidates/opus-mapctrl-interior-1001/` · Commit: 20e00ea21

## Verdict: ACCEPT

- `python mapctrl_interior.py` re-run in place: `VERIFY 36 functions, 120 anchors / ALREADY / FAILS 0` — every anchor is an in-extent instruction boundary decoding to the
  recorded mnemonic; page section already present (`ALREADY`, byte-preserving).
- Semantic sample: 3 rows — `001806F0` null-gated `+0x20` store, `003CD5D0` 0x40-record release/unlink (`02B47770/78/80`), `00291D90` 625-B message dispatcher (state machine in `+0x168` bits 16-19, ten `+0xC8` slots, `0024A440` request into `+0xC0`) — all exact.
- Method verdict for all 17 interior packages: `_index/candidates/auditspec-review-interior-method-1001/REVIEW.md`
  (verdict:ACCEPT).

