# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-float-pipeline-member-vcall-adapters-121-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-FLOAT-PIPELINE-MEMBER-VCALL-AD-DDA3A` · Package: `_index/candidates/opus-member-float-pipeline-member-vcall-adapters-121-byte-form-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 5 functions, 25 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 5 rows, 25 anchors, mode `member`; rejected 0, skipped 0, missing 0. README counts agree.
- Representative `006B2400`, read in full against its sentence: `00811640(c, -1, 0)` (`or edx, -1`, `xor r8d, r8d`); its `xmm0` is kept in `xmm6`. The callee does return a float: both of its `ret` paths set `xmm0` (`xorps` or `movss xmm0, [rcx]`). Then `00811130(c, -2)` and `o` = `00683BF0(c)`; a null `o` returns `rax` (0); else `call [rdi+8]` with `rcx` = o and `xmm1` = x, then `00684280(c, result)`, return 1. Exact.
- Every row, mechanically (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/chk.py`, output `chk.out`): extent equals the form size and the linear decode covers it exactly; the instruction shape (mnemonics and operands, in-body branch targets as offsets, external targets as EXT) equals the representative's with only the field instructions' numbers masked; the sentence matches the package template; every captured value (call/jump targets, resolved rip targets, immediates, slot and field displacements) equals the decoded value; anchors keep the representative's offsets and mnemonics. Result: 5 rows, bad 0 (J = 00684280 / 00684300 / 00684360 / 006843D0 / 00684450; X = 00811640, Y = 00811130, O = 00683BF0, M1 = -1, M2 = -2, S = 8, R = 1 in all).
- Controls (in memory, nothing written): `--plant` changes the last hex digit of the first address in the last row's sentence and the checker flags exactly that row (`TOTAL rows 35 bad 8`, one per form package); `--plant-shape` points the last row at another form's representative body and the checker flags exactly that row (size, shape and anchors all differ; `TOTAL rows 35 bad 8`).

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- The representative was read clause by clause; the other rows stand on the mechanical comparison (shape plus every varying value against its sentence), not on a separate prose reading.
- Callee behaviour is not reviewed except where the sentence states it. The family name on the page and the page's other text are outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
