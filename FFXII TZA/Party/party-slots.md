---
title: "Party slots: the nine seats, the five slot maps the game reads them through, and how a seat reaches its battle unit"
kind: "system"
category: "Party"
addresses: "0x0031B9F0, 0x0031B810, 0x00320AB0, 0x00329CC0, 0x003266C0, 0x0030D9A0"
---

## What the player sees

The party menu shows four fighting members and up to five in reserve. During a summon only the summoner and
the Esper fight, on a chocobo only the rider, in a town only the leader walks, and some story scenes fix who
is in the party; afterwards the party is as it was.

## How it works

### The nine seats

The party lives in the battle state block `[0x02EBF190]` as five slot maps of nine two-byte seats each, `0x12`
bytes apart (`0x0031BA3D`-`0x0031BAAA`):

| Map | Offset | Read by |
|---:|---|---|
| 0 | `+0x5A48` | the live party: the menu, joining and leaving, unequipping (`0x0030FD10`, `0x00273880`) |
| 1 | `+0x5A5A` | the fight: `0x0031B810` and everything that walks the four fighting members |
| 2 | `+0x5A6C` | the battle command menu (`0x0035BC50` at `0x0035BDB9`) |
| 3 | `+0x5A7E` | the rest of the game: equipment, rewards, targets, scripts, mostly through `0x00320AB0` |
| 4 | `+0x5A90` | the members' field actors and the chocobo mount: `0x0031C470` and `0x00320230` (for `0x0035A490`, `0x0035AD40`), `0x0031C0F0`, `0x0031C250`, and `0x0031B950`, the map-4 twin of `0x0031B810` (for `0x00304060`, `0x00304140`) |

Seats 0-3 are the active members and seats 4-8 the reserve. The low byte of a seat is the member's selector,
the row of the party table and of the forty member records; `0xFF` is an empty seat. The leader's selector is
kept at `+0x5AA4`.

### Reading a seat

`0x0031B9F0(seat, map)` returns the low byte of a seat (`0x0031B9F0`-`0x0031BAB7`):

1. The seat must pass the class-23 id check, 0 to 8 (`0x0031BA04`-`0x0031BA0F`;
   [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
2. The map picks the offset; any map above 4 returns `0xFF` (`0x0031BA1E`-`0x0031BA34`).

These turn the selector into a record or a unit:

- `0x00320AB0(seat, map)` returns the member's stats record, `[0x02EBF190] + 8 + selector * 0x1C8`, or 0 for a
  selector above 39 ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md); `0x00320AB4`-`0x00320AD9`);
- `0x0031B810(seat)` reads map 1 directly and returns the battle unit with that selector (`0x0031B81C`-`0x0031B851`,
  `0x002367A0`);
- `0x0031FE70` and `0x00320040` take the map first and pass the stats record on to `0x00329220`
  (`0x0031FE7A`-`0x0031FEBA`, `0x0032004A`-`0x0032008D`);
- `0x0030A6E0` reads map 1 for a mask of the fighting members by kind, main character, guest, Esper or chocobo,
  leaving out members who are down.

Besides the new-game fill below, map 0's seats are written by `0x00329080` (`0x00329122`, `0x00329176`) when a member
joins or leaves ([Party members](party-members.md)).

### A new game's party

`0x00329CC0` fills map 0 from the nine bytes at `0x01EED260`, `00` then eight `FF` (`0x00329CF0`-`0x00329DAE`):

1. A selector is seated and its record activated with `0x00316DF0` (`0x00329D53`-`0x00329D9E`).
2. An empty byte empties the seat, deactivating the record that was there with `0x00323540`
   (`0x00329D0D`-`0x00329D51`).
3. The first byte becomes the leader `+0x5AA4`, and `0x00326500` asks for the default controlled member
   (`0x00329DBB`-`0x00329DC8`).
4. Maps 1-4 become copies of map 0 (`0x00329DE3`-`0x00329E27`).

### Rebuilding the copies

`0x003266C0` rebuilds maps 1-4 from map 0 (`0x003266C0`-`0x00326B97`). It first makes maps 1 and 3 copies of map 0,
empties the reserve of map 1, and makes maps 2 and 4 copies of map 1, after saving map 4
(`0x003266F4`-`0x0032674B`). Then it adjusts the four active seats by the battle mode `0x0030D9A0`
([Battle mode](../Engine-Core/party-control-modes.md)):

| Mode | Seats 0-3 of maps 1, 2 and 4 | Sites |
|---|---|---|
| 0, normal, or any other value | as copied | - |
| 1, summon | seat 3 holds the Esper (`0x003137E0`), the summoner's seat (`0x00313800`) is kept, the others are emptied | `0x003269D2`-`0x00326A32` |
| 2, chocobo | seat 3 of maps 1 and 4 holds party row 26, the chocobo, and the other seats of map 1 are emptied; map 2 keeps only the rider's seat (`0x00327200`) | `0x00326991`-`0x003269D0` |
| 3, town | map 4 is restored; the area's leader (`0x00377C70`) fills its seat of maps 1, 2 and 4, or seat 3, and the other seats of maps 1 and 2 are emptied | `0x003268F3`-`0x0032698C` |
| 4, event party | only the leader's seat is kept, in maps 1, 2 and 4 | `0x0032683F`-`0x003268EE` |
| 5, second event party | map 4 is restored; only the leader's seat is kept, in maps 1 and 2 | `0x00326783`-`0x0032683A` |

In modes 4 and 5 the leader is `+0x5AA4`, or with the area's town bit the area's leader at the controlled
member's seat (`0x003267B7`-`0x003267E8`, `0x0032686E`-`0x0032689F`).

Then, for each active seat whose battle unit holds a different member than map 1 now says, the unit is given
the new member (`0x0023A570`); a unit that changes member while down is torn down first (`0x00326A40`-`0x00326B18`). At
the end `0x00326500` picks the controlled member and `0x022C2670` counts the fighting members that are standing
(`0x00326B1E`-`0x00326B97`).

### The snapshot a menu takes

`0x00326BB0`, run when the menu tasks `0x00281AE0` (`0x00281B52`) and `0x002D70F0` (`0x002D73BC`) open, records the active seats
once; bit `0x1` of `0x022C25A0` marks the snapshot as taken (`0x003278C0` reads it):

1. For each seat 0 to 3 that map 1 holds (`0x00322C50(0x17, i)`, the byte at `[0x02EBF190] + 0x5A5A + 2i`) whose unit
   (`0x002367A0`) has first-byte bit `0x8`, the 48-byte record at `0x022C25B0 + 0x30 x i` gets the member's type at `+0` and
   `+1`, the unit id at `+4`, the position at `+0x10` (`0x00265020`) and the angle at `+0x20` (`0x00265200`).
2. `0x022C25A4` takes the saved leader `[0x02EBF190] + 0x5AA4`, and `0x022C25A5` the controlled member's type (`0x003590D0`),
   or the saved leader when there is none.

`0x00326D60`, from the menu close `0x00281E00` (`0x00281EA8`), reads the snapshot (`0x00326D67`) and clears the mark when
it is done (`0x00327125`). `0x00327360`, run by the area
initialisation `0x002342F0` (`0x00234459`), clears the mark, sets `0x022C25A4` to `0xFF` and each record's type word to
`0xFFFF` and id to 0.

Seat 2's member word and seat 3's unit id, two of the record words above:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2610` | `u16` | 0 (zero-filled tail of `.data`) | seat 2's record `+0`: the low byte is the member's type, `0xFF` for an empty seat; `0x022C2611` holds the same type | `0x00326BB0`, the word `0xFFFF` (`0x00326C1F`) and then the type byte (`0x00326C8C`, through `rsi - 1`); `0x00327360`, the word `0xFFFF` (`0x0032739A`) | `0x00326D60`, a byte at a time as it walks the four records from `0x022C25B0` (`0x00326DFB`, `0x00326E11`, `0x00326F46`) |
| `0x022C2644` | `u32` | 0 (zero-filled tail of `.data`) | seat 3's record `+4`: the unit id `+8` of the unit that held the member when the menu opened, 0 for an empty seat | `0x00326BB0`, 0 (`0x00326C37`) and then the id (`0x00326CAC`, through `rsi + 3`); `0x00327360`, 0 (`0x0032737B`) | `0x00326D60` (`0x00327110`, through `rsi + 3` from `0x022C25B1`), which compares it with the id of the unit that now holds the member and passes both to `0x0024C600` (`0x00327117`) when they differ |

## Layouts

The slot maps in the battle state block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[9]` | map0 | live party seats; low byte = selector, `0xFF` empty (`0x0031BAAA`) |
| `+0x12` | `u16[9]` | map1 | fighting party (`0x0031BA8B`, `0x0031B841`) |
| `+0x24` | `u16[9]` | map2 | battle command menu (`0x0031BA71`) |
| `+0x36` | `u16[9]` | map3 | gameplay (`0x0031BA57`) |
| `+0x48` | `u16[9]` | map4 | rebuilt copy (`0x0031BA3D`) |
| `+0x5A` | `u8[2]` | pad5A | `+0x5AA2`: written only with the whole block (the clear `0x002370D3`, the save image's clears, copies and file read) and read by no other instruction; nothing fixes its width |

The maps start at `[0x02EBF190] + 0x5A48`; the leader is the dword at `+0x5AA4`
([Party data](party-data.md)).

## State

`0x0031BAC0(point, angle, seat, out)` places the member in a seat of map 1 around a point: the controlled member
(`0x003272F0`) stands on the point itself (`0x0031BBF6`-`0x0031BBFD`, `0x0031BD18`). The others take positions from a table
of 4 rows of 3 that `0x0031BAC0` builds on its stack (`0x0031BAEF`-`0x0031BB9B`), the row being `0x022C2670` less 2, or 3
when `0x003135C0` answers non-zero (`0x0031BBDA`-`0x0031BBF2`); with fewer than two standing members it places nobody
(`0x0031BC51`).

The position is turned by the angle (`0x0031BC75`-`0x0031BD0D`). `0x0037D000` calls it for seats 0 to 3 after
`0x0031BD60` (`0x0037D029`-`0x0037D09D`), and so does `0x0037B4D0` (`0x0037BFA6`), which places the party at a field start.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2674` | `i32` | 0 | which position in the row the next placed member takes; each member placed takes the next | `0x0031BAC0`, 1 more (`0x0031BCD9`); `0x0031BD60`, 0 (`0x0031BD64`), from `0x0037D000` (`0x0037D029`), the area teardown reset `0x002341C0` (`0x002341DF`) and the area initialisation `0x002342F0` (`0x00234454`); `0x003266C0`, 0 (`0x00326B39`) | `0x0031BAC0` (`0x0031BC5E`) |

No other instruction reaches `0x022C2674`.

## Modding notes

- The new-game party is the nine bytes at `0x01EED260`; changing the first byte changes who starts and who leads.
- Code that walks the fighting party reads map 1, so a member seated in map 0 joins the fight only after
  `0x003266C0` runs.

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member records a seat points at.
- [Battle mode](../Engine-Core/party-control-modes.md) - the summon,
  chocobo, town and event modes.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe tests over maps 1 and 3.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md) - the fighting party an enemy can notice.
