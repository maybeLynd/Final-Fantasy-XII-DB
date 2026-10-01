## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's entry, id split,
teardown and party spawn; I1's bit-26 mask and the enemy refusals that bypass it; I2's reset and master flag; I3's
re-key wrapper; I6's freshness gate and reward rows; I7's tracked-HP table; and I8's pulse reset and float paths.
SECTION-01, EXP-150 and OPUS block 343 are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_unit_construction.py`, output `falsify_unit_construction.out`, image
`73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| B1 | §2 1,808 bytes; class = `(id >> 8) & 0xFF`, row = `id & 0xFF` | **survives**. `0023A580 mov eax, edx`, `0023A585 sar eax, 8`, `0023A594 movzx esi, al`, `0023A58B movzx r12d, dl` |
| B2 | §2 teardown re-applies `0xFFFF` | **survives**. `00300F6D mov edx, 0xffff`, `00300F75 call 0023A570` |
| B3 | I2 the reset, then the master flag | **survives**. `0023A5B0 call 00236A60`, then `02089300` is read at `0023A5B5` |
| B4 | §2 the party path nulls the spawn | **survives** (`0023AAB1 xor ebp, ebp`) |
| B5 | I1 the bit-26 clear, and the class-1 refusals that skip it | **survives**. `0023A633` and `0023AC4B` are `and qword [rdi], 0xfffffffffbffffff`. The enemy path's refusals at `0023A643`–`0023A648` and `0023A65F`–`0023A662` jump to `0023A63A`, past the clear |
| B6 | I3 the re-key wrapper | **survives**. `00322050` writes `dword [+0xea4] = 0` and `byte [+0xea8] = 0`, resolves `q[unit + 0x10]` through `003220E0`, and stores the 32-bit handle at `+8` |
| B7 | I6 the freshness gate `byte[spawn] & 5 == 0` | **survives** (`0023A791 test byte [rbp], 5`) |
| B8 | I6 the reward rows | **survives**. `0023A965`–`0023A9F4` read `02EBF148` and `02EBF140` by definition `+0x22` / `+0x24`, store `+0xE70` / `+0xE78`, and form the row with `add ecx, eax` |
| B9 | I7 tracked-HP registration | **survives**. `00328FF0` writes `{slot, code}` into `02EC1380 + row·24` (`lea r9, [rax + rax*2]`, `*8`). It writes only when `code ≠ 0` or `slot < 0` (`jns`), and only under a signed `cmp ecx, 2` / `jge` |
| B10 | I8 the pulse reset and the class float paths | **survives**. `002FEAB0` is 10 bytes (`xor eax, eax; mov [rcx + 0xeac], rax; ret`). Class 1's `byte +0x27` goes to `xmm7` by `cvtdq2ps` with no multiply. Class 0's `byte +0x2B` goes to `xmm7` and is multiplied by the 1.5f at `00901B3C` (`0023ABAD`). The common store is `0023ABD6 movss [rdi + 0x6c], xmm7` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).
