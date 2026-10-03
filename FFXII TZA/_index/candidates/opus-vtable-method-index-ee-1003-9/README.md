# Interior citations, cloud-drafted: vtable-method-index.md's entry-cited functions (OPUS, 2026-10-03)

The page named 13 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 11 applied with 55 anchors. Rejected by the mechanical check: 1. Skipped by the session: 1. Missing: 48.

**OPUS corrections on re-read.**

- `0062E5A0`: byte re-read by a non-drafting agent: The wrap loops are described as leaving for every finite value ('an infinity never leaves them'), but the loop exit needs the add to change the value: in float32, adding 2 pi (01CEBC78) or -2 pi (00915624) to any value of magnitude above 2^27 (134217728; verified with numpy float32) rounds back to the same value, so those finite values never leave the loops either, like the infinities. The loop shapes themselves check out (comiss 0,p / ja back-edge; comiss p,2pi / ja back-edge; unordered skips both). Everything else checked: initial M rows from the 3x4, f normalised with sqrtf (stub 00861F14), p = asinf(f.y) - xmm2, y = atan2f(f.x, f.z) + xmm1 (stubs 008
- `00846C20`: byte re-read by a non-drafting agent: The growth path also stores the new capacity (00846F1A mov dword [rbx+8], edi), which the row leaves out while listing the other growth writes; added. Everything else checked: min/max start vectors 01CCD870/01CCD880 (the point-0 compares use the scalar 1e18/-1e18 constants and 0 for w, the same values); comiss + jbe skips unordered, so a NaN changes neither; node = min, max, -1, r8d, r9d at +0..+0x28, and the 20 bytes +0x2C..+0x3F are copied from rbp+3..rbp+0x16, which this body never writes; growth test count == capacity and capacity < (2*count or 1) signed; 0085E680(64n, 0x10), copy loop with null-address skip, 0085E710 on owned non-null old data, owne
- `00846F70`: byte re-read by a non-drafting agent: The growth path also stores the new capacity (0084725A mov dword [rbx+8], edi), which the row leaves out while listing the other growth writes; added. Everything else checked: min/max start at 01CCE8AC (1e18) / 01CCD4E4 (-1e18), comiss + jbe skips NaN; the widening applies when 009002B0 (0.002) > max - min (NaN skips) with 009002EC (-0.001) / 008C5B2C (0.001); q = qword [rcx+0x10]; words = cvttss2si of (v - [q+0x10+4j]) * [q+0x30+4j] AND 0xFFFE for min, + 1.0 then OR 1 for max; dword +0xC = (r8d << 21) OR r9d; growth test, 0085E680(16n, 0x10), copy with null skip, 0085E710, owner byte 1, null-address store skip, count increment.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 11 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
