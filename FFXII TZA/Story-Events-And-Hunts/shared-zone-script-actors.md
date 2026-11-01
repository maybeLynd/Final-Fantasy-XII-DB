---
title: "Shared zone-script actors: the crystal, the teleport and the key-item and message helpers"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00352C80, 0x00356500, 0x00351CE0, 0x00351940, 0x003462D0, 0x0034AC10, 0x00264CE0, 0x00344630, 0x003449A0, 0x003459C0, 0x0034A6D0, 0x0034ABF0, 0x0034B1E0, 0x0034A2C0, 0x002E2120, 0x002E16B0, 0x002A2C00, 0x002A5330, 0x0039BB20, 0x0039C150, 0x002F9860, 0x00300B80, 0x00349800, 0x0034A420, 0x00349BF0, 0x0034B760, 0x0034BB10, 0x00354D00, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x003567F0, 0x00352FA0, 0x00354110, 0x0050C860, 0x0050ED70, 0x0050EF50"
---

## What it lists

Five helper actors appear in many `us` zone scripts with the same code. They are described here once, and the
script pages of each area count them instead of listing their functions. The companion table has one row per
function of the five actors.

| Actor | Carried by | What the player sees |
|---|---|---|
| `system_crystal_actor` | 81 zone scripts | the save crystal or gate crystal of the map: heal, save, teleport |
| `telepoeffectctrl` | the same 81 | the teleport itself: the stone, the flash and the jump |
| `crystaldummyPC` | the same 81 | the character turning toward the crystal; the Crystal Mimic map icons |
| `saveactor` | the same 81 | nothing: no script requests its memory card prompt |
| `イベント特殊効果画面` | 193 zone scripts, the 81 among them | key items received and system messages, for other actors of the same script |

Each function's body is the same in every script that carries the actor, once script-local names are set aside
(see Project notes). The crystal reads its number from the engine, and the item and message helpers take their
values from script globals, so one description serves every script.

### The crystal

`system_crystal_actor` is the crystal the party walks up to. Its full engine side (the heal, the save screen, the
two save-image switches and the teleport) is on [Save crystals and gate crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
Its `init` does the following:

1. When the party lacks key item `0x8040` (Rabanastre), it gives it with `additem_47f` and adds it to the teleport
   list `g_menu_telepo_dest` (script global `0x0BF2`, 31 entries).
2. It reads the crystal number with `getcrystalid(3, 0)`. Number 4 (the Barheim crystal) counts as 0, a save
   crystal, while `ismapjumpgroupflag(0x402A)` is false, that is before story counter 1,540
   ([story flag ids](story-flag-ids.md)).
3. It names the crystal with `setnpcname` from the number (the table below).
4. On Succor Midst Sorrow (field 176), The Acolyte's Burden (186) and Walk of Revelation (608) it keeps the crystal
   hidden and untouchable while the script global `g_btl_クリスタルミミックレッド` (`0x0A33`), `ブルー` (`0x0A32`) or
   `グリーン` (`0x0A31`) is not 2. On Walk of Revelation it also sets flag 127 and releases 128 when the global
   is 2, and the reverse otherwise.

### Talking to the crystal

`talk` runs when the player confirms at the crystal. In order:

1. It suspends battle, heals the whole party with `healall(0)` and plays revive effect 11 on each member who is
   down, then plays sound 45 and requests `crystaldummyPC.クリスタルビュー`.
2. A gate crystal gives its key item with `additem_47f` the first time and adds it to the teleport list.
3. It opens a menu from the two save-image switches, `getsaveramsavestatus` and `getsaveramtelepostatus`; the
   table below gives each menu.
4. Unless a teleport was started, it requests `crystaldummyPC.クリスタルリリース`, resumes battle (`resumebattle`)
   and undoes the `sethpmenu(0)` and `ucoff()` calls it made at the start.

| Crystal | Save allowed, teleport allowed | Save only | Teleport only | Neither |
|---|---|---|---|---|
| gate crystal | "You touch the gate crystal." Save, Teleport, Done | "A strong Mist prevents teleportation." Save, Done | "A strong Mist prevents saving." Teleport, Done | "A strong Mist prevents both saving and teleportation." |
| save crystal | "Save your current game?" Yes, No | the same | "A strong Mist prevents saving." | the same |
| Life Crystal (number 255) | no menu: it waits 30 frames | the same | the same | the same |

### Saving at the crystal

The save choice runs the same steps from every menu:

1. While the zone's scratch1 word `0x12` is non-zero it first warns "You will not be able to leave this area easily.
   You may wish to save your game to a new file."; on the Antechamber of Sky Fortress Bahamut (field 777) the
   warning is "You cannot leave the Bahamut! It is strongly recommended that you save your game to a new file."
2. It sets the entrance index to -2, the zone's save entrance, with `setnowjumpindex`. On Valley of the Dead
   (field 403) while the story counter is below 1,345 it heals the party again instead and keeps the entrance.
3. It fades out, opens the save screen with `openfullscreenmenu_48d(0x8005, 0)`, waits for it to close, fades in
   and puts the entrance index back.

### Choosing a destination

The teleport choice works like this:

1. With no Teleport Stone (item `0x2000`) it says "You don't have any teleport stones."
2. Otherwise it lists the first 25 entries of the teleport list and asks "Select a destination:".
3. Choosing the map the party stands in gives "You cannot teleport to your current location."
4. With an Esper summoned it asks "Teleporting will dismiss your Esper. Proceed?"; on a chocobo it asks
   "Teleporting will cause you to dismount. Proceed?". No cancels.
5. It stores the destination's key item in a file-scope word and requests `telepoeffectctrl.telepoeffect`.

### The teleport

`telepoeffectctrl.telepoeffect` is requested only by the crystal's `talk`, twice in each of the 81 scripts. It
calls `sysSysreqwait(system_crystal_actor::touchon)`, takes one Teleport Stone with `subitem(0x2000, 1)`, plays
sound 95 and the party flash (`effectteleposyncbyid(partycommoneffectplay(12))`), calls `whiteout_d1(2, 0)` and,
with a summon or chocobo out, requests `choco_sum_ctrl_murasawa.sumcho_byebye`. Then it jumps with
`mapjump(field, entrance, 10)`:

| Key item | Destination | Field | Entrance |
|---|---|---|---|
| `0x8040` Rabanastre | Southgate (Rabanastre) | `306` | 4 |
| `0x8042` Nalbina Fortress | West Barbican (Nalbina Town) | `630` | 0 |
| `0x8043` Barheim Passage | North-South Junction (Barheim Passage) | `66` | 0 |
| `0x8044` The Salikawood | Quietened Trace (The Salikawood) | `157` | 4 |
| `0x8045` Nabreus Deadlands | Succor Midst Sorrow (Nabreus Deadlands) | `176` | 0 |
| `0x8047` Archades | Tsenoble (Archades) | `756` | 3 |
| `0x8048` The Sochen Cave Palace | Skybent Chamber (Sochen Cave Palace) | `188` | 3 |
| `0x8049` The Henne Mines | Staging Shaft (Henne Mines) | `718` | 0 |
| `0x804A` Bhujerba | Aerodrome (Bhujerba) | `791` | 0 |
| `0x804B` The Lhusu Mines | Transitway 2 (Lhusu Mines) | `360` | 0 |
| `0x804C` The Tomb of Raithwall | Valley of the Dead (The Tomb of Raithwall) | `403` | 3 |
| `0x804E` Golmore Jungle | The Parting Glade (Golmore Jungle) | `450` | 4 |
| `0x8050` Giruvegan | Gate of Earth (Giruvegan) | `686` | 1 |
| `0x8051` The Stilshrine of Miriam | Walk of Mind (Stilshrine of Miriam) | `594` | 3 |
| `0x8052` The Port at Balfonheim | Sea Breeze Lane (Balfonheim Port) | `823` | 0 |
| `0x8053` The Pharos at Ridorana | The Wellspring (Pharos - First Ascent) | `1101` | 0 |
| `0x8054` Jahara | Banks of the Sogoht (Jahara) | `751` | 0 |
| `0x8055` Eruyt Village | Road of Verdant Praise (Eruyt Village) | `768` | 4 |
| `0x8056` Mt Bur-Omisace | Sand-strewn Pass (Mt Bur-Omisace) | `742` | 3 |
| `0x8057` Dalmasca Estersand | South Bank Village (Dalmasca Estersand) | `129` | 0 |
| `0x8058` Dalmasca Westersand | The Western Divide (Dalmasca Westersand) | `350` | 0 |
| `0x8059` Mosphoran Highwaste | Babbling Vale (Mosphoran Highwaste) | `1151` | 7 |
| `0x805A` Ogir-Yensa Sandsea | Yensa Border Tunnel (Ogir-Yensa Sandsea) | `386` | 1 |
| `0x805B` The Phon Coast | Hunters' Camp (Phon Coast) | `488` | 0 |
| `0x805C` Tchita Uplands, the switch's default | The Chosen Path (Tchita Uplands) | `142` | 3 |

### Crystal numbers, names and key items

The crystal number selects the name tag (`us` `npcdic.bin`, second name of the pair) and the key item `talk` gives:

| Number | Name | Key item | Number | Name | Key item |
|---:|---|---|---:|---|---|
| 0 | Save Crystal | - | 17 | Giruvegan Crystal | `0x8050` |
| 255 | Life Crystal | - | 18 | Miriam Crystal | `0x8051` |
| 1 | Rabanastre Crystal | `0x8040` | 19 | Balfonheim Crystal | `0x8052` |
| 3 | Nalbina Crystal | `0x8042` | 20 | Ridorana Crystal | `0x8053` |
| 4 | Barheim Crystal | `0x8043` | 21 | Jahara Crystal | `0x8054` |
| 5 | Salika Crystal | `0x8044` | 22 | Eruyt Crystal | `0x8055` |
| 6 | Nabreus Crystal | `0x8045` | 23 | Bur-Omisace Crystal | `0x8056` |
| 8 | Archades Crystal | `0x8047` | 24 | Estersand Crystal | `0x8057` |
| 9 | Sochen Crystal | `0x8048` | 25 | Westersand Crystal | `0x8058` |
| 10 | Henne Crystal | `0x8049` | 28 | Mosphoran Crystal | `0x8059` |
| 11 | Bhujerba Crystal | `0x804A` | 29 | Yensa Crystal | `0x805A` |
| 12 | Lhusu Crystal | `0x804B` | 32 | Phon Crystal | `0x805B` |
| 13 | Tomb Crystal | `0x804C` | 33 | Tchita Crystal | `0x805C` |
| 15 | Golmore Crystal | `0x804E` | any other | Gate Crystal | - |

### The crystal's other functions

The remaining functions of the crystal and its helper show or hide it and turn the character:

- `main` shows the crystal and allows talking to it, or hides it when a Crystal Mimic keeps it hidden or a
  file-scope word of the zone script asks for it; it then loops, calling `charefftrigger(2)` once after each touch.
- `touchon` (also bound to `touch`, `fieldsign1` and `fieldsign2`) calls `charefftrigger(1)` and marks the crystal
  touched; `touchoff` calls `charefftrigger(2)` when it is marked and clears the mark.
- `showoff` hides the crystal and blocks talking; `showon` shows it again. Other actors of 28 and 48 zone scripts
  request them (41 and 74 requests).
- `crystaldummyPC.クリスタルビュー` takes the character the player controls (`capturepc(-1)`) and turns it toward
  the crystal; `クリスタルリリース` hands the character back (`releasepc`). `クリスタルタッチ` turns it too; no
  `us` script requests it.
- `crystaldummyPC.main` loops every frame; on Succor Midst Sorrow, The Acolyte's Burden and Walk of Revelation it
  keeps the map-icon flags `0x165`, `0x164`, and 127 and 128, in step with the Crystal Mimic globals and the
  zone's scratch word `0x20`.

### The memory card save actor

`saveactor` holds a memory card save-and-load prompt for Slot 1 with ten slots each way ("Save or load?",
"Format memory card in Slot 1?"), built on the debug memory card verbs. Its `save_load` is requested by no `us`
script, and its `save` and `load` only by `save_load`, so nothing in it reaches the player. The game's save is the
crystal's save screen above.

### The key-item and message helpers

`イベント特殊効果画面` gives key items and shows system messages for other actors of its script. The caller stores
an item id or a message number in the script globals `g_com_set_get_label` (`0x0C88`), `g_com_set_get_label_2`
(`0x0C8C`) and `g_com_set_get_label_3` (`0x0CF0`), then requests the function with `sysReqew`. 106 of the 193
scripts request it, 204 times. Each function wraps its steps in `musictrans(-1, 30, 32)` and
`musictrans(-1, 30, 127)`, `seteventtimestop(1)` and `(0)`, and the `moveblur` verbs. In the table, `label`,
`label_2` and `label_3` stand for the three globals:

| Function | Steps | Requests |
|---|---|---:|
| `だいじなものゲット` | sound 40, then the obtained window for one of item `label` (`additemmes`), which gives it when it closes | 91 |
| `だいじなものゲット_FADE付` | the same, then `wait(8)` and `fadeout(15)` | 10 |
| `だいじなものゲット_MJFADE付` | the same, then `wait(8)` and `fadeout_d0(2, 15)` | 4 |
| `システムメッセージ表示` | system message `label` | 53 |
| `システムメッセージ表示_FADE付` | the same, then `wait(8)` and `fadeout(15)` | 5 |
| `ゲット＆メッセージ表示` | item `label`, then system message `label_2` | 38 |
| `ゲット＆ゲット` | item `label`, then item `label_2` | 1 |
| `GET_SYSMES_GET表示` | item `label`, system message `label_2`, item `label_3` | 1 |
| `GET_SYSMES_SYSMES表示` | item `label`, then system messages `label_2` and `label_3` | 1 |

The items callers pass are key items, from the Ageworn Key (`0x80B5`, 16 requests) and the Auric Message
(`0x80A7`, 10) to the area maps (`0x800B` Ogir-Yensa Sandsea and others); 14 requests pass values from tables of
the calling function.

### How a system message is shown

A system message is an entry of the message list, not a line of the script. The steps:

1. The helper calls `setmeswinmesid(0, number)` (`0x47E`, `0x0034A2C0`), which stores the number in word `+0x58` of
   message slot 0 (`0x002E2120`, [message windows](../Menus-And-HUD/message-windows.md)), then opens the window with
   `ames_1fe` on a section 2 entry that is an empty string in every carrying script.
2. The window opener `0x002E16B0` copies the word into the window request (`0x002E17C5`). When it is non-zero
   (`0x002A2D4A`), the window build `0x002A2C00` takes its low byte minus 1 (`0x002A2D62`-`0x002A2D6B`) and calls
   `0x002A5330` (`0x002A2D71`).
3. `0x002A5330` reads that entry of the list `0x0039BB20` returns, the qword at `0x02AEE888`: section 5 of
   the language's `packfiles/fontpack_it.bin` (the `us` copy for the `us` text; the file carries that name in every
   language folder), bound to `0x02AEE888` by `0x0039C150` (`0x0039C26B`). It formats the entry's text (`0x002F9860`) with the names its
   kind selects into the buffer `0x0209C990` and returns it to the build (`0x002A2D76`).

List = count:u32, then 8-byte entries from +4 entry n-1 for message number n:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` |  | text id, group * 1000 + row (`0x002F9860`) |
| `+0x02` | `u16` |  | first id |
| `+0x04` | `u16` |  | second id |
| `+0x07` | `u8` |  | kind: 0 text only; 1 to 5 name the ids through `0x0035D330`; 1 also gives the first id (`0x00300B80`, `0x002A541B`) |

The `us` list holds 145 entries. The messages callers pass are of kind 0 or 5, so none gives an item:

| Number | Message | Requests |
|---:|---|---:|
| 139 | You are now free to ride the cab. | 38 |
| 140 | You found all of the moogles! | 4 |
| 129 | A crystal appears! | 3 |
| 131 | The ancient device stirs. | 2 |
| 141 | The Lusterless Medallion keens... | 2 |
| 52 | You are now free to enter Lowtown and leave Rabanastre. | 1 |
| 53 | Clan Primer has been added to the Party Menu. | 1 |
| 57 | World Map has been added to the Party Menu. | 1 |
| 60 | Licenses has been added to the Party Menu. | 1 |
| 130 | The Urutan Eater has fallen! | 1 |
| 132 | You hand a potion to the Imperial. | 1 |
| 133 | The gil snapper was drawn into the urn. | 1 |
| 135 | The Strahl can now travel through jagd! | 1 |
| 136 | The Strahl can now travel to Bahamut! | 1 |
| 138 | The way past the colossus is open! | 1 |
| 142 | You are now a member of Clan Centurio! | 1 |
| 90 to 126 | "Your location map for this area is complete!" or "The candle reveals hidden areas on your map of the" with the map's name (kind 5) | 25 |

### How a call is read

The verbs whose effect this page states, with their native bodies ([verb table](../Scripts-And-Script-Commands/verb-table.md)):

| Verb | Id | Native body | Effect |
|---|---|---|---|
| `getcrystalid` | `0x30E` | `0x00352C80` | the crystal number |
| `healall` | `0x3AF` | `0x00356500` | heals the party (argument 0: HP, MP and the status set A) |
| `getsaveramsavestatus`, `getsaveramtelepostatus` | `0x30B`, `0x30A` | `0x00351CE0`, `0x00351940` | 1 while saving (teleporting) is allowed |
| `openfullscreenmenu_48d` | `0x48D` | `0x003462D0` | opens the save screen and waits for it |
| `setnowjumpindex` | `0x3D1` | `0x0034AC10` | the entrance index; -2 resolves to the save entrance (`0x00264CE0`) |
| `haveitem`, `additem_47f`, `subitem` | `0x2E4`, `0x47F`, `0x2F2` | `0x00344630`, `0x003449A0`, `0x003459C0` | item count, give, take ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `additemmes` | `0x480` | `0x0034A6D0`, `0x0034ABF0`, `0x0034B1E0` | the obtained window, then the item |
| `setmeswinmesid` | `0x47E` | `0x0034A2C0` | the system message number of a message slot |
| `ames`, `ames_1fe`, `amese` | `0x00F`, `0x1FE`, `0x145` | `0x00349BF0`, `0x00349800`, `0x0034A420` | a section 2 line in a window |
| `aask`, `aaske` | `0x010`, `0x14A` | `0x0034B760`, `0x0034BB10` | a section 2 line with a choice |
| `mapjump` | `0x08D` | `0x00354D00` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `effectteleposyncbyid` | `0x43D` | `0x003567F0` | waits for the party flash |
| `setnpcname` | `0x38A` | `0x0034B9A0` | the name tag ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | Primary bank flags |
| `capturepc`, `releasepc` | `0x057`, `0x058` | `0x00352FA0`, `0x00354110` | takes and hands back a party member's body ([party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md)) |
| `debug_mc_connect_check`, `debug_mc_write_savedata`, `debug_mc_read_savedata` | `0x20BD`, `0x20B9`, `0x20BA` | `0x0050C860`, `0x0050ED70`, `0x0050EF50` | the memory card verbs of `saveactor` |

### The 81 crystal scripts

`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC` and `saveactor` are carried together, by these zone
scripts:

| Script | Map (region) | Field |
|---|---|---:|
| `alc_c01` | Tsenoble (Archades) | `756` |
| `alc_e01` | Aerodrome (Archades) | `794` |
| `ald_a01` | Alley of Muted Sighs (Old Archades) | `762` |
| `bhm_a04` | Antechamber (Sky Fortress Bahamut) | `777` |
| `bog_a02` | The Muted Scarp (Nabreus Deadlands) | `168` |
| `bog_b02` | Succor Midst Sorrow (Nabreus Deadlands) | `176` |
| `bul_b02` | Sand-strewn Pass (Mt Bur-Omisace) | `742` |
| `byu_a04` | Lhusu Square (Bhujerba) | `806` |
| `byu_b01` | Aerodrome (Bhujerba) | `791` |
| `dor_c12` | 70th Floor (Draklor Laboratory) | `1047` |
| `dor_d06` | Rm 6704 East (Draklor Laboratory) | `1059` |
| `dst_a05` | Passage Entrance (Dalmasca Estersand) | `231` |
| `dst_b01` | South Bank Village (Dalmasca Estersand) | `129` |
| `ene_a08` | Yensa Border Tunnel (Ogir-Yensa Sandsea) | `386` |
| `enw_a05` | The Sandscale Bank (Nam-Yensa Sandsea) | `394` |
| `fon_a06` | Kaukula Pass (Phon Coast) | `483` |
| `fon_b01` | Hunters' Camp (Phon Coast) | `488` |
| `fon_c04` | Rava's Pass (Phon Coast) | `494` |
| `frs_a06` | Path of Hours (The Salikawood) | `156` |
| `frs_b01` | Quietened Trace (The Salikawood) | `157` |
| `gil_a01` | Gate of Earth (Giruvegan) | `686` |
| `gil_c01` | The Haalmikah Water-Steps (Giruvegan) | `694` |
| `gil_g10` | Crystal Core (The Great Crystal) | `341` |
| `gil_l02` | Kanbhru Pis (The Great Crystal) | `1003` |
| `glf_a01` | Banks of the Sogoht (Jahara) | `751` |
| `gol_a04` | The Parting Glade (Golmore Jungle) | `450` |
| `grm_a01` | Central Spur Stairs (Garamsythe Waterway) | `311` |
| `grm_a04` | East Spur Stairs (Garamsythe Waterway) | `314` |
| `grm_b02` | East Sluice Control (Garamsythe Waterway) | `319` |
| `grm_b05` | Central Waterway Control (Garamsythe Waterway) | `322` |
| `grm_e03` | East Sluice Control (Garamsythe Waterway) | `840` |
| `grm_e13` | Central Waterway Control (Garamsythe Waterway) | `850` |
| `hne_a07` | Staging Shaft (Henne Mines) | `718` |
| `lus_a04` | Transitway 2 (Lhusu Mines) | `360` |
| `lus_f05` | Staging Area (Lhusu Mines) | `905` |
| `mfr_a04` | Antiquity's End (The Feywood) | `542` |
| `mic_a01` | The Lightworks (Barheim Passage) | `53` |
| `mic_b06` | North-South Junction (Barheim Passage) | `66` |
| `mic_b07` | no field entry in the zone-script list | - |
| `mic_c02` | Terminus No. 4 Adjunct (Barheim Passage) | `70` |
| `mic_e04` | Terminus No. 7 Adjunct (Barheim Passage) | `894` |
| `mnt_d01` | Babbling Vale (Mosphoran Highwaste) | `1151` |
| `mrm_a02` | Walk of Mind (Stilshrine of Miriam) | `594` |
| `mrm_d03` | Walk of Revelation (Stilshrine of Miriam) | `608` |
| `nac_a01` | West Barbican (Nalbina Town) | `630` |
| `naf_b02` | Upper Apartments (Nalbina Fortress) | `280` |
| `nal_a01` | Stockade (Nalbina Dungeons) | `48` |
| `nal_c02` | The Confiscatory (Nalbina Dungeons) | `710` |
| `ozm_b04` | Sunlit Path (Ozmone Plain) | `533` |
| `pbc_a01` | Fading Vale (Paramina Rift) | `463` |
| `pbc_c01` | Path of the Firstfall (Paramina Rift) | `473` |
| `pla_a05` | The Shaded Path (Tchita Uplands) | `141` |
| `pla_a06` | The Chosen Path (Tchita Uplands) | `142` |
| `pla_b06` | The Nameless Spring (Tchita Uplands) | `149` |
| `rbl_a01` | The Wellspring (Pharos - First Ascent) | `1101` |
| `rbl_a02` | Horizon's Break (Pharos - First Ascent) | `1102` |
| `rbl_a03` | The Reach (Pharos - Second Ascent) | `1103` |
| `rbl_a04` | Reach of the Damned (Pharos - Second Ascent) | `1104` |
| `rbl_a05` | Reach of the Occult (Pharos - Second Ascent) | `1105` |
| `rbl_q01` | Empyrean Ravel (Pharos - Third Ascent) | `1143` |
| `rbn_a17` | Eastgate (Rabanastre) | `305` |
| `rbn_a18` | Southgate (Rabanastre) | `306` |
| `rbn_a19` | Westgate (Rabanastre) | `307` |
| `rrp_a01` | Cellar Stores (Royal Palace) | `567` |
| `rsn_a01` | Port Launch (Dreadnought Leviathan) | `552` |
| `rsn_y01` | Brig No. 1 (Dreadnought Leviathan) | `876` |
| `rui_a03` | The Acolyte's Burden (Sochen Cave Palace) | `186` |
| `rui_a05` | Skybent Chamber (Sochen Cave Palace) | `188` |
| `rwf_a01` | Footfalls of the Past (Ridorana Cataract) | `509` |
| `rwf_b02` | Path of Hidden Blessing (Ridorana Cataract) | `518` |
| `rwg_a01` | Valley of the Dead (The Tomb of Raithwall) | `403` |
| `sav_b01` | Nomad Village (Giza Plains) | `243` |
| `sav_c02` | Crystal Glade (Giza Plains) | `248` |
| `sav_e01` | Nomad Village (Giza Plains) | `260` |
| `sav_f02` | Crystal Glade (Giza Plains) | `265` |
| `srb_a04` | Journey's Rest (Cerobi Steppe) | `500` |
| `var_a01` | Sea Breeze Lane (Balfonheim Port) | `823` |
| `var_b01` | Aerodrome (Balfonheim Port) | `797` |
| `vic_a03` | Road of Verdant Praise (Eruyt Village) | `768` |
| `wdl_a06` | The Western Divide (Dalmasca Westersand) | `350` |
| `ztc_b01` | The Undershore (Zertinan Caverns) | `581` |

### The other 112 scripts with the key-item and message helper

`イベント特殊効果画面` is carried by the 81 scripts above and by these:

| Region | Scripts |
|---|---|
| Archades | `alc_a02`, `alc_b03`, `alc_b04`, `alc_b05`, `alc_b06`, `alc_f01`, `alc_f02`, `alc_f03`, `alc_f04`, `alc_f05` |
| Balfonheim Port | `var_a04`, `var_a05`, `var_a06`, `var_a14`, `var_z01` |
| Barheim Passage | `mic_a02`, `mic_e02` |
| Bhujerba | `byu_a01`, `byu_a02`, `byu_a03`, `byu_a07`, `byu_a08`, `byu_a11`, `byu_a12`, `byu_a14`, `byu_a15`, `byu_a16`, `byu_a17`, `byu_a18` |
| Cerobi Steppe | `srb_a01`, `srb_a02`, `srb_a03`, `srb_b01`, `srb_b02`, `srb_b03`, `srb_b04` |
| Dalmasca Estersand | `dst_a01`, `dst_a02`, `dst_b02` |
| Dalmasca Westersand | `wdl_a05` |
| Draklor Laboratory | `dor_a02`, `dor_c02`, `dor_e04`, `dor_e09`, `dor_z01` |
| Dreadnought Leviathan | `rsn_b01`, `rsn_d01` |
| Eruyt Village | `vic_a01` |
| Garamsythe Waterway | `grm_a06`, `grm_e04`, `grm_e05` |
| Giruvegan | `gil_b01` |
| Giza Plains | `sav_a01`, `sav_a02`, `sav_a03`, `sav_a04`, `sav_c01`, `sav_c03`, `sav_f01`, `sav_g01` |
| Golmore Jungle | `gol_a01`, `gol_b01` |
| Henne Mines | `hne_a03`, `hne_c01` |
| Jahara | `glf_a02`, `glf_a03` |
| Lhusu Mines | `lus_f02` |
| Lowtown | `slm_a01`, `slm_a02`, `slm_a03`, `slm_a04` |
| Mt Bur-Omisace | `bul_a01`, `bul_a02`, `bul_a03` |
| Nabreus Deadlands | `bog_a03`, `bog_a05`, `bog_b04` |
| Nalbina Town | `nac_a02` |
| Nam-Yensa Sandsea | `enw_a02` |
| Necrohol of Nabudis | `bds_f01`, `bds_g01` |
| Ogir-Yensa Sandsea | `ene_a01` |
| Old Archades | `ald_a02` |
| Ozmone Plain | `ozm_c01` |
| Paramina Rift | `pbc_c03` |
| Pharos - First Ascent | `rbl_b01` |
| Pharos - Second Ascent | `rbl_l01` |
| Pharos - Third Ascent | `rbl_n01` |
| Rabanastre | `rbn_a01`, `rbn_a03`, `rbn_a04`, `rbn_a07`, `rbn_a09`, `rbn_a10`, `rbn_a14`, `rbn_a16` |
| Ridorana Cataract | `rwf_d01` |
| Skyferry | `asp_a02` |
| Sochen Cave Palace | `rui_a02` |
| Stilshrine of Miriam | `mrm_b02`, `mrm_c01` |
| Tchita Uplands | `pla_a03`, `pla_a04`, `pla_b04` |
| The Feywood | `mfr_a02`, `mfr_c01` |
| The Salikawood | `frs_a02`, `frs_a05`, `frs_c02` |
| The Tomb of Raithwall | `rwg_c01` |
| Zertinan Caverns | `ztc_a01`, `ztc_c01` |

### Event scripts

The scene scripts `nal_c0200` and `rwg_a0100` hold an actor named `system_crystal_actor` whose functions only
return (`init`, `showoff` and `showon`; `init` and `main`). No script requests them. The script lists of the area
pages show it as differing from the shared actor.

## Columns

| Column | Meaning |
|---|---|
| `actor`, `function` | the shared actor and its function, as the scripts name them |
| `trigger` | the function's slot (`init`, `main`, `talk`, `touchon` and its bound slots, `touchoff`), `requested` when other functions start it by name, `-` when nothing starts it |
| `carried_by` | how many `us` zone scripts carry the actor |
| `requested_by` | the functions that request it, or how many requests the `us` scripts make |
| `does` | what the function does, in game terms |

## Related

- [Save crystals and gate crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md) - the heal, the save screen, the switches and the teleport in the engine.
- [Nalbina Dungeons scripts](nalbina-dungeons-scripts.md) - an area page that counts these actors per script.
- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md) - `additemmes` and the other item verbs.
- [Message windows](../Menus-And-HUD/message-windows.md) - the message slots and the window build.
- [Story flag ids](story-flag-ids.md) - the map-icon flags and `0x402A`.
