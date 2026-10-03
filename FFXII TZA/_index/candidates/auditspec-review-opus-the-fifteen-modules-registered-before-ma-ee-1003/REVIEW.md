# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-fifteen-modules-registered-before-ma-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-FIFTEEN-MODULES-REGISTERED-BEFORE-DE0DC` · Package: `_index/candidates/opus-the-fifteen-modules-registered-before-ma-ee-1003/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

Three rows (`00617810`, `006BC540`, `007A15A0`) are exact, and both of OPUS's corrections hold. Three rows need narrowing:

- **`006A5C00`:** one pointer level is wrong.
- **`005FD2A0`:** the condition on one free call is missing.
- **`005BFC40`:** one claim about the data goes beyond what the body shows.

## SWE2-AUDIT-SPEC narrowings

1. **`006A5C00`, pointer level.** Byte `+0xE8` is read through the cast's output record. It is not a byte of `02E48BD0`. The comparisons are made against qword `+0x28` of that record (`[rsp+0x90]`, with the record at `r9` = `rsp+0x68`); the byte is `[[rsp+0x88]+0xE8]`, which is reached through the record's qword `+0x20`. Replace

   > a hit not on `02E47ED0` (one on `02E48BD0` with byte `+0xE8` = 1 skips the sample) gives

   with

   > a hit whose output record (`r9`) holds a qword `+0x28` other than `02E47ED0` (one whose qword `+0x28` is `02E48BD0` and whose qword `+0x20` points to an object with byte `+0xE8` = 1 skips the sample) gives

   and replace

   > a miss or a hit on `02E47ED0` gives the base and 0

   with

   > a miss or a hit whose record qword `+0x28` is `02E47ED0` gives the base and 0

   Sites: `006A5E0B mov rax, [rsp+0x90]` / `cmp rax, r15` (`r15` = `02E47ED0`) / `cmp rax, r14` (`r14` = `02E48BD0`). Then `006A5E21 mov rax, [rsp+0x88]` / `006A5E29 cmp byte ptr [rax+0xE8], 1`. The 16 bytes at `rsp+0x88` are zeroed before every cast (`006A5DA6`).

2. **`005FD2A0`, conditional free.** Replace

   > (freeing the old via `005F01B0`; a failed allocation keeps it)

   with

   > (freeing the old via `005F01B0` with its count when it differs from the new array and the top bit of `02CB8470` is clear; a failed allocation keeps it)

   Sites: `005FD4A7 cmp rcx, rsi` / `je` and `005FD4AC mov edx, [02CB8470]` / `shr eax, 0x1F` / `not al` / `test al, 1` / `je`. The call is `005FD4C1`. This is the same top-bit test the row already states for `005F03A0`.

3. **`005BFC40`, data claim.** The body reads the list from front to back. It skips entries below the start dword and then consumes an entry only on an exact match. It never checks the order, so "sorted" is a claim about the data. Replace

   > the next unconsumed entry of a sorted dword list

   with

   > the next unconsumed entry of a dword list (read front to back; the body does not check its order)

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 6 functions, 30 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 6 rows, 30 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against a full linear decode of the certified image (SHA256 73461D08..., capstone, function-list extents):
  - `005BFC40` (547 B; one push, so the 6th argument is at `[rsp+0x38]`). Source `rdi` = `[[rdx]]`; destination `rbx` = `[rcx]`. The count `esi` is dword `[6th+8]` and the start `r11d` is dword `[6th+0xC]`. List: `rcx` = dword `[r9]`, count = dword `[r9+rcx]`, entries from `r9+rcx+4`. The pre-skip runs while an entry is below `r11d` (`005BFC77 cmp` / `jae`, unsigned). Unrolled by four: `cmp esi, 4` / `jb`, loop `ecx < esi-3` (`005BFDE5 jb`), stride 0xA0 = 4 x 0x28. Each copy is dwords `+0`..`+0xC`, an xmm `+0x10`, and a qword `+0x20`, which is the whole 0x28-byte record. `005BFCA9 cmp eax, [rdx]` with `eax` = index + start (`+1`, `+2`, `+3` in the unrolled arms); on equality the entry pointer advances and the copy is skipped. The single loop matches, with its first copy at `005BFE16`. Returns `xor eax, eax`.
  - `005FD2A0` (703 B). The first block is as stated: `005F03A0(old, count & 0x7FFFFFFF)` is called only when the pointer differs and the top bit is clear. Then `02CB8450` <- `02CB7DA0` and `02CB8448` <- 0x80000017. The loop runs 0x17 times, with `rdi` stepping by 0x18 from `02CB7DA8` and `r14` by 0x10 from `00D3EB38` (.rdata). The string pointer is `[r14-8]` (`005FD32A`; the correction holds), and `strlen+1` bytes are copied by `00861EBA` (`005FD344`). `rsi` is aligned up to even each step, the store `[rdi]` = `rsi+1` is skipped only if `rsi` is odd (it never is after the align), and an old non-null even value is first passed to `00584730`. Bytes `[rdi-6]`/`[rdi-5]` <- low bytes of `[r14]`/`[r14+4]`; word `[rdi+8]` = 0; word `[rdi+0xA]` keeps bits 13..15. `005FD700(8, [02CB8450], count, &out, 006372B0())` (`005FD3D6`). The word store to `02CB8458` is `(out+0xF) & ~0xF` (`005FD3EF`; the correction holds). `edi` = `(ecx+1) & ~1`, and `0017D260(size*edi, 4)` feeds `00861EC0(ptr, 0, size*edi)` (`005FD422`). `02CB8460`, `02CB8468` = `edi`, `02CB84A8` = 0. The array is replaced only when `edi != [02CB8470]`: `edi` x 0x50 bytes, each element built by `00615550`. A failed allocation with `edi != 0` jumps to the element loop and keeps the old array (`005FD49C`). Element loop over `edi`: `ecx` = `[e+0x18] & 0x7FFFFFFF`, with `cmovne` giving 1 for 0. If that is not 8, `00628050(e, 8)` (`005FD508`) runs, and a 0 result clears `[e+4]`. `[e]` = 0x5E4 (`005FD515`). Then `00861EC0(02CB84B0, 0, 0xB30)` and `005CD0A0(02CB8480)`, returning 0. The only defect is the unstated free condition (above).
  - `00617810` exact (428 B). `006388C0(02CF1C40)` (`0061782B`). Three guards, `02CF6B78`, `02CF6BD8` and `02CF6C38`, each handled the same way. `cmp guard, epoch` / `jle` skips, so the guard is entered only when it is greater (signed). `008092FC` (`0061785E`) then `cmp -1` / `jne`. `00632960(record, 02CF1C40, 00630180(), name, 0x80|0x84|0x88, 0x10, 0, 0)` with records `02CF6B20`/`02CF6B80`/`02CF6BE0` and names `00D5517C`/`00D55184`/`00D5518C` (.rdata) (`006178A2`, `00617915`). `00808B90(008AECF0|008AED00|008AED10)`, then `0080929C(guard)`. Tail `jmp 00639450` with `rcx` = `02CF1C40` (`006179B7`).
  - `006A5C00` (1395 B; the third argument is spilled to `[rsp+0x180]`). A null qword `+8` gives 0x15 (`006A5C18`). The eye is `[rdx..+8]` plus floats `+0x38..+0x40`. The base is eye minus `[+0x68..+0x70]` x `[+0x14]`; its height is raised by `comiss` / `jbe` to `[rdx+4]+[+0x18]` when that is higher, then `+[+0x2C]`. The 0.1 constant `008C5F6C` (.rdata) seeds both the weight sum and the accumulator (base x 0.1). The loop runs 0x14 times, with offsets stepping 0x10 from `rcx+0x78` and weights 4 bytes from `rcx+0x1B8`. `006A1A70([rcx+8], &eye, &target, &record, 0xF)` (`006A5DFE`). The hit point is `[rsp+0x68..]` and the normal `[rsp+0x78..]`; shift = p + n x `[+0x1C]` - target; the value is 0.1 x `00861F14`(|shift|^2). `minss 0.5` (`006A5EF1`, `01CEBB70`) / `maxss -0.5` (`0090030C`) x `min(third` x `[+0x30], 1.0)` + the old weight is stored back to the weight slot and weights the point. Average = acc / sum. `006A5FFF comiss [+0x20], dist` / `jbe`: on a shortfall, avg.y += shortfall x `[+0x34]` and eye.y += 0.8 x that (`008F3108`). If third > 0 and `[+0x24]` > 0: `00861F6E(xmm0` = `[+0x24]`, `xmm1` = third) (`006A60C0`; the correction holds), then `subss 1.0`, `minss 1.0`, `maxss 0`, which lerps `+0x48..+0x50`. If third > 0 and `[+0x24]` <= 0, the average is stored. If third <= 0, `+0x48..+0x50` are untouched. In all cases the eye goes to `+0x58..+0x60` and the result is `xor eax, eax`. The only defect is the pointer level (above).
  - `006BC540` exact (134 B). `ecx` = 0 -> `xor eax, eax`. `0017D260(ecx*0x18, 8)` (`006BC567`); null -> returns that null (`006BC572`). Otherwise `ecx` copies of 0x18 bytes (xmm plus qword, `006BC58F`/`006BC59B`, loop `006BC5A4`) and the block is returned.
  - `007A15A0` exact (149 B). `rbx` = `[rcx+0x18]`, mapped to null when it equals the header `rcx+0x18`, and the same for each next `[node]`. Non-null `[+0x38]`: new = byte `[[+0x38]]` (`007A15D2`); `+0x31` = 1 only when old `+0x30` = 0 and new = 1 (`007A15DD`), else 0; `+0x32` = 1 only when old = 1 and new = 0 (`007A15EF`), else 0 (`007A15FB`); `+0x30` = new. Else, non-null `[+0x40]`: `0079A5F0(node, dword [[+0x40]])` (`007A160E`).
  - Anchors: all thirty are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
