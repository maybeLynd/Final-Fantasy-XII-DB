---
title: "Pharos - Third Ascent scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table has one row per script function of the `dgl` scripts that does something a player can observe. It covers the
four zone scripts and the nine scene scripts of the group, from `plan_master/us`; three maps are in Pharos - Third
Ascent and one, Hell's Challenge, is in Pharos - Subterra:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `dgl_f01` | zone | Womb of the Sun-cryst, field `666` | 7 | 9 | 2 | 0 |
| `dgl_g01` | zone | Womb of the Sun-cryst, field `668` | 12 | 20 | 3 | 0 |
| `dgl_h01` | zone | Heaven's Challenge, field `670` | 8 | 11 | 1 | 0 |
| `dgl_n01` | zone | Hell's Challenge, field `682` | 17 | 24 | 1 | 0 |
| `dgl_a0100` | scene | event `383` | 8 | 32 | 0 | 0 |
| `dgl_a0101` | scene | event `384` | 13 | 72 | 0 | 0 |
| `dgl_f0100` | scene | event `385` | 23 | 173 | 2 | 0 |
| `dgl_g0100` | scene | event `386` | 32 | 1181 | 1 | 0 |
| `dgl_g0101` | scene | event `387` | 37 | 399 | 17 | 0 |
| `dgl_g0102` | scene | event `388` | 27 | 427 | 21 | 0 |
| `dgl_g0103` | scene | event `389` | 31 | 196 | 18 | 0 |
| `dgl_h0100` | scene | event `380` | 15 | 100 | 0 | 0 |
| `dgl_h0101` | scene | event `381` | 16 | 88 | 1 | 0 |

None of the four zone scripts carries the helper actors that many zone scripts share ([Shared zone-script
actors](shared-zone-script-actors.md)). The scene `dgl_g0103` holds its own helper `イベント特殊効果画面_EV`, which is not one
of them, so its functions have rows.

The other maps of Pharos - Third Ascent and Pharos - Subterra are on [Pharos - First Ascent
scripts](pharos-first-ascent-scripts.md). The scenes `dgl_a0100` and `dgl_a0101` are loaded by The Bounds of Truth,
`rbl_j02`, of that group (`SAKIYOMI_ev_dgl_a0100` and `SAKIYOMI_ev_dgl_a0101`), so their rows here name no loading
function.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of
its actor in `other_functions`. The scenes themselves, with their dialogue, are on [Pharos - Third Ascent
scenes](pharos-third-ascent-scenes.md).

### What the scripts do

- Womb of the Sun-cryst, field `666`: below story counter 5,400 `常駐ディレクター.init` loads scene `dgl_f0100` (event 385),
  in which the party stand where King Raithwall cut the Sun-cryst; `常駐ディレクター.main` writes 5400, after the first half
  of the last nethicite, and 5450, after the nethicite drawn together, and jumps to Womb of the Sun-cryst, field
  `668`.
- Womb of the Sun-cryst, field `668`: `常駐ディレクター.main` loads scenes `dgl_g0100` (event 386), `dgl_g0101` (event 387),
  `dgl_g0103` (event 389) and `dgl_g0102` (event 388), shows the boss gauge and removes the foes, and writes 5470,
  after the last nethicite; 5500, after the Judge Gabranth battle; 5550, after Cid's ambition; 5600, after the Famfrit
  battle; 5650, after the Sun-cryst runs wild; and 6000, after Vaan on the ship.
- Womb of the Sun-cryst, field `668`: `常駐ディレクター.main` takes the Dawn Shard and the Sword of Kings and jumps to Saccio
  Lane (Balfonheim Port), field `826`. The scene `dgl_g0103` gives Famfrit.
- Heaven's Challenge, field `670`: `監督.main` shows the boss gauge, removes the foes, loads scenes `dgl_h0100` (event
  380), `dgl_h0101` (event 381) and `pos_z0000` (event 427), and jumps to Empyrean Ravel (Pharos - Third Ascent),
  field `1143`. The scene `dgl_h0101` gives Hashmal.
- Hell's Challenge, field `682`: `常駐監督.main` shows the boss gauge and the Shadowseer's six lines ("Ahhh... It wishesss
  to play... Arise, my ssservant... Arise..."), and jumps to The Wellspring (Pharos - First Ascent), field `1101`, or
  to the field the script global `g_iw_陰陽師終了後ジャンプ先` holds, which the elevators (`ele`) of The Wellspring and of
  Penumbra, Umbra and Abyssal - Interior set to their own map.
- Womb of the Sun-cryst, field `668`, and the scene `dgl_g0102`: `choco_sum_ctrl.sumcho_byebye` and
  `sumcho_byebye_fadeout` release flag `0x0073`, riding a chocobo.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in these scripts: every
assignment to it is a write and every comparison a test ([story counter values](story-counter-values.md)).

### The four message verbs reach one window call

The four message verbs all end in `mes` (`0x461`, `0x00348DF0`), which looks the text id up in the issuing script's
section 2 ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)):

1. `amese` (`0x0034A420`) pushes 0, 0, 0 and -1; `amest` (`0x0034A090`) pushes 0; `ames` (`0x00349BF0`) pushes 1. Each then
   jumps to `0x00349800`, the body of `ames_1fe`.
2. `0x00349800` pops two values (`0x00349827`, `0x00349831`), pushes 0 and 0 (`0x0034983D`, `0x00349847`) and then pushes the
   two values back in their original order (`0x00349851`, `0x0034985B`), so the zeros lie beneath them; it jumps to
   `0x00348DF0` (`0x00349884`).
3. `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context
   to `0x00264D60` (`0x00348E6A`-`0x00348E74`), the section 2 lookup, which keeps the low 24 bits of the id.

### Speakers, places and scenes

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. The
  message window opener `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line; a system message is not spoken by the actor |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`. The Shadowseer's lines begin with the speaker's name, which the text itself carries (`Shadowseer`).

The script list [`pharos-third-ascent-script-list.tsv`](pharos-third-ascent-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Pharos - Third Ascent scenes](pharos-third-ascent-scenes.md) - the nine scenes these scripts load.
- [Pharos - First Ascent scripts](pharos-first-ascent-scripts.md) - the other maps of the Pharos, and the two scenes
  `dgl_a0100` and `dgl_a0101` loaded there.
- [Balfonheim Port scripts](balfonheim-port-scripts.md) - Saccio Lane, where the Womb of the Sun-cryst jumps.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
