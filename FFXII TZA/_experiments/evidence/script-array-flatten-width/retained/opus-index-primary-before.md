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
