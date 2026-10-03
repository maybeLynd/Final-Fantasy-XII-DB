# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-flag-selected-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-FLAG-SELECTED-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-flag-selected-adapters-1003/` (rows committed in `693d650d4`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 11 rows are correct against the bytes. The lead's shape and "what differs" sentence are exact. There are no exclusions. The printed controls cannot fail (see the notes), but the row comparison is sensitive.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 11, committed rows 11, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
  - This package's `fam_rows.py` is the revision that also carries `ex_fetch_call` and `ex_static_vtable`. Its `ex_descriptor_lea` is unchanged from the other packages.
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `rcx`, `same_target_ok`) decodes the census extent. Every `lea rcx` must name one X, and the first is the anchor.
  - It names X through the static initialiser (`lea rcx, [X]` plus a wrapper call) and the wrapper's `lea r8` before its one `call 00632D80`. All such names must agree.
  - It compares all six columns with `rows.tsv`.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 5 (`005A1650`) each failed: value swapped with row 6 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 11 members are 46 B with **one** masked form: `sub rsp,0x28 / lea rcx,[X] / test r8b,r8b / je / mov r8b,1 / call 0063E2E0 / mov al,1 / ... / xor r8d,r8d / call 0063E2E0 / mov al,1 / ...`.
  - The only varying positions are the + 0x4 `lea rcx` (11 distinct X) and the intra-body `je`, by address only. Each member has one `lea rcx` and two calls to `0063E2E0`.
  - The lead ("`lea rcx, [X]`, then a call to the shared traversal `0063E2E0` with the flag in `r8b` normalised to 1 or 0") is exact.
  - This is the same byte form as the 46 B variant of the object-traversal family. No entry and no X is shared with that family's 304 rows.
- **All rows re-derived independently.**
  - Method: a raw-byte `48 8D 0D rel32` + `E8 rel32` index finds the initialiser that loads X, then the wrapper's `lea r8` before its one `call 00632D80` gives the name.
  - **11 of 11 rows are identical** to `rows.tsv`, with 11 distinct X.
- **Sampled rows.** The family has 11 rows, so all 11 were inspected. In each, the anchor is at entry + 0x4. Examples: `00584754` -> `02CA9FA0` PClusterHeaderBase, `005A17F4` -> `02CAE960` PAnimationSlotFilterDeferredLoad, and `00674CD4` -> `02D3E780` PAssetReferenceImport. **11 of 11 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's only varying instruction: the + 0x4 `lea rcx`, which is not the entry instruction, and whose X is unique.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
