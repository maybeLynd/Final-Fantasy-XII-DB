# Consumer check: falsification pass 1 on the equipment-compatibility and shop-stock-ladder contracts (OPUS, 2026-09-29)

corrects: 12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md (section 12's EQ-2 formula: propagation of the section 4 correction of 2026-09-25)
corrects: 12-Items-Equipment-Shops-License/CONTRACT-shop-stock-ladders.md (section 16's 45 -> 46: propagation of SG-2's corrected count of 2026-09-25)

## What was corrected

Neither is a new finding, and neither gets a new CON row. Both carry an earlier supported correction into a section it
had not reached.

- **Equipment compatibility, section 12.** The formula still asserted the pre-2026-09-25 order: "the inner loop accepts
  it and the epilogue drops it".
  - OPUS block 323 measured it, and FABLE corrected section 4 (EQ-2) on 2026-09-25.
  - The formula now asserts the slot-1 loop's refusal at `002FA013`, and the slot-0 epilogue's drop of a carried-in
    off-hand at `002FA077`.
- **Shop stock ladders, section 16.** "45 rows whose last entry always passes" was the 57 - 12 of SWE2-CONTRACT's scan.
  - OPUS block 324 showed row 2 always passes, and FABLE corrected SG-2 and section 14 to 11 all-gated rows on 2026-09-25.
  - So the count is 46.

## Current consumers

- consumer: [_index/candidates/s29-opus-replay-equipment-eligibility/README.md](../s29-opus-replay-equipment-eligibility/README.md):
  agrees. It is the source of the EQ-2 order.
- consumer: [_index/candidates/s30-opus-replay-shop-ladders/README.md](../s30-opus-replay-shop-ladders/README.md): agrees. It is
  the source of the 46 / 11 split.
- consumer: [item-id-encoding-and-equipment-compatibility.md](../../../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)
  does not state the recommender's shield order. Not affected.
- consumer: [the-shop-table-and-its-stock-gates.md](../../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md)
  does not state the 45 / 46 count. Not affected.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_equipment_compat.py` Q2 (fails unless every slot-1
candidate is re-tested with `002F7EC0` at `002FA013` and the epilogue runs at `esi == 0`) and Q8.
regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_shop_ladders.py` G2 and G9 (the fall-through to the last
entry, and the rank floor of 1 that makes row 2's `k3@1` tail always pass).

run: verified at 1285f7fae (BROKEN 0 on both), against the certified image `73461d08…`.
