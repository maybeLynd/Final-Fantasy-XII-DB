# RC-6: the two console map codes that differ from map_ref.bin: a pack cut from the build, and a variant pack (ORACLE, 2026-09-30)

Input for `RC-6` ([the second console table](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/the-second-console-table.md),
what the table holds). SWE2-CONTRACT registered the row. Static evidence from the shipping image (`73461d08…`) and
authored data (`map_ref.bin`'s decoded rows, the shipped archive). **Verdict: ANSWERED as far as authored data goes;
the residue is authoring intent only.**

## The question

The developer console's authored-code table (`01DF6E68`, 1,314 entries indexed by field id) names the field's own map
pack for 599 of its 601 populated entries. Two entries differ:
- **entry 670:** the table says `rbl0102`, and `map_ref.bin` gives the field `rbl0121.mpk`;
- **entry 1003:** the table says `gil0301`, and `map_ref.bin` gives `gil0303.mpk`.

Why?

## Method

[`rc6_packs.py`](rc6_packs.py), output [`rc6_packs.out`](rc6_packs.out), FAILS 0.

It names each field's own pack from the image itself, not from file sizes. `g_pathTables[4]`, the pack path table that
`ResourcePath_Init` (`002DF9A0`) installs, is the same array (`01E5E500`) in all 13 region arms. Its row *n* is the path
of pack index *n*. The script replays that function through [`rc5_paths.py`](rc5_paths.py), copied from the RC-5
record.

Each field's own-pack index comes from `map_ref.bin`'s decoded rows (`map-ref-field-packs.tsv`, column `own_idx`).
Four checks:
- **K1:** join the console table with the kind-4 name of each field's own pack index.
- **K2:** read the kind-4 rows around the two packs.
- **K3:** read the `map_ref` rows of the neighbouring fields and of every field that owns the packs involved.
- **K4:** check the shipped archive for entries naming each code, and the map codes embedded in `gil0303.mpk` and
  `gil0301.mpk`.

Controls:
- K1 must reproduce SWE2-CONTRACT's join (599 agree; 670 and 1003 differ). It does, now with names read from the
  image's own table instead of size-matched ones.
- Kind-4 rows 0 and 1 must be `ous0100.mpk` / `ous0101.mpk`.

## Result

**670 (`rbl0102`): the build's pack table has no `rbl0102`. Its slot is empty, and the field was pointed at another
pack.**
- In the kind-4 table, the `rbl01` packs sit at row 702 + map number: 702 is `rbl0100`, 703 is `rbl0101`, 705 is
  `rbl0103`, and so on.
- **Row 704, the `rbl0102` slot, is empty (NULL).** So are 716, 720, 722, 724 and 725, the slots for `rbl0114`,
  `rbl0118`, `rbl0120`, `rbl0122` and `rbl0123`.
- `rbl0102` is the only one of the 601 console codes with no row anywhere in the pack table.
- `map_ref.bin` still has two fields, 44 and 1112, whose own-pack index is 704, the empty slot.
- Field 670, and its pair 671, own pack index 723, which is `rbl0121`. So do fields 122, 683 and 1230.
- In the shipped archive the code survives only as an effect bank, `ps2data/efb/rbl0102.efb`. There is no pack and no
  map JSON.
- So the map `rbl0102` was cut from the pack table, while `map_ref.bin` repointed field 670 to `rbl0121`. The console
  table still carries the cut code.

**1003 (`gil0301`): field 1003 uses a variant pack of the map the console names.**
- Fields 1000 to 1007 all own `gil0301.mpk` (pack index 678), except 1003, which owns `gil0303.mpk` (index 680).
  1003 is the only field that owns that pack.
- The console table gives 1002, 1003, 1004 and 1005 the same code, `gil0301`. In `map_ref.bin` those four fields also
  share `w2` 275 and `w3` 43.
- `gil0303` ships a pack, an effect bank and a map JSON.
- Its embedded map codes, `gil0101`, `gil0201`, `gil0301`, `ink0301` and `mrm0200`, are `gil0301.mpk`'s set minus
  `ucf3111`. It is built on `gil0301`'s content.
- So the console table names the map (`gil0301`), and `map_ref` names the pack that field 1003 actually loads.

**How this relates to FABLE's record** ([`rc789-fable-0930/`](../rc789-fable-0930/README.md), RC-6):
- The two records agree on both facts.
- This record adds the image's own evidence, the kind-4 pack table:
  - the empty `rbl0102` slot 704;
  - the two `map_ref` fields that still point at it;
  - the 599-of-601 join, reproduced with image-named packs.

## Residue and not claimed

- **Authoring intent is the residue.** Nothing in the image or the data says why the two entries were left so: an
  unregenerated table, or a deliberate naming of the base map. Neither A/B nor original code can settle it, and no fact
  that ASTRA could observe would either.
- **Loading a cut code.** What the console does if entry 670's code is used to load a map was not read.
- **Other fields.** The fields that own the other empty `rbl01` slots were not examined further. Their console entries
  are empty.
