---
title: "Battle verbs: what a script can do to a unit's battle actions, the one commit every action passes through, and the verbs that change stance, thinking and emergency state"
kind: "system"
category: "Scripts and script commands"
addresses: "0x0030F760, 0x00305AB0, 0x0030FA00, 0x00312FA0, 0x00311CF0, 0x00311B20, 0x003138D0, 0x00346EB0, 0x003460C0, 0x00346620, 0x00311E90, 0x00311F50, 0x00307D10, 0x00347970, 0x003473E0, 0x00346A10, 0x0030F2D0, 0x01EEC3C0, 0x01EEC410, 0x002ECF10, 0x0034E160, 0x0035A720, 0x00356530, 0x00344740, 0x0035AE10, 0x003419F0, 0x00357F00, 0x003DDB40, 0x01EFE9D0, 0x00510440, 0x002390B0, 0x005103B0, 0x002394C0, 0x0034CB60, 0x00341DB0, 0x0050E980, 0x00356970, 0x003444D0, 0x00305CC0, 0x003105D0, 0x0030AB40, 0x00313B30, 0x00308270, 0x002FFCF0, 0x01EEC298, 0x01EEC320, 0x01EEC370, 0x01EEC2B0, 0x01EEC2D0, 0x00317E60, 0x00342230, 0x00328BD0, 0x003137F0, 0x0030D9A0, 0x0031B8C0, 0x00426130, 0x00426C90, 0x002FEDC0, 0x00301140, 0x00313480, 0x0034E530, 0x0035A7A0, 0x00343290, 0x0030BFB0, 0x0035AB20, 0x0035A680, 0x00347460, 0x00238B70, 0x00238AE0, 0x0030FED0, 0x0030E130, 0x0030E360, 0x0030EAE0, 0x003446D0, 0x00268530"
---

## What the player sees

In a fight each character picks what to do next: the command chosen in the battle menu, the first
gambit that applies, the next hit of a combo, or a counter when engaged. During scenes the story
steps in: characters draw or sheathe their weapons, stop fighting and stand still while someone
talks, or are taken over for a cutscene and drop what they were doing. The story never says "use
Cure on Vaan now". It changes what a character is allowed to do or how they stand, and the
character's own decision-making does the rest.

## How it works

### One commit, four native callers

`0x0030F760(unit, orderContext, actionId, targetFocus, mode)` is the only place an action becomes
the unit's current action. With a non-zero mode it first calls `0x003105D0`. An id below `0x21F`
refreshes the target link at `+0x778` (`0x00316CF0`, `0x00316CD0`); any other id outside
the battle orders `0x4000..0x4166` is refused (return 0, `0x0030F7D9`-`0x0030F7EC`).

It then clears `+0x700` bits `0x3`, stores the context at `+0x708`, the target at `+0x710` and the id
at `+0x714`, zeroes byte `+0x6B4`, and copies the 0x18 bytes `+0x700..+0x717` to `+0x718..+0x72F`.
A pending no-target issue (`+0x6B0` bit `0x2`) is consumed into `+0x6B9` from `0x022C1DB8`.

The same pending issue also sets `+0x6B6` to 1 (`0x0030F865`-`0x0030F894`). `+0x770` is kept only for a unit whose
stats record byte `+0x05` is 1, or is 0 with an id equal to `+0x744` and a target equal to `+0x740`; otherwise it
is zeroed (`0x0030F832`-`0x0030F85F`). When the unit's `+8` differs from its `+0x24`, `+0x750` is zeroed
(`0x0030F89B`-`0x0030F8A3`).

For a target and an id below `0x21F`: when `0x0030AB40(unit, target, 0)` is above 1, `+0x754` takes the
target, and when the unit's `+8` equals its `+0x24`, every unit of the `0x00236820` list with the same
`+0x24` that is not KO'd or petrified (outside a town) gets `+0x754` = target and the unit's `+0x750`
= target. A listed unit needs a stats record `+0x698`, and the status test covers KO, Stone and X-Zone
(`0x80000003` in `+0x3C` or `+0x64`), skipped when `0x00377C20()` is non-zero (`0x0030F8F3`-`0x0030F916`).

For the same target and id range, while unit flag bit `0x400000` is clear (`0x0030F939`) and the attacker is not yet
registered, it sets the bit `1 << [unit + 0xEA9]` in the target's `+0xEA4`, adds one to the target's byte `+0xEA8`,
and calls `0x00313B30(unit, target, 1)`; "registered" is that bit already set (`0x0030F940`-`0x0030F962`). Every accepted
id returns 1 (`0x0030F97A`).

Its callers are 5 sites in 4 functions: the next-action selector `0x00305AB0` (`0x00305B2F`, `0x00305C9B`),
the order-set scanner `0x00305CC0` (`0x00305DF4`), the combo continuation `0x0030FA00` (`0x0030FA5C`) and the
engage auto-attack `0x00312FA0` (`0x003130DC`). `0x00312FA0` sets flag bit `0x400000` just before its commit
(`0x0030F760(unit, 0x01EEC2B0, 0x96, target, 0)`, target from `+0x28`, cleared on read), so that action
never registers as an attacker.

Before that commit `0x00312FA0` saves `+0xDC8` (word) and `+0xE58` (dword) into the 12-byte record of `0x022C1DB0`
at index `+0xEA9` (`0x00313088`-`0x003130C7`). A commit is followed by `0x00328480(unit, 3)` and `+0x6B4` = 5
(`0x003130E8`-`0x003130F2`); a refused commit runs `0x00308270` (`0x00313109`).

`0x00308270(unit)` undoes that state, and does nothing while flag bit `0x400000` is clear (`0x00308280`): it zeroes
`+0x28`, frees the slot `+0x695` (`0x0030C970`, then `0xFF`), restores `+0xDC8` and `+0xE58` from the `0x022C1DB0`
record, copies the action state back with `0x0030EDA0`, zeroes `+0x690`, and clears flag bit `0x400000` and `+4`
bit `0x4000` (`0x00308282`-`0x003082DF`).

`0x00312FA0` saves and commits only when all of these hold (`0x00312FC3`-`0x00313082`); otherwise it returns with
`+0x28` cleared and nothing else written:

- the unit and the target unit `0x0031B7E0(target)` both have a record `+0x698`, and neither has statuses
  `0x80000003` outside a town;
- flag bit `0x400000` is clear, flag bit `0x800000` is set, and `+4` bits `0x40000` and `0x80000` are clear;
- a party record whose type byte `+4` is `0x1B`-`0x27` has a dword `+0x48` above 0;
- `0x0030EFF0(unit)` returns non-zero.

### How the next action is chosen

`0x00305AB0(unit, mode)` tries each source in order and stops at the first commit. The scanner
`0x00305CC0` passes as context the 0x18-byte entry inside the set (`set + 0x20 + n × 0x18`). A town is
a map whose word in `[0x02ADD100]` has bit `0x8000` set (`0x00377C20`).

1. Flag bit `0x400000` set: `0x00308270` first. Flag `0x4000`: the flag is cleared and the issued command
   `+0xBA0` commits with context `unit + 0xBA0` and target `+0xBB8` when its id is in
   `0x4000..0x4166` or `0x002FFCF0(id, unit)` is 0 (`0x0030F760(unit, unit + 0xBA0, id, +0xBB8, 1)`,
   `0x00305B2F`). A refused commit, or an id `0x002FFCF0` rejects, goes on to step 2 (`0x00305B10`, `0x00305B36`).
2. In a town with a party record (`[+0x698] + 5` = 0): straight to step 6.
3. Outside a town, with status `0x20`, or with a non-party record (`+5` = 1) and status `0x08000000`:
   scan `0x01EEC320`, then step 6. Outside a town the record `+0x698` is read with no null test
   (`0x00305B66`-`0x00305B70`), so a unit without a record faults there.
4. Otherwise scan the order set `+0x6E8`. Then, outside a town for a party unit with `0x08000000`:
   scan `0x01EEC370`. Else, for a null or non-party record or one with dword bit `0x4`: scan `+0x6E0`
   with byte `+0x6B5`, clearing `+0x6F8` and `+0x748`. Else scan `+0x6F8` when set; when that scan does
   not commit, clear `+0x6F8` and `+0x748` (`0x00305C23`-`0x00305C2C`).
5. Scan `+0x6F0`.
6. With mode 0: commit `0x01EEC298` with id `[0x01EEC298]`, no target.

### Issuing a command

`0x00311CF0(unit, target, arg, id, transient)` writes the issued command. It refuses (returns
`0xFFFFFFFE`) a unit with no record `+0x698`, a unit with statuses `0x80000003` outside a town, and
id `0x113` while `+0x714` is `0x113`; id `0x113` also clears bit `0x1` of word `[0x02EBF190] + 0x5AD0`.

While statuses `0x8800203B` are clear it stores the id at `+0xBA0`, clears `+0x6B0` bit `0x2` (`0x00311D81`),
sets `+0xBA4` bit `0x8000` and flag `0x4000`, stores the target at `+0xBB8` (with no target: the unit's own
`+8`, `+0x6B0` bit `0x2` set and `0x022C1DB8[+0xEA9 × 0xC]` = arg), and with a target and a non-zero transient
argument stores the target at `+0x748` and the transient set `0x01EEC2D0` at `+0x6F8`; then it calls `0x00317E60`.
It returns 0 otherwise, including when a status drops the command silently.

The menu path `0x00311B20(actor handle, target handle, arg, id, all)`, a caller named below, returns -1
without issuing when the acting handle resolves to no unit (`0x0031B7E0`), or when a non-zero target handle
resolves to no unit for an id other than `0x414E` (`0x00311B3E`-`0x00311B74`). It passes a transient argument of 1
only for Attack (`0x96`) with no target unit or with a target that `0x0030AB40(unit, target, 0)` puts above 1
(`0x00311B93`-`0x00311BBD`).

With `all` non-zero `0x00311B20` issues to every party-slot unit 0-3 that has a record and no statuses
`0x80000003` outside a town (`0x00311BDE`-`0x00311C86`) and returns 0; otherwise it returns the one
`0x00311CF0` result (`0x00311C93`-`0x00311CA6`).

Its callers are the menu path `0x00311B20` (two sites), which the battle menu `0x002778C0` calls ([battle
menu](../Menus-And-HUD/battle-menu.md)), and `0x003138D0`. The one verb that reaches it is `resetJobs` (`0x05D6`, `0x00342230` →
`0x00328BD0`): resetting the character recorded at `[0x02EBF190] + 0x5AD5` (`0x003137F0`) runs `0x003138D0(1)`, which issues
the fixed command `0x113` to the party-slot-3 unit (`0x0031B8C0(3)`) with itself as target.

`0x003138D0` acts only when `0x0030D9A0()` is 1, the unit exists (`0x003138F1`), the unit's `+0x714` is not `0x113`, and it
does not already hold an issued `0x113` (flag `0x4000` with `+0xBA0` = `0x113`, `0x00313903`-`0x00313913`). It issues the
command only when `0x0031B7E0` resolves the unit's own handle `+8` (`0x0031392D`-`0x00313948`; `0x0031B7E0` gives a unit only
while `0x02089340` has bit `0x10`, `0x0031B7E4`), and then, issued or not, sets bit `0x1` of word `[0x02EBF190] + 0x5AD0` to
its argument (`0x00313962`-`0x00313981`). No verb passes a script-chosen id.

### Emergency and reset

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setemergency` | `0x03BF` | `0x00346EB0` | `0x00311E90`: each party-slot unit 0-3 (`0x0031B810`) that has a record `+0x698` and is not KO'd, petrified or in X-Zone (statuses `0x80000003`, except in a town) is collected at `0x022C1788` (`0x00311EB8`-`0x00311EFF`) and gets dword `+4` bits `0x200` and `0x400` (`0x600`); then `0x002ECF10(actor, 1, 1)` for each of slots 0 to 3 whose actor `0x00263750` returns (an empty slot is skipped, `0x00346ECA`) |
| `setemergency_one` | `0x0546` | `0x003460C0` | `0x00311F50` on the target unit (no KO or petrify check), then the draw |
| the unnamed `0x05CC` | `0x05CC` | `0x00346620` | pops a mode and resolves r = `0x00263F10(actor)` (an owner bound to a captured member, `+0x18` = 2, becomes that member); `0x00311F50(r)`, then `0x002ECF10(r, 1, mode)` as a tail jump (`0x0034665F`) with the popped mode unchanged |
| `resetemergency` | `0x0554` | `0x00347970` | pushes 0 and pops it back (`0x00347987`, `0x0034798F`); the mode is that value tested against 0 (`0x0034799A`), so 0; then for each of slots 0 to 3 whose actor `0x00263750` returns (an empty slot is skipped, `0x003479AD`): `0x0030F2D0`, then `0x002ECF10(actor, 0, 0)` |
| `resetemergency_with_animetionmode(m)` | `0x0555` | `0x003473E0` | the same with a popped `m` turned into the mode: 1 for any non-zero `m`, 0 for 0 (`0x003473FD`); for each filled slot 0 to 3 (`0x0034740E`): `0x0030F2D0`, then `0x002ECF10(actor, 0, mode)` |
| `resetemergency_one(m)` | `0x057F` | `0x00346A10` | the same for one actor with `m` itself as the mode (`0x00346A28`): on r = `0x00263F10(actor)`, `0x0030F2D0(r)`, then `0x002ECF10(r, 0, m)` as a tail jump (`0x00346A4C`) |
| `refresh_party_fightmotion(m)` | `0x0566` | `0x003446D0` | `0x00268530(m)`, then `0x0035AE10(actor, 1)` for each slot 0 to 3 whose actor `0x00263750(slot)` is non-null (`0x003446E7`-`0x00344705`) |

Bits `0x200` and `0x400` are tested in the engagement update `0x00307D10` (`0x00307D84`, `0x00307DA7`, `0x00307DD1`): with bit
`0x200` set the unit counts as engaged while `0x0030B050` finds a qualifying target, and bit `0x400` keeps it engaged
while `0x0030B050` finds no target: the first pass that finds one clears bit `0x400` (`0x00307D9E`), and a pass that finds
no target with bit `0x400` clear clears both bits and the engagement (`0x00307DA7`-`0x00307DD8`), so the bits clear
themselves afterwards.

`0x00307D10` also clears them at once in a town and when the unit flees (`0x00253B90`), except for the party's chocobo
(record byte `+4` `0x1A`, `0x00307D29`-`0x00307D3C`) and, for the flee, a unit with status `0x08000020` (`0x00307D61`): both
are held engaged with the bits left as they are. With bit `0x200` clear the unit is engaged when `0x00307CE0(unit)` is
non-zero and `0x0030BF20([unit +0x708])` is 0 (`0x00307DB2`-`0x00307DC9`). `0x00311E90` and `0x00311F50` set both bits with `or
[+4], 0x600` (`0x00311F19`, `0x00311F5E`).

`0x002FEDC0`, `0x00301140` and `0x00313480` also clear bits `0x200`, `0x400` and `0x10000` (`and [+4], 0xFFFEF9FF` at
`0x002FEDC6`, `0x00301231`, `0x003134A5`). Statuses `0x08000020` hold a unit engaged without these bits.

Each of the three also clears flag `0x800000`, zeroes `+0xDCC` and installs the default order set at `+0x6E8`
the way `0x0030F2D0` does, `0x01EEC410` for a unit without a record (`0x002FEDC0`-`0x002FEE05`, `0x0030122B`-`0x0030126B`,
`0x0031349F`-`0x003134DA`). `0x002FEDC0(unit, s)` then, for a non-zero s, sheathes at once with
`0x002ECF10(actor, 0, 0)` on the unit's actor `+0x10` (`0x002FEE0C`-`0x002FEE19`). `0x00313480(unit)` first plays the
sheathe, `0x002ECF10(actor, 0, 1)` (`0x00313486`-`0x00313493`), and ends by setting flag bit `0x1000000` and `+4` bit
`0x80000` (`0x003134E1`-`0x003134EB`).

`0x0030F2D0`, whose only callers are the three reset verbs (`0x00346A35`, `0x00347413`, `0x003479B2`), clears
bits `0x6` of `0x022C1F48`, zeroes `0x022C1F40` and `+0xDCC`, clears flag `0x800000` and `+4` bits `0x200`, `0x400` and
`0x10000`, and installs the default order set at `+0x6E8`: `0x01EEC3C0` when `[+0x698] + 5` is 0, `0x01EEC410`
otherwise, a unit without a record included (`0x0030F2E1`-`0x0030F331`). For an actor without a battle unit
(`0x0031B760` gives 0) it returns at once (`0x0030F2DF`).

`0x002ECF10(actor, drawn, mode)` resolves the actor's render record (`[0x022C6F28] + index × 0x740`,
used only when `+0x284` is non-zero) and continues in `0x00426130`. It returns at once for a null actor, a null
`+0xC0`, or a dword or low word `[+0xC0]` of -1, and the index is that signed low word (`0x002ECF10`-`0x002ECF2F`);
a record address of 0 also returns (`0x002ECF41`):

- Mode 1: when bits `0x3` of `+0x40B` differ from `drawn`, it sets them, plays motion `0x4035` (draw)
  or `0x4036` (sheathe) through `0x00427320`, updates `+0x294` and sets `+0x284` bit `0x80000`. Otherwise
  nothing.
- Mode 2: when the state differs, it snaps through `0x00426C90` (`0x004261C0`). When it is equal, it takes the
  motion at `+0xCC` if its class (top 4 bits) is 3 or 4, else the one at `+0x3B4` if that class is 3 or 4, and
  otherwise does nothing (`0x004261C2`-`0x004261F0`). It snaps when that motion's low 12 bits are `0x35` (drawing)
  with `drawn` = 1, or `0x36` (sheathing) with any other `drawn` (`0x004261FA`-`0x00426209`); otherwise nothing.
- Any other mode: `0x00426C90(record, drawn)` sets the state at once (bit `0x1` set and bit `0x2` cleared for a
  non-zero `drawn`, both cleared for 0), sets `+0x284` to `(+0x284 & 0x6FFFFFFF) | 0x10000000`, calls
  `0x00426FA0(record)` (`0x00426CEE`), plays motion `0x1001` and updates `+0x294`. Mode 2 snaps through the same body.
- `0x00426C90` then rebinds the record's attached records. When its word `+8` names a record c (not −1) whose
  `+0x290` bit `0x100000` is clear and whose word `+0x2F2` is not 1 (`0x00426D34`, `0x00426D44`), it calls `0x0042F310`
  with c's word `+0`, a parent p and the code `0x10A` (`0x00426DBC`).
- Whenever word `+8` names c, whether or not c passed those tests, every record reached from c through words `+8`
  and `+0xA` (`0x004268D0`, recursively) gets the same call under the same two tests, through `0x0042DC10` (`0x00426DDF`,
  `0x00426DFA`).
- p is the switched record's word `+0`, or c's word `+6` when that is not −1. When c's byte `+0x6A0`
  (`0x003E5CF0`) is `0x1C` or more, p becomes word `+6` of p's record when that is not −1 (`0x00426D73`-`0x00426DAD`);
  when p is −1 or p's record has `+0x284` zero, that read is of address 6 and faults (`0x00426DA3`).
- `0x0042F310(i, p, code)` returns when i or p is −1. It sets bit `0x40000000` of p's record `+0x284` when bit `0x4`
  of it is set, and faults when that `+0x284` is zero, reading a null record (`0x0042F347`). When i's record has a
  non-zero `+0x284` it stores p at `+0x3CE` and the code at `+0x3CC`, and sets bit `0x80000` of `+0x290` after
  clearing bits `0x40000` and `0x100000` (`0x0042F382`-`0x0042F3A0`).

`0x00268530(mode)` brings the four roster actors' weapons in line with their engagement. For each
roster actor, the four pointers at `0x0209A1F0`, an empty one skipped (`0x00268562`), it asks `0x0030BFB0` whether
the unit should hold its weapon drawn and calls `0x002ECF10(actor, drawn, mode)`. An owner bound to a captured
member, `+0x18` = 2, is first replaced by that member through `0x003587C0(byte +0x19, word +0x1A)` when that
returns one (`0x00268564`-`0x0026857A`).

`0x00268530` then sets bit `0x2` of presentation byte `+0x154` and copies the answer into bit `0x1`; the byte
is in the actor's `+0xC0` record, and a null `+0xC0` skips both writes (`0x0026859B`-`0x002685C1`).

`0x0030BFB0` answers 0 without a battle unit or with unit bit `0x10` clear, unit bit `0x800000`
under any of the statuses `0x8000201B`, else `0x00308130` for a party-side unit (record byte `+5` 0)
and `0x00308040(unit, 0)` for any other. It reads the record `+0x698` with no null test (`0x0030BFCD`), so a
unit without a record faults there. The proximity trigger `0x0025C830` runs `0x00268530` with mode 2 when it
starts an event (`0x0025D42E`).

So `resetemergency` and `resetemergency_one(0)` sheathe instantly; only mode 1 plays the sheathe motion `0x4036`,
and only while bits `0x3` of `+0x40B` are not 0. `resetemergency_with_animetionmode(m)` turns every non-zero `m`
into mode 1, so it plays `0x4036` for any non-zero `m` and sheathes instantly for 0. `resetemergency_one(m)` passes
`m` unchanged: 1 plays `0x4036`, 2 snaps when the state differs or when it is equal while a class 3/4 sheathing
motion `0x36` runs, and any other value snaps at once.

### Thinking, cancelling and the stance machine

`setbattlethinkstatus(v)` (`0x02AA`, `0x0034E160`) calls `0x0035A720(actor, v)`: 0 sets record byte
`+9` bit `0x20` and, when the actor has a battle unit (`+0x30` non-zero, `0x0035A731`), cancels its action
(`0x00233F50(actor, 1)`, `0x002ED020`) and stops its movement (`0x0026D6D0`); non-zero clears the bit and resets the
presentation request: `0x00269D60(p, 0, 0)` on p = `+0xC0` (`0x002E97B0`) when p is non-null and its first dword is
not −1 (`0x0035A75D`-`0x0035A76F`), then `0x0026A770(actor, 0, 0)` (`0x0035A77C`).

Both arms end with `0x00226AB0(actor)` and the tail jump `0x00226A50(actor)` (`0x0035A781`-`0x0035A791`).

`setbattlethinkstatus_52e(actor, v)` (`0x052E`, `0x0034E530`) pops v, then the actor index, resolves the actor from
its first argument (`0x00359CA0(index, 1, 1)`, `0x0034E559`: the party pick of that index, focus first, hidden members
kept) and ends with the tail jump `0x0035A720(actor, v)` (`0x0034E56D`). An index at or past the end of the pick gives
a null actor (`0x00359E77`), and `0x0035A720` then faults at byte `+9` (`0x0035A72D` for v = 0, `0x0035A754` otherwise).
A negative index is not refused (signed compare, `0x00359E59`) and reads the stack slot 8 × |index| bytes below the
pick list (`0x00359E5E`).

`setbattlethinkstatus_freetarget_group(group, v)` (`0x04B7`, `0x00356530`) pops v, then the group, and applies it
through `0x0035A7A0(0, group, v)` (`0x00356560`), which walks the scene range of `0x00263FF0(0)` (first ordinal `+0x1DE`,
count `+0x1D6`), skipping those for which `0x002647B0` is non-zero (byte `+0x12` from 0 to 3, the party slots).

A group of 0 or more gives `0x0035A720(actor, v)` only to actors whose group `0x00263BE0` returns equals it
(`0x0035A7F8`); a negative group means every actor in the scene range, with the same steps inline
(`0x0035A83F`-`0x0035A8A6`). A slot that `0x00358940` answers with null (no list at `+8`, or an ordinal at or past its
count) faults at `0x002647B0`'s read of `+0x12` for a negative group or group 1 (`0x00263BE0` answers 1 for null).

`cancel_battle_think_only_crystal_talk` (`0x057A`, `0x00344740`) runs outside a town: in a town (`0x00377C20()`
non-zero) it returns at once (`0x0034474B`). Otherwise every roster member (slots 0 to 3 whose actor `0x00263750`
returns) except the controlled one (`0x00264050(0, −1)`, `0x0034477F`) has its action cancelled (`0x0035AE10(actor, 1)`,
only with a battle unit at `+0x30`, `0x00344784`) and, when `0x00233D70` says so, three presentation resets
(`0x002ECA00(actor, 1)`, `0x002EB430`, `0x002ED020`; `0x003447A2`-`0x003447BC`), whether or not it has a battle unit.

`0x00233D70(actor)` answers 1 when `0x0031B760` finds no battle unit, or when the unit has bit `0x10` set, a `+0x698`
record, and either no status of `0x80000003` or a town (`0x00313F60` → `0x00377C20`); otherwise it answers 0.
`capturepc` cancels the same way ([party during scenes](party-during-scenes.md)).

`setforcefight(a)` (`0x0483`, begin `0x003419F0`, poll `0x00342CE0` → `0x00357F00`) is a state machine
on the scratch block: the begin stores `a >= 0` at `+4`, the draw flag 0 at `+2` and `a | 0x1000000`
at `+0xC`, zeroes the state word `+0` and byte `+3`, and returns 0 (`0x00341A5F`-`0x00341A7F`). Like the
`setforcerelax` begin it pushes the three values and pops them back (`0x00341A1A`-`0x00341A55`).

The poll returns without a step when `0x002EA6A0(r)` is 0, for r = `0x00263F10(actor)`
(`0x00357F2E`): it returns that 0 (`0x00357F37`-`0x00357F46`), and a poll value of 0 ends the verb, so the verb then
finishes without a further step.

`0x002EA6A0(r)` is 1 only when r's byte `+4` is 1 and its `+0xC0` block is present,
has a first dword other than −1 and an object at `+8` whose byte `+0x18` has bit `0x2` set.

Otherwise the poll works on u = `0x00263F40(actor)` (`0x00357F23`): it waits for u to be idle (`0x002E71C0`),
draws the weapon (state 3: `0x002ECF10(u, 1, 1)`, `0x002E8540(u, 1)`, and `0x002E9B40(u)` stored at `+8`),
waits again, and in state 5 calls `0x003DDB40(u, 0, +0xC)` when `+4` is set, then finishes at 7. The poll returns 1,
which keeps the verb waiting, until the state word is 7, and 0 then (`0x0035808C`-`0x00358095`); a state word above 5
takes no step (`0x00357F4E`).

`setforcerelax(a)` (`0x02E0`, begin `0x00341600`, the same poll) sheathes. Its begin pushes 9 and 1
before the same three pops (`0x00341615`, `0x00341628`), so the draw flag `+2` is 1, `+0xC` is
`9 | 0x1000000` (stance entry 9) and `+4` is a itself (`0x00341656`-`0x00341669`). With the flag set:

- state 3 sheathes: `0x002E5BC0(u, 0.0)`, `0x002ECF10(u, 0, 1)` and `0x002E8540(u, 0)` (`0x00357FA2`-`0x00357FC8`);
- state 4 moves on once u is idle, or while its motion still runs once `0x002E4E00(u)` reaches 16
  (`0x00358015`-`0x00358036`), which sets `+3` (`0x00358038`);
- state 5 gives `0x003DDB40` a blend of 4 when `+3` is set and 0 otherwise (`0x00358055`-`0x0035806C`).

`0x003DDB40` sets or clears bit `0x80000` of the render record's `+0x284` through `0x002E8170`, from bit `0x80` of
byte `+0xD` of `0x00263F40(actor)`, and plays a motion through `0x002EB3E0`: with bit `0x1000000` of its argument
set (the `setforcefight` and `setforcerelax` begins always set it) the stance motion `0x01EFE9D0[a & 0xFFFFFF]` (u32
entries, no bound check), otherwise `(actor +0x15) << 20 | a | 0x1000`. A negative argument skips
state 5, so it draws only.

`clearforcefight` (`0x0484`, begin `0x00343770` → `0x00343290`) is `setforcefight`'s pair, and `clearforcerelax`
(`0x02E1`) runs the same begin `0x00343290`. On a = `0x00263F40(actor)` (`0x003432B0`) it calls `0x002E9B40(a)`,
`0x0026A770(a, 0, 0)` and `0x002E5BC0(a, 0)`, then `0x002ECF10(a, d, 1)`. On the record r = `0x00263F10(actor)`
(`0x003432A5`; [battle units](../Characters-And-Objects/battle-units.md), "The script queries") it ends with
`0x002E8540(r, d)` (`0x00343318`), where d = (`0x0030BFB0(r)` ≠ 0) (`0x003432C3`), drawing or sheathing to match the
battle state of r's unit.

`setforcefightmode` (`0x0334`, `0x003444D0`) is a different verb that writes the force-fight
toggle ([force fight mode](../Engine-Core/force-fight-mode.md)).

### Battle setup grants

`btlAtelSetAbility(a, b)` (`0x3000`, `0x00510440` → `0x002390B0`) rebuilds the unit's script-granted
ability set at `+0xE80`: `+0xE80..+0xE8F` are zeroed, then bit `31 − k` is set for each set bit `k`
of `a` and bit `63 − k` for each set bit of `b` (`0x04000000` in `b` sets bit `0x2000000000`). The set's
upper 64 bits (`+0xE88` to `+0xE8F`) stay zero. For an actor without a battle unit (`0x0031B760` gives 0)
`0x002390B0` returns at once and writes nothing (`0x002390CA`).

`btlAtelSetStatus(ref)` (`0x3002`, `0x005103B0` → `0x002394C0`) returns at once for an actor without a battle
unit (`0x002394D9`). Otherwise it zeroes `+0xE90` (`0x002394FC`), reads a table of 32 two-bit values
through a reference (`0x002650B0`) and sets bit `i` of `+0xE90` for value 3. Values 1 and 2 are applied at once
through `0x0030EAE0(record +0x698, 0, i, -1, -1, 0x297)` (`0x00239556`-`0x00239577`). The dword `[[unit + 0x6A0]]`
is read with no null test on `+0x6A0` (`0x002394DF`-`0x002394F7`), so a null `+0x6A0` faults there.

The applies run only when dword `[[unit + 0x6A0]] & 5` is 0, and value 1 also
needs `0x00328370()` bit `0x1`, a draw of the generator at `0x022C256C`
([random number generators](../Random-Numbers/random-number-generators.md)).

The ability list rebuild `0x0030FED0` reads both, only for a record with `+5` = 1: each `+0xE80` bit
becomes `0x0030E130` (`0x00310047`) and each `+0xE90` bit becomes `0x0030E360(unit, 0, i, 0)` (`0x003103E0`).
This covers an immediate-displacement search for `+0xE80`, `+0xE88` and `+0xE90`; the other hits are
the reset `0x00236A60` and functions on other objects.

The rebuild also runs from the equipment setters `0x0031A410`, `0x0031A510` and `0x0031A630` and the licence setter
`0x00323910` ([equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)), and from the level growth `0x0030C470`
and `0x0030C650` ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)).

### Verbs that do not touch battle decisions

`battlemotionplay` (`0x0450`, `0x0050E980`) pops two values and does nothing. `setfightmode`
(`0x01A7`, `0x0034CB60`) is `0x002E8540(actor, v)`, the drawn-weapon state, and `ignorebattlemovectrl`
(`0x04E7`, `0x00341DB0`) is `0x002EBC40(actor, v)`.

`suspendbattle` (`0x0069`) and `suspendbattle_resetmotion` (`0x0586`) share `0x00356970`, which runs
the pause `0x0035AB20` and the motion reset `0x0035A680`. The pause sets `0x02089340` bits `0x20`
(`0x00238B70(1)`, which also sends motion `0x30B` through `0x002E7C10` to every flagged entry of
`[0x0208E688]`) and `0x80` (`0x00238AE0(1)`), then calls `0x0035A590`.

The motion reset calls `0x002EB430`
on every actor of the scene range that has a battle unit, when scene byte `+0x10` bit `0x1` is set
(`0x0035A694`; the scene is `0x00263FF0(0)`, the range runs from ordinal `+0x1DE` for `+0x1D6` actors, and the battle
unit test reads `+0x30`, `0x0035A6BE`). A slot that `0x00358940` answers with null (no list at `+8`, or an ordinal at
or past its count) faults at that read.
`suspendbattle_no_resetmotion` (`0x0587`, `0x00347460` → `0x0035AB20`) is the pause alone.

## Layouts

Battle unit:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` | unitFlags | low dword of the u64: bit `0x4000` issued command, bit `0x400000` no attacker registration, bit `0x800000` stance |
| `+0x004` | `u32` | unitFlags high dword | mask `0x600` emergency (mask `0x60000000000` of the u64), bit `0x10000` engaged |
| `+0x6B0` | `...` | commandStanceFlags | bit `0x2` issued without target |
| `+0x6E0` | `...` | order set | one of the four order sets |
| `+0x6E8` | `...` | order set | one of the four order sets |
| `+0x6F0` | `...` | order set | one of the four order sets |
| `+0x6F8` | `...` | order set | one of the four order sets |
| `+0x700-0x717` | `...` | action block | holds the next three rows |
| `+0x708` | `...` |  | action context |
| `+0x710` | `...` |  | target focus |
| `+0x714` | `u16` |  | action id |
| `+0x718-0x72F` | `...` | block copy | copy of the block |
| `+0x748` | `...` |  | transient-set target |
| `+0x750` | `...` |  | shared target |
| `+0x754` | `...` |  | shared target |
| `+0xBA0` | `u16` |  | issued command id |
| `+0xBA4` | `u16` | issued order flags | the flags word of the issued order at `+0xBA0`: bit `0x8000` set on issue (`0x00311DBB`) |
| `+0xBB8` | `...` |  | issued target |
| `+0xDCC` | `u32` | stanceRecheckDeadlineTick |  |
| `+0xE80` | `u64[2]` |  | script abilities |
| `+0xE90` | `u32` |  | script statuses |
| `+0xEA4` | `...` |  | attackers mask |
| `+0xEA8` | `u8` |  | attacker count |
| `+0xEA9` | `u8` |  | unit index |

Order sets:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01EEC3C0` | `...` | order set | party default |
| `0x01EEC410` | `...` | order set | non-party default |
| `0x01EEC2D0` | `...` | order set | issued transient |
| `0x01EEC2B0` | `...` | order set | engage auto-attack |
| `0x01EEC320` | `...` | order set | status cases |
| `0x01EEC370` | `...` | order set | status cases |
| `0x01EEC298` | `...` | order set | final fallback |

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01EFE9D0` | `...` | stance table | u32 motion ids `0x1001`, `0x1001`, `0x101A`, `0x1018`, `0x1019`, `0x1009`, `0x100A`, `0x403D`, `0x101C`, `0x301B`, … |

Render record [`0x022C6F28`] + idx × `0x740`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x284` | `...` | objectFlags | bit `0x80000` set by draw and sheathe |
| `+0x294` | `...` |  | motion flags |
| `+0x40B` | `...` | flagByte40B | mask `0x3` drawn state |

## Shipped data

| Fact | Value |
|---|---|
| commit callers | 5 sites in 4 functions |
| issued-command callers | 3 sites in 2 functions; the verb `resetJobs` reaches one with the fixed id `0x113` |
| `0x0030F2D0` callers | the three reset verbs only |
| uses in the US scripts | `setforcefight` 2,107 in 343 files; `clearforcefight` 2,120 in 346 files; `setemergency` 104; `setemergency_one` 74; `setforcefightmode` 177 |
| `setbattlethinkstatus_freetarget_group` uses | 1,514, all with group −1: 1,498 × (−1, 0) and 16 × (−1, 1) |
| `btlAtelSetAbility` / `btlAtelSetStatus` uses | 6,746 each |

## Operations

Per emergency verb: one flag write per party-slot unit and one draw request. Per reset verb: one
order-set install and one sheathe per unit. Per `setforcefight`: one poll per frame through
states 0 to 7.

## State

The unit's flag dwords, order-set pointers, action block and its copy, the issued-command fields,
the two script grant words; the render record's drawn state; `0x022C1F48` and `0x022C1F40`.

## Modding notes

- A script cannot make a character use a chosen command; it can engage, disengage, draw, sheathe,
  stop thinking or change the stance. The one script-reachable issue is `resetJobs` on the recorded
  character, which issues command `0x113` to the party-slot-3 unit.
- `setemergency` wears off by itself once no target qualifies; `resetemergency` ends it at once,
  sheathes instantly and reinstalls the default gambit set.
- `setbattlethinkstatus(0)` freezes a character mid-fight: it cancels the action and stops movement
  in one call.
- `setforcefight` with a negative argument only draws the weapon; `clearforcefight` returns the
  weapon to whatever the unit's battle state calls for.
- `battlemotionplay` is inert in this build.

## Related

- [Party during scenes](party-during-scenes.md): the capture that cancels an action.
- [Force fight mode](../Engine-Core/force-fight-mode.md): the toggle behind `setforcefightmode`.
- [Script verb table](verb-table.md): the ids and handlers.
