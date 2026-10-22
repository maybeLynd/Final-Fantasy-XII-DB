---
title: "Chocobos and airships: riding a chocobo, the ride timer and its dismount, and aerodrome travel"
kind: "system"
category: "World, areas and travel"
addresses: "0x00303D90, 0x00303EE0, 0x00303EC0, 0x0030D9A0, 0x003135C0, 0x00303F00, 0x003514D0, 0x00347230, 0x00347820, 0x00347C60, 0x00356630, 0x00355910, 0x0033F650, 0x0050F8A0, 0x0037CFF0, 0x0037CFC0, 0x0037D100, 0x00304440, 0x00234590, 0x00303CC0, 0x00336390, 0x0017D380, 0x0017D3A0, 0x0031B8C0, 0x00311E20, 0x0035CFA0, 0x0035C960, 0x0035CA70, 0x003CA310, 0x003CA860, 0x00304680, 0x00304060, 0x00304140, 0x00237DF0, 0x0034EE20, 0x0034DD90, 0x0032AB60, 0x003EBA90, 0x003EBB70, 0x003EBC50, 0x003EBD00, 0x002E73C0, 0x002EB030, 0x00263750, 0x00306760, 0x005843E0, 0x002EF3C0, 0x002EF410, 0x00261F90, 0x002DEE50, 0x003611F0, 0x0026A7F0, 0x00342E50, 0x00265680, 0x001D50D0, 0x005C5230"
---

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

Riding is held in the battle-state block at `[0x02EBF190]` ([the block's field map](../Party/party-data.md)):

| Field | Meaning |
|---|---|
| `+0x5B04` bit 1 | riding |
| `+0x5AE0` bit 0 | the ride timer is running |
| `+0x5AE0` bit 1 | turbo is on |
| `+0x5AE0` bits 2-3 | turbo charges, 3 on mounting |
| `+0x5AE4` | f32, the ride time left in seconds; 180.0 on mounting |
| `+0x5AE8` | f32, the turbo time left in seconds |
| `+0x5AEC` | the last turbo argument |

`0x00303D90(on)` is the one setter and does nothing when bit 1 already equals `on`:

- `on`: `+0x5B04 |= 2`, `+0x5AE0 |= 0xC`, `+0x5AE4 = 180.0` (`0x43340000`);
- off: `+0x5B04 &= ~2`; the chocobo, the actor in roster entry 3 (`0x00263750(3)`), has its render
  record set to mode 3 (`0x002E73C0(actor, 3)`: `+0x294` bit 27 and the top five bits of `+0x304`);
  `+0x5AEC = 0`; when turbo was on, animation `0x2001` is requested on the chocobo (`0x002EB030`)
  and bit 1 of `+0x5AE0` is cleared.

Its callers are the verb thunks `0x0037CFF0` (on), `0x0037CFC0` (off) and `0x0037D100` (argument), the
full reset `0x00304680`, the dismount task `0x0035CA70` and the special presentation `0x00306760`, whose
kind 5 mounts (the same three stores) and kind 6 dismounts.

### Riding and the mode ladder

`0x0030D9A0` ranks the block's mode bits: `+0x5B04` bit 3 gives 5, bit 2 gives 4, the current area's
record bit 15 (`0x00377C20`, a town) gives 3, bit 1 gives 2, otherwise bit 0 gives 0 or 1. So
`getchocobomodebit` (`0x00303EE0`, the raw bit) and `getchocobomode` (`0x00303EC0`, ladder = 2) differ:
riding into a town, or while bit 2 or 3 is set, keeps the bit but leaves chocobo mode. `0x003135C0`
is ladder = 1.

The area music follows the ladder: unless the field's own track is boss music (`0x00361010`, tested at
`0x00262041`), the field music select `0x00261F90` plays track `0x5B` when the ladder is 1 and track `0x5A`, the
chocobo theme, when it is 2 (`0x0026204A`-`0x00262063`; [music](../Sound-And-Music/music-table.md));
the dismount task stops that track again.

### The verbs

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setchocobomode(v)` | `0x3EC` | `0x003514D0` → `0x0037D100` | `0x00303D90(v)` |
| `ridechocobo` | `0x37E` | Start `0x00347230` → `0x0037CFF0`, Poll `0x00347C60` | `0x00303D90(1)`; the Poll returns `0x005C5230() != 0`, always 0, so it ends on its first poll |
| `getoffchocobo` | `0x37F` | Start `0x00347820` → `0x0037CFC0`, Poll `0x00347C60` | `0x00303D90(0)`, the same Poll |
| `getchocobomodebit()` | `0x511` | `0x00356630` | `+0x5B04` bit 1 |
| `getchocobomode()` | `0x407` | `0x00355910` | ladder = 2 |
| `enable_by_chocobo(v)` | `0x40A` | `0x0033F650` | bit 0 of byte `+0x0B` of the calling actor = `v != 0` |
| `btlAtelSetChocoboTurboMode(v)` | `0x302F` | `0x0050F8A0` | `0x00303F00(v != 0)` |
| `setmapjumpgroupflag(id)` / `releasemapjumpgroupflag(id)` | `0x430` / `0x431` | `0x0034EE20` / `0x0034DD90` | `0x0032AB60(id, 1)` / `(id, 0)`: a primary persistent flag ([persistent flag banks](../Story-Events-And-Hunts/story-flags.md)) |
| `setflystatus(v)` | `0x1E0` | `0x00342E50` → `0x0026A7F0` | bit 0 of the actor's secondary context `+0x151`, and `+0x152` 1 ↔ 2 with the mode word refreshed (`0x002681E0`, `0x0026A85A`) when it flips; then bits 0 and 1 of `+0x151` are copied to bits 0 and 1 of `+0x90` of the record at context `+0x138` (`0x002682D0`, `0x0026A862`) |

No instruction in the image tests bit 0 of the actor byte `+0x0B` with an immediate mask; the byte
is cleared to its top two bits by the record initialiser and has bit 6 cleared by the movement
defaults ([actor record](../Characters-And-Objects/actor-record.md)).

### Mounting and dismounting in the scripts

The keeper scripts (`fon_a07` and the others) mount with `subitem(0x20D8, 1)` (Gysahl Greens),
`suspendbattle`, a fade, `setchocobomode(1); partyallread();`, the riding motion,
`setmapjumpgroupflag(115)`, a re-read of the map music (`musicplay(getnowmapmusicno_47a(0))`) and
`resumebattle`. The dismount routine every script shares (`sumcho_byebye`) is:

```python
if (getchocobomodebit()) { setchocobomode(0); partyallread(); releasemapjumpgroupflag(115); }
```

So persistent flag 115 means "the party is riding" to the scripts, and both the script dismount
and the native one below clear it. The crystal and aerodrome scripts call it before a teleport or a
flight ([save and teleport crystals](save-and-teleport-crystals.md)).

### The ride timer and the turbo timer

The two countdowns live in the shared timer slots at `0x02B5EBC0`, 20 bytes each (Layouts):

- `0x003EBC50(slot, value, target)` loads a slot with a step of `1/60` (`0x3C889A05`) when
  `0x00290180()` is 2 and `1/50` (`0x3CA3D70A`) otherwise, negative when the target is at or below
  the value;
- `0x003EBD00(slot)` starts it, or marks it expired when value and target already agree;
- `0x003EBA90(slot)` reads the value and `0x003EBB70(slot)` the expired byte.

The values are therefore seconds counted at the frame rate: the ride is 180 seconds.

`0x00304440` runs every field frame from the tick's per-slot pre-pass `0x00234590` (`0x00234712`) while
`+0x5AE0` bit 0 is set:

1. `+0x5AE4` = slot 1's value, or 180.0 while the configuration byte `+0xE1D` of `[0x001D50D0()]`
   is set (`0x0017D380`); `+0x5AE8` = slot 2's value;
2. when `0x00303CC0()` allows a dismount, slot 1 has expired, that byte is clear, the ladder is 2
   and the chocobo (`0x0031B8C0(3)`, the unit of roster entry 3) exists: `0x00311E20()` refreshes the
   camera target and `0x0035CFA0(1)` starts the dismount task;
3. when slot 2 has expired and turbo is on: the chocobo's render mode is set to 3, `+0x5AEC` = 0,
   animation `0x2001` is requested and bit 1 is cleared.

Turbo (`0x00303F00(on)`) sets `+0x5AEC`, puts the chocobo's render record in mode 1 (on) or 3 (off)
and, when the bit changes: on requires ladder 2 and a non-zero charge count; it loads slot 2 with
`10 × [0x01DFE0B8]` seconds (the frame base, image value 1.0), spends one charge unless the
configuration byte `+0xE1E` (`0x0017D3A0`) is set, and requests animation `0x2010`; off requests
`0x2001`; either way bit 1 is toggled.

### The turbo charge marks

The party menu task `0x003CA860` shows the charges as up to three marks in its child `0x003CB150`, which keeps the
record `[0x0209AC30] + 0x28` at `+0x1C8` on message 1:

1. Message 16 sets `+0x1D4` bit 0, decodes the child's layout from that record (`0x002432B0`) and runs
   `0x003CB320`. It gives the three 0x58-byte mark records at `+0xC0` their nodes (`+0x40`, from the table
   `0x00D11758`) and shows the marks below the charge count, `+0x14` of `0x003200A0` (bits 2-3 of `+0x5AE0`,
   `0x00304610`); the count, at most 3, goes to `+0x1D0`.
2. Message 2, while `+0x1D4` bit 0 is set, runs `0x003CAED0`. When the count has dropped, the last shown mark
   gets two tweens (`0x002726C0`, `0x002727C0`): the alpha of its four vertex colours over 32 steps and their
   colour over 16.
3. While a tween runs, `0x003CAED0` writes its value (`0x00271960`) into the node's colours; a mark whose
   tweens have both ended (`0x00272710`) is hidden.

### Where a dismount is allowed

`0x00303CC0()` returns 1 only when the ladder is 2, the chocobo exists and `0x00336390(position,
radius, 0)` passes: the chocobo's position (`0x00265020`) and the four points `radius` away along
both axes all lie on walkable ground (`0x0026E100`), with `radius` the larger of the leader's two
`0x00265090` radii.

The menu's Dismount command uses the same test. Its dialog task `0x003CA310`, spawned by the party
menu task `0x003CA860` while chocobo mode is on, shows text `0x832` "Dismount" when the test passes
and `0x87C` "You cannot dismount here." when it does not, and on a confirmed `0x8100` result it
calls `0x0035CFA0(0)`.

The dialog's open message runs `0x0035CF10` (`0x003CA43E`): it clears `0x022CA45C`, resets the battle menu
(`0x00252B40(0x14)`) and takes two holds through `0x002E1C20(8)`. A confirmed Dismount then calls `0x0035D010(1)`
(`0x003CA3B5`), which stores 0 in `0x022CA45C`; a refused test or any answer other than `0x8100` and the cancel
`0x8102` calls `0x0035D010(0)` (`0x003CA3DE`), which stores 1. The close message runs `0x0035CF50` (`0x003CA360`): with
no dismount task in `0x022CA468`, or with `0x022CA45C` set, it releases both holds (`0x002E1CA0(8)`), runs
`0x00252D90` and clears `0x022CA45C`.

### The dismount task

`0x0035CFA0(fromTimer)` spawns a `0xD0`-byte task on `0x0035C960` when the field is live (`0x00265680`)
and no dismount task is running (`0x022CA468` = 0). The handler's open step sets the state byte
`+0xC0` to 6, records the task in `0x022CA468` and, for a timer dismount, resets the battle menu
(`0x00252B40(0x14)`, `0x002E1C20(8)`); every later frame runs the state machine `0x0035CA70`:

| State | What it does | Next |
|---|---|---|
| 6 | fade out, 30 frames (`0x002EFA70(0, 0x1E, 0)`) | 8, then 1 |
| 8 | waits for the fade (`0x002EFD20(0)` = 1) | the stored next state |
| 1 | `0x0026C3C0(0)`, `0x00303D90(0)` (the dismount), `0x003CA1C0`, `0x003C58B0`, `0x003634B0(0xF)` | 9 |
| 9 | `0x002DEBE0(-1)` finds the music slot; `0x002DEE50(slot, 0x5A)` and `0x003611F0(0x5A)` stop the chocobo theme | 10, or 12 with no slot |
| 10 | waits for `0x002F1A30(1)` = 0, then `0x002DEDE0(slot)` | 11, or 12 for a negative slot |
| 11 | waits for `0x001DBBF0(slot)` = 0 | 12 |
| 12 | `0x00360D70` or `0x00360E50`; `0x0026DE00(0)` picks the field's track | 13 or 14, or 2 with no track |
| 13 / 14 | `0x00360C20(track)` = 5 restarts the field music (`0x002DEC00`, `0x002DECE0`); 14 retries `0x00361630(track)` | 2 |
| 2 | `0x00282F80`, `0x00283270(1)`, `0x002839B0`: rebuild the party status records | 3 |
| 3 | builds the slot list from the roster (`0x00282DF0`, the `0x0209AC30 + 0xB10` membership bytes) and applies it (`0x00283870`, `0x003273D0(unit, 1)`, `0x00283840(0)`) | 4 |
| 4 | waits for `0x00283980()`, then `0x00283940`, **`0x0032AB60(0x73, 0)`** (persistent flag 115 cleared, `0x0035CE74` `xor edx, edx`), `0x0026C840(0)`, `0x003634B0(0xF)` | 7 |
| 7 | fade in, 30 frames (`0x002EFA70(0, 0x1E, 1)`) | 5 |
| 5 | ends the task (`0x00244F00`) | |

### Reset, restore and the save

- `0x00304680` is the full reset: `0x00303D90(0)`, the turbo end, `+0x5AE0` bits 0, 2 and 3 cleared,
  the three floats zeroed, `0x0035C900(0)`. It runs from the battle runtime reset `0x00237DF0`
  (`0x00237E4B`) and from `0x00304140`, which calls it when the riding bit is clear.
- `0x00304060` and `0x00304140` are entered through the pointer pair at `0x01EED010` / `0x01EED018`.
  `0x00304060` restores a ride: it re-attaches the chocobo to the leader (`0x002E28C0`, `0x002ECF10`),
  reloads slot 1 with `max(+0x5AE4, 2.0)` (the floor at `0x01CEBC08`) and slot 2 with `+0x5AE8`,
  re-applies turbo from bit 1 and sets bit 0.
- The riding bit is in the save: `0x002EF3C0` copies the whole dword `+0x5B04` into the transition
  record's `+0x28` and `0x002EF410` writes it back ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)).
  The restore `0x005843E0` then clears bit 1 when the block's flag bit 12 is set (`0x0058446A`), so a
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

Struct ChocoboRide base=[`0x02EBF190`]+`0x5AE0` size=`0x10`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | flags | bit 0 timer running, bit 1 turbo on, bits 2-3 turbo charges |
| `+0x04` | `f32` | rideLeft | seconds; 180.0 at mounting (`0x00303D90`, `0x00304440`) |
| `+0x08` | `f32` | turboLeft | seconds (`0x00303F00`, `0x00304440`) |
| `+0x0C` | `u32` | turboArg | the last `0x00303F00` argument |

Struct TimerSlot base=`0x02B5EBC0` size=`0x14`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | start | (`0x003EBC50`) |
| `+0x04` | `i32` | target |  |
| `+0x08` | `f32` | value | `0x003EBA90` |
| `+0x0C` | `f32` | step | ±1/60 or ±1/50 per frame |
| `+0x10` | `u8` | running | `0x003EBD00` |
| `+0x11` | `u8` | expired | `0x003EBB70` |

```python
mode = bit3(+0x5B04) ? 5 : bit2 ? 4 : town ? 3 : bit1 ? 2 : bit0  # 0x0030D9A0
riding            = bit1(+0x5B04)                                        (getchocobomodebit)
chocobo mode      = mode == 2                                            (getchocobomode)
ride ends when    timer slot 1 expired && mode == 2 && 0x00303CC0() && chocobo unit exists
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
- The ride timer pauses with the field: it only counts while `0x00304440` runs, and `0x00304060`
  reloads it from the saved seconds, never below 2.0.

## State

| Address | Kind | Role |
|---|---|---|
| `[0x02EBF190] + 0x5B04` | u32 | the mode bits; bit 1 riding; saved in the transition record |
| `[0x02EBF190] + 0x5AE0`-`+0x5AEF` | struct | the ride state above |
| `0x02B5EBC0` | TimerSlot[] | slot 1 the ride, slot 2 turbo |
| `0x022CA468` | ptr | the running dismount task, 0 when none |
| `0x022CA45C` | u32 | cleared when a timer dismount starts; 1 after a refused Dismount (`0x0035D010`), read by `0x0035CF50` |
| `0x01CEBC08` | f32 | 2.0, the restore floor for slot 1 |
| `0x01DFE0B8` | f32 | the frame base the turbo length multiplies, image value 1.0 |
| `[0x001D50D0()] + 0xE1D`, `+0xE1E` | u8 | configuration bytes: endless ride, endless turbo charges |
| persistent flag 115 | flag | riding, as the scripts see it |
| persistent flag 94 | flag | set before the airship-deck and attack jumps (scripts) |

## Modding notes

- To change the ride length, change the `180.0` the setter and the per-frame refresh write
  (`0x43340000` at `0x00303D90` and `0x00304440`); the timer counts seconds at the frame rate.
- A mount without a script is `0x00303D90(1)` plus flag 115; a dismount without the fade is
  `0x00303D90(0)` plus clearing the flag. The task adds the fade, the music swap and the party
  rebuild.
- Mounting in a town is possible but leaves chocobo mode: the ladder puts the town flag above the
  riding bit, so the theme and the menu command do not follow.
- Airship travel needs no engine change: it is the aerodrome script's gil charge, scene and
  `mapjump`; the route is a story global and the attack is a local random roll.

## Related

- [Zone changes and mapjump](zone-changes-and-mapjump.md): the jump the flights and the deck use.
- [Save and teleport crystals](save-and-teleport-crystals.md): the crystal's dismount.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the transition record that carries `+0x5B04`.
- [The battle-state block field map](../Party/party-data.md): the block the riding fields sit in.
- [Persistent flag banks](../Story-Events-And-Hunts/story-flags.md): flags 115 and 94.
- [Actor record](../Characters-And-Objects/actor-record.md): the roster entries and the actor byte `+0x0B`.
- [The music control file and the BGM stream](../Sound-And-Music/music-table.md): tracks `0x5A` and `0x5B`.
- [Area flags](area-flags-navimapdata.md): the town bit the ladder ranks above riding.
- [Game over](game-over.md): what a party wipe does.
