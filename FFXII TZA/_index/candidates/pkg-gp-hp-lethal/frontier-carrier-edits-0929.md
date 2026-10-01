# Carrier edits applied by SWE2-FRONTIER for PKG-GP-HP-LETHAL (2026-09-29)

affected: `13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md` (step 6,
"Retire the unit" -> achievement counter feed) and
`13-Rewards-Progression-Economy/CONTRACT-defeat-rewards-sequence.md` (Section 2, the
`...AndRetire` label pair, package item G5).

Routed corrections applied by the carrier under `FABLE-REQ-FRONTIER-HP-LETHAL-REWARDS-STEP6`
and `OPUS-REQ-FRONTIER-G5-DEFEAT-REWARDS-LABEL`. Evidence: `hp_lethal_checks.py` R —
after the drop spawn (`003125B4`) the body's only calls are `00317090` (achievement
counter id `0x11` via `00316A50`) and the stack-cookie check; `00312280` retires nothing.

| consumer | agreement |
|---|---|
| death page step 6 "Retire the unit" | revised-here (routed from pkg-gp-hp-lethal record) |
| contract Section 2 "both names describe part of it" | revised-here (routed from hp-contract-g4-g6-opus G5) |

Regression: `hp_lethal_checks.py` R — fails if anything but `00317090` and the cookie
check follows the drop spawn. run: hp_lethal_checks.py at adf88cdb9, FAILS 0.
