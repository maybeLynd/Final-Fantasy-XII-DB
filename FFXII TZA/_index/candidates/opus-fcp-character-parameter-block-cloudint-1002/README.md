# Interior citations, cloud-drafted: fcp-character-parameter-block.md's entry-cited functions (OPUS, 2026-10-02)

The page named 22 F-frontier functions only at their entry. A Claude Code cloud session (session_01XRXP3rS6fx4VxurArNZ8tP) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 22 applied with 98 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `0051CDE0`: wrong loop scope: the 02AEC2D0 template is copied once before the record loop, not per record; an unstated branch (001EDDA0 gate on 00861F5C); ambiguous bit naming
- `00425E10`: ambiguous bit naming: `bit 0x2` reads as bit 2; the test is mask 0x2 = bit 1

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 22 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 4 (the pre-existing four), `verify_doc_addresses --all` 0 documents to confirm.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.

**Pass-22 neighbours (2026-10-02, OPUS).** The new rows re-keyed the page's existing Party finding. `check_publish_neighbours.py` counts a re-keyed finding as added, so the guard refused it. The page never named the Party layer, so its crossing section now carries a Party CLIENT and SERVICE bullet with the four call sites read (`00358A20+0x29`, `00304180+0xB2`, `003045A0+0x18`, `0046CC70+0xEF`). The Party and Spawn findings are now accounted for: `nb_page.py` shows 7 and 3 hits at HEAD, and 0 now.
