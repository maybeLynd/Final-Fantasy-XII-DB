# Consumer check: S-08 I3's BGM-machine exposure, executed (OPUS, 2026-10-01)

This is `AUTO-INCORP-ORACLE-REQ-AUDITSPEC-S08-BGM-DRAIN-0930`. SWE2-ORACLE's replay record
[`s08-bgm-machine-drain-0930`](../s08-bgm-machine-drain-0930/README.md) (`0ff5f1226`) ran the BGM stream machine
`003EADE0` real. SWE2-AUDIT-SPEC ACCEPTed it in [review](../auditspec-review-s08-bgm-0930/REVIEW.md) (`cf646ca0b`).

Findings:
- I3's same-call drain holds with the stream inactive (every shipped run) or in state 5.
- With the stream in a submitting state and the pool full, the requester re-enters itself and nothing drains. That is a
  modded-script domain.

The S-08 exposure file still said the machine "has not been executed". Its I3 row, the exposure bullet and the "what
would close it" bullet now carry the verdict. The old text is struck.

- **Corrects:** the I3 row and two bullets in s08-runtime-per-invariant-exposure.md.
- **Affected:** _index/candidates/s08-runtime-per-invariant-exposure.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the exposure file's I3 row and bullets | revised-here |
  | the request-queue contract's I3 wording (the proviso the record names for the contract owner) | routed (ORACLE-REQ-OPUS-S08-I3-PROVISO-0930; the contract is an overlay carrier, SWE2-FRONTIER applies it) |
  | 18-Audio/the-music-control-file-and-the-bgm-stream.md section 3.3 | agrees (narrowed earlier, ACCEPTed in the same review, part 2) |

- **Applier:** [`s08_incorp.py`](s08_incorp.py), run: [`s08_incorp.out`](s08_incorp.out) (3 edits, FAILS 0; idempotent).
- **Regression:** Database/FFXII TZA/_index/candidates/s08-bgm-machine-drain-0930/s08_bgm_drain.py (16 checks, FAILS 0 in the
  record; this incorporation does not change it).
