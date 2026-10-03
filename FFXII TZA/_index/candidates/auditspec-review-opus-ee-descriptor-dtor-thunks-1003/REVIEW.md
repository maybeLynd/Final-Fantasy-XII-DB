# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-descriptor-dtor-thunks-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-DESCRIPTOR-DTOR-THUNKS-1003` · Package: `_index/candidates/opus-ee-descriptor-dtor-thunks-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 384 rows are correct against the bytes, and the lead's "members differ only at the first instruction" is true. None of the three defect patterns from the earlier sibling reviews changes a stated fact here. The printed controls cannot fail (see the notes), but the row comparison they sit beside is sensitive.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - `ex_vtable_store` uses `_rdata_refs`, which imports `pefile`, and the analysis venv lacks it. Check was therefore run in place with `-B` under `C:\Python314\python.exe` (3.14.6); check mode writes nothing.
  - Exit 0: `members 384, committed rows 384, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.** `ex_vtable_store` decodes 16 bytes and requires the full form: `lea rax, [V]`, `mov qword ptr [rcx], rax`, and `jmp 0x633390`. The form is 15 bytes, so the 16-byte window cannot reach another function's code in a way that changes the result. It reads the RTTI complete-object locator at V - 8, then the type descriptor's decorated name, and states T or the decorated name. It compares all six columns, and requires the anchor to be at or after the entry (`entry_anchor`) and inside the body.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as in the reviewed sibling packages.
  - `ok1` and `ok2` compare an extracted value with a different row's value, and an anchor with anchor + 1. Neither passes anything through the row comparison.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 192 (`00646460`) each failed: value swapped with row 193 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 384 members have **one** masked form: `lea rax, [V]` / `mov qword ptr [rcx], rax` / `jmp 00633390`.
  - The only position that varies is + 0x0, the `lea`, with 384 distinct V. The `jmp` target is `00633390` in 384 of 384.
  - The lead's "members differ only at the first instruction" is exact.
- **All rows re-derived independently.**
  - All 384 rows were recomputed with a separately written RTTI reader: COL = qword at V - 8, signature 1, type-descriptor RVA at COL + 12, name at TD + 0x10.
  - **384 of 384 are identical** to `rows.tsv`, with 384 distinct V.
  - Second source: `members/rtti-class-vtables.tsv` lists all 384 V. Its mangled name equals the image's locator name in 384 of 384.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 27, 55, 82, 109, 137, 164, 192, 219, 246, 274, 301, 328, 356 and 383. Examples:
  - `00597EC0` -> `00D24898`, `.?AV?$PClassDescriptorForType@VPClusterHeader@PBinary@PSerialization@Phyre@@@Phyre@@`, which is `Phyre::PSerialization::PBinary::PClusterHeader`;
  - `005DD020` -> `00D4D920`, the decorated argument `V?$PArray@PEBVPContextSwitch@PRendering@Phyre@@$07@Phyre@@`;
  - `00879AF0` -> `01CD9A68`, `Phyre::PGame::PGameConfig`.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. No member shares a V, so the value-dedup in `derive_all` removed none.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Members differ only at the entry instruction. The adopted sentence allows the entry instruction as the anchor in exactly that case, and each row anchors it.
  - Each row states the member-specific V and the type its locator names, both read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` (a swapped value and a moved anchor) through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes, so that an extractor which stops reading the image fails. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs an interpreter with pefile.
