# Status currency census: the 128 pages not at DOCUMENTED (OPUS, 2026-09-29)

**What this is.**
- A read-only measurement for final-audit precondition 2 ("every system documented"). The goal gate does not assess
  that precondition; My Progress counts it as family DD.
- [`status_currency_census.py`](status_currency_census.py) classifies every page that `progress.coverage_documented`
  does not count, by what its `status:` line names. Rows are in [`census.tsv`](census.tsv).
- **No page was changed.** Re-statusing is gated on the ruling below.

| status word | class | pages |
|---|---|---:|
| PARTIAL | every register row the line names is ANSWERED or WITHDRAWN (incl. SUPERSEDED / NOT A QUESTION dispositions) | **40** |
| PARTIAL | names no register id (the residue is in prose) | 70 |
| PARTIAL | names a live row | 1 |
| REOPENED | names no register id | 16 |
| CORRECTED | names no register id | 1 |

Measured at `dec463b67` against `_index/OPEN-QUESTIONS.md` as read by `check_questions.read_table`.

## The question (routed to FABLE: meanings)

The status ladder says `DOCUMENTED` = all sections filled, every claim tier-cited. FABLE's 2026-09-14 ruling §4 says a
page is `PARTIAL` while residual questions remain.

For the 40 pages in the first row, every residual question the status line names is now closed in the register. Many
were closed by a class-1 or class-2 disposition, whose residue lives on an instrument or carrier rather than the page.

**Is such a page `DOCUMENTED`** once its sections are confirmed filled and tier-cited? Or does a disposition's retained
residue keep the page `PARTIAL`?

**The proposed rule, for ruling:**
- An answered row closes its page residue.
- A disposition closes the page's residue and names where the residue moved.
- The page then reads `DOCUMENTED` with that pointer in the status line.
- The page's own sections must still be checked. The register state alone does not re-status a page.

## The 17 REOPENED/CORRECTED pages

These return only through `DOCUMENTED` → `AUDITED` (EVIDENCE-STANDARD's lifecycle), so each needs its reopening
trigger resolved and a falsification pass. That is per-page work for the page owners, and the census lists them.

## OPUS's own share

Six pages OPUS created are in the table:
- in the first row: `derived-call-signatures.md`, `generated-function-families.md`, and the UC-1 pages
  `referenced-code-the-list-never-had.md`, `the-bodies-the-list-cuts-short.md` and
  `the-code-the-function-list-does-not-contain.md`;
- `the-aspect-fit-and-the-super-wide-bound.md`, which names no id.

OPUS will re-status its own once the rule is decided, checking each page's sections.
