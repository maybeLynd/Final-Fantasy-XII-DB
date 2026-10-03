# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sound-trigger-ee-1003-2)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SOUND-TRIGGER-EE-1003-2-39F64` · Package: `_index/candidates/opus-sound-trigger-ee-1003-2/` (package last changed at `793e20e74`; reviewed at HEAD `85ecbde72`) · Page: `18-Audio/Sound-Selection/sound-trigger.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 3 rows. All 3 were read clause by clause against a raw capstone decode of the certified image. This session hashed the image itself: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. Every row holds as written, including the three OPUS corrections:

- the NaN step-back;
- the unbounded newline store;
- the re-read after a match.

No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0` and exited 0.
- **Counts.** 3 rows with 5 anchors each, 15 in total. The README's `Missing: 0` matches `rows.json`.
- **Constants and strings read from the image.**
  - `01CEBBA8` is the float 1.0 (bytes `0000803f`).
  - `008F8180` is the float 10.0 (bytes `00002041`).
  - `01CB4980` is the float -4.8 (bytes `9a9999c0`).
  - `01CB4568` is the string `[sead][!!error!!]list append error full!`, exactly as quoted.
- **Imports, from the pefile import table.**
  - `008C2120` = `KERNEL32.dll!OutputDebugStringA`.
  - `008C20B8` = `KERNEL32.dll!EnterCriticalSection`.
  - `008C20C0` = `KERNEL32.dll!LeaveCriticalSection`.
  - `00861F6E` is `jmp [008C2C30]`, which is `api-ms-win-crt-math-l1-1-0.dll!powf`. The row names only the address, which is correct.
- **Callees read.**
  - `007A9E50` switches on `edx` (`cmp edx,5`), with its float argument in `xmm0`. So the call shape `007A9E50(ratio, curve)` matches how the body uses its arguments.
  - `0019C5D0` wraps `__stdio_common_vsprintf_s` (`008C2E10`) and maps a negative result to -1 (`0019C615`-`0019C61A`). So "the returned length" is a length, or -1.
  - `00808C40` compares `rcx` against `01F44830`, so it is the cookie check.

Per row:

- **`007AE260`**: exact.
  - A null `t` (`007AE270`) or a zero word [t+4] (`007AE27D`) returns 0.0 through `007AE3FE`.
  - Clamp: `comiss x,0` / `jae`. The taken path applies `minss` with 1.0; the not-taken path (below 0, or NaN since CF is set) gives 0 (`007AE29F`-`007AE2AB`).
  - The points start at `t` + movzx word [t+2] (`007AE2AF`/`007AE2BA`), with a 16-byte stride (`add rcx,rcx` then `*8`). The fields are curve byte +2, key float +4 and value float +8.
  - Search: lo = 0, hi = n - 1, mid = (lo+hi) via `cdq`/`sub`/`sar 1`, a signed division (`007AE2D0`-`007AE2D7`).
    - `ucomiss key,x` / `je` stops on equal or unordered (`007AE2E8`/`007AE2EB`).
    - `comiss` / `jae` sets hi = mid - 1, else lo = mid + 1. The loop continues while `lo <= hi`.
  - After the search: `comiss x, key i` / `jae` skips the step-back, so the step-back happens on below or unordered.
    - `test edx,edx` / `jle` with `dec` steps back only when i > 0 (`007AE307`-`007AE312`).
    - Otherwise `cmp i,n` / `cmovge i, n-1` clamps (`007AE316`/`007AE319`).
  - `v` (`007AE31D`-`007AE389`):
    - i == n - 1 takes value i.
    - Otherwise xmm0 = (x - key i)/(key i+1 - key i) and `edx` = curve byte i are passed to `007AE36E` → `007A9E50`, and v = value i + result·(value i+1 - value i).
  - Byte [t+6] (`007AE392`-`007AE3E5`):
    - 0, or anything other than 1, returns v.
    - 1 with `comiss v,0` / `ja` not taken (v ≤ 0 or NaN) returns 0.0.
    - Otherwise xmm0 = 10.0, xmm1 = (1.0 - v)·(-4.8), and the function tail-jumps to `00861F6E`.
- **`007B5580`**: exact.
  - n = qword [rcx+0x18]. A null n leads to `0019C5D0(rsp+0x20, 0x100, 01CB4568)`. The buffer spans `rsp+0x20` up to the cookie slot at `rsp+0x120`, so it is 0x100 bytes.
  - `cmp eax,0xff` / `jl` (signed) / `sub eax,2`.
  - The newline is stored at `[rsp+0x20+sext(len)]` (`007B55C7`) with no compare before it.
  - The index len + 1 is sign-extended and compared unsigned with `cmp rcx,0x100` / `jae` → `007B5684` → `call 00809728` (`007B55CF`/`007B55D6`). Otherwise the terminator is stored.
  - The function then calls `OutputDebugStringA` and `007A5570(2, buffer)` and returns -1 after the cookie check.
  - Non-null n:
    - qword [rcx+0x18] = qword [n+0x10] (`007B561B`/`007B561F`).
    - Empty list (qword [rcx+0x20] == 0): n goes to +0x28 and +0x20, and [n+0x10] and [n+8] are zeroed.
    - Otherwise [n+8] = qword [rcx+0x28], [n+0x10] = 0, and the old [rcx+0x28] is re-read at `007B5647` (before the store at `007B564F`) and gets n at +0x10. Then [rcx+0x28] = n.
    - `or dword [n+0x1C],1`, [n+0x20] = `r8`, `inc dword [rcx+0xC]`, and dword [n+0x18] goes to [rdx] behind a null test. The function returns 0 with the cookie check.
- **`007E2EB0`**: exact.
  - `cmp byte [rcx+0x94],0` / `jbe` returns 0 for a zero count (`007E2ED0`/`007E2ED7`). The loop bound is re-read with `movzx` each step (`007E2F05`), compared by `jl`.
  - o = qword [r14] with r14 = rcx+0xB0+8i (`007E2EE0`). There is no test on o.
  - EnterCriticalSection(o+8), qword [o+0x98], LeaveCriticalSection(o+8) (`007E2EEA`-`007E2EFA`).
  - Compare with the saved `rdx` (`007E2F00`). A match returns qword [rbp+8i+0xB0], read again from the array at `007E2F34`.
  - If nothing matches, the function returns 0 (`007E2F16`).

- **Absence claims.** "No range test" in `007B5580` was checked against the instructions between `007B55BD` and `007B55C7`, which contain no conditional jump. "No null test on o" in `007E2EB0` holds because the body's only conditional jumps are at `007E2ED7`, `007E2F03` and `007E2F14`.

## SWE2-AUDIT-SPEC limits

- Body statements only. This review does not interpret the curve, the dB-style `powf(10, …)` conversion, or what the list or the controller array represent.
- `00809728` was read only as far as its call to `0080973C` with `ecx` = 8. The row names it only as the target of the failing compare.
- The applier reported `ALREADY`, so the page text was taken to be the `rows.json` text.
