# S-27: the periodic-status builder and its five stages executed as shipped code, every write attributed (OPUS, 2026-09-25, block 310)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-27's runtime cell is PARTIAL: "no periodic-tick
body has executed". This narrow OPUS harness executes the builder `00385DF0`, whose five stages are five of
`CONTRACT-periodic-tick.md`'s seven entries.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set.** The builder's static closure (21 functions) plus the MT19937 body behind the `00379CD0` thunk
  (`00863BF0` with its seed / regenerate helpers), 24 in all. Entering anything else fails a case.
- **One import bridge:** `memset` (thunk `00861EC0` → IAT `008C2A60`), used by stage 1.
- **The generator is the image's own**, lazily seeded by the shipped code.
- **Write attribution.** A write hook credits every non-stack write to the stage that made it; memset fills are
  credited byte by byte.
- **Fixtures** are planted data only: the stats block (`rcx`, as the tick passes `[unit+0x698]`), the two authored
  tables behind `[02EBF118]` and `[02EBF040]`, the decode base, the frame base `[01DFE0B4]`, the mode word
  `[022C314C]` and the field clock `[0208D45C]`.

**6 / 6 pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `A_order_and_empty_ownership` | I-2, I-5, §12 "no stage wrote the unit" | stages entered **1, 2, 3, 4, 5**, once each. **No stage writes the stats block.** With no statuses, **only stage 1 writes, and it writes all of `+0x08..+0x147`**: memset `0x140` bytes, then its sentinels |
| `B_stage3_effect_slots` | §3 effect-slot family, I-6, §10 | slot timers 5 / 1 / 0 plus a `0xFF` row: the new values are **written to `result+0x42+2·slot`** (4, then 0 with id 9 appended to `+0x3E`); timer 0 is skipped; `0xFF` never expires. **The stats `+0x17C` are not written** |
| `C_five_expiries_list_bound` | (observed) | five ids expire in one tick. The `+0x3E` list has four bytes before `+0x42`: **the fifth id is written onto `+0x42`, and slot 0's new timer then reads `6` instead of `0`** |
| `D_stage2_beat_and_regen` | §3 status-word family, §9, I-7 | a beat of 25 becomes **15 in `result+0xDC+2s`**; the stats beat stays 25; no draw. At beat ≤ 10 Regen (`0x19`) draws, and **each draw equals an independent MT19937 seeded 5489** (first value 3499211612). **Heal = (draw mod `byte[+0x1C2]`) + 1, ADDED**, with divisors 7, 1 and 250; flags `0x100 \| 0x400`. **New beat = row `+9` × frame base × 30** (120 at frame base 1, 240 at 2) |
| `F_stage4_drain_modes` | §9 phase, §10 fallback, I-7 | fires only when the clock is a multiple of **frame base × 10** (clocks 20 at 1 and 40 at 2 fire; 25 and 30 do not). The HP arm writes `−(src / 100)`, or **−1 below 100**; the MP arm writes `+0x2A = −(MP / 50)`, or **−1 below 50** |
| `E_I5_no_stage_calls_another` | I-5 | each stage is entered once, from the builder |

## What the execution adds to the contract

1. **I-3 is contradicted.** It says stage 1 "touches `+0x2C`, `+0x3E`, `+0x42` and `+0x13C` and nothing else".
   Measured, stage 1 writes **all 320 bytes `+0x08..+0x147`**: a memset through `00861EC0`, which a displacement sweep
   cannot see, then sentinels at `+0x30`, `+0x38`, `+0x3C`, `+0x3E`, `+0x42..+0x51`, `+0x5C..+0x11D` and
   `+0x11C..+0x13F`. The tick has already zeroed the record (`00310F7A`), so this is a second clear.
2. **No stage advances a stats timer.**
   - Stage 2 writes the new beat to `result+0xDC+2s` (executed). It writes the new duration to `result+0x5C+4s` (static
     only: `00386E43`, in the unexecuted `s ∈ {2, 6}` arm).
   - Stage 3 writes each live slot's decremented timer to `result+0x42+2·slot`. That is **every live slot**, not only
     the expired ones §3's table names.
   - The stats block is written by no stage.

   So §3's "advanced by stage 2 / stage 3", I-4's "the only body that touches `+0x17C`" (it reads it) and §12's
   "stage 3 alone moved `+0x17C`" should read: *the stages compute the next values into the record; whatever commits
   them is downstream* (`003112F0`, not executed here). That is consistent with I-6.
3. **The expiry list is unbounded (latent).** `00385570` appends at `result+0x3E+k` with no bound. A fifth
   simultaneous effect-slot expiry overwrites the low byte of slot 0's new value, measured: `6` instead of `0`.
   Whether authored data can expire five slots in one tick is not established.
4. **§9 confirmed by execution**, including the generator's identity: the shipped MT19937 is standard, seeded 5489.
5. **I-7 confirmed** for stage 2's beat reset and stage 4's interval at both frame bases.
6. **For FABLE, a question, not a contradiction.** Stage 4 writes the MP delta as **negative**. §3 calls it a "drain
   delta"; §11 says "MP creeps back at max MP / 50 per beat". The sign the player sees depends on `003112F0`'s
   application, which is not executed here.

## Not covered

- the tick entry `00310DB0` (gates, I-1's deadline check), because its closure is 1,351 functions with I/O imports;
- stage 5's credit (it ran, with no firing fixture);
- stage 2's Poison (`s = 8`), `s = 10` and duration (`s ∈ {2, 6}`) arms;
- the sink `003112F0`;
- a live game.

## I-3 and I-4 as corrected on 2026-09-25, executed (OPUS, 2026-09-26)

FABLE corrected I-3 and I-4 on this block's evidence. I-3 now reads: stage 1 zeroes all 320 bytes and plants
sentinels. I-4 now reads: stage 3 is the only body that **reads** `+0x17C`, stage 2 the only one that reaches
`+0xBC`/`+0x13C`, and no stage writes the stats block. `i4.py` executes both as worded, over this harness (imported
unchanged; its six cases run first and `result.json` is unchanged).
- **Attribution is by call frame.** A stage's return address is recorded on entry, and reaching it hands
  attribution back to the builder. That is stricter than "the last stage entered".
- **The hooks.** Reads and writes are hooked on the stats block. The translation cache is flushed after the hooks
  are added.

| case | asserted |
|---|---|
| I-4 slots | over four worlds (effect slots, Regen beat, both, empty), stage 3 is the only reader of `+0x17C`..`+0x1BB`, and in the effect-slot world it reads them |
| I-4 pair | stage 2 is the only reader of `+0xBC`..`+0x13B` / `+0x13C`..`+0x17B`, and in the Regen world it reads them |
| I-4 writes | no stage writes any byte of the stats block, in any world |
| I-3 | in the empty world, stage 1's memset covers exactly `0x140` bytes at `result + 8`; no `0xCC` fill is left in `+0x08..+0x147`; the 32 dwords from `+0x5C` and the 32 words from `+0xDC` are all −1 |

**Runs.** 4/4 pass, and two runs give an identical `i4_result.json` (md5 `67bbf320973e8284926eb38a7eb2383e`). The
evidence class and the single `memset` import bridge are the same as the block above.

## Stage 2's damage, Sap, duration and Stop arms, executed (OPUS, 2026-09-29)

Requested by FABLE (`FABLE-REQ-OPUS-POISON-ARM-REPLAY`) for `PKG-GP-STATUS-POISON` Q6. `poison.py` drives `00385DF0` over
this harness, imported unchanged: its six cases run first and `result.json` stays byte-identical
(`d8406998fe0ef323a461472e66486799`). The expected values are the stage-2 table of
[the status write](../../../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md).

**Record fields**, read from `00386C70` in the image:

| field | offset |
|---|---|
| HP delta | `+0x24` |
| flag A | `+0x2C` |
| flag C | `+0x140` |
| apply mask | `+0x54` |
| remove mask | `+0x58` |
| per-status duration | `+0x5C+4s` |
| beat | `+0xDC+2s` |

**Fixtures:** max HP is stats `+0x24` and current HP is `+0x48`. Each case sets stage 4's drain modes `[022C314C]`
to 0, because the harness's case F leaves them at 3 in image data. A first run without that reset read −10 on every
case: that was stage 4's drain, not stage 2.

**14 / 14 cases match, and two runs give an identical `poison_result.json` (md5 `92236ab0e18e826e57eb7c50c4d434d8`).**

| case | expected (page) | observed |
|---|---|---|
| 1. Poison, beat expiring, max HP 1000 | −62, flag A `0x140`, flag C `0x4000` | −62; flag A `0x141`; flag C `0x4000` |
| 2. Poison under Bubble (bit 28) | −125 | −125, and HP Critical applied (500 − 125 = 375 is below the doubled line 400) |
| 3. Poison under Disease (bit 16), current HP 40 | −2 | −2 |
| 4. Poison at max HP 15 (a zero share) | −1 | −1 |
| 5. Sap at HP 1 / HP 2 | nothing / −1 with flag A `0x100` | 0 with flag A `0x1` / −1 with flag A `0x101` |
| 6. A word-1 status whose duration reaches 0 (11 → 1 as a control) | remove-mask bit | remove `0x100000` (bit 20) and duration 0; the control is not removed, duration 1 |
| 7. Stop present with Poison | Poison skipped | no delta, no `0x140`, Poison's beat record untouched (−1) |
| 8. Poison from HP 250 | below the line 200 | −62 and HP Critical applied |
| 9. HP Critical present, HP 500 | at or above the line | −62 and HP Critical removed |

**One row of the page is contradicted: the HP-Critical check is not gated on an HP write.** The page's "after the loop"
row says the check runs "when the record carries an HP write (flag A bit 8)". The code does something else:
- `00386F78`–`00386F95` loads current HP (`+0x48`) and tests flag A bit 8 **only to choose the compared value**.
  - With bit 8 set, it compares current HP plus the delta, or the delta alone when flag A bit 3 marks an absolute
    write.
  - With bit 8 clear, it compares current HP.
- The line comparison and the add/remove of bit 29 then run on every call.

Three competing-reading cases execute it:

| case | observed |
|---|---|
| 10. No status at all, HP 100 | HP Critical **applied** |
| 11. No status, HP 500 | nothing |
| 12. Only HP Critical present, HP 500 | HP Critical **removed** |

Cases 5a and 5b show the same thing: Sap with no HP write still applies HP Critical at HP 1. So, whenever the builder
runs, stage 2 re-derives HP Critical from the unit's HP. That holds for this builder; whether the tick entry
`00310DB0` calls it for every unit is not executed here. The page correction is routed to its owner.

**Not covered:** the s ∈ {2, 6} count arm (Petrify and Doom); the tick entry and the sink `003112F0`; a live game.
