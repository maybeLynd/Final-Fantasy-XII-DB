# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-l-pointer-offset-add-dispatch-adapters-64-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-L-POINTER-OFFSET-ADD-DISPATCH-6449F` · Package: `_index/candidates/opus-member-l-pointer-offset-add-dispatch-adapters-64-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 8 member rows of the 64-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `005A0EC0`** (18 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rbx, rdx` keeps `c`; `mov rdx, qword ptr [r8]` loads `p`; `mov rcx, rbx` puts `c` in `rcx` on both paths before `test rdx, rdx` / `je`.
  - non-null path: `add rdx, 8` (p + 8), `lea r8, [rip + 0x270ce71]` resolving to `02CADD50` (next instruction `005A0EDF` + 0x270ce71), frame teardown, `jmp 0x684080`.
  - null path (`005A0EE9`): `mov edx, 1` with `rcx` = `c` still set, `call 0x80f420`, then `mov rcx, rbx` and `jmp 0x810620`; the body is 64 bytes (`005A0EC0`..`005A0EFF`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 7 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 64 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the `add rdx` immediate (A, 8 or 0x30), the `lea r8` rip target (L), the non-null `jmp` target (J, `00684080` or `00684090`), the `mov edx` immediate (E), the `call` target (F) and the null-path `jmp` target (T).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 8, bad 0`. Per-row decoded fields:
  - `005A0EC0 OK  A=8 E=1 F=80F420 J=684080 L=2CADD50 T=810620`
  - `005A13E0 OK  A=8 E=1 F=80F420 J=684080 L=2CAECE0 T=810620`
  - `005A1A00 OK  A=8 E=1 F=80F420 J=684080 L=2CAEEE0 T=810620`
  - `005A21B0 OK  A=8 E=1 F=80F420 J=684080 L=2CAEFE0 T=810620`
  - `005A2470 OK  A=8 E=1 F=80F420 J=684090 L=2CAD140 T=810620`
  - `005A27F0 OK  A=8 E=1 F=80F420 J=684080 L=2CAEA60 T=810620`
  - `0062F9D0 OK  A=30 E=1 F=80F420 J=684080 L=2CF8580 T=810620`
  - `006CCE20 OK  A=8 E=1 F=80F420 J=684090 L=2E5C050 T=810620`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`00684090 -> 00684091`). The checker flagged it: `006CCE20 BAD J: sentence 00684091 body 684090`, and the package summary became `rows checked 8, bad 1 (rep 005A0EC0, 18 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
