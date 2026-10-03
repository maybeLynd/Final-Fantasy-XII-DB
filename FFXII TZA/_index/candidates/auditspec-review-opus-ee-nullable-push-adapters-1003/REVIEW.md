# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-nullable-push-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-NULLABLE-PUSH-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-nullable-push-adapters-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 287 rows are correct against the bytes. Within each census sub-shape, members differ only at the anchored `lea r8`. The 8 exclusions are genuine for the reason they state. The printed controls cannot fail (see the notes), but the row comparison is sensitive.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 295, committed rows 287, declared exclusions 8` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `r8`) decodes the **census extent**, not a fixed window, so defect (b) cannot arise. It requires exactly one `lea r8`.
  - It names X through each `retool.scan` reference that is `lea rcx, [X]` plus a direct call to a wrapper whose `lea r8` before its one `call 00632D80` is a clean string. Every such name must agree.
  - It compares all six columns with `rows.tsv`.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 143 (`00643A40`) each failed: value swapped with row 144 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - With rip targets, branch targets and immediates masked, the 295 members fall into three forms: 184 × 60 B, 108 × 64 B and 3 × 63 B.
  - Within a form, the varying positions are:
    - the intra-body `je`, by address only;
    - the `lea r8, [X]`, distinct in every member;
    - in the 64 B form, the `add rdx, imm` member offset (3 values).
  - The page's census row already names that offset as what separates the sub-shapes ("none, 8, 1, 0x30, 0x10"). So the lead's "shares the forms in the census table above ... What differs from member to member is the class descriptor X" is accurate as written.
- **All rows re-derived independently.**
  - Method: a **raw-byte** index of every `48 8D 0D rel32` followed directly by `E8 rel32` in executable sections. The initialiser that loads X then gives the wrapper, and the wrapper's `lea r8` before its one `call 00632D80` gives the name.
  - **287 of 287 rows are identical** to `rows.tsv`, with 287 distinct X.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 20, 41, 61, 82, 102, 123, 143, 163, 184, 204, 225, 245, 266 and 286. Examples: `005A2BB8` -> `02CAF0E0` PTimeScaleOffsetController, `0068A134` -> `02E49CD0` PPhysicsRigidBodyBullet, and `00879864` -> `02EB9E60` PGameConfig. In each, the anchor is the member's only `lea r8`. **15 of 15 exact.**
- **Excluded sample.** All 8 exclusions were examined, not just 5. All 8 are "descriptor not named by exactly one class (0)".
  - Each has the family form with one `lea r8`. Its X is one of eight core descriptors at `02CF8270`..`02CF8A80`, for example `0062EE50` -> `02CF8880`.
  - A raw rip-reference sweep shows these descriptors built by other constructors: `00164010` calls `006323C0`, and `00163E30` calls `00631C40`. They are not built through a `00632D80` wrapper. So the extractor's naming path finds **zero** initialisers, exactly as stated.
  - Their RTTI-named types (from `zero-at-load-objects-named-by-rtti.tsv`) include `PClassDescriptorBase`, `PClassDescriptorForClassDescriptor` and `PClassDescriptorConcrete<PClusterDependencyList>`.
  - **Genuine for the stated reason, 8 of 8.** The exclusions are conservative: they earn nothing.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's only varying operand within its sub-shape: the `lea r8`, whose X is unique.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` (a swapped value and a moved anchor) through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Optional recovery.** The 8 excluded X could be named from the vtable their own initialiser stores into them, for example `00164067` stores `00D56488` into `02CF8880`, read through RTTI. That would add up to 8 rows. It is not required.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
