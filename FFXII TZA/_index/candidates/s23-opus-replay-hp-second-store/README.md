# S-23: the HP write's second store executed — `00300530` → `0030E360` → `0030FED0`, no stub (OPUS, 2026-09-25, block 334)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-23's exposure note (block 300) found the one decisive
exposure of the row: **EXP-093's `0030FED0` stub hides a second `+0x48` store**. The contract was corrected on paper
(its §4 boxed correction). The second store had been shown only by EXP-148's separate run of `0030FED0` and by the
static chain. This harness executes it **inside one call of the HP write**.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from block 333. These run with
**no application stub and no stop boundary**:
- the HP write `00300530`;
- its real status transition `0030E360`;
- the recompute `0030FED0`;
- the gates and the owner resolver.

**The flags word.** The caller's flags select the setter's own presentation-free path:

| bit | read at | effect when set |
|---|---|---|
| 1 | `0030059C` | skips the death credit `00469BB0` |
| 4 | — | skips `003283D0` |
| 7 | `00300601` | skips the display `0028F1F0` |

`0x50` are I7's target-HP bits. The harness hooks confirm that none of the three presentation calls runs.

**Fixtures:**
- four idle objects;
- the unit pool with the target's owning unit, whose `+0x10` actor is a zeroed block;
- the stats records: `+0x48` HP, `+0x24` max HP, `+0x64` status.

**3 / 3 pass, and `result.json` is byte-identical over three runs** (md5 `d596bea75a0baba610b38bf2c181c844`).

| case | contract item | observed |
|---|---|---|
| `second_store_on_the_lethal_path` | §4 postcondition / invariant (corrected) | One lethal call (HP 100, delta −150, with a source and with a null source) **stores `+0x48` twice**: `00300530`'s own store at `00300749`, then, through `0030E360` (KO bit 0, mode 3) and `0030FED0`, **again at `00310508`**. The KO bit is set, and no presentation call runs |
| `single_store_without_a_status_transition` | §4 | 100 − 30 stores once, at `00300749` (70). 480 + 50 against cap 500 stores once (clamped to 500). No status transition, no recompute |
| `bound_holds_after_every_store` | §4 invariant | Every stored value lies in `[0, cap]`: the second store clamps too |

## What the execution adds

1. **The exposure is closed by execution.** The single-store claim fails exactly on the path where the status
   transition reaches the recompute, and the second store sits at the site block 300 predicted (`00310508`, the
   `+0x48 = HP > cap ? clamp : HP` sequence at `003104E8`–`00310508`). The contract's corrected text is now executed,
   not only read.
2. **The setter's presentation calls are flag-gated.** Bits 1, 4 and 7 of its own flags word select them, which makes
   a presentation-free run a legitimate path of the shipped code, not a stub.

## Not covered

- the lethal path's death credit and display (flag bits 1 and 7 clear); these are presentation / reward sinks;
- the revive path's respawn chain (`00386A70` → `00301140` → the spawn keep), which needs spawn records;
- a live game.

## EY-4, EY-1 and the presentation calls executed: `ey.py` (OPUS, 2026-09-26)

`ey.py` loads `check.py` (its three cases run first, unchanged). **No application stub.**
- **Planted:** block 334's units and stats records, plus a source target-buffer entry `{key = target unit +0x10, flags}`.
- **Flags word `0x02`:** bit 1 set, so there is no death credit. Bits 4, 6 and 7 are clear, so the display `0028F1F0` and
  `003283D0` run as shipped.

**7 / 7 pass, and `ey_result.json` is byte-identical over two runs** (md5 `b131fd68a7c2d50803c96879a20440c5`).

| case | item | observed |
|---|---|---|
| `EY4_alive_variant_is_entryFlags_bit8` | EY-4, §9 | the source entry's bit 8 (knockback) clear → **`0x2005`**; set → **`0x2006`** |
| `EY4_dead_variant_inverted_2008_2007` | EY-4, §9 | lethal: bit 8 clear → **`0x2008`**; set → **`0x2007`**. This is the inversion §9 records (`neg` / `sbb` / `add 0x2008`) |
| `EY4_no_entry_is_variant_0` | §9 | with no entry for the target (`00316D70` returns −1), the events are `0x2005` / `0x2008` |
| `flag_bit8_death_posts_200E` | §9 | the call's flags bit 8 on a lethal hit → `0x200E` (`00300846`) |
| `EY1_bubble_doubles_the_cap` | EY-1 | a heal of 480 + 400 with max 500 stores **500** without Bubble, and **880** with status bit 28. 480 + 900 with Bubble stores **1000** (2 × 500) |
| `presentation_calls_run_as_shipped` | §4 | the display `0028F1F0` and `003283D0` are entered and return |
| `no_fault` | — | every run returns |

**Still not covered:**
- the death credit `00469BB0` (flags bit 1 clear). It reads `+0x68` of an object this world does not build;
- the revive path's respawn chain.
