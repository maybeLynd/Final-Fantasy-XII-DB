# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-section-019-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-019-CLOUDINT-1003-FD5B0` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-section-019-cloudint-1003/` · Page: `25-EBP-Script-Container/Sections/section-019.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 10 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `0020D270`: an empty range returns `r8`. Per 0xC entry: `test r8, r8; je` skips only the copy (qword by `movsd`, dword `+8`), and both pointers still advance by 0xC. The result is the destination end. Exact.
  - `0020D970`: 0 for `rdx` = 0. The bound is `cmp rdx, 0x1555555555555555; jbe` (unsigned), with the `008C2608` import and `int3` above it. `n` = `rdx*3 << 2`. `cmp n, 0x1000; jb` gives the direct `00210EC0(n)`. Otherwise `n+0x27` is overflow-checked with `cmp rax, rcx; ja` (no wrap continues, wrap calls `008C2608`), then `00210EC0(n+0x27)`, `(p + 0x27) & ~0x1F` and the raw pointer at `[result-8]`. A null result on either path calls `008C2DA8` and `int3`. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
