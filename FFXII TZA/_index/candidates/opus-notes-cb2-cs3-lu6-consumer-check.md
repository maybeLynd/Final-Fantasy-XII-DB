# Affected-consumer check — CB-2, CS-3 and LU-6 (FABLE, Claude Opus 5.5, 2026-09-26)

Corrections on `OPUS-NOTE-FABLE-S20-CB2-FAILED-RECOMMIT`, `OPUS-NOTE-FABLE-S20-CS3-DRAINS-DIFFER` and
`OPUS-NOTE-FABLE-S32-LU6-RESOLVES-CANNOT-DISAGREE`. Each was re-read from the original bytes, and each linked
regression was re-run by FABLE on 2026-09-26 with its committed outputs restored afterwards.
**Status: PROPAGATED 2026-09-26** (it was held open for one routed consumer until then).
SWE2-AUDIT-SEM closed `FABLE-REQ-AUDITSEM-RESCORE-S32-LU6` with ACCEPT. It re-derived both points independently:
`lu6.py` reproduced 10/10, and `0020E600` is pure, with only reads between the two resolves. S-32 is L2 MET in
`_index/L2-VERDICTS.md` at HEAD (checked by FABLE).

## CB-2 — a failed re-commit zeroes the counter and partner

Regression: `_index/candidates/s20-opus-replay-commit/cb26.py`. Case F
(`F_failed_recommit_returns_0_after_the_cancel_ran`) passes.

| consumer | state |
|---|---|
| `07-Combat-Action/CONTRACT-combo-continuation.md` CB-2 body, §10 failure bullet, §12 reproduction step | revised-here |
| `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` (~230: the cancel clears `+0x6B7` and `+0x6B8` in one store) | agrees |
| `07-Combat-Action/CONTRACT-the-moment-an-action-is-committed.md` | agrees (no failure-path claim about the counter) |

## CS-3 — the two ring drains differ

Regression: `_index/candidates/s20-opus-replay-rings/check.py`. `A_action_ring_drains_at_most_eight_per_call` and
`P_presentation_ring_stops_at_the_first_unresolved_entry` pass.

| consumer | state |
|---|---|
| `07-Combat-Action/CONTRACT-native-command-seam.md` CS-3 ("the same resolve-then-act drain loop") | revised-here (drains named by role) |
| `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` §2 ring diagram ("drains until empty") | revised-here |
| `07-Combat-Action/CONTRACT-native-command-seam.md` lines on shape only (indices, stride, advance) | agrees; shape unchanged |
| `_index/candidates/s20-opus-replay-rings/README.md` | agrees; it quotes the old sentence as the thing refuted |

## LU-6 — executed, and the two resolves cannot disagree on one thread

Regression: `_index/candidates/s32-opus-replay-level-advance/lu6.py` (10/10, all pass, including
`control_two_calls_same_key_same_value`). Static: `0020E600` is pure, and there are no writes between `0030C6F7` and
`0030C706`.

| consumer | state |
|---|---|
| `13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md` §13, §14 Q1, LU-6 body | revised-here |
| `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md` | agrees (no divergence claim) |
| `_index/L2-VERDICTS.md` S-32 runtime cell ("not covered: LU-6 … §14's divergence question open") | agrees at HEAD (L2 MET; AUDIT-SEM ACCEPT 2026-09-26 on FABLE-REQ-AUDITSEM-RESCORE-S32-LU6, which this row was routed to) |
| `12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md` ~238 "two resolves" | not a consumer: a different function's resolve pair |
