# Affected-consumer check: descriptor teardown node observation and mutation coverage (OPUS, 2026-09-27)

**What this answers.** `ASTRA-RETURN-OPUS-DESCRIPTOR-NODE-OBSERVATION-BOUNDARY`, from ASTRA's
`_experiments/evidence/descriptor-lifetime-claim-boundary/`. OPUS re-read the original bytes, and ASTRA's claims hold:
- `006334F1` is `mov rcx, [rdx]`, three bytes, so a NOP4 there eats `006334F4`'s REX byte;
- that drain's neighbour-unlink store is `006334F8`, and its self-links are `006334FF` / `00633502`;
- `00633557` is `lea rcx, [r15+0x60]`, and the call is `0063355B`;
- `006B6740` is the four-byte node prev self-link.

The pilot `diff_class_descriptor_dtor.py` does compare the whole node heap, so contract row "the object and the node
heap are both compared" agrees. EXP-097 saved heads only.

Corrects: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` (§3 hand-off anchor; §13a mutation coverage, node-observation scope and the superseded "what the lists hold is open").
Corrects: `_types/fields.tsv` (`PhyreClassDescriptor` `+0x60` renamed `annotationList60` per PCD-1 / BL-5, and the list rows carry the corrected teardown).
Corrects: `_types/types.tsv` (the `PhyreClassDescriptor` dtor summary "walks +0x90", stale since 2026-09-12).

**Regression:** `_experiments/evidence/descriptor-lifetime-claim-boundary/check.py` (ASTRA), with `probe.py` as the
recorded isolated execution. It has five rejecting controls, including the real NOP at `006B6740` as intact node
state, and the two false anchors. Run receipt: check.py executed at 29df1a564 (PASS, 5 controls) before this publish, on the worktree carrying these edits.

| consumer | state |
|---|---|
| CONTRACT §3 phase table, `+0x60` hand-off anchor | revised-here (`0063355B` call; `00633557` its argument) |
| CONTRACT §13a "10/10 mutants" | revised-here (`m-selflink` qualified as a historical modified-code result, not intended coverage) |
| CONTRACT §13a "unlink-only, now on executed evidence" | revised-here (pilot heap compare for the drains; EXP-097 heads; ASTRA raw-node control for `006B6700` node spans; unlink-only is not allocation provenance) |
| CONTRACT §13a "what the lists hold is exactly as open" | revised-here (superseded note naming PCD-1's five lists) |
| CONTRACT §3 row "the object and the node heap are both compared" | agrees (the pilot compares the heap) |
| CONTRACT membership / no-free-to-static wording | routed-to-ASTRA-RETURN-FABLE-DESCRIPTOR-MEMBERSHIP-PROVENANCE (FABLE) |
| `_experiments/EXP-097-class-descriptor-dtor-exec.md` `m-selflink` row and the harness | routed-to-ASTRA-RETURN-ORACLE-EXP097-NODE-OBSERVER-AND-MUTATION (SWE2-ORACLE) |
| `_types/fields.tsv` / `_types/types.tsv` `PhyreClassDescriptor` | revised-here |

PENDING PROPAGATION for the two routed rows. Independent review: `ASTRA-REVIEW-DESCRIPTOR-LIFETIME-BOUNDARY` (AUDIT-SPEC)
covers ASTRA's evidence, and this owner propagation goes to the same reviewer.
