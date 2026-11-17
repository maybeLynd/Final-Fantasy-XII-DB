---
title: "Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings"
kind: "system"
category: "Party"
addresses: "0x003172E0, 0x003170E0, 0x00328B20, 0x003288F0, 0x00316DF0, 0x00317480, 0x00323540, 0x003261D0, 0x00328DB0, 0x00269C70, 0x00322350"
---

## What the player sees

- Characters join and leave as the story goes on, and guests travel with the party for a while.
- A main character who joins adds the gear they are wearing to the inventory, where it counts as owned and worn.
  A guest's gear is never added.
- On their first join, a main character or a guest also brings the items and gil their party row lists.
- A character who joins may catch up, as its party row says: on the first join only for Ashe, Fran,
  Balthier, Basch and the guests of rows 7-14 and 16, on every join for Penelo, never for Vaan, Reks and the
  guest Basch of row 15. Catching up sets
  level and LP from the two strongest members already in the party.
- A character who joins arrives with full HP, unless they have Disease.
- A main character who leaves keeps the gear they are wearing, and it leaves the inventory until they join again.
  A guest who leaves changes nothing in the inventory.
- Some scenes decide who fights, for example leaving Vaan to fight alone.

Joins and leaves are script verbs in the zone scripts. Each change rewrites the party's seats and starts loading the
fighters' models, and the script waits until that loading is done; what a joiner brings comes from their row of the
party table in `battle_pack.bin`.

## How it works

### Members and guests

A party member is named by its selector, which is its row of the party table and of the forty member records
([Party slots](party-slots.md)). Selectors 0-6 are the main characters and 7-25 the guests; `0x00322350` is the
guest test, `sel - 7 <= 0x12` as a byte. Row 26 is the chocobo and rows 27-39 the Espers, which no membership
function accepts. The names are under Shipped data.

### Adding a main character

`0x003172E0(sel)` adds a main character (`0x003172E0`-`0x003173E9`):

1. It refuses a selector above 6, and one already in any of map 0's nine seats (`0x00317310`-`0x00317329`), so nobody
   is in the party twice.
2. `0x00321100` finds a free reserve seat, the first of seats 4-8 of map 3 whose id check fails or whose byte is
   `0xFF` (`0x0032110A`-`0x00321148`); there is no free seat when all five are taken, and the add fails.
3. Map 0 is copied to the staging map `0x022C2580`, and the selector is written to that seat if it is empty there
   (`0x00317343`-`0x00317396`). When the staged seat is not `0xFFFF`, the add returns −1 without activating or
   committing (`0x00317373`, `0x003173EB`); the refusals in steps 1 and 2 return −1 too (`0x003172F2`).
4. The member's record is activated with `0x00316DF0` and the change is committed with `0x003261D0(0)`
   (`0x003173BE`-`0x003173D9`); the add then returns 0 (`0x003173DE`).

### Adding a guest

`0x003170E0(sel)` adds a guest (`0x003170E0`-`0x003171AE`). It refuses a selector outside 7-25 and one already seated,
like the main add. It then tries active seats 3, 2 and 1 of map 3, in that order, and takes the first whose id
check fails or whose byte is `0xFF` (`0x0031711A`-`0x00317157`). Seat 0 is never tried, but the commit closes up the
active seats, so a guest given seat 3 while seat 2 is empty ends up in seat 2.

The seated test looks for the selector in map 0's nine seats (`0x00317100`-`0x00317113`). `0x003170E0` returns -1 for a
refusal and when seats 3, 2 and 1 all fail (`0x00317159`-`0x0031715E`, `0x00317170`); otherwise it tail-jumps to
`0x00326110` (`0x003171AE`) and returns what that returns.

`0x00326110(sel, seat, 0, 1)` then copies map 0 to the staging map (`0x00326129`-`0x00326140`). When the seat's word there
is not `0xFFFF` (empty), or the selector is `0xFF`, it returns -1 without writing, activating or committing
(`0x0032615A`-`0x0032616A`, `0x003261BE`); otherwise it writes the selector to the seat, activates the record with
`0x00316DF0`, commits with `0x003261D0(0)` and returns 0 (`0x00326185`-`0x003261B6`).

### Removing a member or a guest

`0x00328B20(sel)` removes a main character and `0x003288F0(sel)` a guest (`0x00328B20`-`0x00328BC2`,
`0x003288F0`-`0x0032898E`). Each refuses a selector outside its range or not seated in map 0. It copies map 0 to the
staging map, empties the member's seat with `0xFFFF`, deactivates the record with `0x00323540` and commits with
`0x003261D0(0)`. The staging map is `0x022C2580`. Each returns -1
for a refusal (`0x00328925`, `0x00328B2C`, `0x00328B59`) and 0 after the commit (`0x00328988`, `0x00328BBC`); the guest
range is 7-25 (`0x003288F4`-`0x003288F9`) and the main range 0-6 (`0x00328B27`).

### What a join brings

`0x00316DF0(record)` activates a member record that is not yet active, record flag bit `0x10` (`0x00316DFE`):

1. It runs the catch-up below (`0x00316E1D`), unless its second argument has bit `0x2` set and flag bit `0x2000` of the
   party block, read by `0x00236740()`, is clear; it then skips steps 1 and 2 (`0x00316E0F`-`0x00316E1B`). The adds give 0;
   the seat writer `0x00329080(seat, selector, 3)` of the scenario presets gives 3 (`0x00329167`-`0x0032916A`), so a member
   seated there gets no catch-up and no level 90 only while that bit is clear.
2. When flag bit `0x2000` of the party block is set and the record has never been active, flag bit `0x8`, the level is set
   to 90 with `0x0030C470(record, 90, 0)` (`0x00316E25`-`0x00316E3D`).
3. For a main character, each of the five equipment words is added to the inventory, and to the count of equipped
   pieces (`0x00316E87`-`0x00316EB1`).
4. On the record's first activation, flag bit `0x8` clear, each enabled gambit slot's condition is added, and for a main
   character also the id the slot's action row names at `+0x22`, the magick or technick it uses (`0x00316EC3`-`0x00316F92`).
   An item id there goes to the unused channel 4 and adds nothing ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md)).
5. On that first activation the up to ten ids the party row lists at `+0x58` are added, with counts at
   `+0x34` (`0x00316FE1`-`0x00317019`), and the gil at row `+0x3E` (`0x0031701B`-`0x00317034`).
6. HP is set to max HP, or twice max HP under Bubble; under Disease it stays, but at least 1
   (`0x00317048`-`0x00317082`). Flag bits `0x8` and `0x10` are then set.

Steps 3-5 run only for a party record, kind byte `+5` 0, whose selector `+4` is 0-25; any other record goes from
step 2 straight to step 6 (`0x00316E42`-`0x00316E6A`).

`0x00323540(record)` deactivates an active main character (`0x00323540`-`0x003235BA`): each of the five equipment words
leaves the equipped count and the inventory, and flag bit `0x10` is cleared. A guest's equipment is never counted, and
the first-join items and gil are not taken back.

### Catching up on a join

`0x00317480(record)` sets a joining member's level and LP from the party (`0x00317480`-`0x00317667`). The party row's
byte `+0x2C`, bits `0x18`, says when: 1 on the first activation only, 2 on every activation, anything else never
(`0x003174D9`-`0x0031750D`).

1. It takes the two other active main characters with the highest levels, record `+0x1C2`
   (`0x00317540`-`0x003175B4`).
2. The level becomes their average level, at least 1, plus the row's byte `+0x2E`, through `0x0030C470`
   (`0x00317600`-`0x0031762C`).
3. The LP at `+0x190` becomes the row's word `+0x44` plus their average LP, counting the licences they own
   (`0x003237C0`), minus the cost of the licences the member owns; the result is kept between 0 and 99,999
   (`0x003175DF`, `0x00317614`-`0x00317652`).

With no other active main character, the level is 1 plus the row's byte. The shipped values are under Shipped
data.

The party row is the table's word `+8` times the selector `+4` plus the value `0x0020E600` returns for the table's
`+0xC`, added in 32 bits (`0x003174BC`-`0x003174D1`). Nothing guards it: when `[0x02EBF130]` is null (`0x0031749E`) or
`0x0020E600` returns 0 (`0x003174AB`), the row base is 0 and `0x003174D9` reads the byte at address `0x2C`, which faults,
because the first 64 KB of a Windows x64 process are never mapped.

### The commit and the wait

`0x003261D0(mode)` commits the staging map (`0x003261D0`-`0x003264F1`):

1. It closes up the active seats 0-3 and, apart from them, the reserve seats 4-8: each member moves forward over
   the empty seats before it (`0x003262C2`-`0x003262F5`, `0x003262F7`-`0x00326327`). A removed member's seat does not
   stay empty.
2. Each of the new seats 0-3 keeps the roster actor that already shows its member, and the other seats take the
   actors left over (`0x00326340`-`0x00326404`); the four are then installed with `0x00269C70` (`0x00326416`,
   `0x00326435`).
3. The nine seats of map 0 are written with `0x00329080(seat, selector, 0)` (`0x00326450`-`0x00326467`).
4. With mode 0, for each fighting unit `0x00236820(i)`, i 0-3, `0x003261D0` first clears byte `+0x23` of the unit's actor
   `+0x10` with `0x0037B4B0(actor)` when both are present, then records at `0x022C257C` the unit's party row, or `0xFF`
   for no unit or one whose byte `+0x00` bit `0x4` is clear; the model read-in then starts with `0x0037CA80()`
   (`0x00326471`-`0x003264B8`), which rebuilds the maps too (below).

   With mode 1, `0x003266C0` rebuilds the maps instead (`0x003264BF`). Every function on this page calls `0x003261D0` with
   0.

When the allocator `0x002F16B0` gives `0x0037CA80` a task, `0x0037CA80` ends with a tail jump to `0x00233CF0` (`0x0037CA9A`,
`0x0037CAE7`), which calls `0x0030D8B0(0)`, `0x003266C0()` and `0x00311E10(1)` in that order (`0x00233CF6`-`0x00233D05`), so mode
0 also runs the control-mode transition dispatcher `0x0030D8B0`, which mode 1's direct `0x003266C0` call does not.
`0x00233CF0` is told on [Party control modes](../Engine-Core/party-control-modes.md).

Every membership verb raises bit `0x13` of the busy mask `0x022CB720` with `0x003601B0`
([Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)). The verbs' poll handlers wait until
`0x003596B0` reports the read-in done, then clear the bit with `0x003601C0` (`0x0034C38A`-`0x0034C398`, `0x003506A6`-`0x003506B4`).

### The script verbs

| Verb | Handlers | Effect |
|---|---|---|
| `0x353` `addpartymember(sel)` | `0x0034C030`, `0x0034C370` | raises the busy bit and adds a main character with `0x003172E0` (`0x0034C3AC`-`0x0034C3BA`) |
| `0x354` `removepartymember(sel)` | `0x0034C030`, `0x0034CDF0` | removes a main character with `0x00328B20` (`0x0034CE2C`-`0x0034CE31`) |
| `0x355` `setbattlemember(a, b, c)` | `0x0034D4E0`, `0x003506A0` | chooses who fights, below |
| `0x358` `removebattlemember(sel)` | `0x00350160`, `0x003506A0` | for a main character, when more than one fights, moves it to a reserve seat with `0x003286E0` (`0x0035019D`-`0x003501AA`) |
| `0x359` `setbattlememberone(sel)` | `0x00350CD0`, `0x003506A0` | for a main character, keeps it, or else the first fighter, and moves the other main characters out of seats 0-2 with `0x003287A0`; guests and seat 3 stay (`0x00350D29`-`0x00350D52`) |
| `0x35A` `setbattlememberlock(sel, v)` | `0x00351A40`, `0x003506A0` | for a main character, sets or clears record flag bit `0x1` with `0x00328FB0` (`0x00328FD5`, `0x00328FDE`) |
| `0x35B` `addguestbattlemember(sel)` | `0x00352190`, `0x003506A0` | adds a guest with `0x003170E0` (`0x003521CD`-`0x003521DE`) |
| `0x35C` `removeguestbattlemember(sel)` | `0x00352AF0`, `0x003506A0` | removes a guest with `0x003288F0` (`0x00352B0A`-`0x00352B1E`) |
| `0x35E` `ispartymember(sel)` | `0x00353CB0` | a guest: in the fighting seats (`0x003596D0`); a main character: in the party (`0x00359740`) |
| `0x361` `getpartymembermask` | `0x003542C0` | the bit mask of the seated selectors outside the guest range (`0x00359C00`), bit `selector & 31` of each (`0x00359C3A`) |

The table lists the verbs that change membership and two that test it; `0x357` `getbattlemember` (`0x0034F5A0`) and
`0x35D` `isbattlemember` (`0x00353780`) are further queries.

`setbattlemember`, `setbattlememberone` and `addguestbattlemember` first hide the four roster actors of slots 0 to 3
(`0x00263750`) with `0x002ECD50(actor, 0)`, through its thunk `0x0026DC40` (`0x0034D520`-`0x0034D53B`, `0x00350CF5`-`0x00350D10`,
`0x003521A6`-`0x003521C1`).

For a class-3 actor whose bind state `+0x18` is not 1, `0x002ECD50(actor, 0)` clears bit `0x1` of byte `+0x10` of the
presentation record `[actor + 0xC0]`, since `0x002ECD50` writes the low bit of its second argument there, and then
tail-jumps to `0x002E8FD0(actor)`, which refreshes the actor's visibility; `0x002ECD50` itself takes nothing out of a
group (`0x002ECD50`-`0x002ECD76`). `0x002ECD50` is told on [Party during
scenes](../Scripts-And-Script-Commands/party-during-scenes.md).

### Choosing who fights

`setbattlemember(a, b, c)` takes three selectors in the order the script pushes them, `-1` for no selector
(`0x0034D547`-`0x0034D57B`). When every one given has its bit, the selector modulo 32 (`0x0034D568`), among
the main characters of the party (`0x00359C00`, `0x0034D57D`-`0x0034D58F`),
`0x00328DB0(list, 3)` moves them into fighting seats 0-2:

1. A fighting seat is held when its member's record has flag bit `0x1` set, the `setbattlememberlock` bit, or is a
   guest (`0x00328E20`-`0x00328E7F`).
2. A listed member already in seats 0-2 holds its seat; the others are swapped, in order, into the first free
   seat of 0-2 in the staging map (`0x00328E97`-`0x00328F6D`). With no free seat left the change is dropped.
3. The result is committed with `0x003261D0(0)` (`0x00328F71`).

The held seats are read from map 1, seats 0-3, through `0x002367A0` (`0x00328E0D`-`0x00328E7F`); the listed members are
found in map 0 and swapped in its staging copy `0x022C2580` (`0x00328EB0`, `0x00328EED`-`0x00328F65`). A listed selector
that is not seated in map 0 refuses the whole change, and so does running out of free seats: `0x00328DB0` then
returns -1 and commits nothing (`0x00328EA3`-`0x00328EC8`, `0x00328F40`-`0x00328F43`). It returns 0 after the commit
(`0x00328F76`). It reads at least three list entries, an entry of `-1` giving no selector (`0x00328DE3`-`0x00328DFA`,
`0x00328E97`).

If the leader's selector is not among the three, the first one given becomes the leader through `0x00327850`
(`0x0034D5A0`-`0x0034D5C3`, [Party leader](party-leader.md)).

### A member's actor in the roster

`0x00269C70(actor, slot)` installs an actor in the four-slot roster `0x0209A1F0` (`0x00269C70`-`0x00269D55`):

1. The actor's old slot, record byte `+0x12`, is emptied, and its record is reset to `+0x12 = 0xFF`,
   `+0xF = 3` (`0x00269CB7`-`0x00269CD9`).
2. The actor is stored in the slot, `+0x12` becomes the slot and `+0xF` becomes 2, or 3 for a slot outside 0-3
   (`0x00269CDD`-`0x00269CF3`). A slot of `-1` stores nothing and writes `0xFF`, the same as the reset, so it removes
   the actor cleanly; a slot above 3 is stored without a bounds check (`0x00269CE1`).
3. When no leader is set, the actor is requested as leader (`0x00269D21`-`0x00269D34`).

The actor that held the slot before is only notified (`0x00269C91`-`0x00269CAD`); its record keeps `+0x12` and
`+0xF`, so it still names the slot until it is installed again.

The notice sets byte `+0x152` of its controller `+0xC0` to 1 and refreshes its movement mode with `0x002681E0`
([Player movement](../Movement-And-Pathfinding/player-movement.md)). After step 2 the slot's actor gets `+0x152`
= 0 and the same refresh (`0x00269CFB`-`0x00269D17`), and after step 3 the installed actor is refreshed once more
(`0x00269D39`-`0x00269D41`). Both notices and step 3 run only for a slot 0-3 (`0x00269C8C`, `0x00269CF6`, `0x00269D1C`).

Steps 1 and 2 need a non-null actor (`0x00269CB2`). With a null actor the slot keeps its occupant, which gets
`+0x152` = 1 and then 0 again.

### Whom the others follow

Every member who is not controlled follows the leader; the formation and its one anchor are on
[Party leader](party-leader.md). A member who fights needs one of the battle unit slots
([Battle units](../Characters-And-Objects/battle-units.md)).

## Shipped data

### Party rows

The names are the row's name word at `+0x30`, read from text bank 8 of `battle_pack.bin` section 61
(`0x0023AB03`, `0x0031C6B1`, `0x0032958E`).

| Rows | Kind | Names |
|---|---|---|
| 0-6 | main | Vaan, Ashe, Fran, Balthier, Basch, Penelo, Reks |
| 7-16 | guest | Amalia, Basch, Basch, Lamont, Vossler, Vossler, Larsa, Reddas, Basch, Reddas |
| 17-25 | guest | entry 0 of the bank, the placeholder "No name" |
| 26 | chocobo | Chocobo |
| 27-39 | Esper | Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera, Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark |

### Catch-up and first-join items

The catch-up columns are the party row's bytes `+0x2C` bits under mask `0x18` and `+0x2E` and its word `+0x44`; the items
are the row's list at `+0x58` with its counts at `+0x34`, named from the shipped tables, and the gil is the row's
word `+0x3E`. Rows that are not listed have no catch-up, items or gil.

| Row | Catch-up | Level bonus | LP bonus | Items on the first join | Gil |
|---|---|---:|---:|---|---:|
| 0 Vaan | never | 1 | 0 | Potion x5, Steal, the Rabanastre and Nalbina Fortress key items, the gambits Ally: Vaan and Foe: targeting Vaan | 0 |
| 1 Ashe | first join | 1 | 100 | Hi-Potion x6, Phoenix Down x2, Ally: Ashe, Foe: targeting Ashe | 0 |
| 2 Fran | first join | 1 | 35 | Fire, Cure, Foe: any, Foe: targeting ally, Foe: highest HP, Foe: lowest HP, Foe: highest level, Foe: lowest level, Ally: Fran, Foe: targeting Fran | 300 |
| 3 Balthier | first join | 1 | 30 | First Aid, Phoenix Down x2, Ally: any, Ally: party leader, Ally: HP < 70%, Ally: HP < 50%, Ally: HP < 30%, Ally: status = HP Critical, Ally: Balthier, Foe: targeting Balthier | 300 |
| 4 Basch | first join | 2 | 70 | Ally: Basch, Foe: targeting Basch | 0 |
| 5 Penelo | every join | 0 | 20 | Potion x3, Phoenix Down, Foe: nearest visible, Foe: party leader's target, Ally: Penelo, Foe: targeting Penelo | 150 |
| 6 Reks | never | 3 | 0 | Potion x8, Hi-Potion x5, the Nalbina Fortress key item, Cure, Thunder | 0 |
| 7 Amalia | first join | 1 | 0 | Potion x10, Hi-Potion, Phoenix Down x2, Antidote x2, Eye Drops x3, Ally: guest | 1,230 |
| 8, 9 Basch | first join | 2 | 0 | no items | 0 |
| 10 Lamont | first join | 0 | 0 | Hi-Potion x12 | 0 |
| 11 Vossler | first join | 4 | 0 | Phoenix Down x3, Dispel Mote x3, Aeroga Mote | 0 |
| 12 Vossler | first join | 4 | 0 | Phoenix Down x7, Dispel Mote x4, Shock Mote | 0 |
| 13 Larsa | first join | 2 | 0 | no items | 0 |
| 14 Reddas | first join | 2 | 0 | Domaine Calvados x12, Serum x3, Dark Matter | 1,868 |
| 16 Reddas | first join | 2 | 0 | no items | 0 |

### Scripted joins and leaves

Every call of the membership verbs in the 1,114 `us` scripts of `plan_master` passes literal selectors. Three
developer test scripts (`evt_t0081`, `evt_t0083`, `evt_t0090`) make 112 of the 164 calls; the 52 calls of the
other scripts are these:

| Member | Joins (`addpartymember`) | Leaves (`removepartymember`) |
|---|---|---|
| 0 Vaan | no call | no call |
| 1 Ashe | `rsn_y01` | `naf_a01` |
| 2 Fran | `grm_a04`, `nal_b0101`, `rbn_a16` | `naf_a01`, `rbn_a17`, `rbn_a18`, `rbn_a19`, `slm_a01` |
| 3 Balthier | `grm_a04`, `nal_b0100`, `rbn_a16` | `naf_a01`, `rbn_a17`, `rbn_a18`, `rbn_a19`, `slm_a01` |
| 4 Basch | `slm_a01` | `naf_a01` |
| 5 Penelo | `rsn_b01`, `sav_b01` | `naf_a01`, `slm_a02` |

In the prologue at Nalbina (`naf_a01`, `naf_a02`) Basch is neither a party member nor a guest: each area makes him one
of its own battle units, the actor `BASH` set up with `btlAtelSetUnit` (unit 0 in `naf_a01`, unit 2 in `naf_a02`). The
`naf_a01` leaves in the table above are the main function of its actor `常駐監督` removing each of members 1 to 5
that is in the party while `EV_ナルビナ上層マップ進行` is below 10, and `naf_a02` calls none of the four
member and guest verbs.

| Guest | Joins (`addguestbattlemember`) | Leaves (`removeguestbattlemember`) |
|---|---|---|
| 7 Amalia | `grm_b02` | `slm_a01` |
| 8 Basch | `mic_a01` | `mic_b06` |
| 9 Basch | `mic_b06` | `rbn_a17`, `rbn_a18`, `rbn_a19` |
| 10 Lamont | `byu_a01` | `lus_g01` |
| 11 Vossler | `rsn_a01` | `rsn_b01` |
| 12 Vossler | `ene_a02` | `rwg_a01` |
| 13 Larsa | `glf_a02` | `bul_a01` |
| 14 Reddas | `var_z01` | `dgl_g01` |

| `setbattlemember` | Scripts |
|---|---|
| Vaan alone (0, -1, -1) | `rbn_a17`, `rbn_a18`, `rbn_a19`, `slm_a01`, `slm_a02` |
| Vaan and Balthier (0, 3, -1) | `nal_b0100` |
| Vaan, Balthier and Fran (0, 3, 2) | `grm_a04`, `nal_b0101` |
| Vaan and Penelo (0, 5, -1) | `sav_b01`, twice |

No script calls `removebattlemember`, `setbattlememberone` or `setbattlememberlock`, and no script adds Reks or a
guest row above 14. The other eight language folders make the same calls.

## State

The staging map `0x022C2580` is nine `u16` seats laid out like map 0: seats 0-3 fight, seats 4-8 are the reserve.
Each membership change copies map 0 into it (16 bytes for seats 0-7, then seat 8), changes it by seat index, and
`0x003261D0` closes up seats 0-3 and seats 4-8 and writes all nine back to map 0 through `0x00329080(seat, selector, 0)`
(`0x003262BB`-`0x00326327`, `0x00326450`-`0x00326467`). `0x003273D0` instead fills all nine from a list it is handed, `0xFF`
giving `0xFFFF` (`0x0032741D`-`0x003274D8`), and closes them up the same way (`0x003275CB`-`0x00327632`). All nine are 0 in
the file.

### Which seats an access reaches

Most accesses take the seat as an index, so the seats each one can reach decide the rows below:

| Function | Seats 0-3 | Seats 4-8 |
|---|---|---|
| `0x003172E0`, adding a main character | no seat | the free reserve seat from `0x00321100`: read `0x0031736B`, written `0x00317396` |
| `0x00326110`, from the guest add `0x003170E0` (`0x003171AE`), its only caller | seat 3, 2 or 1: read `0x0032615A`, written `0x00326185` | no seat |
| `0x003286E0`, `removebattlemember` | the member's fighting seat: read `0x00328770`, written `0x0032877C` | the free reserve seat from `0x00321100`: read `0x00328779`, written `0x0032877F` |
| `0x003287A0`, `setbattlememberone` | seats 0-2 only: read `0x003288A6`, written `0x003288B2` | the first empty reserve seat: read `0x00328890`, `0x003288AD`, written `0x003288B5` |
| `0x003288F0` and `0x00328B20`, the removes | the member's seat, found among all nine: written `0x0032895E`, `0x00328B92` | the same |
| `0x00328DB0`, `setbattlemember` | the free fighting seat, seats 0-2 only: read `0x00328F55`, written `0x00328F60`; a listed member's seat 3: read `0x00328F4C`, written `0x00328F5D` | the listed member's seat: read `0x00328F4C`, written `0x00328F5D` |
| `0x003261D0`, the commit | close-up and actor match: read `0x003262D1`, `0x00326340`, `0x00326346`, `0x003263CC`; written `0x003262E1`, `0x003262E6` | close-up: read `0x00326303`; written `0x00326313`, `0x00326318` |
| `0x003273D0`, the list fill | close-up and actor match: read `0x003275E0`, `0x00327646`, `0x0032764C`, `0x003276D7`; written `0x003275EF`, `0x003275F3` | close-up: read `0x00327610`; written `0x0032761F`, `0x00327623` |

Both `0x003261D0` (`0x00326450`) and `0x003273D0` (`0x00327760`) read every seat when they write the map back. The 16-byte
copy of seats 0-7 is at `0x0031734B` (`0x003172E0`), `0x00326131` (`0x00326110`), `0x00328758` (`0x003286E0`), `0x00328826`
(`0x003287A0`), `0x00328940` (`0x003288F0`), `0x00328B74` (`0x00328B20`) and `0x00328EF5` (`0x00328DB0`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2582` | `u16` | 0 | seat 1 of the staging map, a fighting seat | the 16-byte copy; `0x003273D0` (`0x00327437`); by seat index: `0x00326110` (`0x00326185`), `0x003286E0` (`0x0032877C`), `0x003287A0` (`0x003288B2`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F60`); the close-up of `0x003261D0` (`0x003262E1`, `0x003262E6`) and of `0x003273D0` (`0x003275EF`, `0x003275F3`) | `0x00326110` (`0x0032615A`); `0x003286E0` (`0x00328770`); `0x003287A0` (`0x003288A6`); `0x00328DB0` (`0x00328F55`); `0x003261D0` (`0x003262D1`, `0x00326340`, `0x00326346`, `0x003263CC`, `0x00326450`); `0x003273D0` (`0x003275E0`, `0x00327646`, `0x0032764C`, `0x003276D7`, `0x00327760`) |
| `0x022C2584` | `u16` | 0 | seat 2 of the staging map, a fighting seat | the 16-byte copy; `0x003273D0` (`0x0032744C`); by seat index: `0x00326110` (`0x00326185`), `0x003286E0` (`0x0032877C`), `0x003287A0` (`0x003288B2`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F60`); the close-up of `0x003261D0` (`0x003262E1`, `0x003262E6`) and of `0x003273D0` (`0x003275EF`, `0x003275F3`) | `0x00326110` (`0x0032615A`); `0x003286E0` (`0x00328770`); `0x003287A0` (`0x003288A6`); `0x00328DB0` (`0x00328F55`); `0x003261D0` (`0x003262D1`, `0x00326340`, `0x00326346`, `0x003263CC`, `0x00326450`); `0x003273D0` (`0x003275E0`, `0x00327646`, `0x0032764C`, `0x003276D7`, `0x00327760`) |
| `0x022C2586` | `u16` | 0 | seat 3 of the staging map, the fourth fighting seat, which `setbattlemember` and `setbattlememberone` never fill | the 16-byte copy; `0x003273D0` (`0x00327463`); by seat index: `0x00326110` (`0x00326185`), `0x003286E0` (`0x0032877C`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x003262E1`, `0x003262E6`) and of `0x003273D0` (`0x003275EF`, `0x003275F3`) | `0x00326110` (`0x0032615A`); `0x003286E0` (`0x00328770`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x003262D1`, `0x00326340`, `0x00326346`, `0x003263CC`, `0x00326450`); `0x003273D0` (`0x003275E0`, `0x00327646`, `0x0032764C`, `0x003276D7`, `0x00327760`) |
| `0x022C2588` | `u16` | 0 | seat 4 of the staging map, the first reserve seat | the 16-byte copy; `0x003273D0` (`0x0032747A`); by seat index: `0x003172E0` (`0x00317396`), `0x003286E0` (`0x0032877F`), `0x003287A0` (`0x003288B5`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x00326313`, `0x00326318`) and of `0x003273D0` (`0x0032761F`, `0x00327623`) | `0x003172E0` (`0x0031736B`); `0x003286E0` (`0x00328779`); `0x003287A0` (`0x00328890`, `0x003288AD`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x00326303`, `0x00326450`); `0x003273D0` (`0x00327610`, `0x00327760`) |
| `0x022C258A` | `u16` | 0 | seat 5 of the staging map, a reserve seat | the 16-byte copy; `0x003273D0` (`0x00327491`); by seat index: `0x003172E0` (`0x00317396`), `0x003286E0` (`0x0032877F`), `0x003287A0` (`0x003288B5`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x00326313`, `0x00326318`) and of `0x003273D0` (`0x0032761F`, `0x00327623`) | `0x003172E0` (`0x0031736B`); `0x003286E0` (`0x00328779`); `0x003287A0` (`0x00328890`, `0x003288AD`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x00326303`, `0x00326450`); `0x003273D0` (`0x00327610`, `0x00327760`) |
| `0x022C258C` | `u16` | 0 | seat 6 of the staging map, a reserve seat | the 16-byte copy; `0x003273D0` (`0x003274A8`); by seat index: `0x003172E0` (`0x00317396`), `0x003286E0` (`0x0032877F`), `0x003287A0` (`0x003288B5`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x00326313`, `0x00326318`) and of `0x003273D0` (`0x0032761F`, `0x00327623`) | `0x003172E0` (`0x0031736B`); `0x003286E0` (`0x00328779`); `0x003287A0` (`0x00328890`, `0x003288AD`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x00326303`, `0x00326450`); `0x003273D0` (`0x00327610`, `0x00327760`) |
| `0x022C258E` | `u16` | 0 | seat 7 of the staging map, a reserve seat | the 16-byte copy; `0x003273D0` (`0x003274BF`); by seat index: `0x003172E0` (`0x00317396`), `0x003286E0` (`0x0032877F`), `0x003287A0` (`0x003288B5`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x00326313`, `0x00326318`) and of `0x003273D0` (`0x0032761F`, `0x00327623`) | `0x003172E0` (`0x0031736B`); `0x003286E0` (`0x00328779`); `0x003287A0` (`0x00328890`, `0x003288AD`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x00326303`, `0x00326450`); `0x003273D0` (`0x00327610`, `0x00327760`) |
| `0x022C2590` | `u16` | 0 | seat 8 of the staging map, the last reserve seat | the copy: `0x003172E0` (`0x0031735A`), `0x00326110` (`0x00326140`), `0x003286E0` (`0x00328766`), `0x003287A0` (`0x00328840`), `0x003288F0` (`0x0032894F`), `0x00328B20` (`0x00328B83`), `0x00328DB0` (`0x00328F04`); `0x003273D0` (`0x003274D8`); by seat index: `0x003172E0` (`0x00317396`), `0x003286E0` (`0x0032877F`), `0x003287A0` (`0x003288B5`), `0x003288F0` (`0x0032895E`), `0x00328B20` (`0x00328B92`), `0x00328DB0` (`0x00328F5D`); the close-up of `0x003261D0` (`0x00326313`, `0x00326318`) and of `0x003273D0` (`0x0032761F`, `0x00327623`) | `0x003172E0` (`0x0031736B`); `0x003286E0` (`0x00328779`); `0x003287A0` (`0x00328890`, `0x003288AD`); `0x00328DB0` (`0x00328F4C`); `0x003261D0` (`0x00326303`, `0x00326450`); `0x003273D0` (`0x00327610`, `0x00327760`) |

No other instruction reaches seats 1-8. The two close-up loops also take the address of seat 4 (`0x00326334`,
`0x0032763F`).

The staging map's address is also taken by `0x0031A300` and `0x00324380`, which write one byte per unit 0-3 from
`0x022C257C`, below the map. The one indexed table read that could reach it, `0x00308E80(i)` on the unit pointers at
`0x022C24E0 + i x 8`, has one caller, the debug menu's "Chara Name" readout (`0x001CFC2A`), whose index field `+0x10A8`
holds only the 0 its constructor `0x001CCB20` stores (`0x001CCE34`, `0x001CCF79`), so it reads the first pointer and never the map.

## Modding notes

- For rows 0-6 a join adds each worn piece to the owned and worn counts and a leave subtracts it, so gear given to
  a member who later leaves goes with them (`0x00316E87`-`0x00316EB1`, `0x00323540`-`0x003235BA`). Guest rows 7-25 skip
  both, so a guest's gear never reaches the inventory, while their first-join items and gil do (`0x00316FE1`-`0x00317034`).
- A guest's seat is the highest free active seat; with seats 1-3 all taken, the guest add fails without a message.
- The catch-up and first-join columns are plain bytes of the party row, so a modded row changes them without code.
- Locking a member with `setbattlememberlock` keeps `setbattlemember` from moving it out of its fighting seat.

## Related

- [Party slots](party-slots.md) - the seats and the five maps the adds and removes write.
- [Party leader](party-leader.md) - the leader, the formation and the roster.
- [Party data](party-data.md) - the party block that holds the seats and the records.
- [Scenario presets](scenario-presets.md) - the sets that refill the party at once.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the member records and their flag word.
- [Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md) - the busy mask.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat AI: `0x002367A0` is called by `0x00301AD0`; those functions are documented on
  [glossary](../Engine-Core/glossary.md).
- Platform: `0x001CCB20` calls `0x005CC930`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Actor entity: `0x002E8FD0` is called by `0x00265B60`, `0x002E35B0`; those functions are documented on
  [actor record](../Characters-And-Objects/actor-record.md).
- Input: `0x00263750` is called by `0x00226BE0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- Save load settings: `0x00236740` is called by `0x00583D60`; those functions are documented on
  [native limits](../Engine-Core/native-limits.md).
- UI: `0x00236820` is called by `0x0031EB20`, `0x00322A80`; those functions are documented on
  [action definition row](../Battle-Actions/action-definition-row.md),
  [target selection](../Battle-Actions/target-selection.md).
