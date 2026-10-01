# Int to float in POPV rounds toward +infinity for negative ints too: a sign-aware model (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md

**Request:** ASTRA-REQ-FABLE-SCRIPT-NEGATIVE-ROUNDING. ASTRA ran the original `cvtdq2ps` stage in isolation on a
negative input. It then compared the result with the `cvt()` helper in
[`script-store-saturation/float_rounding.py`](../script-store-saturation/float_rounding.py). **Verdict: ACCEPT.**

**The defect.** The helper's round-up step added one to the raw bits of the round-to-nearest result. That is the next
float32 toward +∞ only for a positive value; for a negative one it moves away from +∞. The helper's own comment says
"positive values", and its checks used only positive inputs. The claims it supported therefore stand, but it was no model
for a signed 32-bit input.

That record and its output stay unchanged as the historical receipt. [`float_rounding2.py`](float_rounding2.py)
([output](float_rounding2.out)) replaces the helper.

- **F1, F2: the path.** Unchanged. A tag-1 int reaches `cvtdq2ps` (`00267ED2`), and the width-5 store copies the f32 raw.
- **F3: the model.** Rounding is exact integer arithmetic for all four MXCSR modes:
  - RD: `floor(i / ulp) · ulp`;
  - RU: `ceil(i / ulp) · ulp`;
  - RZ: whichever of those two is nearer zero;
  - RN: the nearer of the two, with a tie going to the even significand.

  Here `ulp = 2^max(e − 23, 0)` and `e = ⌊log2 |i|⌋`.
- **F4: an independent check on RN.** RN matches Python's own round-to-nearest-even double → float32 conversion on all 410
  grid values. The grid covers ±(2²⁴ − 2 … 2²⁴ + 66), ±(2²⁵ … 2²⁵ + 70), `INT_MIN` and the 64 values above it, and
  `INT_MAX` and the 64 values below it.
- **F5: the directed modes, checked from the bits.** On the same grid:
  - every result round-trips as a float32;
  - `RD ≤ i ≤ RU`;
  - for an inexact `i`, RU is the float32 after RD, found by stepping the bit pattern;
  - RZ and RN are each one of the two.
- **F6: the stated values.**
  - 16,777,217: RN `4B800000`, RU `4B800001`, as before.
  - −16,777,219: RN `CB800002` (−16,777,220), RD `CB800002`, RU `CB800001` (−16,777,218), RZ `CB800001`. The RN and RU
    values are ASTRA's executed results (MXCSR `1F80` and `5F80`).
  - `INT_MAX`: RN and RU `4F000000`; RD and RZ `4EFFFFFF`.
  - `INT_MIN`: `CF000000` in all four modes.
- **C1: the control sees the defect.** The old helper agrees with the model on every positive grid value. At −16,777,219
  under RU it gives `CB800003` (−16,777,222), where the model gives `CB800001`.
- **C2: F4 exercises the tie rule.** With ties rounded away from zero instead, RN changes on 52 grid values. For example,
  16,777,217 becomes `4B800001`.

**Not claimed:**
- the game's MXCSR;
- native flags or unmasked exceptions;
- which inputs a shipped script stores;
- every negative input (the grid is a sample; F3 is the rule);
- the float → int direction.

| consumer | action | agreement |
|---|---|---|
| `script-variables-and-their-storage-classes.md` §2.2, the conversion paragraph | negative case added: round-up is toward +∞, so −16,777,219 → −16,777,218 (RN −16,777,220) | revised-here |
| `script-store-saturation/float_rounding.py` and its README F3 | left as the historical receipt (positive values only, as its comment said); this record supersedes its `cvt()` | historical |

Regression: `float_rounding2.py` (F1F2, F3–F6, C1, C2). run: float_rounding2.py at 99203604a, FAILS 0.
