# HP floor/cap invariant — focused falsification

Claim: CONTRACT-hp-write-and-lethal-transition.md §4 asserts floor<=HP<=cap after
any storing call with only a stats record as precondition; it says the bound also
survives the separately qualified second store. The implementing HP page says
HP cannot fall below floor or exceed cap. Consumer: OPUS contract, FABLE mechanism.

Hypotheses: the original clamp enforces both bounds even if inconsistent;
it prioritises floor on one branch and cap on another, requiring floor<=cap;
or a native floor setter rejects such inconsistent supplied values.

Method A is sufficient. Read the complete current HP function and floor setter,
verify precise comparisons/jump/convergence, and retain existing EXP093 controls.
Use a few symbolic branch witnesses to illustrate the derived path; these are not
new original-code execution and not a reconstructed implementation proving itself.
B adds no necessary discriminator to these plain finite comparisons. C is needed
only for ordinary script/runtime occurrence, downstream callbacks and consequences.

Controls: ordered floor20/cap50, old50 plus delta-40 or+100 gives20/50. Inconsistent
floor80/cap50 with old50/delta0 selects80; delta100 selects50. Same finite nonnegative
inputs otherwise; statuses0, no integer overflow, admitted main write assumed.
Do not infer death from a numeric HP write or claim these inputs occur in shipped play.

Acceptance: verified binary hash and original bytes, full RET boundary not a first
fragment, exact floor producer/load and branch trace with no hidden second test.
Preserve old EXP093/mutations untouched and specify limits/affected claims. No
general audit campaign. Reject incomplete/zero-case/changed-source inputs.

Cleanup: read-only shipping binary and retained artifacts. No FF12, PC control,
input, save/config/reference edits or new live restoration receipt. Preserve live
permission and persistent spent S19 setup budget. Goal remains accepted whole L1+L2.
