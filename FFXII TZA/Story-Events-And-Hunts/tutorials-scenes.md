[Home](../../README.md) / [Story, events and hunts](README.md) / Tutorial and staff roll scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Tutorial and staff roll scenes: the gambit, license board and map tutorials and the staff roll | reference | Story, events and hunts | Scenes and scripts by area / Opening, ending and Trial Mode | The scene scripts of the group men: the Gambit Screen and license board tutorials, the map hint and the staff roll, with every line they hold in the game's own words and the one field whose script loads one of them. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x003C9FD0, 0x0032FC30, 0x003CA140 |

## What it lists

The table [tutorials-scenes.tsv](tutorials-scenes.tsv) has one row per scene script of the group `men` under
`plan_master/us/event`. No zone script shares their file-name prefix, so their `next` column is `-`. Every
`eventread` and `eventread_e8` call of the zone and scene scripts names its event id as a number; of the four ids,
only 429 (`men_z0005`) is named, in field 13 (`ttl_b01`). The menu scene step `0x003C9FD0` requests the other three
through `0x0032FC30` (`0x003CA07C`) after `0x003CA140` sets their event.

`0x003C9FD0(m)` acts only for manager 3, while the in-use flag `0x02B47750` is set and the unload request byte
`0x022C6D20[3]` (`0x0032F6E0(3)`) is clear; otherwise it returns -1 (`0x003C9FD4`-`0x003C9FF6`). In state 1 it requests
the scene with `0x0032FC30(3, id)` for the id at `0x02B4774C`, sets the start hold with `0x0032ED70(3)` and moves to
state 2 (`0x003CA071`-`0x003CA08B`).

State 3, which `0x003CA1B0(3)` stores (`0x003CA1B0`), starts the scene: once `0x0032F6C0(3)` reports no load pending,
the step releases the hold with `0x00332130(3)` and moves to state 0 (`0x003CA04A`-`0x003CA062`). In state 4, once no
load is pending, it disposes of the scene with `0x00332190(3)`, moves to state 5, clears the in-use flag and sets
the id to -1 (`0x003CA011`-`0x003CA03B`). In any other state it does nothing, and every path past the first tests
returns 0. The whole state machine is on [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md).

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `men_z0001` | `437` | the menu scene step `0x003C9FD0` (menu mode `0x40`) | 11 | - |
| `men_z0002` | `438` | the menu scene step `0x003C9FD0` (menu mode `0x41`) | 14 | - |
| `men_z0003` | `439` | the menu scene step `0x003C9FD0` (menu mode `0x42`) | 1 | - |
| `men_z0005` | `429` | field 13 (`ttl_b01`) | 0 | - |

What opens the three menu scenes: script verb `openfullscreenmenu_48d` with selector 6 opens menu id 22, and
`0x002E1A60` turns parameters 0, 1 and 2 into the menu modes `0x40`, `0x41` and `0x42` ([Menus](../Menus-And-HUD/menus.md));
those load events 437, 438 and 439 through `0x003CA140`, which gives event 440 (`0x1B8`) for any other argument
(`0x003CA153`-`0x003CA164`). Of the 1,274 `openfullscreenmenu_48d` calls of the `us`
scripts that decode (`evt_t0020` has no `EBP2` header), two pass selector 6: `grm_a0480` with parameter 0 and `rbn_a03` with 2. The `opened_by` column gives each.

`0x003CA140(n)` does nothing while `0x02B47750` is set (`0x003CA140`-`0x003CA147`). Otherwise it sets `0x02B47750` and
`0x02B47748` to 1 and stores the event at `0x02B4774C`: 437 for n 0, 438 for 1, 439 for 2 and 440 for any other value
(`0x003CA149`-`0x003CA199`).

No shipped script requests `men_z0002`:

- Event 438 loads for mode `0x41` on menu `0x16` or on menu 2: the menu dispatcher `0x0027FB70` sends both menus to one arm (table `0x00280090`, entries 0 and 20), which hands modes `0x40` and `0x41` to `0x002D7070` (`0x0027FE8C`).
- Verb `0x48D` (`0x00346308`) gives menu `0x16` mode `0x41` only for parameter 1 of selector 6 (`0x002E1A9A`), and gives
  menu 2, which every selector above 6 with bit `0x8000` cleared opens (`0x002E0E00`), its parameter unchanged. No
  script of the nine language trees passes selector 6 with parameter 1 or a selector above 6.
- Verb `0x472` (`0x00347112`) passes `0x002E1A60` parameter 0, so mode `0x40` for selector 6, unless its value stack
  already holds 63 entries; no script of the nine language trees calls it, the undecoded `evt_t0020` image included.
- The body at `0x003470D0` first pushes the integer 0 with `0x00267F90(context, 0)` (nothing is pushed when the stack
  already holds 63 entries, `0x00267F93`) and stores the low byte of the answer of `0x00229EB0()`, zero-extended, in the
  dword `+0x04` of its third argument and 0 in the dword `+0x08` (`0x003470DA`-`0x003470F8`).

  It then takes two values with `0x00267E10(context)`, the pushed 0 and then the script's argument, and calls `0x002E1A60`
  with the second taken as its first argument and the first taken as its second (`0x003470FF`-`0x00347112`).
  `0x002E1690()` follows, and the body ends in a jump to `0x002E0650` (`0x00347117`-`0x00347126`).
- The ten calls of the developer menus (`bin/ctrl`, `bin/evctrl` and `bin/mapctrl`, in the `in` and `ch` trees) pass `0x8005`: the save menu, selector 5, with bit `0x8000`, which skips the fade ([Menus](../Menus-And-HUD/menus.md)).
- The other writers of the request's mode word (`0x0215F1A8`) store 0 (`0x002E0B9D`, `0x002E15DF`, `0x002E1AFA`) or, through the native request `0x002E1B10`, 0, `0x21` or, for menu 2, payload word 2 (`global_flag[2]`, `+0x4`), or 1 when that word is 0 (`0x00253F31`-`0x00253F44`).
- Scripts store only 0 to 15 in that word, apart from the byte fills of `btlctrl` and `mapctrl` (0 or `0xFF` in every byte), and no enemy order writes a payload word.

### The scenes

- `men_z0001`, the Gambit Screen tutorial (`gambit_tutorial.main`), holds nine lines of Balthier, each beginning with
  his name, from the first message below to the second, and two list prompts ("A list of available actions. Press to
  exit." / "A list of available targets. Press to exit.").

Balthier's first line: "This is the Gambit Screen. You can reach it from the Party Menu. To create a gambit, you need
only select an action and a target for that action. Here, let me show you. I'll start by changing the action of one of
my gambits."

His last: "Well, that's the long and short of it. I'll set my gambits as they were before we started. Feel free to
change them later if you like."

- `men_z0002`, the license board tutorial (`sample_tutorial.main`), walks Vaan through the license board, from the
  first message below to the second, and his Action List ("Press to open and advance through Vaan's Action List.").

The board's first line: "This is the license board. The license board shows which licenses you already have, as well
as some new ones waiting to be obtained. Licenses you've acquired are marked with a star."

Its last: "Use the directional buttons to navigate the license board. Select the Accessories 1 license and press to
acquire it."

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

### Columns of tutorials-scripts.tsv

The columns are those of the zone scripts tables (defined on
[Archades scripts](archades-scripts.md)); the three rows fill them as follows.

| Column | Holds |
|---|---|
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions that request it; `-` when neither applies: `main` on all three rows |
| `line_text` | the `us` text of the entries in `lines`, in the same order, separated by ` / `; a choice list is written `(choices: ...)` |
| `flags_released` | the story flag ids the function releases, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); `-` on all three rows |
| `flags_tested` | the story flag ids the function tests, in the same form; `-` on all three rows |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value; `-` on all three rows |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `-` on all three rows |
| `battles` | `boss gauge shown`, `every foe in a group removed` or `every foe in group 0 removed`; `-` on all three rows |
| `other_functions` | how many functions of the actor have no row: 1 on all three rows |

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
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 2,339 |
| empty | 3 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
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
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |
| `opened_by` | the script call that opens the scene, its field and the story counter it runs at |

The steps table [`tutorials-script-steps.tsv`](tutorials-script-steps.tsv) has one row per step:

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

- [Staff roll](../Menus-And-HUD/staff-roll.md) - `men_z0005` line by line.
- [Location title scripts](titles-scripts.md) - field 13, whose script loads the staff roll.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
- [`tutorials-script-list.tsv`](tutorials-script-list.tsv) - the script list, one row per scene script of the group
  with its size (4 rows).

The script list's columns are `script`, `kind` and `place` (the script, `scene`, and its event id), `actors` and
`functions` (the script's actors and functions), `rows` (its rows in a scripts table) and `shared_actors` (the
shared helper actors it carries).

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 77 calls with 19 other topics</summary>

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0032F6C0` | is called by | `0x0025D9E0` |
| `0x0032F6E0` | is called by | `0x0025D9E0` |
| `0x0032FC30` | calls | `0x0032FCA0` |
| `0x0032FC30` | is called by | `0x0025D9E0` |
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |
| `0x00332130` | calls | `0x00263FF0`, `0x0032F1B0` |
| `0x00332190` | calls | `0x00263FF0` |
| `0x003C9FD0` | calls | `0x00332130` |

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

**Characters and objects** (explained on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [debug menu](../Engine-Core/debug-menu.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

**Sound and music** (explained on [menu screens](../Menus-And-HUD/menu-screens.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md))

| Function | | Functions |
|---|---|---|
| `0x0027FB70` | calls | `0x002DE350`, `0x002DEE50` |

**Battle actions**

| Function | | Functions |
|---|---|---|
| `0x0027FB70` | calls | `0x00300060` |
| `0x0032ED70` | is called by | `0x00306BD0` |
| `0x0032F6C0` | is called by | `0x00306B10` |
| `0x0032F6E0` | is called by | `0x00306BD0` |
| `0x0032FC30` | is called by | `0x00306BD0` |
| `0x00332130` | is called by | `0x00306760` |
| `0x00332190` | is called by | `0x00306570`, `0x003065D0` |

**Battle actions** (explained on [action phases](../Battle-Actions/action-phases.md), [battle units](../Characters-And-Objects/battle-units.md), [party control modes](../Engine-Core/party-control-modes.md), [frame update order](../Engine-Core/frame-update-order.md))

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00354D00` | calls | `0x00229EA0` |

**Controls and input** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x002E1B10` | is called by | `0x00253C70` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x00351880` | calls | `0x001D6A70` |
| `0x003529E0` | calls | `0x001D6A70` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x002E1A60` | is called by | `0x003462D0`, `0x003470D0` |
| `0x002E1B10` | is called by | `0x0050DAB0` |
| `0x0032ED70` | is called by | `0x003522C0`, `0x00353080`, `0x00353590` |
| `0x0032F6C0` | is called by | `0x003541B0` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x0032FC30` | is called by | `0x003522C0`, `0x00353080`, `0x00353590`, `0x0050D0C0` |
| `0x00332130` | is called by | `0x00354B20`, `0x00354E80` |
| `0x00332190` | is called by | `0x00356D40` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x00351880` | calls | `0x00267E10` |
| `0x003529E0` | calls | `0x00267E10`, `0x00267F90` |
| `0x00354D00` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

**Scripts and script commands** (explained on [menus](../Menus-And-HUD/menus.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [ebp script container](../EBP-Script-Files/ebp-script-container.md), [debug menu](../Engine-Core/debug-menu.md))

**Scripts and script commands** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

**Menus and HUD**

| Function | | Functions |
|---|---|---|
| `0x0027FB70` | calls | `0x00280D20`, `0x002909F0`, `0x002D7070`, `0x003EF750` |
| `0x002D7070` | is called by | `0x0027FB70` |
| `0x002E1B10` | is called by | `0x0035C7B0`, `0x0035D6B0` |
| `0x003CA140` | is called by | `0x002D70F0` |
| `0x003CA1B0` | is called by | `0x002D70F0` |

**Menus and HUD** (explained on [menu screens](../Menus-And-HUD/menu-screens.md), [hud](../Menus-And-HUD/hud.md), [game over](../World-Areas-And-Travel/game-over.md), [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md))

**Menus and HUD** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [action availability](../Controls-And-Input/action-availability.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

**World, areas and travel**

| Function | | Functions |
|---|---|---|
| `0x0032FC30` | calls | `0x0025D4D0`, `0x003319D0`, `0x003EA6E0` |
| `0x0032FC30` | is called by | `0x00314020` |
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x00332130` | is called by | `0x00378120` |
| `0x003522C0` | calls | `0x0032FC30` |
| `0x00353080` | calls | `0x0032FC30` |
| `0x003C9FD0` | calls | `0x0032FC30` |

**World, areas and travel** (explained on [frame update order](../Engine-Core/frame-update-order.md), [debug logging](../Engine-Core/debug-logging.md), [debug menu](../Engine-Core/debug-menu.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md))

</details>
