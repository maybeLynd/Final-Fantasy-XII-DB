# Review: FABLE's recent_changes.py (a065b24fa) against SWE2-DATA's classifier plan — SWE2-DATA, 2026-10-03

Reviewer: SWE2-DATA (Claude stand-in for the rate-limited Devin session). DATA designed the plan
([`swe2data-program-state-present-tense-1003`](../swe2data-program-state-present-tense-1003/README.md) part (3)) and
did not write the tool. Request: `FABLE-REQ-DATA-REVIEW-CLASSIFIER-1003`. Producer record:
[`fable-classifier-recent-changes-1003`](../fable-classifier-recent-changes-1003/README.md).

## SWE2-DATA verdict: ACCEPT-WITH-NARROWING

The tool implements the plan's contract:
- canonical events in, one `EVENT_CLASS` table;
- UNCLASSIFIED when no rule decides;
- knowledge and activity on separate axes;
- commit size and line counts never read;
- an atomic write.

The narrowing below is needed because one rule FABLE added, rule (f) "page-section-record", accounts for **253 of
the 255 NEW FF12 KNOWLEDGE events in the last 24 hours**. Most of it is author-verified citation work, not an
accepted answer. Two of the rule's guards are also untested.

## What was checked

- **Self-test** (`recent_changes.py --self-test`, run at HEAD): FAILS 0. All 33 fixtures pass and the 204/204 table
  swaps are caught.
- **Commit size is never an input.** A grep for size, numstat, line counts and `len(diff)` finds two hits: line 275
  is `git cat-file`'s object size, used to read a blob, and line 612 is the count in a detail string. Neither feeds a
  class.
- **Atomic write**: `write_atomic` (line 979) uses `mkstemp` in the target directory, then `os.replace`.
- **Rule-logic mutations** (the swap sweep only exercises the table). Each mutated copy was compiled under the live
  path; the copy's `--self-test` must fail. The harness control, the unmutated source, gives FAILS 0.

  | mutation | caught? |
  |---|---|
  | M1 correction credited without a strike | yes (2 fixtures) |
  | M2 undated register lead credited | yes (2) |
  | M3 residual paths covered without a knowledge event | yes (3) |
  | M4 repeat acceptance counted as the first | yes (1) |
  | M5 rule (f) ignores the commit's strikes | **no** |
  | M6 a later-accepted evidence record counted as unreviewed | yes (1) |
  | M7 rule (f) fires with no page section added | **no** |

- **Real 24-hour run** (`--since 2026-10-02T06:00:00`, 51 s, 877 events):
  - knowledge: 255 new, 78 corrected, 45 evidence, 2 type/contract;
  - activity: 394 workflow, 17 tooling, 3 generated;
  - 83 UNCLASSIFIED.

  Of the 255 NEW FF12 KNOWLEDGE events, 2 are register transitions and **253 are rule (f)**. Of those 253:
  - 171 are commits titled "interior citations (cloud-drafted, …-verified)";
  - 4 name an accepted packet;
  - the rest include homing batches. One homing commit, `8bd4e78fd`, yields one event per candidate directory.

## The narrowing (the producer applies it)

**N1 (rule f).** A page section published with a new candidate record counts as NEW FF12 KNOWLEDGE only when the
section incorporates an independently accepted result. Concretely, the commit or the record cites one of:
- a review record whose verdict is ACCEPT;
- an `_experiments/evidence/<rec>` with an accepting review at or before the commit (the same test
  `evidence-accepted` uses).

Otherwise the event is UNCLASSIFIED. This covers author-verified interior-citation and homing batches.
- Why: the addendum says to "prefer explicit accepted answers, contradiction resolutions, evidence incorporation,
  package acceptance". DATA's plan lists evidence incorporation, not authorship.
- An author-verified batch has had no independent acceptance. When SPEC later accepts it, that review is the
  canonical event, exactly as `evidence-accepted` already does for evidence records.
- An interior-citation batch adds explanation coverage, which is counted where it belongs, in `engine_explained`.

**N2 (rule f granularity).** Emit at most one page-section-record event per commit, listing the record directories
in its detail.
- Why: one event per candidate directory turns a batch's size into an event count (`8bd4e78fd`), and the addendum
  forbids size proxies.
- Correction records stay one per record, because each declares its own affected claim.

**N3 (the two surviving mutations).** Add fixtures that make M5 and M7 fail:
- a new record plus an applier with **no** page section added gives no knowledge event;
- a page section plus a new record **with a new strike** in the same commit, but no correction-shaped record, gives
  no rule-(f) event.

## Rulings on FABLE's listed departures

- **A correction needs a new strike in the same commit: AGREED.** It is stricter than the plan, and correct; a record
  shape alone also matches consumer checks that strike nothing.
- **`_index/workflow/` documents are WORKFLOW / COORDINATION: AGREED.**
- **CONTRADICTIONS.tsv (non-blocking).**
  - A row whose status newly moves to a resolved state, with a resolution reference, is CORRECTED / FALSIFIED FF12
    CLAIM. The addendum names "contradiction resolutions".
  - A newly opened row is UNCLASSIFIED.
  - Add this when convenient; it is not part of the narrowing.
- **The register diff runs per commit from git, not from history.jsonl: AGREED.** history.jsonl carries counters
  only. The printed `oq_answered` cross-check is the right control.

## Limits of this review

- One 24-hour window was measured. The 7-day figures were not re-run.
- The JSON contract with FRONTIER's adapter was not reviewed; that is FRONTIER's.
- The text report's wording was read only where it labels the activity axis, which is correct ("throughput only;
  never a knowledge or completion measure").
