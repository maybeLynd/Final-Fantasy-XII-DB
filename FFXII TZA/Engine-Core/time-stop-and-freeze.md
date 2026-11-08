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
byte at B `+0x14` (A `+0x14` is only ever cleared). The bitset `0x01FD46D4` holds the active ids, the dirty
byte `0x01FD46D0` tells the
apply step that something changed, and `0x01FD46A0` / `0x01FD46B8` hold the last combined A and B.

A set bit in a record is an exemption. For a category `c` from 0 to 6: A bit `c` exempts the
category from set 1, A bit `8 + c` from set 2, A bit `0x10000000` together with bit `8 + c` from set 3,
B bit `c` from set 4, B bit `8 + c` from set 5, A bit `16 + c` from set 6 and B bit `16 + c` from
set 7.

The categories:

- 0: the party leader (`0x003590D0()` through `0x003588B0`, [Party leader](../Party/party-leader.md));
- 1: the other roster entries (`0x00263750(0..3)` minus the focus);
- 5: the request's own actor; 6: the request's handle list;
- 2, 3, 4: every other managed actor not in a party slot (`0x002647B0`: byte `+0x12` below 4), by
  the type class `0x00263BE0` gives from the actor class nibble, the low nibble of byte `+0x0E`: 3 for types 1, 2 and 7, 4
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
3. the exemptions: for each category the id's bit is removed again from the pending-set word of every set whose
   record bit is set; a manager whose `+0x28` is non-zero skips those of categories 0, 1, 5 and 6 (`0x00226D99`).

Nothing stops yet: the apply does that.

`0x00227680` starts both records from one default (A bits under mask `0x34FD000000`; B bits under mask
`0x1F3A09001F1F`) and then runs the id's case; ids 4, 6 and 7 also
read the flag. Ids 0, 1, 2, 3, 15, 22 and 27 share one case, 4, 6 and 7 another, 16, 20 and 21 another and
17 to 19 another; 8 and 9, 23 and 25, and 24 and 26 are pairs; id 0 runs `0x00182D10` unless the options bit `0x8`
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
| 4, 5, 7 | the field hold `0x00263480(actor, mode)` while `0x02099DE5` or `0x02099DE6` is non-zero: mode 1 raises 4, mode 0 raises 5, mode 2 raises 7 with the actor as a one-entry handle list (its handle from `0x003589B0`; an empty list when the actor is null) and any other mode raises 4 as well; the request's own actor is null, the fade -1, the flag is `0x02099DE7` = 0 and the apply follows (`0x0026351D`); the boot `0x00266D10` raises 4 and 5 from the hold bytes `0x02099DE6` / `0x02099DE5`; `0x0026A1D0(on, flag)` raises 5 while `on` or `0x02099DE5` is non-zero, with apply (below) | `0x00263480` with both hold bytes clear, `0x0026A1D0` with `on` clear and the boot cancel 5, 4 and 7; `0x0026A1D0` cancels only while `0x02099DE5` is clear too, and both bodies cancel through `0x00225CD0` with fade -1, without the bit test and without the apply (`0x0026352A`-`0x00263540`, `0x0026A258`-`0x0026A27D`) |
| 6 | an event script taking an actor (`0x00263230`, fade 4, flag `0x00377700()`; only while `0x02099DB4` is 0 or below, `0x0209A2A8` is non-zero and the actor's byte `+0x0C` bit `0x80` is clear, `0x0026324D`-`0x002632AD`) and the verb `talkfadeout(fade)` (`0x0026B980`; its thunk `0x00345E50` gives the flag argument -1, which takes the flag `0x00377700() != 0`, and a non-negative argument passes `argument == 0`); the request's own actor is null and neither runs the apply ([world lock](../Scripts-And-Script-Commands/world-lock.md)) | the entry's removal (`0x00263050`, fade 4: `0x00225CD0` directly, once the summed count `0x02099DB4` is 0 or below and only while `0x0209A2A8` is non-zero and the actor's byte `+0x0C` bit `0x80` is clear, `0x00263128`-`0x00263141`) and `talkfadein(fade)` (`0x0026B970`) |
| 10 | `settimestopmagic` (`0x00350400` → `0x00227460`, with apply) and the action display `0x00313DB0`, which raises it for the unit whose action is being shown one at a time ([Action phases](../Battle-Actions/action-phases.md); the acting unit's id as the actor; at party-control level 2 the rider's entry `0x0031E860(0x00327200())`, when non-zero, as a one-entry handle list; fade -1 and flag -1 (`0x00313E52`-`0x00313E98`); the display then runs the apply `0x00226280`, the sound stop `0x002DEE70` and `0x00313A00` itself, `0x00313E9D`-`0x00313EA7`) | `cleartimestopmagic` (`0x00350940` → `0x00226120`, fade -1) and the display's release, `0x00225CD0(10, -1)` (`0x00313F04`), which leaves the apply to the field frame |
| 11 | `seteventtimestop(1)` (`0x0034DC30` → `0x002273B0`, no apply) | `seteventtimestop(0)` (`0x002260C0`) |
| 12 | `settutorial00timestop(1)` (`0x00343CE0` → `0x00227610`) | the same verb with 0 (`0x00226240`) |
| 13 | UI requests 2, 6, 15, 17, 18, 19 and 22 (the full-screen menus) | the UI close |
| 15 | `0x002E2240(1)`, which first sets bits `0x100203` of action row 7 `0x0215F1DC` (`0x002E2248`, [action availability](../Controls-And-Input/action-availability.md)), also moves the main loop to state 6 ([frame update order](frame-update-order.md)) and raises the id through `0x002274A0` (`0x002E2260`) | `0x002E2240(0)`, which clears those bits (`0x002E2265`), moves it to state 2 and releases the id through `0x00226140` (`0x002E227D`) |
| 16 | `maskopen` (`0x00353D90`), `maskopenfast` (`0x003531A0`), `mesvmaskopen` (`0x00354300`), `mesvmaskopenfast` (`0x003535F0`) (`0x002E2440` → `0x002274E0`, on every path: `0x002E245A`; below) | `maskclose` (`0x00354800`), `maskclosefast` (`0x00353A60`) (`0x002E2400` → `0x00226160`, on every path: `0x002E2412`), the area unload `0x002E06B0` (below) |
| 17 | `ucon` / `ucon_4a5` (`0x0026C5D0`), `0x0026C3E0`, `0x00263660` (from the area unload `0x002628B0`, the drive pass `0x0025D9E0`, the tick `0x00314020`, `0x0026CE60`, `0x0026B8A0`, `0x0026B8C0` and `0x0026C8C0`): raised when `0x00265680()` is 0, else released, each followed by the apply, only while manager 0 is live with `0x02098E21` bit `0x1` and `0x02098E20` bit `0x80` clear (below) | the same bodies |
| 18 | `0x0025C830` (← `0x0025C170`, below) through `0x00227420`, with apply | `0x0025B500` through `0x00226100` once its count `0x02099DB8`, the sum over the live managers, reaches 0 or below, then `0x002E1CD0(1, 13)` (below); the apply is left to the field frame |
| 19 | the definition load `0x002678C0` (`0x00226BE0(19, 0, 0, 0, -1, -1)` at `0x00267915`, below), with apply | `clearmapjumpstatus` (`0x0033F940` → `0x0025D580`: `0x00225CD0(19, -1)` at `0x0025D5BE`, without the bit test; below), with apply |
| 22 | `0x0035C7B0(0x0B)` on the game-over route `0x0027EFA0` ([game over](../World-Areas-And-Travel/game-over.md)), and through `0x0035C7A0(0x0B)` from the field frame's wipe post `0x00234590` and the verb `callgameover` (`0x00237D60`); `0x0035C7B0` calls `0x00227370` (`0x0035C810`) only for kind `0x0B` and only past its refusal tests (`0x0035C7BA`-`0x0035C7ED`), with apply | UI request 11's close (`0x002260A0`) |
| 23, 24 | `setstatuserrordispdenystatus(1)` (`0x00227550`), `setstatuserrorctrldenystatus(1)` (`0x00227510`), with apply | the same verbs with 0 (`0x002261B0`, `0x00226180`), with apply |
| 25, 26 | `…dispdenystatus_by_menu(1)` (`0x002275D0`), `…ctrldenystatus_by_menu(1)` (`0x00227590`), with apply | the same verbs with 0 (`0x00226210`, `0x002261E0`), with apply |
| 27 | `skipexec` (`0x0034ECF0` → `0x00360710` → `0x002273E0`), and `0x00360880` (from `0x00228130` on message 18 while bit `0x2000` of the dword at `+8` of its first argument's `+0xC0` pointer is set, `0x002281B7`, which clears the bit after it, `0x002281C3`): for each of the masks `0x022CB9C4`, `0x022CB9C8` and `0x022CB9CC` (managers 1 to 3) that is non-zero it runs `0x00360710(entry, manager)` for the lowest of its bits `0x1` to `0x80` that is set | `skipend` (`0x0034E6D0` → `0x002260E0`), the area unload's skip sweep `0x003603F0(manager)` (from `0x002628B0`, `0x0026293F`), which ends the manager's eight skip entries with `0x00360A50` and, after each one that had executed (state 2), clears bit `0x8000` of `0x022CB720` (`0x003601C0(0xF)`); only when one had executed does it run `0x003600D0`, `0x003601C0(0xF)`, `0x002EFA70(4, 8, 1, 0)` and the release `0x002260E0` (`0x00360432`-`0x00360458`) |
| 1, 3, 8, 9, 14, 20, 21 | nothing: no wrapper and no direct call carries these ids | |

The six mask verbs pop their argument with `0x00267E10` and drop it. `maskopenfast` runs `0x002E2440(1, 0)` and
`mesvmaskopenfast` `0x002E2440(1, 1)`; each then calls `0x002E1C40(0, 3)`, which sets bit `0x8` of the HUD hide word
`0x0215F1AC` and clears it in `0x0215F1B4`, and `0x002E1C70(1, 3)`, which sets bit `0x8` of `0x0215F1B4`
(`0x003531B1`-`0x003531CE`, `0x00353603`-`0x00353620`). `maskclosefast` runs `0x002E2400(1)`, then `0x002E1C40(1, 3)`,
which clears bit `0x8` in both words, and `0x002E1C70(1, 3)` (`0x00353A71`-`0x00353A8F`).

`maskopen`, `mesvmaskopen` and `maskclose` first read the skip byte `0x02099011 + manager × 0x288` of the calling
actor's manager (byte `+0x15`) through `0x00267310` (`0x00353D9D`, `0x0035430D`, `0x0035480D`). While it is set they run
their fast form's three calls with the same arguments. While it is clear they run `0x002E2440(0, 0)`,
`0x002E2440(0, 1)` or `0x002E2400(0)` and end with `0x002E1C40(0, 3)` for the two opens and `0x002E1C40(1, 3)` for the
close, without `0x002E1C70` (`0x00353DD6`-`0x00353DF0`, `0x00354348`-`0x00354365`, `0x00354847`-`0x00354860`).

Every path of the six reaches `0x002E2440`, which starts id 16 through `0x002274E0` (`0x002E245A`), or `0x002E2400`, which
releases it through `0x00226160` (`0x002E2412`), whatever the arguments.

The start wrappers from `0x00227370` to `0x00227640` and the cancel wrappers from `0x002260A0` to
`0x00226260` test the id's bit first, except the starts for 11, 12 and 16, which rely on
`0x00226BE0`'s own held-bit return; a repeated request is ignored either way. The start wrappers for
10, 18, 22, 23, 24, 25 and 26 and the cancel wrappers for 23 to 26 run the apply themselves; the
others leave it to the field frame, which runs `0x00226280` at the end of every pass ([frame update
order](frame-update-order.md)).

The UI requests take their id from `0x00255290(mode & 0x7FFF)`, which the
[game settings](../Saving-Loading-And-Settings/game-settings.md) tabulate. `0x00254740(mode)` returns at once when that
gives -1 (`0x0025475D`); otherwise it raises the id with no actor, no handles, fade -1 and flag -1 (`0x0025479D`) and
runs the apply itself (`0x002547A2`). Before the raise it sets bit `0x1` of `0x02EBDBBC` through `0x003B3B40` for UI
modes 3, 4, `0x14` and `0x18`, and for mode 1 only while `0x002DDC30()` is 0 (`0x0025475F`-`0x0025477E`).

The UI close runs no apply. `0x002544C0(mode)` cancels the id `0x00255290(mode & 0x7FFF)` gives with fade -1 by a tail
jump to `0x00225CD0` (`0x002544F0`), without testing the id's bit; when the map gives -1 and the mode is exactly `0x0B`
it tail-jumps to `0x002260A0` (`0x002544E1`), which cancels 22 when its bit is set, and any other mode returns
(`0x002544FA`). `0x00252D90()` does the same for the current UI mode `0x02092730` (`0x00252DBE`, `0x00252DB2`) and then
zeroes `0x02092730` and `0x02092734` on every path (`0x00252DC5`, `0x00252DCB`).

The field-hold bodies run `0x00263560` first (`0x002634B0`, `0x0026A214`). `0x0026A1D0(on, flag)` stores `on` in `0x02099DE6`
and the flag in `0x02099DE7`, a negative flag with `on` set becoming `0x00377700() == 0` (`0x0026A1EB`-`0x0026A20B`), and then
raises 5 with the flag `0x02099DE7` = 0, fade -1 and the apply (`0x0026A23C`, `0x0026A250`) or cancels as the table says.

The mask verbs do more than the request. `0x002E2440(a, b)` passes `a ≠ 0`, with `0x10` ORed in when `b` is
non-zero, to `0x0029D290`, starts 16 through `0x002274E0`, sets the bits `0x100203` of action-availability row 4
(`0x0215F1D0`, `0x002E245F`, [action availability](../Controls-And-Input/action-availability.md)), runs `0x00267D40(1, 1)`, which
sets bit `0x2` of the bone-physics deny mask `0x02099DA6` ([frame update order](frame-update-order.md)), and sets the
byte `0x0215F1B2` to 1.

`0x002E2400(a)` and the unload `0x002E06B0` undo each step: `0x0029D210(a ≠ 0)` (1 for the unload), the cancel
`0x00226160`, the row-4 bits cleared (`0x002E2417`, `0x002E06C3`), `0x00267D40(1, 0)` and `0x0215F1B2` = 0. All three leave
the apply to the field frame.

Each id-17 body stores `0x00265680()` in `0x02099DE0` and starts or cancels 17, with the apply, only while manager 0
is live (`0x02098E20` bit `0x1`) with `0x02098E21` bit `0x1` and `0x02098E20` bit `0x80` clear; otherwise the slot keeps its
state. It then sets action-availability row 6 for a result of 0 and clears it otherwise (`0x002E1CD0(result ≠ 0, 6)`),
runs `0x002E23D0(result ≠ 0)` and, for a non-zero result, `0x002EF350(1, -1)` (`0x00263692`-`0x002636E0`,
`0x0026C53B`-`0x0026C586`, `0x0026C7E6`-`0x0026C837`).

`0x0026C3E0(record, reset)` sets the record's byte `+0x14` to 0 and `0x0026C5D0(record)` sets it to 1 (`0x0026C410`,
`0x0026C606`). Both then walk the non-null roster slots: speed 0 (`0x0026D6F0(actor, 0.0, 2)`), and, unless the slot is
not the party focus while `0x00377700()` is non-zero and `0x02099DB4` is above 0, `0x0035AE10(actor, 1)` for an actor with
a battle unit and `0x002EB430` when `0x00233D70` accepts it (`0x0026C3E0` only with `reset` non-zero, adding `0x002ED020`);
`0x0026C3E0` also runs `0x002ECEC0` on every slot.

`0x0026C3E0` reads `0x00265680()` before the walk and again after it and `0x00254FC0` (`0x0026C4EC`); when the first
answer was non-zero it runs `0x00237F40` and `0x00358BB0` while `0x00377C20()` is 0, then `0x002DEB90(1)`
(`0x0026C58B`-`0x0026C5B1`).

With `0x02099DB4` above 0, `0x0026C5D0` also clears action-availability row 3 (`0x002E1CD0(1, 3)`, `0x0026C70C`) for
each slot it walks and releases the focus slot's look (`0x002EBE50(focus, 0, 0)` and `0x002E8EE0`, when `0x002E7600` is
non-zero). After the walk, with `0x00265680()` non-zero, it runs `0x00307140(0)`, `0x00363B00(0, 0, 0.0)`, `0x003EC6C0(1)`
and `0x0035A8D0(1)`, then `0x002DEB90(1)`.

Between those, it reads byte `+0x18` of all four roster slots with no null test (`0x0026C766`-`0x0026C76E`), so an
empty slot faults there; a slot whose byte is 1 gets `0x002693D0(other, 1)` for the actor `0x003587C0(+0x19, +0x1A)`
names, when that actor exists and is not the slot itself.

`0x0025C170(m)` returns at once unless manager `m` is live (`+0x10` bit `0x1`). Over the records from `+0x1DA` for
`+0x1D2` entries it clears byte `+0x0C` bit `0x2` and runs `0x0025C830(manager, record)` when the record's `+0x14` bit
`0x20` and `+0x08` bit `0x1` are set; over the records from `+0x1DE` for `+0x1D6` entries it runs
`0x0025C230(manager, record)` when `+0x14` bit `0x20` is set.

`0x0025B500(actor)` returns at once unless the actor's byte `+0x0C` bit `0x40` is set (`0x0025B508`). It clears that
bit, lowers the count at `+0x1E4` of the actor's manager and stores the sum of the live managers' counts in
`0x02099DB8` (`0x0025B558`); at 0 or below it cancels 18 and clears action-availability row 13 (`0x002E1CD0(1, 13)`,
`0x0025B573`).

Around 19, `0x002678C0` runs `0x00238B00(1)`, `0x002509A0(0, 0)` with `0x02099DA7` set to 1 when it was 0, sets
action-availability row 0 (`0x002E1CD0(0, 0)`) and busy bit `0x1000` (`0x003601B0(0xC)`) before its start, and
`0x0025D580` runs `0x00238B00(0)`, `0x00250960(0, 0)` with `0x02099DA7` cleared when it was set, clears row 0
(`0x002E1CD0(1, 0)`) and the busy bit (`0x003601C0(0xC)`) before its cancel.

The records each id builds, read as the categories each set stops (F the party leader, P the
other roster entries, T127 / T3 / T0 the three type classes, R the request's actor, H the handle
list; "all" is every category and "-" no category):

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
- the full-screen menus stop scripts and set 3 only, with record B bits under mask `0x7F00` all set, which
  selects the apply's 1.0 fade;
- the field hold and an event taking an actor keep the party leader and the type-0 actors moving,
  and the other party members too unless the flag is 1;
- ids 16, 20, 21 and 23 to 27 stop no actor and exist for the global bits;
- ids 17 to 19 put nothing in sets 1 to 5, so they stop no movement, but they set the battle stop flag
  and the flag word of the party leader and the other roster entries (sets 6 and 7);
- id 22, the game-over route, is the first row's full freeze above.

### The apply step

`0x00226280` runs only while the dirty byte is set and clears it at the end. It ANDs the first
qword of every A and every B record over all twenty-eight slots into one combined pair (a
cancelled slot holds all-ones, the identity), takes the smallest non-negative B `+0x10` as the
fade and resets each such slot to -1, and ORs bit `0x20000000000` into every slot's B. Then:

- `0x00226640(allExempt, fade, 0)`, the per-actor pass below, with `allExempt` set when the bits of the
  combined B under mask `0x7F00` are all set (`0x0022642D`-`0x00226461`);
- A bit `0x1000000` and B bit `0x1000000`: `0x002EA8E0(0, ~A24)` and `0x002EA8B0(0, ~B24)`, bit `0x1` of the two source
  bytes `0x0215FD44` / `0x0215FD45` ([party control modes](party-control-modes.md) writes their bit `0x4`);
  the status-error verbs name them: the `ctrldeny` verbs clear A24, the `dispdeny` verbs B24;
- A and B bits under mask `0xE000000`: two 16-bit group masks `0x0209215E` / `0x02092162` for the effect system
  (`0x0024B9B0` reads the first; `0x0024C970` initialises both to `0x3FF`): bit `0x2000000` set gives `0x3FF`
  (else 0 for A, `0x3EE` for B), bit `0x4000000` clear ORs `0x76`, bit `0x8000000` sets or clears bit `0x2`, then
  `0x108` is ORed; when A's word is exactly `0x108` and B's lacks bit `0x10`, A's becomes `0x10C` and
  B's gains bit `0x4`;
- A bit `0x20000000`: `0x0035B510(0xFF)` when set, else `0x0035B4B0(5)`, the controller vibration pause
  ([vibration](../Controls-And-Input/vibration.md)): `0x0035B4B0(5)` ORs 5 into the pause mask `0x02EC0B40` (`0x0035B4BA`) and moves
  every playing slot (state 2) of the 32 at `0x02EC0B80` whose mask byte `+0x1C` shares a bit to state 3
  (`0x0035B4C7`-`0x0035B4FD`);
- `0x0035B510(0xFF)` clears the pause mask's low byte (`0x0035B51C`) and moves every slot in state 3 back to 2, whatever
  its mask (`0x0035B530`-`0x0035B53F`);
- A bit `0x40000000` clear: `0x0025A5D0(1)` sets `0x02098DEB`; set: clears it;
- A bits `0x1000000000` and `0x2000000000`: `0x002547C0` gets `0xF` when bit `0x1000000000` is set, else `0xE`, with bits `0x4` and `0x8`
  cleared when bit `0x2000000000` is clear, the pump argument of [subsystem update
  flags](subsystem-update-flags.md); B bit `0x1000000000` the same through `0x00254840` (`0x01E0C2AC`);
- A bit `0x8000000000`: `0x002E24C0(0)` sets bit `0x1` of `0x0215F1B3` when clear, `0x002E24E0(0)` clears it when set;
- unless the skip byte `0x01FD46D1` is set (`0x00227D30` sets it; the apply clears it instead of
  running this block): the audio group mask from B bits under mask `0x1F0300000000` through `0x002DF370`
  and `0x002DF640` (`0x01E0CF98` = 0 or `0x100`); `0x002DF370(mask, on, force)` keeps the paused
  kinds at `0x0215EFD8` and, unless `force` is set, hands `0x001DBA90` only the bits that change
  ([audio manager](../Sound-And-Music/audio-manager.md));
- B bit `0x800000000`: `0x002EBBF0(1, B35)`, bit `0x2` of `0x0215FD56`: B35 set clears the bit and B35 clear sets it
  (`0x002EBC00`-`0x002EBC0F`); the byte's zero state then sets bit `0x1` of the render table's `+0x48818` (character
  distance culling, the table `[0x022C6F28]`), and a non-zero byte clears that bit (`0x002EBC20`, `0x002EBC28`);
- the combined A and B are stored at `0x01FD46A0` and `0x01FD46B8` as two `0x18`-byte records: the qwords `0x01FD46A8`,
  `0x01FD46B0`, `0x01FD46C0` and `0x01FD46C8` receive stack slots the apply never writes, and nothing reads them.

### The per-actor pass and the seven stop sets

`0x00226640(allExempt, fade, three)` walks three managers (one when `three` is set) and every record.
Each set is a live bitset of request ids plus a pending-set and a pending-clear word; the pass
folds them (`live |= set; live &= ~clear;` both zeroed); the hook of set 1 runs when it becomes non-zero, that of
set 3 when it changes, `0x002269A0` of set 5 for every record (it tests the change itself), and those of sets 6 and
7 on every pass for each record with a battle unit.

| Set | Live | Pending set / clear | Hook | What the live set stops |
|---|---|---|---|---|
| 1 | battle unit `+0x40` (`0x00359B80`: `[record + 0x30] + 0xED0`) | `+0x54` / `+0x60` | becoming non-zero: `0x0026D6D0` → `0x0026D6F0(actor, 0.0, 2)`, the movement speed written to 0 | movement |
| 2 | record `+0x10C` | `+0x110` / `+0x114` | no hook | the actor's per-step tail in the drive pass `0x0025DF00`: the animation-driven step `0x003E6EF0`, the mode word `0x002681E0`, the movement step `0x002E5030` and the facing integrator `0x002E5750` run only when the set is 0 and byte `+0x13` bit `0x1` is clear, or byte `+0x0B` bit `0x20` is set; otherwise `0x002E6310` runs instead; the interpreter refuses at `0x0025E524` and `0x00264DF0` refuses the stick |
| 3 | controller `[record + 0xC0] + 0x170` | `+0x174` / `+0x178` | `0x002E92F0`: `0x00428FE0(render record, 0x00264DC0(actor) = 0)` (`0x002E9346`), which writes `+0x304` bit `0x10` and queues `+0x290` bit `0x4000000` or `0x8000000`; `0x00264DC0` is 1 only when the controller exists, this live set is 0 and actor byte `+0x13` bit `0x1` is clear (`0x00264DC0`-`0x00264DDE`); the render record is `[0x022C6F28] + 0x740 × controller word +0`, and the hook returns without the call when the controller is null, its first dword or word is -1, that address is 0 or the record's `+0x284` is 0 (`0x002E9305`-`0x002E933F`); a null actor faults in `0x00264DC0` (read of `[0xC0]`) before the test at `0x002E9305`. `0x00428FE0(record, v)` sets `+0x304` bit `0x10` for a non-zero v and clears it for 0 (`0x00428FE0`-`0x00428FF2`), then ORs `0x4000000` into `+0x290` when v is non-zero and `+0x294` bit `0x8` is clear (`0x00429006`), else `0x8000000` (`0x00429011`) | the additive motions of the character |
| 4 | controller `+0x164` | `+0x168` / `+0x16C` | no hook | presence: `0x002E9FE0` and `0x002E7E90` treat a kind-3 actor with a non-zero set as absent; `0x002E9FE0` returns 1 for an actor whose byte `+3` under mask `0xE0` is not `0x60` (`0x002E9FE6`), and for a kind-3 actor only when its controller exists, this set is 0 (`0x002E9FFC`), controller byte `+0x10` holds bits `0xB` (bits `0x3` when byte `+0x11` has bit `0x20`) and byte `+0x11` holds bits `0x6` (`0x002EA00D`-`0x002EA024`), else 0; a null actor faults at `0x002E9FE0`; `0x002E7E90`, the actor's fade, returns 0.0 for it (`0x002E7EA9`) and for a kind-3 actor without a controller or whose controller lacks `+0x11` bits `0x2` and `0x4` or `+0x10` bits `0x1`, `0x2` and `0x8` (`0x1` and `0x2` when `+0x11` bit `0x20` is set), and otherwise `0x0042FB20` of the controller's render handle, or 1.0 when the controller is missing or its first dword is -1 (`0x002E7EE4`-`0x002E7EFD`) |
| 5 | controller `+0x158` | `+0x15C` / `+0x160` | `0x002269A0(manager, record)` folds this set itself (`0x002269D5`-`0x002269FA`) and, when the live set turned from zero to non-zero or back (`0x00226A0E`), appends the actor's id `0x003589B0(record)` to the manager's list `+0x1F0` (count `+0x1F8`) without a capacity test (`0x00226A2F`, `0x00226A31`); a record whose controller is null returns at once (`0x002269B3`) | the fade (below) |
| 6 | battle unit `+0x44` | `+0x4C` / `+0x58` | `0x00238B40(actor, live ≠ 0 or record byte `+9` bit 0x20)` → battle unit `+4` bit `0x20` (`0x0031B760`) | the unit's stop flag |
| 7 | battle unit `+0x48` | `+0x50` / `+0x5C` | `0x00312130(actor, live = 0 and that bit clear)` → unit flag bit `0x1000000000` set while stopped: set for an argument of 0 and cleared otherwise (`0x00312150`, `0x00312163`), on the qword at `[actor + 0x30]` that `0x0031B760` returns; nothing is written for a null actor or a null `[actor + 0x30]` (`0x00312140`) | the unit's flag word |

After each manager's records, when its list is non-empty:

- with `allExempt` clear: `0x0024FCA0(list, n)` (mask `0x3FE` to `0x02092160`, `0x003B3BA0`, `0x003B1180`, each
  given the list and its count `+0x1F8`: `0x002268CB`, `0x0024FCC0`),
  `0x0024FBF0(list, n, 0.0, fade + 1)` (the global ramp `0x020926E8` toward `0x020926EC` = 0.0
  over `0x020926E6` = fade + 1 frames, stepped by `0x0024BFD0`), then `0x002E8B10(actor, 0.0, fade +
  1)` for each listed actor;
  - `0x0024FBF0` also raises bit `0x4` of `+0x368` on every kind-1 active effect (`0x002FD090`, `0x0024FC58`) and, by a
    tail jump to `0x003B1050(list, n)` (`0x0024FC6C`), on the kind-5 effects owned by the listed actors;
  - it writes the value 1 into bits `0x100` and `0x200` of `0x020926E4` (`0x0024FC23`-`0x0024FC45`) and the step
    `0x020926F0` = (target - `0x020926E8`) / frames (`0x0024FC50`), a frame count of 0 or less becoming 1 (`0x0024FC15`);
- with `allExempt` set: `0x0024FC80` (mask `0x3FF`), `0x0024FB90(1.0, fade + 1)` and `0x002E8B10(actor,
  1.0, fade + 1)`;
  - `0x0024FB90` writes the same ramp with the value 2 in those bits (`and` with `0xFEFF`, then `or` with `0x200`,
    `0x0024FBAD`-`0x0024FBD2`), with the same frame clamp and step, `n = frames <= 0 ? 1 : frames` (`0x0024FBAA`) and
    `0x020926F0` = (target - `0x020926E8`) / n (`0x0024FBD9`-`0x0024FBDD`);
  - when a value-2 ramp ends, `0x0024BFD0` clears bit `0x4` of `+0x368` again: on every kind-1 active effect
    (`0x002FD060`) and on the instance `+0x08` of each of the 36 request entries at `0x02EBEC00`, up to the first
    whose dword `+0` is 0 (`0x003B1000`), called at `0x0024C037` and `0x0024C03C`.

`0x002E8B10` ramps channel 2 of the actor's character render record (`0x00428940(record, 2, value,
frames)`), and does nothing for a null actor, a null controller `+0xC0`, a render handle of -1 or a render record
whose `+0x284` is 0 (`0x002E8B13`-`0x002E8B4A`).
`0x00226A50` and `0x00226AB0` fold sets 6 and 7 for one actor outside the pass, and
`0x00263560` drives both hooks for the four roster actors from the hold bytes `0x02099DE3` to
`0x02099DE6`, also zeroing their movement speed.

`0x00226A50(record)` and `0x00226AB0(record)` return at once when `0x00359B80(record)` gives no battle unit (`0x00226A61`,
`0x00226AC1`). Otherwise each folds its set and then always tail-jumps to the set's hook with the argument the table
gives, whether or not the live set changed: `0x00238B40` (`0x00226A9E`) and `0x00312130` (`0x00226B00`).

`0x02099DE4`, the second hold byte, gets 0 from the unload `0x002628B0` (`0x00262BD7`) and from the boot `0x00266D10`
(`0x00266F45`), each time between two calls of `0x00263560`, which ORs it with `0x02099DE3`, `0x02099DE5` and `0x02099DE6`
(`0x00263576`).

At run time only `0x0026A290` writes `0x02099DE3`: it is the handler of the verb `setmutekiparty`
(`0x0337`, through `0x003452B0`), stores the popped value there and runs `0x00263560`. With manager 0
active (`0x02098E20` bit `0x1`) a non-zero
value raises the battle-unit stop flag and flag bit `0x1000000000` of every roster member and sets their
record byte `+0x09` bit `0x80`, and 0 clears them again while the other hold bytes are 0.

### Cancel, unload and reset

`0x00225CD0(id, fade)` sets the dirty byte, clears the id's bit without testing it first (`0x00225CF3`, `0x00225D08`),
and over all three managers ORs the bit into every record's seven pending-clear words and removes it from the
pending-set words; then both records' first qwords become all-ones, both `+0x14` bytes 0, and B `+0x10` = fade
(`0x00225E1C`-`0x00225E3D`). It runs no apply.

The walk takes a manager only while its `+0x10` bit `0x1` holds (`0x00225D2C`) and skips a null record (`0x00225D69`).
A record without a battle unit (`0x00359B80` gives 0) keeps sets 1, 6 and 7 unmarked (`0x00225D72`, `0x00225DE6`), and
one whose controller `+0xC0` is null keeps sets 3, 4 and 5 unmarked (`0x00225D90`, `0x00225DAF`, `0x00225DCE`); set 2
sits in the record itself (`0x00225D7A`).

Side calls: id 0 runs `0x00182DA0` unless the options bit is set, 12 and 17 run `0x00182D60`, 13 clears
bit `0x20000000000` of its B and runs `0x00182D40`, 15 runs `0x00182D40`.

`0x00225EB0` cancels every active id with fade -1 the same way (the area unload, `0x00262B6C`): it tests the bits of
ids 0 to 27 in turn (`0x00225EE1`), skips a clear one, and for a set one runs the same walk, record writes and side
calls (`0x00225EEF`-`0x0022605B`).

`0x00226B30` resets everything: bitset, dirty and skip bytes 0, every record's first qword all-ones and `+0x14` 0,
the combined pair all-ones; it does not write the fades, which are 0 from the image until the
first apply resets them to -1. It treats the combined pair's two slots like records as well: the dwords
`0x01FD46B0` and `0x01FD46C8` become -1 and the bytes `0x01FD46B4` and `0x01FD46CC` 0 (`0x00226B60`-`0x00226B74`).

`0x00226B10(id)` returns the combined record address, `0x00226BA0()` is "the combined pair restricts
anything" (`A & B` not all-ones), `0x00226BC0()` is "any request active" (read by the field frame's
speed-mode block) and `0x00226BD0(id)` tests one bit (`0x0025C830` tests 10).

## Layouts

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01FD4160` | `...` |  | record A, `0x18` bytes per id at `0x01FD4160` + id*`0x18` (below) |
| `0x01FD4400` | `...` |  | record B, `0x18` bytes per id at `0x01FD4400` + id*`0x18` (below) |
| `0x01FD46A0` | `u64` |  | combined A |
| `0x01FD46B8` | `u64` |  | combined B |
| `0x01FD46B0` | `...` |  | unused copies; with `0x01FD46C8` |
| `0x01FD46C8` | `...` |  | unused copies; with `0x01FD46B0` |
| `0x01FD46D0` | `u8` | dirty |  |
| `0x01FD46D1` | `u8` | skip the audio block once |  |
| `0x01FD46D4` | `u32` | active ids |  |
| `0x02099DE3` | `...` |  | hold bytes `0x02099DE3` to `0x02099DE7`, u8 each (`0x02099DE5` / `0x02099DE6` select ids 5 / 4, `0x02099DE7` the flag) |
| `0x0209215E` | `u16` | effect group masks | with `0x02092162` |
| `0x02092162` | `u16` | effect group masks | with `0x0209215E` |
| `0x0215FD44` | `u8` | source bytes (bit 0x1) | with `0x0215FD45` |
| `0x0215FD45` | `u8` | source bytes (bit 0x1) | with `0x0215FD44` |
| `0x0215F1B3` | `u8` |  | source byte (bit `0x1`) |
| `0x020926E4` | `u16` | flags | the fade ramp |
| `0x020926E6` | `u16` | frames | the fade ramp |
| `0x020926E8` | `f32` | value | the fade ramp |
| `0x020926EC` | `f32` | target | the fade ramp |
| `0x020926F0` | `f32` | step | the fade ramp |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x14` | `u8` |  | cleared only (the flag is in record B) |

Record B:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` |  | permission bits |
| `+0x10` | `i32` |  | fade (-1 no fade; 0 before the first apply) |
| `+0x14` | `u8` | flag |  |

Record (actor):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10C` | `u32` |  | set 2 live |
| `+0x110` | `...` |  | pending set |
| `+0x114` | `...` |  | pending clear |

Controller [record+`0xC0`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x158` | `...` |  | set 5; with `+0x15C` and `+0x160` |
| `+0x15C` | `...` |  | set 5; with `+0x158` and `+0x160` |
| `+0x160` | `...` |  | set 5; with `+0x158` and `+0x15C` |
| `+0x164` | `...` |  | set 4; with `+0x168` and `+0x16C` |
| `+0x168` | `...` |  | set 4; with `+0x164` and `+0x16C` |
| `+0x16C` | `...` |  | set 4; with `+0x164` and `+0x168` |
| `+0x170` | `...` |  | set 3; with `+0x174` and `+0x178` |
| `+0x174` | `...` |  | set 3; with `+0x170` and `+0x178` |
| `+0x178` | `...` |  | set 3; with `+0x170` and `+0x174` |

Battle unit [record+`0x30`]`+0xED0`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x40` | `...` |  | set 1; with `+0x54` and `+0x60` |
| `+0x54` | `...` |  | set 1; with `+0x40` and `+0x60` |
| `+0x60` | `...` |  | set 1; with `+0x40` and `+0x54` |
| `+0x44` | `...` |  | set 6; with `+0x4C` and `+0x58` |
| `+0x4C` | `...` |  | set 6; with `+0x44` and `+0x58` |
| `+0x58` | `...` |  | set 6; with `+0x44` and `+0x4C` |
| `+0x48` | `...` |  | set 7; with `+0x50` and `+0x5C` |
| `+0x50` | `...` |  | set 7; with `+0x48` and `+0x5C` |
| `+0x5C` | `...` |  | set 7; with `+0x48` and `+0x50` |

Manager:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x010` | `...` |  | bit `0x1` live |
| `+0x028` | `...` |  | exemptions of categories 0, 1, 5 and 6 skipped when non-zero |
| `+0x1D6` | `...` | count |  |
| `+0x1DE` | `...` | first |  |
| `+0x1F0` | `...` |  | fade list |
| `+0x1F8` | `...` |  | its count |

## Shipped data

| Fact | Value |
|---|---|
| request ids | 28, slots of `0x18` bytes |
| default record | A `0x34FD000000`, B `0x00001F3A09001F1F` (ids 0 to 3, 15 and 22 drop A bits `0x1000000`, `0x8000000` and `0x20000000` and keep the default B; id 15 also clears the B bits under mask `0x1F0000000000`) |
| records per id | the table above, all 28 cases of `0x00227680` |
| ids never raised | 1, 3, 8, 9, 14, 20, 21 |
| fades passed | 4 (an event taking an actor, its removal), -1 (every other engine site), the verbs' arguments |
| effect masks | `0x3FF` at init (`0x0024C970` stores it to the five words `0x0209215E` to `0x02092166`, `0x0024C98A`-`0x0024CA36`, after clearing the `0x1670` bytes from `0x020910A0` at `0x0024C983`, which zeroes the fade ramp `0x020926E4` to `0x020926F0` and so leaves it stopped at 0.0; [startup constants](startup-constants.md)), `0x3FE` / `0x3FF` during the fade, `0x76`, `0x108`, `0x10C`, `0x3EE` from the apply |

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
  fades over nothing. A fade of 0 becomes one frame (`0x0024FBF0` and `0x0024FB90` clamp to 1).
- The ramp `0x0024BFD0` advances only while bits `0x100` and `0x200` of `0x020926E4` hold 1 or 2 and frames remain,
  and only when its argument is 0 (`0x0024BFD6`, `0x0024BFE9`). Each step adds `0x020926F0` to `0x020926E8` and counts
  `0x020926E6` down (`0x0024BFF8`-`0x0024C007`); at zero it stores the target `0x020926EC` and clears both bits
  (`0x0024C011`-`0x0024C046`).
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
- [`time-stop-and-freeze-registry-accesses.tsv`](time-stop-and-freeze-registry-accesses.tsv): every access
  to the request record block at `0x01FD4160`, taken as a whole (57 rows).
- [`time-stop-and-freeze-record-accesses.tsv`](time-stop-and-freeze-record-accesses.tsv): every access to
  its `0x18`-byte records: records A and B of the twenty-eight request ids (from `0x01FD4160` and `0x01FD4400`) and the
  two after them, at the block's `+0x540` (256 rows).

In the `route` cells of these tables, `SystemStopRegistry` names the record block at `0x01FD4160`.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat formula: `0x00377C20` is called by `0x00300530`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Items equipment shops license: `0x00377C20` is called by `0x00309FB0`, `0x0030FD10`; those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Rewards progression economy: `0x00234590` calls `0x00319600`; `0x00377C20` is called by `0x00312280`; those functions are
  documented on [frame update order](frame-update-order.md),
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md).
