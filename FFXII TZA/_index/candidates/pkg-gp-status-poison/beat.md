# PKG-GP-STATUS-POISON Q1: how often Poison hits (FABLE, Claude Opus 5.5, 2026-09-29)

[`beat.py`](beat.py) runs S, D and M: FAILS 0 ([output](beat.out)). Static, plus data.

**Answer: Poison hits every 12 seconds, at either frame rate.** The same formula gives Sap 0.1 s and Regen 1.5 s.

- **S.** Each run of stage 2 subtracts 10 from the status's beat. When the beat runs out, it reloads to
  `status_data +9 × [01DFE0B4] × 30`. The infliction's default beat is the same value.
- **D.** Byte `+9` is 120 for Poison, 1 for Sap and 15 for Regen.
- **M.** The tick runs once per unit per frame, and the frame base is 1 at 30 fps and 2 at 60. A beat therefore lasts
  `+9 × 3 × fb` frames, which is `+9 / 10` seconds.

**Premises, cited rather than re-derived:**
- the tick runs from the per-unit frame, once per frame (the world-tick page);
- the frame-base values (the boot-fixups contract).

**Not claimed:**
- a live timing. That is the package's adjacent ASTRA obligation.
- the beat during a skip, when a skipped slot's tick runs up to sixteen times a frame (OV-15's skip mask).

**The error.** The tick contract's §11 said "Poison and Sap tick on a beat a third of a second wide". A third of a second is
stage 4's field-drain interval (`frame base × 10` runs), a different timer. The tick page's §1 attributed the felt beat to
that remainder test. Both texts are struck and corrected.

affected: `10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md` (§11)

affected: `10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md` (§1)

consumer: the tick page's stage-4 section ("frame base × 10 ticks … a third of a second") is about the drain, and it agrees.

consumer: the contract's I-7 also agrees. It already lists "stage 2's durations and beats" as scaled by the same word.

consumer: the stats-record field map `+0x13C` ("`status_data +9` × frame base × 30, −10 per tick") agrees.

consumer: the status-write contract's row table (Poison +9 = 120) agrees.

run: beat.py at 022860d96, FAILS 0.
