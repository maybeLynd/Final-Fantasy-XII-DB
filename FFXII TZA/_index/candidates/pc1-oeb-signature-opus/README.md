# Non-author signature: PC-1's residue as OUT OF EVIDENCE BOUNDARY — SIGNED (OPUS, 2026-09-28)

**Request:** FABLE-REQ-OPUS-SIGN-OEB-PC1. FABLE wrote the package
([`../pc1-dev-bytes/`](../pc1-dev-bytes/README.md)), and OPUS signs as the non-author (guard part 4). FABLE applies the
status to the row.

**The residue.** What the development build used FF12CONFIG's ten unread fields for, what `opt02`'s value 3 meant, and
whether that build numbered fields as the shipped name table does. The consumer was compiled out of retail, which is
B-2/d's shape. Under 27f the carriers are the source and `FF12X64.pdb`.

## What I re-checked

Every check was re-run at 48e4242eb, and each gives FAILS 0:
- `pc1_dev_bytes.py`: D1-D5 and controls C1-C2;
- `pc1_pointer_store.py`;
- `pc1_ff12config.py`;
- `pc1_route.py`.

**The one load-bearing claim, re-derived independently.** "`opt02`'s 3 is never decisive" rests on `02B62DAB` always
being 1. I swept every rip-relative access in `.text` whose byte range covers `02B62DAB` with my own width rule. There
are exactly three:
- `00408BDC mov byte ptr [..], 1` (the reset);
- `00408D89 mov byte ptr [..], 1` (the loader, an immediate, not a copy from the file);
- `00408B30 movzx eax, byte ptr [..]` (the getter).

Two writers, both constant 1, and one reader. The package's D2-D4 already rule out image-base-relative, stored and
`lea`-formed addresses into the block.

**Parts 1-2.** The ten bytes are written (defaults and the file copy) and never read, so no shipped consumer exists to
be read. The only other place the meaning could live is the unshipped source and PDB. The PDB is named by the RSDS and
ships nowhere (`lost_build_scan.py` L2, FAILS 0).

## Verdict: SIGNED

All four parts hold. **Closed for the gate, unanswered in fact.** The residue text stays on the row. Everything else
PC-1 asked is answered on the row, and this signature does not touch it.
