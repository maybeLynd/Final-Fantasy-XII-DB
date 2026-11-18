[Home](../../README.md) / [Items, equipment, shops and licenses](README.md) / Bazaar

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Bazaar: every bazaar good, the loot you must sell to unlock it, its price, what it gives, and how unlocking and buying work | reference | Items, equipment, shops and licenses | Shops and bazaar | Each of the 128 goods of the bazaar table: its name, price and the items it gives, the up to three loots and counts that must be sold to unlock it, whether it can come back after it is bought, and whether a script sets it instead, with the loot-sold tally, the refresh after every sale, the flag byte that shows a good, the purchase that empties the tallies, and the two script verbs that offer the Grimoires. | 0x02EBF058, 0x0030B270, 0x0030B180, 0x002FEEB0, 0x00310870, 0x0030B570, 0x002FD780 |

## What it lists

A bazaar good is an id `0xD000 + good`, a bundle that gives up to three items when bought. Selling enough of
its loots unlocks it; buying it uses up the loot sold.

### The table

The goods are section 57 of `battle_pack.bin`, the section its directory entry at file offset `+0xE8` points to,
bound to `0x02EBF058` by the battle data binder (`0x00236F6E`-`0x00236F7C`). It is an `st2e` table of 128 rows of 36
bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | name | name word, read by the query filler `0x0031C5D0` |
| `+0x02` | `u16` | description | description text id, read by the query filler |
| `+0x04` | `u16` | item0 | first item given (`0x002FD780`, `0x002FD7F2`-`0x002FD85D`) |
| `+0x06` | `u8` | count0 | its count; 0 for no item |
| `+0x08` | `u16` | item1 | second item given |
| `+0x0A` | `u8` | count1 | its count |
| `+0x0C` | `u16` | item2 | third item given |
| `+0x0E` | `u8` | count2 | its count |
| `+0x10` | `u32` | price | price in gil, copied to the query record's `+0x28` (`0x0031DA1F`) |
| `+0x14` | `u16` | flags | bit `0x1` it can come back, bit `0x2` a script sets it (`0x0030B33F`, `0x0030B5F6`) |
| `+0x16` | `u16` | loot0 | first loot to sell; an unused slot is id 0 with count 0 (`0x0030B375`-`0x0030B45F`) |
| `+0x18` | `u8` | lootCount0 | its count |
| `+0x1A` | `u16` | loot1 | second loot to sell |
| `+0x1C` | `u8` | lootCount1 | its count |
| `+0x1E` | `u16` | loot2 | third loot to sell |
| `+0x20` | `u8` | lootCount2 | its count |
| `+0x22` | `u16` | c22 | 120 on every row, copied to the query record's `+0x2C` (`0x0031DA32`-`0x0031DA36`) |

### Unlocking a good

Each loot id has a sold tally, one byte in the inventory at `+0x57C8 + loot`, kept between 0 and 99
([Inventory](inventory.md)). A sale through `0x00310870` takes the loot from the inventory, adds the gil (`0x003108AB`-`0x003108BD`), adds the
quantity to the tally (`0x003108D1`-`0x003108E8`) and then runs the refresh `0x0030B270` (`0x003108ED`), its only caller.

`0x00310870(id, quantity, price, flags)` removes the loot with `0x003008A0(id, -quantity, 0, 1, flags)` and hands the
gil setter `0x00254EE0` the old gil plus `price`, floored at 0, `new = max(old + price, 0)` (`0x003108A6`-`0x003108BD`);
the setter meters `new - old` as gil gained or spent (`0x00316A50` kind 6 or 7, `0x00254EF1`-`0x00254F02`) and stores
`new` capped at 99,999,999 (`0x00254F09`-`0x00254F1F`; [Gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

It adds the
quantity to the tally with
`0x003008A0(id, quantity, 0, 3, 0)` (`0x003108D1`-`0x003108E8`). With `flags` bit `0x1` it also posts the gain
notification `0x00469E80(new - old)` (`0x003108C2`-`0x003108CC`); the shop's transaction function gives it `flags` 0
(`0x0056D457`), so no notification is posted. The sale returns 1 (`0x003108F7`).

The refresh checks every good (`0x0030B270`-`0x0030B468`):

1. A good already unlocked once, flag byte bit `0x1`, is skipped unless it can come back (`0x0030B33F`-`0x0030B34C`).
2. A good on offer now, flag bit `0x2`, is skipped (`0x0030B352`-`0x0030B359`).
3. A good with no loot to sell is skipped (`0x0030B35F`-`0x0030B36F`).
4. Each of its three loots must have a tally at least its count (`0x0030B375`-`0x0030B45F`). An unused slot is id 0
   with count 0, so it compares item 0's tally, always 0, with 0 and passes; an id of `0xFFFF` would read as -1
   and fail.
5. When all three are met, flag bits `0x1` and `0x2` are set (`0x0030B461`).

The tallies are read through the loot class's query handler `+0x50` with mode 3, inline for the first two loots
and through `0x0030ADC0` for the third (`0x0030B385`-`0x0030B3CC`, `0x0030B44E`-`0x0030B454`). An id whose class nibble is
`0xF` reads -1, like `0xFFFF`, and an index at or above its class's count, or a class with no handler, reads 0
(`0x0030B37A`-`0x0030B3D2`). The tallies are compared as signed values (`0x0030B3DA`, `0x0030B44C`, `0x0030B45F`).

With no goods table bound at `0x02EBF058` the refresh checks nothing. It returns 1 (`0x0030B279`-`0x0030B295`,
`0x0030B496`).

The flag bytes are one per good at `+0x59C8` of the party block. The shop menu lists every good whose bit `0x2` is
set (mode 2 of `0x002FA920`, [Shops](shops.md)).

Of the fourteen instructions that address `+0x59C8`, the refresh's `or` (step 5 above) is the only one that sets bit
`0x1`. `0x0030B630(id, on)`, for a bazaar id that `0x00322C50(1, id)` accepts, stores bit `0x4` as `on & 1`
(`0x0030B63A`-`0x0030B686`; [Shop screens](../Menus-And-HUD/shop-screens.md)).

### Buying a good

The shop's transaction function `0x0056D370` reads the price from the good's query record, clears its bit `0x80000000` and
multiplies it by the quantity (`0x0056D461`-`0x0056D473`). The purchase `0x002FEEB0(id, quantity, price, flags)` adds the
good through `0x003008A0`, which hands out its
items (`0x002FEEDB`, `0x002FD780`), takes the price from the gil, floored at 0, through `0x00253690` and `0x00254EE0` (`0x002FEEE0`-`0x002FEEF3`; [Gil](../Rewards-EXP-Gil-And-Loot/gil.md)), and calls
`0x0030B180` (`0x002FEF0A`).

`0x002FEEB0` adds the good with `0x003008A0(id, quantity, 0, 1, flags)` and sets the gil to the old gil less `price`,
floored at 0 (`0x002FEECF`-`0x002FEEF3`). With `flags` bit `0x1` it then calls the gain notification
`0x00469E80(new - old)`, an amount of 0 or less, which posts nothing (`0x002FEEF8`-`0x002FEF02`); the shop's transaction
function gives it `flags` 0 (`0x0056D457`). The purchase returns 1 (`0x002FEF14`).

For a bazaar id, `0x0030B180` clears flag bit `0x2`, so the good leaves the list, and sets the
tally of each of its three loots back to 0 (`0x0030B203`-`0x0030B256`). A good that can come back therefore needs its
loots sold again from zero; any other good stays unlocked once and does not return. Both the sale and the purchase
are called only by the shop's transaction function `0x0056D370` (`0x0056D478`, `0x0056D49A`).

### Goods a script offers

The seven goods with flag bit `0x2`, all named Forgotten Grimoire, have no loot to sell. Script verbs `0x2F7`
`sethoridashi` and `0x2F6` `clearhoridashi` set or clear their offer bit through `0x0032AB50` and `0x0030B570`
(`0x0034C710`, `0x0034C2C0`), which writes it only for a bazaar id, class `0xD000`, that `0x00322C50(1, id)` accepts and
whose good has that flag (`0x0030B57A`-`0x0030B5B2`, `0x0030B5F6`-`0x0030B619`). It stores bit `0x2` as `set & 1` and
keeps the other bits (`0x0030B603`-`0x0030B619`). The third verb, `0x2F5` `ishoridashi`, cannot read it: its handler
`0x0034BD90` calls `0x005C5230`, which returns 0.

`0x0032AB50(id, v)` passes `v` on as 1 for any value other than 0 and as 0 otherwise
(`0x0032AB54`-`0x0032AB59`), so any non-zero argument sets the bit.

`0x0030B570` forms the good's row address in 32 bits, `base + (id - 0xD000) × size`, from
the answer of `0x0020E600` and the row size word (`0x0030B5DC`-`0x0030B5F0`). With no goods table,
`[0x02EBF058]` null or `0x0020E600` answering null, the row address is 0 and the flag
test reads the byte at address `0x14` (`0x0030B5BE`, `0x0030B5CB`, `0x0030B5F4`-`0x0030B5F6`).

The `us` zone scripts call `sethoridashi` 135 times and never `clearhoridashi`. Each call offers one good once and sets a bit of script global byte `0x0CDA` (or, for good 99, bit `0x2` of `0x0405`) so it is not offered again. The counts are script global bytes `0x0CD0`-`0x0CD4`, each stopped at 255:

| Good | Monograph | Offered when |
|---|---|---|
| 99 | Hunter's | Gatsly is talked to in Muthru Bazaar (`rbn_a02`) after the hunt Wolf in the Waste (quest 129) is reported |
| 102 | Sage's | `0x0CD0` reaches 100: every opening of a shop through its shopkeeper's talk, all 57 shops (98 calls) |
| 100 | Knight's | `0x0CD1` reaches 30: openings of the Weapon Seller (Archades), Traveling Merchant shop 21 (Mt Bur-Omisace), Targe, Weapons of War, Amal and Beruny |
| 124 | Mage's | `0x0CD2` reaches 25: openings of Granch (Archades), Mait, Mysterious Magicks, Yugri and Quayside Magickery |
| 126 | Scholar's | `0x0CD3` reaches 15: openings of the Armor Seller (Archades), Traveling Merchant shop 22 (Mt Bur-Omisace), Rithil, Antiqued Armors, Panamis and Emma |
| 125 | Warmage's | `0x0CD4` reaches 20: talks to the six hunt notice boards, the Sandsea's from story progress above 80 |
| 101 | Dragoon's | `0x0CD4` reaches 40 |

The `script_sets_availability` cells name each shop and board.

### Clearing

Whenever the party block is bound, by `0x00233C10` (`0x00233C3A`) or `0x00238A80` (`0x00238A99`), the rebaser `0x0030B6A0`
clears every sold tally (`0x0030B702`-`0x0030B737`) and
bits `0x7` of every flag byte (`0x0030B739`-`0x0030B75B`).

`0x00233C10` is called by the load-complete call `0x00285E60` (`0x00285E86`), which the save and load screen `0x00582860` runs
on message 12 with code `0x10` (`0x00582B2C`-`0x00582B4E`; `0x00582CD0`, `0x00582CE6`), by the after-load sequence `0x0036FCC0`
(`0x0036FCF2`), which `debug_load_mapjump` and `debug_loadjfdata` reach, and, when the image header `+0x68` passes
`0x00255260`, by two frame messages ([Loading a save](../Saving-Loading-And-Settings/loading-a-save.md)):

- the area controller `0x00280140`'s, while its state byte is 1 and `0x0032E4D0` answers 0 (`0x002802B4`-`0x002802C2`,
  `0x00280357`-`0x00280379`, `0x002803B8`);
- the new-game widget `0x00394130`'s, once `0x001EDEC0(+0xB4)` answers non-zero, its state is 1 and its counter `+0xC2`
  has run out (`0x00394184`-`0x003941E3`, `0x00394222`).

`0x00233C10` binds the block, and so clears it, only while `[0x02EBF190]` is null (`0x00233C19`-`0x00233C3A`); once the block
is bound, a load through any of these callers clears nothing.

`0x00238A80` is the tail of the image reset `0x002EF650` (`0x002EF67D`), which clears the whole image
(`0x002EF656`-`0x002EF663`). The same two frame messages run it when the header fails (`0x0028037B`, `0x003941E5`), the
new-game widget runs it when it opens, on message 1 (`0x003942F2`), and `0x0022B6E0` runs it when `0x0032E520(1)` answers 0
and `0x0209273C` is 5 (`0x0022B737`-`0x0022B78B`).

## Columns

[`bazaar.tsv`](bazaar.tsv), one row per good:

| Column | Meaning |
|---|---|
| `good` | the row, 0-127 |
| `id` | its encoded id, `0xD000 + good` |
| `name` | its name from the shipped text |
| `price` | gil |
| `gives` | the items it gives, with counts and ids |
| `unlocked_by_selling` | the loots and the counts that must be sold, with ids; `-` when no sale is needed |
| `repeatable` | flag bit `0x1`: it can come back after it is bought |
| `script_sets_availability` | flag bit `0x2`: a script offers it; for the seven script goods, the `sethoridashi` calls that offer it and when ("Goods a script offers" above) |

The 128 goods cost from 70 to 600,000 gil. Fifteen can come back: goods 87-94, 103, 104 and 106-110. The seven
script goods are 99-102 and 124-126.

## Related

- [Shops](shops.md) - the shop menu that lists the goods.
- [Inventory](inventory.md) - the sold tally and the bundle ids.
- [Equipment row](equipment-row.md) - the equipment some goods give.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00322C50` is called by `0x002367A0`, `0x0023A570`, `0x0031B810`, `0x003266C0`, `0x00329CC0`; those functions
  are documented on [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [party data](../Party/party-data.md).
- Movement: `0x00322C50` is called by `0x0031BAC0`, `0x00326BB0`; those functions are documented on
  [game over](../World-Areas-And-Travel/game-over.md), [party data](../Party/party-data.md).
- Party: `0x00322C50` is called by `0x003170E0`, `0x0031AC00`, `0x0031B510`, `0x00320800`, `0x00321100`, `0x00326500`, `0x003287A0`,
  `0x00328DB0`, `0x00329080`; those functions are documented on
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party data](../Party/party-data.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Status periodic terminal: `0x00322C50` is called by `0x0030E130`, `0x0030FED0`, `0x00310DB0`; those functions are documented
  on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Input: `0x0022B6E0` calls `0x00249C30`, `0x0035E9A0`; `0x0032E4D0` is called by `0x00291D90`; `0x00582860` calls `0x00182D40`;
  those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md).
- Presentation: `0x001EDEC0` is called by `0x002B7B80`, `0x002BAF80`, `0x002BC3E0`, `0x002D2DB0`, `0x00366B80`; `0x0022B6E0` calls
  `0x00252A20`, `0x002E65A0`, `0x0036D400`, `0x0036F2C0`, `0x0036F2F0`; `0x0032E4D0` is called by `0x003B21E0`, `0x003B25D0`;
  `0x0032E520` is called by `0x003B53C0`.
- Presentation: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md),
  [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [escape](../Controls-And-Input/escape.md),
  [effect file loading](../Graphics/effect-file-loading.md).
- Presentation: and on [effect element runtime](../Graphics/effect-element-runtime.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- RNG random selection: `0x0022B6E0` calls `0x00379CD0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x0022B6E0` calls `0x0032E520`; `0x00280140` calls `0x0032E4D0`; `0x0032E4D0` is called by `0x003EADE0`; `0x0032E520`
  calls `0x0032E070`, `0x0046DFE0`; `0x0032E520` is called by `0x0024AC30`.
- Resource: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- World area: `0x0022B6E0` calls `0x003318C0`; `0x00280140` calls `0x00267C90`, `0x00268320`, `0x00314440`; `0x0032E520` is called
  by `0x003145E0`; `0x0036FCC0` calls `0x00267C90`, `0x00268320`; `0x00394130` calls `0x00267C90`, `0x00268320`, `0x00314440`,
  `0x00314DC0`; `0x00582860` calls `0x005843E0`.
- World area: those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [loading a save](../Saving-Loading-And-Settings/loading-a-save.md),
  [script variables](../Scripts-And-Script-Commands/script-variables.md),
  [debug menu](../Engine-Core/debug-menu.md).
- World area: and on [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [game over](../World-Areas-And-Travel/game-over.md), [native limits](../Engine-Core/native-limits.md).
