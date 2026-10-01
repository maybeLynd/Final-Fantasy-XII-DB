# S-46: the generator routing re-run under a strict world, plus I3's shared stream (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-46's runtime cell reads *"I4 executed stub-free;
I1/I2/I3/I5/I6 unexecuted (EXP-056/111/144 stubbed)"*. EXP-144 runs every consumer and generator body as shipped, but
two things keep it from being stub-free:
- its import handler returns a constant for **any** import, which is a generic IAT boundary;
- nothing fences which functions run.

## What was run

`check.py` imports EXP-144's module **unchanged**: its nine cases, fixtures, planted generator states and snapshots. It
replaces only EXP-144's `World` with a subclass that:
- **bridges exactly two named imports,** `_time64` (returns `0x1BADD00D`) and `clock` (returns `0x0C0FFEE`). These are
  the two CRT time sources inside `0015BCF0`. **Any other import fails the case by name.**
- **fails the case if a function outside the entry's static closure is entered.** The closure uses the graph's call edges
  plus the tail-jump targets in `TAILS`, which the graph lacks: `0018D680`, `0018D740`, `0018EE20`, `00328370`,
  `002658B0`, `00863D30`, `00863BF0`, `00379CD0` and `00866B90`.

**No application stub.** **All 12 checks pass** (EXP-144's nine, plus I3, I1 and I5), and **`result.json` is
byte-identical over two runs** (md5 `074384c77c4f27c3042752c2584d46b5`).
- **The only imports any case reaches** are `_time64` and `clock`. So EXP-144's generic boundary was never used for
  anything else.

| check | contract item | observed |
|---|---|---|
| EXP-144's nine routes | I6, generators §4 | each consumer advances **exactly its claimed generator**: the loot inliner `003185D0` and the yaw `00239210` → the LCG; the weather roll (slot 2), `0038DB10` and `00389670` → the gameplay MT; `004005E0` → the presentation PRNG; `0015BCF0` and `0018D740` → the graphics MT. The weather roll's slot-1 arm touches none. Both LCG consumers end at three ANSI rounds (`0x11111111 → 0x15EAB4E4`) |
| I3 | I3 | the loot inliner, then the yaw, **in one world with no re-plant**: the LCG ends at three rounds of three rounds (`0xD6217D13`). The second consumer continues the first one's stream |
| I1 | I1 | no case writes both MT states. The graphics-MT cases never write `02EB3870`, and the gameplay-MT cases never write `01F7F600` |
| I5 | I5 | `gfxmt-seed` writes the graphics state inside `01F7F600 .. +0x9C4` |

## Not covered

- I2 (a census-method statement; static by nature);
- I4, executed in `s46-opus-replay-area-seed` (block 336);
- a live game.
