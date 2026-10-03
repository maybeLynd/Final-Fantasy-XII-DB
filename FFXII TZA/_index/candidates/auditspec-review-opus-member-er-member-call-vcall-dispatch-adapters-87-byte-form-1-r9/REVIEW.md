# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-er-member-call-vcall-dispatch-adapters-87-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ER-MEMBER-CALL-VCALL-DISPATCH-A1F0C` · Package: `_index/candidates/opus-member-er-member-call-vcall-dispatch-adapters-87-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 7 member rows of the 87-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 7 functions, 35 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `005C1C10`** (27 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rbx, rcx` keeps `f`, `mov rdi, rdx` keeps `c`, `mov rcx, rdx` / `call 0x5bcac0` computes `o` = `005BCAC0(c)`.
  - `test rax, rax` / `je 0x5c1c5c`: the null path only restores the frame and returns, with `rax` = 0 from the test, so it returns 0.
  - non-null: `mov rcx, rax` / `call qword ptr [rbx + 8]` (the pointer stored at f+8, called with `o`; a member pointer, not a vtable slot); `mov ebx, eax` keeps the low dword; `mov edx, 1` / `mov rcx, rdi` / `call 0x80f420`; `mov edx, ebx` / `mov rcx, rdi` / `call 0x810580`; `mov eax, 1` and return. The body is 87 bytes (`005C1C10`..`005C1C66`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 6 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 87 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the first `call` target (C), the indirect-call displacement (S), the `mov edx` immediate (E), the two later `call` targets (F, G) and the `mov eax` return immediate (R).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 7, bad 0`. Per-row decoded fields:
  - `005C1C10 OK  C=5BCAC0 E=1 F=80F420 G=810580 R=1 S=8`
  - `005C1DA0 OK  C=5BCD20 E=1 F=80F420 G=810580 R=1 S=8`
  - `0066FBF0 OK  C=66E7D0 E=1 F=80F420 G=810580 R=1 S=8`
  - `006A1110 OK  C=69D520 E=1 F=80F420 G=810580 R=1 S=8`
  - `006AF170 OK  C=6AEE00 E=1 F=80F420 G=810580 R=1 S=8`
  - `0079A7D0 OK  C=796960 E=1 F=80F420 G=810580 R=1 S=8`
  - `0079ACF0 OK  C=796CF0 E=1 F=80F420 G=810580 R=1 S=8`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`00796CF0 -> 00796CF1`). The checker flagged it: `0079ACF0 BAD C: sentence 00796CF1 body 796CF0`, and the package summary became `rows checked 7, bad 1 (rep 005C1C10, 27 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
