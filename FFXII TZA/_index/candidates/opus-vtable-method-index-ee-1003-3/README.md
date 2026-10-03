# Interior citations, cloud-drafted: vtable-method-index.md's entry-cited functions (OPUS, 2026-10-03)

The page named 60 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 60 applied with 293 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 210.

**OPUS corrections on re-read.**

- `00637650`: byte re-read by a non-drafting agent: Every store holds (guard 02CF950C with jg/epoch, 00D311B0 at +0, 01F2E5A8 at +8/+0x10/+0x18, dword +0x20 = 0, qword +0x28 = 0, 00D58BF0 "PUInt32" at +0x30, dwords +0x38/+0x3C = 4, qwords +0x40/+0x48 = 0, 00808B90(rcx=008AFE50), footer on the guard). Precision: "pointing at itself" is true only of the +8 cell; +0x10 and +0x18 hold the address of +8, not their own.
- `00725760`: byte re-read by a non-drafting agent: Calls, offsets and bits hold (bt edx,0x1C = bit 0x10000000; unsigned count [t+0x128]; qwords [t+8*i+0x130] with null skip; and ebp,3; [t+0x170] null test; [rsp+0x80] = fifth argument; xmm3 kept in xmm6). Representation fix: slot +0x190 receives r8 = rsp+0x30, the address of the stack copy, not the value.
- `007258C0`: byte re-read by a non-drafting agent: Bytes hold, but "zero-fills ... with 00861EC0" states the callee's purpose; the body calls 00861EC0(buffer, 0, 0x80) and 00861EC0(buffer, 0, 0x100). Reworded to the calls.
- `00789C00`: byte re-read by a non-drafting agent: Loop verified (k = r8d from 1 while k < length: data[k] = byte [rdx + length - k], length re-read after each store; slot +0x20 of [rcx+0xE0] with the data qword; 00715C70(&stack string); returns the slot result). Defect: "(data byte 0 keeps the first byte of rdx)" is a claim about what 007157A0 does, which this body does not show.
- `007D98F0`: byte re-read by a non-drafting agent: Ramp and mode logic hold, no jp (ucomiss/jne, so 0.0 or NaN takes +0x24); 01CEBDA0 is the sign mask 0x80000000 x4; 00861FAA is a jmp [008C2CA0] thunk, import api-ms-win-crt-math expf; 01CEBC78 = 6.2831855, 01CEBC50 = 3.1415927 (.rdata). Defect: 01F41D20 lies in .data (0x01DF0000+) and is written at run time (retool refs: a store in 007D9530), so 2.083333e-05 is only its image value.
- `007F1EC0`: byte re-read by a non-drafting agent: Copies and arithmetic hold: 00D11570 = (1,1,1,0), 00D560A0 = 3.0 x4, 00D22600 = 0.5 x4; s = sum of squares under that mask (haddps twice), r = rsqrtps(s), factor 0.5 r (3 - s r r), each lane times the factor, then lane 3 replaced by the original float +0x10C. Defect: the draft's "x" in "0.5 r (3 - x r r)" is undefined and reads as the x component; it is the masked squared length.
- `00833A60`: byte re-read by a non-drafting agent: Arithmetic holds (scales +0x20/+0x24/+0x28, w = 0, 16-byte records at qword [rcx+0x90]). Precision: the index is the cdq/idiv remainder, which is negative for a negative edx, so "mod" needs to say it is the signed remainder.
- `00848270`: byte re-read by a non-drafting agent: Hash, mask, bucket bound, chain arrays and record stride hold. Precision: the match is order-sensitive (record qword +0 must carry the smaller id, qword +8 the larger, at 008482FE / 00848308), which "whose two object pointers carry the two ids" does not say.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 60 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
