# UQ-133: when the Vendor of Goods can first be used (FABLE, Claude Opus 5.5, 2026-09-27)

**Question left open by the 2026-09-18 narrowings.** Row 24's gates run from 145 to 5,100. The vendor that uses
row 24 stands in field `fon_b01`. What the database did not hold was the story progress at the player's first visit,
so it could not say which gates are already met when the vendor can first be used.

**Answer: 3,100.** From the first visit the vendor offers everything except entry 0, the Diamond Armlet, which joins at
story progress 5,100.

## Evidence (DATA: the shipped scripts and the shop table)

- **The arrival event.** `fon_b01`'s `main(1)` tests the story counter (`シナリオフラグ`) against `0xBFE` (3,070). At or
  below that value it plays arrival event 0 (`eventplay_ec`) and skips the rest of `main`.
- **The counter afterwards.** Three actor functions in `fon_b01` then set the counter to `0xC1C` (3,100), each after the
  event's `eventsync_ee` and the save crystal's `showon` request. These three writes are the script's only writes
  outside its `PUSHDBG` debug jump table, which sets arbitrary values from a debug selection.
- **No later arrival can skip it.** Across all 1,114 decompiled scripts, no write sets the counter anywhere in
  3,071..3,099. The same census finds the writers of 3,070 and of 3,100, so it is not blind. The counter therefore
  never stands in that gap: a player is either at or below 3,070 on arrival, and the event moves them to 3,100, or
  already past it.
- **What that means for the stock scan.** Row 24's first three gates, re-read from `battle_pack.bin`, are 5,100, 3,100
  and 3,050 (kind 2). `002FAD40` returns the first passing entry, and the vendor lists from there to the end. At 3,100
  the first passing entry is entry 1, so entries 1-38 are on offer from the first contact. Entry 0 opens at 5,100,
  which normal play reaches: the field `gil_d01` and event `evt_t0090` write it.

So the row's authoring quirk, per-class ladders with descending gates, is invisible to a player. Every gate from 145 to
3,100 is already met before the vendor can be spoken to. The lines the 2026-09-18 narrowing listed for progress
below 145, or at 3,050, never occur at this vendor in normal play.

## Limits

- **The decompile.** The scripts are the archive's `plan_map` / `event` containers decompiled with `ff12-script`. The
  corpus is untracked scratch, so the control takes its directory and pins `fon_b01`'s listing by SHA-256.
- **Static only.** Nothing was observed live. The "no write in the gap" census covers the shipped scripts only; writes of
  the counter from native code are not censused here.
- **Debug scripts.** They can set any value; the answer is for normal play.
- **Scope.** The shop contract's general caveat (other rows' fields reached before their lowest gate, SG-2) is not
  answered here; only row 24's instance is.

## Files

- `uq133_first_visit.py ATS_DIR`: 6 checks, FAILS 0.
- `consumer-check.md`.
