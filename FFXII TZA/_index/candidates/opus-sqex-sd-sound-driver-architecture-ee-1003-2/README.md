# Interior citations, cloud-drafted: sqex-sd-sound-driver-architecture.md's entry-cited functions (OPUS, 2026-10-03)

The page named 6 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py`. A second local agent, not the drafter, then read every one of the 3 rows against the disassembly: 0 stood, 3 were corrected (wording and path coverage only; no value, callee or anchor changed). OPUS spot-checked the corrections at the bytes before applying (the bullets below name what each re-read found). Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 3. Missing: 5.

**Corrections from the byte re-read.**

- `007AAC80`: byte re-read (non-drafting agent, OPUS spot-checked): Final branch condition incomplete: the dur store is skipped only by comiss xmm7, d / jae (xmm1 at least d); an unordered compare (d NaN, e.g. 0/0 with a zero rate) also stores d. The sentence says only 'when xmm1 is below d', while it spells out the unordered rule for the first compare. (The 'xmm0 above v' test uses comiss/jbe, so unordered correctly falls to the else arm.) All record offsets, stores, 007A9E50 arguments, the 0.0 test and the anchors check out.
- `007AAD90`: byte re-read (non-drafting agent, OPUS spot-checked): Final branch condition incomplete: the dur store is skipped only by comiss xmm7, d / jae (xmm1 at least d); an unordered compare (d NaN, e.g. 0/0 with a zero rate) also stores d. The sentence says only 'when xmm1 is below d', while it spells out the unordered rule for the first compare. (The 'xmm0 above v' test uses comiss/jbe, so unordered correctly falls to the else arm.) All record offsets, stores, 007A9E50 arguments, the 0.0 test and the anchors check out.
- `007E0A40`: byte re-read (non-drafting agent, OPUS spot-checked): The divisibility test is an unsigned 64-bit div of r8 by the sign-extended 32-bit signed product (movsxd rcx, eax / div rcx); 'not a multiple of' misstates a negative product, and the path where the product is 0 (div faults) is not covered.; Everything else checks out: the 0xFFFFFFFB test, n >= 2 signed, cvtdq2pd store to +0x98 only when n is 0, EnterCriticalSection/LeaveCriticalSection IAT slots 008C20B8/008C20C0 (confirmed from the import table), slot k = signed remainder of ([+0xB4] + re-read [+0xB0]) by 2 at rcx+0xC0+0x20k with rdx/r8/fifth dword/r9 at +0/+8/+0x10/+0x18, inc of dword +0xB0 inside the lock (before LeaveCriticalSection at 007E0B2C).

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
