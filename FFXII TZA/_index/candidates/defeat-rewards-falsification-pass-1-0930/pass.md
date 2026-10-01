## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's body, DR-2 to DR-6, the
§10 caps, §14's notifier and §3's install. OPUS block 344's execution is carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_defeat_rewards.py`, output `falsify_defeat_rewards.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| D1 | §2 one body of 857 B; its last calls are `00317090` and the cookie check | **survives**. The extent is 857 B, and the last two direct calls are `00317090` and `00808C40` |
| D2 | DR-2 ECX zeroed for the two evaluators; a flag before `0028FB80` | **survives**. `003124BC` and `003124C6` are `xor ecx, ecx` before `002F8BB0` and `002F90C0`. `00312505`–`00312513` test `00236780`'s result (`cmovne edi, ebp`), and `0028FB80` is called at `00312518` |
| D3 | DR-3 the walk reads `+0x1C2` / `+0x18C`, then calls the level advance | **survives**. The walk accumulates `[rdi + 0x18c]` under the 99,999,999 cap, and `003124A3 call 0030C650` |
| D4 | DR-4 gil = (defeated level − `+0x88`) × `[+0xE78]+0x30` + `[+0xE70]+0x30` | **survives**. `[r14 + 0x698]` → `movzx edi, [rax + 0x1c2]`, `movzx eax, [rax + 0x88]`, `sub`; `imul edi, [[r14 + 0xe78] + 0x30]`; `add edi, [[r14 + 0xe70] + 0x30]` |
| D5 | DR-5 status 12 in either layer; the ×5 as `x + 4x` | **survives**. `00312409 test byte [rdi + 0x69], 0x10`, `0031240F test byte [rdi + 0x79], 0x10`; `00312421 lea eax, [r12 + rcx]`, `00312425 lea r12d, [rax + rcx*4]` |
| D6 | DR-6 requested, setter, notifier | **survives**. `00312556 test edx, edx` / `00312558 cmovns ebp, edx`; `0031255D call 00254EE0`; `00312562 sub ebp, ebx`; `00312566 call 00469E80` |
| D7 | §10 the caps and the second display clamp | **survives**. 999,999, 999, 99,999,999 and 99,999 are loaded at `003123ED`, `003123FF`, `00312438` and `0031247C`. The display clamps: `003124B4 mov esi, 0xf423f` held to `003124E6 cmp edi, esi` / `cmovg`, and `0x3e7` at `003124FB`–`00312502` |
| D8 | §14 the notifier | **survives**. `[rsp + 0x30] = ecx`; `00469EA5 test` / `00469EA7 jle` skips non-positive values; `lea edx, [rax + 0x26]` (with `rax` = 0), then `call 0046AB10` |
| D9 | §3 the install of `+0xE70` / `+0xE78` | **survives**. `0023A965`–`0023A9F4` read `02EBF148` and `02EBF140`, index them by definition `+0x22` / `+0x24`, and store `+0xE70` / `+0xE78` |
| D10 | DR-6 the setter clamps to 99,999,999 | **survives**. `00254EE0` carries `0x5F5E0FF` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).
