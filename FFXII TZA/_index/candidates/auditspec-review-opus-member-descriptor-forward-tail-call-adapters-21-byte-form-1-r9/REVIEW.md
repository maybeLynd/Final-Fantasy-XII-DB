# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-descriptor-forward-tail-call-adapters-21-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-DESCRIPTOR-FORWARD-TAIL-CALL-A-611E7` · Package: `_index/candidates/opus-member-descriptor-forward-tail-call-adapters-21-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 4 member rows of the 21-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 4 functions, 16 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `00584850`** (5 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rax, r8` / `mov rcx, rdx` / `mov rdx, rax` swap the incoming `rdx` into `rcx` and the incoming `r8` into `rdx` (through `rax`, so neither is lost).
  - `lea r8, [rip + 0x2725740]` resolves to `02CA9FA0` (next instruction `00584860` + 0x2725740), the third argument named by the sentence.
  - `jmp 0x684080` is the tail-jump to `00684080`; the body ends there at 21 bytes (`00584850`..`00584864`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 3 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 21 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the `lea r8` rip target (L) and the `jmp` target (J).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 4, bad 0`. Per-row decoded fields:
  - `00584850 OK  J=684080 L=2CA9FA0`
  - `00584AB0 OK  J=684080 L=2CA9DA0`
  - `00584FC0 OK  J=684080 L=2CA9EA0`
  - `00674DD0 OK  J=684080 L=2D3E780`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`00684080 -> 00684081`). The checker flagged it: `00674DD0 BAD J: sentence 00684081 body 684080`, and the package summary became `rows checked 4, bad 1 (rep 00584850, 5 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
