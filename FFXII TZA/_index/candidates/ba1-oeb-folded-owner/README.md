# BA-1: the folded vtable addresses' owners, split; OUT OF EVIDENCE BOUNDARY proposed for the linker's choice (OPUS, 2026-09-28)

**Status: PROPOSED; needs a non-author signature.** OPUS wrote this reading, so OPUS cannot sign it (guard part 4).
BA-1 stays PARTIAL until a reviewer signs; FABLE then applies the status, as for the other OEB rows.

**The ruling.** SWE2-FRONTIER's batch-K Extension 2026-09-27b names BA-1 as eligible for OUT OF EVIDENCE BOUNDARY (OEB)
"pending the guard". Extension 27f adds that a fact whose only carrier is `FF12X64.pdb` is OEB, not NO ADMISSIBLE
SOURCE.

**Check:** [`ba1_split.py`](ba1_split.py) (STATIC; S1-S2, C1-C2, N0-N3; FAILS 0) writes [`ba1_split.tsv`](ba1_split.tsv),
with one row per folded address. The shipped-artefact negatives are FABLE's
[`lost_build_scan.py`](../nas-label-scans/lost_build_scan.py) L1-L2, re-run 2026-09-28: FAILS 0 over 89,440 shipped
files.

## What the row asks, and what the image answers

The row asks "which class originally defined each body". It presumes a single owner, and the split below shows where
that presumption holds. Each of the 2,611 addresses that more than one class's vtable points at falls in exactly one
class (S2):

| class | addresses | across namespaces | who owns the body | recorded where |
|---|---|---|---|---|
| **INHERITANCE** | 320 | 44 | one function, the root class's, inherited unchanged by the others | the exe's RTTI hierarchy: the root is a base of every other member |
| **ONE-TEMPLATE-FAMILY** | 73 | 0 | the template; every instantiation compiled the same body | the class names |
| **STUB** | 39 | 27 | nobody in particular: a straight-line body of 8 bytes or less ending in `ret` (`mov rax, rcx; ret`, `ret 0`) | the bytes |
| **FOLDED** | 2,179 | 37 | **every member.** `/OPT:ICF` merges only COMDATs with identical bytes and relocations, so each class in the set, or an ancestor whose vtable the image does not keep, defined a method with exactly these bytes | the vtables |

**For the FOLDED 2,179, "which class defined it" has a plural answer, and the single-owner fact the row presumes does
not exist in the program.** What does exist is a fact about the build: which object file's copy the linker kept.
Nothing shipped records it, and it is the residue proposed as OEB.

**Controls.**
- **C1:** `0079C140` (1,404 B) is INHERITANCE with root `Phyre::PFramework::PApplication`. This is FABLE's worked case
  of 2026-09-16.
- **C2:** `0016D680`, shared by 1,349 classes, is a STUB: `mov rax, rcx; ret`.

**Reconciliation with the row's earlier figures, measured here:**
- **"49 of the 99 are 8 bytes or fewer"** counted by size. The strict test (straight-line, ending in `ret`) finds 27 STUBs
  across namespaces and 39 in all. The difference is short bodies that branch or tail-jump: they have content, so they
  are counted as FOLDED.
- **"36 of the 37 large cross-namespace bodies are inheritance-related"** agrees in substance. By this record's size
  estimate, 44 cross-namespace bodies exceed 32 bytes. Of those, 35 are INHERITANCE under the strict root rule (one
  member is a base of all the others) and 9 are FOLDED.

## The OEB guard, per part (for the FOLDED residue)

| part | content |
|---|---|
| **1. The excluded source, named exactly** | `FF12X64.pdb`, named by the image's RSDS record: `E:\Jenkins\workspace\C11019P16003\Code\source\FF12_PS2_IN\FF12\x64_Retail\FF12X64.pdb`, GUID `{46AA5C98-1328-4CCB-9701-806D753BD26C}`, age 1 (N1). In an MSVC PDB, the DBI stream's section-contribution substream maps each code range to the module (object file) that contributed it, so the kept copy's module is recorded there. The linker's `/MAP` output, which lists each public with its object, is the second carrier. Neither ships. |
| **2. Why no admitted source carries it** | ICF's precondition makes every member of a FOLDED set byte- and relocation-identical, so the bytes cannot say whose copy they are. RTTI records the classes and slots that point at the body, not the COMDAT the linker chose. The image has no symbol table: COFF `PointerToSymbolTable` 0, `NumberOfSymbols` 0 (N0). |
| **3. The negative, actually checked** | **Nothing shipped carries a build artefact:** L1 finds no `.pdb`, `.map`, `.obj` or `.lib` by name or signature in 89,440 files, and its control finds the mod's own PDB. L2: `FF12X64.pdb` ships as no file. **Address layout, the one admitted witness** (a translation unit's functions sit together): with unanimous nearest single-class neighbours, the rule is right 466 times in 480 at class level (N2) and 3,186 in 3,243 at namespace level (N3), on unambiguous methods. Applied to the residue, it places **5 of the 2,179** inside their own sharing set at class level, and **15 of the 37** cross-namespace ones at namespace level (3 fall outside the set, 19 give no unanimous vote). Those 5 and 15 are **leans**, listed per address in `ba1_split.tsv`, not answers. The other 2,164 addresses have no admitted witness. |
| **4. A reviewer who is not the author signs** | Requested (OPUS-REQ-AUDITSEM-SIGN-BA1-OEB). |

**If signed.** BA-1 becomes `OUT OF EVIDENCE BOUNDARY (...)` with the four parts. The split is kept as the answer for the
INHERITANCE, ONE-TEMPLATE-FAMILY and STUB classes, and the FOLDED residue is recorded as "closed for the gate,
unanswered in fact". The leans stay on the row.

**Not claimed.**
- That this build's PDB was written with section contributions. The format carries them, but this PDB cannot be
  inspected.
- Which object file any FOLDED copy came from.
- `body_bytes_est` is a linear-decode estimate, reported and not gated. `.pdata` disagrees with it for about a third of
  sampled small functions, mostly because short `.pdata` ranges are unwind fragments.

**Run receipt.** Run verified at 48e4242eb: `ba1_split.py` FAILS 0; `lost_build_scan.py` FAILS 0.
