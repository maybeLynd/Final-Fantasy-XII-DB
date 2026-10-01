# Regression: PDeferredLightingSlot0080's zero spans are explicit zero writes, not "no default set" (OPUS, 2026-09-25, repair)

**What was wrong.** Eight `_types/fields.tsv` rows of `PDeferredLightingSlot0080` said:

> *"NO DEFAULT SET HERE. The bytes are zero in every one of the 129 records … So this is not 'defaults to zero'; it is 'the
> preparation did not write here'."*

The rows were `+0x000`, `+0x008`, `+0x010`, `+0x01C`, `+0x040`, `+0x05C`, `+0x064` and `+0x074`.

That reasoning ran from a **sampled** zero (EXP-124's title-menu default buffer) to an **absence of a write**. A sampled zero
cannot distinguish untouched storage from an explicit zero write.

**What the producer shows.** `PDeferredLightingBase`'s constructor `006458A0` writes every byte of every record:
- a 128-iteration record loop at `006458E0`–`00645977` (base `+0x50`, stride 0x80), then record 128 at `0064597D`–`00645A45`;
- `esi` / `rsi` = 0 goes to each zero span;
- the 1.0 / 50 / 100 / `FLT_MAX` immediates go exactly where the sample holds them.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 353. Evidence class
NATIVE-REPLAY (unicorn), `live_game: false`. **No application stub and no stop boundary.**
- It runs `006458A0` over a `0x41D8`-byte object filled `0xA5`.
- Untouched bytes would stay `0xA5`.
- **Result:** all eight spans end 0 in all 129 records, each byte with a recorded writer inside `006458A0`. **No byte of the
  slot array is left `0xA5`.** The twelve non-zero values match the sampled defaults.
- `result.json` is byte-identical over three runs (md5 `363916f0fdb353bd9bfe1f312f5fb75a`).

**This is the smallest check that rejects the original interpretation.** If the preparation did not write those bytes, they
would be `0xA5` here.

## What changed, and what did not

- **Changed:** the meaning and evidence cells of the eight rows. The old reading is kept in the cell text as explicitly
  superseded.
- **Kept, because it is valid:**
  - EXP-124's observation that the sampled default buffer holds 0 there, scoped to the title-menu sample;
  - the record geometry (129 × 0x80);
  - the non-zero defaults.
- **Not claimed:**
  - whether the sampled default buffer was produced by this constructor (the default-buffer copy was never traced);
  - what any of these fields mean. Readiness stays `DISCOVERED` and the field names are unchanged.
- **Consumers checked:** no page or contract cites the superseded wording. `knowledge.sqlite` is a derived mirror and picks
  this up on DATA's next regeneration.
- `types_index.py --validate`: 771 types, 9,006 fields, 0 errors, 0 gaps.

Review routed to a reviewer other than the author. Meaning coordination is left to FABLE.
