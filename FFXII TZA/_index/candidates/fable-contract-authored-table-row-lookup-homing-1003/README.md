# Interior citations, cloud-drafted: CONTRACT-authored-table-row-lookup.md's entry-cited functions (FABLE, 2026-10-03)

The page named 1 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01HfPRM3vgupD1jscEXG8z9Y, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 1 staged with 5 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `0019CD40`: 0019CDC9-0019CDD1: rax = delta*0x18 is added to [rbx+8] and left in rax at ret 0019CDDA; the else-path return was unstated

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
