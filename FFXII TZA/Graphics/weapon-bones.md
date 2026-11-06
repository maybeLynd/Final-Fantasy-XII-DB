---
title: "Weapon bones: every weapon model's keyed points, the blade and grip an effect anchors to, and its special-id bones"
kind: "reference"
category: "Graphics"
addresses: "0x00409250, 0x00422380, 0x003E5AD0, 0x003A4290, 0x00426770"
---

## What it lists

[`weapon-bones.tsv`](weapon-bones.tsv) holds one line for each class-`w` model, the 327 bound ids of kind 16
([Model asset list](model-asset-list.md)). For each it gives the keys of the model's skeleton nodes, whether two of
them are present, and the special-id bones of its `@FCP` block.

The two points are the weapon's blade and grip. A held weapon is a child record of the character that holds it, and
the anchor query finds a point on a child by key (`0x00426770`;
[Effect anchors and targets](effect-anchors-and-targets.md), point kinds 4 and 5, and the fallback to a child's
`n_grip`).

`0x00426770` asks `0x00421E20` for the point on the record itself, whose index is its word `+0x00` (`0x00426776`,
`0x004267B7`), then on its first child `+0x08` (`0x004267FC`), then through `0x0042EF90` with the body `0x0042DA00` on
that child's children `+0x08` and next siblings `+0x0A`, each with its descendants (`0x00426829`, `0x00426844`).
Each hit replaces the stored result (`0x004267C1`, `0x00426806`, `0x0042DA1F`), so the last record in that order with
the point gives it; with no hit it returns null (`0x0042684E`-`0x00426853`). The two points:

| Point | Key | Point id (`0x00422380`) |
|---|---|---|
| `j_blade` | `0x65E` | `0x200` |
| `n_grip` | `0x656` | `0x201` |

The default bone table of [Character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table)
names them for attach slots 18 and 19.

### Where the values come from

Each row is read from the model's `.cm` with the layouts of [Model files](model-files-cm-ca.md):

1. **The node keys.** Node *n* of the `.cm`'s `@FTR` skeleton has the key `0x00409250` returns: bits `0xFFF` of the node
   record's first dword, or the `u16` at record `+0x08` when the record's flag bit `0x40000000` is set.
2. **The special-id bones.** `0x003E5AD0` reads section 1's `u16[32]` at `+0x14C` for special ids 0-31, and the
   `@FCP` block's `+0x3A`, `+0x3C` and `+0x3E` for ids `0x104`-`0x106`; `0xFFFF` means no bone. It also returns
   `0xFFFF` for any other id, and for a model record with no `@FCP` block (`+0x400` = 0, `0x003E5AD7`-`0x003E5ADA`).
3. **The equipment,** the rows of [Equipment list](../Items-Equipment-Shops-And-Licenses/equipment-list.md) whose
   `model_id` names the model, by their category and name.

### Shipped data

| Fact | Value |
|---|---|
| models | 327; 326 ship with an `@FTR`, an `@FCP` and a section 1, and `w2123` does not ship |
| `j_blade` | 185 of the 326 |
| `n_grip` | 284 of the 326 |
| node counts | 2 nodes on 98 models, 3 on 182, 4 on 19, 5 on 26, and 16 on the spear `w5003` |
| key sets | `0x1D 0x656 0x65E` 180; `0x1D 0x656` 57; `0x1D 0x1E` 41; `0x1D 0x656 0x1D00 0x1CFF 0x1CFD` 16; `0x1D 0x656 0x658 0x657` 13; `0x1D 0x656 0x1D00 0x3C5A 0x3C5B` 8; ten others on 11 models. `0x1D` (`model`) is on all 326 |
| special ids `0x104`-`0x106` | `0xFFFF 1 0` on 284; `1 0xFFFF 0` on the 41 `0x1D 0x1E` models; `0xFFFF 0xFFFF 0` on the mace `w2302` |
| special ids 0-31 | no bone on 281; id 14 is bone 2 on 23; ids 0-8 are bone 1 on 20; id 13 is bone 0 on 2 |
| equipment | 373 rows name 295 of the models; 32 are named by no row |

By category:

| Category | Models | Without `j_blade` | Without `n_grip` |
|---|---:|---|---|
| Sword (1H), Sword (2H), Dagger, Axe, Hammer, Katana, Ninja Sword, Rod, Staff, Measure, Hand-bomb | 132 | 0 | 0 |
| Mace (1H) | 13 | `w2302`, whose keys are `0x1D` and `0x66C`-`0x66E` | `w2302` |
| Spear (2H) | 15 | `w5003` (`0x656`, `0x657`, `0x658` and twelve keys `0x18B4`-`0x18BF`), `w5020` (`0x1D 0x1E`) | `w5020` |
| Pole (2H) | 13 | 12 | 0 |
| Bow (2H) | 14 | all | 0 |
| Crossbow (2H) | 9 | all | `w8002`, `w8003` |
| Gun (2H) | 15 | all | `w1018` |
| Arrows | 8 | all | 0 |
| Bolts | 10 | all | `w8209`, `w8210` |
| Shot | 9 | all | 8 (`w8301`-`w8308`) |
| Incendiaries | 8 | all | all |
| Shield | 32 | 22, which carry `0x1D 0x656` (`n_grip` only); the ten others carry both points | 0 |
| Unarmed | 17 | all, `0x1D 0x1E` models | all |
| no equipment row | 32, `w2123` among them | 14 of the 31 shipped | `w1004`, `w1010` |

One model is used by both Katana and Sword (1H) rows; the table counts it once, in the first row.

## Columns

| Column | Meaning |
|---|---|
| `bound_id`, `name`, `cm` | the bound id, the model's name and its `.cm` path |
| `categories`, `equipment` | the equipment categories and the names of the equipment rows that use the model; `categories` is `-` when no equipment row uses it |
| `ftr_nodes`, `keys` | the `@FTR` node count and the node keys |
| `j_blade`, `n_grip` | whether a node has the key `0x65E` or `0x656` |
| `special_bones_0_31` | the set entries of section 1's special-id table, as "id: bone"; `-` when every entry is `0xFFFF` |
| `special_bones_104_106` | the set ones of special ids `0x104`-`0x106`, as "id: bone"; `-` when all three are `0xFFFF` |
| `note` | "not shipped" for a model whose `.cm` the archive lacks |

## Related

- [Model asset list: every model the game can bind, with its model file, motion lanes, remastered parts and the tables and scripts that use it](model-asset-list.md)
- [Model files (.cm, .ca)](model-files-cm-ca.md): `@FTR` and `@FCP`
- [Character render records](character-render-records.md): attach slots and default bones
- [Skeleton entries and bones](skeleton-entries-and-bones.md): bone points and their ids
- [Effect anchors and targets](effect-anchors-and-targets.md): the anchor query that uses the two points

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x003A4290` calls `0x00263C30`, `0x00263FF0`, `0x00358940`, `0x003589B0`; those functions are documented on
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Audio: `0x00421E20` is called by `0x00332C40`, `0x003B99D0`; those functions are documented on
  [animation sounds](../Sound-And-Music/animation-sounds.md), [effect anchors and targets](effect-anchors-and-targets.md).
- Movement: `0x003A4290` calls `0x00264670`, `0x0026E350`; those functions are documented on
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [traps](../World-Areas-And-Travel/traps.md).
- Party: `0x003A4290` calls `0x003590D0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x00421E20` calls `0x002ED570`; those functions are documented on
  [resource sections](../Game-Files-And-Data-Tables/resource-sections.md).
