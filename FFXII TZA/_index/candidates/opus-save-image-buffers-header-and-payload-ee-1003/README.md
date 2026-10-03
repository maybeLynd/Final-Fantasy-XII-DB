# Interior citations, cloud-drafted: save-image-buffers-header-and-payload.md's entry-cited functions (OPUS, 2026-10-03)

The page named 3 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter-r4, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 3 applied with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `007BA7E0`: byte re-read by a non-drafting agent: 'caches 27 plus byte `+0x1A` as header length (0 if not that many remain)' is wrong: when fewer than 27 + byte `+0x1A` bytes remain it RETURNS 0 (`007BA84C jl 0x7ba885`) and caches nothing; the header length is stored to `+0x18` only after the segment-table sum (`007BA877`).; Calling `+8` a 'flag dword' is a purpose claim; the bytes only test its bit `0x80000000` (`007BA7FF`).
- `0087AF40`: byte re-read by a non-drafting agent: 'returns that result' after `0087C6C0` reads as the `0087C6C0` result; the function returns the saved `0087BD60` result (`esi`, `0087B00D cmp esi, 1` / `cmove esi, r15d`) with 1 mapped to 0, ignoring `0087C6C0`'s return.; The input pointer `r8` and output pointer `rcx` are stored into the record AFTER `0087C9F0` returns (`0087AF9D`, `0087AFB0`); only the qwords `+0x30`/`+0x38`/`+0x40` are set before that call.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 3 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
