# Leader capability-policy falsification

ASTRA, 2026-09-12. This package answers FABLE-REQ-ASTRA-CAP-FALSIFY with
counterexamples and corrections, not an AUDITED promotion. Canonical interpretation
is in [capability policy §11](../../../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md).

Claim/hypotheses: test the polarity of `0209A2C5`, whether Immobilize preserves
permission unconditionally, event-predicate membership, and the scope of combo,
incapacity and unit-flag suppression. Existing evidence was FABLE's static reading
of `0023B040` and small event/permit helpers. Distinguishing observations are actual
output bytes, branch reachability, and movement writes when conditions compete.

Method A uses 30 complete contiguous disassemblies of the shipping executable:
`primary.json`, `callees.json`, `state.json`, `outputs.json`, `leaves.json`,
`save-base.json`. Each records body address, length, bytes, SHA-256 and instructions.
The reference EXE SHA-256 is
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred image base `0x120000`. Capstone 5.0.7 and the exact function-extent source
hash are recorded in each receipt. `004235C0` is completely read but its deeper
resource callees are outside this package, so its full semantics remain open.

Method B reuses the established Unicorn 2.1.4/PE instrument on Python 3.14.6.
`probe.py` maps verified shipping bodies at their original addresses in the emulator,
not in the live process. It injects all data, a Windows x64 entry stack with shadow
space and alignment, and saved nonvolatile GPR/XMM values. It checks every reached
instruction against the collected bodies, bounds execution to 30,000 instructions
per case, records all non-stack reads/writes, records invalid accesses, verifies
unchanged code and return/stack/nonvolatile state, and banks each case before assertions.
No body is replaced and there are no callee stubs. Four floating-point constants
are copied from the exact reference binary; all other data are controlled state.

The initial healthy/Immobilize feasibility pair is preserved in `feasibility.json`.
It proved real output and requested-movement writes before the final bounded run.
`result.json` includes 24 valid full-entry cases, 116 event-predicate cases covering
every value in each bitmap's finite candidate range plus adjacent/extreme controls,
five ECX-width/Boolean setter cases, and one deliberately invalid null-status case.
That last case faults before publication and is not a successful return or a claim
about reachable gameplay. No invalid/incomplete run is reported as passing.

`review.py` independently reconstructs initial memory and replays all 1,866 reads
and 147 writes, checks every observed final buffer and the exact native output/movement
write order, and requires the expected nonzero case set. Its negative control deletes
one requested-speed write from a private receipt while retaining return/ABI flags;
review rejects it. This is an evidence-reader mutation, not a mutation of the game or
a substitute for the repository's final mutation campaign. `review.json` records the
raw result hash and the 29 reached body entries. Historical mutation evidence is untouched.

Important boundaries: mode and status data are injected; actual engine initialization,
scheduling and gameplay reachability are not established. Render `+C8 = -1` selects
the native direct `+CC` return; `004235C0` does not execute. The movement actor has
class bits `0x60` and connected movement/adapter records. The separate mask-1
aggregate bit-0 callback branch is not exercised. Other actor classes and native
presentation effects must not be inferred from this run.

Reproduction: from the repository root, use the existing analysis Python environment
to run the six `cap_policy_*.py` collectors in this directory; their defaults populate
the established `Database/Tools/work/ASTRA/cap-policy-*.json` inputs. Run
`probe.py --feasibility` first, preserve its result, then run `probe.py` and `review.py`.
The emulator library requires the existing scoped filesystem access on this host;
no live-game access is required. A changed reference hash, missing callee, failed
control, unexpected instruction or ABI/effect discrepancy stops the relevant case.
This package does not resume controls after the user's exit-and-cleanup authorization.

`manifest.json` seals all package files except itself. The pre-correction page bytes
had SHA-256 `28e1f51bdd6d3cfa3b4ea78c66596e718cdb678489ffb31fa4188e6e66469a53`;
the source request identifies FABLE commit `4da6ff0`. The correction history remains
in the canonical page, the board transactions and ASTRA's handoff.
