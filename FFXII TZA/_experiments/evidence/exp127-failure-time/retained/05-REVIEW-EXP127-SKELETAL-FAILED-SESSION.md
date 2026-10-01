# REVIEW — EXP-127 skeletal-reset-live (ASTRA-REVIEW-EXP127-FAILED-SESSION)

Verdict: **ACCEPT-WITH-NARROWING** — the raw same-thread/stack observations are
sound retained evidence; the healthy-session assertion is correctly withheld;
causation is unknowable from what was kept.

## Method

Re-tallied `skeletal/capture/result.json` directly (5,453 hit records); did not
trust `normalized.json`. Ran `assess.py` — it reproduces and its three gates
hold.

## Re-derived from primary receipts

| Claim | Claimed | Re-derived |
|---|---:|---:|
| Total hits | — | 5,453 = `capture.log` "PASS hits 5453" |
| `003A1C50` target hits | 205 | 205 |
| `003E3C30` entry hits | 1022 | 1022 |
| `003E3C7A` precall / `003E3C7F` postcall | 2113 / 2113 | 2113 / 2113 |
| Paired boundaries | 2113 | 2113 strict `7A→7F` alternations, **zero** orphans |
| Threads | same-thread | all hits `tid=30100` |
| Entry RCX values | 16 | 16 distinct, `0x6DD2C830`–`0x6DF42030` — matches `assess.py` range exactly |
| Window | ~1s | `1789876880.99`–`1789876881.99` |

## The failure boundary

- Last recorded hit: `1789876881.99`. Runtime-error dialog recorded
  `2026-09-20T04:02:09` — **~47 s after the observations completed**. The hits
  precede the failure; they are not contaminated by it.
- `result.json` status `PASS`, API clear/detach succeeded, post CPU samples
  recorded — the instrument's own receipts close cleanly *before* the dialog.
- `runtime-error.json` is a genuine UI capture (accessibility tree of the MSVC
  Runtime dialog on FFXII_TZA.exe, PID 31940). `session-health.json` records
  `root_cause: UNKNOWN` — correct. The retained evidence cannot distinguish an
  instrument-caused crash from an independent game fault, and does not claim to.

## Retained vs withheld

**Retained:** every hit figure above; the single-thread pairing; the entry-RCX
set; the exe identity (canonical sha256 in `run.json` process record).

**Withheld:** healthy-session (the experiment's own INVALID_POST_TRACE status is
correct); any causation; any semantic promotion of the boundary hits into
codec/skeleton behavior — they remain observations on one route, which the page
states.

## Instrument defect (demonstrable)

The liveness gate treated **API clear/detach + post-trace CPU samples** as
session-health evidence. `session-health.json`/`runtime-error.json` prove those
are insufficient — `assess.py` already encodes the repair as a check
(`actual_runtime_error_rejects_despite_cpu_and_api_positive`), and its limits
line is honest ("gate logic regression only; no repaired native instrument").

## Exact future control needed

A **post-trace responsiveness probe** before any "healthy session" label: a
scripted input that produces an observable UI/state transition, or the clean
game-exit path, completed *after* detach. Optional hardening: a post-detach
settle delay plus same-window dialog detection (the dialog capture itself
worked — keep it as a reject condition, which `assess.py` now does).
