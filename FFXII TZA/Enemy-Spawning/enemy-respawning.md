---
title: "Enemy respawning: death counts, cooldowns, the group table that wakes a zone script, and the two-area memory"
kind: "system"
category: "Enemy spawning"
addresses: "00300530, 002395A0, 0032A100, 0032A160, 0032A150, 00235F50, 00235FB0, 002366E0, 00236670, 00235720, 00306E60, 00239710, 0050F8C0, 00306F00, 003250F0, 00307110, 00307030, 003070E0, 00233D20, 0026ADC0, 00307140, 00238B70, 00238AE0, 00307090, 002342F0, 00233780, 002368D0, 00235340, 00235330, 00237DF0, 00233C10, 00233440, 00233550, 00234990, 002352E0, 00300E40, 002350C0, 00328370, 003148F0"
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

The HP modifier `00300530` is the one path to a death. On its lethal branch, when the unit's stats
record at `+0x698` has kind byte `+0x05` = 1 (an enemy built from the enemy definition table,
[battle unit construction](../Characters-And-Objects/battle-unit-construction.md)), it takes the spawn
record at unit `+0x6A0` and increments its death count `+0x08` (`00300801`). It then reads the
frame counter through `0032A150`, divides it by `(int)(30.0 * [01DFE0B8])` with an unsigned `div`
(`00300820`) and stores the quotient at `+0x0C` (`00300829`): the second of the death.

The divisor is 30 at the 30 fps setting and 60 at 60 fps, so the stamp is in whole seconds at
either rate. It then calls the group table's death handler `00306F00` (`0030082F`). When that returns 1 the
group completed, and the modifier skips its own death presentation event (`00300836`); otherwise
it dispatches, when a local flag allows it, `0x200E` when its argument has bit 8, else `0x2007` or
`0x2008` by a second argument (`00300838`-`0030085F`).

### The authored limit and cooldown

`002395A0(table)` is the tail of the script verb that installs a zone's spawn table. The table is
`b_00` = entry count, `b_01` = whether keys are authored, `w_02` = row stride, rows from `+4`. For
each live-bank entry `i` whose flag bit 1 (committed) is clear (`002395E3`) it writes, with
`rand` = `00328370` (the shared gameplay generator,
[random number generators](../Random-Numbers/random-number-generators.md)):

```
rec.w_0A = row.b_00 ? row.b_00 + rand % (row.b_01 + 1) : 0      death limit
rec.w_10 = row.w_02 ? row.w_02 + rand % (row.w_04 + 1) : 0      cooldown, seconds
rec.dw_0C = 0 ; rec.w_08 = 0                                    stamp and count
rec.b_17 = rec.b_18 = table.b_01 ? row.b_06 : 0                 persistence key
```

Both numbers are rolled per entry, so two visits to one zone can give the same monster different
cooldowns. A committed entry keeps its numbers: the roll happens once per bank life.

### The clock

The counter `0208D45C` is advanced by `0032A100`, which the field frame `00234590` calls once per
frame (`002345CA`): when timer 0 reports done (`003EBB70(0)`) it restarts it (`003EBBB0(0, 0, 1)`,
`003EBD00(0)`), then reads the timer's value through `003EBA90(0)` and increments the counter only
when that value differs from the one it kept at `022C317C` (`0032A12A`-`0032A135`). The only other
writer is `0032A160`, which zeroes it, and its one caller is the battle runtime reset `00237DF0`
(`00237E37`). No save writes or restores it.

Other code reads the counter directly (`00319600`,
`003247F0`, `00317670`, `003191B0`); none of it is respawn code.

The same reset zeroes the transition stamp `02089374` (`00237E53`), sets the two field-history
words `02089372` and `02089370` to `0xFFFF` (`00237E5D`, `00237E64`) and clears the bank parity
`0208D454` (`00237E6B`).

The reset runs from the battle-state guard `00233C10`: twice when the
block pointer `02EBF190` is null (`00233C3F`, `00233C48`), once when the block's stamp is not
`0x05071901` (`00233C59`). Its other callers are the area reset `00239960` when the request byte
`0208D455` holds -2 (`0023998E`; the byte is a one-shot request, copied to `0208D456` and set to -1 before the test), `00238AA2` and `00394486`. An ordinary load whose block passes the
stamp test does not restart the clock.

### Two readers of the cooldown

The zone script reads the three fields through three verbs, each a wrapper around one accessor
that resolves the lane through the unit's lane map at `+0x40` (count at `+0`, slot bytes from `+1`,
`0xFF` empty) and the live bank `[0208E690] + slot * 0x250`:

| Accessor | Verb wrapper | Returns |
|---|---|---|
| `00235F50(lane)` | `0050F660` | the death count `+0x08`, or -1 |
| `00235FB0(lane)` | `0050FAB0` | `counter / fps - stamp +0x0C`, the elapsed seconds, or -1 |
| `002366E0(lane)` | `005101F0` | the cooldown `+0x10`, or -1 |
| `00236670()` | `0050FC90` | flag bit 0 of the unit's own entry (retired, awaiting re-entry) when bit 1 is set and bit 2 clear, else -1 |

The elapsed seconds come back as a signed int, so the script's own test is signed. The shipped zone
scripts compare the two verbs with a strict greater-than (every `btlAtelGetRespawnTime` call in the
corpus is `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`), so a cooldown of N seconds
passes at the first second where `floor(counter / fps) - stamp > N`, one second later than N.

The automatic spawn selector `00235720` ([enemy spawning](enemy-spawning.md)) reads the fields
directly and differently. It examines no entry at all when the active count `00308D90()` has reached
the cap byte `0208D458` (`00235758`-`00235766`, returns -1).

It skips an entry whose limit `+0x0A` is non-zero and whose count
`+0x08` has reached it (`002358A1`-`002358B0`). For an entry with flag bit 0 clear and bit 1 set
and a non-zero cooldown, it skips while `seconds - stamp < cooldown` as an unsigned compare
(`002358D1` `sub`, `002358D5` `cmp`, `002358D7` `jb`): the native gate re-admits at `elapsed >= N`.
An entry with bit 0 set, one that range retirement marked, skips the cooldown test altogether.

### After a runtime reset

A reset zeroes the counter but not the stamps in the live bank: the reset's body touches neither
bank pointer, and the initialiser only rewrites uncommitted entries. While a stamp is above the new
clock, the script accessor returns a negative elapsed time, so the scripts' test first passes at
second `stamp + N + 1` of the new clock; the selector's unsigned subtraction wraps to a large value
and re-admits the entry at once. The accessor can even return -1, its own failure value, when the
stamp is exactly `counter + 1`.

### Registering a group member

A zone script puts an enemy in a group with verb `0x3030` `btlAtelSetEventFlagGroup(group, mode)`.
Its handler `0050F8C0` pops two ints and calls `00239710(actor, mode, group)`, which needs the
actor's battle unit (`0031B760`, else returns -1) and writes unit `+0xE98` = `group` and `+0xE99`
= `(old & ~3) | (mode == 1) | (mode == 2) << 1`, bits 2-7 kept (`00239746`-`00239766`), then calls
`00306E60(unit, 1)`.

`00306E60(unit, add)` is the only writer of the member mask. It returns without effect when the unit
is null, its stats record `+0x698` is null or not kind 1, or its group byte `+0xE98` is 0. It
resolves the unit's slot as `002360D0(map at +0x40, 00263D30(actor at +0x10))` and rejects a
negative. The bit is `(int64)(int32)(1 << (slot & 31))`: a 32-bit shift, sign-extended, so slot 31
covers bits 31-63 and slots 32 and above alias onto `slot & 31`. With `add` set the member mask
gains the bit, otherwise it loses it; the dead bit is cleared either way (`00306EEA`).

Range retirement (`002350C0`, `002352BB`) is the one caller with `add` = 0: a retired member leaves
the checklist without dying.

### Completing a group

`00306F00(unit)` runs on every lethal branch of the HP modifier; its own gates keep only a kind-1
unit with a non-zero group byte. With the same gates as the registration and the same slot
resolution it sets `group table[group - 1].deadMask |= bit` (`00306F78`) and tests
`(memberMask & deadMask) == memberMask` (`00306F7C`-`00306F83`). The test is a mask comparison,
not a count: killing a member twice changes nothing, a unit outside the member mask cannot complete
the group, and a group with an empty member mask completes on its first death.

On completion it locks the party (next section) and chooses an arm by `+0xE99` bit 0:

- mode 1 (`00306FC9`-`00306FE8`): clear unit flag bit 47, set the group table's flag bit 0, dispatch
  presentation event `0x2005`;
- any other mode (`0030700C`-`00307012`): set unit flag bit 47, dispatch `0x2008`. The flag is
  raised later by the reaction handler `003250F0`: on the death events it sets unit flag bit 33
  (`00325185`) and, when bit 47 is set (`0032519C`), calls `00307110`, which clears bit 47 and
  sets the group table flag (`0030711A`-`00307133`).

Nothing remembers that a group completed. A member that respawns and re-registers clears its dead
bit, and its next death completes the group again: a room can be cleared twice.

### The lock

Three calls run on every completion, each with argument 1 (`00306FAD`-`00306FBC`):

- `00307140(on)` calls `002E1C20(0xC)` ten times when on (`002E1CA0(0xC)` when off): the row-12
  capability inhibitions ([party roster and control
  suppression](../Party/party-leader.md)), then `00359200(on, 2)`,
  `00359330(2, 1, on)` and `0026BD20(2, on == 0)`;
- `00238B70(on)` sets or clears `02089340` bit 5 and, for every battle-unit slot whose byte `+0`
  has bit 4, posts `002E7C10(actor, actor, 0x30B, 0)`;
- `00238AE0(on)` sets or clears `02089340` bit 7.

The zone script releases the lock with the same calls' off forms through its own verbs; the group table
never releases it. The next area entry does clear the two `02089340` bits: `002342F0` opens with
`02089340 = (02089340 & 0xFFFFC01E) | 0x10`, which also clears the "nothing pending" bit 1; the
row-12 inhibitions stay until their off form runs.

### Delivering the completion to the script

`00307030` runs once per field frame from `00234590` (`00234717`). It does nothing while the gate
`00233D20` is closed: `02089340 & 0xF00` must be 0 and time-stop request 10 must not be raised
(`00226BD0(10)` = 0, [the time-stop
registry](../Engine-Core/time-stop-and-freeze.md)).

With the gate open it walks the 64 entries; for each with flag bit 0 it clears the bit and calls
`0026ADC0(3, i + 1)`, which stores the group number in word 3 of the 64-word table at `[02098E68]`
when the index is below 64, `02098E20` bit 0 is set and the pointer is non-null.

Zone scripts wait on that word (`scratch1 @0x06`) with `waitv`, which waits while it is zero; the word is cleared on
every field transition ([field runtime](../Characters-And-Objects/field-runtime.md)).

`003070E0` reports whether any entry has flag bit 0. The per-unit frame `00233F70` calls it
(`00234095`) and sets `02089340` bit 1 when nothing is pending.

### Resetting the group table

`00307090` walks the 64 entries four at a time (`0x60` per step from `02EC13D0` to `02EC19D0`),
zeroing both masks and clearing flag bit 0 (`and byte ptr [...], 0xFE`). Its one caller is the area
initialiser `002342F0` (`0023442D`), straight after the bank rotation, so membership is rebuilt by
script after every area entry. The group table is BSS and starts at zero.

### The two banks and the return window

`002368D0` allocates two banks of `0x9400` bytes tagged `btlKeepCharWork1` and `btlKeepCharWork2`
at `0208E690` and `0208E698`, 64 spawn records of `0x250` each, and sets the return window
`0208936C` to 300 (`00236A0D`). Bank 1 is the live bank; bank 2 holds the previous area.

`00233780` runs once per area initialisation (`00234423` in `002342F0`), after the area's own reset
and before the group table reset, and returns at once when either bank pointer is null. It reads the
entered field id from `003148F0`, the counter from `0032A150`, and restores when both hold
(`002337D6`-`00233803`):

```
field == 02089372                                          the field from two transitions ago
(u32)(counter - 02089374) <= (u32)((int)(30.0 * [01DFE0B8]) * 0208936C)    unsigned, ja wipes
```

A restore exchanges the two banks' contents through a `0x9400`-byte stack buffer (bank 2 to the
stack, bank 1 to bank 2, the stack to bank 1); the pointers stay. A wipe copies bank 1 over bank 2,
zeroes bank 1 with one `memset`, and sets the 64 spawn-history counters of the new parity to 1.
Both branches flip the parity byte `0208D454` and then shift the history: `02089372 = 02089370`,
`02089370 = field`, `02089374 = counter`. The compare is against the field from two moves ago, so
the restore fires on the pattern A, B, A within the window; entering B again from B wipes.

The window is in seconds because the counter difference is in frames and the multiplier is the
frames per second. `00235340(w)` stores `w`, or 300 when `w` is negative (`cmovs`); `00235330`
returns it. Both reach script only through verb `0x306C` `btlAtelSetMapJumoKeep` (`005107F0`), which
no shipped script calls, so the window is 300 seconds everywhere. After a reset the previous-field
word is `0xFFFF` (sign-extended to -1 at `002337CD`) and `003148F0` never returns a negative, so the
first rotation after any reset wipes.

### The spawn-history counters

`0208D354` holds two banks of 64 `u16` counters, selected by the parity `0208D454`. The wipe sets the
new parity's 64 to 1 (`002339CC`-`002339E2`); the unit installer `0023A570` reads a row's counter,
stores its low byte at the spawn record's `+0x12` and writes back `old + 1`, or 1 once `old` reaches
`00254A40()` ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)). The
reset `00237DF0` clears the parity, not the counters.

### What the save image carries

`00233440(image)` zeroes a `0x20010`-byte image, copies bank 2 to `+0x10` and bank 1 to `+0x10010`
in `0x128` passes of `0x80` bytes, and stores `02089372` at `+0` and `02089370` at `+2`.
`00233550(image)` copies image `+0x10` back into bank 2 and restores the two words; it never touches
bank 1.

Its two callers are in the slot-0 restore `005843E0` (`0058443B`, `0058445E`), so only a load
of the field-transition autosave restores bank 2 and the history; a manual slot restores neither
([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)). The window, the stamp, the
parity and the counter are in no save.

### Killing or tearing down by group

Four helpers walk the 32 battle-unit slots through `00321170` and act on kind-1 units:
`00234880` tears down every unit whose group byte is non-zero, `00234990(mask)` those whose
`mask >> (group & 31) & 1` is set (`00300E40(unit, 0)`), and `00234A10`/`00234A80(mask)` set or
clear unit flag `0x800` (the script's hide bit) on the masked subset. `002352E0` runs
`00300520(stats, 0, 0, 0)` on every kind-1 unit, which goes through the HP modifier and therefore
records a death for each. The mask test keeps 5 bits of the group id, so ids above 32 share a bit
with `id - 32`.

The teardown `00300E40(unit, keepMark)` runs the spawn record clear `00237080` (flags
`& 0xFFFFFF7A`, the word `+0x16` = `0x00FF` so the key `+0x17` is zeroed too, `+0x78`-`+0x7C` zeroed) only when `keepMark` is 0 (`00300F5D`-
`00300F68`). Range retirement is the one caller passing 1, so a retired entry keeps its bit 0 and
its transient state while every other teardown clears them.

## Layouts

Struct SpawnGroupTable base=`02EC13C0` count=64 size=`0x18`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u64` | memberMask | bit (slot & 31), sign-extended from 32 bits; set by `00306E60`(unit, 1) |
| `08` | `u64` | deadMask | set by `00306F00`, cleared by `00306E60` either way |
| `10` | `u8` | flags | bit 0 = completion pending for `00307030` |
| `11` | `u8[7]` | padding |  |

Struct SpawnRecordRespawnFields in the spawn record (`0x250` bytes, spawn-record-fields page):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | flags | bit 0 retired awaiting re-entry, bit 1 committed, bit 2 released |
| `08` | `u16` | deathCount | `00300801` |
| `0A` | `u16` | deathLimit | `002395A0`: base + rand % (range + 1), or 0 |
| `0C` | `u32` | deathSecond | `00300829`: counter / fps |
| `10` | `u16` | cooldown | `002395A0`: base + rand % (range + 1), or 0; whole seconds |
| `12` | `u8` | historyCounter | low byte of the row's `0208D354` counter at install |
| `17` | `u8` | persistenceKey | zeroed with +`0x16` by `00236860` / `00237080`; +`0x18` the authored key the resets restore it from |

Struct SpawnKeepImage size=`0x20010`   (`00233440` writes, `00233550` restores):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00000` | `u16` | fieldTwoAgo | `02089372` |
| `00002` | `u16` | fieldLast | `02089370` |
| `00010` | `u8[37888] bank2` | [0208E698]; restored by 00233550 |  |
| `10010` | `u8[37888] bank1` | [0208E690]; written, never restored |  |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0208D45C` | `u32` | frame counter, +1 per field frame whose timer 0 moved (0032A100); 0 at reset |  |
| `01DFE0B8` | `f32` | frame-rate scale, 1.0 at 30 fps, 2.0 at 60; fps = (int)(30.0 * scale) |  |
| `02089370` | `u16` | last field | `02089372`  u16  field two transitions ago |
| `02089374` | `u32` | counter at the last transition |  |
| `0208936C` | `i32` | return window, seconds (300) |  |
| `0208D454` | `u8` | bank parity | `0208D354`  u16[2][64]  spawn-history counters |
| `02EBF190` | `void*` | battle-state block; dword +0 stamp 0x05071901 |  |
| `02089340` | `u32` | battle flags: bit 1 nothing pending, bit 5 and 7 the lock, bits 8-11 close the gate |  |
| `02098E68` | `void*` | the 64-word field table; word 3 receives the completed group |  |

## Shipped data

- Every spawned unit's entry preamble calls `btlAtelSetEventFlagGroup` right after its level is
  set: 6,746 calls in 502 of the 1,114 zone scripts, 6,206 of them `(0, 0)`. The group argument is
  0-5 and the mode 0-2. Group 0 means no group: both group table paths skip it before indexing.
- All 1,765 `btlAtelGetRespawnTime` calls are `btlAtelGetElapseTime(i) > btlAtelGetRespawnTime(i)`
  with the same lane; 1,737 add `|| btlAtelGetDeadCountNow(i) == 0` and 28 add
  `|| btlAtelGetRespawnCause() == -1`.
- No shipped script calls `btlAtelSetMapJumoKeep`; the window is the native 300 seconds.
- Of the 239 scripts that import the completed-group word, 236 park on it with `waitv`.

## Operations

A kill, in order: the HP modifier bumps `+0x08` and stamps `+0x0C`; `00306F00` sets the dead bit and
tests the mask; on completion the lock engages and the arm is chosen; the reaction handler raises
the flag for a mode other than 1 when the death track ends; the next field frame with an open gate
posts the group number; the zone script wakes and runs the aftermath.

An area entry, in order (`002342F0`): the cap `0208D458` = 28, the area reset `00239960` when
requested, the bank rotation `00233780`, `003221B0`, the group table reset `00307090`, then the zone
script re-registers every member and reinstalls the spawn table, whose initialiser rolls only the
uncommitted entries.

## State

The live bank and the history bank, the four history and window globals, the frame counter and its
last timer value, the parity and the two counter banks, the group table, unit `+0xE98`/`+0xE99` and flag
bits 33 and 47, and word 3 of the field table. Only bank 2 and the two field words reach a save,
and only the autosave's restore brings them back.

## Modding notes

- A respawn wait is `cooldown + 1` seconds by script and `cooldown` seconds by the native selector,
  both in whole seconds at either frame rate. Changing `>` to `>=`, or comparing in frames, shifts
  every respawn in the game.
- The death limit and cooldown are rolled per entry from `base + rand % (range + 1)`; set the range
  to 0 for a fixed value.
- To make a group complete, set its dead bits; nothing counts deaths. A group id above 32 shares a
  mask bit with `id - 32` in the teardown helpers, and a slot of 31 or more in a lane map aliases
  in the group table: keep groups at 1-32 and slots below 31.
- Range retirement unregisters a member and skips its cooldown on return; routing retirement through
  the death path, or clearing flag bit 0 in a teardown, changes both.
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
