# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-phyre-script-object-accessors-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-PHYRE-SCRIPT-OBJECT-ACCESSORS-EE-1003-CBF8E` · Package: `_index/candidates/opus-phyre-script-object-accessors-ee-1003/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 1 row with 5 anchors. The README's `Missing: 0` matches `rows.json`.
- **Constant.** `0xFFF0B9D8` is -1001000 as a signed dword (0x100000000 - 0xFFF0B9D8 = 0xF4628 = 1001000). So "i from -1000999 to 0" is exactly the `jle`-not-taken range above it.

**`00810810`**: exact. Both arguments decode the same way, `edx` at `00810827`-`0081089C` and `r8d` at `008108A1`-`00810907`.

- `s` = qword [rcx+0x20] (`00810816`). `N` = `01CCB510` (`0081081A`, `rdi`).
- i > 0 (`test`/`jle`): qword [s] + 16i (`movsxd`, `shl 4`, `add [r11]`), kept by `cmovb` when it is below qword [rcx+0x10], else `N` (`00810838`/`0081083C`).
- i > -1001000 (signed `jle` not taken): qword [rcx+0x10] + 16·sext(i) (`00810842`-`0081084E`).
- i = -1001000: qword [rcx+0x18] + 0x40 (`00810854`-`0081085A`).
- Below that:
  - `f` = qword [s]; dword [f+8] == 0x16 gives `N` (`00810869`/`0081086D`).
  - Otherwise `c` = qword [f] and `u` = 0xFFF0B9D8 - i (`00810863`/`00810866`). `cmp u, movzx byte [c+0xA]` / `jg` gives `N` (signed). Else `c` + 16·((u - 1) + 2) = `c` + 16(u + 1) (`00810885`-`00810894`).
- Tail:
  - Either result equal to `N` returns 0 (`0081090A`-`00810912`).
  - The dwords +8 must be equal (`00810914`-`0081091B`).
  - `0081091F` calls `00821520` with `ecx` = 0, `rdx` = A(edx) and `r8` = A(r8d).
  - A non-zero result returns 1 (`00810924`-`00810928`); everything else reaches `00810933`, which returns 0.

The row says nothing about `00821520` beyond its arguments and the test on its result, so that body was not needed.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret the slot ranges (positive, local, -1001000, the upvalue-like tail) as script semantics.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
