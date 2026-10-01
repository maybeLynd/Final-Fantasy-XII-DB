## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's static clauses were turned into checks at the interpreter's own instructions and tables.
The ten facts it shares with the script-resume page run first (R1–R10, `falsify_script_resume.py`), then six of its
own (K1–K6). SECTION-11/12's executions are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_interpreter_core.py`, output `falsify_interpreter_core.out`, image
`73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| R1–R10 | I1, I4, I5, I6, I7 and §2's driver, table and lengths (the facts shared with the script-resume page) | **all survive**. Depth reset at `0025E4D8`; budget `0x10000`; 100 targets at `00261DF8`; advance words 0/1/3 at `01EFEA60 + op·24`; opcode 03's flag `0x40`; stop at `0025E60A`, advance at `0025E613`; the depth < 63 append in `002621D0`, stack passed by pointer; the `+0xA8 + sx(+0x11)·0x28` request address; the `02099011 + sx·0x288` poll byte; the pre-dispatch decode for opcodes ≥ `0x47` |
| K1 | §2 the interpreter is 14,646 bytes | **survives** |
| K2 | §2 the stack's extent is `0x284` | **survives**. `002621D0` writes four indexed arrays at `+0x04` (byte), `+0x44` (byte), `+0x84` (dword) and `+0x184` (dword), so 64 entries end at `+0x284` |
| K3 | I5 opcode 00 does not advance, and 01 stops at the same address | **survives**. Opcode 00's table entry is the plain advance `0025E613`, with length 0. Opcode 01's is the stop entry `0025E60A`, which falls into that advance |
| K4 | I6 opcodes above `0x63` still reach the length lookup | **survives**. The advance reloads the saved opcode byte (`movzx edx, [rsp + 0xb8]`) and indexes `01EFEA60` with it, with no bound |
| K5 | §3 integer registers `+0x64..+0x70`, float registers `+0x74..+0x80` | **survives**. The interpreter addresses all eight through `r15`, the actor record |
| K6 | §7 REQSW (`0x24`) and REQEW (`0x27`) arm kind 4 | **survives**. Both arms' control flow reaches one shared store, `002602EE mov byte [rsi + 0x14], 4` |

**Verdict.** The contract's static facts hold. Tier 1 (static).
