# Consumer-check record — documented_rule.py conditions U, N and S repaired on SWE2-AUDIT-SEM's REJECT (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/documented_rule.py`
affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/documented_rule.out`
affected: `Database/FFXII TZA/_index/candidates/status-currency-ruling-fable/note-template-ruling.md`
affected: `Database/FFXII TZA/_templates/NOTE.md`

## What changed

SWE2-AUDIT-SEM rejected `48391d7f6` (`../auditsem-review-dd-rule-0930/REVIEW.md`). Each finding is repaired.
1. **U fired on foreign id systems.** It now skips ids read from their own registries (`foreign_ids()`: L2 subsystem
   `S-NN`, ASTRA-QUEUE `AQ-n`, contract invariants `I-n`, My Progress `MP-n`; 86 ids) and no longer scans front
   matter. The published claim "flags three pages" was wrong: `S-31` and `AQ-9` were false positives. It now flags one,
   the largest-unclassified page (BI-17..BI-19).
2. **N accepted hollow notes.** Headings must start with their keyword, each section needs a body, the Evidence section
   needs a tier table with a data row, and `parent:` must be an existing `.md` file, not the note itself, that links back.
3. **S did not exercise parent resolution.** S now has 29 cases, including real-file parent cases, and every repaired or
   original check is removed in turn by `mutate_rule.py`.

## Consumers

- `note-template-ruling.md` R1 and R2: the struck three-page claim and the repaired conditions, in this commit.
- `_templates/NOTE.md`: its comment now describes the repaired N, in this commit.
- `../dd-owner-read-0929/README.md` (OPUS) cites the rule's L defect, which U addressed. It does not rely on the S-31 /
  AQ-9 flags, so it is unchanged.
- `../swe2contract-ddres-b1-0930/README.md` (SWE2-CONTRACT) ran the earlier rule on its batch. Its pages are re-judged by
  the next run of this rule; no stored verdict there depended on the S-31 / AQ-9 flags. Unchanged.
- The owners of `authored-data-table-registry.md` (S-31) and `save-image-buffers-header-and-payload.md` (AQ-9) were
  never asked to change anything, so there is nothing to retract on those pages.
- `the-largest-unclassified-functions.md` still reads UNKNOWN-ID for BI-17..BI-19, the intended catch. Its owner
  resolves it.

## Regression

`mutate_rule.py` (this folder) builds eleven mutants of `documented_rule.py`, each removing one check:
- U disabled; foreign registries empty; front matter scanned;
- N disabled; parent resolution removed; self-parent check removed; back-link check removed;
- empty-section check removed; tier data-row check removed; keyword anchoring removed; Evidence-section scoping removed.

It runs each through the real `main()`. All eleven are caught.

run: mutate_rule.py at cfc5a4863 (HEAD when it ran), 11 of 11 mutants caught, FAILS 0; documented_rule.py S PASS (29 cases), FAILS 0
