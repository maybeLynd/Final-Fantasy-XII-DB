# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-r-member-call-result-dispatch-adapters-78-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-R-MEMBER-CALL-RESULT-DISPATCH-65B6D` · Package: `_index/candidates/opus-member-r-member-call-result-dispatch-adapters-78-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 6 member rows of the 78-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 6 functions, 30 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `005A0B80`** (22 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rdi, qword ptr [r8]` reads `p` first, `mov rbx, rdx` keeps `c`; `call 0x5a02d0` receives `rcx`, `rdx`, `r8` as received.
  - after the call `mov rcx, rbx`; `test rdi, rdi` / `je`; non-null path `mov r8, rax` (the return value), `mov rdx, rdi` (p), `jmp 0x684080` = (c, p, the return value).
  - null path (`005A0BB2`): `mov edx, 1`, `call 0x80f420` with `rcx` = `c`, `mov rcx, rbx`, `jmp 0x810620`; the body is 78 bytes (`005A0B80`..`005A0BCD`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 5 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 78 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the first `call` target (C), the non-null `jmp` target (J), the `mov edx` immediate (E), the second `call` target (F) and the null-path `jmp` target (T).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 6, bad 0`. Per-row decoded fields:
  - `005A0B80 OK  C=5A02D0 E=1 F=80F420 J=684080 T=810620`
  - `00626DC0 OK  C=613800 E=1 F=80F420 J=684080 T=810620`
  - `00626E10 OK  C=613A30 E=1 F=80F420 J=684080 T=810620`
  - `00626E60 OK  C=613E80 E=1 F=80F420 J=684080 T=810620`
  - `00626EB0 OK  C=6143B0 E=1 F=80F420 J=684080 T=810620`
  - `00626F00 OK  C=614640 E=1 F=80F420 J=684080 T=810620`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`00614640 -> 00614641`). The checker flagged it: `00626F00 BAD C: sentence 00614641 body 614640`, and the package summary became `rows checked 6, bad 1 (rep 005A0B80, 22 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
