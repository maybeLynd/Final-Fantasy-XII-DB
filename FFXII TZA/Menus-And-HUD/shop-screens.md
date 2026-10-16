---
title: "Shop screens: Buy, Sell and Bazaar, the tabs and rows each shows, the price paid, and how a trade reaches the inventory"
kind: "system"
category: "Menus and HUD"
summary: "How a shop opens from a script, the Buy, Sell and Bazaar command rows and when Sell and Bazaar are greyed, the tabs each mode shows and how empty tabs drop out, how the rows and prices are built (the buy price as listed, half of it on a sale), the refusals, the quantity window, the trade commit and its gil roll, the new bazaar goods notice, and the equip offer and bazaar grant window after a purchase."
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
| `0` | Buy (`0x48B`) | "Purchase goods." (`0xC67`) | never greyed (`0057BE1E`) |
| `1` | Sell (`0x48C`) | "Selling loot can make new bazaar goods available for purchase." (`0xC68`) | "You possess no saleable items." (`0xCAB`) |
| `2` | Bazaar (`0x48D`) | "Purchase bazaar goods." (`0xC69`) | "No bazaar goods currently available." (`0xCAC`) |

Sell is offered when any Sell tab has goods and Bazaar when the bazaar list has any, through `0056E880`. A greyed row
refuses the choice (`0057C070`).

### New bazaar goods

Each time `0057BD40` runs, `0057B6F0` looks at every bazaar good the shop lists ([Bazaar](../Items-Equipment-Shops-And-Licenses/bazaar.md)).
A good whose flag bit 2 is clear gets it set (`0030B630(id, 1)`, `0057B752`), and any such good makes the screen post
"New bazaar goods are now available!" (`0x805`, `0057B4A0`) with sound `0x27`. Only goods with bit 2 set are listed
under Bazaar (`0057DC82`), and buying a good clears the bit (`0030B630(id, 0)`, `0056D4C0`).

### Modes and tabs

Choosing a row runs `0056DD50(shop, key)` (`0057C101`), which makes the mode's screen. The key, from `00D23920`, picks
a tab set through `00D233A0`:

| Mode | Key | Tab set | Tabs (`menu_expansion.bin`) |
|---|---|---|---|
| Buy | `0x5AF` | 32 (`00D23C70`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, TECHNICKS, MAGICKS, LOOT, GAMBIT TARGETS (`0x4AB8`-`0x4AD1`) |
| Sell | `0x5A2` | 19 (`00D23CC0`) | WEAPONS, ARMOR, ACCESSORIES, AMMUNITION, ITEMS, LOOT |
| Bazaar | `0x5AE` | 31 (`00D23C60`) | Bazaar (`0x48D`) |

Only the Sell key sets the screen's sell bit (`0056DE3D`-`0056DE4E`). `00564780` keeps a tab only when
`0057D620` reports it has goods, so an empty tab never shows. Before the screen opens, `0057BEE0` measures every name
the mode can list and sizes the window to the widest.

### Rows

`005655F0` builds a tab's rows through `0057CF20` (`005656A2`), one 0x20-byte row per good:

- Buy rows come from the shop's current list, by category (`002FAD30`, `002FA920` mode 1, `0057CFC4`, `0057D022`), as
  [Shops](../Items-Equipment-Shops-And-Licenses/shops.md) describes.
- Bazaar rows come from the shop's bazaar list (`002FA920` mode 2, `0057D07B`).
- Sell rows come from the party's inventory lists through `00D23D00` (`0057D0A2`-`0057D0AD`).

Each row holds the name, the id, the sellable count, the count owned and the price, filled by `0057DED0` (equipment),
`0057DAD0` (items and loot), `0057DD60` (magicks, technicks and gambits) or `0057DC30` (bazaar goods).

### Prices

| Trade | Price per unit |
|---|---|
| Buy | the good's listed price, query record `+0x28` (`0057DBAC`) |
| Sell | half the listed price, rounded down (`sar` at `0057DBC2`, `0057DFDE`) |

Equipment marked unsellable (record `+0x54`, `0057DFBF`) and loot whose half price is 0 (`0057DBCF`-`0057DBDC`) cannot
be sold. The shop screen applies no other change to a price: the four row fillers and the trade commit use the
listed value, and every write of `+0x28` in the query filler `0031C5D0` (14 of them) is a table load, -1 or 0.

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

The help line shows "Press ... to buy goods in quantity." (`0xC6C`) or "... to sell goods in quantity." (`0xC6E`)
while a number is being entered (`0056C783`).

### The trade

The second confirm makes the trade at once; there is no yes-or-no box (`0056D450`-`0056D504`). The total is the row's
price times the quantity:

| Trade | Call | What it changes |
|---|---|---|
| Sell | `00310870(id, quantity, total, 0)` (`0056D478`) | removes the goods, adds the gil, and counts the sale toward the bazaar (`0030B270`) |
| Buy | `002FEEB0(id, quantity, total, 0)` (`0056D49A`) | adds the goods, takes the gil, and marks the good as bought (`0030B180`) |

Each of the two has this one caller. The inventory side is in [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md).
A sale of loot also counts `00316A50(0xE, quantity)`, and every purchase counts `00316A50(0x13, id)`. Then
`002A1DC0` starts the gil total rolling (`0056D4D9`), and when it stops the screen goes on to the step below
(`0056D5C7`).

### After the trade

| Trade | Next |
|---|---|
| a bazaar good | the grant window `0057A4E0` lists the items the good gave (`0057A300`, `0057A480`) |
| equipment bought | the equip offer `0057A620` (`0057A980`); a sale of equipment rebuilds the list |
| anything else | the list is rebuilt with the cursor kept on its row (`0056E410`) |

The equip offer checks each party member (`00317B70`):

1. When someone can equip it, it asks "Equip your purchase now?" (`0x803`).
2. For the categories in `00D23910` it says instead that the item cannot be equipped at a shop and to use the Equip
   command in the Party Menu (`0xCF8`).
3. Yes opens the member picker `0057AC10`, "Select a character to equip." (`0xC70`), which equips through
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
