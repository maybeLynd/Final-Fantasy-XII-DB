# SWE2-AUDIT-SPEC review of `opus-the-script-to-native-calling-convention-cloudint-1002`: ACCEPT

Reviewer: SWE2-AUDIT-SPEC - 2026-10-02 - Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SCRIPT-TO-NATIVE-CALLING-CONVENTION-CLO` - Package: `_index/candidates/opus-the-script-to-native-calling-convention-cloudint-1002/`

## Verdict: ACCEPT

- **Mechanical checker:** `interior_applier.py` re-run at review commit - `ALREADY`, `FAILS 0`.
  All anchors are instruction boundaries inside their cited extents with the recorded mnemonics.
- **Row/anchor reconciliation:** README claims 5 rows / 20 anchors; `rows.json` holds exactly
  5 rows and 20 anchors.
- **Semantic review vs the certified shipping image**
  (SHA256 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8): the full row
  population was verified - all 5 rows disassembled and read against their sentences. All 5 rows byte-exact: `0034E5C0`/`0034EC80` three `00267E10(r9)` pops into the 52-byte helper with (dword+0x28, second, third, first) ordering and the 0/1 fifth stack argument; `0034F380` two pops + getter into the 200-byte helper with (dword+0x28, second, first); `00394600` byte `01EFAC10`==2 early return else tail-jump the 175-byte helper (`0x108`, `00393EA0`, 0); `003DB790` tail-jump `ActorResource_AllocateAndSubmitEntry` with r8d=1.
- **Scope/limits:** static byte-level verification only; the review asserts nothing about runtime
  behavior beyond what the shipped instructions encode.
