---
title: "Identifier spaces: every kind of id, handle and index the engine passes around, its range, its invalid values, what makes and resolves it, and when it can be reused"
kind: "reference"
category: "Engine core"
addresses: "0x003589B0, 0x003588B0, 0x0031B7E0, 0x002E9810, 0x002E97C0, 0x002DF980, 0x002DF960, 0x0036A000, 0x003B38B0, 0x0051CC30, 0x00377190, 0x00377360, 0x0035B2F0, 0x0020E620, 0x0020E600, 0x00309440, 0x003008A0, 0x0030F760, 0x002F9860, 0x002F9920, 0x003214B0, 0x00264D60, 0x0031B9F0, 0x00252E60, 0x00252F40"
---

## What it lists

`identifier-spaces.tsv` holds one row for each kind of identifier: 25 in all. Each row gives the identifier's form
(its bit fields), its range, the values that name nothing, the function that makes it, the function that turns it
back into the thing it names, and what happens to an old value when its slot is used again.

The identifiers fall into four families:

| Family | Rows | Old values after reuse |
|---|---|---|
| Checked handles: a slot plus a stamp, serial or generation that the resolver compares | actor, model binding, effect ticket, bone trail, scene element, fade record, presentation command, vibration, arena | stop resolving: the resolver sees the changed stamp and returns null or 0 |
| Plain indices and fixed ids | resource kind and id, encoded item id, action id, field id, text id, bank and row word, item picture id, script text id, party seat, member selector, inventory list id, bound model id | name the same thing for the whole run; out-of-range values are refused, clamped or read past, as each row says |
| Encoded pointers | encoded pointer | the low 32 bits of an address; the base at `0x01F83530` is 0 |
| Plain addresses | loot pickup | no check: a reused element answers to an old handle |
| Handles nothing looks up | movement entry | harmless: no instruction resolves or compares the handle |

### Ids readers confuse

- **An actor handle is not a battle unit.** `0x003589B0` makes the handle from the actor record. `0x003588B0` turns it
  back into the actor, and `0x0031B7E0` goes one step further to the actor's unit, and only while `0x02089340` bit 4
  is set.
- **A party seat is not a member.** A seat (0 to 8, in one of five slot maps) holds a member selector. The selector
  is the row of the party table and of the forty member records.
- **An encoded item id is not a list position.** The id's nibble picks a class (`0x00309440`: nibble + 5). The menus
  page through the twelve derived inventory lists instead, which `0x00252E60` fills when an owned count goes from 0
  to non-zero.
- **A model-binding handle is not a bound model id.** The bound id (letter class and number) names a model for
  the whole run. The binding handle names one of the 128 binding entries and stops working when that entry is
  retired.
- **A text id has two forms.** `0x002F9860` reads `group × 1000 + row`, while `0x002F9920` searches the rows for a row's
  own id under `group × 10000`. The two agree only where a file numbers its rows from `group × 10000` in order.

## Columns

| Column | Meaning |
|---|---|
| `id_kind` | the row's name |
| `form` | the identifier's bit fields or composition |
| `range` | the values that can name something |
| `invalid` | the values that name nothing, and what the resolver returns for them |
| `made_by` | the function or source that produces the identifier |
| `resolved_by` | the function that turns it into the thing it names |
| `reuse` | what happens to an old value when its slot is used again |
| `page` | the page that explains the identifier, by its path in the database |

## Related

- [Item and ability ids](item-and-ability-ids.md): the encoded id and its classes
- [Battle units](../Characters-And-Objects/battle-units.md): the actor handle
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): binding handles and bound ids
- [Party slots](../Party/party-slots.md): seats and selectors
- [Native limits](native-limits.md): the counts behind the ranges
