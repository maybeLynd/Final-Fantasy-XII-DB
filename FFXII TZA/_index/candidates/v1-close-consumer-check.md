# Affected-consumer check: V-1 answered, and PersistentFlagPayload +0x1534 split by AA-8 (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling.** `v1_embedded_census.py` runs the all-routes census over every UNKNOWN span inside the embedded types.
- Before the split: 378 spans / 1,935 B, and only `+0x1534` is touched.
- After the split: 378 spans / 1,933 B, and none is touched.

Together with the top-level result (`22d38ec57`), every UNKNOWN payload byte is reached by no entry route. That is
reserved space in AA-5's sense.

**Store change.** `PersistentFlagPayload +0x1534 tailBytes1534 u8[4]` becomes three rows, per AA-8's accepted answer:
- `savedMusicOverride` u8;
- `writeOnlyByte1535` u8;
- `unobservedTail1536` u8[2].

The previous evidence is kept inside the new row.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` V-1 | NARROWED → ANSWERED, prior status kept | revised-here |
| `_types/fields.tsv` PersistentFlagPayload `+0x1534` | split | revised-here |
| `14-Story-Event-Quest-Hunt/persistent-flag-banks.md` / AA-8 | already states the three parts; no change | agrees |

Corrects: _types/fields.tsv

Run receipt: `v1_embedded_census.py` executed at 3f61049ee (controls_pass true; 0 touched after the split).
