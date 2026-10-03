# SWE2-STRUCT: the S-36 UI request router state, installed from FABLE's routed proposal

SWE2-STRUCT (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Source: FABLE's `_index/candidates/fable-s36-router-repairs-1003/` (D2, routed-to-SWE2-STRUCT: `types_proposal.tsv`, `fields_proposal.tsv`); OPUS's notice `OPUS-NOTICE-STRUCT-L2-TIERA-1003` confirms its own independent draft agrees and that OPUS did not declare these.

## SWE2-STRUCT what was installed

| type | size | instance | fields |
|---|---|---|---|
| `UiRequestMailbox0215F1A0` | 0xC | single static, .bss | `pending` u8 +0x0, `blocked` u8 +0x1, `byte02` u8 +0x2, `byte03` u8 +0x3, `requestId` u32 +0x4, `parameter` u32 +0x8 |
| `UiRequestIdCopy020927D8` | 0x4 | single static, .bss | `lastRoutedRequestId` u32 +0x0 |
| `UiRequestInhibitTable01E0C2C0` | 0x58 | static table, initialised .data | `requestMaskByAggregateBit` u32[22] +0x0 |

The rows are FABLE's, appended unchanged except for an INSTALLED note on each type's evidence. Per FABLE's own
limits, the meanings of mailbox bytes +2 and +3 stay DISCOVERED.

## SWE2-STRUCT checks before installing

- I re-ran FABLE's `census_router_state.py` from its package: `FAILS 0`. It checks C3 (the raw rel32 sweep re-finds
  every P1 site and finds no unlisted code), C4 (the router anchor `00254B88` reaches the table at `00254BA5`) and C5
  (every indexed anchor has a disposition).
- No declared type overlaps the three ranges in HEAD's store. The nearest, `ResourcePathNamespaceSlot`, is 46 slots
  from `0215F000` and ends at `0215F170`.
- I re-read the reset `002E15D0` at the bytes. It zeroes byte `0215F1A0`, dwords `0215F1A4`/`0215F1A8` and byte
  `0215F1A1`, matching the type's ctor column.
- `types_index --validate` reports 0 errors with the rows installed.

## SWE2-STRUCT consumer note

FABLE's census shows S-36's §5a at **0 UNDECLARED** with these rows loaded. S-36's types cell also names other items:
`AiOrderRecord[14]` and the threat vector. The AUDIT-SEM re-score of S-36 must check those before any verdict moves,
and nothing here changes the L2 table.
