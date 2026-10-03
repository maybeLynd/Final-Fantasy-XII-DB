# SWE2-STRUCT: SpawnCandidateRecord, the format-class-0 candidate record (S-16's last undeclared contract item)

SWE2-STRUCT (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Source: S-16's types cell (`auditsem-types-rescore-2-1003`) names two undeclared items. OPUS declared `SpawnKeepWindowSeconds0208936C` in `51ad88762`, and this record declares the other.

## SWE2-STRUCT the contract item

`05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md` §3 says: "the format-class-0 candidate record: byte `+0x00`
selects the mode, `+0x10` carries the authored position". The store had no type for it.

## SWE2-STRUCT evidence (raw capstone over the certified image)

- **The copy, `003DFD00`.** It is reached through `003209C0` with format class 0, and `003209C0` turns its 1/0 result
  into 0/-1 with `neg`/`sbb`.
  - It loads the table pointer `[02B59D48 + class*8]` and zeroes six qwords of the 0x30-byte output.
  - It returns 0 for a null table, or for an index not below dword `+0x0C`.
  - When the table's version byte `+7` is >= 0x33, it copies the 48-byte entry at `+0x10 + index*0x30`, three
    `movups` at `003DFD48`-`003DFD63`.
  - Otherwise it writes mode 0 (`003DFD6F`) and copies the 16-byte entry at `(index+1)*16` to `+0x10..+0x1F`.
- **Reader `00234AF0`.** Its buffer is at `rbp-0x69`. It reads the floats `+0x10`/`+0x14`/`+0x18` at
  `00234B5E`/`00234B63`/`00234B6C` and copies them to its output x/y/z. At `00234BC2` it compares byte `+0x00` with
  0, where `edi` is zeroed at `00234B37`.
- **Reader `002374E0`**, which receives the same buffer as `rdx`:
  - mode byte `movsx` at `00237505`, branching on 1 and 2;
  - floats `+0x04`/`+0x08`, each multiplied by 0.5 (`01CEBB70`) at `0023750D`/`00237515`;
  - in the mode-2 arm, floats `+0x10`/`+0x14`/`+0x18`/`+0x1C`.

## SWE2-STRUCT store change

`_types/types.tsv` gains `SpawnCandidateRecord` (0x30, STACK, ctor `003DFD00`). `_types/fields.tsv` gains these rows:

| offset | name | type | status |
|---|---|---|---|
| `+0x00` | `mode` | int8 | SEMANTICALLY IDENTIFIED |
| `+0x01` | gap | u8[3] | |
| `+0x04` | `float004` | float | |
| `+0x08` | `float008` | float | |
| `+0x0C` | gap | u8[4] | |
| `+0x10` | `position` | float[3] | SEMANTICALLY IDENTIFIED |
| `+0x1C` | `float01C` | float | |
| `+0x20` | gap | u8[16] | copied only for version >= 0x33 tables |

- Both contract-named items are declared at the granularity the contract names.
- The three unnamed floats claim only their widths and readers.
- `types_index --validate`: 0 errors.
- The edit script is `Tools/work/SWE2-STRUCT/standin1003/edit_spawncand.py`.

## SWE2-STRUCT limits

Static only. The meaning of modes 1 and 2, of the floats at `+0x04`/`+0x08`/`+0x1C`, and of the tail copied for newer
tables is not claimed.
