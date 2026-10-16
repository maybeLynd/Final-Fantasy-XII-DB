---
title: "Inventory: how items, equipment, loot, magicks, technicks, gambits and key items are stored and counted, what changes them, and the gil purse"
kind: "system"
category: "Items, equipment, shops and licenses"
summary: "How the game keeps what the party owns: the encoded id and its class nibble, the fifteen class descriptors and the storage each class uses (a count word with owned and equipped parts capped at 99, or one bit), the bundle and gil ids that expand into other grants, the one change function and its four channels, the first-acquisition marks, the ever-owned bits and the loot-sold tallies, every feature that changes the inventory, the writers that bypass the change function, and the gil purse with its cap."
addresses: "01EEBCC0, 003008A0, 002FD150, 002FD420, 00300B80, 0030B6A0, 003047F0, 00253690, 00254EE0, 003004B0"
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
Each class has a `0x58`-byte descriptor in the table at `01EEBCC0`, fifteen rows indexed by the nibble.

A descriptor holds three region offsets into the party block (`+0x00`, `+0x18`, `+0x28`), the length of the first
region in words (`+0x10`), the id count (`+0x3C`), a change handler (`+0x48`) and a query handler (`+0x50`). The
rebaser `0030B6A0` turns the offsets into pointers at `+0x08`, `+0x20` and `+0x30` whenever the party block is
bound (`0030B6C0`-`0030B6ED`; [Party data](../Party/party-data.md)).

| Nibble | Ids | Class | Storage |
|---|---|---|---|
| 0 | `0x0000`-`0x003F` | items | a count word each at `+0x4748`, and one ever-owned bit each at `+0x57C0` |
| 1 | `0x1000`-`0x11A3` | equipment | a count word each at `+0x47C8` |
| 2 | `0x2000`-`0x21FF` | loot | a count word each at `+0x4B10`, and one sold-tally byte each at `+0x57C8` |
| 3 | `0x3000`-`0x3050` | magicks | one bit each at `+0x4F10` |
| 4 | `0x4000`-`0x4017` | technicks | one bit each at `+0x4F1C` |
| 6 | `0x6000`-`0x60FF` | gambits | one bit each at `+0x4F20` |
| 8 | `0x8000`-`0x81FF` | key items and maps | one bit each at `+0x4F40` |
| 9 | `0x9000`-`0x91FF` | reward packages: gil and two nested grants | none (`002FD530`) |
| A | `0xA000`-`0xA0FF` | package selectors: two triples of ids | none (`002FD640`) |
| C | `0xC000`-`0xC01F` | Quickenings `0xC000`-`0xC011`, Espers `0xC012`-`0xC01E`, Second Board `0xC01F` | one bit each at `+0x4F80` |
| D | `0xD000`-`0xD07F` | bazaar goods: three granted pairs | none (`002FD780`) |
| E | `0xE000`-`0xEFFE` | gil carried as an id, `(id & 0xFFF) * count` | none (`002FD880`) |

Rows 5, 7 and 11 are empty, and nibble F is refused.

### The count word

An item, equipment or loot count word is `owned | equipped << 10`: bits 0-9 count the copies owned and bits 10-15
the copies being worn. The packed handler `002FD150` builds it (`002FD30B`-`002FD31A`, `002FD28C`-`002FD298`), and
its query `002FD8D0` answers four kinds: 0 owned minus worn, 1 owned, 2 worn, 3 the region-two byte
(`002FD906`-`002FD95B`). The bit handler `002FD420` keeps bit `index & 15` of word `index >> 4`.

### Changing the inventory

`003008A0(id, delta, absolute, channel, flags)` makes every change (`003008A0`-`00300B62`):

1. It refuses `0xFFFF`, Unarmed `0x1000`, nibble F, and an index not below the class's id count
   (`003008C0`-`0030092C`).
2. It reads the old value and calls the class's change handler, `+0x48` (`00300931`-`00300960`).
3. On channel 1, when the value goes from 0 or less to more than 0, it sets the first-acquisition marks in the
   party block's flag word `+4`, below (`00300968`-`00300B5A`).

The packed handler has four channels, chosen by `channel` (`002FD198`-`002FD1B9`):

| Channel | Changes | Clamp | Sites |
|---|---|---|---|
| 0 | the free copies, by moving the worn part | worn kept within 0 and owned | `002FD383`-`002FD3F1`; no caller uses it |
| 1 | owned | not below worn, not above 99 | `002FD2AD`-`002FD37C` |
| 2 | worn | 0 to owned | `002FD23C`-`002FD2A5` |
| 3 | the region-two byte | 0 to 99 | `002FD1BF`-`002FD237` |

A rise on channel 1 also sets the item's ever-owned bit (`002FD323`-`002FD34B`). A relative channel-1 change with
`flags` bit 0 posts the obtain message through `0046A630`, in both handlers (`002FD2AD`-`002FD37C`,
`002FD4FB`-`002FD509`).

Neither handler has a channel 4: the packed handler returns 0 without writing
(`002FD1B5`-`002FD1B9`), and the bit handler sets or clears the bit as for any channel. The bit handler
ignores the channel: a result below 1 clears the bit and 1 or more sets it (`002FD49D`-`002FD4E5`). The bundle and
gil classes act only on a relative channel-1 change and call `003008A0` again for each nested grant
(`002FD53F`-`002FD8B4`). A package selector, `0xAxxx`, gives its second triple when `flags` bit 1 is set and its
first otherwise (`002FD6BA`).

Most callers use three wrappers. `00300B80(id, delta, flags)` is a relative channel-1 change, for adding and
removing (`00300B84`-`00300B92`). `00300BA0(id, count, flags)` sets the count outright (`00300BA4`-`00300BB2`).
`0030C410(id)` and `0030F9A0(id)` add or remove one worn copy of a piece of equipment
(`0030C447`-`0030C45C`, `0030F9D7`-`0030F9EB`). `00300490(id, delta, flags)` makes a channel-4 change
(`00300494`-`003004A2`): a member's join calls it, through a function pointer, for an item its gambit actions need,
and it writes no count (`00316F62`-`00316F82`).

### First-acquisition marks

| Id | Bits of the party flag word `+4` | Sites |
|---|---|---|
| a magick | bit 0, and one of bits 1-5 for its school, the action row's `+0x2C & 7` through the table `01EECF98` | `003009F7`, `00300A47`-`00300B5A` |
| a technick | bit 6 | `003009E7` |
| a Quickening | bit 7 | `003009D4` |
| an Esper | bit 8 | `003009C1` |

### Who changes it

| Feature | Sites |
|---|---|
| shop buy and bazaar purchase | `002FEEDB` (`Shop_CommitPurchaseItemAndGil`) |
| shop sell, and the sold tally of loot | `003108A6`, `003108E8` |
| bazaar purchase: the sold tallies of its three loots set to 0 | `0030B220`-`0030B256` |
| steal and poach | `00311457`, `003114A8` |
| an enemy's loot bag picked up | `00319965` |
| a chest | `0050FBA0` (verb `0x3037` `btlAtelOpenTreasureMessage`) |
| a quest or hunt reward | `003F4AEA`, `003F4B1A` (verb `0x37C` `questresultwindow`) |
| an item given in a message window | `002A541B` |
| the item verbs `additem` `0x2E5`, `additem_47f` `0x47F`, `additemmes` `0x480`, `subitem` `0x2F2`, through `0032A810`, and `setitemnum` `0x55C`, through `0032A830`; both floor the result at 0 | `003450DC`, `003449EF`, `0034B252`, `003459ED`, `0034554B` |
| an item used in battle: reserved at commit, refunded on cancel | `0030EFB0`, `003002CB` |
| a member joining or leaving ([Party members](../Party/party-members.md)) | `00316E9C`-`00317009`, `00323586`-`00323594` |
| a Quickening square bought ([Licenses](licenses.md)) | `00323B0D` |
| equipping and unequipping | `0030C410` and `0030F9A0` from `00318B40`, `0031A410`, `0031A510`, `0031A630` |
| `takeaway_item_and_equip` `0x388` and `giveback_item_and_equip` `0x387` | `0030FC7F`, `0030FCE2`, `0030FAF5`, `0030FB48` |
| the scenario presets and the starting inventory | `00239B4F`, `0023AFFF` |
| the developer verbs `btlAtelGetAll*` `0x3070`-`0x3077` | `0030DCE4`-`0030DF74` |
| the developer verb `btlAtelSetRealBattleMode` `0x3024`: 99 of every piece of equipment and every gambit | `00308E14`, `00308E54` (`00308DE0`, from `0050F39E`) |

These are every call of `003008A0` and its wrappers in a scan of all call and jump instructions of the image; the
one indirect call is `00316F82`, to `00300B80` or `00300490`.

### Writes that bypass the change function

- The clear-all `003047F0` stores 0 in every count and bit word (`0030482A`); the party block reset `002370E5` and
  the scenario presets `00239B22` call it.
- The rebaser clears every loot sold tally (`0030B702`-`0030B737`).
- `takeaway_item_and_equip` copies the item and equipment counts to backups at `+0x4F84` and `+0x5004`
  (`0030FC6F`, `0030FCCF`), and `giveback_item_and_equip` adds them back and clears the backups
  (`0030FBBA`-`0030FBC7`).
- The party block reset `002370C0` clears the whole block.

### Gil

The purse is the dword at `+8` of the save header, `[02092758] + 8` (`00253690`-`00253697`). `00254EE0(new)` is its
only writer instruction (`00254F1F`).

It first reports the difference to counter 6 for a gain or counter 7 for a
loss (`00316A50`, `00254EF1`-`00254F02`), then keeps the value between 0 and 99,999,999 (`00254F07`-`00254F15`).
`003004B0(delta, flags)` adds, floored at 0, and with `flags` bit 0 posts the gil line (`003004C3`-`003004E5`);
`00300500` sets, floored at 0.

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
