# PKG-GP-STATUS-POISON Q9: re-inflicting a status the target already has (FABLE, Claude Opus 5.5, 2026-09-29)

[`refresh.py`](refresh.py) runs G, A, I, C, D and M: FAILS 0 ([output](refresh.out)). Static, plus data from `status_data.bin`.

**Answer.**
- **Re-casting Poison on a poisoned target changes nothing.** Its timers keep running, and the cast counts as "no effect".
- **Fourteen statuses do refresh on a re-cast:** Stop, Sleep, Confuse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect,
  Vanish, Regen, Float and Bubble. Their duration and beat restart from the defaults.

**Why (the chain):**
- **G.** For a status the target already has, the candidate resolver continues only when the status row's word `+6` has
  bit 5. Otherwise it skips the status and counts it as "no effect".
- **A.** The add operation `00387BB0` does not test presence. It sets the apply bit and writes the default duration and beat
  into the result record's per-status slots.
- **I.** The record's 32 duration and 32 beat slots start at −1.
- **C.** The applier's copy-through writes every non-negative slot into the target's `+0xBC` / `+0x13C`. It does so after the
  status write, whatever the status write did. For a present status the status write refuses, but the copy-through still
  installs the defaults.
- **D.** Bit 5 is set on exactly the fourteen statuses above. Poison's word is `0xA400`, with bit 5 clear.

The explorer's concern was that the applier copies the timers even when both masks are zero. That is answered by I: untouched
slots are −1, and the copy-through skips them.

affected: `10-Status-Periodic-Terminal/CONTRACT-status-write.md` (invariant 3 and §11)

- Invariant 3's "a refresh is impossible without removing first" was true of the status write alone, and false at the apply
  level for the fourteen statuses. It is struck and scoped, and the mechanism is added.
- §11's "a status refusing to refresh when re-cast" is corrected the same way.

consumer: the status-write page §2.3 ("every case refuses when the bit is already in the requested state") is about the
operation, and it agrees.

consumer: the applier page's step 9 (the copy-through, "non-negative values only") agrees, and is the mechanism.

consumer: a grep for "refresh" across the pages finds no other claim about status refresh. It agrees.

run: refresh.py at 8764d1109, FAILS 0.

**Also found.** The result-record field map says the initialiser fills "the 33 dwords from `+0x5C` and the 33 words from
`+0xDC`". The loop runs 32 times (`edx` = −1 + `0x21`). 33 dwords from `+0x5C` would overlap `+0xDC`. That correction goes
in with Q8's field-map batch, or right after it.

**Not claimed:**
- the second caller of the add operation (`003909F1`) beyond its block-mask gate;
- whether any action reaches the random single-status path with a present status.
