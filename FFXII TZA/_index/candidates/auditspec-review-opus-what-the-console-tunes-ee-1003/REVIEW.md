# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-what-the-console-tunes-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHAT-THE-CONSOLE-TUNES-EE-1003` · Package: `_index/candidates/opus-what-the-console-tunes-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 5 rows (25 anchors) were read clause by clause against the bytes. The package has fewer than 15 rows, so every row was checked. No defect was found.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `interior_applier.py` without `--apply` only verifies. It was run in place with `-B` under the analysis venv python: `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `.out`. The run left the package and the page unchanged.
- **Page text.** Each row's `text` occurs exactly once on the live page. The 130 B, 161 B and 159 B sizes match the disr extents 0x82, 0xa1 and 0x9f. No extent has a jump table, and each listing ends at its `ret`/`jmp`.
- **`001FF6B0`: exact.**
  - The prologue sets rbx = rcx and rsi = rdx. `cmp dword [rcx],3` is at `001FF6CF`; when equal, `je 0x1ff717` goes straight to the tail.
  - Otherwise it calls `002001F0` at `001FF6D4`. No argument register is changed before that call, so "with the incoming registers" holds.
  - It then stores 3 to `[rbx]` and calls `00210EC0` with `ecx = 0x38` (`001FF6E4`).
  - On a non-null result: `lea rdx` -> `008F4120` (bytes `EASTL map\0`), `rcx = rsp+0x50`, call `001EDF00` (`001FF702`). Then `rcx` = block and `rdx` = that result, call `001FE510` (`001FF70D`).
  - `001FF713 mov [rbx+8],rax` stores either `001FE510`'s return or the null block (the `je` at `001FF6F4` reaches it with rax = 0).
  - The tail sets `rdx = rsi` and `rcx = [rbx+8]`, then `jmp 001FF4F0` (`001FF72D`). Both paths reach it.
- **`0021D280`: exact.**
  - `cmp dword [rcx+0x48],0` / `jbe` at `0021D2A0`: unsigned `<= 0`, so the branch is taken only on zero, and it returns `xor eax,eax`.
  - n = `[rcx+0x30]`, v = `[n+0x20]` (spilled to `[rsp+0x50]`), then `dec dword [rcx+0x48]` (`0021D2AF`).
  - Calls `0016D6D0(n)` and `0016DA60(n, rdi+0x28)`.
  - Then `rcx = rdi+0x50`, `rax = [rcx]`, `rdx = n`, `r8d = 0x28`, `call [rax+0x18]` (`0021D2D6`).
  - Then `rcx = rdi+0x58`, `rdx = rsp+0x28`, `r8 = rsp+0x50`, `r9d = movzx byte [rsp+0x50]` (the low byte of v), `call 00199DB0` (`0021D2ED`).
  - With `test rsi,rsi`: v non-null calls `00225160(v)` (`0021D2FF`) and returns its rax; otherwise it returns 0.
- **`00220550`, `002206B0`: exact.** Each masked body is identical to `0021D280` in 42 of 42 instructions, except the final callee: `002255C0` at `002205CF` and `00225880` at `0022072F`, as each row states.
- **`007A45C0`: exact.**
  - rdi = rcx and ebx = r9d. xmm1 and xmm2 are preserved across the call in xmm7 and xmm6.
  - `call 007AB460(rsp+0x20)` at `007A45F4`; `test eax,eax` / `jns` at `007A45FB` (signed). A negative result gives `or eax,-1`.
  - p = qword `[rsp+0x20]`. The stores are `[p]` = 3 (`007A4607`), `[p+8]` = dword `[rdi]`, `movss [p+0xc]` = xmm1, `movss [p+0x10]` = xmm2, and `[p+0x14]` = r9d (`007A4630`).
  - Then `call 007AB550(p)` (`007A4638`), whose eax is the return.
  - Both paths join at the cookie check `call 00808C40` (`__security_check_cookie`, with cookie `01F44830` xor rsp).
- **Anchors.** All 25 are instruction boundaries carrying the recorded mnemonics. Each lies on its clause: the state test, the first call, the allocation and the insert call, and the head store; the zero-count branch, the decrement, the vtable call, the `00199DB0` call and the final callee; and the status call, the sign branch, the first and last record stores, and the commit call.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Notes (non-blocking):
- `007A45C0`: "the returned record `p`" means the record that `007AB460` writes through its pointer argument. `007AB460` stores the record to `[rcx]` (`007AB49E` on its empty path, `007AB507` on its pop path) and returns a status in eax (`0x80000001` on failure). So p is an out-parameter, not rax. The sentence's `007AB460(rsp+0x20)` makes this recoverable. A stricter wording would be "of the record `p` that `007AB460` stores to qword `[rsp+0x20]`".
- The package lists 4 functions as missing (`001967D0`, `001FF4F0`, `00200BF0`, `00202930`). They carry no row and remain entry-only on the page; nothing here credits them.
