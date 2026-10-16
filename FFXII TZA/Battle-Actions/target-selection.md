---
title: "Target selection: which targets the battle menu lists, the 24-unit range and the KO exception"
kind: "system"
category: "Battle actions"
addresses: "0031EB20, 00322A80, 003230E0, 00322490, 0046B870, 0046B690, 0046BAC0, 002FFA60, 002FFB60"
---

## What the player sees

When you choose an action, the target list holds only what that action may affect: the user itself,
the user's allies and the user's foes, each allowed or not by a flag of the action.

- **Range.** A living target is listed only when it is within 24 units, measured on the ground, of
  the character you are controlling - not of the character who will act, when you give an order to
  another party member.
- **Foes.** Enemies come from the actors loaded in the area. KO'd, stoned, X-Zoned and Invisible
  enemies are not listed.
- **KO'd and stoned allies.** An action that may target KO'd units (Raise, Arise, Phoenix Down,
  Revive) lists every KO'd ally from anywhere in the area, with no range limit; likewise stoned allies
  for an action that may target Stone (Stona, Gold Needle). For any other action, a KO'd, stoned or X-Zoned ally is listed but greyed
  out.
- Once the action is chosen, the character walks toward the target; the distance is not tested
  again. The action is called off when its target can no longer be affected - for example the
  target is KO'd and the action cannot target KO'd units - or for the other reasons below.

## How it works

### The list builder

`0031EB20` (4,182 bytes) fills a list block: list code at `+0x00`, the acting
member's focus handle at `+0x08`, the action id at `+0x1C`, the entry count at `+0x40`, the default
entry at `+0x44`, and 8-byte entries from `+0x50` (value at `+0`, flag word at `+4`). It returns the
count, or -1 for a code it does not handle or an invalid action id, -2 when the acting member does not resolve, has no stats
record or is KO, Stone or X-Zone (status bits 0, 1, 31, unless `00377C20()` is non-zero), and -4 when
`002FFCF0(action, unit)` refuses the action. The target codes:

| Code | Candidates | Filter per candidate |
|---|---|---|
| `0xC`, `0xD`, `0xE`, `0x10` | every battle unit slot whose unit has bit 4 of its first byte | `00322A80` |
| `0xF` | member-map positions 4-8 (`00322C50(0x17, i)`), stats record `[02EBF190] + 8 + b * 0x1C8` for the byte `b` at `[02EBF190] + 0x5A7E + i*2` when `b < 0x28` | `00322A80` |
| `0x1A` | the list `0046B4C0` builds for actor managers 0-2 | none further |
| `0x1B` | the list `0046B870` builds for actor managers 0-2 | `003230E0(user, stats, action, 1, 1)` |
| `0x1C` | the list `0046B690` builds for actor managers 0-2 | `003230E0(user, stats, action, 1, 1)` |
| `0x12`-`0x15` | living units (no status bit 0, 1 or 31 unless `00377C20()`) with stats byte `+0x05` = 0 for `0x14`/`0x15`, non-zero for `0x12`/`0x13`; `0x13` and `0x15` also need `00322360(unit)` | - |

For codes `0xC`-`0x10`, the slot lists pass `allowAlly = (code != 0x10)`, `allowFoe = (code` not
`0xD`, `0xE` or `0xF)` and `frustum = (code == 0xE)` to `00322A80`. Before that, the builder
switches to code `0x1B`, runs itself and restores the code, when the acting member is on the party
side (stats `+0x05` = 0) and `allowFoe` is true, or on the enemy side (`+0x05` = 1) and the code is not
`0x10`. So a party member's foe lists (`0xC`, `0x10`) are the actor-manager list `0x1B`, and its ally
lists (`0xD`, `0xE`, `0xF`) are slot walks.

### Slot filter

`00322A80(user, candidateStats, action, frustum, allowAlly, allowFoe)` (456 bytes)
returns -1 to leave the candidate out, 0 to list it greyed, and 1-4 to list it:

1. If the candidate belongs to a battle unit whose actor class nibble (`00263C20`) is 3 or 5, it
   returns -1 (`00322B8B`-`00322B9C`).
2. `003230E0` must pass, else -1 (`00322B43`-`00322B4A`).
3. If the candidate has status bit 0, 1 or 31 and `00377C20()` is 0: it goes to step 5 when the
   action row's word `+0x2C` has bit 6 (`0x40`) and the candidate has bit 0 (KO), or bit 7 (`0x80`)
   and the candidate has bit 1 (Stone); otherwise it returns 0 (`00322B4C`-`00322B86`).
4. A living candidate that is a battle unit must pass `00322490` (else -1, `00322BAF`); with
   `frustum` set it must also pass `00322360` and `00322630` must return 0 (`00322BB8`-`00322BD3`).
5. The result: with flag word `+0x0C` bit 6, 2 for the user itself and 1 for others; with bit 5,
   `0031C500(user, candidate, action)` non-zero gives 3 for others and 2 for the user, zero gives 4 for
   the user and 1 for others; otherwise 1 (`00322BD5`-`00322C26`).

The builder sets entry flag bit 1 (greyed) for a 0, and remembers a 2 (the last one), a 3 (the
first, if no 2) or a 4 (as the default entry `+0x44`); a remembered 2 or 3 gets entry flag bit 0 and
the default entry becomes -2. The entry value is the unit's id `+0x08` (slot walk) or the stats byte
`+0x04` (code `0xF`).

### Ally, foe, self

`003230E0(user, candidateStats, action, allowAlly, allowFoe)` (262 bytes) treats
the candidate as on the user's side when no battle unit owns that stats record, or when
`0030BB10(user, unit, 0)` returns 0 (relationship class 1; see [Area of effect](area-of-effect.md)).
It passes when `allowAlly` and flag bit 2 and same side, or `allowFoe` and flag bit 3 and not same
side, or `allowAlly` and flag bit 0 and the candidate is the user's own stats record
(`00323195`-`003231CE`). It passes 0 as the flags to `0030BB10`, so Confuse on the acting member swaps
which side counts as its own.

### The 24-unit test

`00322490(actorObject)` (203 bytes) returns 1 only when bit 4 of `02089340` is
set, the controlled member's handle (`003590D0`) resolves (`003588B0`), the candidate's battle unit
(`00263E30`), if it has one with bit 4 of its first byte, passes `002FFED0(unit, 0, 3)` (an empty
`002FFF50` mask in mode 3 - which includes the Invisible bit for enemy-side units), and the squared
XZ distance between the two actors' world positions (`00265020`) is at most 576.0 (`00D1081C`, 24
squared; `comiss`/`setbe` at `00322535`).

### Actor-manager lists

`0046B870` (code `0x1B`) and `0046B690` (code `0x1C`) walk the records of actor managers 0-2
(`00263FF0(i)` with bit 0 of `+0x10`; records `+0x1DE` to `+0x1DE + +0x1D6`). A record is considered
when all of these hold:

- `002647B0` returns 0 (byte `+0x12` above 3), and byte `+0x18` is not 1;
- byte `+0x0E` has bits 6 and 7, and its class nibble (`+0x0E & 0xF`) is neither 4 nor 6;
- `00263BE0` returns 0 or 2 (2 for nibble 3, 0 for nibbles 1, 2 and 7);
- `002E9FE0` and `002EA6A0` return non-zero.

| List | Keeps | Marks the others in record `+0x0A` |
|---|---|---|
| `0x1B` (`0046B870`) | `00263BE0` = 0 | bit 3 |
| `0x1C` (`0046B690`) | `00263BE0` = 2 | bit 4 |

A kept record is listed only when `00322490` passes (otherwise `+0x0A` bit 2). Both also set record
`+0x0A` bit 0 when `00317D80` returns 0.

`0046B4C0` (code `0x1A`) calls `0046BAC0(i, 1)` for managers 0-2, which applies the 24-unit test
through `00322480`, a jump to `00322490` (out of range: `+0x0A` bit 1). For all three codes the builder
appends every listed record (for `0x1B`/`0x1C` after `003230E0` passes) and makes the entry nearest
the controlled member the default (`0031E630`; entries whose `002647E0(id)` has bit 0 are not
considered).

### While the action runs

`002FFB60(unit)` (385 bytes) returns a cancel reason. Reason 1 is returned for action `0x414E` while
unit bit 32 is set (and that bit is cleared). The other reasons are tested only with unit bits 24 and
22 clear and either the action id above `0x21E` or the action phase `+0x6B4` below 9, in this order:

| Reason | When |
|---:|---|
| `2` | bit 5 of `02089340` is set |
| `3` | unit bit 14 is set |
| `9` | the user has status bit 0, 1, 3, 4 or 31 (`0x8000001B`) |
| `4` | (action id below `0x21F`) the target count `+0x77C` is 0 or the target `+0x710` does not resolve |
| `5` | (action id below `0x21F`) `002FFA60(action, target)` returns 0 |
| `6` | (action id below `0x21F`) `002FFCF0` refuses the action |
| `7` | bit 13 of the word at `[+0x708]+4` is clear and `0030AF30` times the action out |

`002FFA60(action, target)` returns 1 when the target has none of status bits 0, 1, 31 (or
`00377C20()` is non-zero), or when the action row's `+0x2C` has bit 6 or bit 7 (`002FFA88`-`002FFB43`).

`0030AF30` compares the counter `+0x75C` with `30 * (int)(30.0 * [01DFE0B8])` for an action id below
`0x21F`, 10 times that factor above it, and 60 times it when the word at `[+0x708]+4` is negative. On a
timeout it also performs the cancel: it zeroes the action's timers and targets, clears unit bit 14
(except for actions `0x113` and `0x95`), entry flag bit 10 of `+0x788` and bit 1 of `+0x6B0`, sets bit
21 of the unit's word `+0x04`, and calls `004697C0` and `00290540`.

None of `002FFB60`, `002FFA60` or `0030AF30` reads a position or a distance, and neither does the
availability check behind reason 6 (`002FFCF0` and its callees `0030E9C0`, `0031A7B0`, `00306480`,
`00303BD0`, which take only the stats record, the action id or the unit's cost state).

## Modding notes

- The 24-unit limit is the float at `00D1081C` (576.0, the square of the range); it applies to every
  living candidate in every list, through `00322490`.
- The KO and Stone permissions are bits 6 and 7 of the action row's word `+0x2C`; they also keep
  `002FFA60` from cancelling the action when its target is KO'd, stoned or X-Zoned. In the shipped
  `battle_pack.bin`, bit 6 is set on 10 action rows (Raise twice, Arise, Phoenix Down, Revive, Cry for
  Help, Necromancy, Divide twice, Spawn) and bit 7 on 2 (Stona, Gold Needle).
- Allies, foes and self are bits 2, 3 and 0 of the row's flag word `+0x0C`; bits 5 and 6 choose how
  the default cursor is placed.

## Related

- [Area of effect](area-of-effect.md) - the relationship class and the area gathered after the
  target is chosen.
- [Action range](action-range.md) - how close the user walks before acting.
- [The action definition row](action-definition-row.md) - flag words
  `+0x0C` and `+0x2C`.
- [Battle command availability](command-availability.md)
  - `002FFCF0` and its reason codes.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  0, 1, 3, 4, 5, 24 and 31.
