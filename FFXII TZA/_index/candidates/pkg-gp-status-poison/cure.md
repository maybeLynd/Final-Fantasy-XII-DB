# PKG-GP-STATUS-POISON Q8: how a cure removes Poison (FABLE, Claude Opus 5.5, 2026-09-29)

[`cure.py`](cure.py) runs R, B, O, D, W and M: FAILS 0 ([output](cure.out)). Static, plus data from the shipped
`battle_pack.bin` (us) and `status_data.bin`.

**The chain, for Antidote or Poisona:**
1. **The candidates (B, O).** The candidate builder `003851F0` takes one of three paths:
   - a random single status, for an action with row `+0x2C` bit 9 (and the first argument's byte `+8` set);
   - Remedy's status-table set, for action `0x62`;
   - otherwise `00384C30`. An action with a non-zero recipe gives its row's authored status mask `+0x18`. With a zero recipe
     (a weapon attack), the weapon's status comes from the equipment table's `+0x20`.
2. **The data (D).** Poisona (`0x03`, recipe 1) and Antidote (`0x5B`, recipe 34) both carry `+0x18 = 0x100`, which is Poison
   alone.
   - **Remedy** cures the statuses whose `status_data` row word `+6` has flag `0x400`: Blind, Poison, Silence and Slow. Three
     evaluation-context bits (`+0x28` bits 4, 5, 6; ids 116–118) add {Stop, Doom, Disease}, {Petrify, Confuse, Oil} and {Sleep,
     Sap, Disable, Immobilize}.
   - Remedy's own row mask `0x8380` names the same base four, but the Remedy path does not read it.
   - The four shipped `status_data.bin` copies are byte-identical.
3. **The removal (R).** The remove slot `0038FC10` keeps a candidate only if the target has it and it is **not held in the
   target's word 2 (`+0x3C`)**. For each one kept, it sets record `+0x5C[i] = 0xFF` and the remove-mask bit `+0x58`. Two
   exceptions:
   - On a target that is KO'd, Stoned, or has status bit 31, the candidates survive only when they also lift one of those.
   - When nothing is removed, two globals are raised.
4. **The apply.** The applier's step 8 clears each remove-mask bit with the status write in mode 0.

**Consequences for a reimplementation (M):**
- An Antidote cures Poison.
- It does not cure a Poison held in word 2.
- It does nothing to a KO'd target.
- Wearing off and being cured are indistinguishable from step 8 onward, because both arrive as remove-mask bits.

**W: a second writer of the remove mask.** The periodic builder's stage 2 ORs the record's `+0x58` at two sites:
- `00386F55`, for expired durations;
- `00386FF3`, for HP Critical (bit 29).

[The result-record field map](../../../07-Combat-Action/Result-Record/the-result-record-field-map.md) named only the remove
slot. Its census seeds are the calculator slots (its §2.3 states the limit), and the builder is not one. The row is qualified
there with the old sentence kept.

affected: `07-Combat-Action/Result-Record/the-result-record-field-map.md` (`+0x058` row: the second writer added)

consumer: the applier page's step 8 reads `+0x58` whatever wrote it, and it agrees.

consumer: the status-write page's stage-2 table ("record `+0x58 |= bit`") agrees; it already stated the builder's write.

consumer: the post-result dispatcher's cured / fades messages read `+0x58` for both writers. That is consistent with "cured"
and "wears off" being separate messages downstream of one mask. Which message a removal gets is not claimed here.

run: cure.py at c545ed760, FAILS 0.

**Not claimed:**
- which context bit is which Remedy Lore license;
- who uses the random single-status path;
- the identity of the builder's first argument beyond its byte `+8`.
