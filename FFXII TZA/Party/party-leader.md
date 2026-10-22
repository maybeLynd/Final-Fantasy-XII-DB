---
title: "Party leader: switching who you control, why the others follow at once, where they walk, and when control is taken away"
kind: "system"
category: "Party"
addresses: "0x003272A0, 0x003594B0, 0x00358BC0, 0x00326500, 0x00263750, 0x00338490, 0x00339A60, 0x0023B040, 0x00359200, 0x00359250, 0x003592C0"
---

## What the player sees

- Switching to another character takes effect at once, and the others immediately follow the new leader.
- The members who are not controlled walk in a formation around the leader.
- While the leader is KO'd, turned to stone or in X-Zone, the stick stops responding until the leader recovers;
  areas whose town flag is set waive this (`0x00377C20`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).
- Scripts lock the stick (`setuclockstatus`) or only moving, turning or heading
  (`setucpcmovelockstatus`), and the controls lock when the last member of an enemy group falls
  ([Boss fights](../Battle-Actions/boss-fights.md)).

## How it works

### The leader handle

The leader is one actor handle, `0x022C7FE0`. `0x003272A0` turns it into the leader's battle unit, or none: the battle
flag `0x02089340` bit 4 must be set, the handle must resolve to an actor with a battle unit, and the unit's flag bit
3 must be set (`0x003272A4`-`0x003272CE`). Every reader of the leader's battle unit asks `0x003272A0`; the lock setters
below and the release `0x00358B40` resolve the handle `0x022C7FE0` to its actor directly, without those three tests.

Two more readers keep only the bit-4 test. `0x00327270` returns the leader's actor (`0x003590D0()` through
`0x003588B0`), or none while bit 4 is clear (`0x00327274`-`0x0032728D`). `0x003272F0` returns the leader's
roster slot, the first of slots 0-3 whose `0x00263750` actor is that actor, or -1 when bit 4 is clear,
the handle does not resolve or no slot holds it (`0x003272F6`-`0x0032734E`).

### Changing the leader

A change is a request and a later commit:

1. `0x003594B0(handle)` stores the handle at `0x022C7FE4` and the request kind 1 at `0x022C7FF8` (`0x003594B0`-`0x003594B6`).
2. `0x00358BC0`, once a frame, commits a pending request (`0x00358BC4`-`0x00358C52`). When the handle differs from the
   leader, the old leader is released (`0x00358B40`) and camera context 0 is re-seated with `0x0025A680`, or
   `0x0025A690` for request kind 2 or no previous leader.
3. The handle `0x022C7FE4`, re-read after the release, becomes the leader, the kind returns to 0, and the new
   leader's actor gets its roster-role notice (`0x002681D0`).

The commit runs from the main-loop frames `0x0022A770`, `0x0022B8C0` and `0x0022BC20`, which call it through the thunk
`0x00358BB0` (`0x0022AE3C`, `0x0022BAF9`, `0x0022BD49`; [Frame update order](../Engine-Core/frame-update-order.md)).

Kind 2 comes only from the script verb `0x205` `changetosummonparty`, which raises a pending request's kind
(`0x003594C0`-`0x003594D3`). Between request and commit every reader still sees the old leader, so the formation
follows the new one from the frame of the commit.

### Who asks for a new leader

Three functions call `0x003594B0`:

1. `0x00326500` picks the default controlled member and requests it (`0x003265F6`). The party refreshes call it
   (`0x00326620`, `0x003266C0`, `0x00327850`, `0x00327870`, `0x00329CC0`).
2. `0x00269C70` requests the actor it installs in a roster slot when no leader is set (`0x00269D34`).
3. The developer verb `0x2021` `debug_setpc` (`0x0050C610`) installs an actor in a roster slot. For slots 0-3 it
   requests the actor, commits at once through `0x00358BB0`, re-seats the camera with `0x0025A690` and sends the
   roster-role notice `0x002681D0` (`0x0050C62C`-`0x0050C65D`).

`0x00237F40`, run by `0x0025C830` (`0x0025D41F`) and `0x0026C3E0` (`0x0026C59E`), replaces a fallen leader through the
first of them. It does nothing while bit 9 or bit 10 of `0x02089340` is set, or while the leader `0x003272A0` has unit
bit 2 and a stats record whose status words `+0x64` | `+0x3C` are clear of KO, Stone and X-Zone (`0x80000003`),
or carry them while `0x00377C20()` holds.

Otherwise it lists fighting seats 0-3 with `0x0030A880(list, 3)`: units
standing (or with `0x00377C20()`), of kind `+0x05` 0 and type `+0x04` below 7. The first becomes the selector
`+0x5AA4` through `0x00327810`, which then runs `0x00326500`.

A summon goes the same way: the summon arm of `0x00306760` passes the summoner to `0x00327810` (`0x0030696F`), so the
summoner becomes the controlled member ([Quickenings and summons](../Battle-Actions/quickenings-and-summons.md)).

### The default controlled member

`0x00326500` turns the party's leader selector into the leader handle; [Party slots](party-slots.md) and
[Party data](party-data.md) call the selector at `+0x5AA4` of the party block "the leader" too. The member it
picks depends on the battle mode (`0x00326516`-`0x00326542`):

| Battle mode | Member |
|---|---|
| 0 and 1 (normal, summon) | the party block's leader selector, `+0x5AA4` |
| 2 (chocobo) | party row 26, the chocobo |
| 3 (town) | the area's default leader, `0x00377C70` |
| 4 and 5 (event party) | none, so the fallback below |

When that member has no battle unit with a stats record, it takes the first of fighting seats 0-3 that has one,
and otherwise the actor in roster slot 0 (`0x00326571`-`0x003265D9`).

### The roster

The four active actors are pointers at `0x0209A1F0`; `0x00263750(slot)` returns one for slots 0-3 and none above
(`0x00263750`-`0x00263766`); the compare is unsigned, so a negative slot gives none too. `0x00269C70(actor, slot)` installs an actor in a slot, clearing the actor's previous slot, recording the slot in the
actor's byte `+0x12`, and requesting it as leader when no leader is set ([Party slots](party-slots.md)).

### The follow formation

`0x00338490` places every follower each frame (`0x003385CD`-`0x00338686`). It walks fighting seats 0-3 (`0x0031B810`) and
skips a member that is missing, down (KO, Stone or X-Zone), or the leader itself. Each follower gets an entry in
the four 0x60-byte formation slots at `0x022C7E00`, keyed by its unit's slot byte `+0xEA9`, with its angle around
the leader.

`0x00339A60(unit)` returns a follower's destination (`0x00339A70`-`0x00339AC1`). It gives none when there is no leader,
when the unit is the leader, or when the leader is an enemy-table record, and otherwise finds the unit's entry by
its slot byte. So every follower follows the controlled character, and nobody has to be told when the leader
changes.

### When control is taken away

`0x0023B040` recomputes the control lock once a frame (`0x0023B050`-`0x0023B1FA`). Battle flag `0x02089340` bit 6 raises
every lock bit, and nothing waives it (`0x0023B050`-`0x0023B063`).

The rest comes from the leader's state, and is skipped when the battle mode is chocobo (`0x00303EC0`) or the area's
town bit is set (`0x0023B065`-`0x0023B079`). The lock is raised when the leader is down, when a party wipe is latched
(battle flags `0x600`), on several of the leader's action and status states (`0x0023B0CA`-`0x0023B179`), and in
summon mode when the summoner is down (`0x0023B17C`-`0x0023B1B8`). It is published three ways:

| Lock bit | Published to | Effect |
|---|---|---|
| 0 | `0x022C8000` bit 1 (`0x00359200`) | the stick's speed is forced to 0 |
| 2 | `0x022C8005` bit 1 (`0x003592C0`) | the controlled actor is not turned to the stick |
| 1, inverted | `0x0209A2C5` (`0x0026BD40`) | read by the gameplay capability checks |

The full list of contributions, and the gameplay checks that read `0x0209A2C5`, are on
[Gameplay capability policy](../Controls-And-Input/action-availability.md).

### The movement locks

The stick filter reads one dword and four bytes, and each source of a lock owns its own bit or byte
(`0x00358DAA`, `0x00358DDF`-`0x00358DF4`):

| Lock | Owner | Setter |
|---|---|---|
| `0x022C8000` bit 0 | script `setuclockstatus` | `0x00347E14` |
| `0x022C8000` bit 1 | the leader's state, above | `0x0023B1DC` |
| `0x022C8000` bit 2 | the event lock `0x00307140` | `0x003071C7` |
| `0x022C8000` bit 3 | actor manager slot 3 loaded | `0x0026CC81`-`0x0026CCBA` |
| `0x022C8004` | script `setucpcmovelockstatus` | `0x00359250` |
| `0x022C8005` | the leader's state, above | `0x003592C0` |
| `0x022C8006` | the event lock, bit 1 | `0x00359330` |
| `0x022C8007` | nobody | none: it is read with the others, and only the reset `0x003590E0` clears it (`0x00359115`-`0x00359122`) |

Any bit of `0x022C8000` stops the stick. Of the OR of the four bytes, bit 0 stops the move, bit 1 the turn to the
stick and bit 2 the desired heading (`0x00358DFB`-`0x00358E99`). A setter that leaves a lock standing stops the
leader's actor at once with `0x0026D6D0` (`0x00359221`-`0x00359242`, `0x0035927D`-`0x003592AD`). The event lock also
clears capability byte `0x0209A2C6` while it stands (`0x003071DC`-`0x003071F2`, `0x0026BD20`).

The event lock goes up when the last member of an enemy spawn group falls: the group's death handler `0x00306F00`
calls `0x00307140(1)` once the defeated mask covers the member mask (`0x00306F95`-`0x00306F9A`;
[Boss fights](../Battle-Actions/boss-fights.md), [Enemy respawning](../Enemy-Spawning/enemy-respawning.md)).

## Modding notes

- Every reader of the leader asks `0x003272A0`, so changing `0x022C7FE0` through the request and commit is enough for
  the formation, the camera and the controls to follow.
- A new lock source needs its own bit or byte; clearing someone else's bit releases their lock too.

## Related

- [Party slots](party-slots.md) - the seats and the fighting map the formation walks.
- [Party members](party-members.md) - joining and leaving.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe latches.
- [Battle mode](../Engine-Core/party-control-modes.md) - summon, chocobo and
  town modes.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the town bit.
