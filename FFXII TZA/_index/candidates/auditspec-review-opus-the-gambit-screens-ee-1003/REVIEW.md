# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-gambit-screens-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-GAMBIT-SCREENS-EE-1003-90F54` · Package: `_index/candidates/opus-the-gambit-screens-ee-1003/` (reviewed at HEAD `e06561376`) · Page: `16-UI/Gambit-Screens/the-gambit-screens.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 8 rows. The request asks for at least 15 rows read, so all 8 were read clause by clause against a raw capstone decode of the certified image (SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`, checked in this session). Seven rows are exact. One clause in `005109B0` says the incoming registers are passed to `00280120`, which reads none of them. The narrowing below removes that parenthetical.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** Without `--apply` the script writes nothing (its only writes sit under `--apply`). `interior_applier.py` with the venv python printed `VERIFY 8 functions, 40 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page block is the 2026-10-03 heading at line 417, with 8 rows ending at line 430. The page is clean in the working tree.
- **Extents.** Ends come from `.pdata`, or from `ret` followed by int3 padding where the entry has a chained fragment (`005109B0` ends `00510A33`, `00510B80` ends `00510C75`, `00510C80` ends `00510D72`). Each listing ends in `ret`, every branch lands inside it, and there is no jump table. All 40 anchors are instruction boundaries with the recorded mnemonic.

Per row:

- **`00242B90`** (`00242B90`-`00242C8C`): exact. `00242B9A`-`00242BB4`: `b` = `[[0209AC30]+0x378]`, `t` = `[b+0x20]+0x30`. `00242BB8`/`00242BBD`: `k` = word `[t+0x18+2*word[t+0x18]]`. `00242BC3`/`00242BC8`: `e` = `t` + word `[t+0x10]` + 8k. Rectangle `A` at `rsp+0x20` (`00242BCB`-`00242BFE`, with `and ax,cx`, `cx`=0xFFF, and `shr eax,0xc`). Rectangle `B` at `rsp+0x40` = `dx`, `r8w` plus the same two masked words (`00242BF9`-`00242C2A`). `00242C35`-`00242C5A`: `t` is re-read, and the byte store `[rdi+0x5c]` = byte `[t+word[t+0x12]+(b7>>4)]` + (b7&0xF). Calls at `00242C5D` (`edx`=1), `00242C72` (`rcx`=w, `rdx`=b, `r8`=&A, `r9`=&B) and `00242C7C` (`edx`=0).
- **`002CBE40`** (`002CBE40`-`002CBEC3`): exact. Cookie `01F44830` at `002CBE44`, checked by `00808C40` at `002CBEB9`. `002CBE5A`/`002CBE64`: `d` = `[g+0x2E0]`. On null, `a` = (dword 0 at `rsp+0x20`, `rcx` at `+0x28`, qword 0 at `+0x30`), and `00244F50(0x170, 002CBF80, &a)` runs at `002CBE87`. I read `00244F50`: it returns a pool slot or a fresh allocation, initialised through `002465F0`. `002CBE96` stores `d` to `[g+0x2E0]` (g re-read), then `00246AD0([0208EA28], d)` (`002CBEA5`/`002CBEAC`). For an existing `d`: `test byte [rdx+0x7c],0x20; je` skips the call (`002CBE9F`).
- **`002CC8D0`** (`002CC8D0`-`002CC952`): exact. `002CC8E5` `cmp byte [g+0xdec],0`, and a non-zero byte returns `ecx`. `002CC8FB`-`002CC907`: `sub eax,r8d`, then `cvtsi2ss xmm0,rax` on the zero-extended 32-bit value, so it is unsigned. `002CC90C`-`002CC912`: `cdq; idiv r9d` on 60 (signed), then `cvtdq2ps`. `002CC915` multiplies by `01CEBC50` (f32 3.14159), and `002CC924` divides. The thunk `00861F0E` jumps through IAT slot `008C2BB0`, whose hint/name is `sinf`. `002CC93A`-`002CC948` compute `* (float)edx + (float)ecx`, then `cvttss2si`.
- **`005109B0`** (`005109B0`-`00510A33`): **narrowed**. `005109B9` calls `00280120` and `005109C0` `jne` returns its `eax`. Five `00267E10(r14=r9)` reads (`005109D9`-`00510A01`) go to `ebp`, `esi`, `edi`, `ebx` and `eax`. Then `002D78B0(ecx=v5, edx=v4, r8d=v3, r9d=v2, [rsp+0x20]=v1)` runs at `00510A14`, and its `rax` is returned. The defect: `00280120` (`00280120`-`00280133`) is `mov rcx,[0209AC30]; xor eax,eax; cmp [rcx+0xc0],rax; sete al; ret`. It overwrites `rcx` before any read and never reads `rdx`, `r8` or `r9`. So no incoming register is passed to it.
- **`00510B80`** (`00510B80`-`00510C75`): exact. `00510B8D`/`00510B94` hold the early return. `002640C0` (`002640C0`-`002640C7`) is `mov rax,[02099D70]; ret`, so it takes no argument. Four `002650B0(b, rdi=rcx, 00267E10(rbp=r9))` calls (`00510BC7`, `00510BE0`, `00510BF9`, `00510C12`) give `p1`=`r15`, `p2`=`r14`, `p3`=`rsi`, `p4`=`rdi`. `x`=`ebx`, `y`=`eax`, then `00568460(ecx=y, edx=x, r8=rsp+0x20, r9d=0)` at `00510C38`. The `movsx` stores are `w[0]`->`[rdi]`, `w[1]`->`[rsi]`, `w[2]`->`[r14]` and `w[3]`->`[r15]` (`00510C3D`-`00510C67`). `eax` = sign-extended `w[3]` on return.
- **`00510C80`** (`00510C80`-`00510D72`): exact. It has the same shape as `00510B80`, and `005685B0(y, x, rsp+0x20)` runs at `00510D35`. I read `005685B0`: it loads `r9` from `[[0209AC30]+0x160]` at `005685D3` before any read, so three arguments is right. The stores are at `00510D3A`-`00510D64`.
- **`0056A780`** (`0056A780`-`0056A883`): exact. `0056A796`-`0056A7A4`: `e` = `rcx` + (sext `r9d`+7)<<5. `t` = `[[rdx+0x10]]` (`0056A7A1`). `u` (`0056A7E3`/`0056A7EB`) and `c` (`0056A820`/`0056A824`) are re-read from `[rsi+0x10]`. `0056A7AC` stores `[t+0x18]`. `0056A7B0`/`0056A7B5`: `0020E620(0)` goes to `[t+0x20]`, and `0020E620` reads `ecx` (`sub ecx,[01F83530]`). `0056A7B8`-`0056A7D2`: `002DD7E0(2 or 0)` goes to `[t+0x24]`, and `002DD7E0` reads `ecx`. `0056A7D8`/`0056A7DF` test 0xFFFF and clear the bit. `0056A7E7`-`0056A7FC` store byte `[u+0x39]` and word `[u+0xA]`=k. `0056A801`-`0056A81B` test 0xFFFF, 0x96 and byte `[e+0x10]`==0xF. `0056A82B`-`0056A83F` store `[c+0x24]`=v, `[c+0xC]`=+0x20 and `[c+0xE]`. `0056A843`-`0056A864` call `0029FF60` with `r9d`=movsx word `[e+0xC]`, `[rsp+0x20]`=0x465F and `[rsp+0x28]`=0. `0029FF60` reads all six (`0029FF7A` `[rsp+0x50]` and `002A002B` `[rsp+0x58]` after its prologue). The else branch is `0056A86B`. `0056A874` returns 1.
- **`0056BBD0`** (`0056BBD0`-`0056BC65`): exact. `e` and `t` are formed as in `0056A780` (`0056BBE6`-`0056BBF4`). `0056BBFC` stores `[t+0x18]`. `0056BC00`/`0056BC08` store `[t+0x20]`. `0056BC0B`-`0056BC1B` store word `[[t]+4]`-0x12 to `+0xC` and word `[[t]+6]` to `+0xE`. `0056BC1F`-`0056BC33` store `002DD7E0(2 or 0)` to `[t+0x24]`. `0056BC3B`/`0056BC41` test 0xFFFF and clear the bit. `0056BC45`-`0056BC5C` clear bit 0 of dword `+8` of `[[rdx+0x10]+8]`. `0056BC57` returns 1.

**7 of 8 exact; 1 narrowed.** All 40 anchors were checked.

## SWE2-AUDIT-SPEC narrowing

**`005109B0`: in rows.json and in the page's 2026-10-03 block, line 426.** `00280120` reads no argument register. At `00280120` it loads `rcx` from `[0209AC30]` before using it, and nothing in its 20-byte body (`00280120`-`00280133`) touches `rdx`, `r8` or `r9`. The parenthetical says the incoming registers are passed, and that is false as an argument claim. The sibling rows `00510B80` and `00510C80` already write the same call as a bare `00280120()`.

Replace:

> returns the value of `00280120()` (incoming registers passed through) when it is non-zero;

with:

> returns the value of `00280120()` when it is non-zero;

The anchors are unchanged, and the rest of the row stands.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings (what the rectangles, the slots or the entry table represent) were not reviewed.
- Callee behaviour was read wherever a row depends on it: `00280120`, `002640C0`, `005685B0`, `0020E620`, `002DD7E0`, the argument reads of `0029FF60`, the return of `00244F50`, and the `sinf` IAT name. Opaque callees that a row names only as calls (`002D8BB0`, `002D8C80`, `00246AD0`, `00267E10`, `002650B0`, `00568460`, `002D78B0`) were not followed.
- The "returns nothing" clauses mean the function sets no return value of its own. `rax` holds whatever the last callee left.
