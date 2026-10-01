# Affected-consumer check: FR-2 answered; "the save's sidecar" and "what re-creates icon.sys" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `fr2_icon_pair.py` beside this file (5 checks, FAILS 0).

Two pages assumed the PS2 icon files are written beside the save:
- the shipped-formats page called the pair "the save's sidecar";
- the manual-save page asked what re-creates `icon.sys` and `static.ico`.

On PC nothing writes them. The save transaction deletes them. The `icon.sys` bytes feed only an in-memory PS2 image
that is built into the transaction record at state 7, and state 7 submits only the data file.

| consumer | what it said | state |
|---|---|---|
| `02-Resource-And-Asset-Pipeline/Standard-Formats/shipped-standard-formats.md` §6 | "The PS2 icon pair is not dead weight — it is the save's sidecar" | revised-here (struck; the correction beside it) |
| same page §7, `FR-2` | open: the routine that copies the pool files into a slot | revised-here (ticked; there is no such routine) |
| `19-Save-Load-Settings/how-a-manual-save-is-committed.md`, "Not read" | "what re-creates `icon.sys` and `static.ico` - which a short save also needs" | revised-here (struck; nothing re-creates them) |
| same page, the storage command table (`005826D0` delete-if-exists) | the delete | agrees (the control's I4 rests on it) |
| `_index/OPEN-QUESTIONS.md` FR-2 | OPEN; "Left: the routine that copies the pool icon files into a slot" | revised-here (ANSWERED; the previous status kept as history) |
