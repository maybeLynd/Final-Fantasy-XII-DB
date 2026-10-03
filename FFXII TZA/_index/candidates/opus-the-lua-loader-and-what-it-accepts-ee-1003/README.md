# Interior citations, cloud-drafted: the-lua-loader-and-what-it-accepts.md's entry-cited functions (OPUS, 2026-10-03)

The page named 44 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 44 applied with 220 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `00585270, 005853F0, 00585570`: OPUS re-read: family-sibling rows referred to an unnamed 'family base'; each sibling checked at the bytes to share the base's instruction form and rewritten as a self-contained sentence with its own values (fix_family_siblings.py)
- `00682E30`: OPUS re-read: the branch at 00682E9A tests ZF from `sub rbx, rax` (the cleared pointer), not the bit; the insert at 00682EE9..00682EF7 links before the sentinel, i.e. at the tail
- `0081E5A0`: OPUS re-read: a null qword c+0x38 skips the call but still reaches 0081DC10 with rdi = the incoming rdx (0081E6E0 -> 0081E6FE)
- `008233F0`: OPUS re-read: `jbe 008234C7` at 008234AD calls the line hook when the position is at or below the saved one; the line comparison runs only when it is above
- `00828D30`: OPUS re-read: 008135B0 sets each closure into the table at -(nup+2) (the index-2 table pushed by 008109F0) with nup copies of the top value (the package table copy from 00810730) as upvalues
- `0082F000`: OPUS re-read: the fifth argument of the two 00830540 calls is r15d / r12d, the 0082F360 results or -1 (0082F182, 0082F195)
- `008113D0`: OPUS re-read: the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)
- `00811470`: OPUS re-read: the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)
- `00811530`: OPUS re-read: the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)
- `00811640`: OPUS re-read: the upvalue case loads v = [[rcx+0x20]], tests dword [v+8] against 0x16, then indexes from qword [v] and bounds by byte +0xA of [v] (one dereference more than the row said)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 44 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 4), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
