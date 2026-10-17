---
title: "Battle verbs: what a script can do to a unit's battle actions, the one commit every action passes through, and the verbs that change stance, thinking and emergency state"
kind: "system"
category: "Scripts and script commands"
addresses: "0030F760, 00305AB0, 0030FA00, 00312FA0, 00311CF0, 00311B20, 003138D0, 00346EB0, 003460C0, 00346620, 00311E90, 00311F50, 00307D10, 00347970, 003473E0, 00346A10, 0030F2D0, 01EEC3C0, 01EEC410, 002ECF10, 0034E160, 0035A720, 00356530, 00344740, 0035AE10, 003419F0, 00357F00, 003DDB40, 01EFE9D0, 00510440, 002390B0, 005103B0, 002394C0, 0034CB60, 00341DB0, 0050E980, 00356970, 003444D0, 00305CC0, 003105D0, 0030AB40, 00313B30, 00308270, 002FFCF0, 01EEC298, 01EEC320, 01EEC370, 01EEC2B0, 01EEC2D0, 00317E60, 00342230, 00328BD0, 003137F0, 0030D9A0, 0031B8C0, 00426130, 00426C90, 002FEDC0, 00301140, 00313480, 0034E530, 0035A7A0, 00343290, 0030BFB0, 0035AB20, 0035A680, 00347460, 00238B70, 00238AE0, 0030FED0, 0030E130, 0030E360, 0030EAE0, 003446D0, 00268530"
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

`0030F760(unit, orderContext, actionId, targetFocus, mode)` is the only place an action becomes
the unit's current action. With a non-zero mode it first calls `003105D0`. An id below `21F`<sub>h</sub>
refreshes the target link at `+778`<sub>h</sub> (`00316CF0`, `00316CD0`); any other id outside
`C000h..C166h` is refused (return 0).

It then clears `+700`<sub>h</sub> bits 0-1, stores the context at `+708`<sub>h</sub>, the target at `+710`<sub>h</sub> and the id
at `+714`<sub>h</sub>, zeroes byte `+6B4`<sub>h</sub>, and copies the `18`<sub>h</sub> bytes `+700h..+717h` to `+718h..+72Fh`.
A pending no-target issue (`+6B0`<sub>h</sub> bit 1) is consumed into `+6B9`<sub>h</sub> from `022C1DB8`.

For a target and an id below `21F`<sub>h</sub>: when `0030AB40(unit, target, 0)` is above 1, `+754`<sub>h</sub> takes the
target, and when the unit's `+8` equals its `+24`<sub>h</sub>, every unit of the `00236820` list with the same
`+24`<sub>h</sub> that is not KO'd or petrified (outside a town) gets `+754`<sub>h</sub> = target and the unit's `+750`<sub>h</sub>
= target. While unit flag bit 22 (`400000`<sub>h</sub>) is clear and the attacker is not yet registered, it
sets bit `+EA9`<sub>h</sub> of the target's `+EA4`<sub>h</sub>, adds one to `+EA8`<sub>h</sub>, and calls `00313B30(unit, target, 1)`.

Its callers are 5 sites in 4 functions: the next-action selector `00305AB0` (`00305B2F`, `00305C9B`),
the order-set scanner `00305CC0` (`00305DF4`), the combo continuation `0030FA00` (`0030FA5C`) and the
engage auto-attack `00312FA0` (`003130DC`). `00312FA0` sets flag bit 22 just before its commit
(`0030F760(unit, 01EEC2B0, 96h, target, 0)`, target from `+28`<sub>h</sub>, cleared on read), so that action
never registers as an attacker.

### How the next action is chosen

`00305AB0(unit, mode)` tries each source in order and stops at the first commit. The scanner
`00305CC0` passes as context the `18`<sub>h</sub>-byte entry inside the set (`set + 20h + n × 18h`). A town is
a map whose word in `[02ADD100]` has bit 15 set (`00377C20`).

1. Flag bit 22 set: `00308270` first. Flag `4000`<sub>h</sub>: the flag is cleared and the issued command
   `+BA0`<sub>h</sub> commits with context `unit + BA0h` and target `+BB8`<sub>h</sub> when its id is in
   `C000h..C166h` or `002FFCF0(id, unit)` is 0.
2. In a town with a party record (`[+698h] + 5` = 0): straight to step 6.
3. Outside a town with status `20`<sub>h</sub>, or a non-party record (`+5` = 1) with status `08000000`<sub>h</sub>:
   scan `01EEC320`, then step 6.
4. Otherwise scan the order set `+6E8`<sub>h</sub>. Then, outside a town for a party unit with `08000000`<sub>h</sub>:
   scan `01EEC370`. Else, for a null or non-party record or one with dword bit 2: scan `+6E0`<sub>h</sub>
   with byte `+6B5`<sub>h</sub>, clearing `+6F8`<sub>h</sub> and `+748`<sub>h</sub>. Else scan `+6F8`<sub>h</sub> when set, then clear it.
5. Scan `+6F0`<sub>h</sub>.
6. With mode 0: commit `01EEC298` with id `[01EEC298]`, no target.

### Issuing a command

`00311CF0(unit, target, arg, id, transient)` writes the issued command. It refuses (returns
`FFFFFFFE`<sub>h</sub>) a unit with no record `+698`<sub>h</sub>, a unit with statuses `80000003`<sub>h</sub> outside a town, and
id `113`<sub>h</sub> while `+714`<sub>h</sub> is `113`<sub>h</sub>; id `113`<sub>h</sub> also clears bit 0 of word `[02EBF190] + 5AD0h`.

While statuses `8800203B`<sub>h</sub> are clear it stores the id at `+BA0`<sub>h</sub>, sets `+BA4`<sub>h</sub> bit 15 and flag
`4000`<sub>h</sub>, stores the target at `+BB8`<sub>h</sub> (with no target: the unit's own `+8`, `+6B0`<sub>h</sub> bit 1 set and
`022C1DB8[+EA9h × Ch]` = arg), and with a target and a non-zero transient argument stores the
target at `+748`<sub>h</sub> and the transient set `01EEC2D0` at `+6F8`<sub>h</sub>; then it calls `00317E60`. It returns
0 otherwise, including when a status drops the command silently.

Its callers are the menu path `00311B20` (two sites), which the battle menu `002778C0` calls
([battle menu](../Menus-And-HUD/battle-menu.md)), and `003138D0`. The one verb that reaches it is
`resetJobs` (`05D6`<sub>h</sub>, `00342230` → `00328BD0`): resetting the character recorded at
`[02EBF190] + 5AD5h` (`003137F0`) runs `003138D0(1)`, which issues the fixed command `113`<sub>h</sub> to the
party-slot-3 unit (`0031B8C0(3)`) with itself as target. `003138D0` acts only when `0030D9A0()` is 1,
the unit's `+714`<sub>h</sub> is not `113`<sub>h</sub>, and it does not already hold an issued `113`<sub>h</sub>. No verb passes a
script-chosen id.

### Emergency and reset

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `setemergency` | `03BF`<sub>h</sub> | `00346EB0` | `00311E90`: each party-slot unit 0-3 (`0031B810`) that is not KO'd or petrified (statuses `80000003`<sub>h</sub>, except in a town) is collected at `022C1788` and gets dword `+4` bits 9 and 10 (`600`<sub>h</sub>); then `002ECF10(actor, 1, 1)` for slots 0 to 3 |
| `setemergency_one` | `0546`<sub>h</sub> | `003460C0` | `00311F50` on the target unit (no KO or petrify check), then the draw |
| the unnamed `05CC`<sub>h</sub> | `05CC`<sub>h</sub> | `00346620` | `00311F50`, then `002ECF10(actor, 1, mode)` with a popped mode |
| `resetemergency` | `0554`<sub>h</sub> | `00347970` | pushes 0, then for slots 0 to 3: `0030F2D0`, then `002ECF10(actor, 0, 0)` |
| `resetemergency_with_animetionmode(m)` | `0555`<sub>h</sub> | `003473E0` | the same with mode `m` |
| `resetemergency_one(m)` | `057F`<sub>h</sub> | `00346A10` | the same for one actor |
| `refresh_party_fightmotion(m)` | `0566`<sub>h</sub> | `003446D0` | `00268530(m)`, then `0035AE10(actor, 1)` for slots 0 to 3 |

Bits 9 and 10 are tested in the engagement update `00307D10` (`00307D84`, `00307DA7`, `00307DD1`):
with bit 9 set the unit counts as engaged while `0030B050` finds a qualifying target, bit 10 grants
one grace pass, and the bits clear themselves afterwards. `00307D10` also clears them at once in a
town and when the unit flees (`00253B90`). This covers the operand search of the whole image for
`[reg + 4]` with `200`<sub>h</sub>, `400`<sub>h</sub>, `600`<sub>h</sub> or `FFFFF9FF`<sub>h</sub> and byte `+5` tests.

`002FEDC0`, `00301140` and `00313480` also clear bits 9, 10 and 16 (`and [+4], FFFEF9FFh` at
`002FEDC6`, `00301231`, `003134A5`). Statuses `08000020`<sub>h</sub> hold a unit engaged without these bits.

`0030F2D0`, whose only callers are the three reset verbs (`00346A35`, `00347413`, `003479B2`), clears
bits 1-2 of `022C1F48`, zeroes `022C1F40` and `+DCC`<sub>h</sub>, clears flag `800000`<sub>h</sub> and `+4` bits 9, 10 and
16, and installs the default order set at `+6E8`<sub>h</sub>: `01EEC3C0` when `[+698h] + 5` is 0, `01EEC410`
otherwise.

`002ECF10(actor, drawn, mode)` resolves the actor's render record (`[022C6F28] + index × 740h`,
used only when `+284`<sub>h</sub> is non-zero) and continues in `00426130`:

- Mode 1: when bits 0-1 of `+40B`<sub>h</sub> differ from `drawn`, it sets them, plays motion `4035`<sub>h</sub> (draw)
  or `4036`<sub>h</sub> (sheathe) through `00427320`, updates `+294`<sub>h</sub> and sets `+284`<sub>h</sub> bit 19. Otherwise
  nothing.
- Mode 2: when the state differs, or it is equal while a class 3/4 motion at `+CC`<sub>h</sub> or `+3B4`<sub>h</sub> has
  low 12 bits `35`<sub>h</sub> (drawing) or `36`<sub>h</sub> (sheathing), it snaps through `00426C90`; otherwise nothing.
- Any other mode: `00426C90(record, drawn)` sets the state at once, sets `+284`<sub>h</sub> to
  `(+284h & 6FFFFFFFh) | 10000000h`, plays motion `1001`<sub>h</sub> and updates `+294`<sub>h</sub>.

`00268530(mode)` brings the four roster actors' weapons in line with their engagement. For each
roster actor (an owner bound to a captured member, `+18`<sub>h</sub> = 2, is replaced by that member through
`003587C0`) it asks `0030BFB0` whether the unit should hold its weapon drawn and calls
`002ECF10(actor, drawn, mode)`; it then sets bit 1 of presentation byte `+154`<sub>h</sub> and copies the
answer into bit 0.

`0030BFB0` answers 0 without a battle unit or with unit bit 4 clear, unit bit 23
under any of the statuses `8000201B`<sub>h</sub>, else `00308130` for a party-side unit (record byte `+5` 0)
and `00308040(unit, 0)` for any other. The proximity trigger `0025C830` runs `00268530` with mode 2 when it
starts an event (`0025D42E`).

So `resetemergency` and `resetemergency_one(0)` sheathe instantly; only a non-zero mode 1 plays the
sheathe motion `4036`<sub>h</sub>.

### Thinking, cancelling and the stance machine

`setbattlethinkstatus(v)` (`02AA`<sub>h</sub>, `0034E160`) calls `0035A720(actor, v)`: 0 sets record byte
`+9` bit 5 and, when the actor has a battle unit, cancels its action (`00233F50(actor, 1)`,
`002ED020`) and stops its movement (`0026D6D0`); non-zero clears the bit and resets the
presentation request (`00269D60`, `0026A770`). Both arms end with `00226AB0` and `00226A50`.

`setbattlethinkstatus_52e(actor, v)` (`052E`<sub>h</sub>, `0034E530`) resolves the actor from its first
argument (`00359CA0`). `setbattlethinkstatus_freetarget_group(group, v)` (`04B7`<sub>h</sub>, `00356530`)
applies it through `0035A7A0`; a negative group means every actor in the scene range, skipping those
for which `002647B0` is non-zero.

`cancel_battle_think_only_crystal_talk` (`057A`<sub>h</sub>, `00344740`) runs outside a town: every roster
member except the controlled one has its action cancelled (`0035AE10`) and, when `00233D70` says
so, three presentation resets (`002ECA00`, `002EB430`, `002ED020`). `capturepc` cancels the same
way ([cutscenes](cutscenes-and-the-world-lock.md)).

`setforcefight(a)` (`0483`<sub>h</sub>, begin `003419F0`, poll `00342CE0` → `00357F00`) is a state machine
on the scratch block: the begin stores `a >= 0` at `+4`, the draw flag 0 at `+2` and `a | 1000000h`
at `+C`<sub>h</sub>. The poll returns without a step while `002EA6A0(actor)` is 0; it waits for the actor to
be idle (`002E71C0`), draws the weapon (state 3: `002ECF10(actor, 1, 1)`, `002E8540(actor, 1)`, and
`002E9B40(actor)` stored at `+8`), waits again, and in state 5 calls `003DDB40(actor, 0, +Ch)` when
`+4` is set, then finishes at 7.

`003DDB40` sets or clears bit 19 of the render record's `+284`<sub>h</sub> through `002E8170`, from bit 7 of
byte `+D`<sub>h</sub> of `00263F40(actor)`, and plays a motion through `002EB3E0`: with bit 24 of its argument
set (the `setforcefight` begin always sets it) the stance motion `01EFE9D0[a & FFFFFFh]` (u32
entries, no bound check), otherwise `(actor +15h) << 20 | a | 1000h`. A negative argument skips
state 5, so it draws only.

`clearforcefight` (`0484`<sub>h</sub>, begin `00343770` → `00343290`) is `setforcefight`'s pair: it calls
`002E9B40`, `0026A770(actor, 0, 0)` and `002E5BC0(actor, 0)`, then `002ECF10(actor, d, 1)` and
`002E8540(unit, d)` with d = (`0030BFB0(unit)` ≠ 0), drawing or sheathing to match the unit's battle
state. `setforcefightmode` (`0334`<sub>h</sub>, `003444D0`) is a different verb that writes the force-fight
toggle ([force fight mode](../Engine-Core/force-fight-mode.md)).

### Battle setup grants

`btlAtelSetAbility(a, b)` (`3000`<sub>h</sub>, `00510440` → `002390B0`) rebuilds the unit's script-granted
ability set at `+E80`<sub>h</sub>: `+E80h..+E8Fh` are zeroed, then bit `31 − k` is set for each set bit `k`
of `a` and bit `63 − k` for each set bit of `b` (`04000000`<sub>h</sub> in `b` sets bit 37). Bits 64-127 stay
zero.

`btlAtelSetStatus(ref)` (`3002`<sub>h</sub>, `005103B0` → `002394C0`) reads a table of 32 two-bit values
through a reference (`002650B0`) and sets bit `i` of `+E90`<sub>h</sub> for value 3. Values 1 and 2 are
applied at once through `0030EAE0`, only when dword `[[unit + 6A0h]] & 5` is 0, and value 1 also
needs `00328370()` bit 0, a draw of the generator at `022C256C`
([random number generators](../Random-Numbers/random-number-generators.md)).

The ability list rebuild `0030FED0` reads both, only for a record with `+5` = 1: each `+E80`<sub>h</sub> bit
becomes `0030E130` (`00310047`) and each `+E90`<sub>h</sub> bit becomes `0030E360(unit, 0, i, 0)` (`003103E0`).
This covers an immediate-displacement search for `+E80`<sub>h</sub>, `+E88`<sub>h</sub> and `+E90`<sub>h</sub>; the other hits are
the reset `00236A60` and functions on other objects.

The rebuild also runs from the equipment setters `0031A410`, `0031A510` and `0031A630` and the licence setter
`00323910` ([equipment](../Items-Equipment-Shops-And-Licenses/equipment.md)), and from the level growth `0030C470`
and `0030C650` ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)).

### Verbs that do not touch battle decisions

`battlemotionplay` (`0450`<sub>h</sub>, `0050E980`) pops two values and does nothing. `setfightmode`
(`01A7`<sub>h</sub>, `0034CB60`) is `002E8540(actor, v)`, the drawn-weapon state, and `ignorebattlemovectrl`
(`04E7`<sub>h</sub>, `00341DB0`) is `002EBC40(actor, v)`.

`suspendbattle` (`0069`<sub>h</sub>) and `suspendbattle_resetmotion` (`0586`<sub>h</sub>) share `00356970`, which runs
the pause `0035AB20` and the motion reset `0035A680`. The pause sets `02089340` bits `20`<sub>h</sub>
(`00238B70(1)`, which also sends motion `30B`<sub>h</sub> through `002E7C10` to every flagged entry of
`[0208E688]`) and `80`<sub>h</sub> (`00238AE0(1)`), then calls `0035A590`. The motion reset calls `002EB430`
on every actor of the scene range that has a battle unit, when scene byte `+10`<sub>h</sub> bit 0 is set.
`suspendbattle_no_resetmotion` (`0587`<sub>h</sub>, `00347460` → `0035AB20`) is the pause alone.

## Layouts

```
battle unit   +0 u32 flags (bit 14 issued command, bit 22 no attacker registration, bit 23 stance), +4 u32 (bits 9-10 emergency, bit 16 engaged),
              +0x6B0 bit 1 issued without target, +0x6E0 / +0x6E8 / +0x6F0 / +0x6F8 order sets, +0x700..+0x717 action block:
              +0x708 action context, +0x710 target focus, +0x714 u16 action id; +0x718..+0x72F copy of the block,
              +0x748 transient-set target, +0x750 / +0x754 shared target, +0xBA0 u16 issued command id, +0xBA4 bit 15 set on issue,
              +0xBB8 issued target, +0xDCC u32, +0xE80 u64[2] script abilities, +0xE90 u32 script statuses,
              +0xEA4 attackers mask, +0xEA8 u8 attacker count, +0xEA9 u8 unit index
order sets    01EEC3C0 party default, 01EEC410 non-party default, 01EEC2D0 issued transient, 01EEC2B0 engage auto-attack,
              01EEC320 / 01EEC370 status cases, 01EEC298 final fallback
stance table  01EFE9D0: u32 motion ids 0x1001, 0x1001, 0x101A, 0x1018, 0x1019, 0x1009, 0x100A, 0x403D, 0x101C, 0x301B, …
render record [022C6F28] + idx × 0x740: +0x40B bits 0-1 drawn state, +0x284 bit 19 set by draw and sheathe, +0x294 motion flags
```

## Shipped data

| Fact | Value |
|---|---|
| commit callers | 5 sites in 4 functions |
| issued-command callers | 3 sites in 2 functions; the verb `resetJobs` reaches one with the fixed id `113`<sub>h</sub> |
| `0030F2D0` callers | the three reset verbs only |
| uses in the US scripts | `setforcefight` 2,107 in 343 files; `clearforcefight` 2,120 in 346 files; `setemergency` 104; `setemergency_one` 74; `setforcefightmode` 177 |
| `setbattlethinkstatus_freetarget_group` uses | 1,514, all with group −1: 1,498 × (−1, 0) and 16 × (−1, 1) |
| `btlAtelSetAbility` / `btlAtelSetStatus` uses | 6,746 each |

## Operations

Per emergency verb: one flag write per party-slot unit and one draw request. Per reset verb: one
order-set install and one sheathe per unit. Per `setforcefight`: one poll per frame through
states 0 to 7.

## State

The unit's flag dwords, order-set pointers, action block and its copy, the issued-command fields,
the two script grant words; the render record's drawn state; `022C1F48` and `022C1F40`.

## Modding notes

- A script cannot make a character use a chosen command; it can engage, disengage, draw, sheathe,
  stop thinking or change the stance. The one script-reachable issue is `resetJobs` on the recorded
  character, which issues command `113`<sub>h</sub> to the party-slot-3 unit.
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
