# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-base-aware-ctors-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-BASE-AWARE-CTORS-1003` · Package: `_index/candidates/opus-ee-base-aware-ctors-1003/` (rows committed in `937343614`, reviewed at HEAD `8fabf1300`; the package is unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 132 rows are correct against the bytes. The lead says members differ only in the name and size they pass, but they differ at six instructions and three stack arguments. The narrowing below corrects that sentence. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.**
  - The analysis venv python lacks `pefile`, which `fam_rows.py` imports for `.rdata` reads. `named_call` does not need it, but the module is shared, so check was run under `C:\Python314\python.exe` (3.14.6). Check mode writes nothing, so it was run in place with `-B`.
  - Exit 0: `members 132, committed rows 132, declared exclusions 0` / `control swapped-value refused, control moved-anchor refused` / `FAILS 0`. The output is identical to the committed `fam_rows_check.out`.
- **What the checker tests.** `ex_named_call` decodes the census extent. It requires exactly one `call 0x632d80`, takes the nearest `lea r8, [S]` and `mov r9d, imm` in the ten instructions before it, and requires a clean C string at S. It compares all six columns with `rows.tsv`, fails a missing row or a non-member row, and requires the anchor to be strictly inside the body.
- **Controls' sensitivity: the printed controls are tautologies.** The control code is the same as in the return-value and input-name packages.
  - `ok1` compares row 0's extracted value with a row chosen because its value differs. `ok2` compares an anchor with that anchor + 1. Neither passes anything through the row comparison.
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, the committed `cmd_check`, loaded in memory, still printed both controls "refused" and FAILS 0.
  - The comparison itself is sensitive. In-memory mutations of row 66 (`006625D0`) each failed: value swapped with row 67 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
- **Independent census** (disw.py image reader over `graph/functions.tsv` extents; not retool and not fam_rows).
  - All 132 members are 163 bytes. Masking rip targets, branch targets and immediates leaves **one** form of 36 instructions.
  - Across the 132, the positions that vary are:
    - `+0x2B` `mov dword [rsp+0x30], imm`: 3 values;
    - `+0x38` `mov dword [rsp+0x20], imm`: 5 values;
    - `+0x40` `mov r9d, size`: 33 values;
    - `+0x46` `lea r8, [S]` (the anchor): 132 distinct;
    - `+0x56` `lea rax, [V]`, the vtable stored to `[rdi]`: 132 distinct;
    - `+0x67`, `+0x76` and `+0x85` `lea rdx, [...]`, the arguments to `0063DC80`, `0063DF90` and `0063DFA0`: 132 distinct at each.
- **All rows re-derived independently.** All 132 rows were recomputed with the independent reader: the `lea r8` before the one `call 00632D80`, the string at its target, and the `mov r9d` immediate. **132 of 132 are identical** to `rows.tsv`. The values are unique (132), and so are the names (132).
- **Sampled rows.** 15 spread rows were inspected by hand at 0-based indices 0, 9, 19, 28, 37, 47, 56, 66, 75, 84, 94, 103, 112, 122 and 131. In each, the anchor is the `lea r8` at entry + 0x46, and the string and size match the row. Examples: `00597776` -> `00D244A8` "PClusterHeaderBase" with r9d 0x48, `006CFF56` -> "PModifierNetworkInfoPacket_ModifierCode" with 0x20, and `00879A76` -> `01CD9A50` "PGameConfig" with 0x18.
  - Cross-check: in all 15, the RTTI locator before the stored vtable V at + 0x56 names `PClassDescriptorAbstract<that class>`. For example, `00D245C8` names `.?AV?$PClassDescriptorAbstract@VPClusterHeaderBase@PBinary@PSerialization@Phyre@@@Phyre@@`.
  - **15 of 15 exact.**
- **Excluded sample.** `excluded.tsv` is empty, so there was nothing to sample. The window defect (b) cannot occur here: the extractor decodes the census extent, not a fixed window.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction unique to the member, the `lea r8` class-name argument.
  - Each row states member-specific values from the image: S, its string, and the size.
  - The checker derives every row and refuses a swapped value, through the comparison loop.
  - **Conditions met.**

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the page section.** Replace:

> It calls the two context getters, passes them to the shared descriptor constructor `00632D80` with the class name in `r8` and the instance size in `r9d`, stores the concrete vtable, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers. What differs from member to member is the name and size it passes.

with:

> It calls the two context getters, passes them to the shared descriptor constructor `00632D80` with the class name in `r8`, the instance size in `r9d` and two dword stack arguments, stores its own `PClassDescriptorAbstract<T>` vtable, sets bit `0x2` of dword `+0xFC`, and calls the three member-registration helpers `0063DC80`, `0063DF90` and `0063DFA0`, each with its own `lea rdx` argument. What differs from member to member is the name and size it passes, the two stack dwords (at + 0x2B and + 0x38), the vtable it stores (+ 0x56), and the three `lea rdx` arguments (+ 0x67, + 0x76 and + 0x85). The rows anchor the name `lea`; they do not state the others.

**Notes (non-blocking):**
- **Control repair.** Make the two controls pass mutated copies of `rows.tsv` (a swapped value and a moved anchor) through the same comparison, and assert FAILS > 0. Add one known-answer row recomputed from raw bytes, so that an extractor which stops reading the image fails. Today's controls cannot fail while the extractor returns anything at all. This applies to every package that shares this `fam_rows.py`.
- **Reproducibility.** Add `pefile` to the analysis venv, or say in the README that check needs an interpreter with pefile.
- The members TSV header says "133 members"; its rows and the frontmatter give 132.
