---
title: "Weapon bones: every weapon model's keyed points, the blade and grip an effect anchors to, and its special-id bones"
kind: "reference"
category: "Graphics"
addresses: "0x00409250, 0x00422380, 0x003E5AD0, 0x003A4290, 0x00426770"
---

## What it lists

`weapon-bones.tsv` holds one line for each class-`w` model, the 327 bound ids of kind 16
([Model asset list](model-asset-list.md)). For each it gives the keys of the model's skeleton nodes, whether two of
them are present, and the special-id bones of its `@FCP` block.

The two points are the weapon's blade and grip. A held weapon is a child record of the character that holds it, and
the anchor query finds a point on a child by key (`0x00426770`; [Effect anchors and targets](effect-anchors-and-targets.md),
point kinds 4 and 5, and the fallback to a child's `n_grip`):

| Point | Key | Point id (`0x00422380`) |
|---|---|---|
| `j_blade` | `0x65E` | `0x200` |
| `n_grip` | `0x656` | `0x201` |

The default bone table of [Character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table)
names them for attach slots 18 and 19.

### How it is built

`Database/Tools/catalogues/weapon_bones.py`, on the archive reader `vbflib.py` and the layouts of
[Model files](model-files-cm-ca.md):

1. **The node keys.** Node *n* of the `.cm`'s `@FTR` skeleton has the key `0x00409250` returns: bits 0-11 of the node
   record's first dword, or the `u16` at record `+0x08` when the record's flag bit 30 is set.
2. **The special-id bones.** `0x003E5AD0` reads section 1's `u16[32]` at `+0x14C` for special ids 0-31, and the
   `@FCP` block's `+0x3A`, `+0x3C` and `+0x3E` for ids `0x104`-`0x106`; `0xFFFF` means none.
3. **The equipment,** the rows of [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md) whose
   `model_id` names the model, by their category and name.

### Shipped data

| Fact | Value |
|---|---|
| models | 327; 326 ship with an `@FTR`, an `@FCP` and a section 1, and `w2123` does not ship |
| `j_blade` | 185 of the 326 |
| `n_grip` | 284 of the 326 |
| node counts | 2 nodes on 98 models, 3 on 182, 4 on 19, 5 on 26, and 16 on the spear `w5003` |
| key sets | `0x1D 0x656 0x65E` 180; `0x1D 0x656` 57; `0x1D 0x1E` 41; `0x1D 0x656 0x1D00 0x1CFF 0x1CFD` 16; `0x1D 0x656 0x658 0x657` 13; `0x1D 0x656 0x1D00 0x3C5A 0x3C5B` 8; six others. `0x1D` (`model`) is on all 326 |
| special ids `0x104`-`0x106` | `none 1 0` on 284; `1 none 0` on the 41 `0x1D 0x1E` models; `none none 0` on `w5003` |
| special ids 0-31 | none on 281; id 14 is bone 2 on 23; ids 0-8 are bone 1 on 20; id 13 is bone 0 on 2 |
| equipment | 373 rows name 295 of the models; 32 are named by no row |

By category:

| Category | Models | Without `j_blade` | Without `n_grip` |
|---|---:|---|---|
| Sword (1H), Sword (2H), Dagger, Axe, Hammer, Katana, Ninja Sword, Rod, Staff, Measure, Hand-bomb | 132 | none | none |
| Mace (1H) | 13 | `w2302`, which has only the keys `0x66C`-`0x66E` | `w2302` |
| Spear (2H) | 15 | `w5003` (`0x656`, `0x657`, `0x658` and twelve keys `0x18B4`-`0x18BF`), `w5020` (`0x1D 0x1E`) | `w5020` |
| Pole (2H) | 13 | 12 | none |
| Bow (2H) | 14 | all | none |
| Crossbow (2H) | 9 | all | `w8002`, `w8003` |
| Gun (2H) | 15 | all | `w1018` |
| Arrows | 8 | all | none |
| Bolts | 10 | all | `w8209`, `w8210` |
| Shot | 9 | all | 8 (`w8301`-`w8308`) |
| Incendiaries | 8 | all | all |
| Shield | 32 | 22, which carry `0x1D 0x1E` only; the ten others carry both points | none |
| Unarmed | 17 | all, `0x1D 0x1E` models | all |
| no equipment row | 32, `w2123` among them | 14 of the 31 shipped | `w1004`, `w1010` |

One model is used by both Katana and Sword (1H) rows; the table counts it once, in the first row.

### Checks

- Every row's keys are read from the shipped `.cm`; the unshipped `w2123` is kept with the note "not shipped".
- Two runs over the same files give byte-identical output.

## Columns

| Column | Meaning |
|---|---|
| `bound_id`, `name`, `cm` | the bound id, the model's name and its `.cm` path |
| `categories`, `equipment` | the equipment categories and the names of the equipment rows that use the model |
| `ftr_nodes`, `keys` | the `@FTR` node count and the node keys |
| `j_blade`, `n_grip` | whether a node has the key `0x65E` or `0x656` |
| `special_bones_0_31` | the set entries of section 1's special-id table, as "id: bone"; "none" when every entry is `0xFFFF` |
| `special_bones_104_106` | the set ones of special ids `0x104`-`0x106`, as "id: bone"; "none" when all three are `0xFFFF` |
| `note` | "not shipped" for a model whose `.cm` the archive lacks |

## Related

- [Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it](model-asset-list.md)
- [Model files (.cm, .ca)](model-files-cm-ca.md): `@FTR` and `@FCP`
- [Character render records](character-render-records.md): attach slots, default bones and point ids
- [Effect anchors and targets](effect-anchors-and-targets.md): the anchor query that uses the two points
