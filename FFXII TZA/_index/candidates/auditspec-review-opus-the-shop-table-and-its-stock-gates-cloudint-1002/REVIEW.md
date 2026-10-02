# SWE2-AUDIT-SPEC review of `opus-the-shop-table-and-its-stock-gates-cloudint-1002`: ACCEPT

Reviewer: SWE2-AUDIT-SPEC - 2026-10-02 - Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SHOP-TABLE-AND-ITS-STOCK-GATES-CLOUDINT` - Package: `_index/candidates/opus-the-shop-table-and-its-stock-gates-cloudint-1002/`

## Verdict: ACCEPT

- **Mechanical checker:** `interior_applier.py` re-run at review commit - `ALREADY`, `FAILS 0`.
  All anchors are instruction boundaries inside their cited extents with the recorded mnemonics.
- **Row/anchor reconciliation:** README claims 2 rows / 9 anchors; `rows.json` holds exactly
  2 rows and 9 anchors.
- **Semantic review vs the certified shipping image**
  (SHA256 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8): the full row
  population was verified - all 2 rows disassembled and read against their sentences. `003FD360` byte-exact across the whole stock-gate chain (byte+0x17E/+0x17F, `01F2CC98` table, `0209AC30` row +0xD48 with the 0x1000->0xFFFF fix-up, bit26 clear / bit27 set / r8b low byte, bits16-20 count zeroing, per-entry `00252D10(word+4+9)` / `0057D610(byte+0x17F,word+6)` accept, the `word+4==5`-with-r9d skip, `002CCA10(byte+0xD4B)` gate for 0xA and the 7/8/9/17 -> 0x1B/0x1C/0x1D/0x1E pairing, slot fills at +0xF0..+0xF7 with `00252D40` and `002526F0(8,byte+0x20,1)`, terminator +0xF6=0xFF, and the bits21-25 first-match scan); `0057CDD0` byte-exact (`002497E0(2,ecx*32)` + `00861EC0` zero-fill).
- **Scope/limits:** static byte-level verification only; the review asserts nothing about runtime
  behavior beyond what the shipped instructions encode.
