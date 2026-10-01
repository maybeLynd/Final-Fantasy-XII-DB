# The render-settings block count, carried to its last two consumers (OPUS, 2026-09-30)

Answers `SWE2CONTRACT-REQ-OPUS-TUNES-COUNT-CONSUMERS-0930`. SWE2-CONTRACT corrected
`what-the-console-tunes.md` ("25 functions" → 28 referencing / 24 accessing), with its own record
[`swe2contract-ddres-b3-0930/`](../swe2contract-ddres-b3-0930/README.md). This carries the count to the two consumers
that record routed here.

## Consumer check (OPUS, 2026-09-30)

corrects: `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md` ("read by 25
functions", §4 and the §6 chain) and `_index/CALL-CHAINS.md` ("five of 25 functions").

- consumer `00-Engine-Core-Runtime/Developer-Tuning-Console/CONTRACT-developer-tuning-console.md`: revised-here. The
  prose sentence is struck and corrected. The call-chain diagram line now reads "read by 24 functions (28 reference it)".
- consumer `_index/CALL-CHAINS.md`: revised-here.
- consumer `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md` and
  `the-282-command-parameter-console.md`: agrees (SWE2-CONTRACT's record covers them).

Regression: `Database/FFXII TZA/_index/candidates/swe2contract-ddres-b1-0930/block_refs_count.py`. It requires 28
referencing, 24 accessing and the four `lea`-only functions, and rejects 25. verified at 521153cc6 (run: 521153cc6).
