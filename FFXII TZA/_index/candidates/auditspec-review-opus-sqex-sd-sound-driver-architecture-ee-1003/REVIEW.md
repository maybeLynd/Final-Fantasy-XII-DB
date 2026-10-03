# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-sqex-sd-sound-driver-architecture-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SQEX-SD-SOUND-DRIVER-ARCHITECTURE-EE-1003` · Package: `_index/candidates/opus-sqex-sd-sound-driver-architecture-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `18-Audio/sqex-sd-sound-driver-architecture.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 8 rows, fewer than the 15 the request asks for, so all 8 were read clause by clause against the bytes. All 8 are correct, and so are their 40 anchors. Two wording notes below are non-blocking. No row changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` was run without `--apply` (it writes only with `--apply`), from the package directory, under the analysis venv python with `-B`. Output: `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit 0. This matches the committed `.out`. `git status` on the page and the package was clean afterwards.
- **Page text.** Each row's `text` appears verbatim on the page (8 of 8).
- **Anchors.** Every anchor is an instruction boundary in its function's disr listing, has the recorded mnemonic, and sits on the clause it supports. None of the listings is cut: each ends at `ret`, or for `007AA320` at the `__report_rangecheckfailure` call, at the census size.
- **Rows, clause by clause** (the disr.py listing for each `fn`):

| fn | verdict | decisive instructions |
|---|---|---|
| `007A45C0` | correct | `007A45E9` `lea rcx,[rsp+0x20]` → `007A45F4` call `007AB460`. `007A45FB` `jns` (negative → `or eax,-1`). Stores through the qword at `rsp+0x20`: `007A4607` dword 3 to `[p]`, `007A4612/14` `[rdi]`→`[p+8]` (rdi = incoming rcx), `007A461C` xmm7 (= incoming xmm1)→`+0xc`, `007A4626` xmm6 (= xmm2)→`+0x10`, `007A4630` ebx (= r9d)→`+0x14`. `007A4638` returns `007AB550(p)`. Cookie at `007A4645`. |
| `007A9F40` | correct | Factor 1.0 from `01CEBBA8` (0x3f800000) at `007A9F56`. Count `movsxd [rcx+0x78]`, `jle` at `007A9F61`. Cursor `[rcx+0x38]+0x14`, stride 0x30 at `007A9FB8`. `ucomiss`/`jne` at `007A9F87`: when equal, factor = `[rbx-8]` = `+0xc`; otherwise `+0x10 / +0x14` (`007A9F9C`) with edx = `+0x1c`, call `007A9E50`, then `*(+0xc - +0x8) + +0x8` (`007A9FA5..B3`). `mulss xmm7` at `007A9FBC`. `* [rsi+0x48]` at `007A9FC6`, or at `007A9FEE` on the count ≤ 0 path. |
| `007AA320` | correct | `movzx` word `[rax+4]` with rax = `[rdx+8]`, then `neg dx` / `test dx,dx` / `jle` (signed 16-bit) at `007AA346..4C`. `movsx ecx,dx` → call `007AAA20`, result stored to `[rbx+0x58]` (rbx = rcx). `cmp dword [rax+0x10],0` / `jne` → return 0. Otherwise `0019C5D0(rsp+0x20, 0x100, 01CB44B0)`, with r9 not written in this body. `cmp eax,0xff` / `jl` / `sub eax,2` (signed). Byte 0xa at the index, then a zero byte at index+1 behind `cmp rcx,0x100` / `jae` → `00809728`. Then `call [008C2120]` with `rsp+0x20` and `007A5570(2, rsp+0x20)`; returns -1. Cookie at `007AA3C7`. |
| `007B8C80` | correct | Constants decoded from their bits: `00D22590` 0.15915494, `01CEBB70` 0.5, `01CEBC78` 6.2831855, `008C5F70` 1.5707964, `01CEBC50` 3.1415927, `00915FE4` -1.5707964, `00915620` -3.1415927, `01CB519C` 2.7525562e-06, `01CB51A4` 0.00019840874, `01CB51AC` 0.008333331, `009159F4` 0.16666667, `01CEBBA8` 1.0. Polarity: the `jb` at `007B8C94` subtracts 0.5 when x < 0. The `jbe` at `007B8CC6` gives pi - r only when r > pi/2. The `jae` at `007B8CD9` gives -pi - r when r < -pi/2. The Horner chain `007B8CF5..D38` equals the stated polynomial, with c = `[01CB5194]` (0x32cd365b ≈ 2.389e-08). |
| `007DFE30` | correct | Incoming registers are intact at the `007AECF0` call: rdx, rcx and xmm2 are only copied before it. `shufps xmm2,xmm2,0` at `007DFE59`. `test r8w,r8w` / `jg` (signed word `[rdi+0x72]`) at `007DFE64`. A count that is not positive skips both loops (`007DFE68`, `007DFEA5`). Store loop: `mulps` then `movaps` into the destination at `[rdi+0x30]`. Add loop: `addps` onto the destination at `007DFEBF`. `inc r8w` stored to `+0x72` at `007DFEE7`; `xor eax,eax`. |
| `007E0550` | correct | Byte-for-byte the same form as `007DFE30`, with the word at `+0xca` (`007E056D`, `007E0607`). Anchors `007E0568/7C/87`, `007E05DF` and `007E0607` match. |
| `007E0650` | correct | `01CB8360` stored to `[rcx]` at `007E0660`. Three calls through `[008C20B0]` with rcx+8, rcx+0x30 and rcx+0x58. Then every store in the order stated (`007E0683..070D`), including -1 to dword `+0xa8`, the qword at `+0xac` and the 0x3f800000 dwords at `+0x100/104/108/294`. Returns rbx = rcx. |
| `007E0980` | correct | `cmp r8d,8` / `jle` (signed) and `test r9d,r9d` / `je` → `or eax,-1`. The function is a leaf with no push, so `[rsp+0x28..0x50]` are arguments 5 to 10. Arg 6 → `+0x88` and arg 5 → `+0x210`. edx → `+0x94`, r9d → `+0x90`, r8d → `+0xac`, 1 → `+0x80`. Arg 10 (movsxd) → `+0x290` and is the count of qwords copied from the arg-9 pointer to `rcx+0x270` (destination = r10 + 0x270 + offset). Arg 8 → `+0x268` and is the count of 16-byte `movups` blocks from the arg-7 pointer to `rcx+0x218` (`[r10'+rax+0x208]` after the `+0x10` step). Returns 0. |

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing. Non-blocking wording notes:

- `007A45C0`, "the returned record `p`": `007AB460` returns a status in eax (0, or 0x80000001 on its failure path at `007AB4FC`). It hands the record back through its pointer argument (`007AB507` `mov [rbx],rax`, with rbx = the `rsp+0x20` slot). The row names the `rsp+0x20` argument, so the clause is not false, but "the record `p` that call stores at `rsp+0x20`" would be exact.
- `007A9F40`, "when its float `+0x14` equals 0.0": `ucomiss` / `jne` also takes the "equal" arm when `+0x14` is NaN, because the parity flag is not tested. The row is exact for ordered values.
- `007E0980`: when a count is zero or negative, the matching copy loop does not run (`jle` at `007E09D8` and `007E0A16`). "copies that many" already covers that.
