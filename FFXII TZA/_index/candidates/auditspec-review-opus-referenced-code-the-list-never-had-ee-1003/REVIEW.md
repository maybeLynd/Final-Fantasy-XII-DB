# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-referenced-code-the-list-never-had-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-REFERENCED-CODE-THE-LIST-NEVER-HAD-EE-43FB7` · Package: `_index/candidates/opus-referenced-code-the-list-never-had-ee-1003/` · Page: `99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 1 row, 5 anchors. Rejected 0, skipped 0, missing 0, corrections 1. The correction holds:
  - The inner step is `add ebp, r12d`, the product of the earlier factors (`0088D6A0`).
  - The angle is `k` × (`ebp` × step) in float, widened by `cvtss2sd`.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...).
  - `0088D500` (651 B), exact.
    - Divisors: `01CE3060` (`.rdata`) holds 4, 2, 3, 5. After those, `add r10d,2` (`0088D54F`). Trial `idiv` (`0088D556`) / `imul` / `cmp`. A divisor is repeated while it divides (`0088D5C1`..`0088D5CF` → `0088D570`).
    - The factors are dwords at `r8+8+4i`. A 2 found at position >1 shifts the earlier slots up (`0088D5A3`) and writes 2 to `r8+8`. The first position is skipped by `cmp r9,1` / `je`.
    - `[r8]`=`ecx`, and `[r8+4]`=count.
    - The step is `01CEBC78` (`.rdata` 0x40C90FDB = 6.2831855) / float(`ecx`) (`0088D5FF`).
    - The outer loop runs count-1 times (`jl` skip when count-1 < 1).
    - `m` = n/(`r12d`·p). The inner loop runs p-1 times (`jle` skip), and the offset grows by (p-1)·m.
    - The pair count is ((m-3) `shr` 1)+1 when m>2 (`jle`). `xmm7` += 1.0 gives `k`. The pairs are `cos`/`sin` (thunks `00861F62`/`00861F68` → IAT `cos`/`sin`; `0088D6E7`/`0088D6FA`), each `cvtsd2ss` into `[rbx]`/`[rbx+4]`.
    - `rsi` advances by m floats per multiple. `r12d` ← p·`r12d` after each factor.
    - No result value is set before `ret`.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
