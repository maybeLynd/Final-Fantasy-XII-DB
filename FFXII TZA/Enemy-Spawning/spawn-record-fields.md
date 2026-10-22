---
title: "Spawn record fields: the keep entry behind every spawned enemy, offset by offset, its flag bits and every proven access"
kind: "reference"
category: "Enemy spawning"
addresses: "0x00236100, 0x002360D0, 0x0023A570, 0x0023AC80, 0x002395A0, 0x0023A2E0, 0x00236860, 0x00237080, 0x00239840, 0x00239410, 0x002391C0, 0x002396B0, 0x0023A200, 0x0023A410, 0x00233AD0, 0x00234200, 0x002350C0, 0x00235720, 0x002355A0, 0x002354F0, 0x00235360, 0x00300530, 0x003112F0, 0x00385BA0, 0x0030FED0, 0x00300310, 0x003003F0, 0x00307300, 0x00311F70, 0x00239210, 0x00312EE0, 0x00308040, 0x00238BF0, 0x00301AD0, 0x00321530, 0x00321D40, 0x00233780, 0x00321DC0, 0x00321810"
---

## What it lists

Every enemy placed by a zone script owns one spawn record of `0x250` bytes in the live keep bank at
`[0x0208E690]` (64 records; the history bank at `[0x0208E698]` has the same shape,
[enemy respawning](enemy-respawning.md)). The record outlives the battle unit: it carries the
enemy's death history, its position and facing, its persistence key, its threat table and its whole
stats record, which is why a banked enemy comes back with its HP, statuses and grudges intact.

Code reaches a record three ways:

| Route | How |
|---|---|
| the lane map | unit `+0x40` is the lane map: count at `+0`, one slot byte per lane from `+1`, `0xFF` empty; `0x00236100(map, lane)` returns `[0x0208E690] + slot * 0x250` and `0x002360D0(map, lane)` the slot. Every script accessor opens with this walk through the unit from `0x0031B760` |
| the unit's back-pointer | unit `+0x6A0`, installed by `0x0023A570` for a kind-1 unit and null for party units ([battle unit construction](../Characters-And-Objects/battle-unit-construction.md)) |
| the bank copies | `0x00233780`, `0x00233440`, `0x00233550` and `0x00235360` move whole records with `movups`, structure-blind |

`spawn-record-fields.tsv` lists the accesses the typed scan proved through the lane-map and seed
routes; the back-pointer writers are named per field below with their sites.

## Columns

| Column | Meaning |
|---|---|
| `function` | the function containing the instruction |
| `name` | the name the scan carried for the function, `FUN_` when none |
| `site` | the instruction's address |
| `disp` | the offset reached, relative to the record |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed and passed on |
| `instruction` | the instruction text, checked against the executable |
| `route` | `seed` for a lane-map or bank-base resolution in the function itself, or `arg0+0x80<caller@site` for the stats page passed by that caller |
| `note` | `idx` when an index register takes part |

## Data

### The fields

| Offset | Width | Field | Writers | Readers |
|---|---|---|---|---|
| `+0x000` | `u32` | flags, eight bits (next table) | see the bit table | see the bit table |
| `+0x004` | `f32` | lifecycle point threshold: the absolute value of the float `0x0023A200` receives, with bit 3 for positive and bit 6 for below -1.0; zeroed first. The same call sets unit flag bit 40 for a non-zero float and clears it for 0 | `0x0023A200` | `0x00308040` (`0x003080D0`) |
| `+0x008` | `u16` | death count | `0x00300530` (`0x00300801`, `inc`); zeroed by `0x002395A0` (`0x0023965C`) | `0x00235F50`; `0x00235720` against `+0x0A` |
| `+0x00A` | `u16` | death limit: `row.b_00 + rand % (row.b_01 + 1)`, or 0 | `0x002395A0` | `0x00235EF0`; `0x00235720` |
| `+0x00C` | `u32` | second of the last death: `counter / (int)(30.0 * [0x01DFE0B8])` | `0x00300530` (`0x00300829`); zeroed by `0x002395A0` | `0x00235FB0` (`0x00236017`); `0x00235720` (`0x002358D1`) |
| `+0x010` | `u16` | respawn cooldown in whole seconds: `row.w_02 + rand % (row.w_04 + 1)`, or 0 | `0x002395A0` | `0x002366E0`; `0x00235720` |
| `+0x012` | `u8` | spawn-history counter: the low byte of the row's `0x0208D354` counter before increment, 0 for a `0xFF` row; the ordinal behind the letter after a foe's name | `0x0023A570` | `0x00238BF0` (`0x00238EA9`), passed with the unit's text pointer to `0x00269F20`, which stores it at the actor's `+0x100`; the name drawer `0x00272CE0` adds entry `0x21` + (ordinal - 1) mod 26 of the font sheet's letter text (`0x002B58F0`) when the ordinal is not 0 ([Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)) |
| `+0x014` | `u8` | steal slots, bits 0-2 = the slot is authored (the row's word `+0x32`, `+0x34` or `+0x36` is not `0xFFFF`), set at a fresh spawn; a consumer clears the bit once the slot is taken | `0x0023A570`; cleared per slot by `0x003112F0` (`0x0031146F`) and `0x00385BA0` (`0x00385C17` `0xFB`, `0x00385C41` `0xFD`, `0x00385C6B` `0xFE`) | `0x003112F0`, `0x00385BA0` |
| `+0x015` | `u8` | range-retire inhibit tag, written with bit 4 | `0x002391C0` | `0x00301AD0` (`0x00301D75`, after testing bit 4 at `0x00301D70`) |
| `+0x016` | `u8` | the script's selection, `0xFF` none; bits 0 and 2 of the flags are cleared when it changes | `0x00239840`; `0xFF` from `0x0023A2E0`, `0x00236860` (as a word with `+0x17`), `0x00237080` | `0x00236140` (returns -2 on a bad lane) |
| `+0x017` | `u8` | persistence key; `0x00235360` copies the first history entry with the same key, bit 1 set and bit 0 or 2 set over the live entry | `0x00239840` and `0x0023A2E0` from `+0x18` on a fresh entry; 0 from `0x00236860`; `0x002395A0` | `0x00235360` (`0x0023541F`) |
| `+0x018` | `u8` | the authored key the resets restore `+0x17` from: `row.b_06` when the table's byte `+1` is set, else 0 | `0x002395A0` | `0x0023A2E0`, `0x00239840` |
| `+0x019` | `u8` | enmity decay timer | `0x00321530` (`0x0032156D` forms the address); zeroed by `0x00321810` | [enmity](../Enemy-AI-And-Gambits/enmity.md) |
| `+0x01A` | `u8[40]` | enmity toward combatant id 0-39 | `0x00321D30` (`0x00321D61` forms the `+0x19` base; the per-id byte is reached by index), the enmity writers; `0x00321DC0(base, v)` sets the byte of every id that `0x00322C50(2, id)` admits to `v` clamped to 0-255, run by `0x00321810(unit, on)` with 0 or 1 from `0x002392D0` (verb `btlAtelSetEntryFlag`, `0x00510300`: flag bit 15 clear gives 1, set gives 0; only while spawn byte `+0` bits 0 and 2 are clear) | the same |
| `+0x042` | `u8[14]` | untouched by any function in either route | | |
| `+0x050` | `f32[4]` | persisted world position, stored whole | `0x00300310` (`0x003003CE`), `0x00307300` (`0x003079F4`), `0x00311F70` (`0x00312092`), `0x00239410`, `0x002355A0`, `0x00235720` | the selectors through the bank copies |
| `+0x060` | `f32[4]` | candidate position x, y, z at `+0x60`, `+0x64`, `+0x68` | `0x00239410` (y = 0), `0x002355A0`, `0x00235720`, `0x00234200` (`0x00234291`, from unit `+0xE0`, under the release gate below) | `0x0023A410`: when unit `+0x1F6` has bit 3 the ground probe rewrites `+0x64` and unit `+0x188` is added, then the record is passed to `0x00300310` |
| `+0x070` | `f32` | persisted facing yaw | `0x003003F0` (`0x0030046E`), `0x00307300` (`0x00307A4F`), `0x00311F70` (`0x003120F7`), `0x00239210` (a random yaw in `[0, 360)` when its argument is negative; the same yaw goes to the actor through `0x0026A0D0` and `0x0026B620`) | no reader of the field found; the bank copies carry it |
| `+0x074` | `u32` | unit `+0x160` at slot release | `0x00234200` (`0x0023429E`, under the release gate below) | none found |
| `+0x078` | `u8[5]` | persisted elemental affinity: weak, absorb, resist, immune, and the source's half-again, mirrored with stats `+0x40`-`+0x44` under bit 7 ([elements](../Damage-And-Battle-Formulas/elements.md)) | `0x003112F0` (`or`/`and` per byte, `0x00311954`-`0x00311A74`); zeroed by `0x0023A2E0`, `0x00236860`, `0x00237080` | `0x0030FED0` |
| `+0x07D` | `u8[3]` | untouched | | |
| `+0x080` | `u8[456]` | the stats record, initialised in place by `0x0023AC80` and grown by `0x0030C470` ([unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md)) | the `arg0+0x80` rows of the table | the same |
| `+0x248` | `u8[8]` | untouched | | |

`0x00234200`, the slot release, writes `+0x60`, `+0x74` and flag bit 2 only for a kind-1 unit whose
byte `+0` has bit 4, with a non-null back-pointer, and, when its status words carry `0x80000003`,
only when `0x00377C20()` waives them. The script accessors return -1 for an unmapped lane, except
`0x00236140`, which returns -2 because -1 is a legal selection value.

### The flag bits

`+0x00` is read as a byte or a dword; the same eight bits either way.

| Bit | Meaning | Set by | Cleared by | Tested by |
|---|---|---|---|---|
| 0 | retired by range, awaiting re-entry | `0x002350C0` (`0x002352A6`) | `0x0023A410` (`0x0023A46F`); `0x00239840` (`0x002398C2`, with bit 2, on a selection change); `0x00236860` and `0x00237080` with the mask `0xFFFFFF7A`; `0x0023A2E0` with the same mask on a fresh entry | `0x00235720` (skips the cooldown); `0x00236670`; `0x00235360` (`test r8b, 5`) |
| 1 | activation committed | `0x00233AD0` (`0x00233BA8`, kind-1 units) | nothing until the bank is wiped | `0x002395A0` (`0x002395E3`, skips the entry); `0x00236670`; `0x00235360` (`0x00235413`); `0x002354F0` |
| 2 | the unit's slot was released | `0x00234200` (`0x0023429B`) | `0x0023A410` (`0x0023A465`); the three resets' mask | fresh tests `(flags & 5) == 0` in `0x0023A2E0`, `0x00239840`, `0x0023A200`, `0x002396B0`, `0x0023A410`; `0x002391C0` refuses when set; `0x00236670`; `0x002354F0` picks the first lane with it |
| 3 | lifecycle point mode, positive | `0x0023A200` (float `> 0`) | `0x0023A200`, `0x00312EE0` (`0x00312F30`) | `0x00233AD0` (`0x00233B3A`); `0x00308040` and others as `0x48` with bit 6 |
| 4 | range retire inhibited | `0x002391C0` (with the tag at `+0x15`) | `0x002391C0` (tag 0) | `0x002350C0` (`0x00235159`); `0x00301AD0` (`0x00301D70`); as `0x30` with bit 5 by `0x002FFCF0`, `0x003014C0`, `0x003247F0`, `0x0030DA30`, `0x00384F40` |
| 5 | category-4 mode | `0x002396B0`, on a fresh entry only, when the mode byte `+0x58` becomes 4 | `0x002396B0` (fresh entry, before the set); `0x00237D80` for a kind-1 unit whose byte `+0` has bit 4 | `0x00308040` (`0x00308075`); `0x00238BF0`; `0x002FFF50`; the `0x30` tests |
| 6 | lifecycle point mode, negative | `0x0023A200` (float `< -1.0`) | `0x0023A200`, `0x00312EE0` (`0x00312F21`) | `0x002FFF50` (`0x00300023`); `0x0031FE10`; `0x00329220`; the `0x48` tests |
| 7 | affinity dirty | `0x003112F0` (`0x0031195E`-`0x00311A7E`, once per affinity byte changed) | `0x00236860`, `0x00237080` and, on fresh entries, `0x0023A2E0` (mask `0xFFFFFF7A`) | `0x0030FED0` (`0x0031043A`) |

A fresh entry is one with `(flags & 5) == 0`: neither retired nor released. The steal bits, the
history counter, the key restore and the affinity reset happen only then.

### The resets

| Function | Scope | Writes |
|---|---|---|
| `0x0023A2E0(actor, map)` | installs the lane map at unit `+0x40`; for every mapped fresh entry | `+0x16` = `0xFF`, flags `&= 0xFFFFFF7A`, `+0x78`-`+0x7C` = 0, `+0x17` = `+0x18` |
| `0x00236860(actor, _, lane)` | one mapped entry, no fresh test | flags `&= 0xFFFFFF7A`, word `+0x16` = `0x00FF` (so `+0x17` = 0), `+0x78`-`+0x7C` = 0 |
| `0x00237080(record)` | one record, from the teardown `0x00300E40` when its second argument is 0 | the same as `0x00236860` |
| `0x0023A410(actor)` | the unit's own entry at activation | bits 0 and 2 cleared; when the entry was fresh and the definition row's dword `+0x18` is non-zero, `0x00300520(stats, row.dw_18, 0, 0x297)` first |

### The copies

`0x00235360` copies `0x250` bytes, four `0x80` blocks and a `0x50` tail (`0x00235460`-`0x002354DD`), from
the matching history entry over the live one. The three bank loops in `0x00233780`, `0x00233440` and
`0x00233550` move `0x9400` bytes per bank in 128-byte `movups` pairs. None names a field: the stats
page at `+0x80`, the enmity bytes and the positions travel with everything else.

## Related

- [Enemy respawning](enemy-respawning.md): the death fields, the banks and the group table.
- [Enemy spawning](enemy-spawning.md): the lane map, the selectors and range retirement.
- [Battle unit construction](../Characters-And-Objects/battle-unit-construction.md): the installer.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the record at `+0x80`.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md): the bytes at `+0x19`.
