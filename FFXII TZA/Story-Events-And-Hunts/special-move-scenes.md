---
title: "Special move scenes: the scene script, its actors and what it shows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x0032FCA0, 0x00306BD0, 0x0032FC30, 0x00309230"
---

## What it lists

The table [special-move-scenes.tsv](special-move-scenes.tsv) has one row for the scene script `spc_z0000` under
`plan_master/us/event`, and the script list [special-move-script-list.tsv](special-move-script-list.tsv) one row
with its size. It is the only script whose name begins `spc_`.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `spc_z0000` | `210` | the battle scene step `0x00306BD0`, for every Quickening and Concurrence | 0 | - |

| Script | Kind | Scene | Actors | Functions | Rows in a scripts table |
|---|---|---|---:|---:|---:|
| `spc_z0000` | scene | event `210` | 5 | 17 | 0 |

### The scene

- Event 210 names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene managers
  1 to 3 ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).
- No zone script loads event 210 by a literal id. The battle scene step `0x00306BD0` requests it on scene manager 3
  through `0x0032FC30` (`0x00306C56`) for every Quickening (actions 208 to 225) and Concurrence (actions 226 to 241),
  whose effect id is 210 (`0x00309230`); the `loaded_by` cell gives it.
- The scene's five actors are `監督`, `技読み込み`, `メッセージ監督`, `target00` and `PC00`, whose functions
  include `技読み込み` and `必殺技設定`.
- Its section 2 has no entries, and no function shows a line, gives an item, writes a flag or the story counter, or
  jumps, so the scene has no row in a scripts table.

### Every step

The steps table [`special-move-script-steps.tsv`](special-move-script-steps.tsv) has one row for each step of every
function of `spc_z0000`, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 194 rows.

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
| `resolved` | 173 |
| empty | 21 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, and `-` otherwise.

A scene reads from top to bottom in its functions. In `spc_z0000` (event `210`), `監督.main` files `監督.全体処理`, which
files `技読み込み.技読み込み` and `技読み込み.技読み込み終了待ち`, waiting until each ends, hides the HUD, fades the music to volume 64 over
60 frames and waits 20 frames. In its loop it files `PC00.必殺技設定` and `PC00.武器消し`, waiting for each, when
`isfusion_spattack` is false, then starts `メッセージ監督.message`, plays the attack with `spattackplay`, fades the screen in
at once and starts scene cut 0.

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the exe step that requests the scene: the battle scene step `0x00306BD0` and the actions whose effect id is the event |
| `lines` | the number of entries in the scene's section 2 |
| `synopsis` | the `us` text of every non-empty entry; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the shared
helper actors it carries).

The steps table [`special-move-script-steps.tsv`](special-move-script-steps.tsv) has one row per step:

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

- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [Action phases](../Battle-Actions/action-phases.md) - the battle action phases, with the script verb `spattackread`.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032FC30` calls `0x0032FCA0`; `0x0032FC30` is called by `0x0025D9E0`; `0x0032FCA0` calls `0x002628B0`,
  `0x0032ED80`, `0x00330310`, `0x003306E0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md); and on
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- Combat action: `0x00306BD0` calls `0x00309230`; `0x00306BD0` is called by `0x0030CE10`; `0x00309230` is called by `0x00306BD0`;
  `0x0032FC30` is called by `0x00306BD0`; those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Script VM: `0x0032FC30` is called by `0x003522C0`, `0x00353080`, `0x00353590`, `0x0050D0C0`; those functions are documented on
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [debug menu](../Engine-Core/debug-menu.md).
- World area: `0x00306BD0` calls `0x0032FC30`; `0x0032FC30` calls `0x0025D4D0`, `0x003319D0`, `0x003EA6E0`; `0x0032FC30` is called
  by `0x00314020`; `0x0032FCA0` is called by `0x0032FC30`; those functions are documented on
  [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [debug logging](../Engine-Core/debug-logging.md).
