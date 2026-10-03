# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-why-the-unowned-code-has-no-owner-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHY-THE-UNOWNED-CODE-HAS-NO-OWNER-EE-EC080` · Package: `_index/candidates/opus-why-the-unowned-code-has-no-owner-ee-1003/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 3 rows. All 3 were read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every row holds as written. That includes the OPUS correction on `008820E0`, the sign-extended realloc size. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 3 rows with 5 anchors each, 15 in total. The README's `Missing: 0` matches `rows.json`.
- **Image values.**
  - `01CEB590` holds 33 dwords, (1 << n) - 1 for n = 0 to 32 (`00000000`, `00000001`, `00000003` ... `7FFFFFFF`, `FFFFFFFF`). So "mask table" describes the data.
  - The qword at `01CEB630` is `00861F26`. That address holds `jmp [rip+…]` through IAT slot `008C2B48`, which the pefile import table names `api-ms-win-crt-heap-l1-1-0.dll!free`.
  - The qword at `01CEB620` is `00861F32`. That address holds a `jmp` through `008C2B58`, which is `api-ms-win-crt-heap-l1-1-0.dll!realloc`.

Per row:

- **`0017CB40`**: exact.
  - `cmp r9d,0x20` / `ja` (`0017CB4C`) is the unsigned n > 32 test. The mask dword n is loaded at `0017CB61`, after that test.
  - `r9d` = n + b (`0017CB65`). The tests are `cmp pos, limit-4` / `jl` (signed, `0017CB72`) and `cmp pos, limit - ((n+b+7) sar 3)` / `jg` (signed, `0017CB81`). The second compare is signed, and the row's "above" carries no unsigned qualifier.
  - The failure block `0017CC41`-`0017CC58` sets pos to the limit, zeroes qword +0x10, stores dword +4 = 1 and returns -1.
  - `0017CB87`-`0017CB8C`: n + b = 0 returns 0.
  - Main path: byte 0 shifted right by `cl` = low byte of b (`0017CBA7`). Then the bytes k = 1, 2, 3 and 4 are each shifted left by 8k - b and ORed in, each behind `cmp n+b, 8k` / `jle`. k = 4 also needs `test r11d,r11d` / `je` (b non-zero, `0017CBF5`).
  - `0017CC0B`-`0017CC37`: dword +4 = (n+b) AND 7. The step is `cdq`/`and edx,7`/`add`/`sar 3`, a signed division by 8. Qword +0x10 and dword +0 both advance by it. The result is ANDed with the mask (`0017CC2E`).
- **`006F1C00`**: exact.
  - `a` is set by `sete` (dword [rcx+0x470] == 8, `006F1C23`).
  - `b` = 1 when qword [rcx+0x468] or qword [rcx+0x58] is non-null (`006F1C27`-`006F1C37`). The second compare is against `rbx` = 0.
  - With neither: `c` = 1 (`006F1C4A`), `i` = dword [rcx+0x4D0], replaced by dword [x+0xA0] when it is -1. `cmp i,[x+0x3C]` / `jl` (signed) selects qword [[x+0x48]+8i], else 0 (`006F1C5F`-`006F1C6F`).
  - Otherwise: `c` = 0 (`006F1C75`). `a` gives qword [x+0x90+8·sext(dword [x+0xA4])] (`006F1C86`/`006F1C8D`). Else `cmovne` gives qword [rcx+0x468] (`006F1C9A`), and `b` is necessarily set on that path.
  - Byte stores to `rdx` (saved in `rsi`), `r8` (saved in `rdi`) and `r9`, each behind its own null test (`006F1C9E`-`006F1CB3`). The function returns `rax`.
- **`008820E0`**: exact.
  - `008820EE`: n = qword [rcx+0x70]. The next pointer qword [n+8] is read into `rdi` at `00882103`, before both calls.
  - `00882107`: `call [01CEB630]` (free) on qword [n]. Then [n] and [n+8] are zeroed, and `00882119` calls the same pointer on `n`.
  - `0088212C`-`00882136`: `c` = dword +0x68; zero skips to `00882166`, which zeroes +0x70 and +0x60.
  - Non-zero: `eax` = dword +0x64 + c (32-bit), `movsxd rdx` (`00882141`), `call [01CEB620]` (realloc) with `rcx` = qword +0x58. The result is stored at `0088214A` with no test.
  - Dword +0x68 is re-read and added to +0x64 (`00882151`). Then +0x68, +0x70 and +0x60 are zeroed.

- **Absence claims.** The "no null test" claim in `008820E0` was checked against the only conditional jumps in the body (`008820F5`, `00882125`, `00882136`).

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not say whether these functions belong to any system, which is the page's subject.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
