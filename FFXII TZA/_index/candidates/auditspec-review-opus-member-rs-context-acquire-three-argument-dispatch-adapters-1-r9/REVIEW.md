# SWE2-AUDIT-SPEC review: OPUS member rows (opus-member-rs-context-acquire-three-argument-dispatch-adapters-1-r9)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request; not OPUS, not the drafting agent) · 2026-10-03 · at HEAD `f94b97dcdcf43ed5ff55d4b644cf073a02534e74` (measured first at `74030b6bc`; no input changed between the two) · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-RS-CONTEXT-ACQUIRE-THREE-ARGUM-4A870` · Package: `_index/candidates/opus-member-rs-context-acquire-three-argument-dispatch-adapters-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`, block "Family members explained one by one: context-acquire three-argument dispatch adapters (OPUS, 2026-10-03, ...)", committed in bde699a66. The page is unchanged from that commit to HEAD, and the working tree is clean for it.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 70 rows are exact at the bytes, sentence and anchors alike, and no row text changes. The narrowing is to the package's crediting claim only. The rows credit engine_explained today by the base rule. On this page, which declares their family, the adopted ruling `opus-ee-rulings-1003` §1 makes a member's credit depend on a committed checker that refuses a swapped value. The package ships no such checker, and its applier passes a swapped sentence. See the crediting section for the replacement README text and the route.

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply` and printed `VERIFY 70 functions, 280 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. All 70 row texts appear verbatim in the page block.
- **Applier control (planted defect).** An unmodified scratch copy of the applier (only its DB root pinned) was run on a scratch `rows.json` with three mutations: `005C7E20`'s first anchor relabelled `nop`, `0060B690`'s last anchor moved onto the entry, and a pipe added to `0087A7B0`'s text. It printed exactly those three `VERIFY FAIL` lines, then `FAILS 3`, and exited 1. The page was untouched.
- **Population.** 70 rows and 70 distinct functions. They equal the 70 members that the page's `function_families` entry declares (`members/context-acquire-three-arg-dispatch-adapters.tsv`): no row is a non-member and no member lacks a row. README: rejected 0, skipped 0, missing 0, corrections none.
- **Image.** `rvlib.Img` (sha-checked shipping `FFXII_TZA.exe`, sha256 `73461d08...`, base 0x00120000, section-aware offsets). For all 70 bodies the `functions.tsv` size (47 B) equals the `.pdata` extent, and the decode covers it exactly. No body has an indirect jump, so there is no jump table.

### SWE2-AUDIT-SPEC: the representative, read in full (`005C7E20`, 47 B, `.pdata` `005C7E20..005C7E4F`)

The body runs from `mov [rsp+8], rbx` / `push rdi` / `sub rsp, 0x20` to the tail jump at `005C7E4A`, followed by `int3` padding. Clause by clause:
- "calls `005B4E00` with 0 in `ecx`": `xor ecx, ecx` (`005C7E2A`), then `call 005B4E00` (`005C7E32`, anchor). Before the call, `mov rbx, r8` and `mov rdi, rdx` save the incoming values. `rdx` and `r8` still hold them at the call. The row says nothing about them, so this is no defect.
- "the return value in `r8`": `mov r8, rax` (`005C7E37`, anchor).
- "`r8` as received in `rdx`": `mov rdx, rbx` (`005C7E3A`).
- "`rdx` as received in `rcx`": `mov rcx, rdi` (`005C7E3D`, anchor).
- "tail-jumps to `00684080`": the frame is restored (`mov rbx, [rsp+0x30]`, `add rsp, 0x20`, `pop rdi`), then `jmp 00684080` (`005C7E4A`, anchor). `00684080` is a separate 5-byte function (`jmp 00682D20`).

### SWE2-AUDIT-SPEC: every row regenerated from the bytes (mechanical, with controls)

The reviewer-written checker (scratch, independent of `interior_ingest.py` and of OPUS's verifier) checks each of the 70 members in four steps:
1. **Extent.** The `functions.tsv` size equals the `.pdata` extent, and the decode covers it exactly.
2. **Shape.** The body is normalised and must equal the hand-read representative's. Intra-body branch targets become entry-relative, direct call/jmp targets outside the body become placeholders, and rip operands become placeholders whose resolved targets are kept as fields. Every other operand stays literal, including immediates, displacements and registers. A member that put another value in `ecx`, or used other registers, would therefore differ.
3. **Sentence.** The sentence is regenerated from the member's own fields (its direct targets, in order) and must equal the row's text character for character.
4. **Anchors.** The anchors are regenerated as (address, mnemonic) at the representative's anchor indices (`call` / `mov` / `mov` / `jmp`) and must equal the row's anchors exactly.

**Result: 70 / 70 OK, bad 0.**
- Every member is 47 B.
- All 70 tail-jump to `00684080`.
- The called getter is member-specific: 70 distinct targets, from `005B4E00` through `00879EC0`, each stated in its own row.
- No member has a rip operand. The CURRENT `tdiff.py` concern (differing static cells) does not arise in this form.

**Controls (in memory, against the same checker):**
- (T) one hex digit of `005C7E50`'s tail-jump target changed (`00684080` -> `00684081`);
- (A) `0060B690`'s second anchor moved to the next instruction boundary, a valid-looking `mov`;
- (M) `0087A7B0`'s first anchor relabelled `nop`;
- (S) the sentences of `005C7E80` and `005C7EB0` swapped, so each states the other member's real getter.

The checker refused exactly those five rows and no other (`planted 5, flagged 5`).

**Byte control:** `005C7E50`'s `xor ecx, ecx` was patched to `mov cl, 1` in a patched image copy. The member was refused (shape differs: `mov cl, 1` against `xor ecx, ecx`).

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 sections 1 and 2; auditspec-ruling-scoped-ee-row-1003)

This was measured with `progress.py`'s own helpers at HEAD (`evidence_bearing`, `index_only_headings`, `strip_index_only`, `family_rule_inputs`, `cite_credits`, `doc_credits`) and `check_dispositions` (`accepted_families`, `evaluate`), with no reimplementation.

- **Section 2 (index-only rows).** The page is evidence-bearing and declares no `ee_index_only` heading. These rows state what each body does, so they are not index rows. Section 2 is satisfied.
- **Measured credit.** All 70 credit engine_explained, and only through this block:
  - with the block removed, the page credits 0 of the 70;
  - no other page credits any of them;
  - `doc_credits` puts all 70 in the plain set (template 0, scoped 0);
  - `check_dispositions.evaluate` puts 70 / 70 in `a_set` and `explained_set` and none in `frontier_set`.

  The bodies are 47 B, so each row's entry cite in the function column credits by size alone, as do its interior anchors.
- **Section 1 (explained-once families): the condition is not met.**
  - This page declares `context-acquire three-argument dispatch adapters` (letter C, 70 members, "PROVED BY FORM - ... ONE byte image across all 70"). That is a shape family whose shared form is explained once on its declaring page, which is the case §1 governs. On that page a member counts only when:
    - the citation anchors its distinguishing instruction;
    - the citation states its value;
    - **a committed checker derives every row of the family from the image and refuses a swapped value.**
  - The first two conditions hold. The `call` anchor at entry+0x12 is the distinguishing instruction, and each row names its own getter.
  - The third does not. The package commits only `interior_applier.py`, which checks anchor boundaries, mnemonics and pipes.
  - Measured: an unmodified scratch copy of the applier, run on a `rows.json` in which `005C7E80` and `005C7EB0` exchanged sentences, printed `VERIFY 70 functions, 280 anchors` / `DRY (block differs from rows.json; --apply rewrites it)` / `FAILS 0`, exit 0. It would publish the swap.
  - `progress.py` credits the 70 anyway because `family_rule_inputs` only puts a family in scope when the declaring page carries committed checker rows (`rows.tsv` / `accessor_desc.json`) for one of its members. This family has none (in scope: False; checker-anchored members: 0). The scorer's scope note defers unmarked shape families to `SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`.
  - The credit therefore rests on that scope gap, not on the ruling. It lapses for all 70 once the family is marked, unless a checker is committed.
- **Scoped-row ruling.** No row opens with `Scope:` or carries `scoped row: set-exact`. The ruling sets no condition here.

**Narrowing (exact wording).** In the package README, replace "All 70 rowed functions now measure A." with:

> All 70 rowed functions measure A under `progress.py` at HEAD by the base rule (47-byte bodies, credited only by this block). The family-declaring-page rule (`opus-ee-rulings-1003` §1) does not reach them yet because no committed checker carries rows for this family; under that ruling the credit needs a committed checker that derives every row from the image and refuses a swapped value, which `interior_applier.py` does not do. Until one is committed, the credit is provisional and lapses when the family is marked as a shape family (`SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`).

**Route (OPUS).** Commit a checker for this family in the accepted shape (`fam_rows.py` + `spec.json` + `rows.tsv`, page = this page). Its rows should anchor the distinguishing `call` at entry+0x12 and state the getter, and it needs a swapped-value control. The reviewer's checker above meets that bar and can serve as its basis. With it, the narrowing lifts, and the credit becomes ruling-backed through the `call` anchors.

- Limits: static evidence only. These are body statements, not meanings: the review does not test the family name or what `00684080` and the getters do with the values passed. The drafting agent's draft and OPUS's re-read are not independent review; this record is. The reviewer's scripts (representative dump, template checker with text/anchor/swap/byte controls, applier and swap controls, crediting script) live in a private scratch folder and are not committed.
