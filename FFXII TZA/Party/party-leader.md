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
  areas whose town flag is set waive this ([Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).
- Scripts lock the stick (`setuclockstatus`) or only moving, turning or heading
  (`setucpcmovelockstatus`), and the controls lock when the last member of an enemy group falls
  ([Boss fights](../Battle-Actions/boss-fights.md)).

Who you control is saved as a member number in the party block. Each party refresh turns that number, or a mode's own
choice such as the chocobo, into the one leader the game reads, and every follower's place in the formation is worked
out from that leader each frame.

## How it works

### The leader handle

The leader is one actor handle, `0x022C7FE0`. `0x003272A0` turns it into the leader's battle unit, or no unit: the battle
flag `0x02089340` bit `0x10` must be set, the handle must resolve to an actor with a battle unit, and the unit's flag bit
`0x8` must be set (`0x003272A4`-`0x003272CE`).

Twenty-five functions call `0x003272A0` for the leader's battle unit. Of the 82 call sites of `0x003590D0`, which
returns the handle, eight more go straight on to `0x003588B0` and `0x00263E30` for that actor's unit. Six make
the same three tests inline (`0x00317E60`, `0x00319090`, `0x00319490`, `0x0031ACC0`, `0x0031E630`, `0x00329220`), and
`0x00326BB0` and `0x00326D60` make the first two and take the unit with no test of its bit `0x8`
(`0x00326CDA`-`0x00326D1A`, `0x00326DA2`-`0x00326DC9`).

The lock setters below and the release `0x00358B40` resolve the handle `0x022C7FE0` to its actor directly, without
those three tests.

Two more readers keep only the bit `0x10` test. `0x00327270` returns the leader's actor (`0x003590D0()` through
`0x003588B0`), or no actor while bit `0x10` is clear (`0x00327274`-`0x0032728D`). `0x003272F0` returns the leader's
roster slot, the first of slots 0-3 whose `0x00263750` actor is that actor, or -1 when bit `0x10` is clear,
the handle does not resolve or no slot holds it (`0x003272F6`-`0x0032734E`).

### Changing the leader

A change is a request and a later commit:

1. `0x003594B0(handle)` stores the handle at `0x022C7FE4` and the request kind 1 at `0x022C7FF8` (`0x003594B0`-`0x003594B6`).
2. `0x00358BC0`, once a frame, commits a pending request (`0x00358BC4`-`0x00358C52`). When the handle differs from the
   leader, the old leader is released (`0x00358B40`) and camera context 0 is re-seated with `0x0025A680`, or
   `0x0025A690` for request kind 2 or no previous leader, after `0x00259800(0)` (`0x00358BFC`).
3. The handle `0x022C7FE4`, re-read after the release, becomes the leader, the kind returns to 0, and the new
   leader's actor gets its animation mode set by `0x002681D0`, which writes it to the body's `+0x80` and the
   controller's `+0x153` (`0x002682A7`, `0x002682B5`), when the handle resolves to one (`0x00358C49`). A
   request for the current leader skips the release and the camera calls of step 2 and still does this
   (`0x00358BE4`).

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
   animation mode through `0x002681D0` (`0x0050C62C`-`0x0050C65D`).

`0x00237F40`, run by `0x0025C830` (`0x0025D41F`) and `0x0026C3E0` (`0x0026C59E`), replaces a fallen leader through the
first of them. It does nothing while bit `0x200` or bit `0x400` of `0x02089340` is set, or while the leader `0x003272A0` has unit
bit `0x4` and a stats record whose status words `+0x64` | `+0x3C` are clear of KO, Stone and X-Zone (`0x80000003`),
or carry them while `0x00377C20()` holds.

Otherwise it lists fighting seats 0-3 with `0x0030A880(list, 3)`: units
standing (or with `0x00377C20()`), of kind `+0x05` 0 and type `+0x04` below 7. The first becomes the selector
`+0x5AA4` through `0x00327810`, which then runs `0x00326500`.

A summon goes the same way: the summon arm of `0x00306760` passes the summoner to `0x00327810` (`0x0030696F`), so the
summoner becomes the controlled member ([Quickenings and summons](../Battle-Actions/quickenings-and-summons.md)).

`0x00327810(unit)` writes byte `+4` of the unit's `+0x698` record, or `0xFF` for a null unit or record, zero-extended
into the dword at `[0x02EBF190] + 0x5AA4`, and `0x00327850(sel)` writes the low byte of `sel` there the same way
(`0x00327813`-`0x00327836`, `0x00327857`-`0x0032785A`).

Six instructions store the selector by its displacement `0x5AA4`, and `0x00326500` runs right after each: those two,
`0x00327870(seat)`, which stores the selector held in seat `seat` of map 0, or `0xFF` when `0x00322C50(0x17, seat, 0)`
refuses the seat (`0x00327879`-`0x003278AF`), `0x003220E0` (`0x00322173`), `0x00326620` (`0x003266A3`) and the new-game fill
`0x00329CC0` (`0x00329DC2`). No other store has that displacement.

`0x003220E0(actor)` stores only when the actor's handle, taken before `0x002659D0(actor)` runs, is that of the selector's
unit (`0x00327150`); it stores the actor's own selector, found again from its handle, while bit `0x10` of `0x02089340` is
set, and `0xFF` when that bit is clear or the actor, its unit or its record is missing (`0x0032211F`-`0x00322173`).

Whole-block writes also reach it ([Party data](party-data.md)): the reset `0x002370C0` clears it with `memset`
(`0x002370D3`), `0x002EF5F0` and `0x002EF650` clear the image that holds the block (`0x002EF603`, `0x002EF663`), and `0x002EF4A0`
copies a loaded block's first `0x6000` bytes back over it (`0x002EF4A0`-`0x002EF504`).

### The default controlled member

`0x00326500` turns the party's leader selector, `+0x5AA4` of the party block ([Party slots](party-slots.md),
[Party data](party-data.md)), into the leader handle. The member it
picks depends on the party control mode (`0x00326516`-`0x00326542`):

| Party control mode | Member |
|---|---|
| 0 and 1 (normal, summon) | the party block's leader selector, `+0x5AA4` |
| 2 (chocobo) | party row 26, the chocobo |
| 3 (town) | the area's default leader, `0x00377C70` |
| 4 and 5 (event party) | no member, so the fallback below |

When that member has no battle unit with a stats record, it takes the first of fighting seats 0-3 that has one,
and otherwise the actor in roster slot 0 (`0x00326571`-`0x003265D9`).

Before the pick it runs `0x00311E20` and `0x00326620` (`0x0032650C`, `0x00326511`). `0x00326620` acts in mode 0 only:
when the selector `+0x5AA4` is `0xFF` or not among seats 0-3 of slot map 1 (`+0x5A5A`), it sets the selector to
the row of the first unit `0x0030A880(list, 3)` returns and runs `0x00326500` again (`0x00326626`-`0x003266A9`). In mode
1 a member picked from the selector or the seats also goes through `0x00317400(unit)` (`0x003265FE`-`0x0032660B`), and
`0x00311E20` runs again before the request (`0x003265DB`).

### The roster

The four active actors are pointers at `0x0209A1F0`; `0x00263750(slot)` returns one for slots 0-3 and no actor above
(`0x00263750`-`0x00263766`); the compare is unsigned, so a negative slot gives no actor too. `0x00269C70(actor, slot)` installs an actor in a slot, clearing the actor's previous slot, recording the slot in the
actor's byte `+0x12`, and requesting it as leader when no leader is set ([Party slots](party-slots.md)).

### The follow formation

`0x00338490` places every follower each frame (`0x003385CD`-`0x00338686`). It walks fighting seats 0-3 (`0x0031B810`) and
skips a member that is missing, down (KO, Stone or X-Zone), or the leader itself. Each follower gets an entry in
the four 0x60-byte formation slots at `0x022C7E00`, keyed by its unit's slot byte `+0xEA9`, with its angle around
the leader.

The pass runs in this order:

1. It returns at once when `0x00383C80()` answers 0 (`0x003384D5`-`0x003384DC`). The leader is the answer of
   `0x003272A0()`; its position comes from `0x002646C0` on its actor `+0x10` and its heading from `0x00265200`.
   With no leader or no actor the position is the constant `0x008C5FD0` (0, 0, 0, 1.0) and the heading 0
   (`0x00338513`-`0x0033857C`).
2. Each follower's slot `+0x20` is the answer of `0x004687F0` for the vector `0x00203080` makes from the slot's
   position and the leader's, handed on through `0x0033CB70` and raised by 2π when negative
   (`0x00338634`-`0x0033866B`). With no follower the pass ends here (`0x00338694`-`0x00338697`).

   The slot's position `+0x10` is stored just before: the follower's position from `0x002646C0`, or
   the constant `0x008C5FD0` when its unit has no actor (`0x00338608`-`0x0033863F`).
3. The reference angle is the leader's heading plus π, brought into 0 to 2π (`0x003386C0`-`0x00338854`).

   When `0x003135C0()` answers non-zero it is instead the `0x004687F0` answer, brought into the same
   range, for the vector `0x00203080` makes from the three floats at `+0x30` of the block `0x00202C70`
   fills from the answer of `0x0032A690()` and the leader's position, the first less the second as in
   step 2. `0x00338490` makes no store to the fourth float of the first vector (`0x003386CD`-`0x00338711`).
4. Each filled slot's `+0x24` takes its `+0x20` less the reference angle, brought into -π to π
   (`0x00338860`-`0x003388D6`). The sort that never swaps follows.
5. The spread angle plus `0x022C7DF0` is the step. Two bounds are set for the angles still free: with one
   follower, reference + step to reference + 2π - step, or reference + 140 degrees to reference + 2π -
   140 degrees (`0x00D10AF8`) when `0x003135C0()` answers non-zero; with two, reference + 15 degrees to
   reference + 2π - 15 degrees (`0x00D10AD4`); with any other count, reference to reference + 2π
   (`0x00338CC6`-`0x00338D39`).
6. Then each filled slot is taken in turn. Its angle is `+0x24`, raised by 2π when negative, plus the
   reference (`0x00338D68`-`0x00338DED`, `0x00338F19`). The stay test of step 7 is passed over for a unit whose
   qword `+0x708` is not 0 and whose order `+0x714` is not `0x4021` (`0x00338E06`-`0x00338E1C`).
7. Stay test: the follower keeps its place, and slot `+0x30` and `+0x40` take its own position, when
   `r + f + 0.1 + 0.5` is above `0x004686D0(slot position, leader position)` and `0x0033A3D0` of the same
   two answers non-zero; r is the answer of `0x00309AE0()` and f the larger of its actor's two
   `0x00265090` floats, or 0 when the unit has no actor (`0x00338E22`-`0x00338E9B`).

   `0x00265090` fills the two floats only for an actor whose byte `+3` has `0x60` under mask `0xE0`
   (`0x00265090`-`0x00265098`); for any other actor they are what the stack held. The same holds where
   steps 9 and 12 use it.
8. Otherwise it tries `trunc(π / step)` angles: the slot's angle, then one step below, one above, two
   below, two above and so on, each held inside the two bounds (`0x00338EEC`-`0x00338F67`).

   The point for an angle is built by `0x00203170`, `0x00202F00` with the angle, `0x00202B70` with the vector
   `0x01F004C0` (0, 0, 1.0, 1.0 in the image), `0x00202FE0` with the answer of `0x00309AE0()` and `0x00202B10`
   with the leader's position (`0x00338FCF`-`0x0033901D`).
9. A point is refused when the search of step 10 finds a blocking object, when
   `0x0033D3E0(point, leader position, 2)` answers 1, when `0x00391410(point, point, a)` answers
   non-zero, when `0x00384130` of the point's first and third floats answers `0xFF`, or when
   `0x00336390(point, radius, 1)` answers 0 (`0x0033920A`-`0x00339282`).

   The radius is the larger of the follower's two `0x00265090` floats, and a is the first of the two
   alone, the one returned through `rdx` (`0x0033903C`-`0x00339059`, `0x00339233`). A follower whose unit is
   null or has no actor takes the first point without any of the tests of steps 9 to 11
   (`0x00339022`-`0x00339036`).
10. The search runs only when `0x002EA7F0` answers non-zero for the follower's own object, which
    `0x0031ABE0` gives for the dword `+8` of `0x00236820(slot byte)` (`0x00339051`-`0x00339079`). It is
    `0x00391D10(sphere, list, 0x20, 0x1C)` with the point and the radius, or `0x003920F0` when a coordinate
    of the point is not a number (`0x0033907F`-`0x00339119`).
11. Of the objects found, the follower's own is ignored, and so is one whose unit's `+0xE68` record has
    `(byte +0x18 >> 1) & 7` equal to 1 while the follower's has 4. An object is tested further when it
    has no unit, when the follower is an enemy record (stats byte `+5` = 1) whose `0x00263C20` is not 3,
    or when its unit is an enemy record whose `0x00263C20` is not 3.

    It is blocking when `0x00314EB0(own, object)` is not 0 and `0x00313F80(own, object, out)` is outside 1 to
    3 (`0x00339130`-`0x003391FC`).
12. The first point not refused goes to slot `+0x30` and `+0x40` (`0x0033932E`-`0x0033933B`). When every
    try is refused, or the count of tries is 0, both take the leader's position and `+0x50` the answer
    of a second `0x00309AE0()` (`0x003392D5`-`0x00339327`). Before that `0x00203080`, `0x00309AE0()`, `0x004692F0`
    and `0x00202B10` build a point from the slot's position and the leader's that the slot does not
    take (`0x003392DE`-`0x00339311`).

    In the other two cases `+0x50` takes the larger of the leader actor's two `0x00265090` floats, or 0
    without one (`0x00338E9F`-`0x00338ED9`, `0x0033933F`-`0x0033937C`).
13. After each slot the bounds close in by one step around the angle A it used. For a slot whose `+0x24`
    is not negative the lower bound becomes at least A + step and the upper at most A + 2π - step;
    for a negative one the lower becomes at least A - 2π + step and the upper at most A - step
    (`0x00339381`-`0x003393DC`).

`0x00339A60(unit)` returns a follower's destination (`0x00339A70`-`0x00339AC1`). It gives no destination when there is no
leader, when the unit is the leader, or when the leader is an enemy-table record, and otherwise finds the unit's entry
by its slot byte. So every follower follows the controlled character, and nobody has to be told when the leader
changes.

Its second argument `out` takes the result. With an entry it copies the slot's three vectors from `+0x30` and
returns 1 (`0x00339B27`-`0x00339B53`). Otherwise it returns 0 and writes the unit's own position (`0x002646C0` on its
actor `+0x10`) to `out + 0x00` and `out + 0x10`, and to `out + 0x20` the larger of the actor's two `0x00265090`
radii plus 0.1 (`0x00339AC3`-`0x00339B22`, `0x00339B62`-`0x00339BDB`). With no unit or actor the position is zero and
`out + 0x20` is 0.1.

### When control is taken away

`0x0023B040` recomputes the control lock once a frame (`0x0023B050`-`0x0023B1FA`). Battle flag `0x02089340` bit `0x40` raises
every lock bit, and nothing waives it (`0x0023B050`-`0x0023B063`).

The rest comes from the leader's state, and is skipped when the party control mode is chocobo (`0x00303EC0`) or
the area's town bit is set (`0x00377C20`, through its thunk `0x00313F60`; `0x0023B065`-`0x0023B079`), or when there is
no leader unit (`0x003272A0`, `0x0023B08F`); a skipped derivation publishes the start value. The lock is raised when the
leader is down, when a party wipe is latched
(battle flags `0x600`), on several of the leader's action and status states (`0x0023B0CA`-`0x0023B179`), and in
summon mode when the summoner is down (`0x0023B17C`-`0x0023B1B8`). It is published three ways:

| Lock bit | Published to | Effect |
|---|---|---|
| `0x1` | `0x022C8000` bit `0x2` (`0x00359200(on, 1)`, `0x0023B1D2`-`0x0023B1DC`) | the stick's speed is forced to 0 |
| `0x4` | `0x022C8005` bit `0x2` (`0x003592C0(1, on)`, `0x0023B1C0`-`0x0023B1CD`) | the controlled actor is not turned to the stick |
| `0x2`, inverted | `0x0209A2C5` (`0x0026BD40`, `0x0023B1E1`-`0x0023B1FA`) | read by the gameplay capability checks |

The full list of contributions, how each lock bit is published, and the readers and writers of `0x0209A2C5` are
under [The locks](../Movement-And-Pathfinding/player-movement.md#the-locks) in Player movement.

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
| `0x022C8007` | nobody | no setter: it is read with the others, and only the reset `0x003590E0` clears it (`0x00359115`-`0x00359122`) |

Any bit of `0x022C8000` stops the stick. Of the OR of the four bytes, bit `0x1` stops the move, bit `0x2` the turn to the
stick and bit `0x4` the desired heading (`0x00358DFB`-`0x00358E99`). A setter stops the leader's actor at once
with `0x0026D6D0`: `0x00359200` whenever the dword it leaves is non-zero (`0x00359221`-`0x00359242`), the byte setters
`0x00359250`, `0x003592C0` and `0x00359330` only when the OR of the four bytes they leave has bit `0x1`
(`0x0035927D`-`0x003592AD`, `0x003592ED`-`0x0035931D`, `0x00359353`-`0x00359387`); a turn or heading lock alone does not
stop it.

The event lock also
clears capability byte `0x0209A2C6` while it stands (`0x003071DC`-`0x003071F2`, `0x0026BD20`).

`0x022C8000`-`0x022C800F` is the movement suppression block: at `+0x0` the dword of lock bits, set and cleared by
`0x00359200`; at `+0x4` the four lock bytes; at `+0x8` the stick magnitude `m = sqrtf(x * x + y * y)`, capped at
128 and divided by 128, as an `f32`: `[0x022C8008] = min(128.0, m) * 0.0078125`, with `x` one stick byte less 128
and `y` 128 less the other (`0x0035957F`, `0x003595A7`; `minss`, then `mulss` by 1/128, `0x003595CA`-`0x003595DF`); and at
`+0xC` the walk toggle (`0x003594E0`; both on [Player movement](../Movement-And-Pathfinding/player-movement.md)).

The reset `0x003590E0` clears the dword and the four bytes (`0x0035910F`, `0x00359115`-`0x00359122`).

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

- The readers of the leader on this page all start from the handle `0x022C7FE0`: through `0x003272A0`, through
  their own copy of all or some of its tests, or directly. So changing `0x022C7FE0` through the request and
  commit is enough for the formation, the camera and the controls to follow.
- A new lock source needs its own bit or byte; clearing someone else's bit releases their lock too.

## Related

- [Party slots](party-slots.md) - the seats and the fighting map the formation walks.
- [Party members](party-members.md) - joining and leaving.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe latches.
- [Party control modes](../Engine-Core/party-control-modes.md) - summon, chocobo and
  town modes.
- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md) - the town bit.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat: `0x00263E30` is called by `0x003206E0`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
- Save load settings: `0x002EF650` is called by `0x00280140`; those functions are documented on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md).
- Save load settings: `0x002EF650` calls `0x00238A80`, `0x00253A80`, `0x002EF2D0`; those functions are documented on
  [item and ability ids](../Engine-Core/item-and-ability-ids.md),
  [frame update order](../Engine-Core/frame-update-order.md).
