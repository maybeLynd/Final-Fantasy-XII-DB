---
title: "Time stop and freeze: how menus, cutscenes, Stop magicks and skippable scenes halt actors"
kind: "system"
category: "Engine core"
addresses: "0x00226BE0, 0x00227680, 0x00226280, 0x00226640, 0x002269A0, 0x00225CD0, 0x00225EB0, 0x00226B30, 0x00226B10, 0x00226BA0, 0x00226BC0, 0x00226BD0, 0x00263FF0, 0x00358940, 0x00359B80, 0x003590D0, 0x003588B0, 0x00263750, 0x002647B0, 0x00263BE0, 0x00227370, 0x002273B0, 0x002273E0, 0x00227420, 0x00227460, 0x002274A0, 0x002274E0, 0x00227510, 0x00227550, 0x00227590, 0x002275D0, 0x00227610, 0x00227640, 0x002260A0, 0x002260C0, 0x002260E0, 0x00226100, 0x00226120, 0x00226140, 0x00226160, 0x00226180, 0x002261B0, 0x002261E0, 0x00226210, 0x00226240, 0x00226260, 0x00254740, 0x00255290, 0x00252D90, 0x002544C0, 0x002DDC30, 0x003B3B40, 0x00263480, 0x0026A1D0, 0x00266D10, 0x00263560, 0x00263230, 0x00263050, 0x0026B980, 0x0026B970, 0x00377700, 0x0034DC30, 0x00343CE0, 0x00350400, 0x00350940, 0x002E2440, 0x002E2400, 0x002E06B0, 0x00353D90, 0x00354800, 0x003531A0, 0x00353A60, 0x00354300, 0x003535F0, 0x0026C3E0, 0x0026C5D0, 0x00263660, 0x00265680, 0x00346860, 0x00352000, 0x0025C830, 0x0025C170, 0x0025B500, 0x002678C0, 0x0025D580, 0x0033F940, 0x0035C7B0, 0x0027EFA0, 0x00341D20, 0x003420F0, 0x00341360, 0x00341790, 0x00360710, 0x0034ECF0, 0x0034E6D0, 0x003603F0, 0x002E2240, 0x00313DB0, 0x0031E860, 0x002EA8B0, 0x002EA8E0, 0x002E24C0, 0x002E24E0, 0x0025A5D0, 0x002547C0, 0x00254840, 0x0035B4B0, 0x0035B510, 0x002DF370, 0x002DF640, 0x002EBBF0, 0x0024B9B0, 0x0024C970, 0x0026D6D0, 0x0026D6F0, 0x002E92F0, 0x00264DC0, 0x00428FE0, 0x00238B40, 0x00312130, 0x0031B760, 0x002E9FE0, 0x002E7E90, 0x0025DF00, 0x0024FCA0, 0x0024FBF0, 0x0024FC80, 0x0024FB90, 0x002E8B10, 0x00428940, 0x0024BFD0, 0x00226A50, 0x00226AB0, 0x00182D10, 0x00182D40, 0x00182D60, 0x00182DA0, 0x00182CD0, 0x00182CF0, 0x00227D30, 0x0022A770, 0x0026A290"
---

## What the player sees

Open the main menu in the field and everyone stops mid-step. When an action is shown on its own,
the rest of the field holds while the acting unit keeps moving. Enter a
conversation and the talking actors play while the scene around them waits. Skip a scene and the
world resumes cleanly. Each of these is a different request to one registry, and the differences
between them, who keeps moving, whether only scripts freeze or animation too, which sound groups
mute, come from a small permission record written for each request.

Requests stack. While a menu and a Stop are both active, every actor obeys the stricter of the
two, and when one is released the other still holds. The chocobo's rider, the party leader and
the actor a cutscene names are the exemptions the records carve out.

## How it works

### The request slots

There are twenty-eight request ids. Each has two records, A at `0x01FD4160 + id × 0x18` and B at
`0x01FD4400 + id × 0x18`: a qword of permission bits at `+0`, a fade length at B `+0x10` and a flag
byte at `+0x14`. The bitset `0x01FD46D4` holds the active ids, the dirty byte `0x01FD46D0` tells the
apply step that something changed, and `0x01FD46A0` / `0x01FD46B8` hold the last combined A and B.

A set bit in a record is an exemption. For a category `c` from 0 to 6: A bit `c` exempts the
category from set 1, A bit `8 + c` from set 2, A bit `0x10000000` together with bit `8 + c` from set 3,
B bit `c` from set 4, B bit `8 + c` from set 5, A bit `16 + c` from set 6 and B bit `16 + c` from
set 7.

The categories:

- 0: the party focus actor (`0x003590D0()` through `0x003588B0`);
- 1: the other roster entries (`0x00263750(0..3)` minus the focus);
- 5: the request's own actor; 6: the request's handle list;
- 2, 3, 4: every other managed actor not in a party slot (`0x002647B0`: byte `+0x12` below 4), by
  the type class `0x00263BE0` gives from the low nibble of byte `+0x0E`: 3 for types 1, 2 and 7, 4
  for type 3, and 2 for anything else.

### Starting a request

`0x00226BE0(id, actor, count, handles, fade, flag)` returns at once when the id's bit is set.
Otherwise:

1. the fade goes to B `+0x10`; `0x00227680(id, A, B, max(flag, 0))` builds the records, the flag
   landing at B `+0x14`; the bit and the dirty byte are set;
2. one actor manager is walked when A bit `0x80000000` is set, three when it is clear (`0x00263FF0(m)`, live
   when its `+0x10` bit `0x1` holds): every record from `+0x1DE` for `+0x1D6` entries (`0x00358940`)
   gets the id's bit OR-ed into its seven pending-set words and cleared from its seven
   pending-clear words;
3. for a manager whose `+0x28` is 0, the exemptions: for each category the id's bit is removed
   again from the pending-set word of every set whose record bit is set.

Nothing stops yet: the apply does that.

`0x00227680` starts both records from one default (A bits 24, 26 to 31, 34, 36 and 37; B bits `0x1` to
4, 8 to 12, 24, 27, 33, 35 to 37 and 40 to 44) and then runs the id's case; ids 4, 6 and 7 also
read the flag. Ids 0, 1, 2, 3, 15, 22 and 27 share one case, 4, 6 and 7 another, 8 and 9, 16, 20
and 21, 17 to 19, 23 and 25, 24 and 26 are pairs; id 0 runs `0x00182D10` unless the options bit `0x8`
(`0x002DDC30`, the Battle Mode setting, [game settings](../Saving-Loading-And-Settings/game-settings.md))
is set, id 12 and 17 run `0x00182CF0`, 13 and 15 run `0x00182CD0`.

Those side calls set one bit of the input manager's movement-key mode byte `+0x3A` and mark
`+0x3B`: `0x00182D10` bit `0x2` (`0x00198690`), `0x00182CF0` bit `0x1` (`0x001986B0`) and `0x00182CD0` bit `0x4`
(`0x00198670`); the cancel side calls below, `0x00182DA0`, `0x00182D60` and `0x00182D40`, clear the same
bits ([controls](../Controls-And-Input/controls.md)).

### The twenty-eight requests

| Id | Raised by | Released by |
|---|---|---|
| 0 | UI request 1 (the battle menu) with the options bit clear, request 4 with it set, request 20 always (`0x00254740` through `0x00255290`) | the UI close (`0x00252D90`, `0x002544C0`), fade -1 |
| 2 | UI requests 3 and 24 | the same |
| 4, 5, 7 | the field hold `0x00263480(actor, mode)`: mode 1 raises 4, mode 0 raises 5, mode 2 raises 7 with the actor as a one-entry handle list (an empty list when the actor is null); the flag is `0x02099DE7` = 0; the boot `0x00266D10` raises 4 and 5 from the hold bytes `0x02099DE6` / `0x02099DE5`; `0x0026A1D0(on, flag)` raises 5 | `0x00263480` with both hold bytes clear, `0x0026A1D0` with `on` clear and the boot cancel 5, 4 and 7 |
| 6 | an event script taking an actor (`0x00263230`, fade 4, flag `0x00377700()`) and the verb `talkfadeout(fade)` (`0x0026B980`) | the entry's removal (`0x00263050`, fade 4) and `talkfadein(fade)` (`0x0026B970`) |
| 10 | `settimestopmagic` (`0x00350400` → `0x00227460`, with apply) and the action display `0x00313DB0`, which raises it for the unit whose action is being shown one at a time ([Action phases](../Battle-Actions/action-phases.md); the acting unit's id as the actor; at party-control level 2 the rider's entry as the handle list) | `cleartimestopmagic` (`0x00350940` → `0x00226120`, fade -1) and the display's release |
| 11 | `seteventtimestop(1)` (`0x0034DC30` → `0x002273B0`, no apply) | `seteventtimestop(0)` (`0x002260C0`) |
| 12 | `settutorial00timestop(1)` (`0x00343CE0` → `0x00227610`) | the same verb with 0 (`0x00226240`) |
| 13 | UI requests 2, 6, 15, 17, 18, 19 and 22 (the full-screen menus) | the UI close |
| 15 | `0x002E2240(1)`, which also moves the main loop to state 6 ([frame update order](frame-update-order.md)) | `0x002E2240(0)`, which moves it to state 2 |
| 16 | `maskopen`, `maskopenfast`, `mesvmaskopen`, `mesvmaskopenfast` (`0x002E2440` → `0x002274E0`) | `maskclose`, `maskclosefast` (`0x002E2400` → `0x00226160`), the area unload `0x002E06B0` |
| 17 | `ucon` / `ucon_4a5` (`0x0026C5D0`), `0x0026C3E0`, `0x00263660` (from the area unload `0x002628B0`, the drive pass `0x0025D9E0`, the tick `0x00314020`, `0x0026CE60`, `0x0026B8A0`, `0x0026B8C0` and `0x0026C8C0`): raised when `0x00265680()` is 0, else released, each followed by the apply | the same bodies |
| 18 | `0x0025C830` (← `0x0025C170`) through `0x00227420`, with apply | `0x0025B500` through `0x00226100` once its count `0x02099DB8` reaches 0, then `0x002E1CD0(1)`; the apply is left to the field frame |
| 19 | the definition load `0x002678C0`, with apply | `clearmapjumpstatus` (`0x0033F940` → `0x0025D580`), with apply |
| 22 | `0x0035C7B0(0x0B)` on the game-over route `0x0027EFA0` ([game over](../World-Areas-And-Travel/game-over.md)), with apply | UI request 11's close (`0x002260A0`) |
| 23, 24 | `setstatuserrordispdenystatus(1)` (`0x00227550`), `setstatuserrorctrldenystatus(1)` (`0x00227510`), with apply | the same verbs with 0 (`0x002261B0`, `0x00226180`), with apply |
| 25, 26 | `…dispdenystatus_by_menu(1)` (`0x002275D0`), `…ctrldenystatus_by_menu(1)` (`0x00227590`), with apply | the same verbs with 0 (`0x00226210`, `0x002261E0`), with apply |
| 27 | `skipexec` (`0x0034ECF0` → `0x00360710` → `0x002273E0`) | `skipend` (`0x0034E6D0` → `0x002260E0`), the area unload `0x003603F0` |
| 1, 3, 8, 9, 14, 20, 21 | nothing: no wrapper and no direct call carries these ids | |

The start wrappers from `0x00227370` to `0x00227640` and the cancel wrappers from `0x002260A0` to
`0x00226260` test the id's bit first, except the starts for 11, 12 and 16, which rely on
`0x00226BE0`'s own held-bit return; a repeated request is ignored either way. The start wrappers for
10, 18, 22, 23, 24, 25 and 26 and the cancel wrappers for 23 to 26 run the apply themselves; the
others leave it to the field frame, which runs `0x00226280` at the end of every pass ([frame update
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

- the menus, the game-over route and `0x002E2240` freeze every actor's movement, scripts and both
  battle-unit sets, and queue only the request's own actor for the fade;
- `settimestopmagic` and the action display stop everyone but the chosen actor and leave set 6 alone;
- `seteventtimestop` is the only request that walks all three managers;
- the full-screen menus stop scripts and set 3 only, with record B bits 8 to 14 all set, which
  selects the apply's 1.0 fade;
- the field hold and an event taking an actor keep the focus actor and the type-0 actors moving,
  and the other party members too unless the flag is 1;
- ids 16 to 27 stop no actor at all: they exist for the global bits.

### The apply step

`0x00226280` runs only while the dirty byte is set and clears it at the end. It ANDs the first
qword of every A and every B record over all twenty-eight slots into one combined pair (a
cancelled slot holds all-ones, the identity), takes the smallest non-negative B `+0x10` as the
fade and resets each such slot to -1, and ORs bit `0x20000000000` into every slot's B. Then:

- `0x00226640(allExempt, fade, 0)`, the per-actor pass below, with `allExempt` set when combined B
  bits 8 to 14 are all set;
- A bit `0x1000000` and B bit `0x1000000`: `0x002EA8E0(0, ~A24)` and `0x002EA8B0(0, ~B24)`, bit `0x1` of the two source
  bytes `0x0215FD44` / `0x0215FD45` ([party control modes](party-control-modes.md) writes their bit `0x4`);
  the status-error verbs name them: the `ctrldeny` verbs clear A24, the `dispdeny` verbs B24;
- A and B bits 25 to 27: two 16-bit group masks `0x0209215E` / `0x02092162` for the effect system
  (`0x0024B9B0` reads the first; `0x0024C970` initialises both to `0x3FF`): bit `0x2000000` set gives `0x3FF`
  (else 0 for A, `0x3EE` for B), bit `0x4000000` clear ORs `0x76`, bit `0x8000000` sets or clears bit `0x2`, then
  `0x108` is ORed; when A's word is exactly `0x108` and B's lacks bit `0x10`, A's becomes `0x10C` and
  B's gains bit `0x4`;
- A bit `0x20000000`: `0x0035B510(0xFF)` when set, else `0x0035B4B0(5)`;
- A bit `0x40000000` clear: `0x0025A5D0(1)` sets `0x02098DEB`; set: clears it;
- A bits `0x1000000000` and `0x2000000000`: `0x002547C0` gets `0xF` when bit `0x1000000000` is set, else `0xE`, with bits `0x4` and `0x8`
  cleared when bit `0x2000000000` is clear, the pump argument of [subsystem update
  flags](subsystem-update-flags.md); B bit `0x1000000000` the same through `0x00254840` (`0x01E0C2AC`);
- A bit `0x8000000000`: `0x002E24C0(0)` sets bit `0x1` of `0x0215F1B3` when clear, `0x002E24E0(0)` clears it when set;
- unless the skip byte `0x01FD46D1` is set (`0x00227D30` sets it; the apply clears it instead of
  running this block): the audio group mask from B bits 32, 33 and 40 to 44 through `0x002DF370`
  and `0x002DF640` (`0x01E0CF98` = 0 or `0x100`);
- B bit `0x800000000`: `0x002EBBF0(1, B35)`, bit `0x2` of `0x0215FD56`, whose zero state sets bit `0x1` of the render
  table's `+0x48818` (character distance culling);
- the combined A and B are stored at `0x01FD46A0` and `0x01FD46B8`; `0x01FD46B0` and `0x01FD46C8` receive
  two stack slots the apply never writes, and nothing reads them.

### The per-actor pass and the seven stop sets

`0x00226640(allExempt, fade, three)` walks three managers (one when `three` is set) and every record.
Each set is a live bitset of request ids plus a pending-set and a pending-clear word; the pass
folds them (`live |= set; live &= ~clear;` both zeroed) and fires the set's hook on a change.

| Set | Live | Pending set / clear | On change | What the live set stops |
|---|---|---|---|---|
| 1 | battle unit `+0x40` (`0x00359B80`: `[record + 0x30] + 0xED0`) | `+0x54` / `+0x60` | becoming non-zero: `0x0026D6D0` → `0x0026D6F0(actor, 0.0, 2)`, the movement speed written to 0 | movement |
| 2 | record `+0x10C` | `+0x110` / `+0x114` | none | the actor's per-step tail in the drive pass `0x0025DF00`: the animation-driven step `0x003E6EF0`, the mode word `0x002681E0`, the movement step `0x002E5030` and the facing integrator `0x002E5750` run only when the set is 0 and byte `+0x13` bit `0x1` is clear, or byte `+0x0B` bit `0x20` is set; otherwise `0x002E6310` runs instead; the interpreter refuses at `0x0025E524` and `0x00264DF0` refuses the stick |
| 3 | controller `[record + 0xC0] + 0x170` | `+0x174` / `+0x178` | `0x002E92F0`: `0x00428FE0(render record, 0x00264DC0(actor) = 0)`, which writes `+0x304` bit `0x10` and queues `+0x290` bit `0x4000000` or `0x8000000` | the additive motions of the character |
| 4 | controller `+0x164` | `+0x168` / `+0x16C` | none | presence: `0x002E9FE0` and `0x002E7E90` treat a kind-3 actor with a non-zero set as absent |
| 5 | controller `+0x158` | `+0x15C` / `+0x160` | `0x002269A0` appends the actor's id to the manager's list `+0x1F0` (count `+0x1F8`) | the fade (below) |
| 6 | battle unit `+0x44` | `+0x4C` / `+0x58` | `0x00238B40(actor, live ≠ 0 or record byte `+9` bit 0x20)` → battle unit `+4` bit `0x20` (`0x0031B760`) | the unit's stop flag |
| 7 | battle unit `+0x48` | `+0x50` / `+0x5C` | `0x00312130(actor, live = 0 and that bit clear)` → unit flag bit `0x1000000000` set while stopped | the unit's flag word |

After each manager's records, when its list is non-empty:

- with `allExempt` clear: `0x0024FCA0(list)` (mask `0x3FE` to `0x02092160`, `0x003B3BA0`, `0x003B1180`),
  `0x0024FBF0(list, n, 0.0, fade + 1)` (the global ramp `0x020926E8` toward `0x020926EC` = 0.0
  over `0x020926E6` = fade + 1 frames, stepped by `0x0024BFD0`), then `0x002E8B10(actor, 0.0, fade +
  1)` for each listed actor;
  - `0x0024FBF0` also raises bit `0x4` of `+0x368` on every kind-1 active effect (`0x002FD090`, `0x0024FC58`) and, by a
    tail jump to `0x003B1050(list, n)` (`0x0024FC6C`), on the kind-5 effects owned by the listed actors;
- with `allExempt` set: `0x0024FC80` (mask `0x3FF`), `0x0024FB90(1.0, fade + 1)` and `0x002E8B10(actor,
  1.0, fade + 1)`.

`0x002E8B10` ramps channel 2 of the actor's character render record (`0x00428940(record, 2, value,
frames)`). `0x00226A50` and `0x00226AB0` fold sets 6 and 7 for one actor outside the pass, and
`0x00263560` drives both hooks for the four roster actors from the hold bytes `0x02099DE3` to
`0x02099DE6`, also zeroing their movement speed.

At run time only `0x0026A290` writes `0x02099DE3`: it is the handler of the verb `setmutekiparty`
(`0x0337`, through `0x003452B0`), stores the popped value there and runs `0x00263560`. With manager 0
active (`0x02098E20` bit `0x1`) a non-zero
value raises the battle-unit stop flag and flag bit `0x1000000000` of every roster member and sets their
record byte `+0x09` bit `0x80`, and 0 clears them again while the other hold bytes are 0.

### Cancel, unload and reset

`0x00225CD0(id, fade)` sets the dirty byte, clears the id's bit, and over all three managers ORs
the bit into every record's seven pending-clear words and removes it from the pending-set words;
then both records' first qwords become all-ones, both `+0x14` bytes 0, and B `+0x10` = fade. Side
calls: id 0 runs `0x00182DA0` unless the options bit is set, 12 and 17 run `0x00182D60`, 13 clears
bit `0x20000000000` of its B and runs `0x00182D40`, 15 runs `0x00182D40`.

`0x00225EB0` cancels every active id with fade -1 the same way (the area unload). `0x00226B30` resets
everything: bitset, dirty and skip bytes 0, every record's first qword all-ones and `+0x14` 0,
the combined pair all-ones; it does not write the fades, which are 0 from the image until the
first apply resets them to -1.

`0x00226B10(id)` returns the combined record address, `0x00226BA0()` is "the combined pair restricts
anything" (`A & B` not all-ones), `0x00226BC0()` is "any request active" (read by the field frame's
speed-mode block) and `0x00226BD0(id)` tests one bit (`0x0025C830` tests 10).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01FD4160` | `...` | record A, 0x18 bytes per id at 0x01FD4160 + id*0x18 (below) |  |
| `0x01FD4400` | `...` | record B, 0x18 bytes per id at 0x01FD4400 + id*0x18 (below) |  |
| `0x01FD46A0` | `u64` | combined A |  |
| `0x01FD46B8` | `u64` | combined B |  |
| `0x01FD46B0` | `...` | unused copies | with `0x01FD46C8` |
| `0x01FD46C8` | `...` | unused copies | with `0x01FD46B0` |
| `0x01FD46D0` | `u8` | dirty |  |
| `0x01FD46D1` | `u8` | skip the audio block once |  |
| `0x01FD46D4` | `u32` | active ids |  |
| `0x02099DE3` | `...` | hold bytes 0x02099DE3 to 0x02099DE7, u8 each (0x02099DE5 / 0x02099DE6 select ids 5 / 4, 0x02099DE7 the flag) |  |
| `0x0209215E` | `u16` | effect group masks | with `0x02092162` |
| `0x02092162` | `u16` | effect group masks | with `0x0209215E` |
| `0x0215FD44` | `u8` | source bytes (bit 0x1) | with `0x0215FD45` |
| `0x0215FD45` | `u8` | source bytes (bit 0x1) | with `0x0215FD44` |
| `0x0215F1B3` | `u8` | source byte (bit 0x1) |  |
| `0x020926E4` | `u16` | flags | the fade ramp |
| `0x020926E6` | `u16` | frames | the fade ramp |
| `0x020926E8` | `f32` | value | the fade ramp |
| `0x020926EC` | `f32` | target | the fade ramp |
| `0x020926F0` | `f32` | step | the fade ramp |

Record A:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | permission bits |  |
| `+0x14` | `u8` | flag |  |

Record B:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | permission bits |  |
| `+0x10` | `i32` | fade (-1 none; 0 before the first apply) |  |
| `+0x14` | `u8` | flag |  |

Record (actor):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10C` | `u32` | set 2 live |  |
| `+0x110` | `...` | pending set |  |
| `+0x114` | `...` | pending clear |  |

Controller [record+`0xC0`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x158` | `...` | set 5 | with `+0x15C` and `+0x160` |
| `+0x15C` | `...` | set 5 | with `+0x158` and `+0x160` |
| `+0x160` | `...` | set 5 | with `+0x158` and `+0x15C` |
| `+0x164` | `...` | set 4 | with `+0x168` and `+0x16C` |
| `+0x168` | `...` | set 4 | with `+0x164` and `+0x16C` |
| `+0x16C` | `...` | set 4 | with `+0x164` and `+0x168` |
| `+0x170` | `...` | set 3 | with `+0x174` and `+0x178` |
| `+0x174` | `...` | set 3 | with `+0x170` and `+0x178` |
| `+0x178` | `...` | set 3 | with `+0x170` and `+0x174` |

Battle unit [record+`0x30`]`+0xED0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x40` | `...` | set 1 | with `+0x54` and `+0x60` |
| `+0x54` | `...` | set 1 | with `+0x40` and `+0x60` |
| `+0x60` | `...` | set 1 | with `+0x40` and `+0x54` |
| `+0x44` | `...` | set 6 | with `+0x4C` and `+0x58` |
| `+0x4C` | `...` | set 6 | with `+0x44` and `+0x58` |
| `+0x58` | `...` | set 6 | with `+0x44` and `+0x4C` |
| `+0x48` | `...` | set 7 | with `+0x50` and `+0x5C` |
| `+0x50` | `...` | set 7 | with `+0x48` and `+0x5C` |
| `+0x5C` | `...` | set 7 | with `+0x48` and `+0x50` |

Manager:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x010` | `...` | bit 0x1 live |  |
| `+0x028` | `...` | exemptions skipped when non-zero |  |
| `+0x1D6` | `...` | count |  |
| `+0x1DE` | `...` | first |  |
| `+0x1F0` | `...` | fade list |  |
| `+0x1F8` | `...` | its count |  |

## Shipped data

| Fact | Value |
|---|---|
| request ids | 28, slots of `0x18` bytes |
| default record | A `0x34FD000000`, B `0x00001F3A09001F1F` (ids 0 to 3, 15, 22 drop A bits `0x1000000`, `0x8000000`, `0x20000000` and set B bit `0x1000000`) |
| records per id | the table above, all 28 cases of `0x00227680` |
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
  restriction in force, which is why `0x00225CD0` writes all-ones back.
- Only the first qword of each record is intersected; a permission written anywhere else in the
  slot does not compose.
- The shortest fade among pending requests wins and is consumed; a second apply in the same state
  fades over nothing. A fade of 0 becomes one frame (`0x0024FBF0` and `0x0024FB90` clamp to 1), and the
  ramp `0x0024BFD0` advances only while bits `0x100` and `0x200` of `0x020926E4` hold 1 or 2 and frames remain.
- Ids 1, 3, 8, 9, 14, 20 and 21 have records and no raiser: a mod that needs a new freeze can call
  `0x00226BE0` with one of them and get the record the case builds.
- A request that stops movement for a category also keeps that category's gambits from moving the
  unit, because set 1 writes the movement speed to 0 on the transition.

## Related

- [Frame update order](frame-update-order.md): the end-of-pass apply and the speed-mode test of
  the active bitset.
- [Subsystem update flags](subsystem-update-flags.md): the pump argument the combined A bits `0x1000000000`
  and 37 set.
- [Party control modes](party-control-modes.md): the source bytes' other writer and the rider's
  entry the action display passes.
- [Game over](../World-Areas-And-Travel/game-over.md): the route that raises id 22.
- [Game settings](../Saving-Loading-And-Settings/game-settings.md): the options bit that chooses
  between UI requests 1 and 4.
