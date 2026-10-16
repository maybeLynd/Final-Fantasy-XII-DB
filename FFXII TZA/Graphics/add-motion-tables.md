---
title: "Add-motion tables: .adm, skeletonmapping.bin and highmodelreplace.bin"
kind: "format"
category: "Graphics"
summary: "The files in ps2data/add_motion: the .adm tables of per-bone rotation keys that bend high-detail character models on top of their motion, with their _town variants, how add_motion_list.txt is read, how a render record is given its two tables and which one applies, the keyed and pose-slot track kinds, plus skeletonmapping.bin (bones that follow a partner skeleton) and highmodelreplace.bin (model replacements by story progress), with the shipped census."
addresses: ["001BDC40", "001BDD20", "001BE1A0", "01F81250", "001BE420", "001BE430", "00863110", "002EDF90", "003714A0", "00377C20", "0017FFB0", "004776D0", "0046D380", "0036FFF0", "02AD9E30", "02AD9E38", "00372820", "003703A0", "0037CCC0", "02ADD940", "02ADD938", "0037CB90"]
---

# Add-motion tables: .adm, skeletonmapping.bin and highmodelreplace.bin

## What the player sees

The high-detail models of the main characters and a few NPCs bend some bones on top of whatever
motion is playing: a joint follows another bone's angle through a set of keyed poses, or a face
switches between posed groups under the control of the pose sequencer. In towns some of these models
use a second, civilian set of tables. One high-detail body moves part of its skeleton with a partner
model's bones, and some models are swapped for others as the story advances.

## Where it comes from

The files are in the archive at `ps2data/add_motion/`. All three readers run once at start-up and
read their files whole:

- `001BDC40`, the registry made by `001BE3E0` (kept at `01F81250`), runs `001BDD20`, which reads
  `./PS2Data/add_motion/add_motion_list.txt` and, for each name, `./PS2Data/add_motion/%s.adm` and
  `./PS2Data/add_motion/%s_town.adm` when present;
- the first boot frame `0022A0B0` runs `0036FFF0` (`./PS2Data/add_motion/SkeletonMapping.bin`) and
  `0037CCC0` (`./PS2Data/add_motion/HighModelReplace.bin`).

## Layouts

### .adm

A flat stream, read in order with no offsets.

```
+0x00  i16  track count
track (8 bytes):
  +0x00  u8   kind: 0 keyed by a bone's angle, 1 chosen by a pose sequencer slot
  +0x01  u8   kind 0: which angle (0, 1 or 2) drives the keys
  +0x02  u16  kind 0: the driving bone; kind 1: the sequencer slot
  +0x04  i16  group count
  +0x06  i16  records per group
  then group count x { 0x1C-byte group header, records per group x 0x1C-byte record }
group header (0x1C):
  +0x00  f32[3]  kind 0: the key, one per angle
  +0x18  u32     kind 1: the group's id
record (0x1C):
  +0x00  i32     bone
  +0x04  f32[3]  rotation angles in degrees
  +0x10  f32[3]  copied by the parser; the pose code does not read them
```

The parser `001BE1A0` keeps a 32-byte record per file (`+0x00` name, `+0x14` track count, `+0x18`
tracks), 16 bytes per track (`+0x00` the u16 at file `+0x02`, `+0x02` records, `+0x04` groups,
`+0x06` kind, `+0x07` angle, `+0x08` groups), `0x28` bytes per group (the header, then the record
array at `+0x20`) and the records as they are.

### skeletonmapping.bin

```
+0x00  i32  record count
record:  char[32] model name, i32 n, then i32[n]: per bone of that model, a partner bone or -1
```

### highmodelreplace.bin

```
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
| `skeletonmapping.bin` | 196 bytes, one record: `hc1006_03`, 39 values; bones 20–29 follow 27, 28, 29, 27, 28, 29, 30, 27, 28, 29; bones 31–38 follow 33; the rest −1 |
| `highmodelreplace.bin` | 540 bytes, 22 records; one pair in 21, two in 1; b and c −1 in 18, 1 and 0 in 4; a lower-case `c`, `n` or `s` id maps to the upper-case letter's id; one replacement waits for progress 1570 |

## Loader behaviour

### add_motion_list.txt and .adm

- `001BDD20` reads the list into a stack buffer of the file size plus 1, rounded up to 16
  (`001BDDBA`–`001BDDDE`), and cuts it at each CRLF with `strstr`; a name is taken only when a CRLF
  follows it. Nothing writes a zero byte after the text, so the search after the last CRLF runs past
  the file's last byte into uninitialised stack bytes, up to the first zero.
- The shipped list therefore yields 22 names only while those stack bytes hold no CRLF before a zero.
  When they do, the unterminated `hs0020_01` and the bytes after it become a 23rd name.
- For each name it parses `<name>.adm`, copies the name over the record's `+0x00`, and then parses
  `<name>_town.adm` and names it `<name>_town` with `sprintf`. Both go into the registry's list.
- The name is written over the parsed record, whose track count sits at `+0x14`: a name of 20
  characters or more, `_town` included, overwrites the count and the track pointer.
- `001BE1A0` trusts every count: nothing is checked against the file size, and the sizes are
  multiplied with overflow saturating to all ones before allocation.

### Which table a model uses

- `002EDF90(record, request, resource)` keeps a state at render record `+0x6C8` (0 unbound, 1 and 2
  bound, 3 and 4 released). Request 2 on an unbound record runs `00863110`; request 0 releases, and 1
  or 2 restores a released state. Its caller is `002E3110`, the part attach of the
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- `00863110` takes the file name of the resource between the last backslash and the first dot into
  a 16-byte buffer and calls `001BE430`, which stores the record with that name at `+0x6E8` and the one
  named `<name>_town` at `+0x6F0`.
- `003714A0`, run for every skeleton while its pose is composed, uses `+0x6F0` when it is set and
  bit 15 of the current field's word in the table at `02ADD100` is set (`00377C20`); the registry's
  `+0x20` (`0017FFB0`) forces the town table with 1 and the base table with 2.

### Applying a track

`003714A0` builds two tables per skeleton bone, from group 0's records: the track and the record that
name that bone. Then for each track:

- **Kind 0** (needs two groups or more). The driving bone is looked up in the skeleton that the posed
  skeleton's `+0x0C` names. It takes that bone's angle `+0x190 + 4 × angle` and
  the same angle of the bone's matrix at `+0x230` (`003719F7`–`00371A4A`) and uses their difference
  in degrees; `00180060` / `00180090` can replace it with a set value.
- Kind 0 then finds the pair of groups
  whose keys hold the value and interpolates every record between them, extending past the first and
  last keys.
- **Kind 1**. It asks `004776D0` for the value of sequencer slot `+0x02` (`00371F64`) and applies the
  group whose id equals it; with no such group nothing is applied.
- Either way the angles are turned into radians, written to bone `+0x190`–`+0x198` and every bone
  linked through `+0x278`, and rebuilt into the bone's rotation with `0046D380` (`00371D27`,
  `00372087`).
- Switching between the base and town tables saves and restores the affected bones' state through
  the arrays at record `+0x720`.

### skeletonmapping.bin

`0036FFF0` copies each name (32 bytes, `strncpy`) into a `0x30`-byte record at `[02AD9E30]` (count
`02AD9E38`) with the value array at `+0x28`. `00372820` keeps the last record whose name matches the
model at skeleton `+0xB0`. While the render record's add-motion state is 2 and the record has a
partner skeleton, `003703A0` builds the skinning matrix of each mapped bone from the partner's bone
(`0037065D`–`0037078C`).

### highmodelreplace.bin

`0037CCC0` counts the records, then fills `0x30`-byte rows at `[02ADD940]` (count `02ADD938`): model,
b and c at `+0x00`, the pair count at `+0x0C`, replacements from `+0x10` and progress values from
`+0x20`. Nothing limits a record to four pairs. `0037CB90` looks a model up; its use is described with
the binding verbs in [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
against the [story progress](../Story-Events-And-Hunts/story-progress.md) word.

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
