# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-two-member-registrars-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-TWO-MEMBER-REGISTRARS-1003` · Package: `_index/candidates/opus-ee-two-member-registrars-1003/` (rows committed in `693d650d4`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 38 rows are correct against the bytes. Each V is the vtable stored into the static descriptor right after its `00632D80` construction. The lead is wrong on two points:
- It says members share "one pattern in many spellings" and differ in "the static descriptor and the vtable stored into it". In fact they share one exact 815-byte form and differ at 53 non-branch instructions.
- It calls V "that descriptor's vtable". V is the transient `PClassDescriptorAbstract<T>` vtable, which a later store in every member replaces with `PClassDescriptorConcrete<T>`.

The narrowing below corrects the lead. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - `ex_static_vtable` calls `_rdata_refs`, which imports `pefile`, and the analysis venv lacks it. Check was therefore run in place with `-B` under `C:\Python314\python.exe` (3.14.6); check mode writes nothing.
  - Exit 0: `members 38, committed rows 38, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.**
  - `ex_static_vtable` (reg `any`) decodes the census extent. "loaded" is the set of targets of every `lea` except `lea rax`. The anchor is the **first** `lea rax, [V]` immediately followed by `mov qword ptr [rip+d], rax` whose target is in "loaded".
  - V's RTTI locator gives T, or the decorated name. It compares all six columns with `rows.tsv`.
  - It does not check that the store target is the descriptor that `00632D80` constructs. That holds here by the census.
- **Controls' sensitivity: the printed controls are tautologies.** This is the same code as the reviewed siblings.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison is sensitive. In-memory mutations of row 19 (`005EEE50`) each failed: value swapped with row 20 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 38 members are 815 B with **one** masked form of 158 instructions. The call sequence is the same in all 38: four guard header/footer pairs, `00632D80`, the three `0063DC80`/`0063DF90`/`0063DFA0` helpers, `00632960`, `00632A10`, `006B66C0`, `006B67D0`, `006388C0` and the tail `00639450`.
  - **64 positions vary**: 11 are intra-body branches (by address only), and **53 are real operands**. The real ones include:
    - the guard variables;
    - the `lea rsi` descriptor;
    - the name-pointer cell (`mov rdi, [cell]`);
    - the `PClassDescriptorAbstract` vtable at + 0xA9 (the anchor);
    - the three `lea rdx` helper arguments;
    - the `PClassDescriptorConcrete` vtable at + 0xEC;
    - the teardown thunks;
    - the m_els element descriptor `lea r8` at + 0x296;
    - the `PClassDataMemberArrayDynamic` vtable at + 0x2AC;
    - three dword immediates.
  - So the lead's "many spellings" and its "what differs" sentence are both untrue: there is one spelling, and much more differs.
  - Every member stores two vtables into the same descriptor: `PClassDescriptorAbstract<T>` at + 0xA9, right after `00632D80`, then `PClassDescriptorConcrete<T>` at + 0xEC (38 of 38).
- **All rows re-derived independently.**
  - All 38 rows were recomputed with a separately written reader: the first `lea rax` / `mov [rip], rax` into a `lea`-loaded address, then RTTI at V - 8.
  - **38 of 38 are identical** to `rows.tsv`.
  - In all 38, the store target equals the `rcx` passed to `00632D80`, so V is stored into the constructed descriptor.
- **Sampled rows.** 15 spread rows were inspected at 0-based indices 0, 3, 5, 8, 11, 13, 16, 18, 21, 24, 26, 29, 32, 34 and 37. Examples:
  - `005B5B89` -> `00D33838`, `PClassDescriptorAbstract<PArray<PAnimationChannelTarget,8>>`, giving T = `V?$PArray@VPAnimationChannelTarget@PAnimation@Phyre@@$07@Phyre@@`;
  - `006691E9` -> `00D6A248`, T = `PArray<PDataBlockD3D11,8>`;
  - `006D2A99` -> `00D8CE18`, T = `PArray<PRenderStreamInput,4>`.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction unique to the member (the + 0xA9 `lea rax`; V is distinct in every member).
  - Each row states V and T, read from the image.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the page section.** Replace:

> shares one pattern in many spellings, stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs its static class descriptor through `00632D80`, installs that descriptor's vtable, and registers members and teardowns. What differs from member to member is the static descriptor and the vtable stored into it. Each row anchors the `lea rax, [V]` whose following `mov` stores V into the static descriptor X the body also loads with a `lea` (the member's distinguishing instruction), and states V and the class V's MSVC RTTI complete-object locator names, read from the certified image.

with:

> shares one 815-byte form, stated here once and not repeated per row. Under the thread-safe static-init guard (`008092FC` / `0080929C`), each stub constructs its static class descriptor through `00632D80`, stores the `PClassDescriptorAbstract<T>` vtable into it, calls the three member-registration helpers, then replaces that vtable with `PClassDescriptorConcrete<T>`, and goes on to register the `m_count` and `m_els` members and their teardowns. Members differ in every per-class operand of that form (53 instructions: the descriptor, its guard variables, both vtables, the helper arguments, the element descriptor and the teardowns). Each row anchors the first of them that names the class, the `lea rax, [V]` at + 0xA9 whose following `mov` stores the `PClassDescriptorAbstract<T>` vtable V into the descriptor. It states V and T, the template argument named by V's MSVC RTTI complete-object locator, read from the certified image.

**Notes (non-blocking):**
- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes. Today's controls cannot fail while the extractor returns anything.
- **Checker scope.** `ex_static_vtable` accepts a store into any `lea`-loaded address, not only the `00632D80` descriptor. It is correct here only by the census; the guarded-registration sibling shows the cost (18 rows on non-descriptor objects). Requiring the store target to be the `rcx` of the `00632D80`/`00632C90` call would make the lead's claim part of the check.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs it.
