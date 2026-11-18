[Home](../../README.md) / [Graphics](README.md) / Model effects and motion commands

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Model effects and motion commands: @FEF and the motion entries | format | Graphics | Character models / Model Files | The entries of the .cm and .ca containers that are behaviour rather than shape: the @FEF section that embeds an EFX0010 effect in 144 models, how the model row binds it and the start-up table that names the 144 files, and the motion entries @FMC (command blocks), @FMN (bone channel lists), @FMW (keyed channel data) and @FRM, with the readers that select and decode them and counts over the shipped files. | 0x00504F00, 0x00504E70, 0x00504940, 0x0016D6A0, 0x0040A230, 0x00409F80, 0x02B64380, 0x0041F340, 0x003B3550, 0x0041D220, 0x0041CA70, 0x004090D0, 0x0041CD30, 0x0041BEE0, 0x0041B4E0, 0x00409190, 0x00370E00, 0x0041B550, 0x0041B650, 0x00409170, 0x00409150, 0x0041A470, 0x00418650, 0x00418700, 0x004186A0, 0x0041FCF0 |

## What the player sees

Some monsters, NPCs, summons and gadgets carry an effect authored into their model file. Weapons that
draw, fire and reload, and treasure chests that open, play short command blocks stored in their own
`.cm`. Every other motion a model plays comes from its `.ca` files: each motion is a list of bone
channels with keyed values, plus a command block that runs on the motion's frames.

## Where it comes from

All of these are entries of the `@FRP` containers described in [model files](model-files-cm-ca.md):
`@FEF` only in `.cm` files, `@FRM` only in `.ca` files, and `@FMC`, `@FMN` and `@FMW` in both. The
effect section is registered with the rest of the file in the render resource bank; the bank makes
the model's effect ticket and effect context, as
[resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md) describes.
The motion entries are read when a presentation entry is set up to play a motion (`0x0041D220`).

## Layouts

### @FEF

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` |  | '@FEF', u32 kind 0, u32 length, u32 1 |
| `+0x10` | `char[32]` |  | the container's name |
| `+0x30` | `...` |  | a complete EFX0010 effect file: u32 `+0x08` = 1.0f, u32 `+0x0C` = entry length - `0x30` |

### @FMC, the command block

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` |  | 1 (`0x10001` in 405 of the 32,151 entries) |
| `+0x0C` | `u32` |  | record count |
| `+0x10` | `char[32]` |  | the command block's name (weapon_ready, treasure_open, ...) |
| `+0x30` | `...` |  | records, each: |
| `+0x00` | `u8` |  | 1 for the block's main record |
| `+0x03` | `u8` |  | sub-record count |
| `+0x04` | `u16` |  | record length |
| `+0x06` | `...` |  | sub-records: u16 key, u16 (length << 6 \| command count), then the commands |

A key of `0xFFFF` marks the block of commands that the walker `0x0041DA90` runs before the keyed ones; the other
keys are motion frames. `0x0041CD30` runs no commands: it keeps the marker's offset in the track state's `+0x90`
(`0x0041CE3D`-`0x0041CE42`). The walker reads `+0x90` (`0x0041DAD3`) and runs that block's commands through the table
`0x01EFFAF0` (`0x0041DB05`-`0x0041DB81`) before its calls to `0x0041E1D0`, `0x0041E000`, `0x00418880` and `0x00418750`
(`0x0041DBAD`-`0x0041DBFD`).

It runs them only for an active state (byte `+0x95`, `0x0041DAA8`) and an entry with `+0x0C` bit `0x100000`; with
bit `0x10` also set it skips a command whose table entry has a non-zero byte `+8` (`0x0041DB10`-`0x0041DB3D`). The
commands themselves are the authored presentation commands
([authored-presentation-commands.md](authored-presentation-commands.md)).

### @FMN, the bone channel list

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` |  | kind: `0x02001111` or `0x02001011` |
| `+0x0C` | `u32` |  | record count |
| `+0x10` | `char[32]` |  | the motion's name |
| `+0x50` | `u16` |  | duration in frames |
| `+0x54` | `u32` |  | offset of the constant pool, from the entry: f32 values to the end of the entry |
| `+0xF0` | `...` |  | records (the start `0x00409190` picks for both kinds), 22 bytes each: |
| `+0x00` | `u16` |  | node key |
| `+0x02` | `u16` |  | mask `0x1FF` channel mask, mask `0x7E00` record length (22) |
| `+0x04` | `u16[9]` |  | channel numbers in the paired @FMW; `0x8000` \| n where the mask bit is clear |

`0x00409190(entry)` gives the start of the records from the kind `+0x04`, by `kind & 3` and `(kind >> 24) & 3`
(`0x00409195`, `0x004091A1`). For `kind & 3` of 0 it is `+0x40`, `+0x60` or `+0xC0` for 0, 1 or 2; for `kind & 3`
of 1 it is `+0x70` for 0, `+0x90` for 1, and for 2 `+0xF0` with bit `0x1000` set (`0x004091B3`) or `+0xC0`
without it. Every other kind gives 0 (`0x004091E7`). The start is added to the entry's low 32 bits,
sign-extended (`0x004091B7`); both shipped kinds have bit `0x1000` set and give `+0xF0`.

### @FMW, the channel data

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` |  | channel count |
| `+0x30` | `u32` |  | offset of the value streams, from the entry |
| `+0x34` | `u32` |  | 1 = packed form (u16 channel table, `0x00409170`); otherwise the u32 table form (`0x00409150`) |
| `+0x40` | `...` |  | channel descriptor offsets, from the entry: u16[count] in the packed form, u32[count] otherwise |

```
packed descriptor:  +0x00 u8 frame count, +0x01 u8 n, +0x04 u32[n] frame-stream offsets,
                    then per key {u32 value-stream offset (low 17 bits), f32 bias, f32 scale}
```

A stream element starts with a flag byte: bit `0x80` means a 16-bit little-endian literal follows, bit `0x40`
means the stream's element 0 is reused, and otherwise a signed byte follows. A value is
`literal × scale + bias` for the first key and `literal × scale + previous value` after it; frame
literals add to the previous key's frame.

### @FRM

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0C` | `u32` |  | value 1 |
| `+0x10` | `char[32]` |  | the .ca file's name |
| `+0x30` | `...` |  | payload: byte `+0x01` to `0x003E18D0`, byte `+0x02` low six bits to skeleton `+0xA4`, u32 `+0x08` offset of a second region, from the payload (0 = no second region) |

### The version-1 .ca slot table

`+0x30` holds 80 (the columns) and `+0x34` the rows. `0x004090D0(container, row, column)` returns the
entry at slot `row × 80 + column` when the row is below `+0x34`, otherwise slot `column`; an empty
slot gives NULL, and so does a slot at or past the count `+0x0C` (`0x00409113`-`0x00409117`). The `@FMC`
blocks fill the first `80 × rows` slots and `@FRM` is the last slot.

## Shipped data

| Fact | Value |
|---|---|
| `@FEF` | 144 `.cm` files: 82 monsters, 27 NPCs, 26 summons, 9 gadgets; always entry 6 of 7; all start `EFX0010` with the size word equal to the entry length − `0x30` |
| `0x02B64380` paths | 144, set by `0x0040A230`; each slot is the fold of its file's name, and the 144 paths are exactly the 144 `@FEF` files |
| `.cm` motion entries | 45 files (29 weapons, 16 treasures); 209 `@FMC`, 111 `@FMN`, 111 `@FMW` |
| `.cm` command block names | every weapon: `weapon_shot`, `weapon_deact`, `weapon_active`, `weapon_ready`, `weapon_rlx_ready`; every treasure: `treasure_dead`, `treasure_ready`, `treasure_open`, `treasure_opened` |
| `.ca` entries | 31,942 `@FMC`, 18,303 `@FMN`, 18,303 `@FMW`, 3,164 `@FRM` (one per file, named after it) |
| version-1 `.ca` | 1,195; 80 columns in all; 1 row in 1,150, 3 in 45; `@FRM` in the last slot in all |
| `@FMN` records | 746,592, all 22 bytes, bit `0x8000` clear, mask bits matching the `0x8000` markers in all; no stream runs past its entry |
| `@FMW` form | packed in 110 `.cm` and 17,576 `.ca` entries, table form in 1 `.cm` and 727 `.ca` |
| frame counts | the first byte of each of the 1,446,602 packed channel descriptors equals the paired `@FMN` duration's low byte |
| `@FRM` payload | byte `+0x01` 1 in 2,977, 2 in 169, 4 in 18; second region present in 2,847 |

### The individual records

Every `@FMC`, `@FMN`, `@FMW` and `@FRM` of the shipped `.ca` and `.cm` files and of every used `.mot` slot is listed.
Records are keyed by source file, package slot, entry slot and offset, never by name. An entry whose bytes occur
more than once is written once in the record tables, and `slots` joins each occurrence to it through `content`.

| Table | Rows | One row per |
|---|---|---|
| [`model-effects-and-motion-commands-containers.tsv`](model-effects-and-motion-commands-containers.tsv) | 13,118 | `@FRP` container with any of these entries: `path`, `.mot` `package_slot`, `offset` in the file, `bytes`, `sha256_16`, `version`, the version-1 `columns` and `rows`, `slots`, and the count of each tag |
| [`model-effects-and-motion-commands-slots.tsv`](model-effects-and-motion-commands-slots.tsv) | 314,261 | `@FMC` (109,560), `@FMN` (95,814), `@FMW` (95,814) and `@FRM` (13,073) slot: `container`, `slot`, `tag`, `offset`, `kind`, `length`, `count`, `name`, `content`, and `links` |
| [`part 1`](model-effects-and-motion-commands-commands-part1.tsv) [`part 2`](model-effects-and-motion-commands-commands-part2.tsv) | 1,583,764 | command of each distinct `@FMC` (24,309): `stream`, `stream_kind`, `stream_offset`, `group`, `frame` (`0xFFFF` for the block the walker runs first), `command` order in the group, `offset`, `id`, `length`, and `operands` as stored |
| [`model-effects-and-motion-commands-fmn-part1.tsv`](model-effects-and-motion-commands-fmn-part1.tsv) | 15,805 | distinct `@FMN`: `kind`, `duration`, `tracks`, `track_start`, `pool_offset`, `header` (the bytes from `+0x30` to the records) and `pool` (the constant values as stored) |
| [`part 1`](model-effects-and-motion-commands-tracks-part1.tsv) [`part 2`](model-effects-and-motion-commands-tracks-part2.tsv) | 730,977 | track of each distinct `@FMN`: `record`, `offset`, `node_key`, `channel_mask`, `length`, and `words`, the nine channel words as stored |
| [`model-effects-and-motion-commands-fmw-part1.tsv`](model-effects-and-motion-commands-fmw-part1.tsv) | 24,540 | distinct `@FMW`: `channels`, `form` (1 packed, 0 table), `stream_base`, `header` |
| [`part 1`](model-effects-and-motion-commands-channels-part1.tsv) [`part 2`](model-effects-and-motion-commands-channels-part2.tsv) [`part 3`](model-effects-and-motion-commands-channels-part3.tsv) [`part 4`](model-effects-and-motion-commands-channels-part4.tsv) [`part 5`](model-effects-and-motion-commands-channels-part5.tsv) [`part 6`](model-effects-and-motion-commands-channels-part6.tsv) [`part 7`](model-effects-and-motion-commands-channels-part7.tsv) [`part 8`](model-effects-and-motion-commands-channels-part8.tsv) [`part 9`](model-effects-and-motion-commands-channels-part9.tsv) [`part 10`](model-effects-and-motion-commands-channels-part10.tsv) [`part 11`](model-effects-and-motion-commands-channels-part11.tsv) [`part 12`](model-effects-and-motion-commands-channels-part12.tsv) [`part 13`](model-effects-and-motion-commands-channels-part13.tsv) [`part 14`](model-effects-and-motion-commands-channels-part14.tsv) [`part 15`](model-effects-and-motion-commands-channels-part15.tsv) [`part 16`](model-effects-and-motion-commands-channels-part16.tsv) [`part 17`](model-effects-and-motion-commands-channels-part17.tsv) [`part 18`](model-effects-and-motion-commands-channels-part18.tsv) | 2,057,091 | channel of each distinct `@FMW`: `flags`, `frame_descriptors`, `value_descriptors`, `descriptor`, `frame_runs`, `value_runs`, `keys`, `first_frame`, `last_frame`, `first_value`, `last_value`, `keys_sha16` |
| [`model-effects-and-motion-commands-associations.tsv`](model-effects-and-motion-commands-associations.tsv) | 13,118 | link from a container to what names it: `relation` (`model file`, `model lane`, `action motion` or `script package`), `owner` (the model's bound id, or the script position that loads the slot), `selector` (lane, action-motion id or package slot), `evidence`, and `copies`, the containers with the same bytes |

- A link is one the game's own tables or a script's load makes: the model list, the action-motion array, or the
  package's load site. It does not say a motion would work on a different skeleton. Containers with equal bytes
  (1,101 contents occur more than once, in the language folders) stay separate rows.
- `links` of an `@FMC` slot lists the `@FMN` slots its `0x09` commands start. `links` of an `@FMN` slot gives two
  `@FMW` slots: the one the name search finds, then the one at the same position in the `@FMW` run.
- `frame_runs` and `value_runs` are the stored runs of each stream, as hex in file order, one group per stream.
  `descriptor` is the channel's whole descriptor. The frames and values follow from them by
  [Stepping a channel](#stepping-a-channel).
- `first_value` and `last_value` are the channel's first and last keys as `binary32` bits, high byte first.
  `keys_sha16` is the first 16 digits of the sha1 of the key frames as `u16` followed by the values as `binary32`,
  both little-endian.
- `n1168_e1.ca` is the only container with two `@FMN` of one name: both `idle0`, slots 80 and 88. The name search
  gives slot 89 for both, a section with no channels, so the channel data at slot 97 is not what that search finds.

The tables are written by `Database/Tools/catalogues/motion_entries.py`.

### Script motions and their models

A container row names the script that loads a package, which does not say who plays it.
[`motion-playback-sites.tsv`](motion-playback-sites.tsv) has one row for each of the 15,954 script cues, and
[`motion-playback-fmn.tsv`](motion-playback-fmn.tsv) one row for each of the 77,400 `@FMN` occurrences in script
packages and the 567 action containers with no owner.

A cue word's top byte less `0x10` is the package slot and its low 24 bits the entry, which for these version-0
packages is the `@FMC` slot (`0x004090D0`, `0x00409122`-`0x00409136`). The rows of the `@FMN` table follow the `0x09`
commands of those `@FMC` slots.

`motionplay` and `motionplay_bb` play on the issuing actor or on the actor named before the dot, through `0x003DD8D0`
and `0x002EB0D0(actor +0xC0)`, so they drive the actor's main model. `puppetmotionplay` plays on the puppet in slot
`d` of the table at `0x02B5EA20`, through `0x003EB720` and `0x003DD980`.

The main model comes from the `bindp` verbs (`0x00342640`, `0x002E28E0`). `bindh` and `bindc` attach a second model
(`0x002E3110`), and no `bindh` or `bindc` model in the scripts has a row in `highmodelreplace.bin`, the case in which
poll `0x003409F0` would bind it as main. A capture (`0x00262F90`) gives the script actor the body of another actor, and
sets `+0x18`, so `bindp2_d4` then skips (`0x0033F39A`).

| `status` of a cue | Sites | Meaning |
|---|---|---|
| `one_bind` | 8,485 | the script binds one model to this actor |
| `bind_before_cue` | 4 | several models, and the nearest bind in the cue's function comes first on every path |
| `puppet_one_bind` | 415 | the script binds one model to this puppet slot |
| `puppet_bind_before_cue` | 30 | several models, and the nearest bind in the cue's function comes first on every path |
| `several_binds` | 3,457 | several models bound; which one holds depends on the branch taken |
| `captured_party` | 2,472 | the body is a party or battle member, chosen by the party in play |
| `captured_zone_actor` | 623 | the body is a named actor of script manager 0, the zone in play |
| `captured_and_bound` | 276 | the actor both captures and binds; the order is decided at run time |
| `no_bind_found` | 118 | no bind and no capture on this actor in this script |
| `puppet_several` | 60 | several models bound to this puppet slot |
| `puppet_variable_id` | 14 | the puppet slot is a script variable |

An `@FMN` row is `resolved_one_model` (46,737), `resolved_several_models` (270), `partly_resolved` (558),
`no_fixed_model` (24,687) or `no_cue_site` (5,148), and `reason` says what stops it. The 567 action rows are
`action_no_model_row`: `0x003DCA30` looks a kind-30 motion up in `pc_skillmotion.bin`, `.ard` slot 7 and script
section 19 slot 7, and no row of those three names these ids. Their file names assign no model.

`bone_check` compares the track keys with that model's `@FTR` nodes as `0x00373540` does, one claim per node with flag
`0x100`. A track with no such node gets no row (`0x0041C0A6`), so that bone stays out of the motion. `name_search_fmw`
and `positional_fmw` are both kept, with their channel counts, and `content` joins the track and channel tables,
which keep the constant and absent channels.

`one_bind` means the only model this script binds to that actor, and a cue that runs before the bind plays on no
model of its own. `bind_before_cue` follows only the cue's own function. For `captured_zone_actor` the game finds
the actor by name in the script of manager 0, and which zone that is depends on the play session, so these rows name
no candidate; the table below lists candidates by name. `bone_check` shows a wrong pairing only when it is gross,
because bones share common keys across models; the pairing rests on the bind reading.

### The model behind each motion

[`motion-playback-models.tsv`](motion-playback-models.tsv) folds the `@FMN` occurrences into 9,167 rows, one for
each `@FMN` of a package and one for each ownerless action container. The nine language folders hold the same
`content` for a package's `@FMN`, and `occurrences` counts them. `use_status` says who plays the motion, or what
stops that being fixed.

| `use_status` | Rows | Occurrences | Meaning |
|---|---|---|---|
| `fixed_one_model` | 5,193 | 46,737 | every cue plays on the one model its script binds |
| `fixed_by_cue` | 30 | 270 | every cue is fixed, and different cues name different models |
| `bind_branch` | 1,464 | 13,176 | several models are bound to the actor or puppet slot, and the branch taken decides |
| `capture_or_bind` | 158 | 1,422 | the actor both captures and binds (`0x0033F39A` skips a bind while the capture holds) |
| `party_member_named` | 52 | 468 | a `capturebattleid` with a literal selector names the character |
| `party_slot_at_run_time` | 604 | 5,436 | the capture takes a party or guest slot, the controlled character, or a variable selector |
| `zone_actor_named` | 358 | 3,222 | the capture names an actor of the zone in play, and actors of that name are listed |
| `zone_actor_no_candidate` | 1 | 9 | the capture names an actor that no other script binds or places |
| `no_body_source` | 75 | 675 | the actor has no bind and no capture in this script |
| `puppet_slot_variable` | 4 | 36 | the puppet slot is a script variable |
| `mixed_run_time` | 27 | 243 | the cues are of more than one of these kinds |
| `part_fixed_` and a kind | 62 | 558 | some cues are fixed by a bind, and the others are of that kind |
| `no_literal_cue` | 572 | 5,148 | no cue in the script's listing names an `@FMC` entry that starts it |
| `ownerless_action` | 567 | 567 | an action container with no owner row |

`models` holds the models the binds fix and `candidates` those the script leaves open. For `party_member_named` the
candidate is the model in the [party table](../Party/party-table.md) row of the selector ([verb
arguments](../Scripts-And-Script-Commands/verb-arguments.md), verb `03E9`), and the capture happens only when the
roster holds that member (`0x003509E0`). `party_slot_at_run_time` lists the models of party-table rows 0 to 16.

A captured zone actor is found by name in the script of manager 0. Its candidates are the models other scripts bind
as the main model of an actor of that name, with a `bindp` verb (`0x00342640`, `0x002E28E0`), and the models of the enemy
placements whose `function` is that name, through `model_id` of the
[bestiary](../Enemy-Spawning/bestiary.md). When any candidate is in the area of the capturing script
only those are listed, and `evidence` names each source.

A handler's binds count for every name in its `symlink_actors`: a listing declares each such name as running that
handler's code (`rbn_a01`: `symlink NPC02(NPC01)`). A name in `symlink_actors` has its own directory entry holding
the same code, function, jump and footer offsets as the handler, with its own local storage offset (`+0x1C`) and
copy number (`+0x20`); `0x00266530` builds each record from its entry (`0x00266795`-`0x002667CA`).
`bindh` and `bindc` attach a second model (`0x002E3110`) and the load verbs bind nothing, so neither adds a candidate.

The cue arguments of all 15,954 sites are literals, so `no_literal_cue` means that no motion verb in the script's
listing starts that entry. An `ownerless_action` row names no model and no candidate.

`keyed_channels` counts channels with their mask bit set and `constant_channels` those with it clear. All these
`@FMN` have a non-zero `+0x54`, so `0x00418880` writes each clear channel from the pool (`0x00418ADD`-`0x00418B1F`).
`keyed_over_fmw` counts keyed channels past the end of the section the name search finds. It is 0 in every row, and
the 149 rows whose `name_search_fmw_channels` is 0 have no keyed channel.

`bone_check` gives `model:on_bones/no_bone/bones_without_track` for each model in `models` and `candidates`, by the
claim rule of `0x00373540`. A bone without a track gets no row from this motion. Whether it then shows its rest pose
depends on its byte `+0x28A` while the game runs (`0x0041D6F0`). `skeletons` counts the distinct bone sets among those
models.

`exact_fit` lists the tested models whose bones are exactly the track keys, and `same_bones` every model in [the
asset list](model-asset-list.tsv) with those bones (eight, then `+n`). They show the skeleton a motion was made on,
not the body it plays on: a capture of party slot 0 plays on whoever holds that slot. Of the 5,193 `fixed_one_model`
rows, 3,378 have such a model, and in 3,307 the bound model is one of them.

Its columns are `path`, `package_slot` (`-` for an action container), `fmn_slot`, `name`, `content`, `occurrences`,
`name_search_fmw`, `name_search_fmw_channels`, `tracks`, `keyed_channels`, `keyed_over_fmw`, `constant_channels`,
`cue_sites`, `use_status`, `models`, `candidates`, `skeletons`, `bone_check`, `exact_fit`, `same_bones`, `evidence`
and `reason`.

`Database/Tools/catalogues/motion_playback_models.py` writes the table.

## Loader behaviour

### Binding @FEF

- `0x00504F00` binds the `@FEF` section at model row `+0x228` with `0x00504E70`, which falls back to a
  bank-wide search by tag and name when the model's own entry has no such section.
- `0x00504940` stores the section pointer at row `+0x230` and calls `0x0016D6A0(ticket, section + 0x30)`
  with the bank entry's ticket `+0x44` (`0x005049BD`). `0x0016D6A0` is a bare `ret`: binding the row does
  nothing with the embedded effect.
- The bank entry is the container's own (word `+0x1F0`) when its first word equals the `@FEF` id word
  `+0x228` (`0x00504981`), else the one `0x00409F50` gives for `+0x228` (`0x00504991`); the section is
  `0x004096C0` of that entry with the offset `+0x238` (`0x005049A2`). The call is made only for a non-null
  section (`0x005049B1`).
- `0x0041F340` makes the render record's effect context: when the record's `+0x288` is −1 and the row's
  `@FEF` bank index is set, it calls `0x003B3550(record, ticket)` and stores the result at record `+0x288`
  and row `+0x240`.

- `0x0041F340` takes its blocks in arena 6 through `0x003AB8B0(size, mode)` (`0x0036A100` for mode 0,
  `0x0036B160` for mode 1) and returns them through `0x003AB910`, which calls `0x0036C620` for a null or
  4-byte-aligned pointer and `0x0036C5D0` otherwise.

### The record's effect handle

The handle at record `+0x288` names a `0x38`-byte slot at `0x02EBD480 + (handle & 0x3F) × 0x38`; every
helper below first checks that the slot's id equals the handle and does nothing otherwise. The slot's
`+0x10` is the effect instance and its byte `+0x30` holds three flags.

- `0x003B3400`, from `0x003B3550`, takes the head of the free list `0x02EBDBA0`, appends the slot to the
  used list (`0x02EBDB98` / `0x02EBDBA8`) and writes a new serial (`0x02EBDBB4`) into the bits under mask `0xFFFFFC0` of the id.
- `0x003B3300(handle)`, from `0x0041E860`, ends the instance (`0x0024EE60`), moves the slot back to the
  free list, keeps only bits under mask `0xF000003F` of the id and clears `+0x10`.
- `0x003B3080(handle)` sets bit `0x1` of `+0x30`. The update pass `0x0024B9B0` holds a kind-3 instance on any
  step the bit is clear in the slot its dword `+4` names, and clears the bit when it is set; `0x0042D830` sets it each time
  it processes the record, so a model's effect advances only while its character does.
- `0x003B33A0(handle, b)` sets bit `0x2` of `+0x30` and stores `b` in bit `0x4`; `0x0042D830` passes the
  result of `0x00420FB0` when `0x004210D0` allows it.
- `0x003B3AA0(handle, v)` stores the vector at instance `+0x320` with w = 1, or 1, 1, 1, 1 when the
  instance's `+0x368` bit `0x4000` is set; `0x0042D830` passes the vector from `0x003E5710`.
- `0x003B30D0(handle, a, b)` sets the instance's two tint colours `+0x398` (from `a`) and `+0x334`
  (from `b`) with their red, green and blue at `0x80`, and raises `+0x368` bit `0x8`; when the
  instance's `+0x36A` bit `0x8` is set, it also puts both alphas at `0x80` and drops the bit again.
- `0x003B30A0(handle, v)` stores `v` at instance `+0x08`, and `0x003B3CA0(handle, v)` runs `0x003A9490(v)`
  on the instance, then makes the previous instance current again.

- The registration that makes the ticket indexes the pointer table `0x02B64380` by the fold of the name.
  `0x0041E3A0` calls `0x00409F80` at start-up (`0x0041E40B`), which calls `0x0040A230`: 144 stores of
  `PS2Data\obj_finish\in\<folder>\...\<name>.cm` paths, so every shipped `@FEF` model has its entry.

### The @FEF path table

`0x02B64380` is a table of 8-byte path pointers indexed by a fold of a model's name. For a name that ends in a letter
and four digits, the slot is `0x500` times the letter's character code plus the four digits read as a decimal
number: `m1006` folds to `0x500 × 0x6D + 1006` = 140,526, the slot `0x02C76AF0`. `0x0040A230` stores each of the 144
`.cm` paths of the shipped `@FEF` models in the slot its name folds to.

The registration `0x00409FE0`
([resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md)) reads it. For a file with an
`@FEF` section it folds the last five characters of the file's name (`0x0040A0C0`-`0x0040A129`) and loads that slot
(`0x0040A12C`). It passes the path to `0x001D6EC0` (`0x0040A17F`), which returns the character-effect path that the
async-load manager keeps for the same `.cm` (`0x001A09E0`); the number after `chara\h` in that path goes into the
ticket (`0x003B3B10`, `0x0040A1C4`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [model-effects-and-motion-commands-state.tsv](model-effects-and-motion-commands-state.tsv): the 144 filled slots of `0x02B64380` | `void*` | 0 (zero-filled tail of `.data`) | the `.cm` path of the model whose name folds to the slot: the row's `index`, `name`, `folder` and `path`, with `literal` the address of the string | `0x0040A230`, once at start-up, at the site in `set_by` | `0x00409FE0` (`0x0040A12C`), for the model being registered |

### Selecting a motion

`0x0041D220(entry, descriptor)` sets up a presentation entry:

- `+0x31C` takes the motion number (descriptor `+0x20`) and `+0x31A` the record's signed byte
  `+0x413` (descriptor `+0x24`);
- the `@FMC` section goes to `+0x320`, or `@FRP` when the entry has no `@FMC`;
- when an `@FRM` exists and is longer than its header, `+0x378` gets its payload offset and `+0x37C`
  the second region's offset;
- `0x0041CA70` picks the command block `0x004090D0(container, +0x31A, +0x31C & 0xFFF)` into `+0x368`, and
  `0x0041CD30` positions each track on its first record, keeping the `0xFFFF` block apart.

Command `0x09` (`0x00417F40`) starts a motion. For a command block with `+0x04 & 3` non-zero, the case of every shipped
block, the motion is the `@FMN` at slot `(word +2 >> 1) + +0x2A` of the entry's container (`0x0041805C`-`0x00418087`). The
block with `+0x04 & 3` of 0 would take a name at the command's `+2` instead (`0x00417FF3`-`0x00418057`).

`+0x2A` comes from `0x0041CC90`, or from the record's first-`@FMC` slot `+0x2FA` for a motion number with bits above
`0xFFF` (`0x00423E24`-`0x00423E3A`). In the shipped data the slot is an `@FMN` for all 155,630 commands of the `.ca`
and `.mot` files with no base, and for all 225 of the `.cm` files with the file's first `@FMC` slot as the base.

When the `@FMN`'s kind has `& 3` and `>> 4 & 3` both 1, it binds the channels (`0x0041849B`-`0x00418561`). The `@FMW` is
found by the `@FMN`'s name: `0x00409930` returns the first slot with that tag and name (`0x00409780`), and when there is
none `0x00409FA0` searches the bank (`0x004184C5`-`0x004184FB`).

The model binder `0x0041FCF0` also keeps the model's own first `@FMC` index at record `+0x2FA`
(`0x0041FE83`), which the event map in [model files](model-files-cm-ca.md) adds to.

### Reading the channels

- `0x0041BEE0` binds `@FMN` (or `@FRP`) and `@FMW` by tag and name into a track descriptor (`+0x54`,
  `+0x58`), and `0x0041B4E0` resolves the entries.
- `0x0041B4E0` returns at once, leaving `+0x70` and `+0x78` as they are, when the first resource index
  `+0x50` is `0xFFFF` (`0x0041B4F1`). Otherwise `+0x70` gets slot `+0x5C` (signed) of the section at
  `+0x54` in the resource that `0x00409F50` gives for `+0x50` in the bank `+0x48` (`0x0041B51B`).
- `+0x78` gets slot 0 of the section at `+0x58` in the resource of `+0x52` (`0x0041B539`). Both go through
  `0x004096C0` and `0x00408F80`; a `+0x52` of `0xFFFF` gives `+0x78` = 0.
- It walks the `@FMN` records from the start `0x00409190` gives, advancing by each record's length.
  `0x00370E00` turns the node key into a bone, and `0x0041B550` sets up the record's nine channels in a
  `0x108`-byte row (count at owner `+0x2BC`).
- `0x0041B550` stores the bone at row `+0x100`, the record's offset in the section at `+0xFC` and 0 at `+0x102`
  (`0x0041B585`-`0x0041B5A3`).
- For channel `k`, 0 to 8, `0x0041B550` tests bit `1 << k` of the record word `+2`: a present channel goes to
  `0x0041B650` with the next u16 of the list at record `+4`, and bit `0x80 << k` of `+0x102` is set when that
  returns 1; an absent one gets frame `0xFFFF` at slot `+0x04` and 0 in the eight bytes at `+0x08`
  (`0x0041B5B2`-`0x0041B608`).
- With the section's dword `+0x54` at 0 only present channels take a u16 from the list; otherwise every channel
  takes one (`0x0041B5B9`-`0x0041B5BD`, `0x0041B603`-`0x0041B60F`).
- The `@FMN` duration goes to the descriptor's `+0x16`, and to `+0x18` unless state `+0x96` bit `0x40` is
  set.
- `0x00418880` applies the `@FMN`'s constant values. The pool is the entry plus its `+0x54` (`0x004189CB`-`0x004189D7`). For
  a channel with its mask bit clear, or with slot frame `+0x04` of `0xFFFF`, and only while `+0x54` is non-zero, it
  writes `pool[word & 0x7FFF]`, keeping it at the slot's `+0x0C` (`0x00418ADD`-`0x00418B1F`).
- `0x0041B650` starts a channel and `0x0041A470(slot, @FMW, frame)` moves its pair of keys forward until
  the next key's frame is past the requested frame.
- The values are written to the bone and every bone linked through `+0x278`: `0x00418650` into bone
  `+0x190`, `0x00418700` into `+0x1B0` and `0x004186A0` into `+0x1D0`, the last skipped while bone byte
  `+0x280` bit `0x2` is set.
- Each writer `(bone, row, column, value)` stores the float at element `row * 4 + column` of its array
  (`0x00418670`, `0x00418720`, `0x004186D0`), then moves to the bone `0x0020E600` decodes from `+0x278` and
  stops when that is 0. `0x00418650` and `0x00418700` do nothing for a null bone (`0x00418653`, `0x00418703`).
- `0x004186A0` tests bit `0x2` of the first bone only (`0x004186A4`): with it set no bone is written, and
  the linked bones are written whatever their own bit.

### Stepping a channel

A channel slot keeps the current key's frame at `+0x04`, the next key's frame at `+0x06`, the
previous and next values at `+0x08` and `+0x0C`, and two stream cursors, one for frames (`+0x10`)
and one for values (`+0x16`): byte offset in the stream, element in the run, stream number and step
count. A stream's flag byte also gives the run length in its low six bits: a run holds that many
literals, or one when bit `0x40` is set, of one or two bytes by bit `0x80`, and the cursor moves past the run
when its element reaches the length.

- In the packed form `0x0041BA10` steps the frame cursor and `0x0041BC40` the value cursor, moving to
  the next stream of the channel at the end of one; in the table form `0x0041B920` and `0x0041BB00` do
  the same, with `0x0041B460` decoding a frame delta and `0x0041B3A0` a value (`literal × scale +
  previous`).
- The value steps are `binary32`: the literal goes through `cvtdq2ps`, then `mulss` and `addss`
  (`0x0041B427`-`0x0041B434`, `0x0041BD1D`-`0x0041BD2B`), so a stored value is the result of those rounded steps.
- `0x0041A7F0(slot, @FMW)` reads the first frame delta of a channel; a delta of 0 marks the channel as
  a single key (`+0x04` = `0xFFFF`).
- `0x0041A8E0(slot, @FMW, frame)` moves the key pair forward until the next key is past `frame`, and
  also marks the channel single when its two key frames meet.

### Applying a frame

`0x0041ADA0(stream, …, entry, frame)`, from the seek `0x0041C850`, puts an entry at a frame: the frame
modulo the `@FMN` duration (`+0x50`) becomes the entry's `+0x0C`, every channel moves there
(`0x0041A8E0`), and the bones are written. `0x00418880(stream, entry)`, from the walker, does the same
work each frame for a playing entry (bit `0x2` of `+0x08`) whose word `+0x0A` is 1. Both take the bones
from the model's bone array (`0x0020E600` of model `+0x84`, `0x290` bytes a bone) and the channel rows
from the owner's `+0x2B8` block (`0x108` bytes a row, count `+0x2BC`).

On a non-zero frame (`0x004189F9`) `0x00418880` can adjust the frame in two steps, both only in 60 fps mode
(`0x01F82E38`). `name` is the model name at `+0x3C` of the render record the stream's `+0x2E0` points to, and
`motion` is the stream's section name `+0x2EC`.

- It first rounds the frame down to a whole frame (`floorf`, `0x004192FE`) when `0x001ED240(name, motion, id, frame)`
  answers 1 (`0x004192C9`), or when the frame is exactly one frame step (`0x01DFE0BC`) before the end `+0x16` and
  `0x001EC6B0(motion)` answers 1 (`0x004192F5`).
- It then adds `0x001ED020(name, …)` to the frame (`0x00419329`, `0x00419334`). The answer is 0 except in the two
  branches the table lists.

Each branch of those functions, and of four others that test a name in the same way, is a row of the table
below. A row's conditions all hold together. An event is `0x001EC560` answering non-zero, which needs the marked
slot `0x01DFE40C` at 4 or below with a non-zero count at `0x01F832B0`, and `0x00265680` answering 0.

`0x001ED240` tests the story progress values in one list, and a value in the list settles the answer with two
exceptions. Progress `0x7CE` goes on to the cut-scene names when the count is not 3 or `n1018` is not in the
name, and progress 0 does so outside map `0x112`. So does every progress value not in the list. The cut-scene
names are tried in the table's order, and the first one found settles the answer, so a later name is not tried.
Outside an event the frame test is made first, 10.5 and then 21. Every `|frame - x|` test is strict.

The code holds the conditions only. Nothing in the exe says why a branch exists.

| Table | Rows | One row per |
|---|---|---|
| [`model-effects-and-motion-commands-exceptions.tsv`](model-effects-and-motion-commands-exceptions.tsv) | 69 | branch that gives an adjustment or an answer of 1 |
| [`model-effects-and-motion-commands-exception-assets.tsv`](model-effects-and-motion-commands-exception-assets.tsv) | 260 | name and shipped file it reaches |

| Column | Table | Meaning |
|---|---|---|
| `function`, `branch` | exceptions | the function, and the row's number within it |
| `scope` | exceptions | `event`, `outside event`, or `any` for a function that makes no event test |
| `story_progress` | exceptions | the value `0x00265270` must return |
| `event_count` | exceptions | the marked slot's count at `0x01F832B0` (0 when `0x01DFE40C` is above 4) |
| `cut_frame` | exceptions | the value of the cut-scene frame counter `0x01F832C4` |
| `map` | exceptions | the value of the loaded map `0x00314910()` |
| `cut_name`, `cut_assets` | exceptions | text that must be inside the current cut-scene name (`0x001C50C0`, `strstr`), and the cut-scene files it reaches |
| `name_field`, `match`, `name`, `assets` | exceptions | whether the model or the motion name is tested; `substring` (`strstr`) or `exact` (`strcmp`); the text; and the files it reaches |
| `frame_test` | exceptions | what the frame must satisfy, or, where the cell says so, another value |
| `adjustment` | exceptions | what the answer does |
| `sites` | exceptions | the instructions that decide the row |
| `kind`, `match`, `name`, `path` | exception-assets | `model`, `motion` or `cut scene`; the test; the text; and a shipped file whose name passes it |

`0x001ED0D0` gives the weight `0x00417012` uses, 0.5 unless its row applies. `0x001EDAD0` is used at `0x003D91AC` and
`0x001EDBB0` at `0x002F2CBA` ([element types](effect-element-types.md), [element runtime](effect-element-runtime.md)).
`0x001EDCD0` decides the branch at `0x0040AF5A`. `0x001EC760` also tests cut-scene names, for the number of passes a frame
runs, and has no rows here ([frame update order](../Engine-Core/frame-update-order.md)).

`Database/Tools/catalogues/playback_exceptions.py` writes these tables.

At frame 0 `0x00418880` writes, for each row with a bone, the first value of each of the nine
channels the record's mask names and that has data (`0x0041A7F0`, then `0x00418650`, `0x00418700` or
`0x004186A0`), or the channel's bias from the `@FMW` table at `+0x54` when it has no data, after clearing bit `0x1` of
the bone's byte `+0x28A`; it clears that bit on the non-zero-frame path too (`0x004194B7`).

A bone whose byte `+0x28A` is 0 takes its rest pose from the skeleton
instead (`0x0041D6F0`: `0x00409270` finds the node for the bone's `+0x27E` and `0x00409300` reads it, all
of it into `+0xC0` when bone `+0x28B` bit `0x4` is set, else only the translation into `+0xF0`).

`0x0041D180` copies the 48-byte template `0x02CA43D0` into a bone's `+0xC0` block; both appliers use it before rebuilding
a pose. `0x0041BDC0`, given a bound track at `+0x70`, clears bit `0x80` of the entry's `+0x96`; for a packed motion it
then restarts, in every row, each channel the mask names through `0x0041B650` at frame 0.

With the entry's `+0x96` bit `0x10` set, `0x0041C260` (from `0x0041BEE0`) keeps each bone's current rotation `+0xC0`
(through `0x0046D730`) at `+0x120` and the 32 bytes from `+0xF0` at `+0x130`, or only clears bit `0x400` of the skeleton
entry's word `+0x00` when that bit is set; with bit `0x20` set, `0x0041C200` clears bit `0x10` of each bone's word
`+0x280`.

### Blending into a new motion

While the entry's `+0x96` bit `0x10` is set, `0x00418880` cross-fades each bone whose `+0x28B` bit `0x2`
is set. The progress `+0x98` advances each frame by `[0x01DFE0BC]` × `+0x9C`, and the blend ends (bit `0x10`
cleared) once it passes 1.0. The weight is `+0x98` itself when the stream's word `+0x358` is 16 (the value
authored command `0x08` stores); otherwise it is `+0x98` through the easing curve that the words `+0x358`
and `+0x35A` (stored by command `0x2C`) select: `0x0046FAE0(+0x98, +0x358, +0x35A)` (`0x004189A4`) reads
`0x01F20E60 + ((a × 3 + b) × 0x1E0)`, 120 floats per curve at 60 fps.

The curves' entry count is the dword `0x01F20A98`, 60 in the file: `0x0046FAE0` reads entry
`t × (count − 1)`, clamped to the curve (`0x0046FAEF`), and `0x0046FBF0` doubles the count for the 60 fps time
base (`0x0046FC4D`) and resamples the nine curves to it (`0x0046FCC0`).

[`motion-blend-curves.tsv`](motion-blend-curves.tsv) lists the 60 stored samples of each of the nine curves, with
each sample's address and raw bits. `0x0046FAE0` tests the entry against the count and tests neither `a` nor `b`.
Entries 60 to 119 of each curve are zero in the file.

| Column | Meaning |
|---|---|
| `curve` | `a × 3 + b` |
| `a`, `b` | the two selector words |
| `entry` | the sample, 0 to 59 |
| `address` | the sample's address in the image |
| `f32_bits` | its raw 32-bit float |
| `value` | the same number to nine significant digits |

The 60 fps resampler is `0x0033E5E0`. Entry `2k` is source entry `k`, entry `2k + 1` is the mean of source entries `k`
and `k + 1`, and the last entry copies source entry 59 (`0x0033E84D`-`0x0033E858`). The table comes from the executable
with sha256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

It turns the rotation channels into a matrix (`0x0046D380`, three angles through the sine table
`0x01F004E0`, 32,768 entries) and that into a quaternion at bone `+0x110` (`0x0046D730`, normalised by
`0x00476E70`, which falls back to (0.57735, 0.57735, 0.57735, 0) for a zero quaternion).

It interpolates from the pose kept at `+0x120` toward it with `0x00476F40`, a spherical interpolation
that takes the shorter arc. It copies the start instead when the sine-table value for the angle is 0
or the dot product exceeds 1. It writes the result as the rotation of `+0xC0` (`0x00477130`) and mixes
the translation: `+0xF0` = weight × `+0x1B0` + (1 − weight) × `+0x130`, with w = 1.

With the entry's `+0x96` bit `0x20` set instead, the quaternion goes to bone `+0x1A0` and bit `0x10` of the
bone's word `+0x280` is raised. Otherwise the channels build the matrix `0x02CA43D0`, which
`0x0041D180` copies into the bone's `+0xC0`, with the translation copied from `+0x1B0`.

The other matrix helpers of this code are `0x0046D120` (identity), `0x0046D2A0(m, a)` (identity with
the 2 × 2 rotation by `a` in its first two rows), `0x0046D360` (`0x00202B90`, then w = 1),
`0x0046D950(m, axis, a)` (rotation by `a` about an axis), and `0x0046D8E0` / `0x0046D920`, which store a
vector times the matrix's `+0x3C` into its translation row, with or without w.

## Modding notes

- An `@FEF` model also needs its path in the `0x02B64380` table; that table is filled by code, so a new
  `@FEF` model has no entry.
- Binding the model row passes the embedded `EFX0010` only to the empty routine `0x0016D6A0`.
- Keep each `@FMN` paired with an `@FMW` of the same name; the track binds both by name.
- Keep every `@FMN` record 22 bytes and its mask bits matching the `0x8000` markers.
- A packed channel's frame count byte equals the motion's duration in every shipped file; keep them
  equal.
- In a version-1 `.ca`, the command block for motion n of row r sits at slot `80 × r + n`.

## Related

- [Model files](model-files-cm-ca.md): the containers, the model row and the event map.
- [Resource ownership](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): effect tickets and effect contexts.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` child selector `0x004090D0`.
- [Authored presentation commands](authored-presentation-commands.md): the commands inside `@FMC`.
- [Effect files](effect-files-efx-efb.md): the `EFX0010` format.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 5 calls with 4 other topics</summary>

**Party** (explained on [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [player movement](../Movement-And-Pathfinding/player-movement.md))

| Function | | Functions |
|---|---|---|
| `0x00265680` | is called by | `0x00358CB0`, `0x00358F90` |

**Saving, loading and settings** (explained on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md))

| Function | | Functions |
|---|---|---|
| `0x00314910` | calls | `0x002EF2B0` |

**Status effects and KO** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00265680` | is called by | `0x00310DB0` |

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md))

| Function | | Functions |
|---|---|---|
| `0x00266530` | calls | `0x00265B60` |

</details>
