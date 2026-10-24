---
title: "Feywood scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [feywood-scripts.tsv](feywood-scripts.tsv) has one row per script function of The Feywood that does
something a player can observe. It covers the eight zone scripts and the four scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `mfr_a01` | zone | Walk of Flitting Rifts, field `539` | 34 | 75 | 17 | 0 |
| `mfr_a02` | zone | Walk of Stolen Truths, field `540` | 35 | 70 | 15 | 1 |
| `mfr_a03` | zone | Walk of Dancing Shadow, field `541` | 35 | 76 | 18 | 0 |
| `mfr_a04` | zone | Antiquity's End, field `542` | 26 | 85 | 9 | 5 |
| `mfr_b01` | zone | Redolent Glade, field `545` | 24 | 39 | 6 | 0 |
| `mfr_c01` | zone | White Magick's Embrace, field `548` | 31 | 62 | 12 | 1 |
| `mfr_c02` | zone | Ice Field of Clearsight, field `549` | 36 | 97 | 22 | 0 |
| `mfr_c03` | zone | The Edge of Reason, field `550` | 50 | 143 | 30 | 0 |
| `mfr_a0400` | scene | event `353` | 14 | 103 | 0 | 0 |
| `mfr_b0100` | scene | event `350` | 16 | 73 | 0 | 0 |
| `mfr_b0101` | scene | event `351` | 16 | 72 | 2 | 0 |
| `mfr_c0300` | scene | event `352` | 13 | 61 | 0 | 0 |

Antiquity's End carries the five helper actors that many zone scripts share: the crystal (`system_crystal_actor`,
`telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper `イベント特殊効果画面`; Walk of Stolen
Truths and White Magick's Embrace carry the key-item and message helper alone. Their functions are described once on
[Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts
them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party. Functions that
only move, animate, wait, play sound or set the camera are not listed; each listed row counts the other functions of
its actor in `other_functions`. The scenes themselves, with their dialogue, are on [Feywood
scenes](feywood-scenes.md).

### What the scripts do

- Walk of Flitting Rifts and Walk of Dancing Shadow: `EventDirector.main` loads the location title `ttl_z0000` (event
  215) on the first arrival and sets flags `0x0027` and `0x0028`, then `0x0029`: the location map's exits to Golmore
  Jungle, the Paramina Rift and the Henne Mines.
- Walk of Stolen Truths: talking to `ロケ地図` gives the area map, Feywood, with system message 97. White Magick's
  Embrace: it gives the Feywood Candle with system message 122 ("The candle reveals hidden areas on your map of the
  [value]!").
- Antiquity's End: while the story counter is below 4160, `SAKIYOMI_mfr_a0400.init` loads scene `mfr_a0400` (event
  353). Touching `イベントレクト` shows "A dense Mist prevents you from advancing.", plays the scene and writes 4160, the
  value that marks the Mist wall open.
- Redolent Glade: `EventDirector.main` loads scenes `mfr_b0100` (event 350) and `mfr_b0101` (event 351) and shows the
  boss gauge for the Rafflesia fight; after it, it removes every foe, loads the victory pose scene `pos_z0000` (event
  427) and writes 4200.
- Ice Field of Clearsight and The Edge of Reason: touching each shrine (`hokora00` to `hokora04`) sets its map-icon
  flag, and talking to one gives its voiceless words: "In this sanctum shall the pilgrim find truth and illusion both.
  Illusion betokens the true way."
- Ice Field of Clearsight: touching `hokora03` also sets flag `0x015D`, which draws the location map's link to The
  Edge of Reason.
- The Edge of Reason: the Gigas gate (`gil_gate.talk`) offers "Read the inscription.", "Touch the gate." and "Do
  nothing." Reading shows "Gigas summoner, gate's power is yours to claim. Beyond the One gate lies sacred Giruvegan.
  Over the One gate the Gigas holds sway." once `hokora04` has been touched (bit `0x80` of `mp_gil_flg00`), and
  "Illusion lights true path's way. Stray not and the One gate shall ye reach." before.
- Touching the gate before `hokora04` shows "The elements have battered this gate over long years. It will not
  open." After it, below story counter 4250, with Belias (`getsummonid()` gives 27) it sets flag `0x010D`, the
  location map's exits to Giruvegan, and requests `イベント管理.ベリアス開門_再生`; without Belias it shows "Strong magicks bind the gate. It
  will not open." At 4250 or above it requests `MAP_SECOND_DIRECTOR.再来訪イベント開始`.
- The Edge of Reason: `イベント管理.ベリアス開門_再生` plays scene `mfr_c0300` (event 352), writes
  4230 and jumps to Gate of Earth (Giruvegan), field 686. `常駐監督.main` sets flag `0x002A`, the exits to Giruvegan as
  well.
- Walk of Dancing Shadow: `hunt_kansi.main` gives the Feathered Trophy. In Redolent Glade and The Edge of Reason,
  `wanted_kansi.main` removes the foes of a group.
- On chocobo, two exits of Walk of Flitting Rifts turn the bird back ("The chocobo refuses to go any further.").
- Walk of Flitting Rifts, Walk of Stolen Truths, Walk of Dancing Shadow, Antiquity's End, Redolent Glade, White
  Magick's Embrace, Ice Field of Clearsight and The Edge of Reason hold 11, 10, 11, 1, 2, 9, 12 and 11 treasure
  chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settreasureflag`, `releasetreasureflag`, `istreasureflag` | `0x3F1`, `0x3F2`, `0x3F5` | `0x00352EA0`, `0x00353390`, `0x00354000` | `flags_*` | `Bank512, second half` flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in the scripts of this table that write
or test it: every assignment to it is a write and every comparison a test ([story counter
values](story-counter-values.md)).

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
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank512, second half` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [feywood-script-list.tsv](feywood-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Feywood scenes](feywood-scenes.md) - the four scenes these scripts own.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Golmore Jungle scripts](golmore-jungle-scripts.md) and [Paramina Rift scripts](paramina-rift-scripts.md) - the regions beyond the exits.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
