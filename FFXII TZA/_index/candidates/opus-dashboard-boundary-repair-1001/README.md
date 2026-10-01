# Dashboard view boundaries repaired after ASTRA's REJECT (OPUS, 2026-10-01)

**What a user saw.** The dashboard could confuse "nothing measured" with "zero":
- a tile with nothing in its group (0 of 0) could later show a misleading change;
- the VBF page could call an old-listing comparison "0 differences" when the listing was never read.

Both are fixed.

This record answers `AUTO-REPAIR-OPUS-REQ-ASTRA-VERIFY-DASHBOARD-VIEWS-0929-R`. ASTRA's review REJECTed the delivery
`eae0ed3c7` at two boundaries. The review evidence is
[`dashboard-view-boundary-review`](../../../_experiments/evidence/dashboard-view-boundary-review/README.md) (`266327e27`).
ASTRA's raw results and drivers are not touched.

## 1. Delta basis (RESULT.md): zero ratio vs plain count (OPUS)

**Cause.** In `build_views.annotate_deltas`, the tests `if not m.get("denominator")` and the old denominator's truthiness
treated a denominator of 0 (a ratio with nothing in scope) as `None` (a plain count).

**Repair.**
- `None` vs number decides count vs ratio. The previous value no longer decides it.
- A measure that moved between count and ratio gets `"N/A - basis changed"`, with both sides kept exactly and no
  count, rel, pp, dnum or dden.
- Same-basis 0/0 is 100 % complete (the user's 2026-09-30 rule), so it never divides by zero.
- Both denominators are carried as they were.

## 2. Listing comparison (VBF-RESULT.md): absent is not zero (OPUS)

**Cause.** The capture (`vbf_index.capture`) silently omitted `vs_listing` when the listing was missing.
`build_views.v_vbf` then used `{}` and showed drift 0, with status OK.

**Repair.** The capture now records `vs_listing_failed` for four cases:
- no listing supplied;
- listing not found;
- unreadable;
- no `<size> <name>` rows.

When the comparison is not complete, `v_vbf`:
- emits **no** `listing-drift` measure;
- sets status PARTIAL;
- names the reason in the limits and in a first table row: "Listing comparison UNMEASURED: ...".

The archive inventory stays, because it is independently valid. There is no fallback to the old listing.

The capture still exits 0 when only the comparison is missing, because the inventory is valid. The failure is carried in
the data, not in the exit code. A missing or corrupt archive still exits 1 and gives a FAILED view.

## Tests (OPUS)

[`Database/Tools/dashboard/test_view_boundaries.py`](../../../../Tools/dashboard/test_view_boundaries.py) runs on the real
invocation paths:
- `annotate_deltas` on prior/current generation fixtures;
- the `vbf_index.py` CLI into `v_vbf`, on ASTRA's disclosed two-entry synthetic header shape.

| check | what |
|---|---|
| D1-D3 | controls: count +5 / +50 %; moved ratio dnum +5 / dden +100; changed scope gives no count |
| D4-D7 | 0/0 -> 5/null; 1/2 -> 0/0; 0/0 -> 0/0; 5/null -> 3/10 |
| V1-V4 | controls: matching listing; drift 2; missing archive; corrupt archive |
| V5-V8 | missing listing; no listing; rowless listing; malformed comparison |
| discriminator | D4, D5, D6 and V5 FAIL on the rejected `eae0ed3c7` source (read from git, AST-extracted as ASTRA's probe does) while its D1/D3 controls hold |

Every view also passes `server.check_view`. Run: 2026-10-01, FAILS 0 (`test_view_boundaries.out`).

## Limits (OPUS)

- The full build and server suite is `test_build_views.py`, and its run result is in the publish message.
- Listing parse validity beyond "no rows" is not tested. Concurrent archive mutation is not tested. The original game's
  binding to the archive is not tested. These are ASTRA's stated untested items, and they stay untested.
- A moved-denominator ratio keeps the user's 2026-09-30 headline pp rule. ASTRA's control was written against
  `eae0ed3c7`, which predates that rule's pp (the rule landed in `7f7818aae`).
