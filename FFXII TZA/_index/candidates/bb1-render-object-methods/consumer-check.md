# Affected-consumer check: FABLE's own seven render-object statements corrected with BB-1 (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Character-Rendering/character-render-object.md (§1, the §4 layout block, BB-2's §2 paragraph, the §5 call chain), 17-Presentation-Rendering/CONTRACT-character-render-object.md (R-4)

run: bb1_methods.py at bbd3af82a (worktree = that HEAD plus this package), 4 checks, FAILS 0. Each correction below was
also re-read by hand at the cited instruction.

**The change.** Seven statements in text FABLE wrote or imported are contradicted by the bytes. They are struck, or
annotated inside code blocks, with a dated note:

| # | statement | the bytes |
|---|---|---|
| 5 | §4 layout: `+0x2C8 .. +0x2E0` slot 24, `+0x2E8 .. +0x310` slot 30 | offsets inside each `0x318` record (`record = [+0x58] + i*0x318`, `001FA262`, `001FA8C2`), not fields of the object |
| 6 | §4 layout: `+0x4AC int` | a float: `1.0f` from the constructor's qword store (`001F4EBE`), compared with 0.9 by slot 16 (`001FA5A4`) |
| 8 | §1: "the material overrides that tint a body when a status lands" | slot 24 writes the four refraction parameters (handles `refractionEnabled` / `refractionPower` / `refractionAlpha` / `RefractionSampler`, bound by `001F7790`) |
| 9 | §5 call chain: slot 26 "guarded on `+0x4B4`" | slot 26 `001FAA10` never reads `+0x4B4` |
| 10 | contract R-4: slot 24 "gates at entry" | with `edx` non-zero it stores 1 to byte `+0x230` of a fetched singleton (`001FA1C2`) before its latch test (`001FA1C9`), the same shape R-4 records for `001F89E0` |
| 11 | contract R-4: "the record's `+0x10` bit 0 (`001FA5DE`)" | `+0x10` of the object the record holds at `+0x00` (`001FA5DA`) |
| 14 | BB-2 §2: "`param+0xD0` is the light count" | a light index: `(x + 1) <= 6` at `001F9F08`, stored into the material's `sunIndex` parameter at `001F9F15`, a handle `001F7790` binds |

| consumer | what it says | state |
|---|---|---|
| the render-object page, the five places above | the struck statements | revised-here |
| the render-object contract R-4 | items 10, 11 | revised-here |
| `_types/fields.tsv` `CharacterRenderObject 0x4AC` | `f32`, init `1.0f`, read `movss` at `001FA5A4` | agrees |
| `_types/fields.tsv` `CharacterRenderObject 0x3BC` (the `+0x3B0` out-param reading) | not one of these seven; item 7 of the findings | routed-to-FRONTIER with the other peer items: `FABLE-REQ-FRONTIER-BB1-SLOT-TABLE-CORRECTIONS` |
| the §3 slot table rows for slots 1, 6, 9 and 11 (NOCALLER-INSTALLERS) | items 1 to 4 | routed-to-FRONTIER in the same request |
| `CONTRACT-render-command-list-and-graphics-handshake.md`, `the-ordered-render-command-list.md` | cite `00215320` -> `001F5D70` | agrees (the same route BB-1 states) |

Grep of "light count", "tint a body", "status lands", `+0x4AC`, `+0x2C8`, `+0x2E8` and the R-4 lines across the
database, 2026-09-27. Inbox and audit-log mentions are receipts and are not edited.
