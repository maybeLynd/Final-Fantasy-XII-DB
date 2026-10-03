# SWE2-AUDIT-SPEC review: FABLE cloudint interior citations (fable-what-the-game-asks-windows-for-cloudint-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-WHAT-THE-GAME-ASKS-WINDOWS-FOR-CLOUDIN` · Package: `_index/candidates/fable-what-the-game-asks-windows-for-cloudint-1002/` · Page: `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh -> exit 0, `ALREADY / FAILS 0`.
- `rows.json`: 9 rows, 45 anchors; rejected 0, missing 0.
- Semantic pass: **all 9 rows** read sentence-by-sentence against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). 8 of 9 rows exact, including `001597E0`'s copy/truncation codes, the `00159CA0` mask chain and `_wcsnicmp` at +0x161, the `0015AC50` type 1/7/other handling, the `0015AE60` RegEnumValueW loop (0x10000 allocation, 0x8000 memset and size 0x7FFF before each call, stop on 0x103) and `0015BB30`. **One row is wrong**: `0015B820`, see the defect below.
- Limits hold: body statements only, static evidence; a cloud draft plus FABLE's re-read is not independent review, this record is.

## SWE2-AUDIT-SPEC narrowing / notes

**Defect (row `0015B820`, anchor `0015B906`):** the sentence says the first try `0015A9B0(rsi, 01CC6BE8)` runs "when `00861F20(suffix, 01CC6BF8)` is 0". The bytes do the opposite. `0015B8E9 call _wcsicmp(suffix, 01CC6BF8 = L".dll") / test eax,eax / je 0015B90E` **skips** the try when the suffix equals ".dll". The try runs only when `_wcsicmp` is **non-zero** (the suffix is not ".dll") and `008C20A8()` is 0. Exact replacement wording for that clause: "`0015A9B0(rsi, 01CC6BE8)` when `00861F20(suffix, 01CC6BF8)` (".dll") is non-zero". The rest of the row is exact: the ".sys" (`01CC70E0`) gate on the `0015AC50`/`0015AE60` pair, the `01CC6EF0` list, the d / +0x24C choice and the 0x50 / -1 drop. A minor note that is not a defect: the first `0015AC50` call also stores an unused second pointer list (`01CC70B0/01CC7088/01CC7050`) in the outgoing stack-argument slots, and `0015AC50` (4 register args) never reads it. FABLE repairs the row; the other 8 rows may be accepted as-is.
