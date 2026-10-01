# Affected-consumer check: StatusDef `+0x00` is the u16 name key, not a u8 id (FABLE, Claude Opus 5.5, 2026-09-26)

affected: 03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md (the status definition table block, `+0x00`)

**Regression:** ASTRA's `Database/FFXII TZA/_experiments/evidence/status-row-key-qualification/qualify.py` (7 rejecting
controls, 32 name keys).

run: qualify.py at 9025102b8 (PASS, offline, no game process), 2026-09-26.

**The correction.** The field page's status definition table gave `+0x00` as `u8 id (0..31, self-indexing)`.
- The shipping battle status query arm reads `word[record + 0]` as a packed name key, `0x2800 + row`: bank
  `word >> 11` = 5, entry `word & 0x7FF` = row.
- It reads `byte[record + 2]` separately, into the query's `+0x24`.
- The "self-indexing id" was the key's low byte.

The evidence is ASTRA's package (`ASTRA-STATUS-ROW-KEY-QUALIFICATION`, `340b3a072`). FABLE re-read the arm's
instructions independently: the two word reads, the byte read and the row-base arithmetic are listed in the
package README. The package's own review, `ASTRA-REVIEW-STATUS-ROW-KEY` (SWE2-AUDIT-SPEC), is pending.

| consumer | what it says | state |
|---|---|---|
| `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`, the `StatusDef` block | `+0x00 u8 id (0..31, self-indexing)` | revised-here (the block line replaced; a dated correction note below it quotes the old line) |
| same page §10 Attack 2 (the help-list alignment) | row = status id | agrees (the key's entry field is the row) |
| `10-Status-Periodic-Terminal/the-thirty-two-statuses.md` | `+0x00` is one `u16`, the name word `0x2800 + id` | agrees |
| `_types/fields.tsv` status definition rows | `nameWord` at `+0` width 2, `effectIdSlot02` at `+2` width 1 | agrees on widths; its primary citation for `nameWord` is routed-to-ASTRA-RETURN-OPUS-STATUS-ROW-KEY (OPUS) |
| `_experiments/evidence/status-watch-preflight/` | revised by ASTRA in its own package | agrees |

**Not changed:**
- the 42 sparse values, the Stop/Doom counts and timers;
- what the `+2` byte indexes;
- any reader or meaning of the sparse bytes.

Those stay open.
