# SWE2-AUDIT-SPEC re-review: OPUS UC-1 entry statements after the REJECT (opus-referenced-code-the-list-never-had-uc1-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-UC1-ENTRY-REREVIEW-1003` · Package: `_index/candidates/opus-referenced-code-the-list-never-had-uc1-1002/` (request at `693d650d4`, reviewed at HEAD `33b51c821`; the page and package are unchanged since `693d650d4`) · Page: `99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md` · Earlier review: [`auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002`](../auditspec-review-opus-referenced-code-the-list-never-had-uc1-1002/REVIEW.md) (REJECT) · Ruling: [`fable-uc1-gamecode-route-ruling-1003`](../fable-uc1-gamecode-route-ruling-1003/README.md), test 1 as amended 2026-10-03

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 15 replacements are applied verbatim, and all 53 entry statements are true at the bytes. An independent raw census covers every form the amended test 1 lists, and it finds no reference to any of the 19 bodies that still say "no direct reference was found".

The narrowing is needed because those 19 rows still name the old census, "(call/jump, rip-reference and table scans)". The amended ruling requires the row to name a census that covers all the listed forms. That old census missed exactly the forms behind the REJECT, and the committed regression `uc1_entry_check.py` does not cover them all either (see the checks). The exact replacement wording is below. No body sentence and no anchor changes.

## SWE2-AUDIT-SPEC checks

- **(a) The 15 replacements are verbatim.** `rows.json` at `3a61a9fcd` was diffed against `693d650d4` row by row. Exactly the 15 rejected rows changed. For each one, the new text equals the old text with the head "no direct reference was found (call/jump, rip-reference and table scans)" replaced by the REJECT table's right-hand column, character for character. The anchors are unchanged. Every one of the 53 row texts appears verbatim in the page table (lines 382-434). The record's `corrections` list and README name the 15 and the REJECT.
- **(b) What `uc1_entry_check.py` covers.** The docstring and the board say the checker "re-derives test 1 image-wide". It does not.
  - **Branches.** It linearly decodes only listed bodies (`check_dispositions.load_functions()` extents), and keeps `call`/`j*` instructions with an immediate target. That covers `E8`/`E9`, `0F 8x` and rel8 `EB`/`7x`/`E3`/`loop` **inside listed extents only**. It misses a branch in unlisted code: other UC-1 bodies, thunks such as `0026DC50`, and code past a recorded extent such as `0037C3F0` + 0x150/+0x1F8. A row-named fallback re-decodes the site the row itself names, so the two `0037C3F0` rows and `002ECD20` pass. This fallback cannot find an unnamed site, so it does not help a "no reference" row.
  - **Absolute qwords.** It scans qwords in every section, 8-aligned only.
  - **32-bit image-relative values.** It scans `.rdata` and `.data` only, minus a printable-run filter. It does not scan:
    - `.pdata`, which the ruling lists explicitly. The checker drops it outright instead of classifying the field by offset (BeginAddress, EndAddress, UnwindData).
    - `.text`, where MSVC x64 places switch jump tables of RVAs. These are "RVA tables" in the ruling's sense, and code also uses image-base-relative `[rX+disp32]` operands.
    - `_RDATA`, `.rodata` and `.gfids`. `.gfids` is the CFG table of address-taken function RVAs.
  - **No rip-relative reference scan.** It has none at all, yet the rows claim "rip-reference". The uncommitted `Tools/work/OPUS/cloud/uc1_credible.py` (gitignored, so not reproducible from the repo) has retool's rip refs plus the same jcc and `.rdata`/`.data` RVA additions.
  - **Conclusion.** Neither committed nor named instrument covers the full amended form list, so the rows may not lean on either alone. The rows' claims are nonetheless true; see (d).
- **(c) Re-run and controls.** The checker was copied, with `rows.json`, to a scratchpad directory and `DB` was pointed at the repo read-only. It needs `pefile`, which the analysis venv lacks, so it ran under `C:\Python314\python.exe -B`. Output: `rows 53: {'none, confirmed': 19, 'site named, confirmed': 34}` / `FAILS 0`, identical to the committed `uc1_entry_check.out`. The repo working tree was unchanged by the run.
  - **C1, sensitivity.** Run on the pre-repair `rows.json` from `3a61a9fcd`, it gave `FAILS 15`, exactly the 15 rejected bodies. For example: `FAIL 0042FCC0: says no direct reference, but ['jump 00317EC0@00317EC6 ja']`. The consumer check's "fails exactly the fifteen" holds. A census without jcc and image-relative fields would not have caught these.
  - **C2.** jcc was dropped from the census (`mnemonic in ("jmp","call")`) and the run repeated on the repaired rows: `FAILS 0`. The 14 conditional-jump rows still pass because the row-named fallback decodes each row's own site. "site named, confirmed" therefore means "the named instruction targets the body". It does not mean "the census found it". That is adequate for a site row, but it is not an independent find.
  - **C3.** The `.rdata`/`.data` RVA scan was disabled: `FAILS 1` (`00195340`). The image-relative form is live in the check.
- **(d) Independent raw census.** This is a separate reader written for this review, not retool or the checker. The ImageBase is `0x120000`, read from the PE optional header. It covers every section, as follows:
  - In executable sections, at **every byte offset**: `E8`/`E9` rel32, `0F 80-8F` rel32, `EB`/`70-7F`/`E0-E3` rel8, and rip-relative disp32 candidates (immediate tail 0/1/2/4).
  - In **all ten sections** (`.text` and `.pdata` included), at every offset: dwords equal to start − ImageBase, and qwords equal to the start, aligned or not.
  - Each code hit was then placed at an instruction boundary by linear decode of its container.

  Results:
  - **19 "no direct reference" rows: no reference in any form.** Every raw hit is a non-reference:
    - `00125743`, `008858B0`, `00888690`, `00889330` and `00895570`: rip-disp candidates inside `nop`/`movss`/`mov`/`mulss`/`mov`, which have no rip operand.
    - `00125753`: RVA `0x5753` is the disp of `00428D96 lea rdx,[rip+0x5753]` (target `0042E4F0`), and four `.rdata` hits sit inside the "REQSW"/"FREQSW" string run at `00D11B33`.
    - `008824F0`, `008832D0`, `00884090`, `00888650`, `00888700`, `00888780`, `008888C0`, `0088D4E0`, `0088DB60`, `008922A0`, `00892990`, `00893A80` and `00893AC0`: no raw hit at all.

    None of the 19 has a `.pdata`, `.gfids` or `.text` RVA hit, so the checker's gaps hide nothing **for this record**.
  - **15 repaired rows: each named site is found**, at an instruction boundary in the named container, with the named mnemonic. For example: `002905C3 jne`, `00317EC6 ja`, `003EB8CC jge`, and `.rdata` `01DEAAA4` = RVA of `00195340`. `0031AD90` and `003F5030` also have `.pdata` +4 hits (`02FB4DD4`, `02FC435C`). Those are the previous function's EndAddress, not a way in, as the REJECT said.
  - **The other 19 site and table rows are re-confirmed.**
    - 17 call/jump rows: each named site decodes to `call`/`jmp` with the body as target. `002EB5D0`/`002EBD40` are reached from `0037C5E8`/`0037C540`, past `0037C3F0`'s extent. `002ECD20` is reached from the unlisted thunk `0026DC50`. `00710000`/`00710050` are reached from the unlisted `006DE0D7`/`006DE0F7`.
    - 2 table rows: `01EEC568` and `01F003A0` hold the starts.
    - `00710000`'s many RVA and qword hits are the common value `0x005F0000`/`0x00710000` in data. The row claims a site, not exclusivity, so they do not bear on it.
- **(e) Census naming.** The 34 site and table rows name their site, which satisfies test 1. The 19 absence rows name "(call/jump, rip-reference and table scans)". That names no `0F 8x`/rel8 coverage and no image-relative coverage, and it describes the instrument the amendment found short. **This fails the amended test 1's "The row names that census"**, although the absence itself holds. Hence the narrowing.
- **A count correction to the earlier REJECT (this reviewer's own error).** The REJECT counted 20 "entered from" rows, 31 absence rows and "16 clean". Those counts were wrong. The pre-repair record had **17** call/jump rows, 2 table rows and **34** absence rows. 15 of the 34 were referenced, so **19** were clean. The verdict and the 15 defects are unaffected. The checker's `none, confirmed: 19` is right.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (rows.json `text` and the page table, the 19 rows `00125743`, `00125753`, `008824F0`, `008832D0`, `00884090`, `008858B0`, `00888650`, `00888690`, `00888700`, `00888780`, `008888C0`, `00889330`, `0088D4E0`, `0088DB60`, `008922A0`, `00892990`, `00893A80`, `00893AC0`, `00895570`).** In each row, replace:

> no direct reference was found (call/jump, rip-reference and table scans)

with:

> no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03)

The rest of each row is unchanged. Then re-run `interior_applier.py --apply` and the neighbour gate. `uc1_entry_check.py` keys absence on the prefix "no direct reference was found", so it still passes.

**Alternative repair.** OPUS may instead name its own census, in which case the record must not name SWE2-AUDIT-SPEC's. To do that, extend `uc1_entry_check.py` as follows and name it in the parenthetical:
- raw-scan rel8/rel32 branch targets over all of `.text`, not only listed extents, then confirm each hit at an instruction boundary;
- add rip-relative references;
- scan RVA dwords in every section, `.text`, `_RDATA`, `.rodata` and `.gfids` included;
- classify `.pdata` hits by field offset instead of dropping the section;
- correct the docstring's "image-wide".

**Notes (non-blocking):**
- `uc1_credible.py`, the census that will screen the remaining F-unmet UC-1 bodies, lives under the gitignored `Tools/work/`, so no reviewer can reproduce it from the repo. Commit it beside the regression, or fold it in.
- Add a committed control to `uc1_entry_check.py`: run it on the pre-repair `rows.json` and assert FAILS 15 (C1 above). Without a control, a census that silently reached nothing would also print FAILS 0.
- In the site-row match, `or "+ 0x0" in t.split(";")[0]` accepts any jump from a named container whenever the clause contains "+ 0x0" anywhere. Today it affects only `002ECD20`, which is correct, but it is looser than intended.
- `pefile` is missing from the analysis venv (also noted in the return-value-adapter review).
