# FABLE's lane: cross-links for the completion route, and a spot check of claimed closures (FABLE, Claude Opus 5.5, 2026-09-27)

This record answers the ROUTE part of `FRONTIER-REQ-SWE2-DATA-PROGRESS-REPAIR-CKPT10` for FABLE's lane. It gives
SWE2-DATA exact links; it builds no new reporting tool. `fable_route_links.py` is a read-only git diff over the register,
and its output is [`fable-register-transitions.tsv`](fable-register-transitions.tsv).

## 1. What the TSV is and is not

- **What it is.** Every register row that a `FABLE:` commit changed since 2026-09-26: 95 transitions. Each has the
  commit, the status class before and after, and the first `_index/candidates/` record the new cell cites.
- **What it is not.**
  - **It is not current state.** A later commit can move the same row; BQ-23, for example, passes through PARTIAL
    three times before ANSWERED in `f3625d0dc`. Read current status from `check_questions.py --db` at HEAD.
  - **It is not a reviewer list.** The commit author is FABLE. A `FABLE-PUB-*` task is FABLE's own publication,
    not a review.
- **Two rows parse as `?...`.** BB-4 at `7424a725a` and UQ-333 at `0c194102e` had a literal ` | ` inside the status
  cell at that commit. Both read ANSWERED at HEAD.

## 2. Kept separate, with the actual reviewer

**Approved dispositions: NO ADMISSIBLE SOURCE.** Each is counted closed by the gate. For each, the author is FABLE,
and the reviewer is a non-author whose signature is a commit:

| row | package | reviewer and receipt |
|---|---|---|
| FJ-3 | `nas-package-4-2026-09-27/` | OPUS, `260521390` |
| DM-2 | `nas-package-5-2026-09-27/` | OPUS, `nas5-review-opus/` `b4bd5c2cb` |
| BL-8 (`+0xB0` residue) | `bl8-b0-walkers/` | OPUS, `bl8-b0-nas-review-opus/` `c3dee2be2` |
| X-8 (YEBIS version only) | `nas-package-6-2026-09-27/` | OPUS, `nas6-review-opus/` `82cc0acee` |

**Superseded under a ruling.** The ruling is SWE2-FRONTIER's
[`batch-K-scope-rulings.md`](../register-triage/batch-K-scope-rulings.md). The register write is an application of the
ruling, not a review. Each row's residue stays owned and visible:

| row | ruling | who applied it | residue owner |
|---|---|---|---|
| UQ-80 | 27c | FABLE, `03c573fe6` | the 60 bytes in `uq80_manifest.tsv` |
| UQ-196 / BT-2 | 27c | OPUS, `cd73ae1d5`; the box FABLE, `021279b86` | OPUS static-FIELDS, the DISCOVERED spans |
| UQ-2 | 27c/d | OPUS | OPUS: the 511 untyped position-1 rows |
| SV-1 | 27c | OPUS | the sv1 instruments: the development-image layouts |
| AR-5 | 27c | OPUS, `7be558b7e` | OPUS: the per-(class, slot) residue |
| CD-2, UQ-146, J-C | earlier rulings | as in the TSV | the ruling text names each |

**Transfers.** Ruling 27c-2 reassigned UQ-2, AR-5, T-4 and UQ-46 to OPUS. They remain **required and open until
their own reading lands**: a reassignment is not completion. `FRONTIER-RT-STATIC-*` packages assigned to FABLE are
carriers too. Each row inside them closes on its own.

**Answered.** 56 transitions end in ANSWERED. Most carry only the author's control, with no independent review
receipt. A report must show the reviewer as **UNKNOWN** unless a receipt exists. The independent reviews FABLE knows
of this cycle:
- SWE2-AUDIT-SPEC: ACCEPT ×5 on the status-key and Phyre-wrapper consumers (FABLE-REQ-AUDITSPEC-REVIEW-FABLE-CONSUMERS-0927).
- SWE2-DATA: accepted the FDM group-bit correction (`b8628d225`).
- SWE2-CONTRACT: owner review of the status-write dispatch row (`56b3038ee`).

**Pending, not complete.**
- **EXP-189/086 propagation.** ORACLE's three receipt annotations have not landed
  ([record](../exp189-exp086-consumer-check.md), section 4).
- **The nav-grid row.** It awaits review by AUDIT-SPEC ([record](../navgrid-unit-definition/README.md)).
- **UQ-38, UQ-36, UQ-39 and UQ-212.** They are candidates for OUT OF EVIDENCE BOUNDARY under 27b. No package has
  been signed yet.

## 3. Spot check of representative claimed closures (controls re-run 2026-09-27, HEAD `3d95e439c`)

| closure | class | control re-run | result |
|---|---|---|---|
| T-9 (FABLE) | ANSWERED | `t9-crt-gfids/t9_crt_gfids.py` with its two library arguments | **identical** to the committed `t9_crt_gfids.out`, FAILS 0. The README never gave the arguments; it now does |
| UQ-80 (FABLE) | SUPERSEDED | `uq80-table-field-coverage/uq80_coverage.py` | **it failed at HEAD.** It searched for the *unticked* UQ-80 box, which `03c573fe6` ticked. Fixed to accept either state; the output is then identical to `coverage_run.txt` apart from one "wrote" line. The receipt is unchanged |
| AR-5 (OPUS) | SUPERSEDED | `ar5-vtable-dispatch/ar5_dispatch.py` | FAILS 0 |
| DM-2 (FABLE, OPUS reviewer) | NAS | `nas-package-5-2026-09-27/nas5_reserved.py`; `nas5-review-opus/vk_compare_scan.py` | FAILS 0. The reviewer's scan names the same four functions its review explains. It must run from `Database/`, because the exe path is relative |

**Lesson for the route.** A closure can go stale without anyone editing it. UQ-80's control broke because its own
closing publish ticked the box it read. "Named script exists" and "case count matches" would both have passed. Only
running it showed the failure.

## 4. Parse hazards in the register for any generator

These rows are all counted correctly by `check_questions.py`. They break a naive split on ` | `:
- **Unescaped pipes inside code spans:** PS-1, UQ-218, UQ-242, UQ-255.
- **UQ-239's question and status share one cell.** `check_questions` still reads it as ANSWERED, from its bold span.

Tool: `Database/Tools/work/FABLE/gg3-scratch/reg_cells.py`. It is FABLE's scratch copy, not a deliverable.

## 5. One bucket that must be split, not counted

`check_questions.classify` returns **WITHDRAWN** for every lead word that is not an answer or a partial:
SUPERSEDED (a duplicate, a class-1 ruling or the runtime rule), NOT A QUESTION (class 2), DISSOLVED (a false premise)
and WITHDRAWN itself. That is right for a closed-or-not gate. It is wrong for a learned-state report.

A report needs the lead word, and for SUPERSEDED the carrier it names. The carrier tells a duplicate from a residue
that moved to another row or owner, and that moved residue is required work still open. At HEAD (2026-09-27):
- 3 rows are OPEN: MH-1, UQ-212, GG-1.
- 15 rows are PARTIAL: BA-1, BE-6, BQ-27, BJ-1, SN-1, SQ-1, PC-1, UC-1, UQ-36, UQ-38, UQ-39, UQ-70, UQ-213, UQ-215, UQ-218.

(FABLE's `open_rows.py` prints these through `check_questions.classify` itself.)
