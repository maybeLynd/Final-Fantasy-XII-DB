# OPUS DD content work, folders 15–99: batch 2 (OPUS, 2026-09-30)

Board task `OPUS-DD-UNCLAIMED-15-99-0930`. Both pages had already been reconciled by SWE2-DATA's owner reads. What was
left was status currency and a few lines that still said "open" after their rows were answered.

## save-image-buffers-header-and-payload.md: PARTIAL → DOCUMENTED

Page: [save-image-buffers-header-and-payload.md](../../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md).

- **The status line** said "owner read pending, residue SD-40". SD-40 is answered (OPUS, `sd40-42-header-readers-0930`:
  nothing reads header dwords `0x12` / `0x13` back as fields). The line now says so and keeps UQ-271's SUPERSEDED
  pointer.
- **§5 call chain:** `003BB9B0` "(unread)" → "(read under FV-3, §7)".
- **§6 modding note:** the SD-40 answer, with the record's limits: an edit of the two dwords alone changes nothing a
  reader was found for, and the load follows payload `+0x1044`.
- **§8b:** "stays open as V-9" → answered in the next section, 2026-09-13.
- `documented_rule.py`: **READY-WITH-POINTER**.

## the-shared-drawing-context.md: PARTIAL → DOCUMENTED

Page: [the-shared-drawing-context.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md).

- **The status line** named SD-103, SD-104 and SD-105 as residue. All three are answered (OPUS `c2b5b9927`,
  `f2f55938a`), and the line now says so.
- **§3a's "does not answer GJ-2 … read-and-never-written"** and the blockquote after it are annotated with SD-103. The
  slots are the third qwords of rows 174–176 of the `+0x000` table, written by the row builder `002432B0` through
  `ctx + 24 × row`, which no fixed-displacement census sees. 24·174 + 0x10 = `0x1060`; 24·175 + 0x10 = `0x1078`;
  24·176 + 0x10 = `0x1090`.
- `documented_rule.py`: **READY**.

## Limits (OPUS)

- **No new measurement.** The status lines lean on SD-40 and SD-103..105, whose reviews are routed per their records.
