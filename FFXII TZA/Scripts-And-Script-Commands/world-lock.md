[Home](../../README.md) / [Scripts and script commands](README.md) / World lock

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| World lock: the stop request that holds the world still for a scene or a talk, the field hold, and event time stop | system | Scripts and script commands | Event scenes | How a talk or a scene holds the rest of the world still: stop request 6 and the counter that takes it, the turn toward the talk partner, the field hold and its bytes, which actors the request releases, and the event time stop request. | 0x0034DC30, 0x00263230, 0x00263050, 0x00263480, 0x00226BE0, 0x00225CD0, 0x00377700, 0x00314A60, 0x02099DE7, 0x02099DB4 |

## What the player sees

While a talk or scene runs, the rest of the world holds still: nobody else starts a conversation, and every actor
the stop request locks stops moving.

## How it works

### The world lock

The lock is stop request 6 of the registry. `0x00263230(actor, 1)` takes it when no take is active
(`0x02099DB4` at 0 or below), `0x0209A2A8` is set and the actor's byte `+0x0C` bit `0x80` is clear:
`0x00226BE0(6, 0, 0, 0, 4, flag)` with the flag `0x00377700() != 0`. With a take active it skips the request and the
turn below (`0x0026325A`).

In every case the counter at manager `+0x1E0` is then raised and summed into `0x02099DB4` over the live managers among
0, 1 and 2 (`0x002633CE`-`0x00263402`; managers 3 and 4 are not added), the actor's steering is pushed (`0x002EAB80`) and,
for an actor with a battle unit (`+0x30`), its speed is set to 0 (`0x0026D6F0`) and the taken actor's battle action is
cancelled (`0x0035AE10(actor, 1)`).

Any op other than 1 returns at once (`0x00263233`). A null actor passes the `+0x0C` test (`0x00263276`) and faults at
`0x002632FD` or `0x002633BB`, which read it without a test. The request engine reaches it with flag 1: the talk
filer passes it for slot 2, so every conversation takes the lock when its script starts
([script requests](script-requests.md)).

`0x00263230` also turns the party leader ([Party leader](../Party/party-leader.md)) toward the taken actor, when
the leader (`0x003590D0` → `0x003588B0`, looked up with `0x02099D70` pointed at manager 0) exists and has an armed render
entry (`0x002E7600`): `0x002EC2C0(focus, [actor + 0xB8] + 0x20)`, the movement context's `+0x20`, for a class-1 actor
or `0x002EBFA0(focus, manager, ordinal, 0x30B)` for class 3, then `0x002EC380(focus, 2, 6.0)`, `0x002EBE50(focus, 1)`,
`0x002E8EE0` and `0x002ED040(focus, 1)`. That is the turn the player sees at the start of every talk.

For a class-1 actor and a class-3 leader it also sets bit `0x80` of `+0x62` of the leader's steering record
`[[focus + 0xB8] + 0xF0]` (`0x0026339D`); for an actor of any other class only `0x002ED040(focus, 1)` runs
(`0x002633A9`).

`0x00263050(actor, 1)` is the release: it lowers the counter, sums the counters of the live managers among 0, 1 and 2
into `0x02099DB4` (`0x002630BE`-`0x002630EA`) and, at 0 or below, clears action-availability row 3 (`0x002E1CD0(1, 3)`), sets
`0x02099DE5` to 0 and `0x02099DE7` to `0xFF`, runs the field hold `0x00263480(actor, 2 or 1)` (2 when the actor's byte
`+0x0C` bit `0x80` is set) and `0x00225CD0(6, 4)`, the latter only while `0x0209A2A8` is set and that bit is clear
(`0x00263128`-`0x00263141`).

It then releases the leader's look (`0x002EBE50(focus, 0, 0)` and `0x002E8EE0` when `0x002E7600` is non-zero, then
`0x002ED040(focus, 0)`); the steering pop and the other ops are on
[facing and steering](../Movement-And-Pathfinding/facing-and-steering.md).

`0x002ED040(focus, v)` does nothing for a null actor, a null binding `+0xC0`, a first dword or word of -1, or a render
record `[0x022C6F28] + word × 0x740` that is null or has `+0x284` 0 (`0x002ED047`-`0x002ED083`). Otherwise it stages the
look command at the record's `+0x580` with `v` as its value (`0x003E6CD0` → `0x003E37A0`: bit `0x40000000` set, bit
`0x80000000` = `v & 1`; [character rig and look](../Graphics/character-rig-and-look.md)) and sets the
record's `+0x290` bit `0x800` (`0x002ED085`-`0x002ED08D`).

`0x00377700` returns 1 only when the field bit and the save bit are both clear: the field bit is bit `0x1` of the
byte `[0x02ADD100] + 8 + 3 × field + 2` (`0x0037772D`, `0x0037772F`), read only when the table exists and the field index
is below its count at `+4`, otherwise taken as clear; the save bit is the persistent `+0x1062` bit `0x1`
(`0x00314A60`, set by `setsaverambattlestatus(0)`).

The field hold `0x00263480(actor, mode)` runs `0x00263560` first (`0x002634B0`). While `0x02099DE5` or `0x02099DE6` is
non-zero it raises request 5 for mode 0, 4 for mode 1, 7 for mode 2 and 4 for any other mode. Only mode 2 with a
non-null actor passes a list, the actor's handle from `0x003589B0` as its one entry (`0x002634C9`-`0x002634EB`); every
other case passes no list (`0x002634FD`-`0x00263507`). Each passes `0x02099DE7 == 0` as the flag with fade -1, and the
hold then runs the apply (`0x0026351D`).

With the hold bytes `0x02099DE5` and `0x02099DE6` both clear it releases 5, 4 and 7 instead, through `0x00225CD0` with
fade -1 and without the apply. The talk filer sets `0x02099DE7` to `0x00377700() == 0` and `0x02099DE5` to 1; the
release resets them.

Requests 4, 5, 6 and 7 walk manager 0 alone, because their A bit `0x80000000` is set (`0x00226C77`-`0x00226C91`)
([time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).

Every request locks every actor of the managers it walks and then releases the configured rows: the
party leader always, the other party members only when the flag is 0, and the non-party types by
their configuration. A locked actor keeps the request's bit in `+0x10C`, and the interpreter gate
refuses its script every frame unless the actor's byte `+0x0B` has bit `0x20` set
([script interpreter](script-interpreter.md)). Only the verb `set_force_ignore_timestop` (`0x497`) sets that bit
(`0x003506D0`).

Among actors outside the party, requests 6 and 4 put their bit in `+0x10C` only for class nibbles 1, 2, 7 and 3
(`0x00263BE0`, `0x00227137`-`0x0022729C`; [time stop and freeze](../Engine-Core/time-stop-and-freeze.md)).
`0x00265FF0` gives a new class-1 actor nibble 4 and a class-3 actor nibble 5. While an actor keeps either nibble,
these requests leave its `+0x10C` clear and its movement free, and are no reason for the interpreter to refuse
its script.

The nibble can change later. `0x00265A20` gives nibble 1 to up to 32 records of a manager whose `+0x28` is 0, when
the record's byte `+0x14` is at or above `0x80` (`0x00265A83`-`0x00265ACE`). `0x00269FE0` stores a new nibble for the
verb `setfreetargettype` (`0x265`, `0x003528D6`) and for a battle unit's `+0x58` (`0x00238E3E`). `0x00267CC0` writes 4
and `0x002659A0` writes 5.

Being left out of those classes is what lets an ordinary talk partner run its script: no actor with
`function talk(2)` in the `us` scripts calls `set_force_ignore_timestop`. Those 4,771 actors are 3,159 of type 6,
1,281 of type 1, 239 of type 5, 68 of type 0 and 24 of type 7. The table at `0x01E0C328` sets the class: types 1 and
2 are class 1, types 5 to 7 class 3 (`0x00267B0A`-`0x00267B13`).

Type 6 gets nibble 5 from `0x00265FF0`, or 4 after `npc_to_gimmick` (1,994 actors) or `setfreetargettype(4)` (98
actors), the only value a talk actor passes it. Type 1 gets 4. Type 0 has class 0, which `0x00265FF0` gives no nibble.
All 24 of type 7 are units placed by the `btlAtel` verbs that call `btlAtelSetUnitType(1)`: unit `+0x58` becomes 5
(table `0x01E09EE8`, `0x002396D6`), and `btlAtelSetUnitFinish` writes it as the nibble over `0x00265A20`'s 1 (`0x0023A499`,
`0x00238E3E`).

Of type 5, 238 actors are in scene scripts, whose managers 1 to 3 `0x00265A20` skips (`0x00265A70`), so they keep
nibble 5. The other is in the `wdl_b01` zone script and its `talk` only returns. This count reads each actor's own
script in `us`; the nibble one actor holds at one moment can still change as above.

Request 7 also puts its bit in `+0x10C` for nibbles 4 and 5. The field hold takes it for a talk partner whose byte
`+0x0C` has bit `0x80` set (`0x00268E0A`-`0x00268E30`), and its one-entry list releases only that partner.

Request 6 itself names no actor and no list (`0x00226BE0(6, 0, 0, 0, 4, flag)`), so it releases
no one beyond the configured rows. Of the field hold's requests, only request 7 for mode 2 with a non-null actor
carries a list, one entry long.

### Event time stop

`seteventtimestop(v)` (`0x0398`, `0x0034DC30`) raises stop request 11
through `0x002273B0` or releases it through `0x002260C0` when held ([time stop and
freeze](../Engine-Core/time-stop-and-freeze.md)).

## Layouts

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2099DE5` | `u8` | hold1 | field hold byte |
| `+0x2099DE6` | `u8` | hold2 | field hold byte |
| `+0x2099DE7` | `u8` | holdFlag | the flag the hold passes |
| `+0x2099DB4` | `i32` | activeTakes | sum of the lock counts of managers 0, 1 and 2 |

## Shipped data

| Fact | Value |
|---|---|
| `seteventtimestop` uses | 4,725 |

## Operations

Per lock take: one registry request over manager 0 and its release.

## State

The lock counter and the hold bytes.

## Modding notes

- A conversation takes the world lock with the flag from `0x00377700`: on a field whose record bit
  is set, or after `setsaverambattlestatus(0)`, the other party members keep moving.

## Related

- [Event scenes](event-scenes.md): loading, playing and disposing a scene, movies and skips.
- [The party during scenes](party-during-scenes.md): hiding, capturing and the summon group.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the registry behind the lock.
- [Script requests](script-requests.md): the talk filer and the start flag.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 200 calls with 29 other topics</summary>

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00225CD0` | calls | `0x00263FF0`, `0x00358940`, `0x00359B80` |
| `0x00225CD0` | is called by | `0x00263050` |
| `0x00226BE0` | calls | `0x00263FF0`, `0x003588B0`, `0x00358940`, `0x00359B80` |
| `0x00226BE0` | is called by | `0x00263230` |
| `0x00263050` | calls | `0x003588B0` |
| `0x00263050` | is called by | `0x003DB2A0` |
| `0x00263230` | calls | `0x003588B0`, `0x0035AE10` |
| `0x00263230` | is called by | `0x003DBDC0` |
| `0x00263480` | calls | `0x003589B0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00263480` | is called by | `0x002628B0`, `0x00263050`, `0x00268D10` |
| `0x00263560` | calls | `0x00238B40`, `0x00312130` |
| `0x00263560` | is called by | `0x002628B0`, `0x0037B4D0` |
| `0x0026D6F0` | calls | `0x003588B0` |
| `0x0026D6F0` | is called by | `0x00263230`, `0x0026C5D0`, `0x0026C8C0` |
| `0x002E1CD0` | is called by | `0x0025C830`, `0x00263050`, `0x00263660`, `0x00268D10`, `0x0026C5D0` |
| `0x002E7600` | is called by | `0x00263050`, `0x00263230`, `0x0026C5D0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x002E8EE0` | is called by | `0x00263050`, `0x00263230`, `0x002693D0`, `0x0026C5D0` |
| `0x002EAB80` | is called by | `0x00263230` |
| `0x002EBE50` | is called by | `0x00263050`, `0x00263230`, `0x002693D0`, `0x0026C5D0` |
| `0x002EBFA0` | calls | `0x00265020`, `0x003587C0`, `0x003589B0` |
| `0x002EBFA0` | is called by | `0x00263230` |
| `0x002EC2C0` | calls | `0x00265020` |
| `0x002EC2C0` | is called by | `0x00263230` |
| `0x002EC380` | is called by | `0x00263230` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x002ED040` | is called by | `0x00263050`, `0x00263230` |
| `0x003589B0` | is called by | `0x00234480`, `0x0025C230`, `0x0025C830`, `0x00268650`, `0x00268D10`, `0x0037B4D0`, `0x003B6F80` |
| `0x003590D0` | is called by | `0x0025B600`, `0x0025D9E0`, `0x00263050`, `0x00263230`, `0x00263AC0`, `0x00264010`, `0x00264050`, `0x0026C5D0`, `0x0026C8C0`, `0x0026DFB0` |
| `0x0035AE10` | calls | `0x00233F50` |
| `0x0035AE10` | is called by | `0x00263230`, `0x0026C5D0` |

**Characters and objects** (explained on [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [script requests](script-requests.md))

| Function | | Functions |
|---|---|---|
| `0x00377700` | is called by | `0x00263230`, `0x00268D10`, `0x0026C5D0` |

**Characters and objects** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [force fight mode](../Engine-Core/force-fight-mode.md), [script name bindings](script-name-bindings.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [party during scenes](party-during-scenes.md))

**Characters and objects** (explained on [battle units](../Characters-And-Objects/battle-units.md), [battle verbs](battle-verbs.md))

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x003590D0` | is called by | `0x00362850` |

**Battle actions**

| Function | | Functions |
|---|---|---|
| `0x00225CD0` | is called by | `0x00313DB0` |
| `0x00226BE0` | is called by | `0x00313DB0` |
| `0x003589B0` | is called by | `0x00319F50`, `0x00325260` |
| `0x003590D0` | is called by | `0x00317E60`, `0x00319090` |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [reward verbs](reward-verbs.md), [jump thunks](../Engine-Core/jump-thunks.md))

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00263560` | is called by | `0x0022B8C0`, `0x0022BC20` |

**Gameplay** (explained on [bestiary](../Enemy-Spawning/bestiary.md))

| Function | | Functions |
|---|---|---|
| `0x003589B0` | is called by | `0x0031ADB0` |
| `0x003590D0` | is called by | `0x0031ADB0` |

**Controls and input** (explained on [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

| Function | | Functions |
|---|---|---|
| `0x00225CD0` | calls | `0x00182D40`, `0x00182D60`, `0x00182DA0` |
| `0x002273B0` | calls | `0x00226BE0` |
| `0x00263230` | calls | `0x00226BE0` |
| `0x00263480` | calls | `0x00226BE0` |
| `0x003590D0` | is called by | `0x00226BE0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00225CD0` | is called by | `0x0026A1D0` |
| `0x00226BE0` | is called by | `0x0026A1D0` |
| `0x00263050` | calls | `0x002EAAA0`, `0x002EBE50` |
| `0x00263230` | calls | `0x0026D6F0`, `0x002EAB80`, `0x002EBE50`, `0x002EBFA0`, `0x002EC2C0`, `0x002EC380` |
| `0x00263480` | calls | `0x00263560` |
| `0x00263560` | calls | `0x0026D6F0` |
| `0x00263560` | is called by | `0x0026A1D0`, `0x0026A290` |
| `0x0026D6F0` | calls | `0x002E9BB0`, `0x002EC5B0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0026D6F0` | is called by | `0x0025DF00`, `0x00263560`, `0x00265FF0`, `0x0026A330`, `0x0026C3E0`, `0x0026D6A0`, `0x0026D6D0` |
| `0x002E1CD0` | is called by | `0x0026C3E0` |
| `0x002E7600` | is called by | `0x002690D0` |
| `0x002E8EE0` | is called by | `0x0026C120`, `0x002E28E0`, `0x002E3110`, `0x002E64E0`, `0x002EAAA0`, `0x002EBE50` |
| `0x002EAB80` | calls | `0x002627C0`, `0x00269F90`, `0x0026AE90`, `0x0026C120` |
| `0x002EBE50` | calls | `0x00265200`, `0x002EC3F0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x002EBE50` | is called by | `0x002690D0`, `0x0026C120` |
| `0x002EBFA0` | calls | `0x00265470`, `0x0026A1A0`, `0x0026A870`, `0x0026A8E0`, `0x0026A950`, `0x002E64E0`, `0x002EC2C0` |
| `0x002EBFA0` | is called by | `0x002EAAA0`, `0x002EC510` |
| `0x002EC2C0` | calls | `0x0026A870`, `0x0026A8E0`, `0x0026A950` |
| `0x002EC2C0` | is called by | `0x002EAAA0`, `0x002EBFA0`, `0x002EC510` |
| `0x002EC380` | is called by | `0x002690D0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x003589B0` | is called by | `0x002E5610`, `0x002EBFA0` |
| `0x003590D0` | is called by | `0x0026C3E0`, `0x0026D6F0`, `0x0026D810`, `0x002E45E0`, `0x002E5180`, `0x00319490`, `0x00325D90`, `0x00326BB0`, `0x00326D60`, `0x00343E20`, `0x00345430` |
| `0x0035AE10` | is called by | `0x0026C3E0` |
| `0x00377700` | is called by | `0x0026A1D0`, `0x0026C3E0` |

**Movement and pathfinding** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [script requests](script-requests.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [frame update order](../Engine-Core/frame-update-order.md))

**Movement and pathfinding** (explained on [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [script name bindings](script-name-bindings.md), [actor record fields](../Characters-And-Objects/actor-record-fields.md), [party during scenes](party-during-scenes.md))

**Movement and pathfinding** (explained on [script binding lifecycle](script-binding-lifecycle.md), [party control modes](../Engine-Core/party-control-modes.md), [player movement](../Movement-And-Pathfinding/player-movement.md), [battle units](../Characters-And-Objects/battle-units.md))

**Movement and pathfinding** (explained on [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [party data](../Party/party-data.md), [party slots](../Party/party-slots.md))

**Party**

| Function | | Functions |
|---|---|---|
| `0x00226BE0` | calls | `0x00263750`, `0x003590D0` |
| `0x00263050` | calls | `0x003590D0` |
| `0x00263230` | calls | `0x003590D0` |
| `0x0026D6F0` | calls | `0x003590D0` |
| `0x003589B0` | is called by | `0x00269C70`, `0x00326500`, `0x00353530`, `0x0050C610`, `0x0050D2F0` |
| `0x003590D0` | is called by | `0x00263770`, `0x00269C70`, `0x00327270`, `0x003272A0`, `0x003272F0`, `0x003273B0` |

**Party** (explained on [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md), [party verbs](party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [player movement](../Movement-And-Pathfinding/player-movement.md))

**Party** (explained on [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [reward verbs](reward-verbs.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md))

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x003589B0` | is called by | `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690`, `0x00506700` |
| `0x003590D0` | is called by | `0x003A4290`, `0x003A56F0`, `0x003F1A60`, `0x00426090`, `0x004264A0`, `0x004640A0`, `0x004643D0`, `0x00464650`, `0x00464BD0`, `0x00465120`, `0x00465690`, `0x0046CC70` |

**Graphics** (explained on [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md), [effect element runtime](../Graphics/effect-element-runtime.md), [effect element types](../Graphics/effect-element-types.md), [battle numbers](../Menus-And-HUD/battle-numbers.md))

**Graphics** (explained on [hud](../Menus-And-HUD/hud.md), [authored presentation commands](../Graphics/authored-presentation-commands.md), [legacy ps2 gs layer](../Graphics/legacy-ps2-gs-layer.md), [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md))

**Saving, loading and settings** (explained on [script name bindings](script-name-bindings.md))

| Function | | Functions |
|---|---|---|
| `0x00314A60` | calls | `0x002EF2B0` |

**Menus and HUD** (explained on [party list](../Menus-And-HUD/party-list.md), [battle units](../Characters-And-Objects/battle-units.md))

| Function | | Functions |
|---|---|---|
| `0x003590D0` | is called by | `0x00299BD0`, `0x002C7660` |

</details>
