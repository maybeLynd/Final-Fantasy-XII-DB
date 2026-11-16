---
title: "Quickenings and summons: the one-at-a-time scene for summons, Esper attacks, Quickenings and chocobo mounting"
kind: "system"
category: "Battle actions"
addresses: "0x0030CE10, 0x00306BD0, 0x00306B10, 0x00306760, 0x003065D0, 0x00306570, 0x00306BB0"
---

## What the player sees

Some actions take over the screen with a scene of their own: summoning an Esper (Belias to Zodiark),
Dismiss, each Esper's finishing attack (Hellfire, Frostwave, Judgment Bolt, Gaia's Wrath, Blight,
Tsunami, Condemnation, Soul Purge, Tornado, Big Bang, Meteor, Eschaton, Final Eclipse), the
Quickenings, the Concurrences, and mounting and dismounting a chocobo.

- **One at a time.** There is a single scene for all of them. A unit whose action needs it while
  another is running waits and tries again every frame until the first one has ended.
- **The battle pauses around it.** While the scene plays, the battle units' animation events (hits,
  reactions, ends of actions) are passed over under two different conditions: an actor's timeline events
  while the scene plays or is being closed, for a unit without flag bit `0x2`, and an action's timeline
  events while the scene plays ([What pauses](#what-pauses)).
- **Quickenings during a scene.** A Quickening or Concurrence that comes while a scene is playing
  does not start a scene of its own; it goes ahead without one.
- **Esper attacks.** The results of an Esper's finishing attack are worked out when its scene
  starts, and its enmity is applied then too; the HP changes are applied when the scene ends.
- **Targets stay valid.** While a scene plays, the controlled character's current target always
  counts as a valid target.

Which actions get a scene is one flag in each action's row of `battle_pack.bin`, and the scene plays on scene manager
3, the same one script cutscenes use. During a Quickening chain, the script commands `getspattackskillinfo` and
`spattackplay` read the Quickening the chain reported and run each chain step.

## How it works

### Which actions

An action whose row has bit `0x40000000` of the flag word `+0x0C` goes through
`0x0030CE10`. In the shipped `battle_pack.bin` 87 rows have it: Mount and Dismount (ids `0x94`, `0x95`),
the 13 Esper finishing attacks among `0xB6`-`0xCF`, the 18 Quickenings `0xD0`-`0xE1`, the
Concurrences and unused rows `0xE2`-`0xF1`, the 13 summons `0x106`-`0x112`, Dismiss `0x113`, and
rows named Reserve from 511 on (names from the action-name table of `battle_pack.bin`).

### Asking for the scene

The per-frame presentation step `0x0030CBE0` (run from `0x00234590` at `0x002346F4`) calls
`0x0030CE10(unit, row)` for a pending entry (`0x0030CD99`). `0x0030CE10` returns -1 when the row lacks bit
`0x40000000`, or when the id is in `0xD0`-`0xF1` while the state `0x022C2160` is 5 or 6. Otherwise it clears unit
bit `0x20000000`, calls `0x00306BD0`, sets bit `0x20000000` on success and returns it (`0x0030CEF2`-`0x0030CF0D`).

| `0x0030CE10` returns | The entry |
|---:|---|
| -1 | moves to its state 3 without the scene-granted bit `0x1` of `+0x2C` (`0x0030CDB1`) |
| 0 | stays in its state 1 and is asked again on the next orchestrator frame |
| 1 | moves to state 2; once `0x00306B10` returns 1 (or at once for a unit without bit `0x20000000`) it gets bit `0x1` of `+0x2C` and moves to state 3 (`0x0030CD9E`-`0x0030CDD8`) |

### The stages (state `0x022C2160`, owner `0x022C2168`, kind `0x022C215C`)

The scene moves through these stages:


| State | Set by | Meaning |
|---|---|---|
| `0` | `0x003065D0`, `0x00306570` | idle |
| `1` | `0x00306BD0` (`0x00306C11`) | claimed: owner stored; stays here while scene manager 3 is busy (`0x0032F6E0(3)` non-zero), and only the same owner may claim again |
| `2` | `0x00306BD0` (`0x00306C40`) | loading: `0x00309230(unit, row)`, `0x0032FC30(3)`, `0x0032ED70(3)`, and the kind set from the id |
| `3` | `0x00306B10` (`0x00306B58`) | loaded: once `0x0032F6C0(3)` returns 0, bit `0x1` of `0x022C2158` is cleared and `0x0023B020` schedules the one-shot callback `0x00306560` with the unit's id |
| `4` | `0x00306B10` | ready: the callback (run by `0x00234520` on a later tick) has set bit `0x1` of `0x022C2158`; `0x00306B10` returns 1 |
| `5` | `0x00306760` (`0x00306ADF`) | playing |
| `6`, `7` | `0x003065D0` | ending (both set within one call) |

`0x00306B10(unit)` returns -1 for a unit that is not the owner and for the owner outside states 2-4,
0 while waiting, 1 in state 4. States 6 and 7 are set and left within one `0x003065D0` call, and the
state returns to 0 in that same call when scene manager 3 is already idle.

### The kind (`0x00306BD0`, by action id)

Mount 5, Dismount 6, `0xB6`-`0xCF` 3 (Esper attacks),
`0xD0`-`0xE1` 4 (Quickenings), `0x106`-`0x112` 1 (summons), `0x113` 2 (Dismiss), anything else 7.

### Playing

The standard-action state machine `0x00304850`, for a row with bit `0x40000000`, calls
`0x00306760(unit, row)` in place of the usual presentation event, after the target previews
(`0x00303830`) and the resource payment (`0x00305640`) - except for ids `0xD0`-`0xF1`, the Quickenings and
Concurrences, which skip both (`0x00304F00`-`0x00304F4D`). `0x00306760` moves the unit's presentation slot `+0x694`
to `+0x695` when free, posts `0x003299B0(unit, 0x003098D0(), 0)` when row byte `+0x1C` is 8, then by kind:

- **1 (summon):** sets bit `0x1` of `[0x02EBF190]+0x5B04` (calling `0x0035C620` when it changes); stores the
  summoner's type id at `+0x5AD5` and row byte `+0x26` (the Esper's stats index) at `+0x5AD4`; calls
  `0x00327810(unit)`; stores `(float)0x002FA0E0(summoner stats, +0x26)` at `+0x5AD8` and `+0x5ADC`; calls
  `0x0030C470(Esper stats, summoner stats byte +0x1C2, 0)`.
- **2 (Dismiss):** calls `0x00290740(0)` when bit `0x1` of `+0x5AD0` is set, `0x00306D90(0, unit id, +0x5AD4)`,
  and clears bit `0x1` of `+0x5B04` (calling `0x0035C620`).
- **3 (Esper attack):** `0x00306D90(target list, unit id, +0x5AD4)`, clears the deferred-HP list at
  `0x022C1F50`, calls `0x0030EC00(unit, action id)` and sets `0x022BE970` to 1.
- **4 (Quickening):** `0x00306D90(target list, 0, 0)`, clears `0x022C1F50`, calls `0x0030D720` and
  `0x0030D550`, moves the slot `+0x695` to `+0x696` when free, stores the unit id at `0x022C218C`, the
  Quickening index (id - `0xD0`) at `0x022C2178`, and copies the target list's units to `0x022C21B8`
  (count `0x022C21B4`).
- **5 (Mount):** sets bit `0x2` of `+0x5B04`, `+0x5AE0 |= 0xC` and `+0x5AE4` = 180.0 once.
- **6 (Dismount):** `0x00303D90(0)`.

Then it clears bits `0x100` and `0x200` of every battle unit's flags, starts scene manager 3 (`0x00332130(3)`) and
sets state 5 (`0x00306ADF`).

`0x00306D90(list, unit id, b)`, called for kinds 2 to 4 above, gathers the targets for `0x003B6F70`, a jump to `0x003B6DE0`.
For a non-null list it walks the signed count `+0x04` of 16-byte entries from `+0x08` and keeps, in a local array, the
dword `+0x08` of each non-null `0x0031B760(entry qword +0x00)` (`0x00306DC5`-`0x00306E09`). It then calls
`0x003B6F70(unit id, kept count, array, b as a byte)`, with a null array and a count of 0 for a null list
(`0x00306E23`-`0x00306E39`).

### The chain's choices (`0x002F88B0`)

During a Quickening chain, `0x00309C40` gives each member a set of choices and draws one of them for the member.

`0x0030D600` picks the members in two passes. The first keeps the party slots 0 to 3 (`0x0031B810`) whose unit has a
combat stats record with `+0x05` 0 and a party-table row `+0x04` of at most 6 (Vaan to Reks, the main characters;
guests from row 7 are left out). A record with any of the status bits `0x80000003` in `+0x64 | +0x3C` is kept
only when `0x00377C20` passes it (`0x0030D634`-`0x0030D693`, the list at `0x022C1788`).

The second pass keeps those whose `+0x64 | +0x3C` holds none of the bits `0x8800203B` and whose licence count
`0x00324020` is above 0, in the list at `0x022C24C0` (`0x0030D6B0`-`0x0030D6EA`). That list and its count are what
`0x00309C40` hands to `0x002F88B0` (`0x00309C6B`-`0x00309C8C`), so `L` below is at least 1 for every member.

For each member, `0x002F88B0` reads the licence count `L` (`0x00324020`) and the member's three Quickening slots, the
`u8[3]` at `+0x04` of its party table row.

1. When the member's MP bars `+0x37` are above its charges `+0x4E`, Mist Charge (action 244) is offered first,
   then the `L` Quickenings (`0x002F895A`-`0x002F8A0F`). The draw is Mist Charge when `rand() % (n + 5)` is 0, `n`
   being the number of members (`0x002F8A14`-`0x002F8A2A`).
2. Otherwise only the `L` Quickenings are offered (`0x002F8A86`-`0x002F8B22`).
3. Whenever Mist Charge is not drawn, the choice is slot `rand() % L` (`0x002F8B43`-`0x002F8B59`).

With three members and Mist Charge offered, Mist Charge is drawn 1 time in 8, and each of the `L` Quickenings
`7 / (8 × L)` of the time. Without Mist Charge each Quickening is drawn `1 / L` of the time.

These shares are nominal. `rand` is the C runtime's (import `0x008C3098`) and returns 0 to 32,767, so `% 8`, `% 2` and
`% 1` divide its range evenly, while `% 3` gives remainders 0 and 1 a share of 10,923 in 32,768 and remainder 2 a
share of 10,922.

`0x002F88B0` also finds the largest `L` among the members first, but the value is dropped before it is read
(`0x002F88E0`-`0x002F891E`, `0x002F8977`, `0x002F8A94`).

`0x002F88B0(members, n, chain count, entries)` writes one 16-byte entry per member into `entries`, in member order
(`0x002F8B5D`-`0x002F8B69`), and returns 1; for an `n` of 0 or below it returns 1 having written nothing
(`0x002F88C0`-`0x002F88CD`, `0x002F8920`-`0x002F8923`, `0x002F8B79`). The word `+0x00` is the drawn action and the dword `+0x04`
the number offered: `L + 1` with Mist Charge (`0x002F8975`-`0x002F8979`) and `L` without (`0x002F8A96`). With Mist Charge
the word `+0x08` is `0xF4` and the `L` slot bytes follow as words from `+0x0A` (`0x002F897D`, `0x002F8A09`); without it
they start at `+0x08` (`0x002F8B1D`).

`L` is `0x00324020(stats)` of the member's stats record `[unit + 0x698]`, or 0 for a null record (`0x002F88E3`-`0x002F88F6`,
read the same way each time, the last at `0x002F8B29`-`0x002F8B41`); in the second walk the Mist Charge test reads that
record's bytes `+0x37` and `+0x4E` before that walk's null test (`0x002F895A`-`0x002F8967`). The slot bytes come from the
row `0x0020E600([0x02EBF130] dword +0x0C)` plus the record's byte `+0x04` times the table's word `+0x08`, in 32 bits
(`0x002F89AC`-`0x002F89F2`, `0x002F8A33`-`0x002F8A7F`, `0x002F8AC7`-`0x002F8B06`).

When `0x02EBF130` is 0 or `0x0020E600` answers 0, the row pointer is 0, so the slot reads are of the addresses from `0x4`
(`0x002F89F6`, `0x002F8B0A`, `0x002F8B27`).

`0x00309C40` keeps one 24-byte entry per member:

| Offset | Holds |
|---|---|
| `+0x00` | the unit's id (`0x00309D07`) |
| `+0x04` | the drawn choice (`0x00309D0A`) |
| `+0x06` | up to six offered choices (`0x00309D90`-`0x00309DAE`) |
| `+0x12` | how many were offered (`0x00309DB0`) |
| `+0x13` | the drawn action's charge cost, its row `+0x0A`, when its kind `+0x1E` is 5 or 6; else 0 (`0x00309D72`-`0x00309D85`) |
| `+0x14` | bit `0x1` set when that cost is above the member's charges `+0x4E` (`0x00309DB3`-`0x00309DCF`) |

A Quickening of level 1, 2 or 3 costs 1, 2 or 3 charges ([action list](action-list.md), rows 208-225); Mist Charge
costs none.

### Esper attack damage

`0x0030EC00(unit, id)` resolves the action against every target in the list
(`0x00385F60` into a local result), applies its enmity (`0x003216E0`), runs `0x00312170` and `0x00317670`, and adds the result's
`+0x24` to the slot of the target's index `+0xEA9` in the list at `0x022C1F50` (unit at `0x022C1F58 + i*16`,
value at `0x022C1F60 + i*16`; header = the attacker's stats) (`0x0030EC61`-`0x0030ED45`). The HP is written
only at the end.

### Ending

The frame orchestrator `0x00234590` calls `0x003065D0` every frame (`0x002346F9`). In state 5 or 6 with an
owner it runs these steps (`0x003065D6`-`0x00306716`):

1. While scene manager 3 is still running (`0x002671F0(3)` non-zero) it clears bit `0x1` of `0x022C2158` and
   returns.
2. The state becomes 6.
3. For kind 3 it sets `0x022BE970` to 0, calls `0x0017F5B0(0)`, applies each list entry with
   `0x00300530(target stats, value, attacker stats, 0)` and clears the list.
4. For kind 4 it calls `0x0030D810`, `0x0030EB10(1)` (the same HP application, plus `0x0030E360` with 4 and
   with 5 for each target), releases the slot `+0x696` and calls `0x0030D720`.
5. The state becomes 7. When manager 3 is idle the state, kind and owner are cleared, bits `0x3` of
   `0x022C2158` are cleared, and `0x00238A60()` and `0x00332190(3)` run.

`0x00306570(unit)` performs the same clear when manager 3 is idle (`0x002671F0(3)` returns 0) and the unit is null,
the owner `0x022C2168` is null, or the unit is the owner: bits `0x3` of `0x022C2158`, the kind and the state (the qword
at `0x022C215C`) and the owner are cleared, and `0x00238A60()` and `0x00332190(3)` run (`0x00306574`-`0x003065BD`). For any
other unit, or while manager 3 runs, it returns doing nothing (`0x00306588`, `0x00306596`).

It is called from `0x002341D0`, the area initialisation `0x00234397` and the slot release `0x0030CA14`; the first two give
it a null unit (`xor ecx, ecx`), and the slot release the unit `0x0031B7E0` finds for the slot's unit id, null when
it does not resolve.

### What pauses

`0x00306BB0` returns 1 in states 5 and 6, and `0x00306BA0` in state 5 only. While they do:

- the actor timeline handler `0x00319F50` treats every event of a battle unit without bit `0x2` as handled
  without processing it (`0x00319FAC`-`0x00319FB3`, `0x00306BB0`); for a unit with bit `0x2` it returns 0 before
  that test, in every state (`0x00319FA3`-`0x00319FA6`);
- the frame orchestrator skips its `0x002371B0`/`0x00237140` checks (`0x002345F8`, `0x00306BB0`);
- the action timeline handler `0x00325260` treats every event as handled without processing it
  (`0x00325290`, `0x00306BA0`);
- `0x003229E0`, the validity test for the controlled member's current target, returns 1 instead of
  asking `0x002FFA60` (`0x00322A3B`, `0x00306BB0`);
- the combo gate, which requires state 0 or 7, refuses ([Combos](combos.md)).

## State

| Global | Width | Meaning |
|---|---|---|
| `0x022C2160` | `u32` | stage, 0-7 |
| `0x022C2168` | `void*` | owner unit |
| `0x022C215C` | `u32` | kind, 1-7 |
| `0x022C2158` | `u32` | bit `0x1`: scene ready (set by `0x00306560`) |
| `0x022C1F50` | `u8[520]` | deferred HP list for Esper attacks and Quickenings |
| `0x022BE970` | `u32` | 1 while an Esper attack's scene plays |
| `0x022C2178` / `0x022C218C` | `u32` | Quickening index / its user's id |
| `0x022C21B4` / `0x022C21B8` | `u32` / `void*` | Quickening target count / the targets, one unit pointer per target from `0x022C21B8` on (`0x0030690D`) |

The Quickening chain also keeps one 4-byte entry per main character, party type 0-6, from `0x022C2196`: the character's
Mist pool (stats `+0x06`) when the Quickening starts, a `u16`, and at `+0x02` the Mist charges the character's
Quickenings in the chain have cost, a `u8`:

1. `0x0030D720` (from `0x003066EB` and `0x0030686D`) clears them and the three level
   counters `0x022C2192`-`0x022C2194` ([Concurrence list](concurrence-list.md)).
2. `0x0030D550` (from `0x00306872`) clears the
   entries again and stores each fighting member's pool (`0x0030D5BC`-`0x0030D5EF`).
3. The chain step `0x00313120` adds the
   cost `0x00308FF0` gives to the user's byte while it is below 3 (`0x00313314`-`0x00313333`).
4. When the chain ends,
   `0x0030D810` (from `0x003066C9`) changes each member's Mist pool by `saved - charges x max MP (stats +0x28) - current pool`
   through `0x00300BC0` (`0x0030D850`-`0x0030D889`).

`0x0030D720` makes these stores as well, every one unconditional: 4 to the dwords `0x022C2170` and `0x022C2174`
(`0x0030D74B`, `0x0030D745`), -1 to the Quickening index `0x022C2178` (`0x0030D722`), 0 to its user's id `0x022C218C`
and to the target count `0x022C21B4` (`0x0030D758`, `0x0030D75E`), 4.0 (`0x40800000`) to the floats `0x022C2184`
and `0x022C2188` (`0x0030D76E`, `0x0030D764`), 0 to the qword at `0x022C217C` (`0x0030D751`), and 0 over the `0x100`
bytes from `0x022C21B8` (`0x0030D780`-`0x0030D7A7`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C2194` | `u8` | 0 | the count of Quickenings used from the third slot | `0x0030D720`, 0 (`0x0030D738`); `0x00313120` (`0x003133A9`) | `0x00313120` (`0x0031339D`); `0x00305F10`, as part of the 8 bytes from `0x022C2190` (`0x00305F1A`); `0x002F8D60` through the address `0x0030DB70` passes (`0x0030DC4E`) |
| `0x022C2196` / `0x022C2198` | `u16` / `u8` | 0 | type 0's saved pool / charges | pool: `0x0030D550`, 0 (`0x0030D567`) and by type (`0x0030D5E7`); `0x0030D720`, 0 (`0x0030D7AF`); charges: `0x0030D550` (`0x0030D560`); `0x0030D720` (`0x0030D7A9`); `0x00313120` (`0x00313333`) | `0x0030D810` (`0x0030D871`, `0x0030D86B`); charges also `0x00313120` (`0x00313320`) |
| `0x022C219A` / `0x022C219C` | `u16` / `u8` | 0 | type 1's | as for type 0, the clears at `0x0030D574` / `0x0030D56E` and `0x0030D7BC` / `0x0030D7B6` | as for type 0 |
| `0x022C219E` / `0x022C21A0` | `u16` / `u8` | 0 | type 2's | the clears at `0x0030D581` / `0x0030D57B` and `0x0030D7C9` / `0x0030D7C3` | as for type 0 |
| `0x022C21A2` / `0x022C21A4` | `u16` / `u8` | 0 | type 3's | the clears at `0x0030D58E` / `0x0030D588` and `0x0030D7D6` / `0x0030D7D0` | as for type 0 |
| `0x022C21A6` / `0x022C21A8` | `u16` / `u8` | 0 | type 4's | the clears at `0x0030D59B` / `0x0030D595` and `0x0030D7E3` / `0x0030D7DD` | as for type 0 |
| `0x022C21AA` / `0x022C21AC` | `u16` / `u8` | 0 | type 5's | the clears at `0x0030D5A8` / `0x0030D5A2` and `0x0030D7F0` / `0x0030D7EA` | as for type 0 |
| `0x022C21AE` / `0x022C21B0` | `u16` / `u8` | 0 | type 6's | the clears at `0x0030D5B5` / `0x0030D5AF` and `0x0030D7FD` / `0x0030D7F7` | as for type 0 |

No other instruction reaches these cells. The block's addresses are taken by `0x0030D550`, `0x0030D810`, `0x0030DB70` and
`0x00313120` only.

The chain's choices and the script's Quickening scene keep three more words:

- `0x00309C40`, from `0x002D5EB0`, draws the chain's choices through `0x002F88B0` and then adds one to `0x022C217C`. It hands
  `0x022C217C + 1` to `0x002F88B0` in `r8d` (`0x00309C70`-`0x00309C8C`), but no instruction of `0x002F88B0` reads the incoming
  `r8d`: its only reads, `0x002F89EE` and `0x002F8B02`, follow loads of the record's byte `+0x04` into it (`0x002F89E5`,
  `0x002F8AF9`), so the count does not change the draw.
- `getspattackskillinfo(&unit, &action)` (`0x029A`, `0x00348330`) asks `0x00309C00` for the Quickening the chain reported.
  `0x00309C00(&user, &index)` answers 0 while `0x022C2178` is -1; else it writes that index and the user `0x022C218C`, each
  through a non-null pointer only, sets `0x022C2178` to -1 and answers 1 (`0x00309C00`-`0x00309C31`).
  Then, reported or not, the bridge copies the two script variables into a two-deep history (`0x0034838F`-`0x003483B3`).
- `spattackplay(n)` (`0x029D`, `0x003495A0`) runs the chain step `0x00313120(n)`. It then looks for `n` among the two
  users, newer first (`0x003495BC`-`0x003495DD`), and on a match stores that entry's index in `0x01EF9218`
  (`0x003495E8`-`0x003495F2`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022C217C` | `u32` | 0 | the choice draws since the last chain step | `0x00309C40`, plus 1 (`0x00309DF6`, `0x00309E2D`); `0x00313120`, 0 (`0x003133D2`, `ebp` 0 from `0x003132C1`); `0x0030D720`, 0 with the 8-byte store at `0x0030D751` | `0x00309C40` (`0x00309C70`) |
| `0x022C2180` | `u32` | 0 | the Quickenings the chain has played | `0x00313120`, plus 1 at each chain step (`0x003133AC`); `0x0030D720`, 0 with the 8-byte store at `0x0030D751` | `0x00305F10` (`0x00305F26`), which shows the last action's name through `0x002902D0` and passes it as the second argument (`0x00305FF3`), or `0xC8` when that action is a Concurrence row, `0xE2` to `0xF1` (`0x00305F2F`, `0x00305F37`, `0x00305F42`) |
| `0x01EF9208` | `i32` | -1 | the user of the previous `getspattackskillinfo` | `0x00348330` (`0x00348397`, the newer user `0x01EF920C`) | `0x003495A0` (`0x003495D0`, the second compare, through the address it forms at `0x003495C3`) |
| `0x01EF9210` | `i32` | -1 | the Quickening index of the previous `getspattackskillinfo` | `0x00348330` (`0x003483A3`, the newer index `0x01EF9214`) | `0x003495A0` (`0x003495EF`, for a match on `0x01EF9208`, through the address it forms at `0x003495E8`) |

## Modding notes

- The scene flag is bit `0x40000000` of an action row's word `+0x0C`; clearing it makes the action run as an
  ordinary one (no scene, no wait, no pause).
- The kind is chosen by action id in `0x00306BD0`, not by data, so a new action id only gets the summon,
  Esper-attack or Quickening behaviour inside those id ranges.

## Related

- [Combos](combos.md) - the combo gate that waits for the scene to finish.
- [Action commit](action-commit.md) - the commit that comes before the scene.
- [Area of effect](area-of-effect.md) - the target list the scene reads.
- [How a cutscene runs](../Scripts-And-Script-Commands/event-scenes.md) - scene
  manager 3 in script scenes.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x002D5EB0` calls `0x00271500`, `0x002716F0`; those functions are documented on
  [sound effects](../Sound-And-Music/sound-effects.md).
- Input: `0x002D5EB0` calls `0x00182DA0`, `0x001E0C10`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [player movement](../Movement-And-Pathfinding/player-movement.md).
