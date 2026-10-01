# Music control page-boundary seam

Claim/hypotheses: MC-5 rebase covers all page words consumable by the inclusive maxFieldId reader, versus an exact128 boundary admitting a final page that the callback never visits.

Known evidence: current contracts identify inclusive upper bound, page index arg/128 and rebase rounded count; shipped max1311 works. EXP099 executes real reader/progress getter but explicitly excludes loader and plants absolute page pointers. It cannot establish their production coverage.

Method A sufficient: verify complete original71-byte callback003EAB90 and229-byte reader003EAA70, re-derive exact signed32 arithmetic/write-loop count and inclusive gate; inspect retained EXP099 fixture/result without replay. Five nonnegative header witnesses0/127/128/129/1311 distinguish exact boundary from adjacent and shipped control. These are static calculations, not experimental input cases. No native/PC/game setup.

Acceptance: exact bytes/entry/branches/operand widths and source-producer order retained; count/read-page comparison differentiated; corrupted derivation or zero source rejected. Preserve zero-offset skip and source/input domain. No claim that a shipped packet uses the boundary or game faults. No lifetime/free/caller-frequency assertion.

Consumers FABLE mechanism and OPUS musicctrl/field-selection contracts, independent SPEC review then owner adjudication. Explicit end-to-end producer limitation in existing fixture where relevant. Existing native22/20 results not retracted or rerun. Saves/config/reference unchanged, PC remains OFF. Runtime stop-loss permission unaffected.
