---
title: "Salikawood scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [salikawood-scripts.tsv](salikawood-scripts.tsv) has one row per script function of The Salikawood that does
something a player can observe. It covers the eleven zone scripts and the two scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `frs_a01` | zone | The Omen-Spur, field `151` | 18 | 36 | 10 | 0 |
| `frs_a02` | zone | Trunkwall Road, field `152` | 33 | 93 | 21 | 1 |
| `frs_a03` | zone | Diverging Way, field `153` | 30 | 58 | 21 | 0 |
| `frs_a04` | zone | Sun-dappled Path, field `154` | 25 | 45 | 13 | 0 |
| `frs_a05` | zone | Garden of Decay, field `155` | 27 | 87 | 19 | 1 |
| `frs_a06` | zone | Path of Hours, field `156` | 23 | 99 | 13 | 5 |
| `frs_b01` | zone | Quietened Trace, field `157` | 27 | 85 | 15 | 5 |
| `frs_b02` | zone | Grand Bower, field `158` | 23 | 47 | 14 | 0 |
| `frs_c01` | zone | Corridor of Ages, field `162` | 30 | 56 | 19 | 0 |
| `frs_c02` | zone | Piebald Path, field `163` | 34 | 83 | 18 | 1 |
| `frs_d01` | zone | Living Chasm, field `908` | 16 | 52 | 10 | 0 |
| `frs_b0200` | scene | event `200` | 21 | 87 | 0 | 0 |
| `frs_b0201` | scene | event `201` | 21 | 85 | 0 | 0 |

Path of Hours and Quietened Trace carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`; Trunkwall Road, Garden of Decay and Piebald Path carry the key-item and message helper alone. Their
functions are described once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the
Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Salikawood
scenes](salikawood-scenes.md).

### What the scripts do

- The Omen-Spur: `DIRECTOR.main` loads the location title `ttl_z0002` (event 217) on the first arrival from the
  Mosphoran Highwaste and sets flag `0x0026`, the location map's exits between the Mosphoran Highwaste and The
  Salikawood.
- Trunkwall Road: talking to `サリカ樹林地図` gives the area map, Salikawood, with system message 93 ("Your location map for
  this area is complete!").
- Living Chasm holds the gate to the Phon Coast. Below story counter 3050 the Moogle Boss (`親方`) explains it ("As I'm
  certain you can see, this gate's under repairs, kupo.").
- Living Chasm: from story counter 3050 the Moogle Boss sends the party after his nine apprentices ("...That is, if my
  [value] missing apprentices ever come back from the Salikawood!"): the first talk sets the count to 9, sets the four
  bungalow map icon flags (`0x00BB`, `0x00BC`, `0x00BD`, `0x00BE`) and shows the count gauge in the Salikawood's
  fields.
- The bungalows: Trunkwall Road (`0x00BE`), Garden of Decay (two, `0x00BB` and `0x00BC`) and Path of Hours (`0x00BD`)
  each have a door (`廃屋入口`). From story counter 3050, talking to it lets the party meet the moogles inside ("Ooh? A
  visitor, kupo? We're here working on the gate up ahead.").
- The bungalows: once the round-up runs, the first talk at a bungalow's door releases its map icon flag and the
  moogles leave, two from each bungalow and three from Path of Hours ("Bye-bye, kupo! Oh, there're still [value] of us
  on break out there!").
- The bungalows: with the last of the moogles come system message 140 ("You found all of the moogles!") and "Come with
  us to the gate, kupo?"; Yes jumps to Living Chasm. Below 3050, from 3070, and once a bungalow is emptied, the door
  shows the Forest Bungalow notice that no one is home.
- Living Chasm: when all nine are back, arriving there or talking to the Moogle Boss plays the gate's opening ("Now
  that my apprentices are all back, the repairs took no time at all, kupo!") and writes story counter 3070. His next
  talk gives a reward package with a Sash ("Thanks to you, the repairs to the gate are finished, kupo. Here, a token
  of our gratitude!").
- Living Chasm: arriving from the Phon Coast sets flag `0x0033`, the location map's exits between the Phon Coast and
  The Salikawood.
- Path of Hours: the Forest Traveler (`旅人`) waits for the gate ("Trouble is, the gate's broken."). From story counter
  3070 he speaks by the progress of quest 146: at 30 of the flickering light to the northwest ("If you go through the
  wood in that direction now, you'll see an eerily flickering light."), at 50 "Turns out it was a creature called the
  Braegh!".
- Path of Hours: from story counter 3070, at any other progress of quest 146, the Forest Traveler says "What's this?
  The repairs to the gate are finished? Then I'm off to the Phon Coast...once I find my map."
- Quietened Trace: the Overseer of the Craftsmoogles' League (`マネージャー`) is lost ("I'm top overseer of the
  Craftsmoogles' League, kupo."). Until the Grand Bower fight is won (`g_btl_ボムキング` 2) he warns of bombs ("That
  reminds me, there're bombs on the road ahead! Better stay back, kupo!").
- Quietened Trace: from story counter 3070, at quest 146 progress 30 and 50, the Overseer says "Up ahead, in the
  northwest of the Salikawood, I was chased by a flickering monster!" and "Did you kill that flickering monster? Not
  bad, kupo!".
- Sun-dappled Path: while `g_btl_nm_キャロット` is 1, `監督.main` shows one of four lines of Krjn (`THIRD_カロリーヌ`), chosen by
  a script variable and by whether she has spoken before ("Krjn You have come. And with no unwelcome violence done
  along the way. Good. The mark we hunt is near. Now we fight.").
- Sun-dappled Path: when the fight ends, `wanted_kansi.main` sets the variable to 2; when `sysIsdead2_49f` of Krjn
  returns 1 it shows her farewell ("Your skill is much greater than I would have thought.") and removes her and the
  lesser foes; it then writes 30 to the progress of quest 166 and removes every foe.
- On chocobo, the exit of Quietened Trace to Grand Bower turns the bird back ("The chocobo is nervous and refuses to
  go further. Something ahead must be frightening it."), and so does the exit of Corridor of Ages to Hall of Effulgent
  Light (Necrohol of Nabudis) ("The chocobo refuses to go any further.").
- Grand Bower: while `g_btl_ボムキング` is 1, `監督.main` loads scenes `frs_b0200` (event 200) and `frs_b0201` (event 201)
  the first time, `frs_b0201` alone after that, and shows the boss gauge; when the fight ends it removes every foe,
  sets `g_btl_ボムキング` to 2 and loads the victory pose scene `pos_z0000` (event 427, [Victory pose
  scenes](victory-pose-scenes.md)).
- Corridor of Ages and Piebald Path: arriving from the Necrohol of Nabudis and from the Nabreus Deadlands sets flags
  `0x0035` and `0x0034`, the location map's exits to those regions. In Corridor of Ages, once `g_btl_nm_ブライ` is 1,
  `wanted_kansi.main` removes the foes of a group. In Piebald Path, `hunt_kansi.main` gives the Sickle Trophy and
  removes the foes of a group.
- Piebald Path: while the party holds the Green Bottle, a glow appears in the undergrowth ("Faint Glow The light
  coming from the undergrowth resonates with the green bottle you hold..."); Yes to "Hold the bottle nearer to the
  light?" shatters it ("Without warning, the green bottle shatters!"), gives a reward package with a Hastega Mote,
  takes the Green Bottle and gives the Green-hued Message.
- Piebald Path: the same script holds the blue, red and black bottle glows, which it places only in fields 171, 1151
  and 850.
- The Omen-Spur, Trunkwall Road, Diverging Way, Sun-dappled Path, Garden of Decay, Quietened Trace, Grand Bower,
  Corridor of Ages and Piebald Path hold 2, 8, 12, 4, 6, 4, 4, 7 and 3 treasure chests.

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

The steps table [`salikawood-script-steps.tsv`](salikawood-script-steps.tsv) has one row for each step of every
function of the thirteen scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 10,667 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `frs_a01` | 305 | `frs_b01` | 660 |
| `frs_a02` | 1,155 | `frs_b02` | 787 |
| `frs_a03` | 563 | `frs_c01` | 590 |
| `frs_a04` | 472 | `frs_c02` | 931 |
| `frs_a05` | 1,605 | `frs_d01` | 1,398 |
| `frs_a06` | 995 | `frs_b0200` | 597 |
| | | `frs_b0201` | 609 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Salikawood has 88 such rows.

Some actors run another actor's code: `NPC02` in `frs_a02` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 14 of these rows: 1
in `frs_a02`, 3 in `frs_a05`, 2 in `frs_a06` and 8 in `frs_d01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 10,632 |
| empty | 33 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls that read entry 1 of `frs_d01.mot`, an empty entry. A row whose
`resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the script writes
them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give for the step,
and `-` otherwise.

A scene reads from top to bottom in its director's function. In `frs_b0200` (event `200`), `DIRECTOR.main` files
`AD.準備_ad`, reads motion 1 of `frs_b0200.mot`, waits for both and waits while `scratch1_var_1` is 0. It reads event
sound slots 0 and 1 of `frs_b0200.snd`, waiting for each. It files `AD.カット１_ad` to `AD.カット４_ad` and `AD.終了_ad` one
after another, waiting until each ends, frees both sound slots, waits until `BGM.カット４` ends and disposes of event
manager slot 0.

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

The script list [salikawood-script-list.tsv](salikawood-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`salikawood-script-steps.tsv`](salikawood-script-steps.tsv) has one row per step:

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
- [Salikawood scenes](salikawood-scenes.md) - the two scenes these scripts own.
- [Location title scenes](titles-scenes.md) - the location titles fields load on the first arrival.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Mosphoran Highwaste scripts](mosphoran-highwaste-scripts.md), [Phon Coast scripts](phon-coast-scripts.md), [Nabreus Deadlands scripts](nabreus-deadlands-scripts.md) and [Necrohol of Nabudis scripts](necrohol-of-nabudis-scripts.md) - the regions beyond the exits.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
