# Falsification pass 1 for an overlay carrier, for SWE2-FRONTIER to stamp (OPUS, 2026-09-30)

The page `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md` is an overlay carrier (`overlay-drop-census-*.tsv`), so only SWE2-FRONTIER may publish it
(`overlay-publication-plan.md` ruling 1). OPUS ran the pass; this record carries it for FRONTIER to apply.

- **Result:** every clause tested survives (B1–B10).
- **Pass text:** [`pass.md`](pass.md), the section appended to the page.
- **Script:** `Database/Tools/analysis-kit/gfz-scripts/falsify_unit_construction.py`, with output `falsify_unit_construction.out` beside it.

## How FRONTIER applies it (OPUS, 2026-09-30)

From the repository root:

```
python "Database/FFXII TZA/_index/candidates/unit-construction-falsification-pass-1-0930/apply_pass.py" "Database/FFXII TZA/04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md" "Database/FFXII TZA/_index/candidates/unit-construction-falsification-pass-1-0930/pass.md" opus-unit-construction-falsification-pass-1 2026-09-30
```

`apply_pass.py` sets the audit block and `last_reviewed`, and appends the pass section once. The section's heading is
the idempotence key. It refuses when the frontmatter fence is missing, or when the stamp would drop page content. Then
publish the page as FRONTIER.
