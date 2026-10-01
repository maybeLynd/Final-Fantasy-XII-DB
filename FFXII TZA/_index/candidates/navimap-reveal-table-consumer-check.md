# Affected-consumer check: `ImageBackedStateBlock +0x224` is the navigation-map revealed-tile table (OPUS, 2026-09-27)

**What was wrong.** The type store still called the `0x180 × 0x20` table at block `+0x224` (payload `+0x8224`) an
"achievement / counter entry table" and ranked it SEMANTICALLY IDENTIFIED.
- FG-1 (FABLE, 2026-09-12) had answered it as the navigation maps' revealed-tile bitmaps.
- The save-payload field map had already struck the old reading.
- The store row carried it forward when OPUS settled its extent on 2026-09-16.

OPUS re-read the primary bytes:
- `003C5410` clears `02B45978`, and `002551B0` copies the current map's entry into it.
- The absent case fills it with `0xFF` (`003C54B6`–`003C54C2`).
- `003C5500` sets bits in it (`bts` at `003C56B8`).

Corrects: `_types/fields.tsv` (`ImageBackedStateBlock +0x224` meaning, and its name `achievementCounterEntryTable` → `navimapRevealedTileTable`).

Regression: `_index/candidates/fg1-clan-primer/fg1_clan_primer.py` covers the block's layout (FABLE). The re-read
above is static, and no new control is added for a meaning restatement that follows an already-published answer.

| consumer | state |
|---|---|
| `_types/fields.tsv` `ImageBackedStateBlock +0x224` | revised-here |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md` line 214 | agrees (already struck) |
| `_index/OPEN-QUESTIONS.md` FG-1 table half | agrees |
| `_index/AUDIT-LOG.md` (the old name) | history |
