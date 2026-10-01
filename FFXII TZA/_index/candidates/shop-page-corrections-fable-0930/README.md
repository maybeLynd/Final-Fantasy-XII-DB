# The shop page corrected on GR-13 / GR-14 / GR-15: one row layout, a stable shop price, five high-band records (FABLE, 2026-09-30)

Request: `DATA-REQ-FABLE-SHOP-PAGE-GR13-15-0930`. Source: OPUS's record
[`gr13-15-shop-list-widget-0930`](../gr13-15-shop-list-widget-0930/README.md), section "Page contradictions found
(routed to FABLE, not edited)", commit `9c71391a8`. Page:
[the shop table and its stock gates](../../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md).

The page edit is staged as `Database/Tools/work/FABLE/pagecorr/apply_shop.py` (20 anchors, each matching once; CRLF-safe;
all-or-nothing; `--check` validates without writing). Every byte fact the edit states was read again in the image by
[`shop_page_check.py`](shop_page_check.py) → [out](shop_page_check.out), **FAILS 0**.

## What is applied

Each struck sentence is on the page at HEAD, and each correction carries a dated note that links OPUS's record and
this one. No checkbox state changes and no register row changes.

1. **One row layout.** `0057DAD0`'s cursor is `entry + 8` (`0057DAFF`), and the entry is `rbx - 8` (`0057DB55`). Read
   from the entry, its stores are the name pointer at `+0`, the id at `+8`, the class byte at `+0xA`, the owned count
   or `0xFFFF` at `+0xC`, channel 1 at `+0xE` and the price at `+0x10`. These are the offsets the other three fillers
   write. The following were struck and corrected:
   - "three fillers because there are two row layouts" and "does not build the same row";
   - "So it is three fillers on layout A and `0057DAD0` alone on layout B" and "The two row layouts stand";
   - "a tighter row with no name pointer";
   - the bit-3 bullet's "`+4`", which is now cursor `+4` / entry `+0xC`;
   - "the tail arm selects the row layout", which is now "the filler".

   The layout table's `0057DAD0` column is relabelled as cursor offsets. The two "layout-B half is GR-13" sentences now
   name the zero-price bit's reader: in sale mode, `0056E700` scores 8 for a row with bit 31 set, and the driver
   declines it.
2. **`+0x10` is reused only on inventory-menu lists.** "`+0x10` is not a stable price field ... overwritten when the row
   is laid out" is struck, and so is the entry table's "the layout pass overwrites these bytes". The message-26 arm
   `005651E0` is entered only from the four list procedures, and those are named only by `lea`s in `00564B90`. The shop
   widget and the driver send message 26 to an empty stub.
3. **Five more reference sites.** "nine reference sites in the entire image, and all nine are inside these two builders"
   and "`+2` is skipped every time" are struck. The builders' nine sites are image-base-relative. Five more are
   rip-relative (`00565C25`, `00565D06`, `00563E37`, `00563F5B`, `003FE2C5`), and three of them read word 1 as the first
   argument of `00293110`. Statement 3 of OPUS's record keeps the wording "unread by these two builders".
4. **Five high-band records.** "the four high-band words ... are 1, 1, 2, 3", the "records {1, 1} and {2, 3}" reading,
   and "kinds 0 and 1 arrive as selectors 0x40 and 0x41" are struck. The records are `{1,1} {2,3} {2,4} {2,4} {3,5}`,
   for kinds 0–4, selectors `0x40`–`0x44`. Head arm 4's row gains its default selectors: `0`–`4` and `0x42`–`0x44`,
   because the `ja` at `0057CF94` leads to `0057D08B`.
5. **Bit 5 is set for selector `0x0F` only.** The bit table's "tail arm 3 `0057D3EA`" is struck and replaced by the
   `or` / `cmp esi, 0xf` / `cmovne` sequence. The GR-13 box's reason "so the question is live for shop stock" is struck,
   with a note that it does not hold for the Buy tab. The box stays ticked.
6. **The `+0xC0` pairing is proven.** "read from this pairing, not proven separately" is struck. `0056DD50` creates
   the shop widget (procedure `0056E140`) and passes it to `0056C950`. That function creates the `0056D370` widget and
   stores it at the shop widget's `+0xC0` (`0056C9BC`–`0056C9CB`).

## What is not applied, and why

- **The front-matter `status:` line.** It still says "three list-interface questions stay open" and names a "layout-B
  row". It is a status field that gates parse, and whether the page's status moves now that GR-13, GR-14 and GR-15 are
  answered is the owner's call. Routed to FABLE; this edit does not change the line.
- **OPUS's "only `0057DED0` also writes `+0xB`"** is not written. The check did not read it again.
- **Statement 2's widget-id range** (`0x405`–`0x40F`, record steps B3/C1) is written as GR-14's result, not as a
  new reading. The check reads again that `005651E0` is entered only from the four procedures, and that each of them
  is named only by one `lea` in `00564B90` and by no call or data qword. It does not decode `00564B90`'s id table.
- **The paragraph "the third piece of authored data ... with no reader in the bodies that own it"** stays as written.
  It is scoped to the two builders, and OPUS's record says that scope still holds. The new sentence next to it says the
  second word is read elsewhere.

## Limits

- `00563F62` loads word 1 into `ecx`. The call to `00293110` at `00563F7D` follows only when bit 8 of `r10d` is clear.
  The page says "the first argument of `00293110`", and that is the path it means.
- Static only. Instructions are decoded linearly from their function's start (retool's extents). Two scans find the
  band-table sites: retool's rip-reference index, and a raw `.text` `lea` scan that does not depend on the extents.

## Check

[`shop_page_check.py`](shop_page_check.py) → [out](shop_page_check.out): 57 steps, **FAILS 0**. Controls:
- **P1:** the driver's known price read and bit-31 clear must decode.
- **P2:** the raw `lea` scanner must find the known bank `lea` (16 sites on the party bank, as in GR-8).
- **P3:** a wrong expectation, "price stored at cursor `+0x10`", must fail to match.

## Consumer check

affected: `Database/FFXII TZA/12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md`

- consumer: `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` (layout table, bit table, list-kind section, section 5 note, section 7 boxes): revised-here.
- consumer: `12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md` front-matter `status:`: routed-to FABLE (see "not applied").
- consumer: the same page's in-place notes by SWE2-STRUCT for OPUS (commit `e54b8e670`, landed while this was drafted): they annotate statements 3 and 6 after the original sentences without striking them. They agree with the corrections here, so the strikes stand and the notes remain. Statement 6's struck sentence is now directly followed by that note, and FABLE may drop one of the two.
- consumer: `16-UI/Shop-Screens/the-shop-screens.md` (`0057D620` "the price/name formatter", lists `0057DAD0` as a callee): agrees (no layout claim).
- consumer: `12-Items-Equipment-Shops-License/the-bazaar-recipe-unlock-and-purchase.md` (`0057DAD0` "a shop/bazaar sibling"): agrees.
- consumer: `00-Engine-Core-Runtime/the-encoded-id-class-registry.md` (`0057DAD0`'s six sites, classes 5, 7, 13): agrees.
- consumer: `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` (the stale `byte[rec + 0x54]` now has a consumer, the sale test): routed-to that page's owner, as OPUS's record already routes it.
- consumer: `_index/OPEN-QUESTIONS.md` rows GR-13, GR-14, GR-15: routed-to OPUS (the source record's own routing; no register edit here).

## Regression

run: shop_page_check.py at 4b748e8af (FAILS 0; controls P1 to P3)
