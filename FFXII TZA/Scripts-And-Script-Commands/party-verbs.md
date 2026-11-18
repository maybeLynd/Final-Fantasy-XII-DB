[Home](../../README.md) / [Scripts and script commands](README.md) / Party verbs

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Party verbs: the eight verbs that change the battle party and the poll they share, the appearance verbs, the standard-motion verbs, and the party queries | system | Scripts and script commands | Script commands | What a zone script can do to the party: the eight asynchronous verbs that add, remove, set and lock battle members and the one poll that waits for the read-in, the seven appearance verbs that set level of detail, shadows, character collision and the map-id flag pair on the members combat is servicing, the four standard-motion verbs that push a synthetic argument frame per roster actor, the queries that read the roster and party masks, and the capture forms that take a member's body. | 0x0034D4E0, 0x00350CD0, 0x00350160, 0x00352AF0, 0x0034C030, 0x00352190, 0x00351A40, 0x003506A0, 0x0034CDF0, 0x0034C370, 0x003596B0, 0x0037CB50, 0x003601B0, 0x003601C0, 0x003596D0, 0x00359BA0, 0x00359C00, 0x00359740, 0x00320800, 0x0031B510, 0x00322350, 0x003271D0, 0x0033FD60, 0x00340700, 0x00341190, 0x00341B90, 0x00342360, 0x00342830, 0x00342B30, 0x0031B5A0, 0x0031B670, 0x0031B680, 0x0026AD60, 0x0026A430, 0x002EC680, 0x002ECD80, 0x002E8730, 0x0034F060, 0x0034F890, 0x00350050, 0x003507B0, 0x003580C0, 0x0035AE10, 0x00263750, 0x0034B4B0, 0x0034F5A0, 0x00353780, 0x00353CB0, 0x00353460, 0x0034E7D0, 0x003542C0, 0x003546F0, 0x00341E60, 0x003426F0, 0x003430C0, 0x00342280, 0x003408E0, 0x00340E00, 0x003410C0, 0x00342910, 0x00342EC0, 0x0034CCD0, 0x0034E3E0, 0x02EBF190, 0x0037C3C0, 0x002E6BD0 |

## What the player sees

A story scene adds a guest to the party, takes a main character away, or lines up exactly the
three members the plot needs; the party's shadows and detail level change for a scene; all four
members strike the same pose at once. Every one of these is a zone script calling a party verb.
The verbs that change who is in the party wait until the engine has rebuilt the actors, which is
why a scene pauses for a moment after a character joins or leaves.

## How it works

### The three slot maps

The party block at `[0x02EBF190]` carries nine two-byte seats per [slot map](../Party/party-slots.md#the-nine-seats): map 0 at `+0x5A48` is the
master the mutators edit, map 3 at `+0x5A7E` the gameplay roster the party verbs read, map 1 at
`+0x5A5A` the set combat is servicing, and `+0x5AA4` the leader's selector (`0x003271D0`).

Selectors 0 to 6 are the main characters and 7 to
25 guests (`0x00322350` tests `selector − 7 < 19`). `0x0031B510` collects the roster's first four
slots from map 3 (an empty slot reads `0xFF`), `0x00320800` collects up to nine non-guest selectors
from the whole map, and `0x00263750(slot)` returns the live actor of roster slot 0 to 3 from the
pointer array at `0x0209A1F0`.

Both collectors take an output array and a limit, read the low byte of each two-byte seat of map 3 (`+0x5A7E`), write
the kept selectors packed in slot order, stop once the limit is reached (`0x0031B540`, `0x00320830`), and return how many
they wrote. `0x0031B510` reads slots 0 to 3 and skips `0xFF` (`0x0031B562`; its loop, `0x0031B540`-`0x0031B57C`); `0x00320800`
reads slots 0 to 8 and keeps 0 to 6 and 26 to 254, skipping guests and `0xFF` (`0x00320852` to `0x0032085C`). Each slot
index also passes `0x00322C50(0x17, slot)`, which accepts 0 to 8 (`0x00322FAF`), so it refuses no slot.

### Changing the battle party

| Verb | Id | begin | poll | What the begin does |
|---|---|---|---|---|
| `addpartymember(sel)` | `0x0353` | `0x0034C030` | `0x0034C370` | stores the selector; the poll raises busy bit `0x80000` and adds a main character to the reserve (`0x003172E0`) |
| `removepartymember(sel)` | `0x0354` | `0x0034C030` | `0x0034CDF0` | the poll removes the main character (`0x00328B20`) and then raises bit `0x80000`; a selector above 6, or one absent from map 0's nine slots, is left in place (`0x00328B2A`, `0x00328B59`) and the bit is still raised (`0x0034CE3B`) |
| `setbattlemember(a, b, c)` | `0x0355` | `0x0034D4E0` | `0x003506A0` | hides the four roster actors, raises bit `0x80000`, pops three selectors; when every non-negative one's bit, the selector modulo 32 (`0x0034D568` is a 32-bit shift), is in `0x00359C00` through `0x0035A050`, which keeps the main characters' bits, the roster is reconciled by `0x00328DB0`; when the leader (`0x003271D0`) is not among them the first non-negative selector becomes leader (`0x00327850`), whatever the reconcile did; that selector is not kind-checked, so a guest, which fails the availability test, still becomes leader (`0x0034D5BE`); with all three negative the leader stays (`0x0034D5B9`) |
| `removebattlemember(sel)` | `0x0358` | `0x00350160` | `0x003506A0` | pops the selector (`0x00267E10`, `0x00350178`) and raises bit `0x80000` (`0x00350184`); then, for a selector `0x00322350` does not count as a guest (`0x0035018C`-`0x00350193`) and only while the roster holds more than one (`0x0031B510`, `0x00350195`-`0x003501A5`), `0x003286E0(sel)` (`0x003501AA`): the member's slot is swapped with the first empty reserve slot (`0x003286E0`, `0x00321100`); no empty reserve slot, no change (`0x00328730`); a selector above 6, or one absent from map 0's slots 0 to 3, also changes nothing (`0x003286E7`, `0x00328715`) |
| `setbattlememberone(sel)` | `0x0359` | `0x00350CD0` | `0x003506A0` | for a main character in roster slots 0 to 3: every non-guest in slots 0 to 2 other than it is swapped into the first empty reserve slot (`0x003287A0`); slot 3 and guests stay, and a member stays when no empty reserve slot is left (`0x003288A4`); one outside the roster has the same done around the roster's first member; with an empty roster nothing is done (`0x00350D4B`); `0x003287A0` changes nothing for a selector above 6, which covers a guest as the roster's first member, or for one absent from map 0's slots 0 to 3 (`0x003287AC`, `0x003287E5`) |
| `setbattlememberlock(sel, on)` | `0x035A` | `0x00351A40` | `0x003506A0` | bit `0x1` of the member's stats record (`0x00328FB0`), the pin `setbattlemember` honours: set for a non-zero `on` (`0x00328FD5`), cleared for 0 (`0x00328FDE`); a selector without a battle unit (`0x002367A0`), or whose unit has a null record at `+0x698`, is left alone (`0x00328FC3`, `0x00328FCF`) |
| `addguestbattlemember(sel)` | `0x035B` | `0x00352190` | `0x003506A0` | hides the roster, raises bit `0x80000`, and places a guest absent from map 0 in the highest empty roster slot from 3 down to 1 (`0x003170E0`, `0x00326110`), activating it with `0x00316DF0`; a guest already in map 0 changes nothing (`0x00317108`), and with no empty slot among 3 to 1 nothing is placed (`0x00317159`) |
| `removeguestbattlemember(sel)` | `0x035C` | `0x00352AF0` | `0x003506A0` | removes a guest (`0x003288F0`): its map 0 seat becomes `0xFFFF` in the snapshot, its record is deactivated by `0x00323540`, and `0x003261D0(0)` applies the change (`0x0032895E` to `0x00328983`); a guest absent from map 0 changes nothing (`0x00328925`) |

Each begin except the shared add/remove begin `0x0034C030` raises busy bit `0x80000` (`0x003601B0(0x13)`)
before it touches the party, and the three that rebuild the roster first hide the four roster actors
with `0x002ECD50(actor, 0)`, called through the jump `0x0026DC40`. `0x0034C030` only stores state 0
(`0x0034C039`) and the popped selector (`0x0034C048`); for those two verbs the poll raises the bit,
before the add (`0x0034C3B1`) and after the remove (`0x0034CE3B`).

Guest and main selectors are checked by `0x00322350`: a verb for one kind silently ignores the other.
The add and remove polls leave that check to `0x003172E0` and `0x00328B20`, which act only on a selector
of 6 or below (`0x003172ED`, `0x00328B27`); `setbattlemember` uses the main-character mask instead and
does not check the leader it sets.

The member activation `0x00316DF0` also grants goods. The main add `0x003172E0` (`0x003173D2`) and the seating step
`0x00326110` (`0x003261A6`) that the guest add `0x003170E0` tail-jumps to run it.

So does the seat writer `0x00329080(seat, sel, flags)`, when `0x00322C50(0x17, seat, 1)` accepts the seat, `sel` is not
`0xFF`, `0x00322C50(2, sel, 1)` accepts it, it is at most `0x27` and bit `0x1` of `flags` is set
(`0x003290B0`-`0x0032916A`). The new-game fill `0x00329CC0` runs it with second argument 1 behind the same two tests of the
selector (`0x00329D63`-`0x00329D92`).

With `sel` = `0xFF`, `0x00329080` empties the seat instead, when `0x00322C50(0x17, seat, 0)` accepts it and the selector
there is at most `0x27`: only when bit `0x1` of `flags` is set it hands that record to `0x00323540`, which deactivates
only an active main character (rows 0-6) and leaves any other record as it is (`0x0032354A`-`0x0032355C`), and it writes
`0xFFFF` (`0x003290C2`-`0x00329122`).

`0x00329080` returns 1 when it writes the seat and 0 when it refuses (`0x0032911D`, `0x0032917E`, `0x00329185`). The scenario
presets pass `flags` 3 (`0x00239DC3`), and the commit `0x003261D0` and the list fill `0x003273D0` pass it as 0 (`0x00326454`,
`0x00327763`), so these write the seats without activating or deactivating anyone.

`0x00316DF0` grants only to a party record, kind `+5` 0 with a selector `+4` of 0-25, that is not yet active, bit `0x10`
clear (`0x00316DFE`, `0x00316E42`-`0x00316E6A`). Rows 0-6 add each of their five equipment words to the inventory and equip
it (`0x00300B80`, `0x0030C410`, `0x00316E82`-`0x00316E85`).

Then, for rows 0-25, unless the record's bit `0x8` is set (`0x00316EB3`), it adds each enabled gambit slot's condition
and, for rows 0-6 only, the id its action row names at `+0x22` (`0x00316EC3`-`0x00316F92`), and up to ten items with their
counts (`0x00300B80`) and an amount of gil (`0x003004B0`) from a row of the party definitions `0x02EBF130`.

See [Party members](../Party/party-members.md), [inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) and
[gil](../Rewards-EXP-Gil-And-Loot/gil.md).

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
verb keeps waiting; when done the poll clears bit `0x80000` and returns 0.

The two per-verb polls `0x0034C370` and `0x0034CDF0` do the add or remove on their first visit (states
0 and 1, returning 1), then wait the same way in state 2: they return 1 while `0x003596B0` reports
pending and, once it reports done, clear bit `0x80000` and return 0 (`0x0034C398`, `0x0034CE18`). A
state other than 0 to 2 returns 1 without acting (`0x0034C388`, `0x0034CE08`).

`partyallread` (`0x03EB`, begin `0x0034CCD0`) raises bit `0x80000` and starts the read-in task (`0x0037C980`);
`partyallread2` (`0x046F`, `0x0034D8B0`: `0x00314D40(1)`, then `0x0037CA00` as a tail jump, `0x0034D8B4`-`0x0034D8C2`) runs it
in reverse slot order. Their poll `0x0034E3E0` waits on the same end test, calling `0x00314D40(1)` each frame, and their
result `0x0034D460` follows ([the read-in state machine](../Characters-And-Objects/actor-model-rebuild.md)).

### The appearance verbs

Seven verbs share one shape: pop a value, collect the members with `0x0031B670` (selector 0) and
`0x0031B680` (selector 1), and call one setter on each of up to four in both groups. The collector
`0x0031B5A0` walks the first four slots of map 1, resolves each selector to a battle unit
(`0x002367A0`), keeps units with byte `+0` bit `0x10` whose record at `+0x698` has byte `+5` clear, and
splits them on whether the record's byte `+4` lies in 7 to 25: selector 1 takes the guests,
selector 0 everyone else. The object handed to the setter is the unit's `+0x10`, the actor record.

`0x0031B670` and `0x0031B680` set the group (0 or 1) and jump into `0x0031B5A0`, which writes the kept
actor records packed into the caller's array, stops once the caller's limit (4 in every verb here)
is reached (`0x0031B5D2`), and returns how many it wrote. A selector that `0x002367A0` resolves to no
unit, or a unit whose `+0x698` record is null, is skipped (`0x0031B606`, `0x0031B617`). The slot index
passes `0x00322C50(0x17, slot)`, which accepts 0 to 8, so the `0xFF` fallback at `0x0031B5E9` is never
taken for slots 0 to 3. Each kept unit lands in exactly one group (`0x0031B629` to `0x0031B62F`).

| Verb | Id | Handler | Setter | What it writes |
|---|---|---|---|---|
| `partyusemapid(v)` | `0x040D` | `0x0033FD60` | `0x0026AD60`, then `0x00265020` and `0x002E5DF0` | actor byte `+0x08` bits `0x2` and `0x4` as an exclusive pair (bit `0x2` for non-zero), then re-places the actor at its own position; `0x00265020` reads that position from the three floats at `[actor + 0xB8]` for an actor of class 1 or 3 (`0x00265025` to `0x00265041`) and gives `0, 0, 0` for any other class (`0x00265052`), and `0x002E5DF0` takes those three floats as the new position (`0x0033FE06`, `0x0033FE61`) |
| `partyusecharhit(v)` | `0x040E` | `0x00340700` | `0x0026A430` | actor byte `+0x08` bit `0x8` and byte `+0x09` bit `0x40` to `v != 0` |
| `partysetlod(v)` | `0x040F` | `0x00341190` | `0x002EC680` | presentation byte `+0x13` = `v`, then the refresh `0x002E8CE0`; nothing for a null actor or a null presentation `+0xC0` (`0x002EC683`-`0x002EC694`) |
| `partyshowshadow(v)` | `0x0410` | `0x00341B90` | `0x002ECD80` | presentation byte `+0x151` bit `0x8` = `v & 1`, then `0x002E8FD0`; skipped for a lifecycle byte of 1 or a class other than 3 (actor byte `+0x18` equal to 1 at `0x002ECD80`; actor byte `+0x03` masked with `0xE0` other than `0x60` at `0x002ECD86` to `0x002ECD8E`) and for an actor with no presentation at `+0xC0` (`0x002ECD9A`); the bit is written at `0x002ECD9C` to `0x002ECDA9`, and `0x002E8FD0` is a tail jump with the actor (`0x002ECDAF`) |
| `partyshowshadow_411()` | `0x0411` | `0x00342360` | pushes 1 and jumps into `0x0410` | |
| `partyhideshadow()` | `0x0412` | `0x00342830` | pushes 0 and jumps into `0x0410` | |
| `setpartyprojectionshadow(v)` | `0x0413` | `0x00342B30` | `0x002E8730` | in the `0x740`-byte render record at `[0x022C6F28] + index × 0x740` with `+0x284` set: `+0x304` bits `0x1000` and `0x2000` become `01` for on and `00` for off, and `+0x290` bit `0x400000` is set either way; on (`v` non-zero) clears bit `0x2000` and sets bit `0x1000` (`0x002E8780`, `0x002E878A`), off clears both (`0x002E87DB`), and `+0x290` gets its bit at `0x002E8794` or `0x002E87E5`; the index is the presentation's word `+0`, and a null actor, an actor with no presentation at `+0xC0`, a presentation whose first dword is −1, an index of −1, a record address `[0x022C6F28] + index × 0x740` of 0 (`0x002E8775`, `0x002E87D0`) or a `+0x284` of 0 leaves both words unchanged (`0x002E8734` to `0x002E877E`, `0x002E879F` to `0x002E87D9`) |

### The standard-motion verbs

`partystdmotionplay(m)` (`0x053E`, `0x0034F060`) pops the motion id and, for each roster slot 0 to
3 with an actor, runs `0x0035AE10(actor, 1)` (cancel the unit's action, `0x00233F50`, then
`0x002ED020`), pushes the motion, the float `−1.0` and the flag 1 back onto the value stack and
calls `0x003580C0(actor, stack)`. The three siblings differ in two constants: the `withoutsame`
forms (`0x053F` `0x0034F890`, `0x0541` `0x003507B0`) push the flag 0, and the `_540` forms (`0x0540`
`0x00350050`, `0x0541`) pop a float first and push it instead of `−1.0`.

`0x003580C0` first calls `0x00263A30` on the actor's byte `+0x15` and word `+0`, a lookup that stores
nothing and whose result is dropped (`0x003580EF` overwrites it). It pops the flag, the float and the
motion in that order, resolves the actor's presentation (`0x002E97B0`) and its model entry
(presentation `+8`), and returns at once when either is null (`0x00358113`, `0x00358120`).

The slot is the presentation's motion lane, byte `+0x12` (`0x002E9C00`, `0x00358175`). When the entry
is loaded (`0x002E4C30` above 0 for a lane of 0 or more, `0x00358166`) or no selector is set (a negative
lane, accepted only when `0x002ED6F0` on the entry's `+0x14` id returns 0 lanes, `0x00358155`), it runs
`0x002EAC90(actor)` and then `0x003DDBB0(actor, slot, motion, float)` for flag 0 or `0x003DDB40` for flag
1, the two standard-motion starts; `0x003DDB40` takes any non-zero flag (`0x00358183`). Otherwise
nothing is started.

`0x003DDBB0(actor, slot, motion, float)` does not read `slot`. Through `0x002E8170` it sets or clears bit `0x80000` of the
render record's `+0x284` from bit `0x80` of byte `+0xD` of `0x00263F40(actor)` (`0x003DDBC8`-`0x003DDBD7`); `0x002E8170`
writes only when the actor's presentation `+0xC0` is set, its first dword and word `+0` index are not −1, the record
address `[0x022C6F28] + index × 0x740` is not 0 and that record's `+0x284` is non-zero (`0x002E8173`-`0x002E81AB`).

It then takes the stance motion `0x01EFE9D0[motion & 0xFFFFFF]` when bit `0x1000000` of `motion` is set, and
`(byte +0x15 of actor) << 20 | motion | 0x1000` otherwise (`0x003DDBDC`-`0x003DDBFE`), and ends with
`0x002EB4F0(actor, that, float)` as a tail jump (`0x003DDC02`-`0x003DDC17`).

`party_motionsync_and_relax` (`0x0573`, begin `0x00342910`, poll `0x00342EC0`) marks the four roster
slots in the scratch block and, per visit, for each present slot not yet done asks `0x002673D0` and
`0x002E7330`; while both answer 0 the verb stays busy, otherwise it plays the idle motion
(`0x002EB430`) and marks the slot done.

The marks are scratch bytes `+4` to `+7`, one per roster slot. The begin writes 0 for a slot whose
actor `0x00263750` returns and `0xFF` for an empty one (`0x0034293A`, `0x0034293F`), so a slot empty at
the begin is never waited on. Each poll visit resolves the actor again (`0x00342EE6`) and skips a slot
whose byte is not 0 (`0x00342EEB`) or whose actor is now null (`0x00342EF6`); it writes 1 for done
(`0x00342F16`) and returns 1 while any visited slot answered 0 to both, otherwise 0 (`0x00342F1B`,
`0x00342F30`).

`partystdmotiondispose` (`0x014B`, a jump into `0x0037C3C0`) releases the standard motion of the four
roster actors: for each roster slot 0 to 3 whose actor `0x00263750` returns, `0x002E6BB0(actor, 1)`
enters the shared body `0x002E6BD0` with a third argument of 0. The sibling entry `0x002E6BC0` gives 1
instead, and a second argument of 0 queues nothing (`0x002E6C75`).

The body returns at once for a null actor (`0x002E6BD3`) and then works on the presentation at actor
`+0xC0`:

1. When the presentation is set and its first dword is not −1, it stops the render record's motion (`0x002E6C2E`,
   `0x00427280`-`0x00427294`: dword `+0x294` = `(+0x294 & 0xFFFDFA5F) | 4`, then the tail jump `0x00422C20`) when the
   presentation's word `+0` index is not −1, the record address `[0x022C6F28] + index × 0x740` is not 0 (`0x002E6C23`)
   and that render record has a non-zero `+0x284`; either way it then stores 0 in actor `+0xEC` (`0x002E6C33`).
2. With no presentation, or a negative motion lane (presentation byte `+0x12`, `0x002E6C58`), it
   returns there.
3. Otherwise it drops one count from the lane and one from lane 0 in the actor's binding
   (presentation dword `+4`) with `0x002EB890` (`0x002E6C63`, `0x002E6C6D`), which decrements each lane's
   count word and writes no group word.
4. It queues the lane, then lane 0, for unload when nothing holds it (`0x002E3F00`, `0x002E6C94`; lane 0 at
   `0x002E3FAC` to `0x002E3FED`); with a third argument of 1, not a lane that
   `0x002E9C60(presentation +0x8, lane)` reports held (`0x002E6C79` to `0x002E6C8D`).
5. It sets the lane byte to `0xFF` (`0x002E6CAC`) and, for a render record found as in step 1 (index
   not −1, `+0x284` non-zero), stores `0x0020E620(0)`, the encoded null address, in `+0x42C` and
   `+0x430` (`0x002E6CDA`, `0x002E6D0D`) and clears its `+0x284` bit `0x40000` (`0x002E6D3A`).

### Queries and captures

| Verb | Id | Handler | Result |
|---|---|---|---|
| `getpartymember(&a … &f)` | `0x0352` | `0x0034B4B0` | writes up to six non-guest selectors from the whole map (`0x00320800`, limit 6) into six references, `−1` beyond the count (`0x0034B534`); the word it returns is whatever the last store left in the register: the sixth value, the one written to `f` (`0x0034B575`), which `0x0026B4E0` (`0x0034B57B`) makes the verb's int result. The references are popped last first and decoded by `0x002650B0` (`0x0034B4E0` to `0x0034B4FF`); the six dword stores are unchecked (`0x0034B53F` to `0x0034B579`), so a class 6 or 7 reference, decoded against base 0 (`0x0026516C`), writes to its bare 24-bit offset and faults below `0x10000` |
| `getbattlemember(&a … &d)` | `0x0357` | `0x0034F5A0` | the four roster selectors (`0x0031B510`) into four references, `−1` beyond the count; returns the count |
| `isbattlemember(sel)` | `0x035D` | `0x00353780` | `0x003596D0`: whether the selector is in the roster's four slots |
| `ispartymember(sel)` | `0x035E` | `0x00353CB0` | a guest is looked up in the roster, a main character among all nine non-guest slots (`0x00359740`) |
| `isguestbattlemember(sel)` | `0x035F` | `0x00353460` | `0x00322350` |
| `checkbattlemember(a, b, c)` | `0x0360` | `0x0034E7D0` | 1 when every non-negative selector's bit, the selector modulo 32 (`0x0034E810` is a 32-bit shift), is in the non-guest mask `0x00359C00` (`0x0034E83E`), and the main characters of the roster mask `0x00359BA0` and the request together (`0x0035A050` keeps bits `0x7F`) number at most 3, else 0 (`0x0034E860` to `0x0034E881`); guests already in the roster do not count against the 3; the bound becomes 4 minus the requested guests when the request names a guest (`0x0034E81D`, `0x0034E82B`), but `0x00320800` skips a guest's own selector, so a requested guest's bit is set in `0x00359C00` only by a kept selector of 39 or more, whose 32-bit shift wraps to that bit (`0x00359C3A`); without one such a request returns 0 |
| `getpartymembermask` / `getbattlemembermask` | `0x0361` / `0x0362` | `0x003542C0` / `0x003546F0` | `0x00359C00` (bit `selector & 31` of every selector `0x00320800` keeps) / `0x00359BA0` (bit `selector & 31` of each roster selector `0x0031B510` returns, guests included) as bit masks; both are 32-bit shifts (`0x00359C3A`, `0x00359BDA`), so a selector of 32 or more lands on a lower bit |
| `getbattlemembertotal`, `…onlytotal`, `getguestmemberonlytotal` | `0x03B4`, `0x03CC`, `0x03CE` | `0x00341E60`, `0x003426F0`, `0x003430C0` | `0x003599A0` counted over both collector groups, group 0 only, or group 1 only; the `_543` to `_545` forms (`0x0543` to `0x0545`) take a flag and return the raw collector counts when it is 0 |
| `capturebattlemember(sel)` / `capturebattlemembeructop` | `0x03B3` / `0x03F0` | `0x003408E0` / `0x00340E00` | push `0, 0` or `1, 0` and run `0x00357570` |
| `captureguestmember(i)` | `0x03CD` | `0x003410C0` | captures the `i`-th guest of group 1 through `0x00262F50` and cancels its action ([party during scenes](party-during-scenes.md)): `0x00262F50(target, guest)` (`0x0034110A`) binds them, and only a non-zero return leads to the cancel `0x0035AE10(guest, 1)` (`0x0034111B`); an `i` at or above the group's count (`0x003410F8`) or an empty entry (`0x00341102`) does nothing. The bound test is signed, so a negative `i` takes the 8-byte stack slot `i` entries before the collector's array (`0x003410FA`), for −1 to −4 the home slots where `0x0031B5A0` saved its caller's registers (`0x0031B5A0` to `0x0031B5AF`), and hands it to `0x00262F50` as the guest when it is non-zero |

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
verb: two collector walks over the same four slots of map 1 and up to four setter calls in all,
since each kept unit falls in exactly one group (`0x0031B629` to `0x0031B62F`). A motion verb: four
action cancels and four synthetic calls.

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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 8 calls with 4 other topics</summary>

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x002695A0` | calls | `0x002341C0` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md), [startup constants](../Engine-Core/startup-constants.md))

| Function | | Functions |
|---|---|---|
| `0x00263560` | is called by | `0x0022B8C0`, `0x0022BC20` |
| `0x002695A0` | calls | `0x00229F10` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md))

| Function | | Functions |
|---|---|---|
| `0x002ED6F0` | is called by | `0x002EEEE0` |

**Status effects and KO** (explained on [battle verbs](battle-verbs.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00322C50` | is called by | `0x0030E130`, `0x0030FED0`, `0x00310DB0` |

</details>
