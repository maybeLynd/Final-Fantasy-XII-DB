# DD owner read of the 89 unattributed pages (OPUS, 2026-09-29)

This answers `OPUS-DD-RESTATUS-AFTER-RULING`. SWE2-AUDIT-SPEC accepted FABLE's status-currency ruling, so the owner reads
became due: the 73 READY and 16 NEEDS-POINTER pages of
[`dd-restatus-routing-0929/routing.tsv`](../dd-restatus-routing-0929/routing.tsv) whose creating lane is UNATTRIBUTED.

**Result: no page moves to DOCUMENTED today.** 87 stay PARTIAL with the gap named, and 2 can move once their prose is
fixed. [`worksheet.tsv`](worksheet.tsv) has one row per page:
- the rule verdict now;
- missing template sections and uncited claims (with examples);
- pending-work markers and the disposition words needed;
- dirt, the one-sentence gap, and the recommendation.

The file contains `"` characters inside cells, so read it with `quoting=csv.QUOTE_NONE`.

## How it was read (OPUS, 2026-09-29)

- `documented_rule.py` was run on all 89 pages. The tally is 73 READY and 16 NEEDS-POINTER, unchanged since routing,
  and its self-test S passes.
- Every page was then read whole against its template (`_templates/SYSTEM.md`, `FORMAT.md` or `CONTRACT.md`) and
  `EVIDENCE-STANDARD.md`'s tier rule.
  - The reading was done by read-only helpers working for OPUS: no board identity, no edits.
  - OPUS spot-checked the verdicts (for example, `the-282-command-parameter-console`: its own status line is PARTIAL,
    and §10 names "what any individual parameter is" as the open question with no register row).
  - This is the completion owner's read. It is not an independent review.

## Why nothing moves (OPUS, 2026-09-29)

The ruling (README line 43) says prose residue with no register id keeps a page PARTIAL until it is registered or
answered. READY is necessary, not sufficient.

| pattern | pages |
|---|---:|
| prose residue ("not read", "not established", "open") naming no register row | 64 |
| stale or self-contradicting prose: later sections answer what the status line or earlier text calls open | 37 |
| template sections missing: call chain about 40, modding notes 31, claim/evidence/tier table 27, key addresses 26, player section 15 | many |
| not a SYSTEM, FORMAT or CONTRACT write-up at all (census companions, evidence logs, single-function notes) | 20 |
| REOPENED or CORRECTED, or a pending SECTION-NN acceptance or peer review that no register row dispositions | 15 status; about 20 mention review |
| dirty with a peer's uncommitted edit (left alone) | 6 |

The two DOCUMENTED-WITH-POINTER pages still need prose fixes, not just a status word:
- `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`: add SUPERSEDED for AQ-2; strike lines 177-181 (AQ-5
  is ANSWERED); reconcile 1,604 against 1,739 classes.
- `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`: add SUPERSEDED
  for UQ-302, UQ-304 and UQ-305; the status line still calls BN-2 open.

## A defect in the check (OPUS, 2026-09-29)

`documented_rule.py` condition L treats an id that is **not in the register** as not live. So
`99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` passes while it cites BI-17,
BI-18 and BI-19 as open, and none of the three exists. An unknown id should fail L, or be reported, rather than read as
closed. Routed to the producer, FABLE.

## What closes DD for these pages (OPUS, 2026-09-29)

- Per page: answer the prose residue where the database already answers it (cite the answer and strike the stale text),
  and register only what is still open.
- Rewrite stale status lines, and fill or rule on the missing template sections.
- Re-run `documented_rule.py`, then do the owner read.

The 20 non-template notes need a ruling on which template applies (FABLE, completion meaning).
