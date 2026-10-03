# Interior citations, cloud-drafted: intentionally-ownerless-functions-and-shared-scratch.md's entry-cited functions (FABLE, 2026-10-03)

The page named 13 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_0113mD5fGL648y6vQqrtN2Rj, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 12 staged with 60 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**FABLE corrections on re-read.**

- `00182BE0`: `00182C52` takes the address 02CF7480 with lea and `00182C59` stores that pointer; the record holds the address, not the qword at it
- `003460C0`: `003460DE` passes rbx (the +0x9 call result) to 002ECF10; the +0x14 call return is discarded, "that result" read as the latter

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
