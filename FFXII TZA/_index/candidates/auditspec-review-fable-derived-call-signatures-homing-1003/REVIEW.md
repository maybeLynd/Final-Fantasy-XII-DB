# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-derived-call-signatures-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-DERIVED-CALL-SIGNATURES-HOMING-1003` · Package: `_index/candidates/fable-derived-call-signatures-homing-1003/` · Page: `00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 370, and the sentence is on the page verbatim.
- **rows.json.** 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** The row was read clause by clause against `disr.py` output of the certified image.
  - `00511660`: `mov rdi, r9`, then `call 00280120` at +0x09. That call gets the incoming `rcx`, `rdx`, `r8` and `r9` unchanged.
  - `test eax, eax` / `jne` returns that value.
  - Otherwise there are pops at +0x1A (a, kept in `ebx`) and +0x24 (b), each with `rcx` = the saved `r9`.
  - Then `002D6640(ecx = b, edx = a)`, whose result is returned.
  - Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
