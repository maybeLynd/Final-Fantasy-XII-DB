# The script VM's array index clamp holds only for a positive dimension (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md

**Request:** ASTRA-REQ-FABLE-SCRIPT-ARRAY-CLAMP. ASTRA's evidence is a static reading of the original resolver `00262440`.
[`array_clamp.py`](array_clamp.py) ([output](array_clamp.out)) re-derives it from the certified image. **Verdict: ACCEPT.**

- **K1: the inputs.** The resolver zeroes `ebx` (`0026245D`). Each popped index reaches `0026250C` in `eax`, from one of three
  routes:
  - as an int (`0026257D`);
  - as a truncated float (`00262571`);
  - as `ebx`'s 0 when the stack is empty (`002624DA`).

  The dimension is a signed 32-bit read (`002624D5`).
- **K2: the clamp.** `0026250C`–`00262518` compute `min(max(index, 0), dim − 1)` with a strict `cmovl`.
- **K3: the edge case.** The edge element is read only for `dim ≥ 1`. A dimension of 0 gives index −1, one element before the
  array; a negative dimension gives `dim − 1`. Nothing in this stage rejects a dimension of 0 or less.
- **C: control.** A `cmovle` model would admit index 3 for dimension 3, one past the end. The image's strict compare gives 2.

**Not claimed:**
- whether any shipped array has a dimension of 0 or less;
- upstream validation;
- product overflow;
- a storage fault.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md` §2.2, "an out-of-range script index reads the edge element, it does not fault" | qualified: only for a dimension of 1 or more; 0 gives −1; no dimension validation; not a safety guarantee | revised-here |
| OPUS's `ScriptVariableRef` type and contract text, if they carry the same no-fault wording | theirs | routed-to-OPUS |

Regression: `array_clamp.py` (K1, K2, K3, C). Run verified at 6b44f6914: FAILS 0.
