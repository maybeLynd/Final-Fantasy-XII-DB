---
title: "Dalmasca Estersand scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of Dalmasca Estersand that does something a player can observe. It
covers the eleven zone scripts, the four scene scripts of the region that have an event id and the developer script
`dst_z9900`, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `dst_a01` | zone | The Stepping, field `227` | 32 | 62 | 16 | 1 |
| `dst_a02` | zone | Yardang Labyrinth, field `228` | 35 | 65 | 17 | 1 |
| `dst_a03` | zone | Sand-swept Naze, field `229` | 28 | 44 | 14 | 0 |
| `dst_a04` | zone | Banks of the Nebra, field `230` | 32 | 64 | 17 | 0 |
| `dst_a05` | zone | Passage Entrance, field `231` | 28 | 134 | 15 | 5 |
| `dst_a06` | zone | Murmuring Defile, field `232` | 18 | 77 | 5 | 0 |
| `dst_a07` | zone | Outpost, field `233` | 42 | 213 | 16 | 0 |
| `dst_b01` | zone | South Bank Village, field `129` | 52 | 390 | 23 | 5 |
| `dst_b02` | zone | North Bank Village, field `130` | 34 | 410 | 33 | 1 |
| `dst_c01` | zone | The Yoma, field `132` | 34 | 55 | 19 | 0 |
| `dst_c02` | zone | Broken Sands, field `133` | 39 | 103 | 21 | 0 |
| `dst_a0180` | scene | event `122` | 6 | 26 | 0 | 0 |
| `dst_a0181` | scene | event `724` | 12 | 73 | 16 | 0 |
| `dst_a0580` | scene | event `710` | 10 | 72 | 4 | 0 |
| `dst_b0100` | scene | event `121` | 21 | 148 | 17 | 0 |
| `dst_z9900` | developer | developer script, named by no path array | 0 | 0 | 0 | 0 |

Passage Entrance and South Bank Village carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; The Stepping, Yardang Labyrinth and North Bank Village carry the key-item and message helper
alone. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no
rows here; the Shared helpers column counts them.

The scenes `dst_a0181` and `dst_b0100` hold their own helper
`イベント特殊効果画面_EV`, which is not one of the five, so its functions have rows.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Dalmasca
Estersand scenes](dalmasca-estersand-scenes.md).

### What the scripts do

- The Stepping: on entry while the story counter is 68, `常駐監督.init` loads scene `dst_a0180` or `dst_a0181`.
- The Stepping: while the script global `g_com_mnp_東ダルマスカ砂漠ロケタイ` is 0, `常駐監督.main` plays scene `ttl_z0003` (event
  430) and sets flag `0x001B`, which opens the location map's exits between Dalmasca Estersand and Rabanastre.
  `トマト監視監督.トマト監視` watches the Rogue Tomato (`NM_はぐれトマト`): it removes the foes of a group, loads scene
  `dst_a0181` and writes 70, 75 and 78.
- Yardang Labyrinth: `常駐監督.main` sets flags `0x0020` and `0x0021`, the location map's exits to Nalbina Town and
  to Giza Plains. Its exit to Gizas South Bank jumps to field `249` or field `266`. `花サボ監督.main` removes the foes
  of a group and gives the Cactus Flower.
- Banks of the Nebra, The Stepping, Sand-swept Naze, Yardang Labyrinth, The Yoma, Broken Sands and the Outpost hold
  10, 10, 11, 9, 14, 13 and 4 treasure chests. Semclam Shells are picked up at three spots on the Banks of the Nebra
  and two in South Bank Village; Valeblossom Dew at three spots in Broken Sands; Nebralim at two in the Outpost.
- Passage Entrance: `配置監督.main` loads scene `dst_a0580` and writes 343, the arrival in Dalmasca Estersand after
  the escape from Nalbina Fortress. Shifty Seeq tells of the caved-in entrance to Barheim and turns the party away. Talking to
  `system_anchor_actor` requests `ym_shutoraljump.shtjump`, which loads scene `str_z0000` (event 211) and jumps to
  the field a script variable holds.
- Murmuring Defile: `監督.main` sets flag `0x0022`, the location map's exits to Barheim Passage. Below story counter
  1,540 the door `door_01` is "securely locked"; from 1,540 it asks for the Barheim key, and with the key it shows
  "You use the Barheim key.", sets flag `0x013E` and jumps to The Zeviah Subterrane (Barheim Passage), field `62`,
  entrance 3.
- Outpost: Dantro keeps watch, and touching `集落通行禁止レクト` shows "No one's allowed through 'less they're on
  official business." Five chocobo spots (`チョコへそＦＳ０１` to `０５`) give 1, 3 or 5 gil.
- South Bank Village: the merged villager actor `NPC01` speaks for Tchigri, Dantro's wife, Ada, Ruksel and others.
  Its `talk` takes fish and pickups for gil and items, sells the Dalmasca Estersand map, sets the name flag of
  Sassan, and loads the boat scene
  `dst_b0100` and then jumps to North Bank Village, field `130`, entrance 4.
- South Bank Village also holds the recovering treasure hunter (`ボス.talk`), who gives the Barheim Key, a Balance
  Mote, Magick Gloves and a Golden Amulet, an escaped prisoner from Nalbina (No. 381), and a chocobo spot that gives gil or a Teleport
  Stone.
- North Bank Village: `配置監督.main` shows "They must've attacked the north bank!" and jumps to The Yoma. Touching
  `サボ再会イベントレクト` sets flag `0x0137`, and `クエサボ息子.子サボラスト移動` gives 1000 gil and a Wyrmfire Shot.
  The cockatrice Sassan gives a Koga Blade, and `NPC01.talk` sells the Mosphoran Highwaste map, loads
  `dst_b0100` and jumps back to South Bank Village.
- The Yoma and Broken Sands: `常駐監督.main` sets flags `0x0023` and `0x0024`, the location map's exits to Dalmasca
  Westersand and to Mosphoran Highwaste. In Broken Sands `hunt_kansi.main` gives the Hide-covered Trophy and removes
  the foes of a group.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | the second argument is a section 2 text id; the choices are in that text |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember`, `removepartymember`, `addguestbattlemember`, `removeguestbattlemember` | `0x353`, `0x355`, `0x354`, `0x35B`, `0x35C` | `0x0034C030`, `0x0034D4E0`, `0x0034C030`, `0x00352190`, `0x00352AF0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

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

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
  (`0x002ADDAA`, `0x002B16D4`, `0x002B52EF`): the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes (`0x0026668B`, `0x0026669B`-`0x002666B4`), so its `{actor-name}` header shows no name; that line reads
  `no name shown`. A system message reads `system message`.
- A line whose text carries no name takes the window actor's `setnpcname` name. Failing that, a scene subtitle
  (centred, or in the subtitle font `{alt-font}`) takes the character the window speaks for.
- Then any line without a name takes the speaker of the voice cue joined to it ([Voices](../Sound-And-Music/voices.md)),
  else the actor of the row's `TAGmes_<actor>_<n>` function, else the actor whose mouth function (`paku_on`,
  `unapaku_on`, `クチウナオン`, `kutipaku_on`, `kutipakuON`) is requested in its window or around the request of its
  function.
- A character's game name is the second name its `setnpcname` gives; else the party member whose model its bind verbs
  name, the `c` entries of the script's [actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) read
  against the `model` column of the [party table](../Party/party-table.md), a main member before a guest; else
  the NPC name or string table row whose `in` cell is the actor's name.
- Any other line without a name reads `no name shown`, apart from a scene subtitle, which keeps its row's cell `-`. A
  line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- `NPC02` in `dst_a05` is copy 1 of `NPC01` (`symlink NPC02(NPC01) : 1`), and only `NPC02` is asked to run
  `通行禁止イベント左１`, `通行禁止イベント左２` and `通行禁止イベント２左１`, the left-hand Seeq of the scene that bars the way to Barheim. Copy 1
  calls no `setnpcname`, so these three rows read the name their lines show, Bumbling Seeq, not `NPC01`'s Shifty Seeq.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`dalmasca-estersand-script-steps.tsv`](dalmasca-estersand-script-steps.tsv) has one row for each step
of every function of the fifteen scripts, in the order the function runs them: each call, request, store, branch,
loop, case and return. It has 46,500 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `dst_a01` | 1,063 | `dst_b01` | 16,680 |
| `dst_a02` | 878 | `dst_b02` | 6,667 |
| `dst_a03` | 403 | `dst_c01` | 864 |
| `dst_a04` | 666 | `dst_c02` | 1,289 |
| `dst_a05` | 1,250 | `dst_a0180` | 201 |
| `dst_a06` | 1,112 | `dst_a0181` | 762 |
| `dst_a07` | 3,456 | `dst_a0580` | 628 |
| | | `dst_b0100` | 10,581 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Dalmasca Estersand has 88 such rows.

Some actors run another actor's code: `NPC02` in `dst_a05` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 48 of these rows: 1
in `dst_a05`, 13 in `dst_a07`, 15 in `dst_b01` and 19 in `dst_b02`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 46,067 |
| empty | 424 |
| `does not ship`, with the fact | 9 |

The nine `does not ship` rows are `motionread` calls: five in `dst_a06`, whose motion file `dst_a06.mot` is not in the
archive, and four that read entry 1 of `dst_a07.mot` (three) or of `dst_b02.mot` (one), an empty entry.

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for
the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `dst_a0180` (event `122`), `監督.main` files
`乗っ取り00.cut01_ready` and `イベントトマト.cut01_ready`, and waits for both. It then starts the camera actor's `cut01` and the
tomato's `cut01_go` together, starts camera shot `dst_a01_e01`, fades the music to volume 80 over 180 frames and fades
the screen in over 15 frames.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
| `lines` | the section 2 entries the function passes to the message and ask verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join or leave, guests who join or leave, and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [`dalmasca-estersand-script-list.tsv`](dalmasca-estersand-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone`, `scene` or `developer`, and its map (region) and field id, its event id, or `developer script, named by no path array` |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`dalmasca-estersand-script-steps.tsv`](dalmasca-estersand-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test` |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

The shared steps table [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv) has the same columns from `at`
on, after these:

| Column | Meaning |
|---|---|
| `template` | the template id that the `shared template` rows name |
| `actor`, `function`, `step` | the shared actor, its function and the step number |
| `reference` | the script whose copy of the function the steps were read from, and where the function starts there |

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids, section
3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other scripts' copies
differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Dalmasca Estersand scenes](dalmasca-estersand-scenes.md) - the four scenes these scripts load.
- [Dalmasca Westersand scripts](dalmasca-westersand-scripts.md) - the region beyond The Yoma.
- [Giza Plains scripts](giza-plains-scripts.md) - the region beyond Yardang Labyrinth.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
