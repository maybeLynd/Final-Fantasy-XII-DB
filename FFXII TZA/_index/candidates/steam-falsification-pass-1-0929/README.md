# Consumer check: falsification pass 1 on CONTRACT-steam-integration-subsystem (OPUS, 2026-09-29)

corrects: 20-Platform-Online-Achievements/CONTRACT-steam-integration-subsystem.md (I-1's falsifier: CON-177)
corrects: _index/candidates/s45-opus-replay-counters/README.md ("its one writer": CON-177)

## What was corrected

- **I-1's own falsifier is met.** `01F83450` has a second writer, the manager's destructor `0020CD80`, which frees the
  manager and stores 0. It never installs one, so the invariant's substance survives. The falsifier now reads "a
  non-null store outside `0020CD30`", and the destructor is recorded as a second way into "achievements off".
- **Added, not corrected:**
  - §9's `cmp ebx, 6` branch is answered mechanically: by-id row 6 also awards entries 31-37.
  - I-3 notes that `0020CE10` relies on its one caller's Steam re-read and test of `+0x190`.
- **What survives.**
  - I-2 and I-3: every `SetAchievement` site is guarded.
  - I-4: no by-id row maps to entry 0, and no by-index call site passes a literal 0.
  - I-5: one `SteamAPI_RunCallbacks` call site.
  - I-6 and §3's order.

## Current consumers

- consumer: [s45-opus-replay-counters](../s45-opus-replay-counters/README.md): revised-here (one sentence).
- consumer: [steam-integration-and-achievement-catalogue.md](../../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)
  describes the getter and the null test, and does not count writers; it agrees.
- consumer: `_index/candidates/s45-runtime-per-invariant-exposure.md` and the SEM inbox describe I-1's consequence half;
  they agree.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-177`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_steam.py` K1. It fails unless the stores to `01F83450` are
exactly `0020CD30`'s and the destructor's null store, found by both the bounded and the linear instrument.

run: verified at e02c75920 (BROKEN 0, exit 0), against the certified image `73461d08…`.
