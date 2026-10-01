# Consumer check: falsification pass 1 on the-settings-command-table (OPUS, 2026-09-29)

corrects: 19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md (section 2 Defaults: CON-193; sections 3 and 5, command 11: CON-194)
corrects: 19-Save-Load-Settings/Game-Settings-Config/members/settings_command_table.tsv (command 11's getter: CON-194)
corrects: 19-Save-Load-Settings/Game-Settings-Config/members/gen_settings_commands.py (command 11's getter: CON-194)

## What was corrected

- **CON-193.** The defaults template's second dword is `0x00620400` (bits 10, 17, 21, 22), and dword0 bit 12 is set for
  language ids 1 and 6. The installer also clears the speed-mode field, sets the soundtrack to 1 and all three volumes
  to 100.
- **CON-194.** Command 11's getter reads the live word only while it is non-zero, and otherwise returns NOT opt+0 bit 12.

## Current consumers

- consumer: `_index/_inbox/SWE2-AUDIT-SPEC.md` quotes `0x62000400` in an earlier review record. That is review history,
  not a canonical page; it is not edited, and this record supersedes the value.
- consumer: `19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md` - checked by grep for
  the template value and `00229E40()==6`; no match, so it agrees.
- consumer: `19-Save-Load-Settings/Game-Settings-Config/members/settings_command_table.tsv` and its generator
  `gen_settings_commands.py` hard-code command 11's getter as `u16[0215E6DC] bit 0`; revised-here in both (`CON-194`).
  They carry no defaults, so CON-193 does not touch them.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-193`, `CON-194`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_settings_commands.py` C3 and C4. C3 fails unless the
template's second dword is `0x00620400` and `002DDE60` tests ids 1 and 6 before setting bit 12. C4 fails unless
`002DDD70` branches on a zero live word to NOT opt+0 bit 12.

run: verified at b05d44b1d (BROKEN 0, exit 0), against the certified image `73461d08…`.
