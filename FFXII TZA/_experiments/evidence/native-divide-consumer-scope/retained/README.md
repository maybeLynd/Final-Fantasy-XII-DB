# ScriptVM OPDIV and OPMOD: the zero predicate, the quotient boundary, and no catching frame (OPUS, 2026-09-28)

**Requests:** ASTRA-REQ-OPUS-SCRIPT-DIVISION-GUARD (ASTRA 79) and ASTRA-REQ-OPUS-SCRIPT-DIVIDE-OVERFLOW (ASTRA 80).

**Evidence class:** STATIC, from the certified EXE; nothing executed here. ASTRA's frozen records are the executed and
static evidence this consumes:
- `_experiments/evidence/script-division-unordered-guard/` (79);
- `_experiments/evidence/script-integer-divide-overflow/` (80);

their publication is ASTRA's. [`divide.py`](divide.py) re-reads the bytes independently (I F Z M U C, FAILS 0).

## What the handlers do

**OPDIV (`0x15`, `0025F0AC`), integer path (I).** `00267560` gates it.
- The first pop (`00267E10`) is the **divisor** (`ebx`); the second is the dividend (`eax`).
- The only test before the divide is `test ebx, ebx / je 0025E682`. That target pushes **int 0** (tag `ebp` = 1,
  payload 0).
- Then `cdq / idiv ebx / mov ecx, eax / jmp 0025E68C`.
- **No quotient guard.** No compare against −1 or `0x80000000` sits between the pops and the `idiv`.

**OPDIV float path (F).**
- The top pops to `xmm6` (the **divisor**) and the next to `xmm0` (the dividend).
- The tag decides the load:
  - tag 1 converts with `cvtdq2ps` (rounding by MXCSR.RC, as for the comparator);
  - tag 2 loads the float;
  - any other tag, or an empty stack after `008620C0`, gives `xmm7`.
- `ucomiss xmm6, xmm7` follows. Both `jp` (`0025F19A`) and `jne` (`0025F19C`) reach `divss xmm0, xmm6` (`0025F1A3`).
  Only ordered-equal takes `movaps xmm0, xmm7` (`0025F19E`). So:

  | divisor | result |
  |---|---|
  | +0.0 or −0.0 (ordered equal to 0.0) | `xmm7` |
  | NaN (unordered) | `divss`, so a NaN result |
  | anything else | `divss` |

- The result is pushed with tag 2 while the depth is below `0x3F`.

**The baseline (Z).**
- The interpreter (`0025E4C0`, body `0025E550`–`00261DDB`) sets `ebp` = 1 at `0025E555` and zeroes `xmm7` at `0025E55F`.
- It writes `xmm7` nowhere else but its epilogue restore (`00261DBC`).
- `xmm7` is nonvolatile under the Win64 ABI, so it is **0.0 throughout the body** for conforming callees.

That closes ASTRA 79's "not observed actual initialization / callback preservation" for this function's own code. It
stays open for a non-conforming callee.

**OPMOD (`0x16`, `0025F1D6`) (M).** Two pops, then `cdq / idiv ebx` with **no test of the divisor at all**. The remainder
`edx` is pushed as an int.

## Where the fault goes (U)

- The RUNTIME_FUNCTION covering `0025F0DA` (`0025E550`, chained to `0025E4C0`) has **no handler**.
- Its only direct caller, `0025E0D3`, is in `0025DF00`. That frame's personality is `__GSHandlerCheck` (`00808BA8`),
  which checks the stack cookie and catches nothing.
- The direct-caller chain installs no handler at any level:
  `0025D9E0` → `00314020` → {`0022A770`, `0022B8C0`, `0022BC20`} → `0022A580` → `0022A490` → `0017D6E0` → `0017CCD0`.
  `0017CCD0` is `GameApplication` slot 4, the frame tick, reached only through the vtable.

## What follows

| operands | OPDIV int path | OPMOD |
|---|---|---|
| divisor 0 | int 0 pushed (the guard) | reaches `idiv`: #DE |
| `INT_MIN / −1` | reaches `idiv`: #DE | reaches `idiv`: #DE |
| otherwise | quotient (truncating) | remainder (sign of the dividend) |

- IDIV raises #DE when the divisor is 0 or the quotient does not fit (Intel SDM, IDIV). ASTRA 80 observed that stop at
  `0025F0DA` in an isolated guest, before `mov ecx, eax`: no wrap and no saturation.
- The fault is not caught by any frame from the handler up to the frame tick.

**Not claimed:**
- what the process does with the #DE above the frame tick (the main loop, the CRT frame, the unhandled-exception
  filter: ASTRA's native-exception-filter-tail work);
- whether any authored script supplies these operands;
- the native flags, the MXCSR, or unmasked float exceptions for `divss`.

**Controls (C) and mutations.**
- The U walk's handler reader reports `00808BA8` on `0025DF00`, so it detects a personality when one is present.
- F keeps `jp` and rejects a reversed division. I holds no quotient guard.
- Three mutated copies each fail: F expecting `jnp`; U claiming a handler on `0025D9E0`; I expecting a `cmp ebx, -1`.

## Consumers

| consumer | action | agreement |
|---|---|---|
| ASTRA 79 (`script-division-unordered-guard`) | the same predicate, operand order and zero substitution; Z adds the ABI argument for the baseline | agrees |
| ASTRA 80 (`script-integer-divide-overflow`) | the same boundary: the zero guard only, then `idiv`; U adds that no frame up to the frame tick catches | agrees |
| FABLE's BF-1 table, row `0x15` OPDIV ("a zero divisor is tested on both paths and yields 0") | true for zero, but it omits two things: the int path's `INT_MIN / −1` #DE, and the float predicate (a NaN divisor divides; −0.0 substitutes) | routed-to-OPUS-REQ-FABLE-BF1-DIVIDE-BOUNDARY |
| FABLE's BF-1 table, row `0x16` OPMOD ("MOD 0 faults") | agrees, and `INT_MIN % −1` faults too | routed-to-OPUS-REQ-FABLE-BF1-DIVIDE-BOUNDARY |

**Run receipt.** executed at 6224459a5:
- `divide.py` FAILS 0;
- the three mutated copies FAILS 1 each (F, U, I).
