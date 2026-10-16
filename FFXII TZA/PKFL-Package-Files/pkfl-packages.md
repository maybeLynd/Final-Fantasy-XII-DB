---
title: "PKFL packages: the per-area .mot, .snd, .vpc and .vpcjp containers, their offset and size directory, and the slot readers"
kind: "format"
category: "PKFL package files"
addresses: "0032FCA0, 0032FC30, 0032F430, 022C6E70, 022C6E98, 022C6EE8, 022C6EC0, 0032F260, 0032F290, 0032F2C0, 0032F2F0, 0032F3A0, 0032F320, 0032F360, 003DD4C0, 003DF440, 003DF2C0, 003E9F80, 003E9EF0, 002DF980"
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
`{ebp, mot, fpk}` (three files per area, index `3a`), kind 8 records `{ebp, mot, snd, vpc}` and kind `25`<sub>h</sub>
records `{ebp, mot, snd, vpcjp}` (four per area, index `4a`). Paths come from `002DF980(kind, index)`.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | 'PKFL' | only byte 0 is tested, for non-zero |
| `04`<sub>h</sub> | `u32` | slotCount | 16 (.mot, .snd) or 64 (.vpc, .vpcjp); not read |
| `08`<sub>h</sub> | `{u32 offset, u32 size}[slotCount]` | offsets from the file start; {0, 0} = slot empty |  |

The directory ends at `88`<sub>h</sub> for 16 slots and `208`<sub>h</sub> for 64. Every payload starts on a `800`<sub>h</sub> boundary,
the first at `800`<sub>h</sub>.

## Shipped data

| Fact | Value |
|---|---|
| packages | 10,314: 4,392 `.mot`, 2,304 `.snd`, 1,809 `.vpc`, 1,809 `.vpcjp` |
| empty packages | 27: 9 `.mot`, 9 `.vpc`, 9 `.vpcjp`, every pair `{0, 0}` |
| layout | in all 10,287 others: every pair inside the file, offsets ascending, the first at `800`<sub>h</sub>, each next payload at the first `800`<sub>h</sub> boundary after the one before, zero bytes in the gaps, file size a multiple of `800`<sub>h</sub> |
| `.mot` slots | 0-15 used (1,539, 3,186, 1,737, 1,134, 774, 540, 378, 270, 108, 54, 54, 36, 36, 27, 18, 18 packages); every payload is an `@FRP` container |
| `.snd` slots | 0-7 in every package, payloads starting with the dword 2; slots 8-15 in 9, 1,809, 324, 225, 153, 99, 45 and 18 packages, payloads starting `WD` |
| `.vpc` and `.vpcjp` slots | 0-13 of 64 used, the same occupancy in both (1,782 down to 9); every payload is a `VSP1` voice set |

## Loader behaviour

### The directory tables

`0032F430`, at start-up, allocates four `88`<sub>h</sub>- or `208`<sub>h</sub>-byte tables per area slot: `.mot` at `022C6E70`,
`.snd` at `022C6E98`, `.vpc` at `022C6EE8` and `.vpcjp` at `022C6EC0`. When an area slot
loads, `0032FCA0` (from `0032FC30`) reads into them:

- for area slots 0 to 3, the first `88`<sub>h</sub> bytes of the `.mot` (record index + 1);
- for area slots 1 to 3 (kind 8), also the first `88`<sub>h</sub> bytes of the `.snd` (+ 2) and `208`<sub>h</sub> of the
  `.vpc` (kind 8, + 3) and `.vpcjp` (kind `25`<sub>h</sub>, + 3);
- for area slot 4, none of them.

A table it does not fill, or a file with no size, gets byte 0 cleared. Each request it files sets a pending
bit in the slot's word `022C6E48[g]`: `2000`<sub>h</sub> for the `.mot` (completion `003302B0`), `1000`<sub>h</sub> for the
`.snd` (`00331760`), `8000`<sub>h</sub> for the `.vpc` (`00331820`) and `4000`<sub>h</sub> for the `.vpcjp` (`003317C0`).

### The slot readers

Each reader takes an area slot `g` and a slot `k`, and returns −1 when `g` is 4 or more (a signed test) or
byte 0 of the table is 0. None bounds `k` against the table.

| Reader | Table | Returns | Caller |
|---|---|---|---|
| `0032F260` | `.mot` | offset of slot `k` | `003DD4C0` (script motion slots) |
| `0032F290` | `.mot` | size of slot `k` | `003DD4C0` |
| `0032F2C0` | `.snd` | offset of slot `k` | `003DF440` (sound sets) |
| `0032F2F0` | `.snd` | size of slot `k` | `003DF440` |
| `0032F3A0` | `.snd` | size of slot `k + 8` | `003DF2C0`, which discards the value |
| `0032F320` | `.vpcjp` or `.vpc` | offset of slot `k` | `003E9EF0` (voice loads) |
| `0032F360` | `.vpcjp` or `.vpc` | size of slot `k` | `003E9F80`, `003E9D30`, `003E9E10` |

`0032F320` and `0032F360` take the `.vpcjp` table when their third argument is 0 and the `.vpc` table
otherwise.

### Reading a slot

A consumer allocates the slot's size and files the area file's kind and index with the slot's offset as
the read's file offset (`003E9EF0` passes it in the request record), so only that payload is read. The
read queue rounds the offset down to a `800`<sub>h</sub> boundary
([file requests](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md)). A size of 0
loads nothing.

## Modding notes

- Keep byte 0 non-zero; nothing else in the header is checked, and `slotCount` is never read.
- Put every payload on a `800`<sub>h</sub> boundary: the read starts at the offset rounded down.
- `.mot` and `.snd` directories are read as 16 slots and `.vpc` and `.vpcjp` as 64; a slot number from a
  script has no bound, so a `.mot` or `.snd` slot of 16 or more reads past the table.
- Keep the `.vpc` and `.vpcjp` of an area in step: the voice language picks which one plays.

## Related

- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md): the script motion slots that read `.mot`.
- [Resource sections](../Game-Files-And-Data-Tables/resource-sections.md): the `@FRP` containers inside `.mot`.
- [Voices](../Sound-And-Music/voices.md): the `VSP1` voice sets and the voice verbs.
- [Sound banks](../Sound-And-Music/sound-banks.md): the sound data in `.snd`.
- [File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md): the kinds and records the packages belong to.
