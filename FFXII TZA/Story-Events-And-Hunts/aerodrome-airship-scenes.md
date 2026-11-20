[Home](../../README.md) / [Story, events and hunts](README.md) / Aerodrome airship scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Aerodrome airship scenes: the scene, its text and the aerodrome scripts that load it | reference | Story, events and hunts | Scenes and scripts by area / Scenes that recur through the story | The aerodrome airship scene script pas_z0000: its two lines in the game's own words, its actors, and the five aerodrome zone scripts, Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port, that load it. | 0x003529E0, 0x00351880, 0x0032FCA0 |

## What it lists

The table [aerodrome-airship-scenes.tsv](aerodrome-airship-scenes.tsv) has one row for the scene script `pas_z0000`
under `plan_master/us/event`, and the script list
[aerodrome-airship-script-list.tsv](aerodrome-airship-script-list.tsv) one row with its size. No zone script shares
its file-name prefix, so its `next` column is `-`; the zone scripts that load it are the aerodromes, and `loaded_by`
names each.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `pas_z0000` | `214` | the Aerodromes of Rabanastre, Nalbina Town, Bhujerba, Archades and Balfonheim Port | 2 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `pas_z0000` | scene | event `214` | 26 | 191 | 1 |

### The scene

- Each aerodrome loads event 214 from two functions: its director's `main` (`監督`, `常駐監督` or `EventDirector`)
  and `発着イベント監視.イベント再生とマップジャンプ`, the function the airship counters request, which also holds the
  jumps to the destinations ([Nalbina Town scripts](nalbina-town-scripts.md)).
- The debug control script `evctrl` also loads event 214, as the fourth choice of a debug menu whose event table
  holds 121, 121, 211 and 214 ([ATEL debug companions](../EBP-Script-Files/atel-debug-companions.md)).
- The load goes through `eventread_e8` (`0x0E8`, `0x00351880`) or `eventread` (`0x0E7`, `0x003529E0`), and `0x0032FCA0`
  reads the scene from index `4n` of the event file table
  ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- The scene's actors include `民間飛空艇` (the civilian airship), one set of three for each of the five towns
  (`ラバナスタ用１` to `バーフォン用３`), `客` (passengers) and `カメラマン`.
- Its two lines are Japanese choice lists in the `us` tree: `民間飛空艇発着イベントカメラ` with `何もしない`,
  `離陸カメラ` and `着カメラ`, and a second list with `もう一度` and `やめる`.
- Both lines are stored developer-menu strings, and the scene's script shows neither. No message call names the
  camera menu. The director `監督.main` names the "again / stop" list in two `aask` calls
  ([verb table](../Scripts-And-Script-Commands/verb-table.md)), but its first step jumps past both to a switch on
  `event_global_flag[3]` that plays the departure or the arrival (`pas_z0000` lines 83, 117-121 and 131).
- That function is the scene's one row in [aerodrome-airship-scripts.tsv](aerodrome-airship-scripts.tsv), whose
  columns are those of the zone scripts tables. No function of the scene gives an item, writes a flag or the story
  counter, or jumps.

### Columns of aerodrome-airship-scripts.tsv

The columns are those of the zone scripts tables (defined on
[Archades scripts](archades-scripts.md)); the one row fills them as follows.

| Column | Holds |
|---|---|
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions that request it; `-` when neither applies: `main` here |
| `speaker` | who speaks each line, in line order: a name, `???`, `no name shown` or `system message`; for an actor with a `setnpcname` call, the second names of its pairs: `no name shown` here |
| `line_text` | the `us` text of the entries in `lines`, in the same order, separated by ` / `; a choice list is written `(choices: ...)`: here the one list a call names, `(choices: もう一度 / やめる)` (the scene stores two entries) |
| `flags_released` | the story flag ids the function releases, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); `-` here |
| `flags_tested` | the story flag ids the function tests, in the same form; `-` here |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value; `-` here |
| `battles` | `boss gauge shown`, `every foe in a group removed` or `every foe in group 0 removed`; `-` here |
| `other_functions` | how many functions of the actor have no row: 1 here |

### Every step

The steps table [`aerodrome-airship-script-steps.tsv`](aerodrome-airship-script-steps.tsv) has one row for each step
of every function of `pas_z0000`, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 1,334 rows.

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
| `resolved` | 1,334 |

No step has an empty `resolution` cell.

A scene reads from top to bottom in its director's function. In `pas_z0000` (event `214`), `監督.main` switches on
`event_global_flag[3]`: at 1 it files `民間飛空艇発着イベント選択.離陸`, at 2 `民間飛空艇発着イベント選択.到着`, waiting until it ends, and fades
the screen out at once. It then shows the free targets again and ends the event.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; an entry the `us` tree ships in Japanese: an English sentence, then `Authored text (<its English>): ` and the entry |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the shared
helper actors it carries).

The steps table [`aerodrome-airship-script-steps.tsv`](aerodrome-airship-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. A case whose values meet an earlier case's is followed by `not (x = w)` for each such earlier case `w`, so the cell names only the values the case runs on: `x = lte(78); not (x = lt(78))` runs when x is 78. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. When such a way passes a case that an earlier case overlaps, the item counts only the values that case takes: after `case lt(0x0177)`, a `case lt(0x0182)` that returns gives the item `not (x = lt(0x0182)) or x = lt(0x0177)`, which holds unless 0x0177 <= x < 0x0182. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets, and, for a case whose every value an earlier case already matches, on the case values |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

In `arguments` and `condition`, `bitor`, `or` and `and` stand for the listing's `|`, `||` and `&&`. A comparison
`A == B` that is an operand of `bitor` is written in brackets, `(A == B) bitor (C == D)`, because the script evaluates
the comparison first.

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

- [Nalbina Town scripts](nalbina-town-scripts.md) - the Aerodrome functions that load this scene and the jumps that follow.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md) - riding chocobos and airships.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 13 calls with 4 other topics</summary>

**Characters and objects** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**World, areas and travel** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin manager resource set load (on ebp script container) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |

</details>
