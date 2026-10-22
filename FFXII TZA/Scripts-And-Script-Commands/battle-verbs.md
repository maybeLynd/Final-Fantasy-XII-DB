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

It then clears `+0x700` bits 0-1, stores the context at `+0x708`, the target at `+0x710` and the id
at `+0x714`, zeroes byte `+0x6B4`, and copies the 0x18 bytes `+0x700..+0x717` to `+0x718..+0x72F`.
A pending no-target issue (`+0x6B0` bit 1) is consumed into `+0x6B9` from `0x022C1DB8`.

For a target and an id below `0x21F`: when `0x0030AB40(unit, target, 0)` is above 1, `+0x754` takes the
target, and when the unit's `+8` equals its `+0x24`, every unit of the `0x00236820` list with the same
`+0x24` that is not KO'd or petrified (outside a town) gets `+0x754` = target and the unit's `+0x750`
= target. While unit flag bit 22 (`0x400000`) is clear and the attacker is not yet registered, it
sets bit `+0xEA9` of the target's `+0xEA4`, adds one to `+0xEA8`, and calls `0x00313B30(unit, target, 1)`.

Its callers are 5 sites in 4 functions: the next-action selector `0x00305AB0` (`0x00305B2F`, `0x00305C9B`),
the order-set scanner `0x00305CC0` (`0x00305DF4`), the combo continuation `0x0030FA00` (`0x0030FA5C`) and the
engage auto-attack `0x00312FA0` (`0x003130DC`). `0x00312FA0` sets flag bit 22 just before its commit
(`0x0030F760(unit, 0x01EEC2B0, 0x96, target, 0)`, target from `+0x28`, cleared on read), so that action
never registers as an attacker.

### How the next action is chosen

`0x00305AB0(unit, mode)` tries each source in order and stops at the first commit. The scanner
`0x00305CC0` passes as context the 0x18-byte entry inside the set (`set + 0x20 + n × 0x18`). A town is
a map whose word in `[0x02ADD100]` has bit 15 set (`0x00377C20`).

1. Flag bit 22 set: `0x00308270` first. Flag `0x4000`: the flag is cleared and the issued command
   `+0xBA0` commits with context `unit + 0xBA0` and target `+0xBB8` when its id is in
   `0x4000..0x4166` or `0x002FFCF0(id, unit)` is 0.
2. In a town with a party record (`[+0x698] + 5` = 0): straight to step 6.
3. Outside a town with status `0x20`, or a non-party record (`+5` = 1) with status `0x08000000`:
   scan `0x01EEC320`, then step 6.
4. Otherwise scan the order set `+0x6E8`. Then, outside a town for a party unit with `0x08000000`:
   scan `0x01EEC370`. Else, for a null or non-party record or one with dword bit 2: scan `+0x6E0`
   with byte `+0x6B5`, clearing `+0x6F8` and `+0x748`. Else scan `+0x6F8` when set, then clear it.
5. Scan `+0x6F0`.
6. With mode 0: commit `0x01EEC298` with id `[0x01EEC298]`, no target.

### Issuing a command

`0x00311CF0(unit, target, arg, id, transient)` writes the issued command. It refuses (returns
`0xFFFFFFFE`) a unit with no record `+0x698`, a unit with statuses `0x80000003` outside a town, and
id `0x113` while `+0x714` is `0x113`; id `0x113` also clears bit 0 of word `[0x02EBF190] + 0x5AD0`.

While statuses `0x8800203B` are clear it stores the id at `+0xBA0`, sets `+0xBA4` bit 15 and flag
`0x4000`, stores the target at `+0xBB8` (with no target: the unit's own `+8`, `+0x6B0` bit 1 set and
`0x022C1DB8[+0xEA9 × 0xC]` = arg), and with a target and a non-zero transient argument stores the
target at `+0x748` and the transient set `0x01EEC2D0` at `+0x6F8`; then it calls `0x00317E60`. It returns
0 otherwise, including when a status drops the command silently.

Its callers are the menu path `0x00311B20` (two sites), which the battle menu `0x002778C0` calls
([battle menu](../Menus-And-HUD/battle-menu.md)), and `0x003138D0`. The one verb that reaches it is
`resetJobs` (`0x05D6`, `0x00342230` → `0x00328BD0`): resetting the character recorded at
`[0x02EBF190] + 0x5AD5` (`0x003137F0`) runs `0x003138D0(1)`, which issues the fixed command `0x113` to the
party-slot-3 unit (`0x0031B8C0(3)`) with itself as target. `0x003138D0` acts only when `0x0030D9A0()` is 1,
the unit's `+0x714` is not `0x113`, and it does not already hold an issued `0x113`. No verb passes a
script-chosen id.

### Emergency and reset

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setemergency` | `0x03BF` | `0x00346EB0` | `0x00311E90`: each party-slot unit 0-3 (`0x0031B810`) that is not KO'd or petrified (statuses `0x80000003`, except in a town) is collected at `0x022C1788` and gets dword `+4` bits 9 and 10 (`0x600`); then `0x002ECF10(actor, 1, 1)` for slots 0 to 3 |
| `setemergency_one` | `0x0546` | `0x003460C0` | `0x00311F50` on the target unit (no KO or petrify check), then the draw |
| the unnamed `0x05CC` | `0x05CC` | `0x00346620` | `0x00311F50`, then `0x002ECF10(actor, 1, mode)` with a popped mode |
| `resetemergency` | `0x0554` | `0x00347970` | pushes 0, then for slots 0 to 3: `0x0030F2D0`, then `0x002ECF10(actor, 0, 0)` |
| `resetemergency_with_animetionmode(m)` | `0x0555` | `0x003473E0` | the same with mode `m` |
| `resetemergency_one(m)` | `0x057F` | `0x00346A10` | the same for one actor |
| `refresh_party_fightmotion(m)` | `0x0566` | `0x003446D0` | `0x00268530(m)`, then `0x0035AE10(actor, 1)` for slots 0 to 3 |

Bits 9 and 10 are tested in the engagement update `0x00307D10` (`0x00307D84`, `0x00307DA7`, `0x00307DD1`):
with bit 9 set the unit counts as engaged while `0x0030B050` finds a qualifying target, bit 10 grants
one grace pass, and the bits clear themselves afterwards. `0x00307D10` also clears them at once in a
town and when the unit flees (`0x00253B90`). This covers the operand search of the whole image for
`[reg + 4]` with `0x200`, `0x400`, `0x600` or `0xFFFFF9FF` and byte `+5` tests.

`0x002FEDC0`, `0x00301140` and `0x00313480` also clear bits 9, 10 and 16 (`and [+4], 0xFFFEF9FF` at
`0x002FEDC6`, `0x00301231`, `0x003134A5`). Statuses `0x08000020` hold a unit engaged without these bits.

`0x0030F2D0`, whose only callers are the three reset verbs (`0x00346A35`, `0x00347413`, `0x003479B2`), clears
bits 1-2 of `0x022C1F48`, zeroes `0x022C1F40` and `+0xDCC`, clears flag `0x800000` and `+4` bits 9, 10 and
16, and installs the default order set at `+0x6E8`: `0x01EEC3C0` when `[+0x698] + 5` is 0, `0x01EEC410`
otherwise.

`0x002ECF10(actor, drawn, mode)` resolves the actor's render record (`[0x022C6F28] + index × 0x740`,
used only when `+0x284` is non-zero) and continues in `0x00426130`:

- Mode 1: when bits 0-1 of `+0x40B` differ from `drawn`, it sets them, plays motion `0x4035` (draw)
  or `0x4036` (sheathe) through `0x00427320`, updates `+0x294` and sets `+0x284` bit 19. Otherwise
  nothing.
- Mode 2: when the state differs, or it is equal while a class 3/4 motion at `+0xCC` or `+0x3B4` has
  low 12 bits `0x35` (drawing) or `0x36` (sheathing), it snaps through `0x00426C90`; otherwise nothing.
- Any other mode: `0x00426C90(record, drawn)` sets the state at once, sets `+0x284` to
  `(+0x284 & 0x6FFFFFFF) | 0x10000000`, plays motion `0x1001` and updates `+0x294`.

`0x00268530(mode)` brings the four roster actors' weapons in line with their engagement. For each
roster actor (an owner bound to a captured member, `+0x18` = 2, is replaced by that member through
`0x003587C0`) it asks `0x0030BFB0` whether the unit should hold its weapon drawn and calls
`0x002ECF10(actor, drawn, mode)`; it then sets bit 1 of presentation byte `+0x154` and copies the
answer into bit 0.

`0x0030BFB0` answers 0 without a battle unit or with unit bit 4 clear, unit bit 23
under any of the statuses `0x8000201B`, else `0x00308130` for a party-side unit (record byte `+5` 0)
and `0x00308040(unit, 0)` for any other. The proximity trigger `0x0025C830` runs `0x00268530` with mode 2 when it
starts an event (`0x0025D42E`).

So `resetemergency` and `resetemergency_one(0)` sheathe instantly; only a non-zero mode 1 plays the
sheathe motion `0x4036`.

### Thinking, cancelling and the stance machine

`setbattlethinkstatus(v)` (`0x02AA`, `0x0034E160`) calls `0x0035A720(actor, v)`: 0 sets record byte
`+9` bit 5 and, when the actor has a battle unit, cancels its action (`0x00233F50(actor, 1)`,
`0x002ED020`) and stops its movement (`0x0026D6D0`); non-zero clears the bit and resets the
presentation request (`0x00269D60`, `0x0026A770`). Both arms end with `0x00226AB0` and `0x00226A50`.

`setbattlethinkstatus_52e(actor, v)` (`0x052E`, `0x0034E530`) resolves the actor from its first
argument (`0x00359CA0`). `setbattlethinkstatus_freetarget_group(group, v)` (`0x04B7`, `0x00356530`)
applies it through `0x0035A7A0`; a negative group means every actor in the scene range, skipping those
for which `0x002647B0` is non-zero.

`cancel_battle_think_only_crystal_talk` (`0x057A`, `0x00344740`) runs outside a town: every roster
member except the controlled one has its action cancelled (`0x0035AE10`) and, when `0x00233D70` says
so, three presentation resets (`0x002ECA00`, `0x002EB430`, `0x002ED020`). `capturepc` cancels the same
way ([cutscenes](cutscenes-and-the-world-lock.md)).

`setforcefight(a)` (`0x0483`, begin `0x003419F0`, poll `0x00342CE0` → `0x00357F00`) is a state machine
on the scratch block: the begin stores `a >= 0` at `+4`, the draw flag 0 at `+2` and `a | 0x1000000`
at `+0xC`. The poll returns without a step while `0x002EA6A0(actor)` is 0; it waits for the actor to
be idle (`0x002E71C0`), draws the weapon (state 3: `0x002ECF10(actor, 1, 1)`, `0x002E8540(actor, 1)`, and
`0x002E9B40(actor)` stored at `+8`), waits again, and in state 5 calls `0x003DDB40(actor, 0, +0xC)` when
`+4` is set, then finishes at 7.

`0x003DDB40` sets or clears bit 19 of the render record's `+0x284` through `0x002E8170`, from bit 7 of
byte `+0xD` of `0x00263F40(actor)`, and plays a motion through `0x002EB3E0`: with bit 24 of its argument
set (the `setforcefight` begin always sets it) the stance motion `0x01EFE9D0[a & 0xFFFFFF]` (u32
entries, no bound check), otherwise `(actor +0x15) << 20 | a | 0x1000`. A negative argument skips
state 5, so it draws only.

`clearforcefight` (`0x0484`, begin `0x00343770` → `0x00343290`) is `setforcefight`'s pair: it calls
`0x002E9B40`, `0x0026A770(actor, 0, 0)` and `0x002E5BC0(actor, 0)`, then `0x002ECF10(actor, d, 1)` and
`0x002E8540(unit, d)` with d = (`0x0030BFB0(unit)` ≠ 0), drawing or sheathing to match the unit's battle
state. `setforcefightmode` (`0x0334`, `0x003444D0`) is a different verb that writes the force-fight
toggle ([force fight mode](../Engine-Core/force-fight-mode.md)).

### Battle setup grants

`btlAtelSetAbility(a, b)` (`0x3000`, `0x00510440` → `0x002390B0`) rebuilds the unit's script-granted
ability set at `+0xE80`: `+0xE80..+0xE8F` are zeroed, then bit `31 − k` is set for each set bit `k`
of `a` and bit `63 − k` for each set bit of `b` (`0x04000000` in `b` sets bit 37). Bits 64-127 stay
zero.

`btlAtelSetStatus(ref)` (`0x3002`, `0x005103B0` → `0x002394C0`) reads a table of 32 two-bit values
through a reference (`0x002650B0`) and sets bit `i` of `+0xE90` for value 3. Values 1 and 2 are
applied at once through `0x0030EAE0`, only when dword `[[unit + 0x6A0]] & 5` is 0, and value 1 also
needs `0x00328370()` bit 0, a draw of the generator at `0x022C256C`
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
`[0x0208E688]`) and `0x80` (`0x00238AE0(1)`), then calls `0x0035A590`. The motion reset calls `0x002EB430`
on every actor of the scene range that has a battle unit, when scene byte `+0x10` bit 0 is set.
`suspendbattle_no_resetmotion` (`0x0587`, `0x00347460` → `0x0035AB20`) is the pause alone.

## Layouts

```
battle unit   +0 u32 flags (bit 14 issued command, bit 22 no attacker registration, bit 23 stance), +4 u32 (bits 9-10 emergency, bit 16 engaged),
              +0x6B0 bit 1 issued without target, +0x6E0 / +0x6E8 / +0x6F0 / +0x6F8 order sets, +0x700..+0x717 action block:
              +0x708 action context, +0x710 target focus, +0x714 u16 action id; +0x718..+0x72F copy of the block,
              +0x748 transient-set target, +0x750 / +0x754 shared target, +0xBA0 u16 issued command id, +0xBA4 bit 15 set on issue,
              +0xBB8 issued target, +0xDCC u32, +0xE80 u64[2] script abilities, +0xE90 u32 script statuses,
              +0xEA4 attackers mask, +0xEA8 u8 attacker count, +0xEA9 u8 unit index
order sets    0x01EEC3C0 party default, 0x01EEC410 non-party default, 0x01EEC2D0 issued transient, 0x01EEC2B0 engage auto-attack,
              0x01EEC320 / 0x01EEC370 status cases, 0x01EEC298 final fallback
stance table  0x01EFE9D0: u32 motion ids 0x1001, 0x1001, 0x101A, 0x1018, 0x1019, 0x1009, 0x100A, 0x403D, 0x101C, 0x301B, …
render record [0x022C6F28] + idx × 0x740: +0x40B bits 0-1 drawn state, +0x284 bit 19 set by draw and sheathe, +0x294 motion flags
```

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

- [Cutscenes and the world lock](cutscenes-and-the-world-lock.md): the capture that cancels an action.
- [Force fight mode](../Engine-Core/force-fight-mode.md): the toggle behind `setforcefightmode`.
- [Script verb table](verb-table.md): the ids and handlers.
