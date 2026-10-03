# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-sab-sound-bank-container-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SAB-SOUND-BANK-CONTAINER-CLOUDINT-1002` · Package: `_index/candidates/opus-sab-sound-bank-container-cloudint-1002/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 1 rows, 5 anchors; rejected 0, missing 0.
- Semantic pass: **all 1 rows** (the request asks for at least 15) read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The tree walk, key K = `r9d + r8d*2`, lower-bound descent, insert-when-absent-or-greater and the `+0x28` store are exact; one argument clause is not. See below.
- Limits hold: body statements only, static evidence; a cloud draft plus OPUS's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

**Defect (row `001FB770`).** The row says the call to `001FB470` passes "the low byte of the fifth (stack) argument" and passes "that node". The prologue is `40 53` (`push rbx`) and `48 83 EC 40` (`sub rsp,0x40`), a 0x48-byte frame. So `movzx eax, byte ptr [rsp+0x60]` at `001FB7BD` (bytes `0F B6 44 24 60`) reads entry `rsp+0x18`, which is the **r8 home slot**, not the fifth-argument slot at entry+0x28. Nothing in the function writes that slot, which is the MSVC pattern for passing an empty tag struct by value. The third argument is `lea r8,[rsp+0x50]`, the **address of a stack slot holding the node** (`mov [rsp+0x50],rax` at `001FB7B3`), not the node itself. **Repair:** replace "that node, the stack pair (K, 0), the low byte of the fifth (stack) argument" with "the address of a stack slot holding that node, the address of the stack pair (K, 0), and a byte read from this function's unwritten r8 home slot (an empty-tag argument)". Then re-run `interior_applier.py`. The producer repairs its own row.
