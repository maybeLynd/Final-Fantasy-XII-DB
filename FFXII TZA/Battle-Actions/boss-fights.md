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
through its handler `0x0050F8C0`. It stores the group number in the unit's byte `+0xE98`, sets bit `0x1` of
`+0xE99` for mode 1 and bit `0x2` for mode 2 (clearing them otherwise), and calls
`0x00306E60(unit, 1)` (`0x0023973A`-`0x00239770`). It returns -1 when the actor has no battle unit (`0x0031B760`,
`0x0023972C`) and 0 otherwise (`0x0023977A`).

`0x00306E60(unit, add)` works only for a non-null enemy-side unit (stats `+0x05` = 1) with a group. It takes the
unit's slot from `0x002360D0(unit+0x40, 0x00263D30(actor))`: the slot byte that the actor's lane maps to, any value
but `0xFF` (`0x002360EF`), and a negative result returns (`0x00306EB0`). It sets (`add` = 1) or clears (`add` = 0)
that slot's bit in the group's member mask, and clears it in the group's defeated mask.

The bit is `1 << (slot & 31)` shifted in 32 bits and sign-extended (`0x00306ECE`, `0x00306ED4`, `0x00306EE7`), so
slots 32 and above share the bit of `slot & 31` and slot 31 covers the bits under mask `0xFFFFFFFF80000000`.
The group's entry is
`0x02EC13C0 + (group - 1) * 0x18`: the member mask at `+0x00`, the defeated mask at `+0x08` and a pending
flag at `+0x10` (bit `0x1`). The index `group - 1` has no range test against the 64 entries (`0x00306EB2`-`0x00306EC3`).

### A member is defeated

`0x00306F00(unit)` sets the unit's slot bit in the defeated mask (`0x00306F78`), past the same gates and slot
resolution as `0x00306E60`: a null unit, a null stats record or one whose byte `+5` is not 1, a group byte of 0
or a negative slot returns 0 (`0x00306F09`-`0x00306F55`). When the defeated mask covers the member
mask, the group is complete, and it returns 1 after the steps below (`0x00306FF2`, `0x0030701C`); otherwise it
returns 0 (`0x00306F88`). On completion it:

1. calls `0x00307140(1)`: ten `0x002E1C20(0xC, n)` calls, which set the bit values `0x1`, `0x8`, `0x10`, `0x20`,
   `0x40`, `0x80`, `0x100`, `0x800`, `0x1000` and `0x100000` (mask `0x1019F9`) of row 12 at `0x0215F1F0`
   (`0x00307160`-`0x003071BE`), then `0x00359200(1, 2)`, `0x00359330(2, 1, 1)` and
   `0x0026BD20(2, 0)`;
2. calls `0x00238B70(1)` and `0x00238AE0(1)`, the battle freeze (below);
3. with bit `0x1` of `+0xE99` (mode 1), clears unit bit `0x800000000000`, sets the group's pending flag and posts event
   `0x2005`; otherwise sets unit bit `0x800000000000` and posts event `0x2008`.

### The group-defeated signal

The frame orchestrator calls `0x00307030` (`0x00234717`). When `0x00233D20()` allows it, every pending group
has its flag cleared and its number passed to `0x0026ADC0(3, group)`, which stores it in word 3 of the
array that actor manager 0 points to at `+0x58` (`0x02098E68`), when that manager is active (bit `0x1` of
`0x02098E20`). `0x00307090` zeroes both masks of all 64 entries and clears their pending flag bit `0x1`
(`and byte ptr [...], 0xFE`, `0x003070A0`-`0x003070CB`), leaving the flag byte's other bits;
it is called by the area initialisation (`0x0023442D`).

### Removing enemies

The script command `bosskillall` reaches `0x00234880`, which removes (`0x00300E40(unit, 0)`) every
enemy-side unit with a group (`+0xE98` not 0). `zakokillall` reaches `0x00237690` (through the stub `0x00473B10`), which removes every
enemy-side unit in group 0.

### The battle freeze

`0x00238B70(on)` sets or clears bit `0x20` of the battle flags `0x02089340` and sends message `0x30B`
(`0x002E7C10`) to every unit with bit `0x10` of its first byte. `0x00238AE0(on)` sets or clears bit `0x80`.
The script commands `suspendbattle` (`0x0035AB20`: both on, then `0x0035A590`) and `resumebattle`
(`0x0035A6F0`: `0x00473830(0, 1)`, both off, `0x00267D40(2)`) use the same pair. While bit `0x20` is set, a running
action is cancelled with reason 2 ([Target selection](target-selection.md)) and idle units are not
sent back to choose actions ([Action commit](action-commit.md)).

### The exit lock

`lockmapjump` (`0x0034AD70`) sets bit `0x4` of byte `+0x200` of the running actor manager (`0x002640C0`);
`unlockmapjump` (`0x0034B1C0`) clears it. `0x00264830` returns 1 when any of actor managers 0-2 (`0x288` apart
from `0x02098E10`) has bit `0x1` of `+0x10` and that bit. The script command `sysucoff` polls it
(`0x00346A60`, setting its result to 1 at `0x00346A8E`), and an exit trigger that gets 1 from `sysucoff`
does not jump.

## Shipped data

In the 1,114 `us` scripts:

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
| of those, calling `sysucoff` and branching on its result | 1,525 |
| of those, calling `sysucoff` before any other command | 1,457 |

## Related

- [Quickenings and summons](quickenings-and-summons.md) - another script-visible battle state.
- [Target selection](target-selection.md) - the cancel reasons, including the battle freeze.
- [Action commit](action-commit.md) - the idle-unit queue the freeze stops.
- [Group completion and respawn](../Enemy-Spawning/enemy-respawning.md)
  - the spawn side of the groups.
- [The R2 modal toggle](../Controls-And-Input/escape.md) - the FLEEING mode, which
  boss fights do not switch off.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Combat AI: `0x0031B760` is called by `0x00239040`, `0x003014C0`, `0x00301AD0`, `0x003087E0`, `0x0030F130`.
- Combat AI: those functions are documented on
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [glossary](../Engine-Core/glossary.md), [area of effect](area-of-effect.md),
  [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md).
