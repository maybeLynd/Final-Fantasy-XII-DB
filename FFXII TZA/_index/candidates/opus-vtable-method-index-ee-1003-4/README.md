# Interior citations, cloud-drafted: vtable-method-index.md's entry-cited functions (OPUS, 2026-10-03)

The page named 47 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 47 applied with 233 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 223.

**OPUS corrections on re-read.**

- `00719460`: byte re-read by a non-drafting agent: Every call and operand holds (null r8 or zero low-32 strlen -> 00715A00(rdx, rcx); 007158B0(rsp+0x30, [rcx+8], dword [rcx]+len, -1); 00861EBA(temp data + dword [rcx], r8, len); 00715A00(rdx, &temp); 006DA8A0([01F3BA68], data-8) unless data == 02EA1720 or null; returns rdx). 00861EBA is a jmp [008C2A68] thunk = VCRUNTIME140!memcpy. Defects: the opening "returns in the string object rdx the string rcx with the C string r8 appended" and "the shared empty buffer" state purposes this body does not show (they depend on 00715A00 / 007158B0). Reworded to the calls.
- `007D8E40`: byte re-read by a non-drafting agent: Jump table decoded: 00120000 + 0x6B8F44 = 007D8F44 -> 007D8E79, 007D8EA8, 007D8ECA, 007D8EDD, 007D8EF3, 007D8F04, 007D8F18, 007D8F24 for 0x100..0x107, matching the stated key-to-record order; 01CB7780 = 0.11512925, 008C5B2C = 0.001; 0x106/0x107 cvttss2si stores then own +0x40. Precision: the body computes expf(value * 0.1151293) (mulss before the call at 007D8E79/007D8E81); "expf of the value times 01CB7780" also reads as expf(value) * k.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 47 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
