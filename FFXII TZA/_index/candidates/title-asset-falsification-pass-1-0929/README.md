# Consumer check: falsification pass 1 on the-title-asset-singleton-and-its-distinct-consumer (OPUS, 2026-09-29)

corrects: 16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md (section 7's restored note: CON-202)

## What was corrected

- **CON-202.** `00249320` is called for the title asset by the asset's own request body `00393FF0` (`00394048`), reached
  only from the asset's handler, and not by the `0x1D0` consumer `003939B0`, which makes no direct call to it.

## Current consumers

- consumer: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md` (the title row names
  `00393FF0` and `00394048`): agrees.
- consumer: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md` (the `00393FF0`
  row): agrees.
- consumer: `16-UI/Widget-Object-Model/the-widget-message-protocol.md` (the same factory, with no caller named): agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-202`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_title_asset.py` A8. It fails unless the title call is
`00394048` in `00393FF0`, `00393FF0`'s only caller is the asset handler, and `003939B0` has no direct call to `00249320`.

run: verified at cfc5a4863 (BROKEN 0, exit 0), against the certified image `73461d08…`.
