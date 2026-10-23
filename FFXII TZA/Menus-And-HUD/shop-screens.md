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

These are the only uses of the shop window's `+0x160` and `+0x168` in the 213 functions from `0x0056C000` to
`0x0057E000` and the eight that load `[0x02CA9790]`. The other operands with those displacements there belong to other
records: the stack slot `[rsp+0x160]` of `0x0057C140` (`0x0057C2AF`), and `+0x168` of another widget's own record in
`0x0056F5F0` (`0x0056F6F2`), `0x0056F810` (`0x0056F853`, `0x0056F895`, `0x0056F906`, `0x0056FA09`) and `0x0056FAD0` (`0x0056FAE8`,
`0x0056FBB1`, `0x0056FBFD`).

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
- `0x0056DD00(screen)` answers whether the screen may close: not while the grant window `[0x02CA9790]` and its part
  `[0x02CA97A0]` exist (`0x0057A960`), always once `+0x194` bit 2 is set, and otherwise unless `0x0057A440` reports state 2
  of `0x003F4670`.
- `0x0057B680(i)` returns the grant window's child `+0x158` for `i` below 1, and `0x0057B6A0` closes the grant window's
  parts (`0x0057A5C0`): the list (`0x002CA110`), the panel `[0x02CA9798]`, the help lines (`0x00291D80`, `0x00293110`) and the
  window itself, returning `0xC`.
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
