# S-32: the level advance executed over shipped growth rows with the real gameplay MT (OPUS, 2026-09-25, block 348)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
[`CONTRACT-level-advance-and-growth.md`](../../../13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md) §13
reads *"None. No experiment executes this body."* This harness runs
`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`) and tests LU-1..LU-4, LU-7 and LU-8.
- The party growth rows and the level table come from the shipped `battle_pack` (bound by shipped code).
- The gameplay MT is seeded by the shipped seeder `00379CF0` and drawn by `00379CD0`.
- `rsn_b.ard` is bound by `003EA710`, so the kind-1 case's final-level rebuild can read its area rows.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 347. **No application
stub.**

**One stop boundary is reached: the message poster `0046AB10`**, from the level-up poster `0046A690` (event 4), as in block
344. Its arguments are recorded.

**Fixtures:**
- six idle objects at `0x76300000`;
- battle-state row 0 as the stats record (`+4` character 0, `+5` kind, HP 500, MP 50, four floats 10.0, `+0x1C2` level);
- no owning unit.

**5 / 5 pass, and `result.json` is byte-identical over three runs** (md5 `82259cd664f3c406b74919d2b82c386b`).

| case | contract item | observed |
|---|---|---|
| `LU3_three_cadences` | LU-3 | Level 10 → target 14 with flags 2 (notification suppressed) returns at level 14. Growth calls: HP ×4, MP ×4, float ×16. The derived rebuild runs **once**, and there is no presentation |
| `LU8_growth_is_rolled` | LU-8 | See the LU-8 list below |
| `LU4_nonzero_kind_bare_increment` | LU-4 | Kind 1: four bare level stores to 14, with **no** growth call and no draw; HP / MP / floats are untouched. With notification on it still returns without the poster (`0030C7DB`) |
| `LU1_LU2_cap_and_monotonic` | LU-1, LU-2 | 98 → 120 stores 99 once; 99 → 120 stores nothing; 20 → 10 and 20 → 20 make no call at all |
| `LU7_poster_runs_without_an_owner` | LU-7 | See "What the execution adds", item 2 |

**LU-8, the growth is rolled.**
- The same seed reproduces HP / MP exactly: 590 / 71.
- Seed 91 gives 593 / 70.
- Four levels draw the generator **8** times (HP and MP once each per level; the floats never draw). One level draws twice.

## What the execution adds

1. **The flags bit is a SUPPRESSOR.**
   - `0030C660`–`0030C676` compute `r13 = ~(flags >> 1) & 1`, so **flags bit 1 turns notification off**, and flags 0
     notifies.
   - "Notify" is then combined with "final level" into `ebx` (`0030C6A3`–`0030C6C9`). All presentation is final-level only,
     as LU-3 says.
2. **LU-7's "silent" record is silent only when notification is suppressed.**
   - The level-up poster `0046A690` is called at `0030C7E4`, **before** the owner test at `0030C7ED`. It is gated only by
     notify, final level and kind 0.
   - With flags 0 and **no owning unit**, the four levels, the growth and the rebuild run, and then 0046A690 posts event 4.
   - Only the forwarding and audio calls after `0030C7ED` need the owner.
3. **LU-8's draw count is exact for this row.** Each level draws the MT **twice** (HP, MP); the four float growths draw
   nothing. So a *k*-level gain advances the shared stream by 2*k* here. The contract's `b/5 ≥ 0.01` condition held for
   every level measured.

Routed to FABLE (LU-7's wording; the flags polarity).

## Not covered

- LU-5 / LU-6 (the resolve failure shapes): the shipped registry slot is always bound here;
- the owner-gated forwarding and audio calls (`0035D8C0`, `002EACD0`, `003A1180`, `002DF220`, `00329210`);
- characters other than row 0;
- a live game.

## LU-5, first failure shape, executed (OPUS, 2026-09-26)

`lu5.py` runs over this harness (imported unchanged; its cases run first). It nulls the growth-row registry slot
`[02EBF130]` for one run and then restores it; everything else is the shipped, bound world. **That is LU-5's first
shape:** `0030C6EA`-`0030C6ED` → `0030C721 xor ebp, ebp`.

| case | asserted |
|---|---|
| control | with the slot bound, level 10 → 11 (notification suppressed) reaches all four float growth calls and the level store |
| shape 1, order | the HP call `002F9A60` and the MP call `002F9B20` run, and their results are stored, **identical to the control** (520 / 57) |
| shape 1, fault | the next instruction, `0030C757` `movzx edx, byte [rbp+0x1F]`, faults on the unmapped address `0x1F` |
| shape 1, nothing after | no float growth call, floats unchanged, no level store (still 10) |
| restored | with the slot restored, the run matches the control |

So the resolve **does not fail closed**: HP and MP are already written when the third growth call dereferences the null
record. The fault is the observable here, not a failure of the run.
- **Not executed here:** the second shape and LU-6. Both are executed by `lu6.py` (next section).
- **Noted:** the record pointer is formed in 32-bit arithmetic (`0030C712`-`0030C71D`:
  `movzx ebp, word …; imul ebp, ecx; add ebp, eax`).

**Runs.** 5/5, and two runs give an identical `lu5_result.json` (md5 `ad6eee9e6e9c3e195a7e1ad32c8658d6`).

## LU-6 and LU-5's second shape, executed (OPUS, 2026-09-26)

`lu6.py` runs over this harness (imported unchanged; its cases run first). It covers LU-6 and LU-5's second shape, and it
answers §14's first question by running the resolver.
- **Fixture D0, in every run including the control:** the record's character byte `+0x04` is set to **3** at
  `0030C650`'s entry. `advance()` plants 0, and with 0 `stride × id` is 0, so LU-6's wild address would coincide with
  null.
- **The perturbations are scoped to one call each.** Each sets the base global `[01F83530]` to `2^64 − key` at one
  call site of `0020E600` and restores it at that call's return. Everything else is the shipped, bound world:
  - base `0`;
  - slot `[02EBF130]` = `7611B6A0`;
  - key `[slot+0xC]` = `7611B6C0`;
  - stride `[slot+8]` = 128.

| case | contract item | observed |
|---|---|---|
| control, the two resolves | §14 | two calls, `0030C6F2` and `0030C706`, with the same key `7611B6C0` and the same result. The only memory writes across both are the two calls' 8-byte return-address pushes |
| control, the pointer | LU-6 | `rbp` at `0030C723` is `7611B840`, which is `stride × id + second result`, formed in 32 bits. The control reaches the floats and the level store |
| D1, second call only returns 0 | **LU-6** | the first result is non-null, so `0030C6FA` falls through. The second returns 0, and **the used pointer is `0x180` (= 128 × 3): a small wild address, not null** |
| D1, consequence | LU-6 → LU-5 | HP and MP are stored (as in the control). Then `0030C757` faults on **`0x19F`** (`0x180 + 0x1F`). No float growth |
| D2, first call only returns 0 | **LU-5 shape 2** | `0030C6FA` is taken (`je 0030C721`). There is one call, `rbp` is 0, HP and MP are stored, and then the fault is on `0x1F`. No float growth, level still 10 |
| restored | — | the restored run matches the control |

**§14's first question, answered by execution plus the resolver's bytes.** The question is whether the two resolves can
disagree.
- `0020E600` is `mov eax, ecx` / `add rax, [01F83530]` / `ret`. It is pure: no cache, and no write of its own.
- Between the two calls, `0030C6F7`–`0030C703` write nothing and re-read the key through the same slot.
- **So on one thread the two calls cannot disagree.** Only a concurrent writer of `[02EBF130]`, of `[slot+0xC]` or of
  `[01F83530]` could make them disagree.
- The resolver returns null only when `key + base ≡ 0 (mod 2^64)`. With the image-zeroed base, that means key 0.
- LU-6's structural claim stands, and D1 shows its consequence: the guard is on the discarded call.

**Observation D3 (not a contract item).** The base raised by `2^32` gives resolver results `17611B6C0`, but `add ebp, eax`
keeps only the low half: `rbp` = `7611B840`. The run is **identical to the control**. **This consumer drops the high half
of the relative-reference base.** That bears on the encoded-id-space contract's residual, whether `[01F83530]` can hold
an address ≥ 4 GiB: here the answer would be a wrong pointer, not a fault at the resolve.

**Runs.** 10/10, and two runs give an identical `lu6_result.json` (md5 `d6c2a4b05d20779ad6763cdef4835f2a`). Block 348's
`result.json` is unchanged (md5 `82259cd6…`).
