---
title: "Party members and guests: who can join, how the story adds and removes them, where a guest sits, and what a join brings"
kind: "system"
category: "Party"
addresses: "003172E0, 003170E0, 00328B20, 003288F0, 00316DF0, 00317480, 00323540, 003261D0, 00328DB0, 00269C70, 00322350"
---

## What the player sees

- Characters join and leave as the story goes on, and guests travel with the party for a while.
- A character who joins brings their equipment into the inventory, and on their first join also brings items and
  gil.
- A character who joins may catch up, as its party row says: on the first join only for Ashe, Fran,
  Balthier, Basch and the guests, on every join for Penelo, never for Vaan and Reks. Catching up sets
  level and LP from the two strongest members already in the party.
- A character who joins arrives with full HP, unless they have Disease.
- A character who leaves takes their equipment with them.
- Some scenes decide who fights, for example leaving Vaan to fight alone.

## How it works

### Members and guests

A party member is named by its selector, which is its row of the party table and of the forty member records
([Party slots](party-slots.md)). Selectors 0-6 are the main characters and 7-25 the guests; `00322350` is the
guest test, `sel - 7 <= 12h` as a byte. Row 26 is the chocobo and rows 27-39 the Espers, which no membership
function accepts. The names are under Shipped data.

### Adding a main character

`003172E0(sel)` adds a main character (`003172E0`-`003173E9`):

1. It refuses a selector above 6, and one already in any of map 0's nine seats (`00317310`-`00317329`), so nobody
   is in the party twice.
2. `00321100` finds a free reserve seat, the first of seats 4-8 of map 3 whose id check fails or whose byte is
   `FF`<sub>h</sub> (`0032110A`-`00321148`); there is none when all five are taken, and the add fails.
3. Map 0 is copied to the staging map `022C2580`, and the selector is written to that seat if it is empty there
   (`00317343`-`00317396`).
4. The member's record is activated with `00316DF0` and the change is committed with `003261D0(0)`
   (`003173BE`-`003173D9`).

### Adding a guest

`003170E0(sel)` adds a guest (`003170E0`-`003171AE`). It refuses a selector outside 7-25 and one already seated,
like the main add. It then tries active seats 3, 2 and 1 of map 3, in that order, and takes the first whose id
check fails or whose byte is `FF`<sub>h</sub> (`0031711A`-`00317157`). Seat 0 is never tried, but the commit closes up the
active seats, so a guest given seat 3 while seat 2 is empty ends up in seat 2.

`00326110(sel, seat, 0, 1)` then copies map 0 to the staging map, writes the selector to the seat if it is empty
there, activates the record with `00316DF0` and commits with `003261D0(0)` (`00326129`-`003261B1`).

### Removing a member or a guest

`00328B20(sel)` removes a main character and `003288F0(sel)` a guest (`00328B20`-`00328BC2`,
`003288F0`-`0032898E`). Each refuses a selector outside its range or not seated in map 0. It copies map 0 to the
staging map, empties the member's seat with `FFFF`<sub>h</sub>, deactivates the record with `00323540` and commits with
`003261D0(0)`.

### What a join brings

`00316DF0(record)` activates a member record that is not yet active, record flag bit 4 (`00316DFE`):

1. It runs the catch-up below (`00316E1D`), unless its second argument has bit 1 set and flag bit 13 of the party
   block is clear (`00316E0F`-`00316E1B`). The adds give 0; the seat writer `00329080(seat, selector, 3)` of the
   scenario presets gives 3 (`00329167`-`0032916A`), so a member seated there gets no catch-up.
2. When flag bit 13 of the party block is set and the record has never been active, flag bit 3, the level is set
   to 90 with `0030C470(record, 90, 0)` (`00316E25`-`00316E3D`).
3. For a main character, each of the five equipment words is added to the inventory, and to the count of equipped
   pieces (`00316E87`-`00316EB1`).
4. On the record's first activation, flag bit 3 clear, each enabled gambit slot's condition is added, and for a main
   character also the id the slot's action row names at `+22`<sub>h</sub>, the magick or technick it uses (`00316EC3`-`00316F92`).
   An item id there goes to the unused channel 4 and adds nothing ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md)).
5. On that first activation the up to ten ids the party row lists at `+58`<sub>h</sub> are added, with counts at
   `+34`<sub>h</sub> (`00316FE1`-`00317019`), and the gil at row `+3E`<sub>h</sub> (`0031701B`-`00317034`).
6. HP is set to max HP, or twice max HP under Bubble; under Disease it stays, but at least 1
   (`00317048`-`00317082`). Flag bits 3 and 4 are then set.

`00323540(record)` deactivates an active main character (`00323540`-`003235BA`): each of the five equipment words
leaves the equipped count and the inventory, and flag bit 4 is cleared. A guest's equipment is never counted, and
the first-join items and gil are not taken back.

### Catching up on a join

`00317480(record)` sets a joining member's level and LP from the party (`00317480`-`00317667`). The party row's
byte `+2C`<sub>h</sub>, bits 3-4, says when: 1 on the first activation only, 2 on every activation, anything else never
(`003174D9`-`0031750D`).

1. It takes the two other active main characters with the highest levels, record `+1C2`<sub>h</sub>
   (`00317540`-`003175B4`).
2. The level becomes their average level, at least 1, plus the row's byte `+2E`<sub>h</sub>, through `0030C470`
   (`00317600`-`0031762C`).
3. The LP at `+190`<sub>h</sub> becomes the row's word `+44`<sub>h</sub> plus their average LP, counting the licences they own
   (`003237C0`), minus the cost of the licences the member owns; the result is kept between 0 and 99,999
   (`003175DF`, `00317614`-`00317652`).

With no other active main character, the level is 1 plus the row's byte. The shipped values are under Shipped
data.

### The commit and the wait

`003261D0(mode)` commits the staging map (`003261D0`-`003264F1`):

1. It closes up the active seats 0-3 and, apart from them, the reserve seats 4-8: each member moves forward over
   the empty seats before it (`003262C2`-`003262F5`, `003262F7`-`00326327`). A removed member's seat does not
   stay empty.
2. Each of the new seats 0-3 keeps the roster actor that already shows its member, and the other seats take the
   actors left over (`00326340`-`00326404`); the four are then installed with `00269C70` (`00326416`,
   `00326435`).
3. The nine seats of map 0 are written with `00329080(seat, selector, 0)` (`00326450`-`00326467`).
4. With mode 0, the party rows of the four fighting units are recorded at `022C257C` and the model read-in starts
   with `0037CA80` (`00326471`-`003264B8`); with mode 1, `003266C0` rebuilds the maps instead (`003264BF`). Every
   function on this page calls it with 0.

Every membership verb raises bit `13`<sub>h</sub> of the busy mask `022CB720` with `003601B0`
([Zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)). The verbs' poll handlers wait until
`003596B0` reports the read-in done, then clear the bit with `003601C0` (`0034C38A`-`0034C398`, `003506A6`-`003506B4`).

### The script verbs

| Verb | Handlers | Effect |
|---|---|---|
| `353`<sub>h</sub> `addpartymember(sel)` | `0034C030`, `0034C370` | raises the busy bit and adds a main character with `003172E0` (`0034C3AC`-`0034C3BA`) |
| `354`<sub>h</sub> `removepartymember(sel)` | `0034C030`, `0034CDF0` | removes a main character with `00328B20` (`0034CE2C`-`0034CE31`) |
| `355`<sub>h</sub> `setbattlemember(a, b, c)` | `0034D4E0`, `003506A0` | chooses who fights, below |
| `358`<sub>h</sub> `removebattlemember(sel)` | `00350160`, `003506A0` | for a main character, when more than one fights, moves it to a reserve seat with `003286E0` (`0035019D`-`003501AA`) |
| `359`<sub>h</sub> `setbattlememberone(sel)` | `00350CD0`, `003506A0` | for a main character, keeps it, or else the first fighter, and moves the other main characters out of seats 0-2 with `003287A0`; guests and seat 3 stay (`00350D29`-`00350D52`) |
| `35A`<sub>h</sub> `setbattlememberlock(sel, v)` | `00351A40`, `003506A0` | for a main character, sets or clears record flag bit 0 with `00328FB0` (`00328FD5`, `00328FDE`) |
| `35B`<sub>h</sub> `addguestbattlemember(sel)` | `00352190`, `003506A0` | adds a guest with `003170E0` (`003521CD`-`003521DE`) |
| `35C`<sub>h</sub> `removeguestbattlemember(sel)` | `00352AF0`, `003506A0` | removes a guest with `003288F0` (`00352B0A`-`00352B1E`) |
| `35E`<sub>h</sub> `ispartymember(sel)` | `00353CB0` | a guest: in the fighting seats (`003596D0`); a main character: in the party (`00359740`) |
| `361`<sub>h</sub> `getpartymembermask` | `003542C0` | the bit mask of the seated selectors outside the guest range (`00359C00`) |

The table lists the verbs that change membership and two that test it; `357`<sub>h</sub> `getbattlemember` (`0034F5A0`) and
`35D`<sub>h</sub> `isbattlemember` (`00353780`) are further queries.

`setbattlemember`, `setbattlememberone` and `addguestbattlemember` first take the four roster actors out of the
target group with `002ECD50(actor, 0)`, through its thunk `0026DC40` (`0034D520`-`0034D53B`, `00350CF5`-`00350D10`, `003521A6`-`003521C1`).

### Choosing who fights

`setbattlemember(a, b, c)` takes three selectors in the order the script pushes them, `-1` for none
(`0034D547`-`0034D57B`). When every one given is in the party (`00359C00`, `0034D57D`-`0034D58F`),
`00328DB0(list, 3)` moves them into fighting seats 0-2:

1. A fighting seat is held when its member's record has flag bit 0 set, the `setbattlememberlock` bit, or is a
   guest (`00328E20`-`00328E7F`).
2. A listed member already in seats 0-2 holds its seat; the others are swapped, in order, into the first free
   seat of 0-2 in the staging map (`00328E97`-`00328F6D`). With no free seat left the change is dropped.
3. The result is committed with `003261D0(0)` (`00328F71`).

If the leader's selector is not among the three, the first one given becomes the leader through `00327850`
(`0034D5A0`-`0034D5C3`, [Party leader](party-leader.md)).

### A member's actor in the roster

`00269C70(actor, slot)` installs an actor in the four-slot roster `0209A1F0` (`00269C70`-`00269D55`):

1. The actor's old slot, record byte `+12`<sub>h</sub>, is emptied, and its record is reset to `+12h = FFh`,
   `+Fh = 3` (`00269CB7`-`00269CD9`).
2. The actor is stored in the slot, `+12`<sub>h</sub> becomes the slot and `+F`<sub>h</sub> becomes 2, or 3 for a slot outside 0-3
   (`00269CDD`-`00269CF3`). A slot of `-1` stores nothing and writes `FF`<sub>h</sub>, the same as the reset, so it removes
   the actor cleanly; a slot above 3 is stored without a bounds check (`00269CE1`).
3. When no leader is set, the actor is requested as leader (`00269D21`-`00269D34`).

The actor that held the slot before is only notified (`00269C91`-`00269CAD`); its record keeps `+12`<sub>h</sub> and
`+F`<sub>h</sub>, so it still names the slot until it is installed again.

### Whom the others follow

Every member who is not controlled follows the leader; the formation and its one anchor are on
[Party leader](party-leader.md). A member who fights needs one of the battle unit slots
([Battle units](../Characters-And-Objects/battle-units.md)).

## Shipped data

### Party rows

The names are the row's name word at `+30`<sub>h</sub>, read from text bank 8 of `battle_pack.bin` section 61
(`0023AB03`, `0031C6B1`, `0032958E`).

| Rows | Kind | Names |
|---|---|---|
| 0-6 | main | Vaan, Ashe, Fran, Balthier, Basch, Penelo, Reks |
| 7-16 | guest | Amalia, Basch, Basch, Lamont, Vossler, Vossler, Larsa, Reddas, Basch, Reddas |
| 17-25 | guest | entry 0 of the bank, the placeholder "No name" |
| 26 | chocobo | Chocobo |
| 27-39 | Esper | Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera, Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark |

### Catch-up and first-join items

The catch-up columns are the party row's bytes `+2C`<sub>h</sub> bits 3-4 and `+2E`<sub>h</sub> and its word `+44`<sub>h</sub>; the items
are the row's list at `+58`<sub>h</sub> with its counts at `+34`<sub>h</sub>, named from the shipped tables, and the gil is the row's
word `+3E`<sub>h</sub>. Rows that are not listed have no catch-up, items or gil.

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
| 8, 9 Basch | first join | 2 | 0 | none | 0 |
| 10 Lamont | first join | 0 | 0 | Hi-Potion x12 | 0 |
| 11 Vossler | first join | 4 | 0 | Phoenix Down x3, Dispel Mote x3, Aeroga Mote | 0 |
| 12 Vossler | first join | 4 | 0 | Phoenix Down x7, Dispel Mote x4, Shock Mote | 0 |
| 13 Larsa | first join | 2 | 0 | none | 0 |
| 14 Reddas | first join | 2 | 0 | Domaine Calvados x12, Serum x3, Dark Matter | 1,868 |
| 16 Reddas | first join | 2 | 0 | none | 0 |

### Scripted joins and leaves

Every call of the membership verbs in the 1,114 `us` scripts of `plan_master` passes literal selectors. Three
developer test scripts (`evt_t0081`, `evt_t0083`, `evt_t0090`) make 112 of the 164 calls; the 52 calls of the
other scripts are these:

| Member | Joins (`addpartymember`) | Leaves (`removepartymember`) |
|---|---|---|
| 0 Vaan | none | none |
| 1 Ashe | `rsn_y01` | `naf_a01` |
| 2 Fran | `grm_a04`, `nal_b0101`, `rbn_a16` | `naf_a01`, `rbn_a17`, `rbn_a18`, `rbn_a19`, `slm_a01` |
| 3 Balthier | `grm_a04`, `nal_b0100`, `rbn_a16` | `naf_a01`, `rbn_a17`, `rbn_a18`, `rbn_a19`, `slm_a01` |
| 4 Basch | `slm_a01` | `naf_a01` |
| 5 Penelo | `rsn_b01`, `sav_b01` | `naf_a01`, `slm_a02` |

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

No script calls `removebattlemember`, `setbattlememberone` or `setbattlememberlock`, and none adds Reks or a
guest row above 14. The other eight language folders make the same calls.

## Modding notes

- A join adds the member's equipment to the inventory and a leave removes it, so equipment given to a member who
  later leaves goes with them.
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
