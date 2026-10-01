# SQ-1: the SeSep `dword0` consumer named on the page is UI code, and no reader is found (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md, SQ-1 (register row)

**The changed assumption.** The SQ-1 page said `dword0` of a `SeSep` payload is live, because `00213140` pushes
the record's `+0x40`..`+0x4c` block into a child engine object through `vft[+0x100]`. That was a join on offsets.
[`sq1_dword0.py`](sq1_dword0.py) ([output](sq1_dword0.out)) was verified at 69a61a006, FAILS 0:

- **A1.** `00213140` has one qword reference in the image, `00906DD0`. That is slot 1 of `DynGeoFontTextInstance`'s
  vtable `00906DC8`.
  - The vtable is installed only by the constructor `002130E0` (and by `00213110`), and the constructor's only
    caller is `001E91F3`.
  - The four dwords at `+0x40`..`+0x4c` come from the setter `00213520`, called only at `001E924E` with
    `[r14 + 0x13A0]`.
  - **A1b.** `DynGeoTextureInstance`'s slot 1, `001FB8E0`, makes the same `vft[+0x100]` call on its argument.
- **A2.** The bank object the binder writes holds a packed `{u32 +0x40, u8 +0x44, u32 +0x45, u8 +0x49}` block.
  `00213140` reads four aligned dwords, which is a different shape. The `SepAudioBank` fill `002190B0` copies
  `+0x30`..`+0x3c` as dwords, so the page's "string pointers at `+0x30`/`+0x38`" are not pointers.
- **A3.** The dword at `+0x45` has exactly 8 accesses in the image: the binder's store `00222E53`, and 7 in the bank
  copy/fill/insert family.
- **A4.** In `00210000`-`00224000`, the 10 non-stack 32-bit reads of `[reg + 0x40]` are `00213140`'s (A1) and 9
  element copies. Each copy is stored back within two instructions: 4 in `SepAudioBank` code and 5 in
  `ShoutAudioBank` code (`00907F90`).
- **A5.** No `SepAudioBank` slot (0-10) reads `+0x40` or takes its address.
- **C1 (control).** The sweeps find the binder's own stores and `00213140`'s read at `0021318A`.
- **C2 (control).** The raw scan finds the known slot-10 entry `00223540` at `00907B98`.
- **P (population).** 369 such reads exist image-wide. The **359** outside the audio region are not classified. The
  result is "no reader in the bank code", not "no reader anywhere".

The page's other cite, `007EFC40`, is the `+0x100` slot of the SEAD `Lay` sound vtables (`DynamicSound`,
`PointSound`, `AmbientSound`, `DirectionSound`). Nothing connects it to `00213140`'s call.

**Regression.** Rerun `sq1_dword0.py`. A1 fails if `00213140` gains a second reference, and A3/A4 fail if a
non-copy read appears in the region.
