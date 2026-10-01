# Positive finite amplitude alone does not establish a strict result range

**PASS_ORIGINAL_RANGE_WINDOW — method B, isolated verified instructions.**
This answers a distinct numeric-domain question after the operation-order finding;
the old0.3f/order discriminator was not rerun.

The RNG page, including its current working correction, states the scaled helper
produces values in [0,A). Under the controlled inputs below, the original
arithmetic window does not satisfy that claim for every positive finite A.

| Injected A, sample3FFFFFFF, MXCSR1F80 | Original observed output bits | Meaning |
|---|---|---|
| 00000001, smallest positive subnormal | 00000001 | output=A; strict upper bound fails |
| 3F000000, 0.5f | 3EFFFFFE | ordinary control stays strictly below A |
| 7F7FFFFF, largest positive finite | 7F800000 | +infinity; finite range fails |

OriginalMULSS3D8F52 multiplies sample by amplitude, MULSS3D8F5D separately
multiplies amplitude by mapped shipping1.0, SUBSS3D8F6D subtracts the rounded
products, and3D8F71 stores the result. For the subnormal case the product rounds
to twice the amplitude before subtraction. For the largest-finite case the
product overflows under the masked-exception control. Those explanations are
source/IEEE interpretations of the observed bits, not native CPU status/exception
measurements. A host preflight and host predictions are labelled as predictions.

**Reference:** shipping executable SHA
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000. Complete418B3D8E50 parent source SHA
32f4c93324e6c153518b5b42e85597f75495de8f66171fd58daf355e7b9a063a,
committed in0bcc3d620. Executed unchanged58B3D8F3F..3D8F78 SHA
f35064469004fa9448432dd22dc7c46767058dbb4c833ab86c8063ea4bc3cdd8;
stop3D8F79, max64 instructions per case. No native calls occur inside the window.

**Instrument reuse/state/control:** retain and hash the prior observer function
unchanged, extract only that function rather than re-executing the old capture.
Python/modules/exact loaded DLLs are hashed **before** this capture and checked
unchanged afterward. The source parent/manifest, shipping reader/body/1.0 and
consumer preimage are retained. Inputs include mapped scratch/stack, amplitude,
sample and MXCSR. Raw events contain every executed PC, memory reads, provider
write pieces, normalized writes, register output, before/after memory and stop.
The original first eight-byte store witnesses sample bits before arithmetic;
actual MXCSR control bits are read after the window, which contains no LDMXCSR.
Amplitude/constant preimages remain unchanged and register/output-store bits agree.

The normal detector changes SUBSS to ADDSS only in a disposable fixture. It
produces3FC00000 instead of3EFFFFFE, changes the observed last store, and fails
the original-result predicate. Three unchanged original windows and that one
explicit mutant complete. Missing/faulted/incomplete/zero cases do not pass.
Inputs, raw results and validation are retained; frozen checking only compares.

**Implication:** positive finite amplitude and a mathematical sample in [1,2)
alone do not justify a universal strict/finite binary32 result range. Preserve
the original operation order and attach an evidence-backed input/FP-state domain
to any stronger bound. This packet does not derive the complete safe domain or
invent an exclusion to make the old claim true. The normal control is one case,
not a proof for all normal amplitudes.

**Limits:** sample and amplitude boundaries are injected. This does not establish
their normal recurrence/caller reachability, real game MXCSR, initialization,
native save/restore/full-function return, rendering or effects of unmasked
exceptions/DAZ/FTZ. It is emulator original-instruction evidence, not a live game
or a reconstructed implementation agreeing with its own fixture. Neither the
emulator's status bits nor live IEEE behavior are promoted without support.

**Consumers:** FABLE RNG prose/table and OPUS exact numeric contract/preconditions;
independent SPEC review is required. Universal range and consumer closure stay
pending until their scoped corrections are accepted. No game/PC control, process
attachment, save/config/reference write or live cleanup was involved.

**Player version:** extreme modded values can hit the advertised upper limit or
produce infinity. The database needs an input-domain qualifier; this is not an
observed normal-game failure.
