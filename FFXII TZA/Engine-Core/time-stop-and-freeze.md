---
title: "Time stop and freeze: how menus, cutscenes, Stop magicks and skippable scenes halt actors"
kind: "system"
category: "Engine core"
summary: "The twenty-eight request slots that freeze parts of the world: who raises and releases each one, the two permission records the builder writes per request and what each exempts, the start that marks every actor, the apply that ANDs all slots into one pair and drives the global switches, the per-actor pass that folds the marks into seven live stop sets and the hooks each set fires, the cancel, the area-unload sweep and the reset."
addresses: "00226BE0, 00227680, 00226280, 00226640, 002269A0, 00225CD0, 00225EB0, 00226B30, 00226B10, 00226BA0, 00226BC0, 00226BD0, 00263FF0, 00358940, 00359B80, 003590D0, 003588B0, 00263750, 002647B0, 00263BE0, 00227370, 002273B0, 002273E0, 00227420, 00227460, 002274A0, 002274E0, 00227510, 00227550, 00227590, 002275D0, 00227610, 00227640, 002260A0, 002260C0, 002260E0, 00226100, 00226120, 00226140, 00226160, 00226180, 002261B0, 002261E0, 00226210, 00226240, 00226260, 00254740, 00255290, 00252D90, 002544C0, 002DDC30, 003B3B40, 00263480, 0026A1D0, 00266D10, 00263560, 00263230, 00263050, 0026B980, 0026B970, 00377700, 0034DC30, 00343CE0, 00350400, 00350940, 002E2440, 002E2400, 002E06B0, 00353D90, 00354800, 003531A0, 00353A60, 00354300, 003535F0, 0026C3E0, 0026C5D0, 00263660, 00265680, 00346860, 00352000, 0025C830, 0025C170, 0025B500, 002678C0, 0025D580, 0033F940, 0035C7B0, 0027EFA0, 00341D20, 003420F0, 00341360, 00341790, 00360710, 0034ECF0, 0034E6D0, 003603F0, 002E2240, 00313DB0, 0031E860, 002EA8B0, 002EA8E0, 002E24C0, 002E24E0, 0025A5D0, 002547C0, 00254840, 0035B4B0, 0035B510, 002DF370, 002DF640, 002EBBF0, 0024B9B0, 0024C970, 0026D6D0, 0026D6F0, 002E92F0, 00264DC0, 00428FE0, 00238B40, 00312130, 0031B760, 002E9FE0, 002E7E90, 0025DF00, 0024FCA0, 0024FBF0, 0024FC80, 0024FB90, 002E8B10, 00428940, 0024BFD0, 00226A50, 00226AB0, 00182D10, 00182D40, 00182D60, 00182DA0, 00182CD0, 00182CF0, 00227D30, 0022A770"
---

## What the player sees

Open the main menu in the field and everyone stops mid-step. Cast Stop, or let a target cursor
sit on an enemy, and the rest of the field holds while the one you picked keeps acting. Enter a
conversation and the talking actors play while the scene around them waits. Skip a scene and the
world resumes cleanly. Each of these is a different request to one registry, and the differences
between them, who keeps moving, whether only scripts freeze or animation too, which sound groups
mute, come from a small permission record written for each request.

Requests stack. While a menu and a Stop are both active, every actor obeys the stricter of the
two, and when one is released the other still holds. The chocobo's rider, the party leader and
the actor a cutscene names are the exemptions the records carve out.

## How it works

### The request slots

There are twenty-eight request ids. Each has two records, A at `01FD4160 + id × 0x18` and B at
`01FD4400 + id × 0x18`: a qword of permission bits at `+0`, a fade length at B `+0x10` and a flag
byte at `+0x14`. The bitset `01FD46D4` holds the active ids, the dirty byte `01FD46D0` tells the
apply step that something changed, and `01FD46A0` / `01FD46B8` hold the last combined A and B.

A set bit in a record is an exemption. For a category `c` from 0 to 6: A bit `c` exempts the
category from set 1, A bit `8 + c` from set 2, A bit 28 together with bit `8 + c` from set 3,
B bit `c` from set 4, B bit `8 + c` from set 5, A bit `16 + c` from set 6 and B bit `16 + c` from
set 7.

The categories:

- 0: the party focus actor (`003590D0()` through `003588B0`);
- 1: the other roster entries (`00263750(0..3)` minus the focus);
- 5: the request's own actor; 6: the request's handle list;
- 2, 3, 4: every other managed actor not in a party slot (`002647B0`: byte `+0x12` below 4), by
  the type class `00263BE0` gives from the low nibble of byte `+0x0E`: 3 for types 1, 2 and 7, 4
  for type 3, and 2 for anything else.

### Starting a request

`00226BE0(id, actor, count, handles, fade, flag)` returns at once when the id's bit is set.
Otherwise:

1. the fade goes to B `+0x10`; `00227680(id, A, B, max(flag, 0))` builds the records, the flag
   landing at B `+0x14`; the bit and the dirty byte are set;
2. one actor manager is walked when A bit 31 is set, three when it is clear (`00263FF0(m)`, live
   when its `+0x10` bit 0 holds): every record from `+0x1DE` for `+0x1D6` entries (`00358940`)
   gets the id's bit OR-ed into its seven pending-set words and cleared from its seven
   pending-clear words;
3. for a manager whose `+0x28` is 0, the exemptions: for each category the id's bit is removed
   again from the pending-set word of every set whose record bit is set.

Nothing stops yet: the apply does that.

`00227680` starts both records from one default (A bits 24, 26 to 31, 34, 36 and 37; B bits 0 to
4, 8 to 12, 24, 27, 33, 35 to 37 and 40 to 44) and then runs the id's case; ids 4, 6 and 7 also
read the flag. Ids 0, 1, 2, 3, 15, 22 and 27 share one case, 4, 6 and 7 another, 8 and 9, 16, 20
and 21, 17 to 19, 23 and 25, 24 and 26 are pairs; id 0 runs `00182D10` unless the options bit 3
(`002DDC30`, the Battle Mode setting, [game settings](../Saving-Loading-And-Settings/game-settings.md))
is set, id 12 and 17 run `00182CF0`, 13 and 15 run `00182CD0`.

### The twenty-eight requests

| Id | Raised by | Released by |
|---|---|---|
| 0 | UI request 1 (the battle menu) with the options bit clear, request 4 with it set, request 20 always (`00254740` through `00255290`) | the UI close (`00252D90`, `002544C0`), fade -1 |
| 2 | UI requests 3 and 24 | the same |
| 4, 5, 7 | the field hold `00263480(actor, mode)`: mode 1 raises 4, mode 0 raises 5, mode 2 raises 7 with the actor as a one-entry handle list (an empty list when the actor is null); the flag is `02099DE7` = 0; the boot `00266D10` raises 4 and 5 from the hold bytes `02099DE6` / `02099DE5`; `0026A1D0(on, flag)` raises 5 | `00263480` with both hold bytes clear, `0026A1D0` with `on` clear and the boot cancel 5, 4 and 7 |
| 6 | an event script taking an actor (`00263230`, fade 4, flag `00377700()`) and the verb `talkfadeout(fade)` (`0026B980`) | the entry's removal (`00263050`, fade 4) and `talkfadein(fade)` (`0026B970`) |
| 10 | `settimestopmagic` (`00350400` → `00227460`, with apply) and the target cursor `00313DB0` (the selected unit's id as the actor; at party-control level 2 the rider's entry as the handle list) | `cleartimestopmagic` (`00350940` → `00226120`, fade -1) and the cursor's close |
| 11 | `seteventtimestop(1)` (`0034DC30` → `002273B0`, no apply) | `seteventtimestop(0)` (`002260C0`) |
| 12 | `settutorial00timestop(1)` (`00343CE0` → `00227610`) | the same verb with 0 (`00226240`) |
| 13 | UI requests 2, 6, 15, 17, 18, 19 and 22 (the full-screen menus) | the UI close |
| 15 | `002E2240(1)`, which also moves the main loop to state 6 ([frame update order](frame-update-order.md)) | `002E2240(0)`, which moves it to state 2 |
| 16 | `maskopen`, `maskopenfast`, `mesvmaskopen`, `mesvmaskopenfast` (`002E2440` → `002274E0`) | `maskclose`, `maskclosefast` (`002E2400` → `00226160`), the area unload `002E06B0` |
| 17 | `ucon` / `ucon_4a5` (`0026C5D0`), `0026C3E0`, `00263660` (from the area unload `002628B0`, the drive pass `0025D9E0`, the tick `00314020`, `0026CE60`, `0026B8A0`, `0026B8C0` and `0026C8C0`): raised when `00265680()` is 0, else released, each followed by the apply | the same bodies |
| 18 | `0025C830` (← `0025C170`) through `00227420`, with apply | `0025B500` through `00226100` once its count `02099DB8` reaches 0, then `002E1CD0(1)`; the apply is left to the field frame |
| 19 | the definition load `002678C0`, with apply | `clearmapjumpstatus` (`0033F940` → `0025D580`), with apply |
| 22 | `0035C7B0(0x0B)` on the game-over route `0027EFA0` ([game over](../World-Areas-And-Travel/game-over.md)), with apply | UI request 11's close (`002260A0`) |
| 23, 24 | `setstatuserrordispdenystatus(1)` (`00227550`), `setstatuserrorctrldenystatus(1)` (`00227510`), with apply | the same verbs with 0 (`002261B0`, `00226180`), with apply |
| 25, 26 | `…dispdenystatus_by_menu(1)` (`002275D0`), `…ctrldenystatus_by_menu(1)` (`00227590`), with apply | the same verbs with 0 (`00226210`, `002261E0`), with apply |
| 27 | `skipexec` (`0034ECF0` → `00360710` → `002273E0`) | `skipend` (`0034E6D0` → `002260E0`), the area unload `003603F0` |
| 1, 3, 8, 9, 14, 20, 21 | nothing: no wrapper and no direct call carries these ids | |

The start wrappers from `00227370` to `00227640` and the cancel wrappers from `002260A0` to
`00226260` test the id's bit first, except the starts for 11, 12 and 16, which rely on
`00226BE0`'s own held-bit return; a repeated request is ignored either way. The start wrappers for
10, 18, 22, 23, 24, 25 and 26 and the cancel wrappers for 23 to 26 run the apply themselves; the
others leave it to the field frame, which runs `00226280` at the end of every pass ([frame update
order](frame-update-order.md)).

The records each id builds, read as the categories each set stops (F the focus actor, P the
other roster entries, T127 / T3 / T0 the three type classes, R the request's actor, H the handle
list; "all" is every category and "-" none):

| Id | Flag | A | B | Managers | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0, 1, 2, 3, 22 | | `00000034D4000000` | `00001F3A09001F1F` | 1 | all | all | all | R H | R H | all | all |
| 4 | 0 | `00000024F9040707` | `00001F2B0B001F1F` | 1 | T127 T3 R H | same | same | R H | R H | F P T127 T3 R H | all |
| 4 | 1 | `00000024F9040505` | `00001F2A09001F1F` | 1 | P T127 T3 R H | same | same | R H | R H | F P T127 T3 R H | all |
| 5 | | `00000034EB000000` | `00001F3A0B00101F` | 1 | all | all | all | R H | F P T0 T127 R H | all | all |
| 6 | 0 | `00000004DB040707` | `00001F0B0B001F1F` | 1 | T127 T3 R H | same | same | R H | R H | F P T127 T3 R H | all |
| 6 | 1 | `00000004DB040505` | `00001F0A0B001F1F` | 1 | P T127 T3 R H | same | same | R H | R H | F P T127 T3 R H | all |
| 7 | 0 | `00000024F9044307` | `00001F2B0B005F1F` | 1 | T127 T3 R H | T0 T127 T3 R | same | R H | R | F P T127 T3 R H | all |
| 7 | 1 | `00000024F9044105` | `00001F2A09005F1F` | 1 | P T127 T3 R H | P T0 T127 T3 R | same | R H | R | F P T127 T3 R H | all |
| 8, 9 | | `00000030BD000060` | `00001F3209001F7F` | 1 | F P T0 T127 T3 | all | all | - | R H | all | all |
| 10 | | `00000030BF7F6060` | `00001F320B001F1F` | 1 | F P T0 T127 T3 | same | same | R H | R H | - | all |
| 11 | | `0000002011000000` | `00001F2A0B001F1F` | 3 | all | all | all | R H | R H | all | all |
| 12 | | `00000024DD001F01` | `00001F3A0B1F1F1F` | 1 | P T0 T127 T3 R H | R H | R H | R H | R H | all | R H |
| 13 | | `FFFFFFFFD5FFE0FF` | `FFFFFDFDFDFFFFFF` | 1 | - | F P T0 T127 T3 | same | - | - | - | - |
| 14 | | `00000000BD000000` | `00001F0A09001F1F` | 1 | all | all | all | R H | R H | all | all |
| 15 | | `00000034D4000000` | `0000003A09001F1F` | 1 | all | all | all | R H | R H | all | all |
| 16, 20, 21 | | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFEFFFFFF` | 1 | - | - | - | - | - | - | - |
| 17, 18, 19 | | `FFFFFFFFFFFCFFFF` | `FFFFFFFFFFFCFFFF` | 1 | - | - | - | - | - | F P | F P |
| 23, 25 | | `FFFFFFFFFFFFFFFF` | `FFFFFFFFFEFFFFFF` | 1 | - | - | - | - | - | - | - |
| 24, 26 | | `FFFFFFFFFEFFFFFF` | `FFFFFFFFFFFFFFFF` | 1 | - | - | - | - | - | - | - |
| 27 | | `FFFFFFFFFFFFFFFF` | `FFFFE2FFFFFFFFFF` | 1 | - | - | - | - | - | - | - |

Read as behaviour:

- the menus, the game-over route and `002E2240` freeze every actor's movement, scripts and both
  battle-unit sets, and queue only the request's own actor for the fade;
- Stop and the target cursor stop everyone but the chosen actor and leave set 6 alone;
- `seteventtimestop` is the only request that walks all three managers;
- the full-screen menus stop scripts and set 3 only, with record B bits 8 to 14 all set, which
  selects the apply's 1.0 fade;
- the field hold and an event taking an actor keep the focus actor and the type-0 actors moving,
  and the other party members too unless the flag is 1;
- ids 16 to 27 stop no actor at all: they exist for the global bits.

### The apply step

`00226280` runs only while the dirty byte is set and clears it at the end. It ANDs the first
qword of every A and every B record over all twenty-eight slots into one combined pair (a
cancelled slot holds all-ones, the identity), takes the smallest non-negative B `+0x10` as the
fade and resets each such slot to -1, and ORs bit 41 into every slot's B. Then:

- `00226640(allExempt, fade, 0)`, the per-actor pass below, with `allExempt` set when combined B
  bits 8 to 14 are all set;
- A bit 24 and B bit 24: `002EA8E0(0, ~A24)` and `002EA8B0(0, ~B24)`, bit 0 of the two source
  bytes `0215FD44` / `0215FD45` ([party control modes](party-control-modes.md) writes their bit 2);
  the status-error verbs name them: the `ctrldeny` verbs clear A24, the `dispdeny` verbs B24;
- A and B bits 25 to 27: two 16-bit group masks `0209215E` / `02092162` for the effect system
  (`0024B9B0` reads the first; `0024C970` initialises both to `0x3FF`): bit 25 set gives `0x3FF`
  (else 0 for A, `0x3EE` for B), bit 26 clear ORs `0x76`, bit 27 sets or clears bit 1, then
  `0x108` is ORed; when A's word is exactly `0x108` and B's lacks bit 4, A's becomes `0x10C` and
  B's gains bit 2;
- A bit 29: `0035B510(0xFF)` when set, else `0035B4B0(5)`;
- A bit 30 clear: `0025A5D0(1)` sets `02098DEB`; set: clears it;
- A bits 36 and 37: `002547C0` gets `0xF` when bit 36 is set, else `0xE`, with bits 2 and 3
  cleared when bit 37 is clear, the pump argument of [subsystem update
  flags](subsystem-update-flags.md); B bit 36 the same through `00254840` (`01E0C2AC`);
- A bit 39: `002E24C0(0)` sets bit 0 of `0215F1B3` when clear, `002E24E0(0)` clears it when set;
- unless the skip byte `01FD46D1` is set (`00227D30` sets it; the apply clears it instead of
  running this block): the audio group mask from B bits 32, 33 and 40 to 44 through `002DF370`
  and `002DF640` (`01E0CF98` = 0 or `0x100`);
- B bit 35: `002EBBF0(1, B35)`, bit 1 of `0215FD56`, whose zero state sets bit 0 of the render
  table's `+0x48818` (character distance culling);
- the combined A and B are stored at `01FD46A0` and `01FD46B8`; `01FD46B0` and `01FD46C8` receive
  two stack slots the apply never writes, and nothing reads them.

### The per-actor pass and the seven stop sets

`00226640(allExempt, fade, three)` walks three managers (one when `three` is set) and every record.
Each set is a live bitset of request ids plus a pending-set and a pending-clear word; the pass
folds them (`live |= set; live &= ~clear;` both zeroed) and fires the set's hook on a change.

| Set | Live | Pending set / clear | On change | What the live set stops |
|---|---|---|---|---|
| 1 | battle unit `+0x40` (`00359B80`: `[record + 0x30] + 0xED0`) | `+0x54` / `+0x60` | becoming non-zero: `0026D6D0` → `0026D6F0(actor, 0.0, 2)`, the movement speed written to 0 | movement |
| 2 | record `+0x10C` | `+0x110` / `+0x114` | none | the actor's per-step tail in the drive pass `0025DF00`: the animation-driven step `003E6EF0`, the mode word `002681E0`, the movement step `002E5030` and the facing integrator `002E5750` run only when the set is 0 and byte `+0x13` bit 0 is clear, or byte `+0x0B` bit 5 is set; otherwise `002E6310` runs instead; the interpreter refuses at `0025E524` and `00264DF0` refuses the stick |
| 3 | controller `[record + 0xC0] + 0x170` | `+0x174` / `+0x178` | `002E92F0`: `00428FE0(render record, 00264DC0(actor) = 0)`, which writes `+0x304` bit 4 and queues `+0x290` bit 26 or 27 | the additive motions of the character |
| 4 | controller `+0x164` | `+0x168` / `+0x16C` | none | presence: `002E9FE0` and `002E7E90` treat a kind-3 actor with a non-zero set as absent |
| 5 | controller `+0x158` | `+0x15C` / `+0x160` | `002269A0` appends the actor's id to the manager's list `+0x1F0` (count `+0x1F8`) | the fade (below) |
| 6 | battle unit `+0x44` | `+0x4C` / `+0x58` | `00238B40(actor, live ≠ 0 or record byte `+9` bit 5)` → battle unit `+4` bit 5 (`0031B760`) | the unit's stop flag |
| 7 | battle unit `+0x48` | `+0x50` / `+0x5C` | `00312130(actor, live = 0 and that bit clear)` → unit flag bit 36 set while stopped | the unit's flag word |

After each manager's records, when its list is non-empty:

- with `allExempt` clear: `0024FCA0(list)` (mask `0x3FE` to `02092160`, `003B3BA0`, `003B1180`),
  `0024FBF0(list, n, 0.0, fade + 1)` (the global ramp `020926E8` toward `020926EC` = 0.0
  over `020926E6` = fade + 1 frames, stepped by `0024BFD0`), then `002E8B10(actor, 0.0, fade +
  1)` for each listed actor;
- with `allExempt` set: `0024FC80` (mask `0x3FF`), `0024FB90(1.0, fade + 1)` and `002E8B10(actor,
  1.0, fade + 1)`.

`002E8B10` ramps channel 2 of the actor's character render record (`00428940(record, 2, value,
frames)`). `00226A50` and `00226AB0` fold sets 6 and 7 for one actor outside the pass, and
`00263560` drives both hooks for the four roster actors from the hold bytes `02099DE3` to
`02099DE6`, also zeroing their movement speed.

### Cancel, unload and reset

`00225CD0(id, fade)` sets the dirty byte, clears the id's bit, and over all three managers ORs
the bit into every record's seven pending-clear words and removes it from the pending-set words;
then both records' first qwords become all-ones, both `+0x14` bytes 0, and B `+0x10` = fade. Side
calls: id 0 runs `00182DA0` unless the options bit is set, 12 and 17 run `00182D60`, 13 clears
bit 41 of its B and runs `00182D40`, 15 runs `00182D40`.

`00225EB0` cancels every active id with fade -1 the same way (the area unload). `00226B30` resets
everything: bitset, dirty and skip bytes 0, every record's first qword all-ones and `+0x14` 0,
the combined pair all-ones; it does not write the fades, which are 0 from the image until the
first apply resets them to -1.

`00226B10(id)` returns the combined record address, `00226BA0()` is "the combined pair restricts
anything" (`A & B` not all-ones), `00226BC0()` is "any request active" (read by the field frame's
speed-mode block) and `00226BD0(id)` tests one bit (`0025C830` tests 10).

## Layouts

```
01FD4160 + id*0x18  record A: +0 u64 permission bits, +0x14 u8 flag
01FD4400 + id*0x18  record B: +0 u64 permission bits, +0x10 i32 fade (-1 none; 0 before the first apply), +0x14 u8 flag
01FD46A0  u64 combined A      01FD46B8  u64 combined B      01FD46B0 / 01FD46C8  unused copies
01FD46D0  u8 dirty            01FD46D1  u8 skip the audio block once      01FD46D4  u32 active ids
record (actor):  +0x10C u32 set 2 live, +0x110 / +0x114 pending set / clear
controller [record+0xC0]:  +0x158 / +0x15C / +0x160 set 5;  +0x164 / +0x168 / +0x16C set 4;  +0x170 / +0x174 / +0x178 set 3
battle unit [record+0x30]+0xED0:  +0x40 / +0x54 / +0x60 set 1;  +0x44 / +0x4C / +0x58 set 6;  +0x48 / +0x50 / +0x5C set 7
manager: +0x10 bit 0 live, +0x28 exemptions skipped when non-zero, +0x1D6 count, +0x1DE first, +0x1F0 fade list, +0x1F8 its count
02099DE3..02099DE7  u8 hold bytes (02099DE5 / 02099DE6 select ids 5 / 4, 02099DE7 the flag)
0209215E / 02092162  u16 effect group masks     0215FD44 / 0215FD45  u8 source bytes (bit 0)     0215F1B3  u8 (bit 0)
020926E4 u16 flags, 020926E6 u16 frames, 020926E8 f32 value, 020926EC f32 target, 020926F0 f32 step  the fade ramp
```

## Shipped data

| Fact | Value |
|---|---|
| request ids | 28, slots of `0x18` bytes |
| default record | A `0x34FD000000`, B `0x00001F3A09001F1F` (ids 0 to 3, 15, 22 drop A bits 24, 27, 29 and set B bit 24) |
| records per id | the table above, all 28 cases of `00227680` |
| ids never raised | 1, 3, 8, 9, 14, 20, 21 |
| fades passed | 4 (an event taking an actor, its removal), -1 (every other engine site), the verbs' arguments |
| effect masks | `0x3FF` at init, `0x3FE` / `0x3FF` during the fade, `0x76`, `0x108`, `0x10C`, `0x3EE` from the apply |

## Operations

Per request: the start marks every actor's seven pending words and the dirty byte; the next apply
(the wrapper's own, or the field frame's end-of-pass call) ANDs the slots, runs the per-actor
pass and the global switches. Per release: the cancel marks the pending-clear words and writes
all-ones back; the next apply lifts what no other slot still restricts. Per area change: the
unload sweep and, at the next area's boot, the reset and the hold bytes' re-raise.

## State

The active bitset, the dirty and skip bytes, the fifty-six records, the combined pair; per record
the seven live sets and their pending words; per manager the fade list; the hold bytes; the effect
masks and the fade ramp; the source bytes.

## Modding notes

- A set bit exempts; a cleared bit stops. Reading the records the other way inverts all 28.
- The apply trusts the records, not the bitset: a cancel that cleared only the bit would leave the
  restriction in force, which is why `00225CD0` writes all-ones back.
- Only the first qword of each record is intersected; a permission written anywhere else in the
  slot does not compose.
- The shortest fade among pending requests wins and is consumed; a second apply in the same state
  fades over nothing. A fade of 0 becomes one frame (`0024FBF0` and `0024FB90` clamp to 1), and the
  ramp `0024BFD0` advances only while bits 8 and 9 of `020926E4` hold 1 or 2 and frames remain.
- Ids 1, 3, 8, 9, 14, 20 and 21 have records and no raiser: a mod that needs a new freeze can call
  `00226BE0` with one of them and get the record the case builds.
- A request that stops movement for a category also keeps that category's gambits from moving the
  unit, because set 1 writes the movement speed to 0 on the transition.

## Related

- [Frame update order](frame-update-order.md): the end-of-pass apply and the speed-mode test of
  the active bitset.
- [Subsystem update flags](subsystem-update-flags.md): the pump argument the combined A bits 36
  and 37 set.
- [Party control modes](party-control-modes.md): the source bytes' other writer and the rider's
  entry the target cursor passes.
- [Game over](../World-Areas-And-Travel/game-over.md): the route that raises id 22.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the options bit that chooses
  between UI requests 1 and 4.
