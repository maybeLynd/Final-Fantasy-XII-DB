# Interior citations, cloud-drafted: game-settings-ini-and-runtime-config.md's entry-cited functions (FABLE, 2026-10-03)

The page named 18 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_0113mD5fGL648y6vQqrtN2Rj, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 17 staged with 82 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**FABLE corrections on re-read.**

- `00798AC0`: `00798C9B` stores a qword 0 at P+2 (bytes P+2 to P+9), not a single zero at P+2

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
