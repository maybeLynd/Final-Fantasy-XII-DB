---
title: "Actor model rebuild: the state machine that reloads an actor's model, attachments and body for its current definition, and what runs it"
kind: "system"
category: "Characters and objects"
addresses: "0037B4D0, 0037B4C0, 00377DB0, 02ADD0D8, 002EBB80, 002E96B0, 002E96D0, 0031C250, 0031BEC0, 0031BE30, 002EB7A0, 002EAE20, 002EB540, 002E9810, 002E97C0, 002E4C20, 002E4C30, 002E3DC0, 002E3F00, 002EBD60, 002E3C20, 002E3110, 002E28E0, 002EBC90, 0031C540, 0026D610, 00321380, 002E8450, 0036EC10, 0036F0F0, 0036ECA0, 002ED910, 022D9AB0, 022D9AE0, 00320170, 002EB9D0, 002EB490, 002EC6B0, 0037CB90, 00377A90, 0031BAC0, 00233AD0, 002DEBD0, 002DEB90, 0037C730, 0037C980, 0037CA00, 0037CA80, 0037CB50, 0037C1A0, 0037CE80, 0037C8D0, 003523B0, 005101B0, 00359880, 02EBF3D0, 02EBF3F0, 0034E3E0, 00233AA0, 0031C2F0, 00233CF0, 0037CF50, 00510160, 00342C90, 0037CFD0, 0037CB80, 0037CB10, 002EA6A0, 002E8FD0, 022C8010, 00359800, 00359A30, 0035A0A0, 0035A240, 002E6090"
---

## What the player sees

When a character joins, leaves or changes job, or a battle starts, each party member briefly
vanishes, its model, held items and body are swapped for the ones its current definition calls
for, and it reappears in place. A scene waits while `partyallread` runs. The frames the member is
invisible are the loads this machine waits on.

## How it works

### The rebuild record

The machine `0037B4D0(record)` (thunk `0037B4C0`) works on a 12-byte record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | actor, as an encoded image pointer (0020E620 / 0020E600) |  |
| `04`<sub>h</sub> | `u32` | handle of the binding entry being waited on |  |
| `08`<sub>h</sub> | `u8` | state 0..23 in bits 0-6; bit 7 = place the actor at the end |  |
| `09`<sub>h</sub> | `i8` | party slot, -1 for none |  |
| `0A`<sub>h</sub> | `u8` | pass counter for states 13-15 |  |
| `0B`<sub>h</sub> | `u8` | saved value of 002DEBD0(), restored by 002DEB90 at the end |  |

Every transition keeps bit 7 and writes the new state. A call runs states until one has to wait
(return 0) or state 23 is reached (return 1). An actor that no longer resolves returns 1 at once,
and nothing runs while `00377DB0()` (the byte `02ADD0D8`) is 0.

### The states

Binding entries, handles, the ready bit and the lane tests are those of
[script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md). A part id is the one
`0031BEC0(actor, part, n)` returns, mapped through `002EB7A0`; a value of 0 or less means none.

States 2, 8, 11 and 14 resolve their handle first, and a handle that no longer resolves is requested
again from the current definition (`002EAE20(id, 0)`) without advancing. State 20 waits on its
handle as it is, and state 17 waits on the lane with no recovery: `002E4C30` returns −1 once the lane
record is gone or its stamp differs, so neither wait can end after its target is retired.

| State | What it does | Next |
|---|---|---|
| 0 | hides the actor (`002EBB80(actor, 0)`) | 1 |
| 1 | compares the actor's bound id (`002E96B0`, context `+04`<sub>h</sub>) with the id its definition calls for (`0031C250`, then `002EB7A0`) | 3 when equal; 22 when the new id is negative; else 2 |
| 1 (changed) | when the old id is 0 or more: `0025AB30(actor)`, releases the old main entry (`002EBD60(id, 0)`, `002E3F00(id, lane)`, `002E3DC0(id)`) and each attached part whose id will change; then sets actor `+23`<sub>h</sub> bit 0 and requests the new id | 2 |
| 2 | waits for the main entry; then `002EBC90(actor, 0, 0)`, the variant bytes from `0031C540(unit)` (1 and 0 when it fails) into `0026D610`, the bind `002E28E0`, `002681D0`, `002E5C70` with the three floats at `[actor + B8h]`, `002EAC90`, `002E49B0(actor, 0)`, `002E4A40`, `002E8450(actor, 00321380(unit) or 0)` | 3 |
| 3 | — | 4 |
| 4 | releases the actor's pool entry at `+20`<sub>h</sub> (`0036EC10`), looks up the new pool id (`002ED910`) and acquires an entry (`0036F0F0`) into `+20`<sub>h</sub>; a negative id leaves the released index in `+20`<sub>h</sub>, so the next rebuild releases it again | 5; 7 when the id is negative |
| 5 | waits until the pool entry's state byte is 3 (`0036ECA0`) | 6 |
| 6 | — | 7 |
| 7-9 | part 0 in the slot at context `+30`<sub>h</sub>: when its id changes, detaches it (`002E3C20(actor, 0, 0)`) and releases the old entry; a new id is requested (actor `+23`<sub>h</sub> bit 1), waited on, and attached (`002EBC90(actor, 2)`, `002E3110(actor, 0, 0, entry)` with link `0031BE30`) | 10 |
| 10-12 | the same for part 1 in the slot at `+60`<sub>h</sub> (bit 2, `002E3110(actor, 1, …)`) | 13 |
| 13-15 | the same for part 8, entry n, in the slot at `+C0h + n × 30h` (bit `n + 3`, `002EBC90(actor, n + 4, 0)`, `002E3110(actor, 3, n, …)`), run for n = 0 and 1 with the counter `+0A`<sub>h</sub> | 16 |
| 16 | the motion lane: `00320170` gives the lane the definition calls for; when it is valid, claimable (`002EB9D0`) and differs from context `+12`<sub>h</sub>, it calls `002E6BB0(actor, 1)`, stores it (`002EC6B0`) and requests it (`002EB490`) | 17; 18 otherwise |
| 17 | waits until the lane is loaded (`002E4C30` > 0) | 18 |
| 18 | `002EAC90`, `002E8450(actor, 00321380(unit) or 0)`, and `002699D0` in read-in mode | 19 |
| 19 | the body replacement: `0037CB90(id, 002657E0(actor), 00263FC0(actor))`; a replacement is found or created with `002EB540(id, 0)` | 20; 22 when there is none |
| 20 | waits, then `002EBC90(actor, 3, 1)`, `002E3110(actor, 4, 0, entry)`, `002EAC90` | 21 |
| 21 | — | 22 |
| 22 | places the actor when record bit 7 is set and the slot is not negative; shows it (`002EBB80(actor, 1)`), `00233AD0(actor)`, `00263560()` for a slot, `00359B10()`, restores `002DEB90(+0Bh)` | 23 |
| 23 | done | returns 1 |

`0031C250` takes the definition's selector: for an actor in roster slots 0-3 the byte at
`[02EBF190] + 5A90h + slot × 2` (`FFFF`<sub>h</sub> when `00322C50(17h, slot)` fails or the byte is `FF`<sub>h</sub>),
otherwise word `+4` of the unit's record `+698`<sub>h</sub> (`FFFF`<sub>h</sub> without one). `0031C2F0` maps it to a
model id: `FFFF`<sub>h</sub> gives −1; a high byte of 0 gives the dword at `+70`<sub>h</sub> of the `02EBF130` row for
the low byte (bounded by `00322C50(2, ·)`); a high byte of 1 goes through the `02EBF120` row's
first byte to a `02EBF150` row's first dword; anything else gives −1.

`0026D610(actor, b, c)`, the store of state 2's variant bytes, jumps to `002E6090` for a class-3
actor, which writes `b` and `c` to `[actor + C0h] + 14Ch` and `+14D`<sub>h</sub> when the context exists.

`002EBB80(actor, on)` is the hide and show: for an actor of kind `60`<sub>h</sub> with a context it writes
context `+10`<sub>h</sub> bit `8`<sub>h</sub> and refreshes visibility (`002E8FD0`), which shows the model when
`+10h & Bh` is `B`<sub>h</sub>, or `+10h & 3` is 3 when context `+11`<sub>h</sub> bit `20`<sub>h</sub> is set, together with
`+11h & 6` = 6 and `+164`<sub>h</sub> = 0. An actor with `+11`<sub>h</sub> bit `20`<sub>h</sub> set is therefore not hidden by
state 0.

In read-in mode (`02EBF3FC` = 1) the release paths of states 1, 7, 10 and 13 also call `002E42D0`,
and placement also calls `002E8060` and `002EB030(actor, 1001h)`.

The pool of state 4 is two arrays of `18`<sub>h</sub>-byte entries: 2 at `022D9AB0` and 4 at `022D9AE0`,
chosen by `002647C0(00264EC0(actor))`. Each entry holds a state byte `+0`, two index bytes `+1`
and `+2`, two load handles `+C`<sub>h</sub> and `+10`<sub>h</sub>, the id `+14`<sub>h</sub> and a count `+16`<sub>h</sub>.

`0036F0F0`
returns an entry already holding the id with its count raised, or takes the first entry whose count
is 0, frees its old loads (`001DC100`, `00369800`) and starts the new one (`0036ED50`); it returns
`(+2 << 4) | +1`, or −1 when every entry is in use. `002ED910` takes the id from `003212E0` and
otherwise from word `+6` of the model's `002ED950` row.

Placement (state 22) reads the base position and facing from `00377A90` and asks `0031BAC0` for the
slot's position; when that fails it offsets x by ±1.0 (slot bit 0) and z by ±1.0 (slot bit 1). It
then calls `002681D0`, sets the position (`0026AF80`), the facing and movement heading from
`00377A90` even when `0031BAC0` supplied the position (`0026B620`, `0026A0D0`), the
separation weight from `00265950` (`0026DAC0`), and calls `002EAC90`, `002ECA00(actor, 1)`,
`002E49B0(actor, 0)` and `002E4A40`.

### What runs it

| Runner | Record | How |
|---|---|---|
| `partyallread` (`3EB`<sub>h</sub>, begin `0034CCD0` → `0037C980`) | `02EBF3F0` | a scheduled task (`002F16B0`) with callback `0037C730`, slots 0 to 3, read-in mode 1 |
| `partyallread2` (`46F`<sub>h</sub>, `0034D8B0`) and `summontopartyread` (`207`<sub>h</sub>, `0034FE80`) → `0037CA00` | `02EBF3F0` | the same task, slots 3 down to 0, mode 1 |
| `summonread` (`203`<sub>h</sub>, `0034E1F0`) and `0031A300`, `00324380`, `003261D0`, `003273D0` → `0037CA80` | `02EBF3F0` | slots 0 to 3, mode 0 |
| the world tick `00314020` → `0037C1A0` | `02EBF3D0` | each slot set in the mask `02EBF3E0`, one at a time (`02EBF3DE` holds the slot in progress); a slot whose actor does not resolve or is not ready when reached (`002EA6A0`: actor `+4` = 1 and the main entry's ready bit) is removed from the mask without a rebuild |
| `setupbattle` (`56`<sub>h</sub>) poll `003523B0` | the verb's | `0037CE80` fills the record with bit 7 set and the verb's slot, then the machine runs each frame |
| `btlAtelSetUnit` (`3001`<sub>h</sub>), begin `00510160`, poll `005101B0` | the verb's | the begin applies the unit (`0023A3B0`) and, when `00237650(actor)` is non-zero, fills the record with `0037CF50` (slot −1, bit 7 clear); the poll runs the machine while `00237650` stays non-zero |
| the scene step `00359880` | `022C8018` | for each scene actor with `+14`<sub>h</sub> bit 7 set, `002647B0` = 0 and context `+11`<sub>h</sub> bit 0, `0037CE80(record, actor, −1)` and the machine |

`0037C730` fills the record for the current slot (actor from `00263750`, state 0, bit 7 clear,
counter 0, `+0B`<sub>h</sub> from `002DEBD0`, `002DEB90(1)`, actor `+23`<sub>h</sub> = 0), runs the machine until it
returns 1, adds the step to the slot, and repeats until `0037CB50` reports the walk finished (slot 4
or more going up, below 0 going down). It then calls `00233AA0` (`0030D8B0(1)`, `00326500`,
`00311E10(0)`, `00311E20`) and clears the task pointer `02EBF400`.

The read-in verbs' poll `0034E3E0`, shared with `summonreadsync` (`0204`<sub>h</sub>) and
`summontopartyreadsync` (`0208`<sub>h</sub>), waits while `0037CB50` reports a walk in progress (its third
caller is `00324360`); `partyallread`'s result `0034D460` is `003601C0(13h)`, which clears busy
bit 19.

Every launcher calls `00233CF0` (`0030D8B0(0)`, `003266C0`, `00311E10(1)`), the counterpart of
`00233AA0`, and none tests `02EBF400` first: a read-in started while one runs replaces the task
pointer, and both tasks share the record `02EBF3F0`. `0037C730` clears `02EBF400` on the call after
the one that runs `00233AA0`.

The world tick's mask is set by `partystdmotionrecover` (`014C`<sub>h</sub>): its begin `00342C90` raises busy
bit 18 (`003601B0(12h)`) and sets `02EBF3E0` to `F`<sub>h</sub> when it is 0 (`0037CFD0`); its poll `00342F50`
waits while the mask is non-zero (`0037CB80`). `0037CB10` (from `00266D10`) clears the mask and
`02EBF3DE`.

Placement needs record bit 7 and a slot of 0 or more. The task, the world tick and `0037CF50` fill
the record with bit 7 clear, so they rebuild without moving the actor. `0037CE80` sets bit 7 and
clears context `+11`<sub>h</sub> bit `1`<sub>h</sub>; `setupbattle` passes its slot, so its members are placed, while
the scene step passes slot −1, which skips placement.

### Dispose and recover

The scene step is the last phase of the pair of verbs `disposeentry` (`006B`<sub>h</sub>) and `recoverentry`
(`006C`<sub>h</sub>), which take down and bring back the models of manager 0's battle-eligible actors. They
share the `i16` state word `022C8010`, which the world tick advances once per frame through
`00359800` (called at `00314282`):

| State | Set by | What the tick does |
|---|---|---|
| 0 | `0035A240`, and the scene step when its walk ends | nothing |
| 1 | the `disposeentry` begin `00344EA0` through `0035A640`, only from state 0 | `00359A30`, below, which ends in state 2 |
| 2 | `00359A30` | nothing |
| 3 | the `recoverentry` begin `00345A30` through `0035A660`, only from state 2 | zeroes `022C8024` and `022C8028`, enters state 4 and starts the `entryread` task (`0037C910(0)`), and in the same tick continues as state 4 |
| 4 | the tick | waits until the task pointer `02ADD968` is null (`0037CB40`), then enters state 5 and runs the scene step at once, in the same tick |
| 5 | the tick | the scene step `00359880` |

`00359A30`, the disposal:

1. sets battle flags `02089340` bit 5 (`00238B70(1)`, which also calls `002E7C10(actor, actor,
   30Bh, 0)` for every unit in use with flag bit 4) and bit 7 (`00238AE0(1)`);
2. releases each record of manager 0's ordinal window (first `+1DE`<sub>h</sub>, count `+1D6`<sub>h</sub>, only while bit `1`<sub>h</sub>
   of `+10`<sub>h</sub> is set) that holds a unit at `+30`<sub>h</sub> (`0035A590`: `0026D6D0`, `00233F50(record, 1)`, `002ED020`);
3. clears the keep bit `10`<sub>h</sub> of `+19`<sub>h</sub> in all 128 binding entries (`002E63D0`) and zeroes dword
   `+40`<sub>h</sub> of the 32 lane records (`002E6570`);
4. for every record of slot 0 with `+14`<sub>h</sub> bit 7 and a tag of 4 or more (`002647B0` = 0), takes its
   readiness `002EA6A0` and releases its model with the per-`+04`<sub>h</sub> teardown `0025AB30`; context
   `+11`<sub>h</sub> bit 0 records that readiness, and is cleared for every other record.

The scene step walks slot 0's records one per pass with the counter `022C8028`, rebuilding each
record whose `+14`<sub>h</sub> bit 7 is set, whose tag is 4 or more and whose context `+11`<sub>h</sub> bit 0 was set
at disposal, one machine run at a time (`022C8024` = 1 while one runs, 2 when the walk is done).

The begins store 1 for an accepted call and 0 (dispose) or -1 (recover) otherwise. The
`disposeentry` poll `003453D0` holds an accepted call until the state reads 2, 3 or 5
(`0035A0A0`); the `recoverentry` poll `00346020` holds an accepted call while it does, so it
returns once the walk is back at 0. Both write `022C253D` = 1 (`00314D40`) while they hold.
`0035A240` clears the state from the slot-0 bind's field reset `0026DB30`, from `002695A0` and
from `00266D10`.

## Layouts

```python
rebuild record  +0 u32 encoded actor, +4 u32 pending handle, +8 u8 state | 0x80 place, +9 s8 slot, +0xA u8 pass, +0xB u8 saved byte
read-in record  02EBF3F0 (+0xC 02EBF3FC mode, +0xD 02EBF3FD step, +0xE 02EBF3FE slot, +0x10 02EBF400 task)
tick record     02EBF3D0 (02EBF3DE slot in progress, 02EBF3E0 slot mask)
actor           +0x20 s8 pool entry, +0x23 u8 parts requested (bit 0 main, 1 part 0, 2 part 1, 3-4 part 8)
pool entry      022D9AB0 (2) / 022D9AE0 (4), 0x18 each: +0 state (3 loaded), +1, +2 index bytes, +0xC, +0x10 loads, +0x14 id, +0x16 count
```

## Shipped data

| Verb | Uses in the US scripts |
|---|---|
| `setupbattle` | 2,948 |
| `partyallread` | 1,045 |
| `summontopartyread` / `summontopartyreadsync` | 202 / 202 |
| `summonread` / `summonreadsync` | 13 / 13 |
| `partystdmotionrecover` | 29 |
| `partyallread2` | 0 |

## Operations

Per actor: one main load, up to one pool load, up to four part loads, one lane load and one body
load, each waited on for as many frames as it takes; a read-in walk does this for four slots in
turn.

## State

The two static records `02EBF3D0` and `02EBF3F0`, the task pointer `02EBF400`, the tick slot mask,
the actor's `+20`<sub>h</sub> and `+23`<sub>h</sub> bytes, and the pool entries.

## Modding notes

- An actor that stays invisible after a read-in verb is stuck in a wait state (2, 5, 8, 11, 14, 17
  or 20); byte `+8` of `02EBF3F0` names it. States 17 and 20 cannot recover once their target is
  retired.
- Changing a party member's definition does not change its model by itself; one of the runners
  above has to run the machine.
- `partyallread` rebuilds the party in place; only `setupbattle`'s run moves members to their slot
  positions.
- Starting a second read-in while one runs replaces the first task's pointer; both walk the same
  record.

## Related

- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the binding entries, handles, lanes and attach slots this machine drives.
- [Party verbs](../Scripts-And-Script-Commands/party-verbs.md): the verbs that change the party and wait on the read-in.
- [Actor record fields](actor-record-fields.md): the actor bytes this machine writes.
