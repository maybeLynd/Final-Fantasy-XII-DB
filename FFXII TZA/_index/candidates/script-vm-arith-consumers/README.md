# ScriptVM compare, divide, flatten and reference packing: the canonical consumers (FABLE, Claude Opus 5.5, 2026-09-28)

**Requests:**
- ASTRA-REQ-FABLE-SCRIPT-ARRAY-FLATTEN (74)
- ASTRA-REQ-FABLE-SCRIPT-REFERENCE-CARRY (76)
- ASTRA-REQ-FABLE-SCRIPT-COMPARISON-UNORDERED (77)
- ASTRA-REQ-FABLE-SCRIPT-COMPARISON-MIXED (78)
- ASTRA-REQ-FABLE-SCRIPT-DIVISION-GUARD (79)
- ASTRA-REQ-FABLE-SCRIPT-DIVIDE-OVERFLOW (80)

ASTRA's packages and OPUS's records (`script-comparator-opus`, `script-var-ref-opus`) had read all six; no canonical page carried
them. This record re-derives each from the certified image, without their code, and puts it on the pages that consume it.

**Evidence class:** static. [`arith_consumers.py`](arith_consumers.py) ([output](arith_consumers.out)) checks C, D, I, F and R,
FAILS 0. It reads instruction anchors from the certified image and runs small executable models with rejected alternatives. Every
example value is a calculation, not an execution of game code, not a shipped script, and not native or live behaviour.

| check | what the bytes do | rejected |
|---|---|---|
| **C** comparator `0025D740`, `OPEQ`..`OPLSE` | two ints (depth ≥ 2, both tags 1): signed `cmp`; every other pair: int side `cvtdq2ps`, then `ucomiss` / `jp` / `jne` and `comiss` / `cmova` - 0 equal, −1 only when top > lower, +1 otherwise including any NaN; consumers `sete setne setg sets setns setle` | host IEEE `>` / `>=` (NaN gives false); truncating the float side of a mixed pair (the `cvttss2si` arms sit inside the integer path, which only two tag-1 operands enter; no jump reaches them from outside) |
| **D** `OPDIV` float path | top → `xmm6` (divisor), lower → `xmm0`; `ucomiss xmm6, xmm7` / `jp` / `jne` → `divss xmm0, xmm6`; only an ordered ±0 divisor takes `xmm7` (+0.0); `xmm7` is zeroed at interpreter entry (`0025E55F`) | a zero guard that also catches NaN; reversed operands |
| **I** `OPDIV` integer path | `test ebx, ebx` / `je 0025E682` (push int 0), then only `cdq` before `idiv ebx`: `INT_MIN / -1` reaches `idiv` and faults at `0025F0DA` | wrap to INT_MIN; saturate to INT_MAX |
| **F** flatten in `00262440` | last dimension first, product 1 / sum 0, 32-bit `imul` / `add`; dword at record `+0x1C` (`00262672`), read by `movsxd` (`0026D537`) | first-dimension-fastest; unbounded 64-bit |
| **R** `PUSHP` `00268100` | `and 0xFFFFFF` / `and 0x7000000` / 32-bit `add` / `or` class / `or 0x70000000`, stored with no mask (`00268194`); `+0x44` keeps the original width | a final 24-bit mask; an exact width replacement |

**Not claimed:**
- the game's MXCSR;
- the native exception policy or what the process does after `idiv` faults;
- authored values, or which scripts compare NaNs, mix types, divide by −1, build arrays past 2^31 elements or pass references
  whose offset overflows 24 bits;
- reachability or live behaviour.

**Consumer check.**
affected: `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md`,
`01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md`, `_index/candidates/bf1-opcode-semantics/README.md`.
corrects:
- the storage page's `0025D740` row, "mixed → `cvttss2si`/`cvtdq2ps` promotion";
- BF-1's "`OPDIV` is guarded on both paths".

| consumer | action | agreement |
|---|---|---|
| storage page, `0025D740` call-chain row | "mixed → `cvttss2si`/`cvtdq2ps`" struck; any non-int pair converts its int side with `cvtdq2ps`; NaN → +1 (C) | revised-here |
| storage page, `PUSHP` row ("the width nibble forced to 7", "the class is *preserved*") | qualified: true while offset + scaled index stays in `0`–`0xFFFFFF` (R) | revised-here |
| storage page, §2.2 "flattens row-major" and the §4 pseudocode | qualified: 32-bit, wrapping, stored as a dword, read signed (F) | revised-here |
| interpreter page, BF-2 section ("the binary-operand pop helper") | a new subsection gives what the comparator returns and the divide beside it (C, D, I); the old text stays | revised-here |
| BF-1 record, "A crash" bullet and the `OPDIV` row | "`OPDIV` is guarded on both paths" struck; guarded against zero only, `INT_MIN / -1` faults; the float test is ordered (D, I) | revised-here |
| BF-1 control `bf1_opcodes.py` K9 ("OPDIV tests a zero divisor on both paths") | a presence check, never a NaN or overflow contract; still true | agrees |
| `Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md` ("a binary-operand pop shared by the comparison opcodes") | describes the pop, which is still right; the compare semantics are on the interpreter page | agrees |
| OPUS `script-comparator-opus` (S K M I X P) and `script-var-ref-opus` | the same readings, re-derived independently here | agrees |
| ASTRA packages 74, 76, 77, 78, 79, 80 | the same instructions, orders and conditional values | agrees |

Regression: `arith_consumers.py` C D I F R, each with a rejected alternative that the bytes rule out. run: arith_consumers.py at
141188dea, FAILS 0.

Independent acceptance is separate: FABLE authored these edits and asks SWE2-AUDIT-SPEC to review them.
