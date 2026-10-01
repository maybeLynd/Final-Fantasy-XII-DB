# Consumer-check record — OV apply batch 0929c (SWE2-FRONTIER, 2026-09-29)

Affected: `_index/OPEN-QUESTIONS.md` register rows OV-11, OV-19, OV-25, OV-26, OV-33, OV-39, OV-40, OV-41, OV-42, OV-43, OV-45, OV-46 and the carrier pages `the-actor-request-from-arming-through-start-and-return.md`, `the-resource-owner-from-copy-or-borrow-to-disposal.md`, `the-nonempty-prf-registration-and-specialized-relocation.md`, `the-source-block-mover-and-separate-consumer-refresh.md`, `how-a-battle-unit-is-built-from-its-definition.md` — all touched by this publish.

The consumer `check_questions.py` agrees with the new register/checklist state at publish time: 1,648 ledger rows, 0 stale/early mismatches, 0 cell-count defects, table and document checklists consistent.

**What changed and the agreement state per consumer.**

- Register rows: OV-11, OV-25, OV-39, OV-40, OV-41, OV-43, OV-45, OV-46 marked ANSWERED by FABLE's
  `frontier-apply-bundle-0929b/rows_b.py` (OV-42 removed from the bundle's list because it was already
  applied in an earlier batch); OV-26 upgraded to ANSWERED with the alloc-failure answer
  (`ov26-frp-bounds-fable/alloc.md`, alloc.py A T C S) and a named NULL-buffer-parse residue;
  OV-42, OV-33, OV-19 narrowed to owner-protocol scope keeping only their RT residues. Every row
  keeps its previous verdict struck as verbatim history.
- Carrier boxes: the nine bundle-B boxes ticked with struck question text, the answer, the record
  link and kept obligations; OV-26's box ticked alongside its row so register and checklist stay
  consistent; the OV-42 box text carries FABLE's later corrections — rejection is the negative
  narrowed index (a full queue blocks, pumping), and the arena residue is now answered
  (`ov42-arena-residue-fable/`, arena.py A C T D K: arena 11 whole-replaced at a state change,
  arena-6 orphans never reclaimed).
- Executable-claim correction: the experience curve on
  `how-a-battle-unit-is-built-from-its-definition.md` — `k(12k - 2)` / level 2 = 47 corrected to
  `12k^2` / level 2 = 51 (`exp-curve-fable/unitdef-curve.patch`). Named regression: `curve.py`
  (`exp-curve-fable/`, original bytes under unicorn, K fails if the old formula is reinstated);
  run: curve.py at 3e923f4f5 (FAILS 0, curve.out). The other consumer page is corrected by FABLE
  directly.

**Not claimed:** runtime parity for the kept RT residues (shipped-play rejection, issuance timing,
IO timing); L2 or terminal acceptance; the box-kept obligations on OV-25, OV-40, OV-41.
