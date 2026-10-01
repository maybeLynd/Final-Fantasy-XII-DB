# Scaled procedural random: exact binary32 operation order

Claim: rng-streams.md describes A*(sample-1); shipping3D8E50 performs
f32(f32(A*sample)-f32(A*one)). Competing explanation: factored expression is
equivalent for the relevant finite binary32 inputs, versus observable rounding
difference. Existing authored-integer sibling arithmetic is not this body.

Method B: execute only the verified original58-byte window003D8F3F..003D8F78 in
the existing Unicorn/reader environment. Inject finite amplitude at RSP+30,
sample in XMM1, valid disposable scratch and shipping1.0 at01EF93FC; fixed
MXCSR1F80. Native save/restore and recurrence initialization are omitted, not
stubbed as evidence of their effects. This is isolated original code, not live.

Small feasibility/control first. Host-source prediction seed458DC800/sample
3FB90003/A3E99999A agrees under both formulas: NONDISCRIMINATING, no capture or
replay of prior original recurrence. Seed45848000 gives sample3F900001 and
predicts original3D1999A0 versus factored3D1999A4. These host calculations are
experiment selection, not original behavior proof. Injected sample is a fixture,
not a claim of live initialization/reachability.

Controls: full shipping418B/retainedmanifest and58B identity; normal baseline
A=0.3; exactly representable power-of-two baseline; output and scratch write PCs
and before/after; instruction budget/entry/stop/RSP checks; smallest alternate
operation-order control must distinguish the preferred formula. Failure to reach
stop, unexpected instruction/write, non-discriminating only or identity mismatch
invalidates the run. Do not cycle identical controls or broaden to native effects.

Acceptance: original instruction result distinguishes formulas with exact raw
bits; independent consumer/review required. Persist reusable entry/MXCSR/sample
preconditions and the failed common-seed discriminator. No universal amplitude,
all rounding modes, caller timing or live rendering guarantee.

Cleanup: emulator object disposable; no process/PC/save/config/reference writes.
Consumers: FABLE rng-streams formula and OPUS exact numeric contract. Full
database L1+L2 goal NOT_MET, no L3 phase or new live setup.
