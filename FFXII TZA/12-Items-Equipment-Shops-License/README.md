# Items / Equipment / Shops / License

**Engine category.** Inventory, equipment records, the raw Augment byte, the License Board, shops, Bazaar.

| | |
|---|---|
| Classification source | PrimaryOwner: Items/Equipment/Shops/License |
| Functions | 70 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`the-shop-table-and-its-stock-gates.md`](the-shop-table-and-its-stock-gates.md) —
  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: DOCUMENTED`)*. The 57-shop table behind registry slot `02EBF158`: a dictionary name id per
  shop and a ladder of stock lists, each gated on nothing, story progress (the kind-3 operand bank's
  element 0) or clan rank; the menu lists from the first gate met to the end of the ladder.
- [`the-bazaar-recipe-unlock-and-purchase.md`](the-bazaar-recipe-unlock-and-purchase.md) —
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. The 128-row bazaar table (36 B: three granted pairs, price, flags, three
  required loots with *sold* counts), the loot-sold tally in the inventory's second loot region, the
  flag byte per good, and the sell / refresh / buy functions that move them.
- [`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md) —
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Item IDs encode a category in the top nibble (`0xFFFF` = empty), and
  **every weapon/off-hand restriction is one byte compared against another** — asymmetrically.
- [`CONTRACT-inventory-class-storage.md`](CONTRACT-inventory-class-storage.md) — the fifteen class descriptors and their packed and bitset storage — **BEHAVIORALLY UNDERSTOOD**
- [`CONTRACT-equipment-compatibility.md`](CONTRACT-equipment-compatibility.md) — equip eligibility and the pairing byte, EQ-1 to EQ-8 — **CONTRACT READY**
- [`equipment-slots-and-the-single-stat-rebuild.md`](equipment-slots-and-the-single-stat-rebuild.md) — the five slots, the setter and the stat rebuild `002FEF30` — **AUDITED**
- [`using-an-item-is-an-action-that-costs-an-item.md`](using-an-item-is-an-action-that-costs-an-item.md) — prepare, consume and refund of an item action — **AUDITED**
- [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md) — the licence check for actions and equipment — **AUDITED**
- [`CONTRACT-license-check.md`](CONTRACT-license-check.md) — **BEHAVIORALLY UNDERSTOOD**
- [`license-board-grid-format.md`](license-board-grid-format.md) — the `licd` board files and their readers — **AUDITED**
- [`CONTRACT-shop-stock-ladders.md`](CONTRACT-shop-stock-ladders.md) — the shop gate walk, SG-1 to SG-7 — **CONTRACT READY**
- [`CONTRACT-bazaar-unlock-and-purchase.md`](CONTRACT-bazaar-unlock-and-purchase.md) — **BEHAVIORALLY UNDERSTOOD**
- *(nine pages added to this list 2026-10-02, OPUS, each with the status its own front matter states)*

Documented adjacency: the equipment definition's raw `Augment` byte feeds the derived automatic-effect layer - see [`../10-Status-Periodic-Terminal/Status-And-Augment-Layers/`](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/).

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
