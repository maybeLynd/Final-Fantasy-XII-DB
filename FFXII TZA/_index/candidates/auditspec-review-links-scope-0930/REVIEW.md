# SWE2-AUDIT-SPEC review of check_links.py's three scope corrections (OPUS, 145ac7e3b): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: `145ac7e3b`
(`check_links.py` + `test_check_links.py`), measured at HEAD `d5f06584e`. The question: does any correction hide a
real document link?

**Re-verified at HEAD `9b6c5bc93`** (FABLE session 0aca3c35, 2026-09-30 ~22:05Z, after the first reviewer's session died before publishing). `check_links.py` and `test_check_links.py` are unchanged since `145ac7e3b`. Re-runs: `test_check_links.py` identical (L1-L7 PASS, FAILS 0); `links_fixtures.py` and `links_blanked.py` identical; `links_live.py` identical except the file count (2,583 `.md` files now, 2,547 then) - every exemption count below is unchanged ([recheck_links_live_9b6c5bc93.out](recheck_links_live_9b6c5bc93.out)). The verdict stands.

| request | commit | verdict |
|---|---|---|
| OPUS-REQ-AUDITSPEC-LINKS-SCOPE-0930 | `145ac7e3b` | ACCEPT-WITH-NARROWING |

**Short answer.** At HEAD no real *broken* document link is hidden. But two of the three rules can hide one by
construction, and the code-span rule already blanks two real (resolving) links on live pages. Percent-decoding is
a net gain.

**Tests re-run** ([rerun_test_check_links.out](rerun_test_check_links.out)): L1-L7 PASS, FAILS 0. Sensitivity:
- L2 checks that a capture is not judged, but not the printed count.
- L3 has only a balanced single-backtick span, so it cannot see the pairing defect below.
- No test covers a document that is authored inside a package subdirectory.

**Sensitivity fixtures** ([links_fixtures.py](links_fixtures.py) / [.out](links_fixtures.out)). The fixture tree is
built under `C:\t\auditspec` and runs copies of the checker at `145ac7e3b` and `145ac7e3b^`. Each case plants one
real link. A rendered-Markdown reader's view is the expectation.

| case | shape | pre | post | result |
|---|---|---|---|---|
| A1 | authored `run-01/README.md` in a package subdirectory, broken link | reported | **not judged** | hidden (rule is path-only) |
| A2 | true capture in `retained/`, broken in its new place | reported | not judged | by design |
| A3 | package-level README, broken link | reported | reported | control holds (L1) |
| B1 | ``` ``a`b`` ``` then a real broken link, then `` `c` `` | reported | **not reported** | hidden (mis-pairing) |
| B2, B3 | real link beside / labelled by a span containing `](` | reported / mangled | reported | correct |
| B4, B5, B6 | link text that CommonMark renders as code | reported | not reported | correct (true false positives removed) |
| C1 | `C1%20missing.md`, raw-named file present, decoded file missing | **missed** | reported | fixed by the correction |
| C2 | `%20` target whose decoded file exists | reported | resolves | correct (L5) |
| C3 | `C3%2F..%2Fc3.md` (raw path missing, decoded traversal exists) | reported | **resolves** | hidden (theoretical) |

**Live census at HEAD** ([links_live.py](links_live.py) / [.out](links_live.out)). This is an independent scanner over
HEAD blobs under `Database/FFXII TZA`; it does not import the checker.
- **Captures.** 2,547 `.md` files; 4,623 relative links sit in package-subdirectory files (the checker prints
  4,631, counting every match).
  - 87 links are in files byte-identical to a non-evidence blob (HEAD or history).
  - 777 are in path mirrors (`run-NN/source/Database/...`) or files whose name matches a live page.
  - 3,759 are in renamed page copies under `retained/` (for example `question-ledger.md` with 1,196 links, `primitives.md`
    with 63). All of these are captures in substance.
  - **0** broken links are in files named README/RESULT/PLAN/NOTES/METHODS/SUMMARY/REPORT/REVIEW.
  - So no authored document is hidden today, but nothing in the rule checks that; A1 is the gap.
- **Code spans.** 13 links are exempted now (the commit counted 9; later commits add some). A reference CommonMark
  pairing (equal-length runs, across the paragraph) puts **11** of them inside real code spans, so they are not links
  (for example `vtbl[0xD0](+0x6C0, word[part+0x8A])`).
  - **Two are real links that the rule blanks** ([links_blanked.py](links_blanked.py) / [.out](links_blanked.out)):
    - `how-a-character-turns.md` → `../../_index/ADDRESS-INDEX.md`: 5 backticks on the line;
    - `the-shared-command-state-word.md` → the same target: 15 on the line.
  - Both lines have an odd backtick count, whose partner lies on another line of the paragraph. `CODE_SPAN`
    (`` `[^`\n]*` ``) pairs line-locally and ignores run length, so it builds a span `` `](…ADDRESS-INDEX.md), ` ``
    that CommonMark never forms. Both targets resolve, so nothing broken is hidden today. B1 shows the same mechanism
    hiding a broken link.
- **Percent.** 1 target at HEAD (`Database/Tools/dashboard/VIEW-SCHEMA.md:46`, `FFXII%20TZA`), which resolves.
- **Checker at the worktree** ([rerun_check_links_worktree.out](rerun_check_links_worktree.out)): BROKEN AT HEAD 14.
  All 14 come from one untracked peer scratch file, `Database/Tools/analysis-kit/gfz-scripts/_ov_section.md`, which
  head_scope blocks fail-closed as the commit says. No tracked file is broken; the three crosswalk depth errors the
  commit named are no longer reported.

**Controls.** The captures rule and the percent rule are each sensitive to their own shape (L2, L5). The code-span
rule's control (L3) cannot fail on the defect found here, because its fixture has a single balanced span per line.

**Correction wording for OPUS** (the owner of `check_links.py`):
1. *Code spans:* replace line-local `CODE_SPAN` blanking with CommonMark pairing. A backtick run opens; the next run of
   the **same length** in the **same paragraph** closes it; unmatched runs are literal. Blank only spans so formed
   that contain `](`. Add a test with ``` ``a`b`` [x](missing.md) `c` ``` (must report) and one with an odd-count line
   whose span closes on the next line (must not blank a real link). This review's `links_blanked.py` has a reference
   pairing.
2. *Captures:* the comment "anything in a subdirectory … is a byte-exact capture" is a convention, not a check. Either
   keep judging package-subdirectory files named README/RESULT/PLAN/NOTES/METHODS (0 broken today, so no new debt),
   or state the convention in the evidence-package rules so an authored `run-NN/README.md` is not written there.
3. *Percent:* after `unquote`, refuse or report as broken a target whose decoded form contains `/` or `\` that the raw
   form did not (`%2F`/`%5C`). Browsers do not treat `%2F` as a separator (C3).
