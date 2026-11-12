---
title: "Enemy respawning: death counts, cooldowns, the group table that wakes a zone script, and the two-area memory"
kind: "system"
category: "Enemy spawning"
addresses: "0x00300530, 0x002395A0, 0x0032A100, 0x0032A160, 0x0032A150, 0x00235F50, 0x00235FB0, 0x002366E0, 0x00236670, 0x00235720, 0x00306E60, 0x00239710, 0x0050F8C0, 0x00306F00, 0x003250F0, 0x00307110, 0x00307030, 0x003070E0, 0x00233D20, 0x0026ADC0, 0x00307140, 0x00238B70, 0x00238AE0, 0x00307090, 0x002342F0, 0x00233780, 0x002368D0, 0x00235340, 0x00235330, 0x00237DF0, 0x00233C10, 0x00233440, 0x00233550, 0x00234990, 0x002352E0, 0x00300E40, 0x002350C0, 0x00328370, 0x003148F0"
---

## What the player sees

Kill a wandering monster and, after a while, it is back. How long "a while" is belongs to the
monster: each one carries a cooldown in whole seconds, rolled once from a base and a range the
zone script authored, and measured on a clock that only runs while the field runs. Some monsters
can only die so many times per visit; after that number they stay gone until the area forgets them.

Leave an area and come straight back and the monsters are exactly as you left them: the same ones
alive, the same ones dead, standing where they were, still angry at whoever hit them. The game
remembers two areas: the one you are in and the one before it. Return to the area from two moves
ago within five minutes and its memory is handed back; arrive from anywhere else, or later than
that, and the area is generated fresh and everything respawns.

Some fights end with the zone script reacting: a gate opens, a hunt advances, a boss gauge closes.
The engine keeps a checklist per group of enemies, ticks off each registered member as it dies and,
when the last one falls, locks the party for the aftermath and hands the group's number to the
zone script. A monster that merely wanders out of range and vanishes is not a death and does not
tick the list.

## How it works

### Recording a death

The HP modifier `0x00300530` is the one path to a death. On its lethal branch, when the unit's stats
record at `+0x698` has kind byte `+0x05` = 1 (an enemy built from the enemy definition table,
[battle unit construction](../Characters-And-Objects/battle-unit-construction.md)), it takes the spawn
record at unit `+0x6A0` and increments its death count `+0x08` (`0x00300801`). It then reads the
step counter through `0x0032A150`, divides it by `(int)(30.0 * [0x01DFE0B8])` with an unsigned `div`
(`0x00300820`) and stores the quotient at `+0x0C` (`0x00300829`): the second of the death.

The divisor is 30 at the 30 fps setting and 60 at 60 fps, so the stamp is in whole seconds of
normal-speed play at either rate. It then calls the group table's death handler `0x00306F00` (`0x0030082F`). When that returns 1 the
group completed, and the modifier skips its own death presentation event (`0x00300836`); otherwise
it dispatches, when a local flag allows it, `0x200E` when its argument has bit `0x100`, else `0x2007` or
`0x2008` by a second argument (`0x00300838`-`0x0030085F`).

### The authored limit and cooldown

`0x002395A0(table)` is the tail of the script verb that installs a zone's spawn table. The table is
`b_00` = entry count, `b_01` = whether keys are authored, `w_02` = row stride, rows from `+4`. For
each live-bank entry `i` whose flag bit `0x2` (committed) is clear (`0x002395E3`) it writes, with
`rand` = `0x00328370` (the shared gameplay generator,
[random number generators](../Random-Numbers/random-number-generators.md)):

```python
rec.w_0A = row.b_00 ? row.b_00 + rand % (row.b_01 + 1) : 0      death limit
rec.w_10 = row.w_02 ? row.w_02 + rand % (row.w_04 + 1) : 0      cooldown, seconds
rec.dw_0C = 0 ; rec.w_08 = 0                                    stamp and count
rec.b_17 = rec.b_18 = table.b_01 ? row.b_06 : 0                 persistence key
```

Both numbers are rolled per entry, so two visits to one zone can give the same monster different
cooldowns. A committed entry keeps its numbers: the roll happens once per bank life. The generator is
drawn only for a non-zero base (`0x00239607`, `0x00239635`), so an entry takes 0, 1 or 2 draws, and the cooldown
sum is stored as its low 16 bits (`0x00239652`).

A null table returns at once (`0x002395A3`), and so does a count of 0 or below: `b_00` is read as a signed
byte (`0x002395C4`, `0x00239679`), and the loop runs `i` from 0 while `i < b_00`, with no test against the
bank's 64 records. The row address `4 + i * w_02` (with `w_02` signed) is added to the low 32 bits of the
table pointer and the 32-bit sum is sign-extended (`0x002395ED`-`0x002395F9`). The bank pointer `0x0208E690` is
read with no null test (`0x002395CA`-`0x002395E3`).

### The clock

The counter `0x0208D45C` is advanced by `0x0032A100`, which the field frame orchestrator `0x00234590` calls once per
simulation step (`0x002345CA`): when timer 0 reports done (`0x003EBB70(0)`) it restarts it (`0x003EBBB0(0, 0, 1)`,
`0x003EBD00(0)`), then reads the timer's value through `0x003EBA90(0)` and increments the counter only
when that value differs from the one it kept at `0x022C317C` (`0x0032A12A`-`0x0032A135`). The compare is a float
`ucomiss`, and an unordered result counts as a difference (`0x0032A131`). Every call then stores the value it
read at `0x022C317C` (`0x0032A13B`).

The only other writer is `0x0032A160`, which zeroes it, and its one caller is the battle runtime reset `0x00237DF0`
(`0x00237E37`). No save writes or restores it.

At Frame Rate 60 (`0x01DFE0B8` 2.0) the counter rose by 60.00 a second whenever the field
ran. It stood still while the battle menu or a talk was open and for 1.4 to 3.4 seconds at each area change.

Other code reads the counter directly (`0x00319600`,
`0x003247F0`, `0x00317670`, `0x003191B0`); none of it is respawn code.

The same reset zeroes the transition stamp `0x02089374` (`0x00237E53`), sets the two field-history
words `0x02089372` and `0x02089370` to `0xFFFF` (`0x00237E5D`, `0x00237E64`) and clears the bank parity
`0x0208D454` (`0x00237E6B`).

The reset runs from the battle-state guard `0x00233C10`: twice when the
block pointer `0x02EBF190` is null (`0x00233C3F`, `0x00233C48`), once when the block's stamp is not
`0x05071901` (`0x00233C59`). Its other callers are the area reset `0x00239960` when the request byte
`0x0208D455` holds -2 (`0x0023998E`; the byte is a one-shot request, copied to `0x0208D456` and set to -1 before the test), `0x00238AA2` and `0x00394486`. An ordinary load whose block passes the
stamp test does not restart the clock.

### Two readers of the cooldown

The zone script reads the death limit and the three fields through four verbs, each a wrapper
around one accessor that resolves the lane through the unit's lane map at `+0x40` (count at `+0`,
slot bytes from `+1`, `0xFF` empty) and the live bank `[0x0208E690] + slot * 0x250`; the unit is the one
`0x0031B760` finds for the calling actor.

An accessor returns -1 when `0x0031B760` finds no unit, the map pointer is null, the lane is negative or above
count - 1 (a signed compare), the slot byte is `0xFF`, or the record address comes to 0 (`0x00235F01`-`0x00235F38`,
`0x00235F61`-`0x00235F98`, `0x00235FC1`-`0x00235FF8`, `0x002366F1`-`0x00236728`).

A fifth reads the flags of the unit's own entry, with the same tests and the lane taken from the unit's
signed byte `+0x57` (`0x00236682`, `0x0023667C`-`0x002366B8`):

| Accessor | Verb wrapper | Returns |
|---|---|---|
| `0x00235EF0(lane)` | `0x0050F610` | the death limit `+0x0A` (0 for no limit), or -1 |
| `0x00235F50(lane)` | `0x0050F660` | the death count `+0x08`, or -1 |
| `0x00235FB0(lane)` | `0x0050FAB0` | `counter / fps - stamp +0x0C`, the elapsed seconds, or -1 |
| `0x002366E0(lane)` | `0x005101F0` | the cooldown `+0x10`, or -1 |
| `0x00236670()` | `0x0050FC90` | flag bit `0x1` of the unit's own entry (retired, awaiting re-entry) when bit `0x2` is set and bit `0x4` clear, else -1 |

The elapsed seconds come back as a signed int, so the script's own test is signed. The shipped zone
scripts compare the two verbs with a strict greater-than (every `btlAtelGetRespawnTime` call in the
corpus is `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`), so a cooldown of N seconds
passes at the first second where `floor(counter / fps) - stamp > N`, one second later than N.

The automatic spawn selector `0x00235720` ([enemy spawning](enemy-spawning.md)) reads the fields
directly and differently. It examines no entry at all when the active count `0x00308D90()` has reached
the cap byte `0x0208D458` (`0x00235758`-`0x00235766`, returns -1).

It skips an entry whose limit `+0x0A` is non-zero and whose count
`+0x08` has reached it (`0x002358A1`-`0x002358B0`). For an entry with flag bit `0x1` clear and bit `0x2` set
and a non-zero cooldown, it skips while `seconds - stamp < cooldown` as an unsigned compare
(`0x002358D1` `sub`, `0x002358D5` `cmp`, `0x002358D7` `jb`): the native gate re-admits at `elapsed >= N`.
An entry with bit `0x1` set, one that range retirement marked, skips the cooldown test altogether.

### After a runtime reset

A reset zeroes the counter but not the stamps in the live bank: the reset's body touches neither
bank pointer, and the initialiser only rewrites uncommitted entries. While a stamp is above the new
clock, the script accessor returns a negative elapsed time, so the scripts' test first passes at
second `stamp + N + 1` of the new clock; the selector's unsigned subtraction wraps to a large value
and re-admits the entry at once. The accessor can even return -1, its own failure value, when the
stamp is exactly `counter + 1`.

### Registering a group member

A zone script puts an enemy in a group with verb `0x3030` `btlAtelSetEventFlagGroup(group, mode)`.
Its handler `0x0050F8C0` pops two ints, `mode` first and `group` second (`0x0050F8D8`, `0x0050F8E2`), and
tail-jumps to `0x00239710(actor, mode, group)` (`0x0050F8FE`).

`0x00239710` needs the
actor's battle unit (`0x0031B760`, else returns -1) and writes unit `+0xE98` = the low byte of `group` and `+0xE99`
= `(old & ~3) | (mode == 1) | (mode == 2) << 1`, mask `0xFC` kept: bit `0x1` is cleared in place first
(`0x0023973A`), then the byte is rebuilt (`0x00239746`-`0x00239766`). It then calls
`0x00306E60(unit, 1)` and returns 0 (`0x00239770`, `0x0023977A`).

`0x00306E60(unit, add)` is the only writer of the member mask. It returns without effect when the unit
is null, its stats record `+0x698` is null or not kind 1, or its group byte `+0xE98` is 0. It
resolves the unit's slot as `0x002360D0(map at +0x40, 0x00263D30(actor at +0x10))` and rejects a
negative. The bit is `(int64)(int32)(1 << (slot & 31))`: a 32-bit shift, sign-extended, so slot 31
covers the bits under mask `0xFFFFFFFF80000000` and slots 32 and above alias onto `slot & 31`. With `add` set the member mask
gains the bit, otherwise it loses it; the dead bit is cleared either way (`0x00306EEA`).

Range retirement (`0x002350C0`, `0x002352BB`) is the one caller with `add` = 0: a retired member leaves
the checklist without dying. Neither `0x00306E60` nor `0x00306F00` tests the group index `group - 1` against the
table's 64 records (`0x00306EB2`-`0x00306EC3`, `0x00306F57`-`0x00306F6B`): a group byte above 64 reaches memory past
the table.

### Completing a group

`0x00306F00(unit)` runs on every lethal branch of the HP modifier. Its gates return 0 for a null unit,
a null stats record `+0x698` or one whose byte `+5` is not 1 (`0x00306F09`-`0x00306F26`), a group byte
`+0xE98` of 0 (`0x00306F31`-`0x00306F3A`) and a negative slot from `0x002360D0` (`0x00306F4B`-`0x00306F55`),
the same gates and slot resolution as the registration. Past them it sets
`group table[group - 1].deadMask |= bit` (`0x00306F78`) and tests `(memberMask & deadMask) == memberMask`
(`0x00306F7C`-`0x00306F83`).

The test is a mask comparison, not a count, and nothing before it reads whether the bit is in the
member mask or whether the group has already completed. Every call that passes the gates while the
dead mask covers the member mask takes the completion branch, whether its bit is a member's not yet
recorded, a member's already recorded, or outside the member mask. With an empty member mask, every
call that passes the gates takes it.

On completion it locks the party (next section) and chooses an arm by `+0xE99` bit `0x1`:

- mode 1 (`0x00306FC9`-`0x00306FE8`): clear unit flag bit `0x800000000000`, set the group table's flag bit `0x1`, dispatch
  presentation event `0x2005`;
- any other mode (`0x0030700C`-`0x00307012`): set unit flag bit `0x800000000000`, dispatch `0x2008`. The flag is
  raised later by the reaction handler `0x003250F0`: on the death events it sets unit flag bit `0x200000000`
  (`0x00325185`) and, when bit `0x800000000000` is set (`0x0032519C`), calls `0x00307110`, which clears bit `0x800000000000` and
  sets the group table flag (`0x0030711A`-`0x00307133`).

The reaction handler `0x003250F0(actor, event)` returns 0 for a null actor, an actor without a battle unit
(`0x00263E30`), a unit without flag bit `0x4`, or an event word whose top four bits (`event >> 12`) are not 2
or 5 (`0x003250FD`-`0x00325130`). Events `0x2002`-`0x203C` go through a jump table (`0x0032513C`-`0x0032515C`): the
death events are `0x2007`, `0x2008`, `0x200C` and `0x200E`; `0x2002` calls `0x003082F0`, `0x2003` `0x003083A0`,
`0x2005`, `0x2037` and `0x2039`-`0x203C` call `0x00312FA0`, `0x200D` clears unit flag bit `0x1000000`
(`0x0032517C`) and `0x201C` calls `0x00317810`.

Every accepted event, in the table's range or not, then runs the same tail (`0x003251B3`-`0x003251EA`): when
`0x00322280(event)` is non-zero it sets bit `0x1` of unit dword `+0x690` and, when the stats record `+0x698` is
non-null and its status words `+0x64` and `+0x3C` together hold any bit of `0x80000003`, calls `0x00313F60`; it then
zeroes unit dword `+0x28` and returns 1.

`0x00306F00` reads no record of an earlier completion. The flag bit `0x1` that both arms set (`0x00306FE0`,
and `0x00307133` in `0x00307110`) is tested only by `0x00307030` and `0x003070E0`, and cleared by `0x00307030`
and the reset `0x00307090`. `0x00306F00` returns 0 when the mask test fails (`0x00306F88`) and 1 after either
arm (`0x00306FF2`, `0x0030701C`).

The completion branch stores into neither mask: of the code that addresses the table (`0x02EC13C0`,
`0x02EC13D0`, `0x02EC19D0`), the masks' only writers are `0x00306E60`, `0x00306F00` at `0x00306F78` and
`0x00307090`. So every later call that passes the gates runs the branch again while the dead mask still
covers the member mask. A member that re-registers clears its own dead bit (`0x00306EEA`); the test then fails
until a call sets that bit again.

### The lock

Three calls run on every completion, each with argument 1 (`0x00306F95`-`0x00306FB2`):

- `0x00307140(on)` calls `0x002E1C20(0xC, n)` ten times when on (`0x002E1CA0(0xC, n)` when off): the row-12
  capability inhibitions ([party roster and control
  suppression](../Party/party-leader.md)), then `0x00359200(on, 2)`,
  `0x00359330(2, 1, on)` and `0x0026BD20(2, on == 0)`;
- `0x00238B70(on)` sets or clears `0x02089340` bit `0x20` and, for every battle-unit slot whose byte `+0`
  has bit `0x10`, posts `0x002E7C10(actor, actor, 0x30B, 0)`;
- `0x00238AE0(on)` sets or clears `0x02089340` bit `0x80`.

The ten calls (`0x00307160`-`0x003071BE`) give `n` = 0, 3, 4, 5, 6, 7, 8, 11, 12 and 20, a bit index, so they set or
clear the bit values `0x1`, `0x8`, `0x10`, `0x20`, `0x40`, `0x80`, `0x100`, `0x800`, `0x1000` and `0x100000`
(mask `0x1019F9`) of row 12 at `0x0215F1F0` (`0x002E1C35`-`0x002E1C3C`). `0x00307140` takes any non-zero `on` as on
(`cmovne`, `0x0030715C`), and its last call is a tail jump (`0x003071F2`).

The zone script releases the lock with the same calls' off forms through its own verbs; the group table
never releases it. The next area entry does clear the two `0x02089340` bits: `0x002342F0`, when `0x02089300` is
non-zero (`0x002342F4`), opens with `0x02089340 = (0x02089340 & 0xFFFFC01E) | 0x10` (`0x0023432D`, `0x00234339`,
stored at `0x00234343`).

The AND clears bit `0x1` and the bits under mask `0x3FE0`, among them the lock bits `0x20` and `0x80` and the
gate the bits under mask `0xF00`, and keeps the bits under mask `0xFFFFC01E`, so the "nothing pending" bit `0x2` is kept; the OR sets
bit `0x10`. The row-12 inhibitions stay until their off form runs.

### Delivering the completion to the script

`0x00307030` runs once per simulation step from the orchestrator `0x00234590` (`0x00234717`). It does nothing while the gate
`0x00233D20` is closed: `0x02089340 & 0xF00` must be 0 and time-stop request 10 must not be raised
(`0x00226BD0(10)` = 0, [the time-stop
registry](../Engine-Core/time-stop-and-freeze.md)).

With the gate open it walks the 64 entries; for each with flag bit `0x1` it clears the bit and calls
`0x0026ADC0(3, i + 1)`, which stores the group number in word 3 of the 64-word table at `[0x02098E68]`
when the index is below 64, `0x02098E20` bit `0x1` is set and the pointer is non-null.

Zone scripts wait on that word (`scratch1 @0x06`) with `waitv`, which waits while it is zero; the word is cleared on
every field transition ([field runtime](../Characters-And-Objects/field-runtime.md)).

`0x003070E0` reports whether any entry has flag bit `0x1`. The per-unit frame `0x00233F70` calls it
(`0x00234095`) and sets `0x02089340` bit `0x2` when nothing is pending.

### Resetting the group table

`0x00307090` walks the 64 entries four at a time (`0x60` per step from `0x02EC13D0` to `0x02EC19D0`),
zeroing both masks and clearing flag bit `0x1` (`and byte ptr [...], 0xFE`). Its one caller is the area
initialiser `0x002342F0` (`0x0023442D`), straight after the bank rotation, so membership is rebuilt by
script after every area entry. The group table is BSS and starts at zero.

### The two banks and the return window

`0x002368D0` allocates two banks of `0x9400` bytes tagged `btlKeepCharWork1` and `btlKeepCharWork2`
at `0x0208E690` and `0x0208E698`, 64 spawn records of `0x250` each, zero-fills both (`0x0023696E`, `0x00236999`), and
sets the return window `0x0208936C` to 300 (`0x00236A0D`). Bank 1 is the live bank; bank 2 holds the previous area.

`0x00233780` runs once per area initialisation (`0x00234423` in `0x002342F0`), after the area's own reset
and before the group table reset, and returns at once when either bank pointer is null. It reads the
entered field id from `0x003148F0`, the counter from `0x0032A150`, and restores when both hold
(`0x002337D6`-`0x00233803`):

```python
field == 0x02089372                                          the field from two transitions ago
(u32)(counter - 0x02089374) <= (u32)((int)(30.0 * [0x01DFE0B8]) * 0x0208936C)    unsigned, ja wipes
```

A restore exchanges the two banks' contents through a `0x9400`-byte stack buffer (bank 2 to the
stack, bank 1 to bank 2, the stack to bank 1); the pointers stay. A wipe copies bank 1 over bank 2,
zeroes bank 1 with one `memset`, and sets the 64 spawn-history counters of the new parity to 1.
Both branches flip the parity byte `0x0208D454` and then shift the history: `0x02089372 = 0x02089370`,
`0x02089370 = field`, `0x02089374 = counter`. The compare is against the field from two moves ago, so
the restore fires on the pattern A, B, A within the window; entering B again from B wipes.

The window is in seconds because the counter difference is in simulation steps and the multiplier is the
steps per second at normal speed (30 or 60). The high-speed mode runs two or four steps a frame, so there the window
lasts 150 or 75 wall-clock seconds; menus and time stop do not advance the counter.

With The Stepping (field 227) as A and Yardang Labyrinth (228) as B, after one Cactite was
killed on A (its spawn record: death count 1, time 303): going to B put A's records in bank 2 and fresh ones in
bank 1 and flipped the parity to 1; coming back to A 824 steps later put A's records back in bank 1, the dead
Cactite's record still with death count 1, and set the parity to 0. Going A, B, Sand-swept Naze (229), A instead
flipped the parity at each move, and on A the same record read death count 0: the area was generated fresh.

`0x00235340(w)` stores `w`, or 300 when `w` is negative (`cmovs`); `0x00235330`
returns it. Both reach script only through verb `0x306C` `btlAtelSetMapJumoKeep` (`0x005107F0`), which
no story script calls, so in story play the window is 300 seconds everywhere; the developer Battle Plan Menu
(`bin/btlctrl` lines 1180 and 1187) passes -1, which gives 300, and 0. After a reset the previous-field
word is `0xFFFF` (sign-extended to -1 at `0x002337CD`) and `0x003148F0` never returns a negative, so the
first rotation after any reset wipes.

### The spawn-history counters

`0x0208D354` holds two banks of 64 `u16` counters, selected by the parity `0x0208D454`. The wipe sets the
new parity's 64 to 1 (`0x002339CC`-`0x002339E2`); the unit installer `0x0023A570` reads a row's counter,
stores its low byte at the spawn record's `+0x12` and writes back `old + 1`, or 1 once `old` reaches
`0x00254A40()` ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)). The
reset `0x00237DF0` clears the parity, not the counters.

### What the save image carries

`0x00233440(image)` zeroes a `0x20010`-byte image, copies bank 2 to `+0x10` and bank 1 to `+0x10010`
in `0x128` passes of `0x80` bytes, and stores `0x02089372` at `+0` and `0x02089370` at `+2`. A bank whose
pointer is null is skipped and its part of the image stays zero (`0x00233466`, `0x002334CD`); the two words
are stored either way (`0x00233529`-`0x0023353A`).
`0x00233550(image)` copies image `+0x10` back into bank 2 and restores the two words; it never touches
bank 1. With a null bank 2 pointer it skips the copy and still restores the words (`0x0023355A`,
`0x002335B9`-`0x002335C7`).

Its two callers are in the slot-0 restore `0x005843E0` (`0x0058443B`, `0x0058445E`), so only a load
of the field-transition autosave restores bank 2 and the history; a manual slot restores neither
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)). The window, the stamp, the
parity and the counter are in no save.

### Killing or tearing down by group

Four helpers walk the 32 battle-unit slots through `0x00321170` and act on kind-1 units:
`0x00234880` tears down every unit whose group byte is non-zero, `0x00234990(mask)` those whose
`mask >> (group & 31) & 1` is set (`0x00300E40(unit, 0)`), and `0x00234A10`/`0x00234A80(mask)` set or
clear unit flag `0x800` (the script's hide bit) on the masked subset. `0x002352E0` runs
`0x00300520(stats, 0, 0, 0)` on every kind-1 unit, which goes through the HP modifier and therefore
records a death for each. The mask test keeps 5 bits of the group id, so ids above 32 share a bit
with `id - 32`.

The teardown `0x00300E40(unit, keepMark)` runs the spawn record clear `0x00237080` (flags
`& 0xFFFFFF7A`, the word `+0x16` = `0x00FF` so the key `+0x17` is zeroed too, `+0x78`-`+0x7C` zeroed) only
when `keepMark` is 0 (`0x00300F5D`-`0x00300F68`), and only for a unit whose stats record `+0x698` is null or of
a kind other than 0 (`0x00300EE4`, `0x00300EEC`); a kind-0 unit takes the party arm and returns at `0x00300F5C`
without it. Range retirement is the one caller passing 1, so a retired entry keeps its bit `0x1` and
its transient state while every other teardown clears them.

## Layouts

Struct SpawnGroupTable base=`0x02EC13C0` count=64 size=`0x18`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | memberMask | bit (slot & 31), sign-extended from 32 bits; set by `0x00306E60`(unit, 1) |
| `+0x08` | `u64` | deadMask | set by `0x00306F00`, cleared by `0x00306E60` either way |
| `+0x10` | `u8` | flags | bit `0x1` = completion pending for `0x00307030` |
| `+0x11` | `u8[7]` | padding |  |

Struct SpawnRecordRespawnFields in the spawn record (`0x250` bytes, spawn-record-fields page):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | flags | bit `0x1` retired awaiting re-entry, bit `0x2` committed, bit `0x4` released |
| `+0x08` | `u16` | deathCount | `0x00300801` |
| `+0x0A` | `u16` | deathLimit | `0x002395A0`: base + rand % (range + 1), or 0 |
| `+0x0C` | `u32` | deathSecond | `0x00300829`: counter / fps |
| `+0x10` | `u16` | cooldown | `0x002395A0`: base + rand % (range + 1), or 0; whole seconds |
| `+0x12` | `u8` | historyCounter | low byte of the row's `0x0208D354` counter at install |
| `+0x17` | `u8` | persistenceKey | zeroed with `+0x16` by `0x00236860` / `0x00237080`; `+0x18` the authored key the resets restore it from |

Struct SpawnKeepImage size=`0x20010`   (`0x00233440` writes, `0x00233550` restores):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00000` | `u16` | fieldTwoAgo | `0x02089372` |
| `+0x00002` | `u16` | fieldLast | `0x02089370` |
| `+0x00010` | `u8[37888]` | bank2 | [`0x0208E698`]; restored by `0x00233550` |
| `+0x10010` | `u8[37888]` | bank1 | [`0x0208E690`]; written, never restored |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x0208D45C` | `u32` |  | step counter, +1 per simulation step whose timer 0 moved (`0x0032A100`); 0 at reset |
| `0x01DFE0B8` | `f32` |  | frame-rate scale, 1.0 at 30 fps, 2.0 at 60; fps = (int)(30.0 * scale) |
| `0x02089370` | `u16` |  | last field |
| `0x02089372` | `u16` |  | field two transitions ago |
| `0x02089374` | `u32` |  | counter at the last transition |
| `0x0208936C` | `i32` |  | return window, seconds (300) |
| `0x0208D454` | `u8` |  | bank parity |
| `0x0208D354` | `u16[2][64]` |  | spawn-history counters |
| `0x02EBF190` | `void*` |  | party block; dword +0 stamp `0x05071901` |
| `0x02089340` | `u32` |  | battle flags: bit `0x2` nothing pending, bit `0x20` and `0x80` the lock, bits `0xF00` close the gate |
| `0x02098E68` | `void*` |  | the 64-word field table; word 3 receives the completed group |

## Shipped data

- Every spawned unit's entry preamble calls `btlAtelSetEventFlagGroup` right after its level is
  set: 6,746 calls in 502 of the 769 zone scripts, 6,206 of them `(0, 0)`. The group argument is
  0-5 and the mode 0-2. Group 0 means no group: both group table paths skip it before indexing.
- All 1,765 `btlAtelGetRespawnTime` calls are `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`
  with the same lane; 1,737 add `|| btlAtelGetDeadCountNow(i) == 0` and 28 add
  `|| btlAtelGetRespawnCause() == -1`.
- No story script calls `btlAtelSetMapJumoKeep`, so in story play the window is the native 300 seconds; only the
  developer Battle Plan Menu (`bin/btlctrl`) sets it, to 300 or 0.
- Of the 239 scripts that import the completed-group word, 236 park on it with `waitv`.
- [`enemy-group-completions.tsv`](enemy-group-completions.tsv) gives the 248 groups that hold a placement: 540
  placements in 235 scripts, read from the `btlAtelSetEventFlagGroup` call of each placement's `entryNN` function.
  Group 1 is 235 of the 248 groups. Each row names the group's members, its mode, and what the script runs when the group is
  wiped out:
  - the steps after the `waitv` on the completed-group word, read in words: lines, story counter and game-wide words
    set, items and reward packages given, scenes played, fields the party is moved to, battle verbs, music and the
    functions it starts;
  - for `mic_d01`, whose Zalera fight tests the word with `if`, the steps under that test: the gauge timer stops and
    is hidden, and the party moves to field 894, Terminus No. 7 Adjunct.
- Of the 248, 241 remove every foe in a group, 147 set a game-wide word, 145 play a scene, 134 give items or a
  reward package, 127 move the party to another field, 42 set the story counter and 11 show a line.
- In the table, `map_name` and `region` are the zone's map name and region as the location line shows them, the
  `map_name` and `region` of the zone's row in
  [`zone-asset-list.tsv`](../World-Areas-And-Travel/zone-asset-list.tsv) on all 248 rows; 100 rows are in the Trial
  Mode region.

## Operations

A kill, in order: the HP modifier bumps `+0x08` and stamps `+0x0C`; `0x00306F00` sets the dead bit and
tests the mask; on completion the lock engages and the arm is chosen; the reaction handler raises
the flag for a mode other than 1 when the death track ends; the next simulation step with an open gate
posts the group number; the zone script wakes and runs the aftermath.

An area entry, in order (`0x002342F0`, only while the battle system's up flag `0x02089300` is non-zero, `0x002342F4`):
the cap `0x0208D458` = 28, the area reset `0x00239960` when requested, the bank rotation `0x00233780`, `0x003221B0`, the
group table reset `0x00307090`, then the zone
script re-registers every member and reinstalls the spawn table, whose initialiser rolls only the
uncommitted entries.

## State

The live bank and the history bank, the four history and window globals, the step counter and its
last timer value, the parity and the two counter banks, the group table, unit `+0xE98`/`+0xE99` and flag
bits `0x200000000` and `0x800000000000`, and word 3 of the field table. Only bank 2 and the two field words reach a save,
and only the autosave's restore brings them back.

## Modding notes

- A respawn wait is `cooldown + 1` seconds by script and `cooldown` seconds by the native selector,
  both in whole seconds at either frame rate. Changing `>` to `>=`, or comparing in steps, shifts
  every respawn in the game.
- The death limit and cooldown are rolled per entry from `base + rand % (range + 1)`; set the range
  to 0 for a fixed value.
- To make a group complete, set its dead bits; nothing counts deaths. A group id above 32 shares a
  mask bit with `id - 32` in the teardown helpers, and a slot of 31 or more in a lane map aliases
  in the group table: keep groups at 1-32 and slots below 31.
- Range retirement unregisters a member and skips its cooldown on return; routing retirement through
  the death path, or clearing flag bit `0x1` in a teardown, changes both.
- Completion locks the party through the three on-calls; a mod that raises its own completion must
  issue the off forms or the party stays locked.
- The return window only applies to the pattern A, B, A. Any other route, and any runtime reset,
  wipes the live bank; the wipe is one `memset`, so enmity, positions, statuses and the stats page
  go with it.
- The counter restarts at 0 on a reset while committed stamps stay; a stamp from late in a long
  session can hold an entry for hours by script, while the native selector re-admits it at once.

## Related

- [Enemy spawning](enemy-spawning.md): the lane map, the selectors and range retirement.
- [Spawn record fields](spawn-record-fields.md): the whole `0x250` record and the access table.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): the installer, the
  history counters and the kind byte.
- [Field runtime](../Characters-And-Objects/field-runtime.md): the field frame and the field table.
- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md): the HP modifier's lethal branch.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md): the threat bytes the bank carries.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the spawn-keep images.
- [Random number generators](../Random-Numbers/random-number-generators.md): the roll.
- [`enemy-respawning-groups.tsv`](enemy-respawning-groups.tsv): every access to the group table
  (`SpawnGroupTable`, 64 records of `0x18` bytes at `0x02EC13C0`), one row per instruction (19 rows).

In this access table, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset the instruction reaches from the start of a group record, `kind` a read (`r`), a write (`w`) or
both (`rw`), `instruction` the instruction itself, and `route` `array 0x02EC13C0 reg`: a record of the table at
`0x02EC13C0` picked by an index in a register.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat: `0x00263E30` is called by `0x003206E0`; those functions are documented on
  [battle units](../Characters-And-Objects/battle-units.md).
- Input: `0x00313F60` is called by `0x00253C70`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
