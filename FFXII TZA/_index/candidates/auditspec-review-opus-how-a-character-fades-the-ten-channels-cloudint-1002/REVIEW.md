# SWE2-AUDIT-SPEC review of `opus-how-a-character-fades-the-ten-channels-cloudint-1002`: ACCEPT

Reviewer: SWE2-AUDIT-SPEC - 2026-10-02 - Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-CHARACTER-FADES-THE-TEN-CHANNELS-CLOU` - Package: `_index/candidates/opus-how-a-character-fades-the-ten-channels-cloudint-1002/`

## Verdict: ACCEPT

- **Mechanical checker:** `interior_applier.py` re-run at review commit - `ALREADY`, `FAILS 0`.
  All anchors are instruction boundaries inside their cited extents with the recorded mnemonics.
- **Row/anchor reconciliation:** README claims 19 rows / 83 anchors; `rows.json` holds exactly
  19 rows and 83 anchors.
- **Semantic review vs the certified shipping image**
  (SHA256 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8): the full row
  population was verified - all 19 rows disassembled and read against their sentences. All 19 rows byte-exact, incl. `002915C0`'s full channel-node path (list walk at +0x10F20/+0x9B0 keyed on dword+0x980, `0209BE80`+0x10FC0 alloc of 0x9D0, dual zero-fill, r8-copy vs `+0x991|2`, stack-arg bit 4 and float +0x9A8, `01E0C1E0` lazy fill into +0x10F50/+0x988, buffer helper + 234-byte helper, word+0x9C0=1, head relink via 65-byte helper); the `002E84B0`/`002E8500` +0xC0/dword-at-rcx -1/-1-word record-resolution tails; `002EBBB0`/`002EBBF0` stop-registry bit writers; the four pop-float fade wrappers (`002EDA70`/`002EDA80`/`SetFadeStartDistance`/`002E83A0` argument order verified); `00373160`'s full A-to-E entry copy (dual `+0x84` resolution, +0x8A-count word-index walk at 0x290 stride, +0x270->+0x28E copy, the r8d==-1/0x100/+0x9C==2 gated index remap, `RuntimePointer_EncodeImageAddress` store, dual `0046D100` 64-byte copies, `+0x280|2`, and the -1/+0x276 fix-up); the three `02B3F570`/`02B40528` stride-indexed float stores; `003E4780`'s double-precision product (constants `00D117C0`/`00D117C8` verified); `0041FBF0`/`00420F90`/`004293C0`/`0042DE50` flag-writers and conditional tails.
- **Scope/limits:** static byte-level verification only; the review asserts nothing about runtime
  behavior beyond what the shipped instructions encode.
