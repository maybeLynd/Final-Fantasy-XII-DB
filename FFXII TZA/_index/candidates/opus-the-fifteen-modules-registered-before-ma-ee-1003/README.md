# Interior citations, cloud-drafted: the-fifteen-modules-registered-before-main.md's entry-cited functions (OPUS, 2026-10-03)

The page named 6 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter-r4, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 6 applied with 30 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `005FD2A0`: byte re-read by a non-drafting agent: The string is not named by the source at `00D3EB38`: each step reads the string pointer from the qword 8 bytes BEFORE the stepping pointer (`005FD32A mov rdx, qword ptr [r14 - 8]`), while the dwords are at `+0`/`+4` of it.; The rounded slot size is stored as a word (`005FD3EF mov word ptr [rip+...], ax`); the width was not stated.
- `006A5C00`: byte re-read by a non-drafting agent: The blend factor omits the arguments of `00861F6E` (the CRT `powf` thunk): it is called with float `+0x24` in `xmm0` and the third argument in `xmm1` (`006A608B`, `006A60B5`, `006A60C0`).

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 6 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
