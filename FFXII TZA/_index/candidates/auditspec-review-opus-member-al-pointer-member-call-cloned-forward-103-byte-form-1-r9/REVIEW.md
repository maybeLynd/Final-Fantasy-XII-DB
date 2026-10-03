# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-member-al-pointer-member-call-cloned-forward-103-byte-form-1-r9)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-AL-POINTER-MEMBER-CALL-CLONED-9C1DC` · Package: `_index/candidates/opus-member-al-pointer-member-call-cloned-forward-103-byte-form-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Every row is exact at the bytes; no narrowing.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` from the package dir, without `--apply` (venv python): `VERIFY 4 functions, 20 anchors`, `ALREADY`, `FAILS 0`, exit code 0.
- Image: `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256 `73461D08...D89721F8` (matches the certified hash); extents from `graph/functions.tsv`.
- `rows.json`: 4 rows, 20 anchors, mode `member`; rejected 0, skipped 0, missing 0. README counts agree.
- Representative `006775A0`, read in full against its sentence: `00676700(c)`'s result goes straight into `call [rbx+8]` (no test); `rcx` = c is set before the `test rax, rax`; a non-null `v` calls `00684080(c, v, 02D3E680)` and returns 1; a null `v` calls `0080F420(c, 1)` and `00810620(c)` and returns 1. Exact.
- Every row, mechanically (`Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_nn/chk.py`, output `chk.out`): extent equals the form size and the linear decode covers it exactly; the instruction shape (mnemonics and operands, in-body branch targets as offsets, external targets as EXT) equals the representative's with only the field instructions' numbers masked; the sentence matches the package template; every captured value (call/jump targets, resolved rip targets, immediates, slot and field displacements) equals the decoded value; anchors keep the representative's offsets and mnemonics. Result: 4 rows, bad 0 (A = 00676700 / 00683B50 / 0067EDD0 / 00683B50, L = 02D3E680 / 02D3E680 / 02E4EAF0 / 02E4FF60, J = 00684080 except 00684090 in the last row; F = 0080F420, G = 00810620, E = 1, S = 8, both returns 1 in all). Each row's own `lea` is an anchor, as README says.
- Controls (in memory, nothing written): `--plant` changes the last hex digit of the first address in the last row's sentence and the checker flags exactly that row (`TOTAL rows 35 bad 8`, one per form package); `--plant-shape` points the last row at another form's representative body and the checker flags exactly that row (size, shape and anchors all differ; `TOTAL rows 35 bad 8`). `--plant-same-size` swaps the last rows of the two 103-byte forms onto each other's representative (same extent, so only the shape test and the field values can catch it): both flagged, `TOTAL rows 35 bad 2`.

## SWE2-AUDIT-SPEC limits

- Static body statements only, against the certified image; nothing here was observed in a live process.
- The representative was read clause by clause; the other rows stand on the mechanical comparison (shape plus every varying value against its sentence), not on a separate prose reading.
- Callee behaviour is not reviewed except where the sentence states it. The family name on the page and the page's other text are outside this review.
- OPUS's re-read and the drafting agent are not independent review; this record is.
