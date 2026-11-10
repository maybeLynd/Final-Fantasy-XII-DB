---
title: "Reward verbs: every script verb that adds or removes items, gil, equipment or party members, and exactly what it writes"
kind: "system"
category: "Scripts and script commands"
addresses: "0x00345080, 0x003449A0, 0x0034A6D0, 0x0034ABF0, 0x0034B1E0, 0x003459C0, 0x00345520, 0x00344630, 0x0032A810, 0x0032A830, 0x0032A860, 0x00300B80, 0x00300BA0, 0x003008A0, 0x00346930, 0x00346E30, 0x0032A7F0, 0x003004B0, 0x00254EE0, 0x0050DEE0, 0x0032A800, 0x00354400, 0x00355830, 0x00356570, 0x00356A10, 0x0050FAF0, 0x002FAFD0, 0x002FB430, 0x02EC3E60, 0x0208CD18, 0x0034C370, 0x0034CDF0, 0x003172E0, 0x00328B20, 0x00316DF0, 0x00323540, 0x00349F90, 0x0034A790, 0x0030FBE0, 0x0030FAA0, 0x0034A300, 0x003497B0, 0x0030FD10, 0x00342230, 0x00328BD0, 0x00344C60, 0x00290130, 0x0050F200, 0x00510720, 0x003403E0, 0x0050F910, 0x02EBF190, 0x02EBF130, 0x00316A50, 0x00309F30, 0x0035DF20, 0x003272A0, 0x002FA260, 0x002FA470, 0x002F7FA0, 0x002341C0, 0x00236740, 0x00317480, 0x0030C470, 0x0035A620, 0x0035A630, 0x00320AB0, 0x00324380, 0x0035A250, 0x0030BAD0, 0x00559760, 0x003138D0, 0x00327CB0, 0x002398F0, 0x0030DD70, 0x0030DCB0, 0x0030DD10, 0x003F8C60, 0x003F4AA0, 0x002FA520"
---

## What the player sees

Talking to someone hands over an item with a "Received" message; a chest gives an item or gil; a
quest takes an item away; a story scene adds a character to the party or a guest joins; a prison
stretch strips everyone of their gear and gives it back later. Each of those is a script verb.
Every item and gil change among them ends in the same two places: the one routine that changes the
inventory, or the one that stores the gil total; a character joining or leaving changes the party
slots instead (see Party membership).

## How it works

### Items

| Verb | Id | Handler | What it writes |
|---|---|---|---|
| `additem(item, count)` | `0x02E5` | `0x00345080` | pushes 1 as the message flag (`0x00267F90`, which skips the push when the stack already holds 63 or more values, so the pops then take the count as the flag, the item as the count and the value below them as the item), pops flag, count and item, queues the "received" message (`0x002A3060(item, count, 1)`) when the popped flag is non-zero (`0x003450C5`) and grants through `0x0032A810`; returns the new count (`0x0026B4E0`) |
| `additem_47f(item, count, msg)` | `0x047F` | `0x003449A0` | the same with an explicit message flag |
| `additemmes(item, count)` | `0x0480` | begin `0x0034A6D0`, poll `0x0034ABF0`, result `0x0034B1E0` | the begin queues the message without a grant flag (`0x002A3060(item, count, 0)`) and stores the pair; the poll runs while the message queue is busy (`0x002A2BF0` → `0x0035DF20(0)`, busy while `0x022CA430` is non-zero); the result pushes the item and the count the begin stored at `+0` and `+4` of its state, then 0 (`0x0034B1F4`-`0x0034B218`, each push skipped when the stack holds 63 or more values), pops them back as flag, count and item, skips the message because the flag is 0 (`0x0034B23B`), grants through `0x0032A810` and returns the new count (`0x0026B4E0`) |
| `subitem(item, n)` | `0x02F2` | `0x003459C0` | `0x0032A810(item, −n)`, n negated at `0x003459E2`; returns its result (`0x0026B4E0`) |
| `setitemnum(item, n)` | `0x055C` | `0x00345520` | `0x0032A830(item, n)`: sets the count; returns its result (`0x0026B4E0`) |
| `haveitem(item)` | `0x02E4` | `0x00344630` | `0x0032A860`: the count through `0x00309FB0`, floored at 0 |

`0x0032A810` is `0x00300B80(item, delta, 0)` with the result floored at 0, and `0x0032A830` the same
through `0x00300BA0`; both end in `0x003008A0(item, n, set, 1, mode)`, the one inventory mutator.

`0x003008A0` returns −1 for ids `0xFFFF` and `0x1000`, classes above `0xE` and an index at or past the
class's count at `0x01EEBCFC + class × 0x58`. Otherwise it reads the old count (`0x00309F30`) and calls
the class's handler from `0x01EEBD08 + class × 0x58`; when that slot is null it returns the old count
and writes nothing.

When its fourth argument is 1, the old count is below 1 and the new count is above 0, it sets
discovery bits in `[0x02EBF190] + 4`:

- class 3: bit `0x1`, plus `0x01EECF98[s]`, where s is word `+0x2C & 7` (below 5) of the `0x02EBF138` row
  that byte `+2` of the `0x02EBF0F0` row `id − 0x3000` names;
- class 4: bit `0x40`;
- Quickenings `0xC000` to `0xC011`: bit `0x80`; Espers `0xC012` to `0xC01E`: bit `0x100` (`0x0030099A`-`0x003009D4`).

Grants made with another mode set no bits: `0x00300490` (mode 4) and `0x0030C410` (mode 2).

### Gil

`addgill(n)` (`0x02E7`, `0x00346930`) and `subgill(n)` (`0x02E8`, `0x00346E30`) call
`0x0032A7F0(±n)` → `0x003004B0(n, 0)`. `0x003004B0` computes `max(0, gil + n)` and hands it to
`0x00254EE0`, which records the change in statistics counter 6 (gain) or 7 (loss) through
`0x00316A50` and stores `min(total, 99,999,999)`; the gil window notify `0x00469E80` is skipped because
the flag is 0. The verb returns the uncapped value, so it can report more than is stored.

The debug verb `debug_setgill` (`0x20A3`, `0x0050DEE0` → `0x0032A800` → `0x00300500`) sets gil outright.
The `gillwinopen`, `gillwinclose`, `gillwinstart` and `gillwinsync` verbs (`0x0487` to `0x048A`)
drive the gil window and write nothing.

### Treasure chests

All 1,966 chest talk functions in the US scripts run the same calls in this order:

```
sethpmenu(0); ucoff(); settrapshowstatus(0); btlAtelOpenTreasureStart(); talktreasure(id); sethpmenu_436(0, 5);
btlAtelOpenTreasureMessage(id); sethpmenu_436(1, 5); talktreasureafter(id); btlAtelOpenTreasureFinish(); ucon();
sethpmenu(1); clear_force_char_nearfade(); setmaphighmodeldepth(-1); setmapmodelstatus(1);
setstatuserrordispdenystatus(0); settrapshowstatus(1);
```

`setuptreasure` (`0x02BE`, begin `0x00354400`) places the chest actor and rolls its presence through
`0x002FAED0`: no chest when the opened flag `0x0032AA60(record[9])` is set, otherwise a chest when
`rand % 100` is below byte `+0xA` ([script name bindings](script-name-bindings.md)).

`talktreasure(ref)` (`0x02BF`, begin `0x00355830`) stores the controlled character's actor (`0x003588B0(0x003590D0())`) in
its state (`0x0035586B`) and resolves the chest record through the reference (`0x002650B0`). It has the controlled
character open the chest: `0x00269090` hands `0x00328640` (step 1 below) the record
`{1, opener, chest actor, chest record}`, and `0x00328640` does nothing when the opener is null or has no unit or the
latch is not 0.

It stops the opener's movement (`0x0026D6D0`) only when the opener is non-null (`0x00355892`) and disarms the issuer's
slot 2 (`0x0025D5E0(actor, 2)`, which clears bit `0x4` of the actor's `+0x1C`); its poll `0x00355E20` waits on the
interaction latch `0x0208CD18`.

`talktreasureafter` (`0x0414`, begin `0x00356570`, poll `0x00356A10`) waits on `0x00319180`, the latch's getter, for the
controlled character: the begin pops the reference without using it and stores the controlled character's actor
(`0x003588B0(0x003590D0())`, `0x0035659E`) in its state, which the poll reads.

The latch runs the opening in three steps:

1. `0x00328640(record)`, while the latch is 0 and the record's first actor has a unit, copies the 32-byte record to
   `0x0208CCF8` (opener actor at `0x0208CD00`, chest actor at `0x0208CD08`), stores the chest's id at the opener unit's
   `+0x710`, plays motion `0x201C` on the opener (`0x002EB030`) and sets the latch to 1 (`0x003286BB`).
2. The opener's command step `0x00325260`, case 0, calls `0x00317850` while the latch is 1 and `0x0208CD00` is its own actor
   (`0x00325311`). `0x00317850` plays motion `0x2008` on the chest, starts the chest's effect (`0x002EACD0`, handle kept at
   `0x0208CD1C`) and clears the latch (`0x003178A3`).
3. `0x0032A170`, once the latch is 0, hides the chest actor: it calls `0x0026DC60`, a jump to `0x002EBB80`, with the chest
   actor and 0 (`0x0032A18B`), which clears bit `0x8` of byte `+0x10` of the actor's record at `+0xC0` and refreshes
   the draw test (`0x002EBB96`-`0x002EBBA3`). It then plays `0x2001` on the opener, releases the
   effect (`0x003B0770`) when the handle is valid, clears bit `0x40` of `0x02089340` and sets the handle to -1.

`btlAtelOpenTreasureMessage(ref)` (`0x3037`, begin `0x0050FAF0`) is the payout. It takes a message record (`0x0035E550`,
the record at `0x022CA438`), resolves the chest record through the reference, clears the message record (`0x0035E560`),
stores the dword `0x10000` at its `+0` (`0x0050FB3A`) and runs `0x002FAFD0`:

1. The opened flag is set (`0x0032AD70(record[9], 1)`) when byte `+9` is not `0xFF`, and the
   per-field presence ledger is marked (`0x002FB430(0x02EC3E60, field, record[0], 0)`).
2. `rand % 100` at or above byte `+0xB` gives an item, below it gil.
3. The alternate contents apply when the unit `0x003272A0` returns has `+0x6B` or `+0x7B` bit `0x2` set
   and none of the statuses `0x80000003`.
4. Item: a second `rand % 100` picks word `+0x10` (below 95) or `+0x12` with the alternate flag,
   otherwise `+0xC` (below 50) or `+0xE`. `0xFFFF` gives nothing; any other id gives one.
5. Gil: word `+0x16` with the alternate flag, otherwise `+0x14`. A word of 0 gives nothing. With
   record flag `+8` bit `0x40` the amount is `rand % word + 1`.

The verb then acts on the kind `0x002FAFD0` stored. For an item (kind 0) it adds an item entry to the message
(`0x0035E500(record, 0, item, 1)`, `0x0050FB8E`) and grants the item through `0x00300B80(item, 1, 0)` (`0x0050FBA0`); for gil
(kind 1) it adds a gil entry (`0x0035E500(record, 1, gil, 0)`, `0x0050FB6A`) and grants the gil through `0x003004B0(gil, 0)`
(`0x0050FB76`). When the roll gave nothing (kind 2: an item word `0xFFFF` or a gil word of 0) it adds no entry and
grants nothing (`0x0050FB5A`). On every path it then shows the message (`0x0035DF40`, `0x0050FBA8`).

The presence ledger at `0x02EC3E60` is a ring of three `{field, value bits, mask bits}` entries with
its cursor at `0x02EC3E84` and count at `0x02EC3E88`. Its other users are the clear `0x002FA260` (called
from `0x00233C10` and `0x00237DF0`), `0x002FA470` (called from `0x002341C0`, which adds an entry for field
`0x022BE940` with mask `0xFF` and value 0) and the reorder `0x002F7FA0`.

`0x002FB430(ring, field, bit, value)` looks for the field among the first count entries. When it finds it, it
sets mask bit `1 << bit` and replaces that value bit with `value` (`0x002FB4D0`-`0x002FB4F6`). When it does not, it
takes the entry at the cursor: it stores the field, sets the mask to `1 << bit` alone and ORs `value << bit` into
the value bits, so the replaced entry's other value bits stay (`0x002FB460`-`0x002FB499`).

It then moves the cursor on modulo 3 and raises the count, capped at 3: the cursor `+0x24 = (+0x24 + 1) % 3` and
the count `+0x28 = min(+0x28 + 1, 3)` (`0x002FB49C`-`0x002FB4C2`).

`0x002FA470` adds its entry only when no entry below the count holds field `0x022BE940` (`0x002FA490`-`0x002FA493`); it
then stores mask `0xFF`, value 0 and the field at the cursor and moves the cursor and count the same way
(`0x002FA4AA`-`0x002FA50E`). Both paths end in a jump to `0x002F7FA0(ring, 0x022BE940)` (`0x002FA51A`).

`0x002F7FA0(ring, field)` takes the entries below the count in index order. For each whose field matches, it
swaps that entry with the entry one place after it and then two places after it, modulo 3, `j = (i + k) % 3` for
`k = 1, 2`, stopping at an index that is the cursor or at or past the count, `j == +0x24` or `j >= +0x28`
(`0x002F7FC0`-`0x002F8036`). An entry moved to a later index is tested
again when the walk reaches it.

None of them, nor `0x002FAED0`, reads the value or mask bits to decide presence: the ring's address is formed only in these three
functions, `0x002FAED0` and `0x002FAFD0`, and is handed only to `0x002FB430` and `0x002F7FA0`, which keep no
copy of it, and the image holds no absolute or image-relative copy of it. So `setuptreasure` rolls
a chest's presence every time it runs.

`0x022BE940` is the field `0x002FA520` stores from `0x003148F0()` when an area is initialised
(`0x0023446C`), so the teardown's entry names the field being left.

### Party membership

`addpartymember(sel)` (`0x0353`) grants through `0x003172E0`: a main character not already in the
nine slots at `[0x02EBF190] + 0x5A48` is written into a free index 4 to 8 of a staged copy and
activated with `0x00316DF0(record, 0)`, the copy is committed with `0x003261D0(0)` (`0x003173D9`) and it returns 0.
It returns −1 without activating or committing for a selector above 6, a character already seated, no free
index from `0x00321100`, or a staged index that is not `0xFFFF` (`0x003172F2`, `0x00317373`, `0x003173EB`).

`removepartymember(sel)` (`0x0354`) clears the slot through
`0x00328B20`, which writes `0xFFFF` to the character's index in the staged copy (`0x00328B92`), deactivates with
`0x00323540` and commits with `0x003261D0(0)` (`0x00328BB7`), returning 0; a selector above 6 or one not seated
returns −1 (`0x00328B2C`, `0x00328B59`). The guest verbs (`addguestbattlemember`,
`removeguestbattlemember`) and the treasure flag verbs are on [party verbs](party-verbs.md) and
[script name bindings](script-name-bindings.md).

Activation `0x00316DF0(record, arg)` acts only on a record whose flags bit `0x10` is clear. Unless arg bit
`0x2` is set outside New Game+ (`0x00236740()` = 0), it first calls `0x00317480(record)` and, in New Game+
with flags bit `0x8` clear, grows the record to level 90 with `0x0030C470(record, 0x5A, 0)` (`0x00316E2E`-`0x00316E3D`;
[New Game+ and New Game-](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md)). For a party-side record (`+5` = 0)
with selector below `0x1A`:

- a main character (selector below 7) gets each of the five equipment words at `+0x50` as one owned
  item (`0x00300B80`) and one equipped count (`0x0030C410`, which counts class-1 ids other than
  `0x1000`);
- on the first activation (flags bit `0x8` clear), each entry of the `+0x88` list selected by the mask
  word at `+0xB8` grants its low half as an item; for a main character the id at `+0x22` of the
  action row its high half names is granted too (`0x00300490` below `0x1000`, `0x00300B80` otherwise);
- also on the first activation, the ten starting pairs of the character's row in `0x02EBF130`
  (`+0x58` ids, `+0x34` counts) and the starting gil `+0x3E` (`0x003004B0`).

Every activation then sets flags bits `0x8` and `0x10` and writes `+0x48`: `max(+0x48, 1)` when status bit
`0x10000` is set (`+0x64 | +0x3C`), otherwise `+0x24`, doubled when status bit `0x10000000` is set. Deactivation
`0x00323540` acts only on a non-null record of a main character (`+5` = 0, selector up to 6) whose flags bit `0x10`
is set, and otherwise returns at once (`0x00323540`-`0x0032355C`); it removes each equipped item once (`0x0030F9A0`,
`0x00300B80(item, −1)`) and clears bit `0x10`.

### Taking and giving back everything

`takeaway_item_and_equip` (`0x0388`, begin `0x00349F90` → `0x0035A620` → `0x0030FBE0`) walks the nine
roster indices (`0x00320AB0(i, 3)`), keeping records with `+5` ≠ 0 or a selector outside 7 to `0x19`:
each copies its five equipment words to `+0x5A` and clears the slots (`0x0031A300`). After
`0x00324380` it copies the class-0 counts at `[0x02EBF190] + 0x4748` to `+0x4F84` and the class-1
counts at `+0x47C8` to `+0x5004`, zeroing each through `0x003008A0(id, 0, set)`, bounded by
`0x01EEBCD0` and `0x01EEBD28`.

The takeaway skips indices with no record (`0x0030FC02`). Its call for id `0x1000`, which `0x003008A0` refuses
(`0x003008DD`), copies that count but leaves it in place (`0x0030FCE2`). It returns 1.

`giveback_item_and_equip` (`0x0387`, `0x0034A790` → `0x0035A630` → `0x0030FAA0`) adds the saved counts
back (bounded by `0x01EEBCFC` and `0x01EEBD54`; the add for `0x1000` is refused, `0x0030FB48`), re-equips from `+0x5A`
(`0x0031A710`) the records of the nine indices that pass the takeaway's test (`0x0030FB70`-`0x0030FBA0`), calls `0x00324380`
and clears the `0x83C`-byte backup, returning 1 (`0x0030FBAC`-`0x0030FBCC`). Both poll `0x0034A300`, which runs while
`0x0030BAD0()` is non-zero (`0x0035A250`) and then calls `0x00314D40(1)`.

`takeoff_equip(item)` (`0x055B`, `0x003497B0` → `0x0030FD10`) unequips one item id from every alive
main-character record (`0x0031A630(record, slot, 0xFFFF, 1)`). It collects the records of seats 0-8 of map 0
(`0x00320AB0(i, 0)`) with `+5` = 0 and a selector up to 6 into `0x022C1740`; a record with any of the statuses
`0x80000003` (`+0x64 | +0x3C`) is taken only when `0x00377C20()`, bit `0x8000` of the area's flag word, is
non-zero (`0x0030FD40`-`0x0030FD86`). It then clears every slot of those records that holds the id
(`0x0030FDB0`-`0x0030FDC8`), calls `0x00324380` once and returns 1 (`0x0030FDE2`-`0x0030FDEC`).

`resetJobs(sel)` (`0x05D6`, `0x00342230` → `0x00328BD0`) refuses a selector above 5 (returns −1). It clears the
character's equipment (`0x0031A260`), runs `0x00328990` on each board the job bytes `+0x1C3` and `+0x1C4` name, which
takes back that board's licenses and refunds their LP (`0x00328C16`-`0x00328C35`;
[licenses](../Items-Equipment-Shops-And-Licenses/licenses.md#resetting-the-boards)), calls `0x00559760`, and, when
the selector is the character recorded at `[0x02EBF190] + 0x5AD5`, issues command `0x113` to party slot 3
(`0x003138D0(1)`, [battle verbs](battle-verbs.md)) and calls `0x00313550(0)`.

Only after rebuilding the stats and gambits does `resetJobs` clear the job bytes: one word store puts
`0xFF` in both `+0x1C3` and `+0x1C4` (`0x00328D52`), and
`+0x1C5` is set to `0xFF` after it (`0x00328D5D`).

`0x00559760(sel)` (`0x00328C3C`) looks for the selector in the word `+0x60` of the nine record pointers at
`[0x0209AC30] + 0xAC8` (`0x00282E10`, which skips null pointers and reads `[0x0209AC30]` without a null test, so a null
`[0x0209AC30]` faults at `0x00282E24`).

With no match `0x00559760` returns and writes nothing (`0x00559771`). With a match it zeroes the class-8 entries
`sel + 0x4D` and `3 × sel + 0x53` to `3 × sel + 0x55` of the typed store at `[0x020927C0] + 0x90`
(`0x002527B0(8, index, 0)`, `0x00559786`, `0x005597A3`), the last three being the member's Quickening order the
[license board](../Menus-And-HUD/license-board-screen.md) shows.

It then rebuilds the ability list (`0x0030FED0(record, 0x97)`) and calls `0x00327CB0` with the `+0x14` word of the
character's `0x02EBF130` row. The row address is the table's word `+8` times the selector plus the value `0x0020E600`
returns for the table's `+0xC` (`0x00328C8E`-`0x00328C9E`), added in 32 bits (`0x00328CA1` `add esi, eax`), so the upper
half of that pointer is dropped.

Nothing guards the read: when `[0x02EBF130]` is null (`0x00328C75`) or `0x0020E600` returns 0 (`0x00328C82`), the base stays 0
(`0x00328BE7`) and `0x00328CA3` reads the word at address `0x14`, which faults, because the first 64 KB of a Windows x64
process are never mapped.

For selectors 0 and 5 it adds one to byte `+0xBA` (capped at 12), `+0xBA = min(+0xBA + 1, 12)`, when the record's
kind byte `+5` is 0 (`0x00328CDC`-`0x00328CF5`). It calls `0x00326030` and `0x00327DE0`, clears `+0x68..+0x87`, `+0x37`,
`+0x4E` and `+0x20`, calls `0x00283270(1)`, sets `+0x1C3`/`+0x1C4` to `0xFFFF` and `+0x1C5` to `0xFF`, and returns 0
(`0x00328D5B`). One US script uses it.

### The quest result window

`questresultwindow(n)` (`0x037C`, begin `0x00344C60`) turns n into an id with `0x00473C90`, falling back to the id of row
0.
`0x00473C90(n)` returns −1 when n is at or past the count at `[0x02CA6C60] + 4`; a negative n is not refused, because that
test is signed (`0x00473C9A`), and returns `((dword >> 13) & 0x1FFF) + 0xA000` of the dword at `[0x02CA6C60] + 8 + 4n`,
and a null `[0x02CA6C60]` faults at `0x00473C97`. On a negative result the verb calls `0x00473C90(0)` (`0x00344C8B`) and
passes its result on untested.

It takes action availability row 3 (`0x002E1CD0(0, 3)`, which sets the mask `0x139203` in dword 3 of the capability
table `0x0215F1C0`, `0x002E1CFA`), opens the window through `0x00290130(n, id)` (the jump `0x002E1A50`, called at `0x00344C9A`)
and raises busy bit `0x2000` (`0x003601B0(0xD)`).

`0x00290130` grants at once, when the window opens: it builds the reward bundle (`0x003F8C60`, `0x0029014D`) and, when that
returns non-zero (`0x00290152`-`0x00290154`), grants it (`0x003F4AA0`, `0x0029015B`) and posts it with
`0x003F4BD0([bundle + 0x24], bundle)` (`0x00290169`); a zero return grants and posts nothing.

`0x003F4AA0` adds gil straight through `0x00254EE0` (`gil + [bundle + 4]`) when flag bit `0x1` is set, and `(item, count)`
pairs and single ids through `0x00300B80`: the word `+8` counts the word pairs at `+0xC` and the word `+0xA` the single
ids at `+0x1C`, each single granted once (`0x00300B80(id, 1, 0)`, `0x003F4B1A`).

### Verbs that look like rewards and write nothing

`fs_setclanrank` (`0x7031`) and `btlAtelSetPcLevel` (`0x307F`) share `0x0050F200`, which pops two
values and jumps to the `ret` stub `0x0016D6A0`; `btlAtelAddMaxLicensePoint` (`0x3078`) and the
others on `0x00510720` pop one. `addclanpoint(n)` (`0x04DC`, `0x003403E0` → `0x002E2380`) adds to
statistics counter 17 (`0x00316A50(0x11, n)`) and no script uses it.

`btlAtelSetLevel(a, b)` (`0x3031`, `0x0050F910` → `0x002398F0`) pops b, then a, and jumps to `0x002398F0(actor, b, a)` with
the issuing actor (`0x0050F94E`). That sets a foe's level to a random value from a to a + b
(`0x0030C470(record, a + rand % (b + 1), a)`, the record at unit `+0x698`) and returns 0 (`0x00239939`). It is refused,
returning −1 (`0x00239950`), when the verb's actor has no unit (`0x0031B760`, `0x0023990F`) or when
`[[unit + 0x6A0]] & 5` is non-zero (`0x0023991B`).

The spawn record pointer at unit `+0x6A0` is read with no null test (`0x00239911`-`0x00239918`), so a unit whose
`+0x6A0` is null faults there. The remainder is a signed `idiv` by `b + 1` (`0x00239926`), so b = −1 divides by zero
and faults with a divide error.

Its draw comes from the LCG `0x00328370`, while the chest rolls above draw from the
Mersenne Twister thunk `0x00379CD0`
([which roll uses which generator](../Random-Numbers/which-roll-uses-which-generator.md)).

The debug give-all verbs add 99 of every id (`0x003008A0(id, 99, 0, 1, 0)`): items
(`0x00510850` → `0x0030DD70`, class 0), equipment (`0x00510860` → `0x0030DCB0`, class 1) and event items
(`0x0050F0E0` → `0x0030DD10`, class 2). Each walks the ids from the class base while the index is below the class
count at `0x01EEBCFC`, `0x01EEBD54` or `0x01EEBDAC`. The equipment walk starts at `0x1000`, which `0x003008A0` refuses
(`0x0030DCBC`, `0x003008DD`), so that one id gets nothing.

## Layouts

```python
inventory call   0x003008A0(item id, n, set, mode, arg): class = id >> 12, index = id & 0xFFF, class count at 0x01EEBCFC + class × 0x58
discovery bits   [0x02EBF190] + 4: bit 0x1 and 0x01EECF98[school] for magicks, bit 0x40 technicks, bit 0x80 Quickenings 0xC000..0xC011, bit 0x100 Espers 0xC012..0xC01E
gil              0x003004B0(n, notify) = max(0, gil + n); 0x00254EE0 stores min(total, 99,999,999) and logs counter 6 or 7
chest record     +0 index in the field, +8 flags (bit 0x40 random gil), +9 opened-flag id, +0xA presence %, +0xB item %
chest contents   +0xC/+0xE item words, +0x10/+0x12 alternate item words, +0x14 gil, +0x16 alternate gil
presence ledger  0x02EC3E60: 3 × {u32 field, u32 value bits, u32 mask bits}, cursor 0x02EC3E84, count 0x02EC3E88
party record     [0x02EBF190] + 8 + selector × 0x1C8: +0 flags (bit 0x8 first activation, bit 0x10 active), +0x50 u16[5] equipment,
                 +0x5A u16[5] saved equipment, +0x88 u32[] grants with mask +0xB8 and count +0xBA
backup counts    [0x02EBF190] + 0x4F84 (class 0) and + 0x5004 (class 1), 0x83C bytes
```

## Shipped data

| Fact | Value |
|---|---|
| item verb uses in the US scripts | `additemmes` 4,364; `additem_47f` 2,136; `additem` 1,067; `subitem` 400; `haveitem` 4,044 |
| gil verbs | `addgill` 23, `subgill` 64 |
| chest sequence | 1,966 chests in 385 files, each calling the five chest verbs once |
| `questresultwindow` | 56 uses |
| inventory classes the mutator accepts | 0 to `0xE`, ids `0xFFFF` and `0x1000` refused |

## Operations

Per item verb: one message queue entry and one mutator call. Per chest: one roll and one grant.
Per party join: up to five equipment grants, the first-activation list, ten starting pairs and the
starting gil.

## State

The inventory counts and discovery bits in the party block, the gil total, each chest's opened
flag, the interaction latch `0x0208CD18`, the presence ledger, and the equipment backup words.

## Modding notes

- Every scripted item grant passes through `0x003008A0`; a hook there sees chests, talks, quests and
  party joins alike. The discovery bits are set on the first copy only for mode-1 grants, so the
  action ids a party join grants through `0x00300490` set no discovery bit.
- A chest's contents are decided when it is opened, by the roll in `0x002FAFD0`; its presence is
  decided by the roll in `0x002FAED0` each time `setuptreasure` runs, and the chest code does not read
  back the ledger that roll writes.
- Joining the party grants the character's equipment and starting items; leaving takes only the
  equipment back.
- `additemmes` grants after the message closes, `additem` before it shows.
- `questresultwindow` pays out when the window opens, not when the player closes it.

## Related

- [Party verbs](party-verbs.md): the slot maps the membership verbs write.
- [Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md): the inventory mutator in full.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the gil setter and its clamp.
- [Script verb table](verb-table.md): the ids and handlers.
- See also [treasure chests](../World-Areas-And-Travel/treasure-chests.md): every shipped chest, where it stands and what it holds with the odds of each content.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input: `0x003590D0` is called by `0x00226BE0`; `0x00377C20` is called by `0x00253C70`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Input gameplay: `0x00377C20` is called by `0x00313A00`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
