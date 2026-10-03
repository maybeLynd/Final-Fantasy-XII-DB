# Interior citations, cloud-drafted: sound-trigger.md's entry-cited functions (OPUS, 2026-10-03)

The page named 3 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `007AE260`: byte re-read by a non-drafting agent: NaN wording on the step-back: comiss x, key i followed by jae means an unordered compare (a NaN key, which is exactly where the search stops on the ucomiss/je path) also steps i back, not only 'x below key i'. The index after the search is the last probed mid, and on the no-step path an index of n or more is clamped to n - 1 by cmovge. Rest verified: null t or n = 0 returns 0.0; comiss/jae then minss clamps x to [0, 1.0] (NaN gives 0); 16-byte points at t + word [t+2]; mid via cdq/sub/sar (signed, toward zero); ucomiss + je stops on equal or unordered; 007A9E50(ratio, edx = curve byte); byte [t+6] = 1 uses comiss/ja (NaN returns 0.0), powf thunk 00861F6E
- `007B5580`: byte re-read by a non-drafting agent: Unbounded stack-buffer store: the newline is written at byte [rsp+0x20+len] with len sign-extended and no range test (007B55C7); only the terminator index len + 1 is compared (unsigned) against 0x100 before 00809728. A negative or over-long returned length (0x102 or more) therefore writes outside the 0x100-byte buffer. The 0xFF compare is signed (jl). Rest verified: OutputDebugStringA is the IAT slot 008C2120; 007A5570(2, buffer); free-list pop and tail append with qword [rcx+0x28] re-read; bit 0x1 of dword [n+0x1C]; r8 at [n+0x20]; inc dword [rcx+0xC]; dword [n+0x18] to [rdx] when non-null; returns 0 / -1 with cookie check.
- `007E2EB0`: byte re-read by a non-drafting agent: Re-read after a match: on a match the body returns qword [rcx+0xB0+8i] read again from the array at 007E2F34, after the Enter/LeaveCriticalSection calls, not the o it locked and compared. Also o is used without a null test. Rest verified: count byte [rcx+0x94] tested unsigned first (jbe), re-read with movzx each step; EnterCriticalSection (008C20B8) / LeaveCriticalSection (008C20C0) on o+8 around the qword [o+0x98] read; compare with rdx; 0 when no entry matches.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
