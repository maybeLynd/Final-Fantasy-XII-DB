# Interior citations, cloud-drafted: the-map-ctrl-pack.md's entry-cited functions (FABLE, 2026-10-03)

The page named 31 F-frontier functions only at their entry. A Claude Code cloud session (https://claude.ai/code/session_01GLiazqTkiTNo2qTSeFb6Kg, on FABLE's own cloud credit) drafted one sentence and 1-5 interior anchors per function from FABLE's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo, OPUS's listing code). FABLE checked every row mechanically with `fable_ingest.py` (OPUS's interior_ingest checks) and re-read every sentence against the listing before staging.

**Rows.** 31 staged with 143 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**FABLE corrections on re-read.**

- `0035DAF0`: 0035DC05/0035DC0D load .data (mutable) dwords 01E0C1DC/01E0C1D8; their initial values 0x1C0/0x200 were stated as fixed words
- `002A1D40`: neighbour gate (2026-10-03): the callback address 002A1FB0 named by entry imports its callee 00253690 (Rewards_Progression_Economy), 1 unaccounted edge on the-map-ctrl-pack.md; the pointer is now cited by the instruction that loads it (`lea rdx` at 002A1D80, added as an anchor), and the documented callee 00244F50 stays named by address
- `002A1EB0`: neighbour gate (2026-10-03): the callback address 002A1FB0 named by entry imports its callee 00253690 (Rewards_Progression_Economy), 1 unaccounted edge on the-map-ctrl-pack.md; the pointer is now cited by the instruction that loads it (`lea rdx` at 002A1EF5, added as an anchor), and the documented callee 00244F50 stays named by address
- `002A7E20`: neighbour gate (2026-10-03): the callback address 002A1FB0 named by entry imports its callee 00253690 (Rewards_Progression_Economy), 1 unaccounted edge on the-map-ctrl-pack.md; the pointer is now cited by the instruction that loads it (`lea rdx` at 002A7E60, added as an anchor), and the documented callee 00244F50 stays named by address

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first: every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent). The section is appended at publish time; the publish gates (address, neighbours, correction) run on the result.

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is FABLE's re-read. The session's agreement with FABLE is not independent review; SWE2-AUDIT-SPEC spot-checks.
