# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-animation-channel-binding-and-transform--ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-ANIMATION-CHANNEL-BINDING-AND-TRANSFORM-EE` · Package: `_index/candidates/opus-animation-channel-binding-and-transform--ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 7 rows. The request asks for at least 15 rows, so all 7 were checked. Each was checked clause by clause against an independent decode (`disr.py`). Every anchor is an instruction boundary inside its body with the recorded mnemonic. Six rows are exact. In `005C6D90`, two clauses give a 16-bit store the value of a 31-bit field. The narrowing below rewords that row only.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** I read the source first: without `--apply` it writes nothing. `interior_applier.py -B` printed `VERIFY 7 functions, 35 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page has a 2026-10-02 block and a 2026-10-03 block with distinct headings. `ALREADY` was matched on the 2026-10-03 block (page lines 1132-1144), which holds exactly these 7 rows. The page is clean in the working tree and committed at `HEAD`.
- **Extents.** Every listing ends in `ret`, with branch targets inside and no jump table.

| fn | verdict | decisive bytes |
|---|---|---|
| `005A7AB0` | exact | `005A7AC0`-`005A7AC8` return 0 on a null `rdx` or `rcx`. `005A7AD0`-`005A7ADD`: `lea r11,[obj+0xa0]; mov r9,[r11]; cmp r9,r11; cmove r9,0` (the sentinel ends the walk). `005A7AE6`-`005A7AED` skip a null `+0x18`. The byte compare at `005A7B00`-`005A7B11` runs to the terminator. `005A7B15` `je` returns the element (`005A7B44`). The next element is `[elem]` with the same sentinel test (`005A7B17`-`005A7B20`). The chain step at `005A7B29` is `[obj+0x78]`. The end returns 0 (`005A7B32`). |
| `005AC9B0` | exact | `005AC9C9`/`005AC9D0` store `00D315B0`. `005AC9D3`-`005AC9E8`: `shr 0x1f; not al; test al,1` (bit 31 clear, so not negative) and non-null `[rcx+0x20]`, then `00584730([rcx+0x20])`. `005AC9EE`-`005AC9F4` zero `+0x20`/`+0x18`. `005AC9F7`/`005AC9FE` store `00D312F0`. `005ACA01`-`005ACA20`: with bit 1 set, bit 4 clear calls `00584730(rcx)` and bit 4 set calls `0016D6A0(rcx, 0x28)`. `005ACA26` returns `rcx`. |
| `005C5040` | exact | `005C5044`-`005C5064` return 0 on a null `[rcx+0x10]` or zero low-31 count (`and edi,0x7fffffff; jbe`). Element fetch: count >1 reads `[[base+8]+i*8]` (`005C508B`/`005C508E`); count ==1 reads `[base+8]` itself (`005C5094`-`005C509D`, `cmovne rax,r9`). `c` comes from `005C50A5`/`005C50A8` (`btr 0x1f`). `b` comes from `005C50AC`-`005C50B9` (`test [+0x18],0x7fffffff; cmove`). `005C50BF`-`005C50D5` compute `((2c+b+2)&~1)<<4`, then `+0x1f`, `&~0xf`. `005C50BC`-`005C50CC` compute `(6c+0x11)&~0xf`. `005C50D8` adds them. `005C50DD` `cmova` (unsigned) gives the running maximum from 0. |
| `005C6D90` | narrowed (two word widths) | `005C6DAA` sets `s=[rcx+0x18]`. `005C6DC6`/`005C6DCD`/`005C6DD5` store `+0`=0x30, qword `+4`=2 and `+0xc`=0. `005C6DD9`-`005C6DEA` make the call `[vtbl+0x20]` on `[rcx+0x20]`, or `xorps` when it is null. `005C6DF1` is the `movss` to `+0x30`. `005C6DF6`/`005C6DED` store the words `+0x34`/`+0x36` from the `btr`-masked `[s+8]`/`[s+0x18]`. `005C6DFB` stores `+0x18=[s]`. `005C6DFF`/`005C6E08` store `+0x10`, the `movzx` word at `[s]`. `005C6E14` stores `+0x28=[s+0x20]`. `005C6E18`-`005C6E26` store `(k*0x58+0xf)&~0xf` to `+0x20`. The return is 0x40. |
| `005C6F20` | exact | `005C6F53`-`005C6F73` store `+0`=0x10, `+8`=0, then `01F2CE40`, `01F2CE70`, `01F2CE58` at `+0x10/+0x18/+0x20`. `005C6F4F`/`005C6F5A` set `n`= low 31 of `[t+0x20]`. The entries are `[t+0x28]`, stride 0x18 (`005C6FEE`). The record is `[rdx+0x20] + entry.dword[+0xc]*0x30` (`005C6FAA`-`005C6FB1`), and the result resets to 0 at each iteration (`005C6FA7` is inside the loop). Type 0: `005C6FD9`-`005C6FE4`, `cmp [+0x10],0x80`, `cmovae` 0, else `02CAEB60`. Type 1: entry qword `+0` against the three pointers (`005C6FC0`-`005C6FD0`), then record qword `+8` (`005C6FD2`). Other types give 0. `005C7008` writes the terminator. The return is `((n*8+0x2f)&~0xf)+0x10` (`005C6F6B`/`005C6F77`/`005C7005`). |
| `005C9F30` | exact | `005C9F44`-`005C9F52`: `c`=`btr`-masked `[+0x18]`; equal returns 0. `005C9F5D`/`005C9F60` skip the reallocation when edx equals the whole dword. `005C9F62`-`005C9F6F` call `005E3040(edx, [rcx+0x20], min(edx,c))` (`cmovb`, unsigned). `005C9F77`-`005C9F80` return 0xd when the result is null and edx is non-zero. `005C9F85`-`005C9F9F` free the old pointer when it differs, the sign is clear and it is non-null. `005C9FA4`/`005C9FA8` store the pointer and edx. `005C9FAB`/`005C9FAD` `cmp esi,edi; jae`, then zero qwords `c..edx-1` (`005C9FC0`-`005C9FD1`). The return is 0. |
| `005CB4F0` | exact | `005CB4FA`-`005CB50C` call `[vtbl(rdx)+8](rdx, rcx)`. `005CB50F`/`005CB511` return with `al`=0. Loop count `[rcx+0x18] & 0x7fffffff` (`005CB534`). Elements `[[rcx+0x20]+i*8]`: a non-null element gets `[vtbl+0x18](elem, rdx, rcx)` (`005CB54D`-`005CB556`). A zero byte goes to `005CB591` `xor al,al`. After the loop, `005CB567`-`005CB573` call `[vtbl(rdx)+0x18](rdx, rcx, r8)`, and `005CB576` returns `al=1`. |

**6 of 7 exact; 1 narrowed.** All 35 anchors were checked.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: `005C6D90` (rows.json and the page's 2026-10-03 block).** The words at `+0x34` and `+0x36` are 16-bit stores: `005C6DF6 mov word ptr [rbx+0x34], r14w` and `005C6DED mov word ptr [rbx+0x36], di`. They come from 31-bit values that `btr ...,0x1f` masked at `005C6DBA` and `005C6DC2`. Each word therefore holds only the low 16 bits of its dword, and bit 31 plays no part in it. The row's "the low 31 bits" is false whenever the dword is 0x10000 or more. The full 31-bit `k` still feeds the `+0x20` product (`005C6E18 imul eax, edi, 0x58`), as the row says. Bit 31 is never written into the words, so on its own it would not refute the row: the defect is the width.

Replace:

> word `+0x34` = the low 31 bits of dword `[s+8]`, word `+0x36` = the low 31 bits `k` of dword `[s+0x18]`,

with:

> word `+0x34` = the low 16 bits of dword `[s+8]`, word `+0x36` = the low 16 bits of `k`, where `k` = the low 31 bits of dword `[s+0x18]`,

The anchors are unchanged. The rest of the row stands.

Notes (non-blocking):
- Verdict amended by the coordinating SWE2-AUDIT-SPEC reviewer after the first pass. The first pass classed the width clause as implicit. Under the exact-behaviour standard, a stated value that the store cannot hold is a defect, so it needs a narrowing.
- `005C9F30`: when `edx` equals the whole dword (bit 31 set, so `edx != c`), the body skips the reallocation but still runs the zeroing loop from `c` to `edx-1`. The row states the zeroing clause unconditionally, which matches the code.
