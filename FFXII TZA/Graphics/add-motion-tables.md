---
title: "Add-motion tables: .adm, skeletonmapping.bin and highmodelreplace.bin"
kind: "format"
category: "Graphics"
addresses: "0x001BDC40, 0x001BDD20, 0x001BE1A0, 0x01F81250, 0x001BE420, 0x001BE430, 0x00863110, 0x002EDF90, 0x003714A0, 0x00377C20, 0x0017FFB0, 0x004776D0, 0x0046D380, 0x0036FFF0, 0x02AD9E30, 0x02AD9E38, 0x00372820, 0x003703A0, 0x0037CCC0, 0x02ADD940, 0x02ADD938, 0x0037CB90"
---

## What the player sees

The high-detail models of the main characters and a few NPCs bend some bones on top of whatever
motion is playing: a joint follows another bone's angle through a set of keyed poses, or a face
switches between posed groups under the control of the pose sequencer. In towns some of these models
use a second, civilian set of tables. One high-detail body moves part of its skeleton with a partner
model's bones, and some models are swapped for others as the story advances.

Each name in `add_motion_list.txt` brings in a table `<name>.adm` and, when that file exists, a second table
`<name>_town.adm`. A high-detail model is given the two tables whose names match its own file name, and its bones
follow the town table while the current field is flagged for it.

## Where it comes from

The files are in the archive at `ps2data/add_motion/`. All three readers run once at start-up and
read their files whole:

- `0x001BDC40`, the registry made by `0x001BE3E0` (kept at `0x01F81250`), runs `0x001BDD20`, which reads
  `./PS2Data/add_motion/add_motion_list.txt` and, for each name, `./PS2Data/add_motion/%s.adm` and
  `./PS2Data/add_motion/%s_town.adm` when present;
- the first boot frame `0x0022A0B0` runs `0x0036FFF0` (`./PS2Data/add_motion/SkeletonMapping.bin`) and
  `0x0037CCC0` (`./PS2Data/add_motion/HighModelReplace.bin`).

`0x001BE3E0` builds the registry only while `0x01F81250` is 0: it allocates `0x28` bytes (`0x00210EC0`) and stores the
result there, 0 when the allocation fails, in which case `0x001BDC40` is not run (`0x001BE3ED`-`0x001BE414`). `0x001BDC40`
clears the list pointers `+0x00`, `+0x08` and `+0x10`, gives `+0x18` the vtable `0x00902720` through `0x001EDF00`, which
drops the name it is handed (`0x001BDC73`), sets the table selector `+0x20` to 0 (`0x001BDC79`) and then runs
`0x001BDD20` (`0x001BDC7F`).

## Layouts

All multi-byte fields are little-endian.

### .adm

A flat stream, read in order with no offsets.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i16` |  | track count |

Track (8 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | kind: 0 keyed by a bone's angle, 1 chosen by a pose sequencer slot |
| `+0x01` | `u8` |  | kind 0: which angle (0, 1 or 2) drives the keys |
| `+0x02` | `u16` |  | kind 0: the driving bone; kind 1: the sequencer slot |
| `+0x04` | `i16` |  | group count |
| `+0x06` | `i16` |  | records per group then group count x { `0x1C`-byte group header, records per group x `0x1C`-byte record } |

Group header (`0x1C`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` |  | kind 0: the key, one per angle |
| `+0x18` | `u32` |  | kind 1: the group's id |

Record (`0x1C`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | bone |  |
| `+0x04` | `f32[3]` |  | rotation angles in degrees |
| `+0x10` | `f32[3]` |  | copied by the parser; the pose code does not read them |

The parser `0x001BE1A0` keeps a 32-byte record per file (`+0x00` name, `+0x14` track count, `+0x18`
tracks), 16 bytes per track (`+0x00` the u16 at file `+0x02`, `+0x02` records per group, `+0x04` the
group count, `+0x06` kind, `+0x07` angle, `+0x08` the group array; `0x001BE260`-`0x001BE2AB`), `0x28` bytes
per group (the header, then the record array at `+0x20`) and the records as they are.

### skeletonmapping.bin

```python
+0x00  i32  record count
record:  char[32] model name, i32 n, then i32[n]: per bone of that model, a partner bone or -1
```

### highmodelreplace.bin

```python
record:  i32 model id, i32 b, i32 c (-1 matches anything),
         then pairs {i32 replacement id, i32 lowest story progress} ended by -1
the file ends with a -1 where a record would start
```

## Shipped data

| Fact | Value |
|---|---|
| `add_motion_list.txt` | 251 bytes, 23 lines; 22 end with CRLF, the last (`hs0020_01`) does not |
| names read | 22; all have `<name>.adm`, 15 (all `hc…`) also `<name>_town.adm`; the longest is 9 characters |
| `.adm` files | 39 (30 `hc`, 7 `hn`, 2 `hs`); `hn1018_12` and `hs0020_01` are never read |
| tracks | 4 per file in 35, 2 in 2, 1 in 2; 146 in all, 111 kind 0 and 35 kind 1 |
| kind 1 tracks | always track 0 of a four-track file; slot 0; group 0's header all zero in all 35 |
| kind 0 tracks | angle 1 in 74, 2 in 37; 26 driving bones from 9 to 84 |
| groups | 2 per track in 90, 3 in 22, 4 in 34; group id 1, 2 or 3 in 91 groups of kind 1 tracks |
| records | 3,553; 4 to 18 per group; bones 4 to 84; angles −195.0 to 189.4 degrees; second triple −0.094 to 0.133 |
| the stream | ends exactly at the file size in all 39 |
| every track | one row each in [`add-motion-tables-rows.tsv`](add-motion-tables-rows.tsv), 146 rows: the file, whether the list makes the game read it, its size and SHA-256 prefix, the track's kind, angle, driving bone or slot, group and record counts, each group's key (kind 0, three angles) or id (kind 1), and the bones its records move |
| other text files | `hc1004_02.txt` (2,191 bytes, 59 lines), `pc1004_02_open.txt` (735 bytes) and `pc1004_02_close.txt` (744 bytes), all CRLF. No string in the executable names them: its `add_motion` paths are `add_motion_list.txt`, `%s.adm`, `%s_town.adm`, `SkeletonMapping.bin` and `HighModelReplace.bin`, and the words `numMotion`, `numHighModels` and `anmIndex` occur nowhere in it |
| `hc1004_02.txt` | `numMotion=4`, then per motion a line `motion [<name>]:<joint or texture>,<axis>,<jointIndex or anmIndex>=<n>,numKeys=<k>,numHighModels=<m>` and k keys, each a `key <i>` line followed by m lines `<bone>:` and six numbers. Left Hand: joint 26, axis y, 2 keys of 6 bones. Right Hand: joint 16, axis y, 2 keys of 6 bones. Eyes: texture, anmIndex 0, axis x, 4 keys of bones 6 and 7. Mouth: joint 29, axis z, 2 keys of 6 bones. The joint keys carry six numbers on the `key` line too |
| `pc1004_02_open.txt`, `pc1004_02_close.txt` | `number of joints: 10`, then ten lines `<joint> translate: x y z rotate: x y z` for `s29_j_ago`, `s30_j_dlip_a`, `s31_j_dlip_b`, `s32_j_bero`, the same three again, `s8_j_ulip_a` and `s9_j_ulip_b` twice. The files differ in two numbers only: the third rotation of `s29_j_ago` (27 open, 18.99978828 close) and of `s8_j_ulip_a` (1.817221471 open, 5.000033855 close) |
| `skeletonmapping.bin` | 196 bytes, one record: `hc1006_03`, 39 values; bones 20–29 follow 27, 28, 29, 27, 28, 29, 30, 27, 28, 29; bones 31–38 follow 33; the rest −1 |
| `highmodelreplace.bin` | 540 bytes, 22 records; one pair in 21, two in 1; b and c −1 in 18, 1 and 0 in 4; a lower-case `c`, `n` or `s` id maps to the upper-case letter's id; one replacement waits for progress 1570 |

### Columns of add-motion-tables-rows.tsv

| Column | Holds |
|---|---|
| `sha256_16` | the first 16 hex digits of the `.adm` file's SHA-256, on the row of the file's track 0 (39 rows, one per file); empty on the file's other tracks (107 rows) |
| `group_keys_or_ids` | one entry per group of the track, separated by spaces, as many as `groups` on all 146 rows: for a kind 0 track the group's key, its three angles in degrees written `x/y/z` (for example `0/45/0`); for a kind 1 track the group's id (`0 1 2 3` on 29 tracks) |

## Loader behaviour

### add_motion_list.txt and .adm

- `0x001BDD20` reads the list into a stack buffer of the file size plus 1, rounded up to 16
  (`0x001BDDBA`–`0x001BDDDE`), and cuts it at each CRLF with `strstr`; a name is taken only when a CRLF
  follows it. Nothing writes a zero byte after the text, so the search after the last CRLF runs past
  the file's last byte into uninitialised stack bytes, up to the first zero.
- The shipped list therefore yields 22 names only while those stack bytes hold no CRLF before a zero.
  When they do, the unterminated `hs0020_01` and the bytes after it become a 23rd name.
- For each name it parses `<name>.adm`, copies the name over the record's `+0x00`, and then parses
  `<name>_town.adm` and names it `<name>_town` with `sprintf`. Both go into the registry's list.
- The name is written over the parsed record, whose track count sits at `+0x14`: a name of 20
  characters or more, `_town` included, overwrites the count and the track pointer.
- `0x001BE1A0` trusts every count: nothing is checked against the file size. It allocates
  `track count x 0x10`, `group count x 0x28` and `records per group x 0x1C` bytes, each a 64-bit `mul`
  whose result becomes `0xFFFFFFFFFFFFFFFF` on overflow (`cmovo`, `0x001BE210`, `0x001BE299`, `0x001BE319`).
- It reads the counts as signed 16-bit values (`0x001BE1FB`, `0x001BE28B`, `0x001BE314`). It zeroes the 32-byte record and
  each track and group array after allocating it (`0x001BE1E3`-`0x001BE1F7`, `0x001BE231`, `0x001BE2BE`), fills each record
  array by copying, and returns the record (`0x001BE3CD`). The file comes in its second argument (`0x001BE1B1`); `rcx`
  is replaced by the size `0x20` before any use (`0x001BE1AC`).

### Which table a model uses

- `0x002EDF90(index, request, resource)` keeps a state at render record `+0x6C8` (0 unbound, 1 and 2
  bound, 3 and 4 released). The record is `[0x022C6F28] + index x 0x740` for the signed 16-bit index; an index of -1,
  a record address of 0 or a record whose `+0x284` is 0 is left as it is (`0x002EDF93`-`0x002EDFBC`). Its caller is
  `0x002E3110`, the part attach of the [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- On an unbound record the request becomes the state (`0x002EDFCE`); request 2 then runs `0x00863110` with the record's
  `+0x6E8` and `+0x6F0` (`0x002EDFD4`-`0x002EDFEA`), so request 1 binds it without a lookup. On a bound record request 0
  releases, 1 to 3 and 2 to 4 (`0x002EDFEF`-`0x002EE00C`), and request 1 or 2 restores a released state, 3 to 1 and 4
  to 2 (`0x002EE017`-`0x002EE038`); other requests change nothing.
- In its mode 4 `0x002E3110` sends request 1 for the entry `[+0xC0]` and 2 for the one `0x90` bytes after it, and in
  mode 2 request 0 to both, skipping an entry whose dword `+0x00` is -1; the entry's word `+0x00` is the index and its
  `+0x04` the resource (`0x002E3444`-`0x002E34D2`).
- `0x00863110` takes the file name of the resource between the last backslash and the first dot into
  a 16-byte buffer and calls `0x001BE430`, which stores the record with that name at `+0x6E8` and the one
  named `<name>_town` at `+0x6F0`.
- The resource is an id: `0x002E98F0` splits it into a kind and an index, adding `0x33` to a kind 1 index, and
  `0x002DF980` reads the path from the table `0x0215F000` (`0x00863137`-`0x00863144`). The backslash is searched for back
  from the path's end (`0x0086315C`-`0x00863167`) and the dot with `strchr` (`0x00863174`); `strncpy` copies the name at
  its own length into the zeroed buffer, with no test against its 16 bytes (`0x0086317A`-`0x00863194`).
- `0x001BE430(registry, name, base, town)` compares the name of every record in the registry's list with `name` and
  with `<name>_town`, built with `0x0017D2E0` and `%s_town` (`0x001BE457`-`0x001BE466`, `0x001BE481`-`0x001BE4FC`). Each
  match is stored, so the last record of a name wins; a name with no record leaves its field as it was, and a null
  output is skipped.
- `0x003714A0`, run for every skeleton while its pose is composed, uses `+0x6F0` when it is set and
  bit `0x8000` of the current field's word in the table at `0x02ADD100` is set (`0x00377C20`); the registry's
  `+0x20` (`0x0017FFB0`) forces the town table with 1 and the base table with 2.

### Applying a track

`0x003714A0` builds two tables per skeleton bone, from group 0's records: the track and the record that
name that bone. Then for each track:

- **Kind 0** (needs two groups or more). The driving bone is looked up in the skeleton that the posed
  skeleton's `+0x0C` names. It takes that bone's angle `+0x190 + 4 × angle` and
  the same angle of the bone's matrix at `+0x230` (`0x003719F7`–`0x00371A4A`) and uses their difference
  in degrees; `0x00180060` / `0x00180090` can replace it with a set value.
- Kind 0 then finds the pair of groups `k`, `k + 1` whose keys (group `+0x00`, groups `0x28` bytes apart)
  hold the value `v`, the first or last pair when `v` lies outside them. With
  `t = (v - key[k]) / (key[k + 1] - key[k])` each record's three angles (record `+0x04`-`+0x0C`) become
  `(1 - t) x a[k] + t x a[k + 1]`, so `t` runs past 0 or 1 beyond the end keys (`0x00371B13`-`0x00371C82`).
- **Kind 1**. It asks `0x004776D0` for the value of sequencer slot `+0x02` (`0x00371F64`) and applies the
  group whose id equals it; with no such group nothing is applied.
- Either way the angles are turned into radians, written to bone `+0x190`–`+0x198` and every bone
  linked through `+0x278`, and rebuilt into the bone's rotation with `0x0046D380` (`0x00371D27`,
  `0x00372087`).
- `0x0046D380(matrix, x, y, z)` looks each angle, in radians, up in the sine table `0x01F004E0` of 32768 entries: the
  index is `angle / 2pi x 32768`, truncated and masked with `0x7FFF`, and the cosine is the entry `0x2000` further
  on, wrapping (`0x0046D39E`-`0x0046D485`).
- With `sx` for the sine of `x` and `cx` for its cosine, `0x0046D380` writes the rows `(cy cz, cy sz, -sy, 0)`,
  `(sx sy cz - cx sz, sx sy sz + cx cz, sx cy, 0)`,
  `(cx sy cz + sx sz, cx sy sz - sx cz, cx cy, 0)` and `(0, 0, 0, 1)` (`0x0046D49F`-`0x0046D550`).
- Here the matrix is the scratch `0x02CA43D0`; the posing code copies its first three rows to bone `+0xC0`-`+0xEC`
  and the bone's `+0x1B0`-`+0x1B8` to `+0xF0`-`+0xF8` (`0x00371D2C`-`0x00371E0D`, the same from `0x0037208C`).
- Switching between the base and town tables saves and restores the affected bones' state through
  the arrays at record `+0x720`.

### skeletonmapping.bin

`0x0036FFF0` reads the file whole into a stack buffer of `(size + 1 + 0xF) & ~0xF` bytes, the file size plus 1,
rounded up to 16 (`lea rax, [rcx + 0xf]`, `and rax, 0xfffffffffffffff0`, `0x00370040`-`0x00370077`). A size of 0
(`0x001D6EE0` also gives 0 for a null handle) returns at once, before the close,
and leaves `0x02AD9E30` and `0x02AD9E38` as they are (`0x0037003A`).

It copies each name (32 bytes, `strncpy`) into a `0x30`-byte record at `[0x02AD9E30]` (count
`0x02AD9E38`, `0x00370086`) with the value array at `+0x28`: it stores n at `+0x20` (`0x003700F6`), allocates n × 4 bytes
with `0x0019C580` (`0x00370102`) and copies the n values (`0x00370120`-`0x0037013B`). No count is checked against the file
size.

`0x00372820` keeps the last record whose name matches the
model at skeleton `+0xB0`. While the render record's add-motion state is 2 and the record has a
partner skeleton, `0x003703A0` builds the skinning matrix of each mapped bone from the partner's bone
(`0x0037065D`–`0x0037078C`).

### highmodelreplace.bin

`0x0037CCC0` reads the file whole into a stack buffer the same way (`0x0037CD08`-`0x0037CD3F`); a size of 0 returns 0 at
once, before the close (`0x0037CD02`).

It counts the records, then fills `0x30`-byte rows at `[0x02ADD940]` (count `0x02ADD938`): model,
b and c at `+0x00`, the pair count at `+0x0C`, replacements from `+0x10` and progress values from
`+0x20`. The table is count × `0x30` bytes from `0x0019C580`, zeroed with `0x00861EC0` (`0x0037CD90`-`0x0037CDA4`), and the
body returns 0 (`0x0037CE59`).

Nothing limits a record to four pairs: a fifth pair's replacement lands on the first progress value at `+0x20`
and its progress value at `+0x30`, past the row (`0x0037CE1E`, `0x0037CE30`). `0x0037CB90` looks a model up; its use is
described with the binding verbs in [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
against the [story progress](../Story-Events-And-Hunts/story-progress.md) word.

### The individual records

| Table | Rows | One row per |
|---|---|---|
| [`add-motion-tables-groups.tsv`](add-motion-tables-groups.tsv) | 382 | group header of a track |
| [`add-motion-tables-records.tsv`](add-motion-tables-records.tsv) | 3,553 | bone record of a group |

| Column | Table | Meaning |
|---|---|---|
| `file`, `track`, `group`, `offset` | both | the `.adm`, the track, the group, and where the item starts in the file |
| `kind`, `angle`, `bone_or_slot` | groups | the track's kind, its angle (`-` for kind 1) and the driving bone or sequencer slot |
| `key_or_angles`, `bytes_0c_17`, `id`, `raw` | groups | the three key floats as hex, bytes `+0x0C` to `+0x17`, the `+0x18` word in decimal, and the whole header |
| `record`, `bone` | records | the position in the group and the bone |
| `angles_bits`, `angles_degrees` | records | the three rotation floats, as stored and in decimal |
| `second_triple_bits` | records | the floats at `+0x10`, which the parser copies and the pose code does not read |

`Database/Tools/catalogues/pose_records.py` writes these tables. Every `.adm` ends exactly at its last record.

## Modding notes

- End every line of `add_motion_list.txt`, the last one included, with CRLF, and end the file with
  that CRLF: the search never stops at the file's end.
- Keep a name, with `_town`, under 20 characters, and a model's file name under 16.
- An `.adm` is parsed only for a listed name; ship the base table, and add `_town` only for a model
  that should look different in towns.
- Every record of a group must name a bone the model has: the bone index is used unchecked.
- Keep the records of every group in the same bone order; the bone tables come from group 0.
- Give a `highmodelreplace.bin` record at most four pairs.

## Related

- [Model oscillators and the pose sequencer](model-oscillators-and-pose-sequencer.md): the slot values kind 1 tracks follow.
- [Model files](model-files-cm-ca.md): the `@FTR` skeleton the bone numbers index.
- [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md): the part attach that binds the tables.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): the replacement lookup.
- [Story progress](../Story-Events-And-Hunts/story-progress.md): the value the replacement thresholds compare with.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x001D6EE0` is called by `0x00210760`; those functions are documented on
  [audio manager](../Sound-And-Music/audio-manager.md).
- Save load settings: `0x0019C580` is called by `0x00866200`; those functions are documented on
  [save file format](../Saving-Loading-And-Settings/save-file-format.md).
