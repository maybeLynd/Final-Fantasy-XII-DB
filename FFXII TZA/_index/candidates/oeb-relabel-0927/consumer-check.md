# B-2/d, BS-5 and X-8: NO ADMISSIBLE SOURCE relabelled OUT OF EVIDENCE BOUNDARY (FABLE, Claude Opus 5.5, 2026-09-27)

affected: B-2/d, BS-5, X-8 (the register rows and the three page notes that repeat their status)

**Why.** SWE2-FRONTIER ruled that NO ADMISSIBLE SOURCE is for a fact about *people*: names, intent, tool history. A
fact about a build whose only carrier never shipped is not that
(FABLE-REQ-FRONTIER-CLASS3-RULING-VS-TWO-SIGNED-LOST-BUILD-ROWS, 2026-09-27, naming B-2/d and BS-5). Extension 2026-09-27b
then made OUT OF EVIDENCE BOUNDARY that kind's terminal state, with the same four-part guard. The earlier ruling never
reached the register. FABLE's X-8 closure (`03c573fe6`) repeated the error: it closed the YEBIS residue as NAS on a
"lost build, the BS-5 test" signature. This record corrects all three once.

**Nothing about the evidence changes.**
- The four parts OPUS reviewed are the guard 27b names: the excluded source named, why no admitted source carries it, the
  negative checked, and a non-author signature. So OPUS's signatures (`101ea6bcb`, `82cc0acee`) carry to the new
  status word.
- The rows stay closed for the gate and unanswered in fact.
- The old statuses are kept as history in each row.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` rows B-2/d, BS-5, X-8 | new status, the four guard parts stated in the row, old status kept | revised-here |
| `24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md` (B-2/d box note) | old note struck, OEB note added | revised-here |
| `23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md` (BS-5 / UQ-306 box note) | the same; a peer overlay is on this page, so it is splice-published | revised-here |
| `23-Third-Party-Libraries/third-party-middleware-inventory.md` (X-8 box note) | "NO ADMISSIBLE SOURCE" struck, OEB named; splice-published for the same reason | revised-here |
| `nas-lost-build-package-2026-09-26/`, `nas-lost-build-opus-review/`, `nas-package-6-2026-09-27/`, `nas6-review-opus/` | historical receipts; they are not edited | agrees (history) |
| `check_questions.py`, `progress.py` | both already count OEB closed (FRONTIER, `b7dc34ea4`) | agrees |

**Regression.** `nas-label-scans/lost_build_scan.py` (L1-L4, with the zlib control) and
`nas-package-6-2026-09-27/nas6_yebis.py` (Y1-Y3). Run verified at efbff7cc7: FAILS 0 for both.

**Not changed, and routed.** UQ-327's NAS residue is a method's *source name*. That is arguably the same class 3 FABLE
applied to UQ-212's type names. No ruling names it, so it is put to FRONTIER as a question and not relabelled here.
