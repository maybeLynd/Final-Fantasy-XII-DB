# BT-2: the render record's +0x3D4 name has no writer, and its one reader never runs (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Question.** BT-2's last narrowing declared `CharacterRenderRecord +0x3D4` a 32-byte name, `lookupName3D4`. It is read
by the by-name attach `0042F6C0` → `004218A0` → `00372760`. That narrowing left "the name's writer" open.

**Discriminator.** Is there a store, or an address formation, that reaches `+0x3D4`–`+0x3F3` on this record? If there
is none, does the reader run at all?

**Negative search, which narrowed the question:**
- No displacement store to `+0x3D4`–`+0x3F3`.
- No `lea` into `+0x3C0`–`+0x3F3` except the reader `0042F7DD`.
- No `0x3D4` immediate.
- No whole-record copy: the only 0x740-sized block operation is ResetDefaults' memset (`0041F754`).
- No memcpy or memset into the pool among the 372 functions that load `[022C6F28]`.
- The five candidates in engine bands (`001F8D10`, `001FA3D0`, `0028D980`, `003F1E90`, `003F2600`) all have fields past
  `+0x740`, or `+0x998` on the same base.

**Result** (`bt2_name3d4.py`, N1–N4):

*N1.* The dirty pass `00427DE0` calls `0042F6C0` only when `+0x290` bit 19 is clear and bit 18 is set
(`00427F94 bt eax, 0x12` → `00427F9D`). That is the only call to `0042F6C0`.

*N2.* `0042F6C0` is the only reader of `+0x3D4`: `0042F7DD`, plus the first-byte test at `0042F7EF`. It clears bit 18.

*N3.* No store sets bit 18. The search covers every store to `+0x290` on a base shaped like this record: 0x740 bytes,
`+0x284` addressed, and `+0x290` never accessed as a float.
- 61 or-immediates, none containing `0x40000`.
- `0042F310` and `0042F3B0` clear bits 18 and 20, then set 19.
- `0042F250` clears bits 18–19, then sets 20.
- `005DEC50` and `007BFFA0` copy the word from another object, so they can only propagate the bit.
- `00184CE0` and `004FD060` are other layouts.

*N4.* Nothing writes `+0x3D4`–`+0x3F3`.

**So:** the name is empty, and the by-name attach is dormant in this build. With an empty name it would match only an
empty bone name, and `0042F6C0` tests for exactly that. The 32 bytes are a dormant path's input, not live state.

**Not claimed:**
- A pointer to `+0x290` or `+0x3D4` formed by arithmetic other than displacement forms.
- rep stos / movs.
- Code outside the image.

**Run receipt:** `bt2_name3d4.py`: PASS N1–N4 over 38,161 functions (61 or-immediates, 7 classified other stores); all
6 mutants rejected; FAILS 0 (2026-09-27, before publish).

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x3D4` | extended: no writer, reader dormant | revised-here |
| `_types/fields.tsv` CharacterRenderRecord `+0x290` | extended: bit 18 is the by-name attach's dirty bit, never set | revised-here |
| `_index/OPEN-QUESTIONS.md` BT-2 | narrowing prepended; answers "the name's writer"; row stays OPEN (other DISCOVERED spans) | revised-here |
