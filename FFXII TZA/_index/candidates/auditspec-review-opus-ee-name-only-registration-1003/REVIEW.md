# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-name-only-registration-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-NAME-ONLY-REGISTRATION-1003` · Package: `_index/candidates/opus-ee-name-only-registration-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 91 rows are correct against the bytes, and the lead's account of the shared form and what varies is exact. The 19 exclusions are described wrongly in three places:
- The lead and the `excluded.tsv` header say these members do not derive. All 19 derive.
- The README says "the checker fails if any of them starts deriving". For these 19 that check cannot fail.

They are policy skips (pass-22), not image refusals. The narrowing below corrects the wording. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 110, committed rows 91, declared exclusions 19` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.** `ex_descriptor_lea` decodes the census extent (`_body`). It takes the `lea rcx` instructions; with `same_target_ok`, it keeps the first when all name one X. It names X through every `retool.scan` reference site that is `lea rcx, [X]` followed by a direct call to a wrapper whose `lea r8` before its one `call 00632D80` is a clean string. All such names must agree. It compares all six columns with `rows.tsv`.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 45 (`00641430`) each failed: value swapped with row 46 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
  - **The exclusion check cannot fail for these 19.**
    - `derive_all` removes every `spec.json` `skip` entry from the derived rows unconditionally.
    - So `cmd_check`'s "declared excluded but the image now gives a row" can never fire for them, whatever the image says.
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 110 members have **one** masked form at 32 bytes: `sub rsp,0x28 / lea rcx,[X] / call 006388C0 / lea rcx,[X] / add rsp,0x28 / jmp 00639450`. The call and the jmp go to `006388C0` and `00639450` in 110 of 110.
  - The only positions that vary are the two `lea rcx` instructions, at + 0x4 and + 0x10. They name the same X in every member, with 110 distinct X.
  - The lead's shape and its "what differs" sentence are exact.
- **All rows re-derived independently.**
  - Method: a **raw-byte** index of every `48 8D 0D rel32` (`lea rcx, [rip+d]`) followed directly by `E8 rel32` in executable sections. Through it, the static initialiser that loads X and calls a wrapper. Then the wrapper's `lea r8` before its one `call 00632D80`.
  - **91 of 91 rows are identical** to `rows.tsv`, with 91 distinct X.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 6, 13, 19, 26, 32, 39, 45, 51, 58, 64, 71, 77, 84 and 90. Examples: `00584D14` -> `02CAA0A0` PClusterHeader, `006888E4` -> `02E495D0` PPhysicsShapeBullet, and `00875634` -> `02EB8160` PVisionTrackerWin32. In each, the anchor is the + 0x4 `lea`. **15 of 15 exact.**
- **Excluded sample.** All 19 exclusions were examined, not only 5.
  - **Each one derives** under the independent reader. Each has the 32-byte form, one X and one class name. Examples: `00867660` -> `02EB59F0` PInputSourceTouchRotate, `0086E010` -> `02EB62F0` PInputSourceMotionQuatW, `0086E450` -> `02EB6BF0` PInputSourceVisionTrackerZ.
  - **The stated reason is true:** `00875E10` (229 bytes, 35 distinct direct callees) calls each of the 19 once, and calls none of the 91 row members.
  - Whether `00875E10` is "another layer" was not re-derived. It is the `PInputs::PUtilityInputs` slot-10 entry in the vtable index.
  - The exclusions are conservative: a skipped member earns nothing.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction unique to the member: the + 0x4 `lea`, whose X is unique.
  - Each row states X and its class, both read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met** for the 91 rows.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing 1: the lead's last sentence, in spec.json `lead` and the page section.** Replace:

> Members that do not derive are listed in [`excluded.tsv`](...).

with:

> Nineteen members that derive are left without a row by a declared skip (spec.json `skip`), each with its reason in [`excluded.tsv`](...): `00875E10`, a caller in another layer, calls each of them, and citing them here would pull that caller edge into the page.

**Narrowing 2: README "No rows".** Replace "The checker fails if any of them starts deriving." with:

> These are declared skips, not image refusals: all 19 derive, and `derive_all` removes them before the comparison, so the check does not test them.

The generic `excluded.tsv` header ("members the image refuses for this family's per-member form") is also untrue of these 19. Either regenerate it with a header that distinguishes skips, or add a `skip` marker to their reason.

**Notes (non-blocking):**
- **Control repair.**
  - Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0.
  - Add a raw-byte known-answer row.
  - For skips, have check derive the skipped members separately and assert that they still derive and that the skip reason still holds, for example that `00875E10` still calls them. Without that, the skip list is never re-verified.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
