# Interior citations, cloud-drafted: heading-speed-to-position-delta.md's entry-cited functions (FABLE, 2026-10-02)

The page named 4 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01DvkUokim1xrVUS78Zq26tk, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 3 staged with 15 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**FABLE corrections on re-read.**

- `0022DE60`: the id tests are signed word compares (`0022DF05` jge against 0x5000, `0022DF0F` jl against 0x4000, `0022E05E` movsx), so ids 0x8000-0xFFFF take the lower-id path with a negative index; the text gave no signedness; the vertex stride is 16 (`0022E171` shl 4); the callee at `0022E1BE`, new to the page, is now cited by its site +0x35E
- `00232760`: content verified (`00232790` js on the movsx word +0x52, ecx still 0 at `002327A2`, `002327AB`/`002327AE` pass the saved rcx and rdx); the first callee, new to the page, is now cited by its site +0x10 (`00232770`)
- `00380FA0`: content verified (`00380FEA` je for kind 0, `00380FEF` je for kind 1, `00380FF4` jne after sub 1 for kind 2, `0038103C` je on a zero result); the kind-0 callee, new to the page, is now cited by its site +0x95 (`00381035`)

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
