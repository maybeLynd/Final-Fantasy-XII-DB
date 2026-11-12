---
title: "EBP camera tables: the CML1 shot list and the CAM7 shots a script's camera verbs play"
kind: "format"
category: "EBP script files"
addresses: "0x0032FA10, 0x0032FAC0, 0x002561C0, 0x003DA1F0, 0x0032F3D0, 0x005C5230, 0x00256530, 0x002572E0, 0x003DA400, 0x003DA330, 0x003DA300, 0x00258350, 0x00255410, 0x002554E0, 0x003CC5F0, 0x003CC740, 0x003CC890, 0x0032ED80, 0x02092800, 0x022C6D58, 0x022C6D80, 0x00258190, 0x002ED430, 0x002E7F10, 0x002ED130, 0x002EA890"
---

## What the player sees

The directed camera of a cutscene, and of a field map that frames a moment such as a door
opening, is authored as named shots: where the camera starts, where it looks, how it swings or
cranes to the next pose and how long that takes. Section 9 holds the shots and section 8 the list
of rows a script's camera verbs pick from. 296 of the 345 event scripts and 127 of the 769 field
map scripts in a language tree carry them; a map without them keeps the ordinary follow camera.

A shot can also tie its camera position or its look-at point to an actor of the scene, or to one joint of that actor's
model, so the camera follows that character.

## Where it comes from

Sections 8 and 9 are slots 8 and 9 of the `.ebp` directory
([EBP script container](ebp-script-container.md)). The directory walker `0x003304A0` dispatches
slot 9 first (`0x0033058E`) and slot 8 after it (`0x003305A9`); each handler takes the manager index
from the low four bits of its argument.

| Section | Handler | Steps | Pending bit |
|---|---|---|---|
| 9, CAM7 | `0x0032FAC0` | stores the section at `0x022C6D58[manager]`, clears the four camera channels (`0x002566E0(manager, 0..3)`), runs the loader `0x002561C0`, and only when it returns non-zero sets manager record `+0xE0` (`0x0026CE20`) | `0x80` (`0x0032FB28`) |
| 8, CML1 | `0x0032FA10` | stores the section at `0x022C6D80[manager]`, sets manager record `+0xD8` (`0x0026CE00`), and runs `0x003DA1F0` when `+0xE0` is set | `0x100` (`0x0032FA6C`) |

The teardown `0x0032ED80` runs `0x002561A0` and the channel clear for CAM7, then clears both globals
and both record fields (`0x0032EFC4`, `0x0032F00C`); the free beside each clear is gated on
`0x005C5230(5)`, which returns 0. The manager record and the camera channel entries the verbs bind
are on [actor managers](../Characters-And-Objects/actor-managers.md).

## Layouts

All multi-byte fields are little-endian.

All offsets are from the section start unless a record is named.

CML1 (section 8):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "CML1"; never compared |
| `+0x04` | `u32` | count | rows |
| `+0x08` | `u32[2]` | - | 0; not read |
| `+0x10` | `u8[count][16]` | rows | one 16-byte row per entry, as below; then the names, NUL-terminated, and zero fill to `0x40` |

Row (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | nameOffset | name, from the section start |
| `+0x04` | `i32` | camera | CAM7 record number; -1 when the row names no camera |
| `+0x08` | `u32` | - | zeroed at load |
| `+0x0C` | `u32` | - | low byte zeroed at load |

CAM7 (section 9):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `char[4]` | magic | "CAM7"; anything else and nothing is bound |
| `+0x04` | `u32` | cameras | shot records |
| `+0x08` | `u32` | countB | ease curves |
| `+0x0C` | `u32` | countC | paths |
| `+0x10` | `u32[3]` | - | 0; not read |
| `+0x1C` | `u32` | first | first shot record, from the section start |

```
then the shot records, the ease curves and the paths, back to back
```

Shot record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | - | 0 |
| `+0x04` | `u32` | length | to the next record |
| `+0x08` | `char[24]` | name | copied with strncpy(…, 24) |
| `+0x20` | `u32` | attach | attachment word (`0x002572E0`) |
| `+0x24` | `u16` | eyeJoint | joint for eye attach modes 1 and 2 |
| `+0x26` | `u16` | targetJoint | joint for target attach modes 1 and 2 |
| `+0x28` | `commands` |  | keys and segments, then `0xFF` and three pad bytes |

Key (type 1, `0x40` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | value 1 |
| `+0x04` | `f32[3]` | eye |  |
| `+0x14` | `f32[3]` | target |  |
| `+0x24` | `f32` | angle | to the view's `+0x20` |
| `+0x28` | `f32` | fov | degrees |
| `+0x2C` | `f32[2]` | follow | path-follow values |
| `+0x38` | `f32` | followLead | path-follow value |

```
(+0x10, +0x20, +0x34, +0x3C not read)
```

Segment (type 2, `0x2C` bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` |  | value 2 |
| `+0x04` | `u16[13]` | timing | bit `0x8000` set: ease curve (mask `0x7FFF`); else frames |
| `+0x1E` | `u16` | eyePath | bit `0x8000` set: path (mask `0x3FFF`); bit `0x4000`: progress is a distance |
| `+0x20` | `u16` | targetPath | as eyePath |
| `+0x22` | `u16` | duration | frames |
| `+0x24` | `u8` | kind | 0-6; see Playing a shot |
| `+0x25` | `u8` | absolute | non-zero: the path offsets replace the pose |

Ease curve (array B):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | length | `0x18` + `0x24` * keys |
| `+0x04` | `u32` | keys |  |
| `+0x08` | `f32` | start | time; at or before it the value is `+0x0C` |
| `+0x0C` | `f32` | startValue |  |
| `+0x10` | `f32` | end | time; the normaliser |
| `+0x14` | `f32` | endValue | at or after end, and with no keys |
| `+0x18` | `...` |  | key[keys], `0x24` bytes: `+0x10` a, `+0x14` b, `+0x18` c, `+0x1C` d, `+0x20` span |

Path (array C):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | length | `0x20` + `0x38` * segments + 8 * arcs |
| `+0x04` | `u16` | segments |  |
| `+0x06` | `u16` | arcs |  |
| `+0x08` | `f32[3]` | start | at parameter 0 or below |
| `+0x14` | `f32[3]` | end | at parameter 1 or above |
| `+0x20` | `...` |  | segment[segments], `0x38` bytes: x a b c d, y a b c d, z a b c d, `+0x30` span |

```
then arc[arcs]: f32 distance, f32 parameter
```

Each shot becomes a 0x40-byte entry in `[0x02092810 + manager * 0xBB0]`: `+0x00` the name, `+0x18`
the address of record `+0x28`, `+0x20` and `+0x28` the eye and target actors, `+0x30` and `+0x32`
the joint words, `+0x34`-`+0x3D` the attachment bits.

## Shipped data

Every count is per language tree; the CAM7 sections are byte-identical in all nine trees.

| Fact | Value |
|---|---|
| files | 423, all carrying both sections; neither section appears without the other |
| shots | 3,942; 1 to 69 per file |
| CML1 rows | 3,933; 1 to 69 per file; in 284 files row `k` names shot `k` |
| rows naming no shot (-1) | 2 |
| row count differs from shot count | 11 files, exactly the 11 that hold two shots with one name; in each, the row for that name points at the later shot |
| row names | every row's name equals the name of the shot it points at |
| commands | 7,614 keys, 3,654 segments; streams `K S K E` 3,421, `K E` 421, `K S K S K E` 59, one stream starting with a segment |
| record lengths | 108 (421), 216 (3,421), 324 (59), 432 (20), 388 (11), 280 (3), 560 (2), and 152, 496, 540, 648 and 1,296 once each |
| segment kinds | 0: 3,406; 1: 116; 2: 57; 3: 67; 4: 8; 5 and 6 unused |
| names | at most 23 bytes, all NUL-terminated |
| attachment word `0x80008000` | 3,730 shots (no attachment) |
| eye attached | 180 shots: mode 0 83, mode 1 31, mode 2 66; turn 152, hold height 7, hold ground 5, bit `0x200` 34, bit `0x400` 34 |
| target attached | 181 shots: mode 0 83, mode 1 32, mode 2 66; turn 153, hold height 7, hold ground 1 |
| attach mode 3 | unused |
| eye bits under mask `0x7E00` set with eye actor 0 | 11 shots; never read |
| ease curves, paths | 15,350 and 1,682; each used by exactly one segment word; every curve's spans sum to 1.0 |
| layout checks | every stream ends at its record length, the three arrays end on zero padding, and `first` is `0x20` |

### Every shot, shake and call

`Database/Tools/catalogues/camera_shots.py` reads sections 8 to 11 of the `us` scripts and their code and writes ten
tables. Sections 8 to 11 are byte-identical in all nine trees, so the rows hold for every language. They cover the
script sections only. A camera stored in a map's art files is a different source and has no row here.

| Table | Rows | One row per |
|---|---|---|
| [`ebp-camera-rows.tsv`](ebp-camera-rows.tsv) | 4,233 | row of a section 8 or section 10 list |
| [`ebp-camera-shots.tsv`](ebp-camera-shots.tsv) | 3,942 | shot, with its attachment and timing |
| [`ebp-camera-keys.tsv`](ebp-camera-keys.tsv) | 7,614 | key of a shot |
| [`ebp-camera-segments.tsv`](ebp-camera-segments.tsv) | 3,654 | segment of a shot |
| [`ebp-camera-curves.tsv`](ebp-camera-curves.tsv) | 17,189 | ease curve of section 9 (15,350) or shake curve of section 11 (1,839) |
| [`ebp-camera-curve-keys.tsv`](ebp-camera-curve-keys.tsv) | 37,283 | key of a curve |
| [`ebp-camera-paths.tsv`](ebp-camera-paths.tsv) | 1,682 | path, with its arc table |
| [`ebp-camera-path-segments.tsv`](ebp-camera-path-segments.tsv) | 7,948 | segment of a path |
| [`ebp-camera-shakes.tsv`](ebp-camera-shakes.tsv) | 299 | shake |
| [`ebp-camera-calls.tsv`](ebp-camera-calls.tsv) | 4,660 | script call that names a row |

A script names a row, and the row picks a record, so the tables keep the two apart. In the 11 files with two shots of
one name, 22 shots have `shots_with_name` 2. In each pair the row points at the later shot, and the earlier one has
`rows` `-` and 0 calls. Those 11 are the only records no call names: every other shot, all 299 shakes and all 4,233
rows have at least one. Three rows hold -1, two in the shot lists and one in the shake lists.

The row argument is a constant of this form, and the verbs read only the row part (`0x0034F976`, `0x0034F32B`,
`0x0034EDE9`, `0x00349FF3`, `0x00349776`):

```python
reference = 0x02000000 + row        camera verbs, and one shake call in frs_b0201
reference = 0x0D000000 + row        the other 327 shake calls
```

| Verb | Calls | List | Row argument | Channel argument |
|---|---|---|---|---|
| `camerastart_7e` | 3,833 | shot | second of two | first |
| `camerastart` | 450 | shot | only | none, channel 0 |
| `camerastart_7d` | 39 | shot | second of three | first |
| `camerahitcheck` | 8 | shot | only | none |
| `behindtoeventcamera` | 2 | shot | first of four | none |
| `camerashakestart_1a3` | 328 | shake | second of two | first |

The calls come from the instruction stream, and the argument text and the blocks come from the decompiled listing of
the same file. In every function the two list the same verbs in the same order. A call's `conditions` are the blocks
around it in its function. A function runs when a request is filed for it
([script requests](../Scripts-And-Script-Commands/script-requests.md)): by a REQ-family verb in another function, by
the engine through `0x003DBB60`, or from the start list (`0x00266C50`).

In 22 calls the script's file has no section 8, so `row_name` and `record` are `-`: seven in `evt_t0005` and 15 in
six `global` map scripts. `0x003DA400` returns at once when the manager's list is null (`0x003DA426`).

An attachment names an actor by number. `0x00257AD0` counts the manager's records whose class is 3 and takes the one at
the number less one (`0x00257355`, `0x00257B0A`). Sequences 5, 6 and 7 have class 3 (`0x01E0C328`), and a directory entry's
type word is its sequence. In all 1,114 scripts with code the directory is sorted by that word and the header's
per-sequence counts equal it, so record `i` is directory entry `i`, and the name in `eye_actor_name` follows.

For manager 4 the number is looked up in the manager whose index is at `0x02096504` (`0x0025737C`, `0x0025738A`). The
tables give the name from the script's own directory.

`eye_models` and `target_models` are the files named by bind verbs in that actor's own code, from
[`ebp-actor-manifest-calls.tsv`](ebp-actor-manifest-calls.tsv). `-` means that actor's code holds no bind verb.
All 132 sides with attach mode 2 have one such file, and in all 132 the joint is the key of an `@FTR` node of that
file, whose number is in `eye_joint_node` or `target_joint_node`. Mode 1 takes another lookup and has `-` there.

### Columns of the ten tables

| column | what it holds |
|---|---|
| all: `script` | the script's path under `plan_master/us` |
| rows, shots, shakes, calls: `kind` | `zone` or `event` |
| rows: `list`, `row` | `shot` for section 8 or `shake` for section 10, and the row's position |
| rows: `name_offset`, `name` | the name's offset from the section start in hexadecimal, and the name |
| rows: `record`, `record_name`, `names_match` | the stored record number, -1 for none, that record's name, and whether the two names are equal |
| rows: `records_with_name` | how many records of the section hold the row's name |
| rows: `word_08`, `word_0c` | the row's two words as stored, in hexadecimal |
| rows, shots, shakes: `calls` | the calls that name that row, or that name a row picking that record |
| shots: `shot`, `name`, `shots_with_name`, `rows` | the record number, its name, how many shots hold that name, and the rows that pick it |
| shots: `word_00`, `length`, `attach` | the first word and the attachment word in hexadecimal, and the record length |
| shots: `eye_actor`, `target_actor` | the actor number from `attach`, 0 for no actor; the side's other columns are then `-` |
| shots: `eye_actor_name`, `target_actor_name` | the directory name of that actor |
| shots: `eye_mode`, `target_mode` | the attach mode: 0 the actor's position, 1 and 2 a joint |
| shots: `eye_turn`, `eye_hold_height`, `eye_hold_ground` and the same for `target_` | the three attachment flags, `yes` or `no` |
| shots: `eye_angle_from_joint`, `eye_fov_from_joint` | flags `0x200` and `0x400` of `attach` |
| shots: `eye_joint`, `target_joint` | the stored joint words in hexadecimal, read for modes 1 and 2 |
| shots: `stream`, `keys`, `segments`, `frames` | the commands in order (`K`, `S`, `E`), the counts, and the sum of the segment durations |
| keys, segments: `shot`, `position`, `offset` | the shot, the command's place in its stream, and its offset from the record start in hexadecimal |
| keys: `key`, `eye`, `target`, `angle`, `fov` | the key's place among the shot's keys, the two points as `x y z`, and the two values |
| keys: `follow_a`, `follow_b`, `follow_lead` | the three path-follow values |
| keys, segments: `raw` | all the command's bytes, in hexadecimal |
| segments: `segment`, `duration`, `kind`, `absolute` | the segment's place among the shot's segments and the stored values |
| segments: `timing_raw`, `timing` | the 13 words, as stored and read: `c` and a curve number, or `f` and a frame count |
| segments: `eye_path_raw`, `eye_path`, `target_path_raw`, `target_path` | the words as stored, and the path number, `distance` when progress is a distance, `-` for no path |
| curves, curve-keys: `section`, `curve` | 9 or 11, and the curve's number in its section |
| curves: `length`, `keys`, `start`, `start_value`, `end`, `end_value` | the stored header |
| curves, paths: `used_by` | the segment word or shake slot that names it |
| curve-keys: `key`, `first_16_bytes`, `a`, `b`, `c`, `d`, `span` | the key's place, its first 16 bytes in hexadecimal, and the five values `0x003CC5F0` reads |
| paths: `path`, `length`, `word_02`, `segments`, `arcs` | the path number and the stored header, `word_02` in hexadecimal |
| paths: `start`, `end`, `arc_table` | the two points as `x y z`, and each arc as `distance:parameter` |
| path-segments: `segment`, `x_a` to `z_d`, `span`, `word_34` | the segment's place, the three cubics, the span, and its last word in hexadecimal |
| shakes: `shake`, `name`, `shakes_with_name`, `rows` | as for shots |
| shakes: `duration`, `word_1c`, `curve_slots`, `curves` | the duration, the next word in hexadecimal, the 32 slots as stored, and the slots in use |
| calls: `actor`, `actor_index`, `function`, `symlink_actors` | where the call is; the index is the actor's place in the directory; `symlink_actors` are the actors that run the same code |
| calls: `code_offset`, `verb`, `verb_id`, `arguments`, `channel` | the call's offset in the code section in hexadecimal, the verb, its argument text, and the channel argument, `-` for none |
| calls: `list`, `reference`, `row`, `row_name` | the list named, the row argument in hexadecimal, the row, and the row's name |
| calls: `record`, `record_name` | what the row picks, -1 for no record, `-` when the file has no such list |
| calls: `conditions` | the enclosing blocks, outermost first, `-` for none |

Floats are written with nine significant digits, which keeps each stored value exact.

## Loader behaviour

### CAM7 at load

`0x002561C0(section, manager)`:

1. Returns 0 unless `+0x00` is `CAM7` (`0x002561C8`); the handler then binds nothing.
2. Stores the section at `0x02092808 + manager * 0xBB0` (`0x00256205`).
3. Returns 1 at once when `cameras` is 0 (manager below 5) (`0x00256219`). For a manager of 5 or above
   every count is taken as -1, so the three walks below are skipped (`0x0025620E`, `0x002562E8`, `0x0025633B`).
4. Under arena 5 (`0x0036C1D0(5, 9)` at `0x00256231`, `0x0036C140` at `0x00256387`), allocates `cameras * 0x40`
   bytes for the shot entries at `0x02092810` (`0x0025623B`, `0x00256240`).
5. For each shot, from `section + first`: copies 24 name bytes with `strncpy` (`0x00256276`), so a
   24-byte name has no terminator; stores the command stream address, zeroes `+0x20` and `+0x28`,
   copies the joint words, and steps by `length`.
6. Builds pointer arrays for the ease curves (stepping by the `u32` at `+0`) and the paths
   (stepping by the `u16` at `+0`) at `0x02092818` and `0x02092820`, allocated at `countB * 8` and
   `countC * 8` bytes (`0x002562FE`, `0x00256351`), and returns 1 (`0x00256396`).

Nothing is compared with the section's length.

`0x002572E0(manager)`, run by `0x0026CE60` once `+0xD8` and `+0xE0` are both set, loads the CAM7 section pointer
`[0x02092808 + manager × 0xBB0]` and the section's row offset `+0x1C` (`0x00257304`, `0x00257309`) before any test. It
then does nothing for a manager of 5 or above, a null section pointer or a shot count `+0x04` of 0 or below
(`0x0025730F`-`0x0025732B`), so a null pointer is read at `0x00257309` before its test.

For manager 4, `0x00257AD0` looks the actor up
in the manager whose index is held at `0x02096504` (`0x0025737C`, `0x00257466`), and only while `0x002671F0` of that
manager returns non-zero; otherwise that side's actor is 0 and its bits are still decoded (`0x00257377`,
`0x0025739D`, `0x00257460`, `0x00257487`).

For each shot it stores the eye and target actors at entry `+0x20` and `+0x28` and the bits below in the entry
bytes `+0x34`-`+0x3D` (`0x002573A9`-`0x00257411`, `0x00257493`-`0x002574D7`), stepping by `length` (`0x002574E7`). It
decodes each shot's `attach` word:

| Field | Eye | Target |
|---|---|---|
| actor | mask `0x1FF`: number n, the n-th class-3 record of the manager (`0x00257AD0`, `0x00358960`), 0 for no actor | mask `0x1FF0000` |
| attach mode | mask `0x6000` | mask `0x60000000` |
| turn with the actor | `0x8000` | `0x80000000` |
| hold height | `0x800` | `0x8000000` |
| hold ground position | `0x1000` | `0x10000000` |
| angle and fov from the joint | `0x200`, `0x400` | - |

### CML1 at load

`0x003DA1F0(record)`, given the manager record from `0x00263FF0` (`0x0032FA4A`-`0x0032FA5C`), sets record `+0x18` and
`+0x1A` to -1 and the four channel entries to idle: word `+0x118 + 0x18 x k` to 0 and word `+0x11A + 0x18 x k`
to -1 (`0x003DA204`-`0x003DA247`). It takes section 8 from record `+0xD8` (`0x003DA1FA`) and stops when that is null
(`0x003DA251`); for a `count` above 0 (`0x003DA262`) it then, for each row, zeroes `+0x08` and the low byte of
`+0x0C` (`0x003DA292`, `0x003DA296`).

Its name lookup `0x00256530(manager, name)`, with the manager from record `+0x28`, and the store of its result
in row `+0x04` (`0x003DA284`-`0x003DA28F`) run only when `0x0032F3D0(1)` returns non-zero (`0x003DA282`), and kind 1
ends in `0x005C5230(5)`, which is `xor eax, eax`: the lookup never runs, the authored `camera` column is
used as shipped, and no name is ever compared.

`0x0032F3D0(kind)` reads only its first argument (`0x0032F3D6`). It returns 0 when the byte `0x02B62DAB` read by
`0x00408B30` is 1 or the byte `0x02B62DA8` read by `0x00408B10` is 3 (`0x0032F3D8`-`0x0032F3EA`). Otherwise kinds 0, 1
and 2 return 1 only when `0x005C5230` (given 4, 5 and 14) returns non-zero, which it never does, and any other
kind returns 1 (`0x0032F3EC`-`0x0032F414`).

`0x00256530(manager, name)` returns -1 for a manager of 5 or above or one without a CAM7 section (`0x00256539`,
`0x00256560`). Otherwise it returns the index of the first shot whose entry name matches `name` in its first 23
bytes (`strncmp` at `0x00256594`), and -1 when no shot matches (`0x002565A4`).

### Who reads a row

Each reader checks the row number against `count` and takes row `+0x04` at `+0x14 + row * 0x10`:

| Verb | Handler | Reader | Does |
|---|---|---|---|
| `camerastart_7d`, `camerastart_7e` | `0x0034F2F0`, `0x0034F930` | `0x003DA400` (`0x003DA456`) | binds the shot to a camera channel |
| `camerahitcheck`, `camerahitcheck_33c` | `0x0034EDB0`, `0x0034E9B0` | `0x003DA330` (`0x003DA35E`) | runs the shot on a scratch player and reports a hit (`0x002567E0`, a tail jump at `0x003DA363` with the manager from record `+0x28` and the third argument, or 2 when that is negative, `0x003DA349`-`0x003DA354`); returns 0 when the record has no section 8 or the row is negative or not below `count` (`0x003DA33D`-`0x003DA347`) |
| `behindtoeventcamera` | `0x00349FA0` | `0x003DA300` (`0x003DA31F`) | starts the move to the shot (`0x00255C50`) |

### Playing a shot

`0x00258350` walks the stream from the channel's position each frame:

- a key copies eye, target, angle, fov and the three follow values into the pose, is remembered
  as the segment's start, and the walk continues;
- a segment adds the frame time to its clock, computes its 13 progresses (`0x00255410`: an ease
  curve through `0x003CC5F0`, else clock / frames), its two path offsets (`0x002554E0`), and the
  pose between the remembered key and the key after it by `kind`; once the clock reaches
  `duration` the walk moves on, carrying the rest of the clock;
- `0xFF` marks the channel finished.

The eye is the eye path offset plus the pose's eye and the target likewise, unless `absolute`
is set; both go through the attachment transforms and into the view at `0x02096370`, the fov as
`fov * π / 180`. The eye is interpolated by `0x00257B50`, or by `0x00257BF0` for kind 1 and `0x00257D10` for
kind 2; the target by `0x00258090`, or by `0x00257E40` for kind 3 and `0x00257F60` for kind 4. Kinds 5
and 6 replace both with the path-follow routines `0x00256960` and `0x00256CA0`.

`0x00255410(segment, channel, curves)` reads the clock at channel `+0x08`. For timing word `k` with bit
`0x8000` set it stores the value of curve `word & 0x7FFF` at channel `+0x128 + 4 * k` and the curve's return
value in the byte `+0x15C + k` (`0x0025546A`, `0x0025546F`); for a frame count it stores `clock / frames` there
and, in the byte, 1 while `frames >= clock` (`0x0025547D`-`0x0025549B`).

`0x002554E0(segment, channel, paths)` takes `eyePath` and then `targetPath`. A word without bit `0x8000` gives a
zero offset (`0x0025552F`, `0x00255532`); otherwise path `word & 0x3FFF` is evaluated at progress 8 (eye, channel
`+0x148`) or 9 (target, `+0x14C`) by `0x003CC710` with bit `0x4000` and by `0x003CC6C0` without it
(`0x0025553F`-`0x00255560`), into channel `+0xF0` (eye) or `+0x100` (target), whose fourth float is set to 1.0
(`0x00255565`).

`0x003CC5F0(curve, time, out)` writes the curve's value through `out` and returns a flag. With no keys, or with
`time` past `end`, it writes `endValue` and returns 0 (`0x003CC5FC`, `0x003CC636`); at or before `start` it writes
`startValue` and at exactly `end` it writes `endValue`, returning 1 (`0x003CC60F`, `0x003CC627`).

Otherwise `0x003CC5F0` finds the curve key by summing spans until they pass `time / end` and writes
`a·s³ + b·s² + c·s + d`, `s` the position inside that key, `(time / end - spans before) / span`
(`0x003CC650`-`0x003CC6AE`), and returns 1.

`0x003CC890(path, distance)` turns a distance into a parameter by a binary search of the arcs: 0 below the
first arc's distance and 1.0 above the last (`0x003CC8A9`, `0x003CC8BC`). Between them it returns
`p0 + (d - d0) / (d1 - d0) * (p1 - p0)` from the two arcs around `d`, and `p0` itself when their distances or
parameters are equal (`0x003CC905`-`0x003CC966`).

`0x003CC740(path, t, out)` finds the segment by its span and writes the three cubics to `out` (`0x003CC821`,
`0x003CC850`, `0x003CC87A`): `start` for `t` at or below 0 and `end` for `t` at or above 1.0 (`0x003CC74C`,
`0x003CC76A`), and `end` also when the spans run out before passing `t` (`0x003CC7BE`). Inside a segment the
position is `(t - spans before) / span` (`0x003CC7D3`, `0x003CC7DE`). A plain path word runs the whole path as the
progress goes from 0 to 1 (`0x003CC6C0`); with bit `0x4000` the progress is a distance (`0x003CC710`).

### Attaching the eye and target

Before it walks the stream, `0x00258350` builds the two attachment transforms, the eye's at channel
`+0x190` and the target's at `+0x1D0`. A side whose entry has no actor (`+0x20`, `+0x28`), or whose
manager fails `0x002671F0`, gets the identity (`0x00203170`). Otherwise `0x00258190(attach, matrix,
&fovAdd, &angleSub)` builds it from the side's bits, and the channel byte `+0x189` (eye) or `+0x18A`
(target) is set afterwards, marking the side as attached.

`0x00258190`'s first argument points at the side's fields: the actor at `+0x00`, the dwords for "turn with the
actor" `+0x08`, the attach mode `+0x0C`, "attached" `+0x14`, "hold height" `+0x18`, "hold ground position"
`+0x1C` and the two that select `angleSub` (`+0x20`) and `fovAdd` (`+0x24`), and the joint word `+0x10`
(`0x002581BB`-`0x002582D1`). It:

1. keeps the matrix's old position (`+0x30`, `+0x34`, `+0x38`);
2. sets the rotation: the identity, or with "turn with the actor" a turn about the vertical by the
   actor's heading (`0x00265200`, `0x003CC480(0, heading, 0, matrix)`);
3. takes the point by the attach mode: 0, the actor's position (`0x00265020`); 1, the position of
   joint `eyeJoint` or `targetJoint` from `0x002E7F10`; 2, the same from `0x002ED430`; the joint call's
   return value is not tested (`0x0025823B`), and mode 3 makes no call and keeps whatever the stack
   slots `[rsp+0x20]`-`[rsp+0x28]` hold (`0x0025820F`);
4. writes the point as the position, except that "hold height" keeps the old y and "hold ground
   position" keeps the old x and z once the side is attached (`0x00258278`-`0x002582C0`);
5. with bit `0x200` or bit `0x400` of the word, finds the joint's node (`0x002ED130`) and reads the node's record
   (`0x002EA890`): bit `0x200` puts its `+0x198` in `angleSub`, bit `0x400` its `+0x194` in `fovAdd`. A node of
   `0xFFFF` or a null record leaves both untouched (`0x002582E5`, `0x002582F5`).

The view's angle is then the pose's angle minus `angleSub`, and its fov `fov * π / 180 + fovAdd`.

The two joint modes look in different places:

- `0x002E7F10(actor, joint, 0, out)` takes the actor's model record (`[0x022C6F28] + slot × 0x740`, the table
  whose address is held at `0x022C6F28` (`0x002E7F3E`), the slot the word at `[actor + 0xC0]`) and hands it to
  `0x00426770`, which asks that model and the one
  chained at its `+0x08` for the joint's matrix (`0x00421E20`); it returns 1 when one answered.
- `0x002E7F10` returns 0 for a null actor, a null `[actor + 0xC0]`, a slot dword of -1 or slot word of
  `0xFFFF`, a null model record or a record whose `+0x284` is 0 (`0x002E7F14`-`0x002E7F4E`), and when
  `0x00426770` returns null (`0x002E7F58`).
- `0x002ED430(actor, joint, 0, out)` checks the same slot and passes on to `0x003A6DF0`, which finds the
  model that holds the joint among its flagged nodes (`0x00426650`, `0x00421D70`) and reads the node's
  matrix (`0x00422050`); it returns whether that gave a result. It returns 0 for a null actor, a null
  `[actor + 0xC0]` or a slot dword of -1 (`0x002ED434`-`0x002ED448`), and hands `0x003A6DF0` the slot word, not
  the actor (`0x002ED44A`, `0x002ED44D`).
- `0x002ED130(actor, joint)` runs the flagged-node search on the actor's own model: a model whose
  `+0x9C` is 2 (`0x00372800`) is searched for a node with that id and bit `0x100` of its `+0x04` set
  (`0x003737C0`). `0x002EA890(actor, index)` returns record `index` (`0x290` bytes each) of the
  model's node records at `[+0x84]`.
- `0x002ED130` returns `0xFFFF` on every check that makes `0x002E7F10` return 0 before its call
  (`0x002ED133`-`0x002ED170`); otherwise it tail-jumps to `0x00421D70` with the model record and the joint
  (`0x002ED16A`).

The word's bits beside an actor field of 0 are never read: such a side keeps the identity.

## Modding notes

- The `camera` column of section 8 decides which shot plays; renaming a shot changes nothing.
- Keep section 9's magic; a wrong one leaves the manager without shots while section 8 still binds.
- Keep shot names under 24 bytes.
- A record's `length` must equal `0x28` + `0x40` per key + `0x2C` per segment + 4; nothing checks it.
- A segment blends from the last key the walk stored at the channel's `+0xE0`; start a stream
  with a key unless the shot follows another on the same channel.
- Ease-curve spans must sum to 1.0, and every timing and path word must name an existing curve or
  path; neither is bounds-checked.
- Keep the three arrays in order: their only boundaries are the lengths.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches these sections.
- [EBP camera shake](ebp-camera-shake.md): the CML1 and SHK1 pair that shakes these shots.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the record fields and the camera channel binds.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the camera verbs.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Input: `0x00263FF0` is called by `0x00226BE0`, `0x002E09A0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [frame update order](../Engine-Core/frame-update-order.md).
