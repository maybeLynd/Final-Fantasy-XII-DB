[Home](../../README.md) / [Menus and HUD](README.md) / Enemy names on screen

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Enemy names on screen: the steps from the definition's name word to the overhead name box, the target list and the battle log | operation | Menus and HUD | Battle HUD | The order in which an enemy's name reaches the screen: the definition row's name word, the text and ordinal the unit's construction stores on its actor, the display-name resolver and the NPC name id that overrides the text, the overhead name box with its ordinal letter, the battle menu's target list, the battle log's own name lookup, and the text codes that insert names; with the cases where the field and the log show different names, each step linked to the page that explains it. | 0x0023A570, 0x002B58B0, 0x00269F20, 0x00263990, 0x00272CE0, 0x002B58F0, 0x002C8A60, 0x002C8BC0, 0x0027E530, 0x00272CB0, 0x00272C80, 0x005369C0, 0x00536310, 0x00536280 |

## What the player sees

An enemy's name appears in a box over it, in the battle menu's target list and in the battle log. Several
enemies of the same kind are told apart by a letter after the name.

The name starts as a word in the enemy's row of the area's battle data, which points into the battle text banks. When
the enemy is placed, the game keeps that text on the unit with a spawn number that becomes the letter. The overhead
box and the target list show it from there, and the battle log reads the same word from the area's row.

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
   ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)). It goes in as the blank `0x06`, a
   space (`0x01` if `0x00254A10` is true, else `0x04`) and the letter, one byte, or two for a code outside
   `0x20`-`0xFF` (`0x002B5969`-`0x002B59D3`).
   - An entry of 0 gives a second space byte in place of the letter (`0x002B59AA`-`0x002B59B1`).
7. **The target list.** The battle menu's target-list painter `0x0027E530` draws the unit's name through `0x00272CB0`
   and, when `0x00272C80` gives an ordinal above 0, that ordinal's letter after it, written by `0x0024ABE0` as in step 6
   (`0x0027E657`-`0x0027E6FA`) ([battle menu](battle-menu.md#row-painters),
   [NPC names](../Characters-And-Objects/npc-names.md#names-in-battle-messages)).
8. **The battle log.** The line builder `0x005369C0` names the source and the target through `0x00536310` and
   `0x00536280` ([battle log](../Battle-Actions/battle-log.md#building-the-line)).
   - `0x00536280` takes the name id and the `flag` byte `0x00536310` fills (`0x00536CB6`, `0x00536D2C`).
   - The low byte of the actor's ordinal (`0x00263A10`, 0 while a name id is set or for a stats record with byte
     `+0x05` = 0) is stored beside each name in the line record (`0x00536CF9`, `0x00536D70`).
9. **The log's name.** For a party member (stats byte `+0x05` = 0) it is word `+0x30` of its party table row,
   whatever its actor holds (`0x00536345`-`0x00536388`). For any other unit whose actor has a name id of 0 or more, the
   name is that pair's second name; for
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0023A570` calls `0x00236A60`, `0x00322050`; `0x0023A570` is called by `0x00300E40`, `0x003266C0`; `0x0024ABE0` is
  called by `0x00272CE0`; `0x00263990` is called by `0x0025C230`, `0x0025C830`, `0x00268D10`, `0x00272CB0`, `0x00272CE0`; `0x00263A10`
  is called by `0x00272C80`, `0x00272CE0`; `0x00269F20` is called by `0x00238BF0`; `0x00272C80` calls `0x003588B0`; `0x00272CB0`
  calls `0x003588B0`; `0x00272CE0` calls `0x003588B0`.
- Actor entity: `0x0027E530` calls `0x00272C80`, `0x00272CB0`; `0x002B58B0` is called by `0x0023A570`; `0x002C8BC0` calls
  `0x00272CE0`.
- Actor entity: those functions are documented on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Actor entity: and on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md),
  [frame update order](../Engine-Core/frame-update-order.md), [npc names](../Characters-And-Objects/npc-names.md).
- Combat formula: `0x0023A570` calls `0x0023AC80`; `0x00536310` calls `0x0031B860`; `0x005369C0` calls `0x0031B860`; those
  functions are documented on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Core runtime: `0x00254A10` calls `0x00229E40`; those functions are documented on
  [startup constants](../Engine-Core/startup-constants.md).
- Gameplay: `0x0023A570` calls `0x00322C50`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Presentation: `0x00254A10` is called by `0x002B0280`, `0x002D2DB0`; `0x00263990` is called by `0x002B0280`; `0x002639E0` is
  called by `0x002B0280`; `0x002B58B0` is called by `0x00506700`; those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [menu lists](menu-lists.md),
  [battle numbers](battle-numbers.md).
- Save load settings: `0x00254A10` is called by `0x005832B0`; those functions are documented on
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).
- Script VM: `0x00269F20` is called by `0x00355A00`, `0x00356B70`, `0x00357120`; those functions are documented on
  [npc names](../Characters-And-Objects/npc-names.md).
- Spawn encounter lifecycle: `0x0023A570` calls `0x00236100`; `0x0023A570` is called by `0x0023A3B0`; those functions are
  documented on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- Story event quest hunt: `0x00263990` calls `0x0032A930`; `0x002639E0` calls `0x0032A930`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- World area: `0x0023A570` calls `0x00313F60`; `0x005369C0` calls `0x00264ED0`, `0x003148F0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md),
  [party control modes](../Engine-Core/party-control-modes.md).
