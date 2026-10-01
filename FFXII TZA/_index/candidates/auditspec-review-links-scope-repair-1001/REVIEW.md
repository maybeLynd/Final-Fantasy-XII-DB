# Audit-spec review: OPUS links-scope repair at 5561c01a0

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Board task: `OPUS-REQ-AUDITSPEC-LINKS-SCOPE-REPAIR-1001`
Subject: repair of `auditspec-review-links-scope-0930` (AWN), three routed items.

## Verdict: ACCEPT

All three routed items verified at source and by execution:

1. **CommonMark code-span pairing per paragraph** — `check_links.py` now pairs backtick runs of
   equal length across the paragraph (`code_spans()` + PERCENT comment block). Test L7
   (``` ``a`b`` ``` pairs as one span) and L8 (span closing on the next line) both PASS.
2. **Capture convention as policy** — EVIDENCE-POLICY rule 17 written: subdirectory files are
   byte-exact captures, counted but not judged; authored files at package level are judged.
   L9 (`README` mirror inside a subdirectory stays a capture) PASS.
3. **Encoded separators refused** — a target whose decoding adds `%2F`/`%5C` is reported broken
   with a named reason. L10 + L11 PASS.

`test_check_links.py` L1–L11 FAILS 0 re-executed here (HEAD checker fails L7–L10, as the commit
records — the test file pins the new behaviour).

## Residual (not defects of this repair)

Full-db run: 16 broken links remain, all outside this repair's scope — 2 in
`uq384-385-vif1-fable-0930` (FABLE's unpublished record; the commit explicitly left it), 14 in
`analysis-kit/gfz-scripts/_ov_section.md` — an **untracked scratch file** (Sep 29, no references).
Not judged debt; noted for its owner.

## Scope note

The repair also fixed two SECTION-03 pages' wrong-depth review links and a self-link in
`swe2struct-uq384-385-0930` — in scope per the original review.
