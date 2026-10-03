# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-pointer-member-call-dispatch-adapters-75-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-POINTER-MEMBER-CALL-DISPATCH-A-34344` · Package: `_index/candidates/opus-member-pointer-member-call-dispatch-adapters-75-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 8 member rows of the 75-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `006B2B70`** (21 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rdi, qword ptr [r8]` reads `p` first, `mov rbx, rdx` keeps `c`; neither writes `rcx`, `rdx` or `r8`, so `call 0x6b0760` receives them as received.
  - after the call `mov rcx, rbx` sets `c`; `test rdi, rdi` / `je`; non-null path `mov rdx, rdi` (p) and `jmp 0x6840a0`. No instruction on this path writes `r8`, so the sentence's `(r8 not set)` holds: `r8` carries whatever the callee left.
  - null path (`006B2B9F`): `mov edx, 1`, `call 0x80f420` with `rcx` = `c`, `mov rcx, rbx`, `jmp 0x810620`; the body is 75 bytes (`006B2B70`..`006B2BBA`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 7 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 75 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the first `call` target (C), the non-null `jmp` target (J), the `mov edx` immediate (E), the second `call` target (F) and the null-path `jmp` target (T).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 8, bad 0`. Per-row decoded fields:
  - `006B2B70 OK  C=6B0760 E=1 F=80F420 J=6840A0 T=810620`
  - `006B2BC0 OK  C=6B08A0 E=1 F=80F420 J=684130 T=810620`
  - `006B2C10 OK  C=6B09E0 E=1 F=80F420 J=684130 T=810620`
  - `006B2C60 OK  C=6B0B20 E=1 F=80F420 J=684280 T=810620`
  - `006B2CB0 OK  C=6B0EC0 E=1 F=80F420 J=684300 T=810620`
  - `006B2D00 OK  C=6B1320 E=1 F=80F420 J=684360 T=810620`
  - `006B2D50 OK  C=6B1600 E=1 F=80F420 J=6843D0 T=810620`
  - `006B2DA0 OK  C=6B19A0 E=1 F=80F420 J=684450 T=810620`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`006B19A0 -> 006B19A1`). The checker flagged it: `006B2DA0 BAD C: sentence 006B19A1 body 6B19A0`, and the package summary became `rows checked 8, bad 1 (rep 006B2B70, 21 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
