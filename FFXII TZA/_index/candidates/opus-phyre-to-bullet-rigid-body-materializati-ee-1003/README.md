# Interior citations, cloud-drafted: phyre-to-bullet-rigid-body-materialization.md's entry-cited functions (OPUS, 2026-10-03)

The page named 6 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 6 applied with 30 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 6.

**OPUS corrections on re-read.**

- `00832590`: byte re-read by a non-drafting agent: Two defects. (1) Read-once vs re-read: the 64 bytes at rdx are loaded into xmm6-xmm9 at 008325B3-008325CD, before c's slot +0x50 and slot +8 calls (slot +8 receives rdx), and those registers are what 008327B7-008327C6 store; the draft's 'the 64 bytes at rdx' reads as a load at append time. (2) Growth path omits two writes: 00832785 stores the new block as data qword +0x28 and 00832795 stores the new size as capacity dword +0x20. Also the count passed to 008410B0 is movsxd (sign-extended). Rest verified: comiss/jbe min-max (NaN skips), copy of bytes +0..+0x57 with null-slot skip, 0085E710 when non-null and owner byte set, null-slot test at 008327B5.
- `008382D0`: byte re-read by a non-drafting agent: Argument provenance: when c is null, 0083837F stores rax as returned by 00847E60 (the jmp at 0083837A skips the reload), so qword +0x88 is 00847E60's return value, or 0 when the 0x80-byte block is null; it is not the block itself as the draft reads. Same for +0xA0 (00849B30's return value, second argument qword +0xA8 re-read). The null-test claims are confirmed (byte [rax+0xDD] at 00838421 runs with rax = 0 when the block is null; qword [h] at 00838592) and also apply to the k-loop and entry n-1 word stores through h, and n wraps to 0 when m is 0xFFFF (n-1 then indexes entry -1). Rest verified: stack args at rsp0+0x28/0x30/0x38/0x40, 0x28-byte q layout, 

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 6 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
