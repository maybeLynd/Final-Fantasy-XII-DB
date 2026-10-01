# The Phyre asset container and its neighbours

| ext | files | size |
|---|---:|---:|
| `phyre` | 35,984 | 25,896 MB |
| `ah` | 2,564 | 11.7 MB |
| `ta` | 45 | 46 KB |
| `ker` | 34 | 470 KB |
| `fex` | 14 | 692 KB |

**`.phyre` is 40 % of the archive by count and 72 % by size, and its disposition is `external`.**

That is a decision, not an omission. [COMPLETION-PLAN.md](../../_index/COMPLETION-PLAN.md) §7 puts
re-documenting middleware from the file side out of scope: PhyreEngine is generic across titles and
its container is documented in `ffxii-tza-tools`. **Cross-link it.**

> **But `external` carries an obligation.** The database's stated unique contribution is the loader
> contract — what *this* build registers, rejects and ignores. An `external` row that stops at the
> cross-link has handed the reader to someone else's document and contributed nothing of its own.

That obligation is already partly discharged: the
[file/runtime schema join](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
checked 682 recovered field records against what 169 `.phyre` files declare, and its **22 unresolved
classes are the open edge of exactly this question**. §3b of that document establishes that the only
remaining route is runtime enumeration.

## `ah`, `ta`, `ker`, `fex` are **not** Phyre neighbours — corrected 2026-09-03

**This README's first draft filed all four as unknowns beside `.phyre` because they share a
directory. Sharing `gamedata/d3d11` turns out to mean very little.**

- **`.ah` and `.ta` are plain text**, both starting `/Gam…`. The binary shows what they are:
  `./GameData/D3D11/ArtData/font/jp/fontlist.ah` (`008F8188`) and
  `.\GameData\%s\ArtData\map\%s\%s_%s_srm.ah` (`008F6580`). **Asset list files**, for fonts and for
  maps.
- **`.ker` and `.fex` are font-system files.** Their only strings in the binary are the bare
  extensions at `008F81FC` and `008F8204` — **consecutive, eight bytes apart, immediately after
  `fontlist.ah` and `_shadow.dds.phyre`**. A small extension table sitting inside the font strings.
  `.ker` is almost certainly kerning data.

> **Neither belongs here.** They should move to 16-UI text rendering and the map/asset-list side of
> 02. Recorded rather than silently re-filed, because *"it was in the same folder"* is exactly the
> reasoning that put them here, and it should be visible where it failed.

`.phyre` at 35,984 files remains this folder's subject.

Write sheets to `_templates/FORMAT.md`. See
[_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md) §5.
