# OV-34: no dispatcher moves a prepared state1 owner; only deletion ends it (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-34, `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` §8):** "The eventual
dispatcher/transition for a prepared state1 owner, if used by shipped callers."

[`state1.py`](state1.py) runs A, D, G and C: FAILS 0 ([output](state1.out)). Static.

**Answer: there is none.** The producer selects state 1 when the manager's `+0x201` byte is non-zero. That byte is the
manager's skip mask (OV-15, 8764d1109): a source produced while its manager is being skipped is prepared and pinned but
never queued.

From then on:
- **A.** The owner array is used only by the two deleters, the producer, the handle getters, the initialisers, the armer
  (state 0 → 2 only) and the two state-4 consumers.
- **D.** The deleters take state 1 to 0: they free the backing and clear the handle and state. State 3 goes to 5.
- **G.** Every reader acts only on state 4, so a state-1 owner is never delivered as ready.
- **C.** State 4 is written only by the completion callback `003DD850`. The callback is referenced only by the submitter
  `003DDA70`, whose only caller is the producer's skip-mask-zero branch. A state-1 owner has no queued read, so the callback
  never runs for it.

**For a reimplementation.** A source produced during a skip is dead weight until the script or teardown deletes it. It is
never loaded later when the skip ends, as the page's §4 already observed in its fixture ("does not submit merely because
hold later clears").

**Limit.** The census covers the owner array's rip-addressed users and the callback's references. A function handed an
owner pointer by any other route would escape it. None was seen in the functions read.

run: state1.py at 73d721948, FAILS 0.
