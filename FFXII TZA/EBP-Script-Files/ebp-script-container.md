---
title: "EBP script container: the twenty-slot directory of every zone and event script, and the walk that hands each section to its loader"
kind: "format"
category: "EBP script files"
addresses: "003304A0, 0032FCA0, 0032FC30, 00330310, 0032E400, 0032E620, 002DF980, 002DF9A0, 0036A100, 0036C660, 00332250, 022C6E48, 022C6C00, 0032F1B0, 0032ED80, 0032F430, 0032F850, 00330190, 00330220, 00332100, 00330060, 0032FA10, 0032FAC0, 00331610, 003316B0, 0032FB70, 00330110, 003320E0, 00332110, 003320D0, 0032ED70, 00332130"
---

## What the player sees

Everything a map does beyond its scenery comes from one `.ebp` file: the people who walk and talk,
the doors, chests and save crystals, the weather, the camera cuts and lighting of a cutscene, the
signs on the map. Each zone has one, each event has one, and entering a zone or starting an event
loads it. The container is the file's table of contents: it says which of these parts a given zone
or event carries and where each one starts.

## Where it comes from

Zone scripts sit at `ps2data/plan_master/<language>/plan_map/<area>/<zone>/global/<zone>.ebp` and
event scripts at `ps2data/plan_master/<language>/event/<group>/<event>/<event>.ebp`, in nine
language trees. Four control scripts (`btlctrl`, `ctrl`, `evctrl`, `mapctrl`) sit under
`ps2data/image/ff12/<language>/bin/` in the `in` and `ch` trees only.

The game never opens a script by name. `0032FCA0(manager, id)` turns a script manager index and a
script id into a `(namespace, index)` pair and resolves it through the path tables
(`002DF980` returns `[0215F000 + namespace × 8][index]`, the tables `002DF9A0` installs per
language; see [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md)):

| Manager | Namespace | Index | Files at index, +1, +2, +3 |
|---|---|---|---|
| 0 (zone) | 5 | id × 3 | `.ebp`, `.mot`, `.fpk` |
| 1 to 3 (events) | 8 | id × 4 | `.ebp`, `.mot`, `.snd`, `.vpc` |
| 4 | 1 | id + `0x6B` | the script only |

The zone script is requested from `00314020` (`003140BA`, manager 0, the id held at `01EED064`).
Event scripts go to managers 1 to 3: `003522C0` and `00353080` add 1 to their argument and clamp
it to 1 to 3, and `00353590`, `003CA07C` and `00306BD0` use manager 3.

## Layouts

### Container header

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | magic | 'EBP2' in every shipped container |
| `+0x04` | `u32` | slotCount | 20; slot n is dispatched only when slotCount > n |
| `+0x08` | `u32` | reserved | 0 |
| `+0x0C` | `u32` | reserved | 0 |
| `+0x10` | `u32[20]` | sectionOff | indexed by section number; file-relative offset, 0 = absent |
| `+0x60` | `u8[32]` | padding | 0; the first section starts at +`0x80` |

A section has no stored length: it runs to the next present offset, and the last one to the end of
the file. The walker passes each section on as `fileBase + offset` with the manager index in the
low four bits, so every offset must be a multiple of 16.

### Section table

| Slot | First bytes | Handler, then binder | Kept in | Documented in |
|---|---|---|---|---|
| 0 | `0x8000000B` | `0032F850` → `0026C8C0` | `022C6C28` | [script image](ebp-script-image.md) |
| 2 | | `00330190` → `0026C880` | `022C6CA0` | [script text](ebp-text-sections.md) |
| 3 | | `00330220` → `0026C8A0` | `022C6CC8` | [script text](ebp-text-sections.md) |
| 4 | `NAVI` | `00332100` → `003DFDC0` | | [navigation icons](ebp-navigation-icons.md) |
| 6 | `TIM2` | `00330060` → `0026C860`, `0017F790`, `0029CAC0` | `022C6CF0` | [TIM2 images](../Game-Files-And-Data-Tables/tim2-images.md) |
| 8 | `CML1` | `0032FA10` → `0026CE00` | `022C6D80` | [camera tables](ebp-camera-tables.md) |
| 9 | `CAM7` | `0032FAC0` → `002566E0`, `002561C0`, `0026CE20` | `022C6D58` | [camera tables](ebp-camera-tables.md) |
| 10 | `CML1` | `00331610` → `0026D3A0`, `003DD120` | `022C6DF8` | [camera shake](ebp-camera-shake.md) |
| 11 | `SHK1` | `003316B0` → `0026D3C0`, `0037DC30`, `0037DA90` | `022C6DD0` | [camera shake](ebp-camera-shake.md) |
| 12 | | `0032FB70` → `0026CE40` | `022C6DA8` | [actor manifest](ebp-actor-manifest.md) |
| 14 | `LGT2` | `00330110`, bound later by `0032F1B0` | `022C6E20` | [lighting](ebp-lighting-lgt2.md) |
| 16 | `FF12` | `003320E0` → `003DFE60(0, section)` | | [position entries](ebp-position-entries.md) |
| 17 | | `00332110` → `003DFE60(1, section)` | | [position entries](ebp-position-entries.md) |
| 19 | `FF12` | `003320D0` → `003EAA00` | | [area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md) |

The "Kept in" arrays hold one qword per manager. Slots 1, 5, 7, 13, 15 and 18 have no dispatch:
the walker never reads their offsets. Slot 17 is the same format as slot 16, bound under the
other selector.

## Shipped data

Measured over every `.ebp` in `FFXII_TZA.vbf`.

| Fact | Value |
|---|---|
| `.ebp` files | 10,045: 1,115 per language tree (`kr` and `cn` 1,116), plus the 8 control scripts |
| containers | 10,036; the 9 others are `event/evt_t/evt_t0020/evt_t0020.ebp` in each tree, 2,416 bytes beginning with the word `0x80000007` and no header |
| `us` tree | 1,114 containers: 769 zone scripts and 345 event scripts |
| header | magic `EBP2`, slot count 20, both reserved words 0, padding zero, first offset `0x80`: all 10,036 |
| section offsets | 50,912, every one a multiple of `0x40`, ascending and inside the file in every container |
| container size | 640 to 468,352 bytes (`us` 640 to 421,184) |
| slots never present | 1, 5, 7, 13, 15, 17 and 18, in all 10,036 |
| `us` occupancy | 0: 1,114; 2: 828; 3: 359; 4: 209; 6: 67; 8 and 9: 423; 10 and 11: 113; 12: 842; 14: 140; 16: 517; 19: 271 |
| all-tree occupancy | 0: 10,036; 2: 7,466; 3: 3,232; 4: 1,881; 6: 2,719; 8 and 9: 3,807; 10 and 11: 1,017; 12: 7,578; 14: 1,260; 16: 4,653; 19: 2,439 |
| pairs | 8 and 9 always occur together, and 10 and 11; 2 and 3 do not (2,953 both, 4,513 only 2, 279 only 3) |
| zone-only sections (`us`) | 3, 4, 16 and 19 occur only in zone scripts; 14 only in event scripts |
| section 6 by tree | 67 or 68 files in each Latin-script tree; 556 `kr`, 584 `cn`, 603 `ch`, 633 `in`; plus 3 control scripts in each of `in` and `ch` |
| first bytes | the word or tag in the section table, the same in every file that has the section |

## Loader behaviour

### Requesting a script

`0032FC30(manager, id)` calls `0032FCA0` and, for manager 0, sets bit 0 of the manager's pending
word. `0032FCA0`:

1. tears down the manager's previous script (`0032ED80`, below) and records the id at `022C6D28`
   and `022C6D40`;
2. picks the namespace and index from the table above;
3. for managers 0 to 3, requests the companion files: index + 1 into the `0x88`-byte buffer
   `022C6E70` (pending bit 13), and, for managers 1 to 3, index + 2 into `022C6E98` (bit 12);
4. for managers 1 to 3, requests index + 3 of namespace 8 into the `0x208`-byte buffer `022C6EE8`
   (bit 15) and the same index of namespace 37 into `022C6EC0` (bit 14); each request is made only
   when `0032E400` reports a size;
5. pushes the arena the image will live in: 5 for manager 0, `0xD` for managers 1 and 2 and `0xE`
   for manager 3 when that arena is enabled (`0036B200`), otherwise 5;
6. calls `00330310` to read the script itself.

Namespace 37's table is the `in` tree's (`01ECBCF0`; the `ch` tree's `01EA4D00` for language codes
7, 8 and 11), so its index + 3 names a `.vpcjp` file such as
`in\event\nal_a\nal_a0100\nal_a0100.vpcjp` where namespace 8 names the `.vpc`. The four companion buffers are allocated once,
for all five managers, by `0032F430`.

### Reading it whole

`00330310(manager, id, namespace, index)`:

1. takes the size from `0032E400`, which rounds the size table's figure up to a multiple of 64;
2. sets pending bit 17;
3. allocates that many bytes with `0036A100` in the current arena and labels the block with
   `0036C660` (source name `atelload.c`, tag `0x95C`);
4. stores the buffer at `022C6C00[manager]`, sets the manager record's `+0x11` bit 3, and forms the
   packed value `buffer | manager`;
5. calls `00332250`, which for namespaces 5, 8 and 37 cuts a folder name out of the path (such as
   `event\nal_a\nal_a0100`) and hands it to the text layer under the packed value (`0017FA90`);
6. files an asynchronous whole-file read (`0032E620`) whose completion is `003304A0(packed)`;
7. for manager 0, files a `0x800`-byte pre-read of the zone's index + 2, its `.fpk` (`0032EB40`), which no
   zone ships, so it reads nothing.

Script id `0xD4` (namespace 8 index `0x350`, `event/pre_z/pre_z0000` in the `us` tables) is
preloaded once by `0032F430` into `022C6F10`; a request for it copies that image into the new
buffer and walks it at once instead of reading the file.

### The directory walk

`003304A0` (570 bytes) recovers the file base with `and rdi, 0xFFFFFFF0` (`003304D9`) and the
manager from the low nibble. It sets pending bit 1, and bit 9 when slot 12 is present
(`003304DE`–`003304F5`). It then tests each slot in a fixed order with the same five steps:
`slotCount > n` (unsigned), offset non-zero, `base + offset`, `or` the manager into the low nibble,
call the handler. There is no loop and no table: fifteen `cmp dword ptr [rdi + 4], n` sites cover
fourteen slots, slot 12 being tested twice.

The order is 0, 2, 3, 6, then 9, 8, 11, 10, 12, 16, 17, 4, 19, and last 14, which is skipped for
manager 0 (`0033066B`). The first four calls are bracketed by the text-layer calls `0017FB70` and
`0017FBE0`. The walk reads nothing else: not the magic, not the reserved words and not the padding.

The packed value is carried in 32 bits (`00330510 or eax, ebx`, `00330512 mov ecx, eax`), and each
handler masks it back with `0xFFFFFFF0`, so the buffer must lie below 4 GiB and every section offset
must keep the low four bits clear.

### Handlers

Each handler that keeps its section stores the pointer in its manager array (section table) and
calls its binder; the slot-0 handler `0032F850` first rejects an image whose first byte is 0
([script image](ebp-script-image.md)). Sections 4, 16, 17 and 19 go straight to their subsystem
and are not tracked per manager. Section 14 is only stored; `0032F1B0` binds it.

### Pending word and finish

`022C6E48[manager]` holds the manager's outstanding work:

| Bit | Set by | Cleared by |
|---|---|---|
| 0 | `0032ED70` after an event request, `0032FC30` for manager 0 | `00332130` |
| 1 | the walk | the slot-0 handler `0032F850` |
| 9 | the walk, when slot 12 is present | the slot-12 handler `0032FB70` |
| 12 to 15 | `0032FCA0`, per companion request | their completions `00331760`, `003302B0`, `003317C0`, `00331820` |
| 17 | `00330310` | the end of the walk (`00330696`) |

The other handlers clear bits 4 to 8, 10, 11 and 16, which nothing on this route sets. Every
clearer applies the same rule: when the word without bit 0 becomes zero it clears the record's
`+0x11` bit 3; when the whole word goes from non-zero to zero it runs `0032F1B0(manager)`.

`0032F1B0` binds section 14 through `0037AA90` for managers above 0, with its light bookkeeping
(`0037B230`, `003DE920`, `0037B290`), then runs `0026CE60`, which builds the manager's actors from the
image ([actor managers](../Characters-And-Objects/actor-managers.md)), and `00263C30`.
Bit 0 therefore holds `0032F1B0` back after every part has arrived, until `00332130` clears it
(its callers include `00354B20`, `00354E80` and `00378120`).
For manager 0, `0032F850` and `0032FB70` also run `0025AFC0(0)` once bits 1 and 9 are both clear.

### Teardown

`0032ED80(manager)` runs before every new request. It unbinds what the handlers bound: section 6
(`002E0780`, `0017FA50`, `0029CB10`), section 14 on managers above 0 (`0037AA50`), section 9
(`002561A0`, `002566E0`, `0026CE20(manager, 0)`), section 8 (`0026CE00`), section 11 (`0037DA70`,
`0026D3C0`), section 10 (`0026D3A0`) and section 12 (`0026CE40`), and resets the four shake slots
(`0037DC30(manager, 0..3)`).

It zeroes every manager array
entry and the pending word, and frees the file buffer `022C6C00[manager]` (`003697F0`). The
per-section frees beside each unbind sit behind `005C5230`, which returns 0, so they never run.

## Modding notes

- The magic, the reserved words and the padding are never read; the slot count is, and lowering it
  disables every slot at or above it.
- A section added to slot 1, 5, 7, 13, 15 or 18 is never looked at. Slot 17 is live and takes the
  slot-16 format.
- Keep section offsets multiples of 16 (the shipped files use 64); the low four bits carry the
  manager index.
- Nothing checks a section's extent against the next offset or the file size.
- Section 14 has no effect in a zone script, which manager 0 loads.

## Related

- [Script image](ebp-script-image.md): section 0, the code the interpreter runs.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the record the bind fills and `0026CE60`.
- [File path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md): the path tables and the read.
- [Resource arenas](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md): `0036A100`, the arena stack and block labels.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): what runs the image once it is bound.
