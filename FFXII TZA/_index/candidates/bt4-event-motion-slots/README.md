# BT-4: what the four speed-rule values mean on screen (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (BT-4):** "What the subtypes mean": `0x0D` forces speed to zero, `0x10` arms the coast-down latch, and `0x35`/`0x36` apply a 0.9 decay. The 2026-09-15 narrowing showed they are the index half of the render record's current event (`+0xCC`). Their on-screen meaning was open because no name table for the indices had been found.

**Answer: each index is the slot of the motion it plays.** A render event's low 12 bits select a slot in the character's motion container (`.ca`, an `@FRP` of version 1). That slot holds the `@FMC` motion block the event plays, and every shipped container names its blocks. So the name table is the data, and it is the same in all 1,195 version-1 containers:

| index | motion | posted by | the speed rule it gets |
|---|---|---|---|
| `0x0D` | **`revive`** | a unit whose three terminal statuses have all cleared (`00301140` at `0030127A`); and the target that the ability **Spawn** (action `0x1C7`) moves to its caster (`00307300` at `00307A68`) | speed forced to 0: the unit stands still while it gets up or appears |
| `0x10` | **`c_turbo`** | the type-`0x1A` mount, in place of the ordinary `0x2001` (`ready`), while turbo is on (`00305080` at `003050B5`, `00303F00` at `0030400F`) | the only index that can arm the coast-down latch: a mount stopped out of a turbo run glides to a halt (×0.83 per call to 0.05) |
| `0x35` | **`active`** | `00426130` as event `0x4035`, reached with mode 1 from `BattleUnit_EnterPartyCombatStance` (`00313415`, flag 1) | ×0.9 per call while the weapon is drawn |
| `0x36` | **`deact`** | the same, as `0x4036`, from `BattleUnit_ExitPartyCombatStance` (`00313493`, flag 0) | ×0.9 per call while the weapon is put away |

For its priority comparison, the selection policy maps every kind-3 event to `0x2036`. It maps every kind-4 event to `0x2035`, or to `0x2036` when the index is `0x36`. So the stance pair `0x4035` / `0x4036` is compared with `active` / `deact`'s own priority bytes.

## The mechanism, instruction by instruction (static, the authorised image)

1. **The event is stored in two places.** `00424D80(render, …, event)` takes the event in `r9d` (`00424DA4 mov esi, r9d`) and stores it both into the presentation entry's word `+0x31C` (`00424FA4`) and into the render record's `+0xCC` (`00424FAB`). `+0xCC` is the word the speed rules read.
2. **The entry resolves the event to a child.** `PresentationEntry_RebuildDerivedResourcePointers` `0041CA70` passes the entry's bank word `+0x31A` and `+0x31C & 0xFFF` to `004090D0`, then stores the child it returns at entry `+0x368` (`0041CAB2`–`0041CAD2`). The authored-command page already identifies `+0x368` as the entry's `@FMC` block.
3. **The index arithmetic.** `004090D0`, on a version-1 `@FRP`, computes index = `a × [+0x30] + b` when `a < [+0x34]`, else `b`. The child is then at `[frp + index×4 + 0x40]`, relative to `+0x40` (`004090F2`–`00409107`). Every shipped event container carries `[+0x30] = 0x50`: 80 event slots per bank, so the event index is the slot itself. The `@FMN` / `@FMW` motion data follow from slot `0x50`.

## The data (the shipped `.ca` corpus)

Control C1: all **1,195** version-1 `.ca` files under `ps2data/obj_finish/in` were read.
- 1,150 have one bank and 45 have three.
- Every non-empty slot `0x00`–`0x4F` holds an `@FMC` block.
- Every slot has exactly **one** name across all files, once the relaxed set's `rlx_` prefix is folded (`rlx_revive` / `revive`).

`event-slot-names.tsv` is the whole table: 51 slots, from `0x00` `start_pose` to `0x4A` `field_attack`. Examples:

| slots | names |
|---|---|
| `0x01`–`0x08` | ready, warp_in, warp_out, turn, damage, knockback_s, knockback_l, dead |
| `0x09`–`0x0E` | magic_ready, magic, item, stn, revive, poach |
| `0x10` | c_turbo |
| `0x1A`–`0x24` | the event talk / emote motions |
| `0x30`–`0x3D` | throw, ability_ready, ability, steal, active, deact, avoid, guard/parry ×4, attack |
| `0x47`–`0x4A` | call, summon_attack, summon_damageidle, field_attack |

**Positive control: the other posters name what posts them.**
- `0x2008` `dead` is among the events the spawn-group death record posts (`00306F00`).
- `0x200C` `stn` and `0x200E` `poach` are the two events the terminal-status switch posts for statuses 1 and 31 (field-record page).
- `0x2033` `steal` is category 5's third event in `BattleAction_SelectPhasePresentationEvent`'s table `01EEC1F0`.
- `0x203D` `attack` is category 0's; `0x200B` `item` is category 2's; `0x2009` / `0x200A` `magic_ready` / `magic` are category 1's.

**Sensitivity (C3):** the same census keyed one slot off matches none of the twelve checked names.

## Side finding: the reader of the action row's `+0x30`

`BattleAction_SelectPhasePresentationEvent` `0030A370` returns the row's dword `+0x30` as the action's presentation event in phases 9–11:
- when it is non-zero (`0030A46A`);
- and for action ids `0xD0`–`0xE1` in world state 5 or 6 (`0030A457`).

The value is above the priority table and is kind 0. It is the number of a per-character, per-action motion pack, a version-0 `.ca` named `c<char>_<set>_<number>.ca`. For example, `c1004` ships `c1004_10_3000.ca` to `_3002.ca`, and 3000–3017 are the page's eighteen Quickenings. This supplies the reader the action-row page recorded as not found; the page pointer is applied after UQ-107's publish (see `consumer-check.md`).

## Limits

- **Static only.** The slot a live event plays is not observed. The chain above is read from the image and the names from the data.
- **The bank word `+0x31A`** (0 for single-bank containers) is not traced for the 45 three-bank files.
- **Script verbs can post these indices too.** Examples: `puppetmotionplay` `0x041F` passes a script operand, and the party standard-motion verbs post kind-1 indices. So an authored script can play `revive` or `active` directly, and it gets the same speed rule. The engine posters listed above are the native ones.
- **`c_turbo` is present in every battle set** (576 files), so it is not specific to one species' container. That it is played on the mount follows from the poster (`[+0x698]+4 == 0x1A`), not from the file set.

## Files

- `bt4_event_slots.py [CA_ROOT]`: the control. It runs 5 image checks, plus 3 corpus checks when given the path; FAILS 0 both ways.
- `event-slot-names.tsv`: written by the control's corpus run.
- `consumer-check.md`.
