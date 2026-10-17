---
title: "Party leader: switching who you control, why the others follow at once, where they walk, and when control is taken away"
kind: "system"
category: "Party"
addresses: "003272A0, 003594B0, 00358BC0, 00326500, 00263750, 00338490, 00339A60, 0023B040, 00359200, 00359250, 003592C0"
---

## What the player sees

- Switching to another character takes effect at once, and the others immediately follow the new leader.
- The members who are not controlled walk in a formation around the leader.
- While the leader is KO'd, turned to stone or in X-Zone, the stick stops responding until the leader recovers;
  some areas waive this.
- Some scenes lock the stick, or parts of steering, on purpose.

## How it works

### The leader handle

The leader is one actor handle, `022C7FE0`. `003272A0` turns it into the leader's battle unit, or none: the battle
flag `02089340` bit 4 must be set, the handle must resolve to an actor with a battle unit, and the unit's flag bit
3 must be set (`003272A4`-`003272CE`). Every reader of the leader's battle unit asks `003272A0`; the lock setters
below and the release `00358B40` resolve the handle `022C7FE0` to its actor directly, without those three tests.

Two more readers keep only the bit-4 test. `00327270` returns the leader's actor (`003590D0()` through
`003588B0`), or none while bit 4 is clear (`00327274`-`0032728D`). `003272F0` returns the leader's
roster slot, the first of slots 0-3 whose `00263750` actor is that actor, or -1 when bit 4 is clear,
the handle does not resolve or no slot holds it (`003272F6`-`0032734E`).

### Changing the leader

A change is a request and a later commit:

1. `003594B0(handle)` stores the handle at `022C7FE4` and the request kind 1 at `022C7FF8` (`003594B0`-`003594B6`).
2. `00358BC0`, once a frame, commits a pending request (`00358BC4`-`00358C52`). When the handle differs from the
   leader, the old leader is released (`00358B40`) and camera context 0 is re-seated with `0025A680`, or
   `0025A690` for request kind 2 or no previous leader.
3. The handle `022C7FE4`, re-read after the release, becomes the leader, the kind returns to 0, and the new
   leader's actor gets its roster-role notice (`002681D0`).

Kind 2 comes only from the script verb `205`<sub>h</sub> `changetosummonparty`, which raises a pending request's kind
(`003594C0`-`003594D3`). Between request and commit every reader still sees the old leader, so the formation
follows the new one from the frame of the commit.

### Who asks for a new leader

Three functions call `003594B0`:

1. `00326500` picks the default controlled member and requests it (`003265F6`). The party refreshes call it
   (`00326620`, `003266C0`, `00327850`, `00327870`, `00329CC0`).
2. `00269C70` requests the actor it installs in a roster slot when no leader is set (`00269D34`).
3. The developer verb `2021`<sub>h</sub> `debug_setpc` (`0050C610`) installs an actor in a roster slot. For slots 0-3 it
   requests the actor, commits at once through `00358BB0`, re-seats the camera with `0025A690` and sends the
   roster-role notice `002681D0` (`0050C62C`-`0050C65D`).

`00237F40`, run by `0025C830` (`0025D41F`) and `0026C3E0` (`0026C59E`), replaces a fallen leader through the
first of them. It does nothing while bit 9 or bit 10 of `02089340` is set, or while the leader `003272A0` has unit
bit 2 and a stats record whose status words `+64`<sub>h</sub> | `+3C`<sub>h</sub> are clear of KO, Stone and X-Zone (`80000003`<sub>h</sub>),
or carry them while `00377C20()` holds.

Otherwise it lists fighting seats 0-3 with `0030A880(list, 3)`: units
standing (or with `00377C20()`), of kind `+05`<sub>h</sub> 0 and type `+04`<sub>h</sub> below 7. The first becomes the selector
`+5AA4`<sub>h</sub> through `00327810`, which then runs `00326500`.

### The default controlled member

`00326500` turns the party's leader selector into the leader handle; [Party slots](party-slots.md) and
[Party data](party-data.md) call the selector at `+5AA4`<sub>h</sub> of the party block "the leader" too. The member it
picks depends on the battle mode (`00326516`-`00326542`):

| Battle mode | Member |
|---|---|
| 0 and 1 (normal, summon) | the party block's leader selector, `+5AA4`<sub>h</sub> |
| 2 (chocobo) | party row 26, the chocobo |
| 3 (town) | the area's default leader, `00377C70` |
| 4 and 5 (event party) | none, so the fallback below |

When that member has no battle unit with a stats record, it takes the first of fighting seats 0-3 that has one,
and otherwise the actor in roster slot 0 (`00326571`-`003265D9`).

### The roster

The four active actors are pointers at `0209A1F0`; `00263750(slot)` returns one for slots 0-3 and none above
(`00263750`-`00263766`); the compare is unsigned, so a negative slot gives none too. `00269C70(actor, slot)` installs an actor in a slot, clearing the actor's previous slot, recording the slot in the
actor's byte `+12`<sub>h</sub>, and requesting it as leader when no leader is set ([Party slots](party-slots.md)).

### The follow formation

`00338490` places every follower each frame (`003385CD`-`00338686`). It walks fighting seats 0-3 (`0031B810`) and
skips a member that is missing, down (KO, Stone or X-Zone), or the leader itself. Each follower gets an entry in
the four `60`<sub>h</sub>-byte formation slots at `022C7E00`, keyed by its unit's slot byte `+EA9`<sub>h</sub>, with its angle around
the leader.

`00339A60(unit)` returns a follower's destination (`00339A70`-`00339AC1`). It gives none when there is no leader,
when the unit is the leader, or when the leader is an enemy-table record, and otherwise finds the unit's entry by
its slot byte. So every follower follows the controlled character, and nobody has to be told when the leader
changes.

### When control is taken away

`0023B040` recomputes the control lock once a frame (`0023B050`-`0023B1FA`). Battle flag `02089340` bit 6 raises
every lock bit, and nothing waives it (`0023B050`-`0023B063`).

The rest comes from the leader's state, and is skipped when the battle mode is chocobo (`00303EC0`) or the area's
town bit is set (`0023B065`-`0023B079`). The lock is raised when the leader is down, when a party wipe is latched
(battle flags `600`<sub>h</sub>), on several of the leader's action and status states (`0023B0CA`-`0023B179`), and in
summon mode when the summoner is down (`0023B17C`-`0023B1B8`). It is published three ways:

| Lock bit | Published to | Effect |
|---|---|---|
| 0 | `022C8000` bit 1 (`00359200`) | the stick's speed is forced to 0 |
| 2 | `022C8005` bit 1 (`003592C0`) | the controlled actor is not turned to the stick |
| 1, inverted | `0209A2C5` (`0026BD40`) | read by the gameplay capability checks |

The full list of contributions, and the gameplay checks that read `0209A2C5`, are on
[Gameplay capability policy](../Controls-And-Input/action-availability.md).

### The movement locks

The stick filter reads one dword and four bytes, and each source of a lock owns its own bit or byte
(`00358DAA`, `00358DDF`-`00358DF4`):

| Lock | Owner | Setter |
|---|---|---|
| `022C8000` bit 0 | script `setuclockstatus` | `00347E14` |
| `022C8000` bit 1 | the leader's state, above | `0023B1DC` |
| `022C8000` bit 2 | the event lock `00307140` | `003071C7` |
| `022C8000` bit 3 | actor manager slot 3 loaded | `0026CC81`-`0026CCBA` |
| `022C8004` | script `setucpcmovelockstatus` | `00359250` |
| `022C8005` | the leader's state, above | `003592C0` |
| `022C8006` | the event lock, bit 1 | `00359330` |
| `022C8007` | nobody | none: it is read with the others, and only the reset `003590E0` clears it (`00359115`-`00359122`) |

Any bit of `022C8000` stops the stick. Of the OR of the four bytes, bit 0 stops the move, bit 1 the turn to the
stick and bit 2 the desired heading (`00358DFB`-`00358E99`). A setter that leaves a lock standing stops the
leader's actor at once with `0026D6D0` (`00359221`-`00359242`, `0035927D`-`003592AD`). The event lock also
clears capability byte `0209A2C6` while it stands (`003071DC`-`003071F2`, `0026BD20`).

## Modding notes

- Every reader of the leader asks `003272A0`, so changing `022C7FE0` through the request and commit is enough for
  the formation, the camera and the controls to follow.
- A new lock source needs its own bit or byte; clearing someone else's bit releases their lock too.

## Related

- [Party slots](party-slots.md) - the seats and the fighting map the formation walks.
- [Party members](party-members.md) - joining and leaving.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe latches.
- [Battle mode](../Engine-Core/party-control-modes.md) - summon, chocobo and
  town modes.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the town bit.
