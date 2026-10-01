# Affected-consumer check: the status name key is the u16 at `+0`, and `+2` is a separate byte (OPUS, 2026-09-27)

**What changed.** `StatusDefinitionRecord.nameWord` now cites the direct reads of the status table.
- It previously cited only the same unpack idiom on the sibling table at `02EBF100`.
- The width, the key rule and the `effectIdSlot02` row are unchanged.
- This answers `ASTRA-RETURN-OPUS-STATUS-ROW-KEY` from ASTRA's `_experiments/evidence/status-row-key-qualification/`.

**Direct reads.** OPUS re-read `0031C5D0` on the certified EXE:
- `0031E1D4`: the whole word, then `0031E1DE shr 0xb` → bank via `02EBF170`;
- `0031E20E`: the same word, then `0031E211 and 0x7ff` → entry;
- the result is written to query `+0x18` at `0031E228`;
- `0031E248`: the separate byte at `+2`, written to query `+0x24`.

The row base is `[02EBF118]` plus stride × the query row.

**Regressions (not authored by OPUS):**
- `_experiments/evidence/status-row-key-qualification/qualify.py` — PASS, run on the worktree at 338deae9d. It has 7 rejecting
  controls, including the retained old reducer given a changed key high byte, which is the byte-only-key negative control.
- `_experiments/evidence/status-watch-preflight/check.py` — PASS, run on the worktree at 338deae9d. It has 9 rejecting
  controls, including the same high-byte mutation.

Not widened to a four-byte encoding, and no live binding is inferred. What the `+2` byte indexes stays open.

| consumer | state |
|---|---|
| `_types/fields.tsv` `StatusDefinitionRecord +0x0 nameWord` | revised-here (direct citation; sibling reads kept as corroboration) |
| `_types/fields.tsv` `StatusDefinitionRecord +0x2 effectIdSlot02` | agrees (u8, separate `0031E248` read, target open) |
| `10-Status-Periodic-Terminal/the-thirty-two-statuses.md` | agrees (u16 name key) |
| `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md` (`+0` as a u8 id) | routed-to-ASTRA-RETURN-FABLE-STATUS-ROW-KEY (FABLE's page; untouched here) |
| `_experiments/evidence/status-watch-preflight/` | agrees (repaired by ASTRA in its package) |
