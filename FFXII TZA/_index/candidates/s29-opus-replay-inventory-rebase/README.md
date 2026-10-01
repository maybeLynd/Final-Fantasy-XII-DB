# Regression: EXP-189's corrected ranges and their structural consequence (OPUS, 2026-09-25, repair 4)

**Source.** SWE2-ORACLE's EXP-189 correction: `0030B6A0` zeroes 512 bytes at `+0x57C8` and masks 128 bytes with `0xF8` at
`+0x59C8`. The bounded facts were already in the type store (`BattleSystemState` `+0x57C8` / `+0x59C8`) and in
`CONTRACT-inventory-class-storage.md` line 101. **This package consumes the correction; it does not absorb ORACLE's files and
runs no new campaign.**

## The structural consequence

`0030B6A0`'s **first** loop binds the inventory descriptor table `01EEBCC0` to the same block:
- descriptor `+0x08`, `+0x20` and `+0x30` become block + the descriptor's own dword offsets;
- `+0x40` becomes the running sum of the counts.

Two of those offsets land on the corrected rows:

| region | descriptor | bound at | count | what the store said | now |
|---|---|---|---:|---|---|
| `+0x57C0`, 8 B | 0 (class 5, items), `+0x28` → `+0x30` | `0030B6E6`–`0030B6ED` | `0x40` | "no censused access; semantics open" | reached **through the descriptor pointer**, which displacement censuses cannot see. One bit per id fits, but that is inference and not read. Meaning not claimed |
| `+0x57C8`, 512 B | 2 (class 7, loot), `+0x18` → `+0x20` | `0030B6D5`–`0030B6DC` | `0x200` | "inventory derived state, wholly recomputable" | one byte per loot id, reached through the descriptor. **Only "zeroed at load" is established**; "wholly recomputable" is superseded wording |
| `+0x59C8`, 128 B | none of the fifteen descriptors points here | — | — | masked, bits 3–7 persist | unchanged (the battle-state field map ties it to the bazaar flags) |

**Checked, not changed.** The battle-state field map's *"Class 5 also names `+0x57C0` and class 7 `+0x57C8`"* is **correct
under that page's own numbering**: class = nibble + 5, from `15665baf5`. The contract names the same regions by nibble.
These are two conventions, not a contradiction.

## What was run

`check.py`, with `world.py` / `world.json` / `printf_bridge.py` / `shipped_pack.py` from the lighting regression.
Evidence class NATIVE-REPLAY, `live_game: false`. **No application stub and no stop boundary.** It runs `0030B6A0` over a
`0xA5`-poisoned `0x7410`-byte block.

Result, byte-identical over three runs (md5 `4ae6fa41c31e4e4fa54e737c89579e8a`):
- `+0x57C8..+0x59C7` are zero;
- `+0x59C8..+0x5A47` are `0xA0` (`0xA5 & 0xF8`, so bits 3–7 survive);
- `+0x57C0..+0x57C7`, `+0x57B8..+0x57BF` and `+0x5A48..` stay `0xA5`;
- descriptor 0's `+0x30` = block + `0x57C0`, descriptor 2's `+0x20` = block + `0x57C8`, and descriptor 0's `+0x08` = block +
  `0x4748`.

**What it rejects:**
- a clear wider or narrower than `+0x57C8..+0x59C7`;
- a zeroing, rather than a masking, of `+0x59C8`;
- "no access" for `+0x57C0`.

Review routed to a reviewer other than the author.
