# S-27: the per-unit periodic tick executed end to end with NO application stub (OPUS, 2026-09-25, block 320)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** Block 310 executed the builder `00385DF0` alone and left the
entry `00310DB0` unexecuted (its closure is 1,351 functions). With block 318/319's world builder, the whole per-unit tick
now runs: gates, I-1's deadline check, the builder and the sink `003112F0`.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` copied from block 319:
- **The world.** Five shipped initialisers, nine zero-filled singleton blocks, TEB / TLS, and named import bridges only.
  `world.py`'s docstring and the block 318 README list them.
- **The entry.** `00310DB0` runs over its static closure plus the listed extras, with **no application stub**. Every
  run reaches the entry's own `ret`.
- **Per-case fixtures** are planted data only:
  - the unit: flag word, a class-3 actor with a position block at `+0x10`, the stats block at `+0x698`, the deadline
    at `+0xDD0`;
  - the stats block's Regen status word and beat;
  - the tick counter `[0208D45C]` and the global mode `[022C2160]`;
  - party-slot record 0 at `02098E20` (`+0` active, `+4..+6` non-zero, `+7 = 3`), which the readiness predicate
    `00265680` requires.

**4 / 4 pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `full_tick_stub_free` | §2, §7 | in order: the recompute (`00310DE4`), the deadline check, **the builder, then the sink `003112F0(result, 0, stats, 0xFFFF, 0)`**; the tick returns (98 functions entered) |
| `I1_deadline_between_gate1_and_gate2` | I-1 | an expired deadline (5 < counter 100) **clears bit 30**, and a live one keeps it. **With no stats block (gate 1) the check never runs and the stale bit stays.** With gate 2 refusing (mode 5), the check **still ran and cleared it** before the refusal |
| `gates_refuse_the_builder` | §4 gates | global mode 5 or 6, no ready party slot (`00265680` = 0), and unit bit `0x1000000000` each end the tick **before the builder** |
| `sink_commits_the_beat` | block 310's finding | a stats-block Regen beat of 25 reads **15 after the whole tick**, written **once**, at `003115F8`, inside the sink's copy `003115B6..00311606`. The stages compute the next value into the record (block 310) and **the sink commits it** |

## What the execution adds

1. **The S-27 tick entry is executed, stub-free**, including the gate order I-1 depends on (the contract's §4 table and
   the FABLE correction to I-1).
2. **The commit is the sink's.** Block 310 showed that no stage writes a stats timer; here the sink writes the stats
   beat once, from the record, at `003115F8`. This also confirms by execution the SECTION-01 (Update01) overlay's R2
   correction to the apply-result contract ("`result+0xDC+2i -> stats+0x13C+2i`"), which OPUS's owner review
   (block 184) had confirmed statically.
3. **`00265680` is a party-slot readiness predicate.** It needs every active record in the 0x288-stride table at
   `02098E20` to be loaded (`+7 & 3 == 3`, `+4..+6` non-zero), and it returns 0 when none is active **only if** a
   record is flagged active; an empty table passes the scan and falls through to `002E0540` / `00265720`.

## Not covered

- stage 5's firing and the drain modes through the full entry (block 310 covers them at the builder);
- the sink's other arms (EXP-149 runs the sink with real callees);
- idle objects for the nine zero-filled singletons;
- a live game.

## S-32 LC-5 executed in this world: the periodic tick advances the loot stream (OPUS, 2026-09-26)

`lc5.py` runs the whole tick `00310DB0`, to its own ret with no stub, over this harness (imported unchanged; its cases
run first).
- **The loot stream** is the LCG at `022C256C` (`x = x·0x41C64E6D + 0x3039`). `00319530` steps it three times per draw
  and stores it back at `00319582`. Each run seeds it with `0x1234ABCD`.
- **What the draw needs.** After the sink, the tick draws only for a unit that:
  - is the party focus (`003273B0`) or has `[unit+0x714] = 0x4165`;
  - overlaps a loot pickup (`Loot_FindOverlappingPickupIndex` `002FB150`: 10 slots, flags at `022BE7F0`, positions at
    `022BE800`, stride 0x20);
  - and whose `stats[+5]` is 0 (`00311130`/`00311136`).
- **Planted.** Pickup slot 0 is active at the actor's position, `[unit+0x714] = 0x4165`, and this unit is the
  battle-unit pool's one unit (`[0208E688]`/`[0208E6A0]`). The pool entry lets `002F9400`'s owner lookup `0031B860`
  resolve for a foe-kind record.
- **Allowed shipped targets.** Two shipped functions that the pickup path enters indirectly, `002FD8D0` and `002FD150`,
  are allowed with their closures. They are not stubs.

| case | asserted |
|---|---|
| `stats[+5]` = 0, pickup overlapping | the tick enters `00319530` once, from `00311146`, and the stream has moved exactly three LCG steps (`97852BD0`) |
| `stats[+5]` = 1, pickup overlapping | no draw; the stream is unchanged |
| no stats block | no draw; unchanged (gate 1) |
| no overlapping pickup | no draw; unchanged |

**So the loot stream moves on a party-kind unit's periodic tick when it stands on a loot pickup**, not only on a kill.
That is LC-5.

**Runs.** 4/4, and two runs give an identical `lc5_result.json` (md5 `f45cd4f1a84e939c7bf11c7d20d7b0ff`).
