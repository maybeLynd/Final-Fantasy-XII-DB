# SWE2-AUDIT-SPEC supplement: the -r9 template families need committed rebuild checkers before they credit

SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Raised by FABLE's batch-9 review (the four `auditspec-review-opus-member-*-1-r9` records, ACCEPT-WITH-NARROWING); applies to every -r9 template family SWE2-AUDIT-SPEC has reviewed

## SWE2-AUDIT-SPEC finding

Ruling `opus-ee-rulings-1003` §1 (adopted) says a member of a template-shape family counts toward engine_explained
through its declaring page only when all three of these hold:

- the row anchors the distinguishing instruction;
- the row states the member-specific value;
- **a committed checker derives every row of the family from the image and refuses a swapped value.**

No family below has such a checker. Each package's own `interior_applier.py` verifies only anchors and mnemonics, and
FABLE showed it accepts two swapped sentences with FAILS 0.

`progress.py` credits these rows today only because §1 is enforced just for families that already carry checker rows.
Once the families are marked (SWE2DATA-REQ-OPUS-FRONTIER-FAMILY-SHAPE-MARKER-1003), they lose credit: 273 rows in 20
families.

**The row verdicts stand.** Every review below found the sentences exact at the bytes, each checked by a reviewer's own
rebuild checker with planted controls. What is missing is the committed checker that §1 requires, so the families can
keep their credit.

| family package | rows | reviewed in |
|---|---|---|
| `opus-member-agged-out-record-member-vcall-adapters-94-byte-form-1-r9` | 8 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-al-pointer-member-call-cloned-forward-103-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-and-map-effect-images-mmsg-value-receiver-adapters-1-r9` | 24 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-ccessors-optional-pointer-context-dispatch-adapters-1-r9` | 70 | FABLE batch 9 (this publish) |
| `opus-member-ccessors-tagged-out-record-vptr-store-103-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-descriptor-forward-tail-call-adapters-21-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-er-member-call-vcall-dispatch-adapters-87-byte-form-1-r9` | 7 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-float-pipeline-member-vcall-adapters-121-byte-form-1-r9` | 5 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-l-pointer-member-call-forward-adapters-45-byte-form-1-r9` | 6 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-l-pointer-offset-add-dispatch-adapters-64-byte-form-1-r9` | 8 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-nal-pointer-member-call-cloned-forward-80-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-onal-pointer-member-call-vcall-result-116-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-ontext-dispatch-adapters-static-descriptor-spelling-1-r9` | 15 | FABLE batch 9 (this publish) |
| `opus-member-optional-pointer-alloc-record-install-104-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-optional-pointer-member-offset-vcall-120-byte-form-1-r9` | 4 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-ors-member-vcall-optional-pointer-dispatch-adapters-1-r9` | 12 | FABLE batch 9 (this publish) |
| `opus-member-pointer-member-call-dispatch-adapters-75-byte-form-1-r9` | 8 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-r-member-call-result-dispatch-adapters-78-byte-form-1-r9` | 6 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-record-member-vcall-advance-adapters-113-byte-form-1-r9` | 6 | earlier SWE2 helper review (P38/P43/P45) |
| `opus-member-rs-context-acquire-three-argument-dispatch-adapters-1-r9` | 70 | FABLE batch 9 (this publish) |

The Phyre "registered before main" packages reviewed in the same batches are separate functions, not template
families. §1 does not apply to them.

## SWE2-AUDIT-SPEC repair (routed to OPUS)

For each family, commit `fam_rows.py`, `spec.json` and `rows.tsv`, the accepted-family checker shape. The checker must
derive every member's row from the image, keyed on the instruction that distinguishes members, and refuse a swapped
value. FABLE named the keys for its four families:

- the getter call at +0x12, for both 70-row families;
- the `lea r8` at +0x14, for the static-descriptor family;
- +0x13 and +0x2B, for the member-vcall family.

For the other families, the reviewers' checkers already identify the varying operands:
`Tools/work/SWE2-AUDIT-SPEC/w10/scratch_kk/`, `scratch_mm/` and `scratch_nn/` (`chk.py`).

Until then, each package README's engine_explained sentence should not claim credit. FABLE's four REVIEW records give
the exact replacement wording.

## SWE2-AUDIT-SPEC limits

This record changes no row and no score. It records a crediting condition that the earlier ACCEPT records did not
state.
