# S-24 D-6: one authored bit gates a base term and its matching equipment term together, executed (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY** (unicorn), `live_game: false`. Independent review is requested from SWE2-AUDIT-SEM
(author OPUS).

**Why.** S-24's runtime cell is MIXED with one named remainder, D-6. Block 342 executed D-1..D-5 and D-7 stub-free,
but its sweep "ran every definition of the two areas, and no case isolates the bit", and every equipment word was
`0xFFFF`. This block isolates the bit.

**D-6** (`CONTRACT-stat-derivation.md`): bits 0 and 1 of the definition's `+0x15` select whether parry/attack and
block/magick evade come from the `.ard` row's own bytes or from the weapon/shield, **and** suppress the matching
equipment contribution.

## What runs

This is block 342's world (`probe.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` copied
from `s24-opus-replay-stat-derivation/`):
- `battle_pack` bound by shipped code;
- `rsn_b.ard` (sha256 `41ac8746…`) bound by the game's own binder `003EA710`;
- `002FEF30` run on the foe path with every callee real.

There is **no application stub and no stop boundary**.

**Fixtures:**
- **Definition 0 of `rsn_b`, which ships `+0x15 = 3`** (both bits set). Its bits are set per case in the bound copy
  and restored.
- **A real weapon and a real shield.** The shipped item table (557 rows) was classified by the game's own
  `0031E9A0`: 311 weapons, 33 shields, 168 armour. The first weapon with small `+0x1A`/`+0x1D` is `1001` (14, 5), and
  the first such shield is `10D4` (`+0x18` 25, `+0x19` 10). Each is equipped in the foe record's first equipment word.
- **Level span** 50, or 2 for the growth case.
- **The row addresses** (definition `r13` at `002FF325`, base `rbp` and growth `rbx` at `002FF32F`/`002FF388`) are
  captured by code hooks, not computed.

**Output bytes**, found by differential: `+0x2E` attack, `+0x32` parry, `+0x33` block, `+0x34` magick evade.

| case | asserted |
|---|---|
| W | bit 0 clear: the weapon adds exactly row `+0x1A` to attack and `+0x1D` to parry. Bit 0 set: it adds nothing to either |
| S | bit 1 clear: the shield adds exactly row `+0x18` to block and `+0x19` to magick evade. Bit 1 set: nothing to either |
| X | each bit leaves the other kind alone. With bit 1 set the weapon still adds; with bit 0 set the shield still adds |
| C | +1 on the base row's `+0x2D`/`+0x2E`/`+0x02`/`+0x03` moves attack/parry/block/magick evade by +1 each with the bits set, and by 0 with them clear. +1 on the growth row's `+0x2E` moves parry by the span (2) |

**Runs.** 7/7 pass, and two runs give an identical `result.json` (md5 `7fa1036fdf767d0b331cb2a09a6c9d25`).

**Static cross-check.**
- `002FEF56` / `002FF0B2` arm the two contribution flags `[rsp+0x4C]` / `[rsp+0x70]` to 1.
- The bit-0 block `002FF32A`-`002FF373` adds `base[+0x2D] + growth[+0x2D]·span` to attack and the `+0x2E` terms to
  parry, and clears `[rsp+0x4C]`.
- The bit-1 block `002FF378`-`002FF3C8` does the same with `+0x02`/`+0x03`, and clears `[rsp+0x70]`.
- The equipment loop adds a weapon's terms only while `[rsp+0x4C]` is set (`002FF48E`), and a shield's only while
  `[rsp+0x70]` is set (`002FF477`).

**Not covered:**
- the downstream bytes `+0x35`/`+0x36`, which also move and are not asserted;
- equipment sub-record contributions through `+0x28`, which are not part of D-6;
- a live game.
