---
title: "Old Archades scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x003459C0, 0x00355830, 0x00377B60, 0x003778B0, 0x0034ADA0, 0x0034B760, 0x0034BB10"
---

## What it lists

The table [old-archades-scripts.tsv](old-archades-scripts.tsv) has one row per script function of Old Archades that
does something a player can observe. It covers the two zone scripts and the three scene scripts of the area, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `ald_a01` | zone | Alley of Muted Sighs, field `762` | 49 | 234 | 39 | 5 |
| `ald_a02` | zone | Alley of Low Whispers, field `763` | 38 | 166 | 47 | 1 |
| `ald_a0179` | scene | event `728` | 16 | 134 | 8 | 0 |
| `ald_a0180` | scene | event `727` | 13 | 145 | 13 | 0 |
| `ald_a0200` | scene | event `173` | 26 | 200 | 5 | 0 |

The Alley of Muted Sighs carries the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`. The Alley of Low Whispers carries only `イベント特殊効果画面`. Their functions are described
once on [Shared zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column
counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map or loads a scene.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Old
Archades scenes](old-archades-scenes.md).

### What the scripts do

- Alley of Low Whispers: `EventDirector.main` sets flag `0x002C`, which opens the location map's exits between Old
  Archades and Sochen Cave Palace, then loads and plays scene `ald_a0200` and writes 3210. The exit `__MJ_CTRL002`
  leads to the Skybent Chamber (Sochen Cave Palace), field `188`.
- Alley of Muted Sighs: the scene actors `SAKIYOMI_ev_ald_a0180【初登場】` and `SAKIYOMI_ev_ald_a0179【帝都へ】`
  load scenes `ald_a0180` and `ald_a0179`; the second is requested by Jules (`NPC_JULES.talk`) and the Imperial at
  the gate (`NPC_SOLDIER_A.talk`).
- Alley of Muted Sighs: while the story counter is below 3220, Jules's `talk` writes 3220, sets flag `0x0076` and
  jumps to Trant (Archades), field `641`, entrance 5.
- Alley of Muted Sighs: the Imperial at the gate turns the party away ("We can't just throw open our gates to you
  vulgars") and sets the name-tag flag Bank2048 `0x0417`, after which Jules's tag reads "Jules" instead of
  "Streetear".
- Alley of Low Whispers: five talk functions of `NPC01` set ten Bank2048 name-tag flags. Tags that read
  "Archadian Vulgar" then read "Braggart", "Defiant Lad", "Proud Brother", "Leaving Man", "Waiting Woman", "Dreaming
  Man", "Sensible Man", "Distinguished Elder" or "Granddaughter", and one that read "Archadian Ardent" reads "Weary
  Brother".
- Alley of Low Whispers: the Moogles Eight sing (`MOG_DANCE.talk`). While the story counter is below 3220 they sing
  of the seeq who promised them a gourmet tour or, when the global variable `global_var_3` is 3, that they are to be
  sold ("Now we hear we're to be sold!"); from 3220 on they sing "A band of moogles eight are we..." or, when
  `global_var_3` is 3, their thanks ("Our thanks, good sire, for now we're free!").
- Nine treasure chests stand in the Alley of Muted Sighs and eleven in the Alley of Low Whispers (`treasure_00` to
  `treasure_10`, `talktreasure`).
- The Alley of Muted Sighs holds a crystal; what touching it does, the teleport and its Teleport Stone are on
  [Shared zone-script actors](shared-zone-script-actors.md).

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `aask`, `aaske`, `aask_1ff` | `0x010`, `0x14A`, `0x1FF` | `0x0034B760`, `0x0034BB10`, `0x0034ADA0` | `lines` | a question and its choices: the second argument is a section 2 text id (`0x0034B760` and `0x0034BB10` jump to `0x0034ADA0`) |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname` | `0x399` | `0x0034DFA0` | `flags_set` | Bank2048 flag, the name-tag flags ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem_47f`, `additemmes`, `subitem` | `0x47F`, `0x480`, `0x2F2` | `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `talktreasure` | `0x2BF` | `0x00355830` | `items` | a treasure chest |

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
  second name while that flag is set. An actor whose `setnpcname` calls name several pairs lists each second name,
  separated by `; `.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`old-archades-script-steps.tsv`](old-archades-script-steps.tsv) has one row for each step of every
function of the five scripts, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 14,180 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `ald_a01` | 5,117 | `ald_a0179` | 732 |
| `ald_a02` | 5,816 | `ald_a0180` | 942 |
| | | `ald_a0200` | 1,573 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Old Archades has 39 such rows.

Some actors run another actor's code: `NPC02` in `ald_a01` starts at the same place as `NPC01` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 45 of these rows: 21
in `ald_a01` and 24 in `ald_a02`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 14,108 |
| empty | 72 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that holds the standard motion `stdmotionplay` plays, or the variable that
receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `ald_a0180` (event `727`), `プロデューサー.main` reads its
eight models (`0x03000000` to `0x03000007`) and motion 1 of `ald_a0180.mot`, and waits while `scratch1_var_1` is 0. It
then switches on `scratch1_var_2`: at 0 it files `監督.ジュール登場1`, `BGM.end` and `PC_00.乗っ取り解除`, at 1 and 2 `監督`'s
`ジュール登場2_00` and `ジュール登場2` or `ジュール登場3_00` and `ジュール登場3` and then `PC_00.乗っ取り解除`, waiting until each ends. It goes
back to the wait while `scratch1_var_5` is not 9, then frees the motion and disposes of event manager slot 0.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for a row with lines, the names `setnpcname` gives the actor |
| `lines` | the section 2 entries the function passes to the message verbs and the ask verbs; `system message N` for a message the function hands to the shared item and message helper, `N or M` when it is chosen at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / ` |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a Bank2048 flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; for an item the function hands to the shared item and message helper, the item it stores for it first, `A or B (which one is decided at run time)` when it is chosen at run time |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [old-archades-script-list.tsv](old-archades-script-list.tsv) holds the first table above, one row
per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`old-archades-script-steps.tsv`](old-archades-script-steps.tsv) has one row per step:

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

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message helpers, described once.
- [Old Archades scenes](old-archades-scenes.md) - the three scenes these scripts load.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens, the name-tag flags among them.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
