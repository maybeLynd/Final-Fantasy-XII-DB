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

The ids `0xC012` to `0xC01E` are the thirteen Espers, inventory class 17
([Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md)); the table gives them as ids,
and [Scene rewards](scene-rewards.md) names each one:

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
| `items` | each `additem` call, as `receives` and the item id, separated by `; ` |
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

## Related

- [Victory pose scenes](victory-pose-scenes.md) - the scene and the 139 zone scripts that load it.
- [Quickening and Esper list](../Battle-Actions/quickening-and-esper-list.md) - the Esper ids and the License Board squares they open.
- [Scene rewards](scene-rewards.md) - every item a script gives, the Espers of this scene among them.
- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md) - what `additem` does with an id.
