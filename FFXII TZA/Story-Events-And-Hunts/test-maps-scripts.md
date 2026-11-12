---
title: "Test map scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DD90, 0x0034E0B0, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0, 0x0034B760, 0x0034BB10, 0x0034ADA0, 0x00352190, 0x00352AF0"
---

## What it lists

The table has one row per script function of the test maps that does something a player can observe. It covers the two
`tst_` zone scripts under `plan_master/us/plan_map`; no field loads them (see below), and neither has such a function,
so the table has no row:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `tst_a01` | zone | field `0`, whose entry names the unshipped `plan_work` copy | 5 | 5 | 0 | 0 |
| `tst_j01` | zone | field `9`, no zone-script entry | 5 | 6 | 0 | 0 |

Both scripts place the four party actors `PC00` to `PC03` with `setupbattle`. `tst_a01`'s `setup.init` runs two empty
request arrays; `tst_j01`'s `setup.battle` readies the foe actors and sets their spawn distances, with no foe actor in
the script. No script carries one of the five shared helper actors ([Shared zone-script
actors](shared-zone-script-actors.md)).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step).

### What the scripts do

- `tst_a01` belongs to field 0, whose zone-script entry names
  `plan_work\us\plan_map\tst_a\tst_a01\global\tst_a01.ebp`, a path the archive does not hold ([zone
  changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [asset
  paths](../Game-Files-And-Data-Tables/asset-paths.md)); the shipped `plan_master/us` copy is named by no
  entry.
- `tst_j01` belongs to field 9, the first field of the area `tst_j` by `map_ref.bin`, which has no zone-script entry
  ([zone asset list](../World-Areas-And-Travel/zone-asset-list.md)).
- The one `mapjump` with a literal field 0 or 9 is `mapjump(0, 0, 4)` in `evt_t0505`, an event script that no event id
  names, so no script the game loads names these maps.

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
4. `0x00348DF0` reads the entry's flag through `0x002673A0`, bit `0x1` of the entry's upper half (`0x00348E85`), and
   opens the window through `0x002E16B0` only when that flag is clear (`0x00348EE0`-`0x00348EFF`). With the flag set it
   still makes its six slot calls (`0x00348E91`-`0x00348ECA`) and fills the call record (`0x00348ED7`-`0x00348EDC`) but
   opens no window ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

### Speakers, places and scenes

- The speaker is the second name of each pair the actor's `setnpcname` calls name in `us` `npcdic.bin`. The
  message window opener `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`test-maps-script-steps.tsv`](test-maps-script-steps.tsv) has one row for each step of every function
of the two scripts, in the order the function runs them: each call, request, store, branch, loop, case and return. It
has 35 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `tst_a01` | 19 | `tst_j01` | 16 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). No script of the test maps
carries one of them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has no such row.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 33 |
| empty | 2 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A function reads from top to bottom. In `tst_a01`, `PC00.init` calls `setupbattle(0)`, places the actor at (1.969,
0.000113, 2.587) with `setpos`, calls `sysDVAR` on two script variables and stores in them the ids of the items in
equipment slots 1 and 0 (`getequipitemid`).

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | the names `setnpcname` gives the actor, filled only for a row whose lines include a section 2 line; a system message is not spoken by the actor |
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

The script list [`test-maps-script-list.tsv`](test-maps-script-list.tsv) holds the first table above, one row per script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`test-maps-script-steps.tsv`](test-maps-script-steps.tsv) has one row per step:

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

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids, section
3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other scripts' copies
differ only in these.

## Related

- [Test battle map scripts](test-battle-maps-scripts.md) - the thirty-one `bts_` zone scripts, which place foes as
  well.
- [Opening setup scripts](opening-setup-scripts.md) - the `pre_` zone scripts, which no field loads either.
- [Shared zone-script actors](shared-zone-script-actors.md) - the helper actors the region scripts share.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00263990` is called by `0x0025C230`, `0x0025C830`, `0x00268D10`, `0x00272CB0`, `0x00272CE0`; `0x0032FCA0` calls
  `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0`; `0x00355830` calls `0x0025D5E0`, `0x003588B0`.
- Actor entity: those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [npc names](../Characters-And-Objects/npc-names.md).
- Actor entity: and on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Actor entity: and on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Core runtime: `0x00354D00` calls `0x00229EA0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00355830` calls `0x0026D6D0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- Party: `0x0034D4E0` calls `0x00263750`, `0x0026DC40`, `0x003271D0`, `0x00327850`, `0x00328DB0`, `0x00359C00`, `0x0035A050`,
  `0x003601B0`; `0x00352190` calls `0x00263750`, `0x003170E0`, `0x00322350`; `0x00352AF0` calls `0x00322350`, `0x003288F0`; `0x00355830`
  calls `0x003590D0`.
- Party: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Presentation: `0x00263990` is called by `0x002B0280`; `0x00377B60` is called by `0x002B7B80`, `0x002BAF80`; those functions
  are documented on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x0032FCA0` calls `0x002DF980`, `0x0032E400`, `0x0032E620`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls
  `0x001D6A70`; those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Save load settings: `0x00264F90` is called by `0x00583D60`; those functions are documented on
  [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md).
- Script VM: `0x00264D60` is called by `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`,
  `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0`; `0x00264F90` is called by `0x00357450`, `0x0050CDE0`; `0x002673A0` is called
  by `0x00348DF0`, `0x0034ADA0`, `0x003545B0`, `0x0050EAB0`; `0x002E16B0` is called by `0x0033F950`, `0x00348DF0`, `0x0034ADA0`,
  `0x0050EAB0`; `0x003449A0` calls `0x00267E10`, `0x0026B4E0`.
- Script VM: `0x00345080` calls `0x00267E10`, `0x00267F90`, `0x0026B4E0`; `0x003459C0` calls `0x00267E10`, `0x0026B4E0`; `0x00348DF0`
  calls `0x00267E10`; `0x00348DF0` is called by `0x00349800`; `0x00349800` calls `0x00267E10`, `0x00267F90`, `0x00348DF0`;
  `0x00349800` is called by `0x00349BF0`, `0x0034A090`, `0x0034A420`, `0x0034A7A0`; `0x00349BF0` calls `0x00267F90`, `0x00349800`;
  `0x0034A090` calls `0x00267F90`, `0x00349800`.
- Script VM: `0x0034A420` calls `0x00267F90`, `0x00349800`; `0x0034A6D0` calls `0x00267E10`; `0x0034ADA0` calls `0x00267E10`;
  `0x0034ADA0` is called by `0x0034B760`, `0x0034BB10`; `0x0034B760` calls `0x00267F90`, `0x0034ADA0`; `0x0034B9A0` calls
  `0x00267E10`; `0x0034BB10` calls `0x00267F90`, `0x0034ADA0`; `0x0034C030` calls `0x00267E10`; `0x0034D4E0` calls `0x00267E10`;
  `0x0034DD90` calls `0x00267E10`; `0x0034DFA0` calls `0x00267E10`.
- Script VM: `0x0034E0B0` calls `0x00267E10`, `0x0026B4E0`; `0x0034E320` calls `0x00267E10`; `0x0034E980` calls `0x00267E10`,
  `0x0026B4E0`; `0x0034EE20` calls `0x00267E10`; `0x00351880` calls `0x00267E10`; `0x00352190` calls `0x00267E10`; `0x003529E0` calls
  `0x00267E10`, `0x00267F90`; `0x00352AF0` calls `0x00267E10`; `0x00354D00` calls `0x00267E10`; `0x00355830` calls `0x00267E10`.
- Script VM: those functions are documented on [archades scenes](archades-scenes.md),
  [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md),
  [npc names](../Characters-And-Objects/npc-names.md),
  [force fight mode](../Engine-Core/force-fight-mode.md); and on
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- UI: `0x00263990` is called by `0x002AC5F0`; `0x00264F90` is called by `0x0029C530`; `0x003778B0` is called by `0x0029C530`;
  `0x00377B60` is called by `0x0029C530`; those functions are documented on
  [augments](../Damage-And-Battle-Formulas/augments.md), [zone asset list](../World-Areas-And-Travel/zone-asset-list.md).
- World area: `0x00264ED0` is called by `0x003EA6E0`; `0x00264F90` is called by `0x003145E0`, `0x003778B0`, `0x003C0450`,
  `0x0057FB00`; `0x0032FCA0` is called by `0x0032FC30`; `0x003778B0` calls `0x00264F90`; `0x003778B0` is called by `0x0057FB00`;
  `0x00377B60` is called by `0x0057FB00`.
- World area: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md),
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md),
  [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md).
- World area: and on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md),
  [debug menu](../Engine-Core/debug-menu.md).
