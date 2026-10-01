# Consumer check: falsification pass 1 on CONTRACT-gil-storage-and-movement (OPUS, 2026-09-29)

corrects: 13-Rewards-Progression-Economy/CONTRACT-gil-storage-and-movement.md (section 14 item 1, the section 15 row: CON-174)
corrects: 13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md (writer table, section 10 bullet, section 13a: CON-174)

## What was corrected

- **`00290130` is not orphaned.** Its one inbound edge is the thunk `002E1A50` (`jmp 0x290130`), and the thunk is called
  at `00344C9A` in `FUN_00344C60`, the begin handler of script verb `037C questresultwindow`.
- The 2026-09-22 route census counted edges to `00290130` and never to its thunk.
- So the thirteenth gil writer, the reward-bundle applier `003F4AA0`, is the quest-result window's reward grant: gil
  plus two item lists. Its gil write is a path a player reaches.
- What the handler's two keys select is not read.
- **What survives.**
  - GL-1 to GL-4 at their instructions.
  - GL-5's counts. The setter's 13 callers are 12 calls plus `Debug_SetGilToMaximum`'s tail-jump; the thunk's 3 are 2
    calls plus `0032A850`'s tail-jump. A raw E8/E9 sweep agrees, so catalogue tails hide no caller.
  - GL-6's three `BattleAction_*` writers.
  - `BattleFormula_ApplyTargetResult` in both censuses.
  - §14's reconciliation closure, not re-run.

## Current consumers

- consumer: [gil-storage-clamp-and-every-path-that-moves-it.md](../../../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md): revised-here.
- consumer: `_index/ADDRESS-INDEX.md` lists `00290130` by page and makes no claim; it needs no change.
- consumer: `_index/AUDIT-LOG.md`, `PROGRAM-STATE.md` and the SWE2-CONTRACT inbox quote the 2026-09-22 reading as dated
  history. They are not rewritten; CON-174 supersedes them.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-174`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_gil.py` K1. It fails unless `00290130`'s only inbound edge
is the thunk `002E1A50` and that thunk's only caller is `00344C9A`, in the handler the verb table lists for
`questresultwindow`.

run: verified at cf61ace9f (BROKEN 0), against the certified image `73461d08…`.
