# Consumer check: falsification pass 1 on loader-bound-bin-families (OPUS, 2026-09-29)

corrects: 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md (§3 the behind-camera preset is script-settable; §1 texpack's null check; §2 fontpack_it's walk count and fontpack_fs's slot 0)
corrects: 02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md (§2 fontpack_it slot 1: 0016D6A0 is `ret 0`, not an allocation - follow-up, CON-166)

## What was corrected

- **The behind-camera preset.** The selector setter `0025A160` has three calling functions:
  - `00304060` (call site `003040B7`);
  - `00304140`;
  - `00356CB0`, the native of script verb `setbehindcameratype` (`0x01CB`).

  So "player-authored through the settings data, not per-area" does not hold. Whether shipped scripts call the verb is not
  established. The setter's bound is signed and upper-only. `CON-163`.
- **Three stale rows** (`CON-164`):
  - texpack's idempotence cell is `0208EA88`; `[*(0209AC30)+0x3D8]` is the tex2pack blob, tested by `00280670`;
  - `fontpack_it`'s callback reads all eight directory dwords;
  - `fontpack_fs`'s dir 0 binds `+0x08` only.
- **Made exact.**
  - The 23-entry MRP relocation loop is `00280980`.
  - `00259370` takes the blob in `ECX`, a 32-bit value.
- **What survives.** The lazy loaders and their request codes, the tex2pack and clutpack binders, the `fontpack_it` slot map,
  the `fontpack_fs` faces and flags, and the `fontcolor` and `monotone_chr` binds.

- **Follow-up (`CON-166`).** The `fontpack_it` slot-1 row called `0016D6A0` an allocation. It is `ret 0`, three bytes, with
  2,868 call sites. The query-record pass found it (`falsify_query_record.py` Q6).

## Current consumers

- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-163`, `CON-164`, `CON-166`).
- consumer: [game-application.md](../../../00-Engine-Core-Runtime/Application-Root/game-application.md) agrees. It already cautions that
  `0016D6A0` is a folded `ret 0` leaf.
- consumer: [the scripted-camera player](../../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md) agrees.
  It documents `resumebehindcamera` and `lockbehindcamera`, and makes no claim about the preset's source.
- consumer: [PS2-Image-Data-Formats/README.md](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/README.md) agrees.
  It names `behindcamera` as a family and makes no claim about the preset.
- consumer: [the verb table](../../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) agrees. Row `01CB` already
  binds `setbehindcameratype` to `00356CB0`.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_loader_bound.py`, checks B0-B8.
- B6 fails if the setter loses the verb caller, or if `00356CB0` stops being `setbehindcameratype`, which rejects "not
  per-area".
- B0, B2 and B3 pin the three rows.

run: verified at ba0ab89c9 (BROKEN 0), against the certified image `73461d08…`.
