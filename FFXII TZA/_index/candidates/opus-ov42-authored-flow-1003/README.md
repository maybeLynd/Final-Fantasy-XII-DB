# The shipped getspattackskillinfo -> spattackread flow placed against the two-out-reference precondition (OPUS, 2026-10-03)

Request: `ASTRA-REQ-OPUS-OV42-AUTHORED-FLOW-CONSUME-1003`. The request asks OPUS to consume two records:
- SWE2-DATA's original [`swe2data-ov42-authored-spattack-flow-1003`](../swe2data-ov42-authored-spattack-flow-1003/README.md)
  (`c77a50981`);
- SWE2-AUDIT-SPEC's independent [review](../auditspec-review-swe2data-ov42-authored-spattack-flow-1003/REVIEW.md)
  (`c5f35fc3c`, ACCEPT).

The owning OPUS page is the [calling-convention page](../../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md).
Its "Two out-references: the destination precondition" section (d98208c6e) states the contract the flow is measured
against.

## What changed

The calling-convention page gains one OPUS section, "The shipped 029A -> 029B flow against that precondition":
- the bridge pop order (029A: first pop to RDX, the action destination; second pop to RCX, the unit destination;
  029B: EDX then ECX);
- the file-class cells and their 4-byte, byte-disjoint outputs;
- the loop path as H1 under named premises;
- the init path as H2, cannot establish;
- the four residual propositions kept OPEN word for word in substance: initial queue order, native cell writers,
  allocation / non-alias / lifetime, and action word 0.

## Verified

- [`flow_check.py`](flow_check.py) re-reads both bridges and the class-1 decoder arm at the shipping image: 16 checks,
  FAILS 0 ([`flow_check.out`](flow_check.out)).
- The script-side facts (the three call sites, the descriptors, the bytecode of both flows) are taken from SWE2-DATA's
  `prove_spattack_flow.py` (34 checks, 6 controls) and the reviewer's independent decode of all nine copies. Per the
  request, they are not re-run here.
- [`apply_flow.py`](apply_flow.py) is idempotent ([`apply_flow.out`](apply_flow.out)).
- Gates on the page: `check_links` 0, `check_consistency` 0 naming it, `verify_doc_addresses` 0 REVIEW. `nb_page`
  adds nothing.

## Not claimed

- No natural command execution is inferred.
- No absence claim rests on the discovery census.
- The incorporation stays ACTIVE on ASTRA's side until ASTRA's canonical consumer receipts, as the request states.
