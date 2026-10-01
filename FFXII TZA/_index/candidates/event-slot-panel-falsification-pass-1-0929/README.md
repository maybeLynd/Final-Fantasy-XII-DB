# Consumer check: falsification pass 1 on the-event-slot-panel-and-its-dead-feeder (OPUS, 2026-09-29)

corrects: 00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md (section 3's pusher row; section 4's read count: CON-185)

## What was corrected

- **`001EC680` stores the slot, or -1 above 4** (`cmova`), not `min(slot, 4)`. The page's own section 2 already said so.
- **Only two of the three pusher sites call it** (`00354B63`, `00354ED0`). `0026B750` calls the thunk directly.
- **The panel reads the counters at four sites**, not three.
- **What survives.**
  - The thunk routes and every caller site.
  - The regex literal.
  - The setter: flags cleared first, the same-name exit, the eviction, the `sum_` / `spc_` arms, one exit after the -1
    restore.
  - The pusher's order, refusals and unrestored marker.
  - The driver's two flag reads.

## Current consumers

- consumer: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md` says
  `001EC680` "only stores" and lists it among the marker's writers; it agrees.
- consumer: `_index/candidates/do2-branching-readings/do2-branching-readings.tsv` reads the two eventplay handlers'
  own branches, not `001EC680`; it needs no change.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-185`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_event_slot_panel.py` S5 and S6. S5 fails unless
`001EC680` is the five-instruction `cmova` body with exactly the callers `00354B63` / `00354ED0`. S6 fails unless
`001CD0E0` holds exactly four base-relative reads of the counter array.

run: verified at 949aef41a (BROKEN 0, exit 0), against the certified image `73461d08…`.
