# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-font-data-kerning-and-expansion-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FONT-DATA-KERNING-AND-EXPANSION-EE-10-DF788` · Package: `_index/candidates/opus-font-data-kerning-and-expansion-ee-1003/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 2 rows. Both were read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Both rows hold as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 2 functions, 10 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 2 rows, 5 anchors each, 10 in total. The README's `Missing: 0` matches the empty `missing` list in `rows.json`.

Per row:

- **`001FDDD0`**: exact.
  - First tree: head `rcx`+0x78 (`001FDDDA`), root qword [rcx+0x88] (`001FDDD0`), key `r8d`.
  - Descent: `cmp dword [n+0x20], r8d` / `jl` (`001FDDE6`/`001FDDEA`). The fall-through records `n` in `r9` and loads qword [n+8]; the `jl` arm loads qword [n]. The loop ends on null (`001FDDFB`).
  - Final test: a recorded node equal to the head is kept as the head (`001FDDFD`); otherwise `cmp r8d, [r9+0x20]` / `jge` keeps it and the failing case resets to the head (`001FDE02`-`001FDE08`). Together with the descent test this means equal.
  - `001FDE0F`/`001FDE12`: `a` equal to the head returns 0 through `001FDE56`.
  - Second tree: head `a`+0x30, root qword [a+0x40], key `r10d` (the saved `edx`, `001FDDD7`), with the same shape at `001FDE24`-`001FDE46`.
  - `001FDE49`-`001FDE50`: `b` equal to `a`+0x30 returns 0. Otherwise `001FDE52` returns dword [b+0x24].
- **`001FF990`**: exact.
  - `001FF9AA`/`001FF9AD`: `rdi` = `s`, `rsi` = `m`. `001FF9B0` calls `001FFAB0` with `rcx` = `m`, `rdx` = `s` and `r8` unchanged, and the result `r` goes to `rbx` and `[rsp+0x78]`.
  - `001FF9BD`-`001FF9D0`: a non-null qword [s] gives `[r]` = `001FF990(m, [s], r)`.
  - `001FF9D3`-`001FF9DD`: `s` = qword [s+8], `p` = `r` (`rbp`). A null `s` skips to `001FFA98`, which returns `r`.
  - Loop: `rcx` = `m`+0x30, `call [ [rcx]+0x10 ]` with `edx` = 0x50 and `r8d` = 0 (`001FF9F0`-`001FF9FA`), giving `b`.
  - `001FFA05`-`001FFA11`: the only null test is on `b`+0x20. Inside it, qwords b+0x20, b+0x28 and b+0x30 are zeroed. Then `001EDF00(b+0x38, s+0x38)`, `001A4BF0(b+0x20, [s+0x20], [s+0x28])` and `001FE6B0(b+0x40, s+0x40)` are called (`001FFA20`-`001FFA46`).
  - `001FFA4C`-`001FFA60`: no test on `b`. The code zeroes [b] and [b+8], stores `p` at [b+0x10], byte [s+0x18] at byte [b+0x18], and `b` at [p+8].
  - `001FFA64`-`001FFA79`: `[b]` = `001FF990([rsp+0x60], [s], b)`. `[rsp+0x60]` is the home slot of `rcx`, written at `001FF990` (frame: 3 pushes + 0x40), so it is `m`.
  - `001FFA80`: `p` = `b`. `001FFA91` returns `[rsp+0x78]` = `r`.
- **Callees.** Neither row says what a callee does, so no callee body was needed. The "no null test" claim was checked against every conditional jump in the body; the only tests are at `001FF9C3`, `001FF9DD`, `001FFA11`, `001FFA6A` and `001FFA8B`.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret the trees as kerning or expansion maps.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text. This review did not diff the page itself.
