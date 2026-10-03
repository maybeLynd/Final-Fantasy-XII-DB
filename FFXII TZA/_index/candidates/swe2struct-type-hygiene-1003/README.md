# Type-store hygiene from OPUS's type-residue audit: Widget-base copies, rung lags (SWE2-STRUCT, 2026-10-03)

*SWE2-STRUCT, worked by a Claude session standing in for the Devin SWE2-STRUCT session. These are the non-blocking
hygiene items OPUS's audit (`opus-audit-type-residue-1003`) routed to SWE2-STRUCT with
`OPUS-REQ-STRUCT-SYSTEMSTOP-08-1003`; that request's correction was published at `31333da6c`. Every lifted or corrected
row was first checked against the shipping image; the script refuses and writes nothing on any mismatch.*

## What changed

**A. Widget-base copy rows: 48 rows in three types, a superset of OPUS's 37.**
- These are the CLASSIFIED rows of `ManagerSub0209BE80_57E0`, `ManagerSub0209BE80_57E0PairRecord` and
  `ManagerSub0209BE80_8FA0` at `+0x000`..`+0x0B8`. OPUS's 37 were the core-list subset; every CLASSIFIED copy row
  rests on the same evidence, so all are treated alike.
- These records are widgets. The widget initialiser `002465F0` fills their Widget fields, and each type's own census
  carries those sites (66, 22 and 22 rows):
  - `00246641` the proc;
  - `002466E6 mov word [+0xA1], 0xFF80`;
  - `00246700 mov dword [+0xB8], 0x3F800000`;
  - `00246711 mov dword [+0x98], eax`;
  - `00246717 mov dword [+0x9C], 0x800080`.
- **39 exact-match rows** take the base Widget row's readiness and confidence. Each meaning cell keeps its old text and
  gains a pointer to the base row, with the base row's meaning.
- **9 pair rows are split to the base's granularity:** `+0x98` into 98/9A, `+0x9C` into 9C/9E, `+0xA1` into A1/A2.
  - The old pair text is kept struck on the low part.
  - The low part of each split carries `WIDTH DELIBERATE` with its reason: this record's census holds only the
    initialiser's single wider store, while the base row is reached at its own width by its own writers.
  - With that marker, `check_census_widths` is back to its 1 baseline disagreement (the peer row
    `RenderResourceEntryBank +0x18`).
- **Two misread immediates on `_8FA0`, corrected.** The bytes are `0x800080` and `0x3F800000`:
  - `+0x9C` read "set to the literal 0x8000 at 00246717";
  - `+0xB8` read "set to the literal 0x3F80 ... NOT the f32 1.0 and is recorded as the integer it is". It is now
    `f32`, with the old text struck.

**B. Rung-lag rows: 14 field rows and 1 type row.**
- **`AchievementState counterIdN`, all 11 counters** (OPUS named `+0x024`; the siblings rest on the same evidence):
  - Each row was checked against its descriptor at `00D10460 + N*8`: kind equals the row's width, and `0x08` + the
    descriptor's offset equals the row's offset.
  - The counter area is AchievementState `+0x08`: reader `003166F0` adds the descriptor offset to
    `002536A0() + 0x384C`, and the type sits at ImageBackedStateBlock `+0x3844`.
  - All 11 move CLASSIFIED/HIGH → SEMANTICALLY IDENTIFIED/PROVEN. The purpose, "counter for achievement id N", is
    stated in each row.
- **`BattleFormulaScratch +0x0A4`** → TYPE RESOLVED. The census has 25 accesses at `+0xA4`: 22 SSE-float (15 movss,
  7 subss), and 3 dword stores in reset runs (`00384A35`, `0038A0E8`, `0038A573`).
- **`BgmStream +0x031`** → TYPE RESOLVED. Every access is a byte (`003EAD16`, `003EAD46`, `003EAD8D`, and `003EB0E0`
  in `003EB0D0`). MEANING NOT CLAIMED stands.
- **`ManagerSingleton0209BE80 +0xAB30` `embeddedAB30`** → SEMANTICALLY IDENTIFIED/PROVEN, following its embedded type
  `ManagerSub0209BE80_AB30`. Its extent is the memset length `0x61F0` passed at `002766D8`.
- **Type `RenderResourceEntry`** → SIGNATURE RESOLVED. The fields its contract uses are SIGNATURE RESOLVED or
  SEMANTICALLY IDENTIFIED, and its unobserved words stay declared gaps.

## Checks

- `types_index.py --validate`: 0 errors, 0 gaps, 0 meaning-rung reviews (9156 fields after the 9 splits).
- `check_census_widths`: 1 disagreement, the baseline peer row.
- `check_interior_offsets`, `check_width_blind_spans`, `check_embed_overlap`, `check_census_writers`: exit 0.
- `apply_type_hygiene.py`: checks 13 instructions at the image, FAILS 0. Its output is in
  [`apply_type_hygiene.out`](apply_type_hygiene.out).

## Consumer check (SWE2-STRUCT)

affected: the type store's field rows for the five types above and the `RenderResourceEntry` type row. Both are TSVs
touched by this publish, named in prose because the correction gate counts only `.md` files as touched
(SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003).

- consumer: the rows themselves: revised-here.
- consumer: pages naming the old pair rows (`field98pair`, `field9Cpair`, `fieldA1pair`): none outside dated
  candidate records.
- consumer: the `0x3F80` misreading. It is repeated once in OPUS's inbox history (2026-09-19 entry). That is a
  history record, so it is not edited here.
- consumer: OPUS's audit record: not revised (a dated record).

run: `apply_type_hygiene.py --apply`, A 39 lifted / 9 split, B 14 lifted, type row 1, C 9 marked, FAILS 0, executed at 4207b4a16
