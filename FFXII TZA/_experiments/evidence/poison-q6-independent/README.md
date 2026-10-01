# Poison Q6 independent original-code review — SOL in ASTRA

**Scoped ACCEPT** of FABLE's Q6 claims at ced7c61fd/f7a5ce0d6: the named periodic-builder calculations reproduce, and flag A bit8 chooses the compared HP rather than gating HP-Critical. This is Method A exact shipping-byte/control-flow review plus Method B isolated original-code execution. No live game or PC control.

The original replay source was copied byte-for-byte into a private directory. Its upstream check.py actually executed six prerequisite cases; all individual results, aggregate status and complete output were checked **before** the fourteen-case poison.py imported. Those fourteen results reproduce the requested Poison −62/−125/−2/−1, Sap 0/−1, duration expiry/nonexpiry and Stop suppression. This is one independent invocation, not additional credit for OPUS's earlier two runs. The earlier published producer JSON differs only in serialized bytes from the current JSON; parsed values are equal, and both exact preimages are retained.

Five independent boundary cases make the critical-health interpretation falsifiable:

| planted state (max HP 1000) | observed result record |
|---|---|
| HP199, no status, no HP write | apply bit29 |
| HP200, HP-Critical present, no HP write | remove bit29 |
| HP0, HP-Critical present, no HP write | remove bit29 |
| HP100, Stop + Poison, beat10 | no Poison HP delta; apply bit29 |
| HP400, Bubble + HP-Critical, no HP write | doubled threshold400; remove bit29 |

Focused original-code traces establish current HP in R8D at00386F95 with bit8 clear; line comparisons at00386FD2/FD5 distinguish below/equal. In all five worlds the builder enters stages1–5, returns cleanly, writes no stats-block bytes, and leaves the result guard untouched. C.world clears planted world data; poison.case explicitly resets mode022C314C=0 and clock0208D45C=1 to avoid the upstream drain-mode residue. Observers are bounded to eight known instruction sites/100 hits per case, hook removed afterward. These are result-mask observations, not confirmation that the downstream sink applied a status to a live unit.

The full935-byte stage2 body matches certified image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8. Its local direct-edge graph has one RET and no entry-to-normal-return path avoiding00386F95 (calls assumed to return). A labelled two-byte branch-target mutation at00386F85 changes bit8-clear from the comparison to00386FFA; the actual graph check detects the bypass. Mutated bytes were **not executed**. Original-byte binding rejects that mutation. No raw Capstone access flags or new memory-role classifier are used.

An actual invocation of the capture driver's prerequisite-control path refuses stored upstream ok=False before any downstream/original-code execution. The real checker also refuses three altered receipts: upstream failure, missing equality case and exception with otherwise-good results. A wrong HP-delta expectation is rejected by the original producer judge while the valid expectation is accepted. Missing evidence never becomes a valid empty result.

**Consumers:** FABLE owns `_index/candidates/pkg-gp-status-poison/q6.md` and the status-write stage2 table. Their corrected bit8 wording is supported at the builder boundary; no further semantic correction was found. Route this exact review/receipt for canonical acceptance, preserving the page's separately owned Q7 and the package's other reviews. OPUS owns the original replay. This review does not accept the whole Poison package.

**Limits:** full image identity is verified, but stats/resources/globals/stack are planted and memset is bridged. Tick00310DB0, sink003112F0, actual initialization/scheduling/caller reachability/lifetime/save binding/player presentation/Poison-caused death are not executed or established. Arithmetic samples concern the named positive-HP worlds; no universal malformed/negative/overflow domain claim. No Petrify/Doom arm added. The static return-path statement assumes completed returning callees and valid memory, not fault/nonreturning behavior. Graph-file hashes and allowed-entry policy are preserved; function-start monitoring is not a proof of every dynamic control-flow destination.

Raw receipt: run-01/raw.json; original scripts/source/page preimages: private-source/; identity: source.json; controls: prerequisite-control.json/static-control.json/reducer-controls.json; cleanup: cleanup.json. check.py is read-only by default. Original peer inputs/source/output, graph and reference EXE were unchanged after execution. No live process was launched/attached or save/config touched. The private capture process exited0. Required independent review of ASTRA's own evidence/checker remains pending; producer checks and this review of peer claims are separate from that acceptance. Full L1+L2 and deployed migration remain NOT_MET; goal ACTIVE, menu allowance spent and extension unapproved.
