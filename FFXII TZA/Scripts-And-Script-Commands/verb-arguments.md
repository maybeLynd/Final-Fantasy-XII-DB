[Home](../../README.md) / [Scripts and script commands](README.md) / Script verb arguments

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Script verb arguments: what each argument of a script verb addresses in the game | reference | Scripts and script commands | Script commands | For 960 script verbs, one row per argument: the call id, the argument's number and type, what it addresses in the game (the actor field it sets, the table it indexes, the id space it names, the helper it reaches), the values the US scripts pass, the instructions that pop and use it, and the page that describes what it reaches; verbs with no argument get one row saying what the verb acts on. | 0x00267E10, 0x00267DB0, 0x00267F90, 0x00267F60, 0x0026B4E0, 0x0026B4C0, 0x003DDB40, 0x01EFE9D0 |

## What it lists

[verb-arguments.tsv](verb-arguments.tsv) has 1,449 rows for 960 script verbs, one row per argument.

- **The verbs.** They are taken in order of how many operations of the US scene and zone scripts call them, so
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
| rows | 1,449 |
| verbs | 960 |
| verbs with no argument (one argument-0 row each) | 288 |
| verbs by argument count | 1: 397; 2: 148; 3: 66; 4: 43; 5: 12; 6: 5; 8: 1 |
| argument rows by type | int 827; float 334 |
| rows that name a page | 1,449 |
| the first verbs in the table | `stdmotionplay`, `usemapid`, `motionloop`, `lookatoff`, `motionstartframe` |

### Standard motions

`stdmotionplay` (`0x011D`) and `stdmotionplay_2c2` (`0x02C2`) take a standard-motion id. An id with bit
`0x1000000` set (the scripts pass `0x01000000` to `0x0100001D` as literals) is an index into the 30 words
of the table `0x01EFE9D0`, which `0x003DDB40` plays as a render event, (kind << 12) + slot.

The slot is the `@FMC` entry of that number in the actor's `.ca` motion archives, and it carries the same name in
every archive that fills it, in some archives with the prefix `rlx_` (3,164 archives under `obj_finish/in`; the counts below include both
forms; for slot 1, `ready` in 746 archives and `rlx_ready` in 45).

`0x003DDB40` takes the low 24 bits with no bound; the variables the scripts pass hold only `0x01000000`-`0x01000001`
and `0x01000010`-`0x01000016`. An id without bit `0x1000000` plays as the render event (manager << 20) | id |
`0x1000`¹, the slot of that number of kind 1; the US scripts give 0, 1, 5, 10 and 53 this
way (27, 26, 26, 1 and 1 steps).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DDB85`-`0x003DDB8E` |

</details>

`0x003DDAD0(actor, unused, id)` is the same body with the float it passes to `0x002EB3E0` fixed at -1.0¹, where `0x003DDB40` passes its fourth argument². As in `0x003DDB40`, it overwrites its
second argument, `edx`, at once with bit `0x80` of byte `+0xD` of `0x00263F40(actor)` for `0x002E8170`³. The id is played as above⁴, and the call ends in `0x002EB3E0`⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01CEBC9C`, `0x003DDB1A` |
| ² | `0x003DDB52`, `0x003DDB92` |
| ³ | `0x003DDAE0`-`0x003DDAEF` |
| ⁴ | `0x003DDAF4`-`0x003DDB16` |
| ⁵ | `0x003DDB2F` |

</details>

Its callers are the untimed turn body `0x002690D0`, on its body-turn way¹, and Mode 3 of the per-frame
integrator `0x002E5750`², on [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026937C` |
| ² | `0x002E59CC` |

</details>

| Entry | Id | Render event | Slot | Slot name in the motion archives |
|---:|---|---|---:|---|
| 0 | `0x01000000` | `0x1001` | 1 | `ready` (791 archives) |
| 1 | `0x01000001` | `0x1001` | 1 | `ready` (791 archives) |
| 2 | `0x01000002` | `0x101A` | 26 | `ev_talk_1` (746 archives) |
| 3 | `0x01000003` | `0x1018` | 24 | `ev_trn_r` (781 archives) |
| 4 | `0x01000004` | `0x1019` | 25 | `ev_trn_l` (781 archives) |
| 5 | `0x01000005` | `0x1009` | 9 | `magic_ready` (618 archives) |
| 6 | `0x01000006` | `0x100A` | 10 | `magic` (618 archives) |
| 7 | `0x01000007` | `0x403D` | 61 | `attack` (576 archives) |
| 8 | `0x01000008` | `0x101C` | 28 | `ev_treasure` (621 archives) |
| 9 | `0x01000009` | `0x301B` | 27 | `ev_door` (616 archives) |
| 10 | `0x0100000A` | `0x1008` | 8 | `dead` (611 archives) |
| 11 | `0x0100000B` | `0x1049` | 73 | `summon_damageidle` (576 archives) |
| 12 | `0x0100000C` | `0x3001` | 1 | `ready` (791 archives) |
| 13 | `0x0100000D` | `0x4001` | 1 | `ready` (791 archives) |
| 14 | `0x0100000E` | `0x4036` | 54 | `deact` (571 archives) |
| 15 | `0x0100000F` | `0x4035` | 53 | `active` (571 archives) |
| 16 | `0x01000010` | `0x401E` | 30 | `ev_talk_happy` (169 archives) |
| 17 | `0x01000011` | `0x401F` | 31 | `ev_talk_angry` (169 archives) |
| 18 | `0x01000012` | `0x4020` | 32 | `ev_talk_sad` (169 archives) |
| 19 | `0x01000013` | `0x4021` | 33 | `ev_laugh` (169 archives) |
| 20 | `0x01000014` | `0x4022` | 34 | `ev_yes` (169 archives) |
| 21 | `0x01000015` | `0x4023` | 35 | `ev_no` (169 archives) |
| 22 | `0x01000016` | `0x4024` | 36 | `ev_talk_over` (169 archives) |
| 23 | `0x01000017` | `0x1011` | 17 | `field_magic_ready` (618 archives) |
| 24 | `0x01000018` | `0x1012` | 18 | `field_magic_start` (618 archives) |
| 25 | `0x01000019` | `0x1013` | 19 | `field_magic_end` (618 archives) |
| 26 | `0x0100001A` | `0x1014` | 20 | `field_damage` (611 archives) |
| 27 | `0x0100001B` | `0x1015` | 21 | `field_item` (621 archives) |
| 28 | `0x0100001C` | `0x104A` | 74 | `field_attack` (576 archives) |
| 29 | `0x0100001D` | `0x302F` | 47 | no name: no archive fills slot 47 |

## Related

- [Script verb table](verb-table.md): every call id, its callbacks and its argument count.
- [Verb dispatch](verb-dispatch.md): how a script instruction reaches a verb's callbacks.
- [Party verbs](party-verbs.md): the verbs that act on party members.
- The area script pages under 14-Story-Event-Quest-Hunt/Areas, whose steps call these verbs.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 8 calls with 5 other topics</summary>

**Movement and pathfinding** (explained on [native commands](native-commands.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00267F60`](verb-arguments.md) | is called by | [`0x00345430`](verb-table.md) (on verb table)<br>[`0x003488B0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00349680`](party-during-scenes.md) (on party during scenes)<br>[`0x003548B0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |

**Characters and objects** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263F40`](party-during-scenes.md) (on party during scenes) | calls | [`0x003587C0`](script-requests.md) (on script requests) |

**Battle actions** (explained on [game over](../World-Areas-And-Travel/game-over.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263F40`](party-during-scenes.md) (on party during scenes) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |

**Party** (explained on [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263F40`](party-during-scenes.md) (on party during scenes) | is called by | [`0x00304180`](../Engine-Core/party-control-modes.md) (on party control modes) |

**Graphics** (explained on [party during scenes](party-during-scenes.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263F40`](party-during-scenes.md) (on party during scenes) | is called by | [`0x003B70B0`](party-during-scenes.md) (on party during scenes) |

</details>
