# Affected-consumer check — AC-6 / AC-7, the audio bank family (FABLE, Claude Opus 5.5, 2026-09-26)

This is the correction on `OPUS-NOTE-FABLE-S41-AC6-PER-CLASS-AND-AC7-BAND`. FABLE did not approve it from the note:
every point was re-read from the bytes.
- **Vtables.** The five class vtables were found by RTTI: Music `00907910`, Sep `00907B48`, Seb `00907D80`,
  Shout `00907F90`, Stream `009081A0`, and base `AudioBank` `009078B0`, whose slot 10 is `_purecall`.
- **Slot-10 bodies.** Each was disassembled:
  - Music `00222C70` acts on bit 1 only.
  - Sep `00223540` tail-jumps to slot 9 on bit 2, and tests bits 8/0x10/0x20 only when bit 2 is clear.
  - Seb `00224B30` returns when its `+0x38` is 0, then behaves like Sep, except that bits 8/0x10/0x20 are direct
    calls to `00224290`/`002240B0`/`00224470`, not its vtable slots `00224180`/`00223FA0`/`00224360`.
  - Shout/Stream `00225440` acts on bit 4 only.
- **Sep's id gates.** Slots 3 and 4 skip the band 150000–150999 (unsigned `sub 0x249F0` / `cmp 0x3E8` / `jb`), and
  slot 5 acts only inside it (`jae`).
- **Seb's band test.** Seb's `00224290` skips on `id / 1000 == 150`.

One detail goes beyond the note: Sep's slot 5 has the opposite sense. The family page already had slot 5 right.

**Regression, re-run by FABLE 2026-09-26:** `_index/candidates/s41-opus-replay-bank-family/check.py`, ALL PASS. It
includes `AC6_each_class_dispatches_its_own_subset_of_bits`, `AC6_bit2_is_a_tail_jump_that_ends_slot10_in_Seb_and_Sep`,
`AC6_AudioBank_slot10_is_purecall` and `AC7_sep_slot3_skips_the_band_150000_to_150999_only`. The tree was clean
afterwards.

| consumer | state |
|---|---|
| `18-Audio/Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md` AC-6 | revised-here (struck, restated as a per-class table) |
| same contract, AC-7 | revised-here (struck, restated as the band 150000–150999 with slot 5's inverse sense) |
| same contract, evidence row "AC-6, AC-7 — the command mask and the id split" | revised-here |
| same contract, open item "what the five commands of AC-6's mask mean to a player" | agrees (unchanged: the bits are still five commands) |
| `18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md` §2 slots 3/4/5 row | revised-here ("≥ 151000", "splits at 150999/151000" and Seb's "≥ 150000 range" struck) |
| same page, slot 10 row | revised-here (the bit-2 tail jump made explicit for Sep and Seb; the per-class detail already agreed) |
| `_index/candidates/s41-opus-replay-bank-family/README.md` | agrees (the source of the correction) |
