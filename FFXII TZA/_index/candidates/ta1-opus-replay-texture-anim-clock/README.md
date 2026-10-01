# TA-1: the clock behind a map texture animation's frame (OPUS, 2026-09-25)

**Question (TA-1).** `002F4520` computes `frame = trunc(*[[entry+0x50]+0x90]) - 1`, where `entry` is the tag-30 runtime
entry. The pass clamps the frame and never wraps it, so the playback rate and the looping belong to whatever advances
that float. What advances it?

**Answer.** The float is a **track value of the map's tag-23 animation-slot family**, bound to **channel 9**. Its clock
is that slot's time:

| link | address | what the shipping code does |
|---|---|---|
| entry `+0x50` | `002F57A3`-`002F57CE` in the per-frame pass `002F5550` | when the entry's `+0x58` is 0, store the 0x130-byte slot record that `00466CB0` matches (tag-0 row / sequence id at record `+0x44`/`+0x46`) |
| record `+0x90` | `004677A0` -> `00466420` arm `00466488` | for every track, `00466420(record, channel, &track+0xC)`; channel **9** stores `[record+0x90] = &track+0xC` |
| delta | `004678E0(dt)` | for every active slot (`+0x4C` bit 0): `+0x48 += dt * +0x38` (the **rate**) |
| time | `004668C0` | `+0x44 += +0x48`. With `+0x4C` bit 1 (**loop**) and span `+0x40 - +0x3C` >= 1.0, a crossing wraps once by the span. Otherwise the time clamps to `[+0x3C, +0x40]` and sets bit 2 (**finished**). Then each track is sampled (`00466240`) and each record applied (`00466550`) |
| dt | `0036F460`, called by the field frame at `0022AB43` (when bit 27 of `[00226B10(0)]` is set) | `dt = (acc - frac(prev acc)) * 30 / (30 * [01DFE0B8])`, where `acc` = `[02064AC0]`, the field frame's step accumulator (1.0 x the 1/2/4 speed-up per frame), and `[01DFE0B8]` is the time-base scale (1.0, or 2.0 in the other mode) |

The shipped setters are:
- `00467620` sets active (bit 0 and bit 4);
- `004676C0` sets loop (bit 1);
- `00467660` sets the range, clamped to the authored `+0x20`/`+0x24`;
- `00467700` sets the rate (`+0x38`). ACTL's activation writes 0.0 here.

**Unit.** One time unit is one 30 Hz step at normal speed. Speed-up multiplies it by 2 or 4, and the time-base scale
divides it.

## The replay (`check.py`)

Evidence class **NATIVE-REPLAY** (unicorn), `live_game: false`. It uses `world.py`'s Session with **no application
stub**. The input is the **shipped tag-23 chunk of `dst0101.mpk`** (YM00 section, 2,112 bytes, sha256 in
`result.json`). It is read from the extracted game data with the container walk of `gen_ym00_census.py`.

**World state set up by shipped code:**
- **Arena 6** is registered the way boot does it (`0022A219` / `0022A309`-`0022A321`): `0036D240` then `00369D30(6, ...)`.
  This lets the builder's `003EC8D0(6, ...)` be served.
  - **Declared deviation:** the capacity is 4 MiB instead of boot's 108 MiB, because the harness heap is 16 MiB. The
    granularity is boot's. This is capacity only.
- **`strncmp`**, which the builder imports, is bridged with exact C semantics in this copy of `world.py`.
- **`00217150`**, the matrix multiply behind `00202D70`'s thunk, is added to the allowed set.

**Results:**
- `00466E70` builds 16 slots.
  - Slot 2 comes out active and looping (flags `0x13`), with rate 1.0 and range [0, 39].
  - `004677A0` binds dst0101's **one** channel-9 track: slot 2, track 0, record 0. The record's `+0x90` then **points
    at that track's `+0xC`**.
- **Loop on** (dt = 1.0 per call):
  - the slot time runs 1 ... 38, then **wraps to 0**, and the flags stay `0x13`;
  - the channel-9 value (the texture frame + 1) runs 1 ... 10, 12 ... 16, then **back to 1**. The track cycles on its
    own keyed period while the slot time keeps rising.
- **Loop off:**
  - the time **clamps at 39** and bit 2 sets (flags `0x15`);
  - the channel-9 value **holds** at its last value (16).
- **Rate 2.0:** the time steps 2, 4, 6, 8.

**Runs.** Two runs give an identical `result.json` (md5 `6d922dde00c692a280a8596a0fe88fbf`).

**Static only:**
- the entry `+0x50` store in `002F5550`;
- `002F4520`'s read;
- the dt derivation `0036F460`.

**Also here:**
- `census.py` writes `census.json`: every write and read the build, bind, accumulate and advance phases make
  into the slots, track states and records. That census backs the `MapAnimSlot` / `MapAnimTrackState` rows in
  `_types`. `00466240` was then read in full: the track's local time, key cursor, and a cubic between the bracketing
  keys.

**Not read:**
- which script verbs change rate and loop at run time;
- the other 460 packs' channel-9 tracks.

**Census revised the same day.** The first `census.py` registered its read hook after the build phase. Unicorn reuses
translation blocks compiled without a read callback, so the reads made by code first run during the build (the builder
runs one bind and one advance) were missed. Both hooks are now registered first.
- The revised `census.json` adds **55 entries, all build-phase reads**. It loses none, and the later phases are
  unchanged.
- The three unobserved spans (slot `+0x36`, track `+0x14`, node `+0x48`) still have **no access**, so the
  `MapAnimSlot` / `MapAnimTrackState` / `MapAnimNode` rows stand as published.
