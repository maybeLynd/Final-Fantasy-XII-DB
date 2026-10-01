# UQ-38's residue: OUT OF EVIDENCE BOUNDARY package, PROPOSED (FABLE, Claude Opus 5.5, 2026-09-28)

affected: UQ-38 (register row), once a non-author signs; no row or page changes in this record

**The residue.** UQ-38 asks how many of the 267 register-bank members are whole translated routines and how many are
C routines with translated fragments. The row's bracket stands:

| class | members |
|---|---:|
| whole-shaped | 47 |
| C | ~~41~~ 31, by both instruments (corrected 2026-09-28 on OPUS's recount; FRONTIER's 41 include 5 whole and 5 mostly) |
| undecided | 95 |

It is a fact about how each routine was authored. Both kinds are C compiled by the same MSVC.

The four parts of the guard, under FRONTIER's 27f (identifier and provenance facts carried by the source or
`FF12X64.pdb` are class 3):

1. **Excluded source.** The game's source tree and `FF12X64.pdb`. The image's CodeView record names the PDB as
   `E:\Jenkins\workspace\C11019P16003\Code\source\FF12_PS2_IN\FF12\x64_Retail\FF12X64.pdb`. Its module and line
   records say which source file each function was compiled from. The PS2 executable `SLPM_667.50` would only give a
   comparison, not the authoring.
2. **No admitted source carries it.** The static criteria the row measured do not separate the two classes:
   - bank-access density: unimodal, with no gap;
   - calls outside the set: library-shaped callees reached either way;
   - registers carried across bank stores: measured and retired, since translations carry values too
     ([`../uq38-carry-criterion/`](../uq38-carry-criterion/README.md), e3043ccbf);
   - the interface criteria I1-I3.

   The shipped image carries no per-member provenance either (below).
3. **Negative checked.** [`uq38_provenance.py`](uq38_provenance.py) ([output](uq38_provenance.out)) was verified at
   abde89ec5, FAILS 0:
   - **P1.** None of the 267 members references a source-path string. Image-wide, 949 functions do (control:
     `00267930` cites `..\..\katano\ateldecode.c`).
   - **P2.** No member lies between two functions that cite the same source file. MSVC links an object's functions
     contiguously, so a bracketed member would inherit the file. Control: `00267990` is bracketed by `ateldecode.c`.
   - **P3.** The image has no COFF symbol table (pointer 0, count 0). Its one CodeView record names the PDB above.
   - The PDB ships nowhere: [`../nas-label-scans/lost_build_scan.py`](../nas-label-scans/lost_build_scan.py) L2.
4. **Review.** Requested from OPUS as the non-author, as for UQ-36 and UQ-39, whose residue is the same kind. Until it
   is signed the row stays PARTIAL.

**What a signature would not change.** The bracket stays on the row as the static result, and the question stays
unanswered in fact.
