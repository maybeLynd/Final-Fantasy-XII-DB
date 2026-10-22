---
title: "Boss fights: enemy groups, the group-defeated signal, the battle freeze, the exit lock and the boss gauge"
kind: "system"
category: "Battle actions"
addresses: "0x00239710, 0x00306E60, 0x00306F00, 0x00307030, 0x00307090, 0x00238B70, 0x00238AE0, 0x00264830"
---

## What the player sees

A boss or story fight is not marked by one setting. The area's script builds it from separate pieces:

- **The boss is an enemy in a numbered group.** Ordinary enemies are in group 0. When every member of
  a group has been defeated, the game locks the controls, freezes the battle and, for groups set up
  for it, records the group number where the area's script can read it.
- **The battle freeze** is also switched on and off by the script commands `suspendbattle` and
  `resumebattle`, which far more scripts use than have boss fights, so it is not a boss marker on its
  own.
- **Exits.** A script can lock the zone exits; the exit triggers then do nothing.
- **The boss gauge** is opened by the script. Almost every script that opens it also puts an enemy in
  a group.

## How it works

### Joining a group

The script command `btlAtelSetEventFlagGroup(group, mode)` reaches `0x00239710(actor, mode, group)`
through its handler `0x0050F8C0`. It stores the group number in the unit's byte `+0xE98`, sets bit 0 of
`+0xE99` for mode 1 and bit 1 for mode 2 (clearing them otherwise), and calls
`0x00306E60(unit, 1)` (`0x0023973A`-`0x00239770`).

`0x00306E60(unit, add)` works only for an enemy-side unit (stats `+0x05` = 1) with a group. It takes the
unit's lane (0-31) from `0x002360D0(unit+0x40, 0x00263D30(actor))`, sets (`add` = 1) or clears (`add` = 0) that bit
in the group's member mask, and clears it in the group's defeated mask. The group's entry is
`0x02EC13C0 + (group - 1) * 0x18`: the member mask at `+0x00`, the defeated mask at `+0x08` and a pending
flag at `+0x10` (bit 0).

### A member is defeated

`0x00306F00(unit)` sets the unit's lane in the defeated mask. When the defeated mask covers the member
mask, the group is complete, and it:

1. calls `0x00307140(1)`: ten `0x002E1C20(0xC)` calls, `0x00359200(1, 2)`, `0x00359330(2, 1, 1)` and
   `0x0026BD20(2, 0)`;
2. calls `0x00238B70(1)` and `0x00238AE0(1)`, the battle freeze (below);
3. with bit 0 of `+0xE99` (mode 1), clears unit bit 47, sets the group's pending flag and posts event
   `0x2005`; otherwise sets unit bit 47 and posts event `0x2008`.

### The group-defeated signal

The frame orchestrator calls `0x00307030` (`0x00234717`). When `0x00233D20()` allows it, every pending group
has its flag cleared and its number passed to `0x0026ADC0(3, group)`, which stores it in word 3 of the
array that actor manager 0 points to at `+0x58` (`0x02098E68`), when that manager is active (bit 0 of
`0x02098E20`). `0x00307090` clears all 64 entries;
it is called by the area initialisation (`0x0023442D`).

### Removing enemies

The script command `bosskillall` reaches `0x00234880`, which removes (`0x00300E40(unit, 0)`) every
enemy-side unit with a group (`+0xE98` not 0). `zakokillall` reaches `0x00237690` (through the stub `0x00473B10`), which removes every
enemy-side unit in group 0.

### The battle freeze

`0x00238B70(on)` sets or clears bit 5 (`0x20`) of the battle flags `0x02089340` and sends message `0x30B`
(`0x002E7C10`) to every unit with bit 4 of its first byte. `0x00238AE0(on)` sets or clears bit 7 (`0x80`).
The script commands `suspendbattle` (`0x0035AB20`: both on, then `0x0035A590`) and `resumebattle`
(`0x0035A6F0`: `0x00473830(0, 1)`, both off, `0x00267D40(2)`) use the same pair. While bit 5 is set, a running
action is cancelled with reason 2 ([Target selection](target-selection.md)) and idle units are not
sent back to choose actions ([Action commit](action-commit.md)).

### The exit lock

`lockmapjump` (`0x0034AD70`) sets bit 2 of byte `+0x200` of the running actor manager (`0x002640C0`);
`unlockmapjump` (`0x0034B1C0`) clears it. `0x00264830` returns 1 when any of actor managers 0-2 (`0x288` apart
from `0x02098E10`) has bit 0 of `+0x10` and that bit. The script command `sysucoff` polls it
(`0x00346A60`, setting its result to 1 at `0x00346A8E`), and an exit trigger that gets 1 from `sysucoff`
does not jump.

## Shipped data

From the decompiled shipped scripts (all 1,114 `us` scripts):

| Fact | Count |
|---|---:|
| `btlAtelSetEventFlagGroup(0, 0)` calls | 6,206 |
| calls with group 1 (modes 0, 1, 2) | 438, 74, 13 |
| calls with groups 2-5 (in 5 scripts) | 15 |
| scripts that put an enemy in a group 1-5 | 235 |
| scripts that call `bossgaugeopen` | 162 |
| of those, also putting an enemy in a group 1-5 | 160 (not `lus_a02`, `lus_b01`) |
| scripts that call `suspendbattle` / `resumebattle` | 532 / 470 |
| scripts that call `lockmapjump` | 68 |
| of those, also putting an enemy in a group 1-5 | 19 |
| `mapjump(12)` exit entries | 1,525 |
| of those, calling `sysucoff` in their opening lines | 1,462 |

## Related

- [Quickenings and summons](quickenings-and-summons.md) - another script-visible battle state.
- [Target selection](target-selection.md) - the cancel reasons, including the battle freeze.
- [Action commit](action-commit.md) - the idle-unit queue the freeze stops.
- [Group completion and respawn](../Enemy-Spawning/enemy-respawning.md)
  - the spawn side of the groups.
- [The R2 modal toggle](../Controls-And-Input/escape.md) - the FLEEING mode, which
  boss fights do not switch off.
