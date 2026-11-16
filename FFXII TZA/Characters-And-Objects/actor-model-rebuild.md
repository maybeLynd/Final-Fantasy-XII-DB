---
title: "Actor model rebuild: the state machine that reloads an actor's model, attachments and body for its current definition, and what runs it"
kind: "system"
category: "Characters and objects"
addresses: "0x0037B4D0, 0x0037B4C0, 0x00377DB0, 0x02ADD0D8, 0x002EBB80, 0x002E96B0, 0x002E96D0, 0x0031C250, 0x0031BEC0, 0x0031BE30, 0x002EB7A0, 0x002EAE20, 0x002EB540, 0x002E9810, 0x002E97C0, 0x002E4C20, 0x002E4C30, 0x002E3DC0, 0x002E3F00, 0x002EBD60, 0x002E3C20, 0x002E3110, 0x002E28E0, 0x002EBC90, 0x0031C540, 0x0026D610, 0x00321380, 0x002E8450, 0x0036EC10, 0x0036F0F0, 0x0036ECA0, 0x002ED910, 0x022D9AB0, 0x022D9AE0, 0x00320170, 0x002EB9D0, 0x002EB490, 0x002EC6B0, 0x0037CB90, 0x00377A90, 0x0031BAC0, 0x00233AD0, 0x002DEBD0, 0x002DEB90, 0x0037C730, 0x0037C980, 0x0037CA00, 0x0037CA80, 0x0037CB50, 0x0037C1A0, 0x0037CE80, 0x0037C8D0, 0x003523B0, 0x005101B0, 0x00359880, 0x02EBF3D0, 0x02EBF3F0, 0x0034E3E0, 0x00233AA0, 0x0031C2F0, 0x00233CF0, 0x0037CF50, 0x00510160, 0x00342C90, 0x0037CFD0, 0x0037CB80, 0x0037CB10, 0x002EA6A0, 0x002E8FD0, 0x022C8010, 0x00359800, 0x00359A30, 0x0035A0A0, 0x0035A240, 0x002E6090"
---

## What the player sees

When a character joins, leaves or changes job, or a battle starts, each party member briefly
vanishes, its model, held items and body are swapped for the ones its current definition calls
for, and it reappears in place. A scene waits while `partyallread` runs. The frames the member is
invisible are the loads this machine waits on.

The model a member should have comes from one number: a byte kept for its roster slot in slots 0 to 3, otherwise a
number in its battle unit's stats record. The number's high byte picks one table, or a second table that leads to a
third, and its low byte the row that holds the model. Only a model that differs from the bound one is released and
loaded again.

## How it works

### The rebuild record

The machine `0x0037B4D0(record)` (thunk `0x0037B4C0`) works on a 12-byte record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | actor, as an encoded image pointer (`0x0020E620` / `0x0020E600`) |
| `+0x04` | `u32` |  | handle of the binding entry being waited on |
| `+0x08` | `u8` |  | state 0..23 in the bits under mask `0x7F`; bit `0x80` = place the actor at the end |
| `+0x09` | `i8` |  | party slot, -1 for no slot |
| `+0x0A` | `u8` |  | pass counter for states 13-15 |
| `+0x0B` | `u8` |  | saved value of `0x002DEBD0`(), restored by `0x002DEB90` at the end |

Every transition keeps bit `0x80` and writes the new state. A call runs states until one has to wait
(return 0) or state 23 is reached (return 1). An actor that no longer resolves returns 1 at once,
and nothing runs while `0x00377DB0()` (the dword `0x02ADD0D8`) is 0.

### The states

Binding entries, handles, the ready bit and the lane tests are those of
[script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md). A part id is the one
`0x0031BEC0(actor, part, n)` returns, mapped through `0x002EB7A0`; a value of 0 or less means no part.

`0x0031BEC0` first asks `0x0031C0F0(slot, part, n)` with the actor's roster slot, the index of the four `0x00263750`
actors that equals it, or −1 for any other actor and a null one (`0x0031BEE3`-`0x0031BF00`). When that answer is
negative it asks `0x0031C000(stats + 0x50, part, unit, n)` for the unit `0x00263E30(actor)` and its stats record
`[unit + 0x698]`, and answers −1 without either (`0x0031BF09`-`0x0031BF3A`).

A part's current id is `0x002E96D0(actor, k, n)`: dword `+4` of the slot at context `+0x30` for k 0, `+0x60` for
k 1, `+0x90` for k 2 and 4, and `+0xC0 + n × 0x30` for k 3; any other k, a null actor or a missing context
gives 0 (`0x002E96D0`-`0x002E975F`).

The link that states 7-15 hand to `0x002E3110` is `0x0031BE30(actor, part, n)`: `0x10A`, except for part 8 of a
unit whose stats record `[unit + 0x698]` has byte `+5` = 1, where it is the dword of the table `0x00D107F8`
indexed by byte `+0x40 + n` of the unit's definition `[unit + 0xE60]`, for n 0 and 1 (`0x0031BE44`-`0x0031BEA0`).

States 2, 8, 11 and 14 resolve their handle first, and a handle that no longer resolves is requested
again from the current definition (`0x002EAE20(id, 0)`) without advancing. State 20 waits on its
handle as it is, and state 17 waits on the lane with no recovery: `0x002E4C30` returns −1 once the lane
record is gone (the entry's `+0x1E` is negative, `0x002E4C37`) or its stamp `+0x5C` differs from the entry's
`+0x24` (`0x002E4C52`), so neither wait can end after its target is retired.

| State | What it does | Next |
|---|---|---|
| 0 | hides the actor (`0x002EBB80(actor, 0)`) | 1 |
| 1 | compares the actor's bound id (`0x002E96B0`, context `+0x04`) with the id its definition calls for (`0x0031C250`, then `0x002EB7A0`) | 3 when equal; 22 when the new id is negative; else 2 |
| 1 (changed) | when the old id is 0 or more: `0x0025AB30(actor)`, the old main entry's release when that id is above 0 (`0x002EBD60(id, 0)`, `0x002E3F00(id, lane)`, `0x002E3DC0(id)`) and the release of each attached part whose id will change; then sets actor `+0x23` bit `0x1` and requests the new id | 2 |
| 2 | waits for the main entry; then `0x002EBC90(actor, 0, 0)`, the variant bytes from `0x0031C540(0x003589B0(actor))` (1 and 0 when it fails) into `0x0026D610`, the bind `0x002E28E0`, `0x002681D0`, `0x002E5C70` with the three floats at `[actor + 0xB8]`, `0x002EAC90`, `0x002E49B0(actor, 0)`, `0x002E4A40`, `0x002E8450(actor, 0x00321380(0x003589B0(actor)) or 0)` (`0x0037B763`-`0x0037B80D`) | 3 |
| 3 | — | 4 |
| 4 | releases the actor's pool entry at `+0x20` (`0x0036EC10`), looks up the new pool id (`0x002ED910`) and acquires an entry (`0x0036F0F0`) into `+0x20`; a negative id leaves the released index in `+0x20`, so the next rebuild releases it again | 5; 7 when the id is negative |
| 5 | waits until the pool entry's state byte is 3 (`0x0036ECA0`); a negative index in `+0x20`, when `0x0036F0F0` returned -1, skips the wait (`0x0037B8B3`) | 6 |
| 6 | — | 7 |
| 7-9 | part 0 in the slot at context `+0x30`: when its id changes, detaches it (`0x002E3C20(actor, 0, 0)`) and releases the old entry; a new id is requested (actor `+0x23` bit `0x2`), waited on, and attached (`0x002EBC90(actor, 2, 0)` at `0x0037B99D`, `0x002E3110(actor, 0, 0, entry)` with link `0x0031BE30`) | 10 |
| 10-12 | the same for part 1 in the slot at `+0x60` (bit `0x4`, `0x002E3110(actor, 1, …)`) | 13 |
| 13-15 | the same for part 8, entry n, in the slot at `+0xC0 + n × 0x30` (bit `0x8` for n 0 and `0x10` for n 1, `0x0037BB65`-`0x0037BB74`; `0x002EBC90(actor, n + 4, 0)`, `0x002E3110(actor, 3, n, …)`), run for n = 0 and 1 with the counter `+0x0A` | 16 |
| 16 | the motion lane: `0x00320170(0x003589B0(actor), &lane)` gives the lane the definition calls for (`0x0037BC1E`-`0x0037BC29`), and a non-zero answer, a negative lane or one `0x002EB9D0` does not give back goes to 18 (`0x0037BC30`-`0x0037BC4F`); when it is valid, claimable (`0x002EB9D0`) and differs from context `+0x12`, it calls `0x002E6BB0(actor, 1)`, stores it in context `+0x12` (`0x002EC6B0`), which also points the render record's `+0x42C` at the lane's motion resource and `+0x430` at lane 0's, both from the model's entry in `0x02161DA0` (`0x002EDD20`, `0x002EDE20`; the handle of 0 for a negative lane), and clears bit `0x40000` of render record `+0x284` for a negative lane or one of 16 or more, and requests it (`0x002EB490`) | 17; 18 otherwise |
| 17 | waits until the lane is loaded: `0x002E4C30(entry, lane)` for the main entry `[context + 8]` and the lane at context `+0x12` (`0x0037BCE0`-`0x0037BCFD`) answers 1 once bit `1 << lane` of the lane record's loaded mask `+0x24` is set, 0 while it is clear, and 1 at once for a negative lane (`0x002E4C54`-`0x002E4C65`) | 18 |
| 18 | `0x002EAC90`, `0x002E8450(actor, 0x00321380(0x003589B0(actor)) or 0)` (`0x0037BD2C`-`0x0037BD55`), and `0x002699D0` in read-in mode | 19 |
| 19 | the body replacement: `0x0037CB90(id, 0x002657E0(actor), 0x00263FC0(actor))`; a replacement is found or created with `0x002EB540(id, 0)` | 20; 22 when there is no replacement |
| 20 | waits, then `0x002EBC90(actor, 3, 1)`, `0x002E3110(actor, 4, 0, entry)`, `0x002EAC90` | 21 |
| 21 | — | 22 |
| 22 | places the actor when record bit `0x80` is set and the slot is not negative; shows it (`0x002EBB80(actor, 1)`), `0x00233AD0(actor)`, `0x00263560()` for a slot, `0x00359B10()`, restores `0x002DEB90(+0x0B)` | 23 |
| 23 | done | returns 1 |

`0x002E96B0(actor)` answers the dword `+0x04` of the actor's context `+0xC0`, and -1 for a null actor or a null
context (`0x002E96B0`-`0x002E96C5`).

`0x0025AB30(actor)`, the per-`+0x04` teardown, reads the actor's byte `+0x04`: for 1 it calls `0x002E3AF0(actor)` and
answers what that returns; for 2 it calls `0x003DE5F0(actor)` and for 3 `0x002E3D00(actor)`, both answering 0; for any
other value it calls nothing and answers 0. In every case it then stores the word `0xFF00` at `+0x04`
(`0x0025AB3A`-`0x0025AB8F`).

`0x0031C250` takes the definition's selector: for an actor in roster slots 0-3 the byte at
`[0x02EBF190] + 0x5A90 + slot × 2` (`0xFFFF` when `0x00322C50(0x17, slot)` fails or the byte is `0xFF`),
otherwise word `+4` of the unit's record `+0x698` (`0xFFFF` without one). `0x0031C2F0` maps it to a
model id: `0xFFFF` gives −1; a high byte of 0 gives the dword at `+0x70` of the `0x02EBF130` row for
the low byte (bounded by `0x00322C50(2, ·)`); a high byte of 1 goes through the `0x02EBF120` row's
first byte to a `0x02EBF150` row's first dword; anything else gives −1.

A null actor gives the selector `0xFFFF` (`0x0031C260`), and `0x0031C250` ends in a tail jump to `0x0031C2F0`
with the selector (`0x0031C2A1`, `0x0031C2E9`), so its answer is the model id. A row is the table's data
`0x0020E600([table + 0xC])` plus the index times the stride word `+8`. The high-byte-1 path answers −1 when the
low byte is above the `0x02EBF120` count `+4` less one, or that row's first byte above the `0x02EBF150` count `+4`
less one, both compared unsigned (`0x0031C348`, `0x0031C3A0`).

Only the high-byte-0 path refuses an unbound table: `0x00322C50(2, ·)` gives a null `0x02EBF130` a count of 0
(`0x00322CA6`, `0x0032302A`) and refuses every index (`0x0032303B`), so the answer is -1 (`0x0031C40B`). With `0x02EBF130`
bound but its data null (`0x0031C42F`) the path reads the dword at address `0x70` (`0x0031C45D`-`0x0031C45F`). The
high-byte-1 path tests nothing: a null `0x02EBF120` or `0x02EBF150` gives a count of 0 that every index passes, and a
null table or null data then reads address 0 (`0x0031C380`-`0x0031C383`, `0x0031C3E5`).

`0x0031C540(id, &colour, &variant)` zeroes both outputs and answers −1 unless battle flag `0x02089340` bit `0x10`
is set and the id resolves through `0x003588B0` and `0x00263E30` to a unit with a stats record `[unit + 0x698]`,
and −2 when that record's byte `+5` is not 1 (`0x0031C54A`-`0x0031C592`). Otherwise it reads bytes `+0x12` and
`+0x11` of the definition `[unit + 0xE60]` and answers 0 (`0x0031C5A2`-`0x0031C5B5`); state 2 passes the variant
`+0x11` and the colour `+0x12` to `0x0026D610` (`0x0037B788`-`0x0037B7A5`).

`0x00321380(id, &class)` writes −1 to the output and answers −1 unless the flag is set and the id resolves to a
unit, and −2 when the unit has no stats record (`0x0032138F`-`0x003213C1`). Otherwise it asks
`0x00321400(word stats + 0x50, &class)` and answers 0 whatever that gives (`0x003213D8`-`0x003213E3`). `0x00321400`
stores byte `+0x26`, the motion class, of the main-hand equipment row in `0x02EBF0F8` for that id, or −1 for
the id `0xFFFF` or a row whose slot bits `+0x07` are `0x20` or more (`0x00321458`-`0x0032147B`).

States 2 and 18 replace a negative answer of `0x00321380` with 0 but pass a −1 class on as it is (`0x0037B7B8`-`0x0037B7BD`,
`0x0037BD3F`-`0x0037BD41`). `0x002E8450(actor, class)` stores the class's low byte at context `+0x150` when the actor
has a context (`0x002E845C`), and copies it to render record `+0x40C` when the context's dword `+0` is not −1,
its word `+0` is not `0xFFFF` and the render record `[0x022C6F28] + word × 0x740` has a non-zero `+0x284`
(`0x002E846E`-`0x002E84A0`).

`0x00320170(id, &lane)` answers through `0x003202F0(0, &lane)`, which gives −1 and a lane of −1, when battle flag
bit `0x10` is clear (`0x0032018F`). With it set, an actor `0x003588B0(id)` that is one of the four `0x00263750` actors
goes to `0x00320230(slot, &lane)` (`0x003201B0`-`0x0032021C`), and any other to `0x003202F0` with its unit's stats
record `[unit + 0x698]`, or with 0 when it has no actor or unit (`0x003201C3`-`0x003201F2`).

`0x002EC6B0(actor, lane)` does nothing for a null actor or one without a context; it stores the lane byte at
context `+0x12` first (`0x002EC6E3`). For a lane of 0 or more it stops there when the context's dword `+0` is
−1 (`0x002EC6EF`). Otherwise both handles come from the lane record the main entry `[context + 8]` names, when
its stamp matches: the lane's handle `+0x60 + lane × 4` when bit `1 << lane` of the loaded mask `+0x24` is
set, else 0 (`0x002EC70D`-`0x002EC742`), and lane 0's handle `+0x60` when bit `0x1` is set, else 0
(`0x002EC766`-`0x002EC789`).

`0x002EDD20` and `0x002EDE20` store them encoded with `0x0020E620` at render `+0x42C` and `+0x430`
(`0x002EDD54`, `0x002EDE54`). A negative lane stores `0x0020E620(0)` at both directly (`0x002EC7A8`-`0x002EC808`), and bit
`0x40000` of `+0x284` is cleared for a negative lane or one of 16 or more (`0x002EC79D`, `0x002EC835`). Every
render store needs the context's word `+0` to name a render record with a non-zero `+0x284`.

`0x0026D610(actor, b, c)`, the store of state 2's variant bytes, jumps to `0x002E6090` for a class-3
actor, which writes `b` and `c` to `[actor + 0xC0] + 0x14C` and `+0x14D` when the context exists.

`0x002EBB80(actor, on)` is the hide and show: for an actor of kind `0x60` with a context it writes
context `+0x10` bit `0x8` and refreshes visibility (`0x002E8FD0`), which shows the model when
`+0x10 & 0xB` is `0xB`, or `+0x10 & 3` is 3 when context `+0x11` bit `0x20` is set, together with
`+0x11 & 6` = 6 and `+0x164` = 0. An actor with `+0x11` bit `0x20` set is therefore not hidden by
state 0.

In read-in mode (`0x02EBF3FC` = 1) the release paths of states 1, 7, 10 and 13 also call `0x002E42D0`,
and placement also calls `0x002E8060` and `0x002EB030(actor, 0x1001)`.

The pool of state 4 is two arrays of `0x18`-byte entries: 2 at `0x022D9AB0` and 4 at `0x022D9AE0`,
chosen by `0x002647C0(0x00264EC0(actor))`. Each entry holds a state byte `+0`, two index bytes `+1`
and `+2`, two load handles `+0xC` and `+0x10`, the id `+0x14` and a count `+0x16`.

An index from `0x0036F0F0` names entry `index & 0xF` of `0x022D9AE0` when any of its bits `0xF0` is set and of
`0x022D9AB0` otherwise (`0x0036EC14`-`0x0036EC36`, `0x0036ECA7`-`0x0036ECCB`). The release `0x0036EC10` lowers that
entry's count `+0x16` by one and holds it at 0 (`0x0036EC3D`-`0x0036EC4A`); it frees no load, which waits until
`0x0036F0F0` takes the entry again. `0x0036ECA0` answers the entry's state byte `+0`, and 0 for a negative index
(`0x0036ECA4`); `0x0036EC10` does nothing for a negative index (`0x0036EC12`).

`0x0036F0F0`
returns an entry already holding the id with its count raised, or takes the first entry whose count
is 0, frees its old loads (`0x001DC100`, `0x00369800`) and starts the new one (`0x0036ED50`); it returns
`(+2 << 4) | +1`, or −1 when every entry is in use.

It returns −1 at once for a negative id (`0x0036F104`). A reused entry must have a non-zero state byte; its
byte `+3` is cleared (`0x0036F11C`). The old loads of a taken entry are freed only when its handle `+0xC` is
set (`0x001DC100` through `0x002DF440`, then `0x00369800` on `+0xC` and `+0x10`), and `+0x4` to `+0x13` are
zeroed (`0x0036F1C8`-`0x0036F1FF`); the count is set to 1 and the id stored (`0x0036F21C`, `0x0036F220`).

`0x002ED910` takes the id from `0x003212E0` and
otherwise from word `+6` of the model's `0x002ED950` row. With no actor it skips `0x003212E0` (`0x002ED91F`), and
with no row it returns `0x003212E0`'s negative answer, or −1 with no actor (`0x002ED943`).

Placement (state 22) reads the base position and facing from `0x00377A90` and asks `0x0031BAC0` for the
slot's position; when that fails it offsets x by ±1.0 (slot bit `0x1`) and z by ±1.0 (slot bit `0x2`). It
then calls `0x002681D0`, sets the position (`0x0026AF80`), the facing and movement heading from
`0x00377A90` even when `0x0031BAC0` supplied the position (`0x0026B620`, `0x0026A0D0`), the
separation weight from `0x00265950` (`0x0026DAC0`), and calls `0x002EAC90`, `0x002ECA00(actor, 1)`,
`0x002E49B0(actor, 0)` and `0x002E4A40`.

`0x002E49B0(actor, point)` acts only on an actor whose byte `+0x03` has `0x60` under the mask `0xE0`, with a
context at `+0xC0` and a body at the context's `+0x138` (`0x002E49B6`-`0x002E49E5`). A null point is replaced by
the address of the body's `+0x30` (`0x002E49D9`-`0x002E49DE`). It calls `0x0026E530(point, body + 0x50)` and
writes bit `0x1` of the answer's low byte to bit `0x80` of the actor's byte `+0x0B` (`0x002E49E7`-`0x002E49FA`).
`0x0026E530` itself stores 16 bytes through its second argument on every call (`0x0026E5A1`), so each such
call also rewrites the 16 bytes at the body's `+0x50`.

### What runs it

| Runner | Record | How |
|---|---|---|
| `partyallread` (`0x3EB`, begin `0x0034CCD0` → `0x0037C980`) | `0x02EBF3F0` | a scheduled task (`0x002F16B0`) with callback `0x0037C730`, slots 0 to 3, read-in mode 1 |
| `partyallread2` (`0x46F`, `0x0034D8B0`) and `summontopartyread` (`0x207`, `0x0034FE80`) → `0x0037CA00` | `0x02EBF3F0` | the same task, slots 3 down to 0, mode 1 |
| `summonread` (`0x203`, `0x0034E1F0`) and `0x0031A300`, `0x00324380`, `0x003261D0`, `0x003273D0` → `0x0037CA80` | `0x02EBF3F0` | slots 0 to 3, mode 0 |
| the world tick `0x00314020` → `0x0037C1A0` | `0x02EBF3D0` | each slot set in the mask `0x02EBF3E0`, one at a time, lowest slot first; `0x02EBF3DE` is a flag, 1 while a slot's run is under way (`0x0037C27F`) and 0 once the machine returns 1 (`0x0037C296`), and while it is 1 the next tick runs the machine on the lowest slot still in the mask without refilling the record (`0x0037C1E8`); otherwise the record is filled first (`0x0037C1F5`-`0x0037C254`: actor from `0x00263750`, state 0, bit `0x80` clear, the pass counter zeroed, `+0x0B` from `0x002DEBD0`, `0x002DEB90(1)`, the empty stub `0x0016D6A0`, actor `+0x23` = 0); a slot whose actor does not resolve or is not ready when reached (`0x002EA6A0`: actor `+4` = 1, a context at `+0xC0` whose dword `+0` is not −1, and the main entry `[context + 8]`'s ready bit `+0x18` bit `0x2`, `0x002EA6A5`-`0x002EA6C9`) is removed from the mask without a rebuild; a finished slot is removed and the next set slot starts in the same tick (`0x0037C29D`-`0x0037C2B6`), while a waiting machine ends the tick (`0x0037C294`) |
| `setupbattle` (`0x56`) poll `0x003523B0` | the verb's | `0x0037CE80` fills the record with bit `0x80` set and the verb's slot, then the machine runs each frame; the poll's step byte `+0xC`: at 1, `0x0037CE80(record, actor, byte +0xD)`, step 2 and a first machine run in the same call (`0x003523EE`-`0x00352402`); at 2, while the machine has not reached state 23, it writes `0x022C253D` = 1 (`0x00314D40(1)`) and answers 1 (`0x003523D4`-`0x003523DE`), and at state 23 step 3; at 3 it calls `0x002681C0(actor)` and answers 0 (`0x00352413`-`0x00352424`); any other step writes `0x022C253D` = 1 and answers 1 |
| `btlAtelSetUnit` (`0x3001`), begin `0x00510160`, poll `0x005101B0` | the verb's | the begin applies the unit (`0x0023A3B0`, with the value `0x00267E10` pops, `0x00510173`-`0x0051017D`) and, when `0x00237650(actor)` is non-zero, fills the record with `0x0037CF50` (slot −1, bit `0x80` clear); the poll runs the machine while `0x00237650` stays non-zero, answering 1 while it waits and 0 once it returns 1, and answers 0 when `0x00237650` is 0 (`0x005101BC`-`0x005101DA`) |
| the scene step `0x00359880` | `0x022C8018` | for each scene actor with `+0x14` bit `0x80` set, `0x002647B0` = 0 and context `+0x11` bit `0x1`, `0x0037CE80(record, actor, −1)` and the machine |

`0x0037C730` fills the record for the current slot (actor from `0x00263750`, state 0, bit `0x80` clear,
counter 0, `+0x0B` from `0x002DEBD0`, `0x002DEB90(1)`, actor `+0x23` = 0), runs the machine until it
returns 1, adds the step to the slot, and repeats until `0x0037CB50` reports the walk finished: the task
pointer `0x02EBF400` is 0, or the slot is 4 or more with a step above 0, or below 0 with a step of 0 or
less (`0x0037CB50`-`0x0037CB7B`). It then calls `0x00233AA0` (`0x0030D8B0(1)`, `0x00326500`,
`0x00311E10(0)`, `0x00311E20`) and clears the task pointer `0x02EBF400`.

`0x00233AA0` makes its four calls in that order, `0x0030D8B0(1)`, `0x00326500()`, `0x00311E10(0)` and `0x00311E20()`, and
answers 1 (`0x00233AA4`-`0x00233ABF`).

In the read-in record `0x0037C730` stores the state byte `0x02EBF3F8` as 0 (`0x0037C7DB`), the slot `0x02EBF3F9` (`0x0037C7E1`),
the pass `0x02EBF3FA` as 0 (`0x0037C7D4`) and the saved byte `0x02EBF3FB` from `0x002DEBD0` (`0x0037C7F1`). The world tick's
`0x0037C1A0` fills the tick record the same way: `0x02EBF3D8` (`0x0037C229`), `0x02EBF3D9` (`0x0037C22F`), `0x02EBF3DA`
(`0x0037C222`) and `0x02EBF3DB` (`0x0037C23F`).

`0x0037B4B0(actor)` writes 0 to the parts-requested byte `+0x23` of a non-null actor (`0x0037B4B5`). `0x0031A300`
(`0x0031A3B8`) and `0x00324380` (`0x003243B0`) walk the battle units (`0x00236820(i)`) and call it on each unit's bound actor
`+0x10`; `0x003261D0` (`0x00326490`) and `0x003273D0` (`0x003277A0`) also call it.

The read-in verbs' poll `0x0034E3E0`, shared with `summonreadsync` (`0x0204`) and
`summontopartyreadsync` (`0x0208`), waits while `0x0037CB50` reports a walk in progress (its third
caller is `0x00324360`); `partyallread`'s result `0x0034D460` is `0x003601C0(0x13)`, which clears busy
bit `0x80000`.

Every launcher calls `0x00233CF0` (`0x0030D8B0(0)`, `0x003266C0`, `0x00311E10(1)`), the counterpart of `0x00233AA0`, once the
allocator `0x002F16B0` has returned a task; with a null one it still stores the null pointer at `0x02EBF400` and its mode
byte `0x02EBF3FC`, then returns without filling the task or calling `0x00233CF0` (`0x0037C99A`, `0x0037CA1A`, `0x0037CA9A`). No
launcher tests `0x02EBF400` first: a read-in started while one runs replaces the task pointer, and both tasks share the
record `0x02EBF3F0`.

`0x0037C730` clears `0x02EBF400` in the same call that runs `0x00233AA0`: it sets the task state to 4 (`0x0037C83F`) and jumps
back to its state switch (`0x0037C845`), whose state-4 arm stores the null pointer (`0x0037C772`) and returns.

The world tick's mask is set by `partystdmotionrecover` (`0x014C`): its begin `0x00342C90` raises busy
bit `0x40000` (`0x003601B0(0x12)`) and sets `0x02EBF3E0` to `0xF` when it is 0 (`0x0037CFD0`); its poll `0x00342F50`
waits while the mask is non-zero (`0x0037CB80`). `0x0037CB10` (from `0x00266D10`) clears the mask and
`0x02EBF3DE`.

Placement needs record bit `0x80` and a slot of 0 or more. The task, the world tick and `0x0037CF50` fill
the record with bit `0x80` clear, so they rebuild without moving the actor. `0x0037CE80` sets bit `0x80` and
clears context `+0x11` bit `0x1`; `setupbattle` passes its slot, so its members are placed, while
the scene step passes slot −1, which skips placement.

`0x0037CE80(record, actor, slot)` and `0x0037CF50(record, actor, slot)` fill the record the way `0x0037C730` does:
the encoded actor at `+0`, pass `+0x0A` 0, the slot at `+9` (−1 for any negative slot), state byte `+8` 0,
`+0x0B` from `0x002DEBD0`, then `0x002DEB90(1)`, the empty stub `0x0016D6A0` and actor `+0x23` = 0 for a non-null
actor (`0x0037CEAC`-`0x0037CEE3`, `0x0037CF5F`-`0x0037CFA2`). `0x0037CE80` clears the context bit before the fill
(`0x0037CEA5`) and sets bit `0x80` after it (`0x0037CEE7`).

### Dispose and recover

The scene step is the last phase of the pair of verbs `disposeentry` (`0x006B`) and `recoverentry`
(`0x006C`), which take down and bring back the models of manager 0's battle-eligible actors. They
share the `i16` state word `0x022C8010`, which the world tick advances once per frame through
`0x00359800` (called at `0x00314282`):

| State | Set by | What the tick does |
|---|---|---|
| 0 | `0x0035A240`, and the scene step when its walk ends | nothing |
| 1 | the `disposeentry` begin `0x00344EA0` through `0x0035A640`, only from state 0 | `0x00359A30`, below, which ends in state 2 |
| 2 | `0x00359A30` | nothing |
| 3 | the `recoverentry` begin `0x00345A30` through `0x0035A660`, only from state 2 | zeroes `0x022C8024` and `0x022C8028`, enters state 4 and starts the `entryread` task (`0x0037C910(0)`), and in the same tick continues as state 4 |
| 4 | the tick | waits until the task pointer `0x02ADD968` is null (`0x0037CB40`), then enters state 5 and runs the scene step at once, in the same tick |
| 5 | the tick | the scene step `0x00359880` |

`0x00359A30`, the disposal:

1. sets battle flags `0x02089340` bit `0x20` (`0x00238B70(1)`, which also calls `0x002E7C10(actor, actor,
   0x30B, 0)` for every unit in use with flag bit `0x10`) and bit `0x80` (`0x00238AE0(1)`);
2. releases each record of manager 0's ordinal window (first `+0x1DE`, count `+0x1D6`, when bit `0x1` of `+0x10` is
   set
   before the walk) that holds a unit at `+0x30` (`0x0035A590`: `0x0026D6D0`, `0x00233F50(record, 1)`, `0x002ED020`);
3. clears the keep bit `0x10` of `+0x19` in all 128 binding entries (`0x002E63D0`) and zeroes dword
   `+0x40` of the 32 lane records (`0x002E6570`);
4. for every record of slot 0 with `+0x14` bit `0x80` and a tag of 4 or more (`0x002647B0` = 0), takes its
   readiness `0x002EA6A0` and releases its model with the per-`+0x04` teardown `0x0025AB30`; context
   `+0x11` bit `0x1` records that readiness, and is cleared for every other record.
5. The walk covers the `0x00263C30(0)` records of slot 0 (`0x00359A56`); a record with a unit at `+0x30` also
   gets `0x003589B0(record)`, whose answer is not used (`0x00359A96`-`0x00359AA3`), and the state word `0x022C8010`
   becomes 2 at the end (`0x00359B01`).

The scene step walks slot 0's records one per pass with the counter `0x022C8028`, rebuilding each
record whose `+0x14` bit `0x80` is set, whose tag is 4 or more and whose context `+0x11` bit `0x1` was set
at disposal, one machine run at a time (`0x022C8024` = 1 while one runs, 2 when the walk is done).

Within one tick the step passes over every record that does not qualify (a record without a context counts
as bit `0x1` clear), fills `0x022C8018` for the next one that does with `0x0037CE80(0x022C8018, record, −1)` and runs
the machine at once (`0x0035992B`-`0x003598CB`). A run that reaches state 23 sets `0x022C8024` back to 0 and the
walk goes on in the same tick (`0x003598E4`), and a run that waits ends the tick (`0x003598DE`).

Once `0x022C8028` reaches slot 0's record count `0x00263C30(0)` (`0x003598F4`), the step stores 2 in `0x022C8024`
and, in the same call, sets the state word `0x022C8010` to 0 (`0x003598F8`, `0x00359972`).

The begins store 1 for an accepted call and 0 (dispose) or -1 (recover) otherwise. The
`disposeentry` poll `0x003453D0` holds an accepted call until the state reads 2, 3 or 5
(`0x0035A0A0`); the `recoverentry` poll `0x00346020` holds an accepted call while it does. Both write
`0x022C253D` = 1 (`0x00314D40`) while they hold.

`0x0035A0A0` answers 0 for state 4 too (`0x0035A0B1`, `0x0035A0B4`), so the `recoverentry` poll also returns
while the tick waits in state 4 for the `entryread` task, before the scene step has run, as well as once
the walk is back at 0.
`0x0035A240` clears the state from the slot-0 bind's field reset `0x0026DB30`, from `0x002695A0` and
from `0x00266D10`.

## Layouts

```python
rebuild record  +0 u32 encoded actor, +4 u32 pending handle, +8 u8 state | 0x80 place, +9 s8 slot, +0xA u8 pass, +0xB u8 saved byte
read-in record  0x02EBF3F0 (+0x8 0x02EBF3F8 state, +0x9 0x02EBF3F9 slot, +0xA 0x02EBF3FA pass, +0xB 0x02EBF3FB saved byte, +0xC 0x02EBF3FC mode, +0xD 0x02EBF3FD step, +0xE 0x02EBF3FE slot, +0x10 0x02EBF400 task)
tick record     0x02EBF3D0 (+0x8 0x02EBF3D8 state, +0x9 0x02EBF3D9 slot, +0xA 0x02EBF3DA pass, +0xB 0x02EBF3DB saved byte,
                0x02EBF3DE run flag 0/1, 0x02EBF3E0 slot mask)
actor           +0x20 s8 pool entry, +0x23 u8 parts requested (bit 0x1 main, 0x2 part 0, 0x4 part 1, mask 0x18 part 8)
pool entry      0x022D9AB0 (2) / 0x022D9AE0 (4), 0x18 each: +0 state (3 loaded), +1, +2 index bytes, +0xC, +0x10 loads, +0x14 id, +0x16 count
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

The two static records `0x02EBF3D0` and `0x02EBF3F0`, the task pointer `0x02EBF400`, the tick slot mask,
the actor's `+0x20` and `+0x23` bytes, and the pool entries.

## Modding notes

- An actor that stays invisible after a read-in verb is stuck in a wait state (2, 5, 8, 11, 14, 17
  or 20); byte `+8` of `0x02EBF3F0` names it. States 17 and 20 cannot recover once their target is
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat: `0x00263E30` is called by `0x003206E0`; those functions are documented on [battle units](battle-units.md).
