# V-1: the save payload's residue by every entry route (OPUS, 2026-09-27)

**Question.** The register still read "~470 bytes mapped". What of the 353,424-byte payload is not known, and does
any instruction reach it?

**Discriminator.**
- **K0:** the store's own tiling, measured.
- An offset-tracked census seeded at **every** payload entry route. The published `census_savepayload.py` used one
  route, the active getter.

**Driver.** `v1_residue_census.py`; result `result.json`. It reads the certified exe through the kit's `Image`, plus
`_types/fields.tsv` and `save-payload-accesses.tsv`.

| | |
|---|---|
| K0 tiling | closes at `0x56490`, no gap; PROVEN 335,460 · HIGH 3,095 · PROBABLE 916 · UNKNOWN 13,953 |
| UNKNOWN by owning type | SavePayload 12,018 · PersistentFlagPayload 814 · BattleStatsRecord 600 · ImageBackedStateBlock 274 · GambitConfig 160 · BattleSystemState 63 · SpawnKeepImage 24 |
| seed hosts | 311 functions; by kind, overlapping: getters 104, slots 203, absolute 12 |
| offsets touched in the eight top-level residue spans (12,018 B) | **0** |
| published census rows in them (1,725 sites) | **0** |
| raw displacements in the tail's ranges, any base, whole image | **0** |
| `+0xC818`-range displacements in census-reached bodies | **0** |

**Controls** (`controls_pass: true`):
- **K1:** every documented region is reached, and so is `+0x1044`.
- **K3:** both whole-image clears are found by their `lea 02164280` at payload −0x200.
- **K4:** a planted `+0xC900` access is flagged.
- **K5:** 602 of the published census's 1,725 sites are reproduced. This is a different instrument, and it agrees
  where it overlaps.
- **K6:** the raw sweep sees `00229B81 lea rdx,[rax+0x4E68C]`.

**Reading.** The 12,018 top-level bytes are reserved space in `AA-5`'s accepted sense:
- zeroed by the whole-image clears;
- carried with the image;
- read by nothing in this executable.

Their purpose is not derivable here. V-1 stays open for the 1,935 UNKNOWN bytes inside the five embedded types.

**Boundary:** indirect calls and index-register offsets are not tracked, and a pointer reloaded from memory is killed.
