# The ScriptVM comparator's unordered result (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-COMPARISON-UNORDERED ([ASTRA's package](../../../_experiments/evidence/script-comparison-unordered/README.md)).
[`comparator.py`](comparator.py) ([output](comparator.out)), static, written without ASTRA's code: FAILS 0.

No OPUS record or type row carried this comparator's semantics. The only OPUS surface is `VmValueStack`, whose access
index lists `0025D740`'s pops, and that is unchanged. So this record is OPUS's static corroboration plus an executable
specification.

**S: the comparator.**
- `edi = 1` at entry (`0025D74F`).
- The first pop, the right operand, goes to `xmm7`; the second, the left, goes to `xmm6`.
- `ucomiss xmm6, xmm7` is followed by `jp`, which skips the equality test. If equal, it returns 0.
- Otherwise it sets `eax = −1`, runs `comiss xmm7, xmm6`, then `cmova edi, eax`, and returns `edi`.

An unordered `comiss` sets both CF and ZF, so `cmova` never fires. **Any NaN gives +1.** An ordered compare gives −1 when
right > left, and +1 otherwise.

**K: the consumers.** `OPEQ`..`OPLSE` (`0025EA18`..`0025EA90`) each run `test eax, eax`, then `sete`, `setne`, `setg`,
`sets`, `setns` or `setle`.

**M: the specification.**

| case | result |
|---|---|
| 1 vs 2 | −1 |
| 1 vs 1 | 0 |
| 2 vs 1 | +1 |
| NaN on the left, the right, or both | +1 |

So with a NaN the six opcodes give EQ 0, NE 1, GT 1, LS 0, GTE 1, LSE 0. The host's `NaN > x` and `NaN >= x` are False, so
a host-IEEE model would get GT and GTE wrong. This agrees with ASTRA's executed controls, which include their private JP
discriminator.

**Not claimed:** native flags or unmasked exceptions, the game's MXCSR, bad tags, underflow, which scripts compare NaNs,
or reachability.

| consumer | action | agreement |
|---|---|---|
| OPUS records and types | none carried the comparator's semantics; this record is the OPUS spec | revised-here |
| FABLE's BF-1 table and the interpreter page §4 ("compare greater, push 0/1") | should state the unordered +1 and its opcode results | not OPUS's (ASTRA routed FABLE and DATA directly) |

## Integer and mixed operands (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-COMPARISON-MIXED. Checks I, X and P: FAILS 0.

- **I: the integer fast path.** It runs only when depth ≥ 2 and both tags are 1 (`0025D754`, `0025D7B8`, `0025D7BD`). The
  top pops to `ebp` and the lower to `esi`. `cmp esi, ebp` then decides: equal gives 0, otherwise `cmovl` gives −1 when
  lower < top, and +1 otherwise. It is a **signed integer compare with no conversion**.
- **X: every other tag pair takes the float path.** An int operand is converted with `cvtdq2ps` (top `0025D869`, lower
  `0025D8A6`), a float is copied with `movss`, and then the float compare above applies. So **a mixed compare rounds the
  int by the thread's MXCSR RC.**
- **P: precision.** These are conditional arithmetic, not execution:

| lower | top | nearest-even | round-up |
|---|---|---|---|
| int 16777217 | int 16777216 | +1 | +1 (fast path) |
| int 16777217 | float 16777216 | 0 | +1 |
| float 16777216 | int 16777217 | 0 | −1 |
| int 123 | int 124 | −1 | −1 |

  Three models are rejected:
  - all-float (the both-int case would give 0 under nearest-even);
  - always-nearest (the mixed case under round-up would give 0);
  - reversed operand order (16777217 vs 16777216 would give −1).

**Not claimed:** the game's RC, authored values, native flags, or any execution of the mixed path. ASTRA's NaN runs are
not evidence about the int or mixed paths.
