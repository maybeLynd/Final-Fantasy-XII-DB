# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-descriptor-static-initialisers-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-DESCRIPTOR-STATIC-INITIALISERS-1003` · Package: `_index/candidates/opus-ee-descriptor-static-initialisers-1003/` (rows committed in `4523bdf31`, checker and README revised in `c480be543`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` (section installed at line 4436)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 254 rows are correct against the bytes. An independent cross-check through RTTI agrees 254 of 254. The shape sentence is also exact: all 254 members share one nine-instruction form. But the lead says "What differs from member to member is the class descriptor X". In fact members differ at four independent operands, and two more operands follow from X. Second problem: the lead says a member whose loads name more than one X fails the check. With `first_lea` set, the checker cannot refuse such a member, and every member has two `lea rcx` with different targets. The narrowing below corrects both sentences. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under the analysis venv python. Capstone and pefile were both present. Check mode writes nothing.
  - Exit 0: `members 254, committed rows 254, declared exclusions 0` / `control swapped-value: refused (2 ...)` / `control moved-anchor: refused (1 ...)` / `known answer 001603E0: anchor 001603E4 references 02CAD140 in its raw bytes = committed value` / `FAILS 0`.
  - The output is identical to the committed `fam_rows_check.out`, apart from CRLF line endings.
  - `fam_rows.py apply` (no `--apply`) printed `ALREADY (section matches rows.tsv)` / `FAILS 0`, and `git status` shows the page unchanged.
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `rcx`, `same_target_ok`, `first_lea`) decodes the census extent (`functions.tsv` size, not a fixed window). It takes the **first** `lea rcx` and drops any later one.
  - It names X through every static initialiser that does `lea rcx, [X]` plus a direct call, and that wrapper's `lea r8` before its one `call 00632D80`. All such names must agree.
  - It compares all six columns with `rows.tsv` and requires one row per member.
  - It does **not** check the nine-instruction form, the `[X+0xFC]` clear, the vtable store or the `00808B90` tail. Because of `first_lea`, it also cannot refuse a member whose `lea rcx` loads name two targets.
- **Controls' sensitivity, tested by feeding rows to the checker in memory.** The comparison is sensitive, and the swap/move controls now pass mutated rows through it. That fixes the tautology found in the earlier batches.
  - With the real extractor, each mutation of row 152 (`001660C0`) failed:
    - value swapped with row 153: FAILS 2;
    - name changed: FAILS 1;
    - anchor + 7, onto the call: FAILS 1;
    - row deleted: FAILS 1.
  - **T6:** an image-blind extractor that echoes `rows.tsv` still prints both controls "refused" and FAILS 0. Only the known-answer line reads the image, and it reads row 0 only.
    - Echo + row 0 value corrupted: FAILS 1, caught by the known answer.
    - Echo + row 5 value corrupted: **FAILS 0**.
  - Non-blocking. The rows were re-derived independently below, so this does not affect the verdict.
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 254 members are 53 B. All decode to one masked form: `sub rsp,0x28 / lea rcx,[X] / call W / and dword [X+0xFC],0xFFFFFFFD / lea rax,[V] / lea rcx,[T] / mov qword [X],rax / add rsp,0x28 / jmp 00808B90`.
  - The `and` target is X + 0xFC and the `mov` target is X in 254 of 254 members.
  - `00808B90` is `atexit` (it calls `_onexit`).
  - Distinct values per operand position:
    - entry+0x4 `lea rcx` X: **254**;
    - entry+0xB `call` W: **254**;
    - entry+0x10 `and` target: 254 (= X + 0xFC);
    - entry+0x17 `lea rax` V: **254**;
    - entry+0x1E `lea rcx` T: **254**;
    - entry+0x25 `mov` target: 254 (= X);
    - all other positions: 1.
  - So members differ at six instructions, four of them independent: X, W, V and T.
  - V is each class's own `PClassDescriptorConcrete<T>` vftable, not one shared "concrete vtable". The page's own frontmatter row already says that W is per type ("254 distinct external targets").
- **All rows re-derived independently.**
  - X and its anchor were read from the masked census. 254 of 254 match `rows.tsv`, with 254 distinct X.
  - Class name, two independent ways:
    - W's `lea r8` string before its one `call 00632D80`;
    - the MSVC RTTI type name behind V's complete-object locator, for example `.?AV?$PClassDescriptorConcrete@VPAnimatableComponent@PAnimation@Phyre@@@Phyre@@`.
  - Both agree with the row's name for **254 of 254**.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 18, 36, 54, 72, 90, 108, 126, 145, 163, 181, 199, 217, 235 and 253.
  - Examples: `001603E0` -> `02CAD140` PAnimatableComponent; `00161A90` -> `02CBA400` PShaderParameterCaptureBufferRWStructuredBuffer; `00166950` -> `02E48DD0` PPhysicsShape; `0016D560` -> `02EB9E60` PGameConfig.
  - In each, the anchor is entry + 0x4, and W, V (RTTI) and T were read.
  - `001603E0` was also read in full with `disr.py`.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. The extractor reads the census extent, so defect (b), a fixed byte window, cannot arise.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction that distinguishes the member: the first `lea rcx`, whose X is unique across the 254.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing 1: what differs, in spec.json `lead` and the page section.** Replace:

> stores the concrete vtable at qword [X], and tail-jumps to 00808B90 with rcx = its static teardown (the atexit registration); all 254 have exactly this nine-instruction form. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (the first `lea rcx` in the body; the second loads the member's teardown, part of the shared form). Each row anchors the first such `lea`, the member's distinguishing instruction, and states X and the class X describes.

with:

> stores its class's own `PClassDescriptorConcrete<T>` vftable at qword [X], and tail-jumps to 00808B90 (atexit) with rcx = its static teardown; all 254 have exactly this nine-instruction form. Four operands differ from member to member, each unique to its member: the class descriptor X (the first `lea rcx`, re-used by the `and` at X+0xFC and the vftable store at X), the constructor wrapper the `call` targets, the vftable the `lea rax` loads, and the teardown the second `lea rcx` loads. Each row anchors the first `lea rcx`, the member's distinguishing instruction, and states X and the class X describes; the other three operands follow from the class and are not checked per row.

**Narrowing 2: the refusal sentence.** Replace:

> A member whose loads name more than one X, a descriptor not named by exactly one class, or a value that differs fails it.

with:

> Only the first `lea rcx` is read (the second, the teardown, is ignored); a member with no `lea rcx`, a descriptor not named by exactly one class, or a value that differs fails it.

**Notes (non-blocking):**
- **Bit wording.** "clears bit 0x2" means mask `0xFFFFFFFD`. The page elsewhere says "flag bit 1". "Clears bit 1 (mask 0x2)" would be unambiguous.
- **Control strength.** Extend the known answer from row 0 to every row: each anchor's raw-byte reference must equal its value. It is cheap, and it closes the T6 gap. Today an image-blind extractor passes everything except a defect in row 0.
- **Form check.** The checker's docstring says derive "refuses a member whose body does not have the family's form", but `descriptor_lea` with `first_lea` does not test the form. The form sentence is true today (census above); the checker does not enforce it.
