# Interior citations, cloud-drafted: hchk-hctg-hdat-handbook-indexes.md's entry-cited functions (FABLE, 2026-10-02)

The page named 4 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01F7SYgmZJApKhfTARtFcaab, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 4 staged with 20 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `002C2280`: FABLE re-read: `002C22A2` jne skips only the `00244F50` call; the stack-cookie check call (+ 0x5A) runs on both paths
- `00574080`: FABLE re-read: `005740B2` sets EBP = 0 for a null RCX and `005740DC` then loads through it; the row had no null-RCX path
- `005766E0`: FABLE re-read: `005766F6` reads byte [rcx + 0xC9] before `005766FF` tests RCX

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
