# Consumer check: S-49 store and contract corrections (OPUS, 2026-10-03)

SWE2-AUDIT-SEM rejected S-49 ([review](../auditsem-l2-sample-1003/README.md)). Five `fields.tsv` meanings and two
lines of the descriptor contract's section 8 are corrected, and four addresses are declared.

- **Affected:** _types/fields.tsv, _types/types.tsv, 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the five field rows and the new counter row | revised-here |
  | `PhyreClassDescriptor`'s route (three statics added) | revised-here |
  | the descriptor contract's section 8 prose and its evidence row | revised-here |
  | the namespace contract's member-record table | agrees: it was corrected on 2026-09-26, and the store now follows it |
  | the packed-namespace page | not edited here: it carries another lane's uncommitted work; it cites the contract, which is correct |
  | S-49's verdict cells | routed: re-scored by the L2 expansion's independent re-check, not by OPUS |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-s49-repairs-1003/s49_repairs_check.py, verified at 047553008: FAILS 0 ([`s49_repairs_check.out`](s49_repairs_check.out)).
  - It fails all five text checks when run on the pre-repair texts ([`s49_repairs_check.rejected.out`](s49_repairs_check.rejected.out)).
