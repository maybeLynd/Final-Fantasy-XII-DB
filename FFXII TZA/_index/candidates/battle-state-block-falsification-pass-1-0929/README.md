# Consumer check: falsification pass 1 on CONTRACT-battle-state-block (OPUS, 2026-09-29)

corrects: 11-Party/Battle-State-Block/CONTRACT-battle-state-block.md (the binder's reset, BS-3's reasoning, where BS-5 holds: CON-171)
corrects: 12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md (the rebase runs BEFORE the binder's reset: CON-171)

## What was corrected

- **The binder's reset is `BattleSystem_ResetRuntimeState` (`00237DF0`), not `002370C0`.**
  - It runs `002370C0` first, through `0023AF50`.
  - It ends with `00329CC0`, which fills map 0 from the authored table and copies it into maps 1-4.
  - So after a binder reset the five maps are identical.
- **BS-5's disagreement (map 0 `0xFFFF`, maps 1-4 zero)** is `002370C0`'s own result. It survives only on the setsavedata
  scenario arm of `00239960`, which calls `002370C0` directly. That arm reaches neither `00329CC0` nor the refresher
  `003266C0` through direct calls to depth 8; indirect calls were not followed.
- **BS-3's "not two identical operations".** Nothing reads the block before the memset, so the magic already being set
  cannot make the two first-bind resets differ in the block.
- **The BS-2 table's `jne`** is the fall-through past `00233C53 je`.
- **What survives.** BS-1 (the save-payload offset `0x4E68C`), BS-2's counts (two, one, none), BS-3's bytes, BS-5's loop
  as a statement about `002370C0`, and the `+0x5AC8`/`+0x5ACC` zeroing.

## Current consumers

- consumer: [CONTRACT-bazaar-unlock-and-purchase.md](../../../12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md): revised-here.
  Its FZ-3 note said the binder's rebase acts on a block that was just reset; the reset follows the rebase. The
  conclusion (no bit-0 clear survives) stands.
- consumer: [the setsavedata presets](../../../11-Party/the-setsavedata-presets-test-battle-scenarios.md): agrees. Its §2.2
  names `002399E9` as the direct reset and `-2` as the route to `BattleSystem_ResetRuntimeState`.
- consumer: [version stamps and what loading normalises](../../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md):
  agrees (`00237DF0` reaches `002370C0` through `0023AF50`).
- consumer: the field map (`the-battle-state-block-field-map.md`) calls `002370C0` "the block reset" and says nothing
  about the maps after the binder. Not revised.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-171`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_battle_state_block.py`, checks K1-K3 and B1-B5.
- K1 fails unless the binder reaches only `00237DF0`, whose first-call chain reaches `002370C0` and whose call at
  `00237E41` is `00329CC0` with no branch around it.
- K2 fails unless `002370C0`'s only other caller is `00239960` and its direct arm reaches none of the three map writers.

run: verified at 9ede80afb (BROKEN 0), against the certified image `73461d08…`.
