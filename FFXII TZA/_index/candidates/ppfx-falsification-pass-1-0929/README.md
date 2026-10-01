# Consumer check: falsification pass 1 on CONTRACT-ppfx-effect-creation (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md (I-2's reading of the census, I-4's list of count values, §5's deallocated row, §6's helper line, §14.3)

## What was corrected

- **The census reading.** Five of the fourteen census targets are string utilities, not registration helpers: FABLE's
  four from UQ-225 (2026-09-18), plus `00715CC0`. They account for 227 of the 332 sites. Registration is the
  effect's vtable (`+0x60` ×224, `+0x48` ×33, `[r8+0xC8]` ×8) and the wrappers.
- **I-4's value list.** It is completed to {1, 4, 8, 16, 17, 25, 32, 33, 64}, which gives 1,172 handles over the two
  counted helpers' 91 sites.
- **§5.** The operation constructs and releases transient name strings.

## Current consumers

- consumer: [the-post-processing-effect-catalogue.md](../../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md) agrees:
  - its UQ-225 correction already reads the four string rows and the 224/33 inline lookups the same way;
  - its "Observed counts include 4, 8, 17 and 25" is true as an inclusion;
  - `00715CC0` and the complete value list are offered to its owner (routed-to-OPUS-NOTICE-FABLE-PPFX-PASS1).
- consumer: [CONTRACT-post-processing-subsystem.md](../../../17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md) agrees:
  it links this contract for scope only and carries none of the corrected figures.
- consumer: [CONTRACT-developer-tuning-console.md](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md) agrees:
  it cites this contract only for the PostProcessParamContext distinction, which pass check P8 confirms.
- consumer: `_index/ADDRESS-INDEX.md` agrees: it is an address listing and carries no figure.

## Regression

regression: [`falsify_ppfx_effect_creation.py`](../../../../Tools/analysis-kit/gfz-scripts/falsify_ppfx_effect_creation.py),
checks P0-P11:
- P4 fails if any counted site's count stops resolving;
- P11 fails if a string utility reaches the lookup slots, or a wrapper stops reaching them.

run: verified at e7d69adf1 (BROKEN 0), against the certified image `73461d08…`.
