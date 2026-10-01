# S-12: the weather roll executed end to end against the contract's model and an independent MT (OPUS, 2026-09-25, block 339)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** Block 303 executed the weather **apply** `0026D910`
over the shipped tables. It left *"the roll `0025ACA0` end to end"* uncovered, and `CONTRACT-weather.md` §13 says
*"Empty"*. This harness executes the roll: `0025ACA0` with its real probability source `002658B0`, its real
transition resolver `0025ABA0`, and the real gameplay MT19937 draw (`00379CD0` → `00863BF0`).

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` from block 338. There is no application stub.

**The MT** is seeded by the shipped seeder `00379CF0` → `00863D30` → `00866D60`, with 4537. The harness checks every
roll against an **independent MT19937** (`init_genrand`, standard tempering) seeded the same way.

**Stop boundary** (recorded, nothing substituted): `0026D910`, the apply the roll tail-jumps to, which is block 303's
subject. The slot it receives in `ecx` is the roll's result.

**Fixtures:**
- the persisted slot byte `+0x1060` of the payload `002EF2B0` returns;
- the script-loaded bit `[02098E20]` bit 0;
- the script block `[02098E10]`: word `+0` ≥ 7, `+0x64` the section offset, and `section[1..3]` the three probabilities
  as signed bytes;
- the debug override, dword `+0xAAC` of the object `001D50D0` returns;
- six idle objects.

**2 / 2 pass, and `result.json` is byte-identical over three runs** (md5 `764763c09856b240c77092f7fbe5c6cf`).

| case | contract item | observed |
|---|---|---|
| `roll_matches_the_contract_model` | §12 roll / resolve / probability, I-1, I-2 | **60 rolls**: 10 persisted-slot / probability settings × 6, with the MT advancing throughout. Each slot `0025ACA0` hands the apply equals §12's model driven by the independent MT |
| `override_and_unloaded_script` | §12 | A positive debug override replaces `persisted + 1` as the start slot. With the script not loaded, every probability reads 33 (`0x21`) |

The settings cover every branch:
- probability 100 (no draw);
- probability 0 (straight to the resolver);
- partial probabilities, which draw `(u64(mt) * 100) >> 32` against the threshold;
- each resolver arm for start slots 1, 2 and 3, including slot 2's own 50/50 draw;
- a negative probability byte (`−5`, signed).

## What the execution adds

1. **The roll is executed end to end** with the real MT, so the weather transition is observed, not only read. The
   contract's §12 formulas (the `+1` domain crossing, the saturating probability index, the two draw sites and their
   `* 100 >> 32` scaling) all agree with the shipped code over 60 rolls.
2. **The MT's seeding path is confirmed**: `00863D30` seeds the default `0x1571` (5489) lazily if it has not seeded
   yet, then the given seed. The draws after `00379CF0(4537)` are `MT19937(4537)`'s.

## Not covered

- the field-runtime init core `002620E0`, which is the roll's only caller (P-1 / P-2);
- the verb handler `003565C0`;
- the presentation body `0040AAD0`;
- a live game.

## P-1 / P-2 executed; where I-3, I-6 and I-7 already stand (OPUS, 2026-09-26)

`p12.py` runs over this harness (imported unchanged; its cases run first). It executes the init core `002620E0` in its
three arms with its callees real. EXP-106 had scripted its external chain (the roll `0025ACA0`, the notifications
`003601C0`).
- **Harness change, disclosed.** This block's apply stop (`check.on_apply`) is neutralised for the file. The roll's
  tail jump then runs the apply `0026D910` as shipped, over the shipped `map_ref.bin` / `gramap_weatherinfo.bin`,
  published as block 303 publishes them (field 464).
- **Stop boundary** (recorded): the presentation body `0040AAD0`. Allowed to run, it faults at `003AB970` on render
  state this world does not build.

| case | asserted |
|---|---|
| P-1, non-primary | `+0x28` = 1: returns at once; nothing entered; `+0x10` unchanged |
| P-1, latched | `+0x10` bit 2 set: no roll; the bit stays |
| P-2 | the latched arm still reaches `002621A8` and runs `003601C0(0x0B)` and then `003601C0(0x0C)` |
| P-1, fresh | the body runs the roll `0025ACA0`, whose tail jump runs the apply, up to the presentation boundary |

**Not executed:** the fresh arm's own bit-set (`002621A4`) and its notifications. They come after the presentation
returns.

**Runs.** 4/4, and two runs give an identical `p12_result.json` (md5 `cc3d77bab26ed1d29565715740efdff8`).

**Where the other three S-12 invariants already stand, stub-free:**
- **I-3** (the gate discards, cleared once) and **I-7** (the apply is not slot-atomic): block 303's
  `gated-discard-and-split-slots` case (`s12-opus-replay-weather-apply`).
  - With the gate armed and committed slot 1, request slot 3: the gameplay extraction calls `00377850(351, 3)` and the
    presentation path calls `00377850(351, 1)`.
  - `+0x1061` is written 0 once.
- **I-6** (`{0,0,0}` pins the current slot): this block's grid.
  - `(persisted 0, {0,0,0})` → slot 1, and `(persisted 2, {0,0,0})` → slot 3.
  - With the override, slot 2 → slot 2, all through the real resolver `0025ABA0`.

## P-1's fresh arm run to its end (OPUS, 2026-09-26, `p1fresh.py`)

`p1fresh.py` imports `p12.py` with its default boundary, so p12's cases run first, unchanged; `p12_result.json` keeps md5
`cc3d77ba…`. It then lifts that one boundary: `0040AAD0` and its closure join the allowed set. It plants the one object
the presentation reaches that this world lacks: the 0x80-record pool (stride 0x70) behind `[02B3F528]`, which
`003AB960` scans for a free slot, as a zeroed block. **No application stub.**

**1 / 1 pass; `p1fresh_result.json` is byte-identical over two runs (md5 `b278bf5d…`).** The fresh arm (`mgr+0x28` = 0,
`mgr+0x10` bit 2 clear) runs in this order:
1. the roll `0025ACA0`;
2. the apply `0026D910`;
3. the presentation `0040AAD0`;
4. **the bit-set `002621A4`**, after which `byte[mgr+0x10]` has bit 2 set;
5. the same tail `002621A8` the latched path takes, which notifies `003601C0(0x0B)` and then `(0x0C)`.

The call returns normally. P-1's *"sets that bit itself"* is executed.
