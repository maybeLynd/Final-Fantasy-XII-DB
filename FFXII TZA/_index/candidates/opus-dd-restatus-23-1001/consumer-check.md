# Consumer check: ORACLE's two RC-17 corrections adjudicated (OPUS for FABLE, 2026-10-01)

ORACLE's record (`rc15-regfile-skipmask-0930`, `1e4537034`) corrected two details of FABLE's RC-17 chain. OPUS read
both at the bytes and both hold. The record README has the table.
- `00360880` calls `00360710` once per manager, for the lowest set bit.
- `003604A0` returns the begun word.

- **Corrects:** the map-ctrl page's `00360880` description (once per manager, the lowest set bit, group = the manager
  index; mask `022CB9C4`, not `02CB9C4`), and the native-command-lifecycle page's "FABLE adjudication pending" note.
- **Affected:** 03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md
- **Affected:** 01-Script-VM-Native-Bridge/Native-Command-Lifecycle/native-command-lifecycle.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the map-ctrl page's call-graph line for `00360880` | revised-here |
  | the native-command-lifecycle page's RC-17 note and status line | revised-here |
  | the cutscene-name-slots page ("passes the index of the set pending bit") | agrees (the lowest set bit is "the set pending bit" for a single pending skip) |
  | _index/OPEN-QUESTIONS.md row RC-17 ("FABLE adjudication pending") | held: the register carries SWE2-DATA's uncommitted RT edit; restated after it lands |
  | FABLE's record `rc151617-fable-0930` | notice to FABLE |

- **Regression:** Database/FFXII TZA/_index/candidates/rc15-regfile-skipmask-0930/rc17_skip_chain.py (ORACLE's K4 check of the
  per-manager call).
