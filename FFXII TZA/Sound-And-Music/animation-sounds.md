---
title: "Animation sounds: footsteps, swings and voices authored into animations, the twelve sound types, which variation plays and where it is heard from"
kind: "system"
category: "Sound and music"
addresses: "00520C50, 00520D00, 0046CC70, 0046C250, 0046C6E0, 0046C8F0, 002E9D90, 003A6E60"
---

## What the player sees

- Footsteps change with the ground underfoot.
- A weapon swing sounds like the weapon, and characters grunt, cry out when hurt and mutter while idle.
- A cry is sometimes skipped, and the same cry is never picked twice running.
- An animation that is cut short never plays its later sounds.

## How it works

### The two commands

Animations carry the commands; the character's sound emitter, the render record's sub-object at `+5F0`<sub>h</sub>, plays them
through `0046CC70(emitter, mode, type, volume)`:

| Command | Handler | Passes |
|---|---|---|
| `05`<sub>h</sub> | `00520C50`, through `0046CBA0` | word `+2` as `mode << 12 \| type`, volume 0 for full |
| `29`<sub>h</sub> | `00520D00` | mode 0, type 1, volume the signed word `+2` out of 128 |

### The sound types

The animation containers (`.ca` under `obj_finish`) hold 23,783 `05`<sub>h</sub> and 47,472 `29`<sub>h</sub> commands. Only modes 0 and 4
are authored, and mode-0 types are 1-12:

| Type | Commands | Authored in blocks | Heard from |
|---:|---:|---|---|
| 1 | 47,472 | `ready`, `attack`, `turn`, `field_attack` | bone `101`<sub>h</sub> |
| 2 | 2,092 | `attack` | the weapon attachment `200`<sub>h</sub> |
| 3 | 1,931 | `field_attack`, `attack` | the weapon attachment `200`<sub>h</sub> |
| 4 | 608 | `attack` | bone `0C`<sub>h</sub> |
| 5 | 3,437 | `damage`, `knockback_s`, `poach`, `dead` | bone `0C`<sub>h</sub> |
| 6 | 2,405 | `knockback_l`, `dead`, `poach` | bone `0C`<sub>h</sub> |
| 7 | 1,542 | `ready`, `c_turbo` | bone `0C`<sub>h</sub> |
| 8 | 1,914 | `knockback_l`, `dead` | bone `101`<sub>h</sub> |
| 9 | 3,530 | `ready`, `attack`, `magic`, `ability` | the body, `100`<sub>h</sub> |
| 10 | 4,330 | `ready`, `attack`, `turn`, `ev_walk` | the body |
| 11, 12 | 743, 699 | `active`, `deact` | the body |
| mode 4, 101-104 | 552 | monster blocks | the body |

The `29`<sub>h</sub> volumes are 128 on 45,968 commands, 64 on 748, 255 on 386 and 32 on 370. Type 1 is the footstep. The
attachment and bone `0C`<sub>h</sub> fall back to `100`<sub>h</sub> when missing.

### Which variation

`0046C250(emitter, type)` sets the bank group, emitter byte `+5`, and the variant, byte `+6`. Each draw is
`003A6E60(n)`, the presentation random stream, and the last pick of each family is kept in a nibble of bytes `+1`-`+3`,
so a repeat is stepped down by one, wrapping:

| Type | Group | Variant |
|---:|---:|---|
| 1 | `1` | 0; the footstep varies by ground, below |
| 2 | `0` | by the kind of the `200`<sub>h</sub> attachment: kind 1 picks 0-2, 2 picks 3-5, 3 picks 6-7, 4 picks 8-9, 5 is `0C`<sub>h</sub>, 6 is `0D`<sub>h</sub>; no attachment, no sound |
| 3 | `0` | `0A`<sub>h</sub> |
| 4 | `2` | by the `400`<sub>h</sub> attachment's kind: kind 1 draws 0-3, 0 is silence, else 0-2; kind 2 draws 0-4, 0 is silence, else 6-7; another kind is silence |
| 5 | `2` | draws 0-3, 0 is silence, else 3-5 |
| 6 | `2` | 8 or 9 |
| 7 | `2` | a countdown in byte `+4`; at zero it reloads with 3-11 and draws 0-3, 0 is silence, else `0A`<sub>h</sub>-`0C`<sub>h</sub> |
| 8, 9, 10 | `2` | `15`<sub>h</sub>, `17`<sub>h</sub>, `19`<sub>h</sub> |
| 11, 12 | `0` | `0E`<sub>h</sub>, `0F`<sub>h</sub> |

Types 4 and 5 are also silent when `003326C0` finds nothing for emitter word `+8` (`0046C433`, `0046C50F`).

### Where it is heard from

`0046C6E0` and `0046C8F0` find the point by type from one table, and the source's radius is half the character's
parameter `9001D1E`<sub>h</sub>. `0046C6E0` runs first and can refuse the sound. `0046C8F0` builds the spatial source, scales
its volume byte by `volume / 128`, capped at `7F`<sub>h</sub>, plays nothing when that is 0 and calls the play routine
([Spatial sound](spatial-sound.md)).

### Which sample

`002E9D90(actor record, group, variant, footstep flag)` finds the sample in the actor's sound set at `+C0`<sub>h</sub>:

- Group 0 reads its block from the binding in the presentation record's first attach slot (`[actor + C0h] + 30h`,
  `002E9F50`); only the weapon (`w`) rows of `charseinfo` author that block. Groups 1 and 2 read the set itself.
- For group 1, the footstep, the index is the movement body's ground type `+8A`<sub>h</sub> (`002E9F29`) looked up in
  `soundfoottable.bin`, with the table's 32 added when the flag and the field's environment variant are both set.
- For group 2 with a variant below 10, when the actor's voice-pool entry (`+20`<sub>h</sub> of the actor it resolves to through
  `00263F40` and `00263F10`) has state 3, its bank loaded (`0036ECA0`), the sound comes straight from that bank
  (`0036EC50`, `002E9F81`): the character's own voice.
- The footstep flag is set for types 1, 8, 9 and 10.

### The play routine

`0046CC70` refuses unless the emitter is enabled, byte `+0` = 1, and its owner is live. Then by mode:

| Mode | Does |
|---:|---|
| `0` | the chain above. Footsteps are dropped while a record test with `1A`<sub>h</sub> holds; types 11 and 12 play only for the party's focus character; type 7 not while the last voice still plays. A new voice of types 4-7 stops the playing one, kept at `+18`<sub>h</sub> with its type at `+1C`<sub>h</sub> |
| `1`, `2`, `3` | a direct sound id from one of three bank getters, centred, at `volume * 64 / 128`; not authored |
| `4` | an explicit sound number at the character, bit 31 added below `100`<sub>h</sub> |
| `5` | with type 1, stores `C00`<sub>h</sub> in emitter word `+5` |

`003A0E50(id, position, record)` makes the sound. An id with bit 30 set is a battle-voice line, bank `id >> 8 & FFh`
and line `id & FFh`, played at the point in the Config voice language (`002DF460`); any other id plays from a block
bank at the point (`002DF280`), and -1 plays nothing. The same call serves `0046C8F0`, `00332C40` and `003B99D0`.
`003A0E80(kind, handle)` stops the previous voice of types 4-7 while it still plays (`0046CE04`-`0046CE1F`), with the
kind from emitter byte `+07`<sub>h</sub>: kind 0 through the battle-voice stop (`001DC330`), kind 1 through `002DF0F0`.

The battle routine `00307300` plays mode 4 at a battle record's actor through `00329F70` (`00307727`), which passes
the record's `+08`<sub>h</sub> to `0046CBB0`. That finds the actor's render record (`740`<sub>h</sub> bytes each from `[022C6F28]`) and
calls `0046CC70` on its emitter at `+5F0`<sub>h</sub>.

## Modding notes

- A sound is part of the animation: to add or move one, edit the `05`<sub>h</sub> or `29`<sub>h</sub> command in the animation block.
- The swing sample follows the weapon attachment's kind; the footstep sample follows the ground type and
  `soundfoottable.bin`.
- Voices interrupt voices on one character; footsteps and swings overlap.
- A `29`<sub>h</sub> volume that scales to 0 plays nothing.

## Related

- [Sound effects](sound-effects.md) - the play call.
- [Sound variations](sound-variations.md) - the driver's own kinds, which shipped sounds do not use.
- [Spatial sound](spatial-sound.md) - the source the emitter builds.
