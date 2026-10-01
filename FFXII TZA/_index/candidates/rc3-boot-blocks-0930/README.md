# RC-3: what the two unregistered boot allocations are for (OPUS, 2026-09-30)

Input for `RC-3` ([what the engine fixes at boot](../../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md), the
memory budget). SWE2-CONTRACT registered the row, so it applies this. Static evidence only: the shipping image
`73461d08…` and the database's own published pages. Nothing was executed.

## The 1 MiB block (`01FD4A90`): the per-model oscillator subsystem's shared table

- **The slot has three rip-relative references.** One is the boot store in `0022A0B0` (`0022A2A3`, after `0036D240(0x100000)`). The other two are
  loads in `0040ACF0` (`0040AF65` and `0040AFF2`).
- **Both loads publish the block as the shared table.** Each copies the pointer into `02CA43C0`, then calls the scope
  opener `00415EE0(&local, entry, 1)`.
- **This is already documented.** [The per-model oscillator subsystem](../../../17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md)
  says the `00415EE0` scope-open stores "shared table `01FD4A90` to `02CA43C0`". It runs for modes 0 and 2 of the
  exception-listed dispatch, and on the not-listed path when record `+0x3F` bit 4 is clear. Its register table has
  `02CA43C0` as the "per-frame shared table install", and `members/model-oscillator-subsystem.tsv` row `00415EE0` reads
  "arg 1 opens (02CA43C0 <- 01FD4A90)".
- **The users are the scope family.** `02CA43C0` has 40 rip references: two are `0040ACF0`'s stores, and the rest are
  read-advance-write cursor steps in `00415EE0` (14), `00416270` (8), and `00416450`, `00416600`, `004167C0` and `00416910` (4 each).

So the block is the oscillator stage's shared working table. It is installed per record when the scope opens.

## The 0.5 MiB block (`01FD4A20`): allocated and never read

The block's pointer slot has **one** reference anywhere in the image: its boot store in `0022A0B0` (`0022A284`, after `0036D240(0x80000)`), found
by a rip-relative sweep that counts displacements. No 64-bit or 32-bit absolute copy of `01FD4A20` exists, and no
32-bit RVA copy either.

The same sweeps are the positive control: they find the other slot's three references, listed above. So no code reads
this slot, and nothing in the image reaches the block through it. The allocation is made and its pointer stored, but
the pointer is never used.

## Not claimed

- Why the 0.5 MiB block is allocated. One reading is a leftover of a removed consumer; that is a reading, not a finding.
- That no pointer to the block's contents escapes some other way. The only value that could escape is the one the
  allocator returned, and the boot code only stores it.
- Anything about sizes, which are the boot contract's.
