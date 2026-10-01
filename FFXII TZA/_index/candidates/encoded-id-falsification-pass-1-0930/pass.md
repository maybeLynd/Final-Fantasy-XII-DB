## Falsification pass 1 — 2026-09-30 (OPUS): ten clauses survive; one premise in §14 is broken, its conclusion survives

**Attack.** The contract's static clauses were turned into checks at their instructions and data: the interface (§2),
the registry table (§3), the validator and its tail (§6), I1, I2's class-19 range, I4 and the relocation codec. The
N05 executions and EXP-143's review are carried, not re-run. Script: `Tools/analysis-kit/gfz-scripts/falsify_encoded_id.py`,
output `falsify_encoded_id.out`, image `73461d08…`, BROKEN 1 (E10), exit 0.

| # | Clause attacked | Result |
|---|---|---|
| E1 | §2 `00309440`: low 16 bits, nibble 0..E into `01EEBCC0 + n·0x58 + 0x38`, nibble F returns −1 | **survives**. The 10-instruction body shifts by 12, strides `0x58` from `01EEBCF8` (the table's `+0x38`) and has the −1 path |
| E2 | §3 the table: `+0x38` = nibble + 5; counts sum 6892; lanes and prefixes zero on disk; offset high halves zero; handler pattern | **survives**. The classes are 5..19 in row order and the `+0x3C` counts sum to 6,892. Every `+08/+20/+30` lane and `+40` prefix is zero in the file, and every `+00/+18/+28` high dword is zero. Classes 14, 15, 18 and 19 are mutate-only (`002FD530`, `002FD640`, `002FD780`, `002FD880`), and 10, 12 and 16 have neither handler |
| E3 | §6 the validator's 32-entry table at `00323054` and its shared tail | **survives**. All 32 image-relative targets lie inside `00322C50`, and the tail reads `0032302E cmp ebx, edx`, `00323036 lea eax, [rcx - 1]`, `00323039 cmp ebx, eax`, `00323041 mov eax, 1` |
| E4 | I2 class 19 admits `E000..EFFE` inclusive | **survives**. Arm `00322F63` loads `0xE000` and `0xEFFF`, and the tail's `lea eax, [rcx - 1]` makes the upper bound `EFFE` |
| E5 | §2 the filler's table at `0031E598`; class 12 returns −2 reading neither lane | **survives**. Arm `0031C650` is `mov eax, 0xfffffffe; jmp` |
| E6 | §2 the wrappers: records `022CA520` (tag, dword `+4`) and `022CA480` (tag, word `+6`); negative fill → `0016D6A0` and a 0x98 clear; return the record | **survives**. Both write their tag and lane, call `0031C5D0`, `0016D6A0` and `memset` `00861EC0`, and load their own record address |
| E7 | I4 the rebase clears `state+57C8..59C7` and ANDs 128 bytes from `state+59C8` with `F8` | **survives**. `r11` is zeroed. Eight passes of eight qword stores of `r11` over `0x40` bytes run from `lea rax, [rcx + 0x57c8]` (`0030B702`–`0030B737`). `mov ecx, 0x80` / `and byte [rax], 0xf8` / `lea rax, [rax + 1]` run from `+0x59C8` (`0030B739`–`0030B75B`) |
| E8 | §6 `0020E600` = zero-extended dword + full qword `01F83530` | **survives**. The body is `mov eax, ecx; add rax, [01F83530]; ret` |
| E9 | I1 the input lane each class's query arm reads | **survives** for all 31 classes that read one. WORD `+6` is read for 1, 5..11, 13..18, 30 and 31, and DWORD `+4` for 2..4, 19..29 and 32. Class 12 reads neither (E5) |
| E10 | §14 "The only functions that address the table are the rebase `0030B6A0` and `0030B270`" | **BROKEN**. 49 rip-relative references into `01EEBCC0`–`01EEC1E8` sit in 28 functions (listed in the output; 19 `lea`s of a row base, 24 reads of `+0x3C`, 5 of `+0x10`, 1 of `+0x38`). This independently confirms SWE2-AUDIT-SEM's finding (25 functions by its attribution, 49 references). The prose repair is `AUDITSEM-REQ-CONTRACT-REGISTRY-ADDRESSERS-0930` |
| E11 | the conclusion E10's sentence supported: no code writes the offset qwords (`+00/+18/+28`) | **survives**. Every store through a pointer into the registry span, in all 28 functions (the value-flow engine of `k14-closure-stores-0930/k14_actorflow.py`), is the rebase's own: `+0x40` prefixes and its `+08/+20/+30` lane stores (`0030B6CB`–`0030B6F1`). No store reaches an offset qword |

**Verdict.** The contract's mechanism survives. One premise in §14 is false, and the conclusion drawn from it holds on a
wider census. So the high-half argument stands, on E11 rather than on a two-function count. Tier 1 (static).
