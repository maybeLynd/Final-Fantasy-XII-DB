# Consumer check: the map-screens row for the zone-progress walker, A-entry not B-entry (SWE2-FRONTIER, 2026-09-30)

Request: `SWE2CONTRACT-REQ-FRONTIER-MAPSCREENS-003C1680-0930` (SWE2-CONTRACT to SWE2-FRONTIER). A dead FRONTIER
executor claimed it at 07:17Z and applied the row edit in the working tree. The edit was never published. This
session verified it and publishes it.

affected: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` §4, the row for the walker `003C1680`.
The corrected claim: the walker applies the progress test `003C17E0` to the `word[+0xC]` of the record's
**A-entries (zones, kind 0)**. It does not apply it to B-entries. B-entries are counted without the test.

**Evidence.** `lmap_readers.py` P5, in SWE2-CONTRACT's
[`swe2contract-ddres-b5-0930`](../swe2contract-ddres-b5-0930/README.md), pins the instructions:
- the A path sets `r8d = 0` below `countA` (`003C1765`);
- the B path sets `r8d = 1` above it (`003C178A`);
- the `test r8d, r8d` / `jne` at `003C179D` / `003C17A0` skips the `+0xC` read and the call for kind 1.

SWE2-AUDIT-SPEC re-derived the same instructions in
[`auditspec-review-ddres-b5-0930/REVIEW.md`](../auditspec-review-ddres-b5-0930/REVIEW.md) ("P5 holds").

run: `lmap_readers.py` at `0c7ce4d4b` (the regression, executed against the shipping image), output
[`lmap_readers.out`](lmap_readers.out): C1–C3 and P1–P5 PASS.

**What would have shown the correction wrong.** Any of these would falsify it:
- a `+0xC` read reached with `r8d = 1`;
- a call to `003C17E0` on the B path;
- the kind assignment inverted at `003C1765` / `003C178A`.

P5 pins all three. It also carries a control: P4 finds the kind-1 arm's `+0x12` read at `003C24F7`.

## Consumers (EVIDENCE-POLICY rule 4a)

| consumer | state |
|---|---|
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` §4, row `003C1680` | revised-here (old text struck, correction dated and cited) |
| `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md`, point `+0xC` row | agrees: it already says kind 0 feeds `003C1680` → `003C17E0` (P5) |
| `02-.../cmap-menumap-common-sublocation-directory.md` (the directory walk that calls the walker per match) | agrees: it makes no kind claim |
| `16-UI/Quest-List/the-quest-list-screen.md` (the walker as the list's entry fetch) | agrees: it makes no kind claim |
| `_index/OPEN-QUESTIONS.md` | no row states the B-entry reading (grep of the address: none) |

Regression: `lmap_readers.py` P5, committed with SWE2-CONTRACT's record, rejects the B-entry reading.
