# Interior citations, cloud-drafted: sead-win-config.md's entry-cited functions (OPUS, 2026-10-03)

The page named 47 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 47 applied with 235 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `00220E80, 00220F20, 00220FC0, 007ADBB0, 007ADCA0, 007ADD30, 007ADE80, 007ADF90, 007AE080, 007AE110, 007AE1D0`: OPUS re-read: family-sibling rows referred to an unnamed 'family base'; each sibling checked at the bytes to share the base's instruction form and rewritten as a self-contained sentence with its own values (fix_family_siblings.py)
- `00220DE0`: OPUS re-read: the final store is `sete` of the re-read byte (00220E5B..00220E65), not a constant 1
- `007AA110`: OPUS re-read: the build loop writes only those fields (007AA1C0..007AA1D2); dword +0x18 and qword +0x28 are not written
- `007B4A70`: OPUS re-read: the state-3 path jumps back to the loop test with rbx unchanged on failure (007B4B4E cmovns, 007B4BAA)
- `007B4A70`: OPUS re-read: r9 = rsp+0x40, which holds a copy of qword [s+0x10] (007B4BF4, 007B4C06, 007B4C3B)
- `007D85E0`: OPUS re-read: the record build writes only those fields (007D860D..007D86E4); dword +0x18 and qword +0x28 are not written
- `007D9530`: OPUS re-read: 007AED00 is called at 007D9584 and again at 007D95A4
- `007D99E0`: OPUS re-read: the record build writes only those fields (007D9A0A..007D9AAE); dword +0x18 and qword +0x28 are not written
- `007DA0A0`: OPUS re-read: the record build writes only those fields besides qword +0xC (007DA0DA..007DA10B); dword +0x18 and qword +0x28 are not written
- `007DAAB0`: OPUS re-read: the record build writes only those fields (007DAAE4..007DAB00); dwords +0x30 and +0x40 are not written
- `007DDED0`: OPUS re-read: 02EAE0C0 receives 007DD2B0's return (007DE0BB, 007DE0CA), not the block pointer directly
- `007E9E60`: OPUS re-read: rdx = rsp+0x50, which holds a copy of qword [s+0x10] (007E9EA2..007E9ECE)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 47 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 4), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
