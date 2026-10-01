## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's entry and dispatch,
I1's mask loops and flags, I2's copy-through, I3's dirty flag and outer recompute, §3's layer loops, I6's setter pairs,
I8's availability clear and I7's absent `0x400`. SECTION-01 and OPUS block 332 are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_apply_result.py`, output `falsify_apply_result.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| A1 | §2 2,040 bytes; owners resolved at `00311321` / `0031132C` | **survives**. Both are `call 0031B860` |
| A2 | §2 the numeric dispatch and the source-MP flags | **survives**. The gates are `bt ecx, 8` (`00311610`), `bt ecx, 0xe` (`0031166D`), `byte [rbx + 0x1d]` (`003116A6`, then `00300BC0` at `003116E0`), `test rcx, rcx` (`003116FB`), `test dl, dl` (`00311703`) and `bt r9d, 0xd` (`00311748`). The flags are built as `shr 7`, `not`, `and 0x10`, `shr 0xa`, `and 0x20`, `or` |
| A3 | I1 the two mask loops: mode 3 and mode 0, flags (`x & 0x10` with `0x1000` set) `>> 3` and (`x & 0x20` with `0x2000` set) `>> 4` | **survives**. The mode argument is `3` at `0031153A` and `r13d` = 0 at `0031159F`. The flags are built at `003114D2`–`003114EE` with `bts eax, 0xc` and `bts ecx, 0xd` for the `0x1000` / `0x2000` bits |
| A4 | I2 the copy-through to `target + 0xBC + 4i` and `target + 0x13C + 2i` | **survives**. `r9 = target − record`, the cursor runs from `record + 0x5C`, and the store `[r9 + rcx + 0x60]` lands at `target + 0xBC + 4i` for `0x20` entries, skipping negatives. The words run from `record + 0xDC` through `[rax + r9 + 0x60]` to `target + 0x13C + 2i` |
| A5 | I3 the dirty flag and the outer recompute | **survives**. `mov r14d, 1` at `0031153F`, `003115A4`, `003117D0` and `0031180C`, with no result test. `[rsp + 0x44] = (callerFlags >> 9) & 1` (`00311344`–`00311350`). The tail tests the target, that local and `r14d`, then calls `0030FED0` with `edx = 0` |
| A6 | §3 the two layer loops call `0030E130` | **survives** (`003117CB`, `00311807`) |
| A7 | I6 the absolute/delta pairs | **survives**. All four setters, `00300520` / `00300530` and `00300C90` / `00300CE0`, are loaded by `lea` and called through the selected register |
| A8 | I8 the gate clears availability; the steal loop finds it clear | **survives**. `and byte [rax + 0x14], 0xfb / 0xfd / 0xfe` at `00385C17`, `00385C41` and `00385C6B`; `0031137A call 00385BA0`; `0031146C btr` |
| A9 | I7 no unconditional `0x400` in the target-HP flags | **survives**. There is no `0x400` immediate in `00311610`–`0031166D` |

**Verdict.** The contract's addressed clauses hold; several are compiled in forms the prose does not show (`bts` setting the
`0x1000` / `0x2000` bits, and base-difference addressing for the copy-through). Tier 1 (static).
