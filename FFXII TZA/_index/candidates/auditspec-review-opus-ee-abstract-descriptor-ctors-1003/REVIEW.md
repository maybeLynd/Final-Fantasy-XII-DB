# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-abstract-descriptor-ctors-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-ABSTRACT-DESCRIPTOR-CTORS-1003` · Package: `_index/candidates/opus-ee-abstract-descriptor-ctors-1003/` (rows committed in `4523bdf31`, package last touched in `c480be543`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` (section "Per-member rows: the class name and size each AbstractClassDescriptor constructor registers", installed)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 178 rows are correct against the bytes. The anchored `lea r8, [S]` is unique to each member (178 distinct S), so the rule's conditions are met. Two sentences of the lead are wrong, though:
- "stores the concrete vtable": every member stores its own `PClassDescriptorAbstract<T>` vtable.
- "What differs from member to member is the name and size it passes": members differ at up to nine instructions. The name `lea`, the vtable `lea` and the three `lea rdx` arguments differ in every member.

This is defect pattern (a). The base-aware sibling section on the same page (line ~3232) was already narrowed in this way. The narrowing below corrects both sentences. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** Check was run in place with `-B` under `C:\Python314\python.exe` (it has capstone and pefile). Check mode writes nothing.
  - Exit 0: `members 178, committed rows 178, declared exclusions 0` / `control swapped-value: refused (2 failure(s) ...)` / `control moved-anchor: refused (1 failure(s) ...)` / `known answer 00597690: anchor 005976D0 references 00D24880 in its raw bytes = committed value` / `FAILS 0`.
  - The text is identical to the committed `fam_rows_check.out`. Only the line endings differ (CRLF on checkout).
- **What the checker tests.** `ex_named_call` (target `00632D80`, reg `r8`, size_reg `r9d`) decodes the census extent from `check_dispositions.load_functions()`. It requires exactly one `call 00632D80`. In the ten instructions before that call, it takes the last `lea r8` (whose target must be a clean C string) and the last `mov r9d, imm`. It compares all six columns with `rows.tsv`. It does not test the five-call order, the vtable store, the `+0xFC` bit or the stack arguments that the lead describes.
- **Controls' sensitivity.** The controls now pass mutated copies of the committed rows through the same `compare()` against the image derivation, so they test the comparison, not the extractor.
  - **T6:** an image-blind extractor that echoes `rows.tsv` still printed both controls "refused" and FAILS 0, loaded in memory. The known-answer line also passed, because it recomputes only row 0, and the echoed row 0 is correct. So the controls cannot detect a broken extractor. The known answer covers one row.
  - The comparison itself is sensitive. In-memory mutations of row 89 (`00644BA0` "PMLAABase") each failed:
    - value swapped with row 90: FAILS 2
    - name changed: FAILS 1
    - size 0xB0 -> 0xB4: FAILS 1
    - anchor + 1: FAILS 1
    - row deleted: FAILS 1
  - Not a defect here, because the independent census below re-derives all 178 rows.
- **Independent census.** This used the disw.py image reader over the `graph/functions.tsv` extents, not retool or fam_rows. Operands were masked where they are rip-relative targets or the `mov r9d` immediate.
  - **All 178 members are 152 B with the same 33-instruction skeleton.** Every member's call sequence is exactly `006373D0, 00632D80, 0063DC80, 0063DF90, 0063DFA0` (178 of 178).
  - The positions that vary across the family are:
    - `+0x1E` `mov dword [rsp+0x30], imm` (7th argument): 0 or 8, 2 values
    - `+0x26` `lea rax, [P]`, stored to `[rsp+0x28]` (6th argument): 101 distinct. Where P resolves through the static-initialiser rows, it is the base class's descriptor: 106 of 178, for example PComponent for PAnimatableComponent and PAnimationChannelBase for PAnimationChannel.
    - `+0x32` `mov dword [rsp+0x20], imm` (5th argument): 2, 4, 8 or 0x10
    - `+0x3A` `mov r9d, size`: 37 distinct
    - `+0x40` `lea r8, [S]`: **178 distinct**
    - `+0x50` `lea rax, [V]`, then `mov [rbx], rax`: **178 distinct**
    - `+0x61`, `+0x70` and `+0x7F`, the `lea rdx` argument of each registration helper: **178 distinct each**
  - The vtable stored at `+0` is `PClassDescriptorAbstract<T>` in **178 of 178**, read from the MSVC RTTI complete-object locator at V-8. T equals the row's class name in **178 of 178**. The concrete vtable is stored later by the static initialiser, as the page's own sections state at line ~3811 and in the "PClassDescriptorConcrete static initialisers" lead.
  - `or dword [rbx+0xFC], 2` is in the shared skeleton of all 178.
- **All rows re-derived independently.** Method: for each member, take the last `lea r8` before its one `call 00632D80`, the C string at the target, and the last `mov r9d` immediate. **178 of 178 rows are identical** to `rows.tsv` (anchor, value, name and size), with 178 distinct values.
- **Installed page table.** The 178 rows under "All 178 constructors (OPUS)" are set-equal to `rows.tsv` (member, anchor, S, name/size).
- **Sampled rows, from raw bytes without capstone.** The 15 spread rows were 0-based indices 0, 13, 25, 38, 51, 63, 76, 88, 101, 114, 126, 139, 152, 164 and 177.
  - Each anchor sits at entry + 0x40 and its bytes are `4C 8D 05 rel32`. The rel32 resolves to the row's S, and the C string at S is the row's name.
  - The 6 bytes before each anchor are `41 B9 imm32`, which is the row's size.
  - Anchor + 10 is `E8 rel32` -> `00632D80`.
  - Examples: `00597690` -> `00D24880` "PClusterHeader" 0x54, `00614EF0` -> `00D50A70` "PShaderPassD3D11" 0x2C0, `008758B0` -> `01CD7900` "PVisionTrackerWin32" 0x8.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. The extractor decodes the census extent, and the `lea r8` is always two instructions before the call, well inside the ten-instruction look-back. Defect (b), exclusions caused by a fixed byte window, cannot arise.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors the `lea r8, [S]` at + 0x40, which distinguishes the member, since S is unique.
  - Each row states S, the string and the size, all read from the image.
  - The committed checker derives every row and refuses a swapped value.
  - **Conditions met.** The other distinguishing instructions (the vtable and the three `lea rdx`) are not anchored, which the rule does not require.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the installed page section.** Replace:

> passes its result to the shared descriptor constructor `00632D80` with the class name in `r8`, the instance size in `r9d` and a descriptor pointer as a stack argument, stores the concrete vtable at qword `+0`, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers `0063DC80`, `0063DF90` and `0063DFA0` (all 178 members make exactly these five calls, in this order). What differs from member to member is the name and size it passes.

with:

> passes its result to the shared descriptor constructor `00632D80` with the class name in `r8`, the instance size in `r9d` and three stack arguments (a dword at `[rsp+0x20]`, a descriptor pointer at `[rsp+0x28]` and a dword at `[rsp+0x30]`), stores its own `PClassDescriptorAbstract<T>` vtable at qword `+0`, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers `0063DC80`, `0063DF90` and `0063DFA0`, each with its own `lea rdx` argument (all 178 members are 152 B and make exactly these five calls, in this order). What differs from member to member is the name and size it passes, the two stack dwords (at + 0x1E and + 0x32), the descriptor pointer (+ 0x26), the vtable it stores (+ 0x50), and the three `lea rdx` arguments (+ 0x61, + 0x70 and + 0x7F). The name, the vtable and the three `lea rdx` arguments are unique to each member. The rows anchor the name `lea`; they do not state the others.

**Notes (non-blocking):**
- **Control repair.** The controls test the comparison, not the extractor. To make the extractor side fail when it should, extend the raw-byte known answer from row 0 to every row: `_raw_ref(anchor) == value`, and `41 B9 imm32` at anchor-6 == size.
- **Checker scope.** The checker does not test the shared-form claims of the lead (five calls in order, the vtable store, the `+0xFC` bit). They hold today (census above). A form assertion in `ex_named_call` would keep them true under membership changes.
