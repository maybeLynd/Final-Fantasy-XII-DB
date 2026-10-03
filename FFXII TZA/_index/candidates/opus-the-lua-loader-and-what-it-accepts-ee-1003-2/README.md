# Interior citations, cloud-drafted: the-lua-loader-and-what-it-accepts.md's entry-cited functions (OPUS, 2026-10-03)

The page named 11 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter-r4, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 11 applied with 55 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `0082B9A0`: byte re-read by a non-drafting agent: 'the 16-byte variable entry it indexes' is not what the bytes do: the entry index is the signed word at position byte `+0x42` plus dword `rcx+0x3C` of the word array that is the first qword of the lexer's `+0x50` record (`0082BA73`..`0082BA88`), and the 16-byte entries are in the array at qword `+0x30` of `[rcx]` (`0082BA8D`..`0082BA9A`).
- `0082BB40`: byte re-read by a non-drafting agent: 'the 16-byte variable entry selected by the new count minus 1' / 'selected by the stack record's dword `+4`' hide an indirection: the position is dword `+0x3C` of the function record plus that value, it indexes a signed-word array (first qword of the `+0x50` record of the function record's `+0x18` object), and that word numbers the 16-byte entry in the array at qword `+0x30` of the function record's first qword (`0082BB8E`..`0082BBC1`, `0082BBD5`..`0082BC01`).
- `0082C6E0`: byte re-read by a non-drafting agent: 'the record's line dword' is not on the function record: it is dword `+0x68` of the function record's first-qword object (`0082C72A mov rax, qword ptr [rsi]`, `0082C72D mov r8d, dword ptr [rax + 0x68]`).

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 11 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
