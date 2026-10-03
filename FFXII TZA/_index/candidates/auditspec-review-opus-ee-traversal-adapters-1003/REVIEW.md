# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-traversal-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-TRAVERSAL-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-traversal-adapters-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 304 rows are correct against the bytes, and "what differs from member to member is X" is exact. The lead's "one shape" is the shape of only 116 members, though. The other 188 (46 B) have no null guard and load X once, before the flag branch. The narrowing below corrects the shape sentence. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 304, committed rows 304, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `rcx`, `same_target_ok`) decodes the census extent. It takes every `lea rcx`, requires that they name one X, and anchors the first.
  - It names X through the static initialiser (`lea rcx, [X]` plus a wrapper call) and the wrapper's `lea r8` before its one `call 00632D80`. All such names must agree.
  - It compares all six columns with `rows.tsv`.
  - It does not check the null guard or the two traversal calls that the lead describes.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 152 (`0065F5E0`) each failed: value swapped with row 153 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows). There are three masked forms:
  - **188 × 46 B:** `sub rsp,0x28 / lea rcx,[X] / test r8b,r8b / je / mov r8b,1 / call 0063E2E0 / ... / xor r8d,r8d / call 0063E2E0 / ...`.
    - There is **no null guard and no object-pointer selection**.
    - X is loaded **once**, at entry + 0x4, before the flag branch, and is shared by both calls.
  - **113 × 76 B:** `mov rax,rdx / xor ecx,ecx / add rdx,8 / test r8b,r8b / je`, then on each path `test rax,rax / cmove rdx,rcx / lea rcx,[X] / call 0063E2E0`.
  - **3 × 75 B:** the same as the 76 B form, with `inc rdx` in place of `add rdx, 8`.
  - Within each form, the only varying positions are the `lea rcx` (304 distinct X, the same X at both loads where there are two) and the intra-body `je`, by address only.
  - Each of the 304 members calls `0063E2E0` exactly twice.
  - The page's own census row says the same: "188 at 46 B traverse the object directly; 116 at 75-76 B add a member offset with a null guard".
- **All rows re-derived independently.**
  - Method: a raw-byte `48 8D 0D rel32` + `E8 rel32` index finds the initialiser that loads X, then the wrapper's `lea r8` before its one `call 00632D80` gives the name.
  - **304 of 304 rows are identical** to `rows.tsv`, with 304 distinct X.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 22, 43, 65, 87, 108, 130, 152, 173, 195, 216, 238, 260, 281 and 303.
  - The anchor is at entry + 0x4 in the 46 B members (for example `005D0E64` -> `02CB9A00` PShaderPass).
  - It is at entry + 0x1C, the first of two loads, in the 76 B members (for example `005A2B2C` -> `02CAF0E0` PTimeScaleOffsetController, and `0086A94C` -> `02EB69F0` PInputSourceVisionTrackerX).
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. The extractor decodes the census extent, so defect (b) cannot arise.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's only varying operand, the (first) `lea rcx`, whose X is unique.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead's shape sentence, in spec.json `lead` and the page section.** Replace:

> shares one shape, stated here once and not repeated per row: a null-guarded selection of the object pointer and the flag, then `lea rcx, [X]` and a call to the shared traversal `0063E2E0` on each path.

with:

> shares two forms, stated here once and not repeated per row (the census row above). In 188 members (46 B), `lea rcx, [X]` comes first, then the flag selects one of two calls to the shared traversal `0063E2E0`, with `r8b` set to 1 or 0. In 116 members (75-76 B), the object pointer is offset by a constant member offset (`add rdx, 8`, or `inc rdx` in three members) and null-guarded, and each flag path then does `lea rcx, [X]` and calls `0063E2E0`.

**Notes (non-blocking):**
- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
