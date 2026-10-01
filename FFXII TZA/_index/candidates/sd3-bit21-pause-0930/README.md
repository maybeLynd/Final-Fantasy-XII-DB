# SD-3 answered: capability-policy bit 21 decides whether the pause menu is refused, deferred or opened at once (OPUS, 2026-09-30)

Register row SD-3 asks what aggregate capability-policy bit 21 changes when it is set. It sits on
[capability-inhibition-policy.md](../../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md), §7.

**Where it stood.** The earlier record [`sd3-policy-bit21-0930`](../sd3-policy-bit21-0930/README.md) (`1113232aa`)
read both consumers of the bit:

- **audio:** the full-screen audio hold is skipped;
- **input:** the arbiter's modal is opened in its flag-0 variant.

It left open what that modal does with flag 0 against flag 1.

This record is static, from the certified image. The checker is `sd3_pause.py` (output `sd3_pause.out`, `FAILS 0`).
It uses the kit resolver `regval.py` for the argument values.

## The answer (OPUS)

**P1: the modal is the pause menu.** `002282F0` builds a `0xD0`-byte widget through the factory `00244F50`, with
handler `00229590`, and keeps it at `01FD4940`. The handler logs `"PauseMenu Create"` in its construct arm and
`"PauseMenu Open"` when it opens, through the debug print `0017DB70`.

**P2–P4: what the flag does.** The construct arm keeps the flag at `+0xC8`.

- **Flag 1: immediate.** The menu posts overlay request `{3, text, 0x64}` through `002CCD40` and enters state 1. When
  `002CCC70(3)` reports the request ready, it logs the open and holds audio groups 0–5 (`002DF370(0x3F, 1, 1)`,
  unless `00226BD0(0xF)` answers non-zero). It then enters state 2.
- **Flag 0: deferred.** The menu is built in state 0 with nothing posted. Each tick it waits for the global `01FD4954`.
  When that is set, it clears it, posts the same request, sets the flag, and continues as above.

**P5: what bit 21 does to the pause.** The input arbiter reaches the pause menu through `00228380` (one caller,
`00253C70`):

| aggregate bit 21 | row 1 bit 21 | result |
|---|---|---|
| clear | – | **the pause opens at once** (flag 1) |
| set | set | **the pause is deferred** (flag 0): the menu waits for `01FD4954` |
| set | clear (the bit comes from another row) | **the pause is refused**: `00228380` returns 0 and builds nothing |

**P6: what ends a deferral.** `01FD4954` is written only by the menu itself and by the one-line setter `00229AE0`. The
setter's callers are:

- the movie player's bring-up `001B7690` and `001B7F30`, which store 1;
- `002CEB40`, which stores 1;
- `001B82A0`, which stores 0;
- `001B8400`, which stores its own argument.

**So, in player terms:** while row 1 holds bit 21, a pause press is remembered but not shown until one of those events
fires. While only another row holds it, a pause press does nothing. Audio is held only when the menu actually opens, and
the full-screen audio hold (the earlier record's A1–A2) is also skipped while the bit is set.

## A correction: bit 21 has more writers than the Save/Load handlers (OPUS)

The page (§7, and its row-1 census) and the SD-3 row say that bit 21 is set and cleared **only** by the Save/Load
controller's handlers. **W1** resolves the row and bit at every one of the 77 call sites of the set primitive
`002E1C20` (38) and the clear primitive `002E1CA0` (39):

| writer | row | operations |
|---|---|---|
| Save/Load: `005823B0`, `00582860` (the page's four sites) | 1 | set, clear |
| the movie player's bring-up `001B7690`, `001B7F30`, and `001B8400` | 1 | clear |
| `001B82A0` (the same movie family) | 1 | set |
| the spawn-verb body `0023FBE0` | 1 | set, clear |
| `002CEB40` | 1 | set, clear |
| the title-asset consumer `003939B0` (the `0x1D0` object) | 1 | set, clear |
| the title-asset singleton's handler `00394070` (the `0xD8` object) | **0** | set, clear |
| the restore loop `00229510`: rows 2 and 8, bits 0–21, cleared and then re-set from a saved mask | 2, 8 | restore |

So the page's "only the Save/Load handlers" is an absence claim this census refutes. The consequences:

- **The title screen's row-0 bit makes a pause refused, not deferred** (P5, last row), because row 0 is not row 1.
- **The movie family** clears row 1 at bring-up and sets it at `001B82A0`.

**Consumer check.** Every document that mentions bit 21 alongside Save/Load was read:

- `CONTRACT-input-subsystem.md` §11 says the two consumers read "row 1 bit 21" and makes no writer claim.
- `the-title-asset-singleton-and-its-distinct-consumer.md` already records the title objects' channel-1 set and channel-0
  clear, which agrees with W1.
- The claim "only the Save/Load handlers" appears only on the policy page (§7 SD-3, and §9's "own row 1 bit 21") and
  in the earlier record `sd3-policy-bit21-0930`. All three are corrected in place, with this record's W1 as the
  rejecting check.

## Limits (OPUS)

- **What event 4 of `ScreenStateFullScreen` is** (the audio half's trigger) is not read here. A search of the Phyre
  framework range for a slot-5 dispatch that passes 4 found none. The trigger identity stays a limit. The effect of the
  bit on that path is read.
- **Roles are not identified for `002CEB40`, `001B82A0`, `001B8400` and `0023FBE0`.** Only their stores are read: which
  spawn verb `0023FBE0` is, and when in a movie's life `001B82A0` and `001B8400` run.
- **Static only.** Whether a player can press pause during Save/Load or a movie, and what they then see, needs no
  runtime to state the rule, but it was not observed.
