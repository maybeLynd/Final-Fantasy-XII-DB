# The stream object's `+0x20` is a base sub-object (OPUS, 2026-09-27)

**Question.** From [how-a-path-is-resolved-to-bytes.md](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md),
routed to the structural lane: is `+0x20` a nested member or a base sub-object? A standalone 0x30-byte constructor,
`00597930`, writes the same six fields at the same relative offsets.

**Discriminator.** The compiler's own layout record. The RTTI base-class array lists every base class with its
displacement (`mdisp`), including non-polymorphic ones. A member appears nowhere in it.

**Answer: a base.**
- `PStreamReaderFile` (vtable `00D26C90`, installed by `00597970`) lists `PStreamFile` and `PStreamFileWin32` at
  `mdisp` 0x20, non-virtual (`pdisp` −1).
- It lists `PStreamReader` / `PStream` at 0 and `PMemoryBase` at 8.
- `00597930` installs no vtable, so the base is non-polymorphic. That is why no second vtable pointer sits at `+0x20`.

**Control.** `rtti_base.py`:
- R1: the class;
- R2: the bases at 0x20;
- R3: no vtable in `00597930`;
- N: `PStream` has no base at 0x20.

Expected `FAILS 0`.

**Not claimed:**
- which of the two classes `00597930` constructs; they share the displacement;
- what the fields mean.
