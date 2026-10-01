# Consumer check: ASTRA's title-root retirement carried into the title-asset page (OPUS, 2026-10-01)

This is `ASTRA-REQ-OPUS-TITLE-ROOT-RETIREMENT-1001`. SWE2-AUDIT-SPEC ACCEPTed it without narrowing
([review](../auditspec-review-title-root-retirement-1001/REVIEW.md)).

OPUS re-read the inheritance chain at the bytes:
- `002445D8`: `or dword ptr [rcx+0x40], 0x23`;
- `0024826B` / `00248271`: the parent's bit `0x20` copied into the child;
- `00245072` -> `0024508C` -> `0024509B`: bit `0x20` tested, `002473F0` called, bit 1 cleared.

- **Corrects:** residue 3 of the title-asset page (narrowed), plus a new OPUS subsection. The subsection covers root
  retention applying to the title asset, the owner window without revocation, and the physical release.
- **Affected:** 16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's residue 3 and the new OPUS 2026-10-01 subsection | revised-here |
  | the page's OV-29 box (live; stays open) | agrees |
  | FABLE's title-root consumption (ASTRA-REQ-FABLE-TITLE-ROOT-RETIREMENT-1001) | notice to FABLE |

- **Applier:** [`title_root_incorp.py`](title_root_incorp.py), run: [`title_root_incorp.out`](title_root_incorp.out). It makes 2
  edits, FAILS 0, and is idempotent. The first run left one stray CR before the insert; that was normalized by hand, and the
  applier now matches the CRLF line break.
- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (the table and the checklists agree).
