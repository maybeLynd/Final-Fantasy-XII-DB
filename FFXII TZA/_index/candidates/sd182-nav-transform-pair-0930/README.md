# SD-182: the nav shape subrecords' +0x10 / +0x50 transform pair is authored in the map pack (SWE2-ORACLE, 2026-09-30)

Register row SD-182 (SWE2-DATA, DD batch 5, `b92561451`) is on
[the-unit-shape-distance-primitives.md](../../../06-Movement-And-Navigation/the-unit-shape-distance-primitives.md)
section 3. It asks whether a unit shape's `+0x10` / `+0x50` transform pair (forward, inverse) is authored data or
built per query. The shapes the edge scan reaches are the 144-byte subrecords at `q[tab+0x18] + (si − 0x4000)·144`.

Sub-package `SWE2-ORACLE-SD182-184-0930` under OPUS's parent claim `OPUS-SD180-193-0930`. OPUS's static head start
(the `tab` chain up to `002F6AB0` and the YM00 slot) is taken as the starting point and re-checked here (S1–S3).

| file | evidence class | result |
|---|---|---|
| `sd182_nav_transform_pair.py` → `.out` | **static** (S1–S7) and **data** (D1–D4) | `FAILS 0` |
| `sd182-subrecord-pairs.tsv` | data, one row per (map pack, nav chunk) with at least one subrecord | 832 rows |
| `img.py` | the image reader | — |

## The answer (SWE2-ORACLE)

**Authored. The map pack carries both matrices, and `+0x50` is the inverse of `+0x10` in the file bytes. The engine
points at those bytes and never writes them.**

1. **Where `tab` comes from (S1–S3).**
   - `00322220` stores `0026E500(2)` (or the fallback) at `02EC1378`.
   - `0026E500` returns `q[0209A678]` or `q[0209A680]`.
   - `0026E960` fills those with `&obj[0x40]` / `&obj[0xA8]`, the two 0x68-byte nav tables of the object `002F6AB0`
     builds from the map pack's slot-8 **YM00** section.
   - `002F6AB0` walks the YM00 index (chunk = file + 0x10 + off·16). **Tag 0x1F** goes to
     `00232380(obj + 0x40, chunk)` and **tag 0x11** to `00232380(obj + 0xA8, chunk)`.
   - So `tab` is the tag-0x11 table when the map has one, else the tag-0x1F table. `02EC1370` holds the tag-0x1F table.
2. **The loader rebases; it does not build (S4).**
   - `00232380` walks the nav chunk's own index. For sub-chunk type 4 it stores `tab+0x18` = sub-chunk + 0x10 and
     `tab+0x44` = the sub-chunk's first dword, the count.
   - All its stores go to the table or its own stack.
   - So the subrecords are the loaded file's bytes, in place.
3. **Nothing writes into a subrecord (S5–S7).**
   - The 144-byte index (`lea r,[i+i*8]; shl r,4; add r,[tab+0x18]`) is formed in exactly five functions: `0022CC50`,
     `0022D4B0` (D4B0), `0022D7E0`, `0022DE60` and `0022F8B0`. None stores through the resulting pointer.
   - The two shape consumers never store through the shape pointer:
     - FA0 (`00380FA0`) maps both endpoints through `+0x50` and the answer back through `+0x10`.
     - EB0 (`00381EB0`) uses `+0x50`.
4. **The file bytes already hold the inverse (D1–D4).**
   - **The corpus.** Every shipped `.mpk` has a YM00 section (461). Each indexes both nav chunks; 1 tag-0x1F and 29
     tag-0x11 chunks are zero-size, and the loader skips those (`002F6CB5`). Every non-empty chunk has one type-4
     sub-chunk.
   - **The subrecords: 89,330 in all** (60,145 in tag 0x1F, 29,185 in tag 0x11). By the type dword there are 6,013
     spheres, 9,642 cylinders and 73,675 boxes, with no other type value. Both matrices are affine in every one.
   - **The inverse test.** In **89,330 of 89,330**, `|M(+0x10)·M(+0x50) − I|` stays under 64 float32 roundings of the
     product. The worst is 0.9 roundings (1.05e-3 absolute, on translations of tens of units).
   - **The negative control** discriminates: pairing a forward matrix with the inverse of a different record (forward
     matrices differing by more than 0.01) passes the same test in 0 of 89,174 cases.
   - **55 subrecords carry an identity pair.** All are the tag-0x11 table of `alc0101.mpk`, which is its own inverse.

## What changes on the page, for SWE2-DATA (SWE2-ORACLE)

- **Section 3: SD-182 answered.** The pair is authored.
  - The map pack's YM00 nav chunk (tag 0x1F or 0x11), in its type-4 sub-chunk, stores each shape as
    `type, …, forward 4×4 at +0x10, inverse 4×4 at +0x50`. The inverse is exact to float32 rounding.
  - The engine points `tab+0x18` at those bytes, and no code writes them.
  - `00230790`'s shared workbench is a different object, as the row already says.
- **"The shape record" subsection.** It can name its source: the YM00 nav chunk's type-4 sub-chunk, 144 bytes per
  shape, count at the sub-chunk's `+0`.

## Evidence classes, kept separate (SWE2-ORACLE)

- **Static (S1–S7):** decoded instructions and jump tables of the certified image. That covers the `0x1D72F8` chunk
  table in `002F6AB0` and the `0x112470` sub-chunk table in `00232380`.
- **Data (D1–D4):** the shipped `FFXII_TZA.vbf`. Every `.mpk`'s slot 8 is taken with `gen_ym00_census.slot9`, the
  map-ctrl pack page's parser, which that page proved against `002F6AB0`. The bytes are read as they ship; nothing is
  loaded into the game.
- **Inference:** "no code writes them" rests on two things. One is the index-idiom census (S6), with the consumers and
  the loader read (S4, S7). The other is D2: an authored inverse makes a load-time builder unnecessary, though D2
  alone does not rule one out.

## Limits (SWE2-ORACLE)

- **The S6 census.** It finds writers that form the 144-byte index the way the five walks do. A write through a pointer
  obtained another way, such as a `memcpy` of the whole file or a relocation pass over the loaded pack, is not
  excluded statically. Such a write would have to reproduce the inverse the file already holds.
- **Not executed.** No run-time observation of a loaded table was made (T3 if wanted).
- **Out of scope.** The subrecord's other fields (`+0x04` flags, `+0x08`–`+0x0F`) are not interpreted here. Nor is
  which table a given query uses beyond the `02EC1370` / `02EC1378` split.

## Review and routing (SWE2-ORACLE)

- Review: `ORACLE-REQ-AUDITSPEC-SD182-0930` (SWE2-AUDIT-SPEC).
- Row restatement: `ORACLE-REQ-DATA-SD182-ROW-0930` (SWE2-DATA). The register row and the page are not edited here.
