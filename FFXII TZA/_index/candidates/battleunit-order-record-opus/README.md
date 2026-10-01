# BattleUnit's committed and issued order records (OPUS, 2026-09-28)

**Question.** Is `BattleUnit +0x708` (ctype `ptr`) typed, and are the four rows at `+0xBA0..+0xBB7` right? The rows at
`+0xBA2` and `+0xBA6..+0xBB7` said "unaccessed".

**Discriminator.** Follow the pointer, not the displacement: what `BattleUnit_CommitAction` receives, where it keeps it,
and what reads through it.

**Answer.** [`order_record.py`](order_record.py) ([output](order_record.out)), static on the certified image: FAILS 0. W
failed before the patch.

- **P.** `BattleUnit_CommitAction` (`0030F760`) keeps its second argument in `r12` and stores it at `unit + 0x708`
  (`0030F7F9`). It reads no field of the record itself.
- **S.** Its five callers pass:
  - a gambit set's record, `set + 0x20 + 0x18k` (`00305DE0`);
  - the unit's own `+0xBA0` (`00305B19`);
  - the static records `01EEC298` and `01EEC2B0` (`00305C86`, `003130CB`);
  - the current `+0x708` itself (`0030FA4D`, a re-commit).

  So `+0x708` is an **`AiOrderRecord*`**: the committed order record.
- **I.** `BattleUnit_IssueCommand` writes the action id at `+0xBA0` (`00311D7A`) and ORs 0x8000 into `+0xBA4`
  (`00311DBB`). When unit flag 0x4000 is set, `SelectAndCommitNextAction` clears it and commits `unit + 0xBA0`, with the
  commanded target `+0xBB8` (`00305AE4..00305B2F`). So **`+0xBA0..+0xBB7` is an embedded `AiOrderRecord`**: the issued
  command's order record. Its size is exactly the record's 0x18.
- **R.** BattleUnit bodies read through `+0x708`:
  - +2 as a signed word;
  - +4 tested for 0x2000, 0x200, 0x100, 4 and the sign bit;
  - +6.

  The gambit walk compares candidates against it by pointer identity and tests its +4 for 0x4000. **The sign test (`cmp
  word [rax + 4], 0; jl`, `00308736`, `00328604`) reads exactly the 0x8000 that IssueCommand sets in `+0xBA4`.**
- **D.** The static records are in `.data`:
  - `01EEC298` = `{0x4021, 0, flags 0x2000}`;
  - `01EEC2B0` = `{0x0096 (Attack), 0, flags 0x2000}`;
  - `01EEC2D0` has AiOrderSet's head shape: count 1, then one Attack record at +0x20 with selector0 = 10. IssueCommand
    installs it at `+0x6F8`.

**Correction.** The "unaccessed" rows were displacement-census artifacts. The bytes at `+0xBA2` and `+0xBA6` are read at
record +2 and +6 through `+0x708` whenever the issued record is the committed one. The four rows become one embedded row,
`issuedCommandOrder AiOrderRecord`. FABLE's names are kept in its text, mapped field by field, and the old rows are quoted
whole in its evidence.

**Not claimed:**
- who writes the issued record's +2 and +6..+0x17 (nothing in IssueCommand does);
- `01EEC2D0`'s full extent as a set;
- the flag bits' meaning;
- `001CC515` and `0042016B`, which load `+0x708` of an object not proven to be a BattleUnit.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` BattleUnit `+0x708` | ctype `ptr` → `AiOrderRecord*`; its sources and readers stated | revised-here |
| `_types/fields.tsv` BattleUnit `+0xBA0`, `+0xBA2`, `+0xBA4`, `+0xBA6` | re-cut into one embedded `AiOrderRecord` row, old rows quoted | revised-here |
| `_types/types.tsv` `AiOrderRecord` instance cell | names BattleUnit `+0xBA0`, `01EEC298`, `01EEC2B0` and `01EEC2F0` | revised-here |
| `_types/recoverable-layout-gaps-dispositions.tsv` BattleUnit `0xBA4` ("+0xBA2 and the tail ... no access") | qualified: direct displacements only; read through `+0x708` | revised-here |
| `the-battle-unit-field-map.md` rows `+0x708` (ctype `ptr`) and `+0xBA0` (`issuedCommandActionId`) | should name the record types | routed-to-SWE2-DATA |
| FABLE's BattleUnit names (bfcb07e) | kept inside the new row, field by field | routed-to-FABLE (notice) |

This is OPUS's own check; independent acceptance is requested separately.
