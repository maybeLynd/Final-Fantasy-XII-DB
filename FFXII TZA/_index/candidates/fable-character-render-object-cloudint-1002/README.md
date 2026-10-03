# Interior citations, cloud-drafted: character-render-object.md's entry-cited functions (FABLE, 2026-10-02)

The page named 6 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_013aUyF9Cw8dmXC6Vyt6UA4p, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 6 staged with 23 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `001BD840`: `001BD8C2` is an indirect call through slot +0x10 of the qword at node+0x10 with rcx = node+0x10, so 'allocates' named a purpose the listing does not show; the 16-byte store is skipped when the result plus 0x10 is zero (`001BD8C9` add, `001BD8CD` je), a path the text missed; the stored pair's upper dword is unwritten stack (`001BD890` writes only a dword); the two callees new to the page are now cited by their sites (+0x6B at `001BD8AB`, +0xEF at `001BD92F`)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
