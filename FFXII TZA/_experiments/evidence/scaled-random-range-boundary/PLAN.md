# Strict scaled-random range versus binary32 boundaries

Question/consumer: rng-streams.md states the original scaled helper's value lies
in [0,A). Does that hold for every positive finite binary32 amplitude, even with
the correct multiply-then-subtract expression? FABLE numeric prose, OPUS exact
contract/domain are ready consumers. The order question is already settled;
this is a separate range/precondition question.

H1: for finite A>0 and sample in [1,2), the observed original window always
produces finite0<=out<A. H2: rounding can reach A for tiny positive inputs, or
masked product overflow can produce infinity for large finite inputs.

Method B: exact floating results/flags-mode effects justify the retained original
58B arithmetic window, with controlled memory/ABI/MXCSR. Existing validated
capture/observer reused; no new runtime platform or live setup. A identifies the
order and absence of clamps, but a host prediction is not original execution.
C is unnecessary; normal callers, sample reachability, initialization and actual
game MXCSR stay open. No paired full-function/native-callback effects are claimed.

Prepared discriminator: injected sample3FFFFFFF (largest binary32 below2),
amplitudes00000001 (smallest positive subnormal),3F000000 (0.5f normal control),
7F7FFFFF (largest positive finite). MXCSR1F80 requests nearest rounding, masked
exceptions, no DAZ/FTZ. Retain actual register/stack/constant preimages, raw
instruction/read/write events and output bits. Host preflight predicts endpoint
for subnormal and strict interior for normal; retain it only as prediction.

Positive/detection controls: unchanged exact original bytes and shipping1.0;
normal amplitude/sample case exercises same stores; SUBSS->ADDSS fixture mutant
on that normal case must change the stored output and fail the original result
predicate. New boundary cases, no re-execution of the old0.3f/order discriminator.

Budget: 64 instructions per window, exact entry3D8F3F/stop3D8F79. Acceptance:
all required cases complete, full code/stop/state/constant/write controls pass,
normal detector discriminates; report exact bits and conditional range only.
Invalidation: identity mismatch, fault/incomplete/zero cases, changed inputs,
undiscriminating detector, or unsupported emulator semantics. Preserve failures;
revise method rather than blindly repeat. Do not equate emulator status flags
with real CPU/live exception behavior without independent support.

Restore: disposable emulator instances, no FF12 process, PC controls, saves,
configuration or reference writes. Pin Python/modules/exact DLLs before capture
(lesson from23's disclosed late DLL supplement); preserve inputs/results once.
Route owner/reviewer only once, then publish and take a different eligible claim.

Learned correction: first3D8F44 store is amplitude loaded by MOVSXD3D8F3F,
not sample. An added first-store sample check failed; preserve v1 as provisional.
Reused observer is augmented only with direct initial XMM1/RSP/MXCSR reads;
separate sample and amplitude predicates provide the smallest regression.
Rerun affected boundaries/control with this changed instrument, not unchanged
setup or old0.3f cases. Preserve old23's missing direct-register receipt as a
review limit; it is not a new live or initialization result.
