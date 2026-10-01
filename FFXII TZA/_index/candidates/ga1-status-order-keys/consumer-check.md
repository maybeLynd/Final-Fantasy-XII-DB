# Affected-consumer check: GA-1 — the status order keys, and `+0x13`'s omitted set (FABLE, Claude Opus 5.5, 2026-09-26)

affected: GA-1; 10-Status-Periodic-Terminal/the-thirty-two-statuses.md (the GA-1 box: the `+0x13` bullet and the copied-bytes bullet)

**Regression:** `ga1_status_order_keys.py` beside this file (7 checks, FAILS 0).

run: ga1_status_order_keys.py at 1e5ab1ec0 (FAILS 0), 2026-09-26.

**The correction.** FABLE's 2026-09-15 text said `+0x13` was "the row's own index" and `0xFF` in exactly KO,
Invisible, HP Critical and X-Zone, and it called that set a fourth independent confirmation of the row join.
- The retained table (`status-row-key-qualification/status-table.bin`, sha256 `c5ea6807…`) has `+0x13 = 0xFF` for KO,
  **Stone**, HP Critical and X-Zone.
- Invisible carries `05` at `+0x13`. The KO / Invisible / HP Critical / X-Zone set belongs to `+0x02`.
- `+0x13` equals `+0x10` wherever it is present. It is the display index, not the row id.
- The "fourth confirmation" rested on reading the two sets as one, and is withdrawn. The row join stands on the name
  key at `+0x00`.

**The narrowing.** The five bytes `+0x02`, `+0x10`, `+0x13`, `+0x26` and `+0x27` are order keys for five status
listings, and `0xFF` omits a status. KO, Invisible, HP Critical and X-Zone never queue a battle status reaction.
Sensitivity: K7 shows the old `+0x13` reading fails against the table.

| consumer | what it says | state |
|---|---|---|
| `10-Status-Periodic-Terminal/the-thirty-two-statuses.md`, GA-1 `+0x13` bullet | "the row's own index"; `0xFF` in KO, Invisible, HP Critical, X-Zone; "a fourth independent confirmation" | revised-here (struck and corrected) |
| same page, "what its value selects is not read here" | the copied bytes' meaning unread | revised-here (the order-key table and the four readers added) |
| `_index/OPEN-QUESTIONS.md` GA-1 | the same `+0x13` set and confirmation claim in the 2026-09-15 narrowing | revised-here (status restated PARTIAL with the correction; history kept) |
| `_types/fields.tsv` `StatusDefinitionRecord` `+0x02` `effectIdSlot02`, `+0x10` `armCopiedByte10` and siblings | "copies ... into the applied status record" | routed-to-FABLE-REQ-OPUS-STATUS-ORDER-KEY-FIELDS (the target is the class-26 query record; the bytes are listing order keys, `0xFF` = omitted; the name `effectId` is not supported) |
| `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md` status block | `+0x02` a separate byte, meaning open | agrees (it claims no meaning; this record now supplies one) |
| `00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` "the licence bytes `+0x21`–`+0x25` (class 25 / 32) are read by `00275E40`, `002D02C0` …" | licence readers | routed-to-FABLE-REQ-OPUS-STATUS-ORDER-KEY-FIELDS as a note: `00275E40` and `002D02C0` query class 26 (`mov ecx, 0x1a`), so at those two sites the bytes are status keys; the page's census did not split by class |

**Open, unchanged:**
- `+0x11`–`+0x1D`;
- which reader turns `+0x08` into the running timer;
- which on-screen list each kind is.
