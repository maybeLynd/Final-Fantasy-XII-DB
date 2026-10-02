# Consumer check: 10-Status contradictions from a local reconstruction-readiness pass settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-STATUS-1002: stream R run locally, with no cloud credit. A read-only reader mapped
`10-Status-Periodic-Terminal/` (rated MOSTLY; the map is filed in the RE repo as `docs/readiness/10-status.md`) and found 46
contradictions. It also found two shared claims the bytes refute: stage 5 overwrites result `+0x24` rather than
adding to it, and the "index `0x14`" is a raw pointer value. A second read-only pass drafted the strike edits
(`apply_10status.py`, 111 edits).

OPUS checked the value-changing items at the bytes (`status_check.py`, 24 instructions):
- 1: status 28's removal halves HP, and the applier fires.
- 2 / 4: the evaluation context merges `+0x68` / `+0x78` and takes the target's status words.
- 5: stage 3's slot table is `02EBF040`.
- 8: stage 5's base is `0208D480 + 0x14`.
- 13: the mode is 0..5.
- 14: stage 2 writes durations.
- 15: `002373C0` sets `0x800` only.
- 16: Petrify / Doom store 11.
- 20: `002FA560` is the 28-kind MMSG dispatcher.
- 23: `r14` is zeroed.
- 38: `0030E816` is the recompute tail.
- the two image findings.

Stale "not read / open" claims are struck with pointers to the pages' own dated answers, and only the disfavoured side
of each pair is edited.

- **Affected:** 10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md, 10-Status-Periodic-Terminal/CONTRACT-effect-layers.md, 10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md, 10-Status-Periodic-Terminal/CONTRACT-status-write.md, 10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md, 10-Status-Periodic-Terminal/README.md, 10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md, 10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md, 10-Status-Periodic-Terminal/the-thirty-two-statuses.md, 10-Status-Periodic-Terminal/where-mp-comes-from.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the ten 10-Status pages (each disfavoured side; README labels and the six omitted pages) | revised-here |
  | combat formula pages using the evaluation context (`003847C0`) | agrees (they cite `+0x1A` merged effect ids, not statuses) |
  | RE repo `docs/readiness/10-status.md` (the map, with OPUS's verification header) | routed-to-OPUS (filed from this commit) |
  | the periodic tick's structural hole after `00310FAC` (the map's main gap) | routed-to-OPUS (left for a later read; no page claims it) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-status-readiness-fixes-1002/status_check.py, verified at 11ff52fc5: 24 instructions decode as cited, FAILS 0 ([`status_check.out`](status_check.out)). `apply_10status.py` re-runs as ALREADY (111), FAILS 0.
