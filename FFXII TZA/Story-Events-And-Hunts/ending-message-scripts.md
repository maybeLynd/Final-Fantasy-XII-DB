---
title: "Ending message scripts: what each function of the scene shows"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A090, 0x00264D60"
---

## What it lists

The table [ending-message-scripts.tsv](ending-message-scripts.tsv) has one row per function of the scene script
`msg_z0001` that does something a player can observe. The script belongs to no area: it is the only shipped script
under `plan_master/us/event` whose name begins `msg_`.

| Script | Kind | Scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `msg_z0001` | scene | event `399` | 4 | 41 | 31 | 0 |

Every row shows one line. Thirty functions of the actor `台詞` each pass one entry of the scene's section 2 to the
message verb `amest`, and `監視監督.Movie監視` requests all of them; the last row, `movieSkip監督.Skip監視`, shows the
`Skip` prompt. The scene itself, with its full text and the script that loads it, is on [Ending message scenes](ending-message-scenes.md).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes a battle call, loads a scene or changes the party; in this scene only lines
occur. Each listed row counts the other functions of its actor in `other_functions`.

### What the scene shows

- The lines run from "It's hard to believe a year has passed so quickly." to "Every good sky pirate needs a partner,
  right?", one function each, in the order of the section 2 entries 1 to 30.
- Entry 22, which the function `・・・兄さ` passes, is an empty string in the `us` text, so that function shows no
  words.
- No function names a speaker, sets a flag, writes the story counter or gives an item.

### How a call is read

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amest` | `0x082` | `0x0034A090` | `lines` | the second argument is a section 2 text id |

`amest` (`0x0034A090`) pushes 0 and jumps to `0x00349800`, the body of `ames_1fe`, which pops two values, pushes 0 and 0
and pushes the two values back, so the zeros lie beneath them, and jumps to `mes` (`0x461`, `0x00348DF0`). `mes` pops
eight values; the seventh, the script's second argument, goes with the current field context to `0x00264D60`, the
section 2 lookup, which keeps the low 24 bits of the id ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)).

An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
managers 1 to 3 ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).

### Every step

The steps table [`ending-message-script-steps.tsv`](ending-message-script-steps.tsv) has one row for each step of
every function of `msg_z0001`, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 949 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). This script carries none of
them, so this table has no `shared template` row.

An actor that runs another actor's code would have one `same code` row naming the actor whose steps it runs; this
table has none.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 939 |
| empty | 10 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `msg_z0001` (event `399`), `Movie監督.main` reads an
effect into effect slot 0 and waits for it,  readies movie 25, waits 180 frames and plays it. It starts `監視監督.Movie監視`
and `movieSkip監督.Skip監視` without waiting and waits until `movieSkip監督.Skip監視` ends. After the movie it closes message
windows 0 to 7, fades the music out over 10 frames when `file_var_s0_1` is not 0, waits until `監視監督.Movie監視` ends and
ends the event.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | `scene, event` and the scene's event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | `requested by` and the functions of the same script that request it by name |
| `speaker` | `-` on every row: the scene names no speaker |
| `lines` | the section 2 entry the function passes to the message verb |
| `line_text` | the `us` text of that entry; `(empty string)` for an entry with no text |
| `flags_set`, `flags_released`, `flags_tested` | `-` on every row |
| `counter_set`, `counter_tested` | `-` on every row |
| `items`, `jumps`, `battles`, `scenes`, `party` | `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` on every row: the scene carries none of the shared helper actors |

The script list [ending-message-script-list.tsv](ending-message-script-list.tsv) holds the first table above:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `scene`, and its event id |
| `actors`, `functions` | the script's actors and functions |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries |

The steps table [`ending-message-script-steps.tsv`](ending-message-script-steps.tsv) has one row per step:

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

- [Ending message scenes](ending-message-scenes.md) - the scene's full text and the zone script that loads it.
- [Shared zone-script actors](shared-zone-script-actors.md) - the helper actors the area scripts share, none of which this scene carries.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
