# Rewards / Progression / Economy

**Engine category.** XP, LP, gil, drops, steals, poaches, chain state, and reward triggers.

| | |
|---|---|
| Classification source | PrimaryOwner: Rewards/Progression/Economy |
| Functions | 38 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`loot-drops-and-enemy-chain.md`](loot-drops-and-enemy-chain.md) -
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*. Every loot roll is **`draw % 100` against an authored percentage**, drawn
  from the deterministic shared LCG. Chain has **four ranks** with a penalty that scales with the
  rank you are already at. Found by a write-scan, not by reading this category.
- [`experience-and-license-point-award.md`](experience-and-license-point-award.md) —
  **PARTIAL, tier 1 gates.** Who earns EXP and LP when something dies. Eligibility is gated on
  the **same `0x80000003` status mask that blocks acting** — a disabled character earns
  nothing, not less. EXP is divided by a live count of eligible recipients.
- [`how-experience-is-computed-and-divided.md`](how-experience-is-computed-and-divided.md) - function note of the award page: the EXP computer and its divisor - **REOPENED** (SECTION-03 accepted 2026-10-01; the re-status is left to its owner)
- [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) - the EXP and LP computers - **BEHAVIORALLY UNDERSTOOD**
- [`what-happens-when-an-enemy-dies.md`](what-happens-when-an-enemy-dies.md) - the defeat sequence `00312280` - **DOCUMENTED**
- [`CONTRACT-defeat-rewards-sequence.md`](CONTRACT-defeat-rewards-sequence.md) - **CONTRACT READY**
- [`what-happens-when-a-character-levels-up.md`](what-happens-when-a-character-levels-up.md) - the level advance `0030C650` - **AUDITED**
- [`CONTRACT-level-advance-and-growth.md`](CONTRACT-level-advance-and-growth.md) - **CONTRACT READY**
- [`gil-storage-clamp-and-every-path-that-moves-it.md`](gil-storage-clamp-and-every-path-that-moves-it.md) - the gil setter and its thirteen writers - **AUDITED**
- [`CONTRACT-gil-storage-and-movement.md`](CONTRACT-gil-storage-and-movement.md) - **CONTRACT READY**
- [`the-chain-and-its-sticky-coin.md`](the-chain-and-its-sticky-coin.md) - the chain update and its sticky coin - **AUDITED**
- [`CONTRACT-loot-rolls-and-the-chain.md`](CONTRACT-loot-rolls-and-the-chain.md) - **CONTRACT READY**
- [`world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`](world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) - the ten-slot pickup pool - **AUDITED**
- [`CONTRACT-world-loot-pickup-pool.md`](CONTRACT-world-loot-pickup-pool.md) - **BEHAVIORALLY UNDERSTOOD**
- *(twelve pages added to this list 2026-10-02, OPUS, each with the status its own front matter states)*

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
