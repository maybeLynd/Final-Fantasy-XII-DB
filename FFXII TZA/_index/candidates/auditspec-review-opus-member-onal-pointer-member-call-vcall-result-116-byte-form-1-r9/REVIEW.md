# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-onal-pointer-member-call-vcall-result-116-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ONAL-POINTER-MEMBER-CALL-VCALL-6243E` · Package: `_index/candidates/opus-member-onal-pointer-member-call-vcall-result-116-byte-form-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 4 functions, 20 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 4 rows, 20 anchors, mode `member`; rejected 0, skipped 0, missing 0. README counts agree.
- Representative `005C21B0`, read in full against its sentence: `a` = `005BADB0(c)` is taken first (`rsi`), then `o` = `005BDDC0(c)`; a null `o` returns `rax` (0); otherwise `call [rbx+8]` gets `rcx` = o and `rdx` = a, its `eax` is kept in `ebx`, then `0080F420(c, 1)`, `00810580(c, ebx)` and `mov eax, 1`. Exact.
- Every row, mechanically (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/chk.py`, output `chk.out`): extent equals the form size and the linear decode covers it exactly; the instruction shape (mnemonics and operands, in-body branch targets as offsets, external targets as EXT) equals the representative's with only the field instructions' numbers masked; the sentence matches the package template; every captured value (call/jump targets, resolved rip targets, immediates, slot and field displacements) equals the decoded value; anchors keep the representative's offsets and mnemonics. Result: 4 rows, bad 0 (A = 005BADB0 / 005BCD20 / 00683B50 / 006AAE00, O = 005BDDC0 / 005BDDC0 / 00637170 / 006AC1D0; S = 8, E = 1, R = 1 and F/G = 0080F420/00810580 in all).
- Controls (in memory, nothing written): `--plant` changes the last hex digit of the first address in the last row's sentence and the checker flags exactly that row (`TOTAL rows 35 bad 8`, one per form package); `--plant-shape` points the last row at another form's representative body and the checker flags exactly that row (size, shape and anchors all differ; `TOTAL rows 35 bad 8`).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- The representative was read clause by clause; the other rows stand on the mechanical comparison (shape plus every varying value against its sentence), not on a separate prose reading.
- Callee behaviour is not reviewed except where the sentence states it. The family name on the page and the page's other text are outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
