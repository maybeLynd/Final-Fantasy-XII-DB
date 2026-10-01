# Exact retained-source discriminator: rendering flag stores versus actor kind

Question: which address overlap can let the selected original3E33E0/3E3440
DWORD store change the actor header byte3 highE0 bits? Does excluding all
overlap unnecessarily strengthen the preservation precondition?

H1: any overlap may change the kind. H2: the exact touched bit positions
permit preservation on most/all overlap placements; one narrow alias may
still affect kind. A whole class-stability claim remains out of scope.

Method A is sufficient: reuse canonical raw-object-state and its original
21B/19B snippets plus raw-position-effects/2E6000's original byte3/E0 gate.
Re-decode bytes with the shared reviewed access adapter. Derive the actual
shift/XOR/mask/XOR/dirty-bit formulas, preserve independent d0/d1 reads,
then prove bit invariants through all eight Boolean input assignments per
bit. These are algebraic cases, not native executions or game samples.

All possible non-wrapping DWORD placements covering actor+3 areF=A+q for
q0..3. Map the class mask into each placement; distinguish an unconditional
changed-bit exclusion from actual memory nonaliasing or synchronization.
Do not assume aligned initialized objects. If alignment helps, state it
as a premise and leave its native initialization proof to the owner.

Required controls: actual original valid input; failed retained prerequisite
exit; actual wrong memory-store role; coherent changed original mask and a
missing class-gate input. No missing/zero-case source can pass. Original
catalogue-only extent labels remain; do not invent unwind roots or prove
all function entries/callers. Published raw/case/result inputs stay immutable.

Acceptance: exact per-store mask/geometry invariant or a source-backed
counterexample, including sequential-read limits. FABLE/OPUS consume only
after independent review. Other native callbacks, class lifetime, actual
alias/reuse, scheduling and full CON-172 remain open. No FF12/native/emulated
execution, new observer framework, fixture-level native effect or live ratio.

Existing6B/R13 ABI8969fe745 is already SPECcd86f404d accepted and OPUSc4eb91ad3
incorporated. Do not republish/retest it. User full L1+L2 goal ACTIVE/NOT_MET;
menu branch spent/unapproved, EXP127 invalid. Use original retained data.
