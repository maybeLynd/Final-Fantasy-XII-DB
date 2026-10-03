# Interior citations, cloud-drafted: sound-trigger.md's entry-cited functions (OPUS, 2026-10-03)

The page named 9 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter-r4, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 9 applied with 45 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `007B5AD0`: byte re-read by a non-drafting agent: The 0x28-byte table is not at `02EAD6A0`: its base is loaded from the qword at `02EAD6A0` (`007B5B60 mov rax, qword ptr [rip+...]`).
- `007BC8D0`: byte re-read by a non-drafting agent: The 'most then given dword `+8` = 0, float `+0xC` = 1.0 ...' clause is attributed only to the 0x30-byte slots, but the same writes also go to three of the four 0x40-byte slots (`+0x88` via `007BCB95`, `+0x108`, `+0x148`), while the slot at `+0xC8` and the 0x30-byte slots at `+0x1B8`, `+0x218`, `+0x248`, `+0x278` and `+0x3C8` only get their five fields cleared (again for all but `+0x3C8`); 'most' does not say which.; The 0x40-byte slots' cleared fields (qwords `+8`/`+0x10`, dwords `+0x1C`/`+0x24`, byte `+0x20`, qword `+0x38`) are not stated.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 9 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
