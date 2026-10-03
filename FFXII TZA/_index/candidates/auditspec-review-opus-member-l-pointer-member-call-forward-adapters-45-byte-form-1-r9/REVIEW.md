# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-l-pointer-member-call-forward-adapters-45-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-L-POINTER-MEMBER-CALL-FORWARD-9FED3` · Package: `_index/candidates/opus-member-l-pointer-member-call-forward-adapters-45-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 6 member rows of the 45-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 6 functions, 30 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `005A0BD0`** (13 instructions over its `functions.tsv` extent), clause by clause:
  - prologue saves `rbx`/`rdi`; `mov rbx, r8` and `mov rdi, rdx` copy two arguments into callee-saved registers without writing `rcx`, `rdx` or `r8`, so `call 0x5a02d0` receives all three as received.
  - after the call: `mov r8, rax` (return value into `r8`), `mov rdx, rbx` (received `r8`), `mov rcx, rdi` (received `rdx`).
  - epilogue restores `rbx`/`rdi`, then `jmp 0x684080`; the body is 45 bytes (`005A0BD0`..`005A0BFC`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 5 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 45 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the `call` target (C) and the tail `jmp` target (J).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 6, bad 0`. Per-row decoded fields:
  - `005A0BD0 OK  C=5A02D0 J=684080`
  - `00627050 OK  C=613800 J=684080`
  - `00627080 OK  C=613A30 J=684080`
  - `006270B0 OK  C=613E80 J=684080`
  - `006270E0 OK  C=6143B0 J=684080`
  - `00627110 OK  C=614640 J=684080`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`00614640 -> 00614641`). The checker flagged it: `00627110 BAD C: sentence 00614641 body 614640`, and the package summary became `rows checked 6, bad 1 (rep 005A0BD0, 13 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
