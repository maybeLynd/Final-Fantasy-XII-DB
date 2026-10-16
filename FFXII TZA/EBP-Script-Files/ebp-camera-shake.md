---
title: "EBP camera shake: the CML1 shake list and the SHK1 curves that make a scripted camera tremble"
kind: "format"
category: "EBP script files"
summary: "Sections 10 and 11 of an .ebp script: the CML1 list whose rows the shake verbs name and the SHK1 bank of shakes and curves it indexes; how both are bound to an actor manager and what the load does to them, how a shake's 32 curve slots drive eight random sine oscillators and what each output moves on screen, the shipped banks in all nine language trees, and the rules an edit must follow."
addresses: ["003316B0", "00331610", "0037DA90", "0037DA70", "003DD120", "003DD230", "003DCFB0", "0037D1F0", "0037D130", "0037DD50", "0037D4C0", "00382B70", "003820C0", "003CC5F0", "02ADD980", "022C6DD0", "022C6DF8"]
---

# EBP camera shake: the CML1 shake list and the SHK1 curves that make a scripted camera tremble

## What the player sees

When a summon lands, a blade rings off stone or the ground shudders in a cutscene, the camera
jolts and trembles for a set time and then settles. Each tremble is an authored shake in the
scene's section 11, with working names such as `シェイク01`, `振動02` and `手ブレ01`; section 10 is
the list of rows the script's shake verbs pick from. The motion is random within authored limits,
so the same shake never moves the view twice in exactly the same way.

## Where it comes from

Sections 10 and 11 are slots 10 and 11 of the `.ebp` directory
([EBP script container](ebp-script-container.md)). The directory walker `003304A0` dispatches
slot 11 first (`003305C4`) and slot 10 after it (`003305DF`); each handler takes the manager index
from the low four bits of its argument.

| Section | Handler | Steps | Pending bit |
|---|---|---|---|
| 11, SHK1 | `003316B0` | stores the section at `022C6DD0[manager]` and in manager record `+0xF8` (`0026D3C0`), clears the four shake entries (`0037DC30(manager, 0..3)`), runs the loader `0037DA90` | 10 |
| 10, CML1 | `00331610` | stores the section at `022C6DF8[manager]` and in record `+0xF0` (`0026D3A0`), runs `003DD120` on the record | 11 |

The teardown `0032ED80` runs `0037DA70`, which nulls `02ADD980 + manager * 0x3D0` for a manager
below 5, then clears both globals and both record fields (`0032F060`, `0032F06A`, `0032F0A8`,
`0032F0B2`); the free beside each clear is gated on `005C5230(5)`, which returns 0.

## Layouts

Offsets are from the section start unless a record is named.

```
CML1 (section 10): the layout of section 8
+0x00  char[4]  magic       "CML1"; never compared
+0x04  u32      count       rows
+0x08  u32[2]   -           0; not read
+0x10  row[count]
       +0x00  u32  nameOffset  name, from the section start
       +0x04  i32  shake       SHK1 record number; -1 = none
       +0x08  u32  -           zeroed at load
       +0x0C  u32  -           low byte zeroed at load
then the names, NUL-terminated; zero fill to 0x40

SHK1 (section 11)
+0x00  char[4]  magic       "SHK1"; anything else and nothing is stored
+0x04  u16      records     0 = no curve table is built
+0x06  u16      curves
+0x08  u16      dataOffset  first curve, from the section start
+0x0A  u16      -           0; not read
+0x0C  u32      -           0; not read
+0x10  record[records], 0x60 bytes
       +0x00  char[24]  name      read only by the name lookup, which never runs
       +0x18  u32       duration  read as a u16
       +0x1C  u32       -         0; not read
       +0x20  u16[32]   curve     slot k: 0 = none, else curve number + 1
dataOffset: curve[curves], each starting with an i32 length
```

A curve has the ease-curve layout of the camera tables (`+0x00` length `0x18 + 0x24 * keys`,
`+0x04` keys, start time and value, end time and value, then keys of `a`, `b`, `c`, `d` and span
at `+0x10`-`+0x20`); [EBP camera tables](ebp-camera-tables.md) has it in full. `003CC5F0` skips
the first 16 bytes of each key.

## Shipped data

Every count is per language tree; section 11 is byte-identical in all nine trees.

| Fact | Value |
|---|---|
| files | 113: 109 event scripts and 4 field map scripts; every one also carries sections 8 and 9, and neither section appears without the other |
| shakes | 299; 1 to 13 per file |
| curves, keys | 1,839 curves of 1 to 85 keys, 5,103 keys; 2 to 127 curves per file |
| CML1 rows | 300; one row is -1 and names no shake; the others are a permutation of the file's records, each row's name equal to its record's |
| `dataOffset` | `0x10 + 0x60 * records` in every file, `0x70` to `0x4F0` |
| names | 4 to 20 bytes, NUL-padded to 24 |
| durations | 10 to 1,000; most often 150 (32 shakes), 120 (27), 30 (24), 300 (17), 180 (15), 60 and 1,000 (14 each) |
| curve slots | in every file the non-zero slots number the curves 1 to `curves` in order, once each |
| slot use, k = 0 to 31 | 74, 38, 76, 33, 138, 79, 139, 62, 37, 16, 37, 13, 106, 72, 105, 66, 160, 93, 157, 73, 46, 11, 46, 7, 31, 13, 31, 11, 23, 12, 23, 11 |
| curve checks | every length is `0x18 + 0x24 * keys`, every curve's spans sum to 1.0, each key starts at the previous key's end value (3,264 of 3,264 joints), and the chain ends on the zero padding |

## Loader behaviour

### SHK1 at load

`0037DA90(section, manager)`:

1. Returns unless `+0x00` is `SHK1` (`0037DA96`).
2. Stores the section at `02ADD980 + manager * 0x3D0` (`0037DAC0`).
3. Returns when `records` is 0 (`0037DAC4`).
4. Allocates `curves * 8` bytes for the curve table at `02ADD988 + manager * 0x3D0` and walks
   `curves` steps from `section + dataOffset`, storing each curve's address and adding its
   signed length (`0037DB10`-`0037DB25`). Nothing is compared with the section's length.

### CML1 at load

`003DD120(record)` sets record `+0x1C` and `+0x1E` to -1 and the four shake entries to idle, then
zeroes each row's `+0x08` and the low byte of `+0x0C` (`003DD1C2`, `003DD1C6`). Its name lookup
`0037DB80` runs only when `0032F3D0(1, name)` returns non-zero, which it never does (kind 1 ends in
`005C5230(5)`): the authored `shake` column is used as shipped.

### Starting a shake

`camerashakestart_1a2` (`003492F0`) and `camerashakestart_1a3` (`00349730`) reach `003DD230`, which
checks the row number against `count`, takes row `+0x04` (`003DD29F`) and binds it to one of the
four shake entries with a rate ([actor managers](../Characters-And-Objects/actor-managers.md)).

### Each frame

`003DCFB0(record)` runs every bound entry of the manager:

1. When the record's byte `+0x201` is set, `0037DD50` puts the shake's clock at its duration + 1.
2. `0037D1F0(manager, shake, clock, entry)` marks a shake of -1 finished at once. Otherwise
   `0037D130` evaluates every curve slot at the clock with `003CC5F0` (a slot of 0 gives 0).
3. Slot `k` is value `k mod 4` of oscillator `k div 4`: the speed, the speed's random range, the
   size and the size's random range. Each oscillator's phase grows by `(random × range + speed)`
   times the frame factor `01DFE0BC`, and its output is `sin(phase) × (random × range + size)`.
4. The shake runs while `clock − 0.5 ≤ duration` (the margin is 0 when `001EDDA0` returns non-zero);
   then the entry is finished.
5. The clock grows by the entry's rate times `02B58190` and the frame factor.

The outputs are a three-part offset from oscillators 0-2, a second from oscillators 3-5 added to
the first, and single values from oscillators 6 and 7. `0037D4C0` sums the outputs of every
shake bound to the current camera frame and hands them through `00382B70` to `003820C0`, which:

- adds the first offset to the camera's position and the second to the point it looks at, both
  turned into the camera's frame by the matrix `02AED5C0`;
- adds the third value to the view angle `+0xC4` that `003CBD60` turns the view about its
  forward axis by;
- adds the fourth to the field-of-view angle (`02AED568`).

So slots 0-11 shake the camera's position, 12-23 add a further shake to its aim, 24-27 roll it and
28-31 zoom it.

## Modding notes

- The `shake` column of section 10 decides which shake plays; renaming a shake changes nothing.
- Keep `records` above 0; with 0 the section is stored but no curve table is built.
- `dataOffset` is 16 bits, so the records may not push the curves past 64 KiB: at most 682 records.
- Nothing compares a slot's curve number with `curves` (`0037D130`); keep slots within the file's curves.
- `duration` is read as 16 bits; values above 65,535 lose their high half.
- Leave a random-range slot at 0 for a regular motion; the shipped shakes fill the speed and size
  slots about twice as often as the ranges.
- Curve lengths are signed and unchecked; a wrong one misplaces every later curve.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches these sections.
- [EBP camera tables](ebp-camera-tables.md): the camera shots a shake moves, and the curve layout.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the record fields and the shake entry binds.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the shake verbs.
