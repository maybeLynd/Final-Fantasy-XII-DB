---
title: "Party slots: the nine seats, the five slot maps the game reads them through, and how a seat reaches its battle unit"
kind: "system"
category: "Party"
addresses: "0031B9F0, 0031B810, 00320AB0, 00329CC0, 003266C0, 0030D9A0"
---

## What the player sees

The party menu shows four fighting members and up to five in reserve. During a summon only the summoner and
the Esper fight, on a chocobo only the rider, in a town only the leader walks, and some story scenes fix who
is in the party; afterwards the party is as it was.

## How it works

### The nine seats

The party lives in the battle state block `[02EBF190]` as five slot maps of nine two-byte seats each, `12`<sub>h</sub>
bytes apart (`0031BA3D`-`0031BAAA`):

| Map | Offset | Read by |
|---:|---|---|
| 0 | `+5A48`<sub>h</sub> | the live party: the menu, joining and leaving, unequipping (`0030FD10`, `00273880`) |
| 1 | `+5A5A`<sub>h</sub> | the fight: `0031B810` and everything that walks the four fighting members |
| 2 | `+5A6C`<sub>h</sub> | the battle command menu (`0035BC50` at `0035BDB9`) |
| 3 | `+5A7E`<sub>h</sub> | the rest of the game: equipment, rewards, targets, scripts, mostly through `00320AB0` |
| 4 | `+5A90`<sub>h</sub> | the members' field actors and the chocobo mount: `0031C470` and `00320230` (for `0035A490`, `0035AD40`), `0031C0F0`, `0031C250`, and `0031B950`, the map-4 twin of `0031B810` (for `00304060`, `00304140`) |

Seats 0-3 are the active members and seats 4-8 the reserve. The low byte of a seat is the member's selector,
the row of the party table and of the forty member records; `FF`<sub>h</sub> is an empty seat. The leader's selector is
kept at `+5AA4`<sub>h</sub>.

### Reading a seat

`0031B9F0(seat, map)` returns the low byte of a seat (`0031B9F0`-`0031BAB7`):

1. The seat must pass the class-23 id check, 0 to 8 (`0031BA04`-`0031BA0F`;
   [Item and ability ids](../Engine-Core/item-and-ability-ids.md)).
2. The map picks the offset; any map above 4 returns `FF`<sub>h</sub> (`0031BA1E`-`0031BA34`).

These turn the selector into a record or a unit:

- `00320AB0(seat, map)` returns the member's stats record, `[02EBF190] + 8 + selector * 1C8h`, or 0 for a
  selector above 39 ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md); `00320AB4`-`00320AD9`);
- `0031B810(seat)` reads map 1 directly and returns the battle unit with that selector (`0031B81C`-`0031B851`,
  `002367A0`);
- `0031FE70` and `00320040` take the map first and pass the stats record on to `00329220`
  (`0031FE7A`-`0031FEBA`, `0032004A`-`0032008D`);
- `0030A6E0` reads map 1 for a mask of the fighting members by kind, main character, guest, Esper or chocobo,
  leaving out members who are down.

Besides the new-game fill below, map 0's seats are written by `00329080` (`00329122`, `00329176`) when a member
joins or leaves ([Party members](party-members.md)).

### A new game's party

`00329CC0` fills map 0 from the nine bytes at `01EED260`, `00` then eight `FF` (`00329CF0`-`00329DAE`):

1. A selector is seated and its record activated with `00316DF0` (`00329D53`-`00329D9E`).
2. An empty byte empties the seat, deactivating the record that was there with `00323540`
   (`00329D0D`-`00329D51`).
3. The first byte becomes the leader `+5AA4`<sub>h</sub>, and `00326500` asks for the default controlled member
   (`00329DBB`-`00329DC8`).
4. Maps 1-4 become copies of map 0 (`00329DE3`-`00329E27`).

### Rebuilding the copies

`003266C0` rebuilds maps 1-4 from map 0 (`003266C0`-`00326B97`). It first makes maps 1 and 3 copies of map 0,
empties the reserve of map 1, and makes maps 2 and 4 copies of map 1, after saving map 4
(`003266F4`-`0032674B`). Then it adjusts the four active seats by the battle mode `0030D9A0`
([Battle mode](../Engine-Core/party-control-modes.md)):

| Mode | Seats 0-3 of maps 1, 2 and 4 | Sites |
|---|---|---|
| 0, normal, or any other value | as copied | - |
| 1, summon | seat 3 holds the Esper (`003137E0`), the summoner's seat (`00313800`) is kept, the others are emptied | `003269D2`-`00326A32` |
| 2, chocobo | seat 3 of maps 1 and 4 holds party row 26, the chocobo, and the other seats of map 1 are emptied; map 2 keeps only the rider's seat (`00327200`) | `00326991`-`003269D0` |
| 3, town | map 4 is restored; the area's leader (`00377C70`) fills its seat of maps 1, 2 and 4, or seat 3, and the other seats of maps 1 and 2 are emptied | `003268F3`-`0032698C` |
| 4, event party | only the leader's seat is kept, in maps 1, 2 and 4 | `0032683F`-`003268EE` |
| 5, second event party | map 4 is restored; only the leader's seat is kept, in maps 1 and 2 | `00326783`-`0032683A` |

In modes 4 and 5 the leader is `+5AA4`<sub>h</sub>, or with the area's town bit the area's leader at the controlled
member's seat (`003267B7`-`003267E8`, `0032686E`-`0032689F`).

Then, for each active seat whose battle unit holds a different member than map 1 now says, the unit is given
the new member (`0023A570`); a unit that changes member while down is torn down first (`00326A40`-`00326B18`). At
the end `00326500` picks the controlled member and `022C2670` counts the fighting members that are standing
(`00326B1E`-`00326B97`).

## Layouts

The slot maps in the battle state block:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u16[9]` | map0 | live party seats; low byte = selector, `FF`<sub>h</sub> empty (`0031BAAA`) |
| `12`<sub>h</sub> | `u16[9]` | map1 | fighting party (`0031BA8B`, `0031B841`) |
| `24`<sub>h</sub> | `u16[9]` | map2 | battle command menu (`0031BA71`) |
| `36`<sub>h</sub> | `u16[9]` | map3 | gameplay (`0031BA57`) |
| `48`<sub>h</sub> | `u16[9]` | map4 | rebuilt copy (`0031BA3D`) |

The maps start at `[02EBF190] + 5A48h`; the leader is the dword at `+5AA4`<sub>h</sub>
([Party data](party-data.md)).

## Modding notes

- The new-game party is the nine bytes at `01EED260`; changing the first byte changes who starts and who leads.
- Code that walks the fighting party reads map 1, so a member seated in map 0 joins the fight only after
  `003266C0` runs.

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member records a seat points at.
- [Battle mode](../Engine-Core/party-control-modes.md) - the summon,
  chocobo, town and event modes.
- [KO and Game Over](../Status-Effects-And-KO/ko-and-game-over.md) - the wipe tests over maps 1 and 3.
- [Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md) - the fighting party an enemy can notice.
