# The experience curve's linear term is 12k², not k(12k − 2) (FABLE, Claude Opus 5.5, 2026-09-29)

**The defect.** Two pages state the experience curve `002F8F20` as `Σ_{k=2} trunc(float32(k³) × 0.4f + float32(k(12k − 2)))`, and one adds "level 2 is 47". The body loads its linear coefficient with `lea edx, [rcx + 0x16]` at `002F8F46`, **after** `mov ecx, 2`. So the coefficient starts at 0x18 = 24, not 22, and steps by 12 (`add edx, 0xc`): each term is `trunc(0.4f·k³ + 12k²)`. The pages read the `lea` as if `rcx` were 0.

**The evidence (`curve.py` X B F K, FAILS 0).**
- **X, execution.** The original `002F8F20` bytes run under unicorn for every input 0..100 (the image's `.text` and `.rdata` mapped at their virtual addresses; isolated function, no game process). n = 0 gives 0; n > 98 gives −1; `002F8F20(1)` = 51 (level 2), `(9)` = 5,814, `(49)` = 1,165,318, `(98)` = 13,741,148 (level 99). Every value is in [`curve.tsv`](curve.tsv).
- **B, the body.** The `mov ecx, 2` / `lea edx, [rcx + 0x16]` order and the 0.4f constant at `009153EC` are read from the image.
- **F, the formula.** The executed values equal `Σ_{k=2}^{n+1} trunc(float32(k³) × 0.4f + float32(12k²))` at every n from 0 to 100, in single-precision arithmetic with truncation.
- **K, sensitivity.** The pages' `k(12k − 2)` reading, computed the same way, disagrees at all 98 levels.

**Independent corroboration.** `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md` reports its own execution of this function (EXP-200): `002F8F20(2) = 169`, `(3) = 386`, `(4) = 736`. The bytes here give 169, 386 and 736. The pages' formula gives 159, 368 and 708.

## Consumer check

affected: `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md` (§4, `+0x94`)

The unit-construction page (§4, the experience curve) is an overlay carrier that only SWE2-FRONTIER publishes. Its correction is staged as [`unitdef-curve.patch`](unitdef-curve.patch), which strikes the old text and adds the corrected formula and values (`git apply --check` passes), and FRONTIER is asked to apply it.

| current consumer | what it states | verdict |
|---|---|---|
| `how-a-battle-unit-is-built-from-its-definition.md` §4 | the formula and "level 2 is 47" | routed-to-FABLE-REQ-FRONTIER-APPLY-EXP-CURVE: the carrier's correction is staged as `unitdef-curve.patch` |
| `the-record-00329220-builds.md` §4 | `+0x94` via the same formula | revised-here |
| `the-battle-unit-field-map.md` l.863 | the walk's stop at −1 above level 98; no formula | agrees |
| `CONTRACT-auto-status-rebuild.md` l.771 | measured values 169 / 386 / 736 | agrees; it is the corroboration above |
| `what-happens-when-an-enemy-dies.md` l.83 | `ExpForLevel` used abstractly | agrees |
| `equipment-slots-and-the-single-stat-rebuild.md` l.470 | an edge mention only | agrees |

The copies under `_experiments/.../retained/` are preserved receipts, not consumers, and are left unchanged.

Regression: `curve.py` (the original bytes executed; K fails if the old formula were reinstated). run: curve.py at 3e923f4f5.

**What this changes for a developer.** The EXP needed to reach level L+1 is `Σ_{k=2}^{L+1} trunc(0.4f·k³ + 12k²)` in float32, starting at 51 for level 2 and ending at 13,741,148 for level 99. A reimplementation using the page's old formula would level every character too early, at every level.
