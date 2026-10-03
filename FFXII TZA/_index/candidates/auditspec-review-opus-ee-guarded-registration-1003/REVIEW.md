# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-guarded-registration-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-GUARDED-REGISTRATION-1003` · Package: `_index/candidates/opus-ee-guarded-registration-1003/` (rows committed in `693d650d4`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The values in all 43 rows are correct against the bytes. Each V is the first vtable that the body stores into an address it also loads with a `lea`, and the RTTI name is the locator's. The lead misdescribes what V is for 18 of the 43, and the "no vtable store" exclusion reason is wrong for 19 of the 56. In detail:
- **(a), what V is.** The lead says each stub "constructs its static class descriptor through `00632D80`" and that V is stored "into the static descriptor X".
  - That holds for only 15 rows.
  - 10 rows construct their descriptor through `00632C90` (`PClassDescriptorWrapper<T>`).
  - **18 rows construct no class descriptor at all.** Their V is the vtable of a static data-member object, a `PTypeDefault` or a named-semantic descriptor.
  - "What differs ... is the static descriptor and the vtable" also understates bodies of 129-3757 B.
- **(b), exclusions.** For 19 of the 54 "no vtable store into the static object" exclusions, that wording is untrue in plain reading. Each stores an RTTI-located vtable into a static object, but not at an address the body itself loads by `lea` (or not from `rax`). The checker's narrow store pattern refuses them, not the family form.

The narrowing below corrects the lead, the value-column header and the exclusion reasons. No row changes. If OPUS prefers not to reword, the alternative is to drop the 18 non-descriptor rows (see the notes).

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - `ex_static_vtable` uses `_rdata_refs`, which imports `pefile`, and the analysis venv lacks it. Check was therefore run in place with `-B` under `C:\Python314\python.exe` (3.14.6); check mode writes nothing.
  - Exit 0: `members 99, committed rows 43, declared exclusions 56` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.**
  - `ex_static_vtable` with `reg: any` decodes the census extent. "loaded" is the set of targets of **every** `lea` except `lea rax`, including guard variables, member objects and caller records.
  - The anchor is the first `lea rax, [V]` immediately followed by `mov qword ptr [rip+d], rax` with the target in "loaded". V's RTTI locator gives T (for `PClassDescriptor*<T>`) or the decorated class.
  - It does **not** test that the target is a class descriptor, or that any descriptor constructor is called. That is how 18 non-descriptor rows derive.
  - It compares all six columns with `rows.tsv`.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 21 (`006A72B0`) each failed: value swapped with row 22 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent re-derivation** (disw.py image reader over `graph/functions.tsv` extents, and a separately written RTTI reader; not retool and not fam_rows).
  - All 43 rows were recomputed: the first `lea rax` / `mov [rip], rax` into a `lea`-loaded address, then COL at V - 8 and TD + 0x10.
  - **43 of 43 are identical** to `rows.tsv`.
  - `members/rtti-class-vtables.tsv` gives the same mangled name for all 43 V.
- **What the stored-into object is.** Each row's store target was compared with the `rcx` the body passes to a descriptor constructor:
  - **15 rows:** the body calls `00632D80`, and the target is that descriptor. V is `PClassDescriptorAbstract<T>`, and each of the 15 later stores `PClassDescriptorConcrete<T>` into the same descriptor.
  - **10 rows** (`006143B0`, `006B0760`, `006B08A0`, `006B09E0`, `006B0B20`, `006B0EC0`, `006B1320`, `006B1600`, `006B19A0`, `006B33F0`): the body calls `00632C90`, not `00632D80`, and the target is that descriptor. V is `PClassDescriptorWrapper<T>`.
  - **18 rows:** the body calls neither `00632D80` nor `00632C90`, and the target is not a class descriptor. V is:
    - a data-member object's vtable, 15 rows: `PClassDataMemberPhyreArray<…>` (10), `PClassDataMemberPhyreSharray<…>` (3) and `PClassDataMemberArrayDynamic<…>` (2). They are `00618080`, `00618620`, `00635DC0`, `00665870`, `00666380`, `00667230`, `00696470`, `006A72B0`, `006AE350`, `006BC750`, `006C3380`, `006D0D50`, `006D0FA0`, `006D8EF0` and `00879D60`;
    - `PTypeDefault<unsigned int>`: `006315B0`;
    - `PNamedSemanticDescriptorForType<…>`: `00661A70` and `006D5810`.
  - Example: `006A72B0` constructs the data member at `02E4D730` through the array data-member constructor `00632A10`, then stores `00D7B5D8` (`PClassDataMemberArrayDynamic<PString>`) into it at `006A7353`. That is the row's anchor and value.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39 and 42.
  - **Value and anchor exact in 15 of 15.**
  - By the lead's description, 4 of the 15 are mislabelled. Indices 12 (`00661A70`) and 39 (`006D5810`) are named-semantic descriptors, and 15 (`00667230`) and 21 (`006A72B0`) are data members.
  - Examples of correct descriptor rows: `005B51D9` -> `00D32C40` T = `PArray<float,4>`, and `006B091A` -> `00D7FA70` `sce::Vectormath::Scalar::Aos::Matrix4` (Wrapper).
- **Excluded sample.** All 56 were classified, and 5 were read in full: `005FCF20`, `00693EC0`, `00634830`, `00635470` and `006949A0`. None of the 56 calls `00632D80` or `00632C90`.
  - **35** store no RTTI-located vtable at all, for example `005FCF20` and `00693EC0`. **Genuine.**
  - **2** (`006352A0` and `006357E0`) first store the shared base `PClassDataMember` vtable `00D580B0`, so the value-dedup removes both. That is genuine for the checker's "first store" rule, although `006357E0` later stores its own `PClassDataMemberPhyreSharray<PString>`.
  - **19** do store an RTTI-located vtable (`PMethodCallerConcrete<…>` / `PFunctionCallerConcrete<…>`) into a static object right after its `lea`.
    - The checker refuses them only because the store address is not itself `lea`-loaded: it lies at an offset inside a `lea`-loaded record (19 of 19). In 4 of them the first store is also from `rdi`, `rsi` or `r14`, not `rax`.
    - Examples: `00634830` stores `00D59010` (`PMethodCallerConcrete<PClassDescriptor,…>`), `00635470` stores `00D58F20`, and `006949A0` stores `00D7B060`.
    - These are the same kind of object as the 18 non-descriptor rows that were accepted. The boundary between rows and exclusions is the checker's store pattern, not the family form.
    - **The stated reason is untrue in plain reading.** The exclusions are conservative: they earn nothing.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction unique to the member: the `lea rax`, whose V is distinct across rows.
  - Each row states V and its RTTI class, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **The conditions are met for the values.** What the page says the values *are* is wrong for 18 rows. That is what the narrowing fixes.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing 1: the lead, in spec.json `lead` and the page section.** Replace:

> shares one pattern in many spellings, stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs its static class descriptor through `00632D80`, installs that descriptor's vtable, and registers members and teardowns. What differs from member to member is the static descriptor and the vtable stored into it. Each row anchors the `lea rax, [V]` whose following `mov` stores V into the static descriptor X the body also loads with a `lea` (the member's distinguishing instruction), and states V and the class V's MSVC RTTI complete-object locator names, read from the certified image.

with:

> shares a pattern, not a form (129 to 3757 bytes), stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs one or more static Phyre metadata objects and registers members and teardowns. Members differ in far more than the anchored instruction. Each row anchors the body's first `lea rax, [V]` whose following `mov` stores V into a static object X that the body also loads with a `lea`, and states V and the class V's MSVC RTTI complete-object locator names, read from the certified image: the template argument T for a `PClassDescriptor*<T>`, otherwise the decorated class.
> - In 25 rows, X is the static class descriptor the body constructs. In 15, it is built through `00632D80` and V is its `PClassDescriptorAbstract<T>` vtable, which a later store replaces with `PClassDescriptorConcrete<T>`. In 10, it is built through `00632C90` and V is its `PClassDescriptorWrapper<T>` vtable.
> - In the other 18, the body constructs no class descriptor. X is a static data-member object in 15 rows (`PClassDataMember*<…>`), a `PTypeDefault<unsigned int>` in `006315B0`, and a `PNamedSemanticDescriptorForType<…>` in `00661A70` and `006D5810`.

**Narrowing 2: column headers in spec.json.** Change `value_col` from "vtable V installed" to "first vtable V stored into a lea-loaded static". Change `name_col` from "reflected type (RTTI before V)" to "class named by the RTTI locator before V (T for a class descriptor)".

**Narrowing 3: README "No rows" and the `excluded.tsv` reasons.** Replace "54: no vtable store into the static object" with:

> 35: no RTTI-located vtable is stored at all; 19: a vtable (a `PMethodCallerConcrete` or `PFunctionCallerConcrete` caller object) is stored into an offset inside a `lea`-loaded record, or from a register other than `rax`, which the checker's store pattern does not match. These 19 are refused by the checker's pattern, not by the form.

**Notes (non-blocking):**
- **Alternative to Narrowing 1.** If the rows are meant to be class-descriptor rows only, require the store target to be the `rcx` of a `00632D80`/`00632C90` call in `ex_static_vtable` and re-derive. That gives 25 rows: the 18 listed above move to `excluded.tsv`. Then the lead needs only the `00632C90`/Wrapper correction and the "differs" correction.
- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
