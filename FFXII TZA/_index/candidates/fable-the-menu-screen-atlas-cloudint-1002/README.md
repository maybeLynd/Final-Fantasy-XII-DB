# Interior citations, cloud-drafted: the-menu-screen-atlas.md's entry-cited functions (FABLE, 2026-10-02)

The page named 13 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01GAVL9pjWiJ4RaEZv212gfL, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 13 staged with 62 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `00556DB0`: 002D45C0 gets qword +0x18 of the first child (reloaded from +0xC0), not the child; 'its' fields are that object's
- `00560210`: omitted the first==third rewrite at 005602BC (c := b, b := a) that precedes the signed ordering; named the bytes and the 002F9860 argument per child
- `0056FEF0`: the descriptor holds movsxd of dword +0xD8, not the qword tested for null
- `0057F6B0`: 'ebx' is the incoming rcx (mov rbx, rcx); 'sends' characterised the callee - now states only the call
- `00556DB0`: neighbour gate: the stub whose address the `lea` at `00556DB0` + 0xA0 loads (6 bytes, `mov eax, 1; ret`, an Input-layer hub) is named by role on the page
- `00558CE0`: neighbour gate: the callee at `00558CE0` + 0x115 (null for a null p, p when it starts with a non-empty string, else the n-th NUL-terminated string after a 2-byte zero header; ActorEntity layer) is named by role on the page
- `00560210`: neighbour gate: the same n-th-string lookup, called at `00560210` + 0x52, is named by role on the page

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
