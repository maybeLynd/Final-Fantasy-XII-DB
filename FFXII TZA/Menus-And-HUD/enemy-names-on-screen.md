---
title: "Enemy names on screen: the steps from the definition's name word to the overhead name box, the target list and the battle log"
kind: "operation"
category: "Menus and HUD"
addresses: "0x0023A570, 0x002B58B0, 0x00269F20, 0x00263990, 0x00272CE0, 0x002B58F0, 0x002C8A60, 0x002C8BC0, 0x0027E530, 0x00272CB0, 0x00272C80, 0x005369C0, 0x00536310, 0x00536280"
---

## What the player sees

An enemy's name appears in a box over it, in the battle menu's target list and in the battle log. Several
enemies of the same kind are told apart by a letter after the name.

## Steps

1. **The name word.** Each enemy definition row of an area file holds a name word at `+0x08`
   ([bestiary](../Enemy-Spawning/bestiary.md),
   [area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)).
2. **The text.** When `0x0023A570` applies the definition to a unit, it splits the word into a bank (high 5 bits) and
   an entry (low 11 bits) of the word banks at `0x02EBF170` and renders it with `0x002B58B0(block, 0)`
   ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
   [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).
3. **The ordinal.** For a fresh record of a row whose byte `+0x02` is not `0xFF`, the old value of that row's
   spawn counter becomes the record's ordinal `+0x12`, and the counter goes up; `0x00269F20` stores the text at the
   actor's `+0xF8` and the ordinal at `+0x100`
   ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
4. **The display name.** `0x00263990` returns the text at `+0xF8` while the actor's name id `+0x102` is negative; with
   a name id of 0 or more it returns one of the id's two `npcdic.bin` names, chosen by the id's story flag in Bank2048
   ([NPC names](../Characters-And-Objects/npc-names.md#which-name-is-shown),
   [NPC names](../Characters-And-Objects/npc-names.md#who-sets-the-id)).
5. **The overhead name box.** The HUD gives the unit's entry a name box (`0x002C8A60`), and `0x002C8BC0` fills it from
   `0x00272CE0`, the display name ([HUD](hud.md)).
6. **The letter.** When the name is the `+0xF8` text and the ordinal is not 0, `0x00272CE0` adds a letter: entry
   `0x21 + (ordinal - 1) mod 26` of the font sheet's text (`0x002B58F0`)
   ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
7. **The target list.** The battle menu's target-list painter `0x0027E530` draws the unit's name through `0x00272CB0`
   and, when `0x00272C80` gives a number, that number after it
   ([battle menu](battle-menu.md#row-painters), [NPC names](../Characters-And-Objects/npc-names.md#names-in-battle-messages)).
8. **The battle log.** The line builder `0x005369C0` names the source and the target through `0x00536310` and
   `0x00536280`, with a byte from the actor (`0x00263A10`) as a second argument
   ([battle log](../Battle-Actions/battle-log.md#building-the-line)).
9. **The log's name.** For a unit whose actor has a name id of 0 or more, the name is that pair's second name; for
   any other unit, the definition row's word `+0x08`, rendered through the word banks
   ([NPC names](../Characters-And-Objects/npc-names.md#names-in-battle-messages)).
10. **Names inside message text.** The escape `0F 8` inserts the name for a 16-bit id (`0x002639E0`) and `0F >` the
    speaking character's name (`0x00263990`) ([text codes](text-codes.md)).

## Outcomes

- **An enemy row whose byte `+0x02` is `0xFF`** gets ordinal 0, so its name box shows no letter
  ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).
- **An enemy given an NPC name id by `setnpcname`** shows the pair's name chosen by the flag over its head, but the
  battle log always uses the pair's second name, whatever the flag holds
  ([NPC names](../Characters-And-Objects/npc-names.md#names-in-battle-messages)).
- **The log and the box read different sources**: the box reads the text the construction stored on the actor, the
  log the definition's word again; both render the same word, so the text matches unless a name id is set
  ([NPC names](../Characters-And-Objects/npc-names.md#names-in-battle-messages),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md)).

## Related

- [NPC names](../Characters-And-Objects/npc-names.md): name ids, the dictionary and names in battle messages.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): how a definition becomes a unit.
- [HUD](hud.md): the name boxes and the rest of the overhead parts.
