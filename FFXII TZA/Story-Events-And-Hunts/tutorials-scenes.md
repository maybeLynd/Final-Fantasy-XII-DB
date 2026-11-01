---
title: "Tutorial and staff roll scenes: the gambit, license board and map tutorials and the staff roll"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x003C9FD0, 0x0032FC30, 0x003CA140"
---

## What it lists

The table [tutorials-scenes.tsv](tutorials-scenes.tsv) has one row per scene script of the group `men` under
`plan_master/us/event`. No zone script shares their file-name prefix, so their `next` column is `-`. Every
`eventread` and `eventread_e8` call of the zone and scene scripts names its event id as a number; of the four ids,
only 429 (`men_z0005`) is named, in field 13 (`ttl_b01`). The menu scene step `0x003C9FD0` requests the other three
through `0x0032FC30` (`0x003CA07C`) after `0x003CA140` sets their event.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `men_z0001` | `437` | the menu scene step `0x003C9FD0` (menu mode `0x40`) | 11 | - |
| `men_z0002` | `438` | the menu scene step `0x003C9FD0` (menu mode `0x41`) | 14 | - |
| `men_z0003` | `439` | the menu scene step `0x003C9FD0` (menu mode `0x42`) | 1 | - |
| `men_z0005` | `429` | field 13 (`ttl_b01`) | 0 | - |

What opens the three menu scenes: script verb `openfullscreenmenu_48d` with selector 6 opens menu id 22, and
`0x002E1A60` turns parameters 0, 1 and 2 into the menu modes `0x40`, `0x41` and `0x42` ([Menus](../Menus-And-HUD/menus.md));
those load events 437, 438 and 439 through `0x003CA140`. Of the 1,274 `openfullscreenmenu_48d` calls of the `us`
scripts that decode (`evt_t0020` has no `EBP2` header), two pass selector 6: `grm_a0480` with parameter 0 and `rbn_a03` with 2. The `opened_by` column gives each.

No shipped script requests `men_z0002`:

- Event 438 loads for mode `0x41` on menu `0x16` or on menu 2: the menu dispatcher `0x0027FB70` sends both menus to one arm (table `0x00280090`, entries 0 and 20), which hands modes `0x40` and `0x41` to `0x002D7070` (`0x0027FE8C`).
- Verbs `0x48D` (`0x00346308`) and `0x472` (`0x00347112`) give menu `0x16` mode `0x41` only for parameter 1 of selector 6 (`0x002E1A9A`), and give menu 2, which every selector above 6 opens (`0x002E0E00`), their parameter unchanged. No script of the nine language trees passes selector 6 with parameter 1 or a selector above 6, and none calls verb `0x472`.
- The other writers of the request's mode word (`0x0215F1A8`) store 0 (`0x002E0B9D`, `0x002E15DF`, `0x002E1AFA`) or, through the native request `0x002E1B10`, 0, `0x21` or, for menu 2, payload word 2 (`global_flag[2]`, `+0x4`), or 1 when that word is 0 (`0x00253F31`-`0x00253F44`).
- Scripts store only 0 to 15 in that word, apart from the byte fills of `btlctrl` and `mapctrl` (0 or `0xFF` in every byte), and no enemy order writes a payload word.

### The scenes

- `men_z0001`, the Gambit Screen tutorial (`gambit_tutorial.main`), holds nine lines of Balthier, each beginning with
  his name ("This is the Gambit Screen. You can reach it from the Party Menu." ... "Well, that's the long and short of
  it."), and two list prompts ("A list of available actions. Press to exit." / "A list of available targets. Press to
  exit.").
- `men_z0002`, the license board tutorial (`sample_tutorial.main`), walks Vaan through the license board ("This is the
  license board." ... "Select the Accessories 1 license and press to acquire it.") and his Action List ("Press to open
  and advance through Vaan's Action List.").
- `men_z0002`: its first two entries are "Not enough LP. Vaan needs [value] LP for this tutorial. Press X to exit."
  and "Already have the Accessories 1 license. Unlearn license and start again. Press X to exit."
- `men_z0003` holds one line, the map hint "Your location map often bears a mark showing your destination. Consult the
  map when you are unsure of where to go next."
- `men_z0005`, loaded and played in field 13 (`ttl_b01`), is the staff roll ([Staff roll](../Menus-And-HUD/staff-roll.md)).
- No scene gives an item, sets a flag, writes the story counter or changes the party.
- The tutorial battle groups 1 to 4 ([Tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md)) reach a battle only through script verb `0x45C`, which no script of the nine language trees calls.
- The scripts table [`tutorials-scripts.tsv`](tutorials-scripts.tsv), with the columns of the zone scripts
  tables, has three rows: `gambit_tutorial.main` of `men_z0001` shows lines 0 to 10 (Balthier, and lines with no
  name shown), `sample_tutorial.main` of `men_z0002` shows lines 1 to 13 (Tomaj, and lines with no name shown) and
  `sample_tutorial.main` of `men_z0003` shows line 0, the map hint. The staff roll script `men_z0005` has no row.

### Every step

The steps table [`tutorials-script-steps.tsv`](tutorials-script-steps.tsv) has one row for each step of every function
of the four scripts, in the order the function runs them: each call, request, store, branch, loop, case and return. It
has 2,342 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `men_z0001` | 145 | `men_z0003` | 17 |
| `men_z0002` | 191 | `men_z0005` | 1,989 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). None of these scripts carries
one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 2,205 |
| empty | 137 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `men_z0005` (event `429`), `staffroll_main.main` waits
32 frames, frees fade layers 0, 1 and 2, fades layer 0 out over 0 frames, waits on it and turns user control off. It
fades in over 0 frames, waits 90 frames and then waits one frame at a time until `padt()` holds bit `0x8`, the cancel
button or the OK button. It fades layer 0 out over 60 frames, waits on it, waits 15 frames and ends the event scene.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event, or the exe step that requests the scene through `0x0032FC30` |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `opened_by` | the script call that opens the scene, its field and the story counter it runs at |

The steps table [`tutorials-script-steps.tsv`](tutorials-script-steps.tsv) has one row per step:

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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Staff roll](../Menus-And-HUD/staff-roll.md) - `men_z0005` line by line.
- [Location title scripts](titles-scripts.md) - field 13, whose script loads the staff roll.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [`tutorials-script-list.tsv`](tutorials-script-list.tsv) - the script list, one row per scene script of the group
  with its size (4 rows).

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the
shared helper actors it carries).
