---
title: "Phon Coast scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [phon-coast-scripts.tsv](phon-coast-scripts.tsv) has one row per script function of the Phon Coast that does
something a player can observe. It covers the twelve zone scripts and the two scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `fon_a01` | zone | The Reseta Strand, field `478` | 26 | 41 | 13 | 0 |
| `fon_a02` | zone | Pora-Pora Sands, field `479` | 32 | 63 | 19 | 0 |
| `fon_a03` | zone | The Mauleia Strand, field `480` | 28 | 44 | 13 | 0 |
| `fon_a04` | zone | Cape Uahuk, field `481` | 26 | 41 | 13 | 0 |
| `fon_a05` | zone | Cape Tialan, field `482` | 27 | 43 | 13 | 0 |
| `fon_a06` | zone | Kaukula Pass, field `483` | 21 | 68 | 7 | 5 |
| `fon_a07` | zone | The Hakawea Shore, field `484` | 32 | 62 | 17 | 0 |
| `fon_b01` | zone | Hunters' Camp, field `488` | 89 | 570 | 51 | 5 |
| `fon_c01` | zone | Caima Hills, field `491` | 31 | 61 | 18 | 0 |
| `fon_c02` | zone | The Vaddu Strand, field `492` | 36 | 60 | 21 | 0 |
| `fon_c03` | zone | Limatra Hills, field `493` | 28 | 44 | 13 | 0 |
| `fon_c04` | zone | Rava's Pass, field `494` | 19 | 60 | 5 | 5 |
| `fon_a0600` | scene | event `251` | 31 | 139 | 3 | 0 |
| `fon_b0100` | scene | event `250` | 22 | 244 | 28 | 0 |

Kaukula Pass, Hunters' Camp and Rava's Pass carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`. Their functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have
no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Phon Coast
scenes](phon-coast-scenes.md).

### What the scripts do

- Pora-Pora Sands: below story counter 3100 a Game Hunter (`バンガ`) and the touch area `バンガレクト` bar the way east ("Lo!
  Sorry, there. I can't let you pass. If you wish to go east, go via the village."); from 3100 his talk is replaced by
  `バンガ.talk2` ("Head on through, if you like. But you won't get anywhere if you're not on a chocobo.").
- Cape Tialan: `hunt_kansi.main` gives the Clawed Trophy and removes the foes of a group.
- Kaukula Pass: on the first arrival (`g_com_mnp_フォーン海沿岸ロケタイ` 0), `常駐ディレクター.main` loads scene `fon_a0600` (event 251),
  sets that variable to 1, shows the crystal and sets flag `0x0033`, the location map's exits between the Phon Coast
  and The Salikawood; later, arriving from Living Chasm (The Salikawood) sets `0x0033`.
- Kaukula Pass holds the crystal and the Strahl's anchor: talking to `system_anchor_actor` requests
  `ym_shutoraljump.shtjump`, which loads scene `str_z0000` (event 211) and jumps to the field a script variable holds
  ([Strahl scene](strahl-scenes.md)).
- The Hakawea Shore and Caima Hills: a Wayward Chocobo (`野良騎乗チョコボ`) asks for greens ("Feed the chocobo gysahl
  greens?"); Yes takes one Gysahl Greens and the party rides. Without greens it refuses ("The chocobo doesn't smell
  any greens on you and clearly wants to be left alone.").
- The exits into Hunters' Camp from Cape Uahuk, The Hakawea Shore (two), Caima Hills and The Vaddu Strand ask a rider
  to dismount ("You must dismount to proceed.", Dismount or Cancel).
- Hunters' Camp: while the story counter is at most 3070, `監督.init` loads scene `fon_b0100` (event 250) and `監督.main`
  plays it; touching one of three areas (`イベント起動01` to `03`) walks the party in, waits for the scene and writes story
  counter 3100.
- Hunters' Camp: the Cartographers' Guild moogle (`地図屋`) sells the area map, Phon Coast, with system message 99 ("Your
  location map for this area is complete!"), and gives directions ("First thing, there're five ways in and out of camp
  here.").
- Hunters' Camp: Gurdy (`ガーディ`) hires out chocobos ("Welcome to the chocobo stables. Only [value] gil should you wish
  to hire one, kupo!") and sends the rider to Caima Hills ("Toward Tchita Uplands.") or The Hakawea Shore ("Toward the
  Salikawood.").
- The Hunt Club: the Huntmaster (`バンガ16`) first turns the party away ("We're looking for sharp-taloned birds of prey,
  here, son, not spring chickens. Run along now."), later sets a test, the thalassinon on The Vaddu Strand, where
  `hunt_kansi.main` gives the Shelled Trophy; he takes it ("Welcome to the Hunt Club!").
- The Hunt Club: Atak, Blok and Stok (`バンガ05`, `バンガ13`, `バンガ15`) then take trophies for points ("Hrrm? Got a trophy,
  have you?"). When all rare game is felled, the Huntmaster requests `監督.結果発表` ("And the winner, with [value] points,
  is...").
- The Hunt Club: at the result, each brother with the top score gives a reward package, at 16 points or more a Zodiac
  Spear (Atak), a Zodiac Escutcheon (Blok) or a Ribbon (Stok), below 16 a Staff of the Magi, an Ensanguined Shield or
  a Sage's Ring.
- Hunters' Camp: a glint (`ルース鍵キラリン`) gives the Site 11 Key, and the Fallen Bhujerban (`二級男03`) knows it ("Why, yes!
  It is a key to Site 11!").
- Rava's Pass: arriving from Realm of the Elder Dream (Tchita Uplands) sets flag `0x0049`, the location map's exits
  between the Phon Coast and the Tchita Uplands.
- The Reseta Strand, Pora-Pora Sands, The Mauleia Strand, Cape Uahuk, Cape Tialan, The Hakawea Shore, Caima Hills, The
  Vaddu Strand and Limatra Hills hold 10, 10, 10, 9, 8, 12, 11, 16 and 10 treasure chests.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
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
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`phon-coast-script-steps.tsv`](phon-coast-script-steps.tsv) has one row for each step of every
function of the fourteen scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 18,950 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `fon_a01` | 472 | `fon_b01` | 8,306 |
| `fon_a02` | 694 | `fon_c01` | 852 |
| `fon_a03` | 478 | `fon_c02` | 762 |
| `fon_a04` | 554 | `fon_c03` | 474 |
| `fon_a05` | 499 | `fon_c04` | 371 |
| `fon_a06` | 694 | `fon_a0600` | 1,361 |
| `fon_a07` | 913 | `fon_b0100` | 2,520 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Phon Coast has 87 such rows.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 18,892 |
| empty | 58 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `fon_a0600` (event `251`), `ＡＤ.s01` starts scene cut 1
and starts `cut1` on sixteen actors together, among them `カメラ` and the eight `レモラ` actors. It waits 150 frames, starts
`cut1_バインドオフ２` on `バンガ01` and `バンガ02`, waits 210 frames, starts `cut1_バインドオフ` on `二級男02`, `二級女01` and `二級男01`, waits
50 frames and starts `カメラ.cut1_2`. After 40 frames it files `cut1_バインド` on the six party actors and waits for all six.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown` or `system message`; `-` for a row without a section 2 line, and for a scene row with a subtitle none of those rules names |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank2048` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; `the item held in` and the variable for an item a variable holds; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [phon-coast-script-list.tsv](phon-coast-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`phon-coast-script-steps.tsv`](phon-coast-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v`, a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test` |
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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Phon Coast scenes](phon-coast-scenes.md) - the two scenes these scripts own.
- [Strahl scene](strahl-scenes.md) - the private airship scene the anchor loads.
- [Salikawood scripts](salikawood-scripts.md) and [Tchita Uplands scripts](tchita-uplands-scripts.md) - the regions beyond the exits.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
