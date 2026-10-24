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
flag `0x02089340` bit `0x10` must be set, the handle must resolve to an actor with a battle unit, and the unit's flag bit
`0x8` must be set (`0x003272A4`-`0x003272CE`). Every reader of the leader's battle unit asks `0x003272A0`; the lock setters
below and the release `0x00358B40` resolve the handle `0x022C7FE0` to its actor directly, without those three tests.

Two more readers keep only the bit `0x10` test. `0x00327270` returns the leader's actor (`0x003590D0()` through
`0x003588B0`), or none while bit `0x10` is clear (`0x00327274`-`0x0032728D`). `0x003272F0` returns the leader's
roster slot, the first of slots 0-3 whose `0x00263750` actor is that actor, or -1 when bit `0x10` is clear,
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
first of them. It does nothing while bit `0x200` or bit `0x400` of `0x02089340` is set, or while the leader `0x003272A0` has unit
bit `0x4` and a stats record whose status words `+0x64` | `+0x3C` are clear of KO, Stone and X-Zone (`0x80000003`),
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

`0x0023B040` recomputes the control lock once a frame (`0x0023B050`-`0x0023B1FA`). Battle flag `0x02089340` bit `0x40` raises
every lock bit, and nothing waives it (`0x0023B050`-`0x0023B063`).

The rest comes from the leader's state, and is skipped when the battle mode is chocobo (`0x00303EC0`) or the area's
town bit is set (`0x0023B065`-`0x0023B079`). The lock is raised when the leader is down, when a party wipe is latched
(battle flags `0x600`), on several of the leader's action and status states (`0x0023B0CA`-`0x0023B179`), and in
summon mode when the summoner is down (`0x0023B17C`-`0x0023B1B8`). It is published three ways:

| Lock bit | Published to | Effect |
|---|---|---|
| 0 | `0x022C8000` bit `0x1` (`0x00359200`) | the stick's speed is forced to 0 |
| 2 | `0x022C8005` bit `0x1` (`0x003592C0`) | the controlled actor is not turned to the stick |
| 1, inverted | `0x0209A2C5` (`0x0026BD40`) | read by the gameplay capability checks |

The full list of contributions, and the gameplay checks that read `0x0209A2C5`, are on
[Gameplay capability policy](../Controls-And-Input/action-availability.md).

### The movement locks

The stick filter reads one dword and four bytes, and each source of a lock owns its own bit or byte
(`0x00358DAA`, `0x00358DDF`-`0x00358DF4`):

| Lock | Owner | Setter |
|---|---|---|
| `0x022C8000` bit `0x1` | script `setuclockstatus` | `0x00347E14` |
| `0x022C8000` bit `0x2` | the leader's state, above | `0x0023B1DC` |
| `0x022C8000` bit `0x4` | the event lock `0x00307140` | `0x003071C7` |
| `0x022C8000` bit `0x8` | actor manager slot 3 loaded | `0x0026CC81`-`0x0026CCBA` |
| `0x022C8004` | script `setucpcmovelockstatus` | `0x00359250` |
| `0x022C8005` | the leader's state, above | `0x003592C0` |
| `0x022C8006` | the event lock, bit `0x2` | `0x00359330` |
| `0x022C8007` | nobody | none: it is read with the others, and only the reset `0x003590E0` clears it (`0x00359115`-`0x00359122`) |

Any bit of `0x022C8000` stops the stick. Of the OR of the four bytes, bit `0x1` stops the move, bit `0x2` the turn to the
stick and bit `0x4` the desired heading (`0x00358DFB`-`0x00358E99`). A setter that leaves a lock standing stops the
leader's actor at once with `0x0026D6D0` (`0x00359221`-`0x00359242`, `0x0035927D`-`0x003592AD`). The event lock also
clears capability byte `0x0209A2C6` while it stands (`0x003071DC`-`0x003071F2`, `0x0026BD20`).

`0x022C8000`-`0x022C800F` is the movement suppression block: at `+0x0` the dword of lock bits, set and cleared by
`0x00359200`; at `+0x4` the four lock bytes; at `+0x8` the stick magnitude, capped at 128 and divided by 128, as an
`f32` (`0x003595DF`); and at `+0xC` the walk toggle (`0x003594E0`; both on
[Player movement](../Movement-And-Pathfinding/player-movement.md)). The reset `0x003590E0` clears the dword and the
four bytes (`0x0035910F`, `0x00359115`-`0x00359122`).

The event lock goes up when the last member of an enemy spawn group falls: the group's death handler `0x00306F00`
calls `0x00307140(1)` once the defeated mask covers the member mask (`0x00306F95`-`0x00306F9A`;
[Boss fights](../Battle-Actions/boss-fights.md), [Enemy respawning](../Enemy-Spawning/enemy-respawning.md)).

## State

Each pass of `0x00338490` first marks all four formation slots empty with `0xFF` in their first byte
(`0x00338590`-`0x003385B4`), then gives each follower the next slot: the unit's slot byte `+0xEA9` at `+0x00`, its
position at `+0x10`, its angle around the leader at `+0x20` and the unit at `+0x28` (`0x0033863F`-`0x0033867C`).
Bytes `+0x01`-`+0x0F` of each slot are read and written by no function on their own; the exchange sort's swaps, which
never run, move them inside their 16-byte copies of the slot's first vector (`0x00338969`, `0x00338980` and the other
four swap bodies). Nothing fixes their width.

It then runs an exchange sort over the filled slots (`0x003388E1`-`0x00338C10`) whose every test compares the float at `+0x24`
with itself (`comiss xmm0, xmm0`, then `jbe`, at `0x00338960`, `0x003389D3`, `0x00338A44`, `0x00338ACF`, `0x00338B94`), so it
never swaps two entries. `0x00339A60` finds a unit's slot by comparing the first bytes with its slot byte (`0x00339A9D`-`0x00339AC1`).

The followers are spread around the leader by an angle that depends on the party: 30 degrees when `0x003135C0`
answers non-zero, otherwise 25, 50 or 40 degrees for one, two or three followers (`0x00338C19`-`0x00338C4C`). The
global `0x022C7DF0` is added to it (`0x00338CBC`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C7DF0` | `f32` | 0 | the random part of that angle: `rand() % 50` tenths of a degree, in radians (`0x00338C59`-`0x00338CA1`), drawn again on each pass in which every follower's committed order `+0x714` is the wait `0x4021` (`0x00338600`-`0x00338617`, `0x00338C54`), and kept from the last such pass otherwise | `0x00338490` (`0x00338CA1`) | `0x00338490` (`0x00338CAB`) |
| `0x022C7DF4` | `i32` | 0 | set to 0 each time the random part is drawn; nothing reads it | `0x00338490` (`0x00338C62`) | no instruction |
| `0x022C7E60` | `u8` | 0 | the slot byte of formation slot 1, `0xFF` when the slot is empty | `0x00338490`: `0xFF` (`0x0033859E`), the follower's slot byte (`0x00338679`); the sort's swaps never run | `0x00339A60` (`0x00339AB4`) |
| `0x022C7EC0` | `u8` | 0 | the slot byte of formation slot 2 | as for slot 1, `0xFF` at `0x003385A7` | as for slot 1 |
| `0x022C7F20` | `u8` | 0 | the slot byte of formation slot 3 | as for slot 1, `0xFF` at `0x003385B4` | as for slot 1 |

No other instruction reaches these globals. The slots' addresses are taken by `0x00338490` and `0x00339A60` only.

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
