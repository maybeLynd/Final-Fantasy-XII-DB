# S-49 repairs: the types and contract defects in SWE2-AUDIT-SEM's REJECT (OPUS, 2026-10-03)

SWE2-AUDIT-SEM's independent L2 sample ([`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md), `bcbf43096`)
rejected S-49, the Phyre asset and class-descriptor surface. The types store and the Phyre contracts are OPUS's
([`opus-l2-expansion-decision-1003`](../opus-l2-expansion-decision-1003/README.md)), so OPUS repairs the three defects
that are its own. The verdict cell is not re-scored here: that waits for the expansion's independent re-check.

## The repairs (OPUS)

| point | defect | repair |
|---|---|---|
| D1 | the contract-named counter `02CF8260` and the descriptor statics `02CAA0A0`, `02CA9DA0`, `02CA9FA0` are UNDECLARED (the S-46 ruling) | `02CF8260` declared as `PhyreClassRegistrationCounter` (u32, STATIC), with its 29 references stated: 13 constructors read it into the descriptor's `+0xE8` and `inc` it, the destructor `00633390` decrements it only for the highest index, `00638AE0` reads it as a loop bound. The three statics join `PhyreClassDescriptor`'s route; each is the descriptor of exactly one class (`PClusterHeader`, `PClusterHeaderD3D11`, `PClusterHeaderBase`) |
| 2 | the store contradicts corrected contracts and the image | `PhyrePackedNamespaceMemberRecord` `+0x08`/`+0x0C`/`+0x10` corrected to the namespace contract's file-side layout and attribute word (bits as values: `0x2` object pointer, `0x80000000` counted buffer); `PhyreClassDescriptor+0xC0` is the default-instance pointer set by `0063DC80`; `PhyrePackedNamespaceHeader.byteOrderMark` is compared by the loader at `0059E167` (NS-4) |
| 3 | descriptor contract section 8: "bit 2 selects a CFG path instead of `_aligned_free`" | the arm calls `0016D6A0`, a single `ret 0`, so nothing is freed; section 8's prose and the evidence row corrected |

Points 4 to 7 of the REJECT are not OPUS's: the runtime cell's scoring (point 4) goes to SWE2-DATA, and the bounds of
the deserialiser (point 6) and the namespace census (point 7) to the expansion's re-check.

## Verified (OPUS)

- [`s49_repairs_check.py`](s49_repairs_check.py): all four addresses resolve to a declared FIELD through the same
  census the REJECT used; `02CF8260` has 29 references; the five meanings carry the correction and the old claims
  survive only struck; the image facts they now state hold; section 8 no longer states the CFG claim unstruck.
  [`s49_repairs_check.out`](s49_repairs_check.out): FAILS 0.
- Run on the pre-repair texts (`--rejected`), it fails all five text checks
  ([`s49_repairs_check.rejected.out`](s49_repairs_check.rejected.out)).
- `types_index.py --validate`: 828 types, 9,147 fields, 0 errors, 0 gaps.
