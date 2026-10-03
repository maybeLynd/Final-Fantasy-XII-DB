# Interior citations, cloud-drafted: the-lua-loader-and-what-it-accepts.md's entry-cited functions (OPUS, 2026-10-03)

The page named 11 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 10 applied with 50 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**OPUS corrections on re-read.**

- `00810470`: byte re-read by a non-drafting agent: Unbounded/edge loop: the copy loop counts edi (the 32-bit n) down with sub/jne at 00810518, and the start index uses the sign-extended n, so the draft's 'for k = n-1 down to 0' holds only for positive n; a negative n raises qword [rcx+0x10] by 16 times its magnitude and runs 2^32 + n passes. Everything else verified: n = 0 path stores rdx/tag 0x16 and advances; 0081A8A0 gated by jle on qword [qword [rcx+0x18]+0x18] (signed); 0081ECA0(rcx, n); qword [c+0x18] = rdx; slot k (top re-read) copied to c+0x20+16k; final tag 0x66.
- `0081EFB0`: byte re-read by a non-drafting agent: Read-once vs re-read: the dword [qword [rcx+0x18] + 0x50] stored at dword [s+0xC] is loaded into ebx at 0081EFFC, before the 0081A620 call that receives rcx; the draft orders it after that call. Rest verified: ja 0x28 tail-jump to 0081EDC0 with registers unchanged, cmp r8+1 with -0x23 (= 0xFFFFFFFFFFFFFFDD) ja to the final call 00823710, 0081A620(rcx, 0x14, r8 + 0x21, 0, 5th dword 0), 00861EBA = IAT memcpy, zero byte at s+0x20+r8.
- `0082A7C0`: byte re-read by a non-drafting agent: Re-read wording: after a 0081EEF0 match the body re-reads both qword [rcx+0x50] (rbx at 0082A824) and qword [rcx+0x30] (r10 at 0082A82D); the draft marks only e as re-read, so the f used in the message and as 0082FDE0's first argument reads as the value cached on entry. Also the local-index word is read with movsx (signed). Rest verified: i = movsx word [qword [f+0x20]+0xA], jge/jl signed against dword [d+0x18] re-read (d itself cached in r14), jb unsigned byte compare, message argument chain, dword [rcx+0x10] = 0 then 00824330 as the last instruction, entry shift loop and count decrement, the removal path jumps back to the compare without inc esi (same 

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 10 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
