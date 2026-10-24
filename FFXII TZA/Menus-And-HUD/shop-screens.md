---
title: "Shop screens: Buy, Sell and Bazaar, the tabs and rows each shows, the price paid, and how a trade reaches the inventory"
kind: "system"
category: "Menus and HUD"
addresses: "0x0057B800, 0x0057B890, 0x0057BD40, 0x0056DD50, 0x0057CF20, 0x0056D370, 0x0056E700, 0x0057A620"
---

## What the player sees

- Talking to a shopkeeper opens the shop's name with three choices: Buy, Sell and Bazaar.
- Sell is greyed with "You possess no saleable items." and Bazaar with "No bazaar goods currently available." when
  there is nothing to show.
- Each choice opens tabs such as WEAPONS, ARMOR and LOOT; a tab with nothing in it is left out.
- Picking a row opens a quantity window, and confirming again makes the trade; the gil total rolls to its new value.
- After buying equipment the shop asks "Equip your purchase now?"; after a bazaar purchase it shows what the good
  gave.

## How it works

### Opening a shop

A script opens a shop with `openfullscreenmenu_48d(2, shop)`, menu request 10 ([Menus](menus.md)). The request's
screen calls `0x0057B800(shop)` (`0x0027FCDA`), which creates the command list `0x0057B890`. The shop number is the only
argument; the mode is chosen inside the screen. The title is the shop's name, `0x002FAE40(shop)` (`0x0057B98F`-`0x0057B9C1`).

### The window's memory

The shop window takes two blocks:

1. The window itself, a `0x268`-byte (616-byte) widget that `0x0057B800` builds with procedure `0x0057B890`
   (`0x0057B866`-`0x0057B872`). It ends with 128 bazaar ids, `u16` at `+0x168`-`+0x267`, indexes 0 to 127.
2. A `0x7D0`-byte (2,000-byte) block that message 1 takes from arena 2 (`0x002497E0(2, 0x7D0)`, `0x0057B8DC`-`0x0057B906`)
   and keeps at `+0x160`. It holds 1,000 ids, indexes 0 to 999. Message 18 frees it (`0x003697F0`, `0x0057BCAC`-`0x0057BCB8`).

`0x002497E0(arena, size)` selects the arena (`0x0036C1D0`), allocates (`0x0036A100`) and restores the arena (`0x0036C140`).
The tab rows are a third, per-tab block: `0x0057CDD0(n)` takes `n x 0x20` bytes from the same arena and zeroes them.

The two id arrays are filled by `0x002FA920`, which writes one id per good and takes no length:

- `0x0057B6F0`, the new-goods check, lists the shop's bazaar goods on offer into `+0x168` (mode 2, `0x0057B721`-`0x0057B736`).
  Mode 2 walks every row of the bazaar table `[0x02EBF058]` (`0x002FA9E0`-`0x002FAA1C`), 128 in every shipped
  `battle_pack.bin`, so the array is exactly as long as the table.
- `0x0057B500`, which the window sizer `0x0057BEE0` runs for every tab (`0x0057BF50`), lists a Buy tab's goods (mode 1,
  category byte `0x00D238F8 + tab`) or the bazaar's (mode 2, `0x00D23901 + tab`) into the block at `+0x160`
  (`0x0057B5E9`-`0x0057B617`).

No other instruction reads or writes the shop window's `+0x160` or `+0x168`. The block pointer at `+0x160` is
stored by message 1 (`0x0057B90B`), passed to `0x002FA920` and copied into the tab row by `0x0057B500` (`0x0057B610`,
`0x0057B61C`) and freed by message 18 (`0x0057BCAC`); the ids from `+0x168` are written by `0x002FA920` (`0x002FAA10`) and
read back only by `0x0057B6F0` (`0x0057B740`, `0x0057B74C`).

### The command rows

`0x0057B400` builds three rows (`0x0057B426`-`0x0057B44E`), and `0x0057BD40` sets whether each is offered:

| Row | Label (`menu_command.bin`) | Help | Help when greyed |
|---|---|---|---|
| `0` | Buy (`0x48B`) | "Purchase goods." (`0xC67`) | never greyed (`0x0057BE1E`) |
| `1` | Sell (`0x48C`) | "Selling loot can make new bazaar goods available for purchase." (`0xC68`) | "You possess no saleable items." (`0xCAB`) |
| `2` | Bazaar (`0x48D`) | "Purchase bazaar goods." (`0xC69`) | "No bazaar goods currently available." (`0xCAC`) |

Sell is offered when any Sell tab has goods and Bazaar when the bazaar list has any, through `0x0056E880`. A greyed row
refuses the choice (`0x0057C070`).

### New bazaar goods

Each time `0x0057BD40` runs, `0x0057B6F0` looks at every bazaar good the shop lists ([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)).
A good whose flag bit 2 is clear gets it set (`0x0030B630(id, 1)`, `0x0057B752`), and any such good makes the screen post
"New bazaar goods are now available!" (`0x805`, `0x0057B4A0`) with sound `0x27`. Only goods with bit 2 set are listed
under Bazaar (`0x0057DC82`), and buying a good clears the bit (`0x0030B630(id, 0)`, `0x0056D4C0`).

### Modes and tabs

Choosing a row runs `0x0056DD50(shop, key)` (`0x0057C101`), which makes the mode's screen. The key, from `0x00D23920`, picks
a tab set through `0x00D233A0`:

| Mode | Key | Tab set | Tabs (`menu_expansion.bin`) |
|---|---|---|---|
| Buy | `0x5AF` | 32 (`0x00D23C70`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, TECHNICKS, MAGICKS, LOOT, GAMBIT TARGETS (`0x4AB8`-`0x4AD1`) |
| Sell | `0x5A2` | 19 (`0x00D23CC0`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, LOOT |
| Bazaar | `0x5AE` | 31 (`0x00D23C60`) | Bazaar (`0x48D`) |

Only the Sell key sets the screen's sell bit (`0x0056DE3D`-`0x0056DE4E`). `0x00564780` keeps a tab only when
`0x0057D620` reports it has goods, so an empty tab never shows. Before the screen opens, `0x0057BEE0` measures every name
the mode can list and sizes the window to the widest.

### Rows

`0x005655F0` builds a tab's rows through `0x0057CF20` (`0x005656A2`), one 0x20-byte row per good:

- Buy rows come from the shop's current list, by category (`0x002FAD30`, `0x002FA920` mode 1, `0x0057CFC4`, `0x0057D022`), as
  [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) describes.
- Bazaar rows come from the shop's bazaar list (`0x002FA920` mode 2, `0x0057D07B`).
- Sell rows come from the party's inventory lists through `0x00D23D00` (`0x0057D0A2`-`0x0057D0AD`).

Each row holds the name, the id, the sellable count, the count owned and the price, filled by `0x0057DED0` (equipment),
`0x0057DAD0` (items and loot), `0x0057DD60` (magicks, technicks and gambits) or `0x0057DC30` (bazaar goods).

### Prices

| Trade | Price per unit |
|---|---|
| Buy | the good's listed price, query record `+0x28` (`0x0057DBAC`) |
| Sell | half the listed price, rounded down (`sar` at `0x0057DBC2`, `0x0057DFDE`) |

Equipment marked unsellable (record `+0x54`, `0x0057DFBF`) and loot whose half price is 0 (`0x0057DBCF`-`0x0057DBDC`) cannot
be sold. The shop screen applies no other change to a price: the four row fillers and the trade commit use the
listed value, and every write of `+0x28` in the query filler `0x0031C5D0` (14 of them) is a table load, -1 or 0.

### Refusals

`0x0056E700` refuses a choice when:

1. buying, the party already owns the most it can hold of the good (`0x0056E78F`), so a magick, technick or gambit
   already owned cannot be bought again;
2. buying, one costs more gil than the party has;
3. selling, the good cannot be sold (`0x0056E71A`);
4. selling, none of the good can be sold.

The most the party can hold is 99 for weapons, armour, accessories, ammunition, items and loot, 1 for technicks,
magicks and gambits, and 255 for bazaar goods (`0x00D235F8`).

### The quantity window

The first confirm on a row opens the quantity window at 1 (`0x0056D509`-`0x0056D598`, `0x0056C490`). Weapons, armour,
accessories, ammunition, items and loot take a number; every other kind stays at 1 (`0x00D235E8`). In the window
(`0x0056CA60`):

- left and right pick the ones or tens digit;
- up adds to that digit, up to the smaller of what the party can still hold and what the gil pays for;
- down takes away, down to 1;
- with the modifier held, up and down jump to the limit or to 1.

The help line shows "Press ... to buy goods in quantity." (`0xC6C`) or "... to sell goods in quantity." (`0xC6E`)
while a number is being entered (`0x0056C783`).

### The trade

The second confirm makes the trade at once; there is no yes-or-no box (`0x0056D450`-`0x0056D504`). The total is the row's
price times the quantity:

| Trade | Call | What it changes |
|---|---|---|
| Sell | `0x00310870(id, quantity, total, 0)` (`0x0056D478`) | removes the goods, adds the gil, and counts the sale toward the bazaar (`0x0030B270`) |
| Buy | `0x002FEEB0(id, quantity, total, 0)` (`0x0056D49A`) | adds the goods, takes the gil, and marks the good as bought (`0x0030B180`) |

Each of the two has this one caller. The inventory side is in [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md).
A sale of loot also counts `0x00316A50(0xE, quantity)`, and every purchase counts `0x00316A50(0x13, id)`. Then
`0x002A1DC0` starts the gil total rolling (`0x0056D4D9`), and when it stops the screen goes on to the step below
(`0x0056D5C7`).

### After the trade

| Trade | Next |
|---|---|
| a bazaar good | the grant window `0x0057A4E0` lists the items the good gave (`0x0057A300`, `0x0057A480`) |
| equipment bought | the equip offer `0x0057A620` (`0x0057A980`); a sale of equipment rebuilds the list |
| anything else | the list is rebuilt with the cursor kept on its row (`0x0056E410`) |

The grant window's list `0x003F4840` (from `shop_new.mrp`, kept at `0x02B5F1F8`) draws its rows through the child
`0x003F4330`, which installs the row painter `0x003F41C0` (`0x003F45AB`). For row i it reads an item id at `+0xCC + 8i`
and an amount at `+0xD0 + 8i`:

- for an id it shows the item's icon (record `+0x2C`, through `0x002FABD0`, `0x003933B0` and `0x0035D380`), its name
  (`0x002B58B0`) and the amount (`0x0029FF60`);
- for -1 it shows text `0x7D3` with the amount, formatted into `+0xE4` (`0x002B4090`).

### Row painters and the list state

`0x0056D370` installs four row painters (`0x0056D66E`-`0x0056D6AC`), each with its own label layout: `0x0056CBC0` (`0x00D23568`),
`0x0056CD50` (`0x00D23550`), `0x0056D1B0` (`0x00D23538`) and `0x0056CF10`, which also paints the quantity column (`0x00D23520`). A
painter greys a row (`0x00392FC0`, or `0x00393240` on four labels in `0x0056CF10`):

- buying, when its price `+0x10` (low 31 bits) is above the gil (`0x00253690`); in `0x0056CD50` and `0x0056D1B0` also when the
  party already holds one (`+0x0E`), and in `0x0056CF10` when it holds 99;
- selling, when the price word's bit 31 marks it unsaleable or its sellable count `+0x0C` is 0;
- with the quantity window open, every row but the cursor's.

`0x0056D870(row, widgets, layout)` paints the common part: the icon frame `+0x0A` (none for `-1`), the name and the price.
`0x0056DA80` paints the quantity window's row: the quantity and, when bit 2 is set, the price times the quantity
(`0x0029FF60`). `0x0056D9D0(list, quantity)` stores the quantity at `+0xDC`, sets `+0xE4` bit 2 when `0x0056E700` refuses it
and bit 3 when it is not 1, and passes both to the list.

### Tabs and the help line

- `0x0057D600(buy)` gives the tab count, 9 when buying and 6 otherwise; `0x0057D5E0(buy, i)` the category of tab `i`,
  from `0x00D23D60` (buy: 20 to 27 and 29) or `0x00D23D6C` (otherwise: 8 to 12 and 15); `0x0057D610` is `0x0057D620` with 0.
- Categories 20, 21 and 22 are the three key-item tables. The row builders `0x0057CF20` (`0x0057D420`-`0x0057D45E`) and
  `0x0057D620` (`0x0057D9C2`-`0x0057D9FD`) pass `0x0057DAD0` an end and a start, and it keeps an id only when
  start <= id < end (`0x0057DB2C`-`0x0057DB3B`): category 20 takes `0x8060`-`0x81FF`, 21 takes `0x8000`-`0x803F` and
  22 takes `0x8040`-`0x805F` ([Key item list](../Items-Equipment-Shops-And-Licenses/key-item-list.md)).
- `0x0057CE10(category)` returns the category's row table, one of 17 between `0x00D239A0` and `0x00D23A50`; `0x0057CDD0(n)`
  allocates `n` zeroed 0x20-byte rows from arena 2 (`0x002497E0(2, n x 0x20)`, `0x0057CDDC`-`0x0057CDF6`).
- `0x0056DED0(screen)` is the screen's step: the quantity window's input while it is open (`0x0056CA60`); otherwise the
  tab switch of the [Inventory screen](inventory-screen.md) (`0x00563EC0`, `0x00564300`), which redraws the tab strip
  (`0x005674B0`), takes the help kind `0x0056DC30(category)` into `+0x191`, rebuilds the list (`0x0056C950`, `0x0056E410`)
  and plays sound 10.
- `0x0056DC30` maps categories to help kinds: 0 to `0xB`; 1-4 to 0; 5-8 to 1; 9 to 2; 10 and 27-30 to 3; 11 to 4; 12 and
  31 to 8; 13 to 9; 14 to 10; 15 to 5; 16-21 to 6; 26 to 7; any other to `0xFF`.
- `0x0056E5D0(screen, x)` writes the help line when the mode has goods (`0x0056E880`): `0xC6B`, or `0xC6D` when selling,
  and the row's description through `0x00293100(0x00D235D8[kind], id << 16)`; for kinds other than 11 it also shows the
  member panel for the id (`0x002CC4F0`, `0x002CC2A0`; [Menu screens](menu-screens.md)). `0x0056E840(kind)` and
  `0x0056E860(kind)` read the bytes at `0x00D235D8` (kinds to 11) and `0x00D235C8` (to 10).
- `0x0057B660(mode)` gives 9 for Buy, 6 for Sell and 1 for Bazaar.

### Closing the window

- `0x0056C850(list)` closes the quantity window and rebuilds the list (`0x0056E410`, `0x0056C490`); with no rows left it
  clears the help and closes the screen (`+0x194` bit 2, `0x00244F00`), otherwise it re-attaches the screen and redraws
  the help (`0x0056E5D0`).
- `0x0056E580(screen, v)` returns from the equip offer (`0x0057ADCD`, `0x0057AFFA`, `0x0057C04B`): it sets `+0x194` bit 1 when
  `v` is 0, re-attaches the screen and runs `0x0056C850`.
- `0x0056DD00(screen)` answers whether the screen may close: not while the shop window `[0x02CA9790]` and the part
  `[0x02CA97A0]` exist (`0x0057A960`), always once `+0x194` bit 2 is set, and otherwise unless `0x0057A440` reports state 2
  of `0x003F4670`.
- `[0x02CA9790]` is the shop window itself: its message 1 stores it (`0x0057B8CE`) and message 18 clears it
  (`0x0057BCC2`). `0x0057B680(i)` returns the shop window's child `+0x158` for `i` below 1, and `0x0057B6A0`, a callback of
  the grant window (`0x0057A5C0`), closes the shop's parts: the list (`0x002CA110`), the panel `[0x02CA9798]`, the help
  lines (`0x00291D80`, `0x00293110`) and the shop window (`0x0057B6D1`-`0x0057B6DF`), returning `0xC`.
- `0x0057C010` is the grant window's other callback; `0x0057A4E0` installs it beside `0x0057B6A0` (`0x0057A5CC`). It passes the
  name id of the shop byte `+0xC0` of `[0x02CA9790]` (`0x002FAE40`) through `0x003EABE0` to `0x002CA150(…, 0)`, runs
  `0x002CE7A0(1)` and `0x0056E580([0x02CA9798], 0)`, re-attaches `[0x02CA9790]` (`0x00246AD0`) and returns `0xC`.
- `0x0057CD00(table, id)` returns the index of `id` among the 16-byte entries at `+0x5B8` (count `+0x636`), or 0, for
  the sort strip (`0x005669A5`).

The equip offer checks each party member (`0x00317B70`):

1. When someone can equip it, it asks "Equip your purchase now?" (`0x803`).
2. For the categories in `0x00D23910` it says instead that the item cannot be equipped at a shop and to use the Equip
   command in the Party Menu (`0xCF8`).
3. Yes opens the member picker `0x0057AC10`, "Select a character to equip." (`0xC70`), which equips through
   `0x0031A510` (`0x0057AF18`) once per copy bought.

## Layouts

### The grant list

The grant list is the `0x130`-byte widget with procedure `0x003F4840` that `0x003F47E0` builds and that keeps itself at `0x02B5F1F8`; the grant window `0x0057A4E0` and the quest result window use it.

`GrantList` (`0x130` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x003F4840` |
| `+0x0C0` | `u8` | page | the page on show: 0 none yet (the construct message, `0x003F48E1`), 1 the item list (`0x003F47BB`), 2 the second list (`0x003F4747`). `0x003F4690` opens the next page from it (`0x003F46A8`): from 0 the item list when the copied reward record has its gil bit or item pairs, else the second list when it has single items; from 1 the second list when there are single items; otherwise it answers 0 and message 12 (sub-command `0x12`, the page is done) closes the window. Message 12 drops the finished page's child by it (`0x003F49AE`). `0x003F4670` returns it, or 3 when no window exists (`0x003F4682`); the grant window `0x0057A4E0` and `0x0057A440` wait on that, and so does the quest result window `0x003F4E70` for 3 (`0x003F4F56`) |
| `+0x0C1` | `u8[7]` | pad0C1 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `u64` | owner | the creator's first argument, the first qword of the creation record (`0x003F487F`; `0x0057A4E0` passes its rsi); handed to the item list child `0x003F4330` as the first word of its creation record (`0x003F4750`) |
| `+0x0D0` | `u8[16]` | reward00 | bytes `0x00`-`0x0F` of the `0x24`-byte reward record the creator points to (`0x003F488D`): byte `+0x00` bit 0 marks gil, word `+0x08` the number of item pairs and word `+0x0A` the number of single items, which `0x003F4690` tests to choose the pages (`0x003F46D4`, `0x003F46D9`, `0x003F46E3`); both children get this copy's address (`0x003F46F7`, `0x003F4768`) |
| `+0x0E0` | `u8[16]` | reward10 | bytes `0x10`-`0x1F` of the copied reward record (`0x003F4898`), read by the two children through the copy's address |
| `+0x0F0` | `u8[4]` | reward20 | bytes `0x20`-`0x23` of the copied reward record (`0x003F48A2`), read by the two children through the copy's address |
| `+0x0F4` | `u8[4]` | pad0F4 | read and written by no function; nothing fixes its width |
| `+0x0F8` | `u8[16]` | callbacks00 | bytes `0x00`-`0x0F` of the `0x18`-byte block the creator's third argument points to, or zero when it is null (`0x003F48B4`, `0x003F48CA`, `0x003F48D1`); the grant window `0x0057A4E0` fills it with a byte at `+0x04`, -1 at `+0x06` and the function `0x0057B6A0` at `+0x08`. Both children get its address (`0x003F470D`, `0x003F476D`) |
| `+0x108` | `void*` | callbacks10 | bytes `0x10`-`0x17` of that block (`0x003F48C0`, `0x003F48D8`): the second function, `0x0057C010` from the grant window `0x0057A4E0` |
| `+0x110` | `void*` | itemList | the item list page, `0x128` bytes with procedure `0x003F4330` (`0x00244F50` at `0x003F47A4`, stored at `0x003F47AC`, opened at `0x003F47B6`); 0 on construction (`0x003F48E8`) and when message 12 finishes page 1 (`0x003F49CC`) |
| `+0x118` | `void*` | secondList | the second page, `0xF0` bytes with procedure `0x003F4060`, for the record's single items (`0x00244F50` at `0x003F4730`, stored at `0x003F4738`); 0 on construction (`0x003F48EF`) and when message 12 finishes page 2 (`0x003F49C1`) |
| `+0x120` | `u32` | ownsPicture | bit 0 set when the window loaded its own picture, kind 7 id `0x96` (`0x003F4941`), clear when the caller gave one (`0x003F48FF`); the construct message opens the window at once only without it (`0x003F497A`); the closing message 15 frees the picture only with it (`0x003F49F4`) |
| `+0x124` | `u8[4]` | pad124 | read and written by no function; nothing fixes its width |
| `+0x128` | `void*` | picture | the picture the item list draws with: the caller's (the creator's fourth argument, from `0x0057A4E0`'s [r9 + `0x158`], `0x003F4906`) or the load request kind 7 id `0x96` (`0x00249320`, `0x003F4935`); handed to the item list (`0x003F477E`); freed and cleared by the closing message 15 when owned (`0x003F49FD`-`0x003F4A17`) |

### The shop window

The shop window is the `0x268`-byte widget with procedure `0x0057B890` that `0x0057B800` builds (The window's memory above).

`ShopWindow` (`0x268` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[192]` | header | the widget header, written by the constructor `0x002465F0` (Widgets, The header); procedure `0x0057B890` |
| `+0x0C0` | `u8` | shop | the shop number, the construct message's argument a (`0x0057B8BD`-`0x0057B8C3`): the title is the shop's name `0x002FAE40`(shop) on opening (message 16, `0x0057B977`) and on return from a trade (`0x0057C01B`); the tab lists `0x0057B500` (`0x0057B5E9`, `0x0057B609`) and the new-goods check `0x0057B6F0` (`0x0057B70A`, `0x0057B71A`) list its goods; `0x0057BD40` asks `0x0056E880` whether rows 1 and 2 are offered for it (`0x0057BE23`); choosing a row opens the trade screen `0x0056DD50`(shop, text) (`0x0057C0F0`); the grant window `0x0057A4E0` reads it (`0x0057A573`) |
| `+0x0C1` | `u8` | savedMenuByte | byte `+0xDE0` of the menu layout block [`0x0209AC30`] when the shop opens (`0x0057B92F`-`0x0057B936`); the construct message then calls `0x00285F20`(0), and message 18 restores the saved value with `0x00285F20` (`0x0057BCA0`) |
| `+0x0C2` | `u8[2]` | pad0C2 | read and written by no function; nothing fixes its width |
| `+0x0C4` | `u8` | activeRow | the command row whose trade screen is open: `0x0057C070` stores the confirmed row (`0x0057C0AA`); `0xFF` for none (the construct message `0x0057B8F1`, message 8 `0x0057BA83`). While a row is active `0x0057BD40` draws it in style 0 and the other rows in style 3 (`0x0057BE3C`-`0x0057BE57`); message 8 runs `0x002CB8B0` unless it is row 2 (`0x0057BA72`) |
| `+0x0C5` | `u8[3]` | pad0C5 | read and written by no function; nothing fixes its width |
| `+0x0C8` | `i16` | listCursor | the head of the command rows' list state: `0x002CD4D0` sets it to 0, points `+0xD0` at the rows and registers the state at [`0x0209AC30`] + `0x330` (`0x002CD4E5`, called by `0x0057B400` at `0x0057B421`); the command list builder `0x002C9BF0` takes it as the list's row (`0x002C9C79`) |
| `+0x0CA` | `u8[6]` | pad0CA | read and written by no function; nothing fixes its width |
| `+0x0D0` | `void*` | rowsPointer | the address of the three command rows at `+0xD8`, stored by `0x002CD4D0` (`0x002CD4EB`); read for a row's help text (`0x0057B983`, `0x0057BAC9`, `0x0057BB51`) |
| `+0x0D8` | `u8[96]` | rows | the three `0x20`-byte command rows (The command rows above): `0x002CD4D0` clears them (memset `0x60`, `0x002CD4F1`); `0x0057B400` labels them `0x48B`-`0x48D` with help `0xC67`-`0xC69` (`0x002CD3C0`, `0x0057B426`-`0x0057B44E`); `0x0057BD40` puts a row's help text at its `+0x18` (`0x0057BE80`); the cursor message `0x8000` and message 8 show that help (`0x00291D80`, `0x0057BB5C`, `0x0057BAD6`) |
| `+0x138` | `u32[3]` | offered | per command row, whether it is offered: `0x0057BD40` stores 1 for row 0 and `0x0056E880`(shop, ...) for rows 1 and 2 (`0x0057BE1E`-`0x0057BE3A`); `0x0057C070` refuses a confirmed row whose entry is 0 (`0x0057C087`). The construct message clears the three (`0x0057B8E1`, `0x0057B8E8`) |
| `+0x144` | `u8[4]` | pad144 | read and written by no function; nothing fixes its width |
| `+0x148` | `void*` | commandList | the command list widget, built by `0x002C9BF0` from the rows (`0x0057B47B`, stored at `0x0057B483`), 0 at construction (`0x0057B8D5`); message 10 hands it the input (`0x002D3900`, `0x0057BB00`); its `+0xE0` gets bit 17 when a row is chosen (`0x0057C0A3`-`0x0057C0B1`) and loses it on message 8 (`0x0057BAE0`), and gets bit 21 on sub-command `0x12` (`0x0057BB76`) and loses it on `0xF` (`0x0057BBA9`); message 8 reads its cursor to show the row's help (`0x0057BA8F`) |
| `+0x150` | `u32` | flags | bit 0: picture `0x16` was loaded here (`0x0057B7E7`) and message 18 releases it (`0x002F83E0`(`0x16`), `0x0057BC8D`); bit 1: the bazaar has new goods, set by `0x0057BD40` when `0x0057B6F0` finds some (`0x0057BDD2`), which makes message 19 and sub-command `0x12` show them (`0x0057B4A0`, `0x0057BA14`) and is cleared by the answers `0x8100`-`0x8102` (`0x0057BBF9`); bit 2: the window is closing for a trade, set by `0x0057B6A0` (`0x0057B6D8`) and taken by message 19 (`0x0057B9F1`-`0x0057B9FE`); bit 3: set by message 15 (closing begins, `0x0057BC18`), cleared by message 14 (`0x0057B9E2`); bit 4: set by message 20 unless bit 2 is set (`0x0057BC52`-`0x0057BC5F`), after which each tick waits for `0x00283980` and destroys the window (`0x0057BA31`-`0x0057BA53`); bit 5: sub-command `0xF`'s argument (`0x0057BB8C`-`0x0057BB9E`), cleared by message 8 (`0x0057BAF1`); message 8 does its work only with bit 5 set or bit 3 clear (`0x0057BA60`-`0x0057BA6C`). The construct message sets it to 0 (`0x0057B900`) |
| `+0x154` | `u8[4]` | pad154 | read and written by no function; nothing fixes its width |
| `+0x158` | `void*` | picture | the shop's one picture, kind 7 id `0x96` (the list `0x00D238E0`, one entry): `0x0057B780` has `0x003933F0` load it here (`0x0057B792`, `0x00393431`); `0x0057B680` returns it for index 0 (`0x0057B697`); the grant window `0x0057A4E0` (`0x0057A5DD`), the equip offer `0x0057A980` (`0x0057A9B6`) and `0x0057C070` (`0x0057C0D1`) use it; message 18 releases it through `0x003938B0` (`0x0057BC6D`, `0x003938D0`, `0x003938DD`) |
| `+0x160` | `void*` | goodsBlock | the `0x7D0`-byte block of 1,000 good ids taken from arena 2 by the construct message (`0x002497E0`, `0x0057B90B`); `0x0057B500` has `0x002FA920` fill it for each tab and copies it into the tab row (`0x0057B610`, `0x0057B61C`); message 18 frees it (`0x003697F0`, `0x0057BCAC`) |
| `+0x168` | `u16` | bazaarIds | the first of the 128 bazaar good ids at `+0x168`-`+0x267` that the new-goods check `0x0057B6F0` has `0x002FA920` fill (`0x002FAA10`) and reads back (`0x0057B740`, `0x0057B74C`) |
| `+0x16A` | `u8[254]` | bazaarIds2 | ids 1-127 of the same array |

## Shipped data

| | |
|---|---|
| shops | 57, opened by 98 `openfullscreenmenu_48d(2, shop)` calls in 44 script files |
| distinct goods sold | 589: 106 weapons, 104 armour, 22 accessories, 16 ammunition, 41 items, 7 technicks, 50 magicks, 2 loot, 241 gambits |
| shops that can show each Buy tab | WEAPONS 16, ARMOR 16, ACCESSORIES 15, AMMUNITION 14, ITEMS 30, TECHNICKS 16, MAGICKS 19, LOOT 2, GAMBIT TARGETS 6 |
| largest stock | shop 7, 241 gambits |

## Modding notes

- A shop's stock is its lists in the shop table; the screen shows whatever those lists hold for the current story
  point.
- A new Buy tab needs an entry in tab set 32 at `0x00D23C70` and a goods code in `0x00D23D60`.
- The sell price is always half the listed price; changing it means changing the `sar` in the row fillers.
- Raising a kind's limit in `0x00D235F8` lets the party buy more of it at once.
- A bazaar table of more than 128 goods, with more than 128 on offer at once, makes `0x0057B6F0` write past the shop
  window's 616 bytes; a list of more than 1,000 goods for one tab overruns the 2,000-byte block at `+0x160`.

## Related

- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the shop table and which list is current.
- [Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md) - how bazaar goods unlock.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - what a trade writes.
- [Menus](menus.md) - the request that opens the shop.
- [Dialogs](dialogs.md) - the shared boxes.
