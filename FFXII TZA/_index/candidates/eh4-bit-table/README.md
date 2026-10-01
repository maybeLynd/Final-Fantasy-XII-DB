# EH-4: the producer disposition of every index of the actor record's `+0x1C` request word (OPUS, 2026-09-27)

**Question.** EH-4 asks what any flag bit means. For the 32 indices of `+0x1C`, the page's passes name four and route
or leave the rest. OPUS's extraction of the page left 21 of them as "unstated" or "routed". Which of those can hold a
1 at all?

**Discriminator.** A bit becomes 1 only through a writer, so the writers are enumerated and their outputs combined.
The record block is memset to zero before the initialiser runs (`eh4-rekey/`).

| writer | indices it can set |
|---|---|
| initialiser presets `00266BD0` (by `+0x03` kind row) | 0, 2, 3, 4, 5, 6, 7, 10, 11, 14, 16, 17 |
| masked RMWs (initialiser, battle-unit refresh) | 2, 10 (and they clear 8, 13) |
| engine literals through the setter `0026B4A0` | 8, 13 (`fieldsign`), 10 (battle-unit refresh), 11 (`camerachange`) |
| script `reqenable` literals (all 22,281 calls literal; `Tools/work/data/census_verb_args.tsv`) | 2, 3, 4, 5, 7, 8, 11, 12, 13, 14, 16, 17 |

No other whole-word store reaches the record's `+0x1C`. The only other 4-byte stores to a `+0x1C` in the
census-receiver population are the interpreter's three call-result stores, and their base is the VM state (`rsi` = its
third argument), not the record (`r15` = its second).

**Result** (`eh4-1c-indices.tsv`):
- **NEVER SET — 17 indices: 1, 9, 15 and 18–31.** No writer produces them, so they read zero in every record in the
  shipped build. They are stated non-findings with a proof, not unknowns.
- **SCRIPT-SET, never cleared — index 12.** Scripts set it 1,525 times (the `__MJ_CTRL` moogle scripts), no script
  clears it, and the engine's read list does not include it.
- **NAMED — 2, 8, 10 and 13**, from the page's fifteenth and sixteenth passes.
- **PRODUCED, meaning not claimed — 0, 3, 4, 5, 6, 7, 11, 14, 16 and 17.** Each has its producers listed. 0 and 6
  come from presets only (rows 7 and 3–4 respectively).

**Control.** `eh4_1c_indices.py` (FAILS 0):
- W1: the whole-word stores;
- W2: the engine's literal sites, decoded from each function's entry;
- W3: the script literal set, with no computed argument;
- N: the never-set set;
- U: index 12.

**Not claimed:**
- the meaning of any produced index beyond the four the page names;
- a write from code outside the listed bodies;
- a block copy of a whole record. None is known; the re-key path copies nothing (`eh4-rekey/`).

**The other 56 bits** (`+0x08`, `+0x09`, `+0x0C`, `+0x0D`, `+0x0E`, `+0x13`, `+0x14`) keep the dispositions of the
page's passes, with the day's corrections:
- `+0x13` bits 0–1 are read, but no longer carry the LOD reading (`eh4-1c-presets/eh4_lod_receiver.py`);
- `+0x08` bit 2 is `usemapid`'s `(arg == 0)`, paired with bit 1 `(arg != 0)`, not a char-hit bit.
