---
title: "Party during scenes: hiding the party, the summon leader and followers, summon space, capturing a member and the event party modes"
kind: "system"
category: "Scripts and script commands"
addresses: "0x003415D0, 0x00342250, 0x00341CB0, 0x002ECD50, 0x00352FA0, 0x0034C3D0, 0x00264050, 0x00263750, 0x00262F50, 0x00262F90, 0x002693D0, 0x00266AD0, 0x0035AE10, 0x0034C990, 0x003B6F30, 0x0037D120, 0x00355FE0, 0x00358800, 0x0035AA50, 0x003B6F80, 0x003B6DE0, 0x003B7770, 0x003B8030, 0x003B7A30, 0x003B79D0, 0x02EBCAC0, 0x02EBCC68, 0x0034EB30, 0x01EF2C80, 0x00505240, 0x003B7B00, 0x003B7D80, 0x003B7F40, 0x003B8140, 0x003B8170, 0x003CC2F0, 0x003B7440, 0x003B7E20, 0x003B7BB0, 0x003B7C60, 0x00359B80, 0x00269530"
---

## What the player sees

When a scene starts the party's bodies vanish, and a scene or a summon can take a party member's body over: the
character turns, plays a short motion, and control returns. The same "take over the body" step happens on a small
scale every time the player talks to a townsperson or opens a door.

## How it works

### Hiding the party

`hideparty` (`0x0147`, `0x003415D0`) and `showparty` (`0x0148`, `0x00342250`) call `0x002ECD50(actor,
0 or 1)` for party slots 0 to 3 through `0x00263750`; `hideparty_without_uc` (`0x0498`,
`0x00341CB0`) skips the controlled character. `0x002ECD50` acts only on a class-3 actor that is not a
captured member (bind state `+0x18` is not 1, `0x002ECD50`-`0x002ECD54`): it writes bit `0x1` of byte
`+0x10` of the presentation record (`+0xC0`) and refreshes visibility through `0x002E8FD0`. It hides
the body and leaves the actor and its battle unit in place.

`disposepartywithoutcontrol` (`0x0202`, `0x0034C990` → `0x003B6F30`) clears the party-control byte
`0x02B40534`, empties the follower list (`0x003B6DE0`), narrows the controlled set to one actor
(`0x003B6D60`), the actor of the party slot that holds the summoner's row `+0x5AD5` ([party control
modes](../Engine-Core/party-control-modes.md), `0x003B6D69`-`0x003B6D82`), turns its [animation-driven
movement](../Movement-And-Pathfinding/animation-driven-movement.md) off (`0x0026B500`, `0x003B6D9B`) and
sets its `+9` bit `0x4` (`0x003B6DA0`), and snapshots each controlled actor's pose (`0x003B7510`).

`capturepartyforsummon`
(`0x0232`) does the same and binds the set to manager 3's entries (`0x003B72F0`): for entry i of the
second list of the script image's `+0x68` table ([EBP script image](../EBP-Script-Files/ebp-script-image.md))
with a non-negative ordinal, it clears that actor's `+9` bit `0x1` (`0x003B736E`) and has it capture
controlled actor i (`0x00262F50`, `0x003B7375`). `releasepartyforsummon` (`0x0233`) releases them
(`0x003B7AB0`, which does not read the manager slot 3 its handler passes).

`hide_freetarget_group(g)` (`0x04B8`, `0x003569E0`) and `show_freetarget_group(g)` (`0x04B9`,
`0x00356D00`) call `0x0035AA50(0, g, 0 or 1)`. It walks manager 0's ordinal window (first ordinal at
`+0x1DE`, count at `+0x1D6`), skips party members (`0x002647B0`: byte `+0x12` below 4) and passes
every other actor to `0x002ECD50`, all of them for a negative `g`, otherwise only those whose group
`0x00263BE0` returns equals `g`. The group comes from the class nibble `+0x0E`: 0 gives 1, 1, 2 and 7
give 0, 3 gives 2, any other value 1.

### The summon leader and followers

`setupsummonforevent(n)` (`0x0193`, `0x00346FA0`) names a leader: the actor at ordinal `n` of the
current manager, or for a negative `n` the controlled character (`0x003590D0`, `0x003588B0`).
`0x003B6F80(leader)` walks managers 0 and 1 (`0x003B7036`) whose byte `+0x10` has bit `0x1` set and collects,
up to 31, the handles of every actor with byte `+9` bit `0x10` set other than the leader; it clears
`+9` bits `0x4` and `0x10` on every actor it visits and refreshes it (`0x0026D6D0`).

It then hands the list to `0x003B6DE0(leader, count, handles)`. That keeps the requested count (at
most 32) at `0x02EBCC60` and the handles at `0x02EBCBE0`, and resolves each handle (`0x003588B0`). On
each actor that resolves it clears `+9` bit `0x8` and sets bit `0x4`, so a stale mark cannot drop an
actor, and stores it in the slot; a handle that resolves to null leaves that slot's previous
pointer in place.

A second pass keeps each actor once, marking it with `+9` bit `0x8`, and writes the unique ones to the
front of the followers at `0x02EBCAC0` with their count at `0x02EBCBC0`; it reads every slot without a
null check. The leader's handle goes to `0x02EBCC70` and its actor to `0x02EBCC68`. `0x003B6F30` calls
it with an empty list, which is the follower-list clear above.

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `hidenobattletarget` | `0x0196` | `0x00347D80` → `0x003B7770` | for every actor of the managers among 0 to 2 with `+0x10` bit `0x1` set: in each actor's presentation record (`[actor + 0xC0]`, which `0x002E97B0` returns), the leader gets bit `0x2` of byte `+0x10`; any other actor gets that bit from its own `+9` bit `0x4`, or from bit `0x1` of `+0x14F` of the same record; each actor with a presentation record is refreshed (`0x002E8FD0`, which tests bits `0x1`, `0x2` and `0x8` of that byte) |
| `showsummontarget`, `hidesummontarget` | `0x01D8`, `0x01D9` | `0x00342000`, `0x00342320` → `0x003B70B0(1)`, `0x003B70B0(0)` | for each follower, or its capturer (`0x00263F40`), with a presentation record (`0x002E97B0`): sets or clears bit `0x2` of byte `+0x10`, then refreshes visibility (`0x002E8FD0`) |
| `setrotangzxsummonspace(a)` | `0x0199` | `0x00348660` → `0x003B8030` | pops a float and sets it as the heading (`0x0026B620`) of each follower, or of its capturer when the follower is captured (`0x00263F40`) |
| `releaseallforsummon` | `0x019B` | `0x00348DA0` → `0x003B7A30` | runs `0x002693D0(…, 1)` on the leader and on every follower, or on its capturer when it is captured (`0x00263F40`) |
| `summonplaymotionall` | `0x02AB` | `0x0034EB30` (a `jmp`) → `0x003B79D0` | calls `0x0017F5B0(1)` first when `0x022BE970` is non-zero, then `0x002EB030(follower, 0x1049)` for each follower |

`0x0034EB30` is reached through its pointer at `0x01EF2C80`, the result slot of record `0x2AB` in the
family 0 table.

### Moving the group into summon space and back

Each actor keeps a pose snapshot at `+0xED0` of the record its `+0x30` points to (`0x00359B80`, null
when there is none). `duplicatebattletarget` (`0x0194`, `0x003475D0` → `0x003B7440`) fills it for the
leader (`0x003B73B0`) and for every non-null slot of the requested count: the position
(`0x00265020`), the three floats at body `+0x20` (`0x00265240`), the heading (`0x00265200`, body
`+0xA8`), the movement heading (`0x00263CC0`, body `+0xA4`) and the presentation byte `+0x13`
(`0x002E9BE0`).

`setpossummonspace` (`0x0191`, `0x003482E0` → `0x003B7E20`) clears the party-control byte `0x02B40534`,
calls `0x0025A5F0(1)` and `0x0036D840(0)`, and takes as origin the position of the first follower
handle (`0x02EBCBE0`) when the requested count is above 0, otherwise `(0, 0, 0)`. `0x003B7F40(actor,
origin)` then places each follower and the leader, or their capturers (`0x00263F40`).

`0x003B7F40` sets the position (`0x0026B0C0`) to the actor's own x and z minus the origin's, with a
height of 0, or of `0x002ECE50(actor, 0x9000505)` when bit `0x1` of `+0x151` in the actor's `+0xC0`
record is set (`0x002644C0`). It also computes the old height minus `0x00264670(actor)` but never
uses it, so the old height is discarded rather than offset.

It then sets presentation `+0x13` to 1 (`0x002EC680`), sets bit `0x20` of `+0x151` in the `+0xC0` record
(`0x0026ACE0`) and re-applies the render scale (`0x002E4A40`). Last, `0x003B7E20` runs the same motion
step as `summonplaymotionall`: `0x0017F5B0(1)` when `0x022BE970` is non-zero, then
`0x002EB030(follower, 0x1049)`.

`0x003B7B00(actor)` restores one snapshot onto the actor's capturer, or the actor itself: movement
heading (`0x0026A0D0`), heading (`0x0026B620`), position (`0x0026B0C0`), the body `+0x20` floats
(`0x0026B720`), bit `0x20` of `+0x151` cleared (`0x0026ACE0`), presentation `+0x13` from the snapshot
(`0x002EC680`) and the render scale (`0x002E4A40`).

`summongethertarget(d)` (`0x0370`, `0x00340DA0` → `0x003B8140`) pops a float. It first has `0x003B7D80`
put back the body `+0x20` floats from the snapshot of every non-null slot of the requested count,
then calls `0x00505240(count, 0x02EBCAC0, d)` over all the followers. `summongethertarget_one(d)`
(`0x0572`, `0x003410A0` → `0x003B8170`) does the same with a count of 1, the first follower only.

`0x00505240` works from the origin `(0, 0, 0)` on each actor, or its capturer. For an actor at the
origin its reach point is the larger of the two floats `0x00265090` reads, its height (`0x00263940`,
body `+0xC0` × `+0x24`) and 0.

For any other actor `0x003CC130` measures its heading around the
origin, its elevation and its distance, and `0x003CC2F0(origin, 0, elevation, distance)` rebuilds a
point from them (at `0x00505393` its first angle argument is 0). The heading is dropped, so the point
keeps the actor's distance and elevation but not its direction; the larger float and the height
are then added to its x and y.

The reach is that point's distance from the origin (`0x003CC130`). When the largest reach exceeds
`d`, every actor's position and its body `+0x20` floats are multiplied by `d` divided by that
reach (`0x0026B0C0`, `0x00265240`, `0x0026B720`), which draws the group in around the origin.
`0x003CC2F0(origin, a, b, distance, out)` is a shared helper, also used by the camera code: it
builds a rotation from two angles (`0x003CC480`), rotates `(0, 0, distance)` by it and adds the
origin.

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `resumeposbattletarget` | `0x0195` | `0x00347850` → `0x003B7BB0` | raises `0x02B40534`, restores the leader and every slot of the requested count with `0x003B7B00`, calls `0x002E7A10(follower, 0)` for each follower for which `0x002E7600` is non-zero, then `0x0025A5F0(0)` and `0x0036D840(1)` |
| `resumepartyinfo_spattack` | `0x02A4` | `0x0034D330` → `0x003B7C60`, then `0x003B7180` | the same `0x002E7A10` step for the followers, raises `0x02B40534`, and for each actor of the party set at `0x02EBCA80` calls `0x0026B500(actor, 1)` and `0x003B7B00`; then `0x0025A5F0(0)` and `0x0036D840(1)` |

### Capturing a party member

`capturepc(slot)` (`0x0057`, `0x00352FA0`) is how a script on another actor takes a party member's
body. A slot outside 0 to 3 (`0x002647C0` is an unsigned test for below 4) is replaced by byte
`+0x12` of the controlled character's record (`0x00264050(0, −1)` resolves the party-focus handle),
so `capturepc(−1)` means "the character the player controls"; a slot at or above 0 first calls
the town test `0x00377C20` and drops the result. The actor is `0x00263750(slot)`; `0x00262F50(owner, pc)` binds
them and on success the verb returns 1 and cancels the member's battle action (`0x0035AE10`).

`0x00262F90(owner, pc)` binds only when the member's manager is active, neither record is already
bound (`+0x18` is 0) and the two differ: the member gets `+0x18` = 1 with the owner's manager at
`+0x19` and id at `+0x1A`, the owner gets `+0x18` = 2 with the member's; `0x002E4A40(owner)`
re-applies the render scale; the owner copies the member's body pointers (`+0xC0` and `+0xB8`);
`0x002681E0` refreshes both.

`0x002ECCF0(owner, 1)` then sets presentation `+0x11` bit `0x80`.
`capturepc_not_cancelbattlecommand` (`0x0582`) and the by-id form `capturepcbyentryid`
(`0x02A2`, `0x0034C3D0`, which resolves a handle through `0x003588B0`) skip or keep the cancel.

`captureactor` (`0x0366`, `0x00354E10`) captures by name. It reads the issuer's own entry name
(`0x00263A30(manager, ordinal)`: payload plus its `+0x4C` dword plus the first int of the entry's
`+0x40` record,
`"NOACTOR"` when there is none) and has `0x00358800(0, name)` search manager 0's ordinal window for
an entry with the same name, returning its actor from the table at manager `+8`.

When one is found and it is not the issuer, `0x00262F50(issuer, found)` binds them, so a scene's
actor takes over the zone actor of the same name. The bind is also gated on `0x0053DD10(name)`, which
is `mov eax, 1; ret` and always passes. `captureactor_367(name)` (`0x0367`, `0x00355570`) takes the name as a
string operand resolved through `0x002650B0`.

`releasepc` (`0x0058`, a jump into `0x002693D0(owner, 1)`; `releasepc_404` passes a popped flag)
undoes it. For a capturer, `0x002693D0` resolves the member, clears its steering byte, re-applies
the owner's render value, rebuilds the member's four body pointers with `0x00266AD0` from its class
rather than restoring a saved copy, resets its locomotion, and with the flag runs `0x002EB430` (the
idle motion); then both records get `+0x18` = `0xFFFF0000` and a refresh.

`releasepc_battlemember` (`0x057D`, a jump into `0x00269530`) releases every roster member a scene
actor holds: for each of the four roster actors whose `+0x18` is 1 it resolves the owner from
`+0x19` and `+0x1A` (`0x003587C0`) and, when that is another record, runs `0x002693D0(owner, 1)`. It
reads `+0x18` of each roster pointer without testing it for null (`0x00269556`).

### Event party modes

`seteventpartymode(v)` (`0x050F`, `0x0037D120`) writes bit `0x4` of the party block word
`[0x02EBF190] + 0x5B04` and `seteventparty2mode` (`0x0514`) bit `0x8`; `geteventpartymode` (`0x0510`,
`0x00355FE0`) returns whether the mode ladder `0x0030D9A0` reads 4, and `geteventpartymodebit`
(`0x0513`) returns bit `0x4`.

## Layouts

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2EBF190` | `void*` | partyBlock | `+0x5B04` bit `0x4` event party mode, bit `0x8` event party mode 2 |
| `+0x2EBCC68` | `void*` | summonLeader | the leader's actor |
| `+0x2EBCC70` | `u32` | summonLeaderHandle | the leader's handle |
| `+0x2EBCAC0` | `void*[32]` | followers | the unique follower actors |
| `+0x2EBCBC0` | `i32` | followerCount | count of `followers` |
| `+0x2EBCBE0` | `u32[32]` | followerHandles | the handles as passed |
| `+0x2EBCC60` | `i32` | followerRequested | the requested count, at most 32 |

Actor record fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x09` | `u8` | summonFlags | bit `0x1` cleared on a manager-3 actor before it captures a controlled actor (`0x003B736E`), bit `0x4` follower (also set on the summoner's actor by `0x003B6D60`, `0x003B6DA0`), bit `0x8` dedup mark, bit `0x10` follower candidate |
| `+0x18` | `u8` | bindState | 1 captured, 2 capturer |
| `+0x19` | `u8` | otherManager | the bound partner's manager |
| `+0x1A` | `u16` | otherId | the bound partner's id |

PoseSnapshot (at `+0xED0` of the record an actor's `+0x30` points to):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | position | from `0x00265020` |
| `+0x10` | `f32[3]` | bodyVector | body `+0x20` to `+0x28`, from `0x00265240` |
| `+0x24` | `f32` | heading | body `+0xA8`, from `0x00265200` |
| `+0x34` | `f32` | moveHeading | body `+0xA4`, from `0x00263CC0` |
| `+0x64` | `i8` | presentation13 | presentation `+0x13`, from `0x002E9BE0` |

## Shipped data

| Fact | Value |
|---|---|
| `capturepc` uses in the US scripts | 8,353; `releasepc` 8,632 |
| `hideparty` uses | 1,539 |

## Operations

Per capture: one binding write on each record and one action cancel.

## State

The capture bindings in every actor record, the summon leader and follower globals, and the party block mode
word.

## Modding notes

- `capturepc(−1)` always takes the character the player controls; a script that needs a specific
  member passes its slot.
- `hideparty` hides bodies only; the actors keep running and can still be captured.
- `releasepc` rebuilds the body pointers from the record's class, so a capturer that swapped them
  is not restored to a saved state but to the class default.

## Related

- [Event scenes](event-scenes.md): loading, playing and disposing a scene, movies and skips.
- [The world lock](world-lock.md): what holds everyone else still during a talk or scene.
- [Party verbs](party-verbs.md): the summon party switches.
