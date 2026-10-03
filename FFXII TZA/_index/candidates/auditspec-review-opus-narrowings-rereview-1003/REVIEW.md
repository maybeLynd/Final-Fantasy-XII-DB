# SWE2-AUDIT-SPEC re-review: OPUS's incorporation of the batch-95d495604 narrowings (opus-ee-traversal-adapters-1003 and siblings)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-NARROWINGS-REREVIEW-1003` · Target: `_index/candidates/opus-ee-traversal-adapters-1003/` and the other records whose `95d495604` verdict was ACCEPT-WITH-NARROWING: `opus-ee-base-aware-ctors-1003`, `opus-ee-guarded-registration-1003`, `opus-ee-name-only-registration-1003`, `opus-ee-return-value-adapters-1003`, `opus-ee-two-member-registrars-1003`, `opus-animation-channel-binding-and-transform--ee-1003`, `opus-sound-variant-selection-ee-1003` and `opus-referenced-code-the-list-never-had-uc1-1002`. Incorporated at `c480be543`; checked at HEAD `33eb7192f`.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

Every requested repair checks out but one.
- All six lead replacements are verbatim, in spec.json and on the pages.
- The skips are re-verified by `check`.
- Return-value adapters: 398 rows and 4 exclusions, with the four new rows exact at the bytes.
- Guarded registration: the columns are verbatim and the reasons split 35/19.
- The controls now fail when the comparison is dead.
- `005C6D90`, the three address wordings and the 19 UC-1 phrases are verbatim.

The one residue is guarded-registration Narrowing 3. Its closing sentence was dropped, and the regenerated README now asserts the opposite for the 19 pattern-refused members (exact wording below). Two non-blocking README statements are also wrong.

## SWE2-AUDIT-SPEC checks

- **Checkers re-run.** `fam_rows.py check` was run in place for all 13 EE family records under `C:\Python314\python.exe -B`. The analysis venv still lacks `pefile`. `check` writes nothing, and `git status` of the records was identical before and after.
  - All 13 exit 0 with FAILS 0, and every output is identical to its committed `fam_rows_check.out`.
  - 18 of the 19 `opus-ee-*` records share one `fam_rows.py` (the exception is `verb-adapters`).
- **(1) The six lead replacements are verbatim.** The replacement text of each narrowing was checked by substring in the record's `spec.json` `lead` and on `class-descriptor-and-metadata-system.md`. Every one is True in both:
  - base-aware-ctors;
  - guarded-registration, the lead and both bullets;
  - name-only-registration, both halves around the link;
  - traversal-adapters;
  - two-member-registrars;
  - return-value-adapters: the exclusion sentence, re-worded for the alternative repair (below).

  The superseded phrases occur 0 times on the page: "shares one pattern in many spellings", "a null-guarded selection of the object pointer", "installs that descriptor's vtable", and "What differs ... is the static descriptor and the vtable stored into it".
- **(2) The skips are re-verified against `00875E10`.**
  - `excluded.tsv` marks all 19 reasons `skip: called from 00875E10 ...`, and its header distinguishes skips.
  - `skips_check()` re-extracts each skip, and decodes `00875E10`'s body to require a direct call to each.
  - Sensitivity, in memory: with `skip_caller` pointed at another function, `check` printed 19 `FAIL ... skip_caller ... no longer calls it` lines and exited 1.
  - The README now states the stronger behaviour, which is true.
- **(3) Return-value adapters: the census extent is decoded.**
  - `ex_call_class` now uses `_body(a)`. `check` reports `members 402, committed rows 398, declared exclusions 4`.
  - `excluded.tsv` holds exactly `0062F0F0`, `0063C000`, `006B2950` and `006B2970`, all "reflected type not unique".
  - Raw bytes, independent of capstone: the four new rows' `E8` at `005D346C`, `005D46FC`, `0063EF2C` and `006AF57C` resolve to `005F9880`, `005FADE0`, `0064F9E0` and `006AECC0`. That matches the page rows, and each body is 0x1A B. T (PShader, PShaderParameterCaptureBufferTexture2D, PMotionBlurD3D11, PArray<PTypedObject>) matches the earlier review's verification.
  - The page says 398 in the lead and in the table heading. Its exclusion sentence names the four type-not-unique members correctly.
- **(4) Guarded registration.**
  - `value_col` = "first vtable V stored into a lea-loaded static" and `name_col` = "class named by the RTTI locator before V (T for a class descriptor)", verbatim. They are rendered in the page's table header.
  - The `excluded.tsv` reasons count 35 "no RTTI-located vtable is stored", 19 "a vtable is stored, but into an offset inside a lea-loaded record or from a register other than rax, which the checker's store pattern does not match", and 2 "value shared". That totals 56.
  - **Residue:** see the narrowing.
- **(5) The controls are sensitive.** Tests ran in memory, with nothing written, on traversal-adapters and name-only-registration.
  - The swapped-value and moved-anchor controls now run mutated copies of the committed rows through the same `compare()`. Each adds 1 to FAILS when the comparison returns nothing.
  - With `compare` stubbed to return `[]`, both controls printed `ACCEPTED`, and `check` gave FAILS 2, exit 1.
  - The known answer decodes the anchor's raw bytes without capstone (`E8`/`E9` rel32, or a rip-relative ModRM).
  - With row 0's value shifted by 0x10 in both the rows and the derivation, the known answer printed `FAIL - anchor ... raw bytes reference 02CAF0E0, committed value 02CAF0F0`, and `check` exited 1.
  - Every one of the 13 records prints a known-answer line that matches.
- **(6) `005C6D90`.** The rows.json text holds "word `+0x34` = the low 16 bits of dword `[s+8]`, word `+0x36` = the low 16 bits of `k`, where `k` = the low 31 bits of dword `[s+0x18]`", verbatim. `interior_applier.py`: `VERIFY 7 functions, 35 anchors / ALREADY / FAILS 0`.
- **(7) The three address wordings.** `007CF780` reads "the address `01CB6E80` followed by". `007CFE60` and `007D0710` read "writes the address `01CB6E10` to `[rdx]`". "the qword `01CB6E`" occurs 0 times on `sound-variant-selection.md`. The applier gives `VERIFY 7 functions, 35 anchors / ALREADY / FAILS 0`.
- **(8) The 19 UC-1 phrases.**
  - In `opus-referenced-code-the-list-never-had-uc1-1002/rows.json`, exactly the 19 named rows carry the replacement parenthetical verbatim. The old parenthetical occurs 0 times in rows and on the page, and the new one occurs 19 times on the page.
  - All 53 row texts are on the page. The applier gives `VERIFY 53 functions, 186 anchors / ALREADY / FAILS 0`.
  - `uc1_entry_check.py` gives `rows 53: {'none, confirmed': 19, 'site named, confirmed': 34} / FAILS 0`, identical to the committed `.out`.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (guarded registration, Narrowing 3 not fully incorporated).** The README's "No rows" list dropped the narrowing's closing sentence, "These 19 are refused by the checker's pattern, not by the form." The generator (`fam_rows.py cmd_readme`, line 860) then appends "The other 56 are refused by the image for this family's per-member form, and `check` fails if any of them starts deriving." That re-asserts, for the 19, exactly the plain-reading claim the narrowing withdrew. The `excluded.tsv` header says the same of every non-skip row ("otherwise refused by the image for this family's per-member form"). The 19 do store an RTTI-located caller-object vtable into a static record; only the checker's store pattern refuses them.

**Exact repair.**
- In `opus-ee-guarded-registration-1003/README.md`, replace "The other 56 are refused by the image for this family's per-member form, and `check` fails if any of them starts deriving." with:

  > These 19 are refused by the checker's store pattern, not by the form. `check` fails if any of the 56 starts deriving.

- In the shared generator, stop emitting "The other %d are refused by the image for this family's per-member form" when the family has no skips. In `opus-ee-return-value-adapters-1003/README.md` it reads "The other 4", although no first group exists. Use "All %d are refused by the derivation, for the reasons listed; `check` fails if any of them starts deriving."
- In the `excluded.tsv` header, change "otherwise refused by the image for this family's per-member form" to "otherwise refused by this family's derivation (the reason says how)".

No row changes.

**Notes (non-blocking):**
- Every regenerated README says "`check` needs an interpreter with capstone and pefile (the analysis venv)". The analysis venv (`Collaboration/Tools/analysis/venv`) still has no `pefile` (`ModuleNotFoundError`), so the parenthesis is false. Either install pefile there, or name the interpreter that works (for example `C:\Python314\python.exe`).
- The known answer compares the **committed** row 0 with its raw bytes. An image-blind extractor that echoes a correct `rows.tsv` still gives FAILS 0. With correct rows that case is indistinguishable, so this is accepted as asked. Comparing `derived[row0]` with the raw bytes would make the line test the extractor itself.
- The members file `abstract-class-descriptor-base-aware-constructors.tsv` still says "133 members ... the members differ only in constants" in its header. Its data rows are 132, and the narrowed lead now lists the other differing operands. This was a note in the earlier review and was not in the request.
- The two-member-registrars table header still says "vtable V installed". That was not part of the narrowing, and the lead now defines V as the transient `PClassDescriptorAbstract<T>` vtable. Renaming the column the way guarded's was renamed would keep the two consistent.
