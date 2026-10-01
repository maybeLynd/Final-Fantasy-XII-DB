# SD-61: what a `Phyre::PAnnotation` carries, and what it annotates (OPUS, 2026-09-30)

Register row SD-61 was registered by SWE2-DATA (`how-a-class-registers-its-array-members-and-annotations.md` §7). It asks
what `+0x18`, `+0x20` and `+0x28` of an annotation carry. The constructor `006B66C0` stores its `rdx`, `r8` and `r9d`
there~~, and none of its 70 call sites forms them within 12 instructions~~. *Corrected 2026-09-30 (OPUS, on
SWE2-AUDIT-SEM `e89b4567b`, `auditsem-review-dd-owner-read-2-0930/` A3, A4): that was the register row's premise,
restated here as fact, and it is false. All 70 sites form `rdx`, `r8` and `r9` within 12 instructions (the first at
`005B4FDD`-`005B4FE3`). The `+0x18` reader was also named before this record: `006B67F0` finds an annotation by
comparing its `+0x18` with a key (BL-5). The findings below do not rest on the premise.* This record is static. The checker is
`sd61_pannotation.py` (output `sd61_pannotation.out`, `FAILS 0`). It traces each call site's arguments over up to 80
instructions, using `Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**An annotation is a key, a value type and a value, linked into the list of the class member it annotates.**

| field | carries | evidence |
|---|---|---|
| `+0x00` | vtable `PAnnotation` (`00D80930`), replaced by the derived `PAnnotationWithValue<unsigned int>` (`00D32D50`) | F1, F2 |
| `+0x08` / `+0x10` | a list node, self-linked at construction; `006B67D0` links it into a member's annotation list | F1, F4 |
| `+0x18` | the **key**: a static `{name, 0}` object. At 69 sites it is `02CF8570`, named **`"WriteMask"`** (`001641C0` → `006B66F0`, string `00D56508`) | F2, F3 |
| `+0x20` | the **value's type record**: `01F2E5A0`, whose vtable is `PTypeDefault<unsigned int>` (`00630180` returns it; `006315B0` installs the vtable at `00631683`) | F2, F3 |
| `+0x28` | 0 at every site (`xor r9d, r9d`) | F2 |
| `+0x30` | the **value** (the derived class's field): `0x7FFFFFFF` at the 69 sites | F2 |

- **What it annotates (F2, F4).** At all 69 sites, the annotation follows a member registration through `00632960`
  named **`m_count`**, typed `unsigned int`. It is linked into that member's list, which sits at member `+0x38`: in
  `005B4E00` the member is `02CB3C60` and the list head is `02CB3C98`. So 69 classes attach a `WriteMask = 0x7FFFFFFF`
  annotation to their `m_count` member.
- **The 70th site.** It is `006315B0`, the generic `PAnnotationWithValue<unsigned int>` helper. It passes its own
  caller's key and uses the same value type.
- **Reading (an interpretation, not claimed):** a write mask of `0x7FFFFFFF` on a count keeps the count's top bit
  out of what is written. That fits a container whose top count bit is a flag.

## Limits (OPUS)

- **The classes.** The 69 classes are not named here. Nor is what reads `WriteMask` and applies it.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
