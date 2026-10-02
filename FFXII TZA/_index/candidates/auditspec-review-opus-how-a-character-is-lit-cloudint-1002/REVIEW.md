# SWE2-AUDIT-SPEC review of `opus-how-a-character-is-lit-cloudint-1002`: ACCEPT

Reviewer: SWE2-AUDIT-SPEC - 2026-10-02 - Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-A-CHARACTER-IS-LIT-CLOUDINT-1002` - Package: `_index/candidates/opus-how-a-character-is-lit-cloudint-1002/`

## Verdict: ACCEPT

- **Mechanical checker:** `interior_applier.py` re-run at review commit - `ALREADY`, `FAILS 0`.
  All anchors are instruction boundaries inside their cited extents with the recorded mnemonics.
- **Row/anchor reconciliation:** README claims 4 rows / 18 anchors; `rows.json` holds exactly
  4 rows and 18 anchors.
- **Semantic review vs the certified shipping image**
  (SHA256 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8): the full row
  population was verified - all 4 rows disassembled and read against their sentences. All 4 rows byte-exact: `003477E0`/`00347D60` dword `+0x28` of the `02099D70` getter into the 38-byte helper with edx 1/0; `003AED20` -1-word / zero-sum / +0x284-zero ladder returning dword `+0x28C`; `003DD6C0` 0..4 record scan (byte+0x10 bit0 AND byte+0x17 bit6), 7-byte helper(0) on clear, 22-byte helper + `&0xFFFFFFFD` test, else tail-jump 31-byte helper with 2.
- **Scope/limits:** static byte-level verification only; the review asserts nothing about runtime
  behavior beyond what the shipped instructions encode.
