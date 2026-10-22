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
- **The battle pauses around it.** While the scene plays, the animation events of the battle units
  (hits, reactions, ends of actions) are not processed.
- **Quickenings during a scene.** A Quickening or Concurrence that comes while a scene is playing
  does not start a scene of its own; it goes ahead without one.
- **Esper attacks.** The results of an Esper's finishing attack are worked out when its scene
  starts, and its enmity is applied then too; the HP changes are applied when the scene ends.
- **Targets stay valid.** While a scene plays, the controlled character's current target always
  counts as a valid target.

## How it works

### Which actions

An action whose row has bit 30 (`0x40000000`) of the flag word `+0x0C` goes through
`0x0030CE10`. In the shipped `battle_pack.bin` 87 rows have it: Mount and Dismount (ids `0x94`, `0x95`),
the 13 Esper finishing attacks among `0xB6`-`0xCF`, the 18 Quickenings `0xD0`-`0xE1`, the
Concurrences and unused rows `0xE2`-`0xF1`, the 13 summons `0x106`-`0x112`, Dismiss `0x113`, and
rows named Reserve from 511 on (names from the action-name table of `battle_pack.bin`).

### Asking for the scene

The per-frame presentation step `0x0030CBE0` (run from `0x00234590` at `0x002346F4`) calls
`0x0030CE10(unit, row)` for a pending entry (`0x0030CD99`). `0x0030CE10` returns -1 when the row lacks bit
30, or when the id is in `0xD0`-`0xF1` while the state `0x022C2160` is 5 or 6. Otherwise it clears unit
bit 29, calls `0x00306BD0`, sets bit 29 on success and returns it (`0x0030CEF2`-`0x0030CF0D`).

| `0x0030CE10` returns | The entry |
|---:|---|
| -1 | moves to its state 3 without the scene-granted bit 0 of `+0x2C` (`0x0030CDB1`) |
| 0 | stays in its state 1 and is asked again on the next orchestrator frame |
| 1 | moves to state 2; once `0x00306B10` returns 1 (or at once for a unit without bit 29) it gets bit 0 of `+0x2C` and moves to state 3 (`0x0030CD9E`-`0x0030CDD8`) |

### The stages (state `0x022C2160`, owner `0x022C2168`, kind `0x022C215C`)

The scene moves through these stages:


| State | Set by | Meaning |
|---|---|---|
| `0` | `0x003065D0`, `0x00306570` | idle |
| `1` | `0x00306BD0` (`0x00306C11`) | claimed: owner stored; stays here while scene manager 3 is busy (`0x0032F6E0(3)` non-zero), and only the same owner may claim again |
| `2` | `0x00306BD0` (`0x00306C40`) | loading: `0x00309230(unit, row)`, `0x0032FC30(3)`, `0x0032ED70(3)`, and the kind set from the id |
| `3` | `0x00306B10` (`0x00306B58`) | loaded: once `0x0032F6C0(3)` returns 0, bit 0 of `0x022C2158` is cleared and `0x0023B020` schedules the one-shot callback `0x00306560` with the unit's id |
| `4` | `0x00306B10` | ready: the callback (run by `0x00234520` on a later tick) has set bit 0 of `0x022C2158`; `0x00306B10` returns 1 |
| `5` | `0x00306760` (`0x00306ADF`) | playing |
| `6`, `7` | `0x003065D0` | ending (both set within one call) |

`0x00306B10(unit)` returns -1 for a unit that is not the owner and for the owner outside states 2-4,
0 while waiting, 1 in state 4. States 6 and 7 are set and left within one `0x003065D0` call, and the
state returns to 0 in that same call when scene manager 3 is already idle.

### The kind (`0x00306BD0`, by action id)

Mount 5, Dismount 6, `0xB6`-`0xCF` 3 (Esper attacks),
`0xD0`-`0xE1` 4 (Quickenings), `0x106`-`0x112` 1 (summons), `0x113` 2 (Dismiss), anything else 7.

### Playing

The standard-action state machine `0x00304850`, for a row with bit 30, calls
`0x00306760(unit, row)` in place of the usual presentation event, after the target previews
(`0x00303830`) and the resource payment (`0x00305640`) - except for ids `0xD0`-`0xF1`, the Quickenings and
Concurrences, which skip both (`0x00304F00`-`0x00304F4D`). `0x00306760` moves the unit's presentation slot `+0x694`
to `+0x695` when free, posts `0x003299B0(unit, 0x003098D0(), 0)` when row byte `+0x1C` is 8, then by kind:

- **1 (summon):** sets bit 0 of `[0x02EBF190]+0x5B04` (calling `0x0035C620` when it changes); stores the
  summoner's type id at `+0x5AD5` and row byte `+0x26` (the Esper's stats index) at `+0x5AD4`; calls
  `0x00327810(unit)`; stores `(float)0x002FA0E0(summoner stats, +0x26)` at `+0x5AD8` and `+0x5ADC`; calls
  `0x0030C470(Esper stats, summoner stats byte +0x1C2, 0)`.
- **2 (Dismiss):** calls `0x00290740(0)` when bit 0 of `+0x5AD0` is set, `0x00306D90(0, unit id, +0x5AD4)`,
  and clears bit 0 of `+0x5B04` (calling `0x0035C620`).
- **3 (Esper attack):** `0x00306D90(target list, unit id, +0x5AD4)`, clears the deferred-HP list at
  `0x022C1F50`, calls `0x0030EC00(unit, action id)` and sets `0x022BE970` to 1.
- **4 (Quickening):** `0x00306D90(target list, 0, 0)`, clears `0x022C1F50`, calls `0x0030D720` and
  `0x0030D550`, moves the slot `+0x695` to `+0x696` when free, stores the unit id at `0x022C218C`, the
  Quickening index (id - `0xD0`) at `0x022C2178`, and copies the target list's units to `0x022C21B8`
  (count `0x022C21B4`).
- **5 (Mount):** sets bit 1 of `+0x5B04`, `+0x5AE0 |= 0xC` and `+0x5AE4` = 180.0 once.
- **6 (Dismount):** `0x00303D90(0)`.

Then it clears bits 8 and 9 of every battle unit's flags, starts scene manager 3 (`0x00332130(3)`) and
sets state 5 (`0x00306ADF`).

### Esper attack damage

`0x0030EC00(unit, id)` resolves the action against every target in the list
(`0x00385F60` into a local result), applies its enmity (`0x003216E0`), runs `0x00312170` and `0x00317670`, and adds the result's
`+0x24` to the slot of the target's index `+0xEA9` in the list at `0x022C1F50` (unit at `0x022C1F58 + i*16`,
value at `0x022C1F60 + i*16`; header = the attacker's stats) (`0x0030EC61`-`0x0030ED45`). The HP is written
only at the end.

### Ending

The frame orchestrator `0x00234590` calls `0x003065D0` every frame (`0x002346F9`). In state 5 or 6 with an
owner it runs these steps (`0x003065D6`-`0x00306716`):

1. While scene manager 3 is still running (`0x002671F0(3)` non-zero) it clears bit 0 of `0x022C2158` and
   returns.
2. The state becomes 6.
3. For kind 3 it sets `0x022BE970` to 0, calls `0x0017F5B0(0)`, applies each list entry with
   `0x00300530(target stats, value, attacker stats, 0)` and clears the list.
4. For kind 4 it calls `0x0030D810`, `0x0030EB10(1)` (the same HP application, plus `0x0030E360` with 4 and
   with 5 for each target), releases the slot `+0x696` and calls `0x0030D720`.
5. The state becomes 7. When manager 3 is idle the state, kind and owner are cleared, bits 0-1 of
   `0x022C2158` are cleared, and `0x00238A60()` and `0x00332190(3)` run.

`0x00306570(unit)` performs the same clear for the owner (or for no owner) when manager 3 is idle; it is
called from `0x002341D0`, the area initialisation `0x00234397` and the slot release `0x0030CA14`.

### What pauses

`0x00306BB0` returns 1 in states 5 and 6, and `0x00306BA0` in state 5 only. While they do:

- the actor timeline handler `0x00319F50` treats every event of a battle unit without bit 1 as handled
  without processing it (`0x00319FAC`-`0x00319FB3`, `0x00306BB0`);
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
| `0x022C2158` | `u32` | bit 0: scene ready (set by `0x00306560`) |
| `0x022C1F50` | `u8[520]` | deferred HP list for Esper attacks and Quickenings |
| `0x022BE970` | `u32` | 1 while an Esper attack's scene plays |
| `0x022C2178` / `0x022C218C` | `u32` | Quickening index / its user's id |
| `0x022C21B4` / `0x022C21B8` | `u32` / `void*` | Quickening target count / the targets, one unit pointer per target from `0x022C21B8` on (`0x0030690D`) |

## Modding notes

- The scene flag is bit 30 of an action row's word `+0x0C`; clearing it makes the action run as an
  ordinary one (no scene, no wait, no pause).
- The kind is chosen by action id in `0x00306BD0`, not by data, so a new action id only gets the summon,
  Esper-attack or Quickening behaviour inside those id ranges.

## Related

- [Combos](combos.md) - the combo gate that waits for the scene to finish.
- [Action commit](action-commit.md) - the commit that comes before the scene.
- [Area of effect](area-of-effect.md) - the target list the scene reads.
- [How a cutscene runs](../Scripts-And-Script-Commands/cutscenes-and-the-world-lock.md) - scene
  manager 3 in script scenes.
