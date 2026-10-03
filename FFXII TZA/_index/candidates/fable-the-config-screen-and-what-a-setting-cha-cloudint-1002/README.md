# Interior citations, cloud-drafted: the-config-screen-and-what-a-setting-change-runs.md's entry-cited functions (FABLE, 2026-10-02)

The page named 7 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_017oZMRE9rawUwYiuJTWnT1T, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 7 staged with 34 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `002726C0`: 'the difference of those two' read as +0x0 minus +0x4; `002726CD sub r8d, edx` makes d = (r8d<<4) - (edx<<4) = dword +0x4 minus dword +0x0, sign-extended at `002726D0`
- `002CD8A0`: row left the case-to-arm map undecoded; read the 10-dword case table that the load at `002CD8B5` indexes: 0->002CD8EB, 1->002CD8C1, 2->002CD8CD, 3->002CD8C7, 4->002CD8D9, 5->002CD8DF, 6->002CD8D3, 7,8->002CD8EB, 9->002CD8E5; FABLE on review: the table and image-base addresses removed from the text (a jump-table address is a text-gap citation, and an 8-hex image base reads as an address); the cases are described instead

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
