# Interior citations, cloud-drafted: the-msvc-ordered-container-runtime.md's entry-cited functions (OPUS, 2026-10-03)

The page named 8 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py`. A second local agent, not the drafter, then read every one of the 7 rows against the disassembly, including the rotation helpers' directions and every named import: all 7 stood. Neither agent is an independent reviewer: the non-author check is SWE2-AUDIT-SPEC's.

**Rows.** 7 applied with 35 anchors. Rejected by the mechanical check: 0. Skipped by the session: 1. Missing: 0.

**Corrections from the byte re-read.**

- none needed

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 7 rowed functions now measure A under the base rule. Five of them (`00712F60`, `00714DC0`, `0071E500`, `0071F590`, `0079BA10`) are members of the family `MSVC ordered-container (std::_Tree) runtime` that this page declares; they credit only because that family has no committed family checker (`fam_rows.py` + `spec.json` + `rows.tsv`) on this page and so is outside the family-declaring-page rule's scope. `interior_applier.py` is not such a checker: if the family is brought into scope, these five rows credit nothing until each member has a checker row. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 2), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
