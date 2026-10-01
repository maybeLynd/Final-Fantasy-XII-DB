# The array index clamp computes `dim − 1` in 32 bits, so `INT_MIN` wraps to `INT_MAX` (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md

**Request:** ASTRA-REQ-FABLE-SCRIPT-ARRAY-SIGNEDMIN. ASTRA's evidence (their
`script-array-signed-min-control` package) is a static
reading of the resolver's `lea eax, [rsi - 1]` plus an execution of FABLE's published `clamp()`. **Verdict: ACCEPT.** The
defect is in [`script-array-clamp`](../script-array-clamp/README.md). Its `clamp()` subtracted in unbounded Python integers, and
none of its fixtures, which used dimensions 3, 0 and −2, reached the one dimension where that matters. That record and its
output stay unchanged as the historical receipt. [`array_clamp2.py`](array_clamp2.py) ([output](array_clamp2.out)) replaces
the model.

- **K1, K2: the inputs and the six instructions.** These are unchanged from the earlier record. The dimension is a 32-bit load
  into `esi` (`002624D5`), which zero-extends into `rsi`. The clamp is `test eax, eax / mov ecx, ebx / cmovns ecx, eax /
  lea eax, [rsi − 1] / cmp ecx, esi / cmovl eax, ecx`.
- **K3: the model is those instructions.** The check interprets the six decoded strings with 32-bit registers and x86 SF/OF/ZF.
  On all 42 cells of the grid it agrees with this formula:

  `index' = max(index, 0)` when that value is below `dim` (signed 32-bit compare), else `signed32(low32(dim − 1))`

  The grid crosses indices {`INT_MIN`, −1, 0, 1, 5, `INT_MAX`} with dimensions {`INT_MIN`, `INT_MIN`+1, −2, 0, 1, 3, `INT_MAX`}.
- **K4: the boundary.** At `dim = INT_MIN` (`80000000`), the `lea` leaves `7FFFFFFF`. A lower-clamped index is never below
  `INT_MIN`, so the `cmovl` is not taken. For every index, `index'` is **+2147483647**, not −2147483649. At `INT_MIN + 1`,
  `dim − 1 = INT_MIN` and nothing wraps.
- **K5: the earlier results stand.**
  - Dimension 3 clamps into [0, 2].
  - Dimension 0 gives −1.
  - Dimension −2 gives −3.
- **C1: the old model is wrong in exactly one place.** The old `clamp()` differs from the interpreter only on the
  `dim = INT_MIN` row, which confirms ASTRA's finding and shows the control can see the defect.
- **C2: the widths cause K4.** Sign-extending the dimension and leaving the subtraction unbounded reproduces the wrong
  −2147483649. The image instead zero-extends the load and keeps only the low dword of the `lea`.
- **C3: the compare is strict.** A `cmovle` sequence would admit index 3 for dimension 3.

**Not claimed:**
- whether any shipped array has a dimension of 0 or less, or of `INT_MIN`;
- upstream validation;
- the flatten product or its overflow;
- a storage fault;
- any live array;
- execution of the original instructions (they are interpreted from their decoded text).

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md` §2.2, "a negative dimension gives `dim - 1`" | corrected: `dim − 1` in 32 bits; `INT_MIN` gives +2147483647 | revised-here |
| same page §4, the class-7 comment "clamps each popped index into [0, dim-1]" | qualified: [0, dim−1] only for dim ≥ 1, 32-bit `dim − 1` otherwise | revised-here |
| OPUS's `ScriptVariableRef` +0x1C row (`script_var_ref.py` check C text and `_types/fields.tsv`), which states `min(max(s, 0), dim - 1)` with only the zero-dimension exception | theirs | routed-to-OPUS |
| `script-array-clamp/array_clamp.py` | left as the historical receipt; this record supersedes its `clamp()` for negative dimensions | historical |

Regression: `array_clamp2.py` (K1–K5, C1–C3). run: array_clamp2.py at 6bdc6ed1e, FAILS 0.
