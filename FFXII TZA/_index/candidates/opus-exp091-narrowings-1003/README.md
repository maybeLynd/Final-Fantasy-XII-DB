# EXP-091 consumers narrowed to what the retained fixtures execute (OPUS, 2026-10-03)

*On SWE2ORACLE-REQ-OPUS-EXP091-CONSUMER-NARROWINGS-1003. FABLE reviewed SWE2-ORACLE's EXP-091 resolver-base repair as
a non-author (`auditspec-review-oracle-exp091-resolver-repair-1003`, committed `b9502c733`, ACCEPT-WITH-NARROWING).
Section 4 of that review gives exact replacement text for three OPUS-owned consumers. OPUS applies items A-E as
written, with [`apply_narrowings.py`](apply_narrowings.py) ([`apply_narrowings.out`](apply_narrowings.out)).*

## Applied (OPUS)

FABLE's span census found that 47 of the 54 bodies `bodies.json` lists execute under the retained 87 cases and 10
mutants. Seven do not: `0020E600`, `0025AAD0`, `002F1710`, `00316A50`, `00317E50`, `003BBC80` and `003DC780`. That is a
coverage gap of the fixtures, not a reachability result, and no retained case changes.

| item | where | change |
|---|---|---|
| A | `07-Combat-Action/CONTRACT-commit-action.md` §13a | "~54 shipped bodies" becomes 47 of 54 executed; names the seven, the `0030C0E0` stop at `0030C179`, and the repair package that executes `0020E600` and the action-row arm |
| A (count) | the same sentence | 85/85 becomes 87/87, the retained result since `f7bbac4ef` added the two copy-origin cases. The review offered this fix |
| B | the same contract, the `bodies.json` note | "every listed VA was genuinely executed" becomes "the list is not an execution record: 47 of its 54 VAs execute" |
| C | `_experiments/EXP-091-commit-callees-exec.md`, the closure sentence | "~54 shipped bodies" becomes "`bodies.json` lists 54; the retained fixtures execute 47" |
| D | the same record, its limits | "every listed VA was genuinely executed" becomes the 47/54 statement, the seven names, and the resolver-base plant at `0x1F85D30` vs the `0x1F83530` that `0020E602` reads |
| E | `_index/candidates/s20-runtime-per-invariant-exposure.md`, the "runs as shipped" cell | "~54 bodies" becomes "54 listed, 47 executed (not the seven)" |

Item F is a citation rule for future text that cites the repair package's consumer items 1-2. Nothing on these three
pages cites them today.

Every old text occurred exactly once. The replacement runs in place as one paragraph, so the pages' line wrapping
changes only inside the replaced span.
