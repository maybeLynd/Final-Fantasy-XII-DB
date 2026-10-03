# SWE2-AUDIT-SPEC review: OPUS engine_explained interior citations (opus-sqex-sd-sound-driver-architecture-ee-1003-3)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SQEX-SD-SOUND-DRIVER-ARCHITECTURE-EE-5C4A8` · Package: `_index/candidates/opus-sqex-sd-sound-driver-architecture-ee-1003-3/` · Page: `18-Audio/sqex-sd-sound-driver-architecture.md` (commit 5f91e98be)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 3 rows and their 15 anchors are correct against the bytes; no row text changes. The only narrowing is to the package README, which says the second agent checked "rotation helpers' directions". No such helper exists in these bodies: the phrase is template text from the MSVC ordered-container package.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh from the package folder without `--apply` -> `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0` (exit 0), the same as the committed `.out`. `git status` on the page and the package was clean afterwards (reviewed at HEAD `f49bb4021`).
- `rows.json`: 3 rows, 15 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** (3 of 3; fewer than 15 exist) read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...), with rip targets resolved to their sections and IAT names read from the import table:
  - `007B9050` exact.
    - Entry: `test r9d` / `jne` (`007B9088`), else -1. The stack arguments are argument 5 qword `[rsp+0x340]` -> `+0x70`, argument 6 `L` = `[rsp+0x348]` and argument 7 dword `[rsp+0x350]` -> `+0x484` (frame 0x318 below entry).
    - Dword `+0x500`: `lea [r8*4]` for `r9d==2`, `lea [r8+r8]` for 1, else 0, then `shl 8`. Then `007AD550(movsxd +0x500, 0)` is called twice, into `+0x508`/`+0x510` (`007B9119`).
    - Lookup base `r13` = qword `02EAD0A8` (`.data`). For null `L` or `[L+0x20]==0` there is one entry, `(007AC410(r13,0), 0x3F800000)`, with count 1. A negative count is caught by `test`/`jle` and gives zero entries. Otherwise the loop runs `i < [L+0x20]` (signed `jl`) over `007AC410(r13, [L+8i])` (`007B9165`) and keeps an entry only when the result is non-null, with `[L+8i+4]`.
    - `007AEA20` (`007B91E7`) receives `rcx+0x68`, `edx`, `r8d`, `r9d`, `rcx+0x10`, `&entries`, the count, qword 0, dword 0 and byte 1.
    - `jns` on the result. The negative path:
      - `0019C5D0(buf, 0x100, 01CB52A0)`, where `01CB52A0` is `.rdata` "[sead][!!error!!]ExternalSourceVoice Initialize failed".
      - Newline at the clamped length; `cmp 0x100` / `jae` goes to `00809728`.
      - `OutputDebugStringA` through IAT `008C2120`, then `007A5570(2, buf)`.
      - Qword `+0x68` = 0, and it returns `r`.
    - Otherwise:
      - Identity-pattern fill: 1.0 where row == column, index `i + j*r8d`, for `j < 007AECE0()`.
      - `call [vtbl+0x40]` on qword `+0x68`, then `007B9AF0(rcx, xmm1=0)`.
      - Append under the critical section at `02EADD48` (Enter/Leave through `008C20B8`/`008C20C0`). An empty tail `02EADD30` also sets head `02EADD38`; otherwise `+0x4F8` = the old tail and the old tail's `+0x4F0` = `rcx`. Then `inc dword 02EADD40`.
      - It returns `call [vtbl+0x18]` (`007B9355`).
  - `007DCE20` exact.
    - Dword `[c+8]` -> `+0xA4`, then `007DCC60(rcx+0xA8, [c])` (`007DCE5F`).
    - Signed loop `i < +0xA4` of `007AD550(0x200, 5)` (`007DCE8A`). Then two calls `007AD550(movsxd(+0xA4) << 9, 5)` into `+0x90`/`+0x98`, and dword `+0xA0` = 0.
    - `z` = `4*([c]*([c+4]*[c+8]+0x10) + [c+8]*0x218) + 0x100`, from `007DCEDE..007DCEF8`.
    - `p` -> `+0x38`, then `001218B0([c], [c+4], [c+8], p, z, rcx+0x40)` (`007DCF2A`).
    - `007AEA20(rcx+0x48, [c+0xC], [c+8], 2, rcx+8, &b, 1, 0, 0, byte 0)` (`007DCF92`), where `b` = `(007AC410(qword 02EAD0A8, 0), 1.0)`.
    - `memset` (thunk `00861EC0` -> IAT `008C2A60`) clears 0x100 bytes, and 1.0 is stored at `[i][i]` for i < 8.
    - Virtual calls on a re-read qword `+0x48`:
      - `[vtbl+0x40]` with the matrix.
      - `[vtbl+0x48]` with `rdx` = qword `02EAE098`, `r8` = `movsxd` dword `02EAE090`, `r9` = 0 and dword 0 (`007DD007`).
      - `[vtbl+0x18]`.
    - Returns 0; the cookie is `01F44830`, checked by `00808C40`.
  - `007DFBB0` exact.
    - Word `+0x72` -> `+0x74` (`007DFBD8`), then `n` = `movsxd 007AECE0()`.
    - `cmp word +0x74, 0` / `jg` skips the clear, so the clear runs on signed `<= 0`. The clear path:
      - `memset(qword +0x30, 0, 007AECD0())` (`007DFBFE`).
      - Under `EnterCriticalSection(rcx+8)`, `n` dwords at qword `+0x60` are zeroed. Byte `+0x70` != 0 also zeroes `n` dwords at `+0x68`.
      - Byte `+0x70` = 0 before the leave.
    - `f` = `setg` on word `+0x74`. Block `(qword +0x30, k = 007AECF0(), n)` at `rsp+0x20`.
    - Loop over `i < dword +0x58`: `[vtbl+8]` returning `al==0` (`test al`/`jne`), and then either word `+0x74 > 0` or `[vtbl+0x10]` returning non-zero `al`. When both hold, it calls `[vtbl+0x18](o, &block)` (`007DFD10`) and sets `f`.
    - Scaling is skipped by `ucomiss` float `+0x5C` vs `.rdata` 1.0 `01CEBBA8` / `je`, so equal or unordered skips it. Otherwise `mulps` runs on both halves of the `k` 32-byte blocks (`007DFD57`).
    - Under the critical section:
      - 32 bytes at qword `+0x60` are zeroed.
      - Each block's absolute values (`andnps` with the `.rdata` sign mask `01CEBDA0`) are folded in by `maxps` (`007DFDB4`).
      - Byte `+0x70` != 0 copies the result to qword `+0x68`; otherwise `+0x68` = `maxps(+0x68, +0x60)`.
      - Byte `+0x70` = 0.
    - Returns 0 on both paths (`007DFE00`).
- Anchors: all 15 are strictly inside their bodies, decode to the recorded mnemonic, and sit on the clause they support.
- Family-declaring-page rule (progress.py `cite_credits` / `family_rule_inputs`): the SQEX page declares no accepted family. All 3 functions are members of `SQEX SEAD sound library span`, which is declared elsewhere, so on this page the base rule applies: a strictly interior anchor credits `engine_explained`, and the bodies are 841, 542 and 626 B. "All 3 rowed functions now measure A" is consistent with the rule in force.
- Limits hold: body statements only, static evidence, no runtime claim. The drafter and the second local agent are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowings

README only (`_index/candidates/opus-sqex-sd-sound-driver-architecture-ee-1003-3/README.md`); `rows.json` row text is unchanged.

1. Paragraph 1 claims the second agent checked rotation helpers. None of `007B9050`, `007DCE20` or `007DFBB0` calls one; the phrase belongs to the red-black-tree package.
   - Old: "read every one of the 3 rows against the disassembly, including the rotation helpers' directions and every named import: all 3 stood."
   - New: "read every one of the 3 rows against the disassembly, including every named import (`OutputDebugStringA`, `EnterCriticalSection`, `LeaveCriticalSection`, `memset`) and every virtual-call slot: all 3 stood."
