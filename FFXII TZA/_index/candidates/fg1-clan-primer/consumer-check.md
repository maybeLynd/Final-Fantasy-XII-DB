# Affected-consumer check: FG-1 narrowed; the UI layout page's table global corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `fg1_clan_primer.py` beside this file (3 checks, FAILS 0).

The UI layout page's EC7-92 paragraph said `0037E5B0` bounds against "the `02A8D480`-rooted `+0xC8` table". Both
loads read `02AED490` (`0037E5BA`, `0037E658`), the hunt list's table owner. The rest of that paragraph (ordinal
counting by matching low byte) is right. FG-1's narrowing also names the Primer tabs 0–4 and 6 and reads the rank
table's two minimum counts.

| consumer | what it said | state |
|---|---|---|
| `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`, the `0037E5B0` paragraph | "`02A8D480`-rooted `+0xC8` table" | revised-here (struck; `02AED490` beside it) |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`, the Primer "Not read" line | tabs 0–4 and 6 unnamed; the rank minima unread | revised-here (struck clauses; tabs, hunt tab, minima beneath) |
| `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/hchk-hctg-hdat-handbook-indexes.md` | the six family bases and names | agrees (the tab names are joined through it) |
| `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md` (`menuquest`, the hunt list) | the table the hunt tab indexes | agrees |
| `_index/OPEN-QUESTIONS.md` FG-1 | open clauses | revised-here (PARTIAL, narrowed; the previous status kept as history) |
