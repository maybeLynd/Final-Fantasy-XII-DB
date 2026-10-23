---
title: "Inventory: how items, equipment, loot, magicks, technicks, gambits and key items are stored and counted, what changes them, and the gil purse"
kind: "system"
category: "Items, equipment, shops and licenses"
addresses: "0x01EEBCC0, 0x003008A0, 0x002FD150, 0x002FD420, 0x00300B80, 0x0030B6A0, 0x003047F0, 0x00253690, 0x00254EE0, 0x003004B0"
---

## What the player sees

- Items, equipment and loot are counted, at most 99 of each; a piece of equipment someone is wearing still counts
  as owned, and it cannot be sold or dropped below the number being worn.
- Magicks, technicks, gambits, key items, Quickenings and Espers are simply owned or not.
- Some gifts, such as a picked-up loot bag, show a message naming what was obtained.
- The gil purse holds at most 99,999,999.

## How it works

### Ids and classes

Every thing the party can own has a 16-bit id whose top nibble is its class ([Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
Each class has a `0x58`-byte descriptor in the table at `0x01EEBCC0`, fifteen rows indexed by the nibble.

A descriptor holds three region offsets into the party block (`+0x00`, `+0x18`, `+0x28`), the length of the first
region in words (`+0x10`), the id count (`+0x3C`), a change handler (`+0x48`) and a query handler (`+0x50`). The
rebaser `0x0030B6A0` turns the offsets into pointers at `+0x08`, `+0x20` and `+0x30` whenever the party block is
bound (`0x0030B6C0`-`0x0030B6ED`; [Party data](../Party/party-data.md)).

| Nibble | Ids | Class | Storage |
|---|---|---|---|
| 0 | `0x0000`-`0x003F` | items | a count word each at `+0x4748`, and one ever-owned bit each at `+0x57C0` |
| 1 | `0x1000`-`0x11A3` | equipment | a count word each at `+0x47C8` |
| 2 | `0x2000`-`0x21FF` | loot | a count word each at `+0x4B10`, and one sold-tally byte each at `+0x57C8` |
| 3 | `0x3000`-`0x3050` | magicks | one bit each at `+0x4F10` |
| 4 | `0x4000`-`0x4017` | technicks | one bit each at `+0x4F1C` |
| 6 | `0x6000`-`0x60FF` | gambits | one bit each at `+0x4F20` |
| 8 | `0x8000`-`0x81FF` | key items and maps | one bit each at `+0x4F40` |
| 9 | `0x9000`-`0x91FF` | reward packages: gil and two nested grants | none (`0x002FD530`) |
| A | `0xA000`-`0xA0FF` | package selectors: two triples of ids | none (`0x002FD640`) |
| C | `0xC000`-`0xC01F` | Quickenings `0xC000`-`0xC011`, Espers `0xC012`-`0xC01E`, Second Board `0xC01F` | one bit each at `+0x4F80` |
| D | `0xD000`-`0xD07F` | bazaar goods: three granted pairs | none (`0x002FD780`) |
| E | `0xE000`-`0xEFFE` | gil carried as an id, `(id & 0xFFF) * count` | none (`0x002FD880`) |

Rows 5, 7 and 11 are empty, and nibble F is refused.

### The count word

An item, equipment or loot count word is `owned | equipped << 10`: bits 0-9 count the copies owned and bits 10-15
the copies being worn. The packed handler `0x002FD150` builds it (`0x002FD30B`-`0x002FD31A`, `0x002FD28C`-`0x002FD298`), and
its query `0x002FD8D0` answers four kinds: 0 owned minus worn, 1 owned, 2 worn, 3 the region-two byte
(`0x002FD906`-`0x002FD95B`). The bit handler `0x002FD420` keeps bit `index & 15` of word `index >> 4`.

### Changing the inventory

`0x003008A0(id, delta, absolute, channel, flags)` makes every change (`0x003008A0`-`0x00300B62`):

1. It refuses `0xFFFF`, Unarmed `0x1000`, nibble F, and an index not below the class's id count
   (`0x003008C0`-`0x0030092C`).
2. It reads the old value and calls the class's change handler, `+0x48` (`0x00300931`-`0x00300960`).
3. On channel 1, when the value goes from 0 or less to more than 0, it sets the first-acquisition marks in the
   party block's flag word `+4`, below (`0x00300968`-`0x00300B5A`).

The packed handler has four channels, chosen by `channel` (`0x002FD198`-`0x002FD1B9`):

| Channel | Changes | Clamp | Sites |
|---|---|---|---|
| `0` | the free copies, by moving the worn part | worn kept within 0 and owned | `0x002FD383`-`0x002FD3F1`; no caller uses it |
| `1` | owned | not below worn, not above 99 | `0x002FD2AD`-`0x002FD37C` |
| `2` | worn | 0 to owned | `0x002FD23C`-`0x002FD2A5` |
| `3` | the region-two byte | 0 to 99 | `0x002FD1BF`-`0x002FD237` |

A rise on channel 1 also sets the item's ever-owned bit (`0x002FD323`-`0x002FD34B`). A relative channel-1 change with
`flags` bit 0 posts the obtain message through `0x0046A630`, in both handlers (`0x002FD2AD`-`0x002FD37C`,
`0x002FD4FB`-`0x002FD509`).

Neither handler has a channel 4: the packed handler returns 0 without writing
(`0x002FD1B5`-`0x002FD1B9`), and the bit handler sets or clears the bit as for any channel. The bit handler
ignores the channel: a result below 1 clears the bit and 1 or more sets it (`0x002FD49D`-`0x002FD4E5`). The bundle and
gil classes act only on a relative channel-1 change and call `0x003008A0` again for each nested grant
(`0x002FD53F`-`0x002FD8B4`). A package selector, `0xAxxx`, gives its second triple when `flags` bit 1 is set and its
first otherwise (`0x002FD6BA`).

Most callers use three wrappers. `0x00300B80(id, delta, flags)` is a relative channel-1 change, for adding and
removing (`0x00300B84`-`0x00300B92`). `0x00300BA0(id, count, flags)` sets the count outright (`0x00300BA4`-`0x00300BB2`).
`0x0030C410(id)` and `0x0030F9A0(id)` add or remove one worn copy of a piece of equipment
(`0x0030C447`-`0x0030C45C`, `0x0030F9D7`-`0x0030F9EB`). `0x00300490(id, delta, flags)` makes a channel-4 change
(`0x00300494`-`0x003004A2`): a member's join calls it, through a function pointer, for an item its gambit actions need,
and it writes no count (`0x00316F62`-`0x00316F82`).

### First-acquisition marks

| Id | Bits of the party flag word `+4` | Sites |
|---|---|---|
| a magick | bit 0, and one of bits 1-5 for its school, the action row's `+0x2C & 7` through the table `0x01EECF98` | `0x003009F7`, `0x00300A47`-`0x00300B5A` |
| a technick | bit 6 | `0x003009E7` |
| a Quickening | bit 7 | `0x003009D4` |
| an Esper | bit 8 | `0x003009C1` |

### Who changes it

| Feature | Sites |
|---|---|
| shop buy and bazaar purchase | `0x002FEEDB` (`Shop_CommitPurchaseItemAndGil`) |
| shop sell, and the sold tally of loot | `0x003108A6`, `0x003108E8` |
| bazaar purchase: the sold tallies of its three loots set to 0 | `0x0030B220`-`0x0030B256` |
| steal and poach | `0x00311457`, `0x003114A8` |
| an enemy's loot bag picked up | `0x00319965` |
| a chest | `0x0050FBA0` (verb `0x3037` `btlAtelOpenTreasureMessage`) |
| a quest or hunt reward | `0x003F4AEA`, `0x003F4B1A` (verb `0x37C` `questresultwindow`) |
| an item given in a message window | `0x002A541B` |
| the item verbs `additem` `0x2E5`, `additem_47f` `0x47F`, `additemmes` `0x480`, `subitem` `0x2F2`, through `0x0032A810`, and `setitemnum` `0x55C`, through `0x0032A830`; both floor the result at 0 | `0x003450DC`, `0x003449EF`, `0x0034B252`, `0x003459ED`, `0x0034554B` |
| an item used in battle: reserved at commit, refunded on cancel | `0x0030EFB0`, `0x003002CB` |
| a member joining or leaving ([Party members](../Party/party-members.md)) | `0x00316E9C`-`0x00317009`, `0x00323586`-`0x00323594` |
| a Quickening square bought ([Licenses](licenses.md)) | `0x00323B0D` |
| equipping and unequipping | `0x0030C410` and `0x0030F9A0` from `0x00318B40`, `0x0031A410`, `0x0031A510`, `0x0031A630` |
| `takeaway_item_and_equip` `0x388` and `giveback_item_and_equip` `0x387` | `0x0030FC7F`, `0x0030FCE2`, `0x0030FAF5`, `0x0030FB48` |
| the scenario presets and the starting inventory | `0x00239B4F`, `0x0023AFFF` |
| the developer verbs `btlAtelGetAll*` `0x3070`-`0x3077` | `0x0030DCE4`-`0x0030DF74` |
| the developer verb `btlAtelSetRealBattleMode` `0x3024`: 99 of every piece of equipment and every gambit | `0x00308E14`, `0x00308E54` (`0x00308DE0`, from `0x0050F39E`) |

These are every call of `0x003008A0` and its wrappers in the image; the one indirect call is `0x00316F82`, to
`0x00300B80` or `0x00300490`.

### Writes that bypass the change function

- The clear-all `0x003047F0` stores 0 in every count and bit word (`0x0030482A`) and ends by tail-jumping to
  `0x00253480` (`0x0030483D`), which empties all twelve derived inventory lists (`0x00253240(i, 1)`: every id `0xFFFF`,
  the count at `[0x020927C0] + 0x47B8 + 4i` = 0) and clears every bit of `[0x020927C0] + 0x3244` but bit 0 and bit 0
  of `+0x3245`; the party block reset `0x002370E5` and
  the scenario presets `0x00239B22` call it.
  - `0x0035C560` calls `0x00253480` directly (`0x0035C584`), right after the HUD reset `0x0028F8B0`
    ([HUD](../Menus-And-HUD/hud.md)).
- The rebaser clears every loot sold tally (`0x0030B702`-`0x0030B737`).
- `takeaway_item_and_equip` copies the item and equipment counts to backups at `+0x4F84` and `+0x5004`
  (`0x0030FC6F`, `0x0030FCCF`), and `giveback_item_and_equip` adds them back and clears the backups
  (`0x0030FBBA`-`0x0030FBC7`).
- The party block reset `0x002370C0` clears the whole block.

### Gil

The purse is the dword at `+8` of the save header, `[0x02092758] + 8` (`0x00253690`-`0x00253697`). `0x00254EE0(new)` is its
only writer instruction (`0x00254F1F`).

It first reports the difference to counter 6 for a gain or counter 7 for a
loss (`0x00316A50`, `0x00254EF1`-`0x00254F02`), then keeps the value between 0 and 99,999,999 (`0x00254F07`-`0x00254F15`).
`0x003004B0(delta, flags)` adds, floored at 0, and with `flags` bit 0 posts the gil line (`0x003004C3`-`0x003004E5`);
`0x00300500` sets, floored at 0.

Shops, the bazaar, kill rewards, chests, quest rewards, member joins, the gil
verbs `addgill` `0x2E7` and `subgill` `0x2E8`, battle actions that cost gil and the gil-stealing trap change it
through these.

## Modding notes

- The 99 cap is a clamp in the change function; the count word itself has room for 1,023.
- A bundle id (`0x9xxx`, `0xAxxx`, `0xDxxx`) or a gil id (`0xExxx`) can be given anywhere an item id is accepted,
  and expands into its grants.
- The loot sold tallies are cleared whenever the party block is bound.

## Related

- [Party data](../Party/party-data.md) - the party block that holds every region.
- [Equipment row](equipment-row.md) - the equipment the count words count.
- [Shops](shops.md) - buying and selling.
- [Licenses](licenses.md) - Quickening squares and the presence bits.
- [Party members](../Party/party-members.md) - what a join adds and a leave removes.
- [Scenario presets](../Party/scenario-presets.md) - the inventories the presets set.
