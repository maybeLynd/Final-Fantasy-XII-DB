# UQ-38: the row's proposed criterion is tested and retired - this translator carries values across bank stores (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (UQ-38):** of the 267 register-bank members, how many are whole translated routines and how many are C
routines with translated fragments.

The 2026-09-17 narrowing proposed the discriminator:
> whether x64 registers carry values ACROSS bank stores (C keeps locals in registers; a translation reloads every
> operand from the bank).

**Result: that criterion cannot decide the split, because its premise fails.**

## Measured (`uq38_carry.py`, output `uq38_carry.out`, per-member table `uq38_carry.tsv`)

For each member, the script computes the fraction of xmm register reads whose value was defined **before** the most
recent bank store in the same basic block. It is calibrated on the two sets both earlier instruments agree on:

| set | n | median | p25–p75 |
|---|---:|---:|---|
| whole (both call it a whole translation) | 47 | **0.535** | 0.390–0.667 |
| C-agreed (both call it C with fragments) | 31 | **0.333** | 0.192–0.425 |
| undecided | 104 | 0.436 | 0.378–0.511 |

- The criterion predicts that whole translations sit near **0** (every operand reloaded) and C sits high.
- The measurement runs **the other way**, and the three distributions overlap.
- So no threshold on this ratio separates the sets.

## Why (`uq38_example.py`, output `uq38_example.out`, FAILS 0)

**E1.** In `003CD840` (21,276 B, the largest member both instruments call whole):

```
003CD872  psrldq xmm0, 1
003CD877  mov byte ptr [rip + 0x1f0b724], al   ; bank store, 022D8FA1
003CD87D  movd eax, xmm0
```

- The translated code keeps a 128-bit value live in `xmm0` across a store into the bank.
- The translator therefore allocates PS2 values to host registers; it does not reload every operand.
- **E2:** control. The same search over a body with no bank store finds nothing.

## What this leaves

- The split still needs provenance. That means either the PS2 executable (`system.cnf` in the shipped data names
  `SLPM_667.50`; the ELF itself is not shipped) or the translator's own rules.
- OPUS's lost-build review scoped `UQ-36` / `UQ-39` the same way: answerable from the PS2 executable, which is
  outside this database's evidence boundary.
- **The bracket stands:**
  - at least 47 members are whole-shaped;
  - ~~41~~ **31** are settled as C with fragments by both instruments *(corrected 2026-09-28 on OPUS's recount in `../uq38-oeb-signature-opus/`: FRONTIER's 41 include 5 that ee_member_calls calls whole and 5 mostly)*;
  - 95 are undecided.

## Limits

Static. The ratio is per basic block (defs reset at every branch target, call and jump), so cross-block carries are not
counted. That only lowers every set's ratio equally, and it cannot explain the reversed ordering.

## Files

- `uq38_carry.py` / `.out` / `.tsv`.
- `uq38_example.py` / `.out`.
- `consumer-check.md`.

## Addendum 2026-09-27 (FABLE, Claude Opus 5.5): the interface does not show the split either

A whole PS2 routine could reveal itself at its interface in two ways: taking arguments from the bank's `a0`-`a3` images, or
keeping the PS2 frame (`$sp` / `$fp` / `$ra`) in the bank. [`uq38_interface.py`](uq38_interface.py)
([output](uq38_interface.out), run verified at b9022cc9f, FAILS 0) measures both over the same three sets:

| test | whole (47) | C-agreed (31) | undecided (104) |
|---|---:|---:|---:|
| I1 reads an x64 argument register in its entry block | 43 | 30 | 103 |
| I2 touches bank `a0`-`a3` in its entry block | 0 | 0 | 0 |
| I3 touches bank `$sp` / `$fp` / `$ra` anywhere | 0 | 0 | 0 |

- **Controls.** C1: the same address detector finds bank `v0` in 13 members and bank `a0` in 3. C2: the argument
  detector reports no read for `0015BCF0`, which zeroes `ecx` before any use.
- **What this shows.** The translator gives every member, whole or not, an x64 C-ABI entry, and it does not emulate the
  PS2 stack or return address in the bank.
- **So the interface carries no whole-versus-C signal.** Three structural criteria have now failed on the calibrated
  sets: value carry across bank stores, the entry interface, and the PS2 frame registers. Two census signals
  disagree on the 95: access density and outside calls. That strengthens the scope OPUS gave UQ-36/39: the split needs
  provenance (`SLPM_667.50`, not shipped) or the translator's rules. The bracket is unchanged: 47 / ~~41~~ 31 / 95.
