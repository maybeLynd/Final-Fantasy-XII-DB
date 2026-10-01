# Type references spelled with MSVC's class-key code (OPUS, 2026-09-27)

**Question.** [EVIDENCE-STANDARD.md](../../EVIDENCE-STANDARD.md) §13h found one type spelled two ways, for example
`VPString` beside `PString` and `UD3D11_…` beside `D3D11_…`. It routed the question to the type store's owner rather
than strip a letter on a name-shape argument. The hypothesis it could not test was MSVC decoration residue.

**Discriminator: the image itself.** In an MSVC decorated name, a class-type template argument is written
`V<Name>@` and a struct `U<Name>@`. The letter is the class key, not part of the name, for example
`.?AV?$PClassDataMemberPhyreArray@VPString@Phyre@@@Phyre@@`. For each prefixed reference in the store, the test is
that the prefixed spelling occurs only inside decorated names (`[?@$]<ref>@`), never as a bare token, and that the
name without the letter is a declared type.

**Result.** Four references on 41 rows pass that test:

| reference | declared type | decorated occurrences | bare occurrences |
|---|---|---:|---:|
| `VPString` | `PString` | 15 | 0 |
| `VPMatrix4` | `PMatrix4` | 7 | 0 |
| `VPMatrix4x3` | `PMatrix4x3` | 3 | 0 |
| `UD3D11_DEPTH_STENCILOP_DESC` | `D3D11_DEPTH_STENCILOP_DESC` | 2 | 0 |

The 41 rows now reference the declared types. Each row's evidence keeps the old spelling and the proof.
`UNRESOLVED` (a placeholder) and legitimate U/V names such as `Vu1RegisterBank02064B00` are untouched. The `UCD3D11_…`
cases the section cited no longer appear in the store.

**Control.** `dedecorate.py`:
- D: the discriminator, per reference;
- R: the regression — no row spells a declared type with a class-key prefix. It fails on the store before the fix.
- P: the decorated contexts exist, and every corrected row carries the record;
- N: legitimate names are left alone.

Expected `FAILS 0` after the fix. `--apply` performs the correction.
