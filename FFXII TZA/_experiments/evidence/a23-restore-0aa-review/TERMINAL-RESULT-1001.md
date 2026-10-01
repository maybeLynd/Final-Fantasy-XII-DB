# Scoped MP16 acceptance; restore counterexample remains a rejection

Exact historical requirements.py from commit
0aa544606e35de0b2f6056b0af469fa048d7fe8a, SHA
b47e084f994abcfdb12a4edb43088934b118eff241d33d002e5e6ac5438a2d84.
The required git-show exited 0, produced 39,374 bytes and no stderr. The current
checkout differs even after line-ending normalization; this is not current
deployment acceptance. Generation.py remains separately pinned c165172d.

Independent driver exit 0, no stderr, 99/99 complete cases: 76 counter/gate
combinations, 16 invalid supplied requirements, two protocol-default cases,
three missing/malformed terminal inputs and two absent-acceptance controls.
Actual terminal_facts/terminal_observed and public measure ran without producer
test import or mocked functions. The public measure read real owned TSV/JSON
fixtures. Full inputs, expected values, outputs and exceptions are retained.

For a valid thirty-pass requirement, accepted T is always all thirty or none.
Every partial integer counter 1..29 leaves unaccepted T at 0/30 and contributes
zero to accepted union; it appears only in terminal_observed. An authoritative
accepted-gate fixture selects all thirty regardless of that reporter counter.
Counter 30 alone does not accept T. Counter -1/0/30/31 and malformed counter
types do not become observed partial progress. Invalid supplied requirements
refuse through both helper and public paths: failed T, accepted None, required
30, UNMEASURED and NOT READY. This differs from valid unaccepted T (30 facts,
accepted 0). Missing required_consecutive uses the fixed protocol constant.

Two actual driver invocations also refused a missing and corrupt source before
result creation. Their nonzero exits/stderr and missing outputs are controls,
not passing experiments with zero cases. No original restore sample repeated.

**ACCEPT this bounded MP16 adapter subclaim for exact 0aa.** Overall existing
OPUS review is **REJECT**, because retained Windows restore admits ASTRA-alias
and ASTRA-alias. as one physical file while returning success, setting CURRENT
and reporting a clean ordinary reader. The original five pkg: repair stays
accepted at its tested scope; string injectivity does not prove physical
filesystem uniqueness. Preserve those separate conclusions in OPUS's repair.

Limits: gate fixtures do not validate real audit receipts, ancestry/drift,
preconditions, rejected/ended run presentation, current/deployed source,
rendered browser behavior or full M0-M5. This test alone does not certify a
terminal run or database completion. No FF12 evidence of any kind was acquired.
Retained archive-input qualification is read-only, not another restore run.
Raw ZIP bodies stay at their pinned retained paths; repository ZIP ignore
prevents publication as ordinary paths. The additive published index supplies
exact archive/member hashes and manifests, and drivers require the pinned
retained archive/base. An absent archive must be INCOMPLETE, never substituted.
Original results and cleanup receipts remain immutable; all own children ended.
