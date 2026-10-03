# Interior citations, cloud-drafted: the-vp8-codec-interface-and-its-control-map.md's entry-cited functions (OPUS, 2026-10-03)

The page named 8 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py`. A second local agent, not the drafter, then read every one of the 5 rows against the disassembly: 3 stood, 2 were corrected (wording and path coverage only; no value, callee or anchor changed). Both corrected rows (`0016F080`, `0016F2A0`) were re-read at the bytes by the non-author review (auditspec-review-opus-the-vp8-codec-interface-and-its-control--ee-1003-2); OPUS's `00713210` spot-check belongs to the MSVC ordered-container package, not to this page. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 5 applied with 25 anchors. Rejected by the mechanical check: 0. Skipped by the session: 3. Missing: 0.

**Corrections from the byte re-read.**

- `0016F080`: byte re-read (non-drafting agent, OPUS spot-checked): 'whose results end only in a discarded register' is inaccurate: xgetbv (XCR0 AND 6 = 6) and leaf 7 (bit 0x20 of its ebx, run only when the maximum leaf is at least 7) set bits 0x40 and 0x80 of the feature word r8d, which is not discarded but masked by and r8d, 0x10 at 0016F140. Callee lists, globals, the ecx bit 0x200 test and anchors check out.
- `0016F2A0`: byte re-read (non-drafting agent, OPUS spot-checked): The wait path is a check-first loop: with eax = ebx = 2 it does lock cmpxchg before any Sleep and skips Sleep entirely when the dword already reads 2 (0016F409/0016F411); 'calls Sleep(0) until it reads 2' implies at least one Sleep. IAT names (malloc 008C2B40, free 008C2B48, Sleep 008C21B0) and the thunks (00861EC0 -> memset, 00861EF6 -> __intrinsic_setjmp) are confirmed from the import table; all offsets, values and anchors check out.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 5 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
