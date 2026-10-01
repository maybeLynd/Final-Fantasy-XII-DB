# Affected-consumer check: two FABLE claims on the actor-storage page struck on OPUS's controls (FABLE, Claude Opus 5.5, 2026-09-27)

Request: `OPUS-REQ-FABLE-EH4-1C-PRESETS-STRIKE`. OPUS carries both corrections in the EH-4 register row already; this is
the owning editor's page edit.

affected: 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md (seventeenth pass: the eight-indices claim and the protected-pair blockquote; fifth pass: the `+0x13` verb row, its blockquote and the 16-setter count)
run: eh4_1c_presets.py and eh4_lod_receiver.py (OPUS, _index/candidates/eh4-1c-presets/) re-run by FABLE at f4da22707, FAILS 0 each. R1/R2 of the first measure the presets that refute the eight-indices and protected-pair sentences; L1-L3 and R1 of the second measure the LOD verbs' receiver.

| consumer | what it said | state |
|---|---|---|
| `04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md`, seventeenth pass | `0, 4, 5, 6, 7, 14, 16, 17` "can only be arriving from `reqenable` / `reqdisable`"; "the engine protects two indices it never sets itself" | revised-here: both struck, correction beneath citing `00266BD0`'s presets (the page's own second pass) |
| same page, sixteenth pass | the clearer refuses to clear 4 and 5 while `+0x0C` bit 5 stands | agrees; the protection itself is not affected |
| same page, fifth pass table and blockquote | "`+0x13` the whole byte - `setlod` / `partysetlod` / `puppetsetlod`"; "`+0x13` IS THE LOD BYTE" | revised-here: row and blockquote struck, correction beneath (the verbs write `SecondaryContextElement +0x013`) |
| same page, fifth pass count | "123 short setters, 16 with a verb behind them" | revised-here: qualified - three of the 16 write the secondary context; 13 stand |
| same page, the `+0x13` bit table (bits 0, 1, 7) and the `&0x3C` / `cmp 0x80` readings | this record's `+0x13` bits | agrees; unaffected by the struck LOD reading |
| `_types/fields.tsv`, `SecondaryContextElement 0x013 lodLevel` | the LOD byte on the context | agrees |
| _index/OPEN-QUESTIONS.md EH-4 | both corrections already carried by OPUS | agrees; not revised here |
| SWE2-DATA's reqenable census conclusion (`OPUS-REQ-SWE2DATA-REQENABLE-CENSUS-EXEC-HALF`) | inherited the eight-indices premise | corrected by SWE2-DATA on the board 2026-09-27; not a page here |

Regenerated with it: nothing.
