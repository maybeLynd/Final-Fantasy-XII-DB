# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-optional-pointer-alloc-record-install-104-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-OPTIONAL-POINTER-ALLOC-RECORD-2D402` · Package: `_index/candidates/opus-member-optional-pointer-alloc-record-install-104-byte-form-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 4 functions, 20 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 4 rows, 20 anchors, mode `member`; rejected 0, skipped 0, missing 0. README counts agree.
- Representative `00680520`, read in full against its sentence: `0080F420(c, 1)`; `b` = `00810240(c, 0x10)`; a non-null `b` gets qword [b+8] = `r8` and qword [b] = `02E41070`; then `0080FA50(c, 0xFFF0B9D8 = -1001000, 00D6FDE0)` (that rip target is the string "PhyreObject"); `jmp 00810F60` with `edx` = -2 and `rcx` = c. Exact.
- Every row, mechanically (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/chk.py`, output `chk.out`): extent equals the form size and the linear decode covers it exactly; the instruction shape (mnemonics and operands, in-body branch targets as offsets, external targets as EXT) equals the representative's with only the field instructions' numbers masked; the sentence matches the package template; every captured value (call/jump targets, resolved rip targets, immediates, slot and field displacements) equals the decoded value; anchors keep the representative's offsets and mnemonics. Result: 4 rows, bad 0 (V = 02E41070 / 02E41270 / 02E41170 / 02E41470; F = 0080F420, B = 00810240, N = 16, D = 8, P = 0080FA50, K = -1001000, S = 00D6FDE0, T = 00810F60, M = -2 in all). Each row's own `lea` is an anchor, as README says.
- Controls (in memory, nothing written): `--plant` changes the last hex digit of the first address in the last row's sentence and the checker flags exactly that row (`TOTAL rows 35 bad 8`, one per form package); `--plant-shape` points the last row at another form's representative body and the checker flags exactly that row (size, shape and anchors all differ; `TOTAL rows 35 bad 8`).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- The representative was read clause by clause; the other rows stand on the mechanical comparison (shape plus every varying value against its sentence), not on a separate prose reading.
- Callee behaviour is not reviewed except where the sentence states it. The family name on the page and the page's other text are outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
