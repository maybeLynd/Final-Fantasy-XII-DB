# Consumer check: 12-Items contradictions from a local reconstruction-readiness pass settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-ITEMS-1002: stream R run locally, with no cloud credit. A read-only reader mapped
`12-Items-Equipment-Shops-License/` (rated MOSTLY; the map is filed in the RE repo as `docs/readiness/12-items.md`).
It found 43 contradictions, 15 of them value-changing. A second read-only pass drafted the strike edits
(`apply_12items.py`, 73 edits with one OPUS addition; only disfavoured sides; strikes open and close on one line).

OPUS re-checked the value-changing items at the bytes (`items_check.py`):
- the write dispatch slot `+0x48`;
- `00308FF0`'s return;
- the licence check's stats record and guest row 6;
- the bazaar purchase gate;
- the decode base `01F83530`;
- the `[02EBF190]+8` table root;
- the callers of `0030B270` and `00328BD0`.

- **Affected:** 12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md, 12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md, 12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md, 12-Items-Equipment-Shops-License/CONTRACT-license-check.md, 12-Items-Equipment-Shops-License/README.md, 12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md, 12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md, 12-Items-Equipment-Shops-License/license-board-grid-format.md, 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md, 12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md, 12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md, 12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the twelve 12-Items pages (each disfavoured side; README labels) | revised-here |
  | CONTRACT-shop-stock-ladders.md (never the disfavoured side) | agrees |
  | RE repo `docs/readiness/12-items.md` | routed-to-OPUS (filed from this commit) |
  | the map's structural gaps `00323D10` (licence purchase) and `00309060` (action gil cost), and its three unstated maps | routed-to-OPUS (left for later reads) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-items-readiness-fixes-1002/items_check.py, verified at 9c53f6973: 12 instructions decode as cited, FAILS 0 ([`items_check.out`](items_check.out)). `apply_12items.py` re-runs as ALREADY (73), FAILS 0.
