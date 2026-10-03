# SWE2-AUDIT-SPEC review: OPUS member rows (opus-member-ors-member-vcall-optional-pointer-dispatch-adapters-1-r9)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request; not OPUS, not the drafting agent) · 2026-10-03 · at HEAD `f94b97dcdcf43ed5ff55d4b644cf073a02534e74` (measured first at `74030b6bc`; no input changed between the two) · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ORS-MEMBER-VCALL-OPTIONAL-POIN-98E12` · Package: `_index/candidates/opus-member-ors-member-vcall-optional-pointer-dispatch-adapters-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`, block "Family members explained one by one: member-vcall optional-pointer dispatch adapters (OPUS, 2026-10-03, ...)", committed in bde699a66. The page is unchanged from that commit to HEAD, and the working tree is clean for it.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 12 rows are exact at the bytes, sentence and anchors alike, and no row text changes. Every member's own getter and static cell is stated correctly, including the members whose static differs from the common `02E404B0`. The narrowing is to the package's crediting claim only: ruling `opus-ee-rulings-1003` §1 needs a committed checker that refuses a swapped value on the family's declaring page, and this package has none. One optional anchor note follows. It does not block.

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply` and printed `VERIFY 12 functions, 60 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. All 12 row texts appear verbatim in the page block.
- **Applier control (planted defect).** An unmodified scratch copy (DB root pinned) was run with three mutations: `005FFA10`'s first anchor relabelled `nop`, `006AC4F0`'s last anchor moved onto the entry, and a pipe added to `0079AA50`'s text. It printed exactly those three `VERIFY FAIL` lines, then `FAILS 3`, and exited 1. The page was untouched.
- **Population.** 12 rows and 12 distinct functions. They equal the 12 declared members (`members/member-vcall-optptr-dispatch-adapters.tsv`). README: rejected 0, skipped 0, missing 0, corrections none.
- **Image.** `rvlib.Img` (sha-checked, base 0x00120000, section-aware). For all 12 bodies the `functions.tsv` size (119 B) equals the `.pdata` extent, and the decode covers it exactly. Each body has three `ret`s, the last at entry+0x76, followed by `int3` padding. The one indirect transfer is `call qword ptr [rdi+8]`. There is no indirect jump and no jump table.

### SWE2-AUDIT-SPEC: the representative, read in full (`005FFA10`, 119 B, `.pdata` `005FFA10..005FFA87`)

- "`f` = `rcx` and `c` = `rdx`": `mov rdi, rcx` / `mov rbx, rdx`.
- "`o` = `005F86B0(c)`": `mov rcx, rdx` / `call 005F86B0` (`005FFA23`, anchor).
- "returns 0 when `o` is null": `test rax, rax` / `je 005FFA7C`. That path only restores the frame and executes `ret` with `rax` = `o` = 0.
- "`v` = the pointer at qword [f+8] called with `o`": `mov rcx, rax` / `call qword ptr [rdi+8]` (`005FFA30`, anchor). This is a function pointer stored in `f`, not a vtable slot. The row says "the pointer at qword [f+8]", which is exact.
- "when `v` is non-null calls `00684080(c, v, 02CB7080)`":
  - `mov rcx, rbx` (c, on both paths), then `test rax, rax` / `je 005FFA5A`;
  - fallthrough: `lea r8, [rip+0x26b763e]` (`005FFA3B`, anchor) resolves to `02CB7080` in `.data`;
  - then `mov rdx, rax` and `call 00684080` (`005FFA45`, anchor).
- "else `0080F420(c, 1)` and `00810620` with `c` in `rcx`": at `005FFA5A`, `mov edx, 1` / `call 0080F420` / `mov rcx, rbx` / `call 00810620`. Both are calls, not tail jumps, and the row's verb "calls" covers both.
- "returns 1": `mov eax, 1` on both the non-null path (`005FFA4A`) and the null-`v` path (`005FFA6C`), then frame restore and `ret`. The anchor `005FFA58` is the non-null path's `pop rdi`.

The row is exact.

### SWE2-AUDIT-SPEC: every row regenerated from the bytes (mechanical, with controls)

The checker is the same reviewer-written one as this batch's sibling reviews:
1. **Extent.** The size equals the `.pdata` extent.
2. **Shape.** The normalised shape equals the representative's, with every non-target operand literal, including the `[rdi+8]` slot and both `mov eax, 1`.
3. **Sentence.** The sentence is regenerated from the member's four direct targets and its **resolved** `lea r8` target (resolved-target comparison, as in the CURRENT `tdiff.py`; the target must lie in `.data`). It must equal the row character for character.
4. **Anchors.** The anchors are regenerated at the representative's indices (`call` / `call` / `lea` / `call` / `pop`) and must equal the row's.

**Result: 12 / 12 OK, bad 0.** All 12 bodies are 119 B. All 12 use `00684080`, `0080F420` and `00810620`. The member-specific values, each stated correctly in its own row:
- **Getter:** 10 distinct targets. `005FFA10` and `005FFA90` both call `005F86B0`, and `0079A9D0` and `0079AA50` both call `00796960`.
- **Static:** 5 distinct cells. Eight members pass `02E404B0`. The four that differ are `005FFA10` (`02CB7080`), `006AB090` (`02E4EAF0`), `0079A9D0` (`02EA9400`) and `0079AA50` (`02CF8A80`). Each of those rows states its own cell.
- **Distinctness:** no single instruction distinguishes every member, but the (getter, static) pair is unique to each of the 12. Each row anchors both the getter `call` and the `lea r8`.

**Controls:**
- (T) `005FFA90`'s `00810620` changed to `00810621`;
- (A) `006AC4F0`'s second anchor moved to the next boundary (a valid `mov`);
- (M) `0079AA50`'s first anchor relabelled `nop`;
- (S) the sentences of `00678F10` and `006A12B0` swapped, so each names the other's getter.

The checker refused exactly those five rows (`planted 5, flagged 5`).

**Byte control:** `005FFA90`'s `call qword ptr [rdi+8]` was patched to `[rdi+0x10]`. The member was refused (shape differs).

**Optional anchor note (non-blocking).** Each row's fifth anchor is the epilogue `pop rdi` at entry+0x48 (for example `005FFA58`). It is a valid interior boundary and credits correctly. The instruction that performs the row's "returns 1" is `mov eax, 1` at entry+0x3A, which is `005FFA4A`, `005FFACA`, `00678F4A`, `006A12EA`, `006A8D4A`, `006AB0CA`, `006AC52A`, `006BFD9A`, `006C753A`, `006C868A`, `0079AA0A` and `0079AA8A` (all twelve confirmed to decode as `mov eax, 1`). The sibling static-descriptor package applied the same kind of epilogue-to-operative move (README correction). OPUS may do the same here, with the recorded mnemonic `mov`.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 sections 1 and 2; auditspec-ruling-scoped-ee-row-1003)

This was measured with `progress.py`'s own helpers at HEAD and `check_dispositions`.

- **Section 2.** The page is evidence-bearing with no `ee_index_only`, and the rows are statements about the bodies. Section 2 is satisfied.
- **Measured credit.** All 12 credit, and only through this block:
  - with the block removed, the page credits 0;
  - no other page credits any of the 12;
  - `doc_credits`: plain 12, template 0, scoped 0;
  - `check_dispositions.evaluate`: 12 / 12 in `a_set` and `explained_set`, 0 in `frontier_set`.

  The bodies are 119 B, so each row's entry cite also credits by size.
- **Section 1: the condition is not met.**
  - The page declares `member-vcall optional-pointer dispatch adapters` (letter C, "PROVED BY FORM - 12 members, all 119 bytes, ONE operand-aware byte image and ONE instruction-form skeleton"). That is a shape family explained once on its declaring page.
  - The rows anchor the distinguishing `call` and `lea` and state their values.
  - No committed checker derives every row and refuses a swapped value. Measured: the package's applier (unmodified scratch copy), run on a `rows.json` with the `00678F10` / `006A12B0` sentences exchanged, printed `VERIFY 12 functions, 60 anchors` / `DRY (block differs ...)` / `FAILS 0`, exit 0.
  - The 12 credit only because `family_rule_inputs` leaves this family out of scope (no committed checker rows; in scope: False), pending `SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`.
- **Scoped-row ruling.** No row carries `Scope:` or `scoped row: set-exact`. It does not apply.

**Narrowing (exact wording).** In the package README, replace "All 12 rowed functions now measure A." with:

> All 12 rowed functions measure A under `progress.py` at HEAD by the base rule (119-byte bodies, credited only by this block). The family-declaring-page rule (`opus-ee-rulings-1003` §1) does not reach them yet because no committed checker carries rows for this family; under that ruling the credit needs a committed checker that derives every row from the image and refuses a swapped value, which `interior_applier.py` does not do. Until one is committed, the credit is provisional and lapses when the family is marked as a shape family (`SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`).

**Route (OPUS).** Commit a `fam_rows.py` + `spec.json` + `rows.tsv` checker for this family. Each row needs both distinguishing anchors, the getter `call` (entry+0x13) and the `lea r8` (entry+0x2B), because neither alone separates all 12. The checker needs a swapped-value control.

- Limits: static evidence only, body statements not meanings. The review does not test what `00684080`, `0080F420`, `00810620` or the getters do. The draft and OPUS's re-read are not independent review; this record is. The reviewer's scripts are in a private scratch folder and are not committed.
