# Affected-consumer check — status write §10 row 3: "party-type unit" is the Esper rows (FABLE, Claude Opus 5.5, 2026-09-26)

This is the correction on `OPUS-NOTE-FABLE-STATUS-WRITE-ROW3-IS-THE-ESPER-ROWS`. The shortcut's condition is kind
`+5 == 0` and type `+4` in `0x1B..0x27`. FABLE wrote that as "a party-type unit" and concluded that "a party member's KO
posts no rewards". The type range is exactly the **thirteen Esper rows** (27..39) of the 40-row party table. FABLE's
own FO-1 answer (2026-09-12) independently gives row `0x1B` as Belias, the first Esper.

`_index/candidates/s26-opus-replay-status-write/row3.py` was re-run by FABLE (ALL PASS, tree clean afterwards):
- types `0x1B` and `0x27` take defeat only;
- types `0x1A`, `0x28` and 0 take reaction, defeat and rewards.

So a party member's KO takes the full path, and only a summoned Esper's KO skips rewards.

| consumer | state |
|---|---|
| `10-Status-Periodic-Terminal/CONTRACT-status-write.md` invariant 2's exception and §10 row 3 | revised-here |
| `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md` summary item 2, the cleanup branch list, and the terminal-three bullet | revised-here |
| `_index/PARITY-STATUS.md` "the party-side shortcut" (generated) | not hand-edited; its label is the harness's, and "party-side" is not a wrong-scope claim about KO rewards |
