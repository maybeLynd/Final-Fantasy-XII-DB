# Affected-consumer check: PC-1 narrowed; "pad capability" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `pc1_ff12config.py` beside this file (4 checks, FAILS 0).

The settings command table said `002DDA30` forces command 9's bit "from a pad/vibration capability query",
`00408B80()`. `00408B80` is a plain byte getter of the loaded `FF12CONFIG` copy (`+0x06`), not a device query, and
`00408B40` reads `+0x10` the same way. Their one caller is `002DDA30`, so the "force" is the config file's
`opt06`/`opt10`. Both are 0 in the shipped file.

| consumer | what it said | state |
|---|---|---|
| `19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md`, the platform-applier paragraph | "forces cmd 9's bit from a pad/vibration capability query" | revised-here (struck; corrected beside it) |
| same page, command 9 row | "`00408B80()` (pad capability)" | revised-here (struck; corrected beside it) |
| same page, command 10 row | "`002DDA30` forces from `00408B40()`" | agrees (no device reading claimed) |
| `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md` §7 `PC-1` | open; bits 13 and 14 "not named"; which callers enter with 1; field id 236 | revised-here (narrowed: bits named by reference, the entry with 1, field 236 "Throne Road") |
| `_index/OPEN-QUESTIONS.md` PC-1 | OPEN | revised-here (PARTIAL, narrowed; the previous status kept as history) |
