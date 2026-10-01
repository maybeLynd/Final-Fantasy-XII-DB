# S-03: the mode word's setters, reset, getters and save round trip executed (OPUS, 2026-09-26)

**Evidence class: NATIVE-REPLAY** (unicorn), `live_game: false`. Independent review is requested from SWE2-AUDIT-SEM
(author OPUS).

**Why.** S-03's runtime cell is MIXED.
- **EXP-098** ran the ladder composition `0030D9A0` → `00377C20` → `003148F0` with **zero scripted boundaries**
  (invariants 1–3).
- **Left open.** The contract itself names what stayed unexecuted: "the four setters, the save round trip, the 21
  consumers".
- **This block** runs the setters, the reset, the getters and the save pair.

**What runs.**
- **The world** is block 348's: `probe.py`, with `world.py`, `world.json`, `printf_bridge.py` and `shipped_pack.py`.
  `battle_pack` is bound by shipped code, which also builds the battle state block `[02EBF190]`.
- **No application stub.**
- **Stop boundary** (recorded): `0035C620`, where the bit-0 setter tail-jumps after its write. It reads `+0x28` of a
  null object here.

| case | asserted |
|---|---|
| L | the ladder over all 16 low-nibble values, with bits 4–31 set and clear: 3 → 5, 2 → 4, 1 → 2, 0 → 1, else 0 (invariants 1/2) |
| P | the bit-3 and bit-2 setters: one write that sets or clears exactly the bit; unrelated bits survive; no write when equal |
| Z | the bit-0 setter: the same one write, then **a tail jump to `0035C620` with `edx` = the new flags word**; nothing when equal |
| C | the chocobo setter. **Enable:** flags `\|= 2`, `+0x5AE0 \|= 0xC`, `+0x5AE4 = 180.0f`, and no other byte of `+0x5AD0..+0x5B0F`. **Disable:** flags `&= ~2`, `002E73C0(slot-3 actor, 3)`, `+0x5AEC = 0`. No write when equal |
| R | the reset `0030DA10` zeroes `+0x5B04` and `+0x5B08` |
| G | the four bit getters return each bit. `003072C0` / `00307280` / `00303EC0` return `ladder() == 4` / `== 5` / `== 2` for all 16 values |
| S | **capture** `002EF3C0`: state `+0x5AE0..+0x5AEF` → rec `+0x08`, state `+0x5AD0..+0x5ADF` → rec `+0x18`, flags → rec `+0x28`. **Restore** `002EF410`: `+0x5AE0` half and flags always; the `+0x5AD0` half only when rec `+0x18` bit 1 is set |

**Runs.** 10/10, and two runs give an identical `result.json` (md5 `309f0a150a404ca900e914d5adc17cf0`).

**Two corrections to the contract** (it is OPUS's own, and it is corrected in the same commit):
- §3 stated `state+0x5AD0..+0x5AEF` at `rec+0x08..+0x27`. The two halves are in the opposite order, and the
  restore's second half is conditional.
- §7 called only bits 2 and 3 plain. The bit-0 setter also tail-calls `0035C620`.

## The disable arm, modes 4 / 5 and the pre-emption executed (OPUS, 2026-09-26)

These three scripts each import `check.py`, whose ten cases run first and unchanged (`result.json` keeps md5 `309f0a15…`).
None uses an application stub. The call graph has no tail-jump edges, so the shipped targets reached by `jmp` join the
allowed set: `00263750`, `002EB030`, `0026BD40` and `00377C20`.

| script | cases | md5 (identical ×2) | what it executes |
|---|---|---|---|
| `c7.py` | 4 / 4 | `c958f73d…` | **§7's disable arm**: slot 3 filled (planted) + `+0x5AE0` bit 1 → `002E73C0(actor3, 3)`, `00329A10` → `002EB030(actor3, 0x2001)`, bit 1 cleared, other bits kept, `+0x5AEC = 0`. Slot 3 empty → no post, bit 1 still cleared. Bit 1 clear → nothing. The test uses the value read before the roster calls; the toggle XORs the current word (a disclosed perturbation shows both) |
| `m45.py` | 3 / 3 | `749fe4ed…` | **§6's modes 4 / 5**: `003266C0` under ladder 4 rewrites `+0x5A5A` / `+0x5A6C` / `+0x5A90` to the leader alone (at the leader's position); under ladder 5 the first two identically and `+0x5A90` restored to its prior content; `+0x5A7E` = the base nine in both. **The runs differ in `+0x5A90` only.** Ladders 0 / 1 / 2 are reported |
| `consumers.py` | 3 / 3 | `d4689789…` | **invariant 1's pre-emption** on `0023B040`: ladder 2 → `00303EC0` = 1, the leader path (`003272A0` onward) is skipped; ladders 4 and 5 with the chocobo bit still set → `00303EC0` = 0 and the leader path runs. *This world has no leader, so the emitted values coincide; the cases show the path* |

**Not covered:**
- `0035C620` itself (the bit-0 setter's tail target; the contract states only the call);
- the other consumers' bodies beyond `0023B040` and `003266C0` (`00313DB0`'s inline `== 2` at `00313E57` is a census
  fact: it is reached only after a party unit is found);
- invariant 4 (a caller census fact: the script-set modes' accessors are reached only through jump thunks);
- a live game.
