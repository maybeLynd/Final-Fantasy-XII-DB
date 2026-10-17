---
title: "Party verbs: the eight verbs that change the battle party and the poll they share, the appearance verbs, the standard-motion verbs, and the party queries"
kind: "system"
category: "Scripts and script commands"
addresses: "0034D4E0, 00350CD0, 00350160, 00352AF0, 0034C030, 00352190, 00351A40, 003506A0, 0034CDF0, 0034C370, 003596B0, 0037CB50, 003601B0, 003601C0, 003596D0, 00359BA0, 00359C00, 00359740, 00320800, 0031B510, 00322350, 003271D0, 0033FD60, 00340700, 00341190, 00341B90, 00342360, 00342830, 00342B30, 0031B5A0, 0031B670, 0031B680, 0026AD60, 0026A430, 002EC680, 002ECD80, 002E8730, 0034F060, 0034F890, 00350050, 003507B0, 003580C0, 0035AE10, 00263750, 0034B4B0, 0034F5A0, 00353780, 00353CB0, 00353460, 0034E7D0, 003542C0, 003546F0, 00341E60, 003426F0, 003430C0, 00342280, 003408E0, 00340E00, 003410C0, 00342910, 00342EC0, 0034CCD0, 0034E3E0, 02EBF190, 0037C3C0, 002E6BD0"
---

## What the player sees

A story scene adds a guest to the party, takes a main character away, or lines up exactly the
three members the plot needs; the party's shadows and detail level change for a scene; all four
members strike the same pose at once. Every one of these is a zone script calling a party verb.
The verbs that change who is in the party wait until the engine has rebuilt the actors, which is
why a scene pauses for a moment after a character joins or leaves.

## How it works

### The three party maps

The party block at `[02EBF190]` carries nine two-byte slots per map: map 0 at `+5A48`<sub>h</sub> is the
master the mutators edit, map 3 at `+5A7E`<sub>h</sub> the gameplay roster the party verbs read, map 1 at
`+5A5A`<sub>h</sub> the set combat is servicing, and `+5AA4`<sub>h</sub> the leader's selector (`003271D0`).

Selectors 0 to 6 are the main characters and 7 to
25 guests (`00322350` tests `selector − 7 < 19`). `0031B510` collects the roster's first four
slots from map 3 (an empty slot reads `FF`<sub>h</sub>), `00320800` collects up to nine non-guest selectors
from the whole map, and `00263750(slot)` returns the live actor of roster slot 0 to 3 from the
pointer array at `0209A1F0`.

### Changing the battle party

| Verb | Id | begin | poll | What the begin does |
|---|---|---|---|---|
| `addpartymember(sel)` | `0353`<sub>h</sub> | `0034C030` | `0034C370` | stores the selector; the poll raises busy bit 19 and adds a main character to the reserve (`003172E0`) |
| `removepartymember(sel)` | `0354`<sub>h</sub> | `0034C030` | `0034CDF0` | the poll removes the main character (`00328B20`) and then raises bit 19 |
| `setbattlemember(a, b, c)` | `0355`<sub>h</sub> | `0034D4E0` | `003506A0` | hides the four roster actors, raises bit 19, pops three selectors; when every non-negative one is an available main character (`00359C00` through `0035A050`) the roster is reconciled by `00328DB0`; when the leader (`003271D0`) is not among them the first non-negative selector becomes leader (`00327850`), whatever the reconcile did |
| `removebattlemember(sel)` | `0358`<sub>h</sub> | `00350160` | `003506A0` | only while the roster holds more than one: the member's slot is swapped with the first empty reserve slot (`003286E0`, `00321100`); no empty reserve slot, no change |
| `setbattlememberone(sel)` | `0359`<sub>h</sub> | `00350CD0` | `003506A0` | for a main character in roster slots 0 to 3: every non-guest in slots 0 to 2 other than it is swapped into the first empty reserve slot (`003287A0`); slot 3 and guests stay; one outside the roster has the same done around the roster's first member |
| `setbattlememberlock(sel, on)` | `035A`<sub>h</sub> | `00351A40` | `003506A0` | bit 0 of the member's stats record (`00328FB0`), the pin `setbattlemember` honours |
| `addguestbattlemember(sel)` | `035B`<sub>h</sub> | `00352190` | `003506A0` | hides the roster, raises bit 19, and places a guest absent from map 0 in the highest empty roster slot from 3 down to 1 (`003170E0`, `00326110`), activating it with `00316DF0` |
| `removeguestbattlemember(sel)` | `035C`<sub>h</sub> | `00352AF0` | `003506A0` | removes a guest (`003288F0`) |

Each begin raises busy bit 19 (`003601B0(13h)`) before it touches the party, and the three that
rebuild the roster first hide the four roster actors with `002ECD50(actor, 0)`. Guest and main
selectors are checked by `00322350`: a verb for one kind silently ignores the other.

The guest activation `00316DF0` also grants goods. For a record of type 0 to 6 it adds each of
its five equipment words to the inventory and equips it (`00300B80`, `0030C410`); unless the
record's bit 3 is set it then adds up to ten items with their counts (`00300B80`) and an amount of
gil (`003004B0`) from a row of the party definitions `02EBF130`
([inventory](../Items-Equipment-Shops-And-Licenses/inventory.md),
[gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

`00328DB0(list, 3)` builds a fixed mask from map 1's first four units (a stats record with bit 0,
the lock, or a guest keeps its slot), looks each requested selector up in map 0 (a missing one
returns −1 with nothing applied), treats one already in slots 0 to 2 as fixed, and swaps the rest
into the unlocked slots among 0 to 2 in order; a request that runs past slot 2 also returns −1
with nothing applied. Slot 3 is never filled by it.

Every mutator copies map 0 into the snapshot at `022C2580`, edits the snapshot, and calls
`003261D0(0)`: it compacts slots 0 to 3 and 4 to 8 separately, rebuilds the roster pointer array
(`00269C70`), writes the nine slots back (`00329080`), snapshots the four combat units'
selectors to `022C257C` and starts the read-in task (`0037CA80`). The member verbs therefore do
not need `partyallread`: the read-in the shared poll waits on is started by the mutator.

The shared poll `003506A0` asks `003596B0` whether the party read-in is still pending: the
read-in task's end test `0037CB50` reports done when no task exists (`02EBF400` null) or its slot
cursor `02EBF3FE` has left the roster (past 3 going up, below 0 going down). While pending the
verb keeps waiting; when done the poll clears bit 19 and returns 0. The two per-verb polls
`0034C370` and `0034CDF0` do the add or remove on their first visit (states 0 and 1), then wait
the same way in state 2.

`partyallread` (`03EB`<sub>h</sub>, begin `0034CCD0`) raises bit 19 and starts the read-in task
(`0037C980`); `partyallread2` (`046F`<sub>h</sub>, `0034D8B0` → `0037CA00`) runs it in reverse slot order.
Their poll `0034E3E0` waits on the same end test, calling `00314D40(1)` each frame, and their
result `0034D460` follows
([the read-in state machine](../Characters-And-Objects/actor-model-rebuild.md)).

### The appearance verbs

Seven verbs share one shape: pop a value, collect the members with `0031B670` (selector 0) and
`0031B680` (selector 1), and call one setter on each of up to four in both groups. The collector
`0031B5A0` walks the first four slots of map 1, resolves each selector to a battle unit
(`002367A0`), keeps units with byte `+0` bit 4 whose record at `+698`<sub>h</sub> has byte `+5` clear, and
splits them on whether the record's byte `+4` lies in 7 to 25: selector 1 takes the guests,
selector 0 everyone else. The object handed to the setter is the unit's `+10`<sub>h</sub>, the actor record.

| Verb | Id | Handler | Setter | What it writes |
|---|---|---|---|---|
| `partyusemapid(v)` | `040D`<sub>h</sub> | `0033FD60` | `0026AD60`, then `00265020` and `002E5DF0` | actor byte `+08`<sub>h</sub> bits 1 and 2 as an exclusive pair (bit 1 for non-zero), then re-places the actor at its own position |
| `partyusecharhit(v)` | `040E`<sub>h</sub> | `00340700` | `0026A430` | actor byte `+08`<sub>h</sub> bit 3 and byte `+09`<sub>h</sub> bit 6 to `v != 0` |
| `partysetlod(v)` | `040F`<sub>h</sub> | `00341190` | `002EC680` | presentation byte `+13`<sub>h</sub> = `v`, then the refresh `002E8CE0` |
| `partyshowshadow(v)` | `0410`<sub>h</sub> | `00341B90` | `002ECD80` | presentation byte `+151`<sub>h</sub> bit 3 = `v & 1`, then `002E8FD0`; skipped for a lifecycle byte of 1 or a class other than 3 |
| `partyshowshadow_411()` | `0411`<sub>h</sub> | `00342360` | pushes 1 and jumps into `0410`<sub>h</sub> | |
| `partyhideshadow()` | `0412`<sub>h</sub> | `00342830` | pushes 0 and jumps into `0410`<sub>h</sub> | |
| `setpartyprojectionshadow(v)` | `0413`<sub>h</sub> | `00342B30` | `002E8730` | in the `740`<sub>h</sub>-byte render record at `[022C6F28] + index × 740h` with `+284`<sub>h</sub> set: `+304`<sub>h</sub> bits 12 and 13 become `01` for on and `00` for off, and `+290`<sub>h</sub> bit 22 is set either way |

### The standard-motion verbs

`partystdmotionplay(m)` (`053E`<sub>h</sub>, `0034F060`) pops the motion id and, for each roster slot 0 to
3 with an actor, runs `0035AE10(actor, 1)` (cancel the unit's action, `00233F50`, then
`002ED020`), pushes the motion, the float `−1.0` and the flag 1 back onto the value stack and
calls `003580C0(actor, stack)`. The three siblings differ in two constants: the `withoutsame`
forms (`053F`<sub>h</sub> `0034F890`, `0541`<sub>h</sub> `003507B0`) push the flag 0, and the `_540` forms (`0540`<sub>h</sub>
`00350050`, `0541`<sub>h</sub>) pop a float first and push it instead of `−1.0`.

`003580C0` pops the flag, the float and the motion in that order, resolves the actor's
presentation (`002E97B0`) and its model entry, and when the entry is loaded (`002E4C30`) or no
selector is set, runs `002EAC90(actor)` and then `003DDBB0(actor, slot, motion, float)` for flag 0
or `003DDB40` for flag 1, the two standard-motion starts.

`party_motionsync_and_relax` (`0573`<sub>h</sub>, begin `00342910`, poll `00342EC0`) marks the four roster
slots in the scratch block and, per visit, for each present slot not yet done asks `002673D0` and
`002E7330`; while both answer 0 the verb stays busy, otherwise it plays the idle motion
(`002EB430`) and marks the slot done.

`partystdmotiondispose` (`014B`<sub>h</sub>, a jump into `0037C3C0`) releases the standard motion of the four
roster actors: `002E6BB0(actor, 1)` stops the render record's motion (`00427280`), drops the
actor's motion lane (presentation byte `+12`<sub>h</sub>) from its binding's count and group words
(`002EB890`), queues it for unload when nothing holds it (`002E3F00`), sets the lane byte to
`FF`<sub>h</sub>, and resets the render record's `+42C`<sub>h</sub> and `+430`<sub>h</sub> and clears its `+284`<sub>h</sub> bit 18.

### Queries and captures

| Verb | Id | Handler | Result |
|---|---|---|---|
| `getpartymember(&a … &f)` | `0352`<sub>h</sub> | `0034B4B0` | writes up to six non-guest selectors from the whole map (`00320800`) into six references, `−1` beyond the count; the word it returns is whatever the last store left in the register |
| `getbattlemember(&a … &d)` | `0357`<sub>h</sub> | `0034F5A0` | the four roster selectors (`0031B510`) into four references, `−1` beyond the count; returns the count |
| `isbattlemember(sel)` | `035D`<sub>h</sub> | `00353780` | `003596D0`: whether the selector is in the roster's four slots |
| `ispartymember(sel)` | `035E`<sub>h</sub> | `00353CB0` | a guest is looked up in the roster, a main character among all nine non-guest slots (`00359740`) |
| `isguestbattlemember(sel)` | `035F`<sub>h</sub> | `00353460` | `00322350` |
| `checkbattlemember(a, b, c)` | `0360`<sub>h</sub> | `0034E7D0` | 1 when every non-negative selector is an available main character and the combined mask (`0035A050` over `00359BA0 \| request`) fits the slots the guests leave, else 0 |
| `getpartymembermask` / `getbattlemembermask` | `0361`<sub>h</sub> / `0362`<sub>h</sub> | `003542C0` / `003546F0` | `00359C00` (all non-guests) / `00359BA0` (the roster) as bit masks |
| `getbattlemembertotal`, `…onlytotal`, `getguestmemberonlytotal` | `03B4`<sub>h</sub>, `03CC`<sub>h</sub>, `03CE`<sub>h</sub> | `00341E60`, `003426F0`, `003430C0` | `003599A0` counted over both collector groups, group 0 only, or group 1 only; the `_543` to `_545` forms (`0543`<sub>h</sub> to `0545`<sub>h</sub>) take a flag and return the raw collector counts when it is 0 |
| `capturebattlemember(sel)` / `capturebattlemembeructop` | `03B3`<sub>h</sub> / `03F0`<sub>h</sub> | `003408E0` / `00340E00` | push `0, 0` or `1, 0` and run `00357570` |
| `captureguestmember(i)` | `03CD`<sub>h</sub> | `003410C0` | captures the `i`-th guest of group 1 through `00262F50` and cancels its action ([cutscenes](cutscenes-and-the-world-lock.md)) |

`partycommoneffectplay(v)` (`043E`<sub>h</sub>, `00350B90`) hands the value to `00268690` and returns its
result.

## Layouts

```python
party block   [02EBF190]: +0x5A48 u16[9] master (map 0), +0x5A5A u16[9] combat set (map 1), +0x5A7E u16[9] gameplay roster (map 3), +0x5AA4 u8 leader
snapshot      022C2580 u16[9]: the edited copy of map 0; 003261D0 compacts it, writes it back and starts the read-in
roster array  0209A1F0: 4 × actor pointer (00263750)
selector      0..6 main character, 7..25 guest (00322350), 0xFF empty slot
busy bit 19   003601B0(0x13) / 003601C0(0x13): a party change in progress
appearance    actor +0x08 bits 1-2 (map-id pair), bit 3 and +0x09 bit 6 (hit reaction); presentation +0x13 LOD, +0x151 bit 3 blob shadow; render record +0x304 bits 12-13 projection shadow
motion frame  push motion, float, flag; 003580C0 pops flag, float, motion
```

## Shipped data

| Fact | Value |
|---|---|
| battle-party verbs in the US scripts | `addpartymember` 45, `removepartymember` 36, `setbattlemember` 26, `addguestbattlemember` 27, `removeguestbattlemember` 30; the other three 0 |
| `partyallread` | 1,045 uses |
| appearance verbs | `partyusemapid` 459, `partysetlod` 35, `partyusecharhit` 25, the shadow forms 1 |
| motion verbs | `partystdmotionplay_540` 278, `partystdmotionplay` 66, `party_motionsync_and_relax` 370 |
| queries | `getbattlemember` 93, `getbattlemembertotal` 26, `getbattlememberonlytotal` 25, `ispartymember` 13 |
| collector bound | four slots for the roster and the combat set, nine for the non-guest map |

## Operations

A party change: one begin, then one poll per frame until the read-in task finishes. An appearance
verb: two collector walks and up to eight setter calls. A motion verb: four action cancels and
four synthetic calls.

## State

The party block's three maps and leader byte, the roster pointer array, busy bit 19, and the
per-actor bytes the setters write.

## Modding notes

- `setbattlemember` is all-or-nothing on availability, on the lock and on free slots, but changes
  the leader regardless.
- `setbattlememberone` and `removebattlemember` can never empty the roster.
- The appearance verbs read the combat set, the motion verbs the live roster array; the two can
  differ, and nothing reconciles them.
- `partyshowshadow` with 1 and `partyshowshadow_411` are the same call; both skip a member whose
  class is not 3.
- A script that changes the party must wait: the verbs are asynchronous and the actors do not
  exist until the read-in has run.

## Related

- [Party read-in state machine](../Characters-And-Objects/actor-model-rebuild.md): what the polls wait for.
- [Cutscenes and the world lock](cutscenes-and-the-world-lock.md): capturing a member's body.
- [Native commands](native-commands.md): begin and poll.
- [Verb dispatch](verb-dispatch.md): the value stack the motion verbs reuse.
