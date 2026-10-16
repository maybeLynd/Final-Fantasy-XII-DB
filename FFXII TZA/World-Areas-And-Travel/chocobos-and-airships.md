---
title: "Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel"
kind: "system"
category: "World, areas and travel"
summary: "What riding a chocobo is to the engine: one mode bit in the battle-state block and one persistent flag, the three-minute ride timer and the turbo timer in the shared timer slots, the dismount task that fades, swaps the party back and clears the flag, the menu's Dismount command and the ground test behind it, the mode ladder that tells riding from the other modes, the music the ride selects, the verbs the keeper and crystal scripts use, how a save carries the riding bit, and airship travel, which has no verb of its own and is a gil charge, a scene and a map jump in the aerodrome scripts."
addresses: ["00303D90", "00303EE0", "00303EC0", "0030D9A0", "003135C0", "00303F00", "003514D0", "00347230", "00347820", "00347C60", "00356630", "00355910", "0033F650", "0050F8A0", "0037CFF0", "0037CFC0", "0037D100", "00304440", "00234590", "00303CC0", "00336390", "0017D380", "0017D3A0", "0031B8C0", "00311E20", "0035CFA0", "0035C960", "0035CA70", "003CA310", "003CA860", "00304680", "00304060", "00304140", "00237DF0", "0034EE20", "0034DD90", "0032AB60", "003EBA90", "003EBB70", "003EBC50", "003EBD00", "002E73C0", "002EB030", "00263750", "00306760", "005843E0", "002EF3C0", "002EF410", "00261F90", "002DEE50", "003611F0", "0026A7F0", "00342E50", "00265680", "001D50D0", "005C5230"]
---

# Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel

## What the player sees

At a chocobo keeper, or a wild chocobo, the player hands over Gysahl Greens, the screen fades and
the leader is riding, with the chocobo theme playing. The ride lasts three minutes; when the time
runs out the party is set down where it stands, and the player can also get off through the menu's
Dismount command, by touching a crystal, by boarding an airship or when a scene needs the party on
foot. The menu refuses to dismount where the chocobo has no room to stand.

At an aerodrome counter the player buys a ticket and chooses whether to watch the flight: the
party then either sees the departure scene and arrives at the other aerodrome, or spends the flight
on the airship's deck. Now and then a monster attacks the airship in flight.

## How it works

### The riding state

Riding is held in the battle-state block at `[02EBF190]` (the block's field map):

| Field | Meaning |
|---|---|
| `+0x5B04` bit 1 | riding |
| `+0x5AE0` bit 0 | the ride timer is running |
| `+0x5AE0` bit 1 | turbo is on |
| `+0x5AE0` bits 2-3 | turbo charges, 3 on mounting |
| `+0x5AE4` | f32, the ride time left in seconds; 180.0 on mounting |
| `+0x5AE8` | f32, the turbo time left in seconds |
| `+0x5AEC` | the last turbo argument |

`00303D90(on)` is the one setter and does nothing when bit 1 already equals `on`:

- `on`: `+0x5B04 |= 2`, `+0x5AE0 |= 0xC`, `+0x5AE4 = 180.0` (`0x43340000`);
- off: `+0x5B04 &= ~2`; the chocobo, the actor in roster entry 3 (`00263750(3)`), has its render
  record set to mode 3 (`002E73C0(actor, 3)`: `+0x294` bit 27 and the top five bits of `+0x304`);
  `+0x5AEC = 0`; when turbo was on, animation `0x2001` is requested on the chocobo (`002EB030`)
  and bit 1 of `+0x5AE0` is cleared.

Its callers are the verb thunks `0037CFF0` (on), `0037CFC0` (off) and `0037D100` (argument), the
full reset `00304680`, the dismount task `0035CA70` and the special presentation `00306760`, whose
kind 5 mounts (the same three stores) and kind 6 dismounts.

### Riding and the mode ladder

`0030D9A0` ranks the block's mode bits: `+0x5B04` bit 3 gives 5, bit 2 gives 4, the current area's
record bit 15 (`00377C20`, a town) gives 3, bit 1 gives 2, otherwise bit 0 gives 0 or 1. So
`getchocobomodebit` (`00303EE0`, the raw bit) and `getchocobomode` (`00303EC0`, ladder = 2) differ:
riding into a town, or while bit 2 or 3 is set, keeps the bit but leaves chocobo mode. `003135C0`
is ladder = 1.

The area music follows the ladder: the field music select `00261F90` plays track `0x5B` when the
ladder is 1 and track `0x5A`, the chocobo theme, when it is 2 (music);
the dismount task stops that track again.

### The verbs

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setchocobomode(v)` | `0x3EC` | `003514D0` → `0037D100` | `00303D90(v)` |
| `ridechocobo` | `0x37E` | Start `00347230` → `0037CFF0`, Poll `00347C60` | `00303D90(1)`; the Poll returns `005C5230() != 0`, always 0, so it ends on its first poll |
| `getoffchocobo` | `0x37F` | Start `00347820` → `0037CFC0`, Poll `00347C60` | `00303D90(0)`, the same Poll |
| `getchocobomodebit()` | `0x511` | `00356630` | `+0x5B04` bit 1 |
| `getchocobomode()` | `0x407` | `00355910` | ladder = 2 |
| `enable_by_chocobo(v)` | `0x40A` | `0033F650` | bit 0 of byte `+0x0B` of the calling actor = `v != 0` |
| `btlAtelSetChocoboTurboMode(v)` | `0x302F` | `0050F8A0` | `00303F00(v != 0)` |
| `setmapjumpgroupflag(id)` / `releasemapjumpgroupflag(id)` | `0x430` / `0x431` | `0034EE20` / `0034DD90` | `0032AB60(id, 1)` / `(id, 0)`: a primary persistent flag (persistent flag banks) |
| `setflystatus(v)` | `0x1E0` | `00342E50` → `0026A7F0` | bit 0 of the actor's secondary context `+0x151`, and `+0x152` 1 ↔ 2 |

No instruction in the image tests bit 0 of the actor byte `+0x0B` with an immediate mask; the byte
is cleared to its top two bits by the record initialiser and has bit 6 cleared by the movement
defaults ([actor record](../Characters-And-Objects/actor-record.md)).

### Mounting and dismounting in the scripts

The keeper scripts (`fon_a07` and the others) mount with `subitem(0x20D8, 1)` (Gysahl Greens),
`suspendbattle`, a fade, `setchocobomode(1); partyallread();`, the riding motion,
`setmapjumpgroupflag(115)`, a re-read of the map music (`musicplay(getnowmapmusicno_47a(0))`) and
`resumebattle`. The dismount routine every script shares (`sumcho_byebye`) is:

```
if (getchocobomodebit()) { setchocobomode(0); partyallread(); releasemapjumpgroupflag(115); }
```

So persistent flag 115 means "the party is riding" to the scripts, and both the script dismount
and the native one below clear it. The crystal and aerodrome scripts call it before a teleport or a
flight ([save and teleport crystals](save-and-teleport-crystals.md)).

### The ride timer and the turbo timer

The two countdowns live in the shared timer slots at `02B5EBC0`, 20 bytes each (Layouts):

- `003EBC50(slot, value, target)` loads a slot with a step of `1/60` (`0x3C889A05`) when
  `00290180()` is 2 and `1/50` (`0x3CA3D70A`) otherwise, negative when the target is at or below
  the value;
- `003EBD00(slot)` starts it, or marks it expired when value and target already agree;
- `003EBA90(slot)` reads the value and `003EBB70(slot)` the expired byte.

The values are therefore seconds counted at the frame rate: the ride is 180 seconds.

`00304440` runs every field frame from the tick's per-slot pre-pass `00234590` (`00234712`) while
`+0x5AE0` bit 0 is set:

1. `+0x5AE4` = slot 1's value, or 180.0 while the configuration byte `+0xE1D` of `[001D50D0()]`
   is set (`0017D380`); `+0x5AE8` = slot 2's value;
2. when `00303CC0()` allows a dismount, slot 1 has expired, that byte is clear, the ladder is 2
   and the chocobo (`0031B8C0(3)`, the unit of roster entry 3) exists: `00311E20()` refreshes the
   camera target and `0035CFA0(1)` starts the dismount task;
3. when slot 2 has expired and turbo is on: the chocobo's render mode is set to 3, `+0x5AEC` = 0,
   animation `0x2001` is requested and bit 1 is cleared.

Turbo (`00303F00(on)`) sets `+0x5AEC`, puts the chocobo's render record in mode 1 (on) or 3 (off)
and, when the bit changes: on requires ladder 2 and a non-zero charge count; it loads slot 2 with
`10 × [01DFE0B8]` seconds (the frame base, image value 1.0), spends one charge unless the
configuration byte `+0xE1E` (`0017D3A0`) is set, and requests animation `0x2010`; off requests
`0x2001`; either way bit 1 is toggled.

### Where a dismount is allowed

`00303CC0()` returns 1 only when the ladder is 2, the chocobo exists and `00336390(position,
radius, 0)` passes: the chocobo's position (`00265020`) and the four points `radius` away along
both axes all lie on walkable ground (`0026E100`), with `radius` the larger of the leader's two
`00265090` radii.

The menu's Dismount command uses the same test. Its dialog task `003CA310`, spawned by the party
menu task `003CA860` while chocobo mode is on, shows text `0x832` "Dismount" when the test passes
and `0x87C` "You cannot dismount here." when it does not, and on a confirmed `0x8100` result it
calls `0035CFA0(0)`.

### The dismount task

`0035CFA0(fromTimer)` spawns a `0xD0`-byte task on `0035C960` when the field is live (`00265680`)
and no dismount task is running (`022CA468` = 0). The handler's open step sets the state byte
`+0xC0` to 6, records the task in `022CA468` and, for a timer dismount, resets the battle menu
(`00252B40(0x14)`, `002E1C20(8)`); every later frame runs the state machine `0035CA70`:

| State | What it does | Next |
|---|---|---|
| 6 | fade out, 30 frames (`002EFA70(0, 0x1E, 0)`) | 8, then 1 |
| 8 | waits for the fade (`002EFD20(0)` = 1) | the stored next state |
| 1 | `0026C3C0(0)`, `00303D90(0)` (the dismount), `003CA1C0`, `003C58B0`, `003634B0(0xF)` | 9 |
| 9 | `002DEBE0(-1)` finds the music slot; `002DEE50(slot, 0x5A)` and `003611F0(0x5A)` stop the chocobo theme | 10, or 12 with no slot |
| 10 | waits for `002F1A30(1)` = 0, then `002DEDE0(slot)` | 11, or 12 for a negative slot |
| 11 | waits for `001DBBF0(slot)` = 0 | 12 |
| 12 | `00360D70` or `00360E50`; `0026DE00(0)` picks the field's track | 13 or 14, or 2 with no track |
| 13 / 14 | `00360C20(track)` = 5 restarts the field music (`002DEC00`, `002DECE0`); 14 retries `00361630(track)` | 2 |
| 2 | `00282F80`, `00283270(1)`, `002839B0`: rebuild the party status records | 3 |
| 3 | builds the slot list from the roster (`00282DF0`, the `0209AC30 + 0xB10` membership bytes) and applies it (`00283870`, `003273D0(unit, 1)`, `00283840(0)`) | 4 |
| 4 | waits for `00283980()`, then `00283940`, **`0032AB60(0x73, 0)`** (persistent flag 115 cleared, `0035CE74` `xor edx, edx`), `0026C840(0)`, `003634B0(0xF)` | 7 |
| 7 | fade in, 30 frames (`002EFA70(0, 0x1E, 1)`) | 5 |
| 5 | ends the task (`00244F00`) | |

### Reset, restore and the save

- `00304680` is the full reset: `00303D90(0)`, the turbo end, `+0x5AE0` bits 0, 2 and 3 cleared,
  the three floats zeroed, `0035C900(0)`. It runs from the battle runtime reset `00237DF0`
  (`00237E4B`) and from `00304140`, which calls it when the riding bit is clear.
- `00304060` and `00304140` are entered through the pointer pair at `01EED010` / `01EED018`.
  `00304060` restores a ride: it re-attaches the chocobo to the leader (`002E28C0`, `002ECF10`),
  reloads slot 1 with `max(+0x5AE4, 2.0)` (the floor at `01CEBC08`) and slot 2 with `+0x5AE8`,
  re-applies turbo from bit 1 and sets bit 0.
- The riding bit is in the save: `002EF3C0` copies the whole dword `+0x5B04` into the transition
  record's `+0x28` and `002EF410` writes it back ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).
  The restore `005843E0` then clears bit 1 when the block's flag bit 12 is set (`0058446A`), so a
  load into the second spawn-keep pair never arrives riding.

### Airship travel

There is no airship verb; `setflystatus` is the only flight-named verb and no shipped script calls
it. The five aerodrome scripts (`rbn_b01`, `nac_b01`, `byu_b01`, `alc_e01`, `var_b01`) share the
boarding counter and departure watcher actors:

1. the counter prices the route (`getprice(0xB005..0xB007)`) and keeps the route code in
   `global_flag[2]`;
2. a monster attack is rolled with `rand_29(100)` against a chance that rises with quest 153's
   progress, into `battle_global_flag[1]`;
3. `subgill(price)`; a fade; the dismount routine above; scene 214 (`eventread_e8(0, 214)`,
   `eventplay_ec(0)`);
4. the jump, always `mapjump(field, entrance, 1)`: with the attack, `setmapjumpgroupflag(94)` and
   field 125 (`asp_a02`); declining to watch, the destination aerodrome by route code (`0x314`/4,
   `0x320`/3, `0x317`/7, `0x31A`/7, `0x31D`/7); otherwise `setmapjumpgroupflag(94)` and field 124
   (`asp_a01`, the deck), whose script jumps on to `asp_a02` or the destination by the same code.

The private airship's counter (`nac_b01`) jumps with `mapjump(dest, entrance, 4)`.
Everything in a flight is therefore a gil write, a scene and a map jump
([zone changes](zone-changes-and-mapjump.md)).

## Layouts

```
struct ChocoboRide base=[02EBF190]+0x5AE0 size=0x10
+0x00  u32  flags       bit 0 timer running, bit 1 turbo on, bits 2-3 turbo charges
+0x04  f32  rideLeft    seconds; 180.0 at mounting (00303D90, 00304440)
+0x08  f32  turboLeft   seconds (00303F00, 00304440)
+0x0C  u32  turboArg    the last 00303F00 argument
```

```
struct TimerSlot base=02B5EBC0 size=0x14
+0x00  i32  start      (003EBC50)
+0x04  i32  target
+0x08  f32  value      003EBA90
+0x0C  f32  step       ±1/60 or ±1/50 per frame
+0x10  u8   running    003EBD00
+0x11  u8   expired    003EBB70
```

```
mode = bit3(+0x5B04) ? 5 : bit2 ? 4 : town ? 3 : bit1 ? 2 : bit0        (0030D9A0)
riding            = bit1(+0x5B04)                                        (getchocobomodebit)
chocobo mode      = mode == 2                                            (getchocobomode)
ride ends when    timer slot 1 expired && mode == 2 && 00303CC0() && chocobo unit exists
```

## Shipped data

| Verb or flag | Scripts | Calls |
|---|---|---|
| `setchocobomode` | 126 | 209 |
| `getchocobomodebit` | 503 | 5,228 |
| `getchocobomode` | 251 | 338 |
| `enable_by_chocobo` | 72 | 326 |
| `ridechocobo`, `getoffchocobo`, `btlAtelSetChocoboTurboMode`, `setflystatus` | 0 | 0 |
| `setmapjumpgroupflag(115)` / `releasemapjumpgroupflag(115)` | | 45 / 190 |
| `setmapjumpgroupflag(94)` | | 21 |
| `eventread_e8(0, 214)` | | 10 |
| `releasemapjumpgroupflag(94)` | | 4 |

Counts over the 1,114 `us` zone and event scripts. Five scripts spend the Gysahl Greens
(`subitem(0x20D8, 1)`), and 14 scripts call `setchocobomode(1)`.

## Operations

- Riding is engine-global: one bit, one flag, one timer. There is no per-actor rider state; the
  chocobo is the actor in roster entry 3 and the render-mode and animation calls target it.
- Two dismount paths exist, the scripts' `setchocobomode(0)` plus `releasemapjumpgroupflag(115)`
  and the native task, which clears the same flag in state 4. The menu's Dismount command and the
  timer both go through the task.
- The ride timer pauses with the field: it only counts while `00304440` runs, and `00304060`
  reloads it from the saved seconds, never below 2.0.

## State

| Address | Kind | Role |
|---|---|---|
| `[02EBF190] + 0x5B04` | u32 | the mode bits; bit 1 riding; saved in the transition record |
| `[02EBF190] + 0x5AE0`-`+0x5AEF` | struct | the ride state above |
| `02B5EBC0` | TimerSlot[] | slot 1 the ride, slot 2 turbo |
| `022CA468` | ptr | the running dismount task, 0 when none |
| `022CA45C` | u32 | cleared when a timer dismount starts |
| `01CEBC08` | f32 | 2.0, the restore floor for slot 1 |
| `01DFE0B8` | f32 | the frame base the turbo length multiplies, image value 1.0 |
| `[001D50D0()] + 0xE1D`, `+0xE1E` | u8 | configuration bytes: endless ride, endless turbo charges |
| persistent flag 115 | flag | riding, as the scripts see it |
| persistent flag 94 | flag | set before the airship-deck and attack jumps (scripts) |

## Modding notes

- To change the ride length, change the `180.0` the setter and the per-frame refresh write
  (`0x43340000` at `00303D90` and `00304440`); the timer counts seconds at the frame rate.
- A mount without a script is `00303D90(1)` plus flag 115; a dismount without the fade is
  `00303D90(0)` plus clearing the flag. The task adds the fade, the music swap and the party
  rebuild.
- Mounting in a town is possible but leaves chocobo mode: the ladder puts the town flag above the
  riding bit, so the theme and the menu command do not follow.
- Airship travel needs no engine change: it is the aerodrome script's gil charge, scene and
  `mapjump`; the route is a story global and the attack is a local random roll.

## Related

- [Zone changes and mapjump](zone-changes-and-mapjump.md): the jump the flights and the deck use.
- [Save and teleport crystals](save-and-teleport-crystals.md): the crystal's dismount.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the transition record that carries `+0x5B04`.
- The battle-state block field map: the block the riding fields sit in.
- Persistent flag banks: flags 115 and 94.
- [Actor record](../Characters-And-Objects/actor-record.md): the roster entries and the actor byte `+0x0B`.
- The music control file and the BGM stream: tracks `0x5A` and `0x5B`.
- [Area flags](area-flags-navimapdata.md): the town bit the ladder ranks above riding.
- [Game over](game-over.md): what a party wipe does.
