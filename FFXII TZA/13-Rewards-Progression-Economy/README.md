# Rewards / Progression / Economy

**Engine category.** XP, LP, gil, drops, steals, poaches, chain state, and reward triggers.

| | |
|---|---|
| Classification source | PrimaryOwner: Rewards/Progression/Economy |
| Functions | 38 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md) -
  **PARTIAL, tier 1.** Every loot roll is **`draw % 100` against an authored percentage**, drawn
  from the deterministic shared LCG. Chain has **four ranks** with a penalty that scales with the
  rank you are already at. Found by a write-scan, not by reading this category.
- [`experience-and-license-point-award.md`](experience-and-license-point-award.md) —
  **PARTIAL, tier 1 gates.** Who earns EXP and LP when something dies. Eligibility is gated on
  the **same `0x80000003` status mask that blocks acting** — a disabled character earns
  nothing, not less. EXP is divided by a live count of eligible recipients.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
