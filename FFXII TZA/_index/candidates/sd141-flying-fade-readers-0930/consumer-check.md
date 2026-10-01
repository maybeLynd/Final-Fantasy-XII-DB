# Consumer check: SD-141 reopened on SWE2-AUDIT-SPEC's REJECT (OPUS, 2026-10-01)

SWE2-AUDIT-SPEC's [review](../auditspec-review-sd141-0930/REVIEW.md) (`e1a2c0f05`) shows that the flying-fade pair is
read: `006084B0` hands `02CB8160` to the copy `005DEC50`, which reads `02CB8410` / `02CB8414`. The record's "no reader by
any route" is struck, and the reviewer's wording replaces it.

- **Corrects:** in this README, "No instruction in the image reads either global by any route", "What it fades: nothing in the shipped build", "For modding: ... has no effect in this build", and the F3 limit's "No such lea target exists within 16 bytes"; in the register, SD-141's ANSWERED status; on the reflected render-parameters page, the SD-141 answer notes, the ticked box and the DOCUMENTED status.
- **Affected:** _index/OPEN-QUESTIONS.md, 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | this record, the register row SD-141, the page's line 146 note, box, status and `reopened_count` | revised-here |
  | _index/candidates/dd-data-4-0930/README.md (registered SD-141 as a question) | agrees (it asks, it does not answer) |
  | _index/candidates/sd-incorporation-fable-0930/README.md (FABLE's incorporation of the answer) | routed-to-FABLE (the incorporation is now stale) |
  | _index/candidates/opus-dd-1599-0930/batch3.md (owner read citing the answer) | routed-to-OPUS (superseded by this reopening) |

- **Regression:** Database/FFXII TZA/_index/candidates/auditspec-review-sd141-0930/sd141_handon.py (the reviewer's hand-on
  trace, H1-H3), run: sd141_handon.py at d72abc0ea (FAILS 0).
