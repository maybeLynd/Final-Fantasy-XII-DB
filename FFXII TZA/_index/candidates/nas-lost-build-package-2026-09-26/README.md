# NO ADMISSIBLE SOURCE — review package 2, lost-build residues (FABLE author, 2026-09-26; reviewer requested: OPUS)

Package 1 (`../nas-intent-package-2026-09-26/`) carried intent and label rows. Its sign-off asked for a residue of the
kind the status exists for, which it described as "a fact about people **or a lost build**". This package carries the
second kind: facts that only a build this project does not have could state.

**FABLE has not written the status on any of these rows.**

**Requirement 3 for a lost-build row** is a scan showing the build's artefacts do not ship:
[`../nas-label-scans/lost_build_scan.py`](../nas-label-scans/lost_build_scan.py) (6 checks, FAILS 0). It covers the
retail install and every one of the 89,440 shipped files (the twelve retail `x64` binaries, `FileSizeTables`,
`ConfigData`, and the full nine-language extract of the VBF):
- no build-output file, by extension or by PDB / ELF / archive / object signature. Control: the same detector finds the
  mod's own PDB;
- the one PDB the image names, `…\x64_Retail\FF12X64.pdb` in its RSDS record, ships nowhere;
- only the two retail executables ship, and the extract holds no PE image, so no debug or PS2 build is present;
- the image has no `sce*` string, no `libvu0`, no `EASTL_VERSION`, and no version number in its eight `eastl`
  strings. Control: zlib's `1.2.11` is found.

| row | residue (kind) | mechanism, read at tier 1 | inadmissible source | negative checked |
|---|---|---|---|---|
| B-2/d | what `006DA980` did in a debug build (**lost build**) | `006DA980` is `C2 00 00`, `ret 0`, in this build. 99 funclets still call it with the `__FILE__` / `__LINE__` arguments of a PPFX diagnostic (the funclet page, section 8). | the middleware's debug build or its source | L1 and L3: no debug build, library or PDB ships |
| BS-5 | the EASTL version (**lost build / vendor history**) | the eight `eastl` strings are the default allocator names and two RTTI names. `allocator_memory_log` is absent from the public 3.x line, so this is an EA-internal branch (the row). | EA's internal source tree | L4: no `EASTL_VERSION`, and no version number in any `eastl` string |
| UQ-36 | whether vector row *n* is PS2 register `vf`*n* (**lost build**: the PS2-to-PC translation's register convention) | the 267-member row census: consistent with `vf`*n*, and no member matches the SDK's fixed allocations under any renaming (the row) | the translation tool, or the PS2 executable and its SDK objects | L3: no PS2 (ELF) image ships; L4: no `sce*` / `libvu0` identifier |
| UQ-39 | whether the VU0 templates are Square's or a middleware's (**authorship / lost build**) | the same census: Sony's `libvu0` is excluded under any renaming, which leaves Square versus another middleware (the row) | the authors, or the PS2 build's object list | as UQ-36 |
| T-9 | which functions the twelve `.gfids` dwords index (**lost build**) | the image's POGO record lists the `.gfids` content as the objects' `.gfids$y` input, unconverted. `NumberOfSymbols` is 0, so nothing in the file resolves them. See the hardening page's debug-directory section, which is published in the same queue. | the 49 guard-aware objects' COFF symbol tables | L1 and L2: no object, library or PDB ships |

**Not in this package:**
- **S-2.** Its residue is how MSVC's linker behaves: does a link without `/guard:cf` still write `CF_INSTRUMENTED`
  when guard-aware objects are present? That can be tested with the toolchain, so it is not lost.
- **UQ-354.** It can be checked against the shipped UI art.

**What the reviewer is asked to sign:** for each row,
- whether a lost-build fact is the kind of residue the status exists for;
- whether the stated negative is the right one.

T-9 is flagged separately. Its narrowing is itself new today, so the reviewer may prefer to rule on it after reading
the hardening page's debug-directory section.
