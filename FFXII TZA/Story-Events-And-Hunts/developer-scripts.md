---
title: "Developer scripts: the debug menus and test scenes no path array names"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032FCA0, 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10, 0x00352190, 0x00352AF0"
---

## What it lists

The table [developer-scripts.tsv](developer-scripts.tsv) has one row per script function of the developer scripts
that does something a player can observe. It covers the eighteen scripts under `event/evt_t` of `plan_master/us`. The
nineteenth folder there, `evt_t0020`, holds an `.ebp` with no `EBP2` header and no code
([story counter values](story-counter-values.md)).

No path array names these scripts: the [asset path table](../Game-Files-And-Data-Tables/asset-paths.md) has no
entry for any of them. An event id `n` names the scene script at index `4n` of the event file table, so none of them
has an event id. Their `place` cell reads `developer script, named by no path array`, and their kind in the script
list is `developer`.

| Script | Actors | Functions | Rows |
|---|---:|---:|---:|
| `evt_t0005` | 51 | 163 | 1 |
| `evt_t0009` | 1 | 2 | 1 |
| `evt_t0015` | 5 | 20 | 13 |
| `evt_t0016` | 1 | 2 | 1 |
| `evt_t0023` | 3 | 7 | 1 |
| `evt_t0080` | 1 | 2 | 1 |
| `evt_t0081` | 8 | 68 | 1 |
| `evt_t0082` | 18 | 116 | 7 |
| `evt_t0083` | 16 | 213 | 4 |
| `evt_t0084` | 7 | 233 | 4 |
| `evt_t0085` | 21 | 219 | 6 |
| `evt_t0086` | 11 | 95 | 3 |
| `evt_t0090` | 3 | 11 | 6 |
| `evt_t0094` | 2 | 3 | 1 |
| `evt_t0096` | 1 | 3 | 1 |
| `evt_t0500` | 1 | 2 | 1 |
| `evt_t0505` | 10 | 29 | 4 |
| `evt_t0509` | 5 | 13 | 1 |

No script of the group carries a shared helper actor, so the `shared_actors` cell is 0 on every row.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes table
[developer-scenes.tsv](developer-scenes.tsv) has one row per script, with its section 2 entries and their text.

### What the scripts do

- Most of them are debug menus, by their actors' names:
  - `Map_Debug_menu_mtanaka` (`evt_t0080`, `evt_t0081`, `evt_t0086`);
  - `Map_Debug_menu_t_hirose` (`evt_t0082`, `evt_t0084`);
  - `Map_Debug_menu_naomif` (`evt_t0083`) and `Map_Debug_menu_s_ohzono` (`evt_t0085`);
  - `デバッグ監督` (`evt_t0090`);
  - `トライアルデバッグメニュー` (`evt_t0094`, a Trial Mode debug menu);
  - `イベントデバッグメニュー` (`evt_t0500`).
- `evt_t0096`, `evt_t0505` and `evt_t0509` show menus too, by their section 2 entries: `MoB menu`, the party
  question `パーティー構成は？` and `Map Jump(Set Location ID)`.
- A menu asks its question with `aask` (`evt_t0083` and `evt_t0090` also with `aaske`, and `evt_t0083` with
  `aask_1ff`) and acts on the answer. Of the table's 57 rows, 18 jump to a field, 10 write the
  story counter, 21 give or take items and 7 change the party. The counter writes are in the nine scripts
  that [story counter values](story-counter-values.md) counts as developer menus.
- Three scripts load scenes by a literal event id: `evt_t0016` (12 scenes), `evt_t0090` (10) and `evt_t0500`
  (19).
- `evt_t0005` has 51 actors. Its motion calls name entries 1 and 2 of `evt_t0005.mot`, the motion file in its own
  folder; both entries are empty (see [Every step](#every-step)).
- `evt_t0015` carries `イベント特殊効果画面_EV`, whose functions give the item held in a variable and show system
  messages. It is not the shared helper `イベント特殊効果画面`, so its functions have rows.
- `evt_t0009` sets the body radius of the four party slots from the answer to its question (the example under
  [Every step](#every-step)).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | a question and its choices: the second argument is a section 2 text id (`0x0034B760` and `0x0034BB10` jump to `0x0034ADA0`) |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |
| `removepartymember`, `addguestbattlemember`, `removeguestbattlemember` | `0x354`, `0x35B`, `0x35C` | `0x0034C030`, `0x00352190`, `0x00352AF0` | `party` | party row selectors: a member leaves, a guest joins, a guest leaves ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

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

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. No listed
  function of these scripts has one, so the `speaker` cell is `-` on every row.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`developer-script-steps.tsv`](developer-script-steps.tsv) has one row for each step of every function
of the eighteen scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 78,071 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `evt_t0005` | 1,340 | `evt_t0084` | 9,529 |
| `evt_t0009` | 52 | `evt_t0085` | 7,718 |
| `evt_t0015` | 248 | `evt_t0086` | 11,231 |
| `evt_t0016` | 142 | `evt_t0090` | 5,823 |
| `evt_t0023` | 65 | `evt_t0094` | 308 |
| `evt_t0080` | 289 | `evt_t0096` | 2,742 |
| `evt_t0081` | 10,615 | `evt_t0500` | 952 |
| `evt_t0082` | 6,018 | `evt_t0505` | 9,760 |
| `evt_t0083` | 9,893 | `evt_t0509` | 1,346 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv).
None of these scripts carries one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 76,279 |
| `does not ship` | 63 |
| empty | 1,729 |

A script that no path array names has no motion or sound entry there. For these scripts the steps read the `.mot` and
`.snd` in the script's own folder, when one ships there, and the `resolution` cell says so. Only `evt_t0005` and
`evt_t0015` ship a `.mot`, no developer script ships a `.snd`, and only `evt_t0005`'s steps name its file.

The 63 `does not ship` rows are all in `evt_t0005`: its `motionread` and `motionplay_bb` calls name entries 1 and
2 of `evt_t0005.mot`, and both entries of the file are empty, so the calls play nothing.

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A menu reads from top to bottom in its main function. In `evt_t0009`, `Map_Director.main` sets the area map to not
jammed (`setnavimapjamming(0)`), closes message windows 0 to 7, waits 2 frames and asks a question in window 6. The
answers 1 to 4 store 40, 45, 50 or 55 in `file_var_s0_1`. For any answer it then takes party slots 0 to 3 in turn
(`capturepc`), sets each one's body radius to that value divided by 100 (`setradius`), waits a frame and releases
it (`releasepc_404`). It then waits a frame and ends the event (`eventdispose`).

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | `developer script, named by no path array` on every row |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `main`), or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | `-` on every row: no listed function's actor has a name pair |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_tested` | `-` on every row: no listed function sets or tests a story flag |
| `flags_released` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md) |
| `counter_set`, `counter_tested` | the story counter values written and tested, each written value with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `items` | items the function gives or takes, by name; a fixed count is written `xN`, a count the game computes reads `, as many as <expression> gives`, and an item the script holds in a variable is named by the variable |
| `jumps` | the field and entrance of each `mapjump`, the field as map name (region) and field id; a field the script holds in a variable or computes is named by the expression |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join or leave, as guests too, and the fighting party the function sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` on every row: no listed function belongs to a shared helper actor |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [developer-script-list.tsv](developer-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `developer`, and `developer script, named by no path array` |
| `actors`, `functions` | the script's actors and functions |
| `rows` | the script's rows in the main table |
| `shared_actors` | 0 on every row: no script carries a shared helper actor |

The scenes table [developer-scenes.tsv](developer-scenes.tsv) has one row per script:

| Column | Meaning |
|---|---|
| `scene` | the script, by its file name |
| `event_id`, `loaded_by`, `next` | `-` on every row: no script has an event id |
| `lines` | the number of entries in the script's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)` |
| `items`, `party`, `flags_set`, `counter_set` | what the script's own functions give or take, change in the party, set and write, as in the main table |

The steps table [`developer-script-steps.tsv`](developer-script-steps.tsv) has one row per step:

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
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its control codes dropped; `-` for every other step |
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

- [Story counter values](story-counter-values.md) - the counter values these menus write, and the developers' names
  for them from the `evt_t0505` scenario menu.
- [Script censuses](script-censuses.md) - the developer scripts in the counts of every us script.
- [Script language differences](script-language-differences.md) - the calls the `kr`, `cn` and `ch` copies of these
  scripts add.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
