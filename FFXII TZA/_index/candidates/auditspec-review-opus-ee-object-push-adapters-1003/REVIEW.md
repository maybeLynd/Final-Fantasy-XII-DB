# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-object-push-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-OBJECT-PUSH-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-object-push-adapters-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 297 rows are correct against the bytes. Within each census sub-shape, members differ only at the anchored `lea r8`. The 7 exclusions are genuine for the reason they state. The printed controls cannot fail (see the notes), but the row comparison is sensitive.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 304, committed rows 297, declared exclusions 7` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `r8`) decodes the census extent, not a fixed window. It requires exactly one `lea r8`.
  - It names X through the static initialiser (`lea rcx, [X]` plus a wrapper call) and that wrapper's `lea r8` before its one `call 00632D80`. All such names must agree.
  - It compares all six columns with `rows.tsv`.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 148 (`00642B10`) each failed: value swapped with row 149 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - With rip targets, branch targets and immediates masked, there are five forms: 188 × 21 B, 111 × 31 B, 3 × 31 B and two singletons of 31 B. That matches the page's census row: "188 at 21 B push directly; 116 at 31 B add a constant member offset under a null guard".
  - Within every form, the **only** varying position is the `lea r8, [X]`, at + 0x9 in the 21 B form and + 0xC in the 31 B forms.
  - The lead's "What differs from member to member is the class descriptor X" is exact within the census sub-shapes, which the lead cites.
- **All rows re-derived independently.**
  - Method: a raw-byte `48 8D 0D rel32` + `E8 rel32` index finds the initialiser that loads X, then the wrapper's `lea r8` before its one `call 00632D80` gives the name.
  - **297 of 297 rows are identical** to `rows.tsv`, with 297 distinct X.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 21, 42, 63, 85, 106, 127, 148, 169, 190, 211, 233, 254, 275 and 296. Examples: `005A0E89` -> `02CAD640` PAnimationChannelTarget, `0063F54C` -> `02D356A0` PMLAABase, and `00869650`'s anchor `0086965C` -> `02EB66F0` PInputSourceMotionLinearAccelerationX. **15 of 15 exact.**
- **Excluded sample.** All 7 exclusions were examined. All 7 are "descriptor not named by exactly one class (0)".
  - Each has the form with one `lea r8`. Its X is one of the core descriptors `02CF8370`..`02CF8A80`, for example `0062EF00` -> `02CF8880`, `0062F1C0` -> `02CF8470` and `0062FB60` -> `02CF8680`.
  - These descriptors are built by other constructors, not a `00632D80` wrapper (`00164010` calls `006323C0`, and `00163E30` calls `00631C40`). So the naming path finds zero initialisers, as stated.
  - These are the same seven X that the nullable sibling excludes, plus that sibling's eighth, `02CF8270`.
  - **Genuine for the stated reason, 7 of 7.** The exclusions are conservative: they earn nothing.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's only varying instruction: the `lea r8`, whose X is unique.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Optional recovery.** The 7 excluded X could be named from the vtable each one's initialiser stores into it, read through RTTI (see the nullable review). That would add up to 7 rows.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
