# S-16: EXP-145's spawn-placement execution re-run under a strict world (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-16's runtime cell reads *"EXP-145 executes spawn
placement `00234AF0` in both modes … under disclosed stubs"*. Block 294 showed that EXP-145's one scripted boundary, the
tail thunk `00861F02` (`jmp qword [008C2BD0]`), is the CRT import `atan2f`. Nothing in EXP-145, however, fenced which
functions run or refused other imports.

## What was run

`check.py` imports EXP-145's module **unchanged**: its 20 cases, its fixtures and **every assertion in its `check()`**.
It replaces only two things:
- **EXP-145's `World`,** with a subclass that:
  - treats `00861F02` as the named import it is. The name is resolved from the import directory at run time, and the
    run fails unless it is `atan2f`. The arguments are y = `xmm0` and x = `xmm1`, the registers the shipped caller
    loads.
  - fails the case on **any other import**;
  - fails the case if a function **outside the static closure** of the case's entries is entered. The entries are
    `00234AF0`, `00235330` / `00235340` and `003209C0`. The closure adds the tail-jump targets the graph lacks:
    `003DFD00`, `00328370`, `0031AC90`, `00861F02`, and `003A1960`, the squared-XZ distance reached by the thunk
    `0031E620`.
- **EXP-145's `RESULT` path.** EXP-145's own `result.json` is left as published (md5 `a04b4692…` before and after).

**No application stub.** **20 / 20 of EXP-145's cases pass with no failure**, with 34 functions allowed and 7 `atan2f`
calls. **`result.json` and `strict.json` are byte-identical over two runs** (md5 `f2114c18…` / `5e857e6b…`).

| contract item | EXP-145 cases (all passing here) |
|---|---|
| I1: a negative window restores 300 | `win-neg`, `win-zero`, `win-pos` |
| I2: the caller rejects negative, not zero | `fetch-direct`, `fetch-null`, `fetch-oob` |
| I3: two exclusive modes, validated differently | point `point-hit`, `point-arc-miss`, `point-band-*`, `point-coincident`, `point-no-slots`; area `area-box-*`, `area-ellipse-hit`, `area-shape3`; `oldfmt-point` |
| I4: only the leader is consulted | `null-leader`, `probe-allslots-fail` |
| I5: an empty band is refused first | `empty-band` |
| I6's producer half: area mode leaves `out_observed` unwritten | the area cases |
| I7: `Y` is not written | `area-box-hit`: `out.y` carries the `0xCD` stack sentinel, although the authored y was 7.5 |
| I8: the sine table, and `atan2` as the inverse | the area draws read the table as shipped. The `atan2` half is the named import |

## I6's consumer half executed (OPUS, 2026-09-26, `i6_consumer.py`)

`i6_consumer.py` runs `Spawn_SelectAndPrepareAutomaticEntry` (`00235720`) as shipped over EXP-145's world. It uses
EXP-145's fixture builders and the area-box-hit fixture, so the placement `00234AF0` inside it runs in **area** mode. The
harness is as strict as `check.py`: one named import (`atan2f`, asserted) and a closure fence (43 functions). **No
application stub.**
- **Planted data only:** an actor whose `+0x30` is a unit; the unit's `+0x38` candidate list and `+0x40` spawn index list;
  spawn record 0 with bit 0 set (no timing gate); the cap byte `[0208D458]` = 4, the attempts byte `[0208D457]` = 3, the
  threshold `[02F973B8]` = 100.0 and the max radius `[02089364]` = 15.0.
- **The stale slot (disclosed).** At `00235720`'s entry a hook writes a float into the caller's own `out_observed` slot
  (entry `rsp − 0xB4`, `[rsp+0x34]` after the prologue). It stands for whatever an earlier call left there. A write
  hook on the slot confirms that **nothing else writes it**.

**2 / 2 pass; `i6_consumer_result.json` is byte-identical over two runs (md5 `bdfdd7bb…`).**

| case | observed |
|---|---|
| `A_stale_slot_below_threshold_accepts_the_area_candidate` | stale 0.0: one placement call returns 1 **without writing the slot**. The caller accepts: the spawn record's `+0x50` / `+0x60` receive the position, the unit gains `0x4000000`, and the return value is 1 |
| `R_stale_slot_not_below_refuses_every_successful_candidate` | stale 1000.0: the same successful area placement is refused **three times** (the attempts byte). There is no spawn write and no unit flag, and the return value is −1 |

*Also observed:* the accepted position's `y` (`+0x54`) is `0xCDCDCDCD`, the stack sentinel. **I7's unwritten `Y` reaches
the spawn record.**

## Not covered

- a live game.
