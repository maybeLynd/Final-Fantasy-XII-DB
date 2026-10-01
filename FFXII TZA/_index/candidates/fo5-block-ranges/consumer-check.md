# Affected-consumer check: FO-5 answered; five battle-state rows re-placed as stats-record fields (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `fo5_block_ranges.py` beside this file (5 checks, FAILS 0).

The battle-state block's field map listed `+0x2E5D`, `+0x2EA8`, `+0x2EAA`, `+0x2EC1` and `+0x2ED1` as block fields.
The first was called "one function's private fields, unread", and the others "not named by any page". They are
fields `+5`, `+0x50`, `+0x52`, `+0x69` and `+0x79` of stats record 26. The reader forms block `+ 0x2E58` (record 26)
and reads relative to it. The rest of FO-5's two ranges is placed, as stats records 25–39, inventory backup B, the
unused mirror tail and the two descriptor regions.

| consumer | what it said | state |
|---|---|---|
| `11-Party/Battle-State-Block/the-battle-state-block-field-map.md` §2.3, row `+0x2E5D` | "one function's private fields, unread" | revised-here (struck; record 26's `+5` beside it) |
| same table, rows `+0x2EA8`, `+0x2EAA`, `+0x2EC1`, `+0x2ED1` | "not named by any page" | revised-here (dated note: record 26's `+0x50`/`+0x52`/`+0x69`/`+0x79`) |
| same page §7, `UQ-127` | open | revised-here (ticked; the placement beneath) |
| same page §2.2 (forty `0x1C8`-byte records from `+8`) and §2.8 (region A, the class descriptors) | the layout | agrees (the answer rests on it) |
| `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` (the `+0x57C0` and `+0x57C8` regions) | items' region C, loot's region B | agrees |
| `_index/OPEN-QUESTIONS.md` FO-5 | OPEN | revised-here (ANSWERED; the previous status kept as history) |
