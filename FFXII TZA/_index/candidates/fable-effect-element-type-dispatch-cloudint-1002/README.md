# Interior citations, cloud-drafted: effect-element-type-dispatch.md's entry-cited functions (FABLE, 2026-10-02)

The page named 56 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01Tuxsu5PvhCRfeUeyC5pKSu, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 50 staged with 229 anchors. Rejected by the mechanical check: 0. Skipped by the session: 6. Missing: 0.

**FABLE corrections on re-read.**

- `001DB340`: slot test read as (qword rcx+0x20) + quotient*8; it tests the qword at rcx+0x20+quotient*8 ([rbx+rax*8+8], rbx=rcx+0x18)
- `0024B1C0`: 02091150 is the array itself (lea), not a qword holding its base
- `003A7CB0`: the slot table base is loaded through two qwords (qword [qword 02EBEFA0]), not one
- `003A9510`: the slot table base is loaded through two qwords (qword [qword 02EBEF90]), not one
- `003A98D0`: the slot table base is loaded through two qwords (qword [qword 02EBEF78]), not one
- `0043E9C0`: arguments are not all unchanged (r8/r9 hold the jump target and image base) and in-range types also return: the offset table's tenth arm is the ret at 0043EA18, taken by 89 of the 98 in-range types (tables read from the image)
- `00455560`: E index read as a sum of two dwords; it is the dword at D+0x2A0 indexed by dword rcx+0x298; `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `004559C0`: E index read as a sum of two dwords; it is the dword at D+0x2A0 indexed by dword rcx+0x298; `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `0045A220`: E index read as a sum of two dwords; it is the dword at D+0x2B0 indexed by dword rcx+0x298; `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `0045A6A0`: `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `0045AEF0`: E index read as a sum of two dwords; it is the dword at D+0x2A0 indexed by dword rcx+0x298; `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `0045B2B0`: E index read as a sum of two dwords; it is the dword at D+0x2A0 indexed by dword rcx+0x298; `s` on the 00399600 path is dword +4 of the buffer passed to it, not that call's return (which only gates an early return)
- `00463FF0`: order: 00377190 is called before bit 1 of +0x248 is set (00464024 call, 00464029 or)
- `004FF270`: r8 is clobbered (byte +0xC2 minus the case steps) before every arm, so not all incoming arguments are passed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
