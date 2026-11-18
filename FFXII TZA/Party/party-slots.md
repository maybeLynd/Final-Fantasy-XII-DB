[Home](../../README.md) / [Party](README.md) / Party slots

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Party slots: the nine seats, the five slot maps the game reads them through, and how a seat reaches its battle unit | system | Party | The party in play | How the party is seated: the nine two-byte seats of the live party, four active and five reserve, the four copies the battle, the battle menu and the rest of the game read instead, how a new game fills them, how the copies are rebuilt for summons, chocobo rides, towns and scripted party modes, and the functions that turn a seat into a stats record or a battle unit. | 0x0031B9F0, 0x0031B810, 0x00320AB0, 0x00329CC0, 0x003266C0, 0x0030D9A0 |

## What the player sees

The party menu shows four fighting members and up to five in reserve. During a summon only the summoner and
the Esper fight, on a chocobo only the rider, in a town only the leader walks, and some story scenes fix who
is in the party; afterwards the party is as it was.

The game keeps the real party as one list of nine seats in the party block, plus four working copies that the fight,
the battle menu and the rest of the game read. A summon, a chocobo ride, a town or a scripted party rebuilds the
copies from the real list for that mode, while the real list stays as it was.

## How it works

### The nine seats

The party lives in the party block `[0x02EBF190]` as five slot maps of nine two-byte seats each, `0x12`
bytes apart¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031BA3D`-`0x0031BAAA` |

</details>

| Map | Offset | Read by |
|---:|---|---|
| 0 | `+0x5A48` | the live party: the menu, joining and leaving, unequipping (`0x0030FD10`, `0x00273880`) |
| 1 | `+0x5A5A` | the fight: `0x0031B810` and everything that walks the four fighting members |
| 2 | `+0x5A6C` | the battle command menu (`0x0035BC50` at `0x0035BDB9`) |
| 3 | `+0x5A7E` | the rest of the game: equipment, rewards, targets, scripts, mostly through `0x00320AB0` |
| 4 | `+0x5A90` | the members' field actors and the chocobo mount: `0x0031C470` and `0x00320230` (for `0x0035A490`, `0x0035AD40`), `0x0031C0F0`, `0x0031C250`, and `0x0031B950`, the map-4 twin of `0x0031B810` (for `0x00304060`, `0x00304140`) |

Seats 0-3 are the active members and seats 4-8 the reserve. The low byte of a seat is the member's selector,
the row of the party table and of the forty member stats records; `0xFF` is an empty seat. The leader selector is
kept at `+0x5AA4`; [Party leader](party-leader.md) turns it into the leader, the handle `0x022C7FE0`.

### Reading a seat

`0x0031B9F0(seat, map)` returns the low byte of a seat¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031B9F0`-`0x0031BAB7` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The seat must pass the class-23 id check, 0 to 8 (`0x0031BA04`-`0x0031BA0F`; [Item and ability ids](../Engine-Core/item-and-ability-ids.md)); a seat that fails it returns `0xFF`. | `0x0031BA11` |
| 2 | The map picks the offset; any map above 4 returns `0xFF`, and so does a negative map. | `0x0031BA1E`-`0x0031BA34` |
| 3 | Otherwise it returns the byte at `[0x02EBF190]` + the map's offset + 2 × seat. | `0x0031BA36`-`0x0031BAAA` |

These turn the selector into a record or a unit:

- `0x00320AB0(seat, map)` returns the member's stats record, `[0x02EBF190] + 8 + selector * 0x1C8`, or 0 for a
  selector above 39 ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md); `0x00320AB4`-`0x00320AD9`);
- `0x0031B810(seat)` reads map 1 directly and returns the battle unit with that selector¹; a seat that `0x00322C50(0x17, seat, 0)` refuses is looked up as selector `0xFF` instead
 ²;
- `0x0031FE70` and `0x00320040` take the map first and pass the stats record on to `0x00329220`
 ³;
- `0x0030A6E0` reads map 1 for a mask of the fighting members by kind, main character, guest, Esper or chocobo,
  leaving out members who are down.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031B81C`-`0x0031B851`, `0x002367A0` |
| ² | `0x0031B822`-`0x0031B835` |
| ³ | `0x0031FE7A`-`0x0031FEBA`, `0x0032004A`-`0x0032008D` |

</details>

Besides the new-game fill below, map 0's seats are written by `0x00329080`¹ when a member
joins or leaves ([Party members](party-members.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00329122`, `0x00329176` |

</details>

### A new game's party

`0x00329CC0` fills map 0 from the nine bytes at `0x01EED260`, `00` then eight `FF`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00329CF0`-`0x00329DAE` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | A selector is seated and its record activated with `0x00316DF0`, when `0x00322C50(2, selector)` accepts it as a row of the party definitions and it is at most `0x27`; otherwise the seat is left as it was. | `0x00329D53`-`0x00329D9E`<br>`0x00329D53`-`0x00329D8B` |
| 2 | An empty byte empties the seat, deactivating the record that was there with `0x00323540`. A seat whose selector is above `0x27` holds no record and is left as it was. | `0x00329D0D`-`0x00329D51`<br>`0x00329D2C`-`0x00329D32` |
| 3 | The first byte becomes the leader selector `+0x5AA4`, and `0x00326500` asks for the default controlled member. | `0x00329DBB`-`0x00329DC8` |
| 4 | Maps 1-4 become copies of map 0. | `0x00329DE3`-`0x00329E27` |

Each seat index first passes `0x00322C50(0x17, seat)`, which accepts 0 to 8, so no seat is skipped¹. The fill starts with a call of `0x003148F0`, the current area index,
whose result it does not use², and the leader selector is stored as a dword³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00329CF4`-`0x00329D07`, `0x00329D13`-`0x00329D23` |
| ² | `0x00329CD5` |
| ³ | `0x00329DC2` |

</details>

### Rebuilding the copies

`0x003266C0` rebuilds maps 1-4 from map 0¹. It first calls `0x00311E20`², then
makes maps 1 and 3 copies of map 0, empties the reserve of map 1, and makes maps 2 and 4 copies of map 1, after
saving map 4³. Then it adjusts the four active seats by the party control mode `0x0030D9A0`
([Party control modes](../Engine-Core/party-control-modes.md)):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003266C0`-`0x00326B97` |
| ² | `0x003266EF` |
| ³ | `0x003266F4`-`0x0032674B` |

</details>

| Mode | Seats 0-3 of maps 1, 2 and 4 | Sites |
|---|---|---|
| 0, normal, or any other value | as copied | - |
| 1, summon | seat 3 holds the Esper (`0x003137E0`); of seats 0-2 only the summoner's is kept, the map-0 seat `0x00313800` finds for the summoner's row among all nine, when it is seat 0, 1 or 2; a summoner in seat 3, in seats 4-8 or not found keeps no seat, and the others are emptied | `0x003269D2`-`0x00326A32` |
| 2, chocobo | seat 3 of maps 1 and 4 holds party row 26, the chocobo, and the other seats of map 1 are emptied; map 2 keeps only the rider's seat (`0x00327200`) when it is seat 0, 1 or 2, and its seat 3 is emptied in every case (`0x003269AB`) | `0x00326991`-`0x003269D0` |
| 3, town | map 4 is restored; the area's leader (`0x00377C70`) fills its seat of maps 1, 2 and 4, or seat 3, and the other seats of maps 1 and 2 are emptied | `0x003268F3`-`0x0032698C` |
| 4, event party | only the leader's seat is kept, in maps 1, 2 and 4 | `0x0032683F`-`0x003268EE` |
| 5, second event party | map 4 is restored; only the leader's seat is kept, in maps 1 and 2 | `0x00326783`-`0x0032683A` |

In modes 4 and 5 the leader's seat is that of the leader selector `+0x5AA4`, or with the area's town bit the area's leader at the controlled
member's seat¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003267B7`-`0x003267E8`, `0x0032686E`-`0x0032689F` |

</details>

Then, for each seat `s` from 0 to 3, the loop takes the roster actor `0x00263750(s)` and its unit `0x00263E30(actor)`;
a seat without either is passed over (`0x00326A40`-`0x00326A5E`, back branch `0x00326B18`). The unit's present id is
its stats record's word `+0x04` when unit flag bit `0x4` is set, else `0xFFFF`; the new id is the whole word of
map 1's seat `s`; equal ids leave the unit as it is¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00326A64`-`0x00326A82` |

</details>

A unit that holds no member goes straight to `0x0023A570(unit, new id)`¹. A unit whose seat is now empty first loses flag bit `0x4000000`². A unit that changes from one member to another gets, before that same clear and the install:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00326A88`-`0x00326A8C`, `0x00326B04`-`0x00326B0A` |
| ² | `0x00326A8E`-`0x00326A92`, `0x00326AFD` |

</details>

- `0x002ECF10(a, b, 0)`, with `a` the unit's actor pointer `+0x10` and `b` the bit `0x800000` of the unit's
  flags, and `0x003105D0(unit)`
 ¹;
- `0x00300E40(unit, 0)` when its first byte has bit `0x2` clear and either it has no stats record `+0x698` or that
  record's dwords `+0x64` and `+0x3C` together have a bit of `0x80000003` set while `0x00313F60()` answers 0
 ²;
- `0x002E42D0(a)`, `0x002699D0(a)` and `0x002ECEC0(a)`, and flag bit `0x40` set³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00326A94`-`0x00326AA9` |
| ² | `0x00326AAE`-`0x00326ADA` |
| ³ | `0x00326ADF`-`0x00326AFA` |

</details>

The call at `0x00326B0A` is the one call found that can pass a party id to the installer
([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)); it passes the seat's word for
the unit of the roster actor with the seat's index.

At the end `0x00326500` picks the controlled member, and `0x022C2670` counts the seats 0 to 3 that
`0x00322C50(0x17, seat, 0)` accepts, whose member byte is `0x27` or less and whose party record has none of the bits
`0x80000003` set, or has them while `0x00313F60()` answers non-zero¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00326B1E`-`0x00326B97` |

</details>

### Who asks for a seat's unit

Twenty-seven direct call or jump instructions have `0x0031B810` as their target, one in each of twenty-seven
functions, and no pointer to it is stored in the file: each of them takes its unit from a seat of map 1.

In the table a seat unit is in play when it has a stats record whose
dwords `+0x64` and `+0x3C` have none of the bits `0x80000003`, or has them while `0x00377C20()` answers non-zero.
`0x00313F60`, named in the loop above, is a jump to `0x00377C20`: the two are one test.

| Function | Its call of `0x0031B810` | Page, and its use of the seat's unit |
|---|---|---|
| `0x00234150` | `0x0023416A` | listed on [Field runtime](../Characters-And-Objects/field-runtime.md): for each seat unit with flag bit `0x10`, `0x002FED60(unit, 1)` when `0x00308010(unit, 1)` answers non-zero, else `0x002FEDC0(unit, 1)` (`0x00234168`-`0x002341A6`) |
| `0x00234DA0` | `0x00234DE2` | [Enemy spawning](../Enemy-Spawning/enemy-spawning.md) |
| `0x002350C0` | `0x00235215` | [Enemy spawning](../Enemy-Spawning/enemy-spawning.md) |
| `0x00235DD0` | `0x00235DFE` | [Verb table](../Scripts-And-Script-Commands/verb-table.md) |
| `0x00237140` | `0x00237152` | [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) |
| `0x002371B0` | `0x002371C2` | [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) |
| `0x00237260` | `0x00237272` | [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) |
| `0x002372E0` | `0x002372F2` | [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) |
| `0x00237460` | `0x002374A8` | [Verb table](../Scripts-And-Script-Commands/verb-table.md) |
| `0x002F8BB0` | `0x002F8C96` | [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md) |
| `0x002FB8C0` | `0x002FB912` | [Traps](../World-Areas-And-Travel/traps.md) |
| `0x003001D0` | `0x003001FA` | named on [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md): `0x002ECEC0(a)`, with `a` the unit's actor pointer `+0x10`, for each in-play seat unit (`0x003001F8`-`0x00300263`) |
| `0x00301310` | `0x00301344` | named on [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md): `(u, v, w)` stores `w` in the dword `+0xBB8` of each in-play seat unit that holds `v` there (0 with flag bit `0x4000` clear) and whose word `+0xBA0` is `0x115` or less, when that word's row of the table `0x02EBF138` has byte `+0x2C` bit `0x40` and byte `+0x64` of `u`'s stats record has bit `0x1`, or bit `0x80` and bit `0x2` (`0x00301342`-`0x00301493`) |
| `0x00301AD0` | `0x00302712` | [Enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md): for opcodes 34 and 35 with `s` = 18, takes the least (34) or the greatest (35) `0x0031E6F0` answer over the in-play seat units, collected on the first candidate (`0x003026EC`-`0x003027C1`) |
| `0x00307E70` | `0x00307E9A` | [Force fight mode](../Engine-Core/force-fight-mode.md) |
| `0x00309FB0` | `0x0030A054` | [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md): raises its count by one for each in-play seat unit whose word `+0xDC8` equals the id (`0x0030A052`-`0x0030A0DE`) |
| `0x0030A8A0` | `0x0030A8D4` | [Enmity](../Enemy-AI-And-Gambits/enmity.md) |
| `0x0030D160` | `0x0030D482` | [Area of effect](../Battle-Actions/area-of-effect.md): when the target handle gives a unit (`0x0030D18A`-`0x0030D195`), the user's byte `+0x6B6` is 0 and bit `0x2` of the action row's `+0x0C` is set, adds the actor of each in-play seat unit the list does not hold yet to the targets (`0x0030D205`-`0x0030D20C`, `0x0030D461`-`0x0030D50A`) |
| `0x0030D600` | `0x0030D636` | [Quickenings and summons](../Battle-Actions/quickenings-and-summons.md) |
| `0x0030F130` | `0x0030F268` | [Gambits](../Enemy-AI-And-Gambits/gambits.md): adds to the candidates each seat member whose statuses meet the action's mask in the bits `0x80000003` (`0x0030F266`-`0x0030F2B2`) |
| `0x00310920` | `0x00310972` | [Navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) |
| `0x00311B20` | `0x00311BF7` | [Battle verbs](../Scripts-And-Script-Commands/battle-verbs.md): with `all` set and past its two -1 exits (`0x00311B3E`-`0x00311B74`), issues to each in-play seat unit through `0x00311CF0` (`0x00311BE6`-`0x00311C86`) |
| `0x00311E90` | `0x00311EBA` | [Battle verbs](../Scripts-And-Script-Commands/battle-verbs.md) |
| `0x00313670` | `0x0031369A` | [Navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md): re-places each in-play seat unit but the leader with `0x00311F70(0, unit, 0)` (`0x0031368A`-`0x0031370A`) |
| `0x00313B30` | `0x00313BD4` | [Action commit](../Battle-Actions/action-commit.md) |
| `0x00338490` | `0x003385C2` | [Party leader](party-leader.md) |
| `0x00388D50` | `0x00388DF2` | [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) |

Twelve of these functions collect their seat units in the one staging list `0x022C1788`, each with its own walk,
and so overwrite what the last of them left there: `0x003001D0`, `0x00301310`, `0x00301AD0`, `0x00307E70`, `0x00309FB0`,
`0x0030D160`, `0x0030D600`, `0x00310920`, `0x00311B20`, `0x00311E90`, `0x00313670` and `0x00313B30` (the stores at `0x00300230`,
`0x0030137A`, `0x00302747`, `0x00307ED0`, `0x0030A089`, `0x0030D4B8`, `0x0030D685`, `0x003109A8`, `0x00311C2D`, `0x00311EF0`,
`0x003136D0` and `0x00313C0A`). `0x0030A880` hands the same list to the party list builder
([Enmity](../Enemy-AI-And-Gambits/enmity.md)).

`0x00235DD0` and `0x00237460` hand on an index their caller supplies, so they can ask for seats 4 to 8 of map 1 as
well; the other twenty-five ask for seats 0 to 3 only.

### The snapshot a menu takes

`0x00326BB0`, run when the menu tasks `0x00281AE0`¹ and `0x002D70F0`² open, records the active seats
once; bit `0x1` of `0x022C25A0` marks the snapshot as taken (`0x003278C0` reads it):

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00281B52` |
| ² | `0x002D73BC` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | For each seat 0 to 3 that map 1 holds (`0x00322C50(0x17, i)`, the byte at `[0x02EBF190] + 0x5A5A + 2i`) whose unit has first-byte bit `0x8`, the 48-byte record at `0x022C25B0 + 0x30 x i` gets the member's type at `+0` and `+1`, the unit id at `+4`, the position at `+0x10` and the angle at `+0x20`. | `0x002367A0`<br>`0x00265020`<br>`0x00265200` |
| 2 | `0x022C25A4` takes the leader selector `[0x02EBF190] + 0x5AA4`. `0x022C25A5` takes the controlled member's type, byte `+4` of the stats record `+0x698` of the unit that `0x003588B0` and `0x00263E30` give for the handle from `0x003590D0`, only while bit `0x10` of `0x02089340` is set; it takes the leader selector when that bit is clear, when a step gives null and when the type is `0xFF`. | `0x00326CC6`-`0x00326CD4`<br>`0x00326CDA`-`0x00326D26`<br>`0x00326D2C`-`0x00326D48` |

`0x00326D60`, from the menu close `0x00281E00`¹, reads the snapshot² and clears the mark when
it is done³. `0x00327360`, run by the area
initialisation `0x002342F0`⁴, clears the mark, sets `0x022C25A4` to `0xFF` and each record's type word to
`0xFFFF` and id to 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00281EA8` |
| ² | `0x00326D67` |
| ³ | `0x00327125` |
| ⁴ | `0x00234459` |

</details>

The records' member words and unit ids, seat 0's member word being the base `0x022C25B0`:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C25B4` | `u32` | 0 (zero-filled tail of `.data`) | seat 0's record `+4`: the unit id `+8` of the unit that held the member when the menu opened, 0 for an empty seat | `0x00326BB0`, 0 (`0x00326C0A`) and then the id (`0x00326CAC`, through `rsi + 3`); `0x00327360`, 0 (`0x00327369`) | `0x00326D60` (`0x00327110`, through `rsi + 3` from `0x022C25B1`) |
| `0x022C25E0` | `u16` | 0 (zero-filled tail of `.data`) | seat 1's record `+0`: the low byte is the member's type, `0xFF` for an empty seat; `0x022C25E1` holds the same type | `0x00326BB0`, the word `0xFFFF` (`0x00326C10`) and then the type byte (`0x00326C8C`, through `rsi - 1`); `0x00327360`, the word `0xFFFF` (`0x00327391`) | `0x00326D60`, a byte at a time as it walks the four records from `0x022C25B0` (`0x00326DFB`, `0x00326E11`, `0x00326F46`) |
| `0x022C25E4` | `u32` | 0 (zero-filled tail of `.data`) | seat 1's record `+4`: the unit id `+8` of the unit that held the member when the menu opened, 0 for an empty seat | `0x00326BB0`, 0 (`0x00326C19`) and then the id (`0x00326CAC`, through `rsi + 3`); `0x00327360`, 0 (`0x0032736F`) | `0x00326D60` (`0x00327110`, through `rsi + 3` from `0x022C25B1`) |
| `0x022C2610` | `u16` | 0 (zero-filled tail of `.data`) | seat 2's record `+0`: the low byte is the member's type, `0xFF` for an empty seat; `0x022C2611` holds the same type | `0x00326BB0`, the word `0xFFFF` (`0x00326C1F`) and then the type byte (`0x00326C8C`, through `rsi - 1`); `0x00327360`, the word `0xFFFF` (`0x0032739A`) | `0x00326D60`, a byte at a time as it walks the four records from `0x022C25B0` (`0x00326DFB`, `0x00326E11`, `0x00326F46`) |
| `0x022C2614` | `u32` | 0 (zero-filled tail of `.data`) | seat 2's record `+4`: the unit id `+8` of the unit that held the member when the menu opened, 0 for an empty seat | `0x00326BB0`, 0 (`0x00326C28`) and then the id (`0x00326CAC`, through `rsi + 3`); `0x00327360`, 0 (`0x00327375`) | `0x00326D60` (`0x00327110`, through `rsi + 3` from `0x022C25B1`) |
| `0x022C2640` | `u16` | 0 (zero-filled tail of `.data`) | seat 3's record `+0`: the low byte is the member's type, `0xFF` for an empty seat; `0x022C2641` holds the same type | `0x00326BB0`, the word `0xFFFF` (`0x00326C2E`) and then the type byte (`0x00326C8C`, through `rsi - 1`); `0x00327360`, the word `0xFFFF` (`0x003273A3`) | `0x00326D60`, a byte at a time as it walks the four records from `0x022C25B0` (`0x00326DFB`, `0x00326E11`, `0x00326F46`) |
| `0x022C2644` | `u32` | 0 (zero-filled tail of `.data`) | seat 3's record `+4`: the unit id `+8` of the unit that held the member when the menu opened, 0 for an empty seat | `0x00326BB0`, 0 (`0x00326C37`) and then the id (`0x00326CAC`, through `rsi + 3`); `0x00327360`, 0 (`0x0032737B`) | `0x00326D60` (`0x00327110`, through `rsi + 3` from `0x022C25B1`), which compares it with the id of the unit that now holds the member and passes both to `0x0024C600` (`0x00327117`) when they differ |

## Layouts

<details>
<summary>Show the memory layouts</summary>

The slot maps in the party block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[9]` | map0 | live party seats; low byte = selector, `0xFF` empty (`0x0031BAAA`) |
| `+0x12` | `u16[9]` | map1 | fighting party (`0x0031BA8B`, `0x0031B841`) |
| `+0x24` | `u16[9]` | map2 | battle command menu (`0x0031BA71`) |
| `+0x36` | `u16[9]` | map3 | gameplay (`0x0031BA57`) |
| `+0x48` | `u16[9]` | map4 | rebuilt copy (`0x0031BA3D`) |
| `+0x5A` | `u8[2]` | pad5A | `+0x5AA2`: written only with the whole block (the clear `0x002370D3`, the save image's clears, copies and file read) and read by no other instruction; nothing fixes its width |

The maps start at `[0x02EBF190] + 0x5A48`; the leader selector is the dword at `+0x5AA4`
([Party data](party-data.md)).

</details>

## State

<details>
<summary>Show the state it keeps</summary>

`0x0031BAC0(point, angle, seat, out)` places the member in a seat of map 1 around a point: the controlled member¹ stands on the point itself². The others take positions from a table
of 4 rows of 3 that `0x0031BAC0` builds on its stack³, the row being `0x022C2670` less 2, or 3
when `0x003135C0` answers non-zero⁴; with fewer than two standing members it places nobody⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003272F0` |
| ² | `0x0031BBF6`-`0x0031BBFD`, `0x0031BD18` |
| ³ | `0x0031BAEF`-`0x0031BB9B` |
| ⁴ | `0x0031BBDA`-`0x0031BBF2` |
| ⁵ | `0x0031BC51` |

</details>

Two more cases stand on the point¹: a seat with no
member record (`0x00322C50(0x17, seat)` fails or the seat byte is above `0x27`), and a
member whose record dwords `+0x64` and `+0x3C` together have a bit of `0x80000003` set
while `0x00313F60()` answers 0. The record is `[0x02EBF190] + 8 + 0x1C8 × type`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031BC03`-`0x0031BC20`, `0x0031BD18` |
| ² | `0x0031BBA0`-`0x0031BBCB` |

</details>

`0x0031BAC0` answers 1 when it wrote a position and 0 when it placed nobody¹: with fewer than two standing members². It also
repeats the `0x00322C50(0x17, seat)` call and tests the seat byte for `0xFF`³, but both are reached only after the first call passed and the
byte was `0x27` or less.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031BD14`, `0x0031BD20` |
| ² | `0x0031BC51`-`0x0031BC58` |
| ³ | `0x0031BC2F`-`0x0031BC4B` |

</details>

The member takes entry `row * 3 + position` of the table, the position being `0x022C2674`. Each entry is an x and z
offset from the point (`0x00D10830`-`0x00D10890` and zeros, `0x0031BAEF`-`0x0031BB9B`; x and z read at `0x0031BC94` and
`0x0031BC8E`):

| Row | When | Position 0 | Position 1 | Position 2 |
|---:|---|---|---|---|
| 0 | 2 standing members | (0.6, -2.2) | (0, 0) | (0, 0) |
| 1 | 3 standing members | (-0.8, -1.2) | (0.8, -1.2) | (0, 0) |
| 2 | 4 standing members | (-1.0, -1.2) | (1.0, -1.2) | (0.6, -2.2) |
| 3 | `0x003135C0` non-zero (party control mode 1) | (1.8, 2.0) | (0, 0.2) | (0, 0) |

The offset is turned by the angle `a`, which `0x00325E60` brings into -π to π. With `t = a / 2π × 32768`, the sine
is sample `t & 0x7FFF` of the sine table `0x01F004E0` and the cosine sample `(t + 0x2000) & 0x7FFF`; the member
stands at `x = point.x + dx × cos + dz × sin` and `z = point.z + dz × cos - dx × sin`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031BC75`-`0x0031BD0D` |

</details>

Its height `out + 4` is copied from the float at `rsp + 0x24` of the function's frame, which `0x0031BAC0` does not
write¹. `0x0037D000` calls it for seats 0 to 3 after
`0x0031BD60`², and so does `0x0037B4D0`³, which places the party at a field start.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031BCF0` |
| ² | `0x0037D029`-`0x0037D09D` |
| ³ | `0x0037BFA6` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2674` | `i32` | 0 | which position in the row the next placed member takes; each member placed takes the next | `0x0031BAC0`, 1 more (`0x0031BCD9`); `0x0031BD60`, 0 (`0x0031BD64`), from `0x0037D000` (`0x0037D029`), the area teardown reset `0x002341C0` (`0x002341DF`) and the area initialisation `0x002342F0` (`0x00234454`); `0x003266C0`, 0 (`0x00326B39`) | `0x0031BAC0` (`0x0031BC5E`) |

No other instruction reaches `0x022C2674`.

</details>

## Modding notes

- The new-game party is the nine bytes at `0x01EED260`; changing the first byte changes who starts and who leads.
- Code that walks the fighting party reads map 1, so a member seated in map 0 joins the fight only after
  `0x003266C0` runs.

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member stats records a seat points at.
- [Party control modes](../Engine-Core/party-control-modes.md) - the summon,
  chocobo, town and event modes.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe tests over maps 1 and 3.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md) - the fighting party an enemy can notice.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 6 calls with 5 other topics</summary>

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031BD60`](party-slots.md) | is called by | [`0x002341C0`](../World-Areas-And-Travel/traps.md) (on traps) |

**Steam and achievements** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) | is called by | [`0x003160C0`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) | calls | [`0x002EF2B0`](../Saving-Loading-And-Settings/save-data-fields.md) (on save data fields) |
| [`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |

**Combat** (explained on [battle units](../Characters-And-Objects/battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x003206E0`](../Characters-And-Objects/battle-units.md) (on battle units) |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00313A00`](../Battle-Actions/action-phases.md) (on action phases) |

</details>

---

[← Party members and guests](party-members.md) | [Party leader →](party-leader.md)
