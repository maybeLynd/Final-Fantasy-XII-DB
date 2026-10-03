# SWE2-AUDIT-SPEC review: OPUS member rows (opus-member-ontext-dispatch-adapters-static-descriptor-spelling-1-r9)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request; not OPUS, not the drafting agent) · 2026-10-03 · at HEAD `f94b97dcdcf43ed5ff55d4b644cf073a02534e74` (measured first at `74030b6bc`; no input changed between the two) · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-ONTEXT-DISPATCH-ADAPTERS-STATI-C470F` · Package: `_index/candidates/opus-member-ontext-dispatch-adapters-static-descriptor-spelling-1-r9/` · Page: `22-Middleware-PhyreEngine/Script-Object-Accessors/phyre-script-object-accessors.md`, block "Family members explained one by one: optional-pointer context dispatch adapters, static-descriptor spelling (OPUS, 2026-10-03, ...)", committed in bde699a66. The page is unchanged from that commit to HEAD, and the working tree is clean for it.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 rows are exact at the bytes, sentence and anchors alike, and no row text changes. Every member's own static cell and tail-jump target is stated correctly. The narrowing is to the package's crediting claim only, for the same reason as its three sibling packages in this batch: ruling `opus-ee-rulings-1003` §1 needs a committed checker that refuses a swapped value on the family's declaring page, and this package has none. See the crediting section.

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply` and printed `VERIFY 15 functions, 75 anchors` / `ALREADY` / `FAILS 0`, exit 0. This is identical to the committed `interior_applier.out`. All 15 row texts appear verbatim in the page block.
- **Applier control (planted defect).** An unmodified scratch copy (DB root pinned) was run with three mutations: `005847A0`'s first anchor relabelled `nop`, `005A22F0`'s last anchor moved onto the entry, and a pipe added to `006CDDD0`'s text. It printed exactly those three `VERIFY FAIL` lines, then `FAILS 3`, and exited 1. The page was untouched.
- **Population.** 15 rows for a family the page declares with 16 members (`members/optptr-static-descriptor-dispatch-adapters.tsv`). The one member without a row, `00584C70` (same 60-byte form, static `02CAA0A0`), is already cited on the evidence-bearing `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`. That page explains `02CAA0A0`, so the package correctly targeted only the unexplained 15. README: rejected 0, skipped 0, missing 0.
- **OPUS's correction.** The README records one correction for all 15 rows: anchor each row's own `lea r8` instead of the `add rsp` epilogue. Every row carries the `lea` at entry+0x14 as an anchor, and the checker below regenerates it there.
- **Image.** `rvlib.Img` (sha-checked, base 0x00120000, section-aware). For all 15 bodies the `functions.tsv` size (60 B) equals the `.pdata` extent, and the decode covers it exactly, ending at `jmp 00810620` with `int3` padding after. No body has an indirect jump.

### SWE2-AUDIT-SPEC: the representative, read in full (`005847A0`, 60 B, `.pdata` `005847A0..005847DC`)

- "`c` = `rdx`": `push rbx` / `sub rsp, 0x20` / `mov rbx, rdx`.
- "`p` = qword [r8]": `mov rdx, qword ptr [r8]` (`005847A9`, anchor). Then `mov rcx, rbx`, so `rcx` = c on both paths.
- "when `p` is non-null tail-jumps to `00684080` with (c, p, `02CA9FA0`)":
  - `test rdx, rdx` (`005847AF`, anchor) / `je 005847C5` (`005847B2`, anchor);
  - fallthrough: `lea r8, [rip+0x27257e5]` (`005847B4`, anchor) resolves to `02CA9FA0` in `.data`; the row passes the cell's address, not its contents, which is exactly what `lea` does;
  - then `add rsp, 0x20` / `pop rbx` / `jmp 00684080` (`005847C0`, anchor).
- "otherwise calls `0080F420(c, 1)` and tail-jumps to `00810620` with `c` in `rcx`": `mov edx, 1` / `call 0080F420` / `mov rcx, rbx` / frame restore / `jmp 00810620` (`005847D7`).

The row is exact.

### SWE2-AUDIT-SPEC: every row regenerated from the bytes (mechanical, with controls)

The checker is the same reviewer-written one as this batch's sibling reviews:
1. **Extent.** The size equals the `.pdata` extent.
2. **Shape.** The normalised shape equals the representative's, with every non-target operand literal.
3. **Sentence.** The sentence is regenerated from the member's direct targets and its **resolved** `lea r8` target. This is the same discipline as the CURRENT `tdiff.py`, which compares rip operands by resolved target. The regenerated sentence must equal the row character for character, and the target must lie in `.data`.
4. **Anchors.** The anchors are regenerated at the representative's indices (`mov` / `test` / `je` / `lea` / `jmp`) and must equal the row's.

**Result: 15 / 15 OK, bad 0.** All 15 bodies are 60 B. The member-specific values, each stated correctly in its own row:
- **Statics.** 15 distinct static cells, all in `.data`: `02CA9FA0`, `02CA9DA0`, `02CA9EA0`, `02CAD040`, `02CAD840`, `02CAE960`, `02CAD540`, `02CAD440`, `02CAE350`, `02D3E780`, `02E4E1E0`, `02E4E720`, `02E4F900`, `02E4FF60`, `02E5C710`.
- **Tail-jump target.** It is not uniform. Ten members tail-jump to `00684080`. Five tail-jump to `00684090`: `006A94C0`, `006AA740`, `006ADCC0`, `006AF9C0` and `006CDDD0`, and their rows say `00684090`. A template proof that masked the jump target would have hidden this difference. The checker keeps the target as a field.

**Controls:**
- (T) `00584A00`'s `00810620` changed to `00810621`;
- (A) `005A22F0`'s second anchor moved to the next boundary (its `je`);
- (M) `006CDDD0`'s first anchor relabelled `nop`;
- (S) the sentences of `00584F10` and `005A1190` swapped, so each names the other's static.

The checker refused exactly those five rows (`planted 5, flagged 5`).

**Byte control:** `00584A00`'s `lea r8` displacement was raised by 0x10, so its static moved. The member was refused (`TEXT mismatch`).

**Observation (non-blocking, not a row defect).** `00684090` is a separate 9-byte function: `mov r8, qword ptr [rdx+0x10]` / `jmp 00682D20`. `00684080` is the 5-byte `jmp 00682D20`. So for the five `00684090` members, the static that the body passes in `r8` is replaced, before the shared `00682D20`, by qword `[p+0x10]`. The rows state what each body passes, which is exact. A reader who takes the third argument as the descriptor `00682D20` receives would be wrong for these five. The family's description on the page ("ONE operand-aware byte image") does not mention the two targets either.

### SWE2-AUDIT-SPEC: engine_explained crediting (ruling opus-ee-rulings-1003 sections 1 and 2; auditspec-ruling-scoped-ee-row-1003)

This was measured with `progress.py`'s own helpers at HEAD and `check_dispositions`.

- **Section 2.** The page is evidence-bearing with no `ee_index_only`, and the rows are statements about the bodies. Section 2 is satisfied.
- **Measured credit.** All 15 credit, and only through this block:
  - with the block removed, the page credits 0;
  - no other page credits any of the 15;
  - `doc_credits`: plain 15, template 0, scoped 0;
  - `check_dispositions.evaluate`: 15 / 15 in `a_set` and `explained_set`, 0 in `frontier_set`.
- **Section 1: the condition is not met.**
  - The page declares `optional-pointer context dispatch adapters, static-descriptor spelling` (letter C, "PROVED BY FORM - 16 members, all 60 bytes, ONE operand-aware byte image"). That is a shape family explained once on its declaring page.
  - The rows anchor the distinguishing `lea r8` and state its value.
  - No committed checker derives every row and refuses a swapped value. Measured: the package's own applier, run (unmodified scratch copy) on a `rows.json` with `00584F10` / `005A1190` sentences exchanged, printed `VERIFY 15 functions, 75 anchors` / `DRY (block differs ...)` / `FAILS 0`, exit 0.
  - The 15 credit only because `family_rule_inputs` leaves a family with no committed checker rows out of scope (in scope: False; checker-anchored members: 0), pending `SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`.
- **Scoped-row ruling.** No row carries `Scope:` or `scoped row: set-exact`. It does not apply.

**Narrowing (exact wording).** In the package README, replace "All 15 rowed functions now measure A." with:

> All 15 rowed functions measure A under `progress.py` at HEAD by the base rule (60-byte bodies, credited only by this block). The family-declaring-page rule (`opus-ee-rulings-1003` §1) does not reach them yet because no committed checker carries rows for this family; under that ruling the credit needs a committed checker that derives every row from the image and refuses a swapped value, which `interior_applier.py` does not do. Until one is committed, the credit is provisional and lapses when the family is marked as a shape family (`SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003`).

**Route (OPUS).** Commit a `fam_rows.py` + `spec.json` + `rows.tsv` checker for this family. Its rows should anchor the distinguishing `lea r8` at entry+0x14 and state the resolved static. It should also keep the tail-jump target as a field (`00684080` / `00684090`) and carry a swapped-value control.

- Limits: static evidence only, body statements not meanings. The draft and OPUS's re-read are not independent review; this record is. The reviewer's scripts are in a private scratch folder and are not committed.
