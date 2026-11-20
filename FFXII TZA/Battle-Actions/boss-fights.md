[Home](../../README.md) / [Battle actions](README.md) / Boss fights

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Boss fights: enemy groups, the group-defeated signal, the battle freeze, the exit lock and the boss gauge | system | Battle actions | How an action runs | How a boss or story fight is built from script pieces rather than one flag - enemies put into numbered groups, the signal that wakes the script when a whole group is defeated, the input lock and battle freeze around the aftermath, the commands that remove grouped or ungrouped enemies, the exit lock that stops zone exits, and how the boss gauge relates to the groups. | 0x00239710, 0x00306E60, 0x00306F00, 0x00307030, 0x00307090, 0x00238B70, 0x00238AE0, 0x00264830 |

## What the player sees

A boss or story fight is not marked by one setting. The area's script builds it from separate pieces:

- **The boss is an enemy in a numbered group.** Ordinary enemies are in group 0. When every member of
  a group has been defeated, the game locks the controls, freezes the battle and, for groups set up
  for it, records the group number where the area's script can read it.
- **The battle freeze** is also switched on and off by the script commands `suspendbattle` and
  `resumebattle`, which far more scripts use than have boss fights, so it is not a boss marker on its
  own.
- **Exits.** A script can lock the zone exits; the exit triggers then do nothing.
- **The boss gauge** is opened by the script. Almost every script that opens it also puts an enemy in
  a group.
- **Which fight it is** follows from the area and the story counter ([Story
  progress](../Story-Events-And-Hunts/story-progress.md)). The script of `grm_g01`, for one, switches on the
  counter when the area starts, and after the win it sets the counter to 33 before it leaves the map.

## How it works

### Joining a group

The script command `btlAtelSetEventFlagGroup(group, mode)` reaches `0x00239710(actor, mode, group)`
through its handler `0x0050F8C0`. It stores the group number in the unit's byte `+0xE98`, sets bit `0x1` of
`+0xE99` for mode 1 and bit `0x2` for mode 2 (clearing them otherwise), and calls
`0x00306E60(unit, 1)`¹. It returns -1 when the actor has no battle unit² and 0 otherwise³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023973A`-`0x00239770` |
| ² | `0x0031B760`, `0x0023972C` |
| ³ | `0x0023977A` |

</details>

`0x00306E60(unit, add)` works only for a non-null enemy-side unit (stats `+0x05` = 1) with a group. It takes the
unit's slot from `0x002360D0(unit+0x40, 0x00263D30(actor))`: the slot byte that the actor's lane maps to, any value
but `0xFF`¹, and a negative result returns². It sets (`add` = 1) or clears (`add` = 0)
that slot's bit in the group's member mask, and clears it in the group's defeated mask.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002360EF` |
| ² | `0x00306EB0` |

</details>

The bit is `1 << (slot & 31)` shifted in 32 bits and sign-extended¹, so
slots 32 and above share the bit of `slot & 31` and slot 31 covers the bits under mask `0xFFFFFFFF80000000`.
The group's entry is
`0x02EC13C0 + (group - 1) * 0x18`: the member mask at `+0x00`, the defeated mask at `+0x08` and a pending
flag at `+0x10` (bit `0x1`). The index `group - 1` has no range test against the 64 entries².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00306ECE`, `0x00306ED4`, `0x00306EE7` |
| ² | `0x00306EB2`-`0x00306EC3` |

</details>

### A member is defeated

`0x00306F00(unit)` sets the unit's slot bit in the defeated mask¹, past the same gates and slot
resolution as `0x00306E60`: a null unit, a null stats record or one whose byte `+5` is not 1, a group byte of 0
or a negative slot returns 0². When the defeated mask covers the member
mask, the group is complete, and it returns 1 after the steps below³; otherwise it
returns 0⁴. On completion it:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00306F78` |
| ² | `0x00306F09`-`0x00306F55` |
| ³ | `0x00306FF2`, `0x0030701C` |
| ⁴ | `0x00306F88` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | calls `0x00307140(1)`: ten `0x002E1C20(0xC, n)` calls, which set the bit values `0x1`, `0x8`, `0x10`, `0x20`, `0x40`, `0x80`, `0x100`, `0x800`, `0x1000` and `0x100000` (mask `0x1019F9`) of row 12 at `0x0215F1F0`, then `0x00359200(1, 2)`, `0x00359330(2, 1, 1)` and `0x0026BD20(2, 0)`; | `0x00307160`-`0x003071BE` |
| 2 | calls `0x00238B70(1)` and `0x00238AE0(1)`, the battle freeze (below); |   |
| 3 | with bit `0x1` of `+0xE99` (mode 1), clears unit bit `0x800000000000`, sets the group's pending flag and posts event `0x2005`; otherwise sets unit bit `0x800000000000` and posts event `0x2008`. |   |

### The group-defeated signal

The frame orchestrator calls `0x00307030`¹. When `0x00233D20()` allows it, every pending group
has its flag cleared and its number passed to `0x0026ADC0(3, group)`, which stores it in word 3 of the
array that actor manager 0 points to at `+0x58`², when that manager is active (bit `0x1` of
`0x02098E20`). `0x00307090` zeroes both masks of all 64 entries and clears their pending flag bit `0x1`
(`and byte ptr [...], 0xFE`, `0x003070A0`-`0x003070CB`), leaving the flag byte's other bits;
it is called by the area initialisation³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00234717` |
| ² | `0x02098E68` |
| ³ | `0x0023442D` |

</details>

### Removing enemies

The script command `bosskillall` reaches `0x00234880`, which removes (`0x00300E40(unit, 0)`) every
enemy-side unit with a group (`+0xE98` not 0). `zakokillall` reaches `0x00237690` (through the stub `0x00473B10`), which removes every
enemy-side unit in group 0.

### The battle freeze

`0x00238B70(on)` sets or clears bit `0x20` of the battle flags `0x02089340` and, through `0x002E7C10`, clears the aim of
every unit with bit `0x10` of its first byte that passes the checks of `0x002E7C10` ([character rig and
look](../Graphics/character-rig-and-look.md#solve-bodies)); `0x002E7C10` never reads the `0x30B` that
`0x00238B70` passes as its third argument.
`0x00238AE0(on)` sets or clears bit `0x80`. The script commands `suspendbattle` (`0x0035AB20`: both on, then `0x0035A590`)
and `resumebattle` (`0x0035A6F0`: `0x00473830(0, 1)`, both off, `0x00267D40(2)`) use the same pair.

While bit `0x20` is set, a running action is cancelled with reason 2 ([Target selection](target-selection.md)) and
idle units are not sent back to choose actions ([Action commit](action-commit.md)).

`0x00473830(value, mode)` takes the manager from `0x00263FF0(0)` and returns at once when bit `0x1` of the manager's byte
`+0x10` is clear¹. Otherwise it walks the indices from the manager's word `+0x1DE` up to, not
including, that word plus its word `+0x1D6`, and asks `0x00358940(manager, index)` for each record². A record whose qword `+0x30` is null is passed over³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0047383E`-`0x0047384C` |
| ² | `0x00473853`-`0x00473879`, `0x004738AD`-`0x004738B2` |
| ³ | `0x00473881`-`0x00473886` |

</details>

With mode 1 every such record gets `0x0023A120(record, value)`. With mode 0 a record gets that call only when
`0x00263BE0(record)` answers 0 or 2¹. Any other mode calls nothing for the
records². The answer of `0x00358940` is used with no null test³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00473888`-`0x0047388A`, `0x00473893`-`0x004738A8` |
| ² | `0x0047388C`-`0x00473891` |
| ³ | `0x00473881` |

</details>

### The exit lock

`lockmapjump`¹ sets bit `0x4` of byte `+0x200` of the running actor manager²;
`unlockmapjump`³ clears it. `0x00264830` returns 1 when any of actor managers 0-2 (`0x288` apart
from `0x02098E10`) has bit `0x1` of `+0x10` and that bit. The script command `sysucoff` polls it
(`0x00346A60`, setting its result to 1 at `0x00346A8E`), and an exit trigger that gets 1 from `sysucoff`
does not jump.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0034AD70` |
| ² | `0x002640C0` |
| ³ | `0x0034B1C0` |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

In the 1,114 `us` scripts:

| Fact | Count |
|---|---:|
| `btlAtelSetEventFlagGroup(0, 0)` calls | 6,206 |
| calls with group 1 (modes 0, 1, 2) | 438, 74, 13 |
| calls with groups 2-5 (in 5 scripts) | 15 |
| scripts that put an enemy in a group 1-5 | 235 |
| scripts that call `bossgaugeopen` | 162 |
| of those, also putting an enemy in a group 1-5 | 160 (not `lus_a02`, `lus_b01`) |
| scripts that call `suspendbattle` / `resumebattle` | 532 / 470 |
| scripts that call `lockmapjump` | 68 |
| of those, also putting an enemy in a group 1-5 | 19 |
| `mapjump(12)` exit entries | 1,525 |
| of those, calling `sysucoff` and branching on its result | 1,525 |
| of those, calling `sysucoff` before any other command | 1,457 |

</details>

## Related

- [Quickenings and summons](quickenings-and-summons.md) - another script-visible battle state.
- [Target selection](target-selection.md) - the cancel reasons, including the battle freeze.
- [Action commit](action-commit.md) - the idle-unit queue the freeze stops.
- [Group completion and respawn](../Enemy-Spawning/enemy-respawning.md)
  - the spawn side of the groups.
- [The R2 modal toggle](../Controls-And-Input/escape.md) - the FLEEING mode, which
  boss fights do not switch off.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 11 calls with 4 other topics</summary>

**Enemy AI and gambits** (explained on [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [glossary](../Engine-Core/glossary.md), [area of effect](area-of-effect.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031B760`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) | is called by | [`0x00239040`](../Party/party-table.md) Battle unit: select ai order set variant from authored unit (on party table)<br>[`0x003014C0`](../Enemy-AI-And-Gambits/gambits.md) Ai order: evaluate and resolve action target (on gambits)<br>[`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x003087E0`](area-of-effect.md) Ai order: select final target from candidates (on area of effect)<br>[`0x0030F130`](../Party/party-slots.md) Ai order: build candidate target buffer from stored range and status (on party slots) |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263BE0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |
| [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x002E09A0`](../Menus-And-HUD/menus.md) (on menus) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x002623A0`](../Engine-Core/frame-update-order.md) (on frame update order) |

</details>
