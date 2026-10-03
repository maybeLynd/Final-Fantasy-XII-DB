# SWE2-AUDIT-SPEC review: OPUS member rows (opus-member-ccessors-optional-pointer-context-dispatch-adapters-1-r9)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request; not OPUS, not the drafting agent) · 2026-10-03 · at HEAD `f94b97dcdcf43ed5ff55d4b644cf073a02534e74` (measured first at `74030b6bc`; no input changed between the two) · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-CCESSORS-OPTIONAL-POINTER-CONT-89658` · Package: `_index/candidates/opus-member-ccessors-optional-pointer-context-dispatch-adapters-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`, block "Family members explained one by one: optional-pointer context dispatch adapters (OPUS, 2026-10-03, ...)", committed in bde699a66. The page is unchanged from that commit to HEAD, and the working tree is clean for it.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 70 rows are exact at the bytes, sentence and anchors alike, and no row text changes. The narrowing is to the package's crediting claim only. The rows credit engine_explained today by the base rule. On this page, which declares their family, the adopted ruling `opus-ee-rulings-1003` §1 makes a member's credit depend on a committed checker that refuses a swapped value. The package ships no such checker, and its applier passes a swapped sentence. See the crediting section for the replacement README text and the route.

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply` and printed `VERIFY 70 functions, 350 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. All 70 row texts appear verbatim in the page block.
- **Applier control (planted defect).** An unmodified scratch copy (DB root pinned) was run on a scratch `rows.json` with three mutations: `005C7970`'s first anchor relabelled `nop`, `0060B1E0`'s last anchor moved onto the entry, and a pipe added to `0087A760`'s text. It printed exactly those three `VERIFY FAIL` lines, then `FAILS 3`, and exited 1. The page was untouched.
- **Population.** 70 rows and 70 distinct functions. They equal the 70 declared members (`members/optional-pointer-context-dispatch-adapters.tsv`): no extra row and no member without a row. README: rejected 0, skipped 0, missing 0, corrections none.
- **Image.** `rvlib.Img` (sha-checked, base 0x00120000, section-aware). For all 70 bodies the `functions.tsv` size (80 B) equals the `.pdata` extent, and the decode covers it exactly. Each body ends at its second tail jump, at entry+0x4B, and the next function starts at entry+0x50. No body has an indirect jump.

### SWE2-AUDIT-SPEC: the representative, read in full (`005C7970`, 80 B, `.pdata` `005C7970..005C79C0`)

- "`p` = qword [r8] (read first)": `mov rdi, qword ptr [r8]` (`005C797A`, anchor) is the first instruction after the prologue, before the call.
- "`c` = `rdx`": `mov rbx, rdx`.
- "calls `005B4E00` with 0 in `ecx`": `xor ecx, ecx`, then `call 005B4E00` (`005C7982`, anchor).
- "when `p` is non-null tail-jumps to `00684080` with (c, p, the return value)":
  - `mov rcx, rbx` is set before the test, so `rcx` = c on both paths;
  - then `test rdi, rdi` / `je 005C79A4` (`005C798D`, anchor);
  - fallthrough: `mov r8, rax`, `mov rdx, rdi`, frame restore, `jmp 00684080` (`005C799F`, anchor).
- "otherwise calls `0080F420(c, 1)` and tail-jumps to `00810620` with `c` in `rcx`": at `005C79A4`, `mov edx, 1` with `rcx` = c still set, then `call 0080F420` (`005C79A9`, anchor), `mov rcx, rbx`, frame restore, `jmp 00810620` (`005C79BB`).

The row is exact.

### SWE2-AUDIT-SPEC: every row regenerated from the bytes (mechanical, with controls)

The checker is the same reviewer-written one as the sibling review of `...context-acquire-three-argument...`. It checks each member in four steps:
1. **Extent.** The size equals the `.pdata` extent, and the decode covers it.
2. **Shape.** The normalised body must equal the representative's, with every operand literal except external targets and rip operands, whose resolved targets are kept as fields.
3. **Sentence.** The sentence is regenerated from the member's own four direct targets and must equal the row character for character.
4. **Anchors.** The anchors are regenerated at the representative's indices (`mov` / `call` / `je` / `jmp` / `call`) and must equal the row's.

**Result: 70 / 70 OK, bad 0.**
- Every member is 80 B.
- Every member uses `00684080`, `0080F420` and `00810620`.
- The getter is member-specific: 70 distinct targets, the same 70 getters as the three-argument family, each stated in its own row.
- No rip operands.

**Controls:**
- (T) `005C79C0`'s `00810620` changed to `00810621`;
- (A) `0060B1E0`'s second anchor moved to the next boundary (a valid `mov`);
- (M) `0087A760`'s first anchor relabelled `nop`;
- (S) the sentences of `005C7A10` and `005C7A60` swapped.

The checker refused exactly those five rows (`planted 5, flagged 5`).

**Byte control:** `005C79C0`'s null-path `mov edx, 1` was patched to `mov edx, 2`. The member was refused (shape differs).

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 sections 1 and 2; auditspec-ruling-scoped-ee-row-1003)

This was measured with `progress.py`'s own helpers at HEAD (`evidence_bearing`, `index_only_headings`, `strip_index_only`, `family_rule_inputs`, `cite_credits`, `doc_credits`) and `check_dispositions` (`accepted_families`, `evaluate`).

- **Section 2.** The page is evidence-bearing and declares no `ee_index_only` heading. The rows state what each body does. Section 2 is satisfied.
- **Measured credit.** All 70 credit, and only through this block:
  - with the block removed, the page credits 0;
  - no other page credits any of them;
  - `doc_credits`: plain 70, template 0, scoped 0;
  - `check_dispositions.evaluate`: 70 / 70 in `a_set` and `explained_set`, 0 in `frontier_set`.

  The bodies are 80 B, so the entry cite in each row credits by size alone.
- **Section 1: the condition is not met.**
  - The page declares `optional-pointer context dispatch adapters` (letter C, 70 members, "PROVED BY FORM - 70 members, all 80 bytes, ONE byte image across all 70"). That is a shape family explained once on its declaring page.
  - The first two conditions hold. The `call` anchor at entry+0x12 is the distinguishing instruction, and each row names its getter.
  - The checker condition is not met. The package commits only `interior_applier.py`.
  - Measured: an unmodified copy run on a `rows.json` in which `005C7A10` and `005C7A60` exchanged sentences printed `VERIFY 70 functions, 350 anchors` / `DRY (block differs ...)` / `FAILS 0`, exit 0.
  - `progress.py` credits the 70 because this family has no committed checker rows (in scope: False; checker-anchored members: 0), and unmarked shape families wait on `SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`. The credit rests on that scope gap, not on the ruling.
- **Scoped-row ruling.** No row carries `Scope:` or `scoped row: set-exact`. It does not apply.

**Narrowing (exact wording).** In the package README, replace "All 70 rowed functions now measure A." with:

> All 70 rowed functions measure A under `progress.py` at HEAD by the base rule (80-byte bodies, credited only by this block). The family-declaring-page rule (`opus-ee-rulings-1003` §1) does not reach them yet because no committed checker carries rows for this family; under that ruling the credit needs a committed checker that derives every row from the image and refuses a swapped value, which `interior_applier.py` does not do. Until one is committed, the credit is provisional and lapses when the family is marked as a shape family (`SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`).

**Route (OPUS).** Commit a `fam_rows.py` + `spec.json` + `rows.tsv` checker for this family. Each row should anchor the distinguishing `call` at entry+0x12 and state the getter, and the checker needs a swapped-value control. The narrowing then lifts.

- Limits: static evidence only, body statements not meanings. The draft and OPUS's re-read are not independent review; this record is. The reviewer's scripts are in a private scratch folder and are not committed.
