---
title: "Victory pose scripts: what each function of the scene gives"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00345080"
---

## What it lists

The table [victory-pose-scripts.tsv](victory-pose-scripts.tsv) has one row per function of the scene script
`pos_z0000` that does something a player can observe. The script belongs to no area: it is the only script under
`plan_master/us/event` whose name begins `pos_`.

| Script | Kind | Scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `pos_z0000` | scene | event `427` | 10 | 42 | 1 | 0 |

The one row is `EFFECT.EFFECT_READ`, which `AD.main` requests. It holds thirteen `additem` calls, one for each of the
ids `0xC012` to `0xC01E`. The scene's other functions, among them `勝利ポーズ実行` of the actors `PC_001`, `PC_004`,
`WEAPON_001` and `OPTION_001` and `勝利カメラ再生` of `CAMERA`, show no line and give nothing. The scene, with the zone scripts that load
it, is on [Victory pose scenes](victory-pose-scenes.md).

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes a battle call, loads a scene or changes the party; in this scene only item calls
occur. The listed row counts the other functions of its actor in `other_functions`.

### What the ids are

The ids `0xC012` to `0xC01E` are the thirteen Espers, inventory class 17 ([Quickening and Esper
list](../Battle-Actions/quickening-and-esper-list.md)); the table names them as that list and [Scene
rewards](scene-rewards.md) do:

| Id | Esper | Id | Esper |
|---|---|---|---|
| `0xC012` | Belias | `0xC019` | Shemhazai |
| `0xC013` | Mateus | `0xC01A` | Chaos |
| `0xC014` | Adrammelech | `0xC01B` | Zeromus |
| `0xC015` | Hashmal | `0xC01C` | Exodus |
| `0xC016` | Cúchulainn | `0xC01D` | Ultima |
| `0xC017` | Famfrit | `0xC01E` | Zodiark |
| `0xC018` | Zalera | | |

A row lists every call its function's body holds. Each call sits in its own arm of a switch on the current field
id (`nowmap`) and runs only while that Esper is not held (`haveitem(id) == 0`), so a showing of the scene gives at
most the one Esper of the field it plays on. The fields of the thirteen arms, in the order of the listing:

| Field | Map (region) | Esper |
|---:|---|---|
| 415 | Cloister of Flame (The Tomb of Raithwall) | Belias (`0xC012`) |
| 71 | Terminus No. 7 (Barheim Passage) | Zalera (`0xC018`) |
| 612 | Hall of Worth (Stilshrine of Miriam) | Mateus (`0xC013`) |
| 223 | Empyrean Seat (Mosphoran Highwaste) | Exodus (`0xC01C`) |
| 698 | Gate of Wind (Giruvegan) | Shemhazai (`0xC019`) |
| 670 | Heaven's Challenge (Pharos - Third Ascent) | Hashmal (`0xC015`) |
| 668 | Womb of the Sun-cryst (Pharos - Third Ascent) | Famfrit (`0xC017`) |
| 342 | No. 1 Cloaca (Garamsythe Waterway) | Cúchulainn (`0xC016`) |
| 590 | Athroza Quicksands (Zertinan Caverns) | Adrammelech (`0xC014`) |
| 733 | Special Charter Dig (Henne Mines) | Zodiark (`0xC01E`) |
| 618 | Throne of Veiled Gods (Stilshrine of Miriam) | Zeromus (`0xC01B`) |
| 438 | The Crucible (Necrohol of Nabudis) | Chaos (`0xC01A`) |
| 888 | Crystal Peak (The Great Crystal) | Ultima (`0xC01D`) |

The map names are those of [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md).

### How a call is read

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `additem` | `0x2E5` | `0x00345080` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |

An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
managers 1 to 3 ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).

### Every step

The steps table [`victory-pose-script-steps.tsv`](victory-pose-script-steps.tsv) has one row for each step of every
function of `pos_z0000`, in the order the function runs them: each call, request, store, branch, loop, case and
return. It has 12,175 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). This script carries none of
them, so this table has no `shared template` row.

Some actors run another actor's code: `PC_002` in `pos_z0000` starts at the same place as `PC_001` and runs the same
functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 6 of these rows: 6 in
`pos_z0000`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 12,138 |
| empty | 37 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb that takes none). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `pos_z0000` (event `427`), `AD.main` hides the HUD,
turns user control off, files `EFFECT.EFFECT_READ` and waits until it ends. It files `PC_001.のっとり判定`, `PC_002.のっとり判定`,
`PC_003.のっとり判定` (when `file_var_s1_5` is below 2) and `PC_004.のっとり判定4`, waiting for each, then files `装備武器判定` on the
party actors together and waits for all. It reads motion 1 of `pos_z0000.mot` when `file_var_s1_6` or `file_var_s1_7`
is at least 1, and each of motions 2 to 9 when its own variable is at least 1.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | `scene, event` and the scene's event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | `requested by` and the functions of the same script that request it by name |
| `speaker`, `lines`, `line_text` | `-`: the scene shows no line |
| `flags_set`, `flags_released`, `flags_tested` | `-` |
| `counter_set`, `counter_tested` | `-` |
| `items` | each `additem` call, as `receives` and the item's name, separated by `; ` |
| `jumps`, `battles`, `scenes`, `party` | `-` |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-`: the scene carries none of the shared helper actors |

The script list [victory-pose-script-list.tsv](victory-pose-script-list.tsv) holds the first table above:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `scene`, and its event id |
| `actors`, `functions` | the script's actors and functions |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries |

The steps table [`victory-pose-script-steps.tsv`](victory-pose-script-steps.tsv) has one row per step:

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

- [Victory pose scenes](victory-pose-scenes.md) - the scene and the 139 zone scripts that load it.
- [Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md) - the Esper ids and the License Board squares they open.
- [Scene rewards](scene-rewards.md) - every item a script gives, the Espers of this scene among them.
- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md) - what `additem` does with an id.
