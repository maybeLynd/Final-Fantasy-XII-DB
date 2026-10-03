# Interior citations, cloud-drafted: CONTRACT-ppfx-effect-creation.md's entry-cited functions (OPUS, 2026-10-03)

The page named 3 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `00718350`: byte re-read by a non-drafting agent: Body checks out (64-bit strlen loop from rbx = -1, test of the low dword ebx, 007153B0(t, ebx, 0) with rcx still t, memcpy (00861EBA -> VCRUNTIME140 memcpy) of movsxd(ebx+1) bytes to qword [t+8] read after the call, empty/null path freeing qword [t+8]-8 via 006DA8A0 unless null or 02EA1720, then 0 and 02EA1720). Defect: 'calls 007153B0(t, that dword, 0), stores it at dword [t]' - after a call, 'it' reads as the call's return value; the code stores ebx, the length dword (mov dword [rdi], ebx at 007183D4), and the return in eax is discarded. Named explicitly.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
