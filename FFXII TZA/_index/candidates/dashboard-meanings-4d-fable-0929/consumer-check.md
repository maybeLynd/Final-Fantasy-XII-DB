# Consumer-check record: DASHBOARD-MEANINGS 4d, the delta rule after the user's 2026-09-30 directive (FABLE, 2026-09-29)

affected: `Database/FFXII TZA/_index/workflow/DASHBOARD-MEANINGS.md`

## What changed

Section 4d said that a delta is shown only like-for-like and that a moved denominator is "scope changed", never a number.
The user rejected that display ("+12 of -10") and asked for the completion-percentage change since the last refresh.
OPUS relayed this as OPUS-NOTICE-FABLE-DELTA-DIRECTIVE-0930 and implemented it:
- `build_views.py` `annotate_deltas` adds `pp = 100*n/d - 100*pn/pd` when the denominator or scope moved. `na` stays
  "scope changed", and `dnum` / `dden` carry the count changes for the tooltip.
- A zero denominator counts as 100 % complete.
- `server.py` shows `pp` to two decimals.

The old bullet is struck and superseded. What survives of like-for-like is now stated:
- a changed view definition is still "N/A - definition changed", with no number;
- a count with no denominator shows a signed change only when its definition and scope are unchanged.

The baseline bullet now says the refresh is short:
- the `supervise.py` refresher checks for new data every 5 s, and a build takes about 45 s;
- the 30-minute controller cadence is the fallback.

## Consumers

- consumer: the dashboard itself (`Database/Tools/dashboard/build_views.py`, `server.py`, commit `7f7818aae`): agrees. The
  restated rule describes what the code does.
- consumer: `_index/candidates/dashboard-views-0929/README.md` (OPUS's record) uses "like-for-like" for its own
  implementation history. It is not FABLE's text and is not restated here; routed-to-OPUS-NOTICE-FABLE-DELTA-DIRECTIVE-0930,
  whose closing note names it.
- No other page states the delta rule. A grep for `like-for-like` over the database finds only these two files.

## Regression

regression: `Database/Tools/dashboard/test_live.py` D2 (a moved denominator still carries the completion-% change), D9
(the moved-denominator `pp` with `dnum` / `dden` kept), D10 (0 of 0 -> 0 of 10 gives -100 points).
`test_build_views.py` B9 (a definition change gives "N/A - definition changed" with no `pp`).

run: test_live.py at 82cb3490a (FAILS 0; D2, D9, D10 PASS); test_build_views.py at 82cb3490a (B9 PASS)
