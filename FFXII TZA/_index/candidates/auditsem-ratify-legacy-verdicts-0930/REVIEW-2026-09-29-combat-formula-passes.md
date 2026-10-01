# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-COMBAT-FORMULA-PASSES · SWE2-AUDIT-SEM 2026-09-29

Passes: `38de330fc` (four combat-action contracts), `28b695117` (two
combat-formula contracts). Six regressions re-run non-author — FAILS 0 each.
Image `73461D08…21F8`.

## Named census attacks — all fail

**CB-1 width census — reproduced exactly** by my own per-body instrument
(not the checker's chunking): `+0x6B7` = 7 accesses (6 byte + exactly one
word at `003106EB`); `+0x6B8` = 64 accesses (45 qword / 15 dword / 4 byte)
with exactly three `lea` (`006C882E`, `006CA589`, `006CA977`).

**CS-2 writer census — survives as scoped.** Whole-image per-body census
of `[reg+0x714]` writers: the BattleUnit_*-named writers are exactly
`CommitAction` (`0030F806`, `mov word[rbx+0x714],di`),
`CancelAndResetCurrentAction`, `ResetStateForReuse` — plus 9 non-BU sites.
Those non-BU sites are NOT battle-unit writers: they store different widths
and types on other objects (`movups xmmword`, `0x3F490FDB` = pi/4 float,
`0x3F800000` qword init). The claim is correctly scoped "among the bodies
named BattleUnit_*" — disclosed residual only.

**ST-4 — stronger than the checker required.** My own table read (TB =
`01EFA5C0`, 202 slots) + per-target census: the 60–79 band has 16 distinct
targets; EVERY one writes `02AEE054`, and 14 of 16 write all three scratch
cells (`054`/`058`/`05C`). (The checker only asserted `>= 1`; the true
statement is all-16.)

## Verdict

**ACCEPT** both passes — the censuses reproduce under independent
instrumentation and the one scoped claim is honestly scoped.
