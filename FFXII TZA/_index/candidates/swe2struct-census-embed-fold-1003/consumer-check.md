# Consumer check: EMBED interior arrays fold element k onto element 0; SystemStopRecord census regenerated (SWE2-STRUCT, 2026-10-03)

*SWE2-STRUCT, worked by a Claude session standing in for the Devin SWE2-STRUCT session. It follows up the census lead in
`swe2struct-systemstop08-1003` (published at `31333da6c`).*

**The defect.** `gen_route_seeded_census.py` (STRUCT's own generator) walks an `EMBED Parent +OFF stride=S count=N` route
as a derived run whose emit window is **one element** (`span = S`). It never read `count`. So a register standing at
element k > 0 (root offset `rebase + k*S`) had every access dropped.
- SystemStopRecord lost all bank-B accesses that way. The builder `00227680`'s single caller `00226C72` passes
  `r8 = 01FD4160 + 0x2A0 + i*0x18`, element 28 + i of the 56-record array. The census held 89 bank-A rows from the
  builder and **0 of its 82 bank-B accesses**: 73 at `+0x00`, 6 at `+0x08`, 3 at `+0x14`.

**The fix.**
- `_fold_element(dv, d, breg)` folds a displacement inside `rebase .. rebase + span*count` back onto element 0. Both the
  displacement and the register's base move by the same `k*span`, so the base-depth checks are unchanged. It is
  applied at the derived run's three emit gates.
- `derive_specs` reads the alternative's `count=` from the child's own route text. The alternative tuple keeps its
  shape. An alternative without a declared count is unchanged.
- **Before patching**, the unpatched generator reproduced the committed SystemStopRecord census byte-for-byte.

**The regeneration.**
- SystemStopRecord: +105 rows, 0 removed.
  - The 82 builder bank-B sites match an independently decoded set exactly.
  - The 23 caller rows are the bank-B record's accesses through `r12` in `00226BF0`: the `addr` lea, 21 reads of
    `+0x00` (flag tests and loads), and the write `00226C4B mov dword ptr [r12 + 0x10], eax`.

- **affected:** the SystemStopRecord access census (`system-stop-record-accesses.tsv`), the generator
  (`gen_route_seeded_census.py`, a `.py`) and the type store's SystemStopRecord rows. They are named in prose because
  the correction gate counts only `.md` files as touched (SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003).
- **Regression:** `census_bankb_check.py` (this directory). It decodes the builder's bank-B accesses from the image and
  requires each one in the census at its offset. Run at 4207b4a16: FAILS 0
  ([`census_bankb_check.out`](census_bankb_check.out)). On the census as committed at that sha: FAILS 82.

## Consumers

| consumer | state |
|---|---|
| the SystemStopRecord census | revised-here (regenerated with the fix) |
| type-store `SystemStopRecord +0x10` evidence | revised-here: the bank-B write `00226C4B` from the caller is appended |
| type-store `SystemStopRecord +0x14` evidence | revised-here: the bank-B store `002276B0` (`r9b`, the builder's fourth argument) and the two builder reads `00227814` / `002278F5` are appended. The meaning stays MEANING NOT CLAIMED |
| type-store `SystemStopRecord +0x00` and `+0x08` rows | consistent: the bank-B writers fit both meanings as stated. `+0x08` still has no reader |
| the system-stop contract's builder description | consistent: it already names the stores in both records (FABLE, `fable-systemstop-08-1003`) |
| the registry census (`system-stop-registry-accesses.tsv`) | not revised: a STATIC route on the registry that does not follow the builder's argument registers into the callee. A separate behaviour of this tool, and not the element-fold defect |
| the other EMBED-array censuses this generator writes | not regenerated in this publish; see the impact table below. Each one's next regeneration adds its element-k rows, and each should be diffed when it happens |

## Impact on the other EMBED-array censuses (measured, not applied)

Regenerated into scratch with the fixed generator and diffed against the committed files (first five columns):

| type | rows added | rows removed |
|---|---:|---:|
| `WorldLootDropEntry` | +0 | -0 |
| `ManagerSub8FA0SlotRecord02B8` | +0 | -0 |
| `ManagerSubA0D0Record` | +0 | -0 |
| `ManagerSub00A0Entry` | +0 | -0 |
| `ManagerSub7EA0Entry` | +0 | -0 |
| `ManagerSub7FB0Record` | +0 | -0 |
| `BattleMenuChildRecord1E0` | +7 | -0 |
| `BattleMenuPanelWidget3010Block` | +11 | -0 |
| `WidgetSingleton02AED490EntryA` | +0 | -0 |
| `WidgetSingleton02AED490EntryB` | +1 | -0 |
| `WidgetSingleton02CA99C0QueueEntry` | +7 | -0 |
| `WidgetSingleton02B457E0Record` | +0 | -0 |
| `ManagerSub5380PoolAEntry` | +0 | -0 |
| `ManagerSub5380PoolBEntry` | +0 | -0 |
| `ManagerSub5380PoolCEntry` | +0 | -0 |
| `MapScreenPageSlot` | +0 | -0 |
| `GlyphRunRecord14` | +0 | -0 |
| `PDeferredLightingSlot0080` | +0 | -0 |
| `ManagerSub0209BE80_57E0PairRecord` | +3 | -0 |
| `AuthoredExpressionRecord` | +0 | -0 |

20 types measured; the run was stopped there (at about one type a minute it was not worth the usage for an informational table). Every measured type gained rows or none, and **none lost a row**. The gains (`BattleMenuChildRecord1E0` +7, `BattleMenuPanelWidget3010Block` +11, `WidgetSingleton02AED490EntryB` +1, `WidgetSingleton02CA99C0QueueEntry` +7, `ManagerSub0209BE80_57E0PairRecord` +3) are each type's element-k accesses. The rest of the route-seeded EMBED-array censuses are unmeasured, and the follow-up regenerates and diffs each.

