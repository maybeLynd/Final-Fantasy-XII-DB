# The script variable reference and its store (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-STORE-SATURATION ([ASTRA's package](../../../_experiments/evidence/script-store-saturation/README.md)).
[`script_var_ref.py`](script_var_ref.py) ([output](script_var_ref.out)) does not use ASTRA's code. Checks S, R and W: FAILS 0.
W failed before the patch.

**S: the store `0026D530`.** It contains no call. The width comes from bits 28..31 of the record's +0x18. Widths above 5
return without storing. The table at image base + `0x14D5F4` sends each width to its own arm:

| width | stored as | clamp |
|---|---|---|
| 0 | u8 | `[0, 255]`; a negative stores 0 |
| 1 | s8 | `[-128, 127]` |
| 2 | u16 | `[0, 0xFFFF]` |
| 3 | s16 | floor `0xFFFF8001` (−32767), ceiling `0x8000` (+32768), then the low word |
| 4, 5 | dword | none (a raw copy) |

**The s16 edge.** Storing +32768 or more writes `0x8000`, which a signed read gives back as −32768. PUSHV's width-3 read is a
`movsx`. Why the range is `[-32767, +32768]` is not claimed.

**R: the record `ScriptVariableRef30` (new type, 0x30).** POPV (`00267E60`) and PUSHV (`00267FC0`) each pass a 0x30-byte stack
local as the fifth argument of the resolver `00262440`. The two frames, `sub rsp, 0x60` with the record at rsp + 0x30 and at
rbp − 0x30, each bound it to 0x30. The fields:

| offset | field | writer / reader |
|---|---|---|
| +0x00 | kind00 = 6 | the resolver |
| +0x04 | count04 (int16) | 2 when descriptor bit 27 is set, else r13w; POPV reads it signed |
| +0x08 | source08 (u16) | the word at the resolver's second argument |
| +0x0A | operand0A (u16) | the variable operand, the table index |
| +0x0C | tableDescriptor0C | the table entry's descriptor dword |
| +0x10 | address10 | the class base (descriptor bits 24..26) plus the low 24 bits |
| +0x18 | descriptor18 | the final descriptor; its width bits drive the store and the load |
| +0x1C | index1C (int32) | the element index, read sign-extended |
| +0x20 | value20 | POPV stores it before `0026D530`; PUSHV loads the variable into it |

**The verb-dispatch page is wrong about this function.** It says "`0026D530` releases the block"
(`scriptvm-verb-dispatch-and-parameter-encoding.md` line 1414). `0026D530` has no call and releases nothing; it is the store.
That correction is routed to the page's owner.

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` / `fields.tsv` | ScriptVariableRef30 added (11 rows) | revised-here |
| `script-variables-and-their-storage-classes.md` (FABLE's s16 correction, `_index/candidates/script-store-saturation/`) | the same per-width policy, derived independently | agrees |
| `scriptvm-verb-dispatch-and-parameter-encoding.md` line 1414, "`0026D530` releases the block" | contradicted: no call, a store | routed-to-SWE2-DATA (OPUS-REQ-DATA-VERB-PAGE-0026D530) |

**Run receipt:** `script_var_ref.py` FAILS 0; `types_index.py --validate`: 0 errors; the width, reference, embed and route
checks: 0.

## The array index and its clamp (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-ARRAY-CLAMP ([ASTRA's package](../../../_experiments/evidence/script-array-clamp-precondition/README.md)).
Check C: FAILS 0.

For an array variable, the resolver `00262440` computes `index1C` from the array header:

- The rank is a u16 at +4. Rank − 1 below zero skips the loop, so a rank-0 array gets no subscripts.
- The dimensions are s32 values from +8, taken last first.
- Each popped subscript is taken either as a float (`cvttss2si`, `00262571`) or as a dword (`0026257D`). It becomes
  `min(max(s, 0), dim − 1)`: `ebx` = 0 is the floor (`cmovns`), and `cmovl` compares against `dim − 1`.
  **(Corrected below, "The array clamp at INT_MIN": `cmp` is against `dim` itself, and `dim − 1` is 32-bit. The formula
  holds only for positive dimensions.)**
- That value is multiplied by the product of the later dimensions and summed.

**The clamp keeps the index in range only for strictly positive dimensions.** A zero dimension gives −1 for that stage, and
nothing in this stage rejects it. The field's row now states that. No validation of dimensions or storage is claimed, and none
is invented.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 `index1C` | qualified: strictly positive dimensions; zero gives −1 | revised-here |

## POPV converts first, and +0x04 is the value kind (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-POPV-CONVERSION ([ASTRA's package](../../../_experiments/evidence/script-popv-conversion-order/README.md)).
Check K: FAILS 0.

**Correction of my own row.** The record's +0x04 is the value kind, not a count. The resolver writes 2 when descriptor bit 27
is set, else 1. POPV (`00267E84..00267E96`) branches on it. The row `count04` is renamed `kind04`, and its old text is kept in
the evidence.

**The order.** POPV converts first, then stores:

| kind | operand on the stack | conversion |
|---|---|---|
| 1 (integer) | float | `cvttss2si` (`00267F4C`) |
| 1 (integer) | int | copied raw (`00267F57`) |
| 2 (float) | int | `cvtdq2ps` (`00267ED2`) |
| 2 (float) | float | copied raw |
| either | empty stack | 0 |

The converted value goes to +0x20, and only then does `0026D530` clamp it by width. `cvttss2si` truncates (1.75 → 1) and gives
`0x80000000` at 2^31 and above. So a float of 2^31 or more popped into a u8 variable stores **0x00**, and into an s16 stores
`0x8001`. A real-valued clamp would give 0xFF and `0x8000` instead.

**Not claimed:** native MXCSR status or unmasked exceptions, the notification callback, or which kind/width pairs ship.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 +0x04 / +0x20 | `count04` renamed `kind04`; `value20` gains the conversion-before-clamp order | revised-here |
| FABLE's storage-classes page (width saturation) | the clamp stands; the conversion precedes it | agrees |

## The lookup POPV calls is read-only, and its result is discarded (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-POPV-LOOKUP. Check N: FAILS 0.

**`0032F240` is a read.** It is 32 bytes with two `ret`s, no call and no store. It reads the byte flag at `022C6D18 + i` and
returns either the dword at `022C6D28 + 4i` or −1.

**Its result goes nowhere.** POPV calls it only when `[rdi + 0x28] − 1 <= 2` and the resolver returned 0 (`00267F1E..00267F2D`).
The next instructions are `lea rcx, [record]; call 0026D530`, and `0026D530` loads eax from the record (`0026D53B`) before it
reads eax. So on this path the returned id is discarded. Nothing is dispatched or notified here.

**Not claimed:** the tables' contents or writers, what the other seven callers do with the value, native faults, or
reachability.

| consumer | action | agreement |
|---|---|---|
| `scriptvm-verb-dispatch-and-parameter-encoding.md` line 1414, "`0032F240` fires when..." | a read-only lookup whose result POPV discards, not an event | routed-to-SWE2-DATA (note on OPUS-REQ-DATA-VERB-PAGE-0026D530) |

## The kind-2 conversion rounds by MXCSR (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-FLOAT-ROUNDING ([ASTRA's package](../../../_experiments/evidence/script-popv-float-rounding/README.md)).
Check F: FAILS 0. W failed before the row was patched.

**The path.** For kind 2 with an integer operand, POPV runs `movd` (`00267EC9`), then `cvtdq2ps` (`00267ED2`), then
`movss` into the record's +0x20 (`00267ED5`), and jumps to the store. The store's width 4 and 5 arm copies the dword raw.
POPV (`00267E60..00267F60`) has no `ldmxcsr`, `fldcw` or other rounding override. So `cvtdq2ps` rounds by whatever MXCSR
rounding control the thread already has. Unlike the kind-1 `cvttss2si`, it is not a truncating form.

**Where it shows.** Every integer with |n| <= 2^24 converts exactly, so the rounding mode matters only above 2^24. For
16777217 the arithmetic gives `0x4B800000` (16,777,216) under round-to-nearest-even and `0x4B800001` (16,777,218) under
round-up. ASTRA's two isolated controls record exactly these values. An always-nearest host cast or a raw bit copy would
not model this path.

**ASTRA's input-label correction is kept as they filed it.** Their first adapter returned a stale RN label for both runs.
The normalized inputs come from the original invocation and the recorded RC, not from a new measurement. This record
relies only on the two converted values and the static path.

**Not claimed:** the game's actual MXCSR RC, native flags or unmasked exceptions, negative or round-down inputs, which
kind/width pairs ship, callers, or live behaviour.

The value20 row also now cites kind 2's own +0x20 stores (`00267EC1`, `00267ED5`, `00267EEA`) beside `00267F1A`.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 `value20` | qualified: `cvtdq2ps` rounds by MXCSR RC; exact up to 2^24 | revised-here |
| FABLE's storage-classes page (POPV conversion order) | f8a527325 already extended it with the same RC dependence, from FABLE's own static check | agrees |

## The array clamp at INT_MIN (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-ARRAY-SIGNEDMIN ([ASTRA's package](../../../_experiments/evidence/script-array-signed-min-control/README.md)).
Check A: FAILS 0. W failed before the row was patched.

**Correction of my own text.** Above I wrote that `cmovl` compares against `dim − 1`. It does not. The instructions are
`cmovns ecx, eax` (`m = max(s, 0)`), `lea eax, [rsi − 1]`, `cmp ecx, esi` and `cmovl eax, ecx` (`00262510..00262518`):

- The compare is against `dim` itself, and signed.
- The fallback is `dim − 1` computed in 32 bits.
- So the stage is `m` if `m < dim`, else the 32-bit `dim − 1`.

For a positive dimension that equals `min(max(s, 0), dim − 1)`. For any dimension ≤ 0, `m < dim` is false, so the stage
is `dim − 1` whatever the subscript:

| dim | stage | unbounded `min(max(s, 0), dim − 1)` |
|---|---|---|
| 0 | −1 | −1 |
| −2 | −3 | −3 |
| `INT_MIN + 1` | `INT_MIN` | `INT_MIN` |
| `INT_MIN` (`0x80000000`) | **`0x7FFFFFFF`** (2,147,483,647) | −2,147,483,649 |

The two agree except at `INT_MIN`, where the 32-bit subtraction wraps. The `index1C` row now states this form, and my
check C's description is corrected. The positive-dimension and zero-dimension findings stand.

**Not claimed:** any shipped array with a non-positive dimension, the 32-bit products of later dimensions (`imul`) and
their overflow, native faults, or reachability.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 `index1C` | corrected: the compare-against-dim form; INT_MIN gives `0x7FFFFFFF` | revised-here |
| this README's array-index section and `script_var_ref.py` C | the "compares against `dim − 1`" text corrected, the old text kept | revised-here |
| FABLE's `array_clamp.py` and the storage-classes page's negative-dimension formula | ASTRA routed these to FABLE as primary owner | not-touched (FABLE's) |

## The flattened index is 32-bit and read back signed (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-ARRAY-FLATTEN ([ASTRA's package](../../../_experiments/evidence/script-array-flatten-width/README.md)).
Check L: FAILS 0. W failed before the row was patched.

**The loop.**
- The sum starts at 0 (`00262487 mov r10d, ebx`) and the product at 1 (`002624AD mov r8d, r13d`, with `r13d` = 1 from
  `00262478`).
- `rbp` starts at the last dimension (`header + 8 + 4 · (rank − 1)`) and steps back 4 each pass (`0026251B`). So the
  first subscript popped pairs with the last dimension.
- Each pass runs `imul eax, r8d` (stage × product), `imul r8d, esi` (product × dimension) and `add r10d, eax`.
- All three are 32-bit, and nothing checks for overflow before the loop's `jns`. So the products, the contributions and
  the sum all wrap modulo 2^32.
- `r10d` goes to +0x1C (`00262672`), and the store reads it back signed (`0026D537 movsxd`).

**Worked values.** These are arithmetic on the decoded instructions, not execution, and not any shipped array:

| dims | subscripts (source order) | index |
|---|---|---|
| 2 × 3 | (1, 0) | 3 |
| 2 × 3 | (1, 2) | 5 |
| 65536 × 65536 | (0, 0) | 0 |
| 65536 × 65536 | (32768, 0) | `0x80000000`, read as INT_MIN |
| 65536 × 65536 | (65535, 65535) | `0xFFFFFFFF`, read as −1 |

Three wrong models are rejected by the check:
- unbounded arithmetic gives 2,147,483,648;
- saturation gives INT_MAX;
- pairing the first subscript with the first dimension gives 1 for (1, 0).

**Not claimed:** that the compiler pushes subscripts in source order, any real overflow, shipped array shapes, the
callback at `[rdi + 0x98]` (its caller reloads `r10d` from `rsp + 0x78` after it), native faults, or reachability.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 `index1C` | qualified: 32-bit products and sum, wrapping modulo 2^32, read back signed; last dimension pairs with the first pop | revised-here |

## Round-up for negative values, and my check's sign-blind helper (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-NEGATIVE-ROUNDING ([ASTRA's package](../../../_experiments/evidence/script-popv-negative-rounding/README.md)).
Check F extended: FAILS 0.

**Correction of my own check.** The helper in check F added 1 to the float's raw bits for round-up, whatever the sign.
Check F only ever ran it on 16777217, which is positive. For a negative value, round-up moves toward +infinity, so the
magnitude shrinks and the raw bits step **down**. For −16777219:

| mode | converted bits | value |
|---|---|---|
| nearest-even | `CB800002` | −16,777,220 |
| round-up | `CB800001` | −16,777,218 |
| the helper's first rule | `CB800003` | −16,777,222 (wrong) |

The helper is now sign-aware, and check F asserts both negative values. The first rule is kept as a rejected control.
The `value20` row now states the sign rule. The positive results stand.

**Not claimed:** round-down, other negatives, native flags, or the game's RC.

## PUSHP's reference keeps class and width only in the 24-bit domain (OPUS, 2026-09-28)

**Request:** ASTRA-REQ-OPUS-SCRIPT-REFERENCE-CARRY ([ASTRA's package](../../../_experiments/evidence/script-reference-offset-carry/README.md)).
Check P: FAILS 0. W failed before the rows were patched.

**PUSHP (`00268100`) is a consumer of this record.**
- It reads `descriptor18` (`00268118`) and `index1C` (`00268120`).
- It scales the index by the width's stride through the table at image base + `0x1481A4`: widths 0–1 are unscaled, 2–3
  use `add edx, edx`, 4–5 use `lea edx, [rdx*4]`, and above 5 the index is unscaled.
- It **overwrites the record's +0x00** with the original width nibble (`00268150`). It then pushes that byte as the
  value's source kind (`00268180`, `00268185`), with tag 1.
- The pushed dword is `low32((d & 0xFFFFFF) + scaled) | (d & 0x07000000) | 0x70000000` (`00268158..0026816C`, stored at
  `00268194`).

**Nothing masks after the add.** So the class survives and the width is 7 only while the sum stays below 2^24. These
are conditional calculations on the decoded instructions:

| descriptor | index | result | class | width |
|---|---|---|---|---|
| `02FFFFFE` | 1 | `72FFFFFF` | 2 | 7 |
| `02FFFFFF` | 1 | `73000000` | **3** | 7 |
| `02000000` | −1 | `FFFFFFFF` | 7 | **15** (bit 27 set) |
| `42000000` (width 4) | −1 | `FFFFFFFC` | 7 | 15 |

A final 24-bit mask (`72000000`) and an exact width-7 replacement (`7FFFFFFC`) are rejected models.

**Not claimed:** any shipped reference that overflows, what consumes a reference, or native faults.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` ScriptVariableRef30 `kind00`, `descriptor18`, `index1C` | PUSHP's reads, its overwrite of +0x00, and the packing with its offset domain | revised-here |
| `_types/fields.tsv` ScriptVariableRef30 `value20` | the sign rule of round-up | revised-here |
| the storage-classes page §2.1 table (`PUSHP` row) and §9's OPUS subsection "PUSHP forces the width nibble, not the class" (`WIDTH := 7`, "the code ... keeps it") | true inside the 24-bit domain; needs the qualifier | routed-to-FABLE (note on ASTRA-REQ-FABLE-SCRIPT-REFERENCE-CARRY) |
