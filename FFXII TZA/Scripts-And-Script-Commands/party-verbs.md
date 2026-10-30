---
title: "Party verbs: the eight verbs that change the battle party and the poll they share, the appearance verbs, the standard-motion verbs, and the party queries"
kind: "system"
category: "Scripts and script commands"
addresses: "0x0034D4E0, 0x00350CD0, 0x00350160, 0x00352AF0, 0x0034C030, 0x00352190, 0x00351A40, 0x003506A0, 0x0034CDF0, 0x0034C370, 0x003596B0, 0x0037CB50, 0x003601B0, 0x003601C0, 0x003596D0, 0x00359BA0, 0x00359C00, 0x00359740, 0x00320800, 0x0031B510, 0x00322350, 0x003271D0, 0x0033FD60, 0x00340700, 0x00341190, 0x00341B90, 0x00342360, 0x00342830, 0x00342B30, 0x0031B5A0, 0x0031B670, 0x0031B680, 0x0026AD60, 0x0026A430, 0x002EC680, 0x002ECD80, 0x002E8730, 0x0034F060, 0x0034F890, 0x00350050, 0x003507B0, 0x003580C0, 0x0035AE10, 0x00263750, 0x0034B4B0, 0x0034F5A0, 0x00353780, 0x00353CB0, 0x00353460, 0x0034E7D0, 0x003542C0, 0x003546F0, 0x00341E60, 0x003426F0, 0x003430C0, 0x00342280, 0x003408E0, 0x00340E00, 0x003410C0, 0x00342910, 0x00342EC0, 0x0034CCD0, 0x0034E3E0, 0x02EBF190, 0x0037C3C0, 0x002E6BD0"
---

## What the player sees

A story scene adds a guest to the party, takes a main character away, or lines up exactly the
three members the plot needs; the party's shadows and detail level change for a scene; all four
members strike the same pose at once. Every one of these is a zone script calling a party verb.
The verbs that change who is in the party wait until the engine has rebuilt the actors, which is
why a scene pauses for a moment after a character joins or leaves.

## How it works

### The three party maps

The party block at `[0x02EBF190]` carries nine two-byte slots per map: map 0 at `+0x5A48` is the
master the mutators edit, map 3 at `+0x5A7E` the gameplay roster the party verbs read, map 1 at
`+0x5A5A` the set combat is servicing, and `+0x5AA4` the leader's selector (`0x003271D0`).

Selectors 0 to 6 are the main characters and 7 to
25 guests (`0x00322350` tests `selector − 7 < 19`). `0x0031B510` collects the roster's first four
slots from map 3 (an empty slot reads `0xFF`), `0x00320800` collects up to nine non-guest selectors
from the whole map, and `0x00263750(slot)` returns the live actor of roster slot 0 to 3 from the
pointer array at `0x0209A1F0`.

### Changing the battle party

| Verb | Id | begin | poll | What the begin does |
|---|---|---|---|---|
| `addpartymember(sel)` | `0x0353` | `0x0034C030` | `0x0034C370` | stores the selector; the poll raises busy bit `0x80000` and adds a main character to the reserve (`0x003172E0`) |
| `removepartymember(sel)` | `0x0354` | `0x0034C030` | `0x0034CDF0` | the poll removes the main character (`0x00328B20`) and then raises bit `0x80000` |
| `setbattlemember(a, b, c)` | `0x0355` | `0x0034D4E0` | `0x003506A0` | hides the four roster actors, raises bit `0x80000`, pops three selectors; when every non-negative one is an available main character (`0x00359C00` through `0x0035A050`) the roster is reconciled by `0x00328DB0`; when the leader (`0x003271D0`) is not among them the first non-negative selector becomes leader (`0x00327850`), whatever the reconcile did |
| `removebattlemember(sel)` | `0x0358` | `0x00350160` | `0x003506A0` | only while the roster holds more than one: the member's slot is swapped with the first empty reserve slot (`0x003286E0`, `0x00321100`); no empty reserve slot, no change |
| `setbattlememberone(sel)` | `0x0359` | `0x00350CD0` | `0x003506A0` | for a main character in roster slots 0 to 3: every non-guest in slots 0 to 2 other than it is swapped into the first empty reserve slot (`0x003287A0`); slot 3 and guests stay; one outside the roster has the same done around the roster's first member |
| `setbattlememberlock(sel, on)` | `0x035A` | `0x00351A40` | `0x003506A0` | bit `0x1` of the member's stats record (`0x00328FB0`), the pin `setbattlemember` honours |
| `addguestbattlemember(sel)` | `0x035B` | `0x00352190` | `0x003506A0` | hides the roster, raises bit `0x80000`, and places a guest absent from map 0 in the highest empty roster slot from 3 down to 1 (`0x003170E0`, `0x00326110`), activating it with `0x00316DF0` |
| `removeguestbattlemember(sel)` | `0x035C` | `0x00352AF0` | `0x003506A0` | removes a guest (`0x003288F0`) |

Each begin raises busy bit `0x80000` (`0x003601B0(0x13)`) before it touches the party, and the three that
rebuild the roster first hide the four roster actors with `0x002ECD50(actor, 0)`. Guest and main
selectors are checked by `0x00322350`: a verb for one kind silently ignores the other.

The guest activation `0x00316DF0` also grants goods. For a record of type 0 to 6 it adds each of
its five equipment words to the inventory and equips it (`0x00300B80`, `0x0030C410`); unless the
record's bit `0x8` is set it then adds up to ten items with their counts (`0x00300B80`) and an amount of
gil (`0x003004B0`) from a row of the party definitions `0x02EBF130`
([inventory](../Items-Equipment-Shops-And-Licenses/inventory.md),
[gil](../Rewards-EXP-Gil-And-Loot/gil.md)).

`0x00328DB0(list, 3)` builds a fixed mask from map 1's first four units (a stats record with bit `0x1`,
the lock, or a guest keeps its slot), looks each requested selector up in map 0 (a missing one
returns −1 with nothing applied), treats one already in slots 0 to 2 as fixed, and swaps the rest
into the unlocked slots among 0 to 2 in order; a request that runs past slot 2 also returns −1
with nothing applied. Slot 3 is never filled by it.

Every mutator copies map 0 into the snapshot at `0x022C2580`, edits the snapshot, and calls
`0x003261D0(0)`: it compacts slots 0 to 3 and 4 to 8 separately, rebuilds the roster pointer array
(`0x00269C70`), writes the nine slots back (`0x00329080`), snapshots the four combat units'
selectors to `0x022C257C` and starts the read-in task (`0x0037CA80`). The member verbs therefore do
not need `partyallread`: the read-in the shared poll waits on is started by the mutator.

The shared poll `0x003506A0` asks `0x003596B0` whether the party read-in is still pending: the
read-in task's end test `0x0037CB50` reports done when no task exists (`0x02EBF400` null) or its slot
cursor `0x02EBF3FE` has left the roster (past 3 going up, below 0 going down). While pending the
verb keeps waiting; when done the poll clears bit `0x80000` and returns 0. The two per-verb polls
`0x0034C370` and `0x0034CDF0` do the add or remove on their first visit (states 0 and 1), then wait
the same way in state 2.

`partyallread` (`0x03EB`, begin `0x0034CCD0`) raises bit `0x80000` and starts the read-in task
(`0x0037C980`); `partyallread2` (`0x046F`, `0x0034D8B0` → `0x0037CA00`) runs it in reverse slot order.
Their poll `0x0034E3E0` waits on the same end test, calling `0x00314D40(1)` each frame, and their
result `0x0034D460` follows
([the read-in state machine](../Characters-And-Objects/actor-model-rebuild.md)).

### The appearance verbs

Seven verbs share one shape: pop a value, collect the members with `0x0031B670` (selector 0) and
`0x0031B680` (selector 1), and call one setter on each of up to four in both groups. The collector
`0x0031B5A0` walks the first four slots of map 1, resolves each selector to a battle unit
(`0x002367A0`), keeps units with byte `+0` bit `0x10` whose record at `+0x698` has byte `+5` clear, and
splits them on whether the record's byte `+4` lies in 7 to 25: selector 1 takes the guests,
selector 0 everyone else. The object handed to the setter is the unit's `+0x10`, the actor record.

| Verb | Id | Handler | Setter | What it writes |
|---|---|---|---|---|
| `partyusemapid(v)` | `0x040D` | `0x0033FD60` | `0x0026AD60`, then `0x00265020` and `0x002E5DF0` | actor byte `+0x08` bits `0x2` and `0x4` as an exclusive pair (bit `0x2` for non-zero), then re-places the actor at its own position |
| `partyusecharhit(v)` | `0x040E` | `0x00340700` | `0x0026A430` | actor byte `+0x08` bit `0x8` and byte `+0x09` bit `0x40` to `v != 0` |
| `partysetlod(v)` | `0x040F` | `0x00341190` | `0x002EC680` | presentation byte `+0x13` = `v`, then the refresh `0x002E8CE0` |
| `partyshowshadow(v)` | `0x0410` | `0x00341B90` | `0x002ECD80` | presentation byte `+0x151` bit `0x8` = `v & 1`, then `0x002E8FD0`; skipped for a lifecycle byte of 1 or a class other than 3 |
| `partyshowshadow_411()` | `0x0411` | `0x00342360` | pushes 1 and jumps into `0x0410` | |
| `partyhideshadow()` | `0x0412` | `0x00342830` | pushes 0 and jumps into `0x0410` | |
| `setpartyprojectionshadow(v)` | `0x0413` | `0x00342B30` | `0x002E8730` | in the `0x740`-byte render record at `[0x022C6F28] + index × 0x740` with `+0x284` set: `+0x304` bits `0x1000` and `0x2000` become `01` for on and `00` for off, and `+0x290` bit `0x400000` is set either way |

### The standard-motion verbs

`partystdmotionplay(m)` (`0x053E`, `0x0034F060`) pops the motion id and, for each roster slot 0 to
3 with an actor, runs `0x0035AE10(actor, 1)` (cancel the unit's action, `0x00233F50`, then
`0x002ED020`), pushes the motion, the float `−1.0` and the flag 1 back onto the value stack and
calls `0x003580C0(actor, stack)`. The three siblings differ in two constants: the `withoutsame`
forms (`0x053F` `0x0034F890`, `0x0541` `0x003507B0`) push the flag 0, and the `_540` forms (`0x0540`
`0x00350050`, `0x0541`) pop a float first and push it instead of `−1.0`.

`0x003580C0` pops the flag, the float and the motion in that order, resolves the actor's
presentation (`0x002E97B0`) and its model entry, and when the entry is loaded (`0x002E4C30`) or no
selector is set, runs `0x002EAC90(actor)` and then `0x003DDBB0(actor, slot, motion, float)` for flag 0
or `0x003DDB40` for flag 1, the two standard-motion starts.

`party_motionsync_and_relax` (`0x0573`, begin `0x00342910`, poll `0x00342EC0`) marks the four roster
slots in the scratch block and, per visit, for each present slot not yet done asks `0x002673D0` and
`0x002E7330`; while both answer 0 the verb stays busy, otherwise it plays the idle motion
(`0x002EB430`) and marks the slot done.

`partystdmotiondispose` (`0x014B`, a jump into `0x0037C3C0`) releases the standard motion of the four
roster actors: `0x002E6BB0(actor, 1)` stops the render record's motion (`0x00427280`), drops the
actor's motion lane (presentation byte `+0x12`) from its binding's count and group words
(`0x002EB890`), queues it for unload when nothing holds it (`0x002E3F00`), sets the lane byte to
`0xFF`, and resets the render record's `+0x42C` and `+0x430` and clears its `+0x284` bit `0x40000`.

### Queries and captures

| Verb | Id | Handler | Result |
|---|---|---|---|
| `getpartymember(&a … &f)` | `0x0352` | `0x0034B4B0` | writes up to six non-guest selectors from the whole map (`0x00320800`) into six references, `−1` beyond the count; the word it returns is whatever the last store left in the register |
| `getbattlemember(&a … &d)` | `0x0357` | `0x0034F5A0` | the four roster selectors (`0x0031B510`) into four references, `−1` beyond the count; returns the count |
| `isbattlemember(sel)` | `0x035D` | `0x00353780` | `0x003596D0`: whether the selector is in the roster's four slots |
| `ispartymember(sel)` | `0x035E` | `0x00353CB0` | a guest is looked up in the roster, a main character among all nine non-guest slots (`0x00359740`) |
| `isguestbattlemember(sel)` | `0x035F` | `0x00353460` | `0x00322350` |
| `checkbattlemember(a, b, c)` | `0x0360` | `0x0034E7D0` | 1 when every non-negative selector is an available main character and the combined mask (`0x0035A050` over `0x00359BA0 \| request`) fits the slots the guests leave, else 0 |
| `getpartymembermask` / `getbattlemembermask` | `0x0361` / `0x0362` | `0x003542C0` / `0x003546F0` | `0x00359C00` (all non-guests) / `0x00359BA0` (the roster) as bit masks |
| `getbattlemembertotal`, `…onlytotal`, `getguestmemberonlytotal` | `0x03B4`, `0x03CC`, `0x03CE` | `0x00341E60`, `0x003426F0`, `0x003430C0` | `0x003599A0` counted over both collector groups, group 0 only, or group 1 only; the `_543` to `_545` forms (`0x0543` to `0x0545`) take a flag and return the raw collector counts when it is 0 |
| `capturebattlemember(sel)` / `capturebattlemembeructop` | `0x03B3` / `0x03F0` | `0x003408E0` / `0x00340E00` | push `0, 0` or `1, 0` and run `0x00357570` |
| `captureguestmember(i)` | `0x03CD` | `0x003410C0` | captures the `i`-th guest of group 1 through `0x00262F50` and cancels its action ([party during scenes](party-during-scenes.md)) |

`partycommoneffectplay(v)` (`0x043E`, `0x00350B90`) hands the value to `0x00268690` and returns its
result.

## Layouts

```python
party block   [0x02EBF190]: +0x5A48 u16[9] master (map 0), +0x5A5A u16[9] combat set (map 1), +0x5A7E u16[9] gameplay roster (map 3), +0x5AA4 u8 leader
snapshot      0x022C2580 u16[9]: the edited copy of map 0; 0x003261D0 compacts it, writes it back and starts the read-in
roster array  0x0209A1F0: 4 × actor pointer (0x00263750)
selector      0..6 main character, 7..25 guest (0x00322350), 0xFF empty slot
busy bit 0x80000   0x003601B0(0x13) / 0x003601C0(0x13): a party change in progress
appearance    actor +0x08 bits 0x2 and 0x4 (map-id pair), bit 0x8 and +0x09 bit 0x40 (collision with other characters); presentation +0x13 LOD, +0x151 bit 0x8 blob shadow; render record +0x304 bits 0x1000 and 0x2000 projection shadow
motion frame  push motion, float, flag; 0x003580C0 pops flag, float, motion
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

The party block's three maps and leader byte, the roster pointer array, busy bit `0x80000`, and the
per-actor bytes the setters write.

The roster pointer array `0x0209A1F0` holds four actor pointers, eight bytes each. `0x00269C70(actor, slot)` empties the
actor's old slot (`+0x12`) and stores the actor in the new one. The world and field resets clear the whole array with
two 16-byte stores of 0, and the second store covers slots 2 and 3:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0209A200` | `ptr[2]` | 0 (zero-filled tail of `.data`) | roster slots 2 and 3: the live actors of the third and fourth party members | `0x00269C70` (`0x00269CC8`, 0 for the old slot; `0x00269CE1`, the actor), from `0x002681C0`, `0x003261D0`, `0x003273D0` and `0x0050C610`; 0 from `0x0025BFB0` (`0x0025C01F`), `0x002695A0` (`0x002695B7`) and `0x0026DB30` (`0x0026DB5A`) | by slot from the array's start, which `0x0025B2E0` (`0x0025B2FC`), `0x0025C230` (`0x0025C39B`), `0x0025C830` (`0x0025CC56`), `0x0025D9E0` (`0x0025DC4D`), `0x00263560` (`0x002635A1`), the getters `0x00263750` (`0x00263758`), `0x00263770` (`0x00263780`) and `0x002637B0` (`0x002637B8`), `0x00268530` (`0x00268545`), `0x00268690` (`0x002686BB`), `0x00269530` (`0x00269541`), `0x00269C70` (`0x00269C82`), `0x0026C3E0` (`0x0026C41B`) and `0x0026C5D0` (`0x0026C5E5`) form |

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
- [Party during scenes](party-during-scenes.md): capturing a member's body.
- [Native commands](native-commands.md): begin and poll.
- [Verb dispatch](verb-dispatch.md): the value stack the motion verbs reuse.
