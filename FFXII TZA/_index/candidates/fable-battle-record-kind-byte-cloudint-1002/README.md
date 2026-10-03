# Interior citations, cloud-drafted: battle-record-kind-byte.md's entry-cited functions (FABLE, 2026-10-02)

The page named 5 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_013aUyF9Cw8dmXC6Vyt6UA4p, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 5 staged with 25 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `00273910`: content verified (`00273925` cmp 3, `0027393D` sete after the call at `00273934` with ecx restored from ebx); the first callee, new to the page, is now cited by its site `00273910` + 0x8 (`00273918`), where rcx still holds the incoming value
- `003528C0`: content verified (`003528C6` rcx = r9, `003528D3` rcx = the saved rdx, `003528DB`/`003528DE` re-read word +0 and byte +0x15 from rbx after both calls); the tail-jump target, new to the page, is now cited by its site `003528C0` + 0x27 (`003528E7`)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
