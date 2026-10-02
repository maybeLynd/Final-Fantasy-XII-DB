# Consumer check: two citation fixes found by the page gates (OPUS, 2026-10-02)

Two OPUS lines failed the database-wide page gates. `interior_ingest.py` runs these gates, and its F-interior apply
found the failures after SWE2-AUDIT-SPEC accepted the interior method.

- **`verify_doc_addresses` flagged two `.text` gap addresses.** The 01-Script-VM readiness correction (`1f193fec9`) on
  `scriptvm-native-dispatch-table.md` cited two function ranges by their exclusive ends, `003DC297` and `003DC2C9`.
  Those end addresses fall in `.text` gaps. They are restated as entry plus size: `003DC270` (0x27 bytes) and
  `003DC2A0` (0x29 bytes). The readiness applier carries the same text, so it still re-runs as ALREADY.
- **`check_consistency` found a fifth size disagreement.** OPUS's licence-check line (`5258d2c88`) gave the wrapper
  `00323600` as 43 B, against 47 B on the licence-board page. The wrapper ends with the 5-byte `jmp 00323D10` at
  `00323600+0x2A`, so its extent is 0x2F = 47 B. The 43 is struck.

The gates are back to their baselines: `check_consistency` reports the four known disagreements, and
`verify_doc_addresses --all` reports 0 documents to confirm.

- **Affected:** 01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md, 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 01 dispatch-table page (OPUS line) | revised-here |
  | the 12 licence-check page (OPUS line) | revised-here |
  | `16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md` (47 B) | agrees |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-scriptvm-readiness-fixes-1002/scriptvm_check.py, verified at fd96f1634: FAILS 0; `check_consistency.py` 4 known; `verify_doc_addresses.py --all` 0 documents to confirm.
