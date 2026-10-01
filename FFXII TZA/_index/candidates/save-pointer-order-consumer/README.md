# Consumer check: Save's record-before-load order, and a stale `[0, x)` (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md, UQ-41 (register row)

Consumes ASTRA-RETURN-FABLE-SAVE-POINTER-RECORD-ALIAS
(`_experiments/evidence/save-pointer-record-alias-byte-preserved/`). **Verdict: ACCEPT**, re-read from the listing.
`Save` (`0036D930`) writes each pointer record (`0036D969`, into `02EC0A00`) before it loads that target's 16 bytes
(`0036D974`) and stores them (`0036D977`, into `02EC0800`). So a target that covers its own pointer slot is
snapshotted after the write. The contract already carries the rule as its Precondition 3 (SWE2-CONTRACT, on its own
copy of this return).

The consumer sweep for this page found a second, older defect. The UQ-41 answer text on the page, and its copy in the
register row, still said `003D8E50(x)` is "a random number in `[0, x)`". ASTRA's scaled-random-range-boundary
refuted that in general, and rng-streams.md was corrected in ac1406035. Both copies are now struck and point there.

| consumer | action | agreement |
|---|---|---|
| the workbench save/restore page, §3 | the order note added below Save's listing | revised-here |
| same page, the UQ-41 answer text | `[0, x)` struck and qualified | revised-here |
| `_index/OPEN-QUESTIONS.md` UQ-41 | the same phrase struck; verdict unchanged | revised-here |
| `00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md` §4 | none: Precondition 3 already states it | agrees |
| `rng-streams.md` | none: already corrected (ac1406035) | agrees |

Regression: [`save_order.py`](save_order.py) ([output](save_order.out)). S1 binds record < load < store from the
listing, and control C refuses the reordered copy. Run verified at 58b80e38a: FAILS 0.
