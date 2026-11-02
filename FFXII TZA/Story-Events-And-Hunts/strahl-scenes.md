---
title: "Strahl scenes: the scene, its text and the zone scripts that load it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x0032FCA0"
---

## What it lists

The table [strahl-scenes.tsv](strahl-scenes.tsv) has one row for the scene script `str_z0000` under
`plan_master/us/event`, and the script list [strahl-script-list.tsv](strahl-script-list.tsv) one row with its size.
No zone script shares its file-name prefix, so its `next` column is `-`; the zone scripts that load it belong to other
areas, and `loaded_by` names each.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `str_z0000` | `211` | 18 zone scripts: five aerodromes and thirteen field maps | 2 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `str_z0000` | scene | event `211` | 8 | 40 | 1 |

### The scene

- The private airship desks of the Aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port
  load event 211 from a talk function (`シュトラール受付.talk_step01` in Nalbina Town, `NPC01.talk_step01` or
  `NPC01.talk_09a` elsewhere; [Nalbina Town scripts](nalbina-town-scripts.md)).
- Thirteen field maps load it from `ym_shutoraljump.shtjump`: Passage Entrance (Dalmasca Estersand), Yensa Border
  Tunnel (Ogir-Yensa Sandsea), The Sandscale Bank (Nam-Yensa Sandsea), Kaukula Pass (Phon Coast), Babbling Vale
  (Mosphoran Highwaste), Sunlit Path (Ozmone Plain) and Path of the Firstfall (Paramina Rift).
- The other six are The Chosen Path (Tchita Uplands), Footfalls of the Past (Ridorana Cataract), both Crystal Glade
  maps (Giza Plains), Journey's Rest (Cerobi Steppe) and The Western Divide (Dalmasca Westersand).
- The debug control script `evctrl` also loads event 211, as the third choice of a debug menu whose event table
  holds 121, 121, 211 and 214 ([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md)).
- The load goes through `eventread` (`0x0E7`, `0x003529E0`) or `eventread_e8` (`0x0E8`, `0x00351880`), and `0x0032FCA0`
  reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The scene's actors are `監督`, `ユニットＡ`, `ユニットＢ`, `ユニットＣ`, `カメラ`, `効果音`, `背景曲` and
  `STURAHL`. Its two lines are choice lists of digits, `(choices: 0 / 1 / 2 / 3)` and `(choices: 0 / 1)`.
- The director `監督.main` asks its choice lists with `aask` ([verb table](../Scripts-And-Script-Commands/verb-table.md)); that
  is the scene's one row in [strahl-scripts.tsv](strahl-scripts.tsv), whose columns are those of the zone
  scripts tables. No function of the scene gives an item, writes a flag or the story counter, or jumps.

### Columns of strahl-scripts.tsv

The columns are those of the zone scripts tables (defined on
[Archades scripts](archades-scripts.md)); the one row fills them as follows.

| Column | Holds |
|---|---|
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions that request it; `-` when neither applies: `main` here |
| `speaker` | who speaks each line, in line order: a name, `???`, `no name shown` or `system message`; for an actor with a `setnpcname` call, the second names of its pairs: `no name shown` here |
| `line_text` | the `us` text of the entries in `lines`, in the same order, separated by ` / `; a choice list is written `(choices: ...)`: here `(choices: 0 / 1 / 2 / 3) / (choices: 0 / 1)` |
| `flags_released` | the story flag ids the function releases, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); `-` here |
| `flags_tested` | the story flag ids the function tests, in the same form; `-` here |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value; `-` here |
| `battles` | `boss gauge shown`, `every foe in a group removed` or `every foe in group 0 removed`; `-` here |
| `other_functions` | how many functions of the actor have no row: 1 here |

### Every step

The steps table [`strahl-script-steps.tsv`](strahl-script-steps.tsv) has one row for each step of every function of
`str_z0000`, in the order the function runs them: each call, request, store, branch, loop, case and return. It has 371
rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). This script carries none of
them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 357 |
| empty | 14 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `str_z0000` (event `211`), `監督.main` reads motion 1 of
`str_z0000.mot`, reads an effect into effect slot 0 while it files `STURAHL.バインドオン`, and waits for both, then reads
event sound slots 0 and 1. It hides the party and, by `file_var_s0_2`, files `ユニットＡ.メイン`, `ユニットＢ.メイン` or `ユニットＣ.メイン`
and waits until it ends. It then files `STURAHL.バインドオフ` and waits for it, releases the effect and the event sounds,
shows the party again and disposes of event manager slot 0.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)` |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the shared
helper actors it carries).

The steps table [`strahl-script-steps.tsv`](strahl-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
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

- [Nalbina Town scripts](nalbina-town-scripts.md) - the private airship desk that loads this scene.
- [Aerodrome airship scenes](aerodrome-airship-scenes.md) - the scene the same aerodromes load for the public airships.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
