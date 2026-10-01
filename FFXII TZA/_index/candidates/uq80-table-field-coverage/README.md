# UQ-80: the row meaning of the authored tables, measured by a maintained instrument (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UQ-80):** "The contents of the other 26 slots": the row meaning of the authored tables behind the class slots,
beyond their names.

**What this record does.** `uq80_coverage.py` measures, for each of the 23 `st2e` tables in the us `battle_pack.bin`,
which bytes of the record have a stated meaning. It is re-runnable, and its only inputs are the exe, the function list
and the extract.

The 23 tables are:
- the 20 sections the UQ-80 box lists, where the key-item line is three sections;
- `eitm_data`, `status_data` and `action_data`.

Coverage comes from two sources, and `uq80_manifest.tsv` records every field with its source:
- **Existing pages.** Each such field names its page.
- **This pass (`PASS`).** Each field names its evidence: a reader instruction, the data tally, or both.

The run prints each table's coverage and a final residue line listing every unmapped (table, offset). It exits 1 on any
failed control.

**Result:** 15 of 23 tables fully mapped, and a residue of **60 unmapped bytes in 8 tables**, named:

| table | unmapped bytes | why |
|---|---|---|
| `chr_data` (40 × 128) | `0x07`, `0x08`, `0x09`, `0x2d`, `0x32`, `0x74`, `0x76`, `0x78`, `0x7a`, `0x7b`, `0x7c` | no reader found (`+0x07` and `+0x32` read but not decoded) |
| `m_daiji` / `g_daiji` / `q_daiji` | `0x00`, `0x01` each | a u16 with no reader in the slot-loading functions (`m_daiji`: equals the row index on 48 of 64 rows) |
| `menkyo_data` | `0x04` | no reader found |
| `eitm_data` (557 × 52) | 19 bytes in `0x06`–`0x33` | the `+0x18`..`+0x23` region changes layout by item kind; read but not decoded |
| `status_data` (32 × 40) | `0x11`, `0x12`, `0x14`–`0x1f` | no reader found (mostly `0xFF` / small ids) |
| `action_data` (543 × 60) | `0x04`, `0x0a`, `0x0b`, `0x1d`, `0x1f`–`0x21`, `0x28`, `0x3a` | the action page calls them shape only |

Fully mapped by existing pages before this pass: 4 tables (`gambit_data`, `eis_data`, `questreward_data`,
`attribute_data`). The four class slots that are not pack entries (`02EBF150`, `02EBF120`, `02EBF0D8`, `02EBF0D0`) are
named and not measured.

**The limit on "no reader".** Row pointers handed on to another function (91 call sites) are not followed. So "no
reader found" is bounded by this instrument, not an image-wide absence claim.

## FABLE's review of the reader's pass

**Spot checks.** Twelve `PASS` fields were drawn at random (seed 80) across tables. Every cited reader exists at the
stated address, with the stated width and displacement: for example `license_data +4` at `0031DEFB` and `0031E093`,
`eventitem_data +8` at `0031CC01`, and `chr_data +4` at `002F89F8`. Where no reader was found, the rows say so rather
than guessing.

**Corrected in review:**
- **`action_data +0x38` / `+0x39`.** The reader named it a "(family, tier) key". It is the action's menu position,
  low byte = page 0..10 and high byte = row 0..16, as the action page's 2026-09-18 narrowing establishes from the data.
  The reader found here, `00237FC0`, builds that page × row grid at `0208D308`, so this pass supplies the reader the
  page lacked.
- **`action_data +0x1C` and `+0x30`/`+0x31`.** These are credited from FABLE's BT-4 record: `+0x1C` is the category that
  `BattleAction_SelectPhasePresentationEvent` `0030A370` uses to index its event table; `+0x30` is the action's own
  presentation event, which `0030A370` returns.

**The reader's controls:**
- every shape and name, matched through the `01E4D830` table;
- stated counts reproduced: `price_data` 45 rows equal to 1; `questreward` rows 128–172; action `+0x15`..`+0x17` zero on
  all 543;
- three published row layouts re-derived, with a negative control;
- planted wrong answers rejected by the width, displacement and pad checks.

## Contradictions this pass found on other pages (verified by FABLE)

- **Encoded-id page, class 16.** It says `price_data`'s non-1 values run "from 30 to 11,160". The data runs 15..999,999
  over 83 rows.
- **Unit-definition page, line 129.** It says the registry "records its 456-byte rows" for the party table `02EBF130`.
  The registry now gives `chr_data` as 40 × 128. The 456-byte figure is the stats record, which lines 50 and 161 of that
  page describe correctly.
- **Action page, `+0x28`.** It says "the 26 Esper attacks". The 26 rows are ids `0xD0`–`0xE1`, the 18 Quickenings, plus
  `0xE2`–`0xE5`, `0xE7`, `0xEA`, `0xED` and `0xF1`, the 8 Concurrences. FABLE's own line; corrected in this publish.
- **`_types/fields.tsv` LicenseNodeRecord.** It says "the whole record … is honestly empty". The pages map `+2`
  (description id), `+4` (LP cost) and `+6` (square kind).
- **Not confirmed:** the reader's doubt about `CONTRACT-periodic-tick.md`'s `+6` timer slot. The contract names table
  `02EBF040`, which is consistent with the registry, so this is not routed.

## Files

- `uq80_coverage.py`, the instrument: `--write-coverage coverage.tsv`; stdlib + capstone.
- `uq80_manifest.tsv`.
- `coverage.tsv` and `coverage_run.txt`, today's run, FAILS 0.
- 23 `<table>-fields.tsv` files: tally, readers, meaning, evidence, source.
- `notes.md`, the reader's method.
- `trace.py`, the reader sweep. It reads the scratch instruction cache `y1p_all.txt` and is not needed to re-run the
  instrument.
- `pack.py`, `tally.py`, `joins.py`, `citecov.py` and `fields_emit.py`.
