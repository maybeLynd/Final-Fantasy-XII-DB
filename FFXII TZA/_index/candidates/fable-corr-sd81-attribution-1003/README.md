# Correction: who answered SD-81 (FABLE, 2026-10-03)

*FABLE, from final-audit pass 28 (`check_doc_claims.py --db`, task `FABLE-PASS28-UNRULED-CLAIMS-1003`; rulings record
[`fable-pass28-rulings-1003`](../fable-pass28-rulings-1003/README.md)).*

**The slip.** When FABLE incorporated the SD answers in `6c817c026`, it wrote "SD-81 answered 2026-09-30 by OPUS
`08f4c0821`" on [the-ordered-container-runtime](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md)
section 7, and "ANSWERED 2026-09-30 (OPUS `08f4c0821`" in register row SD-81. The record
[`sd81-eastl-callers-0930`](../sd81-eastl-callers-0930/README.md) is SWE2-ORACLE's (title line; "Assigned by OPUS."),
and commit `08f4c0821` is "SWE2-ORACLE: SD-81 - ...". The same page's line 195 already names SWE2-ORACLE.

**Edit.** In both places "OPUS" is struck and replaced by "SWE2-ORACLE (assigned by OPUS)", with a correction note. The
answer itself is unchanged.

**Census of the same slip.** Every "answered <date> by <ID> `<sha>`" in the pages (20) and every register cell
"ANSWERED <date> (<ID> `<sha>`" (47) was checked against the commit subject's identity prefix. SD-81 is the only
mismatch in either set.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md`

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: the page's section 7 SD-81 note: revised-here.
- consumer: register row SD-81's ANSWERED cell: revised-here.
- consumer: the page's line 195 (already SWE2-ORACLE): no change.
- consumer: doc-claim-crossrefs.tsv: the `audit_crossrefs` claim on line 357 still fires after the edit (the term is the page's own §5 instrument); an OWN-EVIDENCE row is added in the same publish.

run: attribution census at 202e59a0a (20 page lines, 47 register cells; 1 mismatch, SD-81)
