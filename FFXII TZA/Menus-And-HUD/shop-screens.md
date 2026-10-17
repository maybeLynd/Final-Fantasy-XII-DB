---
title: "Shop screens: Buy, Sell and Bazaar, the tabs and rows each shows, the price paid, and how a trade reaches the inventory"
kind: "system"
category: "Menus and HUD"
addresses: "0057B800, 0057B890, 0057BD40, 0056DD50, 0057CF20, 0056D370, 0056E700, 0057A620"
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
screen calls `0057B800(shop)` (`0027FCDA`), which creates the command list `0057B890`. The shop number is the only
argument; the mode is chosen inside the screen. The title is the shop's name, `002FAE40(shop)` (`0057B98F`-`0057B9C1`).

### The command rows

`0057B400` builds three rows (`0057B426`-`0057B44E`), and `0057BD40` sets whether each is offered:

| Row | Label (`menu_command.bin`) | Help | Help when greyed |
|---|---|---|---|
| `0` | Buy (`48B`<sub>h</sub>) | "Purchase goods." (`C67`<sub>h</sub>) | never greyed (`0057BE1E`) |
| `1` | Sell (`48C`<sub>h</sub>) | "Selling loot can make new bazaar goods available for purchase." (`C68`<sub>h</sub>) | "You possess no saleable items." (`CAB`<sub>h</sub>) |
| `2` | Bazaar (`48D`<sub>h</sub>) | "Purchase bazaar goods." (`C69`<sub>h</sub>) | "No bazaar goods currently available." (`CAC`<sub>h</sub>) |

Sell is offered when any Sell tab has goods and Bazaar when the bazaar list has any, through `0056E880`. A greyed row
refuses the choice (`0057C070`).

### New bazaar goods

Each time `0057BD40` runs, `0057B6F0` looks at every bazaar good the shop lists ([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)).
A good whose flag bit 2 is clear gets it set (`0030B630(id, 1)`, `0057B752`), and any such good makes the screen post
"New bazaar goods are now available!" (`805`<sub>h</sub>, `0057B4A0`) with sound `27`<sub>h</sub>. Only goods with bit 2 set are listed
under Bazaar (`0057DC82`), and buying a good clears the bit (`0030B630(id, 0)`, `0056D4C0`).

### Modes and tabs

Choosing a row runs `0056DD50(shop, key)` (`0057C101`), which makes the mode's screen. The key, from `00D23920`, picks
a tab set through `00D233A0`:

| Mode | Key | Tab set | Tabs (`menu_expansion.bin`) |
|---|---|---|---|
| Buy | `5AF`<sub>h</sub> | 32 (`00D23C70`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, TECHNICKS, MAGICKS, LOOT, GAMBIT TARGETS (`4AB8`<sub>h</sub>-`4AD1`<sub>h</sub>) |
| Sell | `5A2`<sub>h</sub> | 19 (`00D23CC0`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, LOOT |
| Bazaar | `5AE`<sub>h</sub> | 31 (`00D23C60`) | Bazaar (`48D`<sub>h</sub>) |

Only the Sell key sets the screen's sell bit (`0056DE3D`-`0056DE4E`). `00564780` keeps a tab only when
`0057D620` reports it has goods, so an empty tab never shows. Before the screen opens, `0057BEE0` measures every name
the mode can list and sizes the window to the widest.

### Rows

`005655F0` builds a tab's rows through `0057CF20` (`005656A2`), one `20`<sub>h</sub>-byte row per good:

- Buy rows come from the shop's current list, by category (`002FAD30`, `002FA920` mode 1, `0057CFC4`, `0057D022`), as
  [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) describes.
- Bazaar rows come from the shop's bazaar list (`002FA920` mode 2, `0057D07B`).
- Sell rows come from the party's inventory lists through `00D23D00` (`0057D0A2`-`0057D0AD`).

Each row holds the name, the id, the sellable count, the count owned and the price, filled by `0057DED0` (equipment),
`0057DAD0` (items and loot), `0057DD60` (magicks, technicks and gambits) or `0057DC30` (bazaar goods).

### Prices

| Trade | Price per unit |
|---|---|
| Buy | the good's listed price, query record `+28`<sub>h</sub> (`0057DBAC`) |
| Sell | half the listed price, rounded down (`sar` at `0057DBC2`, `0057DFDE`) |

Equipment marked unsellable (record `+54`<sub>h</sub>, `0057DFBF`) and loot whose half price is 0 (`0057DBCF`-`0057DBDC`) cannot
be sold. The shop screen applies no other change to a price: the four row fillers and the trade commit use the
listed value, and every write of `+28`<sub>h</sub> in the query filler `0031C5D0` (14 of them) is a table load, -1 or 0.

### Refusals

`0056E700` refuses a choice when:

1. buying, the party already owns the most it can hold of the good (`0056E78F`), so a magick, technick or gambit
   already owned cannot be bought again;
2. buying, one costs more gil than the party has;
3. selling, the good cannot be sold (`0056E71A`);
4. selling, none of the good can be sold.

The most the party can hold is 99 for weapons, armour, accessories, ammunition, items and loot, 1 for technicks,
magicks and gambits, and 255 for bazaar goods (`00D235F8`).

### The quantity window

The first confirm on a row opens the quantity window at 1 (`0056D509`-`0056D598`, `0056C490`). Weapons, armour,
accessories, ammunition, items and loot take a number; every other kind stays at 1 (`00D235E8`). In the window
(`0056CA60`):

- left and right pick the ones or tens digit;
- up adds to that digit, up to the smaller of what the party can still hold and what the gil pays for;
- down takes away, down to 1;
- with the modifier held, up and down jump to the limit or to 1.

The help line shows "Press ... to buy goods in quantity." (`C6C`<sub>h</sub>) or "... to sell goods in quantity." (`C6E`<sub>h</sub>)
while a number is being entered (`0056C783`).

### The trade

The second confirm makes the trade at once; there is no yes-or-no box (`0056D450`-`0056D504`). The total is the row's
price times the quantity:

| Trade | Call | What it changes |
|---|---|---|
| Sell | `00310870(id, quantity, total, 0)` (`0056D478`) | removes the goods, adds the gil, and counts the sale toward the bazaar (`0030B270`) |
| Buy | `002FEEB0(id, quantity, total, 0)` (`0056D49A`) | adds the goods, takes the gil, and marks the good as bought (`0030B180`) |

Each of the two has this one caller. The inventory side is in [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md).
A sale of loot also counts `00316A50(Eh, quantity)`, and every purchase counts `00316A50(13h, id)`. Then
`002A1DC0` starts the gil total rolling (`0056D4D9`), and when it stops the screen goes on to the step below
(`0056D5C7`).

### After the trade

| Trade | Next |
|---|---|
| a bazaar good | the grant window `0057A4E0` lists the items the good gave (`0057A300`, `0057A480`) |
| equipment bought | the equip offer `0057A620` (`0057A980`); a sale of equipment rebuilds the list |
| anything else | the list is rebuilt with the cursor kept on its row (`0056E410`) |

The grant window's list `003F4840` (from `shop_new.mrp`, kept at `02B5F1F8`) draws its rows through the child
`003F4330`, which installs the row painter `003F41C0` (`003F45AB`). For row i it reads an item id at `+CCh + 8i`
and an amount at `+D0h + 8i`:

- for an id it shows the item's icon (record `+2C`<sub>h</sub>, through `002FABD0`, `003933B0` and `0035D380`), its name
  (`002B58B0`) and the amount (`0029FF60`);
- for -1 it shows text `7D3`<sub>h</sub> with the amount, formatted into `+E4`<sub>h</sub> (`002B4090`).

### Row painters and the list state

`0056D370` installs four row painters (`0056D66E`-`0056D6AC`), each with its own label layout: `0056CBC0` (`00D23568`),
`0056CD50` (`00D23550`), `0056D1B0` (`00D23538`) and `0056CF10`, which also paints the quantity column (`00D23520`). A
painter greys a row (`00392FC0`, or `00393240` on four labels in `0056CF10`):

- buying, when its price `+10`<sub>h</sub> (low 31 bits) is above the gil (`00253690`); in `0056CD50` and `0056D1B0` also when the
  party already holds one (`+0E`<sub>h</sub>), and in `0056CF10` when it holds 99;
- selling, when the price word's bit 31 marks it unsaleable or its sellable count `+0C`<sub>h</sub> is 0;
- with the quantity window open, every row but the cursor's.

`0056D870(row, widgets, layout)` paints the common part: the icon frame `+0A`<sub>h</sub> (none for `-1`), the name and the price.
`0056DA80` paints the quantity window's row: the quantity and, when bit 2 is set, the price times the quantity
(`0029FF60`). `0056D9D0(list, quantity)` stores the quantity at `+DC`<sub>h</sub>, sets `+E4`<sub>h</sub> bit 2 when `0056E700` refuses it
and bit 3 when it is not 1, and passes both to the list.

### Tabs and the help line

- `0057D600(buy)` gives the tab count, 9 when buying and 6 otherwise; `0057D5E0(buy, i)` the category of tab `i`,
  from `00D23D60` (buy: 20 to 27 and 29) or `00D23D6C` (otherwise: 8 to 12 and 15); `0057D610` is `0057D620` with 0.
- `0057CE10(category)` returns the category's row table, one of 17 between `00D239A0` and `00D23A50`; `0057CDD0(n)`
  allocates `n` zeroed `20`<sub>h</sub>-byte rows (`002497E0(2)`).
- `0056DED0(screen)` is the screen's step: the quantity window's input while it is open (`0056CA60`); otherwise the
  tab switch of the [Inventory screen](inventory-screen.md) (`00563EC0`, `00564300`), which redraws the tab strip
  (`005674B0`), takes the help kind `0056DC30(category)` into `+191`<sub>h</sub>, rebuilds the list (`0056C950`, `0056E410`)
  and plays sound 10.
- `0056DC30` maps categories to help kinds: 0 to `B`<sub>h</sub>; 1-4 to 0; 5-8 to 1; 9 to 2; 10 and 27-30 to 3; 11 to 4; 12 and
  31 to 8; 13 to 9; 14 to 10; 15 to 5; 16-21 to 6; 26 to 7; any other to `FF`<sub>h</sub>.
- `0056E5D0(screen, x)` writes the help line when the mode has goods (`0056E880`): `C6B`<sub>h</sub>, or `C6D`<sub>h</sub> when selling,
  and the row's description through `00293100(00D235D8[kind], id << 16)`; for kinds other than 11 it also shows the
  member panel for the id (`002CC4F0`, `002CC2A0`; [Menu screens](menu-screens.md)). `0056E840(kind)` and
  `0056E860(kind)` read the bytes at `00D235D8` (kinds to 11) and `00D235C8` (to 10).
- `0057B660(mode)` gives 9 for Buy, 6 for Sell and 1 for Bazaar.

### Closing the window

- `0056C850(list)` closes the quantity window and rebuilds the list (`0056E410`, `0056C490`); with no rows left it
  clears the help and closes the screen (`+194`<sub>h</sub> bit 2, `00244F00`), otherwise it re-attaches the screen and redraws
  the help (`0056E5D0`).
- `0056E580(screen, v)` returns from the equip offer (`0057ADCD`, `0057AFFA`, `0057C04B`): it sets `+194`<sub>h</sub> bit 1 when
  `v` is 0, re-attaches the screen and runs `0056C850`.
- `0056DD00(screen)` answers whether the screen may close: not while the grant window `[02CA9790]` and its part
  `[02CA97A0]` exist (`0057A960`), always once `+194`<sub>h</sub> bit 2 is set, and otherwise unless `0057A440` reports state 2
  of `003F4670`.
- `0057B680(i)` returns the grant window's child `+158`<sub>h</sub> for `i` below 1, and `0057B6A0` closes the grant window's
  parts (`0057A5C0`): the list (`002CA110`), the panel `[02CA9798]`, the help lines (`00291D80`, `00293110`) and the
  window itself, returning `C`<sub>h</sub>.
- `0057C010` is the grant window's other callback; `0057A4E0` installs it beside `0057B6A0` (`0057A5CC`). It passes the
  name id of the shop byte `+C0`<sub>h</sub> of `[02CA9790]` (`002FAE40`) through `003EABE0` to `002CA150(…, 0)`, runs
  `002CE7A0(1)` and `0056E580([02CA9798], 0)`, re-attaches `[02CA9790]` (`00246AD0`) and returns `C`<sub>h</sub>.
- `0057CD00(table, id)` returns the index of `id` among the 16-byte entries at `+5B8`<sub>h</sub> (count `+636`<sub>h</sub>), or 0, for
  the sort strip (`005669A5`).

The equip offer checks each party member (`00317B70`):

1. When someone can equip it, it asks "Equip your purchase now?" (`803`<sub>h</sub>).
2. For the categories in `00D23910` it says instead that the item cannot be equipped at a shop and to use the Equip
   command in the Party Menu (`CF8`<sub>h</sub>).
3. Yes opens the member picker `0057AC10`, "Select a character to equip." (`C70`<sub>h</sub>), which equips through
   `0031A510` (`0057AF18`) once per copy bought.

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
- A new Buy tab needs an entry in tab set 32 at `00D23C70` and a goods code in `00D23D60`.
- The sell price is always half the listed price; changing it means changing the `sar` in the row fillers.
- Raising a kind's limit in `00D235F8` lets the party buy more of it at once.

## Related

- [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) - the shop table and which list is current.
- [Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md) - how bazaar goods unlock.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - what a trade writes.
- [Menus](menus.md) - the request that opens the shop.
- [Dialogs](dialogs.md) - the shared boxes.
