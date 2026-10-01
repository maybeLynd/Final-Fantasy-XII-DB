# The script VM's variable store saturates by width; its s16 range is off by one (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md

**Request:** ASTRA-REQ-FABLE-SCRIPT-STORE-SATURATION. ASTRA's evidence executes the original store leaf `0026D530` in
isolation. [`store_saturation.py`](store_saturation.py) ([output](store_saturation.out)) re-derives it statically from the certified
image and adds the read side. **Verdict: ACCEPT.**

- **S1: the store.** `0026D530` takes the width from descriptor bits 28..31. Widths above 5 return without storing (`ja` →
  `ret`). The six-entry table at image base + `0x14D5F4` sends each width to its own clamp:

  | width | type | clamp before the store |
  |---|---|---|
  | 0 | u8 | `[0, 255]` |
  | 1 | s8 | `[-128, 127]` |
  | 2 | u16 | `[0, 0xFFFF]` |
  | 3 | s16 | floor `0xFFFF8001` (−32767), ceiling `0x8000` (+32768), then a word store (`0026D5C4`) |
  | 4, 5 | s32, f32 | none; the same raw dword copy |

- **S2: the read.** `PUSHV` (`00267FC0`) dispatches by width through its table at image base + `0x1480E8`. Width 3 reaches
  `0026802F` `movsx ecx, word ptr`, a sign-extending read.
- **S3: the consequence, modelled from S1 and S2.**
  - A store of +32768 or more into an s16 variable writes `0x8000`, which reads back as −32768.
  - A store of −32768 writes `0x8001`, which reads back −32767.
  - +32767 and −32767 round-trip.
- **C: control.** The conventional `[-32768, 32767]` clamp would store `0x7FFF` / `0x8000` at the two edges, where the image
  stores `0x8000` / `0x8001`. The u16 arm saturates 65536 to `0xFFFF`. So the sign flip is the s16 arm's own range.

**Evidence classes, kept apart:** ASTRA's is isolated execution of the store; FABLE's S1–S3 are static.

**Not claimed:**
- that any shipped script stores such a value;
- what the caller converts before the store;
- the s16 range's design intent.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md` §2.2, the store (`POPV` "stores it through `0026D530`") | the per-width saturation and the s16 sign flip added | revised-here |
| `scriptvm-verb-dispatch-and-parameter-encoding.md`, the EC7-98 `00267E60` paragraph ("and `0026D530` releases the block") | "releases" struck; the store stated: record `+0x20` → `qword[+0x10]` at `dword[+0x1C]` index, saturating by bits 28..31, no store for width ≥6, no call and no release | corrected 2026-09-30, SWE2-DATA (page owner), on OPUS `7f169f26f` + ASTRA-REQ-DATA-SCRIPT-STORE-SATURATION; S1 re-verified against the shipping body |

Regression: `store_saturation.py` (S1, S2, S3, C). Run verified at d0ddff9d7: FAILS 0.

## The float conversion comes before the clamp (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SCRIPT-POPV-CONVERSION)

[`popv_conversion.py`](popv_conversion.py) ([output](popv_conversion.out)) re-derives the order from the image and models it.
**Verdict: ACCEPT.**

- **P1: the order.** `POPV`'s integer-kind stage reads the popped operand by tag:
  - tag 1 as the raw dword (`00267F57`);
  - tag 2 through `cvttss2si` (`00267F4C`);
  - an empty stack as 0.

  The value goes into the record's `+0x20`, and only then is the width store `0026D530` called (`00267F37`).
- **P2: the consequence, modelled.**
  - 1.75 stores 1.
  - The largest float below 2³¹ (`4EFFFFFF`) stores 255 into a u8 and `0x8000` into an s16.
  - 2³¹ (`4F000000`) converts to `0x80000000`, which the clamp treats as negative: 0 into a u8, `0x8001` into an s16.
- **C: control.** Round-to-nearest would store 2 for 1.75; saturating the float before converting would store 255 for 2³¹.
  The image does neither.

**Evidence classes:** ASTRA executed the stage in isolation under MXCSR `1F80`; this record is static. The indefinite result
assumes a masked invalid exception.

**Not claimed:** whether a shipped script pushes such a float into an integer variable.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md`, the saturation paragraph | the conversion-before-clamp order and its edge values added | revised-here |

Regression: `popv_conversion.py` (P1, P2, C). Run verified at c64f4addd: FAILS 0.

## POPV's lookup result is discarded (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SCRIPT-POPV-LOOKUP)

[`popv_lookup.py`](popv_lookup.py) ([output](popv_lookup.out)). **Verdict: ACCEPT.** This is a correction of the storage-classes
page's `POPV` row.

- **L1: the lookup is read-only.** `0032F240` (32 B) makes no call and no memory write. It reads the enable byte at
  `022C6D18 + i` and returns the dword at `022C6D28 + 4i` when set, else −1.
- **L2: the call site.** `POPV` calls it (`00267F2D`) only when `uint32(slot +0x28 − 1) ≤ 2` and `esi == 0`. The next
  instructions are `lea rcx, [rsp + 0x30] / call 0026D530`, with no read of `eax` between.
- **L3: the result is discarded.** `0026D530` does not touch `rax` before `0026D53B` overwrites `eax`. So on `POPV`'s path the
  id is unused: no notification is emitted, and the store does not depend on the lookup.
- **C: control.** A planted `mov dword ptr [rsp + 0x50], eax` after the call is reported as a use of the returned value.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md` §2.1, the `POPV` row ("select a notification (`0032F240`)") | struck and corrected: a read-only lookup whose id `POPV` discards | revised-here |
| the same page, OPUS's `0032F240` section ("returning a notification id") | qualified additively: `POPV` discards the id; other callers (the voice verbs) use it | revised-here |
| `scriptvm-verb-dispatch-and-parameter-encoding.md` line 1383 ("the entry's `0032F240` notify") and `CONTRACT-steam-integration-subsystem.md` ("the slot-notification lookup") | labels only, not `POPV` claims; a read-only id lookup, not a notifier | routed-to-SWE2-CONTRACT |

Not claimed: table values, the writers' timing, or other callers' reachability.

Regression: `popv_lookup.py` (L1, L2, L3, C). Run verified at b22809a95: FAILS 0.

## Int to float rounds by MXCSR (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-SCRIPT-FLOAT-ROUNDING)

[`float_rounding.py`](float_rounding.py) ([output](float_rounding.out)). **Verdict: ACCEPT.**

- **F1: the float-kind stage.** A tag-1 (int) operand goes `movd` / `cvtdq2ps` / `movss` (`00267EC9`–`00267ED5`). A tag-2 float
  is copied as it is, and an empty stack stores 0.0.
- **F2: no second rounding.** Width 5 stores a raw dword, so the conversion is the only rounding step.
- **F3: modelled.** 16,777,217 (2²⁴ + 1) becomes `4B800000` under round-to-nearest-even and `4B800001` under round-up. Ints up
  to 2²⁴ in magnitude convert exactly in both modes.
- **C: control.** A truncating model gives `4B800000` in both modes, so the mode dependence is `cvtdq2ps`'s.

**Evidence classes:** ASTRA executed both rounding modes in isolation (MXCSR `1F80` and `5F80`); this record is static.

**Not claimed:**
- the game's MXCSR;
- native flags;
- whether any shipped script stores such an int into a float variable.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md`, the conversion paragraph | the int-to-float direction and its rounding-mode dependence added | revised-here |

Regression: `float_rounding.py` (F1, F2, F3, C). Run verified at 89edb9a6c: FAILS 0.
