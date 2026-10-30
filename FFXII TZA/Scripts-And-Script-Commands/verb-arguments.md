---
title: "Script verb arguments: what each argument of a script verb addresses in the game"
kind: "reference"
category: "Scripts and script commands"
addresses: "0x00267E10, 0x00267DB0, 0x00267F90, 0x00267F60, 0x0026B4E0, 0x0026B4C0, 0x003DDB40, 0x01EFE9D0"
---

## What it lists

[verb-arguments.tsv](verb-arguments.tsv) has 129 rows for 100 script verbs, one row per argument.

- **The verbs.** They are taken in order of how many operations of the shipped scene and zone scripts call them, so
  the verbs that most scene steps use come first.
- **Which verbs have rows.** A verb is listed once all of its arguments are read to the point where the game uses
  them. The [verb table](verb-table.md) lists every call id.
- **Verbs with no argument.** Such a verb has one row with argument 0, saying what the verb acts on: the calling
  actor, its motion, its shadow or the camera.

How an argument is read:
- A verb's handler takes its arguments from the script stack: `0x00267E10` pops an integer and `0x00267DB0` a float.
- Argument 1 is the one the script pushes first, so the handler pops it last.
- A handler that pushes constants of its own (`0x00267F90` for an integer, `0x00267F60` for a float) and then jumps to
  a shared body pops those constants first. The row counts only the script's own arguments.

## Columns

| Column | Meaning |
|---|---|
| `call_id` | the verb's sixteen-bit call id, as in [verb-table.tsv](verb-table.tsv) |
| `verb` | the verb's name in the scripts |
| `argument` | 1 for the first argument the script pushes; 0 on the one row of a verb with no argument |
| `type` | `int` (popped by `0x00267E10`) or `float` (popped by `0x00267DB0`); `-` for argument 0 |
| `addresses` | what the argument is in the game: the field it sets, the table it indexes, the id space it names, and the helper it is passed to |
| `values` | the values the 1,114 us scripts pass, most frequent first, with their counts; "variable" for a value computed in the script |
| `evidence` | the instructions: the pop, and the uses that the `addresses` cell names |
| `page` | the final page that describes what the argument reaches, with its section where one applies |

## Data

| Fact | Value |
|---|---|
| rows | 129 |
| verbs | 100 |
| verbs with no argument (one argument-0 row each) | 28 |
| verbs by argument count | 1: 53; 2: 11; 3: 6; 4: 2 |
| argument rows by type | int 71; float 30 |
| rows that name a page | 129 |
| the first verbs in the table | `stdmotionplay`, `usemapid`, `motionloop`, `lookatoff`, `motionstartframe` |

## Related

- [Script verb table](verb-table.md): every call id, its callbacks and its argument count.
- [Verb dispatch](verb-dispatch.md): how a script instruction reaches a verb's callbacks.
- [Party verbs](party-verbs.md): the verbs that act on party members.
- The area script pages under 14-Story-Event-Quest-Hunt/Areas, whose steps call these verbs.
