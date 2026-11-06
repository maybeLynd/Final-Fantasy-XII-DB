---
title: "PKFL packages: the per-area .mot, .snd, .vpc and .vpcjp containers, their offset and size directory, and the slot readers"
kind: "format"
category: "PKFL package files"
addresses: "0x0032FCA0, 0x0032FC30, 0x0032F430, 0x022C6E70, 0x022C6E98, 0x022C6EE8, 0x022C6EC0, 0x0032F260, 0x0032F290, 0x0032F2C0, 0x0032F2F0, 0x0032F3A0, 0x0032F320, 0x0032F360, 0x003DD4C0, 0x003DF440, 0x003DF2C0, 0x003E9F80, 0x003E9EF0, 0x002DF980, 0x003DDA20, 0x0034AB50, 0x00347B00, 0x003DD8D0, 0x003DD980, 0x003DEC90, 0x003EA0D0, 0x0036B970, 0x003499C0, 0x003DD770"
---

## What the player sees

Nothing directly. Each area's extra motions, its sound set and its voice clips arrive in PKFL packages,
and a package is how a script asks for "motion 3" or "voice 5" of the current area without knowing where
in the file it lies. The `.vpc` and `.vpcjp` packages of an area are the same clips in the chosen voice
language and in Japanese.

## Where it comes from

The packages sit beside each area's script in the archive, `<area>.mot`, `<area>.snd`, `<area>.vpc` and
`<area>.vpcjp`. They are files of the per-area records in the resource kinds the area loader uses
([file size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)): kind 5 records are
`{ebp, mot, fpk}` (three files per zone, index `3a` for field id `a`), kind 8 records `{ebp, mot, snd, vpc}` and kind `0x25`
records `{ebp, mot, snd, vpcjp}` (four per event, index `4a` for event number `a`). Paths come from `0x002DF980(kind, index)`.

## Layouts

All multi-byte fields are little-endian.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | 'PKFL' | only byte 0 is tested, for non-zero |
| `+0x04` | `u32` | slotCount | 16 (.mot, .snd) or 64 (.vpc, .vpcjp); not read |
| `+0x08` | `{u32 offset, u32 size}[slotCount]` |  | offsets from the file start; {0, 0} = slot empty |

The directory ends at file offset `0x88` for 16 slots and `0x208` for 64. Every payload starts on a `0x800`
boundary, the first at file offset `0x800`.

No package is held in memory whole. `0x0032FCA0` reads only the directory, the first `0x88` or `0x208` bytes, into
the table of that size `0x0032F430` allocated for the manager slot, and the slot readers use it as read. Each payload
is read on its own into its consumer's buffer ([reading a slot](#reading-a-slot)). The one check is byte 0: when
it is 0, every slot reader refuses with −1. The readers return a slot's offset and size as stored.

## Shipped data

| Fact | Value |
|---|---|
| packages | 10,314: 4,392 `.mot`, 2,304 `.snd`, 1,809 `.vpc`, 1,809 `.vpcjp` |
| empty packages | 27: 9 `.mot`, 9 `.vpc`, 9 `.vpcjp`, every pair `{0, 0}` |
| layout | in all 10,287 others: every pair inside the file, offsets ascending, the first at file offset `0x800`, each next payload at the first `0x800` boundary after the one before, zero bytes in the gaps, file size a multiple of `0x800` |
| `.mot` slots | 0-15 used (1,539, 3,186, 1,737, 1,134, 774, 540, 378, 270, 108, 54, 54, 36, 36, 27, 18, 18 packages); every payload is an `@FRP` container |
| `.snd` slots | 0-7 in every package, payloads starting with the dword 2; slots 8-15 in 9, 1,809, 324, 225, 153, 99, 45 and 18 packages, payloads starting `WD` |
| `.vpc` and `.vpcjp` slots | 0-13 of 64 used, the same occupancy in both (1,782 down to 9); every payload is a `VSP1` voice set |

Four tables list every package and every used slot:

| File | Rows | One row per |
|---|---:|---|
| [`pkfl-packages-rows.tsv`](pkfl-packages-rows.tsv) | 10,314 | package file in each of the nine language folders |
| [`pkfl-mot-slots-rows.tsv`](pkfl-mot-slots-rows.tsv) | 9,909 | used `.mot` slot, with its `@FRP` container |
| [`pkfl-snd-slots-rows.tsv`](pkfl-snd-slots-rows.tsv) | 21,114 | used `.snd` slot, with its split container and list, or its `WD` bank |
| [`pkfl-voice-slots-rows.tsv`](pkfl-voice-slots-rows.tsv) | 9,180 | used `.vpc` or `.vpcjp` slot, with its `VSP1` cues |

Every row gives the language folder, the archive path and the area. A package row adds its size, SHA-256, used
slots, the folders with the same bytes, the size-table kind and id that name it, the slots its area's script loads
and the used slots it never loads. A slot row adds the offset and size, the decoded payload, the script steps that
load the slot (`script@pc`) and the number of steps that play from it.

### Columns of the package and slot tables

Lists of slot numbers, entries and ids are in ascending order and separated by spaces. Where such a column has
nothing to list, the cell holds `-` instead.

| Column | Holds |
|---|---|
| `family` | in pkfl-packages-rows.tsv and pkfl-voice-slots-rows.tsv, the package's extension: `mot`, `snd`, `vpc` or `vpcjp` |
| `sha256` | the SHA-256 of the package file, 64 hexadecimal digits |
| `slots_used` | the slots whose directory pair is not `{0, 0}`; the placeholder on the 27 empty packages |
| `same_bytes_in` | the language folders whose file at the same path has the same bytes, its own folder included: all nine on 10,296 rows, `de es fr it us` on 10 and `ch cn in kr` on 8 |
| `fst_kind_id` | each file size table entry that names the package: the kind (5, 8 or 37, which is `0x25`) and the id, then the builds whose table holds it (such as `CH` or `KR+CH+CN`), entries separated by semicolons; the placeholder on the 1,436 packages no table names |
| `fst_size_match` | `yes` when the size those entries record equals the package's `bytes`, on all 8,878 named packages; `-` on the 1,436 others |
| `slots_loaded` | the slots that the steps of the package's script load (the placeholder on 198 rows) |
| `slots_never_loaded` | the used slots the script never loads: `slots_used` less `slots_loaded` |
| `loads_of_empty_slots` | the slots the script loads that are empty: `slots_loaded` less `slots_used`; it occurs in `.mot`, `.vpc` and `.vpcjp` packages only |
| `list_slots` | in a `.snd` package, the slots 0 to 7 whose first part is an `SPP1` list; empty on the 8,010 other packages |
| `list_slots_never_loaded` | of those, the slots the script never loads; empty on the other packages |
| `size_field` | in pkfl-mot-slots-rows.tsv, the `@FRP` size at `+0x08`, at most the slot size |
| `size_field_equals_slot` | `yes` when `size_field` equals the slot's `size` (9,729 rows), `no` when it is smaller (180) |
| `name_matches` | `yes` when `name` is `<area>.mNN` with `NN` the slot number; `yes` on all 9,909 rows |
| `member_count` | the number of members in the `@FRP` container, the sum of the counts in `member_tags` |
| `member_tags` | each member tag with its count, such as `@FMC x5 @FMN x5 @FMW x5 @FRM x1` |
| `fmc_count` | the number of `@FMC` members, which bounds the entry a motion cue may name |
| `cue_entries_not_below_fmc` | the cue entries at or above `fmc_count`; the placeholder on all 9,909 rows, since every entry is below the count |
| `members_inside` | `yes` when every member lies inside the slot; `yes` on all 9,909 rows |
| `loaded_by` | in the three slot tables, the script steps that load the slot, each as the script and the step's offset (`alc_a0100.ebp@0x00BE8`); the placeholder when no step loads it |
| `load_sites` | the number of steps in `loaded_by` |
| `cue_sites` | the number of steps that play from the slot |
| `cue_entries` | the distinct entries those cue words name; the placeholder where `cue_sites` is 0 |
| `format_page` | the page that describes the payload's format |
| `split_count` | in pkfl-snd-slots-rows.tsv, the part count of the two-part container in slots 0 to 7: 2 on all 18,432 such rows; empty on the 2,682 `WD` rows |
| `split_end_equals_size` | `yes` when the second part ends at the slot's size (18,423 rows); `no 0x100` on the 9 rows of slot 6 of `bhm_c0102`, the list with no records part |
| `spp1_magic` | `SPP1` when the first part is a sound list (4,095 rows), empty otherwise |
| `spp1_count` | the list's id count (`+0x04`); 0 when the slot holds no list, empty on `WD` rows |
| `spp1_ids` | the list's ids |
| `bank_length` | the list's `bankLength` (`+0x08`), the bytes of `SeSep` records to open |
| `has_map_no` | the list's `hasMapNo` (`+0x10`): 1 on 2,871 rows, 0 on 1,224 |
| `map_no` | the list's `mapNo` (`+0x12`): a map number, or 65535 (`0xFFFF`) on 1,215 rows |
| `wd_slot_asked` | when `has_map_no` is 1, the slot `8 + map_no % 10` whose size is asked for; the placeholder when it is 0 |
| `sesep_source` | where the `SeSep` records were read: `part 1`, the second part, on 4,086 rows; the placeholder on the 9 rows of slot 6 of `bhm_c0102` |
| `sesep_ids` | the ids of those records, in order |
| `sesep_matches_list` | `yes` when `sesep_ids` equals `spp1_ids` (4,086 rows), `no` on the 9 rows of slot 6 of `bhm_c0102` |
| `wd_bank_id` | on a `WD` row, the bank id (`u16 +2`); the slot is `8 + wd_bank_id % 10` on all 2,682 rows |
| `wd_data_size` | the trailing data size (`u32 +4`) |
| `wd_count8`, `wd_countC` | the two record counts at `+0x08` and `+0x0C`, equal on every row |
| `wd_flags14` | the flags at `+0x14`: `0x8000` (1,116 rows), `0x0` (918) or `0x10000` (648) |
| `cues_without_bank` | in pkfl-voice-slots-rows.tsv, the cues that have no `sabf` bank: 0, or 1 or 2 on 36 rows |
| `cues_outside` | the cues that lie outside the slot; 0 on all 9,180 rows |
| `sabf_banks` | the cues that have a `sabf` bank; with `cues_without_bank` it makes `cue_count` |
| `bank_names` | the bank name of each cue in cue order, `-` for a cue without a bank |
| `cue_entries_over_count` | the cue entries at or above `cue_count`; the placeholder on all 9,180 rows |

### What the slots hold

- `.mot`: all 1,101 slots of a folder are `@FRP` version 0 named `<area>.mNN`, `NN` the slot number
  ([resource sections](../Game-Files-And-Data-Tables/resource-sections.md)). 1,100 hold equal numbers of `@FMC`,
  `@FMN` and `@FMW` members and one `@FRM`; slot 5 of `wdl_a0600` holds 3, 2, 2 and 1.
- The `@FRP` size at `+0x08` equals the slot size in 1,081 and is smaller in 20, which end in zero bytes: slots 2
  and 4-7 of `dgl_h0100` and `rwg_b0200`, 2-4, 6 and 7 of `dgl_h0101`, and 3-7 of `rwg_b0100`.
- `.snd` slots 0-7: each is the two-part container `0x0036B970` splits (count 2 in all 2,048 of a folder). 1,593 have
  both parts empty (0x40 bytes); 455 hold an `SPP1` list and its `SeSep` records
  ([map sounds](../Sound-And-Music/map-sounds.md)).
- `.snd` slots 8-15: 298 `WD` wave banks, each with its own bank id at `u16 +2`
  ([map pack](../World-Areas-And-Travel/mpk-map-pack.md)). The slot is 8 + bank id % 10 in all 298, and the bank id is
  the map number (`+0x12`) of a list in the same package in 296: `nac_a0300` slot 9 (2251) and `rwf_c0100` slot
  10 (4702) are the others.
- `WD` record counts `+0x08` and `+0x0C` are equal in all 298; the flags `+0x14` are 0x8000 in 124, 0 in 102 and
  0x10000 in 72.
- `.vpc` and `.vpcjp`: 510 `VSP1` sets per extension and folder, 2,554 cues, 2,551 of them a `sabf` bank and 3 with
  size 0 ([voices](../Sound-And-Music/voices.md)).
- The `.vpc` and `.vpcjp` of an area use the same slots, with the same cue count, the same cues without a bank and
  the same bank name in every cue in 508 of the 510 slot pairs. In slot 0 of `rwg_d0100` and slot 1 of `rwg_d0101`
  the `.vpc` banks are named `sum_Fah` and the `.vpcjp` banks `sum_INOUT`.

### The language folders

Each of the nine folders `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr` and `us` holds 488 `.mot` (300 under
`event/`, 188 under `plan_map/<x>/<zone>/global/`), 256 `.snd`, 201 `.vpc` and 201 `.vpcjp`. The copies are
byte-identical in all nine except `var_z0100.vpc` and `var_z0102.vpc`, one version in `ch`, `cn`, `in` and `kr` and
another in `de`, `es`, `fr`, `it` and `us`.

The path arrays name a build's own folder for kind 8 (`in` for Japanese, ASIA and IN) and the `in` or the `ch` copy
for kind `0x25` ([file size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)). The area loader asks
kind `0x25` only for the `.vpcjp` (`0x0032FDD4`, `0x0032FFD6`), so the `.vpcjp` in `cn`, `de`, `es`, `fr`, `it`, `kr` and
`us`, 1,407 files, are named by no path: the image holds the `in` and `ch` `.vpcjp` paths only.

### What no script loads

- The test events `evt_t0005` and `evt_t0015`: their `.mot`, `.vpc` and `.vpcjp` (four files per folder) are in no
  path array or size table, and no string in the image contains `evt_t`. `evt_t0005.mot` is empty and its script
  asks for slots 1 and 2.
- In every folder, 45 `.mot` packages have one used slot their area's script never loads. 16 of them have no load
  at all: `sum_a0000` to `sum_m0000` (slot 0 only), `evt_t0015`, and the zones `dst_a01` and `ene_a01`.
- 15 `.snd` lists in 8 packages are never loaded: `bhm_c0102` 6, `dgl_g0100` 4, `rbn_a0300` 3-7, `sum_a0000` 1 and
  2, `sum_a0001` 7, `sum_b0000` 1 and 2, `sum_c0000` 1 and 2, `sum_e0001` 3. No script loads a `WD` slot, and
  `0x003DF2C0` discards the size `0x0032F3A0` gives for one (see [the slot readers](#the-slot-readers)).
- 9 voice slots are never loaded: slots 0 and 1 of `evt_t0005` and 0-6 of `naf_a0101`.
- Scripts load 33 `.mot` slots that hold nothing, and 2 voice slots: slot 1 of `naf_b0100` and slot 3 of
  `nal_a0100`. 59 `.mot` cue words name such a slot and 73 a slot that is never loaded; neither plays.

## Loader behaviour

### The directory tables

`0x0032F430`, at start-up, allocates four `0x88`- or `0x208`-byte tables per manager slot: `.mot` at `0x022C6E70`,
`.snd` at `0x022C6E98`, `.vpc` at `0x022C6EE8` and `.vpcjp` at `0x022C6EC0`. When a manager slot
loads, `0x0032FCA0` (from `0x0032FC30`) reads into them:

- for manager slots 0 to 3, the first `0x88` bytes of the `.mot` (record index + 1);
- for manager slots 1 to 3 (kind 8), also the first `0x88` bytes of the `.snd` (+ 2) and `0x208` of the
  `.vpc` (kind 8, + 3) and `.vpcjp` (kind `0x25`, + 3);
- for manager slot 4, none of them.

A table it does not fill, or a file with no size, gets byte 0 cleared. Each request it files sets a pending
bit in the slot's word `0x022C6E48[g]`: `0x2000` for the `.mot` (completion `0x003302B0`), `0x1000` for the
`.snd` (`0x00331760`), `0x8000` for the `.vpc` (`0x00331820`) and `0x4000` for the `.vpcjp` (`0x003317C0`).

### The slot readers

Each reader takes a manager slot `g` and a slot `k`, and returns −1 when `g` is 4 or more (a signed test) or
byte 0 of the table is 0. No reader bounds `k` against the table.

| Reader | Table | Returns | Caller |
|---|---|---|---|
| `0x0032F260` | `.mot` | offset of slot `k` | `0x003DD4C0` (script motion slots) |
| `0x0032F290` | `.mot` | size of slot `k` | `0x003DD4C0` |
| `0x0032F2C0` | `.snd` | offset of slot `k` | `0x003DF440` (sound sets) |
| `0x0032F2F0` | `.snd` | size of slot `k` | `0x003DF440` |
| `0x0032F3A0` | `.snd` | size of slot `k + 8` | `0x003DF2C0`, which discards the value |
| `0x0032F320` | `.vpcjp` or `.vpc` | offset of slot `k` | `0x003E9EF0` (voice loads) |
| `0x0032F360` | `.vpcjp` or `.vpc` | size of slot `k` | `0x003E9F80`, `0x003E9D30`, `0x003E9E10` |

`0x0032F320` and `0x0032F360` take the `.vpcjp` table when their third argument is 0 and the `.vpc` table
otherwise.

### Reading a slot

A consumer allocates the slot's size and files the area file's kind and index with the slot's offset as
the read's file offset (`0x003E9EF0` passes it in the request record), so only that payload is read. The
read queue rounds the offset down to a `0x800` boundary
([file requests](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md)). A size of 0
loads nothing.

`0x003E9EF0(record, table)` takes the offset from `0x0032F320` with the manager slot in record byte `+5`, the slot in
byte `+0` and `table` (`0x003E9EF0`-`0x003E9F0A`). For table 0 (`.vpcjp`) or 1 (`.vpc`) it files the kind word `+0xC`
or `+0xE`, the index word `+0x10`, the buffer `+0x20` or `+0x28` and the size `+0x14` or `+0x18`
(`0x003E9F0F`-`0x003E9F59`), with completion `0x003E9D30` for table 0 and `0x003E9E10` otherwise (`0x003E9F1F`-`0x003E9F31`).
It then sets the record's byte `+4` to 2 unless it is 5 (`0x003E9F5E`-`0x003E9F64`).

`0x003DF440(g, id, k)` pushes arena 5 after taking the size (`0x003DF45A`-`0x003DF468`) and pops it on every path
(`0x003DF541`). For a size above 0 it takes the offset (`0x003DF483`), turns `g` and `id` into the kind and index with
`0x0032F170` (`0x003DF49A`), and allocates with `0x0036A100`, or, when that gives null, with `0x0036A190` in arena 6
(`0x003DF4A9`-`0x003DF4C3`).

It stores the kind, `index + 2`, the block, `id`, the size and the offset in the slot
record (`0x003DF4E3`-`0x003DF50F`). While `0x00267310(g)` is non-zero it parks the record in state 1 and reads nothing
(`0x003DF513`-`0x003DF526`); otherwise `0x003DF550` files the read (`0x003DF52F`).

### The script steps that reach a slot

The manager slot is always the running script's, so a script reads only its own packages.

| Verb | Path to the reader | Calls per folder |
|---|---|---:|
| `motionread` `0x0A2` | `0x003492A0` -> `0x003DDA20` arms record `0x02B581A0 + (16g + k) x 0x1C` and sets `1 << k` in `0x02B58A60[g]` (`0x003DDA5D`); the sweep `0x003DD4C0` reads the size and offset | 1,511 |
| `eventsoundread` `0x151` | `0x00344660` -> `0x003DF3E0` -> `0x003DEC90`, then `0x003DF440` reads the size and offset | 459 |
| `voiceread` `0x085`, `voiceread_20a` `0x20A` | `0x0034EE40`, `0x0034E8B0` -> `0x003EA0D0` frees slot `k` (`0x003EA0F0`) and loads it from both tables (`0x003EA139`, `0x003EA14B`); a slot the free leaves in state 2, 4 or 5 is not loaded and the call answers 0 (`0x003EA10B`, `0x003EA11B`). Each table load `0x003E9F80` reads the size with `0x0032F360` (`0x003EA009`) and, while `0x00267310(manager)` is non-zero, parks the slot in state 1 without a read (`0x003EA095`-`0x003EA0A1`); otherwise `0x003E9EF0` reads the offset and files the read (`0x003EA0AD`) | 389, 171 |

A `.mot` slot plays through a motion cue word: the top byte less 0x10 is the slot and the low 24 bits the entry.
`motionplay` `0x0A5` (`0x0034B2C0`) pushes a blend of 0.0 and runs `motionplay_bb` `0x0BB` (`0x0034AB50`), which splits
the word (`0x0034AB96`-`0x0034AB9C`) and refuses a slot above 15 (`0x0034ABAB`). `puppetmotionplay` `0x41E` and `0x41F` do
the same in `0x00347B00` (`0x00347B57`-`0x00347B7D`).

Both also refuse while `0x00267310` gives a non-zero byte for the calling actor's manager slot, its byte `+0x15`
(`0x0034AB8E`-`0x0034ABA9`, `0x00347B70`-`0x00347B7B`), and take `g` from the running script's record `+0x28`
(`0x0034ABB0`, `0x00347B82`). `0x0034AB50` pops its last argument as an integer and converts it to a float
(`0x0034AB72`-`0x0034AB7B`), plays its own actor and calls `0x003DD8D0` (`0x0034ABC2`). `0x00347B00` pops a float
(`0x00267DB0`, `0x00347B30`), plays the actor `0x003EB720` gives for a popped id, does nothing when that is null
(`0x00347B63`-`0x00347B6E`), and calls `0x003DD980` (`0x00347B95`).

`0x003DD8D0` and `0x003DD980` play only a record in state 4 (`0x003DD905`, `0x003DD9B5`), as motion
`(16g + k) << 16 | entry` (`0x003DD949`-`0x003DD954`). `0x00427320` takes the block back from `0x003DD740` with `g` from
bits `0xF00000` and `k` from bits `0xF0000` (`0x00427518`-`0x00427528`). In every shipped cue word the entry is below the
slot's `@FMC` count.

`0x003DD8D0` hands `0x002E9560(actor)` to `0x002E4F40` (`0x003DD90E`-`0x003DD919`), sets bit `0x1` of actor byte `+0xD`
and stores `k` at `+0xF5` (`0x003DD91E`-`0x003DD925`), calls `0x002E8170(actor, [r + 0xD] >> 7)` with `r` the record
`0x00263F40(actor)` returns (`0x003DD92C`-`0x003DD93B`), and posts with `0x002EB080(actor, motion, 0, float)` (`0x003DD958`).
`0x003DD980` hands `0x002E95B0(actor)` to `0x002E4FA0` (`0x003DD9BE`-`0x003DD9C9`), calls `0x002E81D0(actor, 0)` (`0x003DD9D3`)
and posts with `0x002EB0D0(0, actor, motion, 0, float)` (`0x003DD9F9`).

Each folder's scripts make 15,954 motion cue calls (`motionplay` 7,554, `motionplay_bb` 7,881, `puppetmotionplay`
514 and `puppetmotionplay_41f` 5), 4,943 voice cue calls and 2,877 sound
cue calls with a literal word; every voice and sound cue names a slot its script loads. All nine folders call these
verbs with the same arguments. The four directory tables are reached only by the seven readers, `0x0032F430` and
`0x0032FCA0`.

### Slot numbers out of range

- `.mot`, `k` of 16 or more, record `16g + k` free (state 0, `0x003DDA3B`): `0x003DDA20` arms it with no bound and sets
  `1 << (k & 31)` in mask `g`. The sweep tests bits `0x1` to `0x8000` of each mask (`0x003DD510`, `0x003DD68A`), so it
  never reads the table for it; the record stays in state 2 and `motionreadsync` (`0x003499C0`) waits while the state
  is 2 or 3 (`0x003499E5`).
- `.mot`, `k` of 16 or more, record `16g + k` in use: `0x003DDA20` arms nothing (`0x003DDA40`, `0x003DDA69`), and
  `motionreadsync` follows the state of that record (`0x003DD770`).
- Record `16g + k` is, for `k` from 16 to 79 - 16g, a slot of a later manager slot; record 80 starts at the masks
  `0x02B58A60`.
- `.mot`, an empty slot: the sweep finds size 0 and sets state 0 (`0x003DD574`-`0x003DD578`), so `motionreadsync` goes
  on and the cues play nothing.
- `.snd`, `k` above 7: `0x003DEC90` releases nothing (`0x003DEC9E`). `0x003DF440` reads the size (`0x003DF45A`) and, when
  it is above 0 (a `WD` slot), allocates the block, takes record pointer 0 (`0x003DF4C8`-`0x003DF4E1`) and stores to
  address `0x2C` (`0x003DF4EA`), which faults. A size of 0 returns at `0x003DF46F`. Either way `1 << (k & 31)` is set
  in `0x02B59C20[g]` (`0x003DF42B`).
- `.snd`, `k` of 16 or more: `0x0032F2F0` reads the pair at table + 8 + 8k, past the `0x88` bytes.
- Voice, an empty slot: `0x003EA0D0` frees the slot first, both table loads return 0 at size 0 (`0x003EA013`), and the
  slot stays free (state 0).
- Voice, `k` of 64 or more: the record `0x02B5D0B0 + k x 0x40` has no bound (`0x003E9F93`-`0x003E9FAA`); record 64 starts
  at `0x02B5E0B0`, the word `0x003EA015` tests, and `0x0032F360` reads past the `0x208` bytes.

## Modding notes

- Keep byte 0 non-zero; nothing else in the header is checked, and `slotCount` is never read.
- Put every payload on a `0x800` boundary: the read starts at the offset rounded down.
- `.mot` and `.snd` directories are read as 16 slots and `.vpc` and `.vpcjp` as 64. Use `.mot` slots 0-15: the sweep
  never loads a higher one (`0x003DD68A`), so `motionreadsync` waits for good, or follows the record of another area
  slot that the number reaches (`0x003499E5`, `0x003DD770`).
- Load `.snd` slots 0-7 only: `eventsoundread` of a slot from 8 up that has a size stores through a null record
  (`0x003DF4EA`), and one of 16 or more reads past the table. Voice slots are 0-63.
- Build a package as the shipped ones are: `PKFL`, the slot count, the pairs, zeros to `0x800`, each payload at the
  next `0x800` boundary and zeros to the boundary after the last. All 10,314 shipped packages rebuild byte for byte
  this way.
- A `.snd` slot 0-7 keeps the two-part container: count, part sizes, the header of `(count + 1) × 4` bytes
  rounded up to 0x40, `h = (4 × (count + 1) + 0x3F) & ~0x3F`, each non-empty part behind 0x40 zero bytes.
  `0x0036B970` refuses one whose header and parts do not add up to the block size: it needs
  `h + Σ (size ? size + 0x40 : 0) == [block + 0x18]`, the block 0x40 bytes before the container
  (`0x0036BA16`-`0x0036BA45`, `0x0036BA48`).
- A `VSP1` set rebuilds byte for byte from its banks with the cue table padded to 0x40, each bank at the next 0x10
  boundary, and a cue without a bank at the next offset with size 0.
- A cue's bank offset and size must each fit 24 bits and the bank must start with `sabf`: `0x003E9C10` reads
  `+0x08 & 0xFFFFFF` and `+0x0C & 0xFFFFFF` (`0x003E9C94`, `0x003E9CE2`), compares the magic (`0x003E9CC6`-`0x003E9CD8`), and
  writes the volume into bits `0x7F000000` of `+0x08` and the pan into `+0x0F` (`0x003E9CF9`-`0x003E9D09`).
- Keep the slot and cue order of the `.vpc` and `.vpcjp` the same, and change the `.vpcjp` in `in` (and `ch` for the
  Korean and Chinese builds); the other `.vpcjp` copies are never read.
- Keep the package's size-table entry: the area loader reads no directory for a negative size (`0x0032FE54`).
- Keep the `.vpc` and `.vpcjp` of an area in step: the voice language picks which one plays.

## Related

- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): the script motion slots that read `.mot`.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` containers inside `.mot`.
- [Voices](../Sound-And-Music/voices.md): the `VSP1` voice sets and the voice verbs.
- [Sound banks](../Sound-And-Music/sound-banks.md): the sound data in `.snd`.
- [File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md): the kinds and records the packages belong to.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x003DEC90` calls `0x002DEB40`, `0x002DF050`; `0x003E9C10` calls `0x002DF660`; those functions are documented on
  [actor record](../Characters-And-Objects/actor-record.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Input: `0x00267310` is called by `0x002E09A0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00263F40` is called by `0x00300310`, `0x003003F0`, `0x00310920`, `0x00311F70`, `0x0033FFC0`, `0x00345430`,
  `0x00349680`, `0x0037D000`, `0x003B7B00`, `0x003B7D80`, `0x003B7F40`, `0x00505240`; `0x00267310` is called by `0x002E45E0`,
  `0x002E5750`; `0x002EB0D0` is called by `0x002E28E0`.
- Movement: those functions are documented on [battle units](../Characters-And-Objects/battle-units.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md).
- Movement: and on [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md).
- Movement: and on [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md).
- Party: `0x00263F40` is called by `0x00304180`; those functions are documented on
  [party control modes](../Engine-Core/party-control-modes.md).
