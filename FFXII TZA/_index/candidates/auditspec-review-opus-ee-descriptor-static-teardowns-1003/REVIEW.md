# SWE2-AUDIT-SPEC review: OPUS template-family rows (opus-ee-descriptor-static-teardowns-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-EE-DESCRIPTOR-STATIC-TEARDOWNS-1003` · Package: `_index/candidates/opus-ee-descriptor-static-teardowns-1003/` (rows committed in `4523bdf31`, package last changed in `c480be543`, reviewed at HEAD `33eb7192f`; the package and its members file are unmodified in the working tree) · Page: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` (section "Per-member rows: the class descriptor each of the PClassDescriptor static teardowns loads")

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 311 rows are correct against the bytes. All 93 exclusions are real refusals of the naming method, not checker artefacts. One lead sentence is wrong, though: "What differs from member to member is the class descriptor X". Every member also differs at its **entry instruction**, `lea rax, [V]`. V is the member's own `PClassDescriptorForType<T>` vftable, and the 404 members have 404 distinct V. This is defect pattern (a). The narrowing below corrects the lead. No row changes.

## SWE2-AUDIT-SPEC checks

- **Checker re-run.** `fam_rows.py check` was run in place with `-B` under `C:\Python314\python.exe` (which has capstone and pefile). Check mode writes nothing.
  - Exit 0: `members 404, committed rows 311, declared exclusions 93` / `control swapped-value: refused (2 failure(s) from the comparison)` / `control moved-anchor: refused (1 failure(s) from the comparison)` / `known answer 008A8E20: anchor 008A8E27 references 02CAD140 in its raw bytes = committed value` / `FAILS 0`.
  - The output matches the committed `fam_rows_check.out`; the only difference is line endings (CRLF in the committed file).
- **What the checker tests.**
  - `ex_descriptor_lea` (reg `rcx`, `same_target_ok`) decodes the census extent and requires exactly one `lea rcx` target.
  - `_descriptor_name` names X through every `lea rcx, [X]` that a direct `call` follows. It then reads that wrapper's `lea r8` among the 10 instructions before its one `call 00632D80`.
  - It compares all six columns with `rows.tsv`. It does not check `lea rax, [V]`, the store or the `jmp 00633390`.
- **Controls' sensitivity.**
  - **T6:** with an image-blind extractor that echoes `rows.tsv`, monkeypatched in memory, `cmd_check` still printed both controls "refused" and FAILS 0. The swapped-value and moved-anchor controls test only the comparison.
  - The new raw-byte **known answer** is image-anchored. When the echoed rows and the committed row 0 both carried a wrong value, it printed `known answer 008A8E20: FAIL` (FAILS 2). It covers one row.
  - The comparison itself is sensitive. In-memory mutations of row 155 (`008B0310`) each failed: values swapped with row 156 (FAILS 2), name changed (FAILS 1), anchor + 1 (FAILS 1), row deleted (FAILS 1).
  - **Gap:** an invented row for a declared-excluded member passes with FAILS 0, because `compare` does `continue` for any entry in `excluded.tsv` without checking for a committed row. The test row was `008A9570 / 008A9577 / lea / 02CB3B50 / PInventedClass`. Today `rows.tsv` and `excluded.tsv` are disjoint (311 + 93 = 404 = members), so no current row is affected. See the notes.
- **Independent census.** The census used the disw.py image reader over the `graph/functions.tsv` extents, not retool or fam_rows.
  - All 404 members are 26 B and mask (rip operands masked, call/jmp targets kept) to **one** form: `lea rax, [V] / lea rcx, [X] / mov qword ptr [X], rax / jmp 00633390`.
  - In all 404, the store target equals the `lea rcx` target.
  - **V has 404 distinct values**, and X has 311 distinct values among the rows. Each member therefore differs at two operands: V at entry + 0 and X at entry + 7 (and in the store's displacement at + 0xE, to the same X).
  - Sampled V's RTTI (COL at `[V-8]`) is `PClassDescriptorForType<T>`, for example `00D29A38` -> `PClassDescriptorForType<PAnimatableComponent>`.
- **All rows re-derived independently.**
  - Method: a raw-byte `48 8D 0D rel32` + `E8 rel32` index finds the initialiser that loads X. The wrapper's `lea r8` before its one `call 00632D80` gives the name.
  - **311 of 311 rows are identical** to `rows.tsv` (anchor, value, name), with 311 distinct values.
  - **Second, independent route:** the template argument of each row's V RTTI type name equals the row's class name in **311 of 311** rows, and all 311 are `PClassDescriptorForType`.
- **Sampled rows.** 16 spread rows were inspected with `disr.py`, at 1-based rows 1, 23, 45, ... 309 and 311: `008A8E20`, `008A90E0`, `008AAFD0`, `008AB290`, `008AB550`, `008AE7D0`, `008B0030`, `008B02F0`, `008B0DE0`, `008B27D0`, `008B2A90`, `008B5800`, `008B71D0`, `008B93A0`, `008BDD60` and `008C14E0`.
  - In each, the anchor is entry + 7 (`lea rcx`) and its target is the row's X. For example, `008B02F7` -> `02D35500` PScreenSpaceAmbientOcclusionD3D11, and `008C14E7` -> `02EB9E60` PGameConfig.
  - **16 of 16 exact.**
- **Excluded sample and window check (defect b).** All 93 have a single X, and none has a wrapper that calls `00632D80`, so the 10-instruction window never decides an exclusion.
  - **84** have no `lea rcx, [X]` + direct-call site anywhere.
    - `008A9570` (X `02CB3B50`) was read in full. X is a function-local static, built inline in `005B4E00` under `_Init_thread_header`: `lea rsi, [X]` ... `mov r8, rdi` (rdi loaded from `[02CB5BC8]`) / `mov rcx, rsi` / `call 00632D80`. The name is a runtime-loaded pointer, not a static string.
    - `008A9590`, `008A95B0`, `008A95D0` and `008A95F0` show the same reference pattern: one `lea rsi`, two vftable stores, and an unwind `lea rcx, [X]; jmp <dtor>`.
  - **9** (`008AF090`-`008AF190`) have `lea rcx, [X]; call` sites. Every callee is something other than a `00632D80` wrapper (`00631A60`-class getters, `006388C0`, `005A7A40`, `0063BC00`), with zero calls to `00632D80`.
  - Reason text "descriptor not named by exactly one class (0)" is accurate for all 93.
- **Rule check (opus-ee-rulings-1003 §1).**
  - Each row anchors an instruction that distinguishes the member: the `lea rcx`, whose X is unique.
  - Each row states X and its class, read from the image.
  - The checker derives every row and refuses a swapped value.
  - **Conditions met.** The rule does not require the anchor to be the only distinguishing instruction. Only the lead's description of what differs is wrong.
- **Page frontmatter and census row** say "mask to ONE distinct byte image" and give the 26 B shape `lea rax, [vftable] ; lea rcx, [static object] ; mov [static object], rax ; jmp 00633390`. The census confirms this.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing: the lead, in spec.json `lead` and the page section.** Replace:

> shares one shape, stated here once and not repeated per row: each loads its class descriptor X into rcx, stores a vtable pointer at qword [X] and tail-jumps to the descriptor destructor 00633390. What differs from member to member is the class descriptor X its `lea rcx, [X]` loads (every load of it in the body names the same X). Each row anchors the first such `lea`, the member's distinguishing instruction,

with:

> shares one 26-byte shape, stated here once and not repeated per row: `lea rax, [V]` / `lea rcx, [X]` / `mov qword ptr [X], rax` / `jmp 00633390`, which resets the static descriptor X to its own `PClassDescriptorForType<T>` vftable V and tail-jumps to the descriptor destructor. Members differ at two values: V (the entry instruction) and the class descriptor X (the `lea rcx` and the store, which name the same X). Each row anchors the `lea rcx, [X]`, a distinguishing instruction,

**Notes (non-blocking):**
- **Checker gap.** In `compare`, an entry listed in `excluded.tsv` that also has a committed row should FAIL. Today it is skipped, and an invented row passes with FAILS 0. This is the same shared `fam_rows.py`, so the sibling packages inherit the gap.
- **Controls.** The swapped-value and moved-anchor controls still cannot fail under an extractor that echoes `rows.tsv`. Only the known answer, for row 0, is image-anchored. Extend the known answer to every row's value (cheap: `_raw_ref` per anchor), or to a spread sample.
- **Possible re-earning.** For the 93 exclusions, V's RTTI type name names the class directly (for example `008A9570`: V `00D32DD0` = `PClassDescriptorForType<PArray<uint,3>>`). A V-RTTI naming route could give rows to members that the initialiser route cannot name. Any such row would need its own uniqueness check.
