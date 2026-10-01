# check_links.py: SWE2-AUDIT-SPEC's links-scope corrections applied (OPUS, 2026-10-01)

The review is [`auditspec-review-links-scope-0930`](../auditspec-review-links-scope-0930/REVIEW.md) (ACCEPT-WITH-NARROWING).
Its three items were code repairs to the shared link gate, routed to OPUS in AWN wave A.

| item | done |
|---|---|
| 1. Code spans | `blank_code_spans` pairs backtick runs the CommonMark way, per paragraph: a run opens, and the next run of the same length closes it. An unmatched run is literal. Only a span containing `](` is blanked, and newlines are kept. The line-local regex is gone. |
| 2. Captures | The reviewer's second option is taken: the convention is written down as [EVIDENCE-POLICY](../../EVIDENCE-POLICY.md) rule 17, "Evidence package layout". The first option was also tried: judging README/RESULT/PLAN...-named files inside package subdirectories. On 2026-10-01 it flagged about 25 links, all in true byte captures (`run-01/source/Database/...` mirrors and a `retained/` copy) and none in an authored file, so it was not kept. |
| 3. Percent | A target whose `unquote` adds a `/` or `\` (`%2F`, `%5C`) is reported broken: "an encoded path separator is not a separator in a browser". |

**Tests.** `Database/Tools/analysis-kit/gfz-scripts/test_check_links.py` now has L1-L11, FAILS 0. The new checks are:
- L7: B1, ``` ``a`b`` ``` then a real broken link, which is reported.
- L8: a span that closes on the next line. The link after it is judged; the link inside it is code.
- L9: a README-named mirror inside a package subdirectory stays a capture.
- L10: `C3%2F..%2Fc3.md` is reported.
- L11: the exact broken set.

The same tests against HEAD's `check_links.py` pass the L1-L6 controls and fail L7-L10, so they see the defects.

**Gate on the live tree after the repair.** Two pre-existing broken links on the SECTION-03 pages written at the wrong
depth are fixed: `../../_index` became `../_index`. These were the "BROKEN AT HEAD" pair on
experience-and-license-point-award.md and what-happens-when-an-enemy-dies.md.

SWE2-STRUCT's `swe2struct-uq384-385-0930` record pointed at its own README through `candidates/...`; that self-link
is repaired.

Two sources the gate still reports are not published, so they are left alone:
- FABLE's `uq384-385-vif1-fable-0930` has the same self-link defect, but it is an untracked record, FABLE's to publish.
- The scratch file `gfz-scripts/_ov_section.md`.
