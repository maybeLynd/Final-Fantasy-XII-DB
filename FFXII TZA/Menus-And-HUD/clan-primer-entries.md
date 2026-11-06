---
title: "Clan Primer entries: every Traveler's Tips and Bestiary entry and the four unused handbook families, with each entry's name, text, unlock rule, section and the monsters it counts"
kind: "reference"
category: "Menus and HUD"
addresses: "0x005760A0, 0x00571F60, 0x00571710, 0x00577550, 0x00575E80, 0x00315910, 0x003154B0, 0x00576CA0, 0x00576E30, 0x00576860, 0x00576A50, 0x00576300, 0x00315820, 0x00315420, 0x00315D50, 0x00315DC0, 0x00316930, 0x002F9920, 0x00D23740, 0x00D23750, 0x00D23688"
---

## What it lists

The Clan Primer opens four categories from the Party Menu: Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips
([Clan Primer](clan-primer.md)). This page lists the entries of the two categories that are handbook families:

- Traveler's Tips, 16 entries of advice in 4 sections, such as "Restoring MP" under "Tricks of the Trade";
- the Bestiary, 384 monster entries in 32 sections: one per region from "The Dalmasca Sands" to "The Necrohol of
  Nabudis", then Marks, Elite Marks, Espers, Bosses, Rare Game, Humanoids and The Archadian Empire.

Hunts are listed on [Hunts](../Story-Events-And-Hunts/hunts.md) and the Sky Pirate's Den statues on
[Achievements](../Steam-And-Achievements/achievements.md). Four more handbook families ship, `story`,
`world`, `person` and `knowledge` (300 entries), but no category opens them; they are listed here too.

The data is in three files:

- [clan-primer-entries.tsv](clan-primer-entries.tsv), one line per entry of each of the six families (700 lines);
- [clan-primer-texts.tsv](clan-primer-texts.tsv), one line per text slot of the Traveler's Tips and Bestiary entries
  (1,024 lines);
- [clan-primer-sections.tsv](clan-primer-sections.tsv), one line per section of each family (61 lines).

The file layouts are on [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md). Each Bestiary line
links to the enemy definitions of [Bestiary](../Enemy-Spawning/bestiary.md) whose `primer_entry` is
that entry.

### What the player sees in an index

1. A section is listed once one of its entries is unlocked (`0x00571F60`, `0x00572017`).
2. Its unlocked entries follow in record order, and a locked entry takes no row (`0x005720B9`-`0x005720F6`). The blank
   rows after them (`0x00572103`-`0x00572135`) are added only when fewer entries were listed than `0x00576740` counted as
   unlocked, and both counts use the same test (`0x00576CA0`), so they are never added.
   - `0x00576CA0(kind, index)` passes a kind it does not handle, a negative one or one above 7
     (`0x00576CA4`-`0x00576CB7`). Kinds 0 to 5 and 7 ask `0x003154B0` with the category `0x00D23750[kind]`, the same
     number except kind 5, the Bestiary, which asks category 6 (`0x00576CF5`-`0x00576D08`).
   - Kind 6, the Hunts, answers 0 with no data manager `[0x02CA9738]`, while bit `0x2` of its `+0x100` is set or
     with no quest table `+0xF8`, and otherwise the answer of `0x0037F060(1, index, table)` (`0x00576CC1`-`0x00576CEE`).
3. A Bestiary section's caption reads "???" until part of one of its maps has been explored (`0x00576A50`); the
   regional sections list those maps, the last seven sections no map.
4. A Bestiary row shows the number of defeats still needed for the next text slot, unless the entry's flag says
   otherwise (`0x00571817`-`0x005718B0`); the `countdown` column gives which rows show it.
5. For the thirteen Espers the us index row shows the summon's short name, "Belias", in place of the entry's name
   "Belias, the Gigas" (`0x005717E2`-`0x005717F2`).
   - `0x00571710` shows the countdown only when the row's layout has a countdown cell (byte `+2` not `0xFF`), the
     entry's flag `+0x14` bit `0x1` is clear, it has slots (`+0x15`) and its count `+0x16` is below the last slot's
     threshold, one byte per slot from `+0x18` (`0x00571805`-`0x00571848`).
   - The number, written by `0x0029FF60`, is a threshold less the count: the one after the last threshold the count
     has reached, the second when the count is below the first, or the only one (`0x0057184A`-`0x005718B0`). The
     cell's bit `0x1` at `+0x08` is set exactly when it shows (`0x005718B5`-`0x005718C5`).
   - The short name is the entry's `+0x08`, used when it is set and `0x00254A10` returns 0 (`0x005717DF`-`0x005717F8`).

### How an entry unlocks

Traveler's Tips and the four unused families keep one unlock bit per entry at save `+0x32CC`. Each time an index is
built, `0x00577550` tests the entry's record of `menuhandbook_<family>.dat` (`0x00575E80`) and sets or clears the bit
(`0x00315910`), so an entry follows its condition both ways. In the shipped files the only test used is the story
counter ([Story counter values](../Story-Events-And-Hunts/story-counter-values.md)):

- Traveler's Tips: 11 entries always, 5 by the story counter (105, 230, 244 and 1380 twice);
- `story`: all 69 by the story counter; `world`: 5 by the story counter, the other 69 always; `person` and
  `knowledge`: always.

A Bestiary entry is unlocked by a rule of `menuhandbook.bin` (`0x003154B0`), or with no rule by its own kill count:

- with no rule, once this monster has been defeated: its kill count, save byte `+0x3404` + entry less 1, is above 0
  (`0x00315420`); 367 entries;
- a type 0 rule, once the story counter reaches the rule's value; 14 entries;
- a type 1 rule, once the monster of another entry has been defeated: Enkidu (252) opens with Gilgamesh (251).
- a rule of any other type, or no rule table bound at `0x022C2550`, falls back to the entry's own kill count; an entry
  number of `0x200` or more is never unlocked (`0x00315533`-`0x00315539`, `0x0031553B`-`0x0031558E`, `0x003155C5`-`0x003155C8`).
- `0x003154B0` finds the rule as the first of the table's records whose low 12 bits are the entry number
  (`0x0031556D`-`0x0031557B`); type 0 passes when the story counter (`0x00265270`), as a signed 16-bit value, has reached
  the rule's value (`0x003155D0`-`0x003155E8`).

Two entries are not counted by defeats at all (`0x00315820` skips them through `0x00315D50`). The field-frame sweep
`0x00316930` sets each one's count to 1 once its quest passes `0x00315DC0`: Gilgamesh (251) with quest 167, "Battle on
the Big Bridge", at progress 100, and Shadowseer (259) with quest 170, "God or Devil?", at progress 70, or when the
quest is cleared. It does so only while the count is at most 0 (save byte 0 or 1, `0x003169E0`-`0x003169FA`), and stores
2 in the byte (`0x00316A0C`).

`0x00315DC0(quest)` fails for quest -1 and passes for a cleared quest (`0x0046B1A0`) (`0x00315DC8`-`0x00315DDE`). It also
passes when the handbook table `[0x022C2550]` or one of the two offset hops to its quest list is missing
(`0x00315DE9`-`0x00315E10`, `0x00315E75`). Otherwise it passes when the quest is in that list and its progress
(`0x0046B180`) has reached the list's value for it, and fails for a quest not in the list (`0x00315E2C`-`0x00315E6D`).

### What an entry shows

- Traveler's Tips: the name and one text. No picture is drawn (`0x00575B80` skips this family).
- Bestiary: the name, the kill count (`0x005760A0`), a picture, and two, three or seven text slots, read in order;
  the first slot whose condition fails ends the list (`0x00576300`, `0x00576E30`).

A Bestiary entry's slots all follow one mode, the mode word of its record in `menuhandbook_monster.dat`:

| Mode | A slot shows when | Entries |
|---|---|---:|
| 0 | the kill count is at least the slot's value | 370 |
| 1 | the story counter is at least the slot's value | 13 |
| 2 | this monster or the monster of the entry the value names has been defeated | 1 |

- Slot 0 is two lines, such as "Plant" and "Cactus"; later slots carry a heading before code `0x03`, mostly
  "Observations" or "Description" for slot 1, and texts such as "Aletap Rumors" or "The Town Crier" for slot 2.
- The mode 0 test is unsigned, so a count of -1, a monster never counted, passes every slot (`0x00576EBD`-`0x00576EC4`).
  It runs only for a listed entry, and an entry without a rule is listed only once its count is above 0, so -1
  meets it only for an entry a rule opens. Of those 15, 13 use mode 1 and Enkidu (252) mode 2, whose tests are
  signed (`0x00576EE4`, `0x00576EF0`).
- Rogue Tomato (211) alone pairs a rule with mode 0: its rule, story counter 78, comes from the `in` copy of
  `menuhandbook.bin` and its slots, 1 defeat each, from the us `menuhandbook_monster.dat`. The `in`, `ch`, `kr`,
  `cn`, `de`, `fr`, `it` and `es` copies of that table give it mode 1, story counter 78 for each slot.
- The story counter reaches 78 in `dst_a01`'s `トマト監視監督.トマト監視`, its one shipping write of 78, after
  `while (scratch1_var_1 != 2)`. That variable is scratch1 word 3, where `0x00307030` posts a completed mode 1 group
  (`0x00307063`); the two Rogue Tomato units are groups 1 and 2 (`btlAtelSetEventFlagGroup(1, 1)` and `(2, 1)`).
- A group completes only in the KO sequence (`0x00306F00` at `0x0030082F`), after the KO that `0x003171C0` counts:
  both units are unit type 0, mode 1 (`0x002396D6`), so the class-nibble skip does not apply.
- No other write brings the counter to 78 or more first: every other script write of 78 or more runs only
  once the counter is 78 or more, or never runs
  ([story counter values](../Story-Events-And-Hunts/story-counter-values.md)). So the count is at least 1
  when the entry opens, and both slots open by the count itself.
- Dalan's House (`slm_a03`) writes 115 and 120 on an entry below 110 (`常駐監督.main` line 186,
  `EVダラン登場` lines 270-271). Below 100 the only way into Lowtown and the Garamsythe Waterway is the
  Overflow Cloaca (`grm_g01`), entered from `naf_b04` below 25: Rabanastre's Lowtown doors test for 100
  (`rbn_a01` line 2492, `rbn_a03` line 4275, `rbn_a18` line 1841), and the other ways in leave `mic_d01` and
  `rrp_a06`, open from 316 and 190.
- In `grm_g01` below 27, `story counter < 27` (`case lt(27)`, line 205), `常駐監督.main` closes floor group 1
  (lines 272-276), which every floor path from the entrance to the exit into North Sprawl crosses, and the rat
  fight ends by writing 33 and jumping to Muthru Bazaar (lines 321, 327).

The read marks and the new-entry badge are described on [Clan Primer](clan-primer.md).

### Where the values come from

1. Each family's kind-7 base id is the `u16` at `0x00D23740` + 2 × family; the us path array names its
   `menuhandbook_<family>.bin` catalog (base), `.dat` unlock table (base + 1) and numbered files (base + 2 + n).
2. The names: families 0-4 through `0x002F9920`, text group id / 10000 and the row whose id equals it; the Bestiary
   through battle-text bank 8 (`0x003214B0`). The Esper short names are the class-20 names `0x0035D330(0x14, 0x106 + k)`,
   the summon actions 262-274 of [Action list](../Battle-Actions/action-list.md).
3. The unlock rules, slot thresholds and section gates as above; the rules come from the `in` copy of
   `menuhandbook.bin`, the one the path array names (kind-7 id `0xC8`, loaded by `0x003158B0`).
4. The text of each slot from the entry's text bundle, through the glyphs of the us font
   ([Text codes](text-codes.md), [Fonts](fonts.md)).
5. A section's map numbers are Map entries, named by the areas that carry them in
   [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md).

## Columns

### clan-primer-entries.tsv

| Column | Meaning | Read by |
|---|---|---|
| `family`, `family_name` | the family number 0-5 and its name: `story`, `world`, `person`, `knowledge`, Traveler's Tips, Bestiary | `0x005760A0` (slot 0 `+0xD2`) |
| `opened_by` | the category whose record at `0x00D23688` names the family, or `-` when no category names it | `0x0056F810` |
| `entry` | the record number in the family's catalog | `0x005760A0` |
| `name`, `name_id` | the record's name and its text id (families 0-4) or battle-text word (Bestiary) | `0x002F9920`, `0x003214B0` |
| `index_name` | the name the us index row shows: the Esper short name for words `0x4210`-`0x421C`, else `name` | `0x005761B0`-`0x005761FF`, `0x00571710` |
| `section`, `section_caption` | the section the entry is listed under, and its caption | `0x00576740`, `0x00576A50` |
| `unlock` | the unlock condition in plain words, with the story moment of the counter value | `0x00575E80`, `0x003154B0` |
| `save` | the save bit at `+0x32CC` that holds the unlock (families 0-4), or the Bestiary's kill count byte | `0x00315910`, `0x00315420` |
| `slots`, `slot_mode`, `slot_unlocks` | Bestiary: the number of text slots, the mode and each slot's condition | `0x005760A0`, `0x00576860`, `0x00576E30` |
| `countdown` | Bestiary: whether the index row shows the defeats to the next slot, and up to which count | `0x00571710` |
| `text_file`, `text_lines` | the text bundle that holds the entry, and its number of text slots | `0x00575D10`, `0x00576300` |
| `picture` | the picture file and the picture inside it | `0x00575DD0`, `0x00575B80` |
| `monsters`, `monster_count` | Bestiary: the enemy definitions (area, row, name) whose `primer_entry` is this entry, and how many; for the ten entries no definition names, which unlock by the story counter alone (33, 35, 278 and 377-383), `no definition names it` and the definitions the entry stands for, joined by the entry's gallery model to the definitions' `model_id`, or by name for Ba'Gamnan, whose gallery model no definition uses; their count stays 0 | [Bestiary](../Enemy-Spawning/bestiary.md) |
| `gallery_model_id`, `gallery_model` | the viewer's `monsterModelId` of `monstergallery.json` entry `MonsterId<n>`, and the model of a linked definition with that id | `0x001EB9C0` |
| `explanation` | a one-line summary | |

### clan-primer-texts.tsv

| Column | Meaning | Read by |
|---|---|---|
| `family`, `family_name`, `entry`, `name` | the entry, as in the entries file | |
| `slot` | the text slot, from 0 | `0x00576300` |
| `heading` | Bestiary: the part before code `0x03`, its lines joined by " / " (all of slot 0) | `0x00573BE0` |
| `text` | the text; line breaks are written as spaces, so a word the text breaks at a line end reads "lack- ing" | `0x00576300`, `0x00574900` |
| `shown_when` | the slot's condition; Traveler's Tips text shows with the entry | `0x00576E30` |

The text keeps its glyphs as the us font draws them. The pen-position code `0F o` is written as a space and an
inline icon as `[icon X]`, X its letter; colour and layout codes leave nothing ([Text codes](text-codes.md)).

### clan-primer-sections.tsv

| Column | Meaning | Read by |
|---|---|---|
| `family`, `family_name`, `section` | the section | `0x00576740` |
| `caption_id`, `caption` | the caption's text id and text | `0x00576A50` |
| `first_entry`, `entries` | the first entry listed under it and the number of its entries; the entries of a section are consecutive | `0x00576740` |
| `caption_shown` | always, or once part of a listed map has been explored, with the text shown until then | `0x00576A50` |
| `maps` | the gate's Map entries, each with the areas that carry it | `0x00255120`, `0x003779F0` |

## Data

### The families

| Family | Opened by | Entries | Sections | Unlocks | Text |
|---|---|---:|---:|---|---|
| Traveler's Tips (`tutorial`) | Traveler's Tips | 16 | 4 | 11 always, 5 by story counter | in the texts file |
| Bestiary (`monster`) | Bestiary | 384 | 32 | 367 by defeat, 14 by story counter, 1 by another monster, 2 through quests | in the texts file |
| `story` | no category | 69 | 4 | all by story counter | not in the texts file: each bundle carries its own glyph sheet |
| `world` | no category | 74 | 10 | 5 by story counter, 69 always | not in the texts file: each bundle carries its own glyph sheet |
| `person` | no category | 57 | 4 | always | not in the texts file: each bundle carries its own glyph sheet |
| `knowledge` | no category | 100 | 7 | always | not in the texts file: each bundle carries its own glyph sheet |

- The four unused families' names and captions are empty in the us text: 267 of their 325 names and captions,
  through 247 text ids, each "NOT USED" in the `fr` text. The other 58 are 57 `world` names and one `knowledge`
  name, place names such as "The Garamsythe Waterway" and "The Archadian Empire"; 47 of them use the text id of a
  Bestiary caption.
- Each of their text bundles carries its own glyph sheet, which `0x00575710` registers (`0x0039BEC0`), and their strings
  read as nonsense through the us font, so the texts file leaves them out. Each entry has one text slot, except 28
  `world` entries with two.

### The Bestiary

- Slots: 164 entries with 2, 215 with 3 and 5 with 7 (Seeq, Urutan-Yensa, Garif, Baknamy and Bangaa, entries
  372-376).
- The countdown shows on 212 rows. The 172 without it are Rare Game, Marks, Elite Marks, Bosses, Espers and The
  Archadian Empire, and four regional entries.
- Entries unlocked by the story counter: Battery Mimic and Tiny Battery (341), Miriam Guardian and Miriam Facer
  (2200), Rogue Tomato (78), Ba'Gamnan (660), Ahriman (3200), and the seven Archadian Empire entries Imperial (253),
  Imperial Elite (966), Judge Ghis (1015), Judge Bergan (2350), Imperial Armament (3500), Doctor Cid (3500) and Judge
  Gabranth (5500).
- Ten entries have no enemy definition that counts for them: Battery Mimic, Tiny Battery, Ba'Gamnan and the seven
  Archadian Empire entries, all unlocked by the story counter.
- The viewer's model is the model of a linked definition for 373 of the 374 entries with definitions; Skeleton
  (32) shows `0x006E0021`, which none of its four definitions uses.

## Related

- [Clan Primer: the Hunts, Bestiary, Sky Pirate's Den and Traveler's Tips pages, how entries unlock, and the monster viewer](clan-primer.md)
- [Handbook files: the hctg, hchk, hdat and himg files behind Clan Primer entries, how each is read, and what each field shows](../Game-Files-And-Data-Tables/handbook-files.md)
- [Bestiary: every enemy definition of every area with its name, level, stats, elements, statuses, loot and rewards](../Enemy-Spawning/bestiary.md)
- [Hunts: every hunt with its name, petitioner, row picture, record text, the progress that shows each part and when its row is marked done](../Story-Events-And-Hunts/hunts.md)
- [Achievements: the achievement list, the counters and conditions that award each one, and how an award reaches Steam](../Steam-And-Achievements/achievements.md)
- [Story counter values: every value the shipped scripts write to the main story counter, and the scripts and functions that write it](../Story-Events-And-Hunts/story-counter-values.md)
- [Kill rewards: what an enemy's death triggers, when it gives nothing, and the order of chain, EXP, LP, gil, loot and counters](../Rewards-EXP-Gil-And-Loot/kill-rewards.md)
- [JSON configs: every key of the jsondata documents, the code that reads it and what it sets, and the monster viewer's entries](../Game-Files-And-Data-Tables/json-configs.md)
- [Area flags: the navimapdata.bin record for every area, the town flag, the KO, Stone and X-Zone override and the other bits](../World-Areas-And-Travel/area-flags-navimapdata.md)

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x003171C0` calls `0x00263C20`; those functions are documented on
  [glossary](../Engine-Core/glossary.md).
- Combat AI: `0x0046B180` is called by `0x00321190`; `0x0046B1A0` is called by `0x00321190`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat formula: `0x00306F00` is called by `0x00300530`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Core runtime: `0x00254A10` calls `0x00229E40`; `0x00265270` is called by `0x001EC760`; `0x00316930` is called by `0x0022A770`;
  those functions are documented on [startup constants](../Engine-Core/startup-constants.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Developer: `0x001EB9C0` calls `0x001C6320`; those functions are documented on
  [json configs](../Game-Files-And-Data-Tables/json-configs.md).
- Gameplay: `0x00306F00` calls `0x003299B0`; `0x0035D330` calls `0x0031C5D0`; `0x00576A50` calls `0x00309EC0`; those functions are
  documented on [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md).
- Input: `0x00265270` is called by `0x00253C70`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Platform online achievements: `0x00255120` is called by `0x003160C0`; `0x00265270` is called by `0x003154B0`, `0x003161A0`;
  `0x00315420` is called by `0x003154B0`, `0x00315E90`, `0x003161A0`; `0x003154B0` calls `0x00315420`; `0x00315820` calls
  `0x00315D50`; `0x00315D50` is called by `0x00315820`; `0x00315DC0` is called by `0x00316930`; `0x00316930` calls `0x00315E90`,
  `0x003162E0`; `0x00316930` is called by `0x00316670`.
- Platform online achievements: `0x003779F0` is called by `0x003160C0`; `0x0046B180` is called by `0x00316480`; `0x0046B1A0` is
  called by `0x00316480`; `0x005760A0` calls `0x00315420`; `0x00576CA0` calls `0x003154B0`; `0x00576E30` calls `0x00315420`;
  `0x00577550` calls `0x00316930`.
- Platform online achievements: those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [achievements](../Steam-And-Achievements/achievements.md), [gil](../Rewards-EXP-Gil-And-Loot/gil.md),
  [jump thunks](../Engine-Core/jump-thunks.md), [bestiary](../Enemy-Spawning/bestiary.md).
- Platform online achievements: and on [frame update order](../Engine-Core/frame-update-order.md),
  [shops](../Items-Equipment-Shops-And-Licenses/shops.md).
- Presentation: `0x00254A10` is called by `0x002B0280`, `0x002D2DB0`; `0x00265270` is called by `0x001CD0E0`; `0x002F9920` is
  called by `0x0037E5B0`, `0x0037E8D0`; `0x0035D330` is called by `0x003BBD00`, `0x00506700`; `0x0046B1A0` is called by
  `0x00578450`.
- Presentation: those functions are documented on
  [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [menu lists](menu-lists.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [quest menu files](../Game-Files-And-Data-Tables/quest-menu-files.md),
  [augments](../Damage-And-Battle-Formulas/augments.md); and on [battle numbers](battle-numbers.md).
- Resource: `0x00265270` is called by `0x001DA220`, `0x001DA970`; `0x003158B0` calls `0x00249180`; `0x00575B80` calls `0x0024A440`;
  those functions are documented on [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md),
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md).
- Rewards progression economy: `0x003171C0` is called by `0x00312280`; those functions are documented on
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md).
- Save load settings: `0x00254A10` is called by `0x005832B0`; `0x0046B180` calls `0x002EF2B0`; `0x0046B1A0` calls `0x002EF2B0`;
  those functions are documented on
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Script VM: `0x0046B180` is called by `0x00351F90`; `0x0046B1A0` is called by `0x0033FAA0`; those functions are documented on
  [quests](../Story-Events-And-Hunts/quests.md).
- Spawn encounter lifecycle: `0x00306F00` calls `0x002360D0`; those functions are documented on
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md).
- Story event quest hunt: `0x00265270` is called by `0x001ED240`; those functions are documented on
  [model effects and motion commands](../Graphics/model-effects-and-motion-commands.md).
- Story event quest hunt: `0x00265270` is called by `0x00377970`; `0x00575E80` calls `0x0032A8A0`; those functions are
  documented on [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- World area: `0x00255120` is called by `0x00576A50`; `0x00265270` is called by `0x001EDCD0`, `0x003145E0`, `0x003EAA70`;
  `0x002F9920` is called by `0x003C0450`, `0x00576A50`; `0x00307030` is called by `0x00234590`; `0x003154B0` calls `0x00265270`;
  `0x003779F0` is called by `0x00576A50`; `0x00575E80` calls `0x00265270`; `0x00576740` calls `0x00576A50`; `0x00576A50` calls
  `0x003148F0`; `0x00576E30` calls `0x00265270`.
- World area: those functions are documented on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- World area: and on [force fight mode](../Engine-Core/force-fight-mode.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [party control modes](../Engine-Core/party-control-modes.md).
