# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-registry-fetch-adapters-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-REGISTRY-FETCH-ADAPTERS-1003` · Package: `_index/candidates/opus-ee-registry-fetch-adapters-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 15 rows are correct against the bytes, and the lead's "no two members call the same one" holds for all 84 members. The 69 exclusions are genuine for the reason they state: the image holds no static class name for those fetch functions. The printed controls cannot fail (see the notes), but the row comparison is sensitive.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (3.14.6), because the analysis venv lacks the `pefile` that the shared module imports. Check mode writes nothing.
  - Exit 0: `members 84, committed rows 15, declared exclusions 69` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
  - This package's `fam_rows.py` adds `ex_fetch_call` and `_r8_string` to the shared module.
- **What the checker tests.**
  - `ex_fetch_call` decodes the census extent. The value G is the target of the first direct call.
  - The name comes from inside G: the `r8` argument of G's first call to `00632C90` or `00632D80`. That is either a `lea r8, [S]`, or `mov r8, REG` with REG loaded from an image qword that points at a clean string.
  - It compares all six columns with `rows.tsv`.
  - It does not itself test that G is unique. The value-dedup in `derive_all` would remove members that share a G.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 7 (`006B2EF0`) each failed: value swapped with row 8 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - With rip targets, branch targets and immediates masked, there are two forms:
    - 15 × 68 B: these are exactly the 15 rows;
    - 69 × 70 B: these are exactly the 69 exclusions. This form adds `xor ecx, ecx` at + 0x6, passing a null argument to the fetch.
  - In both forms, the only varying positions are the intra-body `je` (by address) and the **two** fetch calls, one per path. They have the same target within a member.
  - All 84 first-call targets are distinct, so "no two members call the same one" is exact. Each member's other two calls go to `0063E2E0` (168 of 168).
- **All rows re-derived independently.**
  - All 15 rows were recomputed: G, then the `lea r8` before G's first `00632C90`/`00632D80` call. **15 of 15 are identical.**
  - Cross-check: in each G, the vtable stored right after that call has an RTTI locator naming `PClassDescriptorWrapper<the same type>`. For example, `005A02D0` -> "PTimer" / `.?AV?$PClassDescriptorWrapper@VPTimer@Phyre@@@Phyre@@`, and `00613800` -> `CD3D11_BLEND_DESC`.
  - Each G ends `mov rax, rbx`, with rbx the descriptor it constructs (checked on `005A02D0`, `006B0760` and `00613800`). So "the class whose descriptor it constructs and returns" holds.
- **Sampled rows.** The family has only 15 rows, so all 15 were inspected (indices 0-14). The anchor is the first-path call at entry + 0xE in each. **15 of 15 exact.**
- **Excluded sample.** 5 were inspected in depth: `005CAC90`, `005CB0F0`, `0060FEF0`, `00673460` and `006BE720`. The census property was checked on all 69.
  - All 69 have the 70 B form with `xor ecx, ecx`.
  - In each sampled G, the `r8` name argument is `mov r8, rdi`, with rdi loaded from a `.data` cell such as `02CB5BC8` in `005B4E00`. That cell lies past `SizeOfRawData`, so it is **zero at load**. G fills it at run time from its own argument, which these adapters pass as null.
  - The type is a template instance known only through RTTI of the stored vtable, for example `PClassDescriptorAbstract<PArray<unsigned int,4>>` for `005B4E00` and `PArray<PShaderParameterCaptureBufferLocation,2>` for `005EE190`.
  - So "fetch function names no class" is literally true of the image, and the cause is the member's own form, not a read window.
  - **Genuine, 69 of 69.** The exclusions are conservative: they earn nothing.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the member's first fetch call; its target is unique to the member.
  - Each row states G and the class G constructs, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC notes (non-blocking)

- **Optional recovery.**
  - Each of the 69 excluded members still has a unique G: a distinguishing instruction with a member-specific value.
  - A row could state G and the template type taken from RTTI of the vtable G stores. That is the decorated name, as the destructor-thunk package does.
  - This would add up to 69 rows. It is not required, but it is the larger share of this family.
- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
