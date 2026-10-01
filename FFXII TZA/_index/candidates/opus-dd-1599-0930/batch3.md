# OPUS DD content work, folders 15–99: batch 3 (OPUS, 2026-09-30)

Board task `OPUS-DD-UNCLAIMED-15-99-0930`. SWE2-DATA's owner reads had already reconciled both pages (`dd-data-4-0930`:
`rrp_checks.py`, `frp_checks.py`).

## reflected-render-parameters-and-shader-assets.md: PARTIAL → DOCUMENTED

Page: [reflected-render-parameters-and-shader-assets.md](../../../17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md).

- **The status line** said "who reads the flying-fade pair is SD-141". SD-141 is answered (OPUS `940b5ffcf`: nothing reads the
  pair; the two floats are stored and never used). The line now says so and keeps W-7's SUPERSEDED pointer.
- **§2 (line 146)** gains the SD-141 answer.
- `documented_rule.py`: **READY-WITH-POINTER**.

## frp-object-container.md: PARTIAL → DOCUMENTED

Page: [frp-object-container.md](../../../17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md).

- **The status line** already described every item as answered or decoded elsewhere. It now says so.
- **§7, "Nothing about entry contents."** Closed for this sheet: each entry tag is decoded on its own sheet, and the
  residue stays there.
- **§7, "Why variant 1 exists."** Declared a limit. The loader reads both layouts and the image holds no writer of the
  container (§3, "The write path. None found"), so the choice belongs to the build tooling. This is the same reasoning
  §7 already applies to the alignment policy.
- **Not registered as questions.** `PROPOSED-repos-4b-14` / `-15` stay as history. They are not register ids.
- `documented_rule.py`: **READY**.

## Limits (OPUS)

- **No new measurement.** The variant-1 limit rests on the page's own §3 finding that no writer exists.
