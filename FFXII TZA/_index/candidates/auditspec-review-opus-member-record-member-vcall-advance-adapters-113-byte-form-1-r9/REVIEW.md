# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-record-member-vcall-advance-adapters-113-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-RECORD-MEMBER-VCALL-ADVANCE-AD-90292` · Package: `_index/candidates/opus-member-record-member-vcall-advance-adapters-113-byte-form-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 6 functions, 30 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 6 rows, 30 anchors, mode `member`; rejected 0, skipped 0, missing 0. README counts agree.
- Representative `005CC3E0`, read in full against its sentence: the fifth argument is `[rsp+0x50]` after `push rdi; sub rsp, 0x20` (entry +0x28); a null `rdx` returns 0; `add qword [rax], 8`, then `edx` = dword [new value - 8], `call [r8+8]` with `rcx` = o; a null `r9` returns 0; `k` is compared with `02CAD440 | 1` (`lea` + `or rax, 1`, `jne` to the 0 return); else qword [out] = 0, qword [out+8] = the call result, return 1. Exact.
- Every row, mechanically (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/chk.py`, output `chk.out`): extent equals the form size and the linear decode covers it exactly; the instruction shape (mnemonics and operands, in-body branch targets as offsets, external targets as EXT) equals the representative's with only the field instructions' numbers masked; the sentence matches the package template; every captured value (call/jump targets, resolved rip targets, immediates, slot and field displacements) equals the decoded value; anchors keep the representative's offsets and mnemonics. Result: 6 rows, bad 0 (L = 02CAD440 / 02CADC50 / 02CAD840 / 02CF8470 / 02CB6B80 / 02E4E430; A = B = D = S = 8, O = 1, Z = 0, R = 1 in all).
- Controls (in memory, nothing written): `--plant` changes the last hex digit of the first address in the last row's sentence and the checker flags exactly that row (`TOTAL rows 35 bad 8`, one per form package); `--plant-shape` points the last row at another form's representative body and the checker flags exactly that row (size, shape and anchors all differ; `TOTAL rows 35 bad 8`).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- The representative was read clause by clause; the other rows stand on the mechanical comparison (shape plus every varying value against its sentence), not on a separate prose reading.
- Callee behaviour is not reviewed except where the sentence states it. The family name on the page and the page's other text are outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
