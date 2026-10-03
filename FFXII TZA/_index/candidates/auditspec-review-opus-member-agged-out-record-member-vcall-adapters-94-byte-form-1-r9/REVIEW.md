# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-agged-out-record-member-vcall-adapters-94-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-AGGED-OUT-RECORD-MEMBER-VCALL-9C717` · Package: `_index/candidates/opus-member-agged-out-record-member-vcall-adapters-94-byte-form-1-r9/` (reviewed at HEAD `5d585421e`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 8 member rows of the 94-byte adapter form (mode `member`). Every row was checked against a raw capstone decode of the certified image; this session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every sentence holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. Its last lines were `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit code 0.
- **Representative read in full: `005CC300`** (29 instructions over its `functions.tsv` extent), clause by clause:
  - `mov rbx, r9` (out), `mov rdi, r8` (k), `mov rax, rcx` (f); `test rdx, rdx` / `je` to `005CC351` (`xor eax, eax`, return 0) when `o` is null.
  - `mov rcx, rdx` / `call qword ptr [rax + 8]` gives `v` (the pointer stored at f+8, called with `o`); `mov rcx, rax` keeps `v`; `test rbx, rbx` / `je` returns 0 when `out` is null.
  - `lea rax, [rip + 0x2881303]` resolves to `02E4D630` (next instruction `005CC32D` + 0x2881303), `or rax, 1`, `cmp rdi, rax` / `jne` returns 0 when `k` differs; else `mov qword ptr [rbx], 0`, `mov eax, 1`, `mov qword ptr [rbx + 8], rcx` and return 1. The body is 94 bytes (`005CC300`..`005CC35D`).
  - The sentences state no behaviour of any callee (only what each body passes and returns), so no callee body needed reading. No float constants and no vtable slots occur in this form.
- **The other 7 rows, proven mechanically** (`w10/scratch_mm/chk.py`, output `chk.out`). For every row the checker decoded the body over its `functions.tsv` extent and required:
  - the extent to equal 94 bytes and the decode to cover it exactly;
  - the instruction sequence to equal the representative's, mnemonic by mnemonic and operand by operand, with intra-body branch targets compared as offsets and only the operands of the field instructions masked;
  - the sentence to match one fixed template whose only variable parts are the captured fields, so all non-field wording is identical across rows;
  - each captured field to equal the value decoded from its instruction (direct targets from the operand, rip operands resolved as next-instruction address plus displacement, immediates and displacements from capstone's operand detail). Fields compared per row: the indirect-call displacement (S), the `lea rax` rip target (L), the `or` immediate (O), the stored zero (Z), the return immediate (R) and the `out` store displacement (D).
  - the anchors to sit at the representative's offsets, each on an instruction boundary with the recorded mnemonic.
- **Result:** `rows checked 8, bad 0`. Per-row decoded fields:
  - `005CC300 OK  D=8 L=2E4D630 O=1 R=1 S=8 Z=0`
  - `00610B50 OK  D=8 L=2D3A440 O=1 R=1 S=8 Z=0`
  - `00610BB0 OK  D=8 L=2D3A640 O=1 R=1 S=8 Z=0`
  - `00610CA0 OK  D=8 L=2CB7080 O=1 R=1 S=8 Z=0`
  - `006A68F0 OK  D=8 L=2E518D0 O=1 R=1 S=8 Z=0`
  - `006A9360 OK  D=8 L=2E404B0 O=1 R=1 S=8 Z=0`
  - `006AB210 OK  D=8 L=2CF8470 O=1 R=1 S=8 Z=0`
  - `006AB270 OK  D=8 L=2E4EAF0 O=1 R=1 S=8 Z=0`
- **Planted-defect control** (`chk.py --plant`, output `chk_plant.out`). One hex digit of the first address in the last row's sentence was altered in memory (`02E4EAF0 -> 02E4EAF1`). The checker flagged it: `006AB270 BAD L: sentence 02E4EAF1 body 2E4EAF0`, and the package summary became `rows checked 8, bad 1 (rep 005CC300, 29 insns)`.

## SWE2-AUDIT-SPEC limits

- These are body statements, not meanings. The review does not test the family name, what the shared callees do with the values passed, or what the referenced data cells hold.
- The checker proves each row equivalent to the representative and its sentence to the template; the representative itself was read by hand against one capstone decode, not a second independent decoder.
- `intdump.py` prints past a body's end into the next function when no int3 padding follows; the checker bounds every decode by the `functions.tsv` extent instead, and only that extent was judged.
