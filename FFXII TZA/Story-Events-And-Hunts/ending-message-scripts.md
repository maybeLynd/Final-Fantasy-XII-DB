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

## Related

- [Ending message scenes](ending-message-scenes.md) - the scene's full text and the zone script that loads it.
- [Shared zone-script actors](shared-zone-script-actors.md) - the helper actors the area scripts share, none of which this scene carries.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
