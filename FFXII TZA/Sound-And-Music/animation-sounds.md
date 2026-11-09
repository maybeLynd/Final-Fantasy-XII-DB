---
title: "Animation sounds: footsteps, swings and voices authored into animations, the twelve sound types, which variation plays and where it is heard from"
kind: "system"
category: "Sound and music"
addresses: "0x00520C50, 0x00520D00, 0x0046CC70, 0x0046C250, 0x0046C6E0, 0x0046C8F0, 0x002E9D90, 0x003A6E60"
---

## What the player sees

- Footsteps change with the ground underfoot.
- A weapon swing sounds like the weapon, and characters grunt, cry out when hurt and mutter while idle.
- A cry is sometimes skipped, and the same cry is never picked twice running.
- An animation that is cut short never plays its later sounds.

The animation files carry the sound commands, each naming a sound type. When one fires, the character's sound emitter
picks a variation, finds the sample in the character's own sound set (for a footstep, through `soundfoottable.bin` and
the ground type underfoot) and plays it from a point on the body.

## How it works

### The three commands

Animations carry the commands; the character's sound emitter, the render record's sub-object at `+0x5F0`, plays them
through `0x0046CC70(emitter, mode, type, volume)`:

| Command | Handler | Passes |
|---|---|---|
| `0x05` | `0x00520C50`, through `0x0046CBA0` | word `+2` as `mode << 12 \| type`, volume 0 for full |
| `0x29` | `0x00520D00` | mode 0, type 1, volume the signed word `+2` out of 128 |
| `0x19` | `0x00520CE0` | mode 0, type 1, volume 0 for full: the footstep with no volume word |

### Every occurrence

[`fmc-sound-occurrences-1.tsv`](fmc-sound-occurrences-1.tsv) has one row for each of the 166,242 uses of `0x05` and
`0x29`: one `@FMC` slot of one container, by one command. `container`, `path`, `package_slot`, `fmc_slot`, `name`
and `content` name the block, and `stream`, `group`, `frame`, `command`, `offset` and `operand_hex` the command, as
in the [motion tables](../Graphics/model-effects-and-motion-commands.md). `mode`, `type` and
`volume` decode the operand word as above. No sound command sits in a `0xFFFF` block.

`owners` are the models that play the block. A lane, an action motion and a model's own file name their owner; a
script package takes the models of the cues that name the entry, from [motion
playback](../Graphics/model-effects-and-motion-commands.md). `owner_status` says which, and
`reason` says what stops it.

[`fmc-sound-selections.tsv`](fmc-sound-selections.tsv) has one row for each model, mode and type used, keyed by
`selection` (`model/mode/type`). `source` gives where the sound comes from:

| `source` | Rows | Meaning |
|---|---|---|
| `own_block` | 1,765 | group 2: the `bank` from the model's `block2`, with the `variants` the type picks |
| `footstep_set` | 316 | type 1: the `bank` from `block1`, sounds picked by ground and weather |
| `attached_model_block0` | 1,498 | group 0: `block0` of the model in the first attach slot |
| `no_block_for_group` | 199 | the model has no block for the group, so `0x002E9D90` gives -1 |
| `explicit` | 5 | modes 1 and 4: the sound number in `se000` |

`playable` and `not_playable` split the variants by the block index rule of [Sound banks](sound-banks.md): a sound
is playable when its slot exists and its byte `+0x04` is set. A `footstep_set` row lists all 44 numbers
`soundfoottable.bin` names, 0 to 43, and `not_playable` holds those the bank has no playable sound for. Only one
model's block is a fixed fact: which variant plays is drawn as above.

Mode 4 (552 occurrences, numbers 101 to 104) resolves to registry slot 0, the first block to register. `0x003A13F0`
requests blocks 0, 1 and 2 in that order (`0x003A14AD`, `0x003A152C`, `0x003A15AB`), and those numbers exist only in
`se000`. Group 0 takes its block from the model in the actor's first attach slot, and type 1 picks the sound by the
ground under the actor, so those rows give the bank or the variants and not the one sound. Authored does not mean
played: `0x0046CC70` has the gates listed above.

### The sound types

The animation containers (`.ca` under `obj_finish`) hold 23,783 `0x05` and 47,472 `0x29` commands; no `.ca` under `ps2data` authors `0x19`. Only modes 0 and 4
are authored in the `.ca` files. One `.cm`, `obj_finish/in/treasure/t0006.cm`, adds mode 1 in FMC slot 8
`treasure_open`: type 68, which is `0x003A1180(68)`, `se000` sound 68 (`0x0046CFE6`-`0x0046CFE8`). Mode-0 types are 1-12:

| Type | Commands | Authored in blocks | Heard from |
|---:|---:|---|---|
| 1 | 47,472 | `ready`, `attack`, `turn`, `field_attack` | bone `0x101` |
| 2 | 2,092 | `attack` | the weapon attachment `0x200` |
| 3 | 1,931 | `field_attack`, `attack` | the weapon attachment `0x200` |
| 4 | 608 | `attack` | bone `0x0C` |
| 5 | 3,437 | `damage`, `knockback_s`, `poach`, `dead` | bone `0x0C` |
| 6 | 2,405 | `knockback_l`, `dead`, `poach` | bone `0x0C` |
| 7 | 1,542 | `ready`, `c_turbo` | bone `0x0C` |
| 8 | 1,914 | `knockback_l`, `dead` | bone `0x101` |
| 9 | 3,530 | `ready`, `attack`, `magic`, `ability` | the body, `0x100` |
| 10 | 4,330 | `ready`, `attack`, `turn`, `ev_walk` | the body |
| 11, 12 | 743, 699 | `active`, `deact` | the body |
| mode 4, 101-104 | 552 | monster blocks | the body |

The `0x29` volumes are 128 on 45,968 commands, 64 on 748, 255 on 386 and 32 on 370. Type 1 is the footstep. The
attachment and bone `0x0C` fall back to `0x100` when missing.

### Which variation

`0x0046C250(emitter, type)` sets the bank group, emitter byte `+5`, and the variant, byte `+6`. Each draw is
`0x003A6E60(n)`, the presentation random stream, and the last pick of each family is kept in a nibble of bytes `+1`-`+3`,
so a repeat is stepped down by one, wrapping:

| Type | Group | Variant |
|---:|---:|---|
| 1 | `1` | 0; the footstep varies by ground, below |
| 2 | `0` | by the kind of the `0x200` attachment: kind 1 picks 0-2, 2 picks 3-5, 3 picks 6-7, 4 picks 8-9, 5 is `0x0C`, 6 is `0x0D`; no attachment, no sound |
| 3 | `0` | `0x0A` |
| 4 | `2` | by the `0x400` attachment's kind: kind 1 draws 0-3, 0 is silence, else 0-2; kind 2 draws 0-4, 0 is silence, else 6-7; another kind is silence |
| 5 | `2` | draws 0-3, 0 is silence, else 3-5 |
| 6 | `2` | 8 or 9 |
| 7 | `2` | a countdown in byte `+4`; at zero it reloads with 3-11 and draws 0-3, 0 is silence, else `0x0A`-`0x0C` |
| 8, 9, 10 | `2` | `0x15`, `0x17`, `0x19` |
| 11, 12 | `0` | `0x0E`, `0x0F` |

Types 4 and 5 are also silent when `0x003326C0` finds nothing for emitter word `+8` (`0x0046C433`, `0x0046C50F`).

### Where it is heard from

`0x0046C6E0` and `0x0046C8F0` find the point by type from one table, and the source's radius is half the character's
parameter `0x9001D1E`. `0x0046C6E0` runs first and can refuse the sound. `0x0046C8F0` builds the spatial source, scales
its volume byte by `volume / 128`, keeps the low 8 bits of the result, plays nothing when that is 0, caps it at
`0x7F` and calls the play routine
([Spatial sound](spatial-sound.md)).

The radius is `0.5 * param`, or 0 when `0x002EDBD0` returns null for the emitter's word `+8`
(`0x0046C7E4`-`0x0046C808`, `0x0046CA06`-`0x0046CA2A`). Each reads its own copy of the twelve-entry jump table
(`0x0046C898`, `0x0046CB64`): types 1 and 8 ask `0x00421E20` for `0x101`, types 2 and 3 ask `0x00426770` for `0x200`,
types 4-7 ask for bone `0x0C`, and types 9-12 for `0x100`, which is also the fallback of `0x200` and `0x0C`
(`0x0046C76A`-`0x0046C7D3`, `0x0046C98C`-`0x0046C9F5`).

`0x0046C6E0` returns 0 when the emitter's word `+8` is -1 or names a record
whose `+0x284` is 0 (`0x0046C70C`-`0x0046C73A`), for a type outside 1-12 (`0x0046C74E`), and for a footstep (type 1)
whose volume from `0x00361CF0` is 0 (`0x0046C85F`-`0x0046C864`); otherwise it returns 1. The footstep's pan and volume
come from `0x00361CF0`, the other types' from `0x00361BF0` (`0x0046C84F`, `0x0046C81E`).

The footstep also passes the float at `0x01F004D0 + 4 * b`, with `b` the byte `+0xB5` of the character object
`0x003E56C0` returns (shipped values 25.0, 35.0, 45.0 and 55.0 for `b` 0 to 3; `0x0046C825`-`0x0046C842`,
`0x0046CAE5`-`0x0046CB0A`).

`0x0046C8F0` refuses as `0x0046C6E0` does except for the footstep volume test
(`0x0046C92B`-`0x0046C970`), and builds the source with `0x003617B0` and the `0x01F004D0` float for a footstep, with
`0x00361750` for the other types (`0x0046CB1D`, `0x0046CA4F`).

The volume byte is the source's `+0x19`: `byte * volume / 128`, truncated toward zero and kept to its low
8 bits (`0x0046CA5F`-`0x0046CA77`); a volume of 0 leaves the byte as it is (`0x0046CA72`). A zero result returns 0
(`0x0046CB4D`). Then `byte = min(byte, 0x7F)` (`0x0046CA7F`-`0x0046CA89`): a byte of 127 with a volume of 255
gives 253 and then 127, while 200 with 200 gives 312, kept as 56, which the cap leaves as it is. It then
calls `0x003A0E50` with the sound id and returns its result (`0x0046CAAE`).

### Which sample

`0x002E9D90(actor record, group, variant, footstep flag)` finds the sample in the actor's sound set at `+0xC0`:

- Group 0 reads its block from the binding in the presentation record's first attach slot (`[actor + 0xC0] + 0x30`,
  `0x002E9F50`); only the weapon (`w`) rows of `charseinfo` author that block. Groups 1 and 2 read the set itself.
- For group 1, the footstep, the index is the movement body's ground type `+0x8A` (`0x002E9F29`) looked up in
  `soundfoottable.bin`, with the table's 32 added when the flag and the field's environment variant are both set.
  With a negative flag group 1 plays the variant as given (`0x002E9E99`).
- For group 2 with a variant below 10, when the actor's voice-pool entry (`+0x20` of the actor it resolves to through
  `0x00263F40` and `0x00263F10`) has state 3, its bank loaded (`0x0036ECA0`), the sound comes straight from that bank
  (`0x0036EC50`, `0x002E9F81`): the character's own voice.
- Outside that voice case a non-zero flag adds the field's environment variant `0x02099DBC` to the variant before the
  block lookup, for every group (`0x002E9FA7`).
- The footstep flag is set for types 1, 8, 9 and 10.
- A group above 2 gives -1 (`0x002E9E72`), as do the gates listed on
  [Character SE tables](../Game-Files-And-Data-Tables/character-se-tables-chse.md).

### The play routine

`0x0046CC70` refuses unless the emitter is enabled, byte `+0` = 1, and its owner is live. Then by mode:

| Mode | Does |
|---:|---|
| `0` | the chain above. Footsteps are dropped while a record test with `0x1A` holds; types 11 and 12 play only for the party's focus character; type 7 not while the last voice still plays. A new voice of types 4-7 stops the playing one, kept at `+0x18` with its type at `+0x1C` |
| `1`, `2`, `3` | a direct sound id from one of three bank getters, centred, at `volume * 64 / 128`; not authored |
| `4` | an explicit sound number at the character, bit `0x80000000` added below `0x100` |
| `5` | with type 1, stores `0xC00` in emitter word `+5` |

`0x003A0E50(id, position, record)` makes the sound. An id with bit `0x40000000` set is a battle-voice line, bank `id >> 8 & 0xFF`
and line `id & 0xFF`, played at the point in the Config voice language (`0x002DF460`); any other id plays from a block
bank at the point (`0x002DF280`), and -1 plays nothing. The same call serves `0x0046C8F0`, `0x00332C40` and `0x003B99D0`.
`0x003A0E80(kind, handle)` stops the previous voice of types 4-7 while it still plays (`0x0046CE04`-`0x0046CE1F`), with the
kind from emitter byte `+0x07`: kind 0 through the battle-voice stop (`0x001DC330`), kind 1 through `0x002DF0F0`.

That kind is written when a voice of types 4-7 starts: `0x003A10F0(id)` returns 1 when bit `0x40000000` of the id is clear
(a block-bank sound) and 0 when it is set (a battle-voice line), and `0x0046D055`-`0x0046D05E` stores it at `+0x07`
beside the handle `+0x18` and the type `+0x1C`.

The battle routine `0x00307300` plays mode 4 at a battle record's actor through `0x00329F70` (`0x00307727`), which passes
the record's `+0x08` to `0x0046CBB0`. That finds the actor's render record (`0x740` bytes each from `[0x022C6F28]`) and
calls `0x0046CC70` on its emitter at `+0x5F0`.

## Modding notes

- A sound is part of the animation: to add or move one, edit the `0x05` or `0x29` command in the animation block.
- The swing sample follows the weapon attachment's kind; the footstep sample follows the ground type and
  `soundfoottable.bin`.
- Voices interrupt voices on one character; footsteps and swings overlap.
- A `0x29` volume that scales to 0 plays nothing.

## Related

- [Sound effects](sound-effects.md) - the play call.
- [Sound variations](sound-variations.md) - the driver's own kinds, which shipped sounds do not use.
- [Spatial sound](spatial-sound.md) - the source the emitter builds.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Resource: `0x002EDBD0` calls `0x00409660`, `0x00409F50`; `0x00421E20` calls `0x002ED570`; those functions are documented on
  [resource sections](../Game-Files-And-Data-Tables/resource-sections.md).
- Rewards progression economy: `0x003A1180` is called by `0x0030C650`; those functions are documented on
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- World area: `0x003A13F0` is called by `0x00266D10`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
