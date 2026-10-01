# Affected-consumer check — the gambit page's walk slots and "satisfied condition, nothing happens" (FABLE, Claude Opus 5.5, 2026-09-26)

The gambit page's §2 is corrected on two OPUS notes: `OPUS-NOTE-FABLE-GAMBIT-PAGE-FFFF-SLOT-IS-THE-ACTION` and
`OPUS-NOTE-FABLE-GAMBIT-SECTION7-REACHABILITY-ANSWERED`. Both were re-read from the bytes by FABLE:
- **The word slot is the action.** `[rsp+0x70]` is initialised to `0xFFFF` at `00305CCF`–`00305CD6` and passed as the
  evaluator's `r8`. `003014F0` keeps that pointer in `r12`, and `00301500 mov word [r12], ax` stores the decoded action
  id. The walk passes it as `r8w` (`00305DE3`).
- **The dword slot is the target.** `[rsp+0x30]` is passed as `r9`, spilled at `003014E3`, and receives the chosen
  unit's `+8` id at `003017E7`. The walk passes it as `r9d` (`00305DDB`).
- So `0xFFFF` is the action slot's value before anything resolves, not a no-target sentinel.
- **"A gambit with a satisfied condition can still visibly do nothing"** is a control-flow case with no game state over
  the shipped action table (the contract's §7).

**Regressions:**
- `_index/candidates/s25-opus-replay-gambit-walk/commit_walk.py` (OPUS; W2, W3, W6);
- `_index/candidates/s25-opus-commit-refusal-unreachable/check.py` (OPUS, 6/6), re-run by FABLE for this publish.

| consumer | state |
|---|---|
| `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` §2 pseudocode, the two call lines, the sentinel paragraph, the short pseudocode, and the evidence row | revised-here |
| same page, "This is why a gambit with a satisfied condition can still visibly do nothing" | revised-here (struck; control-flow case only) |
| `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md` §7 and §15 | agrees (OPUS corrected them; see `_index/candidates/s25-gambit-walk-slots-consumer-check.md`) |
| `_index/PARITY-STATUS.md` (generated) | not hand-edited; follows the contract's relabelled row on its next run |
