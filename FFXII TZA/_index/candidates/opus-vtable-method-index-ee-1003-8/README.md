# Interior citations, cloud-drafted: vtable-method-index.md's entry-cited functions (OPUS, 2026-10-03)

The page named 13 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 13 applied with 65 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 47.

**OPUS corrections on re-read.**

- `007A1790`: byte re-read by a non-drafting agent: The body multiplies all three stored values by 0xFF in both branches (imul ecx, eax, 0xff / imul ecx, edx, 0xff / imul [S+8], 0xff, and imul of S+0/S+4/S+8), but 'stores P.x, P.y and dword S+8 times 0xFF' reads as if only S+8 is scaled; reworded to 'each of ... times 0xFF' (32-bit products). Everything else checked: IAT slots resolve to USER32 GetCursorPos/GetWindowRect/GetClientRect/GetWindowInfo/ScreenToClient; signed bounds (js/jge); bit 0x80 of S+0xC/S+0xE/S+0xD; non-zero-only update; [o] = 1 inside / 0 outside; slot +0x38 retry loop on 0x8007001E; end step. The stack-cookie clause was dropped to stay within the length limit.
- `007E96A0`: byte re-read by a non-drafting agent: Two precision defects. (1) Read order: word [f+6] is read into edi BEFORE a's slot +0x28 call (007E9720) and that pre-call value is compared; only the 007B2200 argument re-reads it. (2) 'newlines/terminators added' hides an unchecked store: after each 0019C5D0 the body writes 0xA at index k = result (minus 2 when result >= 0xFF, signed jl) with no bound check, then checks k+1 < 0x100 (unsigned) before the 0 terminator and calls 00809728 otherwise, so a negative or large result writes the newline outside the 0x100-byte buffer. The second message (01CB91B0) takes no format arguments and does not call 007E8B40 again. Rest checked: 7-argument format order ma
- `00834970`: byte re-read by a non-drafting agent: '(a+2) mod 3' hides the signed arithmetic: the index is computed with imul 0x55555556, shr 31, add (signed division truncating toward zero) and a subtraction, i.e. the C remainder (a+2) % 3 on a 32-bit signed value, negative when a+2 < 0. Everything else checked: a re-read for h on each pass; h negated with the xorps sign mask 01CEBDA0; slot +0x50 called on rcx twice per j; c = v.k*[rcx+0x20+4k]*r + offset - v.k*m with fourth float 0; dot against the best (reset to -1e18 per j, second pass compares against the updated best); jbe skips NaN; store at r8+16j; signed j loop (jle).
- `008585E0`: byte re-read by a non-drafting agent: Ruled on the CORRECTED text from vtable-method-index-r8h-fix.json. Its new clause holds: the copy loop (008586E0..00858707) stores qword i into C's data for i below the re-called slot +0xB8 result (signed jl) with no compare against n (and C's data is null when n <= 0). One defect remains: the byte passed as 00854830's second argument is movzx edx, byte [rbp+0x67] = entry rsp+8, the incoming rcx home slot, which this body never writes (only +0x10/+0x18/+0x20 are saved there); 'a stack byte' hides that it is an unwritten caller-area byte. Everything else checked: n movsxd dword +0x104, js/jle paths (count = n even when negative), 0085E680(8n, 0x10), null-

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 13 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
